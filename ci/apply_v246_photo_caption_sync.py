#!/usr/bin/env python3
from pathlib import Path
import json

MANIFEST = Path("../../ci/v246_visual_photo_manifest.json")
BOOK = Path("app/src/main/res/raw/book_content.json")
OUT = Path("V246_PHOTO_CAPTION_SYNC_AUDIT.json")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
book = json.loads(BOOK.read_text(encoding="utf-8"))
by_id = {x["id"]: x for x in manifest}
assert len(by_id) == 8, len(by_id)

targets = {}
for unit in book["units"]:
    for lesson in unit["lessons"]:
        for lang_key, title_key, caption_key in (
            ("english", "en_title", "en_caption"),
            ("tamil", "ta_title", "ta_caption"),
        ):
            for block in lesson[lang_key]:
                fig = block.get("figure")
                if fig in by_id:
                    item = by_id[fig]
                    assert str(item["lesson"]) == str(lesson["number"]), (fig, item["lesson"], lesson["number"])
                    block["title"] = item[title_key]
                    block["caption"] = item[caption_key]
                    targets.setdefault(fig, set()).add(lang_key)

assert set(targets) == set(by_id), (set(by_id) - set(targets), set(targets) - set(by_id))
assert all(v == {"english", "tamil"} for v in targets.values()), targets

BOOK.write_text(json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
text = BOOK.read_text(encoding="utf-8")

stale = ["AnkClix", "Selvaganesh17", "Frederick Noronha"]
assert not any(name in text for name in stale), [name for name in stale if name in text]

expected = {
    "fig_v246_delhi_smog": ("Sumita Roy Dutta", "CC BY-SA 4.0 International"),
    "fig_v246_algal_bloom": ("Christian Fischer", "CC BY-SA 3.0 Unported"),
    "fig_v246_rainwater_harvesting": ("Biswarup Ganguly", "CC BY 3.0 Unported"),
}
for fig, (author, licence) in expected.items():
    item = by_id[fig]
    assert item["author"] == author, (fig, item["author"])
    assert item["license"] == licence, (fig, item["license"])
    assert author in item["en_caption"] and author in item["ta_caption"], fig
    assert licence in item["en_caption"] and licence in item["ta_caption"], fig

OUT.write_text(json.dumps({
    "scope": "post-atlas bilingual photograph caption/credit synchronisation",
    "photoCount": len(by_id),
    "syncedIds": sorted(targets),
    "replacedPhotoIds": sorted(expected),
    "staleCreditNamesAbsent": stale,
    "licencesScreenSource": "app/src/main/res/raw/v246_photo_credits.json",
    "status": "PASS",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
