# Environmental Studies v2.4.5 — Quiz Device-Gate Audit

**Branch:** `qa/v2.4.5-quiz-device-gate-20261001`  
**Base:** `8c58d606f5288ade9a77bc7f4ce85898c45656ad`  
**Scope:** quiz device-gate QA only.

## Files authorised for this phase

- `.github/workflows/pure-native-qa.yml` — route this branch through the existing full reconstruction/build gate and add Android emulator instrumentation.
- `ci/apply_v245_quiz_device_gate.py` — apply one reproduced bilingual quiz-UI correction and generate the instrumentation test.
- `V245_QUIZ_DEVICE_GATE_AUDIT.md` — preserve the audit evidence and the physical-device boundary.

No lesson content, quiz-bank questions, figures, animations, navigation architecture, signing configuration, privacy implementation or production package ID is authorised for change.

## Reproduced defect before editing

**File:** reconstructed `app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/QuizScreen.kt`

The result line was:

`Text("Score: $score / ${unit.quiz.size}", ...)`

That string is unconditional. Therefore after switching the quiz to Tamil and pressing **Check answers**, the score remained English-only although the question, options and answer feedback were Tamil.

**Classification:** P1 bilingual UI defect.

## Surgical correction

Tamil mode must render:

`மதிப்பெண்: <score> / 10`

English mode must retain:

`Score: <score> / 10`

No assessment data or scoring logic is changed.

## Automated device-like gate

The generated Android instrumentation test must verify, on a clean emulator:

1. entry into Unit 1 quiz;
2. 10-question quiz route/title;
3. answer selection;
4. portrait → landscape → portrait recreation without crash;
5. selected answer surviving rotation;
6. Check answers feedback and score;
7. English → Tamil switch;
8. Tamil question, feedback and score rendering;
9. system Back from quiz returns to the Units screen.

## Explicitly not claimed by emulator testing

Real-device clipping/collision behaviour, OEM gesture navigation, touch comfort, OS low-memory kill/relaunch and prolonged memory/thermal behaviour remain **physical-device-only** checks. A successful emulator run will not be reported as physical-device QA.
