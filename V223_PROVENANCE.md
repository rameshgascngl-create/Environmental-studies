# Environmental Studies v2.2.3 — Tamil Coherence Provenance

## Scope
Sentence-level Tamil coherence correction only. This pass follows the v2.2.2 Tamil college terminology/editorial pass and addresses residual literal translation, compressed noun strings, unnatural clause order, register inconsistency and field-language phrasing.

No English lesson content, figure routing, Android architecture, navigation, permissions, privacy behavior or scientific-visual assets are authorised to change.

## Baseline
- Repository: `rameshgascngl-create/Environmental-studies`
- Baseline branch: `correction/v2.2.2-tamil-college-editorial-20260930`
- Baseline HEAD: `bca389b6ff7e8ea64a0fabb0b95e5830f933e8a0`
- Successful v2.2.2 CI run: `36753313926`
- Baseline `book_content.json` SHA-256: `7781bd031ef43fdab16e44c024e87584f79550da5e86d0a88b7f0913f510dd4e`

## Correction branch
- `correction/v2.2.3-tamil-coherence-20261001`
- Branch point: `bca389b6ff7e8ea64a0fabb0b95e5830f933e8a0`

## Version
- versionName: **2.2.3**
- versionCode: **20203**

## Editorial gate
- All 46 Tamil lessons are explicitly reviewed.
- Sentence-level correction is preferred over blind global substitution.
- Tamil Nadu textbook scientific terms are retained where established.
- English technical terms are retained only where they improve scientific precision or preserve official names/abbreviations.
- English payload and figure routing must remain byte-logically unchanged.
- Any source/build assertion failure blocks the APK.

## Release gate
TAMIL COHERENCE AUDIT → STATIC INTEGRITY PASS → BUILD/LINT/TEST PASS → PHYSICAL DEVICE TAMIL QA → CONTENT FREEZE → FINAL RELEASE
