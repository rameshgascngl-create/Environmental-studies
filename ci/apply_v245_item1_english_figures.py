#!/usr/bin/env python3
from pathlib import Path
import json

BOOK = Path("app/src/main/res/raw/book_content.json")
data = json.loads(BOOK.read_text(encoding="utf-8"))

fixes = {
    ("u2l1", 4): {
        "figure": "fig_005_u02_en",
        "title": "Energy enters ecosystems and nutrients are recycled",
        "alt": "Energy enters ecosystems and nutrients are recycled",
        "expected_text": "Energy enters mainly as sunlight; nutrients are recycled through ecosystem processes.",
    },
    ("u2l5", 4): {
        "figure": "fig_013_u02_en",
        "title": "The water cycle connects atmosphere, land and water",
        "alt": "The water cycle connects atmosphere, land and water",
        "expected_text": "Water continually moves between atmosphere, land, surface water and groundwater.",
    },
    ("u4l6", 4): {
        "figure": "fig_038_u04_en",
        "title": "Waste hierarchy: prevention before disposal",
        "alt": "Waste hierarchy: prevention before disposal",
        "expected_text": "Preferred actions are at the top; disposal is the last option.",
    },
    ("u5l1", 5): {
        "figure": "fig_046_u05_en",
        "title": "Simplified greenhouse effect",
        "alt": "Simplified greenhouse effect",
        "expected_text": "A simplified conceptual view of the greenhouse effect.",
    },
}

lessons = {lesson["id"]: lesson for unit in data["units"] for lesson in unit["lessons"]}
for (lesson_id, index), fix in fixes.items():
    lesson = lessons[lesson_id]
    block = lesson["english"][index]
    assert block["kind"] == "figure", (lesson_id, index, block.get("kind"))
    assert not block.get("figure"), (lesson_id, index, block.get("figure"))
    assert block.get("text") == fix["expected_text"], (lesson_id, index, block.get("text"))
    block["figure"] = fix["figure"]
    block["caption"] = block["text"]
    block["title"] = fix["title"]
    block["alt"] = fix["alt"]
    block["text"] = ""

BOOK.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for (lesson_id, index), fix in fixes.items():
    block = lessons[lesson_id]["english"][index]
    assert block["figure"] == fix["figure"]
    assert block["caption"] == fix["expected_text"]
    assert block["title"] == fix["title"]
    assert block["alt"] == fix["alt"]
    assert block["text"] == ""

print("ITEM1_ENGLISH_FIGURE_BLOCKS_PASS", len(fixes))
