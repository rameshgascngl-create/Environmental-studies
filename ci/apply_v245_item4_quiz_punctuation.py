#!/usr/bin/env python3
from pathlib import Path
import json

BOOK=Path("app/src/main/res/raw/book_content.json")
data=json.loads(BOOK.read_text(encoding="utf-8"))
quizzes=[q for unit in data["units"] for q in unit["quiz"]]
assert len(quizzes)==58

q1=data["units"][0]["quiz"][0]
expected="Concept to remember Environmental Studies is not merely 'ecology' or 'pollution studies'. It studies relationships among Earth systems, organisms and human society."
replacement="Concept to remember: Environmental Studies is not merely 'ecology' or 'pollution studies'. It studies relationships among Earth systems, organisms and human society."
assert q1["explanationEn"]==expected, q1["explanationEn"]
q1["explanationEn"]=replacement

BOOK.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

quizzes=[q for unit in data["units"] for q in unit["quiz"]]
bad=[]
for index,q in enumerate(quizzes,1):
    en=q.get("explanationEn","").strip()
    ta=q.get("explanationTa","").strip()
    if not en or not ta:
        bad.append((index,"missing explanation"))
    if en.startswith("Concept to remember ") and not en.startswith("Concept to remember: "):
        bad.append((index,"English Concept to remember prefix missing colon"))
    if ta.startswith("முக்கியக் கருத்து ") and not ta.startswith("முக்கியக் கருத்து: "):
        bad.append((index,"Tamil முக்கியக் கருத்து prefix missing colon"))
assert not bad,bad

Path("V245_ITEM4_QUIZ_PUNCTUATION_AUDIT.json").write_text(
    json.dumps({
        "questions":len(quizzes),
        "u1_q1_explanationEn":q1["explanationEn"],
        "colon_consistency":"PASS",
        "content_changes":1,
    },ensure_ascii=False,indent=2)+"\n",
    encoding="utf-8",
)
print("ITEM4_QUIZ_EXPLANATION_PUNCTUATION_PASS",len(quizzes))
