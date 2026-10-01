package edu.gascnagercoil.environmentalsciences.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.SavedStateHandle
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import kotlinx.coroutines.flow.StateFlow

/**
 * Owns reading state that must survive configuration changes and process recreation.
 *
 * Durable user preferences are mirrored to SharedPreferences where the existing app
 * already persisted them; SavedStateHandle is the authoritative in-session state.
 */
class LearningStateViewModel(
    application: Application,
    private val savedStateHandle: SavedStateHandle,
) : AndroidViewModel(application) {

    private val preferences =
        application.getSharedPreferences("learning_state", android.content.Context.MODE_PRIVATE)

    val route: StateFlow<String> = savedStateHandle.getStateFlow(
        KEY_ROUTE,
        preferences.getString("last_route", "home") ?: "home",
    )

    val languageName: StateFlow<String> = savedStateHandle.getStateFlow(
        KEY_LANGUAGE,
        preferences.getString("language", LanguageMode.ENGLISH.name) ?: LanguageMode.ENGLISH.name,
    )

    fun setRoute(value: String) {
        savedStateHandle[KEY_ROUTE] = value
        if (value != "search") {
            preferences.edit().putString("last_route", value).apply()
        }
    }

    fun setLanguage(value: String) {
        savedStateHandle[KEY_LANGUAGE] = value
        preferences.edit().putString("language", value).apply()
    }

    fun readingPosition(unitNumber: Int, lessonId: String, mode: LanguageMode): Int {
        val key = readingKey(unitNumber, lessonId, mode)
        return savedStateHandle.get<Int>(key)
            ?: preferences.getInt(key, 0).coerceAtLeast(0)
    }

    fun setReadingPosition(unitNumber: Int, lessonId: String, mode: LanguageMode, index: Int) {
        val key = readingKey(unitNumber, lessonId, mode)
        val safeIndex = index.coerceAtLeast(0)
        savedStateHandle[key] = safeIndex
        preferences.edit().putInt(key, safeIndex).apply()
    }

    fun quizAnswers(unitNumber: Int, questionCount: Int): StateFlow<String> {
        val key = quizAnswersKey(unitNumber)
        val defaultValue = List(questionCount) { -1 }.joinToString(",")
        return savedStateHandle.getStateFlow(key, defaultValue)
    }

    fun quizChecked(unitNumber: Int): StateFlow<Boolean> =
        savedStateHandle.getStateFlow(quizCheckedKey(unitNumber), false)

    fun setQuizAnswer(unitNumber: Int, questionCount: Int, questionIndex: Int, optionIndex: Int) {
        val key = quizAnswersKey(unitNumber)
        val current = savedStateHandle.get<String>(key)
            ?: List(questionCount) { -1 }.joinToString(",")
        val answers = current.split(',').mapNotNull { it.toIntOrNull() }.toMutableList()
        while (answers.size < questionCount) answers.add(-1)
        if (questionIndex in answers.indices) {
            answers[questionIndex] = optionIndex
            savedStateHandle[key] = answers.joinToString(",")
        }
        savedStateHandle[quizCheckedKey(unitNumber)] = false
    }

    fun setQuizChecked(unitNumber: Int, checked: Boolean) {
        savedStateHandle[quizCheckedKey(unitNumber)] = checked
    }

    private fun readingKey(unitNumber: Int, lessonId: String, mode: LanguageMode): String =
        "lesson_scroll_${unitNumber}_${lessonId}_${mode.name}"

    private fun quizAnswersKey(unitNumber: Int): String = "quiz_answers_$unitNumber"

    private fun quizCheckedKey(unitNumber: Int): String = "quiz_checked_$unitNumber"

    private companion object {
        const val KEY_ROUTE = "reader_route"
        const val KEY_LANGUAGE = "reader_language"
    }
}
