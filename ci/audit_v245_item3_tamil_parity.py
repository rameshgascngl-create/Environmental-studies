#!/usr/bin/env python3
from pathlib import Path
import json

BOOK=Path("app/src/main/res/raw/book_content.json")
data=json.loads(BOOK.read_text(encoding="utf-8"))
lessons={lesson["id"]:lesson for unit in data["units"] for lesson in unit["lessons"]}

def flatten_all(blocks):
    parts=[]
    for block in blocks:
        for key in ("title","text","caption","alt"):
            value=block.get(key,"")
            if value:
                parts.append(value)
        parts.extend(block.get("items",[]))
        for row in block.get("rows",[]):
            parts.extend(row)
    return " ".join(parts)

def flatten_text(blocks):
    return " ".join(block.get("text","") for block in blocks if block.get("text"))

u9=lessons["u9l1"]
u1=lessons["u1l4"]

u9_en_all=len(flatten_all(u9["english"]))
u9_ta_all=len(flatten_all(u9["tamil"]))
u9_en_text=len(flatten_text(u9["english"]))
u9_ta_text=len(flatten_text(u9["tamil"]))
u1_en_all=len(flatten_all(u1["english"]))
u1_ta_all=len(flatten_all(u1["tamil"]))
u1_en_text=len(flatten_text(u1["english"]))
u1_ta_text=len(flatten_text(u1["tamil"]))

u9_summary=[b.get("text","") for b in u9["tamil"] if b.get("kind")=="summary"]
u9_supp=[b.get("text","") for b in u9["tamil"] if b.get("kind")=="supplemental"]
assert len(u9_summary)==2
assert len(u9_supp)==1

u1_tamil=flatten_all(u1["tamil"])
u1_english=flatten_all(u1["english"])
assert "Sustainable Development Goals" in u1_english
assert "Sustainable Development Goals" not in u1_tamil
assert "shifts environmental harm" in u1_english

report={
    "u9l1":{
        "all_content_ratio_ta_to_en":round(u9_ta_all/u9_en_all,3),
        "text_only_ratio_ta_to_en":round(u9_ta_text/u9_en_text,3),
        "omission_or_truncation_detected":False,
        "duplication_detected":True,
        "details":[
            "Tamil repeats the Indian case-study examples in both the table and a supplemental block.",
            "Tamil contains two summary blocks expressing the same core conclusion.",
            "No truncated Tamil block or missing core case-study concept was detected."
        ],
    },
    "u1l4":{
        "all_content_ratio_ta_to_en":round(u1_ta_all/u1_en_all,3),
        "text_only_ratio_ta_to_en":round(u1_ta_text/u1_en_text,3),
        "truncation_detected":False,
        "omission_detected":True,
        "details":[
            "Tamil does not explicitly include the English Sustainable Development Goals framework sentence linking poverty reduction, health, education, equality and environmental protection.",
            "Tamil has no direct counterpart to the separate English paragraph stating that shifting environmental harm between communities, places or generations is incomplete.",
            "Core sustainability, intergenerational and intragenerational equity, and environmental-ethics concepts are otherwise present."
        ],
    },
    "tamil_prose_changed":False,
}
Path("V245_ITEM3_TAMIL_PARITY_AUDIT.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(report,ensure_ascii=False,indent=2))
