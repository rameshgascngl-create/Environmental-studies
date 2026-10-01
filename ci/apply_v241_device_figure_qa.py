from __future__ import annotations

from pathlib import Path
import json

ROOT = Path.cwd()
APP = ROOT / "app"
UI = APP / "src/main/java/edu/gascnagercoil/environmentalsciences/ui"
NATIVE = UI / "NativeContent.kt"
SVG = UI / "SvgFigureBlock.kt"
GRADLE = APP / "build.gradle.kts"
BOOK = APP / "src/main/res/raw/book_content.json"

native = NATIVE.read_text(encoding="utf-8")
if "DialogProperties(usePlatformDefaultWidth = false)" not in native:
    native = native.replace(
        "import androidx.compose.ui.draw.clip\n",
        "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.clipToBounds\n",
    )
    native = native.replace(
        "import androidx.compose.ui.input.pointer.pointerInput\n",
        "import androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.ui.layout.onSizeChanged\n",
    )
    native = native.replace(
        "import androidx.compose.ui.unit.dp\n",
        "import androidx.compose.ui.unit.IntSize\nimport androidx.compose.ui.unit.dp\n",
    )
    native = native.replace(
        "import androidx.compose.ui.window.Dialog\n",
        "import androidx.compose.ui.window.Dialog\nimport androidx.compose.ui.window.DialogProperties\n",
    )

    old = '''@Composable
private fun ZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {
    Dialog(onDismissRequest = dismiss) {
        Surface(
            modifier = Modifier.fillMaxWidth().fillMaxHeight(0.9f),
            shape = RoundedCornerShape(18.dp),
            tonalElevation = 6.dp
        ) {
            var scale by remember { mutableFloatStateOf(1f) }
            var offsetX by remember { mutableFloatStateOf(0f) }
            var offsetY by remember { mutableFloatStateOf(0f) }
            Box(Modifier.fillMaxSize()) {
                Image(
                    painter = painterResource(resId),
                    contentDescription = description,
                    contentScale = ContentScale.Fit,
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(12.dp)
                        .pointerInput(Unit) {
                            detectTransformGestures { _, pan, zoom, _ ->
                                scale = (scale * zoom).coerceIn(1f, 5f)
                                offsetX += pan.x
                                offsetY += pan.y
                            }
                        }
                        .graphicsLayer(
                            scaleX = scale,
                            scaleY = scale,
                            translationX = offsetX,
                            translationY = offsetY
                        )
                )
                TextButton(onClick = dismiss, modifier = Modifier.align(Alignment.TopEnd).padding(8.dp)) {
                    Text("Close")
                }
            }
        }
    }
}
'''
    new = '''@Composable
private fun ZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {
    val painter = painterResource(resId)
    val intrinsic = painter.intrinsicSize
    val wideFigure = intrinsic.width > 0f && intrinsic.height > 0f && intrinsic.width > intrinsic.height * 1.25f
    val readingScale = if (wideFigure) 1.65f else 1.2f
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current
    val viewerHeightFraction = if (configuration.screenWidthDp > configuration.screenHeightDp) 0.94f else 0.72f

    Dialog(
        onDismissRequest = dismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(viewerHeightFraction)
                .padding(horizontal = 8.dp),
            shape = RoundedCornerShape(18.dp),
            tonalElevation = 6.dp
        ) {
            var scale by remember(resId) { mutableFloatStateOf(readingScale) }
            var offsetX by remember(resId) { mutableFloatStateOf(0f) }
            var offsetY by remember(resId) { mutableFloatStateOf(0f) }
            var viewportSize by remember { mutableStateOf(IntSize.Zero) }

            fun setScale(target: Float) {
                scale = target.coerceIn(1f, 5f)
                offsetX = 0f
                offsetY = 0f
            }

            Column(Modifier.fillMaxSize()) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp),
                    horizontalArrangement = Arrangement.End,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    TextButton(onClick = { setScale(1f) }) { Text("1×") }
                    TextButton(onClick = { setScale(readingScale) }) { Text("\${readingScale}×") }
                    TextButton(onClick = dismiss) { Text("Close / மூடு") }
                }
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .clipToBounds()
                        .onSizeChanged { viewportSize = it },
                    contentAlignment = Alignment.Center
                ) {
                    Image(
                        painter = painter,
                        contentDescription = description,
                        contentScale = ContentScale.Fit,
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(8.dp)
                            .pointerInput(viewportSize) {
                                detectTransformGestures { _, pan, zoom, _ ->
                                    val nextScale = (scale * zoom).coerceIn(1f, 5f)
                                    if (nextScale <= 1.001f) {
                                        scale = 1f
                                        offsetX = 0f
                                        offsetY = 0f
                                    } else {
                                        val maxX = viewportSize.width * (nextScale - 1f) / 2f
                                        val maxY = viewportSize.height * (nextScale - 1f) / 2f
                                        offsetX = (offsetX + pan.x).coerceIn(-maxX, maxX)
                                        offsetY = (offsetY + pan.y).coerceIn(-maxY, maxY)
                                        scale = nextScale
                                    }
                                }
                            }
                            .graphicsLayer(
                                scaleX = scale,
                                scaleY = scale,
                                translationX = offsetX,
                                translationY = offsetY
                            )
                    )
                }
                Text(
                    "Pinch to zoom · Drag to pan  •  விரித்து பெரிதாக்கவும் · இழுத்து நகர்த்தவும்",
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp)
                )
            }
        }
    }
}
'''
    if native.count(old) != 1:
        raise SystemExit("Native ZoomDialog anchor changed")
    native = native.replace(old, new)
    NATIVE.write_text(native, encoding="utf-8")

svg = SVG.read_text(encoding="utf-8")
if "DialogProperties(usePlatformDefaultWidth = false)" not in svg:
    svg = svg.replace(
        "import androidx.compose.ui.graphics.graphicsLayer\n",
        "import androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.draw.clipToBounds\n",
    )
    svg = svg.replace(
        "import androidx.compose.ui.input.pointer.pointerInput\n",
        "import androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.ui.layout.onSizeChanged\n",
    )
    svg = svg.replace(
        "import androidx.compose.ui.unit.dp\n",
        "import androidx.compose.ui.unit.IntSize\nimport androidx.compose.ui.unit.dp\n",
    )
    svg = svg.replace(
        "import androidx.compose.ui.window.Dialog\n",
        "import androidx.compose.ui.window.Dialog\nimport androidx.compose.ui.window.DialogProperties\n",
    )

    old = '''@Composable
private fun SvgZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {
    Dialog(onDismissRequest = dismiss) {
        Surface(modifier = Modifier.fillMaxWidth().fillMaxHeight(0.9f), shape = MaterialTheme.shapes.large) {
            var scale by remember { mutableFloatStateOf(1f) }
            var offsetX by remember { mutableFloatStateOf(0f) }
            var offsetY by remember { mutableFloatStateOf(0f) }
            Box(Modifier.fillMaxSize()) {
                SvgResource(
                    resId = resId,
                    description = description,
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(12.dp)
                        .pointerInput(Unit) {
                            detectTransformGestures { _, pan, zoom, _ ->
                                scale = (scale * zoom).coerceIn(1f, 5f)
                                offsetX += pan.x
                                offsetY += pan.y
                            }
                        }
                        .graphicsLayer(scaleX = scale, scaleY = scale, translationX = offsetX, translationY = offsetY)
                )
                TextButton(onClick = dismiss, modifier = Modifier.align(androidx.compose.ui.Alignment.TopEnd).padding(8.dp)) { Text("Close") }
            }
        }
    }
}
'''
    new = '''@Composable
private fun SvgZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {
    val readingScale = 1.65f
    val configuration = LocalConfiguration.current
    val viewerHeightFraction = if (configuration.screenWidthDp > configuration.screenHeightDp) 0.94f else 0.72f

    Dialog(
        onDismissRequest = dismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(viewerHeightFraction)
                .padding(horizontal = 8.dp),
            shape = MaterialTheme.shapes.large
        ) {
            var scale by remember(resId) { mutableFloatStateOf(readingScale) }
            var offsetX by remember(resId) { mutableFloatStateOf(0f) }
            var offsetY by remember(resId) { mutableFloatStateOf(0f) }
            var viewportSize by remember { mutableStateOf(IntSize.Zero) }

            fun setScale(target: Float) {
                scale = target.coerceIn(1f, 5f)
                offsetX = 0f
                offsetY = 0f
            }

            Column(Modifier.fillMaxSize()) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp),
                    horizontalArrangement = Arrangement.End,
                    verticalAlignment = androidx.compose.ui.Alignment.CenterVertically
                ) {
                    TextButton(onClick = { setScale(1f) }) { Text("1×") }
                    TextButton(onClick = { setScale(readingScale) }) { Text("1.65×") }
                    TextButton(onClick = dismiss) { Text("Close / மூடு") }
                }
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .clipToBounds()
                        .onSizeChanged { viewportSize = it },
                    contentAlignment = androidx.compose.ui.Alignment.Center
                ) {
                    SvgResource(
                        resId = resId,
                        description = description,
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(8.dp)
                            .pointerInput(viewportSize) {
                                detectTransformGestures { _, pan, zoom, _ ->
                                    val nextScale = (scale * zoom).coerceIn(1f, 5f)
                                    if (nextScale <= 1.001f) {
                                        scale = 1f
                                        offsetX = 0f
                                        offsetY = 0f
                                    } else {
                                        val maxX = viewportSize.width * (nextScale - 1f) / 2f
                                        val maxY = viewportSize.height * (nextScale - 1f) / 2f
                                        offsetX = (offsetX + pan.x).coerceIn(-maxX, maxX)
                                        offsetY = (offsetY + pan.y).coerceIn(-maxY, maxY)
                                        scale = nextScale
                                    }
                                }
                            }
                            .graphicsLayer(
                                scaleX = scale,
                                scaleY = scale,
                                translationX = offsetX,
                                translationY = offsetY
                            )
                    )
                }
                Text(
                    "Pinch to zoom · Drag to pan  •  விரித்து பெரிதாக்கவும் · இழுத்து நகர்த்தவும்",
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp)
                )
            }
        }
    }
}
'''
    if svg.count(old) != 1:
        raise SystemExit("SVG ZoomDialog anchor changed")
    svg = svg.replace(old, new)
    SVG.write_text(svg, encoding="utf-8")

gradle = GRADLE.read_text(encoding="utf-8")
if 'versionCode = 20400' not in gradle or 'versionName = "2.4.0"' not in gradle:
    raise SystemExit("v2.4.0 identity anchor changed")
gradle = gradle.replace('versionCode = 20400', 'versionCode = 20401')
gradle = gradle.replace('versionName = "2.4.0"', 'versionName = "2.4.1"')
GRADLE.write_text(gradle, encoding="utf-8")

book = json.loads(BOOK.read_text(encoding="utf-8"))
if book.get("nativeVersion") != "2.4.0":
    raise SystemExit(f"Unexpected nativeVersion: {book.get('nativeVersion')}")
book["nativeVersion"] = "2.4.1"
BOOK.write_text(json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

native_now = NATIVE.read_text(encoding="utf-8")
svg_now = SVG.read_text(encoding="utf-8")
gradle_now = GRADLE.read_text(encoding="utf-8")
book_now = json.loads(BOOK.read_text(encoding="utf-8"))

report = {
    "versionName": "2.4.1",
    "versionCode": 20401,
    "device_qa_trigger": "v2.4.0 screenshots showed large dead dialog space and unreadably small labels in expanded landscape PNG/SVG figures at default fit scale",
    "platform_default_dialog_width_disabled_png": "DialogProperties(usePlatformDefaultWidth = false)" in native_now,
    "platform_default_dialog_width_disabled_svg": "DialogProperties(usePlatformDefaultWidth = false)" in svg_now,
    "portrait_viewer_height_fraction": 0.72,
    "landscape_viewer_height_fraction": 0.94,
    "wide_png_initial_reading_scale": 1.65,
    "nonwide_png_initial_reading_scale": 1.2,
    "svg_initial_reading_scale": 1.65,
    "one_tap_overview_scale": True,
    "one_tap_reading_scale": True,
    "pan_is_bounded_to_viewport": "coerceIn(-maxX, maxX)" in native_now and "coerceIn(-maxX, maxX)" in svg_now,
    "bilingual_close": native_now.count('Text("Close / மூடு")') >= 1 and svg_now.count('Text("Close / மூடு")') >= 1,
    "bilingual_gesture_hint": "விரித்து பெரிதாக்கவும்" in native_now and "விரித்து பெரிதாக்கவும்" in svg_now,
    "figure_assets_reencoded": False,
    "scientific_content_changed": False,
    "book_change": "nativeVersion only; v2.4.0 C4 alt fields preserved",
    "physical_device_retest_required": True,
}
if 'versionCode = 20401' not in gradle_now or 'versionName = "2.4.1"' not in gradle_now:
    raise SystemExit(report)
if book_now.get("nativeVersion") != "2.4.1":
    raise SystemExit(report)
for key in [
    "platform_default_dialog_width_disabled_png",
    "platform_default_dialog_width_disabled_svg",
    "one_tap_overview_scale",
    "one_tap_reading_scale",
    "pan_is_bounded_to_viewport",
    "bilingual_close",
    "bilingual_gesture_hint",
]:
    if not report[key]:
        raise SystemExit(report)

Path("V241_DEVICE_FIGURE_QA_AUDIT.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
