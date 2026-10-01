from pathlib import Path

UI = Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui")
NAV = UI / "NavigationHost.kt"
HOME = UI / "HomeScreens.kt"
LESSON = UI / "LessonReader.kt"
QUIZ = UI / "QuizScreen.kt"
GRADLE = Path("app/build.gradle.kts")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def ensure_items_indexed_import(text: str) -> str:
    if "import androidx.compose.foundation.lazy.itemsIndexed" not in text:
        marker = "import androidx.compose.foundation.lazy.items\n"
        if marker in text:
            text = text.replace(marker, marker + "import androidx.compose.foundation.lazy.itemsIndexed\n", 1)
        else:
            package_end = text.index("\n", text.index("package ")) + 1
            text = text[:package_end] + "\nimport androidx.compose.foundation.lazy.itemsIndexed\n" + text[package_end:]
    return text


nav = NAV.read_text(encoding="utf-8")
nav = replace_once(
    nav,
    '''    val navigate: (String) -> Unit = { destination ->
        if (destination == "search") routeBeforeSearch = route
        learningState.setRoute(destination)
    }''',
    '''    val navigate: (String) -> Unit = remember(route, learningState) {
        { destination ->
            if (destination == "search") routeBeforeSearch = route
            learningState.setRoute(destination)
        }
    }''',
    "remembered navigation lambda",
)
nav = replace_once(
    nav,
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
    '''    val back: () -> Unit = remember(route, routeBeforeSearch, learningState) {
        {
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
        }
    }''',
    "remembered back lambda",
)
NAV.write_text(nav, encoding="utf-8")

home = ensure_items_indexed_import(HOME.read_text(encoding="utf-8"))
home = home.replace("items(book.units) { unit ->", "items(book.units, key = { it.number }) { unit ->")
home = home.replace("items(unit.lessons) { lesson ->", "items(unit.lessons, key = { it.id }) { lesson ->")
home = home.replace(
    "items(unit.opening) { NativeBlock(it) }",
    '''itemsIndexed(
            unit.opening,
            key = { index, block -> "unit:${unit.number}:opening:${block.kind}:$index" },
        ) { _, block ->
            NativeBlock(block)
        }''',
)
HOME.write_text(home, encoding="utf-8")

lesson = ensure_items_indexed_import(LESSON.read_text(encoding="utf-8"))
lesson = lesson.replace("items(unit.lessons) { l ->", "items(unit.lessons, key = { it.id }) { l ->")
lesson = lesson.replace(
    "items(englishBlocks) { NativeBlock(it) }",
    '''itemsIndexed(
                    englishBlocks,
                    key = { index, block -> "${lesson.id}:en:${block.kind}:$index" },
                ) { _, block -> NativeBlock(block) }''',
)
lesson = lesson.replace(
    "items(tamilBlocks) { NativeBlock(it) }",
    '''itemsIndexed(
                    tamilBlocks,
                    key = { index, block -> "${lesson.id}:ta:${block.kind}:$index" },
                ) { _, block -> NativeBlock(block) }''',
)
LESSON.write_text(lesson, encoding="utf-8")

quiz = QUIZ.read_text(encoding="utf-8")
quiz = replace_once(
    quiz,
    "itemsIndexed(unit.quiz) { index, q ->",
    '''itemsIndexed(
            items = unit.quiz,
            key = { index, q -> "${unit.number}:${q.questionEn.hashCode()}:$index" },
        ) { index, q ->''',
    "quiz stable key",
)
QUIZ.write_text(quiz, encoding="utf-8")

gradle = GRADLE.read_text(encoding="utf-8")
if "metricsDestination = layout.buildDirectory.dir" not in gradle:
    block = '''
composeCompiler {
    reportsDestination = layout.buildDirectory.dir("compose_compiler")
    metricsDestination = layout.buildDirectory.dir("compose_compiler")
}
'''
    dependency_marker = "\ndependencies {"
    position = gradle.find(dependency_marker)
    if position < 0:
        raise AssertionError("dependencies block not found")
    gradle = gradle[:position] + "\n" + block + gradle[position:]
GRADLE.write_text(gradle, encoding="utf-8")

assert "items(book.units, key = { it.number })" in home
assert "items(unit.lessons, key = { it.id })" in home
assert "items(unit.lessons, key = { it.id })" in lesson
assert 'key = { index, q ->' in quiz
assert "remember(route, learningState)" in nav
assert "metricsDestination" in gradle
assert "reportsDestination" in gradle
print("B3 added stable lazy-list keys, remembered navigation lambdas and Compose compiler reports.")
