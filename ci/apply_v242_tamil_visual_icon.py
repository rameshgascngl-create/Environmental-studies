from __future__ import annotations
from pathlib import Path
import json, xml.etree.ElementTree as ET

ROOT=Path.cwd()
APP=ROOT/'app/src/main'
RAW=APP/'res/raw'
DRAW=APP/'res/drawable'
VALUES=APP/'res/values'
MANIFEST=APP/'AndroidManifest.xml'
GRADLE=ROOT/'app/build.gradle.kts'
BOOK=RAW/'book_content.json'

replacements={
 'sci_u01_l13_ta.svg':[
   ('தொழில்நுட்பம் &amp;','தொழில்நுட்பம் மற்றும்'),
   ('கழிவு &amp;','கழிவுகள் மற்றும்'),
   ('வெளியீடுகள்','உமிழ்வுகள்'),
 ],
 'sci_u03_l32_ta.svg':[
   ('நிலம்/கடல்','நிலம் / கடல்'),
   ('பயன்பாட்டு மாற்றம்','பயன்பாட்டில் மாற்றம்'),
   ('ஊடுருவும் அயல்','ஆக்கிரமிப்பு அயல்'),
 ],
 'sci_u04_l44_ta.svg':[
   ('சங்கிலி வெளிப்பாடு','சங்கிலி வழி வெளிப்பாடு'),
   ('கசிவு ஊடுருவல்','கசிவு / ஊடுருவல்'),
 ],
 'sci_u04_l45_ta.svg':[
   ('கேள்வித்திறன் / இதயநலம்','கேள்வித்திறன் / இதய நலம்'),
 ],
 'sci_u04_l47_ta.svg':[
   ('உயிரி மருத்துவக்','உயிரிமருத்துவக்'),
   ('பாதுகாப்பான உயிரி','பாதுகாப்பான'),
   ('மருத்துவ சிகிச்சை','உயிரிமருத்துவக் கழிவு சிகிச்சை'),
   ('கழிவு ஓட்டங்களை கலக்க வேண்டாம்','கழிவு வகைகளை ஒன்றோடொன்று கலக்க வேண்டாம்'),
 ],
 'sci_u05_l54_ta.svg':[
   ('மேல்வளிமண்டல UV →','மேல்வளிமண்டல UV கதிர்கள் →'),
   ('Cl / Br வெளியீடு','Cl / Br விடுவிப்பு'),
   ('அதிக UV-B','UV-B அதிகரிப்பு'),
   ('பொருட்கள் பாதிப்பு','பொருட்கள் மீது பாதிப்பு'),
 ],
 'sci_u06_l61_ta.svg':[
   ('அதே சேவைக்கு குறைந்த உள்ளீடு = அதிக திறன்','அதே சேவைக்கு குறைந்த ஆற்றல் உள்ளீடு = அதிக செயல்திறன்'),
 ],
 'sci_u06_l63_ta.svg':[
   ('அளவிடு &amp; கண்காணி','அளவிட்டு கண்காணி'),
   ('திறன் மிக்க பயன்பாடு','சிக்கனமான பயன்பாடு'),
   ('பாதுகாப்பாக','பாதுகாப்பான'),
 ],
 'sci_u07_l71_ta.svg':[
   ('மதிப்பீடு &amp;','மதிப்பீடு மற்றும்'),
 ],
 'sci_u09_l93_ta.svg':[
   ('நடவடிக்கை &amp;','நடவடிக்கை மற்றும்'),
   ('மறுகணக்காய்வு','மீள் கணக்காய்வு'),
 ],
 'sci_u09_l94_ta.svg':[
   ('சேமி &amp; கண்காணி','சேமித்தல் மற்றும் கண்காணித்தல்'),
 ],
 'sci_u09_l95_ta.svg':[
   ('உள்ளூர் சுற்றுச்சூழல் கவனிப்பு','உள்ளூர் சுற்றுச்சூழல் கண்காணிப்பு'),
   ('உயிரற்ற கூறுகள்','உயிரற்ற கூறுகளைப்'),
   ('உயிருள்ள கூறுகள்','உயிருள்ள கூறுகளைப்'),
   ('பதிவுசெய்தல்','பதிவு செய்தல்'),
   ('மனிதச் செயல்பாடுகளால் ஏற்படும் அழுத்தங்களைப் பதிவுசெய்தல் செய்','மனிதச் செயல்பாடுகளின் அழுத்தங்களைப் பதிவு செய்தல்'),
 ],
 'sci_u09_l96_ta.svg':[
   ('மறுஆய்வு &amp; மேம்பாடு','மறுஆய்வு மற்றும் மேம்பாடு'),
 ],
}
changed_svg=[]
for name,repls in replacements.items():
    p=RAW/name
    s=p.read_text(encoding='utf-8')
    before=s
    for old,new in repls:
        if old not in s:
            raise SystemExit(f'Missing SVG text anchor in {name}: {old}')
        s=s.replace(old,new)
    if s!=before:
        p.write_text(s,encoding='utf-8')
        changed_svg.append(name)

p95=RAW/'sci_u09_l95_ta.svg'
s95=p95.read_text(encoding='utf-8')
s95=s95.replace(
    '<text x="685.0" y="427.5" text-anchor="middle" class="small">மனிதச் செயல்பாடுகளின் அழுத்தங்களைப் பதிவு செய்தல்</text>',
    '<text x="685.0" y="410.0" text-anchor="middle" style="font-family:Noto Sans Tamil;fill:#17352E;font-size:24px">மனிதச் செயல்பாடுகளின்</text>\n'
    '<text x="685.0" y="442.0" text-anchor="middle" style="font-family:Noto Sans Tamil;fill:#17352E;font-size:24px">அழுத்தங்களைப் பதிவு செய்தல்</text>'
)
p95.write_text(s95,encoding='utf-8')

p=RAW/'sci_u04_l47_ta.svg'
s=p.read_text(encoding='utf-8')
s=s.replace(
    '<text x="770.0" y="488.5" text-anchor="middle" class="small">பாதுகாப்பான</text>\n'
    '<text x="770.0" y="521.5" text-anchor="middle" class="small">உயிரிமருத்துவக் கழிவு சிகிச்சை</text>',
    '<text x="770.0" y="480.0" text-anchor="middle" class="small">பாதுகாப்பான</text>\n'
    '<text x="770.0" y="510.0" text-anchor="middle" style="font-family:Noto Sans Tamil;fill:#17352E;font-size:25px">உயிரிமருத்துவக் கழிவு</text>\n'
    '<text x="770.0" y="536.0" text-anchor="middle" class="small">சிகிச்சை</text>'
)
p.write_text(s,encoding='utf-8')

new_svgs={
'sci_u03_l31_levels_ta.svg':'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" role="img" aria-label="உயிரிய பல்வகைத்தன்மையின் மூன்று நிலைகள்">
<rect width="1200" height="720" fill="#F7FBF8"/>
<style>.h{font-family:Noto Sans Tamil;fill:#17352E;font-size:34px;font-weight:700}.t{font-family:Noto Sans Tamil;fill:#17352E;font-size:27px;font-weight:700}.s{font-family:Noto Sans Tamil;fill:#17352E;font-size:22px}</style>
<text x="600" y="55" text-anchor="middle" class="h">உயிரிய பல்வகைத்தன்மையின் மூன்று நிலைகள்</text>
<rect x="55" y="110" width="330" height="535" rx="30" fill="#EAF3FB"/><rect x="435" y="110" width="330" height="535" rx="30" fill="#ECF7EE"/><rect x="815" y="110" width="330" height="535" rx="30" fill="#FFF3E7"/>
<text x="220" y="170" text-anchor="middle" class="t"><tspan x="220" dy="0">மரபியல்</tspan><tspan x="220" dy="34">பல்வகைத்தன்மை</tspan></text>
<circle cx="165" cy="350" r="62" fill="#7FA9C4"/><circle cx="250" cy="330" r="62" fill="#7FA9C4"/><circle cx="275" cy="420" r="62" fill="#7FA9C4"/>
<text x="220" y="555" text-anchor="middle" class="s"><tspan x="220">ஒரே சிற்றினத்துக்குள் காணப்படும்</tspan><tspan x="220" dy="30">மரபியல் வேறுபாடுகள்</tspan></text>
<text x="600" y="170" text-anchor="middle" class="t"><tspan x="600">சிற்றின</tspan><tspan x="600" dy="34">பல்வகைத்தன்மை</tspan></text>
<circle cx="540" cy="340" r="62" fill="#7AA56A"/><rect x="640" y="278" width="124" height="124" rx="25" fill="#7AA56A"/><path d="M600 430 L525 545 L675 545 Z" fill="#7AA56A"/>
<text x="600" y="585" text-anchor="middle" class="s"><tspan x="600">ஒரு பகுதியில் காணப்படும்</tspan><tspan x="600" dy="30">பல்வேறு சிற்றினங்கள்</tspan></text>
<text x="980" y="160" text-anchor="middle" class="t"><tspan x="980">சமூக / சூழ்நிலை மண்டல</tspan><tspan x="980" dy="34">பல்வகைத்தன்மை</tspan></text>
<path d="M855 500 L980 285 L1105 500 Z" fill="#8AAC84"/><circle cx="1000" cy="345" r="48" fill="#E1C879"/><path d="M860 535 Q980 430 1100 535" stroke="#7FA9C4" stroke-width="30" fill="none"/>
<text x="980" y="585" text-anchor="middle" class="s"><tspan x="980">பல்வேறு வாழிடங்கள் மற்றும்</tspan><tspan x="980" dy="30">சூழ்நிலை மண்டலங்கள்</tspan></text>
</svg>''',
'sci_u03_l33_india_ta.svg':'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" role="img" aria-label="இந்தியாவின் உயிரிய பல்வகைத்தன்மை — முக்கிய வாழிடங்கள்">
<rect width="1200" height="720" fill="#EAF6FB"/><style>.h{font-family:Noto Sans Tamil;fill:#17352E;font-size:34px;font-weight:700}.t{font-family:Noto Sans Tamil;fill:#17352E;font-size:26px;font-weight:600}.s{font-family:Noto Sans Tamil;fill:#17352E;font-size:22px}</style>
<text x="600" y="55" text-anchor="middle" class="h">இந்தியாவின் உயிரிய பல்வகைத்தன்மை — முக்கிய வாழிடங்கள்</text>
<text x="175" y="150" text-anchor="middle" class="t">இமயமலை</text><path d="M25 505 L175 235 L325 505 Z" fill="#8FA88F"/><path d="M110 390 L175 280 L240 390 Z" fill="#F4F7F5"/>
<text x="485" y="225" text-anchor="middle" class="t">காடுகள்</text><path d="M340 505 L485 330 L630 505 Z" fill="#72A767"/><circle cx="455" cy="410" r="30" fill="#2F6D5F"/><path d="M515 430 L550 390 L585 445 Z" fill="#2F6D5F"/>
<text x="760" y="310" text-anchor="middle" class="t">வறண்ட நிலங்கள்</text><rect x="650" y="445" width="230" height="100" fill="#D7C58B"/><circle cx="765" cy="385" r="38" fill="#F1D95B"/>
<text x="1020" y="230" text-anchor="middle" class="t">கடற்கரை மற்றும் தீவுகள்</text><path d="M875 505 L1010 350 L1190 465 L1190 545 L875 545 Z" fill="#72A767"/><ellipse cx="1030" cy="365" rx="65" ry="34" fill="#2F6D5F"/><path d="M1090 370 L1145 338 L1145 402 Z" fill="#2F6D5F"/>
<rect x="0" y="545" width="1200" height="175" fill="#76ABC6"/><text x="600" y="655" text-anchor="middle" fill="#FFFFFF" style="font-family:Noto Sans Tamil;font-size:24px">மலைகள் · காடுகள் · வறண்ட பகுதிகள் · கடற்கரை மற்றும் தீவு சூழ்நிலை மண்டலங்கள்</text>
</svg>''',
'sci_u03_l34_conservation_ta.svg':'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" role="img" aria-label="உயிரிய பல்வகைத்தன்மைப் பாதுகாப்பின் இரண்டு அணுகுமுறைகள்">
<rect width="1200" height="720" fill="#F7FBF8"/><style>.h{font-family:Noto Sans Tamil;fill:#17352E;font-size:34px;font-weight:700}.t{font-family:Noto Sans Tamil;fill:#17352E;font-size:28px;font-weight:700}.s{font-family:Noto Sans Tamil;fill:#17352E;font-size:22px}</style>
<text x="600" y="55" text-anchor="middle" class="h">உயிரிய பல்வகைத்தன்மைப் பாதுகாப்பின் இரண்டு அணுகுமுறைகள்</text>
<rect x="55" y="115" width="520" height="535" rx="30" fill="#E9F5EC"/><rect x="625" y="115" width="520" height="535" rx="30" fill="#FFF2E8"/>
<text x="315" y="175" text-anchor="middle" class="t">சூழல் உள் பாதுகாப்பு</text><text x="315" y="208" text-anchor="middle" class="s">(In-situ conservation)</text>
<path d="M140 475 L315 285 L490 475 Z" fill="#7BA76D"/><circle cx="315" cy="300" r="72" fill="#89B97D"/><rect x="300" y="350" width="30" height="160" fill="#9A6A47"/>
<text x="315" y="565" text-anchor="middle" class="s"><tspan x="315">இயற்கை வாழிடத்திலேயே இனங்களையும்</tspan><tspan x="315" dy="30">சூழ்நிலை மண்டலத்தையும் பாதுகாத்தல்</tspan></text>
<text x="885" y="175" text-anchor="middle" class="t">சூழல் வெளி பாதுகாப்பு</text><text x="885" y="208" text-anchor="middle" class="s">(Ex-situ conservation)</text>
<rect x="720" y="320" width="330" height="190" rx="28" fill="#FFFFFF"/><circle cx="815" cy="410" r="45" fill="#7AA56A"/><rect x="900" y="365" width="105" height="90" rx="20" fill="#D7E8F6"/>
<text x="885" y="565" text-anchor="middle" class="s"><tspan x="885">இனங்கள் மற்றும் மரபணு வளங்களை</tspan><tspan x="885" dy="30">இயற்கை வாழிடத்திற்கு வெளியே பாதுகாத்தல்</tspan></text>
</svg>''',
'sci_u03_l35_corridor_ta.svg':'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" role="img" aria-label="வாழிடத் துண்டாக்கத்தை குறைக்கும் வனவிலங்கு வழித்தடம்">
<rect width="1200" height="720" fill="#EAF6FB"/><style>.h{font-family:Noto Sans Tamil;fill:#17352E;font-size:34px;font-weight:700}.s{font-family:Noto Sans Tamil;fill:#17352E;font-size:23px}</style>
<text x="600" y="55" text-anchor="middle" class="h">வாழிடத் துண்டாக்கத்தை குறைக்கும் வனவிலங்கு வழித்தடம்</text>
<rect x="0" y="480" width="1200" height="240" fill="#D9C98F"/>
<circle cx="165" cy="275" r="75" fill="#5E965C"/><rect x="148" y="330" width="34" height="150" fill="#8A6043"/><path d="M25 480 L165 325 L305 480 Z" fill="#79A66C"/>
<circle cx="1035" cy="275" r="75" fill="#5E965C"/><rect x="1018" y="330" width="34" height="150" fill="#8A6043"/><path d="M895 480 L1035 325 L1175 480 Z" fill="#79A66C"/>
<rect x="440" y="445" width="320" height="60" fill="#8C8C8C"/><rect x="500" y="365" width="200" height="70" rx="28" fill="#7CA66C"/><path d="M465 435 L520 365 L520 435 Z" fill="#7CA66C"/><path d="M680 365 L735 435 L680 435 Z" fill="#7CA66C"/>
<path d="M535 345 Q570 310 620 320 Q660 304 690 330 L720 355 L695 382 L660 360 L625 365 L590 354 L560 375 L530 356 Z" fill="#8E684B"/>
<text x="600" y="575" text-anchor="middle" class="s"><tspan x="600">துண்டிக்கப்பட்ட வாழிடங்களை இணைத்து உயிரினங்களின் நகர்வு,</tspan><tspan x="600" dy="31">இனப்பெருக்கம் மற்றும் மரபணு பரிமாற்றத்தை ஆதரிக்கிறது</tspan></text>
</svg>'''
}
for name,content in new_svgs.items():
    (RAW/name).write_text(content+'\n',encoding='utf-8')

data=json.loads(BOOK.read_text(encoding='utf-8'))
route={
 'fig_019_u03_ta':'sci_u03_l31_levels_ta',
 'fig_021_u03_ta':'sci_u03_l33_india_ta',
 'fig_023_u03_ta':'sci_u03_l34_conservation_ta',
 'fig_025_u03_ta':'sci_u03_l35_corridor_ta',
}
routed=[]
for unit in data.get('units',[]):
    for lesson in unit.get('lessons',[]):
        for block in lesson.get('tamil',[]):
            old=block.get('figure')
            if old in route:
                block['kind']='svg_figure'
                block['figure']=route[old]
                routed.append((old,route[old]))
if len(routed)!=4:
    raise SystemExit(f'Expected 4 Tamil figure routes, got {routed}')

DRAW.mkdir(parents=True,exist_ok=True)
foreground='''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#FFF8F0" android:pathData="M54,18 A36,36 0,1 0,54,90 A36,36 0,1 0,54,18"/>
    <path android:fillColor="#F2CD5C" android:pathData="M37,29 A7,7 0,1 0,37,43 A7,7 0,1 0,37,29"/>
    <path android:fillColor="#2F8068" android:pathData="M51,58 C57,42 70,34 82,33 C80,47 70,57 56,61 C52,62 50,61 51,58 Z"/>
    <path android:strokeColor="#1F6552" android:strokeWidth="2.6" android:fillColor="@android:color/transparent" android:strokeLineCap="round" android:pathData="M54,62 C61,51 68,44 76,39"/>
    <path android:fillColor="#74A9C6" android:pathData="M24,63 C34,55 44,70 54,63 C64,55 74,70 84,62 L84,77 C74,84 64,70 54,77 C44,84 34,70 24,78 Z"/>
    <path android:fillColor="#1F6552" android:pathData="M30,80 L50,86 L54,83 L58,86 L78,80 L78,86 L58,92 L54,89 L50,92 L30,86 Z"/>
</vector>'''
legacy='''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="48dp" android:height="48dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#145C4E" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="#FFF8F0" android:pathData="M54,18 A36,36 0,1 0,54,90 A36,36 0,1 0,54,18"/>
    <path android:fillColor="#F2CD5C" android:pathData="M37,29 A7,7 0,1 0,37,43 A7,7 0,1 0,37,29"/>
    <path android:fillColor="#2F8068" android:pathData="M51,58 C57,42 70,34 82,33 C80,47 70,57 56,61 C52,62 50,61 51,58 Z"/>
    <path android:strokeColor="#1F6552" android:strokeWidth="2.6" android:fillColor="@android:color/transparent" android:strokeLineCap="round" android:pathData="M54,62 C61,51 68,44 76,39"/>
    <path android:fillColor="#74A9C6" android:pathData="M24,63 C34,55 44,70 54,63 C64,55 74,70 84,62 L84,77 C74,84 64,70 54,77 C44,84 34,70 24,78 Z"/>
    <path android:fillColor="#1F6552" android:pathData="M30,80 L50,86 L54,83 L58,86 L78,80 L78,86 L58,92 L54,89 L50,92 L30,86 Z"/>
</vector>'''
mono='''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#FF000000" android:pathData="M54,18 A36,36 0,1 0,54,90 A36,36 0,1 0,54,18 M51,58 C57,42 70,34 82,33 C80,47 70,57 56,61 C52,62 50,61 51,58 Z M24,63 C34,55 44,70 54,63 C64,55 74,70 84,62 L84,77 C74,84 64,70 54,77 C44,84 34,70 24,78 Z M30,80 L50,86 L54,83 L58,86 L78,80 L78,86 L58,92 L54,89 L50,92 L30,86 Z"/>
</vector>'''
(DRAW/'ic_launcher_foreground.xml').write_text(foreground+'\n',encoding='utf-8')
(DRAW/'ic_launcher_legacy.xml').write_text(legacy+'\n',encoding='utf-8')
(DRAW/'ic_launcher_monochrome.xml').write_text(mono+'\n',encoding='utf-8')
(DRAW/'launch_screen.xml').write_text('''<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/launch_background"/>
    <item android:width="152dp" android:height="152dp" android:gravity="center" android:drawable="@drawable/ic_launcher_legacy"/>
</layer-list>
''',encoding='utf-8')

colors=VALUES/'colors.xml'
cs=colors.read_text(encoding='utf-8')
if 'launch_background' not in cs:
    cs=cs.replace('</resources>','    <color name="launch_background">#EAF5F0</color>\n</resources>')
cs=cs.replace('#1F6552','#145C4E')
colors.write_text(cs,encoding='utf-8')

themes=VALUES/'themes.xml'
ts=themes.read_text(encoding='utf-8')
if 'Theme.EnvironmentalStudies.Starting' not in ts:
    ts=ts.replace('</resources>','''    <style name="Theme.EnvironmentalStudies.Starting" parent="Theme.EnvironmentalStudies">
        <item name="android:windowBackground">@drawable/launch_screen</item>
    </style>
</resources>''')
themes.write_text(ts,encoding='utf-8')

v31=APP/'res/values-v31'
v31.mkdir(parents=True,exist_ok=True)
(v31/'themes.xml').write_text('''<resources>
    <style name="Theme.EnvironmentalStudies.Starting" parent="Theme.EnvironmentalStudies">
        <item name="android:windowSplashScreenBackground">@color/launch_background</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/ic_launcher_foreground</item>
        <item name="android:windowSplashScreenAnimationDuration">350</item>
    </style>
</resources>
''',encoding='utf-8')

mt=MANIFEST.read_text(encoding='utf-8')
if 'android:theme="@style/Theme.EnvironmentalStudies"' not in mt and 'android:theme="@style/Theme.EnvironmentalStudies.Starting"' not in mt:
    raise SystemExit('Manifest theme anchor changed')
mt=mt.replace('android:theme="@style/Theme.EnvironmentalStudies"','android:theme="@style/Theme.EnvironmentalStudies.Starting"')
MANIFEST.write_text(mt,encoding='utf-8')

g=GRADLE.read_text(encoding='utf-8')
if 'versionCode = 20401' not in g or 'versionName = "2.4.1"' not in g:
    raise SystemExit('v2.4.1 identity anchor changed')
g=g.replace('versionCode = 20401','versionCode = 20402').replace('versionName = "2.4.1"','versionName = "2.4.2"')
GRADLE.write_text(g,encoding='utf-8')
data['nativeVersion']='2.4.2'
BOOK.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

for p in sorted(RAW.glob('sci_*_ta.svg')):
    ET.parse(p)
all_ta='\n'.join(p.read_text(encoding='utf-8') for p in sorted(RAW.glob('sci_*_ta.svg')))
forbidden=['பதிவுசெய்தல் செய்','உயிரி மருத்துவக்','மறுகணக்காய்வு','நிலம்/கடல்','ஊடுருவும் அயல்','வரண்ட நிலங்கள்']
residual={x:all_ta.count(x) for x in forbidden}
if any(residual.values()):
    raise SystemExit(f'Residual Tamil visual defects: {residual}')

book_text=BOOK.read_text(encoding='utf-8')
for old in route:
    if f'"figure": "{old}"' in book_text:
        raise SystemExit(f'Old Tamil raster route remains: {old}')

report={
 'versionName':'2.4.2','versionCode':20402,
 'tamil_svg_files_reviewed':len(list(RAW.glob('sci_*_ta.svg'))),
 'existing_tamil_svg_files_edited':sorted(changed_svg),
 'new_unit3_textbook_svg_plates':sorted(new_svgs),
 'unit3_png_routes_replaced':routed,
 'tamil_visual_forbidden_phrase_counts':residual,
 'launcher_icon_redesigned':True,
 'adaptive_foreground_updated':(DRAW/'ic_launcher_foreground.xml').exists(),
 'monochrome_icon_updated':(DRAW/'ic_launcher_monochrome.xml').exists(),
 'legacy_icon_updated':(DRAW/'ic_launcher_legacy.xml').exists(),
 'pre_android12_launch_screen':(DRAW/'launch_screen.xml').exists(),
 'android12_plus_splash_theme':(v31/'themes.xml').exists(),
 'starting_theme_applied':'Theme.EnvironmentalStudies.Starting' in MANIFEST.read_text(),
 'internet_dependency_added':False,
 'lesson_prose_changed':False,
 'english_content_changed':False,
 'physical_device_retest_required':True,
}
Path('V242_TAMIL_VISUAL_ICON_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
