from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET

ROOT = Path.cwd()
APP = ROOT / "app"
MAIN = APP / "src/main"
RES = MAIN / "res"
RAW = RES / "raw"
BOOK = RAW / "book_content.json"
MANIFEST = MAIN / "AndroidManifest.xml"
GRADLE = APP / "build.gradle.kts"
PROGUARD = APP / "proguard-rules.pro"
SRC = MAIN / "java"

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


book = json.loads(BOOK.read_text(encoding="utf-8"))
gradle = GRADLE.read_text(encoding="utf-8")
manifest_text = MANIFEST.read_text(encoding="utf-8")
manifest_root = ET.parse(MANIFEST).getroot()
application = manifest_root.find("application")
proguard = PROGUARD.read_text(encoding="utf-8") if PROGUARD.exists() else ""

dependencies = "\n".join(
    line.strip()
    for line in gradle.splitlines()
    if any(token in line for token in ("implementation(", "debugImplementation(", "androidTestImplementation(", "releaseImplementation("))
)

pngs = sorted(RES.rglob("*.png"))
svgs = sorted(RAW.glob("*.svg"))
png_records = []
for p in pngs:
    dims = png_dimensions(p)
    png_records.append(
        {
            "path": str(p.relative_to(ROOT)),
            "bytes_on_disk": p.stat().st_size,
            "width": dims[0] if dims else None,
            "height": dims[1] if dims else None,
            "rgba_decoded_bytes": dims[0] * dims[1] * 4 if dims else None,
        }
    )

svg_records = []
small_svg_text = []
versioned_svg_assets = []
for p in svgs:
    text = p.read_text(encoding="utf-8", errors="replace")
    viewbox = re.search(r'viewBox\s*=\s*["\']([^"\']+)', text)
    sizes = [float(x) for x in re.findall(r'font-size\s*[:=]\s*["\']?([0-9]+(?:\.[0-9]+)?)', text)]
    if not sizes:
        sizes = [float(x) for x in re.findall(r'<text[^>]+font-size=["\']([0-9]+(?:\.[0-9]+)?)', text)]
    rec = {
        "path": str(p.relative_to(ROOT)),
        "viewBox": viewbox.group(1) if viewbox else None,
        "minimum_text_units": min(sizes) if sizes else None,
        "text_size_samples": sorted(set(sizes))[:12],
    }
    svg_records.append(rec)
    if sizes and min(sizes) < 36:
        small_svg_text.append(rec)
    if re.search(r'(^|/)(?:v22|v221)[^/]*\.svg$', str(p.relative_to(ROOT)), re.I):
        versioned_svg_assets.append(str(p.relative_to(ROOT)))

# Include drawable SVG-like XML/vector names and any raw assets whose file names carry version prefixes.
versioned_assets = sorted(
    str(p.relative_to(ROOT))
    for p in RES.rglob("*")
    if p.is_file() and re.match(r"v22(?:1)?_", p.name, re.I)
)

app_attrs = {}
if application is not None:
    for key in ("allowBackup", "dataExtractionRules", "fullBackupContent", "debuggable"):
        app_attrs[key] = application.attrib.get(ANDROID_NS + key)

activities = []
for activity in manifest_root.findall(".//activity"):
    activities.append(activity.attrib.get(ANDROID_NS + "name"))
preview_activity = any(name and "PreviewActivity" in name for name in activities)

units = book.get("units", [])
quiz_counts = {str(u.get("number")): len(u.get("quiz", [])) for u in units}

mismatches = []
lesson_rows = []
for u in units:
    for lesson in u.get("lessons", []):
        en = lesson.get("english", [])
        ta = lesson.get("tamil", [])
        row = {
            "lesson": str(lesson.get("number")),
            "title_en": lesson.get("titleEn"),
            "title_ta": lesson.get("titleTa"),
            "english_blocks": len(en),
            "tamil_blocks": len(ta),
        }
        lesson_rows.append(row)
        if len(en) != len(ta):
            mismatches.append(row)

raw_book = BOOK.read_text(encoding="utf-8")
phrases = {
    "generic_environmental_implication": raw_book.count("What is one important environmental implication of"),
    "generic_familiar_situation": raw_book.count("Apply the concept to one familiar situation"),
    "remember_blocks_en": raw_book.count("Remember:"),
    "remember_blocks_ta": raw_book.count("நினைவில்"),
}

# Look for common placeholder syntax, while excluding normal format punctuation.
placeholder_patterns = {
    "square_tokens": re.findall(r"\[[A-Z][A-Z0-9_ -]{2,}\]", raw_book),
    "double_braces": re.findall(r"\{\{[^{}]+\}\}", raw_book),
    "angle_tokens": re.findall(r"<(?:TITLE|TOPIC|LESSON|PLACEHOLDER|TODO)[^>]*>", raw_book, flags=re.I),
    "todo_tokens": re.findall(r"\b(?:TODO|TBD|PLACEHOLDER)\b", raw_book, flags=re.I),
}

source_text = "\n".join(
    p.read_text(encoding="utf-8", errors="replace")
    for p in SRC.rglob("*.kt")
)

network_markers = sorted(set(re.findall(
    r"(?:android\.webkit\.WebView|WebView\(|android\.permission\.INTERNET|retrofit|okhttp|firebase|analytics)",
    source_text + "\n" + manifest_text + "\n" + gradle,
    flags=re.I,
)))

native_version = book.get("nativeVersion")
schema_version = book.get("schemaVersion")

report = {
    "book_sha256": sha256(BOOK),
    "schemaVersion": schema_version,
    "nativeVersion": native_version,
    "gradle_version_name_matches": re.findall(r'versionName\s*=\s*"([^"]+)"', gradle),
    "gradle_version_code_matches": [int(x) for x in re.findall(r"versionCode\s*=\s*(\d+)", gradle)],
    "release": {
        "explicit_debuggable_false": bool(re.search(r"release\s*\{[\s\S]*?isDebuggable\s*=\s*false", gradle)),
        "minify_enabled": bool(re.search(r"release\s*\{[\s\S]*?isMinifyEnabled\s*=\s*true", gradle)),
        "shrink_resources": bool(re.search(r"release\s*\{[\s\S]*?isShrinkResources\s*=\s*true", gradle)),
        "debug_application_suffix_present": 'applicationIdSuffix = ".debug"' in gradle,
        "release_application_suffix_present": bool(re.search(r"release\s*\{[\s\S]*?applicationIdSuffix", gradle)),
        "signing_from_environment": "ENVSTUDIES_KEYSTORE_PATH" in gradle,
        "signing_from_local_properties": "local.properties" in gradle or "localProperties" in gradle,
    },
    "dependencies": {
        "ui_tooling_debug_only": 'debugImplementation("androidx.compose.ui:ui-tooling")' in gradle,
        "ui_test_manifest_debug_only": 'debugImplementation("androidx.compose.ui:ui-test-manifest")' in gradle,
        "ui_tooling_preview_implementation": 'implementation("androidx.compose.ui:ui-tooling-preview")' in gradle,
        "reflection_or_json_runtime_markers": [
            line for line in dependencies.splitlines()
            if re.search(r"gson|kotlinx-serialization|reflect|moshi", line, re.I)
        ],
    },
    "manifest": {
        "application_attributes": app_attrs,
        "preview_activity_present": preview_activity,
        "activities": activities,
    },
    "proguard_non_comment_lines": [
        line.strip()
        for line in proguard.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ],
    "network_markers": network_markers,
    "figures": {
        "png_count": len(pngs),
        "png_total_bytes_on_disk": sum(x["bytes_on_disk"] for x in png_records),
        "png_total_rgba_decoded_bytes_if_all_loaded": sum(x["rgba_decoded_bytes"] or 0 for x in png_records),
        "png_width_histogram": {
            str(width): sum(1 for x in png_records if x["width"] == width)
            for width in sorted({x["width"] for x in png_records if x["width"]})
        },
        "png_records": png_records,
        "svg_count_raw": len(svgs),
        "svg_small_text_count": len(small_svg_text),
        "svg_small_text": small_svg_text,
        "version_prefixed_assets": versioned_assets,
        "version_prefixed_svg_count": len(versioned_svg_assets),
    },
    "content": {
        "unit_count": len(units),
        "lesson_count": len(lesson_rows),
        "quiz_counts": quiz_counts,
        "block_count_mismatch_count": len(mismatches),
        "block_count_mismatches": mismatches,
        "phrase_counts": phrases,
        "placeholder_matches": placeholder_patterns,
    },
}

Path("V240_STATIC_FINDINGS.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print("=== V2.4.0 STATIC FINDINGS ===")
print(json.dumps({
    "schemaVersion": report["schemaVersion"],
    "nativeVersion": report["nativeVersion"],
    "gradle_version_name_matches": report["gradle_version_name_matches"],
    "gradle_version_code_matches": report["gradle_version_code_matches"],
    "release": report["release"],
    "manifest": report["manifest"],
    "proguard_non_comment_lines": report["proguard_non_comment_lines"],
    "network_markers": report["network_markers"],
    "figures_summary": {
        "png_count": report["figures"]["png_count"],
        "png_total_bytes_on_disk": report["figures"]["png_total_bytes_on_disk"],
        "png_total_rgba_decoded_bytes_if_all_loaded": report["figures"]["png_total_rgba_decoded_bytes_if_all_loaded"],
        "png_width_histogram": report["figures"]["png_width_histogram"],
        "svg_count_raw": report["figures"]["svg_count_raw"],
        "svg_small_text_count": report["figures"]["svg_small_text_count"],
        "version_prefixed_assets_count": len(report["figures"]["version_prefixed_assets"]),
    },
    "content": report["content"],
}, ensure_ascii=False, indent=2))
