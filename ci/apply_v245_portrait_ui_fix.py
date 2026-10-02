#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT=Path.cwd()
BRAND=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/BrandExperience.kt"
VISUAL=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/VisualLearning.kt"
NAV=ROOT/"app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/NavigationHost.kt"
BOOK=ROOT/"app/src/main/res/raw/book_content.json"
EXPECTED_BOOK_SHA256="b968c3e8cab017cf40e284c40dceece7fc74173c3f69f39836b67c071be9d360"

def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert sha256(BOOK)==EXPECTED_BOOK_SHA256, "validated book payload changed before portrait UI fix"

brand=BRAND.read_text(encoding="utf-8")
start=brand.index("@Composable\ninternal fun LivingEnvironmentHero")
end=brand.index("@Composable\ninternal fun ExploreByDoing", start)

new_hero=r'''@Composable
internal fun LivingEnvironmentHero(mode: LanguageMode, modifier: Modifier = Modifier) {
    val tamil = mode == LanguageMode.TAMIL
    val transition = rememberInfiniteTransition(label = "living-environment")
    val drift by transition.animateFloat(
        initialValue = -6f,
        targetValue = 6f,
        animationSpec = infiniteRepeatable(tween(3200), repeatMode = RepeatMode.Reverse),
        label = "water-drift"
    )
    val primary = MaterialTheme.colorScheme.primary
    val water = MaterialTheme.colorScheme.tertiary
    val leaf = MaterialTheme.colorScheme.secondary
    val sun = Color(0xFFEFCB57)
    val brush = Brush.horizontalGradient(
        listOf(MaterialTheme.colorScheme.primaryContainer, MaterialTheme.colorScheme.surfaceContainerHigh)
    )
    val title = if (tamil) "சுற்றுச்சூழல் ஆய்வுகள்" else "ENVIRONMENTAL STUDIES"
    val tagline = if (tamil) "கற்போம் · கவனிப்போம் · ஆராய்வோம்" else "Learn · Observe · Explore"
    val description = if (tamil)
        "பாடங்கள், அறிவியல் விளக்கப்படங்கள், களக் கவனிப்புகள், வினாடிவினா மற்றும் ஊடாடும் மாதிரிகள்"
    else
        "Lessons, scientific visuals, field observation, quizzes and interactive models"

    Surface(modifier = modifier.fillMaxWidth(), shape = RoundedCornerShape(28.dp), tonalElevation = 3.dp) {
        BoxWithConstraints(Modifier.fillMaxWidth().background(brush)) {
            if (maxWidth < 420.dp) {
                Column(
                    Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Row(
                        Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        EnvironmentMark(
                            primary = primary,
                            water = water,
                            leaf = leaf,
                            sun = sun,
                            drift = drift,
                            modifier = Modifier.size(76.dp)
                        )
                        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text(
                                if (tamil) title else "ENVIRONMENTAL\nSTUDIES",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.ExtraBold,
                                maxLines = 2,
                                color = MaterialTheme.colorScheme.onPrimaryContainer
                            )
                            Text(
                                tagline,
                                style = MaterialTheme.typography.titleSmall,
                                color = primary,
                                fontWeight = FontWeight.SemiBold,
                                maxLines = 2
                            )
                        }
                    }
                    Text(description, style = MaterialTheme.typography.bodyMedium)
                }
            } else {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 18.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    EnvironmentMark(
                        primary = primary,
                        water = water,
                        leaf = leaf,
                        sun = sun,
                        drift = drift,
                        modifier = Modifier.size(104.dp)
                    )
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            title,
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.ExtraBold,
                            maxLines = 1,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                        Text(
                            tagline,
                            style = MaterialTheme.typography.titleMedium,
                            color = primary,
                            fontWeight = FontWeight.SemiBold
                        )
                        Text(description, style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
        }
    }
}

@Composable
private fun EnvironmentMark(
    primary: Color,
    water: Color,
    leaf: Color,
    sun: Color,
    drift: Float,
    modifier: Modifier = Modifier,
) {
    Canvas(modifier) {
        drawCircle(Color(0xFFF7F3E8), radius = size.minDimension * 0.46f)
        drawCircle(sun, radius = size.minDimension * 0.075f, center = Offset(size.width * .31f, size.height * .28f))
        val hills=Path().apply {
            moveTo(size.width*.14f,size.height*.62f)
            lineTo(size.width*.34f,size.height*.43f)
            lineTo(size.width*.47f,size.height*.58f)
            lineTo(size.width*.62f,size.height*.38f)
            lineTo(size.width*.86f,size.height*.64f)
            close()
        }
        drawPath(hills, leaf.copy(alpha=.92f))
        val leafPath=Path().apply {
            moveTo(size.width*.53f,size.height*.57f)
            cubicTo(size.width*.60f,size.height*.37f,size.width*.78f,size.height*.30f,size.width*.87f,size.height*.32f)
            cubicTo(size.width*.84f,size.height*.49f,size.width*.72f,size.height*.60f,size.width*.56f,size.height*.63f)
            close()
        }
        drawPath(leafPath, primary)
        drawLine(primary, Offset(size.width*.55f,size.height*.64f), Offset(size.width*.78f,size.height*.40f), strokeWidth=3.4f, cap=StrokeCap.Round)
        for (i in 0..2) {
            val y=size.height*(.69f+i*.065f)
            drawLine(water, Offset(size.width*.18f+drift,y), Offset(size.width*.82f+drift,y), strokeWidth=5f, cap=StrokeCap.Round)
        }
        val book=Path().apply {
            moveTo(size.width*.23f,size.height*.83f); lineTo(size.width*.46f,size.height*.90f); lineTo(size.width*.50f,size.height*.86f)
            lineTo(size.width*.54f,size.height*.90f); lineTo(size.width*.77f,size.height*.83f); lineTo(size.width*.77f,size.height*.91f)
            lineTo(size.width*.54f,size.height*.98f); lineTo(size.width*.50f,size.height*.94f); lineTo(size.width*.46f,size.height*.98f); lineTo(size.width*.23f,size.height*.91f); close()
        }
        drawPath(book, primary)
    }
}

'''
brand=brand[:start]+new_hero+brand[end:]
BRAND.write_text(brand,encoding="utf-8")

visual=VISUAL.read_text(encoding="utf-8")
old='Row(Modifier.fillMaxWidth().height(IntrinsicSize.Min), horizontalArrangement = Arrangement.spacedBy(10.dp)) {'
new='Row(Modifier.fillMaxWidth().height(138.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {'
assert old in visual, "language-card row anchor missing"
visual=visual.replace(old,new,1)
VISUAL.write_text(visual,encoding="utf-8")

nav=NAV.read_text(encoding="utf-8")
old='NavigationBarItem(selected = selected, onClick = onClick, icon = { Icon(icon, contentDescription = label) }, label = { Text(label) })'
new='NavigationBarItem(selected = selected, onClick = onClick, icon = { Icon(icon, contentDescription = label, modifier = Modifier.size(26.dp)) }, label = { Text(label) }, alwaysShowLabel = true)'
assert old in nav, "phone navigation icon anchor missing"
nav=nav.replace(old,new,1)
old='NavigationRailItem(selected = selected, onClick = onClick, icon = { Icon(icon, contentDescription = label) }, label = { Text(label) })'
new='NavigationRailItem(selected = selected, onClick = onClick, icon = { Icon(icon, contentDescription = label, modifier = Modifier.size(26.dp)) }, label = { Text(label) }, alwaysShowLabel = true)'
assert old in nav, "rail navigation icon anchor missing"
nav=nav.replace(old,new,1)
NAV.write_text(nav,encoding="utf-8")

assert sha256(BOOK)==EXPECTED_BOOK_SHA256, "book payload changed during portrait UI fix"

checks={
    "portrait_hero_breaks_at_word_boundary": '"ENVIRONMENTAL\\nSTUDIES"' in BRAND.read_text(),
    "portrait_hero_uses_narrow_layout": 'if (maxWidth < 420.dp)' in BRAND.read_text(),
    "portrait_description_full_width": 'Text(description, style = MaterialTheme.typography.bodyMedium)' in BRAND.read_text(),
    "language_cards_equal_fixed_height": 'height(138.dp)' in VISUAL.read_text(),
    "phone_nav_uses_material_icons": 'Icon(icon, contentDescription = label, modifier = Modifier.size(26.dp))' in NAV.read_text(),
    "legacy_letter_nav_absent": 'Text(label.take(1))' not in NAV.read_text(),
}
assert all(checks.values()),checks
Path("V245_PORTRAIT_UI_AUDIT.json").write_text(json.dumps({
    "scope":"portrait-only device QA polish",
    "versionName":"2.4.5",
    "versionCode":20405,
    "book_content_sha256":sha256(BOOK),
    "book_content_unchanged":True,
    "scientific_content_changed":False,
    "tamil_content_changed":False,
    "quiz_payload_changed":False,
    "svg_assets_changed":False,
    "checks":checks,
},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(checks,indent=2))
