#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

MANIFEST = Path("app/src/main/AndroidManifest.xml")
TEST = Path("app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/TtsVisibilitySmokeTest.kt")
AUDIT = Path("V245_TTS_VISIBILITY_AUDIT.json")
ACTION = "android.intent.action.TTS_SERVICE"
ANDROID = "{http://schemas.android.com/apk/res/android}"

before = MANIFEST.read_text(encoding="utf-8")
before_sha = hashlib.sha256(before.encode()).hexdigest()
root_before = ET.fromstring(before)
present_before = any(
    node.get(ANDROID + "name") == ACTION
    for node in root_before.findall("./queries/intent/action")
)
permissions_before = sorted(
    node.get(ANDROID + "name")
    for node in root_before.findall("uses-permission")
    if node.get(ANDROID + "name")
)

after = before
if not present_before:
    intent = (
        "    <intent>\n"
        f"        <action android:name=\"{ACTION}\" />\n"
        "    </intent>\n"
    )
    if "<queries" in after:
        marker = "</queries>"
        assert marker in after, "Malformed existing <queries> block"
        after = after.replace(marker, intent + marker, 1)
    else:
        marker = "    <application"
        assert marker in after, "Application element not found"
        queries = (
            "    <queries>\n"
            + intent
            + "    </queries>\n\n"
        )
        after = after.replace(marker, queries + marker, 1)
    MANIFEST.write_text(after, encoding="utf-8")

root_after = ET.parse(MANIFEST).getroot()
actions = [
    node.get(ANDROID + "name")
    for node in root_after.findall("./queries/intent/action")
]
assert ACTION in actions, actions
permissions_after = sorted(
    node.get(ANDROID + "name")
    for node in root_after.findall("uses-permission")
    if node.get(ANDROID + "name")
)
assert permissions_after == permissions_before, (permissions_before, permissions_after)
assert "android.permission.INTERNET" not in permissions_after

narration = Path(
    "app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/AnimationNarration.kt"
).read_text(encoding="utf-8")
assert "TextToSpeech.LANG_MISSING_DATA" in narration
assert "TextToSpeech.LANG_NOT_SUPPORTED" in narration
assert "இந்த மொழிக்கான உரை-ஒலி குரல் சாதனத்தில் நிறுவப்படவில்லை" in narration
assert "A text-to-speech voice for this language is not installed on the device" in narration

TEST.parent.mkdir(parents=True, exist_ok=True)
TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.content.Intent
import android.speech.tts.TextToSpeech
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class TtsVisibilitySmokeTest {
    @Test
    fun ttsServiceIsVisibleAndLanguageHandlingIsSafe() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val intent = Intent(TextToSpeech.Engine.INTENT_ACTION_TTS_SERVICE)
        val visible = context.packageManager.queryIntentServices(intent, 0)
        assertTrue("No TTS service is visible through package visibility", visible.isNotEmpty())

        val latch = CountDownLatch(1)
        var initStatus = TextToSpeech.ERROR
        val tts = TextToSpeech(context.applicationContext) { status ->
            initStatus = status
            latch.countDown()
        }
        try {
            assertTrue("TTS initialisation timed out", latch.await(20, TimeUnit.SECONDS))
            assertEquals("TTS engine failed to initialise", TextToSpeech.SUCCESS, initStatus)

            val english = tts.setLanguage(Locale.ENGLISH)
            assertTrue(
                "Default TTS image must support English",
                english != TextToSpeech.LANG_MISSING_DATA &&
                    english != TextToSpeech.LANG_NOT_SUPPORTED,
            )
            val englishSpeak = tts.speak(
                "Environmental Studies",
                TextToSpeech.QUEUE_FLUSH,
                null,
                "environmental_tts_qa_en",
            )
            assertEquals(TextToSpeech.SUCCESS, englishSpeak)

            val tamil = tts.setLanguage(Locale("ta", "IN"))
            val tamilAvailable = tamil != TextToSpeech.LANG_MISSING_DATA &&
                tamil != TextToSpeech.LANG_NOT_SUPPORTED
            val tamilSpeak = if (tamilAvailable) {
                tts.speak(
                    "சுற்றுச்சூழல் அறிவியல்",
                    TextToSpeech.QUEUE_FLUSH,
                    null,
                    "environmental_tts_qa_ta",
                )
            } else {
                null
            }
            if (tamilAvailable) assertEquals(TextToSpeech.SUCCESS, tamilSpeak)

            val out = File(context.filesDir, "tts-qa").apply { mkdirs() }
            File(out, "status.txt").writeText(
                buildString {
                    appendLine("tts_service_count=${visible.size}")
                    appendLine("tts_init=PASS")
                    appendLine("english_tts=PASS")
                    appendLine("tamil_language_result=$tamil")
                    appendLine("tamil_voice_available=$tamilAvailable")
                    appendLine(
                        if (tamilAvailable) "tamil_tts=PASS"
                        else "tamil_tts=FALLBACK_EXPECTED_NO_INSTALLED_VOICE"
                    )
                    appendLine("missing_tamil_voice_ui_fallback=STATICALLY_VERIFIED")
                }
            )
        } finally {
            tts.stop()
            tts.shutdown()
        }
    }
}
''', encoding="utf-8")

after_bytes = MANIFEST.read_bytes()
AUDIT.write_text(
    json.dumps(
        {
            "scope": "Android 11+ TTS package visibility only",
            "manifest_sha256_before": before_sha,
            "manifest_sha256_after": hashlib.sha256(after_bytes).hexdigest(),
            "tts_query_present_before": present_before,
            "tts_query_present_after": True,
            "permissions_before": permissions_before,
            "permissions_after": permissions_after,
            "permissions_changed": False,
            "internet_permission_added": False,
            "tts_smoke_test": str(TEST),
            "missing_tamil_voice_fallback_static_check": True,
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
print(AUDIT.read_text(encoding="utf-8"))
