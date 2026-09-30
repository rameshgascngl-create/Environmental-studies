# Environmental Studies v2.2.2 — Tamil College-Level Editorial Provenance

## Scope
Tamil-only higher-education editorial pass. The objective is to retain Tamil Nadu textbook scientific terminology where established while raising sentence structure, conceptual explanation and pedagogical register to undergraduate/college level.

No new syllabus, feature, navigation, Android architecture, network, privacy or signing change is authorised.

## Repository provenance
- Repository: `rameshgascngl-create/Environmental-studies`
- Immediate audited baseline branch: `correction/v2.2.1-tamil-editorial-scivis-20260929`
- Immediate audited baseline HEAD: `28c41128c4e9867b57732a357880f2b1a637a66a`
- New correction branch: `correction/v2.2.2-tamil-college-editorial-20260930`
- Branch point: `28c41128c4e9867b57732a357880f2b1a637a66a`
- `main` must remain untouched during this work package.

## v2.2.1 build proof
- GitHub Actions run: `36737578066`
- Build job: `109963210448`
- Run conclusion: SUCCESS
- v2.2.1 artifact: `Environmental-Studies-v2.2.1-CORRECTION-DEVICE-QA`
- Artifact ID: `11107947089`
- v2.2.1 corrected `book_content.json` SHA-256: `766910513a31c5ea9ccb9514237f8664c31076c92d3fd79bb1005643133da599`
- v2.2.1 device-QA APK SHA-256: `2dfaed8a8976fede3dfa429f94211a5e61f168cf6921b6084d90fbc2e462d259`

The v2.2.2 workflow must reconstruct the v2.2.1 corrected baseline and assert the exact content hash above **before** applying the v2.2.2 Tamil college-level pass.

## Version assignment
- versionName: **2.2.2**
- versionCode: **20202**

## Intended v2.2.2 content identity
Local pre-CI audit candidate:
- `book_content.json` SHA-256: `7781bd031ef43fdab16e44c024e87584f79550da5e86d0a88b7f0913f510dd4e`
- English lesson payload stable hash before/after Tamil pass: `2f34a366bf6bd27f62f703284e335262c7fc1ed79e48221973532c5af93485a0`
- Units: 9
- Lessons: 46
- Tamil SVG files expected to change: 6

The CI build must independently reproduce these values; this record alone is not build proof.

## Release gate
TAMIL AUDIT → SOURCE CORRECTED → STATIC INTEGRITY PASS → CLEAN BUILD PASS → PHYSICAL DEVICE QA → CONTENT FREEZE → FINAL RELEASE
