from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json

ROOT=Path.cwd()
APP=ROOT/"app/src/main"
UI=APP/"java/edu/gascnagercoil/environmentalsciences/ui"
MODEL=APP/"java/edu/gascnagercoil/environmentalsciences/model/ContentModels.kt"
REPO=APP/"java/edu/gascnagercoil/environmentalsciences/data/ContentRepository.kt"
BOOK=APP/"res/raw/book_content.json"

# 1) Backwards-compatible optional alt field.
model=MODEL.read_text(encoding="utf-8")
old="""    val figure: String?,
    val caption: String
)"""
new="""    val figure: String?,
    val caption: String,
    val alt: String = ""
)"""
if old not in model and 'val alt: String = ""' not in model:
    raise SystemExit("ContentBlock schema anchor changed")
if old in model:
    MODEL.write_text(model.replace(old,new),encoding="utf-8")

repo=REPO.read_text(encoding="utf-8")
old="""        figure = if (o.has("figure")) o.optString("figure").takeIf { it.isNotBlank() } else null,
        caption = o.optString("caption")
    )"""
new="""        figure = if (o.has("figure")) o.optString("figure").takeIf { it.isNotBlank() } else null,
        caption = o.optString("caption"),
        alt = o.optString("alt")
    )"""
if old not in repo and 'alt = o.optString("alt")' not in repo:
    raise SystemExit("ContentRepository alt anchor changed")
if old in repo:
    REPO.write_text(repo.replace(old,new),encoding="utf-8")

# 2) Add concise language-native alt text without changing any existing content field.
data=json.loads(BOOK.read_text(encoding="utf-8"))
before=deepcopy(data)
actual=0
added=0

def add_alt(block:dict, language:str|None=None):
    global actual,added
    if block.get("kind") not in {"figure","svg_figure"} or not block.get("figure"):
        return
    actual+=1
    title=(block.get("title") or "").strip()
    fig=block.get("figure")
    if fig=="fig_010_u02_en":
        alt="Carbon cycle among the atmosphere, organisms, oceans, soil and rocks"
    elif fig=="fig_064_u02_ta":
        alt="வளிமண்டலம், உயிரினங்கள், கடல்கள், மண் மற்றும் பாறைகளுக்கு இடையிலான கார்பன் சுழற்சி"
    elif fig=="fig_032_u04_ta":
        alt="தேர்ந்தெடுக்கப்பட்ட தேசிய சுற்றுப்புறக் காற்றுத் தரநிலை மதிப்புகள்"
    else:
        alt=title
    if not alt:
        caption=(block.get("caption") or "").strip()
        alt=caption.split(";")[0].strip() if caption else ""
    if not alt:
        raise SystemExit(f"No meaningful alt text source for {fig}")
    block["alt"]=alt
    added+=1

for unit in data.get("units",[]):
    for block in unit.get("opening",[]): add_alt(block)
    for lesson in unit.get("lessons",[]):
        for block in lesson.get("english",[]): add_alt(block,"english")
        for block in lesson.get("tamil",[]): add_alt(block,"tamil")
    for block in unit.get("review",[]): add_alt(block)

BOOK.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

without_alt=deepcopy(data)
def strip_alt(obj):
    if isinstance(obj,dict):
        obj.pop("alt",None)
        for v in obj.values(): strip_alt(v)
    elif isinstance(obj,list):
        for v in obj: strip_alt(v)
strip_alt(without_alt)
if without_alt!=before:
    raise SystemExit("C4 changed existing book content; only alt keys are authorised")

# 3) Image and SVG semantics use the alt text, including expanded views.
native=UI/"NativeContent.kt"
t=native.read_text(encoding="utf-8")
if "val figureDescription = block.alt.ifBlank" not in t:
    anchor="    var expanded by remember { mutableStateOf(false) }\n    if (resId == 0) return\n"
    repl=anchor+'    val figureDescription = block.alt.ifBlank { block.title.ifBlank { block.caption.ifBlank { "Teaching figure" } } }\n'
    if t.count(anchor)!=1: raise SystemExit("Native figure description anchor changed")
    t=t.replace(anchor,repl)
    t=t.replace(
        'contentDescription = block.title.ifBlank { block.caption.ifBlank { "Teaching figure" } },',
        'contentDescription = figureDescription,'
    )
    t=t.replace('if (expanded) ZoomDialog(resId) { expanded = false }','if (expanded) ZoomDialog(resId, figureDescription) { expanded = false }')
    t=t.replace('private fun ZoomDialog(resId: Int, dismiss: () -> Unit) {','private fun ZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {')
    t=t.replace('contentDescription = "Enlarged teaching figure",','contentDescription = description,')
    native.write_text(t,encoding="utf-8")

svgp=UI/"SvgFigureBlock.kt"
s=svgp.read_text(encoding="utf-8")
if "val figureDescription = block.alt.ifBlank" not in s:
    s=s.replace(
        "import androidx.compose.ui.input.pointer.pointerInput\n",
        "import androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.ui.semantics.contentDescription\nimport androidx.compose.ui.semantics.semantics\n"
    )
    anchor="    if (resId == 0) return\n    var expanded by remember { mutableStateOf(false) }\n"
    repl=anchor+'    val figureDescription = block.alt.ifBlank { block.title.ifBlank { block.caption.ifBlank { "Teaching figure" } } }\n'
    if s.count(anchor)!=1: raise SystemExit("SVG description anchor changed")
    s=s.replace(anchor,repl)
    s=s.replace(
        "SvgResource(resId = resId, modifier = Modifier.fillMaxWidth().heightIn(min = 220.dp, max = 380.dp).padding(8.dp))",
        "SvgResource(resId = resId, description = figureDescription, modifier = Modifier.fillMaxWidth().heightIn(min = 220.dp, max = 380.dp).padding(8.dp))"
    )
    s=s.replace("if (expanded) SvgZoomDialog(resId) { expanded = false }","if (expanded) SvgZoomDialog(resId, figureDescription) { expanded = false }")
    s=s.replace(
        "private fun SvgResource(resId: Int, modifier: Modifier = Modifier) {",
        "private fun SvgResource(resId: Int, description: String, modifier: Modifier = Modifier) {"
    )
    s=s.replace(
        "        modifier = modifier,\n",
        "        modifier = modifier.semantics { contentDescription = description },\n"
    )
    s=s.replace(
        "private fun SvgZoomDialog(resId: Int, dismiss: () -> Unit) {",
        "private fun SvgZoomDialog(resId: Int, description: String, dismiss: () -> Unit) {"
    )
    s=s.replace(
        "                    resId = resId,\n                    modifier = Modifier",
        "                    resId = resId,\n                    description = description,\n                    modifier = Modifier"
    )
    # C2 rewrites the inline SVG call to multiline form. Its description must
    # refer to the block-local figureDescription; the zoom-dialog call uses
    # its own description parameter. Keep those two scopes distinct.
    head, marker, tail = s.partition("@Composable\nprivate fun SvgResource")
    if not marker:
        raise SystemExit("SvgResource function marker changed")
    head = head.replace("description = description,", "description = figureDescription,")
    s = head + marker + tail
    svgp.write_text(s,encoding="utf-8")

# 4) Quiz options: whole row selectable, >=48dp target, one radio semantic target.
quiz=UI/"QuizScreen.kt"
q=quiz.read_text(encoding="utf-8")
if "Role.RadioButton" not in q:
    q=q.replace("import androidx.compose.foundation.layout.*\n","import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.selection.selectable\n")
    q=q.replace("import androidx.compose.ui.Modifier\n","import androidx.compose.ui.Modifier\nimport androidx.compose.ui.semantics.Role\n")
    old="""                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            RadioButton(selected = answers[index] == oi, onClick = { select(index, oi) })
                            Column(Modifier.weight(1f)) {"""
    new="""                        Row(
                            Modifier
                                .fillMaxWidth()
                                .heightIn(min = 48.dp)
                                .selectable(
                                    selected = answers[index] == oi,
                                    onClick = { select(index, oi) },
                                    role = Role.RadioButton,
                                ),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            RadioButton(selected = answers[index] == oi, onClick = null)
                            Column(Modifier.weight(1f)) {"""
    if q.count(old)!=1: raise SystemExit("Quiz radio row anchor changed")
    q=q.replace(old,new)
    quiz.write_text(q,encoding="utf-8")

# 5) Sliders and wastewater choices: bilingual descriptions + explicit >=48dp row targets.
sim=UI/"SimulationScreen.kt"
m=sim.read_text(encoding="utf-8")
if "private fun a11y(" not in m:
    m=m.replace("import androidx.compose.foundation.layout.*\n","import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.selection.selectable\n")
    m=m.replace("import androidx.compose.ui.Modifier\n","import androidx.compose.ui.Modifier\nimport androidx.compose.ui.semantics.Role\nimport androidx.compose.ui.semantics.contentDescription\nimport androidx.compose.ui.semantics.semantics\nimport androidx.compose.ui.semantics.stateDescription\n")
    for name in ["GreenhouseCard","LogisticCard","EnergyPyramidCard","NoiseCard","WastewaterCard"]:
        m=m.replace(f"item {{ {name}() }}",f"item {{ {name}(language) }}")
        m=m.replace(f"private fun {name}() {{",f"private fun {name}(language: LanguageMode) {{")

    m=m.replace(
        "Slider(value = co2, onValueChange = { co2 = it }, valueRange = 280f..1000f)",
        '''Slider(
            value = co2,
            onValueChange = { co2 = it },
            valueRange = 280f..1000f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Carbon dioxide concentration", "கார்பன் டைஆக்சைடு செறிவு")
                stateDescription = "${co2.toInt()} ppm"
            }
        )'''
    )
    m=m.replace(
        "Slider(value = ratePercent, onValueChange = { ratePercent = it }, valueRange = 5f..100f)",
        '''Slider(
            value = ratePercent,
            onValueChange = { ratePercent = it },
            valueRange = 5f..100f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Intrinsic growth rate", "உள்ளார்ந்த வளர்ச்சி விகிதம்")
                stateDescription = "${"%.2f".format(r)}"
            }
        )'''
    )
    m=m.replace(
        "Slider(value = capacity, onValueChange = { capacity = it }, valueRange = 200f..1400f)",
        '''Slider(
            value = capacity,
            onValueChange = { capacity = it },
            valueRange = 200f..1400f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Carrying capacity", "தாங்கும் திறன்")
                stateDescription = "${capacity.toInt()}"
            }
        )'''
    )
    m=m.replace(
        "Slider(value = producer, onValueChange = { producer = (it / 500f).toInt() * 500f }, valueRange = 1000f..20000f)",
        '''Slider(
            value = producer,
            onValueChange = { producer = (it / 500f).toInt() * 500f },
            valueRange = 1000f..20000f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Producer energy", "உற்பத்தியாளர் ஆற்றல்")
                stateDescription = "${producer.toInt()}"
            }
        )'''
    )
    m=m.replace(
        "Slider(value = efficiency, onValueChange = { efficiency = it }, valueRange = 5f..20f)",
        '''Slider(
            value = efficiency,
            onValueChange = { efficiency = it },
            valueRange = 5f..20f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Energy transfer efficiency", "ஆற்றல் பரிமாற்றத் திறன்")
                stateDescription = "${efficiency.toInt()} percent"
            }
        )'''
    )
    m=m.replace(
        "Slider(value = a, onValueChange = { a = it }, valueRange = 30f..100f)",
        '''Slider(
            value = a,
            onValueChange = { a = it },
            valueRange = 30f..100f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Sound level A", "ஒலி நிலை A")
                stateDescription = "${a.toInt()} decibels"
            }
        )'''
    )
    m=m.replace(
        "Slider(value = b, onValueChange = { b = it }, valueRange = 30f..100f)",
        '''Slider(
            value = b,
            onValueChange = { b = it },
            valueRange = 30f..100f,
            modifier = Modifier.semantics {
                contentDescription = a11y(language, "Sound level B", "ஒலி நிலை B")
                stateDescription = "${b.toInt()} decibels"
            }
        )'''
    )

    old="""    val desc = listOf(
        "Screening removes coarse solids.",
        "Primary settling removes settleable solids.",
        "Biological treatment oxidises dissolved and fine organic matter.",
        "Secondary settling separates biomass from treated water.",
        "Disinfection or polishing targets remaining pathogens or contaminants."
    )
    var stage by remember { mutableIntStateOf(0) }"""
    new="""    val desc = listOf(
        "Screening removes coarse solids.",
        "Primary settling removes settleable solids.",
        "Biological treatment oxidises dissolved and fine organic matter.",
        "Secondary settling separates biomass from treated water.",
        "Disinfection or polishing targets remaining pathogens or contaminants."
    )
    val stagesTa = listOf("திரையிடல்", "முதன்மை படிவுறுதல்", "உயிரியல் சிகிச்சை", "இரண்டாம் படிவுறுதல்", "இறுதிச் சுத்திகரிப்பு")
    var stage by remember { mutableIntStateOf(0) }"""
    if m.count(old)!=1: raise SystemExit("Wastewater stage anchor changed")
    m=m.replace(old,new)

    old="""            Row(verticalAlignment = Alignment.CenterVertically) {
                RadioButton(selected = stage == index, onClick = { stage = index })
                Text(name, fontWeight = if (stage == index) FontWeight.Bold else FontWeight.Normal)
            }"""
    new="""            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 48.dp)
                    .selectable(
                        selected = stage == index,
                        onClick = { stage = index },
                        role = Role.RadioButton,
                    )
                    .semantics(mergeDescendants = true) {
                        contentDescription = a11y(language, name, stagesTa[index])
                    },
                verticalAlignment = Alignment.CenterVertically
            ) {
                RadioButton(selected = stage == index, onClick = null)
                Text(name, fontWeight = if (stage == index) FontWeight.Bold else FontWeight.Normal)
            }"""
    if m.count(old)!=1: raise SystemExit("Wastewater radio row anchor changed")
    m=m.replace(old,new)

    helper='''\nprivate fun a11y(language: LanguageMode, english: String, tamil: String): String =
    if (language == LanguageMode.TAMIL) tamil else english
'''
    insert="\n@Composable\nprivate fun ToolCard(title: String, content: @Composable ColumnScope.() -> Unit) {"
    if m.count(insert)!=1: raise SystemExit("a11y helper insertion anchor changed")
    m=m.replace(insert,helper+insert)
    sim.write_text(m,encoding="utf-8")

# Static audit; physical accessibility verification remains a separate gate.
model_now=MODEL.read_text(encoding="utf-8")
repo_now=REPO.read_text(encoding="utf-8")
native_now=native.read_text(encoding="utf-8")
svg_now=svgp.read_text(encoding="utf-8")
quiz_now=quiz.read_text(encoding="utf-8")
sim_now=sim.read_text(encoding="utf-8")

alt_values=[]
for unit in data["units"]:
    for block in unit.get("opening",[]):
        if block.get("figure"): alt_values.append(block.get("alt",""))
    for lesson in unit.get("lessons",[]):
        for lang in ("english","tamil"):
            for block in lesson.get(lang,[]):
                if block.get("figure"): alt_values.append(block.get("alt",""))
    for block in unit.get("review",[]):
        if block.get("figure"): alt_values.append(block.get("alt",""))

report={
    "task":"C4 accessibility semantics",
    "actual_figure_blocks":actual,
    "alt_fields_added":added,
    "empty_alt_count":sum(not x.strip() for x in alt_values),
    "max_alt_characters":max(map(len,alt_values)) if alt_values else 0,
    "existing_book_fields_unchanged_except_alt":without_alt==before,
    "backwards_compatible_optional_default":'val alt: String = ""' in model_now and 'o.optString("alt")' in repo_now,
    "png_uses_alt":'contentDescription = figureDescription' in native_now,
    "svg_uses_alt":'contentDescription = description' in svg_now,
    "quiz_selectable_radio_rows":'role = Role.RadioButton' in quiz_now and 'RadioButton(selected = answers[index] == oi, onClick = null)' in quiz_now,
    "quiz_min_touch_target":'.heightIn(min = 48.dp)' in quiz_now,
    "slider_semantics_count":sim_now.count("modifier = Modifier.semantics"),
    "wastewater_selectable_row":'stagesTa[index]' in sim_now and 'RadioButton(selected = stage == index, onClick = null)' in sim_now,
    "wastewater_min_touch_target":'.heightIn(min = 48.dp)' in sim_now,
    "talkback_physically_verified":False,
    "font_scaling_200_percent_physically_verified":False,
    "verification_note":"Source-level semantics and touch-target audit only; TalkBack and 200% font-scale behaviour still require physical/emulator accessibility QA."
}
if actual!=91 or added!=91 or report["empty_alt_count"]!=0:
    raise SystemExit(report)
if report["slider_semantics_count"]!=7:
    raise SystemExit(report)
if not all(report[k] for k in [
    "existing_book_fields_unchanged_except_alt","backwards_compatible_optional_default",
    "png_uses_alt","svg_uses_alt","quiz_selectable_radio_rows","quiz_min_touch_target",
    "wastewater_selectable_row","wastewater_min_touch_target"
]):
    raise SystemExit(report)

Path("V240_C4_ACCESSIBILITY_AUDIT.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(report,ensure_ascii=False,indent=2))
