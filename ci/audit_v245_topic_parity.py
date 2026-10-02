#!/usr/bin/env python3
from pathlib import Path
import json
import sys

BOOK = Path("app/src/main/res/raw/book_content.json")
ALLOWLIST = Path("../../ci/parity-allowlist.json")
OUT = Path("V245_TOPIC_PARITY_AUDIT.json")
DRAWABLE = Path("app/src/main/res/drawable-nodpi")
RAW = Path("app/src/main/res/raw")

data = json.loads(BOOK.read_text(encoding="utf-8"))
allow = json.loads(ALLOWLIST.read_text(encoding="utf-8"))

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

resources = {
    p.stem for p in DRAWABLE.glob("fig_*_en.png")
} | {
    p.stem for p in RAW.glob("sci_*.svg")
}
all_refs = []
blank = []
per_lesson = []
mismatches = []
topic_pairs = {}

for unit in data["units"]:
    for lesson in unit["lessons"]:
        lid = lesson["id"]
        en = figures(lesson, "english")
        ta = figures(lesson, "tamil")
        for lang, items in (("english", en), ("tamil", ta)):
            for item in items:
                if not item["id"]:
                    blank.append({"lessonId": lid, "language": lang, "kind": item["kind"]})
                else:
                    all_refs.append(item["id"])
        row = {
            "lessonId": lid,
            "englishCount": len(en),
            "tamilCount": len(ta),
            "english": en,
            "tamil": ta,
        }
        per_lesson.append(row)
        if len(en) != len(ta):
            mismatches.append(lid)
            entry = allow.get(lid)
            if entry is None:
                topic_pairs[lid] = {"status": "UNLISTED_MISMATCH"}
            else:
                mapped_en = {
                    ref
                    for group in entry.get("matchedTopics", []) + entry.get("openTopics", [])
                    for ref in group.get("english", [])
                }
                mapped_ta = {
                    ref
                    for group in entry.get("matchedTopics", []) + entry.get("openTopics", [])
                    for ref in group.get("tamil", [])
                }
                actual_en = {x["id"] for x in en}
                actual_ta = {x["id"] for x in ta}
                assert mapped_en == actual_en, (lid, "english topic map", mapped_en, actual_en)
                assert mapped_ta == actual_ta, (lid, "tamil topic map", mapped_ta, actual_ta)
                topic_pairs[lid] = entry
        else:
            topic_pairs[lid] = {
                "status": "BALANCED",
                "topics": [
                    {
                        "topic": e["title"] or e["caption"] or e["id"],
                        "english": [e["id"]],
                        "tamil": [t["id"]],
                        "tamilTitle": t["title"],
                    }
                    for e, t in zip(en, ta)
                ],
            }

ref_set = {r for r in all_refs if r}
unresolved = sorted(ref_set - resources)
orphaned = sorted(resources - ref_set)

expected_open = {"u2l1", "u2l5", "u4l6", "u5l1"}
assert set(mismatches) == expected_open, (mismatches, expected_open)
assert set(allow) == expected_open, (set(allow), expected_open)

open_entries = sorted(
    lid for lid, entry in allow.items()
    if entry.get("status") == "OPEN"
)
accepted_entries = sorted(
    lid for lid, entry in allow.items()
    if entry.get("status") == "ACCEPTED"
)
invalid_status = sorted(
    lid for lid, entry in allow.items()
    if entry.get("status") not in ("OPEN", "ACCEPTED")
)

deleted_topic_checks = {
    "eutrophication": {
        "deletedEnglish": "fig_033_u04_en",
        "deletedResourceAbsent": "fig_033_u04_en" not in resources,
        "englishAlternatives": ["fig_034_u04_en", "fig_035_u04_en"],
        "tamilCounterparts": ["sci_u04_l43_eutrophication_ta", "sci_u04_l43_lake_ta"],
        "labelSpecific": True,
        "recommendation": "Keep fig_033 deleted; the lesson retains two English diagrams paired by topic with two Tamil SVGs."
    },
    "climate-to-adaptation": {
        "deletedEnglish": "fig_048_u05_en",
        "deletedResourceAbsent": "fig_048_u05_en" not in resources,
        "englishAlternatives": ["fig_049_u05_en"],
        "tamilCounterparts": ["sci_u05_l53_mitigation_ta"],
        "labelSpecific": True,
        "recommendation": "Keep fig_048 deleted; the more specific mitigation/adaptation English diagram remains paired with the Tamil SVG."
    },
    "hazard-to-resilience": {
        "deletedEnglish": "fig_057_u07_en",
        "deletedResourceAbsent": "fig_057_u07_en" not in resources,
        "englishAlternatives": ["fig_058_u07_en"],
        "tamilCounterparts": ["sci_u07_l73_risk_ta"],
        "labelSpecific": True,
        "recommendation": "Keep fig_057 deleted; the more specific disaster-risk English diagram remains paired with the Tamil SVG."
    },
}
for check in deleted_topic_checks.values():
    assert check["deletedResourceAbsent"]
    assert all(x in ref_set for x in check["englishAlternatives"])
    assert all(x in ref_set for x in check["tamilCounterparts"])

report = {
    "scope": "per-lesson diagram-topic parity and resource integrity",
    "lessonCount": len(per_lesson),
    "englishFigureCount": sum(x["englishCount"] for x in per_lesson),
    "tamilFigureCount": sum(x["tamilCount"] for x in per_lesson),
    "perLesson": per_lesson,
    "topicPairs": topic_pairs,
    "mismatchLessons": mismatches,
    "allowlistOpen": open_entries,
    "allowlistAccepted": accepted_entries,
    "invalidAllowlistStatus": invalid_status,
    "blankFigureKeys": blank,
    "unresolvedFigureRefs": unresolved,
    "orphanedTeachingResources": orphaned,
    "deletedTopicChecks": deleted_topic_checks,
    "gate": "FAIL_OPEN_PARITY" if open_entries else "PASS",
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))

hard_errors = bool(blank or unresolved or orphaned or invalid_status)
unlisted = any(topic_pairs[lid].get("status") == "UNLISTED_MISMATCH" for lid in mismatches)
if hard_errors or unlisted:
    sys.exit(8)
if open_entries:
    print("OPEN parity entries block FINAL: " + ", ".join(open_entries), file=sys.stderr)
    sys.exit(9)
