from __future__ import annotations

from pathlib import Path
import json
import struct

ROOT = Path.cwd()
UI = ROOT / "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui"
RES = ROOT / "app/src/main/res"
NATIVE = UI / "NativeContent.kt"
HELPER = UI / "FigureBitmap.kt"
TARGET_WIDTH_PX = 800

native = NATIVE.read_text(encoding="utf-8")
needle = "painter = painterResource(resId),"
if native.count(needle) != 2:
    raise SystemExit(f"Expected exactly two painterResource(resId) calls, found {native.count(needle)}")
native = native.replace(needle, "painter = rememberDownsampledFigurePainter(resId),", 1)
NATIVE.write_text(native, encoding="utf-8")

HELPER.write_text(r'''package edu.gascnagercoil.environmentalsciences.ui

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.painter.BitmapPainter
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.platform.LocalContext

private const val INLINE_FIGURE_TARGET_WIDTH_PX = 800

/**
 * Decodes large drawable-nodpi teaching plates with an explicit sampling bound for
 * inline lesson display. The zoom dialog deliberately keeps painterResource() so a
 * learner can still inspect the original-resolution plate on demand.
 */
@Composable
internal fun rememberDownsampledFigurePainter(
    resId: Int,
    targetWidthPx: Int = INLINE_FIGURE_TARGET_WIDTH_PX,
): Painter {
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
''', encoding="utf-8")

def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"Not a PNG with IHDR: {path}")
    return struct.unpack(">II", data[16:24])

records = []
for p in sorted(RES.rglob("*.png")):
    w, h = png_dimensions(p)
    sample = 1
    while w // (sample * 2) >= TARGET_WIDTH_PX:
        sample *= 2
    decoded_w = max(1, w // sample)
    decoded_h = max(1, h // sample)
    records.append({
        "path": str(p.relative_to(ROOT)),
        "width": w,
        "height": h,
        "inline_inSampleSize": sample,
        "estimated_inline_width": decoded_w,
        "estimated_inline_height": decoded_h,
        "theoretical_full_rgba_bytes": w * h * 4,
        "estimated_inline_rgba_bytes": decoded_w * decoded_h * 4,
    })

full = sum(r["theoretical_full_rgba_bytes"] for r in records)
bounded = sum(r["estimated_inline_rgba_bytes"] for r in records)

report = {
    "task": "C1 bounded PNG decoding",
    "png_count": len(records),
    "inline_target_width_px": TARGET_WIDTH_PX,
    "theoretical_all_full_rgba_bytes": full,
    "estimated_all_inline_rgba_bytes": bounded,
    "estimated_reduction_bytes": full - bounded,
    "estimated_inline_fraction": round(bounded / full, 6) if full else None,
    "full_resolution_zoom_retained": "painter = painterResource(resId)," in native,
    "bounded_inline_decoder_present": "rememberDownsampledFigurePainter(resId)" in native,
    "measured_peak_heap_2gb_emulator": False,
    "measurement_note": (
        "Static PNG header arithmetic and source inspection only. Peak heap on a 2 GB emulator "
        "has not yet been physically measured and must not be reported as measured evidence."
    ),
    "records": records,
}

if len(records) != 64:
    raise SystemExit(f"Expected 64 PNG teaching assets, found {len(records)}")
if not report["bounded_inline_decoder_present"] or not report["full_resolution_zoom_retained"]:
    raise SystemExit("C1 source contract not satisfied")

Path("V240_C1_IMAGE_DECODE_AUDIT.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps({k: v for k, v in report.items() if k != "records"}, indent=2))
