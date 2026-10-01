from __future__ import annotations

from pathlib import Path
import json
import math
import re

ROOT=Path.cwd()
UI=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui"
RAW=ROOT/"app/src/main/res/raw"
SVG_BLOCK=UI/"SvgFigureBlock.kt"

records=[]
large=set()
for p in sorted(RAW.glob("sci_*.svg")):
    text=p.read_text(encoding="utf-8")
    vb=re.search(r'''viewBox\s*=\s*["']\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)["']''',text)
    if not vb:
        raise SystemExit(f"Missing viewBox: {p.name}")
    width=float(vb.group(3))
    sizes=[float(x) for x in re.findall(r'''font-size\s*[:=]\s*["']?([0-9]+(?:\.[0-9]+)?)''',text)]
    if not sizes:
        raise SystemExit(f"No font sizes found: {p.name}")
    minimum=min(sizes)
    required=math.ceil(width*11.0/minimum)
    display=600 if required>400 else 400
    effective=minimum*display/width
    if display==600:
        large.add(p.stem)
    records.append({
        "resource":p.stem,
        "viewbox_width":width,
        "minimum_svg_font_units":minimum,
        "computed_width_for_11dp_equivalent":required,
        "production_min_display_width_dp":display,
        "minimum_effective_dp_equivalent_at_default_scale":round(effective,2),
    })

if len(records)!=36:
    raise SystemExit(f"Expected 36 SVGs, found {len(records)}")
if min(r["minimum_effective_dp_equivalent_at_default_scale"] for r in records)<11.0:
    raise SystemExit("Display-width contract does not reach 11dp-equivalent minimum")

# A blanket font-size rewrite to 36 units was deliberately rejected: the source
# diagrams use fixed node geometry, and enlarging text independently creates label
# collisions (especially in Tamil). Preserve the validated geometry and enlarge the
# entire diagram viewport instead; narrow devices can pan horizontally.
src=SVG_BLOCK.read_text(encoding="utf-8")
if "largeSvgCanvasResources" not in src:
    src=src.replace(
        "import androidx.compose.foundation.gestures.detectTransformGestures\n",
        "import androidx.compose.foundation.gestures.detectTransformGestures\nimport androidx.compose.foundation.horizontalScroll\nimport androidx.compose.foundation.rememberScrollState\n"
    )
    src=src.replace(
        "import androidx.compose.ui.platform.LocalContext\n",
        "import androidx.compose.ui.platform.LocalConfiguration\nimport androidx.compose.ui.platform.LocalContext\n"
    )
    marker="import edu.gascnagercoil.environmentalsciences.model.ContentBlock\n\n"
    values=",\n    ".join(f'\"{name}\"' for name in sorted(large))
    block=f'''private val largeSvgCanvasResources = setOf(
    {values}
)

'''
    if src.count(marker)!=1:
        raise SystemExit("SVG resource-set insertion anchor changed")
    src=src.replace(marker,marker+block)

    anchor="""    if (resId == 0) return
    var expanded by remember { mutableStateOf(false) }
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {"""
    repl="""    if (resId == 0) return
    var expanded by remember { mutableStateOf(false) }
    val minimumDisplayWidthDp = if (block.figure in largeSvgCanvasResources) 600 else 400
    val availableDisplayWidthDp = (LocalConfiguration.current.screenWidthDp - 56).coerceIn(280, 900)
    val svgDisplayWidth = maxOf(minimumDisplayWidthDp, availableDisplayWidthDp).dp
    val svgScroll = rememberScrollState()
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {"""
    if src.count(anchor)!=1:
        raise SystemExit("SVG display-width anchor changed")
    src=src.replace(anchor,repl)

    old="""        ElevatedCard(onClick = { expanded = true }, modifier = Modifier.fillMaxWidth()) {
            SvgResource(resId = resId, modifier = Modifier.fillMaxWidth().heightIn(min = 220.dp, max = 380.dp).padding(8.dp))
        }"""
    new="""        ElevatedCard(onClick = { expanded = true }, modifier = Modifier.fillMaxWidth()) {
            Box(Modifier.fillMaxWidth().horizontalScroll(svgScroll)) {
                SvgResource(
                    resId = resId,
                    modifier = Modifier
                        .width(svgDisplayWidth)
                        .heightIn(min = 220.dp, max = 380.dp)
                        .padding(8.dp)
                )
            }
        }"""
    if src.count(old)!=1:
        raise SystemExit("SVG inline renderer anchor changed")
    src=src.replace(old,new)
    SVG_BLOCK.write_text(src,encoding="utf-8")

report={
    "task":"C2 SVG legibility",
    "svg_count":len(records),
    "source_font_units_preserved":True,
    "blanket_minimum_36_unit_rewrite_applied":False,
    "blanket_rewrite_rejection_reason":"Fixed-node SVG layouts collide when text alone is enlarged; Tamil labels are the highest-risk cases.",
    "production_strategy":"Preserve source geometry and enforce a 400dp or 600dp minimum diagram display width with horizontal pan on narrower screens.",
    "minimum_effective_dp_equivalent_default_scale":min(r["minimum_effective_dp_equivalent_at_default_scale"] for r in records),
    "large_canvas_svg_count":len(large),
    "large_canvas_resources":sorted(large),
    "horizontal_pan_enabled":"horizontalScroll(svgScroll)" in SVG_BLOCK.read_text(encoding="utf-8"),
    "pinch_zoom_retained":"detectTransformGestures" in SVG_BLOCK.read_text(encoding="utf-8"),
    "android_font_scale_applies_inside_svg":False,
    "accessibility_note":"SVG text is vector artwork and does not follow Android fontScale. Scalable captions/alt semantics and zoom remain the accessibility fallback.",
    "english_tamil_overlap_physically_verified":False,
    "verification_note":"No source text-size mutation was made, so C2 introduces no new text-layout collision by changing SVG geometry. Physical-device visual QA is still required.",
    "records":records,
}
Path("V240_C2_SVG_LEGIBILITY_AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="records"},ensure_ascii=False,indent=2))
