#!/usr/bin/env python3
from pathlib import Path
import json

book=Path("app/src/main/res/raw/book_content.json")
data=json.loads(book.read_text())

en={
 (1,1): "Concept to remember Environmental Studies is not merely 'ecology' or 'pollution studies'. It studies relationships among Earth systems, organisms and human society.",
 (1,5): "Environmental ethics examines the moral relationship between humans, other organisms and ecosystems.",
 (2,3): "A watershed links hillslopes, soil, vegetation, streams and groundwater. Rainfall may run off to streams or infiltrate and recharge groundwater.",
 (2,4): "Removing vegetation from a steep slope can increase runoff and soil loss.",
 (3,5): "Habitat corridors can help animals move between habitat patches, maintain gene flow and reduce the ecological effects of fragmentation when appropriately planned.",
 (4,3): "Under the 2009 CPCB NAAQS, PM₂.₅ has an annual value of 40 µg/m³ and a 24-hour value of 60 µg/m³.",
 (4,4): "Waste management begins before disposal. The preferred sequence is prevention and reduction, followed by reuse or repair, recycling or biological treatment, appropriate recovery and finally safe disposal.",
 (4,5): "Exposure connects an environmental concentration to a receptor.",
 (6,3): "Rainwater harvesting can supplement supply or recharge where design, geology and maintenance are suitable.",
 (6,5): "A circular economy seeks to keep products and materials useful for longer through durable design, sharing, maintenance, repair, reuse, remanufacturing and recycling.",
 (7,2): "Hazards become disasters when they intersect exposed and vulnerable people, infrastructure or ecosystems.",
 (7,4): "Disaster risk can be reduced by lowering exposure and vulnerability and by improving preparedness and resilience.",
 (7,5): "Environmental management is a continuous cycle: establish a baseline, identify significant impacts, set objectives, assign responsibilities, implement controls, monitor indicators and correct deviations.",
 (9,5): "A strong environmental case study separates observation from analysis. Define the problem and evidence, identify direct and underlying causes, affected ecosystems and people, and responsible institutions.",
}
ta={
 (1,1): "முக்கியக் கருத்து: சுற்றுச்சூழல் ஆய்வு சூழலியல் அல்லது மாசுபாடு ஆய்வுக்கு மட்டும் வரையறுக்கப்படாது; பூமி அமைப்புகள், உயிரினங்கள் மற்றும் மனித சமூகம் ஆகியவற்றுக்கிடையிலான ஒன்றையொன்று சார்ந்த உறவுகளை பல்துறை அணுகுமுறையில் ஆராய்கிறது.",
 (1,5): "சுற்றுச்சூழல் அறநெறி மனிதர்கள், பிற உயிரினங்கள் மற்றும் சூழ்நிலை மண்டலங்களுக்கிடையிலான அறநெறி உறவை ஆராய்கிறது.",
 (2,3): "மழைநீர் மேற்பரப்பில் ஓடி ஓடைகளில் சேரலாம் அல்லது மண்ணில் ஊடுருவி நிலத்தடி நீரைச் செறிவூட்டலாம்.",
 (2,4): "தாவர மூடுபரப்பை அகற்றுவது மண்ணரிப்பையும் கீழ்நிலப் பகுதிகளில் வண்டல் படிதலையும் அதிகரிக்கலாம்.",
 (2,5): "உணவுச் சங்கிலி ஒரு எளிய உணவுத் தொடர்புப் பாதையை காட்டுகிறது; உணவு வலை இயற்கை சூழ்நிலை மண்டலங்களில் உள்ள பல ஒன்றோடொன்று இணைந்த உணவுத் தொடர்புகளை காட்டுகிறது.",
 (3,5): "வாழிட வழித்தடங்கள் விலங்குகள் துண்டிக்கப்பட்ட வாழிடப் பகுதிகளுக்கிடையே நகரவும் மரபணு ஓட்டத்தைத் தக்கவைக்கவும் வாழிடம் துண்டாக்கத்தின் சூழலியல் விளைவுகளை குறைக்கவும் உதவலாம்.",
 (4,3): "2009 CPCB தேசிய சுற்றுப்புறக் காற்றுத் தரநிலைகளில் PM₂.₅-க்கான ஆண்டு மதிப்பு 40 µg/m³; 24 மணி மதிப்பு 60 µg/m³.",
 (4,4): "கழிவு மேலாண்மையில் தடுப்பும் குறைப்பும் முதலில் வருகின்றன; பின்னர் மறுபயன்பாடு அல்லது பழுதுபார்ப்பு, மறுசுழற்சி அல்லது உயிரியல் சிகிச்சை, பொருத்தமான மீட்பு மற்றும் இறுதியாக பாதுகாப்பான அகற்றம் வருகின்றன.",
 (4,5): "வெளிப்பாடு என்பது சுற்றுச்சூழல் செறிவை ஒரு பாதிக்கப்படக்கூடிய பெறுநருடன் இணைக்கிறது.",
 (6,1): "ஆற்றல் திறன் என்பது அதே பயனுள்ள சேவையை குறைந்த ஆற்றல் உள்ளீட்டில் வழங்குவதாகும்.",
 (6,3): "மழைநீர் சேகரிப்பும் நிலத்தடி நீர் செறிவூட்டலும் உள்ளூர் மழைப்பொழிவு, மண்–பாறை அமைப்பு, வடிவமைப்பு மற்றும் பராமரிப்பு ஆகியவற்றுக்கு ஏற்ப திட்டமிடப்பட வேண்டும்.",
 (6,5): "சுழற்சிப் பொருளாதாரம் தயாரிப்புகள், கூறுகள் மற்றும் பொருட்களை நீண்டகாலம் பயனுள்ள நிலையில் வைத்திருக்க முயல்கிறது.",
 (7,2): "மக்கள், கட்டிடங்கள், உட்கட்டமைப்பு அல்லது சூழ்நிலை மண்டலங்கள் இடரால் பாதிக்கப்படக்கூடிய பகுதிகளில் இருப்பது வெளிப்பாடு; பாதிப்புக்குள்ளாகும் தன்மை அதிகமானால் பேரிடர் அபாயமும் அதிகரிக்கலாம்.",
 (7,5): "சுற்றுச்சூழல் மேலாண்மை தொடர்ச்சியான சுழற்சி; அடிப்படை நிலையை அறிந்து, தாக்கங்களை அடையாளம் கண்டு, இலக்குகளை அமைத்து, பொறுப்புகளை ஒதுக்கி, நடவடிக்கைகளை செயல்படுத்தி, குறியீடுகளை கண்காணித்து, குறைகளைச் சரிசெய்ய வேண்டும்.",
 (9,5): "களக் குறிப்புகளில் நேரடி கவனிப்பையும் ஊகத்தையும் பிரித்துப் பதிவு செய்ய வேண்டும்; மீண்டும் மேற்கொள்ளப்படும் கவனிப்புகள் விளக்கத்தின் வலிமையை அதிகரிக்கின்றன.",
}
for ui,u in enumerate(data["units"], start=1):
    for qi,q in enumerate(u["quiz"], start=1):
        if (ui,qi) in en: q["explanationEn"]=en[(ui,qi)]
        if (ui,qi) in ta: q["explanationTa"]=ta[(ui,qi)]

assert sum(bool(q.get("explanationEn","").strip()) for u in data["units"] for q in u["quiz"]) == 58
assert sum(bool(q.get("explanationTa","").strip()) for u in data["units"] for q in u["quiz"]) == 58
book.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print("V245_EXPLANATION_REFINEMENT_PASS", len(en), len(ta))
