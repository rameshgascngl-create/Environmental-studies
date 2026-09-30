# Environmental Studies v2.2.2 — Tamil College-Level Editorial Audit

## Audit objective
Review the complete Tamil lesson layer across all 9 units / 46 lessons and remove school-coaching phrasing, machine-translated constructions, terminology drift, duplicated wording and scientifically weak Tamil formulations while preserving the accepted English/scientific structure.

The target is **Tamil Nadu textbook terminology + undergraduate explanatory register**, not verbatim reproduction of any single textbook.

## Findings in the v2.2.1 Tamil layer
The v2.2.1 pass solved major terminology and scientific-visual defects but still retained systematic editorial artifacts:
- repeated school-style scaffolds such as `முக்கிய சொற்கள்`, `நினைவில் கொள்க`, `சிந்தித்துப் பாருங்கள்`, `கருத்தின் சாரம்`;
- `செயல்முறையும் எடுத்துக்காட்டும்` and `காட்சி வழிக் கற்றல்` constructions that read like generated UI copy rather than college text;
- duplicated or concatenated diagram explanations;
- inconsistency in biodiversity, conservation, climate and disaster-risk terminology;
- over-literal phrases and malformed forms including several duplicated words and inconsistent transliterations;
- imperative-heavy SVG labels in field-learning diagrams.

## Correction classes

### 1. Academic register
Systematic headings are normalized to:
- `முக்கியக் கலைச்சொற்கள்`
- `முக்கியக் கருத்து`
- `சிந்தனை வினா`
- `பாடச்சுருக்கம்`
- `விரிவான விளக்கம்`
- `படக்கருத்து`

### 2. Biodiversity and conservation
Canonical forms include:
- `உயிரிய பல்வகைத்தன்மை`
- `மரபியல் பல்வகைத்தன்மை`
- `சிற்றின பல்வகைத்தன்மை`
- `சூழ்நிலை மண்டல பல்வகைத்தன்மை`
- `சூழல் உள் பாதுகாப்பு`
- `சூழல் வெளிப் பாதுகாப்பு`

The biodiversity and conservation lessons are rewritten as connected explanatory prose rather than definition fragments.

### 3. Climate and atmospheric science
Canonical forms include:
- `பசுமைக்குடில் விளைவு`
- `பசுமைக்குடில் வாயு`
- `தணித்தல்`
- `தழுவல்`
- `மீள்தன்மை`
- `அமிலப் படிவு`
- `ஓசோன் படலச் சிதைவு`
- `மாண்ட்ரியல் நெறிமுறை`

The greenhouse explanation explicitly distinguishes incoming solar radiation, outgoing infrared radiation and absorption/re-emission by greenhouse gases.

### 4. Pollution and health
The Tamil layer distinguishes:
- emission / `உமிழ்வு`
- environmental concentration
- exposure / `வெளிப்பாடு`
- effect
- hazard / `இடர்`
- risk / `அபாயம்`
- vulnerability / `பாதிப்புக்குள்ளாகும் தன்மை`

This removes the previous tendency to use hazard and risk as interchangeable Tamil words.

### 5. Disaster-risk terminology
Lesson 7.3 is rewritten around the formal conceptual relationship among:
`இடர் · வெளிப்பாடு · பாதிப்புக்குள்ளாகும் தன்மை · தயார்நிலை · மீள்தன்மை`.

### 6. Field-learning register
Fieldwork lessons retain practical intent but replace conversational command fragments in SVGs with academically neutral nominal labels where appropriate.

### 7. Scientific prose repair
Twenty-two visual-learning paragraphs that were duplicated, concatenated or too schematic are rewritten as complete causal scientific explanations.

## Integrity requirements
The correction is accepted only if all of the following pass:
- 9 units and 46 lessons remain.
- English unit titles, English lesson titles and English lesson payload are byte/logically unchanged by the Tamil pass.
- Tamil figure/resource routing is unchanged.
- all SVG files remain valid XML.
- the deprecated phrases defined by the editorial gate are absent.
- the expected six Tamil SVG files, and no unintended visual assets, are changed by the v2.2.2 pass.
- v2.2.1 content identity is verified before applying v2.2.2.
- a clean Android lint, unit-test and debug APK build succeeds.
- the APK remains pure native Android with no INTERNET permission and no HTML/JS/CSS runtime payload.

## Remaining mixed-script policy
Latin-script material is not treated as an error when it is a scientific abbreviation, measurement notation, internationally fixed treaty/statutory name, proper name or first-occurrence technical synonym. Each remaining mixed-script occurrence is emitted into `V222_TAMIL_COLLEGE_AUDIT.json` for explicit review instead of being blindly transliterated.

## Device-QA gate
Static editorial success does not prove Tamil glyph shaping or visual fit. Physical-device QA remains mandatory for:
- Tamil line breaking and conjunct rendering;
- SVG label clipping;
- normal-scale readability;
- portrait/landscape layout;
- English/Tamil figure parity;
- Back/navigation behavior;
- complete offline operation.
