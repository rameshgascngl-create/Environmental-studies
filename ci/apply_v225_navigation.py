from pathlib import Path
import hashlib
import json

ROOT = Path.cwd()
APP = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/App.kt"
GRADLE = ROOT / "app/build.gradle.kts"
BOOK = ROOT / "app/src/main/res/raw/book_content.json"
EXPECTED_BOOK_SHA256 = "1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


assert sha256(BOOK) == EXPECTED_BOOK_SHA256, "v2.2.4 book payload identity mismatch"

app = APP.read_text(encoding="utf-8")

old_back = '''    val back: () -> Unit = {
        route = when {
            route == "search" -> routeBeforeSearch
            route.startsWith("lesson:") || route.startsWith("quiz:") || route.startsWith("review:") || route.startsWith("unit:") -> "units"
            route.startsWith("supp:") || route == "privacy" -> "more"
            else -> "home"
        }
    }'''
new_back = '''    val back: () -> Unit = {
        route = when {
            route == "search" -> routeBeforeSearch
            route.startsWith("lesson:") -> {
                val unitNumber = route.split(':').getOrNull(1)?.toIntOrNull()
                if (unitNumber != null) "unit:$unitNumber" else "units"
            }
            route.startsWith("quiz:") || route.startsWith("review:") || route.startsWith("unit:") -> "units"
            route.startsWith("supp:") || route == "privacy" -> "more"
            else -> "home"
        }
    }'''
app = replace_once(app, old_back, new_back, "logical lesson back destination")

app = replace_once(
    app,
    '''                    actions = {
                        Box {''',
    '''                    actions = {
                        if (inLesson) {
                            TextButton(onClick = { navigate("home") }) {
                                Text(if (language == LanguageMode.TAMIL) "முகப்பு" else "Home")
                            }
                        }
                        Box {''',
    "persistent lesson Home action",
)

app = replace_once(
    app,
    '''                LessonBody(unit, lesson, mode, onMode, navigate, visualFocus, Modifier.weight(1f))''',
    '''                LessonBody(
                    unit = unit,
                    lesson = lesson,
                    mode = mode,
                    onMode = onMode,
                    navigate = navigate,
                    visualFocus = visualFocus,
                    showNavigationBar = false,
                    modifier = Modifier.weight(1f)
                )''',
    "wide LessonBody call",
)

app = replace_once(
    app,
    '''                    navigate,
                    visualFocus,
                    Modifier.fillMaxHeight().fillMaxWidth().widthIn(max = 900.dp)
                )''',
    '''                    navigate = navigate,
                    visualFocus = visualFocus,
                    showNavigationBar = true,
                    modifier = Modifier.fillMaxHeight().fillMaxWidth().widthIn(max = 900.dp)
                )''',
    "mobile LessonBody call",
)

app = replace_once(
    app,
    '''    navigate: (String) -> Unit,
    visualFocus: Boolean,
    modifier: Modifier
) {''',
    '''    navigate: (String) -> Unit,
    visualFocus: Boolean,
    showNavigationBar: Boolean,
    modifier: Modifier
) {''',
    "LessonBody signature",
)

app = replace_once(
    app,
    '''    val scope = rememberCoroutineScope()
    val progress by remember {''',
    '''    val scope = rememberCoroutineScope()
    var lessonActionsOpen by remember(lesson.id) { mutableStateOf(false) }
    val progress by remember {''',
    "lesson action menu state",
)

old_header = '''            item {
                Text("${lesson.number} ${if (mode == LanguageMode.TAMIL) lesson.titleTa else lesson.titleEn}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(12.dp))
                LanguageSelector(mode, onMode)
                if (visualFocus) {
                    Spacer(Modifier.height(8.dp))
                    Text("Figure focus / படங்கள் மட்டும்", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)
                }
            }'''
new_header = '''            item {
                Text(
                    "${lesson.number} ${if (mode == LanguageMode.TAMIL) lesson.titleTa else lesson.titleEn}",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    LanguageSelector(mode, onMode)
                    Box {
                        TextButton(onClick = { lessonActionsOpen = true }) {
                            Text(if (mode == LanguageMode.TAMIL) "மேலும் ⋮" else "More ⋮")
                        }
                        DropdownMenu(
                            expanded = lessonActionsOpen,
                            onDismissRequest = { lessonActionsOpen = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text(if (mode == LanguageMode.TAMIL) "அச்சிடுக" else "Print") },
                                onClick = {
                                    lessonActionsOpen = false
                                    PdfExporter.printLesson(context, unit, lesson, mode)
                                }
                            )
                            DropdownMenuItem(
                                text = { Text(if (mode == LanguageMode.TAMIL) "PDF ஆகச் சேமிக்க" else "Save PDF") },
                                onClick = {
                                    lessonActionsOpen = false
                                    pdfLauncher.launch(exportName)
                                }
                            )
                        }
                    }
                }
                if (visualFocus) {
                    Spacer(Modifier.height(8.dp))
                    Text("Figure focus / படங்கள் மட்டும்", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)
                }
            }'''
app = replace_once(app, old_header, new_header, "lesson actions overflow")

app = replace_once(
    app,
    '''        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            state = listState,''',
    '''        LazyColumn(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            state = listState,''',
    "reserve space for persistent lesson navigation",
)

old_footer = '''            item {
                HorizontalDivider()
                Spacer(Modifier.height(8.dp))
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedButton(
                        onClick = { previous?.let { navigate("lesson:${unit.number}:${it.id}") } },
                        enabled = previous != null,
                        modifier = Modifier.weight(1f)
                    ) { Text("← Previous") }
                    Button(
                        onClick = { next?.let { navigate("lesson:${unit.number}:${it.id}") } },
                        enabled = next != null,
                        modifier = Modifier.weight(1f)
                    ) { Text("Next →") }
                }
                Spacer(Modifier.height(8.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(
                        onClick = { PdfExporter.printLesson(context, unit, lesson, mode) },
                        modifier = Modifier.weight(1f)
                    ) { Text("Print") }
                    OutlinedButton(
                        onClick = { pdfLauncher.launch(exportName) },
                        modifier = Modifier.weight(1f)
                    ) { Text("Save PDF") }
                }
            }
        }
    }
}'''

new_footer = '''            item { Spacer(Modifier.height(12.dp)) }
        }

        if (showNavigationBar) {
            HorizontalDivider()
            NavigationBar(modifier = Modifier.fillMaxWidth()) {
                NavigationBarItem(
                    selected = false,
                    enabled = previous != null,
                    onClick = { previous?.let { navigate("lesson:${unit.number}:${it.id}") } },
                    icon = { Text("‹") },
                    label = { Text(if (mode == LanguageMode.TAMIL) "முந்தைய" else "Previous") }
                )
                NavigationBarItem(
                    selected = false,
                    onClick = { navigate("unit:${unit.number}") },
                    icon = { Text("☰") },
                    label = { Text(if (mode == LanguageMode.TAMIL) "அலகு" else "Unit") }
                )
                NavigationBarItem(
                    selected = false,
                    onClick = { navigate("home") },
                    icon = { Text("⌂") },
                    label = { Text(if (mode == LanguageMode.TAMIL) "முகப்பு" else "Home") }
                )
                NavigationBarItem(
                    selected = false,
                    enabled = next != null,
                    onClick = { next?.let { navigate("lesson:${unit.number}:${it.id}") } },
                    icon = { Text("›") },
                    label = { Text(if (mode == LanguageMode.TAMIL) "அடுத்து" else "Next") }
                )
            }
        }
    }
}'''
app = replace_once(app, old_footer, new_footer, "persistent lesson navigation footer")

APP.write_text(app, encoding="utf-8")

gradle = GRADLE.read_text(encoding="utf-8")
gradle = replace_once(gradle, 'versionCode = 20204', 'versionCode = 20205', "versionCode")
gradle = replace_once(gradle, 'versionName = "2.2.4"', 'versionName = "2.2.5"', "versionName")
GRADLE.write_text(gradle, encoding="utf-8")

assert sha256(BOOK) == EXPECTED_BOOK_SHA256, "book payload changed during navigation-only pass"

final_app = APP.read_text(encoding="utf-8")
checks = {
    "lesson_home_action": 'Text(if (language == LanguageMode.TAMIL) "முகப்பு" else "Home")' in final_app,
    "unit_contents_route": 'onClick = { navigate("unit:${unit.number}") }' in final_app,
    "lesson_nav_bar": "if (showNavigationBar)" in final_app,
    "previous_nav": 'label = { Text(if (mode == LanguageMode.TAMIL) "முந்தைய" else "Previous") }' in final_app,
    "next_nav": 'label = { Text(if (mode == LanguageMode.TAMIL) "அடுத்து" else "Next") }' in final_app,
    "print_in_more": 'Text(if (mode == LanguageMode.TAMIL) "அச்சிடுக" else "Print")' in final_app,
    "pdf_in_more": 'Text(if (mode == LanguageMode.TAMIL) "PDF ஆகச் சேமிக்க" else "Save PDF")' in final_app,
    "lesson_back_to_current_unit": 'if (unitNumber != null) "unit:$unitNumber" else "units"' in final_app,
}
assert all(checks.values()), checks

audit = {
    "versionName": "2.2.5",
    "versionCode": 20205,
    "scope": "lesson navigation UX only",
    "book_content_sha256": sha256(BOOK),
    "book_content_unchanged": True,
    "english_payload_unchanged": True,
    "tamil_payload_unchanged": True,
    "figure_routing_unchanged": True,
    "direct_home_from_lesson": True,
    "direct_unit_contents_from_lesson": True,
    "persistent_previous_next_navigation": True,
    "print_pdf_moved_to_lesson_more_menu": True,
    "system_back_from_lesson_returns_current_unit": True,
    "wide_layout_side_list_preserved": True,
    "checks": checks,
}
Path("V225_NAVIGATION_UX_AUDIT.json").write_text(
    json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

Path("V225_NAVIGATION_UX_CHANGELOG.md").write_text(
    """# Environmental Studies v2.2.5 — Lesson Navigation UX\n\n"
    "- Added a direct Home action while reading a lesson.\n"
    "- Added persistent Previous / Unit / Home / Next navigation on phone and focus-mode lesson reading.\n"
    "- Android Back from a lesson now returns to that lesson's current Unit Contents page rather than the all-units page.\n"
    "- Moved Print and Save PDF out of the prominent lesson footer into a compact lesson More menu.\n"
    "- Preserved the wide-layout lesson side list.\n"
    "- Preserved the exact v2.2.4 book payload and all scientific/Tamil content.\n"
    """,
    encoding="utf-8",
)

print(json.dumps(audit, ensure_ascii=False, indent=2))
