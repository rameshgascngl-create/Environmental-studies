#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

BOOK = Path("app/src/main/res/raw/book_content.json")
data = json.loads(BOOK.read_text(encoding="utf-8"))
lessons = {lesson["id"]: lesson for unit in data["units"] for lesson in unit["lessons"]}

U9_DELETED_SUMMARY = "பாடச்சுருக்கம்: ஒரு நிகழ்வாய்வின் நோக்கம் நிகழ்வை மட்டும் நினைவில் வைத்துக்கொள்வது அல்ல; அதன் காரணங்கள், தாக்கங்கள், சம்பந்தப்பட்ட தரப்புகள், மேற்கொள்ளப்பட்ட நடவடிக்கைகள் மற்றும் அதிலிருந்து பெறப்படும் பாடங்களைப் பகுப்பாய்வு செய்வதாகும்."
U9_DELETED_SUPPLEMENT = "போபால் வாயுப் பேரிடர் (Bhopal gas disaster) — 2–3 டிசம்பர் 1984: தொழிற்சாலை பாதுகாப்பு, மெத்தில் ஐசோசயனேட் (methyl isocyanate) வெளிப்பாடு, அவசரநிலைத் தயார்நிலை மற்றும் சுற்றுச்சூழல் சுகாதாரம். கங்கை செயல் திட்டம் (Ganga Action Plan) — 1985: ஆற்றுமாசு கட்டுப்பாடு, கழிவுநீர் சிகிச்சை மற்றும் நிறுவன மேலாண்மைச் சவால்கள். சைலன்ட் வேலி (Silent Valley) — 1970கள்–1980கள்: கேரளாவின் வெப்பமண்டல எப்போதும் பசுமையான காடு மற்றும் முன்மொழியப்பட்ட நீர்மின் திட்டத்தைச் சுற்றிய பாதுகாப்புப் போராட்டம். சிப்கோ இயக்கம் (Chipko movement) — 1970கள்: இமயமலைப் பகுதிகளில் சமூக அடிப்படையிலான காடு பாதுகாப்பு இயக்கம்."
U9_RETAINED = "முக்கியக் கருத்து: நிகழ்வாய்வுகள் சுற்றுச்சூழல் கருத்துக்களை உண்மையான முடிவுகளுடன் இணைக்கின்றன."
U1_KEY = "முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) · சுற்றுச்சூழல் அறநெறி"
SDG_SENTENCE = "நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு ஆகியவற்றை ஒருங்கிணைக்கும் உலகளாவிய கட்டமைப்பை வழங்குகின்றன."
HARM_SHIFT = "சுற்றுச்சூழல் பாதிப்பை ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது இன்றைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ வெறுமனே மாற்றும் தீர்வு முழுமையற்றது."

u9 = lessons["u9l1"]
u1 = lessons["u1l4"]

u9_texts = [b.get("text", "") for b in u9["tamil"]]
duplication = U9_DELETED_SUMMARY in u9_texts or U9_DELETED_SUPPLEMENT in u9_texts
retained = sum(x == U9_RETAINED for x in u9_texts) == 1
assert not duplication
assert retained

u1_t0 = u1["tamil"][0]
u1_t1 = u1["tamil"][1]
u1_t2 = u1["tamil"][2]
sdg_key = u1_t0.get("kind") == "key_terms" and u1_t0.get("text") == U1_KEY
sdg_sentence = u1_t1.get("kind") == "explanation" and SDG_SENTENCE in u1_t1.get("text", "")
harm_shift = u1_t2 == {"kind": "p", "text": HARM_SHIFT}
omission = not (sdg_key and sdg_sentence and harm_shift)
assert not omission

report = {
    "item3_status": "CLOSED",
    "book_content_sha256": hashlib.sha256(BOOK.read_bytes()).hexdigest(),
    "u9l1": {
        "duplication_detected": False,
        "deleted_original_tamil_indexes": [4, 6],
        "original_tamil_block_7_retained_unchanged": retained,
    },
    "u1l4": {
        "omission_detected": False,
        "sdg_key_term_present": sdg_key,
        "sdg_framework_sentence_present": sdg_sentence,
        "approved_harm_shifting_paragraph_present": harm_shift,
    },
    "tamil_prose_changed": True,
    "change_scope": "user-approved Item 3 only",
}
Path("V245_ITEM3_TAMIL_PARITY_AUDIT.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
