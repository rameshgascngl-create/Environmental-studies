package edu.gascnagercoil.environmentalsciences.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun UnitSceneHero(unitNumber: Int, modifier: Modifier = Modifier) {
    EnvironmentalUnitScene(
        unitNumber = unitNumber,
        modifier = modifier
            .fillMaxWidth()
            .height(190.dp)
            .clip(RoundedCornerShape(22.dp)),
    )
}

@Composable
fun UnitSceneThumbnail(unitNumber: Int, modifier: Modifier = Modifier) {
    EnvironmentalUnitScene(
        unitNumber = unitNumber,
        modifier = modifier.clip(RoundedCornerShape(16.dp)),
    )
}

@Composable
private fun EnvironmentalUnitScene(unitNumber: Int, modifier: Modifier) {
    Canvas(modifier = modifier.background(Color(0xFFE9F3F1))) {
        val w = size.width
        val h = size.height

        fun sky(top: Color = Color(0xFF86C9F4), bottom: Color = Color(0xFFE8F4FF)) {
            drawRect(Brush.verticalGradient(listOf(top, bottom)))
        }

        fun sun(x: Float = 0.82f, y: Float = 0.20f, scale: Float = 0.12f) {
            val c = Offset(w * x, h * y)
            drawCircle(
                brush = Brush.radialGradient(
                    listOf(Color(0xFFFFF8C4), Color(0xFFFFC857), Color.Transparent),
                    center = c,
                    radius = h * scale * 2.2f,
                ),
                radius = h * scale * 2.2f,
                center = c,
            )
            drawCircle(Color(0xFFFFD166), radius = h * scale, center = c)
        }

        fun hills() {
            val far = Path().apply {
                moveTo(0f, h * 0.64f)
                cubicTo(w * 0.20f, h * 0.46f, w * 0.34f, h * 0.54f, w * 0.50f, h * 0.42f)
                cubicTo(w * 0.66f, h * 0.31f, w * 0.82f, h * 0.49f, w, h * 0.39f)
                lineTo(w, h)
                lineTo(0f, h)
                close()
            }
            drawPath(far, Brush.verticalGradient(listOf(Color(0xFF7EBB78), Color(0xFF3F7D57))))
            val near = Path().apply {
                moveTo(0f, h * 0.76f)
                cubicTo(w * 0.22f, h * 0.60f, w * 0.40f, h * 0.70f, w * 0.58f, h * 0.55f)
                cubicTo(w * 0.72f, h * 0.44f, w * 0.86f, h * 0.67f, w, h * 0.58f)
                lineTo(w, h)
                lineTo(0f, h)
                close()
            }
            drawPath(near, Brush.verticalGradient(listOf(Color(0xFF4F9A61), Color(0xFF245B45))))
        }

        fun river() {
            val p = Path().apply {
                moveTo(w * 0.42f, h * 0.55f)
                cubicTo(w * 0.50f, h * 0.67f, w * 0.43f, h * 0.77f, w * 0.34f, h)
                lineTo(w * 0.66f, h)
                cubicTo(w * 0.59f, h * 0.78f, w * 0.62f, h * 0.65f, w * 0.56f, h * 0.54f)
                close()
            }
            drawPath(p, Brush.verticalGradient(listOf(Color(0xFF78D5F5), Color(0xFF1F78B4))))
            repeat(5) { i ->
                val yy = h * (0.68f + i * 0.06f)
                drawLine(Color.White.copy(alpha = 0.48f), Offset(w * 0.42f, yy), Offset(w * 0.55f, yy), 2f)
            }
        }

        fun trees(start: Int = 0, count: Int = 8, y: Float = 0.78f) {
            repeat(count) { i ->
                val x = w * (0.06f + ((i + start) % 10) * 0.095f)
                val trunkTop = h * (y - 0.17f - (i % 3) * 0.015f)
                drawRect(Color(0xFF6D4C41), Offset(x, trunkTop), Size(w * 0.018f, h * 0.18f))
                drawCircle(Color(0xFF2F7D45), radius = h * 0.075f, center = Offset(x + w * 0.009f, trunkTop))
                drawCircle(Color(0xFF3D9655), radius = h * 0.055f, center = Offset(x - w * 0.025f, trunkTop + h * 0.03f))
                drawCircle(Color(0xFF4CA563), radius = h * 0.050f, center = Offset(x + w * 0.04f, trunkTop + h * 0.03f))
            }
        }

        fun clouds() {
            repeat(3) { i ->
                val x = w * (0.12f + i * 0.27f)
                val y = h * (0.16f + (i % 2) * 0.08f)
                drawCircle(Color.White.copy(alpha = 0.72f), h * 0.045f, Offset(x, y))
                drawCircle(Color.White.copy(alpha = 0.75f), h * 0.060f, Offset(x + w * 0.04f, y - h * 0.015f))
                drawCircle(Color.White.copy(alpha = 0.70f), h * 0.042f, Offset(x + w * 0.08f, y))
            }
        }

        when (unitNumber) {
            1 -> {
                sky(Color(0xFF4F9EDB), Color(0xFFD8F3FF))
                sun()
                val earth = Offset(w * 0.48f, h * 0.62f)
                drawCircle(
                    brush = Brush.radialGradient(
                        listOf(Color(0xFF81D4FA), Color(0xFF1976B9)),
                        center = Offset(earth.x - w * 0.08f, earth.y - h * 0.10f),
                        radius = h * 0.35f,
                    ),
                    radius = h * 0.29f,
                    center = earth,
                )
                val land1 = Path().apply {
                    moveTo(earth.x - w * 0.13f, earth.y - h * 0.14f)
                    cubicTo(earth.x - w * 0.04f, earth.y - h * 0.25f, earth.x + w * 0.02f, earth.y - h * 0.15f, earth.x + w * 0.09f, earth.y - h * 0.17f)
                    cubicTo(earth.x + w * 0.12f, earth.y - h * 0.05f, earth.x + w * 0.02f, earth.y + h * 0.02f, earth.x - w * 0.03f, earth.y + h * 0.05f)
                    close()
                }
                drawPath(land1, Color(0xFF4D9D65))
                drawArc(Color.White.copy(alpha = 0.35f), 195f, 125f, false, Offset(earth.x-h*0.29f,earth.y-h*0.29f), Size(h*0.58f,h*0.58f), style=Stroke(h*0.018f))
                clouds()
            }
            2 -> {
                sky()
                sun()
                hills()
                river()
                trees(count = 9)
            }
            3 -> {
                sky(Color(0xFF5FA7D8), Color(0xFFDFF5EE))
                sun(0.80f, 0.16f, 0.10f)
                hills()
                trees(count = 10)
                drawOval(Color(0xFF2F7FC1), Offset(w * 0.02f, h * 0.76f), Size(w * 0.34f, h * 0.20f))
                repeat(5) { i ->
                    val bx = w * (0.18f + i * 0.11f)
                    val by = h * (0.24f + (i % 2) * 0.06f)
                    drawArc(Color(0xFF25384A), 200f, 140f, false, Offset(bx, by), Size(w*0.06f,h*0.045f), style=Stroke(2.4f))
                }
            }
            4 -> {
                sky(Color(0xFF7F9AA9), Color(0xFFDCE2E4))
                drawRect(Brush.verticalGradient(listOf(Color(0xFFC7D0D4), Color(0xFF8B969B))), Offset(0f,h*0.38f), Size(w,h*0.30f))
                repeat(7) { i ->
                    val bw = w * (0.07f + (i%3)*0.018f)
                    val bh = h * (0.22f + (i%4)*0.05f)
                    val x = w * (0.03f + i*0.135f)
                    drawRect(Color(0xFF53656E), Offset(x, h*0.78f-bh), Size(bw,bh))
                    repeat(3) { r -> repeat(2) { c ->
                        drawRect(Color(0xFFFFD77A).copy(alpha=0.65f), Offset(x+bw*(0.2f+c*0.42f), h*0.78f-bh+bh*(0.20f+r*0.22f)), Size(bw*0.14f,bh*0.08f))
                    }}
                }
                drawRect(Color(0xFF5F7F45), Offset(0f,h*0.78f), Size(w,h*0.22f))
                repeat(4) { i ->
                    drawCircle(Color(0xFF3C8B52), h*0.045f, Offset(w*(0.12f+i*0.24f),h*0.78f))
                }
            }
            5 -> {
                sky(Color(0xFF72A9D6), Color(0xFFE8F0F3))
                sun(0.80f,0.20f,0.14f)
                val globe=Offset(w*0.34f,h*0.62f)
                drawCircle(Brush.radialGradient(listOf(Color(0xFF7DD3FC),Color(0xFF146C94)),center=globe,radius=h*0.26f),h*0.24f,globe)
                drawCircle(Color(0xFF4E9F65),h*0.09f,Offset(globe.x-w*0.05f,globe.y-h*0.05f))
                val storm=Offset(w*0.70f,h*0.50f)
                repeat(4){i->
                    val ang=(i*PI/2.0).toFloat()
                    val p=Offset(storm.x+cos(ang)*h*0.10f,storm.y+sin(ang)*h*0.10f)
                    drawArc(Color.White.copy(alpha=0.85f),i*70f,220f,false,Offset(p.x-h*0.08f,p.y-h*0.08f),Size(h*0.16f,h*0.16f),style=Stroke(h*0.026f))
                }
            }
            6 -> {
                sky(Color(0xFF6EB9E8), Color(0xFFE7F7F2))
                sun()
                drawRect(Color(0xFF6FAE54), Offset(0f,h*0.70f), Size(w,h*0.30f))
                repeat(3){i->
                    val x=w*(0.12f+i*0.24f)
                    val y=h*0.62f
                    val pw=w*0.18f
                    val ph=h*0.11f
                    drawRect(Color(0xFF174C6C), Offset(x,y), Size(pw,ph))
                    repeat(3){c-> drawLine(Color(0xFF70BCE8),Offset(x+pw*(c+1)/4f,y),Offset(x+pw*(c+1)/4f,y+ph),1.5f)}
                    drawLine(Color(0xFF5C6B73),Offset(x+pw*0.5f,y+ph),Offset(x+pw*0.5f,h*0.78f),3f)
                }
                val tx=w*0.84f
                drawLine(Color(0xFFECEFF1),Offset(tx,h*0.72f),Offset(tx,h*0.31f),6f)
                val hub=Offset(tx,h*0.31f)
                repeat(3){i->
                    val a=(i*2*PI/3).toFloat()
                    drawLine(Color.White,hub,Offset(hub.x+cos(a)*h*0.16f,hub.y+sin(a)*h*0.16f),5f)
                }
            }
            7 -> {
                sky(Color(0xFF8AB8D5), Color(0xFFE2EBEE))
                clouds()
                drawRect(Color(0xFF7A8B8F), Offset(0f,h*0.58f), Size(w,h*0.18f))
                repeat(6){i->
                    val x=w*(0.05f+i*0.16f)
                    drawRect(Color(0xFF566A70),Offset(x,h*0.40f),Size(w*0.10f,h*0.28f))
                }
                drawRect(Brush.verticalGradient(listOf(Color(0xFF7BC4E8),Color(0xFF2A79A4))),Offset(0f,h*0.76f),Size(w,h*0.24f))
                repeat(5){i-> drawCircle(Color(0xFF3B8E54),h*0.045f,Offset(w*(0.10f+i*0.18f),h*0.73f))}
            }
            8 -> {
                sky(Color(0xFF7EB6DB), Color(0xFFF0F4F1))
                sun(0.82f,0.17f,0.09f)
                hills()
                drawRect(Color(0xFFF1E8D5),Offset(w*0.12f,h*0.34f),Size(w*0.36f,h*0.46f))
                drawRect(Color(0xFF4C6A74),Offset(w*0.15f,h*0.38f),Size(w*0.30f,h*0.045f))
                repeat(4){i-> drawLine(Color(0xFF7A8D94),Offset(w*0.18f,h*(0.49f+i*0.07f)),Offset(w*0.42f,h*(0.49f+i*0.07f)),2f)}
                drawCircle(Color(0xFF4D9D65),h*0.09f,Offset(w*0.69f,h*0.58f))
                drawLine(Color(0xFF6D4C41),Offset(w*0.69f,h*0.66f),Offset(w*0.69f,h*0.82f),5f)
            }
            else -> {
                sky(Color(0xFF77B6DA), Color(0xFFE6F3EC))
                sun()
                hills()
                trees(count=7)
                drawRect(Color(0xFFB7A27D),Offset(w*0.16f,h*0.70f),Size(w*0.52f,h*0.13f))
                drawRect(Color(0xFFE7E2D5),Offset(w*0.24f,h*0.50f),Size(w*0.32f,h*0.20f))
                drawPath(Path().apply{
                    moveTo(w*0.20f,h*0.50f); lineTo(w*0.40f,h*0.38f); lineTo(w*0.60f,h*0.50f); close()
                },Color(0xFF9C5A4A))
            }
        }

        drawRect(
            brush = Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.08f))),
            topLeft = Offset.Zero,
            size = Size(w, h),
        )
    }
}
