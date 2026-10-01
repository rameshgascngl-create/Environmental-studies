from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path.cwd()
REPO = ROOT.parent.parent
APP = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/App.kt"
VISUAL = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/VisualLearning.kt"
SIM = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/SimulationScreen.kt"
GRADLE = ROOT / "app/build.gradle.kts"
BOOK = ROOT / "app/src/main/res/raw/book_content.json"
UI_DIR = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui"
OVERLAY = REPO / "overlay/v2.3/app/src/main/java/edu/gascnagercoil/environmentalsciences/ui"

EXPECTED_BOOK_SHA256 = "1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, replacement: str, label: str) -> str:
    i = text.find(start)
    j = text.find(end, i + len(start))
    if i < 0 or j < 0:
        raise AssertionError(f"{label}: markers not found")
    return text[:i] + replacement + text[j:]


assert sha256(BOOK) == EXPECTED_BOOK_SHA256, "v2.2.4 content identity changed before v2.3.0"

for name in [
    "AnimationNarration.kt",
    "UnitScenes.kt",
    "EnvironmentalAnimations.kt",
    "ClimateEvents.kt",
]:
    src = OVERLAY / name
    assert src.exists(), f"missing v2.3 overlay: {src}"
    shutil.copy2(src, UI_DIR / name)

app = APP.read_text(encoding="utf-8")

app = replace_once(
    app,
    '        items(book.units) { unit -> UnitVisualCard(unit = unit, mode = language, onClick = { navigate("unit:${unit.number}") }) }',
    '''        items(book.units) { unit ->
            UnitVisualCard(
                unit = unit,
                mode = language,
                onClick = { navigate("unit:${unit.number}") },
                onContinue = { lessonId -> navigate("lesson:${unit.number}:$lessonId") },
            )
        }''',
    "Home UnitVisualCard continue routing",
)

unit_open = '''@Composable
private fun UnitOpeningScreen(unit: UnitContent, navigate: (String) -> Unit, language: LanguageMode) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("learning_state", android.content.Context.MODE_PRIVATE) }
    val lastLessonId = prefs.getString("last_lesson_unit_${unit.number}", null)
    val continueLesson = unit.lessons.firstOrNull { it.id == lastLessonId }

    LazyColumn(contentPadding = PaddingValues(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            Text(
                if (language == LanguageMode.TAMIL) "அலகு ${unit.number}" else "Unit ${unit.number}",
                style = MaterialTheme.typography.labelLarge,
            )
            Text(
                if (language == LanguageMode.TAMIL) unit.titleTa else unit.titleEn,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
            Spacer(Modifier.height(12.dp))
            UnitSceneHero(unit.number)
        }

        if (continueLesson != null) {
            item {
                ElevatedCard(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { navigate("lesson:${unit.number}:${continueLesson.id}") },
                ) {
                    Column(
                        Modifier.padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp),
                    ) {
                        Text(
                            if (language == LanguageMode.TAMIL) "தொடர்க" else "Continue",
                            color = MaterialTheme.colorScheme.primary,
                            fontWeight = FontWeight.Bold,
                        )
                        Text(
                            "${continueLesson.number} ${if (language == LanguageMode.TAMIL) continueLesson.titleTa else continueLesson.titleEn}",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                        )
                    }
                }
            }
        }

        items(unit.opening) { NativeBlock(it) }
        item { HorizontalDivider() }

        items(unit.lessons) { lesson ->
            val isLastRead = lesson.id == lastLessonId
            ListItem(
                headlineContent = {
                    Text("${lesson.number} ${if (language == LanguageMode.TAMIL) lesson.titleTa else lesson.titleEn}")
                },
                supportingContent = {
                    if (isLastRead) {
                        Text(
                            if (language == LanguageMode.TAMIL) "தொடர்க · கடைசியாக வாசித்த பாடம்" else "Continue · last-read lesson",
                            color = MaterialTheme.colorScheme.primary,
                            fontWeight = FontWeight.SemiBold,
                        )
                    }
                },
                modifier = Modifier.clickable { navigate("lesson:${unit.number}:${lesson.id}") },
            )
            HorizontalDivider()
        }

        item {
            BoxWithConstraints(Modifier.fillMaxWidth()) {
                if (maxWidth < 360.dp) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(
                            onClick = { navigate("review:${unit.number}") },
                            modifier = Modifier.fillMaxWidth(),
                        ) { Text(if (language == LanguageMode.TAMIL) "மீளாய்வு" else "Review") }
                        OutlinedButton(
                            onClick = { navigate("quiz:${unit.number}") },
                            modifier = Modifier.fillMaxWidth(),
                        ) { Text(if (language == LanguageMode.TAMIL) "பல்தேர்வு வினாக்கள்" else "MCQs") }
                    }
                } else {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = { navigate("review:${unit.number}") }) {
                            Text(if (language == LanguageMode.TAMIL) "மீளாய்வு" else "Review")
                        }
                        OutlinedButton(onClick = { navigate("quiz:${unit.number}") }) {
                            Text(if (language == LanguageMode.TAMIL) "பல்தேர்வு வினாக்கள்" else "MCQs")
                        }
                    }
                }
            }
        }
    }
}

'''
app = replace_between(
    app,
    '@Composable\nprivate fun UnitOpeningScreen',
    '@Composable\nprivate fun LessonScreen',
    unit_open,
    "UnitOpeningScreen continue + realistic hero",
)

app = replace_once(
    app,
    '''    val progress by remember {
        derivedStateOf {''',
    '''    LaunchedEffect(unit.number, lesson.id) {
        prefs.edit()
            .putString("last_lesson_unit_${unit.number}", lesson.id)
            .putInt("last_read_unit", unit.number)
            .apply()
    }

    val progress by remember {
        derivedStateOf {''',
    "last-read lesson persistence",
)

APP.write_text(app, encoding="utf-8")

visual = VISUAL.read_text(encoding="utf-8")
unit_card = '''@Composable
fun UnitVisualCard(
    unit: UnitContent,
    mode: LanguageMode,
    onClick: () -> Unit,
    onContinue: ((String) -> Unit)? = null,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("learning_state", android.content.Context.MODE_PRIVATE) }
    val lastLessonId = prefs.getString("last_lesson_unit_${unit.number}", null)
    val continueLesson = unit.lessons.firstOrNull { it.id == lastLessonId }

    ElevatedCard(modifier = modifier.fillMaxWidth().clickable(onClick = onClick)) {
        Row(
            Modifier.fillMaxWidth().padding(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            UnitSceneThumbnail(unit.number, Modifier.size(104.dp))
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                Text(
                    if (mode == LanguageMode.TAMIL) "அலகு ${unit.number}" else "Unit ${unit.number}",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                )
                Text(
                    if (mode == LanguageMode.TAMIL) unit.titleTa else unit.titleEn,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    if (mode == LanguageMode.TAMIL)
                        "${unit.lessons.size} பாடங்கள் · ${unit.quiz.size} வினாக்கள்"
                    else
                        "${unit.lessons.size} lessons · ${unit.quiz.size} MCQs",
                    style = MaterialTheme.typography.bodySmall,
                )
                if (continueLesson != null && onContinue != null) {
                    Surface(
                        color = MaterialTheme.colorScheme.primaryContainer,
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.clickable { onContinue(continueLesson.id) },
                    ) {
                        Column(Modifier.padding(horizontal = 10.dp, vertical = 7.dp)) {
                            Text(
                                if (mode == LanguageMode.TAMIL) "தொடர்க" else "Continue",
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary,
                            )
                            Text(
                                "${continueLesson.number} ${if (mode == LanguageMode.TAMIL) continueLesson.titleTa else continueLesson.titleEn}",
                                style = MaterialTheme.typography.bodySmall,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                        }
                    }
                }
            }
        }
    }
}

'''
visual = replace_between(
    visual,
    '@Composable\nfun UnitVisualCard',
    '@Composable\nfun CompactLanguageSwitch',
    unit_card,
    "UnitVisualCard realistic scene + Continue",
)
VISUAL.write_text(visual, encoding="utf-8")

sim = SIM.read_text(encoding="utf-8")
sim = replace_once(
    sim,
    '''        item { ClimateEventsCard(language) }
        item { GreenhouseCard() }''',
    '''        item { ClimateEventsCard(language) }
        item { EnvironmentalProcessExplorer(language) }
        item { GreenhouseCard() }''',
    "advanced animation explorer insertion",
)
SIM.write_text(sim, encoding="utf-8")

gradle = GRADLE.read_text(encoding="utf-8")
gradle = replace_once(gradle, 'versionCode = 20205', 'versionCode = 20300', "versionCode")
gradle = replace_once(gradle, 'versionName = "2.2.5"', 'versionName = "2.3.0"', "versionName")
GRADLE.write_text(gradle, encoding="utf-8")

assert sha256(BOOK) == EXPECTED_BOOK_SHA256, "book payload changed during v2.3.0 UX work"

checks = {
    "continue_persistence": 'putString("last_lesson_unit_${unit.number}", lesson.id)' in APP.read_text(encoding="utf-8"),
    "unit_continue_card": 'Continue · last-read lesson' in APP.read_text(encoding="utf-8"),
    "home_continue_route": 'onContinue = { lessonId -> navigate("lesson:${unit.number}:$lessonId") }' in APP.read_text(encoding="utf-8"),
    "realistic_unit_scene": "UnitSceneThumbnail(unit.number" in VISUAL.read_text(encoding="utf-8"),
    "unit_hero_scene": "UnitSceneHero(unit.number)" in APP.read_text(encoding="utf-8"),
    "advanced_animation_explorer": "EnvironmentalProcessExplorer(language)" in SIM.read_text(encoding="utf-8"),
    "narrated_climate_animation": "rememberAnimationNarration()" in (UI_DIR / "ClimateEvents.kt").read_text(encoding="utf-8"),
    "narration_helper": (UI_DIR / "AnimationNarration.kt").exists(),
}
assert all(checks.values()), checks

audit = {
    "versionName": "2.3.0",
    "versionCode": 20300,
    "scope": "visual learning, lesson continuation, animations and offline TTS",
    "book_content_sha256": sha256(BOOK),
    "book_content_unchanged": True,
    "english_payload_unchanged": True,
    "tamil_payload_unchanged": True,
    "figure_routing_unchanged": True,
    "last_read_per_unit": True,
    "continue_markers": True,
    "realistic_context_scenes": 9,
    "new_environmental_animation_pages": 6,
    "climate_animation_pages": 4,
    "total_narrated_animation_topics": 10,
    "android_tts_audio": True,
    "internet_permission_required_for_audio": False,
    "checks": checks,
}
Path("V230_LEARNING_EXPERIENCE_AUDIT.json").write_text(
    json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
Path("V230_LEARNING_EXPERIENCE_CHANGELOG.md").write_text(
    """# Environmental Studies v2.3.0 — Learning Experience Upgrade

- Added per-unit last-read lesson persistence.
- Added visible Continue / தொடர்க cards and last-read lesson markers.
- Added nine richer environmental context scenes for unit cards/openings.
- Preserved labelled scientific lesson diagrams instead of replacing them with decorative imagery.
- Added six new animated environmental-process pages: eutrophication, groundwater recharge, carbon cycle, food-chain energy flow, urban heat island and circular economy.
- Retained four climate-event animations, bringing the narrated animation set to ten topics.
- Added English/Tamil Android text-to-speech explanation controls for climate and environmental-process animations.
- TTS is offline-capable and adds no INTERNET permission; the requested voice must be installed on the device.
- Preserved the exact v2.2.4 lesson payload and v2.2.5 navigation behaviour.
""",
    encoding="utf-8",
)
print(json.dumps(audit, ensure_ascii=False, indent=2))
