#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT=Path.cwd()
NAV=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/NavigationHost.kt"
SVG=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/SvgFigureBlock.kt"
NATIVE=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/NativeContent.kt"
BOOK=ROOT/"app/src/main/res/raw/book_content.json"
EXPECTED_BOOK_SHA256="b968c3e8cab017cf40e284c40dceece7fc74173c3f69f39836b67c071be9d360"

def sha256(p: Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert sha256(BOOK)==EXPECTED_BOOK_SHA256, "validated book payload changed before lesson/figure UI correction"

nav=NAV.read_text(encoding="utf-8")
old='''                            Text("Environmental Studies", maxLines = 1, overflow = TextOverflow.Ellipsis)
                            if (wide && !focusMode) Text("சுற்றுச்சூழல் ஆய்வுகள்", style = MaterialTheme.typography.labelMedium)'''
new='''                            Text(
                                if (inLesson) {
                                    if (language == LanguageMode.TAMIL) "பாடம்" else "Lesson"
                                } else {
                                    "Environmental Studies"
                                },
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            if (wide && !focusMode && !inLesson) Text("சுற்றுச்சூழல் ஆய்வுகள்", style = MaterialTheme.typography.labelMedium)'''
assert old in nav, "lesson top-app-bar anchor missing"
NAV.write_text(nav.replace(old,new,1),encoding="utf-8")

svg=SVG.read_text(encoding="utf-8")
insert_after='''private fun svgAriaLabel(context: Context, resId: Int): String? {
    val parser = android.util.Xml.newPullParser()
    context.resources.openRawResource(resId).use { input ->
        parser.setInput(input, Charsets.UTF_8.name())
        while (parser.eventType != XmlPullParser.END_DOCUMENT) {
            if (parser.eventType == XmlPullParser.START_TAG && parser.name == "svg") {
                return parser.getAttributeValue(null, "aria-label")?.takeIf { it.isNotBlank() }
            }
            parser.next()
        }
    }
    return null
}
'''
aspect_helper='''
private fun svgAspectRatio(context: Context, resId: Int): Float {
    val parser = android.util.Xml.newPullParser()
    context.resources.openRawResource(resId).use { input ->
        parser.setInput(input, Charsets.UTF_8.name())
        while (parser.eventType != XmlPullParser.END_DOCUMENT) {
            if (parser.eventType == XmlPullParser.START_TAG && parser.name == "svg") {
                val parts = parser.getAttributeValue(null, "viewBox")
                    ?.trim()
                    ?.split(Regex("\\\\s+"))
                    ?.mapNotNull { it.toFloatOrNull() }
                if (parts != null && parts.size == 4 && parts[3] > 0f) {
                    return (parts[2] / parts[3]).coerceIn(1f, 2.4f)
                }
                break
            }
            parser.next()
        }
    }
    return 16f / 10f
}
'''
assert insert_after in svg, "SVG metadata helper anchor missing"
svg=svg.replace(insert_after,insert_after+aspect_helper,1)

old='''    val minimumDisplayWidthDp = if (block.figure in largeSvgCanvasResources) 600 else 400
    val availableDisplayWidthDp = (LocalConfiguration.current.screenWidthDp - 56).coerceIn(280, 900)
    val svgDisplayWidth = maxOf(minimumDisplayWidthDp, availableDisplayWidthDp).dp
    val svgScroll = rememberScrollState()
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        if (block.title.isNotBlank()) Text(block.title, style = MaterialTheme.typography.titleMedium)
        ElevatedCard(onClick = { expanded = true }, modifier = Modifier.fillMaxWidth()) {
            Box(Modifier.fillMaxWidth().horizontalScroll(svgScroll)) {
                SvgResource(
                    resId = resId,
                    description = figureDescription,
                    modifier = Modifier
                        .width(svgDisplayWidth)
                        .heightIn(min = 220.dp, max = 380.dp)
                        .padding(8.dp)
                )
            }
        }
'''
new='''    val figureAspectRatio = remember(resId) { svgAspectRatio(context, resId) }
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        if (block.title.isNotBlank()) Text(block.title, style = MaterialTheme.typography.titleMedium)
        ElevatedCard(onClick = { expanded = true }, modifier = Modifier.fillMaxWidth()) {
            Box(Modifier.fillMaxWidth().padding(4.dp)) {
                SvgResource(
                    resId = resId,
                    description = figureDescription,
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(figureAspectRatio)
                        .padding(8.dp)
                )
            }
        }
'''
assert old in svg, "inline SVG fixed-width scroll anchor missing"
svg=svg.replace(old,new,1)
old='''            var scale by remember(resId) { mutableFloatStateOf(readingScale) }'''
assert old in svg, "SVG dialog initial-scale anchor missing"
svg=svg.replace(old,'''            var scale by remember(resId) { mutableFloatStateOf(1f) }''',1)
SVG.write_text(svg,encoding="utf-8")

native=NATIVE.read_text(encoding="utf-8")
old='''    val readingScale = if (wideFigure) 1.65f else 1.2f
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current'''
new='''    val readingScale = if (wideFigure) 1.65f else 1.2f
    val readingScaleLabel = if (wideFigure) "1.65×" else "1.2×"
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current'''
assert old in native, "raster reading-scale anchor missing"
native=native.replace(old,new,1)
old='''            var scale by remember(resId) { mutableFloatStateOf(readingScale) }'''
assert old in native, "raster dialog initial-scale anchor missing"
native=native.replace(old,'''            var scale by remember(resId) { mutableFloatStateOf(1f) }''',1)

literal = r'Text("\${readingScale}×")'
old='''                    TextButton(onClick = { setScale(readingScale) }) { ''' + literal + ''' }'''
assert old in native, "literal readingScale label anchor missing"
native=native.replace(old,'''                    TextButton(onClick = { setScale(readingScale) }) { Text(readingScaleLabel) }''',1)
NATIVE.write_text(native,encoding="utf-8")

assert sha256(BOOK)==EXPECTED_BOOK_SHA256, "book payload changed during lesson/figure UI correction"

literal_check = r'Text("\${readingScale}×")'
checks={
    "lesson_top_bar_contextual": '"பாடம்" else "Lesson"' in NAV.read_text(),
    "inline_svg_fit_whole_plate": ".aspectRatio(figureAspectRatio)" in SVG.read_text(),
    "inline_svg_fixed_width_removed": "svgDisplayWidth" not in SVG.read_text(),
    "svg_dialog_opens_at_1x": "mutableFloatStateOf(1f)" in SVG.read_text(),
    "raster_dialog_opens_at_1x": "mutableFloatStateOf(1f)" in NATIVE.read_text(),
    "raster_reading_scale_literal_fixed": 'Text(readingScaleLabel)' in NATIVE.read_text(),
    "literal_template_absent": literal_check not in NATIVE.read_text(),
}
assert all(checks.values()),checks
Path("V245_LESSON_FIGURE_UI_AUDIT.json").write_text(json.dumps({
    "scope":"lesson app-bar and scientific figure presentation only",
    "versionName":"2.4.5",
    "versionCode":20405,
    "book_content_sha256":sha256(BOOK),
    "book_content_unchanged":True,
    "scientific_content_changed":False,
    "svg_asset_bytes_changed":False,
    "tamil_lesson_payload_changed":False,
    "quiz_payload_changed":False,
    "package_identity_changed":False,
    "signing_changed":False,
    "checks":checks,
},ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
print(json.dumps(checks,indent=2))
