from pathlib import Path
import re
import xml.etree.ElementTree as ET

MANIFEST = Path("app/src/main/AndroidManifest.xml")
text = MANIFEST.read_text(encoding="utf-8")

if re.search(r'android:allowBackup\s*=\s*"[^"]*"', text):
    text = re.sub(
        r'android:allowBackup\s*=\s*"[^"]*"',
        'android:allowBackup="false"',
        text,
        count=1,
    )
else:
    count = text.count("<application")
    if count != 1:
        raise AssertionError(f"Expected one <application> element, found {count}")
    text = text.replace("<application", '<application\n        android:allowBackup="false"', 1)

MANIFEST.write_text(text, encoding="utf-8")

root = ET.parse(MANIFEST).getroot()
application = root.find("application")
assert application is not None
allow_backup = application.attrib.get("{http://schemas.android.com/apk/res/android}allowBackup")
assert allow_backup == "false", allow_backup

print("A3 applied: Android backup is disabled for application preferences and local learning state.")
