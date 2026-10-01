from pathlib import Path
import json
import re

ROOT = Path.cwd()
GRADLE = ROOT / "app/build.gradle.kts"
BOOK = ROOT / "app/src/main/res/raw/book_content.json"
RAW = ROOT / "app/src/main/res/raw"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


gradle = GRADLE.read_text(encoding="utf-8")
gradle = replace_once(gradle, 'versionCode = 20300', 'versionCode = 20400', "versionCode")
gradle = replace_once(gradle, 'versionName = "2.3.0"', 'versionName = "2.4.0"', "versionName")
GRADLE.write_text(gradle, encoding="utf-8")

data = json.loads(BOOK.read_text(encoding="utf-8"))
assert data.get("schemaVersion") == 1, "schemaVersion must remain backwards-compatible"
old_native = data.get("nativeVersion")
data["nativeVersion"] = "2.4.0"

mapping: dict[str, str] = {}
for path in sorted(RAW.glob("v22*.svg")):
    old_stem = path.stem
    match = re.fullmatch(r"v22(?:1)?_(.+)", old_stem)
    if not match:
        continue
    new_stem = f"sci_{match.group(1)}"
    target = path.with_name(new_stem + path.suffix)
    if target.exists():
        raise AssertionError(f"Target SVG already exists: {target}")
    mapping[old_stem] = new_stem
    path.rename(target)

assert len(mapping) == 36, f"Expected 36 version-prefixed SVGs, found {len(mapping)}"


def migrate(value):
    if isinstance(value, dict):
        return {key: migrate(item) for key, item in value.items()}
    if isinstance(value, list):
        return [migrate(item) for item in value]
    if isinstance(value, str) and value in mapping:
        return mapping[value]
    return value


data = migrate(data)
BOOK.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

book_text = BOOK.read_text(encoding="utf-8")
assert '"nativeVersion": "2.4.0"' in book_text
assert not re.search(r'"v22(?:1)?_[^"]+"', book_text)
assert not list(RAW.glob("v22*.svg"))
assert len(list(RAW.glob("sci_*.svg"))) >= 36

Path("V240_SVG_RENAME_MAP.json").write_text(
    json.dumps(mapping, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
Path("V240_RELEASE_IDENTITY_AUDIT.json").write_text(
    json.dumps(
        {
            "versionName": "2.4.0",
            "versionCode": 20400,
            "book_nativeVersion_before": old_native,
            "book_nativeVersion_after": "2.4.0",
            "schemaVersion": data["schemaVersion"],
            "renamed_svg_assets": len(mapping),
            "old_prefixes_remaining_in_book": 0,
            "old_prefixes_remaining_in_raw": 0,
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)

print(f"A5 reconciled release identity and renamed {len(mapping)} SVG assets.")
