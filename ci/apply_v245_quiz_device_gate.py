from pathlib import Path
import json

ROOT = Path('.')
QUIZ = ROOT / 'app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/QuizScreen.kt'
TEST = ROOT / 'app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/QuizDeviceQaTest.kt'
AUDIT_JSON = ROOT / 'V245_QUIZ_DEVICE_GATE_AUDIT.json'
AUDIT_MD = ROOT / 'V245_QUIZ_DEVICE_GATE_AUDIT.md'

src = QUIZ.read_text(encoding='utf-8')
old = 'Text("Score: $score / ${unit.quiz.size}", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)'
new = '''Text(
                    if (mode == LanguageMode.TAMIL) "மதிப்பெண்: $score / ${unit.quiz.size}" else "Score: $score / ${unit.quiz.size}",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                )'''
if old not in src:
    raise SystemExit('Expected v2.4.5 score line not found; stop rather than patch blindly.')
if src.count(old) != 1:
    raise SystemExit(f'Expected exactly one score line, found {src.count(old)}.')
patched = src.replace(old, new)
QUIZ.write_text(patched, encoding='utf-8')

TEST.parent.mkdir(parents=True, exist_ok=True)
TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences

import android.content.pm.ActivityInfo
import android.content.res.Configuration
import androidx.compose.ui.test.assertExists
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.fetchSemanticsNodes
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTouchInput
import androidx.compose.ui.test.swipeDown
import androidx.compose.ui.test.swipeUp
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import edu.gascnagercoil.environmentalsciences.data.ContentRepository
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class QuizDeviceQaTest {

    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun quizBilingualStateRotationAndBackNavigation() {
        val unit = ContentRepository(composeRule.activity).load().units.first { it.number == 1 }
        val first = unit.quiz.first()
        val selectedOptionIndex = 0
        val expectedEnglishFeedback = if (first.answer == selectedOptionIndex) {
            "Correct"
        } else {
            "Correct answer: ${first.answer + 1}"
        }
        val expectedTamilFeedback = if (first.answer == selectedOptionIndex) {
            "சரி"
        } else {
            "சரியான விடை: ${first.answer + 1}"
        }
        val expectedScore = if (first.answer == selectedOptionIndex) 1 else 0

        composeRule.onNodeWithText("Start learning").performClick()
        scrollDownUntil("MCQs")
        composeRule.onNodeWithText("MCQs").performClick()

        composeRule.onNodeWithText("Unit 1 · Exam Practice MCQs").assertIsDisplayed()
        composeRule.onNodeWithText(first.questionEn).assertExists()
        composeRule.onNodeWithText(first.options[selectedOptionIndex].en).performClick()

        composeRule.activity.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        composeRule.waitUntil(timeoutMillis = 15_000) {
            composeRule.activity.resources.configuration.orientation == Configuration.ORIENTATION_LANDSCAPE
        }
        composeRule.onNodeWithText("Unit 1 · Exam Practice MCQs").assertExists()
        composeRule.onNodeWithText(first.questionEn).assertExists()

        composeRule.activity.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        composeRule.waitUntil(timeoutMillis = 15_000) {
            composeRule.activity.resources.configuration.orientation == Configuration.ORIENTATION_PORTRAIT
        }
        composeRule.onNodeWithText("Unit 1 · Exam Practice MCQs").assertExists()

        scrollDownUntil("Check answers", maxSwipes = 28)
        composeRule.onNodeWithText("Check answers").performClick()
        composeRule.onNodeWithText("Score: $expectedScore / 10").assertExists()

        scrollUpUntil("Unit 1 · Exam Practice MCQs", maxSwipes = 28)
        composeRule.onNodeWithText(expectedEnglishFeedback).assertExists()

        composeRule.onNodeWithText("தமிழ்").performClick()
        composeRule.onNodeWithText("அலகு 1 · தேர்வு பயிற்சி பல்தேர்வு வினாக்கள்").assertExists()
        composeRule.onNodeWithText(first.questionTa).assertExists()
        composeRule.onNodeWithText(expectedTamilFeedback).assertExists()

        scrollDownUntil("மதிப்பெண்: $expectedScore / 10", maxSwipes = 28)
        composeRule.onNodeWithText("மதிப்பெண்: $expectedScore / 10").assertExists()

        composeRule.activity.onBackPressedDispatcher.onBackPressed()
        composeRule.waitForIdle()
        composeRule.onNodeWithText("அலகு 1: ${unit.titleTa}").assertExists()
    }

    private fun scrollDownUntil(text: String, maxSwipes: Int = 12) {
        repeat(maxSwipes) {
            if (composeRule.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty()) return
            composeRule.onRoot().performTouchInput { swipeUp() }
            composeRule.waitForIdle()
        }
        composeRule.onNodeWithText(text).assertExists()
    }

    private fun scrollUpUntil(text: String, maxSwipes: Int = 12) {
        repeat(maxSwipes) {
            if (composeRule.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty()) return
            composeRule.onRoot().performTouchInput { swipeDown() }
            composeRule.waitForIdle()
        }
        composeRule.onNodeWithText(text).assertExists()
    }
}
''', encoding='utf-8')

audit = {
    'versionName': '2.4.5',
    'versionCode': 20405,
    'scope': 'quiz device-gate correction and instrumentation only',
    'reproduced_defect': {
        'file': str(QUIZ),
        'before': 'Score: $score / ${unit.quiz.size}',
        'condition': 'Tamil quiz mode after Check answers',
        'classification': 'P1 bilingual UI defect',
    },
    'score_localised_in_tamil': 'மதிப்பெண்: $score / ${unit.quiz.size}' in patched,
    'english_score_preserved': 'Score: $score / ${unit.quiz.size}' in patched,
    'quiz_content_changed': False,
    'lesson_content_changed': False,
    'figure_assets_changed': False,
    'navigation_logic_changed': False,
    'signing_changed': False,
    'instrumentation_test_created': str(TEST),
    'instrumentation_scope': [
        'quiz entry from unit 1',
        '10-question title/route availability',
        'answer selection',
        'portrait-landscape-portrait recreation',
        'answer persistence across rotation',
        'check-answer feedback',
        'English score rendering',
        'Tamil language switch',
        'Tamil question rendering',
        'Tamil feedback rendering',
        'Tamil score rendering',
        'system back returns to Units',
    ],
    'physical_device_only_checks': [
        'visual clipping and text collisions at real device font scale',
        'touch comfort on the user device',
        'OEM back-gesture behaviour',
        'low-memory process kill by the device OS',
        'long-session thermal/memory behaviour',
    ],
}
AUDIT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
AUDIT_MD.write_text('''# Environmental Studies v2.4.5 — Quiz Device Gate

A static review reproduced one concrete bilingual UI defect before physical-device testing: the quiz result line remained English-only (`Score:`) while the quiz was in Tamil mode. The correction changes only that result label to `மதிப்பெண்:` in Tamil and preserves the English label.

No quiz questions, lesson prose, figures, routes, signing configuration or release-hardening behaviour are changed. An Android instrumentation test is generated to exercise quiz entry, answer selection, portrait/landscape recreation, state retention, answer checking, English/Tamil rendering and system Back navigation.

Physical-device-only visual and OEM behaviour remains a final manual gate and must not be inferred from emulator success.
''', encoding='utf-8')
