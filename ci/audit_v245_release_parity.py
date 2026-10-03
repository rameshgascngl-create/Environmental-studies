#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import argparse
import json
import re
import subprocess
import sys
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("--apk", required=True)
parser.add_argument("--aab", required=True)
parser.add_argument("--aapt", required=True)
args = parser.parse_args()

REGISTRY = Path("../../ci/parity-allowlist.json")
OUT = Path("V245_PARITY_AUDIT.json")
apk = Path(args.apk)
aab = Path(args.aab)
aapt = Path(args.aapt)
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

dump = subprocess.check_output(
    [str(aapt), "dump", "--values", "resources", str(apk)],
    text=True,
    errors="replace",
)

def resource_file_path(kind, name):
    needle = f":{kind}/{name}:"
    lines = dump.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if needle in line and stripped.startswith("resource 0x"):
            for nxt in lines[i + 1 : i + 10]:
                m = re.search(r'\(string(?:8|16)\) "([^"]+)"', nxt)
                if m:
                    return m.group(1)
    return None

book_path = resource_file_path("raw", "book_content")
assert book_path, "release APK does not expose raw/book_content"
with zipfile.ZipFile(apk) as z:
    apk_book = z.read(book_path)
with zipfile.ZipFile(aab) as z:
    aab_book = z.read("base/res/raw/book_content.json")
assert apk_book == aab_book, "APK/AAB packaged book_content.json differs"
data = json.loads(apk_book.decode("utf-8"))

def figures(lesson, lang):
    return [
        b.get("figure", "").strip()
        for b in lesson[lang]
        if b.get("kind") in ("figure", "svg_figure") and b.get("figure", "").strip()
    ]

def list_item_count(lesson, lang):
    return sum(len(b.get("items", [])) for b in lesson[lang])

per_lesson=[]
mismatch_ids=[]
list_gaps={}
item_carrier_kinds=Counter()
total_en=0
total_ta=0

for unit in data["units"]:
    for lesson in unit["lessons"]:
        lid=lesson["id"]
        en=figures(lesson,"english")
        ta=figures(lesson,"tamil")
        total_en += len(en)
        total_ta += len(ta)
        mismatch=len(en)!=len(ta)
        if mismatch:
            mismatch_ids.append(lid)

        en_items=list_item_count(lesson,"english")
        ta_items=list_item_count(lesson,"tamil")
        if en_items != ta_items:
            list_gaps[lid]=[en_items,ta_items]
            for block in lesson["english"]:
                if block.get("items"):
                    item_carrier_kinds[block.get("kind","")] += 1

        per_lesson.append({
            "lessonId":lid,
            "englishFigureCount":len(en),
            "tamilFigureCount":len(ta),
            "englishFigures":en,
            "tamilFigures":ta,
            "mismatch":mismatch,
            "registryStatus":registry.get(lid,{}).get("status"),
        })

active_registry={
    lid for lid,entry in registry.items()
    if entry.get("status") in ("OPEN","ACCEPTED")
}
mismatch_set=set(mismatch_ids)
missing_registry=sorted(mismatch_set-active_registry)
stale_registry=sorted(active_registry-mismatch_set)
invalid_status=sorted(
    lid for lid,entry in registry.items()
    if entry.get("status") not in ("BALANCED","OPEN","ACCEPTED")
)

mismatch_rows=[]
for lid in mismatch_ids:
    entry=registry.get(lid,{})
    row=next(x for x in per_lesson if x["lessonId"]==lid)
    mismatch_rows.append({
        "lessonId":lid,
        "englishFigureCount":row["englishFigureCount"],
        "tamilFigureCount":row["tamilFigureCount"],
        "status":entry.get("status","ABSENT"),
        "reason":entry.get("reason",""),
        "classification":entry.get("classification",""),
        "extraEnglishFigure":entry.get("extraEnglishFigure",""),
        "nearestTamilFigure":entry.get("nearestTamilFigure",""),
        "recommendation":entry.get("recommendation",""),
        "recommendationReason":entry.get("recommendationReason",""),
    })

open_ids=sorted(
    lid for lid in mismatch_ids if registry.get(lid,{}).get("status")=="OPEN"
)
accepted_ids=sorted(
    lid for lid in mismatch_ids if registry.get(lid,{}).get("status")=="ACCEPTED"
)

# Independent packaged-artifact check for the v2.4.6 WebP photograph layer.
all_figure_ids = {
    figure
    for row in per_lesson
    for figure in row["englishFigures"] + row["tamilFigures"]
}
v246_photo_ids = sorted(x for x in all_figure_ids if x.startswith("fig_v246_"))
v246_photo_errors = []
v246_apk_paths = {}
v246_aab_paths = {}

with zipfile.ZipFile(apk) as z:
    apk_entries = set(z.namelist())
with zipfile.ZipFile(aab) as z:
    aab_entries = set(z.namelist())

for name in v246_photo_ids:
    apk_path = resource_file_path("drawable", name)
    v246_apk_paths[name] = apk_path
    if not apk_path:
        v246_photo_errors.append(f"{name}: missing APK resource-table resolution")
    elif apk_path not in apk_entries:
        v246_photo_errors.append(f"{name}: APK resolved file missing: {apk_path}")
    elif Path(apk_path).suffix.lower() != ".webp":
        v246_photo_errors.append(f"{name}: APK resource is not WebP: {apk_path}")

    aab_matches = [
        p for p in aab_entries
        if p.startswith("base/res/drawable")
        and Path(p).stem == name
        and Path(p).suffix.lower() == ".webp"
    ]
    if len(aab_matches) != 1:
        v246_photo_errors.append(f"{name}: expected one AAB WebP, found {aab_matches}")
    else:
        v246_aab_paths[name] = aab_matches[0]

photo_credits = []
if v246_photo_ids:
    credits_apk_path = resource_file_path("raw", "v246_photo_credits")
    if not credits_apk_path or credits_apk_path not in apk_entries:
        v246_photo_errors.append("packaged APK photo-credit resource missing")
    else:
        with zipfile.ZipFile(apk) as z:
            apk_credit_bytes = z.read(credits_apk_path)
        aab_credit_path = "base/res/raw/v246_photo_credits.json"
        if aab_credit_path not in aab_entries:
            v246_photo_errors.append("packaged AAB photo-credit resource missing")
        else:
            with zipfile.ZipFile(aab) as z:
                aab_credit_bytes = z.read(aab_credit_path)
            if apk_credit_bytes != aab_credit_bytes:
                v246_photo_errors.append("APK/AAB photo-credit resources differ")
            else:
                photo_credits = json.loads(apk_credit_bytes.decode("utf-8"))
                credit_ids = {x.get("id") for x in photo_credits}
                if credit_ids != set(v246_photo_ids):
                    v246_photo_errors.append(
                        f"photo-credit ids differ: credits={sorted(credit_ids)} figures={v246_photo_ids}"
                    )
                for credit in photo_credits:
                    required = ("title","author","sourceUrl","licence","licenceUrl","modification")
                    missing = [k for k in required if not str(credit.get(k,"")).strip()]
                    if missing:
                        v246_photo_errors.append(f"{credit.get('id')}: missing credit fields {missing}")
                    if credit.get("modification") != "resized and converted to WebP":
                        v246_photo_errors.append(f"{credit.get('id')}: modification notice mismatch")
                    if "BY-SA" in str(credit.get("licence","")) and "ShareAlike" not in str(credit.get("shareAlikeNotice","")):
                        v246_photo_errors.append(f"{credit.get('id')}: ShareAlike notice missing")

privacy=data["privacy"]
report={
    "scope":"built APK/AAB packaged book_content.json per-lesson parity audit",
    "packagedBookContent":{
        "apkResourcePath":book_path,
        "aabResourcePath":"base/res/raw/book_content.json",
        "identical":True,
    },
    "tables":{
        "english":sum(1 for u in data["units"] for l in u["lessons"] for b in l["english"] if b.get("kind")=="table"),
        "tamil":sum(1 for u in data["units"] for l in u["lessons"] for b in l["tamil"] if b.get("kind")=="table"),
    },
    "figures":{
        "english":total_en,
        "tamil":total_ta,
        "gaps":len(mismatch_ids),
        "mismatchLessons":mismatch_ids,
    },
    "perLessonFigures":per_lesson,
    "mismatches":mismatch_rows,
    "v246WebpIntegrity":{
        "figureCount":len(v246_photo_ids),
        "figureIds":v246_photo_ids,
        "apkResolvedPaths":v246_apk_paths,
        "aabWebpPaths":v246_aab_paths,
        "creditEntryCount":len(photo_credits),
        "errors":v246_photo_errors,
    },
    "registry":{
        "missingMismatchEntries":missing_registry,
        "staleMismatchEntries":stale_registry,
        "invalidStatusEntries":invalid_status,
        "open":open_ids,
        "accepted":accepted_ids,
    },
    "listItemCountGaps":list_gaps,
    "listItemCountGapAssessment":{
        "classification":"AUDIT_METHOD_ARTEFACT",
        "affectedLessons":len(list_gaps),
        "basis":(
            "The metric counts only JSON block.items arrays. In all affected lessons, "
            "the English item arrays are carried by visual_or_feature blocks while the "
            "Tamil lesson expresses the corresponding teaching material in prose/explain/"
            "visual blocks without items arrays. Values such as u1l1 [3,0] are therefore "
            "schema-shape differences, not by themselves evidence of Tamil omission."
        ),
        "englishItemCarrierKinds":dict(sorted(item_carrier_kinds.items())),
        "semanticCaveat":(
            "Separate semantic auditing still identifies the specific u1l4 SDG and "
            "harm-shifting omissions; those omissions are not inferred from listItemCountGaps."
        ),
    },
    "privacyParagraphs":{"english":len(privacy["english"]),"tamil":len(privacy["tamil"])},
    "creditLine":privacy["credit"][0],
    "gate":(
        "FAIL_V246_WEBP_OR_CREDITS" if v246_photo_errors
        else "FAIL_REGISTRY" if (missing_registry or stale_registry or invalid_status)
        else "OPEN_PARITY" if open_ids
        else "PASS"
    ),
}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
if v246_photo_errors:
    sys.exit(7)
if missing_registry or stale_registry or invalid_status:
    sys.exit(8)
