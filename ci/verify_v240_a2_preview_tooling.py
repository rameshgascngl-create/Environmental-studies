from pathlib import Path
import re
import xml.etree.ElementTree as ET

GRADLE = Path("app/build.gradle.kts")
MANIFEST = Path("app/src/main/AndroidManifest.xml")

gradle = GRADLE.read_text(encoding="utf-8")
manifest = ET.parse(MANIFEST).getroot()
android_name = "{http://schemas.android.com/apk/res/android}name"

assert 'debugImplementation("androidx.compose.ui:ui-tooling")' in gradle
assert 'debugImplementation("androidx.compose.ui:ui-test-manifest")' in gradle

for forbidden in (
    'implementation("androidx.compose.ui:ui-tooling")',
    'releaseImplementation("androidx.compose.ui:ui-tooling")',
    'implementation("androidx.compose.ui:ui-test-manifest")',
    'releaseImplementation("androidx.compose.ui:ui-test-manifest")',
):
    assert forbidden not in gradle, forbidden

activities = [node.attrib.get(android_name, "") for node in manifest.findall(".//activity")]
assert not any("PreviewActivity" in name for name in activities), activities

print("A2 verified: preview tooling is debug-only and PreviewActivity is absent.")
