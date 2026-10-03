#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

ROOT = Path.cwd()
VISUAL = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/VisualLearning.kt"
HOME = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/HomeScreens.kt"
BOOK = ROOT / "app/src/main/res/raw/book_content.json"
GRADLE = ROOT / "app/build.gradle.kts"
OUT = ROOT / "V246_VISUAL_ATLAS_TAP_AUDIT.json"

EXPECTED_BOOK_SHA256 = "e0d152e9c51be5bb095ba11c8fdc171467eb594ec75fe17158a9bada0a8ea8d4"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha256(BOOK) == EXPECTED_BOOK_SHA256, "validated v2.4.6 book payload changed before Visual Atlas tap fix"

visual = VISUAL.read_text(encoding="utf-8")
home = HOME.read_text(encoding="utf-8")
gradle = GRADLE.read_text(encoding="utf-8")

old_model = 'private data class VisualItem(val en: String, val ta: String, val unitNumber: Int)'
new_model = 'private data class VisualItem(val en: String, val ta: String, val unitNumber: Int, val lessonId: String)'
assert old_model in visual, "VisualItem model anchor missing"
visual = visual.replace(old_model, new_model, 1)

old_items = '''private val visualItems = listOf(
    VisualItem("Greenhouse effect", "பசுமைக்குடில் விளைவு", 5),
    VisualItem("Biodiversity", "உயிரிய பல்வகைத்தன்மை", 3),
    VisualItem("Pollution pathways", "மாசுபாட்டு வழித்தடங்கள்", 4),
    VisualItem("Circular economy", "சுழற்சிப் பொருளாதாரம்", 6),
)'''
new_items = '''private val visualItems = listOf(
    VisualItem("Greenhouse effect", "பசுமைக்குடில் விளைவு", 5, "u5l1"),
    VisualItem("Biodiversity", "உயிரிய பல்வகைத்தன்மை", 3, "u3l1"),
    VisualItem("Pollution pathways", "மாசுபாட்டு வழித்தடங்கள்", 4, "u4l1"),
    VisualItem("Circular economy", "சுழற்சிப் பொருளாதாரம்", 6, "u6l4"),
)'''
assert old_items in visual, "Visual Atlas item registry anchor missing"
visual = visual.replace(old_items, new_items, 1)

old_signature = 'fun VisualHighlights(mode: LanguageMode, modifier: Modifier = Modifier) {'
new_signature = 'fun VisualHighlights(mode: LanguageMode, onOpen: (Int, String) -> Unit, modifier: Modifier = Modifier) {'
assert old_signature in visual, "VisualHighlights signature anchor missing"
visual = visual.replace(old_signature, new_signature, 1)

old_card = 'OutlinedCard(Modifier.size(width = 260.dp, height = 210.dp)) {'
new_card = '''OutlinedCard(
                    Modifier
                        .size(width = 260.dp, height = 210.dp)
                        .clickable { onOpen(item.unitNumber, item.lessonId) }
                ) {'''
assert old_card in visual, "Visual Atlas card anchor missing"
visual = visual.replace(old_card, new_card, 1)

old_home = 'item { VisualHighlights(language) }'
new_home = '''item {
            VisualHighlights(
                mode = language,
                onOpen = { unitNumber, lessonId ->
                    navigate("lesson:$unitNumber:$lessonId")
                },
            )
        }'''
assert old_home in home, "Home VisualHighlights call anchor missing"
home = home.replace(old_home, new_home, 1)

VISUAL.write_text(visual, encoding="utf-8")
HOME.write_text(home, encoding="utf-8")

assert sha256(BOOK) == EXPECTED_BOOK_SHA256, "book payload changed during Visual Atlas tap fix"
assert 'versionCode = 20405' in gradle and 'versionName = "2.4.5"' in gradle, "version identifiers changed"

visual_after = VISUAL.read_text(encoding="utf-8")
home_after = HOME.read_text(encoding="utf-8")
routes = {
    "Greenhouse effect": "lesson:5:u5l1",
    "Biodiversity": "lesson:3:u3l1",
    "Pollution pathways": "lesson:4:u4l1",
    "Circular economy": "lesson:6:u6l4",
}
checks = {
    "whole_card_clickable": '.clickable { onOpen(item.unitNumber, item.lessonId) }' in visual_after,
    "visual_items_have_lesson_ids": all(lesson_id in visual_after for lesson_id in ("u5l1", "u3l1", "u4l1", "u6l4")),
    "home_routes_visual_cards_to_lessons": 'navigate("lesson:$unitNumber:$lessonId")' in home_after,
    "home_passes_named_on_open_callback": 'onOpen = { unitNumber, lessonId ->' in home_after,
    "callback_is_typed": 'onOpen: (Int, String) -> Unit' in visual_after,
    "book_content_unchanged": sha256(BOOK) == EXPECTED_BOOK_SHA256,
    "version_identifiers_unchanged": 'versionCode = 20405' in gradle and 'versionName = "2.4.5"' in gradle,
}
assert all(checks.values()), checks

OUT.write_text(
    json.dumps(
        {
            "scope": "v2.4.6 Home Visual Atlas tap navigation only",
            "defect": "Visual Atlas cards rendered without any click handler",
            "resolution": "Entire card is clickable and routes to the concept's related lesson",
            "routes": routes,
            "bookContentSha256": sha256(BOOK),
            "scientificContentChanged": False,
            "quizPayloadChanged": False,
            "figureAssetsChanged": False,
            "packageIdentityChanged": False,
            "signingChanged": False,
            "versionName": "2.4.5",
            "versionCode": 20405,
            "checks": checks,
            "status": "PASS",
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
print(OUT.read_text(encoding="utf-8"))
