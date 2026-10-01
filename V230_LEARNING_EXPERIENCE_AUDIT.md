# Environmental Studies v2.3.0 — Learning Experience Audit

## Requested upgrades
1. Preserve the validated mobile navigation from v2.2.5.
2. Remember the last-read lesson separately within each unit.
3. Mark it visibly as **Continue / தொடர்க**.
4. Make the visual experience richer and more realistic.
5. Add more animation pages.
6. Add audio explanation for animations.

## Implementation
### Continue / தொடர்க
Each lesson visit stores the lesson ID under its own unit key. Unit opening pages display a prominent Continue card and mark the last-read row. Home unit cards expose Continue directly when a saved lesson exists.

### Visual realism
Nine unit-specific context scenes use depth, gradients, atmospheric layering, water/terrain/vegetation/city elements and environmental context. These enrich the home/unit experience while leaving scientific figures intact for precise teaching.

### Animation expansion
The existing four climate animations are retained. Six additional process animations are added:
- Eutrophication
- Groundwater recharge
- Carbon cycle
- Food-chain energy flow
- Urban heat island
- Circular economy

### Audio explanation
All ten animation topics support English or Tamil narration through Android TextToSpeech. Audio can be stopped immediately when switching topics. If a Tamil or English voice is not installed, the app reports that condition rather than silently failing.

## Content freeze
The authoritative `book_content.json` must remain byte-identical:
`1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40`

No scientific lesson prose, Tamil terminology, English prose or figure routing is authorised to change in this phase.

## Physical-device QA
- Visit different lessons in at least three units and verify each unit remembers its own last-read lesson.
- Confirm Continue / தொடர்க opens the correct saved lesson from Home and Unit Contents.
- Check unit scene rendering in portrait/landscape and large-text mode.
- Run every animation for at least one full cycle and rotate the device.
- Test English Listen and Tamil விளக்கம் கேட்க.
- Verify Stop interrupts narration.
- Verify missing TTS language data produces a clear message.
- Confirm animations remain smooth on the validated phone without app closure or memory pressure.
