from pathlib import Path
import hashlib
import json
import re

UI = Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui")
APP = UI / "App.kt"

source = APP.read_text(encoding="utf-8")
lines = source.splitlines(keepends=True)

package_match = re.search(r"(?m)^package\s+[^\n]+\n", source)
if not package_match:
    raise AssertionError("Package declaration not found")
package_line = package_match.group(0)

imports = "\n".join(
    line for line in source.splitlines()
    if line.startswith("import ")
)
header = package_line + "\n" + imports + "\n\n"

# Preserve the topRoutes declaration with the navigation host.
top_routes_match = re.search(r"(?m)^private val topRoutes\s*=.*$", source)
if not top_routes_match:
    raise AssertionError("topRoutes declaration not found")
top_routes = top_routes_match.group(0).replace("private val topRoutes", "internal val topRoutes")

# Locate each top-level function including contiguous annotations immediately above it.
pattern = re.compile(
    r"(?m)^(?P<annotations>(?:@[^\n]+\n)*)"
    r"(?P<signature>(?:(?:private|internal|public)\s+)?(?:suspend\s+)?fun\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\()"
)
matches = list(pattern.finditer(source))
if not matches:
    raise AssertionError("No top-level functions found")

blocks = {}
order = []
for index, match in enumerate(matches):
    start = match.start()
    end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
    name = match.group("name")
    block = source[start:end].rstrip() + "\n"
    blocks[name] = block
    order.append(name)

expected_order = [
    "EnvironmentalStudiesApp",
    "RailItem",
    "HomeScreen",
    "UnitsScreen",
    "UnitOpeningScreen",
    "LessonScreen",
    "LessonBody",
    "LanguageSelector",
    "SectionLabel",
    "ReviewScreen",
    "MoreScreen",
    "SupplementalScreen",
    "SearchScreen",
    "PrivacyScreen",
    "openPrivacyPolicyUrl",
]
assert order == expected_order, (order, expected_order)

def expose(block: str, names: set[str]) -> str:
    for name in names:
        block = re.sub(
            rf"(?m)^(\s*)private\s+fun\s+{re.escape(name)}\s*\(",
            rf"\1internal fun {name}(",
            block,
            count=1,
        )
    return block

groups = {
    "NavigationHost.kt": [
        "EnvironmentalStudiesApp",
        "RailItem",
    ],
    "HomeScreens.kt": [
        "HomeScreen",
        "UnitsScreen",
        "UnitOpeningScreen",
    ],
    "LessonReader.kt": [
        "LessonScreen",
        "LessonBody",
        "LanguageSelector",
        "SectionLabel",
        "ReviewScreen",
    ],
    "SettingsScreen.kt": [
        "MoreScreen",
        "PrivacyScreen",
        "openPrivacyPolicyUrl",
    ],
    "SupportingScreens.kt": [
        "SupplementalScreen",
        "SearchScreen",
    ],
}

public_entry = {"EnvironmentalStudiesApp"}
called_from_navigation = {
    "HomeScreen",
    "UnitsScreen",
    "UnitOpeningScreen",
    "LessonScreen",
    "ReviewScreen",
    "MoreScreen",
    "SupplementalScreen",
    "SearchScreen",
    "PrivacyScreen",
}

written = {}
for filename, names in groups.items():
    body_parts = []
    if filename == "NavigationHost.kt":
        body_parts.append(top_routes + "\n")
    for name in names:
        block = blocks[name]
        if name in called_from_navigation:
            block = expose(block, {name})
        body_parts.append(block)
    content = header + "\n".join(body_parts).rstrip() + "\n"
    path = UI / filename
    path.write_text(content, encoding="utf-8")
    written[filename] = {
        "functions": names,
        "lines": len(content.splitlines()),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
    }

APP.unlink()

assert not APP.exists()
assert (UI / "NativeContent.kt").is_file(), "Block renderers were already split before this task"
assert (UI / "SvgFigureBlock.kt").is_file(), "SVG block renderer was already split before this task"
assert (UI / "PdfExporter.kt").is_file(), "PDF export was already split before this task"

report = {
    "baseline_app_lines": len(source.splitlines()),
    "baseline_app_functions": order,
    "created_files": written,
    "pre_existing_focused_files": [
        "NativeContent.kt",
        "SvgFigureBlock.kt",
        "PdfExporter.kt",
    ],
    "finding_corrections": {
        "block_renderers": "Already separate in NativeContent.kt and SvgFigureBlock.kt; no duplicate refactor was performed.",
        "pdf_export": "Already separate in PdfExporter.kt; App.kt only called it, so no PDF exporter move was required.",
    },
}
Path("V240_B1_ARCHITECTURE_REFACTOR.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
