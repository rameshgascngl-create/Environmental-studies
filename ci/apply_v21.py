from pathlib import Path

ROOT = Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui")
app_path = ROOT / "App.kt"
sim_path = ROOT / "SimulationScreen.kt"

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected block: {label}")
    return text.replace(old, new, 1)

def replace_between(text: str, start: str, end: str, replacement: str, label: str) -> str:
    a = text.find(start)
    if a < 0:
        raise SystemExit(f"Missing start marker: {label}")
    b = text.find(end, a + len(start))
    if b < 0:
        raise SystemExit(f"Missing end marker: {label}")
    return text[:a] + replacement + text[b:]

app = app_path.read_text(encoding="utf-8")
app = replace_once(app, 'var languageName by rememberSaveable { mutableStateOf(prefs.getString("language", LanguageMode.BOTH.name) ?: LanguageMode.BOTH.name) }', 'var languageName by rememberSaveable { mutableStateOf(prefs.getString("language", LanguageMode.ENGLISH.name) ?: LanguageMode.ENGLISH.name) }', "default language")
app = replace_once(app, 'val language = runCatching { LanguageMode.valueOf(languageName) }.getOrDefault(LanguageMode.BOTH)', 'val storedLanguage = runCatching { LanguageMode.valueOf(languageName) }.getOrDefault(LanguageMode.ENGLISH)\n    val language = if (storedLanguage == LanguageMode.BOTH) LanguageMode.ENGLISH else storedLanguage', "language normalization")
app = replace_once(app, 'route == "home" -> HomeScreen(book, navigate)', 'route == "home" -> HomeScreen(book, navigate, language) { languageName = it.name }', "home route")
app = replace_once(app, 'route == "units" -> UnitsScreen(book, navigate)', 'route == "units" -> UnitsScreen(book, navigate, language)', "units route")
app = replace_once(app, 'route == "tools" -> SimulationScreen()', 'route == "tools" -> SimulationScreen(language)', "tools route")
app = replace_once(app, 'book.units.firstOrNull { it.number == n }?.let { UnitOpeningScreen(it, navigate) }', 'book.units.firstOrNull { it.number == n }?.let { UnitOpeningScreen(it, navigate, language) }', "unit route")
app = replace_once(app, 'else -> HomeScreen(book, navigate)', 'else -> HomeScreen(book, navigate, language) { languageName = it.name }', "fallback home route")

home = '''@Composable
private fun HomeScreen(
    book: Book,
    navigate: (String) -> Unit,
    language: LanguageMode,
    onMode: (LanguageMode) -> Unit,
) {
    val tamil = language == LanguageMode.TAMIL
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item { HomeVisualHero(language) }
        item {
            LanguageGateway(
                current = language,
                onSelect = {
                    onMode(it)
                    navigate("units")
                },
            )
        }
        item {
            ElevatedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(if (tamil) "தமிழ் கற்றல் பகுதி" else "English learning section", fontWeight = FontWeight.SemiBold)
                    Text(if (tamil) "9 அலகுகள் · 46 பாடங்கள் · படங்கள் · வினாடிவினா · ஊடாடும் மாதிரிகள்" else "9 units · 46 lessons · visual learning · quizzes · interactive models")
                    Button(onClick = { navigate("unit:1") }) { Text(if (tamil) "கற்றலைத் தொடங்குக" else "Start learning") }
                }
            }
        }
        item {
            BoxWithConstraints(Modifier.fillMaxWidth()) {
                if (maxWidth < 420.dp) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedButton(onClick = { navigate("units") }, modifier = Modifier.fillMaxWidth()) { Text(if (tamil) "அலகுகள்" else "Explore units") }
                        OutlinedButton(onClick = { navigate("tools") }, modifier = Modifier.fillMaxWidth()) { Text(if (tamil) "காலநிலை மற்றும் ஊடாடும் கருவிகள்" else "Climate & interactive tools") }
                    }
                } else {
                    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        OutlinedButton(onClick = { navigate("units") }) { Text(if (tamil) "அலகுகள்" else "Explore units") }
                        OutlinedButton(onClick = { navigate("tools") }) { Text(if (tamil) "ஊடாடும் கருவிகள்" else "Interactive tools") }
                    }
                }
            }
        }
        item { VisualHighlights(language) }
        items(book.units) { unit -> UnitVisualCard(unit = unit, mode = language, onClick = { navigate("unit:${unit.number}") }) }
    }
}

'''

units = '''@Composable
private fun UnitsScreen(book: Book, navigate: (String) -> Unit, language: LanguageMode) {
    LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        items(book.units) { unit ->
            ElevatedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(if (language == LanguageMode.TAMIL) "அலகு ${unit.number}: ${unit.titleTa}" else "Unit ${unit.number}: ${unit.titleEn}", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                    unit.lessons.forEach { lesson ->
                        OutlinedCard(Modifier.fillMaxWidth().clickable { navigate("lesson:${unit.number}:${lesson.id}") }) {
                            Column(Modifier.padding(12.dp)) {
                                Text("${lesson.number} ${if (language == LanguageMode.TAMIL) lesson.titleTa else lesson.titleEn}", fontWeight = FontWeight.Medium)
                            }
                        }
                    }
                    BoxWithConstraints(Modifier.fillMaxWidth()) {
                        if (maxWidth < 420.dp) {
                            Column {
                                TextButton(onClick = { navigate("review:${unit.number}") }, modifier = Modifier.fillMaxWidth()) { Text(if (language == LanguageMode.TAMIL) "மீளாய்வு" else "Review") }
                                TextButton(onClick = { navigate("quiz:${unit.number}") }, modifier = Modifier.fillMaxWidth()) { Text(if (language == LanguageMode.TAMIL) "பல்தேர்வு பயிற்சி (${unit.quiz.size})" else "MCQ practice (${unit.quiz.size})") }
                            }
                        } else {
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                TextButton(onClick = { navigate("review:${unit.number}") }) { Text(if (language == LanguageMode.TAMIL) "மீளாய்வு" else "Review") }
                                TextButton(onClick = { navigate("quiz:${unit.number}") }) { Text(if (language == LanguageMode.TAMIL) "பல்தேர்வு பயிற்சி (${unit.quiz.size})" else "MCQ practice (${unit.quiz.size})") }
                            }
                        }
                    }
                }
            }
        }
    }
}

'''

unit_open = '''@Composable
private fun UnitOpeningScreen(unit: UnitContent, navigate: (String) -> Unit, language: LanguageMode) {
    LazyColumn(contentPadding = PaddingValues(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            Text(if (language == LanguageMode.TAMIL) "அலகு ${unit.number}" else "Unit ${unit.number}", style = MaterialTheme.typography.labelLarge)
            Text(if (language == LanguageMode.TAMIL) unit.titleTa else unit.titleEn, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        }
        items(unit.opening) { NativeBlock(it) }
        item { HorizontalDivider() }
        items(unit.lessons) { lesson ->
            ListItem(headlineContent = { Text("${lesson.number} ${if (language == LanguageMode.TAMIL) lesson.titleTa else lesson.titleEn}") }, modifier = Modifier.clickable { navigate("lesson:${unit.number}:${lesson.id}") })
            HorizontalDivider()
        }
        item {
            BoxWithConstraints(Modifier.fillMaxWidth()) {
                if (maxWidth < 360.dp) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = { navigate("review:${unit.number}") }, modifier = Modifier.fillMaxWidth()) { Text(if (language == LanguageMode.TAMIL) "மீளாய்வு" else "Review") }
                        OutlinedButton(onClick = { navigate("quiz:${unit.number}") }, modifier = Modifier.fillMaxWidth()) { Text(if (language == LanguageMode.TAMIL) "பல்தேர்வு வினாக்கள்" else "MCQs") }
                    }
                } else {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = { navigate("review:${unit.number}") }) { Text(if (language == LanguageMode.TAMIL) "மீளாய்வு" else "Review") }
                        OutlinedButton(onClick = { navigate("quiz:${unit.number}") }) { Text(if (language == LanguageMode.TAMIL) "பல்தேர்வு வினாக்கள்" else "MCQs") }
                    }
                }
            }
        }
    }
}

'''

app = replace_between(app, '@Composable\nprivate fun HomeScreen', '@Composable\nprivate fun UnitsScreen', home, "HomeScreen")
app = replace_between(app, '@Composable\nprivate fun UnitsScreen', '@Composable\nprivate fun UnitOpeningScreen', units, "UnitsScreen")
app = replace_between(app, '@Composable\nprivate fun UnitOpeningScreen', '@Composable\nprivate fun LessonScreen', unit_open, "UnitOpeningScreen")
app = replace_once(app, 'Text("${lesson.number} ${lesson.titleEn}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)\n                Text(lesson.titleTa, style = MaterialTheme.typography.titleLarge)', 'Text("${lesson.number} ${if (mode == LanguageMode.TAMIL) lesson.titleTa else lesson.titleEn}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)', "lesson title")
app = replace_once(app, 'if (mode != LanguageMode.TAMIL) {', 'if (mode == LanguageMode.ENGLISH) {', "english section")
app = replace_once(app, 'if (mode != LanguageMode.ENGLISH) {', 'if (mode == LanguageMode.TAMIL) {', "tamil section")
lang_selector = '''@Composable
private fun LanguageSelector(mode: LanguageMode, onMode: (LanguageMode) -> Unit) {
    CompactLanguageSwitch(mode = mode, onMode = onMode)
}

'''
app = replace_between(app, '@Composable\nprivate fun LanguageSelector', '@Composable\nprivate fun SectionLabel', lang_selector, "LanguageSelector")
app_path.write_text(app, encoding="utf-8")

sim = sim_path.read_text(encoding="utf-8")
if 'import edu.gascnagercoil.environmentalsciences.model.LanguageMode' not in sim:
    sim = replace_once(sim, 'import androidx.compose.ui.unit.dp\n', 'import androidx.compose.ui.unit.dp\nimport edu.gascnagercoil.environmentalsciences.model.LanguageMode\n', "simulation import")
sim = replace_once(sim, 'fun SimulationScreen() {', 'fun SimulationScreen(language: LanguageMode) {', "simulation signature")
sim = replace_once(sim, '        item { GreenhouseCard() }', '        item { ClimateEventsCard(language) }\n        item { GreenhouseCard() }', "climate event insertion")
sim_path.write_text(sim, encoding="utf-8")
print("v2.1 UI integration applied")
