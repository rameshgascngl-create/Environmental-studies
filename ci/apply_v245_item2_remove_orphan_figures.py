#!/usr/bin/env python3
from pathlib import Path
import json

BOOK = Path("app/src/main/res/raw/book_content.json")
DRAWABLE = Path("app/src/main/res/drawable-nodpi")
data = json.loads(BOOK.read_text(encoding="utf-8"))

remove = {
    "fig_033_u04_en": "Redundant eutrophication pathway; u4l3 already contains the more complete fig_034_u04_en and fig_035_u04_en sequence.",
    "fig_045_u05_en": "Superseded greenhouse-effect sketch; u5l1 uses the complete sci_u05_l51_en and restored fig_046_u05_en visual.",
    "fig_048_u05_en": "Redundant generic climate chain; u5l2 has sci_u05_l52_en and u5l3 has the more specific fig_049_u05_en.",
    "fig_057_u07_en": "Redundant generic hazard-to-resilience chain; u7l3 uses the more specific fig_058_u07_en diagram.",
}

references = set()
for unit in data["units"]:
    for lesson in unit["lessons"]:
        for language in ("english", "tamil"):
            for block in lesson[language]:
                if block.get("kind") in ("figure", "svg_figure") and block.get("figure"):
                    references.add(block["figure"])

deleted = []
for name, reason in remove.items():
    assert name not in references, f"{name} is still referenced"
    path = DRAWABLE / f"{name}.png"
    assert path.is_file(), f"Expected orphan asset missing before deletion: {path}"
    path.unlink()
    deleted.append({"figure": name, "reason": reason})

for item in deleted:
    assert not (DRAWABLE / f"{item['figure']}.png").exists()

Path("V245_ITEM2_ORPHAN_FIGURES.json").write_text(
    json.dumps({"deleted": deleted}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print("ITEM2_ORPHAN_FIGURES_REMOVED", ",".join(item["figure"] for item in deleted))
