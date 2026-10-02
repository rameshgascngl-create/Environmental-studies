#!/usr/bin/env python3
"""Audit releaseQa AndroidTest dex closure without external Python packages.

Collects every class descriptor referenced by the instrumentation APK under
kotlin/, kotlinx/, and androidx/test/, compares that set with classes defined
in the minified app APK, and emits exact QA-only keep rules.

This script intentionally does not modify application source or production
R8 rules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zipfile
from pathlib import Path

PREFIXES = ("Lkotlin/", "Lkotlinx/", "Landroidx/test/")


def u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


def read_uleb128(data: bytes, off: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        b = data[off]
        off += 1
        value |= (b & 0x7F) << shift
        if b < 0x80:
            return value, off
        shift += 7
        if shift > 35:
            raise ValueError("invalid ULEB128")


def read_dex_string(data: bytes, off: int) -> str:
    _, pos = read_uleb128(data, off)
    end = data.find(b"\x00", pos)
    if end < 0:
        raise ValueError("unterminated dex string")
    # Class descriptors are ASCII-compatible. Replacement is deliberate for
    # unrelated MUTF-8 strings that are never used as descriptors here.
    return data[pos:end].decode("utf-8", errors="replace")


def normalize_class_descriptor(desc: str) -> str | None:
    while desc.startswith("["):
        desc = desc[1:]
    if desc.startswith("L") and desc.endswith(";"):
        return desc
    return None


def parse_dex(data: bytes) -> tuple[set[str], set[str], set[str]]:
    if len(data) < 0x70 or not data.startswith(b"dex\n"):
        raise ValueError("not a dex file")

    string_ids_size = u32(data, 0x38)
    string_ids_off = u32(data, 0x3C)
    type_ids_size = u32(data, 0x40)
    type_ids_off = u32(data, 0x44)
    class_defs_size = u32(data, 0x60)
    class_defs_off = u32(data, 0x64)

    strings: list[str] = []
    for i in range(string_ids_size):
        string_data_off = u32(data, string_ids_off + i * 4)
        strings.append(read_dex_string(data, string_data_off))

    types: list[str] = []
    for i in range(type_ids_size):
        descriptor_idx = u32(data, type_ids_off + i * 4)
        types.append(strings[descriptor_idx])

    all_referenced: set[str] = set()
    referenced: set[str] = set()
    for desc in types:
        normalized = normalize_class_descriptor(desc)
        if normalized:
            all_referenced.add(normalized)
            if normalized.startswith(PREFIXES):
                referenced.add(normalized)

    defined: set[str] = set()
    for i in range(class_defs_size):
        class_idx = u32(data, class_defs_off + i * 32)
        desc = normalize_class_descriptor(types[class_idx])
        if desc:
            defined.add(desc)

    return all_referenced, referenced, defined


def apk_dex_sets(path: Path) -> tuple[set[str], set[str], set[str], list[dict[str, object]]]:
    all_class_refs: set[str] = set()
    filtered_refs: set[str] = set()
    all_defs: set[str] = set()
    dex_meta: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as zf:
        dex_names = sorted(
            (n for n in zf.namelist() if n.startswith("classes") and n.endswith(".dex")),
            key=lambda n: (0 if n == "classes.dex" else int(n[7:-4])),
        )
        if not dex_names:
            raise SystemExit(f"No classes*.dex found in {path}")
        for name in dex_names:
            data = zf.read(name)
            refs_all, refs_filtered, defs = parse_dex(data)
            all_class_refs |= refs_all
            filtered_refs |= refs_filtered
            all_defs |= defs
            dex_meta.append(
                {
                    "name": name,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data),
                    "allReferencedClassCount": len(refs_all),
                    "filteredReferencedClassCount": len(refs_filtered),
                    "definedClassCount": len(defs),
                }
            )
    return all_class_refs, filtered_refs, all_defs, dex_meta


def java_name(desc: str) -> str:
    assert desc.startswith("L") and desc.endswith(";")
    return desc[1:-1].replace("/", ".")


def write_keep_rules(path: Path, classes: list[str]) -> None:
    lines = [
        "# QA-only AndroidTest R8 rules.",
        "# Generated from releaseQa AndroidTest dex references absent from the minified app dex.",
        "# Production release does not consume this file.",
        "-dontwarn javax.lang.model.element.**",
    ]
    for desc in classes:
        lines.append(f"-keep class {java_name(desc)} {{ *; }}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-apk", required=True, type=Path)
    ap.add_argument("--app-apk", required=True, type=Path)
    ap.add_argument("--json-out", required=True, type=Path)
    ap.add_argument("--missing-out", required=True, type=Path)
    ap.add_argument("--keep-out", required=True, type=Path)
    args = ap.parse_args()

    test_all_refs, test_refs, test_defs, test_dex = apk_dex_sets(args.test_apk)
    _, _, app_defs, app_dex = apk_dex_sets(args.app_apk)

    absent_from_app = sorted(test_refs - app_defs)
    unresolved_combined = sorted(test_refs - app_defs - test_defs)
    unresolved_all_combined = sorted(test_all_refs - app_defs - test_defs)
    defined_in_test_not_app = sorted((test_refs & test_defs) - app_defs)

    args.missing_out.write_text(
        "\n".join(java_name(x) for x in absent_from_app) + ("\n" if absent_from_app else ""),
        encoding="utf-8",
    )
    write_keep_rules(args.keep_out, absent_from_app)

    report = {
        "scope": "releaseQa AndroidTest dex closure",
        "prefixes": ["kotlin/", "kotlinx/", "androidx/test/"],
        "testApk": str(args.test_apk),
        "appApk": str(args.app_apk),
        "testApkSha256": hashlib.sha256(args.test_apk.read_bytes()).hexdigest(),
        "appApkSha256": hashlib.sha256(args.app_apk.read_bytes()).hexdigest(),
        "testDex": test_dex,
        "appDex": app_dex,
        "referencedClassCount": len(test_refs),
        "appDefinedClassCount": len(app_defs),
        "testDefinedClassCount": len(test_defs),
        "absentFromMinifiedAppDexCount": len(absent_from_app),
        "absentFromMinifiedAppDex": [java_name(x) for x in absent_from_app],
        "definedInTestButAbsentFromAppCount": len(defined_in_test_not_app),
        "definedInTestButAbsentFromApp": [java_name(x) for x in defined_in_test_not_app],
        "unresolvedInCombinedRuntimeCount": len(unresolved_combined),
        "unresolvedInCombinedRuntime": [java_name(x) for x in unresolved_combined],
        "unresolvedAllCombinedRuntimeCount": len(unresolved_all_combined),
        "unresolvedAllCombinedRuntime": [java_name(x) for x in unresolved_all_combined],
        "generatedKeepRuleCount": len(absent_from_app),
        "generatedKeepRulesFile": str(args.keep_out),
    }
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"EXACT_KEEP_RULE_COUNT={len(absent_from_app)}")
    print(f"UNRESOLVED_COMBINED_RUNTIME_COUNT={len(unresolved_combined)}")
    print(f"UNRESOLVED_ALL_COMBINED_RUNTIME_COUNT={len(unresolved_all_combined)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
