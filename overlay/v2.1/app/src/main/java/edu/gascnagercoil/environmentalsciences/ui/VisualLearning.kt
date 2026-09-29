package edu.gascnagercoil.environmentalsciences.ui

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import edu.gascnagercoil.environmentalsciences.model.UnitContent

@Composable
fun LanguageGateway(
    current: LanguageMode,
    onSelect: (LanguageMode) -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(modifier, verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(
            if (current == LanguageMode.TAMIL) "கற்றல் மொழியைத் தேர்ந்தெடுக்கவும்" else "Choose your learning section",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold,
        )
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            LanguageCard(
                title = "English",
                subtitle = "English learning section",
                selected = current == LanguageMode.ENGLISH,
                onClick = { onSelect(LanguageMode.ENGLISH) },
                modifier = Modifier.weight(1f),
            )
            LanguageCard(
                title = "தமிழ்",
                subtitle = "தமிழ் கற்றல் பகுதி",
                selected = current == LanguageMode.TAMIL,
                onClick = { onSelect(LanguageMode.TAMIL) },
                modifier = Modifier.weight(1f),
            )
        }
    }
}

@Composable
private fun LanguageCard(
    title: String,
    subtitle: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val container = if (selected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
    ElevatedCard(modifier = modifier.clickable(onClick = onClick)) {
        Column(
            Modifier
                .fillMaxWidth()
                .background(container)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(subtitle, style = MaterialTheme.typography.bodySmall)
            if (selected) {
                Text("✓", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun HomeVisualHero(mode: LanguageMode, modifier: Modifier = Modifier) {
    val title = if (mode == LanguageMode.TAMIL) "சுற்றுச்சூழலைக் கற்று · காண்ந்து · ஆராயுங்கள்" else "Learn · Visualise · Explore the Environment"
    val subtitle = if (mode == LanguageMode.TAMIL) {
        "பாடங்கள், உயர்தர விளக்கப்படங்கள், வினாடி வினா மற்றும் ஊடாடும் மாதிரிகள்"
    } else {
        "Lessons, high-resolution figures, quizzes and interactive environmental models"
    }
    val brush = Brush.horizontalGradient(
        listOf(MaterialTheme.colorScheme.primaryContainer, MaterialTheme.colorScheme.tertiaryContainer)
    )
    Surface(modifier = modifier.fillMaxWidth(), shape = RoundedCornerShape(24.dp), tonalElevation = 2.dp) {
        Column(
            Modifier
                .background(brush)
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text(subtitle, style = MaterialTheme.typography.bodyLarge)
        }
    }
}

private data class VisualItem(val en: String, val ta: String, val enFigure: String, val taFigure: String?)

private val visualItems = listOf(
    VisualItem("Greenhouse effect", "பசுமை இல்ல விளைவு", "fig_046_u05_en", "fig_047_u05_ta"),
    VisualItem("Biodiversity", "உயிரினப் பல்வகைமை", "fig_020_u03_en", "fig_021_u03_ta"),
    VisualItem("Pollution pathways", "மாசுபாட்டு வழித்தடங்கள்", "fig_034_u04_en", "fig_036_u04_ta"),
    VisualItem("Sustainability", "நிலைத்தன்மை", "fig_053_u06_en", "fig_054_u06_ta"),
)

@Composable
fun VisualHighlights(mode: LanguageMode, modifier: Modifier = Modifier) {
    Column(modifier, verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            if (mode == LanguageMode.TAMIL) "படங்களால் கற்போம்" else "Learn visually",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold,
        )
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            contentPadding = PaddingValues(end = 12.dp),
        ) {
            items(visualItems) { item ->
                VisualHighlightCard(item, mode)
            }
        }
    }
}

@Composable
private fun VisualHighlightCard(item: VisualItem, mode: LanguageMode) {
    val context = LocalContext.current
    val requested = if (mode == LanguageMode.TAMIL) item.taFigure ?: item.enFigure else item.enFigure
    val resId = remember(requested) {
        context.resources.getIdentifier(requested, "drawable", context.packageName)
    }
    OutlinedCard(Modifier.size(width = 260.dp, height = 210.dp)) {
        Column(Modifier.fillMaxWidth()) {
            if (resId != 0) {
                Image(
                    painter = painterResource(resId),
                    contentDescription = if (mode == LanguageMode.TAMIL) item.ta else item.en,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(158.dp)
                        .padding(6.dp)
                        .clip(RoundedCornerShape(14.dp)),
                    contentScale = ContentScale.Fit,
                )
            } else {
                Spacer(Modifier.height(158.dp))
            }
            Text(
                if (mode == LanguageMode.TAMIL) item.ta else item.en,
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

private fun unitFigureName(unitNumber: Int, mode: LanguageMode): String {
    val english = mapOf(
        1 to "fig_001_u01_en",
        2 to "fig_010_u02_en",
        3 to "fig_020_u03_en",
        4 to "fig_034_u04_en",
        5 to "fig_046_u05_en",
        6 to "fig_053_u06_en",
        7 to "fig_057_u07_en",
        8 to "fig_055_u07_en",
        9 to "fig_062_u09_en",
    )
    val tamil = mapOf(
        1 to "fig_002_u01_ta",
        2 to "fig_012_u02_ta",
        3 to "fig_021_u03_ta",
        4 to "fig_036_u04_ta",
        5 to "fig_047_u05_ta",
        6 to "fig_054_u06_ta",
        7 to "fig_059_u07_ta",
        8 to "fig_061_u07_ta",
        9 to "fig_063_u09_ta",
    )
    return if (mode == LanguageMode.TAMIL) tamil[unitNumber] ?: english.getValue(unitNumber) else english.getValue(unitNumber)
}

@Composable
fun UnitVisualCard(
    unit: UnitContent,
    mode: LanguageMode,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val figure = unitFigureName(unit.number, mode)
    val resId = remember(figure) { context.resources.getIdentifier(figure, "drawable", context.packageName) }
    ElevatedCard(modifier = modifier.fillMaxWidth().clickable(onClick = onClick)) {
        Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
            if (resId != 0) {
                Image(
                    painter = painterResource(resId),
                    contentDescription = null,
                    modifier = Modifier.size(104.dp).clip(RoundedCornerShape(16.dp)),
                    contentScale = ContentScale.Crop,
                )
            }
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    if (mode == LanguageMode.TAMIL) "அலகு ${unit.number}" else "Unit ${unit.number}",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                )
                Text(
                    if (mode == LanguageMode.TAMIL) unit.titleTa else unit.titleEn,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    if (mode == LanguageMode.TAMIL) "${unit.lessons.size} பாடங்கள் · ${unit.quiz.size} வினாக்கள்" else "${unit.lessons.size} lessons · ${unit.quiz.size} MCQs",
                    style = MaterialTheme.typography.bodySmall,
                )
            }
        }
    }
}

@Composable
fun CompactLanguageSwitch(mode: LanguageMode, onMode: (LanguageMode) -> Unit, modifier: Modifier = Modifier) {
    Row(modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        FilterChip(
            selected = mode == LanguageMode.ENGLISH,
            onClick = { onMode(LanguageMode.ENGLISH) },
            label = { Text("English") },
            modifier = Modifier.weight(1f),
        )
        FilterChip(
            selected = mode == LanguageMode.TAMIL,
            onClick = { onMode(LanguageMode.TAMIL) },
            label = { Text("தமிழ்") },
            modifier = Modifier.weight(1f),
        )
    }
}
