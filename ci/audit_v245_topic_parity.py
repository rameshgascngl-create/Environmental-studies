#!/usr/bin/env python3
from pathlib import Path
import json
import sys

BOOK = Path("app/src/main/res/raw/book_content.json")
REGISTRY = Path("../../ci/parity-allowlist.json")
OUT = Path("V245_TOPIC_PARITY_AUDIT.json")
DRAWABLE = Path("app/src/main/res/drawable-nodpi")
RAW = Path("app/src/main/res/raw")

data = json.loads(BOOK.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

def figures(lesson, lang):
    return [
        {
            "id": b.get("figure", "").strip(),
            "kind": b.get("kind"),
            "title": b.get("title", "").strip(),
            "caption": b.get("caption", "").strip(),
        }
        for b in lesson[lang]
        if b.get("kind") in ("figure", "svg_figure")
    ]

lessons = {
    lesson["id"]: lesson
    for unit in data["units"]
    for lesson in unit["lessons"]
}
assert len(lessons) == 46, len(lessons)
assert set(registry) == set(lessons), (
    "registry coverage mismatch",
    sorted(set(lessons) - set(registry)),
    sorted(set(registry) - set(lessons)),
)

resources = {
    p.stem for p in DRAWABLE.glob("fig_*")
    if p.suffix.lower() in (".png", ".webp", ".jpg", ".jpeg")
} | {
    p.stem for p in RAW.glob("sci_*.svg")
}

all_refs = []
blank = []
per_lesson = []
registry_errors = []
open_entries = []
accepted_entries = []
balanced_entries = []

for lid in sorted(lessons):
    lesson = lessons[lid]
    en = figures(lesson, "english")
    ta = figures(lesson, "tamil")
    actual_en = {x["id"] for x in en if x["id"]}
    actual_ta = {x["id"] for x in ta if x["id"]}
    registry_en = {
        ref for ref in actual_en
        if not ref.startswith(("sci_v246_", "fig_v246_"))
    }
    registry_ta = {
        ref for ref in actual_ta
        if not ref.startswith(("sci_v246_", "fig_v246_"))
    }
    v246_en = actual_en - registry_en
    v246_ta = actual_ta - registry_ta

    for lang, items in (("english", en), ("tamil", ta)):
        for item in items:
            if not item["id"]:
                blank.append({"lessonId": lid, "language": lang, "kind": item["kind"]})
            else:
                all_refs.append(item["id"])

    entry = registry[lid]
    status = entry.get("status")
    matched = entry.get("matchedTopics", [])
    opened = entry.get("openTopics", [])
    groups = matched + opened

    mapped_en = [ref for group in groups for ref in group.get("english", [])]
    mapped_ta = [ref for group in groups for ref in group.get("tamil", [])]

    if len(mapped_en) != len(set(mapped_en)):
        registry_errors.append({"lessonId": lid, "error": "duplicate English registry reference"})
    if len(mapped_ta) != len(set(mapped_ta)):
        registry_errors.append({"lessonId": lid, "error": "duplicate Tamil registry reference"})
    if set(mapped_en) != registry_en:
        registry_errors.append({
            "lessonId": lid,
            "error": "English legacy topic map does not equal legacy lesson references",
            "mapped": sorted(set(mapped_en)),
            "actual": sorted(registry_en),
        })
    if set(mapped_ta) != registry_ta:
        registry_errors.append({
            "lessonId": lid,
            "error": "Tamil legacy topic map does not equal legacy lesson references",
            "mapped": sorted(set(mapped_ta)),
            "actual": sorted(registry_ta),
        })

    # v2.4.6 atlas parity is deterministic by resource naming and is audited
    # after the atlas is applied. Shared photographs must occur in both
    # languages; SVGs must form exact _e / _t pairs.
    v246_photo_en = {ref for ref in v246_en if ref.startswith("fig_v246_")}
    v246_photo_ta = {ref for ref in v246_ta if ref.startswith("fig_v246_")}
    if v246_photo_en != v246_photo_ta:
        registry_errors.append({
            "lessonId": lid,
            "error": "v2.4.6 shared photograph parity mismatch",
            "english": sorted(v246_photo_en),
            "tamil": sorted(v246_photo_ta),
        })

    v246_svg_en = {ref for ref in v246_en if ref.startswith("sci_v246_")}
    v246_svg_ta = {ref for ref in v246_ta if ref.startswith("sci_v246_")}
    bad_v246_en = sorted(ref for ref in v246_svg_en if not ref.endswith("_e"))
    bad_v246_ta = sorted(ref for ref in v246_svg_ta if not ref.endswith("_t"))
    if bad_v246_en or bad_v246_ta:
        registry_errors.append({
            "lessonId": lid,
            "error": "v2.4.6 SVG suffix contract mismatch",
            "english": bad_v246_en,
            "tamil": bad_v246_ta,
        })
    v246_svg_en_keys = {ref[:-2] for ref in v246_svg_en if ref.endswith("_e")}
    v246_svg_ta_keys = {ref[:-2] for ref in v246_svg_ta if ref.endswith("_t")}
    if v246_svg_en_keys != v246_svg_ta_keys:
        registry_errors.append({
            "lessonId": lid,
            "error": "v2.4.6 SVG bilingual pair mismatch",
            "englishOnly": sorted(v246_svg_en_keys - v246_svg_ta_keys),
            "tamilOnly": sorted(v246_svg_ta_keys - v246_svg_en_keys),
        })

    for group in matched:
        if not group.get("topic") or not group.get("english") or not group.get("tamil"):
            registry_errors.append({
                "lessonId": lid,
                "error": "matched topic must name the topic and map both languages",
                "topic": group,
            })

    for group in opened:
        if not group.get("topic"):
            registry_errors.append({"lessonId": lid, "error": "open topic has no topic name"})
        if bool(group.get("english")) == bool(group.get("tamil")):
            registry_errors.append({
                "lessonId": lid,
                "error": "open topic must identify an unresolved one-sided visual",
                "topic": group,
            })

    raw_mismatch = len(en) != len(ta)
    if status == "BALANCED":
        balanced_entries.append(lid)
        if opened:
            registry_errors.append({"lessonId": lid, "error": "BALANCED entry contains openTopics"})
        if raw_mismatch:
            registry_errors.append({"lessonId": lid, "error": "BALANCED entry has unequal raw counts"})
    elif status == "ACCEPTED":
        accepted_entries.append(lid)
        if opened:
            registry_errors.append({"lessonId": lid, "error": "ACCEPTED entry contains openTopics"})
        if not raw_mismatch:
            registry_errors.append({
                "lessonId": lid,
                "error": "stale ACCEPTED exception: raw counts are balanced; remove the exception",
            })
        if not entry.get("reason", "").strip():
            registry_errors.append({"lessonId": lid, "error": "ACCEPTED entry requires a reason"})
    elif status == "OPEN":
        open_entries.append(lid)
        if not opened:
            registry_errors.append({"lessonId": lid, "error": "OPEN entry has no openTopics"})
        if not entry.get("reason", "").strip():
            registry_errors.append({"lessonId": lid, "error": "OPEN entry requires a reason"})
    else:
        registry_errors.append({"lessonId": lid, "error": f"invalid registry status: {status}"})

    per_lesson.append({
        "lessonId": lid,
        "englishCount": len(en),
        "tamilCount": len(ta),
        "rawCountMismatch": raw_mismatch,
        "registryStatus": status,
        "matchedTopics": matched,
        "openTopics": opened,
        "english": en,
        "tamil": ta,
    })

ref_set = set(all_refs)
unresolved = sorted(ref_set - resources)
orphaned = sorted(resources - ref_set)

deleted_topic_checks = {
    "eutrophication": {
        "deletedEnglish": "fig_033_u04_en",
        "deletedResourceAbsent": "fig_033_u04_en" not in resources,
        "englishAlternatives": ["fig_034_u04_en", "fig_035_u04_en"],
        "tamilCounterparts": ["sci_u04_l43_eutrophication_ta", "sci_u04_l43_lake_ta"],
        "classification": "label-specific",
        "recommendation": "Keep fig_033 deleted; two retained English diagrams remain explicitly topic-paired with the two Tamil SVGs."
    },
    "climate-to-adaptation": {
        "deletedEnglish": "fig_048_u05_en",
        "deletedResourceAbsent": "fig_048_u05_en" not in resources,
        "englishAlternatives": ["fig_049_u05_en"],
        "tamilCounterparts": ["sci_u05_l53_mitigation_ta"],
        "classification": "label-specific",
        "recommendation": "Keep fig_048 deleted; the retained mitigation/adaptation English diagram is explicitly topic-paired with the Tamil SVG."
    },
    "hazard-to-resilience": {
        "deletedEnglish": "fig_057_u07_en",
        "deletedResourceAbsent": "fig_057_u07_en" not in resources,
        "englishAlternatives": ["fig_058_u07_en"],
        "tamilCounterparts": ["sci_u07_l73_risk_ta"],
        "classification": "label-specific",
        "recommendation": "Keep fig_057 deleted; the retained disaster-risk English diagram is explicitly topic-paired with the Tamil SVG."
    },
}
for name, check in deleted_topic_checks.items():
    if not check["deletedResourceAbsent"]:
        registry_errors.append({"topic": name, "error": "deleted English resource unexpectedly present"})
    for ref in check["englishAlternatives"] + check["tamilCounterparts"]:
        if ref not in ref_set:
            registry_errors.append({"topic": name, "error": f"required retained counterpart missing: {ref}"})

decision_rows = [
    {
        "lessonId": lid,
        "extraEnglishFigure": registry[lid].get("extraEnglishFigure", ""),
        "nearestTamilFigure": registry[lid].get("nearestTamilFigure", ""),
        "status": registry[lid].get("status", ""),
        "reason": registry[lid].get("reason", ""),
    }
    for lid in open_entries
]

report = {
    "scope": "explicit per-lesson diagram-topic parity and resource integrity",
    "lessonCount": len(per_lesson),
    "englishFigureCount": sum(x["englishCount"] for x in per_lesson),
    "tamilFigureCount": sum(x["tamilCount"] for x in per_lesson),
    "balancedRegistryEntries": balanced_entries,
    "acceptedRegistryEntries": accepted_entries,
    "openRegistryEntries": open_entries,
    "userDecisionRows": decision_rows,
    "perLesson": per_lesson,
    "blankFigureKeys": blank,
    "unresolvedFigureRefs": unresolved,
    "orphanedTeachingResources": orphaned,
    "registryErrors": registry_errors,
    "deletedTopicChecks": deleted_topic_checks,
    "gate": (
        "FAIL_RESOURCE_OR_REGISTRY"
        if (blank or unresolved or orphaned or registry_errors)
        else "FAIL_OPEN_PARITY"
        if open_entries
        else "PASS"
    ),
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))

if blank or unresolved or orphaned or registry_errors:
    sys.exit(8)
if open_entries:
    print(
        "OPEN parity entries block FINAL: " + ", ".join(open_entries),
        file=sys.stderr,
    )
    sys.exit(9)
