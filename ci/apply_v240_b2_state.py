from pathlib import Path
import re
import shutil

ROOT = Path.cwd()
REPO = ROOT.parent.parent
UI = Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui")
NAV = UI / "NavigationHost.kt"
LESSON = UI / "LessonReader.kt"
QUIZ = UI / "QuizScreen.kt"
GRADLE = Path("app/build.gradle.kts")
VM_OVERLAY = REPO / "overlay/v2.4/app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/LearningStateViewModel.kt"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


assert VM_OVERLAY.is_file()
shutil.copy2(VM_OVERLAY, UI / "LearningStateViewModel.kt")

gradle = GRADLE.read_text(encoding="utf-8")
if 'androidx.lifecycle:lifecycle-viewmodel-compose:2.9.4' not in gradle:
    gradle = replace_once(
        gradle,
        'implementation("androidx.activity:activity-compose:1.11.0")',
        'implementation("androidx.activity:activity-compose:1.10.1")\n    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.9.4")',
        "Lifecycle ViewModel dependency",
    )
GRADLE.write_text(gradle, encoding="utf-8")

nav = NAV.read_text(encoding="utf-8")
nav = replace_once(
    nav,
    "fun EnvironmentalStudiesApp() {",
    "fun EnvironmentalStudiesApp(learningState: LearningStateViewModel = androidx.lifecycle.viewmodel.compose.viewModel()) {",
    "application ViewModel parameter",
)
nav = replace_once(
    nav,
    'var route by rememberSaveable { mutableStateOf(prefs.getString("last_route", "home") ?: "home") }',
    'val route by learningState.route.collectAsState()',
    "route state",
)
nav = replace_once(
    nav,
    'var languageName by rememberSaveable { mutableStateOf(prefs.getString("language", LanguageMode.ENGLISH.name) ?: LanguageMode.ENGLISH.name) }',
    'val languageName by learningState.languageName.collectAsState()',
    "language state",
)

nav = re.sub(
    r'''\n    LaunchedEffect\(route\) \{\n        if \(route != "search"\) prefs\.edit\(\)\.putString\("last_route", route\)\.apply\(\)\n    \}\n    LaunchedEffect\(languageName\) \{\n        prefs\.edit\(\)\.putString\("language", languageName\)\.apply\(\)\n    \}\n''',
    "\n",
    nav,
    count=1,
)
nav = replace_once(
    nav,
    '''    val navigate: (String) -> Unit = { destination ->
        if (destination == "search") routeBeforeSearch = route
        route = destination
    }''',
    '''    val navigate: (String) -> Unit = { destination ->
        if (destination == "search") routeBeforeSearch = route
        learningState.setRoute(destination)
    }''',
    "navigate state",
)
nav = replace_once(
    nav,
    '''    val back: () -> Unit = {
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
    }''',
    '''    val back: () -> Unit = {
        learningState.setRoute(
            when {
                route == "search" -> routeBeforeSearch
                route.startsWith("lesson:") -> {
                    val unitNumber = route.split(':').getOrNull(1)?.toIntOrNull()
                    if (unitNumber != null) "unit:$unitNumber" else "units"
                }
                route.startsWith("quiz:") || route.startsWith("review:") || route.startsWith("unit:") -> "units"
                route.startsWith("supp:") || route == "privacy" -> "more"
                else -> "home"
            }
        )
    }''',
    "back state",
)

for old, new in [
    ('{ route = "home" }', '{ navigate("home") }'),
    ('{ route = "units" }', '{ navigate("units") }'),
    ('{ route = "tools" }', '{ navigate("tools") }'),
    ('{ route = "more" }', '{ navigate("more") }'),
    ('{ languageName = it.name }', '{ learningState.setLanguage(it.name) }'),
]:
    nav = nav.replace(old, new)

# Convert any remaining direct route assignments in navigation controls.
nav = re.sub(
    r'(?m)(?<!val )(?<!var )\\broute\\s*=\\s*"([^"]+)"',
    lambda match: f'learningState.setRoute("{match.group(1)}")',
    nav,
)

assert "languageName =" not in "\n".join(
    line for line in nav.splitlines()
    if "val languageName" not in line
)
assert not re.search(r"(?m)^\s*route\s*=", nav)
NAV.write_text(nav, encoding="utf-8")

lesson = LESSON.read_text(encoding="utf-8")
lesson = replace_once(
    lesson,
    '''    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("learning_state", android.content.Context.MODE_PRIVATE) }
    val scrollKey = "lesson_scroll_${unit.number}_${lesson.id}_${mode.name}"
    val listState = rememberLazyListState(initialFirstVisibleItemIndex = prefs.getInt(scrollKey, 0).coerceAtLeast(0))''',
    '''    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("learning_state", android.content.Context.MODE_PRIVATE) }
    val learningState: LearningStateViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
    val listState = rememberLazyListState(
        initialFirstVisibleItemIndex = learningState.readingPosition(unit.number, lesson.id, mode)
    )''',
    "reading state initialisation",
)
lesson = replace_once(
    lesson,
    '''            val saved = prefs.getInt(scrollKey, 0).coerceAtLeast(0)
            runCatching { listState.scrollToItem(saved) }''',
    '''            val saved = learningState.readingPosition(unit.number, lesson.id, mode)
            runCatching { listState.scrollToItem(saved) }''',
    "reading state restore",
)
lesson = replace_once(
    lesson,
    '''        snapshotFlow { listState.firstVisibleItemIndex }.collect { index ->
            if (!visualFocus) prefs.edit().putInt(scrollKey, index).apply()
        }''',
    '''        snapshotFlow { listState.firstVisibleItemIndex }.collect { index ->
            if (!visualFocus) {
                learningState.setReadingPosition(unit.number, lesson.id, mode, index)
            }
        }''',
    "reading state persistence",
)
assert "scrollKey" not in lesson
LESSON.write_text(lesson, encoding="utf-8")

quiz = QUIZ.read_text(encoding="utf-8")
quiz = replace_once(
    quiz,
    '''fun QuizScreen(unit: UnitContent, mode: LanguageMode, onMode: (LanguageMode) -> Unit) {
    var encoded by rememberSaveable(unit.number) { mutableStateOf(List(unit.quiz.size) { -1 }.joinToString(",")) }
    var checked by rememberSaveable(unit.number) { mutableStateOf(false) }''',
    '''fun QuizScreen(unit: UnitContent, mode: LanguageMode, onMode: (LanguageMode) -> Unit) {
    val learningState: LearningStateViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
    val encoded by learningState.quizAnswers(unit.number, unit.quiz.size).collectAsState()
    val checked by learningState.quizChecked(unit.number).collectAsState()''',
    "quiz state initialisation",
)
quiz = replace_once(
    quiz,
    '''    fun select(q: Int, option: Int) {
        val next = answers.toMutableList()
        next[q] = option
        encoded = next.joinToString(",")
        checked = false
    }''',
    '''    fun select(q: Int, option: Int) {
        learningState.setQuizAnswer(
            unitNumber = unit.number,
            questionCount = unit.quiz.size,
            questionIndex = q,
            optionIndex = option,
        )
    }''',
    "quiz answer mutation",
)
quiz = replace_once(
    quiz,
    'Button(onClick = { checked = true }, modifier = Modifier.fillMaxWidth()) {',
    'Button(onClick = { learningState.setQuizChecked(unit.number, true) }, modifier = Modifier.fillMaxWidth()) {',
    "quiz check state",
)
QUIZ.write_text(quiz, encoding="utf-8")

assert 'rememberSaveable(unit.number)' not in quiz
assert "learningState.quizAnswers" in quiz
assert "learningState.readingPosition" in lesson
assert "learningState.languageName.collectAsState()" in nav
assert "learningState.route.collectAsState()" in nav
print("B2 moved language, reading position and quiz state into SavedStateHandle-backed ViewModel state.")
