from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT=Path.cwd()
REPO=ROOT.parent.parent
UI=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui"
THEME=UI/"theme"
RAW=ROOT/"app/src/main/res/raw"
FONT_DIR=ROOT/"app/src/main/res/font"
OVERLAY=REPO/"overlay/v2.4/app/src/main/res"
FONT_SRC=OVERLAY/"font/noto_sans_tamil.ttf"
LICENCE_SRC=OVERLAY/"raw/noto_sans_tamil_ofl.txt"
FONT_DST=FONT_DIR/"noto_sans_tamil.ttf"
LICENCE_DST=RAW/"noto_sans_tamil_ofl.txt"

if not FONT_SRC.is_file() or not LICENCE_SRC.is_file():
    raise SystemExit("Task C3 overlay font or OFL licence is missing")
FONT_DIR.mkdir(parents=True,exist_ok=True)
shutil.copy2(FONT_SRC,FONT_DST)
shutil.copy2(LICENCE_SRC,LICENCE_DST)

typography=THEME/"TamilTypography.kt"
typography.write_text(r'''package edu.gascnagercoil.environmentalsciences.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import edu.gascnagercoil.environmentalsciences.R

/**
 * Bundled OFL font used by Compose so Tamil rendering does not depend on the
 * device vendor's optional font set. The same font is resolved explicitly for
 * Tamil text inside AndroidSVG diagrams.
 */
internal val NotoSansTamilFamily = FontFamily(
    Font(R.font.noto_sans_tamil)
)

private val BaseTypography = Typography()

internal val AppTypography = Typography(
    displayLarge = BaseTypography.displayLarge.copy(fontFamily = NotoSansTamilFamily),
    displayMedium = BaseTypography.displayMedium.copy(fontFamily = NotoSansTamilFamily),
    displaySmall = BaseTypography.displaySmall.copy(fontFamily = NotoSansTamilFamily),
    headlineLarge = BaseTypography.headlineLarge.copy(fontFamily = NotoSansTamilFamily),
    headlineMedium = BaseTypography.headlineMedium.copy(fontFamily = NotoSansTamilFamily),
    headlineSmall = BaseTypography.headlineSmall.copy(fontFamily = NotoSansTamilFamily),
    titleLarge = BaseTypography.titleLarge.copy(fontFamily = NotoSansTamilFamily),
    titleMedium = BaseTypography.titleMedium.copy(fontFamily = NotoSansTamilFamily),
    titleSmall = BaseTypography.titleSmall.copy(fontFamily = NotoSansTamilFamily),
    bodyLarge = BaseTypography.bodyLarge.copy(fontFamily = NotoSansTamilFamily),
    bodyMedium = BaseTypography.bodyMedium.copy(fontFamily = NotoSansTamilFamily),
    bodySmall = BaseTypography.bodySmall.copy(fontFamily = NotoSansTamilFamily),
    labelLarge = BaseTypography.labelLarge.copy(fontFamily = NotoSansTamilFamily),
    labelMedium = BaseTypography.labelMedium.copy(fontFamily = NotoSansTamilFamily),
    labelSmall = BaseTypography.labelSmall.copy(fontFamily = NotoSansTamilFamily),
)
''',encoding="utf-8")

theme=THEME/"Theme.kt"
theme_text=theme.read_text(encoding="utf-8")
if "typography = AppTypography" not in theme_text:
    anchor="        colorScheme = if (isSystemInDarkTheme()) Dark else Light,\n"
    if theme_text.count(anchor)!=1:
        raise SystemExit("Theme typography insertion anchor changed")
    theme_text=theme_text.replace(anchor,anchor+"        typography = AppTypography,\n")
    theme.write_text(theme_text,encoding="utf-8")

svg_file=UI/"SvgFigureBlock.kt"
svg=svg_file.read_text(encoding="utf-8")
if "SVGExternalFileResolver" not in svg:
    svg=svg.replace(
        "import android.graphics.drawable.PictureDrawable\n",
        "import android.content.Context\nimport android.graphics.Typeface\nimport android.graphics.drawable.PictureDrawable\n"
    )
    svg=svg.replace(
        "import android.widget.ImageView\n",
        "import android.widget.ImageView\nimport androidx.core.content.res.ResourcesCompat\n"
    )
    svg=svg.replace(
        "import com.caverock.androidsvg.SVG\n",
        "import com.caverock.androidsvg.SVG\nimport com.caverock.androidsvg.SVGExternalFileResolver\nimport edu.gascnagercoil.environmentalsciences.R\n"
    )
    marker="import edu.gascnagercoil.environmentalsciences.model.ContentBlock\n\n"
    resolver=r'''private val tamilSvgFontLock = Any()
@Volatile private var tamilSvgFontInstalled = false

private fun ensureTamilSvgFontResolver(context: Context) {
    if (tamilSvgFontInstalled) return
    synchronized(tamilSvgFontLock) {
        if (tamilSvgFontInstalled) return
        val typeface = ResourcesCompat.getFont(context.applicationContext, R.font.noto_sans_tamil)
            ?: error("Bundled Noto Sans Tamil font could not be loaded")
        SVG.registerExternalFileResolver(object : SVGExternalFileResolver() {
            override fun resolveFont(fontFamily: String?, fontWeight: Int, fontStyle: String?): Typeface? =
                if (fontFamily?.contains("Noto Sans Tamil", ignoreCase = true) == true) typeface else null
        })
        tamilSvgFontInstalled = true
    }
}

'''
    if svg.count(marker)!=1:
        raise SystemExit("SvgFigureBlock resolver insertion anchor changed")
    svg=svg.replace(marker,marker+resolver)
    parse_anchor='    val picture = remember(resId) {\n        context.resources.openRawResource(resId).use { SVG.getFromInputStream(it).renderToPicture() }\n    }'
    parse_repl='    val picture = remember(resId) {\n        ensureTamilSvgFontResolver(context)\n        context.resources.openRawResource(resId).use { SVG.getFromInputStream(it).renderToPicture() }\n    }'
    if svg.count(parse_anchor)!=1:
        raise SystemExit("SvgFigureBlock parse anchor changed")
    svg=svg.replace(parse_anchor,parse_repl)
    svg_file.write_text(svg,encoding="utf-8")

tamil_svgs=sorted(RAW.glob("sci_*_ta.svg"))
all_svgs=sorted(RAW.glob("sci_*.svg"))
for p in tamil_svgs:
    text=p.read_text(encoding="utf-8")
    text=text.replace('font-family="sans-serif"','font-family="Noto Sans Tamil"')
    text=text.replace("font-family:sans-serif","font-family:Noto Sans Tamil")
    p.write_text(text,encoding="utf-8")

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

report={
    "task":"C3 bundled Tamil font",
    "font_family":"Noto Sans Tamil",
    "font_sha256":sha(FONT_DST),
    "ofl_sha256":sha(LICENCE_DST),
    "font_bytes":FONT_DST.stat().st_size,
    "compose_font_family_declared":"NotoSansTamilFamily" in typography.read_text(encoding="utf-8"),
    "compose_typography_applied":"typography = AppTypography" in theme.read_text(encoding="utf-8"),
    "androidsvg_1_4_resolver_registered":"SVG.registerExternalFileResolver" in svg_file.read_text(encoding="utf-8"),
    "tamil_svg_count":len(tamil_svgs),
    "all_svg_count":len(all_svgs),
    "tamil_svgs_explicit_font_count":sum("Noto Sans Tamil" in p.read_text(encoding="utf-8") for p in tamil_svgs),
    "licence_bundled":LICENCE_DST.is_file(),
}
if report["tamil_svg_count"]!=18 or report["all_svg_count"]!=36:
    raise SystemExit(report)
if report["tamil_svgs_explicit_font_count"]!=18:
    raise SystemExit("Not all Tamil SVGs explicitly reference Noto Sans Tamil")
if not all([report["compose_font_family_declared"],report["compose_typography_applied"],report["androidsvg_1_4_resolver_registered"],report["licence_bundled"]]):
    raise SystemExit(report)

Path("V240_C3_TAMIL_FONT_AUDIT.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(report,ensure_ascii=False,indent=2))
