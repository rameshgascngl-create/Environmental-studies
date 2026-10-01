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

active_rules = [
    line.strip()
    for line in proguard.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]

if not reflection_dependencies:
    broad_rules = [
        rule for rule in active_rules
        if re.search(r"-keep\s+class\s+\*\*|-keep\s+class\s+edu\.gascnagercoil\.environmentalsciences\.\*\*", rule)
    ]
    assert not broad_rules, f"Broad R8 keep rules are not justified: {broad_rules}"

assert "isMinifyEnabled = true" in gradle
assert "isShrinkResources = true" in gradle

print("A4 reflection dependencies:", reflection_dependencies)
print("A4 active application keep rules:", active_rules)
print("A4 verified: no unjustified broad R8 keep rule is required.")
