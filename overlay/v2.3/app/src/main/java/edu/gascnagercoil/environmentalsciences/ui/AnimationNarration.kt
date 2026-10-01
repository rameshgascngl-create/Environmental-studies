package edu.gascnagercoil.environmentalsciences.ui

import android.speech.tts.TextToSpeech
import android.widget.Toast
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import java.util.Locale

internal data class AnimationNarration(
    val ready: Boolean,
    val speak: (String, LanguageMode) -> Unit,
    val stop: () -> Unit,
)

@Composable
internal fun rememberAnimationNarration(): AnimationNarration {
    val context = LocalContext.current
    var ready by remember { mutableStateOf(false) }
    val tts = remember {
        TextToSpeech(context.applicationContext) { status ->
            ready = status == TextToSpeech.SUCCESS
        }
    }

    DisposableEffect(tts) {
        onDispose {
            tts.stop()
            tts.shutdown()
        }
    }

    return AnimationNarration(
        ready = ready,
        speak = { text, mode ->
            if (!ready) {
                Toast.makeText(
                    context,
                    if (mode == LanguageMode.TAMIL) "ஒலி இயந்திரம் தயாராகிறது" else "Audio engine is starting",
                    Toast.LENGTH_SHORT,
                ).show()
            } else {
                val locale = if (mode == LanguageMode.TAMIL) Locale("ta", "IN") else Locale.ENGLISH
                val languageResult = tts.setLanguage(locale)
                if (languageResult == TextToSpeech.LANG_MISSING_DATA ||
                    languageResult == TextToSpeech.LANG_NOT_SUPPORTED
                ) {
                    Toast.makeText(
                        context,
                        if (mode == LanguageMode.TAMIL)
                            "இந்த மொழிக்கான உரை-ஒலி குரல் சாதனத்தில் நிறுவப்படவில்லை"
                        else
                            "A text-to-speech voice for this language is not installed on the device",
                        Toast.LENGTH_LONG,
                    ).show()
                } else {
                    tts.setSpeechRate(if (mode == LanguageMode.TAMIL) 0.88f else 0.94f)
                    tts.setPitch(1.0f)
                    tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "environmental_animation_explanation")
                }
            }
        },
        stop = { tts.stop() },
    )
}
