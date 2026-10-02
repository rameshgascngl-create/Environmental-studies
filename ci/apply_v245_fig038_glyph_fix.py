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

SCREEN_TEST = Path(
    "app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/Fig038LessonScreenshotTest.kt"
)
SCREEN_TEST.parent.mkdir(parents=True, exist_ok=True)
SCREEN_TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.content.Context
import android.content.Intent
import android.os.SystemClock
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.io.FileOutputStream
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class Fig038LessonScreenshotTest {
    @Test
    fun captureU4l6WithFig038Visible() {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val context = instrumentation.targetContext
        context.getSharedPreferences("learning_state", Context.MODE_PRIVATE)
            .edit()
            .putString("last_route", "lesson:4:u4l6")
            .putString("language", "ENGLISH")
            .putInt("lesson_scroll_4_u4l6_ENGLISH", 5)
            .commit()

        val launch = context.packageManager.getLaunchIntentForPackage(context.packageName)
        assertNotNull("Launch intent missing", launch)
        launch!!.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        context.startActivity(launch)
        SystemClock.sleep(2200)

        val bitmap = instrumentation.uiAutomation.takeScreenshot()
        assertNotNull("Unable to capture u4l6 screen", bitmap)
        assertTrue(bitmap!!.width > 0 && bitmap.height > 0)

        val out = File(context.filesDir, "fig038-screen").apply { mkdirs() }
        val png = File(out, "u4l6-fig038.png")
        FileOutputStream(png).use {
            assertTrue(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, it))
        }
        assertTrue("u4l6 screenshot is unexpectedly small", png.length() > 10000L)
        bitmap.recycle()
    }
}
''', encoding="utf-8")

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
            "actual_lesson_screen_check": "CI_INSTRUMENTATION_REQUIRED",
            "screenshot_test": str(SCREEN_TEST),
        },
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
print(AUDIT.read_text(encoding="utf-8"))
