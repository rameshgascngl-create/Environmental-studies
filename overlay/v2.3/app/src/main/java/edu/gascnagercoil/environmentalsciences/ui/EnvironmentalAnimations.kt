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
import androidx.compose.material3.Button
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

private enum class EnvironmentalProcess {
    EUTROPHICATION,
    GROUNDWATER,
    CARBON_CYCLE,
    ENERGY_FLOW,
    URBAN_HEAT,
    CIRCULAR_ECONOMY,
}

private data class ProcessText(
    val process: EnvironmentalProcess,
    val en: String,
    val ta: String,
    val enExplanation: String,
    val taExplanation: String,
)

private val environmentalProcesses = listOf(
    ProcessText(
        EnvironmentalProcess.EUTROPHICATION,
        "Eutrophication",
        "மிகை உணவூட்டம்",
        "Excess nitrogen and phosphorus stimulate algal growth. When the algal biomass dies, microbial decomposition consumes dissolved oxygen, which can stress or kill aquatic animals.",
        "அதிக நைட்ரஜன் மற்றும் பாஸ்பரஸ் பாசிகளின் வளர்ச்சியை அதிகரிக்கின்றன. பாசி உயிர்த்தொகை இறந்த பின் நுண்ணுயிர் சிதைவு கரைந்த ஆக்சிஜனைப் பயன்படுத்துவதால் நீர்வாழ் விலங்குகள் பாதிக்கப்படலாம்.",
    ),
    ProcessText(
        EnvironmentalProcess.GROUNDWATER,
        "Groundwater recharge",
        "நிலத்தடி நீர் மீள்நிரப்பு",
        "Rainfall can run off at the surface, be taken up by plants, or infiltrate into soil. Water that percolates below the root zone can replenish groundwater when geology and land cover permit.",
        "மழைநீர் மேற்பரப்பில் ஓடலாம், தாவரங்களால் எடுத்துக்கொள்ளப்படலாம் அல்லது மண்ணுக்குள் ஊடுருவலாம். வேர் மண்டலத்திற்குக் கீழே ஊடுருவிச் செல்லும் நீர், நிலவியல் மற்றும் நிலமூடி ஏற்றதாக இருந்தால், நிலத்தடி நீரை மீள்நிரப்புகிறது.",
    ),
    ProcessText(
        EnvironmentalProcess.CARBON_CYCLE,
        "Carbon cycle",
        "கார்பன் சுழற்சி",
        "Photosynthesis transfers carbon dioxide from the atmosphere into biomass. Respiration, decomposition and combustion return carbon to the atmosphere, while oceans and long-term geological storage exchange carbon on different time scales.",
        "ஒளிச்சேர்க்கை வளிமண்டல கார்பன் டைஆக்சைடை உயிர்த்தொகைக்குள் கொண்டு செல்கிறது. சுவாசம், சிதைவு மற்றும் எரிப்பு கார்பனை மீண்டும் வளிமண்டலத்திற்குத் திருப்புகின்றன; கடலும் நீண்டகால புவியியல் சேமிப்புகளும் வேறுபட்ட கால அளவுகளில் கார்பனை பரிமாறுகின்றன.",
    ),
    ProcessText(
        EnvironmentalProcess.ENERGY_FLOW,
        "Energy flow in a food chain",
        "உணவுச் சங்கிலியில் ஆற்றல் ஓட்டம்",
        "Solar energy captured by producers is transferred through trophic levels. Only part of the energy becomes new biomass at each transfer; much is used in metabolism and released as heat.",
        "உற்பத்தியாளர்கள் பிடித்துக் கொள்கின்ற சூரிய ஆற்றல் ஊட்டநிலைகள் வழியாக மாற்றப்படுகிறது. ஒவ்வொரு மாற்றத்திலும் ஒரு பகுதி மட்டுமே புதிய உயிர்த்தொகையாக சேமிக்கப்படுகிறது; பெரும்பகுதி வளர்சிதை மாற்றத்தில் பயன்படுத்தப்பட்டு வெப்பமாக வெளியேறுகிறது.",
    ),
    ProcessText(
        EnvironmentalProcess.URBAN_HEAT,
        "Urban heat island",
        "நகர வெப்பத் தீவு",
        "Dark roofs and paved surfaces absorb and store heat, while reduced vegetation limits evaporative cooling. Shade, trees, reflective surfaces and better urban design can reduce local heat exposure.",
        "கருமையான கூரைகள் மற்றும் பதிக்கப்பட்ட மேற்பரப்புகள் வெப்பத்தை உறிஞ்சி சேமிக்கின்றன; தாவரக்குறைவு ஆவியாதல் மூலம் ஏற்படும் குளிர்விப்பை குறைக்கிறது. நிழல், மரங்கள், ஒளியைப் பிரதிபலிக்கும் மேற்பரப்புகள் மற்றும் சிறந்த நகர வடிவமைப்பு உள்ளூர் வெப்ப வெளிப்பாட்டை குறைக்க உதவும்.",
    ),
    ProcessText(
        EnvironmentalProcess.CIRCULAR_ECONOMY,
        "Circular economy",
        "சுழற்சிப் பொருளாதாரம்",
        "A circular system keeps products and materials useful for longer through maintenance, reuse, repair, remanufacture and recycling. Prevention and longer product life usually come before material recycling.",
        "சுழற்சிப் பொருளாதாரம் பராமரிப்பு, மறுபயன்பாடு, பழுதுபார்ப்பு, மறுஉற்பத்தி மற்றும் மறுசுழற்சி மூலம் பொருட்களையும் மூலப்பொருட்களையும் நீண்டகாலம் பயன்பாட்டில் வைத்திருக்கிறது. கழிவு உருவாவதைத் தவிர்த்தலும் பொருளின் பயன்பாட்டுக் காலத்தை நீட்டித்தலும் பொதுவாக மறுசுழற்சிக்கு முன்னுரிமை பெறுகின்றன.",
    ),
)

@Composable
fun EnvironmentalProcessExplorer(mode: LanguageMode) {
    var selected by remember { mutableStateOf(EnvironmentalProcess.EUTROPHICATION) }
    val item = environmentalProcesses.first { it.process == selected }
    val tamil = mode == LanguageMode.TAMIL
    val narration = rememberAnimationNarration()

    ElevatedCard(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(
                if (tamil) "சுற்றுச்சூழல் செயல்முறைகள் — இயக்கப் பக்கங்கள்" else "Environmental Processes — Animated Pages",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
            Text(
                if (tamil)
                    "ஒரு செயல்முறையைத் தேர்ந்தெடுத்து இயக்கத்தைப் பாருங்கள்; பின்னர் ஒலி விளக்கத்தைக் கேளுங்கள்."
                else
                    "Choose a process, watch the animated pathway, then listen to the explanation.",
                style = MaterialTheme.typography.bodyMedium,
            )

            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(end = 8.dp),
            ) {
                items(environmentalProcesses) { process ->
                    FilterChip(
                        selected = selected == process.process,
                        onClick = {
                            narration.stop()
                            selected = process.process
                        },
                        label = { Text(if (tamil) process.ta else process.en) },
                    )
                }
            }

            EnvironmentalProcessCanvas(selected)

            Text(
                if (tamil) item.ta else item.en,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                if (tamil) item.taExplanation else item.enExplanation,
                style = MaterialTheme.typography.bodyMedium,
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Button(
                    onClick = { narration.speak(if (tamil) item.taExplanation else item.enExplanation, mode) },
                    modifier = Modifier.weight(1f),
                ) {
                    Text(if (tamil) "🔊 விளக்கம் கேட்க" else "🔊 Listen")
                }
                OutlinedButton(
                    onClick = narration.stop,
                    modifier = Modifier.weight(1f),
                ) {
                    Text(if (tamil) "நிறுத்து" else "Stop")
                }
            }
            Text(
                if (tamil)
                    "ஒலி விளக்கம் Android உரை-ஒலி (TTS) வசதியைப் பயன்படுத்துகிறது; தமிழ் குரல் சாதனத்தில் நிறுவப்பட்டிருக்க வேண்டும்."
                else
                    "Audio uses Android text-to-speech. The corresponding language voice must be installed on the device.",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.primary,
            )
        }
    }
}

@Composable
private fun EnvironmentalProcessCanvas(process: EnvironmentalProcess) {
    val transition = rememberInfiniteTransition(label = "environmental-process")
    val phase by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(4200, easing = LinearEasing)),
        label = "phase",
    )

    Canvas(
        Modifier
            .fillMaxWidth()
            .height(240.dp)
            .background(Color(0xFFF3F7F7), RoundedCornerShape(20.dp))
            .padding(8.dp),
    ) {
        val w = size.width
        val h = size.height

        when (process) {
            EnvironmentalProcess.EUTROPHICATION -> {
                drawRect(Brush.verticalGradient(listOf(Color(0xFFBDE8F7), Color(0xFF3D95B5))))
                drawRect(Color(0xFF7A5B3A), Offset(0f, h * 0.80f), Size(w, h * 0.20f))
                repeat(16) { i ->
                    val x = w * ((i * 0.067f + phase * 0.20f) % 1f)
                    val y = h * (0.18f + (i % 5) * 0.055f)
                    drawCircle(Color(0xFF5AAE45).copy(alpha = 0.80f), h * 0.018f, Offset(x, y))
                }
                repeat(9) { i ->
                    val x = w * (0.10f + i * 0.09f)
                    val y = h * (0.68f + 0.04f * sin((phase * 2f * PI + i).toFloat()))
                    drawCircle(Color.White.copy(alpha = 0.55f), h * 0.010f, Offset(x, y))
                }
                repeat(3) { i ->
                    val x = w * (0.58f + i * 0.12f)
                    val y = h * (0.66f + (i % 2) * 0.07f)
                    drawOval(Color(0xFF38576A), Offset(x, y), Size(w * 0.11f, h * 0.045f))
                    drawPath(Path().apply {
                        moveTo(x, y + h * 0.02f)
                        lineTo(x - w * 0.04f, y)
                        lineTo(x - w * 0.04f, y + h * 0.04f)
                        close()
                    }, Color(0xFF38576A))
                }
            }

            EnvironmentalProcess.GROUNDWATER -> {
                drawRect(Brush.verticalGradient(listOf(Color(0xFF8DD0F0), Color(0xFFE7F4F8))), size = Size(w, h * 0.46f))
                drawRect(Color(0xFF5D9C4E), Offset(0f, h * 0.43f), Size(w, h * 0.13f))
                drawRect(Color(0xFFC5A46D), Offset(0f, h * 0.56f), Size(w, h * 0.22f))
                drawRect(Color(0xFF8C7458), Offset(0f, h * 0.78f), Size(w, h * 0.22f))
                repeat(14) { i ->
                    val x = w * (0.08f + (i % 7) * 0.13f)
                    val y = h * (0.10f + ((phase + i * 0.09f) % 1f) * 0.68f)
                    drawLine(Color(0xFF1976D2), Offset(x, y), Offset(x - 3f, y + 15f), 3f, StrokeCap.Round)
                }
                drawRect(Color(0xFF4DA7D8).copy(alpha = 0.75f), Offset(0f, h * 0.88f), Size(w, h * 0.12f))
                repeat(7) { i ->
                    val x = w * (0.12f + i * 0.12f)
                    val top = h * (0.58f + ((phase + i * 0.11f) % 1f) * 0.24f)
                    drawCircle(Color(0xFF61B8E5), h * 0.010f, Offset(x, top))
                }
            }

            EnvironmentalProcess.CARBON_CYCLE -> {
                drawRect(Brush.verticalGradient(listOf(Color(0xFF8DCCF1), Color(0xFFE7F4ED))))
                drawRect(Color(0xFF4C9A57), Offset(0f, h * 0.72f), Size(w, h * 0.28f))
                drawCircle(Color(0xFF337A48), h * 0.12f, Offset(w * 0.25f, h * 0.56f))
                drawRect(Color(0xFF6D4C41), Offset(w * 0.235f, h * 0.56f), Size(w * 0.03f, h * 0.19f))
                drawRect(Color(0xFF6E7E86), Offset(w * 0.72f, h * 0.48f), Size(w * 0.12f, h * 0.24f))
                repeat(4) { i ->
                    val x = w * (0.77f + (i % 2) * 0.04f)
                    val y = h * (0.40f - ((phase + i * 0.17f) % 1f) * 0.24f)
                    drawCircle(Color(0xFF607D8B).copy(alpha = 0.55f), h * 0.025f, Offset(x, y))
                }
                repeat(8) { i ->
                    val a = (phase * 2f * PI + i * PI / 4f).toFloat()
                    val center = Offset(w * 0.48f, h * 0.48f)
                    val p = Offset(center.x + cos(a) * w * 0.20f, center.y + sin(a) * h * 0.18f)
                    drawCircle(Color(0xFF2F6F89), h * 0.013f, p)
                }
            }

            EnvironmentalProcess.ENERGY_FLOW -> {
                drawRect(Brush.verticalGradient(listOf(Color(0xFF8FD2F2), Color(0xFFEAF5E7))))
                drawCircle(Color(0xFFFFC857), h * 0.12f, Offset(w * 0.12f, h * 0.18f))
                val y = h * 0.72f
                val nodes = listOf(
                    Offset(w * 0.20f, y),
                    Offset(w * 0.42f, y - h * 0.10f),
                    Offset(w * 0.64f, y - h * 0.20f),
                    Offset(w * 0.84f, y - h * 0.30f),
                )
                val radii = listOf(h * 0.085f, h * 0.066f, h * 0.052f, h * 0.040f)
                nodes.forEachIndexed { i, p ->
                    drawCircle(listOf(Color(0xFF4B9B55), Color(0xFF94714F), Color(0xFF607D8B), Color(0xFF455A64))[i], radii[i], p)
                    if (i < nodes.lastIndex) {
                        drawLine(Color(0xFFFFA726), p, nodes[i + 1], 7f, StrokeCap.Round)
                        val moving = Offset(
                            p.x + (nodes[i + 1].x - p.x) * phase,
                            p.y + (nodes[i + 1].y - p.y) * phase,
                        )
                        drawCircle(Color(0xFFFFF3A6), h * 0.016f, moving)
                    }
                }
            }

            EnvironmentalProcess.URBAN_HEAT -> {
                drawRect(Brush.verticalGradient(listOf(Color(0xFF88B9D6), Color(0xFFE3E5E2))))
                drawCircle(
                    Brush.radialGradient(listOf(Color(0xFFFFF2A8), Color(0xFFFFA726), Color.Transparent), center = Offset(w*0.80f,h*0.18f), radius = h*0.28f),
                    h * 0.28f,
                    Offset(w * 0.80f, h * 0.18f),
                )
                repeat(7) { i ->
                    val x = w * (0.03f + i * 0.14f)
                    val bh = h * (0.18f + (i % 4) * 0.07f)
                    drawRect(Color(0xFF5F686C), Offset(x, h * 0.78f - bh), Size(w * 0.10f, bh))
                }
                drawRect(Color(0xFF565B5D), Offset(0f, h * 0.78f), Size(w, h * 0.22f))
                repeat(5) { i ->
                    val x = w * (0.12f + i * 0.18f)
                    val y0 = h * (0.76f - ((phase + i * 0.17f) % 1f) * 0.42f)
                    val p = Path().apply {
                        moveTo(x, y0)
                        cubicTo(x - 10f, y0 - 18f, x + 10f, y0 - 34f, x, y0 - 52f)
                    }
                    drawPath(p, Color(0xFFFF7043).copy(alpha = 0.72f), style = Stroke(5f, cap = StrokeCap.Round))
                }
                repeat(4) { i -> drawCircle(Color(0xFF3A8A50), h * 0.035f, Offset(w*(0.10f+i*0.24f),h*0.77f)) }
            }

            EnvironmentalProcess.CIRCULAR_ECONOMY -> {
                drawRect(Brush.verticalGradient(listOf(Color(0xFFDDF4EC), Color(0xFFEAF0F2))))
                val center = Offset(w * 0.50f, h * 0.50f)
                val radius = h * 0.28f
                val labels = listOf(Color(0xFF2E7D32), Color(0xFF388E3C), Color(0xFF43A047), Color(0xFF66BB6A), Color(0xFF81C784))
                repeat(5) { i ->
                    val a1 = (i * 72f + phase * 360f)
                    drawArc(
                        labels[i],
                        a1,
                        48f,
                        false,
                        Offset(center.x - radius, center.y - radius),
                        Size(radius * 2f, radius * 2f),
                        style = Stroke(h * 0.055f, cap = StrokeCap.Round),
                    )
                }
                drawCircle(Color.White, h * 0.10f, center)
                drawRect(Color(0xFF607D8B), Offset(center.x-w*0.035f,center.y-h*0.045f), Size(w*0.07f,h*0.09f))
            }
        }

        drawRect(
            Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.06f))),
            Offset.Zero,
            Size(w, h),
        )
    }
}
