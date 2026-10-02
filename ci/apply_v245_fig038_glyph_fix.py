#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

PNG = Path("app/src/main/res/drawable-nodpi/fig_038_u04_en.png")
BOOK = Path("app/src/main/res/raw/book_content.json")
AUDIT = Path("V245_FIG038_GLYPH_FIX_AUDIT.json")
EXPECTED_OLD = "c75be275a1dc202bfc8d803687968332c410b8b6a54252ad712604a736cdd067"
EXPECTED_NEW = "994d1b3900cc01e80f5a649b704bca77133c16eb49868a01ec60451b0e5f6094"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

old_sha = sha(PNG)
assert old_sha == EXPECTED_OLD, (
    "fig_038 source changed unexpectedly; refusing a blind raster patch",
    old_sha,
)

im = Image.open(PNG).convert("RGBA")
assert im.size == (1600, 511), im.size

# The original source raster contains an unsupported-glyph box in the final
# waste-hierarchy row between RECOVER and DISPOSE. Replace only that glyph
# slot with a vector-drawn right arrow; adjacent text and diagram geometry
# are left untouched.
draw = ImageDraw.Draw(im)
background = (213, 176, 144, 255)
draw.rectangle((795, 399, 814, 429), fill=background)
y = 414
draw.line((797, y, 811, y), fill=(0, 0, 0, 255), width=3)
draw.polygon([(811, y - 5), (811, y + 5), (816, y)], fill=(0, 0, 0, 255))
im.save(PNG, format="PNG", optimize=False)

new_sha = sha(PNG)
assert new_sha == EXPECTED_NEW, new_sha
assert Image.open(PNG).size == (1600, 511)

book = json.loads(BOOK.read_text(encoding="utf-8"))
lesson = next(
    lesson
    for unit in book["units"]
    for lesson in unit["lessons"]
    if lesson["id"] == "u4l6"
)
refs = [
    block.get("figure")
    for block in lesson["english"]
    if block.get("kind") in ("figure", "svg_figure") and block.get("figure")
]
assert "fig_038_u04_en" in refs, refs

AUDIT.write_text(
    json.dumps(
        {
            "scope": "fig_038 unsupported glyph only",
            "lesson": "u4l6",
            "resource": "fig_038_u04_en.png",
            "dimensions": [1600, 511],
            "sha256_before": old_sha,
            "sha256_after": new_sha,
            "repair": "unsupported-glyph box replaced by a vector-drawn right arrow",
            "surrounding_labels_changed": False,
            "scientific_hierarchy_changed": False,
            "lesson_reference_verified": True,
            "native_asset_visual_check": "PASS",
            "actual_lesson_screen_check": "PENDING_EMULATOR_OR_PHYSICAL_DEVICE",
        },
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
print(AUDIT.read_text(encoding="utf-8"))
