# Environmental Studies v2.4.4 — Academic Content and Quiz Audit

**Audit type:** static, audit-only  
**Canonical candidate:** `correction/v2.4.4-release-readiness-20261001`  
**Candidate commit:** `2a384909bd3daf366c52bd77a9d1195f08ef3d07`  
**Validated CI:** GitHub Actions run #104 — PASS  
**Book SHA-256:** `e6b18d2cca5f92d324188b4d8b4187edc7995416ea12b08dea8d2c1633658d4c`

No lesson, quiz, figure, Kotlin source, Android configuration or release identity is changed by this audit branch.

## 1. Corpus structure

- Units: **9**
- Lessons: **46**
- Quiz questions: **58**
- English structured comparison tables: **18**
- Tamil structured comparison tables: **18**
- Tamil table parity by lesson: **PASS**
- Active Tamil PNG teaching routes: **0**
- Stale Tamil teaching PNG resources: **0**
- Tamil teaching figures are now routed through SVG resources.
- Tamil privacy paragraphs: **4**
- English privacy paragraphs: **4**

## 2. Quiz distribution

| Unit | Questions |
|---|---:|
| 1 | 5 |
| 2 | 5 |
| 3 | 7 |
| 4 | 5 |
| 5 | 5 |
| 6 | 5 |
| 7 | 5 |
| 8 | 14 |
| 9 | 7 |

Unit 8 contributes **14/58 = 24.1%** of the complete question bank and contains nearly three times the number of questions found in Units 1, 2, 4, 5, 6 and 7. This is a genuine assessment-weighting imbalance unless Unit 8 is deliberately intended to receive substantially greater assessment weight.

## 3. Feedback and explanation

The current 58 quiz objects contain **no answer-explanation field**. The quiz therefore identifies correctness but does not explain why the selected answer is correct or why distractors are wrong. This weakens formative-learning value, particularly for self-study.

Recommended v2.4.5 schema extension:

- `explanationEn`
- `explanationTa`

The UI should reveal the explanation **after an answer is committed**, not before.

## 4. Option-length cue audit

Correct-answer position is reasonably balanced:

- A: **13**
- B: **16**
- C: **16**
- D: **13**

Therefore there is no important answer-position bias.

However, option length remains a test-wiseness issue:

- the correct answer is the **unique longest option in 20/58 questions (34.5%)**;
- the correct answer is **equal to the longest option in 39/58 questions (67.2%)**, including ties.

This does not prove that every such item is defective, but it is strong enough to justify item-by-item rewriting. Distractors should be parallel in grammatical form, specificity and approximate length.

## 5. Bilingual assessment requirements for the next implementation

A v2.4.5 quiz revision should preserve exact scientific equivalence between English and Tamil while avoiding literal translation where it produces unnatural Tamil. Each rewritten item should satisfy all of the following:

1. one unambiguously best answer;
2. scientifically plausible distractors;
3. comparable option length and grammatical structure;
4. no clue from absolute terms unless scientifically necessary;
5. no duplicated fact tested with trivially altered wording;
6. English and Tamil answers mapped to the same option index;
7. concise post-answer explanation in both languages;
8. college-level terminology consistent with the established Tamil glossary;
9. no alteration of lesson prose merely to make a quiz item easier;
10. factual claims requiring regulatory limits, dates or standards should remain source-verifiable.

## 6. Suggested rebalance without reducing the total bank

If the intended total remains **58**, a much more even distribution would be:

| Unit | Target |
|---|---:|
| 1 | 6 |
| 2 | 6 |
| 3 | 7 |
| 4 | 6 |
| 5 | 6 |
| 6 | 6 |
| 7 | 7 |
| 8 | 7 |
| 9 | 7 |
| **Total** | **58** |

This is a pedagogical distribution proposal, not a release gate. Final weighting should follow the actual syllabus/contact-hour emphasis.

## 7. Figures and Tamil rendering status

The v2.4.4 static release-readiness gate establishes:

- all stale Tamil raster teaching assets removed;
- no active Tamil PNG routes;
- Tamil SVG XML parsing passes;
- bundled Noto Sans Tamil font resolver is present;
- AndroidSVG and Noto Sans Tamil licence resources survive the minified release resource table;
- CSS-only `rx/ry` dependencies in the identified SVGs were converted to explicit SVG attributes.

This removes the known raster shaping defect from the teaching-figure pipeline. It **does not constitute physical-device proof** of Tamil glyph shaping inside AndroidSVG. That remains a device-QA gate.

## 8. Release separation

The v2.4.4 release candidate should remain frozen while this academic audit is reviewed. Quiz rewriting should be implemented on a separate v2.4.5 content branch after the v2.4.4 device QA decision, so that a pedagogical revision cannot obscure a packaging/signing or figure-rendering regression.

## Audit verdict

**v2.4.4 academic content is structurally coherent enough for device QA, but the quiz bank is not yet a strong formative-assessment system.** The two principal quiz weaknesses are missing explanations and uneven/unit-biased item distribution, with option-length cues as a secondary quality problem.

This report does not classify v2.4.4 as store-ready. Production signing, public stable Privacy Policy hosting and physical-device QA remain separate release gates.
