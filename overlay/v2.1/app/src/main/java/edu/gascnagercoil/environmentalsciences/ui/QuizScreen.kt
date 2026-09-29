package edu.gascnagercoil.environmentalsciences.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import edu.gascnagercoil.environmentalsciences.model.UnitContent

@Composable
fun QuizScreen(unit: UnitContent, mode: LanguageMode, onMode: (LanguageMode) -> Unit) {
    var encoded by rememberSaveable(unit.number) { mutableStateOf(List(unit.quiz.size) { -1 }.joinToString(",")) }
    var checked by rememberSaveable(unit.number) { mutableStateOf(false) }
    val answers = remember(encoded) {
        encoded.split(',').mapNotNull { it.toIntOrNull() }.toMutableList().apply {
            while (size < unit.quiz.size) add(-1)
        }
    }
    val score = answers.zip(unit.quiz).count { (a, q) -> a == q.answer }

    fun select(q: Int, option: Int) {
        val next = answers.toMutableList()
        next[q] = option
        encoded = next.joinToString(",")
        checked = false
    }

    LazyColumn(contentPadding = PaddingValues(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item {
            Text(
                if (mode == LanguageMode.TAMIL) "அலகு ${unit.number} · தேர்வு பயிற்சி பல்தேர்வு வினாக்கள்" else "Unit ${unit.number} · Exam Practice MCQs",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
            )
            Spacer(Modifier.height(10.dp))
            LanguageSelectorQuiz(mode, onMode)
        }
        itemsIndexed(unit.quiz) { index, q ->
            ElevatedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (mode == LanguageMode.TAMIL) {
                        if (q.questionTa.isNotBlank()) Text(q.questionTa, fontWeight = FontWeight.SemiBold)
                    } else {
                        if (q.questionEn.isNotBlank()) Text(q.questionEn, fontWeight = FontWeight.SemiBold)
                    }
                    q.options.forEachIndexed { oi, opt ->
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            RadioButton(selected = answers[index] == oi, onClick = { select(index, oi) })
                            Column(Modifier.weight(1f)) {
                                if (mode == LanguageMode.TAMIL) {
                                    if (opt.ta.isNotBlank()) Text(opt.ta)
                                } else {
                                    if (opt.en.isNotBlank()) Text(opt.en)
                                }
                            }
                        }
                    }
                    if (checked && answers[index] >= 0) {
                        val correct = answers[index] == q.answer
                        Text(
                            if (mode == LanguageMode.TAMIL) {
                                if (correct) "சரி" else "சரியான விடை: ${q.answer + 1}"
                            } else {
                                if (correct) "Correct" else "Correct answer: ${q.answer + 1}"
                            },
                            color = if (correct) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                            fontWeight = FontWeight.SemiBold
                        )
                    }
                }
            }
        }
        item {
            Button(onClick = { checked = true }, modifier = Modifier.fillMaxWidth()) {
                Text(if (mode == LanguageMode.TAMIL) "விடைகளைச் சரிபார்க்க" else "Check answers")
            }
            if (checked) {
                Spacer(Modifier.height(8.dp))
                Text("Score: $score / ${unit.quiz.size}", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
private fun LanguageSelectorQuiz(mode: LanguageMode, onMode: (LanguageMode) -> Unit) {
    CompactLanguageSwitch(mode, onMode)
}
