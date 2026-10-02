#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("--apk", required=True)
parser.add_argument("--aab", required=True)
parser.add_argument("--aapt", required=True)
args = parser.parse_args()

OUT = Path("V245_RELEASE_RESOURCE_INTEGRITY.json")
apk = Path(args.apk)
aab = Path(args.aab)
aapt = Path(args.aapt)
for p in (apk, aab, aapt):
    assert p.is_file(), p

# Resolve release APK resource names to their actual (possibly shortened)
# packaged file paths through resources.arsc.
resource_dump = subprocess.check_output(
    [str(aapt), "dump", "--values", "resources", str(apk)],
    text=True,
    errors="replace",
)

def resource_file_path(kind: str, name: str):
    needle = f":{kind}/{name}:"
    lines = resource_dump.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            needle in line
            and stripped.startswith("resource 0x")
            and not stripped.startswith("spec resource")
        ):
            for nxt in lines[i + 1 : i + 10]:
                m = re.search(r'\(string8\) "([^"]+)"', nxt)
                if m:
                    return m.group(1)
                m = re.search(r'\(string16\) "([^"]+)"', nxt)
                if m:
                    return m.group(1)
    return None

with zipfile.ZipFile(apk) as z:
    apk_entries = set(z.namelist())
    book_apk_path = resource_file_path("raw", "book_content")
    assert book_apk_path, "raw/book_content missing from release APK resources.arsc"
    assert book_apk_path in apk_entries, book_apk_path
    apk_book_bytes = z.read(book_apk_path)

with zipfile.ZipFile(aab) as z:
    aab_entries = set(z.namelist())
    aab_book_path = "base/res/raw/book_content.json"
    assert aab_book_path in aab_entries
    aab_book_bytes = z.read(aab_book_path)

assert apk_book_bytes == aab_book_bytes, "APK/AAB packaged book_content.json differs"
data = json.loads(aab_book_bytes.decode("utf-8"))

refs = {
    block.get("figure", "").strip()
    for unit in data["units"]
    for lesson in unit["lessons"]
    for lang in ("english", "tamil")
    for block in lesson[lang]
    if block.get("kind") in ("figure", "svg_figure") and block.get("figure", "").strip()
}
png = sorted(x for x in refs if x.startswith("fig_"))
svg = sorted(x for x in refs if x.startswith("sci_"))
unexpected = sorted(refs - set(png) - set(svg))
assert len(refs) == 96, len(refs)
assert len(png) == 31, len(png)
assert len(svg) == 65, len(svg)
assert not unexpected, unexpected

apk_missing_table = []
apk_missing_file = []
apk_paths = {}
for name in sorted(refs):
    kind = "drawable" if name.startswith("fig_") else "raw"
    path = resource_file_path(kind, name)
    if path is None:
        apk_missing_table.append(name)
        continue
    apk_paths[name] = path
    if path not in apk_entries:
        apk_missing_file.append({"resource": name, "path": path})

aab_missing_file = []
for name in sorted(refs):
    suffix = name + (".png" if name.startswith("fig_") else ".svg")
    expected = (
        f"base/res/drawable-nodpi/{suffix}"
        if name.startswith("fig_")
        else f"base/res/raw/{suffix}"
    )
    # AGP may include a configuration suffix in the drawable directory.
    present = (
        expected in aab_entries
        or any(
            x.startswith("base/res/drawable") and Path(x).name == suffix
            for x in aab_entries
        )
        if name.startswith("fig_")
        else expected in aab_entries
    )
    if not present:
        aab_missing_file.append(name)

apk_png_resolved = sum(x in apk_paths for x in png)
apk_svg_resolved = sum(x in apk_paths for x in svg)
aab_png_files = sum(
    any(x.startswith("base/res/drawable") and Path(x).name == name + ".png" for x in aab_entries)
    for name in png
)
aab_svg_files = sum(f"base/res/raw/{name}.svg" in aab_entries for name in svg)

assert not apk_missing_table, apk_missing_table
assert not apk_missing_file, apk_missing_file
assert not aab_missing_file, aab_missing_file
assert (apk_png_resolved, apk_svg_resolved) == (31, 65)
assert (aab_png_files, aab_svg_files) == (31, 65)
assert "resources.arsc" in apk_entries
assert "base/resources.pb" in aab_entries

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

report = {
    "scope": "built release artefact figure-resource integrity",
    "expectedNamesSource": "packaged APK/AAB book_content.json",
    "packagedBookContent": {
        "apkResourcePath": book_apk_path,
        "aabResourcePath": aab_book_path,
        "identical": True,
        "sha256": sha256_bytes(apk_book_bytes),
    },
    "expectedUniqueFigures": 96,
    "expectedPngFigures": 31,
    "expectedSvgFigures": 65,
    "apk": {
        "path": str(apk),
        "bytes": apk.stat().st_size,
        "sha256": sha256_file(apk),
        "resourcesArscPresent": True,
        "resourcesArscResolved": {
            "total": len(apk_paths),
            "png": apk_png_resolved,
            "svg": apk_svg_resolved,
        },
        "resolvedFileEntriesPresent": len(apk_paths) - len(apk_missing_file),
        "missingFromResourcesArsc": apk_missing_table,
        "missingResolvedFileEntries": apk_missing_file,
        "resolvedResourcePaths": apk_paths,
    },
    "aab": {
        "path": str(aab),
        "bytes": aab.stat().st_size,
        "sha256": sha256_file(aab),
        "baseResourcesPbPresent": True,
        "baseModuleFileEntriesPresent": {
            "total": aab_png_files + aab_svg_files,
            "png": aab_png_files,
            "svg": aab_svg_files,
        },
        "missingBaseModuleFileEntries": aab_missing_file,
    },
    "gate": "PASS",
}
OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
