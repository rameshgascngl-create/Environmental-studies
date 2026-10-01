# Environmental Studies v2.4.4 — Quiz Bank Academic Audit

**Audit branch:** `audit/v2.4.4-academic-content-quiz-20261001`  
**Audited release-readiness base:** `2a384909bd3daf366c52bd77a9d1195f08ef3d07`  
**Release-readiness CI:** run `36884542874` — PASS  
**Audited content file:** `book_content_v244_release_readiness.json` from the successful QA artifact  
**Scope:** quiz-bank academic quality only. No lesson prose, figures, navigation, signing, privacy, launcher, Android architecture or release-hardening code is changed by this audit.

## Gate status

The v2.4.4 release-readiness workflow completed successfully, including native-source reconstruction, Tamil editorial/naturalisation passes, release hardening, bounded PNG decoding, SVG legibility, bundled Tamil font, accessibility, device-figure correction, Tamil visual/icon correction, Living Environment visual atlas, privacy URL verification, debug QA build and minified release-pipeline exercise.

Production signing remains a separate release gate: the QA artifact reports `signed_release_available=false` because the original production signing secrets were not configured on the runner. No replacement signing key was generated. This does **not** block the isolated academic quiz-bank work package.

## Current quiz-bank inventory

| Unit | Unit title | Current MCQs |
|---|---|---:|
| 1 | Environment and Human Society | 5 |
| 2 | Ecosystems and Natural Resources | 5 |
| 3 | Biodiversity and Conservation | 7 |
| 4 | Environmental Pollution and Human Health | 5 |
| 5 | Climate Change and Global Environmental Issues | 5 |
| 6 | Sustainable Resource Use and Lifestyle | 5 |
| 7 | Environmental Management and Disaster Risk | 5 |
| 8 | Environmental Laws, Policies and Global Cooperation | 14 |
| 9 | Case Studies, Campus Activities and Field Learning | 7 |
| **Total** |  | **58** |

## Academic findings

### P0 — none
No quiz defect found that should reopen the already-passed v2.4.4 release-hardening work.

### P1 — assessment balance and coverage

1. **Question distribution is strongly unbalanced.** Most units have only five questions, while Unit 8 has fourteen.
2. **Unit 8 is dominated by year-recall.** Thirteen of its fourteen questions primarily ask for enactment/adoption/entry-into-force years. This is too narrow for a college-level Environmental Studies assessment and under-tests purpose, institutional roles, application and environmental citizenship.
3. **Several lessons are not directly sampled by the current unit quiz.**
   - Unit 2: biogeochemical cycles and mineral/food/energy resources are not directly assessed.
   - Unit 4: soil pollution, noise/physical pollution and specialised waste streams are under-sampled.
   - Unit 6: sustainable campuses/communities is not directly assessed.
   - Unit 9: water-use/rainwater observation and local environmental observation need direct questions.
4. The bank relies mainly on one-step recognition. It needs more cause–effect, scenario, interpretation and evidence-based questions.

### P1 — bilingual data integrity

1. Unit 3 question 6 contains Tamil text inside two English option fields:
   - `இந்தோ-பர்மா (Indo-Burma)`
   - `மேற்குத் தொடர்ச்சி மலைகள்–இலங்கை (Western Ghats–Sri Lanka)`
2. Unit 9 question 1 Tamil wording contains the grammatical form `கணக்காய்வுயின்`; it should be normalised to `கணக்காய்வின்`.
3. Bilingual MCQs should be semantically parallel rather than literal word-for-word translations, while retaining standard scientific/legal terms where required.

## v2.4.5 quiz-bank acceptance target

The implementation work package should:

- produce **90 MCQs total — exactly 10 per unit**;
- preserve the existing `book_content.json` schema and current QuizScreen contract;
- ensure every lesson is represented by at least one directly aligned question;
- mix approximately **40% concept/understanding, 40% application/cause–effect, 20% scenario/interpretation**;
- reduce Unit 8 rote date/year dependence and test the **purpose and application** of laws, institutions and agreements;
- retain only stable, source-verifiable legal/environmental facts and avoid volatile counts such as current numbers of protected/Ramsar sites;
- provide four plausible options per item with exactly one defensible answer;
- keep English fields free of Tamil-script contamination;
- keep Tamil academically natural and college-ready;
- remove duplicated numbering defects, malformed units and ambiguous distractors;
- keep lesson prose, figures, visual routes, animations, navigation, signing, privacy and release hardening byte-for-byte outside the quiz/version scope.

## Implementation boundary

The next implementation branch should change only:

1. a dedicated quiz-bank transformation/audit script;
2. the QA workflow assertions needed to apply and validate that script;
3. reconstructed `book_content.json` quiz arrays;
4. `versionName/versionCode` to **2.4.5 / 20405**;
5. generated quiz-bank audit evidence.

No release signing work should be mixed into this academic content package.

## External fact controls

For legislation and international agreements, implementation must validate against authoritative sources such as India Code / MoEFCC and the official Ramsar, CBD and UNFCCC treaty pages before accepting a question. Scientific standards such as Indian NAAQS values should be verified against CPCB or the governing notification rather than copied from secondary summaries.
