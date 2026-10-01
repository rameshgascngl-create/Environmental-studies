from pathlib import Path
import json, html

ROOT=Path(".")
RAW=ROOT/"app/src/main/res/raw"
BOOK=RAW/"book_content.json"
INK="#17352E"; BG="#F7FBF8"

def svg_head(title,lang):
    fam='"Noto Sans Tamil","Noto Sans",sans-serif' if lang=="ta" else '"Noto Sans",sans-serif'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xml:lang="{lang}" viewBox="0 0 1200 720" role="img" aria-label="{html.escape(title)}"><defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{INK}"/></marker><style>.t{{font-family:{fam};fill:{INK};font-size:42px;font-weight:700}}.s{{font-family:{fam};fill:{INK};font-size:30px}}.sm{{font-family:{fam};fill:{INK};font-size:26px}}.box{{stroke:{INK};stroke-width:3;rx:24;ry:24}}.arr{{stroke:{INK};stroke-width:5;fill:none;marker-end:url(#a);stroke-linecap:round}}</style></defs><rect width="1200" height="720" fill="{BG}"/>'''

def tx(x,y,s,cls="s",anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{html.escape(s)}</text>'

def box(x,y,w,h,label,fill="#E8F5E9",cls="sm"):
    words=label.split(); lines=[]; cur=""
    maxc=24 if cls=="sm" else 20
    for word in words:
        cand=(cur+" "+word).strip()
        if cur and len(cand)>maxc: lines.append(cur); cur=word
        else: cur=cand
    if cur: lines.append(cur)
    if len(lines)>3: lines=lines[:2]+[" ".join(lines[2:])]
    lh=31 if cls=="sm" else 35
    sy=y+h/2-(len(lines)-1)*lh/2+9
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="box" fill="{fill}"/>'+''.join(tx(x+w/2,sy+i*lh,z,cls) for i,z in enumerate(lines))

def ar(x1,y1,x2,y2): return f'<path d="M{x1} {y1} L{x2} {y2}" class="arr"/>'

def biodiversity(lang):
    if lang=="en":
        title="Major direct pressures on biodiversity"
        center="Biodiversity loss / change"
        labels=["Land / sea-use change","Direct exploitation","Climate change","Pollution","Invasive alien species"]
    else:
        title="உயிரிய பல்வகைத்தன்மைக்கு நேரும் முக்கிய நேரடி அழுத்தங்கள்"
        center="உயிரிய பல்வகைத்தன்மை இழப்பு / மாற்றம்"
        labels=["நில / கடல் பயன்பாட்டு மாற்றம்","நேரடி சுரண்டல்","காலநிலை மாற்றம்","மாசுபாடு","ஊடுருவும் அயல் இனங்கள்"]
    s=svg_head(title,lang)+tx(600,58,title,"t")
    s+=box(450,300,300,120,center,"#FFEBEE")
    coords=[(450,100),(50,250),(850,250),(170,540),(780,540)]
    for (x,y),lab in zip(coords,labels):
        s+=box(x,y,300,90,lab,"#E3F2FD")
        sx=x+150; sy=y+90 if y<300 else y
        ex=600; ey=300 if y<300 else 420
        s+=ar(sx,sy,ex,ey)
    return s+"</svg>"

def soil(lang):
    if lang=="en":
        title="Soil contamination: distinct exposure pathways"
        soil0="Contaminated soil"
        paths=[["Plant uptake","Food / food-chain exposure"],["Leaching","Groundwater","Drinking-water exposure"],["Runoff / erosion","Surface water","Aquatic ecosystems"]]
    else:
        title="மண் மாசுபாடு: தனித்த வெளிப்பாட்டு பாதைகள்"
        soil0="மாசுபட்ட மண்"
        paths=[["தாவர உறிஞ்சல்","உணவு / உணவுச் சங்கிலி வழி வெளிப்பாடு"],["கசிவு","நிலத்தடி நீர்","குடிநீர் வழி வெளிப்பாடு"],["மேற்பரப்பு ஓட்டம் / அரிப்பு","மேற்பரப்பு நீர்","நீர்வாழ் சூழ்நிலை மண்டலங்கள்"]]
    s=svg_head(title,lang)+tx(600,58,title,"t")+box(450,105,300,90,soil0,"#FFF3E0")
    xs=[80,450,820]; fills=["#E8F5E9","#E3F2FD","#E0F2F1"]
    for x,path,fill in zip(xs,paths,fills):
        s+=ar(600,195,x+150,270); y=270
        for i,label in enumerate(path):
            s+=box(x,y,300,80,label,fill)
            if i<len(path)-1: s+=ar(x+150,y+80,x+150,y+105)
            y+=105
    return s+"</svg>"

def greenhouse(lang):
    if lang=="en":
        title="Greenhouse effect: absorption and re-emission of infrared radiation"
        solar="Incoming solar radiation"; surf="Surface absorbs energy and warms"; ir="Outgoing infrared radiation"
        ghg="Greenhouse gases absorb and re-emit infrared radiation"; down="Part is emitted downward"; space="Part escapes to space"
    else:
        title="பசுமை இல்ல விளைவு: அகச்சிவப்புக் கதிர்வீச்சின் உறிஞ்சலும் மறுகதிர்வீச்சும்"
        solar="உள்வரும் சூரியக் கதிர்வீச்சு"; surf="மேற்பரப்பு ஆற்றலை உறிஞ்சி வெப்பமடைகிறது"; ir="வெளியேறும் அகச்சிவப்புக் கதிர்வீச்சு"
        ghg="பசுமை இல்ல வாயுக்கள் அகச்சிவப்புக் கதிர்வீச்சை உறிஞ்சி மீண்டும் கதிர்வீசுகின்றன"; down="ஒரு பகுதி கீழ்நோக்கி மேற்பரப்பை அடைகிறது"; space="ஒரு பகுதி விண்வெளிக்குத் தப்புகிறது"
    s=svg_head(title,lang)+tx(600,55,title,"t")
    s+=box(60,150,280,90,solar,"#FFF3E0")+ar(340,195,470,330)
    s+=box(430,330,340,100,surf,"#E8F5E9")+ar(600,330,600,245)+box(440,145,320,90,ir,"#E3F2FD")
    s+=ar(600,145,600,115)+box(360,500,480,100,ghg,"#F3E5F5")
    s+=ar(600,500,600,455)+ar(500,600,310,650)+box(40,625,340,70,down,"#FFE0B2")+ar(700,600,890,650)+box(820,625,340,70,space,"#E3F2FD")
    return s+"</svg>"

(RAW/"v22_u03_l32_en.svg").write_text(biodiversity("en"),encoding="utf-8")
(RAW/"v22_u03_l32_ta.svg").write_text(biodiversity("ta"),encoding="utf-8")
(RAW/"v22_u04_l44_en.svg").write_text(soil("en"),encoding="utf-8")
(RAW/"v22_u04_l44_ta.svg").write_text(soil("ta"),encoding="utf-8")
(RAW/"v221_u05_l51_en.svg").write_text(greenhouse("en"),encoding="utf-8")
(RAW/"v221_u05_l51_ta.svg").write_text(greenhouse("ta"),encoding="utf-8")

# Improve Tamil SVG language and font handling without rasterising labels.
pairs=[("மூலங்களை வரைபடு","கழிவு உருவாகும் இடங்களை வரைபடமிடு"),("காரணம் பகுப்பாய்வு","காரணங்களைப் பகுப்பாய்வு செய்"),
("வீணைத் தவிர்","வீணாக்கத்தைத் தவிர்"),("திறமையான பயன்பாடு","திறன் மிக்க பயன்பாடு"),
("நீர்ப் பயன்பாட்டு கவனிப்பு","நீர்ப் பயன்பாடு மற்றும் மழைநீர் கண்காணிப்பு"),("நீர் வரவை அறி","நீர் மூலங்களை அடையாளம் காண்"),
("கசிவு/இழப்பை காண்","கசிவு மற்றும் வீணாக்கத்தை கண்டறி"),("மனித அழுத்தம் பதிவு","மனிதச் செயல்பாடுகளால் ஏற்படும் அழுத்தங்களைப் பதிவு செய்"),
("செயல் பொறுப்பு","செயல் மற்றும் பொறுப்பை நிர்ணயி"),("குறியீடு கண்காணி","முன்னேற்றக் குறியீட்டைக் கண்காணி"),
("அமிலத் திணிவு","அமிலப் படிவு"),("சூழல் மண்டலம்","சூழ்நிலை மண்டலம்"),("உயிரினப் பன்மை","உயிரிய பல்வகைத்தன்மை"),
("ஆக்கிரமிப்பு அயல் இனங்கள்","ஊடுருவும் அயல் இனங்கள்")]
for p in RAW.glob("v22_*_ta.svg"):
    s=p.read_text(encoding="utf-8")
    for a,b in pairs: s=s.replace(a,b)
    s=s.replace("font-family:sans-serif",'font-family:"Noto Sans Tamil","Noto Sans",sans-serif')
    if "xml:lang=" not in s: s=s.replace("<svg ",'<svg xml:lang="ta" ',1)
    p.write_text(s,encoding="utf-8")

book=json.loads(BOOK.read_text(encoding="utf-8"))
def lesson(n): return next(l for u in book["units"] for l in u["lessons"] if l["number"]==n)
# Replace the scientifically vague greenhouse PNG pair in lesson flow; keep packaged PNGs untouched.
for lang,old,new,title,cap in [
("english","fig_046_u05_en","v221_u05_l51_en","The greenhouse effect is an energy-balance process","Incoming solar radiation warms the surface; Earth emits infrared radiation. Greenhouse gases absorb and re-emit part of that outgoing infrared radiation; some is emitted downward and some escapes to space."),
("tamil","fig_047_u05_ta","v221_u05_l51_ta","பசுமை இல்ல விளைவு: ஆற்றல் சமநிலைச் செயல்முறை","சூரியக் கதிர்வீச்சை உறிஞ்சி பூமியின் மேற்பரப்பு வெப்பமடைகிறது; பூமி அகச்சிவப்புக் கதிர்வீச்சை வெளியிடுகிறது. பசுமை இல்ல வாயுக்கள் அதன் ஒரு பகுதியை உறிஞ்சி மீண்டும் கதிர்வீசுகின்றன; ஒரு பகுதி கீழ்நோக்கி மேற்பரப்பை அடைகிறது, மற்றொரு பகுதி விண்வெளிக்குத் தப்புகிறது.")
]:
    for b in lesson("5.1")[lang]:
        if b.get("figure")==old:
            b["kind"]="svg_figure"; b["figure"]=new; b["title"]=title; b["caption"]=cap

# Synchronise scientific captions for corrected v2.2 SVGs.
for b in lesson("3.2")["english"]:
    if b.get("figure")=="v22_u03_l32_en":
        b["title"]="Major direct pressures on biodiversity"; b["caption"]="Land/sea-use change, direct exploitation, climate change, pollution and invasive alien species are major direct pressures driving biodiversity loss or change."
for b in lesson("3.2")["tamil"]:
    if b.get("figure")=="v22_u03_l32_ta":
        b["title"]="உயிரிய பல்வகைத்தன்மைக்கு நேரும் முக்கிய நேரடி அழுத்தங்கள்"; b["caption"]="நில/கடல் பயன்பாட்டு மாற்றம், நேரடி சுரண்டல், காலநிலை மாற்றம், மாசுபாடு மற்றும் ஊடுருவும் அயல் இனங்கள் உயிரியல் பல்வகைத்தன்மை இழப்பு அல்லது மாற்றத்தை ஏற்படுத்தும் முக்கிய நேரடி அழுத்தங்களாகும்."
for b in lesson("4.4")["english"]:
    if b.get("figure")=="v22_u04_l44_en":
        b["title"]="Soil contamination: distinct exposure pathways"; b["caption"]="Contaminated soil can expose organisms through plant uptake and the food chain, drinking water through leaching to groundwater, and aquatic ecosystems through runoff or erosion."
for b in lesson("4.4")["tamil"]:
    if b.get("figure")=="v22_u04_l44_ta":
        b["title"]="மண் மாசுபாடு: தனித்த வெளிப்பாட்டு பாதைகள்"; b["caption"]="மாசுபட்ட மண்ணிலிருந்து தாவர உறிஞ்சல் வழியாக உணவுச் சங்கிலிக்கும், கசிவு வழியாக நிலத்தடி நீர் மற்றும் குடிநீருக்கும், மேற்பரப்பு ஓட்டம் அல்லது அரிப்பு வழியாக நீர்வாழ் சூழ்நிலை மண்டலங்களுக்கும் மாசுபடுத்திகள் செல்லலாம்."

BOOK.write_text(json.dumps(book,ensure_ascii=False,indent=2),encoding="utf-8")
print("CORRECTED_SVG_COUNT",len(list(RAW.glob("*.svg"))))
print("TAMIL_SVG_COUNT",len(list(RAW.glob("*_ta.svg"))))
