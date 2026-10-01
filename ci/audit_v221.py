from pathlib import Path
import json, re, xml.etree.ElementTree as ET, hashlib, sys

ROOT=Path(".")
RAW=ROOT/"app/src/main/res/raw"
DRAW=ROOT/"app/src/main/res/drawable-nodpi"
DRAW_V4=ROOT/"app/src/main/res/drawable-nodpi-v4"
BOOK=RAW/"book_content.json"
BUILD=ROOT/"app/build.gradle.kts"
data=json.loads(BOOK.read_text(encoding="utf-8"))

lessons=[l for u in data["units"] for l in u["lessons"]]
assert len(data["units"])==9
assert len(lessons)==46
assert len({l["id"] for l in lessons})==46
assert len({l["number"] for l in lessons})==46
assert all(l.get("english") and l.get("tamil") for l in lessons)

blocks=[(l["number"],lang,b) for l in lessons for lang in ("english","tamil") for b in l[lang]]
learning=[x for x in blocks if x[2].get("kind")=="learning_outcome"]
generic=[x for x in blocks if x[1]=="tamil" and (x[2].get("title") or "").strip()=="தமிழில் விளக்கம்"]
assert not learning, learning
assert not generic, generic

# No dormant objective language should remain in the authoritative lesson data.
text=json.dumps(data,ensure_ascii=False)
for phrase in ("By the end of this lesson","Learning Objectives","Learning Outcomes","கற்றல் விளைவுகள்:","கற்றல் நோக்கங்கள்"):
    assert phrase not in text, phrase

# Terminology freezes.
for bad in ("சூழல் மண்டலம்","மிகை ஊட்டச்சத்துச் செறிவூட்டல்","அமிலத் திணிவு","பசுங்குடில் வாயு","பசுங்குடில் விளைவு"):
    assert bad not in text, f"legacy Tamil term remains: {bad}"
for good in ("சூழ்நிலை மண்டலம்","மிகை உணவூட்டம்","அமிலப் படிவு","பசுமை இல்ல வாயு","உயிரிய பல்வகைத்தன்மை"):
    assert good in text, f"master term absent: {good}"

# Referenced figures must exist locally.
refs=[]
for num,lang,b in blocks:
    fig=(b.get("figure") or "").strip()
    if fig: refs.append((num,lang,fig))
missing=[]
for num,lang,fig in refs:
    choices=[RAW/(fig+".svg"),DRAW/(fig+".png"),DRAW_V4/(fig+".png")]
    if not any(p.exists() for p in choices): missing.append((num,lang,fig))
assert not missing, missing

# All SVGs parse; no external image dependencies; Tamil SVGs contain Tamil Unicode text.
svgs=sorted(RAW.glob("*.svg"))
ta_svgs=sorted(RAW.glob("*_ta.svg"))
for p in svgs:
    ET.parse(p)
    s=p.read_text(encoding="utf-8")
    assert "http://" not in re.sub(r'xmlns="http://www.w3.org/2000/svg"',"",s), p.name
    assert "https://" not in s, p.name
for p in ta_svgs:
    s=p.read_text(encoding="utf-8")
    assert re.search(r"[\u0B80-\u0BFF]",s), f"no Tamil Unicode in {p.name}"
    assert "தமிழில் விளக்கம்" not in s
    assert "அமிலத் திணிவு" not in s
    assert "மூலங்களை வரைபடு" not in s
    assert "காரணம் பகுப்பாய்வு" not in s
    assert "வீணைத் தவிர்" not in s
    assert "மனித அழுத்தம் பதிவு" not in s
    assert "குறியீடு கண்காணி" not in s

# Resource-id collisions.
stems=[p.stem for p in svgs]+[p.stem for p in DRAW.glob("*.png")]+[p.stem for p in DRAW_V4.glob("*.png")]
dups=sorted({x for x in stems if stems.count(x)>1})
assert not dups, f"duplicate resource stems: {dups}"

# Figure parity after removing redundant visual duplicates.
parity=[]
for l in lessons:
    en=[b for b in l["english"] if b.get("kind") in ("figure","svg_figure") and b.get("figure")]
    ta=[b for b in l["tamil"] if b.get("kind") in ("figure","svg_figure") and b.get("figure")]
    if len(en)!=len(ta): parity.append((l["number"],len(en),len(ta)))
assert not parity, parity

# Version identity.
gradle=BUILD.read_text(encoding="utf-8")
assert 'applicationId = "edu.gascnagercoil.environmentalsciences"' in gradle
assert 'minSdk = 24' in gradle
assert 'targetSdk = 36' in gradle
assert 'versionCode = 20201' in gradle
assert 'versionName = "2.2.1"' in gradle

# Remaining Latin-script terms in Tamil are reported, not blindly removed.
allowed=re.compile(r"\b(?:PM2\.5|PM10|CPCB|NAAQS|SO2|SO₂|NO2|NO₂|NOx|NOₓ|O3|O₃|CO|BOD|COD|TDS|pH|BIS|IS|EIA|CBD|UNFCCC|CITES|NDCs|LED|CFCs|HCFCs|dB|Leq|MoEFCC|UNEP|Ramsar|Stockholm|Vienna|Montreal|Kyoto|Paris|Van|Sanrakshan|Evam|Samvardhan|Adhiniyam|Forest|Conservation|Act|Himalaya|Indo-Burma|Western|Ghats|Sri|Lanka|Sundaland|Nicobar|Eutrophication|Endemism|Biodiversity|hotspot|Mitigation|Adaptation|Hazard|Hazards|Exposure|Risk|Vulnerability|Environmental|Impact|Assessment|E-waste|Biomedical|waste|phytoremediation|bioremediation|stratosphere)\b")
remaining=[]
for num,lang,b in blocks:
    if lang!="tamil": continue
    for field in ("title","text","caption"):
        s=b.get(field) or ""
        stripped=allowed.sub("",s)
        toks=sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9.-]*",stripped)))
        if toks: remaining.append({"lesson":num,"field":field,"terms":toks,"text":s})
    for row in b.get("rows") or []:
        for cell in row:
            s=str(cell); stripped=allowed.sub("",s)
            toks=sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9.-]*",stripped)))
            if toks: remaining.append({"lesson":num,"field":"table","terms":toks,"text":s})

report={
"units":len(data["units"]),
"lessons":len(lessons),
"english_tamil_pairs":len(lessons),
"learning_outcome_blocks":len(learning),
"generic_tamil_explanation_headings":len(generic),
"png_count":len(list(DRAW.glob("*.png")))+len(list(DRAW_V4.glob("*.png"))),
"svg_count":len(svgs),
"tamil_svg_count":len(ta_svgs),
"figure_parity_exceptions":parity,
"missing_referenced_images":missing,
"remaining_latin_entries":remaining,
"book_content_sha256":hashlib.sha256(BOOK.read_bytes()).hexdigest(),
}
Path("V221_STATIC_AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="remaining_latin_entries"},ensure_ascii=False,indent=2))
print("REMAINING_LATIN_ENTRY_COUNT",len(remaining))
print("V221 STATIC AUDIT: PASS")
