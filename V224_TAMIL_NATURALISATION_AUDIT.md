# Environmental Studies v2.2.4 — Tamil Naturalisation & Terminology Consistency Audit

## Why this pass is required
The v2.2.3 coherence pass removed major literal translation and sentence-structure defects, but a second lexical audit found residual administrative/machine-like forms, especially repeated `தொடர்பான`, `தொடர்புடைய`, `தொடர்புடன்` and generic `பரஸ்பர தொடர்பு` constructions. The same scan also exposed a small set of terminology drift in review prompts, unit pathways, quizzes and supplemental material.

## Audited result
- 9 units / 46 lessons retained.
- 46 Tamil review prompts rebuilt from the canonical Tamil lesson titles.
- 9 Tamil unit pathways rebuilt from the canonical Tamil lesson titles.
- 19 lesson bodies receive context-sensitive naturalisation.
- 125 JSON fields differ from the v2.2.3 baseline.
- English lesson payload remains unchanged.
- Figure/resource routing remains unchanged.

## Main naturalisation decisions
- `ஒன்றோடொன்று தொடர்புடன் செயல்படுகின்றன` → `ஒன்றையொன்று சார்ந்து செயல்படுகின்றன` where genuine interdependence is intended.
- `தொடர்பான முக்கியக் கருத்துகள்` review-template language is removed; review prompts are generated from the Tamil lesson title.
- `தொடர்புடைய` is replaced by `இணைந்த`, `சார்ந்த`, `பொருந்தும்`, or explicit causal wording according to meaning.
- `தொடர்புடைய தரப்புகள்` → `சம்பந்தப்பட்ட தரப்புகள்` in case-study/fieldwork contexts.
- Acid-deposition wording now states the chemical and deposition pathway explicitly instead of saying it is merely “related to” acidic compounds.

## Terminology consistency restored
- `உயிரிய பல்வகைத்தன்மை`
- `சூழ்நிலை மண்டலம்`
- `பசுமைக்குடில் விளைவு / பசுமைக்குடில் வாயு`
- `மீள்தன்மை`
- `மிகை உணவூட்டம் (Eutrophication)`
- `உயிரிமருத்துவக் கழிவு`
- `இடர்` for hazard and `அபாயம்` for risk
- `உமிழ்வு` in the climate-emissions context
- `சூழல் உள் பாதுகாப்பு` for in-situ conservation

## Deliberate retention
Not every occurrence of `தொடர்பு` is an error. Scientific phrases such as `உணவுத் தொடர்பு`, `சூழலியல் தொடர்புகள்`, `மனித–வனவிலங்கு தொடர்பு` and communication-related uses remain. `பரஸ்பர நன்மை` is also retained in the ecological-interaction context rather than being altered merely because it contains `பரஸ்பர`.

## Static blacklist after correction
The following residual forms are required to be absent from the built book payload:
`தொடர்புடன்`, `தொடர்பான`, `தொடர்புடைய`, `பரஸ்பர தொடர்பு`, `உயிரினப் பன்மை`, `பசுமை இல்ல`, `சூழல்மண்டலம்`, `சூழல் மண்டலம்`, `மீள்திறன்`, `பேரிடர் ஆபத்து`, `உயிரி மருத்துவக் கழிவு`, `மிகை ஊட்டச்சத்துச் செறிவூட்டல்`.

## Device-QA gate
Static editorial success does not prove Tamil glyph shaping or visual fit. Physical-device QA remains mandatory for Tamil line breaking, conjunct rendering, clipping, diagram labels, normal-scale readability, portrait/landscape layout and English/Tamil switching.
