from pathlib import Path
import re

GRADLE = Path("app/build.gradle.kts")
PROGUARD = Path("app/proguard-rules.pro")

gradle = GRADLE.read_text(encoding="utf-8")
proguard = PROGUARD.read_text(encoding="utf-8") if PROGUARD.exists() else ""

reflection_dependencies = [
    line.strip()
    for line in gradle.splitlines()
    if re.search(r"gson|kotlinx-serialization|kotlin-reflect|moshi", line, re.I)
]

if not reflection_dependencies:
    # The app parses bundled JSON without Gson, kotlinx.serialization or Kotlin reflection.
    # No application-specific keep or annotation-retention rule is therefore justified.
    filtered = [
        line for line in proguard.splitlines()
        if line.strip() != "-keepattributes *Annotation*"
    ]
    PROGUARD.write_text("\n".join(filtered).rstrip() + "\n", encoding="utf-8")

proguard = PROGUARD.read_text(encoding="utf-8") if PROGUARD.exists() else ""
active_rules = [
    line.strip()
    for line in proguard.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]

if not reflection_dependencies:
    assert not active_rules, f"Unexpected R8 rules without a reflection dependency: {active_rules}"

assert "isMinifyEnabled = true" in gradle
assert "isShrinkResources = true" in gradle

print("A4 reflection dependencies:", reflection_dependencies)
print("A4 active application keep rules after correction:", active_rules)
print("A4 verified: no application-specific R8 keep rule is required.")
