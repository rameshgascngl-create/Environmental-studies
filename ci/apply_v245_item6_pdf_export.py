#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path.cwd()
PDF=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/PdfExporter.kt"
TEST=ROOT/"app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/PdfExporterRenderTest.kt"

def replace_once(text, old, new, label):
    count=text.count(old)
    assert count==1, f"{label}: expected one match, found {count}"
    return text.replace(old,new,1)

s=PDF.read_text(encoding="utf-8")
s=replace_once(
    s,
    '''import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
''',
    '''import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import androidx.core.content.res.ResourcesCompat
import com.caverock.androidsvg.SVG
import com.caverock.androidsvg.SVGExternalFileResolver
''',
    "PDF imports",
)
s=replace_once(
    s,
    '''import edu.gascnagercoil.environmentalsciences.model.ContentBlock
''',
    '''import edu.gascnagercoil.environmentalsciences.R
import edu.gascnagercoil.environmentalsciences.model.ContentBlock
''',
    "R import",
)
s=replace_once(
    s,
    '''        val document = PdfDocument()
        val normal = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = android.graphics.Color.BLACK
            textSize = 12f
            typeface = Typeface.create("sans-serif", Typeface.NORMAL)
        }
        val heading = Paint(normal).apply {
            textSize = 18f
            typeface = Typeface.create("sans-serif", Typeface.BOLD)
        }
        val subheading = Paint(normal).apply {
            textSize = 14f
            typeface = Typeface.create("sans-serif", Typeface.BOLD)
        }
''',
    '''        val document = PdfDocument()
        val bodyTypeface = if (mode == LanguageMode.TAMIL) {
            checkNotNull(ResourcesCompat.getFont(context, R.font.noto_sans_tamil)) {
                "Bundled Noto Sans Tamil font could not be loaded"
            }
        } else {
            Typeface.create("sans-serif", Typeface.NORMAL)
        }
        val normal = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = android.graphics.Color.BLACK
            textSize = 12f
            typeface = bodyTypeface
        }
        val heading = Paint(normal).apply {
            textSize = 18f
            typeface = Typeface.create(bodyTypeface, Typeface.BOLD)
        }
        val subheading = Paint(normal).apply {
            textSize = 14f
            typeface = Typeface.create(bodyTypeface, Typeface.BOLD)
        }
''',
    "bundled Tamil PDF font",
)
figure_anchor='''        fun drawFigure(block: ContentBlock) {
            val name = block.figure ?: return
            val resId = context.resources.getIdentifier(name, "drawable", context.packageName)
            if (resId == 0) return
            val bitmap = BitmapFactory.decodeResource(context.resources, resId) ?: return
            try {
                val maxWidth = PAGE_WIDTH - MARGIN * 2
                val maxHeight = 330f
                val scale = min(maxWidth / bitmap.width.toFloat(), maxHeight / bitmap.height.toFloat())
                val width = bitmap.width * scale
                val height = bitmap.height * scale
                ensureSpace(height + 34f)
                val left = (PAGE_WIDTH - width) / 2f
                val dst = android.graphics.RectF(left, y, left + width, y + height)
                page!!.canvas.drawBitmap(bitmap, null, dst, null)
                y += height + 8f
                if (block.caption.isNotBlank()) drawWrapped(block.caption, caption, 4f)
            } finally {
                bitmap.recycle()
            }
        }

'''
svg_renderer='''        fun drawSvgFigure(block: ContentBlock) {
            val name = block.figure?.trim().orEmpty()
            if (name.isBlank()) return
            val resId = context.resources.getIdentifier(name, "raw", context.packageName)
            if (resId == 0) return

            val tamilTypeface = ResourcesCompat.getFont(context, R.font.noto_sans_tamil)
            if (tamilTypeface != null) {
                SVG.registerExternalFileResolver(object : SVGExternalFileResolver() {
                    override fun resolveFont(fontFamily: String?, fontWeight: Int, fontStyle: String?): Typeface? =
                        if (fontFamily?.contains("Noto Sans Tamil", ignoreCase = true) == true) tamilTypeface else null
                })
            }

            val picture = runCatching {
                context.resources.openRawResource(resId).use { SVG.getFromInputStream(it).renderToPicture() }
            }.getOrNull() ?: return
            if (picture.width <= 0 || picture.height <= 0) return

            val maxWidth = PAGE_WIDTH - MARGIN * 2
            val maxHeight = 330f
            val scale = min(maxWidth / picture.width.toFloat(), maxHeight / picture.height.toFloat())
            val width = picture.width * scale
            val height = picture.height * scale
            ensureSpace(height + 34f)
            val left = (PAGE_WIDTH - width) / 2f
            val canvas = page!!.canvas
            val saveCount = canvas.save()
            canvas.translate(left, y)
            canvas.scale(scale, scale)
            canvas.drawPicture(picture)
            canvas.restoreToCount(saveCount)
            y += height + 8f
            if (block.caption.isNotBlank()) drawWrapped(block.caption, caption, 4f)
        }

'''
assert figure_anchor in s
s=s.replace(figure_anchor,figure_anchor+svg_renderer,1)
s=replace_once(
    s,
    '''            when (block.kind) {
                "figure" -> drawFigure(block)
                "table" -> {
''',
    '''            when (block.kind) {
                "figure" -> drawFigure(block)
                "svg_figure" -> drawSvgFigure(block)
                "table" -> {
''',
    "SVG PDF dispatch",
)
PDF.write_text(s,encoding="utf-8")

TEST.parent.mkdir(parents=True,exist_ok=True)
TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import edu.gascnagercoil.environmentalsciences.model.ContentBlock
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import edu.gascnagercoil.environmentalsciences.model.Lesson
import edu.gascnagercoil.environmentalsciences.model.UnitContent
import edu.gascnagercoil.environmentalsciences.ui.PdfExporter
import java.io.ByteArrayOutputStream
import java.io.OutputStream
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class PdfExporterRenderTest {
    private val context = ApplicationProvider.getApplicationContext<Context>()

    @Test
    fun exportsEnglishPngAndTamilSvg() {
        val unit = UnitContent(
            number = 2,
            titleEn = "Ecosystems and Natural Resources",
            titleTa = "சூழ்நிலை மண்டலங்கள் மற்றும் இயற்கை வளங்கள்",
            opening = emptyList(),
            lessons = emptyList(),
            review = emptyList(),
            quiz = emptyList(),
        )
        val englishFigure = ContentBlock(
            kind = "figure",
            title = "Energy flow",
            text = "",
            items = emptyList(),
            rows = emptyList(),
            figure = "fig_005_u02_en",
            caption = "Energy enters mainly as sunlight; nutrients are recycled through ecosystem processes.",
            alt = "Energy flow through an ecosystem",
        )
        val tamilFigure = ContentBlock(
            kind = "svg_figure",
            title = "சூழ்நிலை மண்டலத்தின் அமைப்பும் செயல்பாடும்",
            text = "",
            items = emptyList(),
            rows = emptyList(),
            figure = "sci_u02_l21_ecosystem_ta",
            caption = "ஆற்றல் பாய்கிறது; ஊட்டச்சத்துகள் மீண்டும் சுழல்கின்றன.",
            alt = "சூழ்நிலை மண்டலத்தின் அமைப்பும் செயல்பாடும்",
        )
        val lesson = Lesson(
            id = "pdfqa",
            number = "2.1",
            titleEn = "Ecosystems: Structure and Function",
            titleTa = "சூழ்நிலை மண்டலங்களின் அமைப்பும் செயல்பாடும்",
            english = listOf(englishFigure),
            tamil = listOf(tamilFigure),
        )
        val control = lesson.copy(english = emptyList(), tamil = emptyList())

        val english = render(unit, lesson, LanguageMode.ENGLISH)
        val englishControl = render(unit, control, LanguageMode.ENGLISH)
        val tamil = render(unit, lesson, LanguageMode.TAMIL)
        val tamilControl = render(unit, control, LanguageMode.TAMIL)

        assertTrue(english.startsWithPdfHeader())
        assertTrue(tamil.startsWithPdfHeader())
        assertTrue("English PNG did not contribute to PDF output", english.size > englishControl.size + 500)
        assertTrue("Tamil SVG did not contribute to PDF output", tamil.size > tamilControl.size + 500)

        val outDir = context.filesDir.resolve("pdf-qa").apply { mkdirs() }
        outDir.resolve("english-figure.pdf").writeBytes(english)
        outDir.resolve("tamil-svg.pdf").writeBytes(tamil)
    }

    private fun render(unit: UnitContent, lesson: Lesson, mode: LanguageMode): ByteArray {
        val output = ByteArrayOutputStream()
        val method = PdfExporter::class.java.getDeclaredMethod(
            "writeLesson",
            Context::class.java,
            OutputStream::class.java,
            UnitContent::class.java,
            Lesson::class.java,
            LanguageMode::class.java,
        )
        method.isAccessible = true
        method.invoke(PdfExporter, context, output, unit, lesson, mode)
        return output.toByteArray()
    }

    private fun ByteArray.startsWithPdfHeader(): Boolean =
        size >= 4 && this[0] == '%'.code.toByte() && this[1] == 'P'.code.toByte() &&
            this[2] == 'D'.code.toByte() && this[3] == 'F'.code.toByte()
}
''',encoding="utf-8")

checks={
    "svg_dispatch":'"svg_figure" -> drawSvgFigure(block)' in PDF.read_text(encoding="utf-8"),
    "androidsvg_picture":"renderToPicture()" in PDF.read_text(encoding="utf-8"),
    "pagination":"ensureSpace(height + 34f)" in PDF.read_text(encoding="utf-8"),
    "bundled_tamil_font":"R.font.noto_sans_tamil" in PDF.read_text(encoding="utf-8"),
    "pdf_instrumentation_test":TEST.is_file(),
}
assert all(checks.values()),checks
Path("V245_ITEM6_PDF_EXPORT_AUDIT.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")
print(json.dumps(checks,indent=2))
