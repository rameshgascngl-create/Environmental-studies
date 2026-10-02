#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

BOOK = Path("app/src/main/res/raw/book_content.json")
KEEP = Path("app/src/main/res/raw/keep.xml")
AUDIT = Path("V245_RELEASE_RESOURCE_KEEP_AUDIT.json")

LEGACY = """<resources xmlns:tools="http://schemas.android.com/tools"
    tools:keep="@raw/*" />
"""
EXPECTED = """<resources xmlns:tools="http://schemas.android.com/tools"
    tools:keep="@drawable/fig_*,@raw/sci_*"
    tools:shrinkMode="strict" />
"""

data = json.loads(BOOK.read_text(encoding="utf-8"))
refs = {
    block.get("figure", "").strip()
    for unit in data["units"]
    for lesson in unit["lessons"]
    for lang in ("english", "tamil")
    for block in lesson[lang]
    if block.get("kind") in ("figure", "svg_figure") and block.get("figure", "").strip()
}
png = sorted(x for x in refs if x.startswith("fig_"))
svg = sorted(x for x in refs if x.startswith("sci_"))
unexpected = sorted(refs - set(png) - set(svg))

assert len(refs) == 96, len(refs)
assert len(png) == 31, len(png)
assert len(svg) == 65, len(svg)
assert not unexpected, unexpected

before = KEEP.read_text(encoding="utf-8") if KEEP.exists() else ""
if before:
    assert before in (LEGACY, EXPECTED), (
        "Existing keep.xml is neither the known legacy rule nor the authorised final rule; "
        "refusing blind overwrite"
    )

changed = before != EXPECTED
if changed:
    KEEP.parent.mkdir(parents=True, exist_ok=True)
    KEEP.write_text(EXPECTED, encoding="utf-8")

assert KEEP.read_text(encoding="utf-8") == EXPECTED

AUDIT.write_text(
    json.dumps(
        {
            "scope": "release resource shrinker keep policy",
            "bookFigureUniqueCount": len(refs),
            "bookPngFigureUniqueCount": len(png),
            "bookSvgFigureUniqueCount": len(svg),
            "keepFile": str(KEEP),
            "legacyPolicyDetected": before == LEGACY,
            "policyChanged": changed,
            "keepSha256": hashlib.sha256(KEEP.read_bytes()).hexdigest(),
            "drawableRule": "@drawable/fig_*",
            "rawRule": "@raw/sci_*",
            "shrinkMode": "strict",
            "shrinkResourcesDisabled": False,
            "figureNamesRenamed": False,
        },
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
print(AUDIT.read_text(encoding="utf-8"))
