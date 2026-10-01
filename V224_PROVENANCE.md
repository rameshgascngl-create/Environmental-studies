# Environmental Studies v2.2.4 — Tamil Naturalisation & Terminology Consistency Provenance

## Scope
Tamil naturalisation and terminology consistency only. This pass starts from the successful v2.2.3 Tamil-coherence build and removes residual translation-like constructions without changing the English lesson payload, figure routing, Android architecture, navigation, permissions, privacy behaviour or scientific visual assets.

The pass is deliberately context-sensitive. It does **not** globally replace every occurrence of `தொடர்பு`.

## Baseline
- Repository: `rameshgascngl-create/Environmental-studies`
- Baseline branch: `correction/v2.2.3-tamil-coherence-20261001`
- Baseline HEAD: `e66ae72ec765f7e8318108dcfdd5cdfbe71728a1`
- Successful v2.2.3 CI run: `36796396838`
- Baseline `book_content.json` SHA-256: `1f3b63f25719a7b495528770db4853f01461ebbd4b2b75136235d31ce6ddd211`

## Correction branch
- `correction/v2.2.4-tamil-naturalisation-20261001`
- Branch point: `e66ae72ec765f7e8318108dcfdd5cdfbe71728a1`

## Version
- versionName: **2.2.4**
- versionCode: **20204**

## Editorial rule
Choose the Tamil construction from the intended scientific relationship:
- dependence/interdependence → `சார்ந்து / ஒன்றையொன்று சார்ந்து`
- interaction or coordinated functioning → `இணைந்து / ஒன்றுடன் ஒன்று இணைந்து`
- topical reference → `பற்றிய`
- legal applicability → `பொருந்தும்`
- causal/mechanistic relation → state the cause explicitly rather than using a vague `தொடர்புடையது`

Scientific uses of `தொடர்பு` such as food relationships, ecological interactions, communication, human–wildlife interaction and Android Contacts permission are retained where they are semantically correct.

## Target content identity
Expected v2.2.4 `book_content.json` SHA-256:
`1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40`

## Release gate
NATURALISATION AUDIT → STATIC INTEGRITY PASS → BUILD/LINT/TEST PASS → PHYSICAL-DEVICE TAMIL QA → CONTENT FREEZE → FINAL RELEASE
