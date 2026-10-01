from pathlib import Path
import json
import re

UI = Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui")
APP = UI / "App.kt"

app_text = APP.read_text(encoding="utf-8")
kt_files = sorted(UI.glob("*.kt"))

top_level_functions = []
for match in re.finditer(
    r"(?m)^(?:@[^\n]+\n)*(?:(?:private|internal|public)\s+)?(?:suspend\s+)?fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
    app_text,
):
    line = app_text.count("\n", 0, match.start()) + 1
    top_level_functions.append({"name": match.group(1), "line": line})

composables = []
for match in re.finditer(
    r"(?m)^@Composable\s*\n(?:(?:private|internal|public)\s+)?fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
    app_text,
):
    composables.append(match.group(1))

report = {
    "app_line_count": len(app_text.splitlines()),
    "app_top_level_function_count": len(top_level_functions),
    "app_top_level_functions": top_level_functions,
    "app_composables": composables,
    "ui_files": {
        p.name: len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        for p in kt_files
    },
    "pdf_exporter_files": [
        p.name for p in kt_files if "PdfExporter" in p.read_text(encoding="utf-8", errors="replace")
    ],
    "state_markers": {
        "language_rememberSaveable": bool(re.search(r"languageName\s+by\s+rememberSaveable", app_text)),
        "reading_position_shared_preferences": "lesson_scroll_" in app_text,
        "last_lesson_shared_preferences": "last_lesson_unit_" in app_text,
    },
    "lazy_column_calls_in_app": len(re.findall(r"\bLazyColumn\s*\(", app_text)),
    "lazy_items_calls_in_app": len(re.findall(r"\bitems(?:Indexed)?\s*\(", app_text)),
}
Path("V240_B_ARCHITECTURE_FINDINGS.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
