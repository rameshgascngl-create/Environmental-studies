#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path.cwd()
NATIVE=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/NativeContent.kt"
BITMAP=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/FigureBitmap.kt"
SVG=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/SvgFigureBlock.kt"

def replace_once(text, old, new, label):
    count=text.count(old)
    assert count==1, f"{label}: expected one match, found {count}"
    return text.replace(old,new,1)

# FigureBitmap: return null rather than throwing if a resource cannot be decoded.
s=BITMAP.read_text(encoding="utf-8")
s=replace_once(
    s,
    '''): Painter {
    val resources = LocalContext.current.resources
    val bitmap = remember(resId, targetWidthPx, resources) {
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeResource(resources, resId, bounds)
        require(bounds.outWidth > 0 && bounds.outHeight > 0) {
            "Unable to read teaching figure bounds for resource $resId"
        }

        var sample = 1
        while (bounds.outWidth / (sample * 2) >= targetWidthPx) {
            sample *= 2
        }

        val options = BitmapFactory.Options().apply {
            inSampleSize = sample
            inPreferredConfig = Bitmap.Config.ARGB_8888
        }
        requireNotNull(BitmapFactory.decodeResource(resources, resId, options)) {
            "Unable to decode teaching figure resource $resId"
        }
    }
    return remember(bitmap) { BitmapPainter(bitmap.asImageBitmap()) }
}
''',
    '''): Painter? {
    val resources = LocalContext.current.resources
    val bitmap = remember(resId, targetWidthPx, resources) {
        if (resId == 0) {
            null
        } else {
            val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
            BitmapFactory.decodeResource(resources, resId, bounds)
            if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
                null
            } else {
                var sample = 1
                while (bounds.outWidth / (sample * 2) >= targetWidthPx) {
                    sample *= 2
                }
                val options = BitmapFactory.Options().apply {
                    inSampleSize = sample
                    inPreferredConfig = Bitmap.Config.ARGB_8888
                }
                BitmapFactory.decodeResource(resources, resId, options)
            }
        }
    }
    return remember(bitmap) { bitmap?.let { BitmapPainter(it.asImageBitmap()) } }
}
''',
    "nullable bitmap painter",
)
BITMAP.write_text(s,encoding="utf-8")

# Native PNG figure block: blank/missing resource ids and decode failures keep the
# caption visible and never reach painterResource/bitmap decoder exception paths.
s=NATIVE.read_text(encoding="utf-8")
s=replace_once(
    s,
    '''    val resId = remember(block.figure) {
        context.resources.getIdentifier(block.figure.orEmpty(), "drawable", context.packageName)
    }
    var expanded by remember { mutableStateOf(false) }
    if (resId == 0) return
''',
    '''    val figureName = block.figure.orEmpty().trim()
    val resId = remember(figureName) {
        if (figureName.isBlank()) 0 else context.resources.getIdentifier(figureName, "drawable", context.packageName)
    }
    var expanded by remember { mutableStateOf(false) }
    if (resId == 0) {
        MissingFigureCaption(block)
        return
    }
''',
    "PNG resource guard",
)
s=replace_once(
    s,
    '''    val animatedVariant: (@Composable () -> Unit)? = when (block.figure) {
        "fig_010_u02_en" -> ({ AnimatedCarbonCycle(isTamil = false) })
        "fig_064_u02_ta" -> ({ AnimatedCarbonCycle(isTamil = true) })
        else -> null
    }
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
''',
    '''    val animatedVariant: (@Composable () -> Unit)? = when (block.figure) {
        "fig_010_u02_en" -> ({ AnimatedCarbonCycle(isTamil = false) })
        "fig_064_u02_ta" -> ({ AnimatedCarbonCycle(isTamil = true) })
        else -> null
    }
    val figurePainter = if (animatedVariant == null) rememberDownsampledFigurePainter(resId) else null
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
''',
    "nullable painter use",
)
s=replace_once(
    s,
    '''        ElevatedCard(
            modifier = Modifier.fillMaxWidth(),
            onClick = { expanded = true }
        ) {
            if (animatedVariant != null) {
                Box(Modifier.padding(8.dp)) { animatedVariant() }
            } else {
                Image(
                    painter = rememberDownsampledFigurePainter(resId),
                    contentDescription = figureDescription,
                    modifier = Modifier.fillMaxWidth().padding(8.dp),
                    contentScale = ContentScale.Fit
                )
            }
        }
        if (block.caption.isNotBlank() && animatedVariant == null) Text(block.caption, style = MaterialTheme.typography.bodySmall)
''',
    '''        ElevatedCard(
            modifier = Modifier.fillMaxWidth(),
            onClick = { if (animatedVariant != null || figurePainter != null) expanded = true }
        ) {
            if (animatedVariant != null) {
                Box(Modifier.padding(8.dp)) { animatedVariant() }
            } else if (figurePainter != null) {
                Image(
                    painter = figurePainter,
                    contentDescription = figureDescription,
                    modifier = Modifier.fillMaxWidth().padding(8.dp),
                    contentScale = ContentScale.Fit
                )
            } else {
                Text(
                    block.caption.ifBlank { block.title.ifBlank { "Figure unavailable" } },
                    modifier = Modifier.padding(12.dp),
                    style = MaterialTheme.typography.bodySmall,
                )
            }
        }
        if (block.caption.isNotBlank() && animatedVariant == null && figurePainter != null) {
            Text(block.caption, style = MaterialTheme.typography.bodySmall)
        }
''',
    "PNG failure placeholder",
)
s=replace_once(
    s,
    '''@Composable
private fun ZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {
''',
    '''@Composable
private fun MissingFigureCaption(block: ContentBlock) {
    val text = block.caption.ifBlank { block.title }
    if (text.isNotBlank()) {
        ElevatedCard(Modifier.fillMaxWidth()) {
            Text(text, Modifier.padding(12.dp), style = MaterialTheme.typography.bodySmall)
        }
    }
}

@Composable
private fun ZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {
''',
    "PNG missing-resource caption",
)
NATIVE.write_text(s,encoding="utf-8")

# SVG figure block: guard blank/missing ids and malformed SVG decoding.
s=SVG.read_text(encoding="utf-8")
s=replace_once(
    s,
    '''    val resId = remember(block.figure) {
        context.resources.getIdentifier(block.figure.orEmpty(), "raw", context.packageName)
    }
    if (resId == 0) return
''',
    '''    val figureName = block.figure.orEmpty().trim()
    val resId = remember(figureName) {
        if (figureName.isBlank()) 0 else context.resources.getIdentifier(figureName, "raw", context.packageName)
    }
    if (resId == 0) {
        if (block.caption.isNotBlank()) {
            ElevatedCard(Modifier.fillMaxWidth()) {
                Text(block.caption, Modifier.padding(12.dp), style = MaterialTheme.typography.bodySmall)
            }
        }
        return
    }
''',
    "SVG resource guard",
)
s=replace_once(
    s,
    '''    val picture = remember(resId) {
        ensureTamilSvgFontResolver(context)
        context.resources.openRawResource(resId).use { SVG.getFromInputStream(it).renderToPicture() }
    }
    AndroidView(
''',
    '''    val picture = remember(resId) {
        runCatching {
            ensureTamilSvgFontResolver(context)
            context.resources.openRawResource(resId).use { SVG.getFromInputStream(it).renderToPicture() }
        }.getOrNull()
    }
    if (picture == null) {
        Box(modifier, contentAlignment = androidx.compose.ui.Alignment.Center) {
            Text("Figure unavailable", style = MaterialTheme.typography.bodySmall)
        }
        return
    }
    AndroidView(
''',
    "SVG parse failure guard",
)
SVG.write_text(s,encoding="utf-8")

checks={
    "bitmap_painter_nullable":": Painter?" in BITMAP.read_text(encoding="utf-8"),
    "bitmap_no_require":"require(" not in BITMAP.read_text(encoding="utf-8") and "requireNotNull" not in BITMAP.read_text(encoding="utf-8"),
    "png_blank_guard":"figureName.isBlank()" in NATIVE.read_text(encoding="utf-8"),
    "png_placeholder":"Figure unavailable" in NATIVE.read_text(encoding="utf-8"),
    "svg_blank_guard":"figureName.isBlank()" in SVG.read_text(encoding="utf-8"),
    "svg_parse_guard":"runCatching" in SVG.read_text(encoding="utf-8"),
}
assert all(checks.values()),checks
Path("V245_ITEM5_FIGURE_ROBUSTNESS_AUDIT.json").write_text(
    json.dumps(checks,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(checks,indent=2))
