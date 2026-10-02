#!/usr/bin/env python3
from pathlib import Path

TEST=Path("app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/TtsVisibilityProbeTest.kt")
TEST.parent.mkdir(parents=True,exist_ok=True)
TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.content.Context
import android.content.Intent
import android.os.Build
import android.speech.tts.TextToSpeech
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import java.util.Locale
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import org.json.JSONObject
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class TtsVisibilityProbeTest {
    @Test
    fun recordTtsVisibilityAndTamilSupport() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val services = context.packageManager.queryIntentServices(
            Intent(TextToSpeech.Engine.INTENT_ACTION_TTS_SERVICE),
            0,
        )
        val latch = CountDownLatch(1)
        var initStatus = Int.MIN_VALUE
        var tts: TextToSpeech? = null
        tts = TextToSpeech(context) { status ->
            initStatus = status
            latch.countDown()
        }
        val callbackReceived = latch.await(10, TimeUnit.SECONDS)
        var languageResult = Int.MIN_VALUE
        var currentEngine = ""
        if (callbackReceived && initStatus == TextToSpeech.SUCCESS) {
            currentEngine = tts?.defaultEngine.orEmpty()
            languageResult = tts?.setLanguage(Locale("ta", "IN")) ?: Int.MIN_VALUE
        }
        val report = JSONObject().apply {
            put("sdk", Build.VERSION.SDK_INT)
            put("visible_tts_services", services.size)
            put("visible_tts_packages", services.mapNotNull { it.serviceInfo?.packageName }.distinct())
            put("callback_received", callbackReceived)
            put("init_status", initStatus)
            put("tts_success", initStatus == TextToSpeech.SUCCESS)
            put("default_engine", currentEngine)
            put("tamil_language_result", languageResult)
            put(
                "tamil_supported",
                languageResult != TextToSpeech.LANG_MISSING_DATA &&
                    languageResult != TextToSpeech.LANG_NOT_SUPPORTED &&
                    languageResult != Int.MIN_VALUE
            )
        }
        val outDir = context.filesDir.resolve("tts-qa").apply { mkdirs() }
        outDir.resolve("tts-visibility.json").writeText(report.toString(2))
        tts?.shutdown()
    }
}
''',encoding="utf-8")
print("TTS_VISIBILITY_PROBE_CREATED")
