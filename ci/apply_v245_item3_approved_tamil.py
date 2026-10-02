#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import hashlib
import json

BOOK = Path("app/src/main/res/raw/book_content.json")
AUDIT = Path("V245_ITEM3_APPROVED_CONTENT_APPLY.json")

U9_BLOCK4 = "பாடச்சுருக்கம்: ஒரு நிகழ்வாய்வின் நோக்கம் நிகழ்வை மட்டும் நினைவில் வைத்துக்கொள்வது அல்ல; அதன் காரணங்கள், தாக்கங்கள், சம்பந்தப்பட்ட தரப்புகள், மேற்கொள்ளப்பட்ட நடவடிக்கைகள் மற்றும் அதிலிருந்து பெறப்படும் பாடங்களைப் பகுப்பாய்வு செய்வதாகும்."
U9_BLOCK6_TITLE = "கற்றலுக்கு பயன்படும் இந்திய சுற்றுச்சூழல் வழக்குகள்"
U9_BLOCK6_TEXT = "போபால் வாயுப் பேரிடர் (Bhopal gas disaster) — 2–3 டிசம்பர் 1984: தொழிற்சாலை பாதுகாப்பு, மெத்தில் ஐசோசயனேட் (methyl isocyanate) வெளிப்பாடு, அவசரநிலைத் தயார்நிலை மற்றும் சுற்றுச்சூழல் சுகாதாரம். கங்கை செயல் திட்டம் (Ganga Action Plan) — 1985: ஆற்றுமாசு கட்டுப்பாடு, கழிவுநீர் சிகிச்சை மற்றும் நிறுவன மேலாண்மைச் சவால்கள். சைலன்ட் வேலி (Silent Valley) — 1970கள்–1980கள்: கேரளாவின் வெப்பமண்டல எப்போதும் பசுமையான காடு மற்றும் முன்மொழியப்பட்ட நீர்மின் திட்டத்தைச் சுற்றிய பாதுகாப்புப் போராட்டம். சிப்கோ இயக்கம் (Chipko movement) — 1970கள்: இமயமலைப் பகுதிகளில் சமூக அடிப்படையிலான காடு பாதுகாப்பு இயக்கம்."
U9_BLOCK7 = "முக்கியக் கருத்து: நிகழ்வாய்வுகள் சுற்றுச்சூழல் கருத்துக்களை உண்மையான முடிவுகளுடன் இணைக்கின்றன."

U1_KEY_OLD = "முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · சுற்றுச்சூழல் அறநெறி"
U1_KEY_NEW = "முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) · சுற்றுச்சூழல் அறநெறி"
U1_EXPLAIN_OLD = "தற்போதைய தலைமுறையின் தேவைகளை நிறைவேற்றும் போது எதிர்கால தலைமுறைகளின் தேவைகளைப் பூர்த்தி செய்யும் திறனை பாதிக்காத வளர்ச்சியே நிலைத்த வளர்ச்சி. சுற்றுச்சூழல் அறநெறி மனிதர்கள், பிற உயிரினங்கள், இயற்கை வளங்கள் மற்றும் எதிர்கால தலைமுறைகள் குறித்த நமது பொறுப்புகளை ஆராய்கிறது. சுற்றுச்சூழல் பாதுகாப்பு, சமூக நீதி மற்றும் பொருளாதார நலன் ஆகியவற்றை ஒருங்கிணைத்துப் பார்ப்பது அவசியம்."
SDG_SENTENCE = "நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு ஆகியவற்றை ஒருங்கிணைக்கும் உலகளாவிய கட்டமைப்பை வழங்குகின்றன."
HARM_SHIFT = "சுற்றுச்சூழல் பாதிப்பை ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது இன்றைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ வெறுமனே மாற்றும் தீர்வு முழுமையற்றது."

before_bytes = BOOK.read_bytes()
before_sha = hashlib.sha256(before_bytes).hexdigest()
data = json.loads(before_bytes.decode("utf-8"))
original = deepcopy(data)
lessons = {lesson["id"]: lesson for unit in data["units"] for lesson in unit["lessons"]}

u9 = lessons["u9l1"]
u1 = lessons["u1l4"]

# Exact approval guards.
assert len(u9["tamil"]) >= 8
assert u9["tamil"][4].get("kind") == "summary"
assert u9["tamil"][4].get("text") == U9_BLOCK4
assert u9["tamil"][6].get("kind") == "supplemental"
assert u9["tamil"][6].get("title") == U9_BLOCK6_TITLE
assert u9["tamil"][6].get("text") == U9_BLOCK6_TEXT
assert u9["tamil"][7].get("kind") == "summary"
assert u9["tamil"][7].get("text") == U9_BLOCK7
retained_block7 = deepcopy(u9["tamil"][7])

assert u1["tamil"][0].get("kind") == "key_terms"
assert u1["tamil"][0].get("text") == U1_KEY_OLD
assert u1["tamil"][1].get("kind") == "explanation"
assert u1["tamil"][1].get("text") == U1_EXPLAIN_OLD

# Apply only the approved changes.
u9["tamil"].pop(6)
u9["tamil"].pop(4)

u1["tamil"][0]["text"] = U1_KEY_NEW
u1["tamil"][1]["text"] = U1_EXPLAIN_OLD + " " + SDG_SENTENCE
u1["tamil"].insert(2, {"kind": "p", "text": HARM_SHIFT})

# Semantic no-touch proof: every lesson except the two authorised lessons is identical.
orig_lessons = {lesson["id"]: lesson for unit in original["units"] for lesson in unit["lessons"]}
new_lessons = {lesson["id"]: lesson for unit in data["units"] for lesson in unit["lessons"]}
for lid in sorted(orig_lessons):
    if lid not in {"u9l1", "u1l4"}:
        assert new_lessons[lid] == orig_lessons[lid], f"Unexpected lesson change: {lid}"

# English is untouched in both authorised lessons.
assert new_lessons["u9l1"]["english"] == orig_lessons["u9l1"]["english"]
assert new_lessons["u1l4"]["english"] == orig_lessons["u1l4"]["english"]

# All non-Tamil lesson metadata is untouched.
for lid in ("u9l1", "u1l4"):
    old = deepcopy(orig_lessons[lid]); new = deepcopy(new_lessons[lid])
    old.pop("tamil"); new.pop("tamil")
    assert new == old, f"Unexpected non-Tamil change in {lid}"

# Verify the precise approved Tamil result.
assert retained_block7 in new_lessons["u9l1"]["tamil"]
assert new_lessons["u9l1"]["tamil"][5] == retained_block7
assert all(b.get("text") != U9_BLOCK4 for b in new_lessons["u9l1"]["tamil"])
assert all(b.get("text") != U9_BLOCK6_TEXT for b in new_lessons["u9l1"]["tamil"])

assert new_lessons["u1l4"]["tamil"][0]["text"] == U1_KEY_NEW
assert new_lessons["u1l4"]["tamil"][1]["text"] == U1_EXPLAIN_OLD + " " + SDG_SENTENCE
assert new_lessons["u1l4"]["tamil"][2] == {"kind": "p", "text": HARM_SHIFT}

BOOK.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
after_sha = hashlib.sha256(BOOK.read_bytes()).hexdigest()

AUDIT.write_text(json.dumps({
    "scope": "user-approved Item 3 Tamil content correction only",
    "bookSha256Before": before_sha,
    "bookSha256After": after_sha,
    "u9l1": {
        "deletedOriginalTamilIndexes": [4, 6],
        "originalTamilBlock7RetainedUnchanged": True,
    },
    "u1l4": {
        "tamil0SdgKeyTermApplied": True,
        "tamil1SdgFrameworkSentenceApplied": True,
        "newParagraphAfterOriginalTamil1": HARM_SHIFT,
    },
    "otherLessonsUnchanged": True,
    "englishUnchanged": True,
    "nonTamilLessonMetadataUnchanged": True,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(AUDIT.read_text(encoding="utf-8"))
