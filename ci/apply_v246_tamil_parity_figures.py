#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import hashlib
import json

from PIL import Image, ImageDraw, ImageFont, features

ROOT = Path.cwd()
BOOK = ROOT / "app/src/main/res/raw/book_content.json"
DRAWABLE = ROOT / "app/src/main/res/drawable-nodpi"
TA_FONT = ROOT / "app/src/main/res/font/noto_sans_tamil.ttf"
AUDIT = ROOT / "V246_TAMIL_PARITY_FIGURE_AUDIT.json"

assert BOOK.is_file(), BOOK
assert TA_FONT.is_file(), TA_FONT
assert features.check("raqm"), "Pillow RAQM/HarfBuzz support is required for Tamil shaping"
DRAWABLE.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "u2l1": {
        "figure": "fig_005_u02_ta",
        "anchor": "sci_u02_l21_ecosystem_ta",
        "position": "after",
        "title": "சூழ்நிலை மண்டலத்தில் ஆற்றல் நுழைவும் ஊட்டச்சத்து மறுசுழற்சியும்",
        "caption": "ஆற்றல் பெரும்பாலும் சூரிய ஒளியாக சூழ்நிலை மண்டலத்திற்குள் நுழைகிறது; ஊட்டச்சத்துகள் சூழ்நிலை மண்டலச் செயல்முறைகள் மூலம் மறுசுழற்சி செய்யப்படுகின்றன.",
        "alt": "சூரியன், உற்பத்தியாளர்கள், நுகர்வோர் மற்றும் சிதைப்பவர்கள் இடையிலான ஆற்றல் மற்றும் ஊட்டச்சத்து தொடர்பு",
        "english": "fig_005_u02_en",
        "size": [1600, 570],
    },
    "u2l5": {
        "figure": "fig_014_u02_ta",
        "anchor": "sci_u02_l25_watercycle_ta",
        "position": "after",
        "title": "மழைநீர் மேற்பரப்பில் ஓடலாம், மண்ணுள் ஊடுருவலாம் அல்லது நிலத்தடி நீரைச் செறிவூட்டலாம்",
        "caption": "நீர் பாதுகாப்பு, மழைநீர் மேற்பரப்பு ஓட்டம், ஊடுருவல், சேமிப்பு, ஆவியாதல் மற்றும் மனிதப் பயன்பாடு ஆகியவற்றுக்கிடையில் எவ்வாறு பகிரப்படுகிறது என்பதையும் சார்ந்துள்ளது.",
        "alt": "மழைநீர் மேற்பரப்பு ஓட்டம், மண்ணுள் ஊடுருவல் மற்றும் நிலத்தடி நீர் செறிவூட்டல்",
        "english": "fig_014_u02_en",
        "size": [1600, 800],
    },
    "u4l6": {
        "figure": "fig_038_u04_ta",
        "anchor": "sci_u04_l46_hierarchy_ta",
        "position": "before",
        "title": "கழிவு மேலாண்மை முன்னுரிமை: அகற்றத்திற்கு முன் தடுப்பு",
        "caption": "முன்னுரிமைச் செயல்கள் மேல்பகுதியில் உள்ளன; இறுதி அகற்றம் கடைசி தேர்வாகும்.",
        "alt": "தடுப்பு, மறுபயன்பாடு, மறுசுழற்சி, மீட்பு மற்றும் இறுதி அகற்றம் ஆகியவற்றைக் காட்டும் கழிவு மேலாண்மை முன்னுரிமை",
        "english": "fig_038_u04_en",
        "size": [1600, 512],
    },
    "u5l1": {
        "figure": "fig_046_u05_ta",
        "anchor": "sci_u05_l51_ta",
        "position": "after",
        "title": "எளிமைப்படுத்தப்பட்ட பசுமைக்குடில் விளைவு",
        "caption": "பசுமைக்குடில் விளைவை எளிமையாகக் காட்டும் கருத்தியல் விளக்கப்படம்.",
        "alt": "சூரிய ஒளி, பூமியிலிருந்து வெளியேறும் அகச்சிவப்புக் கதிர்வீச்சு மற்றும் மீண்டும் திரும்பும் ஆற்றலைக் காட்டும் எளிமைப்படுத்தப்பட்ட பசுமைக்குடில் விளைவு",
        "english": "fig_046_u05_en",
        "size": [1600, 800],
    },
}

BG=(247,250,248); DARK=(82,123,111)
def f(sz):
    return ImageFont.truetype(str(TA_FONT), sz, layout_engine=ImageFont.Layout.RAQM)
def round_save(im, path, radius=34):
    mask=Image.new("L", im.size, 0)
    md=ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,im.width-1,im.height-1), radius=radius, fill=255)
    rgba=im.convert("RGBA")
    rgba.putalpha(mask)
    rgba.save(path, optimize=True)

def make_u2l1(path):
    W,H=1600,570; im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.ellipse((118,85,294,261),fill=(247,203,89)); d.text((206,302),"சூரியன்",font=f(34),fill="black",anchor="mm")
    d.rounded_rectangle((430,125,805,265),radius=28,fill=(178,211,145)); d.rounded_rectangle((890,125,1165,265),radius=28,fill=(219,203,153)); d.rounded_rectangle((650,377,1005,505),radius=28,fill=(202,178,148))
    d.text((617,195),"உற்பத்தியாளர்கள்",font=f(36),fill="black",anchor="mm"); d.text((1028,195),"நுகர்வோர்",font=f(36),fill="black",anchor="mm"); d.text((827,440),"சிதைப்பவர்கள்",font=f(36),fill="black",anchor="mm")
    d.line((296,171,421,171),fill=DARK,width=9); d.line((806,171,880,171),fill=DARK,width=9); d.line((570,275,685,382),fill=DARK,width=9); d.line((1005,275,920,382),fill=DARK,width=9)
    round_save(im,path)

def make_u2l5(path):
    W,H=1600,800; im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.ellipse((156,94,323,261),fill=(250,221,111)); land=[(0,575),(0,800),(1600,800),(1600,520),(1470,555),(1330,590),(1160,620),(980,640),(820,638),(700,620),(610,580),(500,510),(390,466),(300,455),(210,468),(120,505)]; d.polygon(land,fill=(229,239,230)); d.rectangle((0,672,1600,800),fill=(209,229,243))
    d.arc((1075,85,1300,230),205,335,fill=(157,187,204),width=25); d.arc((1260,95,1500,240),205,335,fill=(157,187,204),width=25); d.line((1215,200,1215,430),fill=(90,145,177),width=10); d.line((1320,200,1320,430),fill=(90,145,177),width=10)
    d.arc((330,425,690,645),200,340,fill=(117,171,111),width=36); d.line((674,505,674,650),fill=DARK,width=13); d.polygon([(674,690),(648,648),(700,648)],fill=DARK)
    d.multiline_text((510,400),"தாவரங்கள் மேற்பரப்பு ஓட்டத்தைக்\nகுறைக்கின்றன",font=f(31),fill="black",anchor="mm",align="center",spacing=4); d.text((845,540),"ஊடுருவல்",font=f(34),fill="black",anchor="mm"); d.text((1245,718),"நிலத்தடி நீர்",font=f(36),fill="black",anchor="mm")
    round_save(im,path)

def make_u4l6(path):
    W,H=1600,512; im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    bands=[ ([(245,78),(1355,78),(1235,168),(365,168)],(167,207,185),"தடுப்பு / குறைத்தல்",36), ([(365,182),(1235,182),(1130,267),(470,267)],(190,214,175),"மறுபயன்பாடு / பழுதுபார்ப்பு",32), ([(470,282),(1130,282),(1044,363),(555,363)],(226,210,153),"மறுசுழற்சி / உரமாக்கல்",34)]
    for pts,c,t,sz in bands:
        d.polygon(pts,fill=c); xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; d.text(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2+2),t,font=f(sz),fill="black",anchor="mm")
    pts=[(555,378),(1044,378),(955,449),(645,449)]; d.polygon(pts,fill=(222,179,143)); d.text((710,414),"மீட்பு",font=f(28),fill="black",anchor="mm"); d.text((910,414),"அகற்றம்",font=f(28),fill="black",anchor="mm"); d.line((786,414,834,414),fill="black",width=4); d.polygon([(834,414),(820,405),(820,423)],fill="black")
    round_save(im,path)

def make_u5l1(path):
    W,H=1600,800; im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.ellipse((105,89,296,280),fill=(250,221,111)); d.text((202,320),"சூரியன்",font=f(32),fill="black",anchor="mm"); d.ellipse((758,255,1160,657),fill=(204,225,237),outline=(117,163,186),width=7)
    for start in range(0,360,12): d.arc((679,175,1242,738),start,start+6,fill=(145,177,165),width=10)
    d.line((286,215,746,377),fill=(225,169,49),width=11); d.text((620,230),"உள்வரும் சூரிய ஒளி",font=f(31),fill="black",anchor="mm")
    d.arc((876,15,1088,365),135,250,fill=(180,88,87),width=11); d.arc((1075,214,1374,510),220,70,fill=(180,88,87),width=11)
    d.multiline_text((1270,72),"வெளியேறும்\nஅகச்சிவப்புக்\nகதிர்வீச்சு",font=f(28),fill="black",anchor="mm",align="center",spacing=2); d.multiline_text((1370,270),"சிறிதளவு ஆற்றல்\nமீண்டும் திரும்புகிறது",font=f(29),fill="black",anchor="mm",align="center",spacing=3); d.text((800,767),"பசுமைக்குடில் வாயுக்கள் வெளியேறும் அகச்சிவப்பு ஆற்றலைப் பாதிக்கின்றன",font=f(29),fill="black",anchor="mm")
    round_save(im,path)

makers={"u2l1":make_u2l1,"u2l5":make_u2l5,"u4l6":make_u4l6,"u5l1":make_u5l1}
for lid,spec in TARGETS.items():
    makers[lid](DRAWABLE / f"{spec['figure']}.png")

before=json.loads(BOOK.read_text(encoding="utf-8"))
after=deepcopy(before)
lesson_by_id={l["id"]:l for u in after["units"] for l in u["lessons"]}
for lid,spec in TARGETS.items():
    lesson=lesson_by_id[lid]
    assert any(b.get("figure")==spec["english"] for b in lesson["english"]), (lid,"English source figure missing")
    assert not any(b.get("figure")==spec["figure"] for b in lesson["tamil"]), (lid,"Tamil counterpart already present")
    anchors=[i for i,b in enumerate(lesson["tamil"]) if b.get("figure")==spec["anchor"]]
    assert len(anchors)==1,(lid,anchors)
    idx=anchors[0] + (1 if spec["position"]=="after" else 0)
    lesson["tamil"].insert(idx,{
        "kind":"figure","title":spec["title"],"text":"","items":[],"rows":[],
        "figure":spec["figure"],"caption":spec["caption"],"alt":spec["alt"]
    })

check=deepcopy(after)
for u in check["units"]:
    for lesson in u["lessons"]:
        if lesson["id"] in TARGETS:
            new_id=TARGETS[lesson["id"]]["figure"]
            lesson["tamil"]=[b for b in lesson["tamil"] if b.get("figure")!=new_id]
assert check==before,"Unexpected book-content mutation beyond the four Tamil figure insertions"
BOOK.write_text(json.dumps(after,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

image_rows=[]
for lid,spec in TARGETS.items():
    p=DRAWABLE/f"{spec['figure']}.png"
    with Image.open(p) as im:
        assert list(im.size)==spec["size"],(lid,im.size,spec["size"])
        im.verify()
    image_rows.append({"lessonId":lid,"englishFigure":spec["english"],"tamilFigure":spec["figure"],"dimensions":spec["size"],"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})

final=json.loads(BOOK.read_text(encoding="utf-8"))
for u in final["units"]:
    for lesson in u["lessons"]:
        if lesson["id"] in TARGETS:
            en=sum(1 for b in lesson["english"] if b.get("kind") in ("figure","svg_figure") and b.get("figure"))
            ta=sum(1 for b in lesson["tamil"] if b.get("kind") in ("figure","svg_figure") and b.get("figure"))
            assert en==ta,(lesson["id"],en,ta)

AUDIT.write_text(json.dumps({
    "scope":"four user-approved Tamil visual counterparts for legacy English reinforcement figures",
    "status":"PASS",
    "insertedCount":4,
    "insertedIds":[TARGETS[x]["figure"] for x in TARGETS],
    "images":image_rows,
    "englishLessonBlocksChanged":False,
    "existingTamilBlocksChanged":False,
    "scientificLessonTextChanged":False,
    "quizPayloadChanged":False,
    "photoCreditsChanged":False,
    "packageIdentityChanged":False,
    "signingChanged":False,
    "versionIdentifiersChanged":False,
    "greenhouseTamilOverlapCorrection":{
        "figure":"fig_046_u05_ta",
        "label":"வெளியேறும் அகச்சிவப்புக் கதிர்வீச்சு",
        "oldAnchor":[1130,63],
        "newAnchor":[1270,72],
        "lineCount":3,
        "purpose":"move label clear of the left outgoing-infrared arc"
    },
},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(AUDIT.read_text(encoding="utf-8"))
