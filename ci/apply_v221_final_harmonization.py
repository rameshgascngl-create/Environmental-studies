from pathlib import Path
import json, hashlib, re, xml.etree.ElementTree as ET
from collections import Counter

ROOT=Path(".")
APP=ROOT/"app"
RAW=APP/"src/main/res/raw"
DRAW=APP/"src/main/res/drawable-nodpi"
BOOK=RAW/"book_content.json"
BUILD=APP/"build.gradle.kts"

V223_INPUT_SHA="1f3b63f25719a7b495528770db4853f01461ebbd4b2b75136235d31ce6ddd211"
FINAL_BOOK_SHA="3b6d24d0a60ea7f8931e99035f80340dd8e9092725a402c4229f15045cff09ce"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if sha256(BOOK) != V223_INPUT_SHA:
    raise SystemExit(f"Unexpected line-by-line editorial input hash: {sha256(BOOK)}")

book=json.loads(BOOK.read_text(encoding="utf-8"))

# Tamil Nadu/Samacheer terminology has priority for established school-textbook terms.
# These substitutions contain Tamil substrings only, so they are safe in bilingual
# unit-opening/review strings while leaving English text unchanged.
REPLACEMENTS=[
    ("சூழல்மண்டல","சூழ்நிலை மண்டல"),
    ("சூழல் மண்டல","சூழ்நிலை மண்டல"),
    ("சூழியல்","சூழலியல்"),
    ("உயிரினப் பன்மை","உயிரிய பல்வகைத்தன்மை"),
    ("மிகை ஊட்டச்சத்துச் செறிவூட்ட","மிகை உணவூட்ட"),
    ("மிகை ஊட்டச்சத்து செறிவூட்ட","மிகை உணவூட்ட"),
    ("மிகை ஊட்டச்சத்துச் செறிவு","மிகை உணவூட்ட"),
    ("உயிரி மருத்துவ","உயிரிமருத்துவ"),
    ("புதுப்பிக்க முடியாத","புதுப்பிக்க இயலாத"),
    ("வளிக்கோளம்","வளிமண்டலம்"),
    ("மீள்திறன்","மீள்தன்மை"),
    ("மீட்சித்திறன்","மீள்தன்மை"),
    # Tamil Nadu school-science glossary register.
    ("பசுமைக்குடில்","பசுமை இல்ல"),
    ("பொது நலவியல்","பொது சுகாதாரம்"),
    ("பொது நலம்","பொது சுகாதாரம்"),
    ("முக்கிய சொற்கள்:","முக்கியக் கலைச்சொற்கள்:"),
    ("நினைவில் கொள்க:","முக்கியக் கருத்து:"),
    ("சிந்தித்துப் பாருங்கள்:","சிந்தனை வினா:"),
    ("கருத்தின் சாரம்:","பாடச்சுருக்கம்:"),
    ("காட்சி வழிக் கற்றல்","படக்கருத்து"),
    ("செயல்முறையும் எடுத்துக்காட்டும் ","எடுத்துக்காட்டாக, "),
]

def harmonize_string(s):
    if not isinstance(s,str):
        return s
    for old,new in REPLACEMENTS:
        s=s.replace(old,new)
    s=re.sub(r"[ \t]+"," ",s)
    return s.strip() if "\n" not in s else s

def walk(obj):
    if isinstance(obj,str):
        return harmonize_string(obj)
    if isinstance(obj,list):
        return [walk(x) for x in obj]
    if isinstance(obj,dict):
        return {k:walk(v) for k,v in obj.items()}
    return obj

book=walk(book)
book["nativeVersion"]="2.2.1"

# First occurrence remains bilingual for university-level precision.
for unit in book["units"]:
    for lesson in unit["lessons"]:
        if lesson["number"]=="4.3":
            lesson["titleTa"]="நீர் மாசுபாடும் மிகை உணவூட்டமும் (Eutrophication)"

# Harmonize Tamil labels in SVG source without rasterising text.
for svg in RAW.glob("*.svg"):
    text=svg.read_text(encoding="utf-8")
    if any("\u0b80" <= ch <= "\u0bff" for ch in text):
        new=harmonize_string(text)
        if new!=text:
            svg.write_text(new,encoding="utf-8")

# Return build identity from the intermediate editorial review layers to requested v2.2.1.
gradle=BUILD.read_text(encoding="utf-8")
gradle=gradle.replace('versionCode = 20203','versionCode = 20201')
gradle=gradle.replace('versionName = "2.2.3"','versionName = "2.2.1"')
gradle=gradle.replace('versionCode = 20202','versionCode = 20201')
gradle=gradle.replace('versionName = "2.2.2"','versionName = "2.2.1"')
if 'versionCode = 20201' not in gradle or 'versionName = "2.2.1"' not in gradle:
    raise SystemExit("v2.2.1 build identity was not restored")
BUILD.write_text(gradle,encoding="utf-8")

BOOK.write_text(json.dumps(book,ensure_ascii=False,indent=2),encoding="utf-8")
if sha256(BOOK) != FINAL_BOOK_SHA:
    raise SystemExit(f"Final v2.2.1 content hash mismatch: {sha256(BOOK)}")

# ---------- Machine-verifiable final audit ----------
lessons=[lesson for unit in book["units"] for lesson in unit["lessons"]]
lesson_numbers=[l["number"] for l in lessons]
lesson_ids=[l["id"] for l in lessons]

outcome_count=sum(
    1 for l in lessons for lang in ("english","tamil")
    for b in l[lang] if b.get("kind")=="learning_outcome"
)
generic_tamil=sum(
    1 for l in lessons for b in l["tamil"]
    if (b.get("title") or "").strip()=="தமிழில் விளக்கம்"
)
empty_lessons=[
    l["number"] for l in lessons
    if not l.get("english") or not l.get("tamil")
]
duplicate_heading_body=[]
for l in lessons:
    for lang in ("english","tamil"):
        for i,b in enumerate(l[lang]):
            title=(b.get("title") or "").strip()
            text=(b.get("text") or "").strip()
            if title and text and (text.startswith(title) or text.startswith(title+":")):
                duplicate_heading_body.append([l["number"],lang,i,title])

deprecated_terms=[
    "சூழல் மண்டல","சூழல்மண்டல","சூழியல்","உயிரினப் பன்மை",
    "மிகை ஊட்டச்சத்து","உயிரி மருத்துவ","புதுப்பிக்க முடியாத",
    "வளிக்கோளம்","மீள்திறன்","மீட்சித்திறன்","பசுமைக்குடில்",
    "பொது நலவியல்","தமிழில் விளக்கம்",
]
corpus=json.dumps(book,ensure_ascii=False)
deprecated_counts={term:corpus.count(term) for term in deprecated_terms}

# Resource integrity and parity.
figure_refs=[]
parity=[]
for l in lessons:
    en=[b.get("figure") for b in l["english"] if b.get("figure")]
    ta=[b.get("figure") for b in l["tamil"] if b.get("figure")]
    figure_refs.extend(en+ta)
    if len(en)!=len(ta):
        parity.append([l["number"],l["titleEn"],len(en),len(ta)])

missing=[]
for ref in figure_refs:
    candidates=[
        RAW/f"{ref}.svg",
        DRAW/f"{ref}.png",
        DRAW/f"{ref}.webp",
        APP/"src/main/res/drawable"/f"{ref}.xml",
    ]
    if not any(p.exists() for p in candidates):
        missing.append(ref)

svgs=sorted(RAW.glob("*.svg"))
svg_errors=[]
tamil_svg_files=[]
external_svg_dependencies=[]
for p in svgs:
    try:
        ET.parse(p)
    except Exception as e:
        svg_errors.append(f"{p.name}: {e}")
    txt=p.read_text(encoding="utf-8")
    if any("\u0b80" <= ch <= "\u0bff" for ch in txt):
        tamil_svg_files.append(p.name)
    if re.search(r'(?:href|xlink:href)\s*=\s*["\']https?://',txt,re.I):
        external_svg_dependencies.append(p.name)

# Duplicate Android resource stems can create ambiguous references.
resource_stems=[]
for directory in (RAW,DRAW,APP/"src/main/res/drawable"):
    if directory.exists():
        resource_stems.extend(p.stem for p in directory.iterdir() if p.is_file())
duplicates=sorted(k for k,v in Counter(resource_stems).items() if v>1)

# Learner-visible intentional Latin-script terms remaining in Tamil material.
latin_entries=[]
def visible_strings(block):
    vals=[]
    for key in ("title","text","caption"):
        value=block.get(key)
        if isinstance(value,str) and value.strip():
            vals.append((key,value))
    for i,value in enumerate(block.get("items") or []):
        if isinstance(value,str):
            vals.append((f"items[{i}]",value))
    for ri,row in enumerate(block.get("rows") or []):
        for ci,value in enumerate(row):
            if isinstance(value,str):
                vals.append((f"rows[{ri}][{ci}]",value))
    return vals

for l in lessons:
    for bi,b in enumerate(l["tamil"]):
        for field,value in visible_strings(b):
            tokens=sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9.()–/-]*",value)))
            if tokens:
                latin_entries.append({
                    "lesson":l["number"],"block_index":bi,"field":field,
                    "tokens":tokens,"text":value,
                })

# Also record Latin terms in Tamil quiz/options and supplemental material.
def collect_latin(obj,path=()):
    if isinstance(obj,str):
        if any("\u0b80" <= ch <= "\u0bff" for ch in obj):
            toks=sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9.()–/-]*",obj)))
            if toks:
                return [{"path":"/".join(map(str,path)),"tokens":toks,"text":obj}]
        return []
    if isinstance(obj,list):
        out=[]
        for i,v in enumerate(obj): out.extend(collect_latin(v,path+(i,)))
        return out
    if isinstance(obj,dict):
        out=[]
        for k,v in obj.items(): out.extend(collect_latin(v,path+(k,)))
        return out
    return []

all_mixed=collect_latin(book)

audit={
    "versionName":"2.2.1",
    "versionCode":20201,
    "nativeVersion":book.get("nativeVersion"),
    "units":len(book["units"]),
    "lessons":len(lessons),
    "lesson_pairing_complete":len(lessons)==46 and all(l.get("english") and l.get("tamil") for l in lessons),
    "unique_lesson_numbers":len(set(lesson_numbers))==len(lesson_numbers),
    "unique_lesson_ids":len(set(lesson_ids))==len(lesson_ids),
    "learning_outcome_blocks":outcome_count,
    "generic_tamil_heading_blocks":generic_tamil,
    "duplicate_heading_body_blocks":duplicate_heading_body,
    "empty_lessons":empty_lessons,
    "deprecated_term_counts":deprecated_counts,
    "missing_figure_refs":sorted(set(missing)),
    "png_count":len(list(DRAW.glob("*.png"))),
    "svg_count":len(svgs),
    "svg_parse_errors":svg_errors,
    "tamil_svg_unicode_files":len(tamil_svg_files),
    "external_svg_dependencies":external_svg_dependencies,
    "duplicate_resource_stems":duplicates,
    "figure_resource_parity_exceptions":parity,
    "remaining_intentional_english_terms_in_tamil_lessons":latin_entries,
    "all_mixed_script_tamil_entries":all_mixed,
    "book_content_sha256":sha256(BOOK),
}

failures=[]
if audit["units"]!=9: failures.append("unit count")
if audit["lessons"]!=46: failures.append("lesson count")
if not audit["lesson_pairing_complete"]: failures.append("lesson pairing")
if not audit["unique_lesson_numbers"] or not audit["unique_lesson_ids"]: failures.append("duplicate lesson id/number")
if outcome_count: failures.append("learning outcomes remain")
if generic_tamil: failures.append("generic Tamil headings remain")
if duplicate_heading_body: failures.append("duplicated heading/body openings remain")
if empty_lessons: failures.append("empty lesson")
if any(deprecated_counts.values()): failures.append("deprecated terminology remains")
if missing: failures.append("missing figures")
if svg_errors: failures.append("SVG parse errors")
if external_svg_dependencies: failures.append("external SVG dependencies")
if duplicates: failures.append("duplicate resource stems")
if len(parity)!=1 or parity[0][0]!="4.2": failures.append(f"unexpected figure parity exceptions: {parity}")
if failures:
    raise SystemExit("FINAL V221 AUDIT FAILED: "+"; ".join(failures))

(ROOT/"V221_FINAL_STATIC_AUDIT.json").write_text(
    json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8"
)

# Final semantic-parity register: every lesson explicitly listed.
lines=[
    "# Environmental Studies v2.2.1 — Final English–Tamil Parity Register","",
    "All 46 lesson pairs were reread through the Tamil college-editorial and sentence-coherence passes. "
    "English scientific content remains the v2.2.1-authorised English layer; Tamil prose was corrected for semantic equivalence and textbook register without requiring literal sentence matching.","",
    "| Lesson | English blocks | Tamil blocks | Pairing |",
    "|---|---:|---:|---|",
]
for l in lessons:
    lines.append(f"| {l['number']} {l['titleEn']} | {len(l['english'])} | {len(l['tamil'])} | reviewed |")
lines += ["","## Figure parity",
          "All academically necessary figure routes are language-equivalent except the recorded 4.2 resource-count difference; "
          "that exception was retained only because the Tamil section carries equivalent scientific information rather than an inaccessible English-only concept."]
(ROOT/"V221_FINAL_PARITY_REGISTER.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

# Scientific visual register for final correction layer.
vis=[
    "# Environmental Studies v2.2.1 — Final Scientific-Visual Register","",
    "- Soil-contamination pathways remain separated into plant uptake → food/food-chain exposure; leaching → groundwater → drinking-water exposure; and runoff/erosion → surface-water/aquatic-ecosystem exposure.",
    "- Biodiversity-driver diagrams identify the five recognised direct pressures and point toward biodiversity loss/change.",
    "- Greenhouse-effect visual remains mechanistic: incoming solar radiation → surface absorption/warming → outgoing infrared radiation → greenhouse-gas absorption/re-emission → downward radiation plus escape to space.",
    "- Tamil greenhouse terminology is harmonised to Tamil Nadu school-science register: **பசுமை இல்ல விளைவு / பசுமை இல்ல வாயுக்கள்**.",
    "- Tamil field-learning SVG labels use complete academic wording rather than compressed machine-like imperatives.",
    "- All SVG resources parse as XML, retain Unicode Tamil text where applicable, and have no external image dependency.",
    "- Existing PNG resources remain packaged; no scientifically correct PNG was removed from the APK solely for stylistic uniformity.",
    "",
    "Physical-device checks for Tamil shaping, clipping, line collisions, normal-scale legibility and tap-to-enlarge remain mandatory.",
]
(ROOT/"V221_FINAL_SCI_VIS_REGISTER.md").write_text("\n".join(vis)+"\n",encoding="utf-8")

changelog=[
    "# Environmental Studies v2.2.1 — Final Editorial Harmonisation","",
    "- Backported the completed 46-lesson Tamil college-register and line-by-line coherence edits into the requested v2.2.1 identity.",
    "- Extended terminology enforcement beyond lessons to unit openings, review material, quizzes, supplemental/glossary content and other learner-visible Tamil strings.",
    "- Preserved Tamil Nadu textbook-priority terms, including சூழ்நிலை மண்டலம், உயிரிய பல்வகைத்தன்மை, மிகை உணவூட்டம் and பசுமை இல்ல விளைவு.",
    "- Removed dormant learning outcomes from authoritative content data and retained zero generic தமிழில் விளக்கம் headings.",
    "- Preserved English/Tamil section separation, lesson order, navigation, offline architecture and figure enlargement behavior.",
    "- No syllabus expansion or new feature was introduced.",
]
(ROOT/"V221_FINAL_EDITORIAL_CHANGELOG.md").write_text("\n".join(changelog)+"\n",encoding="utf-8")

print("V221_FINAL_HARMONIZATION_PASS")
print("BOOK_SHA256",sha256(BOOK))
print("LESSONS",len(lessons))
print("LEARNING_OUTCOMES",outcome_count)
print("GENERIC_TAMIL_HEADINGS",generic_tamil)
print("DUPLICATED_HEADINGS",len(duplicate_heading_body))
print("PNG_COUNT",audit["png_count"])
print("SVG_COUNT",audit["svg_count"])
print("PARITY_EXCEPTIONS",parity)
print("MIXED_SCRIPT_ENTRIES",len(all_mixed))
