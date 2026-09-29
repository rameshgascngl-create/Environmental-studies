package edu.gascnagercoil.environmentalsciences.ui

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import edu.gascnagercoil.environmentalsciences.model.LanguageMode
import kotlin.math.PI
import kotlin.math.sin

private enum class ClimateEvent { CYCLONE, FLOOD, DROUGHT, HEATWAVE, EL_NINO }

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ClimateEventsCard(mode: LanguageMode) {
    var selected by rememberSaveable { mutableStateOf(ClimateEvent.CYCLONE.name) }
    var playing by rememberSaveable { mutableStateOf(true) }
    var speed by rememberSaveable { mutableFloatStateOf(1f) }
    val event = runCatching { ClimateEvent.valueOf(selected) }.getOrDefault(ClimateEvent.CYCLONE)
    val transition = rememberInfiniteTransition(label = "climate-event")
    val loop by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = (2600 / speed.coerceIn(.5f, 2f)).toInt(), easing = LinearEasing),
            repeatMode = RepeatMode.Restart,
        ),
        label = "climate-progress",
    )
    val progress = if (playing) loop else .35f

    ElevatedCard(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(localClimate(mode, "Climate events â€” animated explainer", "à®•à®¾à®²à®¨à®¿à®²à¯ˆ à®¨à®¿à®•à®´à¯à®µà¯à®•à®³à¯ â€” à®‡à®¯à®•à¯à®• à®µà®¿à®³à®•à¯à®•à®®à¯"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
            Text(localClimate(mode,
                "Visualise cyclone, flood, drought, heatwave and El NiÃ±oâ€“ocean warming as conceptual animations.",
                "à®šà¯‚à®±à®¾à®µà®³à®¿, à®µà¯†à®³à¯à®³à®®à¯, à®µà®±à®Ÿà¯à®šà®¿, à®µà¯†à®ªà¯à®ªà®…à®²à¯ˆ à®®à®±à¯à®±à¯à®®à¯ à®Žà®²à¯ à®¨à®¿à®©à¯‹â€“à®•à®Ÿà®²à¯ à®µà¯†à®ªà¯à®ªà®®à®¾à®±à¯à®±à®¤à¯à®¤à¯ˆ à®•à®°à¯à®¤à¯à®¤à®¿à®¯à®²à¯ à®‡à®¯à®•à¯à®•à®ªà¯à®ªà®Ÿà®®à®¾à®•à®•à¯ à®•à®¾à®£à¯à®™à¯à®•à®³à¯."))
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                ClimateEvent.entries.forEach { candidate ->
                    FilterChip(selected = event == candidate, onClick = { selected = candidate.name }, label = { Text(eventName(candidate, mode)) })
                }
            }
            ClimateEventCanvas(event, progress, Modifier.fillMaxWidth().height(250.dp))
            Text(eventExplanation(event, mode))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = { playing = !playing }, modifier = Modifier.weight(1f)) {
                    Text(if (playing) localClimate(mode, "Pause", "à®‡à®Ÿà¯ˆà®¨à®¿à®±à¯à®¤à¯à®¤à¯") else localClimate(mode, "Play", "à®‡à®¯à®•à¯à®•à¯"))
                }
                OutlinedButton(onClick = { speed = 1f }, modifier = Modifier.weight(1f)) {
                    Text(localClimate(mode, "Reset speed", "à®µà¯‡à®•à®¤à¯à®¤à¯ˆ à®®à¯€à®Ÿà¯ë§ø+«¸+âŠJBˆBˆBˆ^
‰ÛØØ[Û[X]J[ÙK[š[X][ÛˆÜYY‹¸+¡ø+«ø+¥x+ãx+¥H8+­x+áø+¥x+«¸+ãHŠ_Nˆ	È‰KŒYˆ‹™›Ü›X]
ÜYY
_påÈŠBˆÛY\Š˜[YHHÜYYÛ•˜[YPÚ[™ÙHHÈÜYYH]K˜[YT˜[™ÙHHY‹‹Œ™ŠBˆ^
ˆØØ[Û[X]J[ÙKÛÛ˜Ù\X[XXÚ[™È[š[X][ÛˆÛ›NÈ]Ù\È›Ý›Ü™XØ\ÝH™X[]™[ˆ‹¸+¡ø+©8+àH8+¥x+¬8+àx+©8+ãx+©8+àx+ª¸+ãH8+ª¸+àx+¬8+¯ø+©8+¬¸+àx+¥x+ãx+¥x+¯¸+ªH8+¡ø+«ø+¥x+ãx+¥H8+­x+¯ø+¬ø+¥x+ãx+¥x+«¸+ãH8+«¸+§ø+ãx+§ø+àx+«¸+áÎÈ8+¢x+¨ø+ãx+«¸+â8+«ø+¯¸+ªH8+ª8+¯ø+¥x+­8+ãx+­x+â8+«¸+àx+ªx+ãx+ªx+¬x+¯ø+­x+¯ø+ª¸+ãx+ª¸+©8+¯ø+¬¸+ãx+¬¸+âˆŠKˆÝ[HHX]\šX[[YK\ÙÜ˜\K˜›ÙTÛX[ˆÛÛÜˆHX]\šX[[YK˜ÛÛÜ”ØÚ[YKœš[X\žKˆ
BˆBˆBŸB‚ÛÛ\ÜØX›Bœš]˜]H[ˆÛ[X]Q]™[Ø[˜\Ê]™[ˆÛ[X]Q]™[›ÙÜ™\ÜÎˆ›Ø][ÙYšY\Žˆ[ÙYšY\ˆH[ÙYšY\ŠHÂˆ˜[š[X\žHHX]\šX[[YK˜ÛÛÜ”ØÚ[YKœš[X\žBˆØ[˜\Ê[ÙYšY\‹˜˜XÚÙÜ›Ý[™
X]\šX[[YK˜ÛÛÜ”ØÚ[YKœÝ\™˜XÙU˜\šX[
JHÂˆ˜[ÈHÚ^™KÚYˆ˜[HÚ^™KšZYÚˆÚ[ˆ
]™[
HÂˆÛ[X]Q]™[ÖPÓÓ‘HOˆÂˆ˜]Ô™XÝ
ÛÛÜŠ‘‘‘MÑ‘ŠKÚ^™HHÚ^™JË
JBˆ˜]Ô™XÝ
ÛÛÜŠ‘Œ‘ÑŒŠKÜYHÙ™œÙ]
‹
ˆŽŠKÚ^™HHÚ^™JË
ˆŒÌ™ŠJBˆ˜[ÈHÙ™œÙ]
È
ˆMY‹
ˆYŠBˆ›Ý]J›ÙÜ™\ÜÈ
ˆÍŒ‹]›ÝHÊHÂˆ™\X]

HÈ\›HO‚ˆ˜[˜Y]\ÈHÈ
ˆ
Œˆ
È\›H
ˆŒÍYŠBˆ˜]Ð\˜ÊÛÛÜ‹•Ú]K˜ÛÜJ[HHŽL™ŠK\›H
ˆMY‹ŒÍY‹˜[ÙKÙ™œÙ]
ËžH˜Y]\ËËžHH˜Y]\ÊKÚ^™J˜Y]\È
ˆ‹˜Y]\È
ˆŠKÝ[HHÝ›ÚÙJÚYHL™ˆH\›H
ˆKY‹Ø\HÝ›ÚÙPØ\”›Ý[™
JBˆBˆBˆ˜]ÐÚ\˜ÛJÛÛÜŠ‘ŒÍÌÊK˜Y]\ÈH‹Ù[\ˆHÊBˆBˆÛ[X]Q]™[‘“ÓÑOˆÂˆ˜]Ô™XÝ
ÛÛÜŠ‘ÑP‘‘ŠKÚ^™HHÚ^™JË
JBˆ˜[Ø]\•ÜH
ˆ
NˆHŒˆ
ˆÚ[Š›ÙÜ™\ÜÈ
ˆ™ˆ
ˆJKÑ›Ø]

JBˆ˜]Ô™XÝ
ÛÛÜŠ‘ŒÐŽMJKÜYHÙ™œÙ]
‹Ø]\•Ü
KÚ^™HHÚ^™JËHØ]\•Ü
JBˆ™\X]
ŒŠHÈHO‚ˆ˜[H
H
ˆÙˆ
È›ÙÜ™\ÜÈ
ˆLŒŠH	HÂˆ˜[HH
H
ˆÙˆ
È›ÙÜ™\ÜÈ
ˆ
ˆKŽŠH	H

ˆNŠBˆ˜]Ó[™JÛÛÜŠ‘ŽPÌ
KÙ™œÙ]
JKÙ™œÙ]
H‹H
ÈŠKÙ‹Ø\HÝ›ÚÙPØ\”›Ý[™
BˆBˆ˜]Ô™XÝ
ÛÛÜŠ‘‘ÍJKÜYHÙ™œÙ]
È
ˆŒY‹
ˆÙŠKÚ^™HHÚ^™JÈ
ˆŒN‹
ˆŒ™ŠJBˆ˜]Ô]
]

K˜\HÈ[Ý™UÊÈ
ˆŒ‹
ˆÙŠNÈ[™UÊÈ
ˆŒNY‹
ˆŒÌŠNÈ[™UÊÈ
ˆŒÌ‹
ˆÙŠNÈÛÜÙJ
HKÛÛÜŠ‘Ž‘MŒÊJBˆBˆÛ[X]Q]™[‘“ÕQÒOˆÂˆ˜]Ô™XÝ
ÛÛÜŠ‘‘‘‘MÐN
KÚ^™HHÚ^™JË
JBˆ˜]ÐÚ\˜ÛJÛÛÜŠ‘‘‘ŒÌ
K˜Y]\ÈHÈ
ˆŒY‹Ù[\ˆHÙ™œÙ]
È
ˆŽ™‹
ˆŒŒ™ŠJBˆ˜[Ü›Ý[™H
ˆY‚ˆ˜]Ô™XÝ
ÛÛÜŠ‘‘ÎPMJKÜYHÙ™œÙ]
‹Ü›Ý[™
KÚ^™HHÚ^™JËHÜ›Ý[™
JBˆ™\X]

HÈHO‚ˆ˜[HÈ
ˆ
H
ÈJHÈY‚ˆ˜]Ô]
]

K˜\HÈ[Ý™UÊÜ›Ý[™
NÈ[™UÊHL™‹Ü›Ý[™
ÈÍŠNÈ[™UÊ
È‹Ü›Ý[™
ÈMYŠNÈ[™UÊH™‹Ü›Ý[™
ÈŠHKÛÛÜŠ‘‘ÍJKÝ[HHÝ›ÚÙJÙŠJBˆBˆBˆÛ[X]Q]™[’PUÐU‘HOˆÂˆ˜]Ô™XÝ
ÛÛÜŠ‘‘‘‘LŒŠKÚ^™HHÚ^™JË
JBˆ˜]ÐÚ\˜ÛJÛÛÜŠ‘‘‘ŽŒ
K˜Y]\ÈHÈ
ˆŒLY‹Ù[\ˆHÙ™œÙ]
È
ˆÎ‹
ˆŒŒ™ŠJBˆ˜[˜\Ù[[™HH
ˆÎ‚ˆ˜]Ô™XÝ
ÛÛÜŠ‘ÐPPM
KÜYHÙ™œÙ]
‹˜\Ù[[™JKÚ^™HHÚ^™JËH˜\Ù[[™JJBˆ™\X]
JHÈHO‚ˆ˜[HÈ
ˆ
ŒNˆ
ÈH
ˆŒM™ŠBˆ˜[]H]

Bˆ›Üˆ
Ý\[ˆ‹Œ
HÂˆ˜[^HH
ˆŒYˆ
ÈÝ\
ˆ
ˆŒN‚ˆ˜[H
ÈÚ[Š
Ý\Èˆ
È›ÙÜ™\ÜÈ
ˆŠH
ˆJKÑ›Ø]

H
ˆY‚ˆYˆ
Ý\OH
H]›[Ý™UÊ^JH[ÙH]›[™UÊ^JBˆBˆ˜]Ô]
]ÛÛÜŠ‘‘MLL
K˜ÛÜJ[HHYŠKÝ[HHÝ›ÚÙJ‹Ø\HÝ›ÚÙPØ\”›Ý[™
JBˆBˆBˆÛ[X]Q]™[‘SÓ’S“ÈOˆÂˆ˜]Ô™XÝ
ÛÛÜŠ‘‘QŒ‘‘ŠKÚ^™HHÚ^™JË
ˆŒÍYŠJBˆ˜]Ô™XÝ
ÛÛÜŠ‘ŒNMÍN
KÜYHÙ™œÙ]
‹
ˆŒÍYŠKÚ^™HHÚ^™JË
ˆYŠJBˆ˜[Ø\›VHÈ
ˆ
Œ™ˆ
ÈMYˆ
ˆ›ÙÜ™\ÜÊBˆ˜]ÓÝ˜[
ÛÛÜŠ‘‘‘ÌÊK˜ÛÜJ[HHÍYŠKÙ™œÙ]
Ø\›VHÈ
ˆŒN‹
ˆŠKÚ^™JÈ
ˆŒÍ™‹
ˆŒNŠJBˆ™\X]

HÈHO‚ˆ˜[HH
ˆ
ŒŒÙˆ
ÈH
ˆŒYŠBˆ˜]Ó[™Jš[X\žKÙ™œÙ]
È
ˆŒMY‹JKÙ™œÙ]
È
ˆÍY‹JKÙ‹Ø\HÝ›ÚÙPØ\”›Ý[™
BˆBˆBˆBˆBŸB‚œš]˜]H[ˆ]™[˜[YJ]™[ˆÛ[X]Q]™[[ÙNˆ[™ÝXYÙS[ÙJHHÚ[ˆ
]™[
HÂˆÛ[X]Q]™[ÖPÓÓ‘HOˆØØ[Û[X]J[ÙKÞXÛÛ™H‹¸+¦¸+à¸+¬x+¯¸+­x+¬ø+¯ÈŠBˆÛ[X]Q]™[‘“ÓÑOˆØØ[Û[X]J[ÙK‘›ÛÙ‹¸+­x+á¸+¬ø+ãx+¬ø+«¸+ãHŠBˆÛ[X]Q]™[‘“ÕQÒOˆØØ[Û[X]J[ÙK‘›ÝYÚ‹¸+­x+¬x+§ø+ãx+¦¸+¯ÈŠBˆÛ[X]Q]™[’PUÐU‘HOˆØØ[Û[X]J[ÙK’X]Ø]™H‹¸+­x+á¸+ª¸+ãx+ª¸+¡x+¬¸+âŠBˆÛ[X]Q]™[‘SÓ’S“ÈOˆØØ[Û[X]J[ÙK‘[špì[È‹¸+£¸+¬¸+ãH8+ª8+¯ø+ªx+âÈŠBŸB‚œš]˜]H[ˆ]™[^[˜][ÛŠ]™[ˆÛ[X]Q]™[[ÙNˆ[™ÝXYÙS[ÙJHHÚ[ˆ
]™[
HÂˆÛ[X]Q]™[ÖPÓÓ‘HOˆØØ[Û[X]J[ÙKHÞXÛÛ™H\ÈÜ™Ø[š\ÙY›Ý][™ÈÝË\™\ÜÝ\™HÚ\˜Ý[][ÛˆÝ™\ˆØ\›HØÙX[ˆØ]\‹ˆH[š[X][ÛˆYÚYÚÈ›Ý][Û‹ÛÝY˜[™È[™HØÙX[ˆÝ\™˜XÙHÚ]Ý]™\™\Ù[[™ÈH™X[ÝÜ›H˜XÚËˆ‹¸+¦¸+à¸+§ø+¯¸+ªH8+¥x+§ø+¬¸+ãH8+ª8+à8+¬8+¯ø+ªx+ãH8+«¸+áø+¬¸+ãH8+¢x+¬8+àx+­x+¯¸+¥x+àx+«¸+ãH8+©8+¯¸+­8+­8+àx+©8+ãx+©8+«¸+¨ø+ãx+§ø+¬¸+©8+ãx+©8+â8+¦¸+ãH8+¦¸+àx+¬x+ãx+¬x+¯È8+¤¸+­8+àx+¦x+ãx+¥x+àx+ª¸+§ø+àx+©8+ãx+©8+ª¸+ãx+ª¸+§ø+ãx+§È8+¦¸+àx+­8+¬x+ãx+¦¸+¯È8+¦¸+à¸+¬x+¯¸+­x+¬ø+¯ø+«ø+¯ø+ªx+ãH8+¡x+§ø+¯ø+ª¸+ãx+ª¸+§ø+â8+¡x+«¸+ãx+¦¸+«¸+¯¸+¥x+àx+«¸+ãKˆ8+¡ø+ª8+ãx+©8+¡ø+«ø+¥x+ãx+¥x+ª¸+ãx+ª¸+§ø+«¸+ãH8+¢x+¨ø+ãx+«¸+â8+«ø+¯¸+ªH8+ª¸+àx+«ø+¬¸+ãH8+ª¸+¯¸+©8+â8+«ø+â8+¥x+¯¸+§ø+ãx+§ø+àx+­x+©8+¯ø+¬¸+ãx+¬¸+âˆŠBˆÛ[X]Q]™[‘“ÓÑOˆØØ[Û[X]J[ÙK‘›ÛÙ[™ÈØØÝ\œÈÚ[ˆØ]\ˆ^ÙYYÈHØ\XÚ]HÙˆÚ[›™[Ë˜Z[˜YÙHÜˆHÜ›Ý[™ÈÝÜ™H[™ÛÛ™^H]ˆ˜Z[™˜[Ø]ÚY[ÛÛ™][Ûˆ[™˜Z[˜YÙH[X]\‹ˆ‹¸+¡¸+¬x+àx+¥x+¬ø+ãK8+­x+§ø+¯ø+¥x+¯¸+¬¸+ãx+¥x+¬ø+ãH8+¡x+¬¸+ãx+¬¸+©8+àH8+ª8+¯ø+¬¸+©8+ãx+©8+¯ø+ªx+ãH8+ª8+à8+¬8+ãH8+©8+¯¸+¦x+ãx+¥x+àx+«¸+ãH8+©8+¯ø+¬x+ªx+â8+­x+¯ø+§È8+ª8+à8+¬8+¬ø+­x+àH8+¡x+©8+¯ø+¥x+¬8+¯ø+¥x+ãx+¥x+àx+«¸+ãH8+ª¸+âø+©8+àH8+­x+á¸+¬ø+ãx+¬ø+«¸+ãH8+£ø+¬x+ãx+ª¸+§ø+¬¸+¯¸+«¸+ãKˆ8+«¸+­8+â8+«ø+¬ø+­x+àK8+ª8+à8+¬8+ãx+ª¸+ãx+ª¸+¯ø+§ø+¯ø+ª¸+ãx+ª¸+àH8+ª8+¯ø+¬¸+â8+«¸+¬x+ãx+¬x+àx+«¸+ãH8+­x+§ø+¯ø+¥x+¯¸+¬¸+ãH8+¡x+«¸+â8+ª¸+ãx+ª¸+àH8+¡x+ªx+â8+©8+ãx+©8+àx+«¸+ãH8+«¸+àx+¥x+ãx+¥x+¯ø+«ø+«¸+ãKˆŠBˆÛ[X]Q]™[‘“ÕQÒOˆØØ[Û[X]J[ÙK‘›ÝYÚ]™[ÜÈ›ÝYÚÝ\ÝZ[™YØ]\ˆYšXÚ]ˆY][Ü›ÛÙÚXØ[YÜšXÝ[\˜[[™Y›ÛÙÚXØ[›ÝYÚ\™H™[]Y]›ÝY[XØ[ˆ‹¸+ª8+à8+¨ø+ãx+§ø+¥x+¯¸+¬ˆ8+ª8+à8+¬8+ãx+ª¸+ãx+ª¸+¬x+ãx+¬x+¯¸+¥x+ãx+¥x+àx+¬x+â8+­x+¬x+§ø+ãx+¦¸+¯ø+«ø+â8+¢x+¬8+àx+­x+¯¸+¥x+ãx+¥x+àx+¥x+¯ø+¬x+©8+àKˆ8+­x+¯¸+ªx+¯ø+¬¸+â8+­x+áø+¬ø+¯¸+¨ø+ãH8+«¸+¬x+ãx+¬x+àx+«¸+ãH8+ª8+à8+¬8+¯ø+«ø+¬¸+ãH8+­x+¬x+§ø+ãx+¦¸+¯È8+©8+â¸+§ø+¬8+ãx+ª¸+àx+§ø+â8+«ø+­x+âÈ8+¡¸+ªx+¯¸+¬¸+ãH8+¤¸+ªx+ãx+¬x+¬¸+ãx+¬‹ˆŠBˆÛ[X]Q]™[’PUÐU‘HOˆØØ[Û[X]J[ÙKHX]Ø]™H\ÈH\š[ÙÙˆ[\ÝX[HYÚX]™[]]™HÈØØ[ÛÛ™][ÛœËˆ\˜][Û‹[ZY]KšYÚ][YH[\\˜]\™H[™^ÜÝ\™H[™›Y[˜ÙH[\XÝËˆ‹¸+¢x+¬ø+ãx+¬ø+à¸+¬8+ãH8+¡ø+«ø+¬¸+ãx+ª¸+â8+¤¸+ª¸+ãx+ª¸+¯ø+§ø+àx+«¸+ãx+ª¸+âø+©8+àH8+©8+â¸+§ø+¬8+ãx+ª8+ãx+©8+àH8+¡x+©8+¯ø+¥H8+­x+á¸+ª¸+ãx+ª¸+ª8+¯ø+¬¸+â8+ª8+¯ø+¬¸+­x+àx+«¸+ãH8+¥x+¯¸+¬¸+«¸+ãH8+­x+á¸+ª¸+ãx+ª¸+¡x+¬¸+â8+£¸+ªx+ª¸+ãx+ª¸+§ø+àx+«¸+ãKˆ8+ª8+à8+§ø+¯ø+ª¸+ãx+ª¸+àK8+¢8+¬8+ª¸+ãx+ª¸+©8+«¸+ãK8+¡ø+¬8+­x+àx+ª8+áø+¬8+­x+á¸+ª¸+ãx+ª¸+ª8+¯ø+¬¸+â8+«¸+¬x+ãx+¬x+àx+«¸+ãH8+­x+á¸+¬ø+¯ø+ª¸+ãx+ª¸+¯¸+§ø+àH8+©8+¯¸+¥x+ãx+¥x+©8+ãx+©8+â8+«¸+¯¸+¬x+ãx+¬x+àx+«¸+ãKˆŠBˆÛ[X]Q]™[‘SÓ’S“ÈOˆØØ[Û[X]J[ÙK‘[špì[È[›Û™\È[\ÝX[HØ\›HÙ[˜[ÙX\Ý\›ˆ\]X]ÜšX[XÚYšXÈÝ\™˜XÙHØ]\œÈ[™Ú[™Ù\È[ˆ›ÜXØ[][ÜÜ\šXÈÚ\˜Ý[][Û‹ˆ]Ø[ˆ[™›Y[˜ÙH˜Z[™˜[]\›œË]Ù\È›Ý]\›Z[™H]™\žH[ÛœÛÛÛˆÝ]ÛÛYHžH]Ù[‹ˆ‹¸+«¸+©8+ãx+©8+¯ø+«È8+«¸+¬x+ãx+¬x+àx+«¸+ãH8+¥x+¯ø+­8+¥x+ãx+¥x+àH8+¦¸+«¸+­x+á¸+¬ø+¯ø+ª¸+ãH8+ª¸+¦¸+¯ø+ª¸+¯ø+¥x+ãH8+¥x+§ø+¬¸+¯ø+ªx+ãH8+«¸+áø+¬x+ãx+ª¸+¬8+ª¸+ãx+ª¸+àH8+ª8+à8+¬8+ãH8+­x+­8+¥x+ãx+¥x+©8+ãx+©8+â8+­x+¯ø+§È8+¦¸+à¸+§ø+¯¸+¥x+àx+©8+¬¸+ãH8+«¸+¬x+ãx+¬x+àx+«¸+ãH8+­x+á¸+ª¸+ãx+ª¸+«¸+¨ø+ãx+§ø+¬ˆ8+­x+¬ø+¯ø+«¸+¨ø+ãx+§ø+¬¸+¦¸+ãH8+¦¸+àx+­8+¬x+ãx+¦¸+¯È8+«¸+¯¸+¬x+ãx+¬x+¦x+ãx+¥x+¬ø+ãH8+£¸+¬¸+ãH8+ª8+¯ø+ªx+âø+­x+¯ø+ªx+ãH8+«¸+àx+¥x+ãx+¥x+¯ø+«È8+¡x+«¸+ãx+¦¸+¦x+ãx+¥x+¬ø+ãKˆ8+¡ø+©8+àH8+«¸+­8+â8+­x+§ø+¯ø+­x+¦x+ãx+¥x+¬ø+â8+ª¸+ãH8+ª¸+¯¸+©8+¯ø+¥x+ãx+¥x+¬¸+¯¸+«¸+ãNÈ8+¡¸+ªx+¯¸+¬¸+ãH8+¤¸+­x+ãx+­x+â¸+¬8+àH8+ª¸+¬8+àx+­x+«¸+­8+â8+­x+¯ø+¬ø+â8+­x+â8+«ø+àx+«¸+ãH8+©8+ªx+¯ø+«ø+¯¸+¥H8+ª8+¯ø+¬8+ãx+¨ø+«ø+¯ø+ª¸+ãx+ª¸+©8+¯ø+¬¸+ãx+¬¸+âˆŠBŸB‚œš]˜]H[ˆØØ[Û[X]J[ÙNˆ[™ÝXYÙS[ÙK[ŽˆÝš[™ËNˆÝš[™ÊHHYˆ
[ÙHOH[™ÝXYÙS[ÙK•SRS
HH[ÙH[‚