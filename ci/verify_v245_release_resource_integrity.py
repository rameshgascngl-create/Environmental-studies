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
    assert "base/resources.pb" in aab_entries
    aab_resources_pb = z.read("base/resources.pb")

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
assert len(refs) >= 96, len(refs)
assert len(png) >= 31, len(png)
assert len(svg) >= 65, len(svg)
assert not unexpected, unexpected

v246_png = sorted(x for x in png if x.startswith("fig_v246_"))
v246_webp = v246_png
legacy_png = sorted(x for x in png if not x.startswith("fig_v246_"))
v246_svg = sorted(x for x in svg if x.startswith("sci_v246_"))
if v246_png or v246_svg:
    assert len(v246_png) == 8, len(v246_png)
    assert len(v246_svg) == 112, len(v246_svg)
    assert len(png) == 43, len(png)
    assert len(legacy_png) == 35, len(legacy_png)
    assert len(svg) == 177, len(svg)
    assert len(refs) == 220, len(refs)

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
drawable_exts = (".png", ".webp", ".jpg", ".jpeg")
def aab_drawable_path(name: str):
    matches = [
        x for x in aab_entries
        if x.startswith("base/res/drawable")
        and Path(x).stem == name
        and Path(x).suffix.lower() in drawable_exts
    ]
    assert len(matches) <= 1, (name, matches)
    return matches[0] if matches else None

def aab_drawable_present(name: str) -> bool:
    return aab_drawable_path(name) is not None

for name in sorted(refs):
    present = (
        aab_drawable_present(name)
        if name.startswith("fig_")
        else f"base/res/raw/{name}.svg" in aab_entries
    )
    if not present:
        aab_missing_file.append(name)

apk_png_resolved = sum(x in apk_paths for x in png)
apk_svg_resolved = sum(x in apk_paths for x in svg)
aab_png_files = sum(aab_drawable_present(name) for name in png)
aab_svg_files = sum(f"base/res/raw/{name}.svg" in aab_entries for name in svg)

# Verify resource entry names inside the AAB base module resource table,
# not merely the presence of files in base/res.
aab_missing_table = sorted(name for name in refs if name.encode("utf-8") not in aab_resources_pb)
aab_png_table = sum(name.encode("utf-8") in aab_resources_pb for name in png)
aab_svg_table = sum(name.encode("utf-8") in aab_resources_pb for name in svg)

assert not apk_missing_table, apk_missing_table
assert not apk_missing_file, apk_missing_file
assert not aab_missing_table, aab_missing_table
assert not aab_missing_file, aab_missing_file
assert (apk_png_resolved, apk_svg_resolved) == (len(png), len(svg))
assert (aab_png_table, aab_svg_table) == (len(png), len(svg))
assert (aab_png_files, aab_svg_files) == (len(png), len(svg))
assert "resources.arsc" in apk_entries
assert "base/resources.pb" in aab_entries

# v2.4.6 photographs are deliberately WebP resources. Prove the resource
# table resolves each fig_v246 name to a WebP file in both APK and AAB.
apk_v246_wrong_extension = {
    name: apk_paths.get(name)
    for name in v246_webp
    if not apk_paths.get(name) or Path(apk_paths[name]).suffix.lower() != ".webp"
}
aab_v246_paths = {name: aab_drawable_path(name) for name in v246_webp}
aab_v246_wrong_extension = {
    name: path
    for name, path in aab_v246_paths.items()
    if not path or Path(path).suffix.lower() != ".webp"
}
assert not apk_v246_wrong_extension, apk_v246_wrong_extension
assert not aab_v246_wrong_extension, aab_v246_wrong_extension

# Every packaged v2.4.6 photograph must also have a packaged attribution
# record. This is checked from the same APK/AAB being audited, not only source.
photo_credits = []
credits_apk_path = None
credits_aab_path = None
if v246_webp:
    credits_apk_path = resource_file_path("raw", "v246_photo_credits")
    assert credits_apk_path, "raw/v246_photo_credits missing from release APK resources.arsc"
    assert credits_apk_path in apk_entries, credits_apk_path
    credits_aab_path = "base/res/raw/v246_photo_credits.json"
    assert credits_aab_path in aab_entries
    with zipfile.ZipFile(apk) as z:
        credits_apk_bytes = z.read(credits_apk_path)
    with zipfile.ZipFile(aab) as z:
        credits_aab_bytes = z.read(credits_aab_path)
    assert credits_apk_bytes == credits_aab_bytes, "APK/AAB v246 photo credits differ"
    photo_credits = json.loads(credits_apk_bytes.decode("utf-8"))
    credit_ids = {x.get("id") for x in photo_credits}
    assert credit_ids == set(v246_webp), (sorted(credit_ids), v246_webp)
    for credit in photo_credits:
        for key in ("title", "author", "sourceUrl", "licence", "licenceUrl", "modification"):
            assert str(credit.get(key, "")).strip(), (credit.get("id"), key)
        assert credit["modification"] == "resized and converted to WebP", credit["id"]
        if "BY-SA" in credit["licence"]:
            assert "ShareAlike" in credit.get("shareAlikeNotice", ""), credit["id"]

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
    "expectedUniqueFigures": len(refs),
    "expectedPngOrRasterFigures": len(png),
    "expectedLegacyPngFigures": len(legacy_png),
    "expectedWebpFigures": len(v246_webp),
    "expectedSvgFigures": len(svg),
    "v246PhotoFigures": len(v246_webp),
    "v246PhotoFormat": "webp",
    "v246PhotoCredits": {
        "count": len(photo_credits),
        "apkResourcePath": credits_apk_path,
        "aabResourcePath": credits_aab_path,
        "ids": [x["id"] for x in photo_credits],
        "requiredModificationNotice": "resized and converted to WebP",
    },
    "v246SvgFigures": len(v246_svg),
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
        "v246WebpResolved": len(v246_webp) - len(apk_v246_wrong_extension),
        "v246WrongExtension": apk_v246_wrong_extension,
        "missingFromResourcesArsc": apk_missing_table,
        "missingResolvedFileEntries": apk_missing_file,
        "resolvedResourcePaths": apk_paths,
    },
    "aab": {
        "path": str(aab),
        "bytes": aab.stat().st_size,
        "sha256": sha256_file(aab),
        "baseResourcesPbPresent": True,
        "baseResourcesPbResolved": {
            "total": aab_png_table + aab_svg_table,
            "png": aab_png_table,
            "svg": aab_svg_table,
        },
        "missingFromBaseResourcesPb": aab_missing_table,
        "baseModuleFileEntriesPresent": {
            "total": aab_png_files + aab_svg_files,
            "png": aab_png_files,
            "svg": aab_svg_files,
        },
        "v246WebpFiles": len(v246_webp) - len(aab_v246_wrong_extension),
        "v246WrongExtension": aab_v246_wrong_extension,
        "missingBaseModuleFileEntries": aab_missing_file,
    },
    "gate": "PASS",
}
OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
