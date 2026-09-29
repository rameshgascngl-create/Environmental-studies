package edu.gascnagercoil.environmentalsciences.ui

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import kotlin.math.cos
import kotlin.math.sin

private enum class ClimateEvent {
    HEATWAVE,
    CYCLONE,
    MONSOON,
    DROUGHT,
}

private data class ClimateEventText(
    val event: ClimateEvent,
    val en: String,
    val ta: String,
    val enExplanation: String,
    val taExplanation: String,
)

private val climateEvents = listOf(
    ClimateEventText(
        ClimateEvent.HEATWAVE,
        "Heatwave",
        "வெப்ப அலை",
        "Persistent high temperatures can develop when strong high pressure, clear skies and dry soils reinforce surface heating. Climate change can increase the frequency and intensity of some heat extremes.",
        "வலுவான உயர் அழுத்தம், மேகமற்ற வானம், உலர்ந்த மண் ஆகியவை மேற்பரப்பு வெப்பமாதலை அதிகரிக்கும்போது நீடித்த அதிக வெப்பநிலை உருவாகலாம். காலநிலை மாற்றம் சில கடுமையான வெப்ப நிகழ்வுகளின் அடிக்கடி நிகழ்தல் மற்றும் தீவிரத்தை அதிகரிக்கலாம்.",
    ),
    ClimateEventText(
        ClimateEvent.CYCLONE,
        "Tropical cyclone",
        "வெப்பமண்டலப் புயல்",
        "Warm ocean water supplies heat and moisture. Rising moist air, condensation and latent-heat release can help lower central pressure and organise rotating inflow when other atmospheric conditions are favourable.",
        "சூடான கடல் நீர் வெப்பத்தையும் ஈரப்பதத்தையும் வழங்குகிறது. ஈரமான காற்று மேலெழுதல், திரவமாதல் மற்றும் மறைவெப்ப வெளியீடு ஆகியவை, ஏற்ற வளிமண்டல நிலைகளில், மைய அழுத்தம் குறைந்து சுழலும் காற்றோட்டம் ஒழுங்குபட உதவுகின்றன.",
    ),
    ClimateEventText(
        ClimateEvent.MONSOON,
        "Indian monsoon",
        "இந்திய பருவமழை",
        "Seasonal land-ocean heating differences and large-scale atmospheric circulation move moisture toward the Indian subcontinent. Topography, including the Western Ghats, strongly modifies rainfall distribution.",
        "நிலமும் கடலும் பருவகாலத்தில் வேறுபட்ட அளவில் வெப்பமடைவதும் பெரிய அளவிலான வளிமண்டலச் சுழற்சியும் ஈரப்பதத்தை இந்தியத் துணைக்கண்டத்திற்குக் கொண்டு செல்கின்றன. மேற்கு தொடர்ச்சி மலை உள்ளிட்ட நிலவடிவு மழைப் பகிர்வை வலுவாக மாற்றுகிறது.",
    ),
    ClimateEventText(
        ClimateEvent.DROUGHT,
        "Drought",
        "வறட்சி",
        "Drought develops when water availability remains below normal for an extended period. Rainfall deficits, high evaporation, soil-moisture loss and water demand can interact; drought is not simply the absence of rain.",
        "நீர் கிடைப்புத் தன்மை நீண்ட காலம் இயல்பை விடக் குறைந்திருக்கும்போது வறட்சி உருவாகிறது. மழைக் குறைவு, அதிக ஆவியாதல், மண் ஈரப்பத இழப்பு மற்றும் நீர் தேவை ஒன்றோடொன்று தொடர்புபடலாம்; வறட்சி என்பது மழையின்மை மட்டும் அல்ல.",
    ),
)

@Composable
fun ClimateEventsCard(mode: LanguageMode) {
    var selected by remember { mutableStateOf(ClimateEvent.MONSOON) }
    val selectedText = climateEvents.first { it.event == selected }
    val tamil = mode == LanguageMode.TAMIL

    ElevatedCard(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(
                text = if (tamil) "காலநிலை நிகழ்வுகள் — இயக்க விளக்கம்" else "Climate Events — Animated Explorer",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = if (tamil)
                    "நிகழ்வைத் தேர்ந்தெடுத்து அதன் செயல்முறையை இயக்கப்படமாகக் காணுங்கள்."
                else
                    "Choose an event and observe a lightweight conceptual animation of the process.",
                style = MaterialTheme.typography.bodyMedium,
            )

            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(end = 8.dp),
            ) {
                items(climateEvents) { item ->
                    FilterChip(
                        selected = selected == item.event,
                        onClick = { selected = item.event },
                        label = { Text(if (tamil) item.ta else item.en) },
                    )
                }
            }

            ClimateAnimation(event = selected)

            Text(
                text = if (tamil) selectedText.ta else selectedText.en,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                text = if (tamil) selectedText.taExplanation else selectedText.enExplanation,
                style = MaterialTheme.typography.bodyMedium,
            )
            Text(
                text = if (tamil)
                    "குறிப்பு: இது கருத்துணர்வுக்கான விளக்க மாதிரி; வானிலை அல்லது காலநிலை முன்னறிவிப்பு மாதிரி அல்ல."
                else
                    "Note: This is a conceptual learning model, not a weather or climate forecasting model.",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary,
            )
        }
    }
}

@Composable
private fun ClimateAnimation(event: ClimateEvent) {
    val transition = rememberInfiniteTransition(label = "climate-event")
    val phase by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 2800, easing = LinearEasing),
        ),
        label = "phase",
    )

    val primary = MaterialTheme.colorScheme.primary
    val secondary = MaterialTheme.colorScheme.secondary
    val tertiary = MaterialTheme.colorScheme.tertiary
    val surface = MaterialTheme.colorScheme.surfaceVariant

    Canvas(
        modifier = Modifier
            .fillMaxWidth()
            .height(210.dp)
            .background(surface, RoundedCornerShape(18.dp))
            .padding(8.dp),
    ) {
        val w = size.width
        val h = size.height

        when (event) {
            ClimateEvent.HEATWAVE -> {
                drawRect(Color(0xFFFFD180), topLeft = Offset.Zero, size = Size(w, h))
                drawCircle(Color(0xFFFF9800), radius = h * 0.14f, center = Offset(w * 0.82f, h * 0.20f))
                repeat(5) { i ->
                    val x = w * (0.12f + i * 0.18f)
                    val y0 = h * (0.82f - ((phase + i * 0.13f) % 1f) * 0.35f)
                    val path = Path().apply {
                        moveTo(x, y0)
                        cubicTo(x - 16f, y0 - 24f, x + 16f, y0 - 46f, x, y0 - 70f)
                    }
                    drawPath(path, primary, style = Stroke(width = 6f, cap = StrokeCap.Round))
                }
                drawRect(Color(0xFF8D6E63), topLeft = Offset(0f, h * 0.82f), size = Size(w, h * 0.18f))
            }

            ClimateEvent.CYCLONE -> {
                drawRect(Color(0xFFB3E5FC), topLeft = Offset.Zero, size = Size(w, h))
                val center = Offset(w * 0.52f, h * 0.48f)
                repeat(4) { ring ->
                    val radius = h * (0.12f + ring * 0.10f)
                    val start = phase * 360f + ring * 28f
                    drawArc(
                        color = if (ring % 2 == 0) primary else secondary,
                        startAngle = start,
                        sweepAngle = 255f,
                        useCenter = false,
                        topLeft = Offset(center.x - radius, center.y - radius),
                        size = Size(radius * 2f, radius * 2f),
                        style = Stroke(width = 8f, cap = StrokeCap.Round),
                    )
                }
                drawCircle(Color.White, radius = h * 0.055f, center = center)
                drawRect(Color(0xFF0277BD), topLeft = Offset(0f, h * 0.84f), size = Size(w, h * 0.16f))
            }

            ClimateEvent.MONSOON -> {
                drawRect(Color(0xFFB3E5FC), topLeft = Offset.Zero, size = Size(w, h))
                drawRect(Color(0xFF4FC3F7), topLeft = Offset(0f, h * 0.72f), size = Size(w * 0.38f, h * 0.28f))
                val mountain = Path().apply {
                    moveTo(w * 0.58f, h * 0.84f)
                    lineTo(w * 0.72f, h * 0.32f)
                    lineTo(w * 0.86f, h * 0.84f)
                    close()
                }
                drawPath(mountain, Color(0xFF66BB6A))
                repeat(4) { i ->
                    val y = h * (0.30f + i * 0.10f)
                    val dx = ((phase + i * 0.17f) % 1f) * w * 0.46f
                    drawLine(
                        color = primary,
                        start = Offset(w * 0.08f + dx, y),
                        end = Offset(w * 0.22f + dx, y),
                        strokeWidth = 7f,
                        cap = StrokeCap.Round,
                    )
                }
                repeat(7) { i ->
                    val x = w * (0.48f + i * 0.055f)
                    val dropY = h * (0.25f + ((phase + i * 0.11f) % 1f) * 0.40f)
                    drawLine(secondary, Offset(x, dropY), Offset(x - 5f, dropY + 18f), 5f, StrokeCap.Round)
                }
            }

            ClimateEvent.DROUGHT -> {
                drawRect(Color(0xFFFFECB3), topLeft = Offset.Zero, size = Size(w, h))
                drawCircle(Color(0xFFFFA000), radius = h * 0.13f, center = Offset(w * 0.82f, h * 0.20f))
                drawRect(Color(0xFFC8A56A), topLeft = Offset(0f, h * 0.62f), size = Size(w, h * 0.38f))
                repeat(7) { i ->
                    val x = w * (0.08f + i * 0.14f)
                    drawLine(Color(0xFF6D4C41), Offset(x, h * 0.68f), Offset(x + 30f, h * 0.90f), 4f)
                    drawLine(Color(0xFF6D4C41), Offset(x + 30f, h * 0.90f), Offset(x + 52f, h * 0.78f), 4f)
                }
                val pulse = 10f + 7f * sin(phase * 6.28318f)
                drawCircle(tertiary, radius = pulse, center = Offset(w * 0.18f, h * 0.32f))
            }
        }
    }
}
