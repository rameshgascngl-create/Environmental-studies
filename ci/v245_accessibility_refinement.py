#!/usr/bin/env python3
from pathlib import Path

p=Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/SvgFigureBlock.kt")
s=p.read_text()
old='''    val figureDescription = block.alt.ifBlank {
        svgAriaLabel(context, resId).orEmpty().ifBlank {
            block.title.ifBlank { block.caption.ifBlank { "Teaching figure" } }
        }
    }'''
new='''    val figureDescription = svgAriaLabel(context, resId).orEmpty().ifBlank {
        block.alt.ifBlank {
            block.title.ifBlank { block.caption.ifBlank { "Teaching figure" } }
        }
    }'''
if old not in s:
    raise SystemExit("Expected v2.4.5 SVG semantics anchor not found")
p.write_text(s.replace(old,new,1))
print("V245_SVG_ARIA_SEMANTICS_PASS")
