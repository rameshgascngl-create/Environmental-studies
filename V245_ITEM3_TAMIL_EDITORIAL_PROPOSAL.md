# Environmental Studies v2.4.5 — Item 3 Tamil editorial proposal

Status: **PROPOSAL ONLY — NOT APPLIED**  
Tamil wording status: **USER REVIEW REQUIRED**

This document is review material only. It does **not** authorise a change to `book_content.json`. Array indexes are zero-based indexes in the current reconstructed v2.4.5 RC lesson payload.

## u9l1 — Tamil duplication

### Current evidence

Tamil block **2** (`kind: table`) already contains the Indian case-study set: Bhopal gas disaster, Ganga Action Plan, Silent Valley, Chipko movement and Delhi–NCR air pollution.

Tamil block **4** (`kind: summary`) currently reads:

> பாடச்சுருக்கம்: ஒரு நிகழ்வாய்வின் நோக்கம் நிகழ்வை மட்டும் நினைவில் வைத்துக்கொள்வது அல்ல; அதன் காரணங்கள், தாக்கங்கள், சம்பந்தப்பட்ட தரப்புகள், மேற்கொள்ளப்பட்ட நடவடிக்கைகள் மற்றும் அதிலிருந்து பெறப்படும் பாடங்களைப் பகுப்பாய்வு செய்வதாகும்.

Tamil block **6** (`kind: supplemental`) currently reads:

> **கற்றலுக்கு பயன்படும் இந்திய சுற்றுச்சூழல் வழக்குகள்**  
> போபால் வாயுப் பேரிடர் (Bhopal gas disaster) — 2–3 டிசம்பர் 1984: தொழிற்சாலை பாதுகாப்பு, மெத்தில் ஐசோசயனேட் (methyl isocyanate) வெளிப்பாடு, அவசரநிலைத் தயார்நிலை மற்றும் சுற்றுச்சூழல் சுகாதாரம். கங்கை செயல் திட்டம் (Ganga Action Plan) — 1985: ஆற்றுமாசு கட்டுப்பாடு, கழிவுநீர் சிகிச்சை மற்றும் நிறுவன மேலாண்மைச் சவால்கள். சைலன்ட் வேலி (Silent Valley) — 1970கள்–1980கள்: கேரளாவின் வெப்பமண்டல எப்போதும் பசுமையான காடு மற்றும் முன்மொழியப்பட்ட நீர்மின் திட்டத்தைச் சுற்றிய பாதுகாப்புப் போராட்டம். சிப்கோ இயக்கம் (Chipko movement) — 1970கள்: இமயமலைப் பகுதிகளில் சமூக அடிப்படையிலான காடு பாதுகாப்பு இயக்கம்.

Tamil block **7** (`kind: summary`) currently reads:

> முக்கியக் கருத்து: நிகழ்வாய்வுகள் சுற்றுச்சூழல் கருத்துக்களை உண்மையான முடிவுகளுடன் இணைக்கின்றன.

Block 7 should be retained because it is the direct Tamil counterpart of English block 3: “Remember: Case studies connect concepts with real decisions.”

### Proposed diff — USER REVIEW REQUIRED

```diff
u9l1.tamil  # current/original indexes

[0] key_terms      — keep
[1] explanation    — keep
[2] table          — keep
[3] think_apply    — keep
-[4] summary        — DELETE entire current block
[5] depth          — keep
-[6] supplemental   — DELETE entire current block
[7] summary        — keep
```

**Proposed result:** remove blocks 4 and 6 only. Do not rewrite the remaining Tamil blocks.

**Reason:** block 4 repeats the analytical framework already stated in block 1; block 6 repeats the case-study material already preserved more completely in block 2. Block 7 carries a valid English–Tamil summary counterpart and must remain.

---

## u1l4 — missing SDG framework and harm-shifting statement

### Block 0 — key terms

**Current Tamil block 0**

> முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · சுற்றுச்சூழல் அறநெறி

**Proposed Tamil block 0 — USER REVIEW REQUIRED**

> முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) · சுற்றுச்சூழல் அறநெறி

```diff
u1l4.tamil[0]
- முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · சுற்றுச்சூழல் அறநெறி
+ முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) · சுற்றுச்சூழல் அறநெறி
```

### Block 1 — explanation

**Current Tamil block 1**

> தற்போதைய தலைமுறையின் தேவைகளை நிறைவேற்றும் போது எதிர்கால தலைமுறைகளின் தேவைகளைப் பூர்த்தி செய்யும் திறனை பாதிக்காத வளர்ச்சியே நிலைத்த வளர்ச்சி. சுற்றுச்சூழல் அறநெறி மனிதர்கள், பிற உயிரினங்கள், இயற்கை வளங்கள் மற்றும் எதிர்கால தலைமுறைகள் குறித்த நமது பொறுப்புகளை ஆராய்கிறது. சுற்றுச்சூழல் பாதுகாப்பு, சமூக நீதி மற்றும் பொருளாதார நலன் ஆகியவற்றை ஒருங்கிணைத்துப் பார்ப்பது அவசியம்.

**Proposed Tamil block 1 — USER REVIEW REQUIRED**

> தற்போதைய தலைமுறையின் தேவைகளை நிறைவேற்றும் போது எதிர்கால தலைமுறைகளின் தேவைகளைப் பூர்த்தி செய்யும் திறனை பாதிக்காத வளர்ச்சியே நிலைத்த வளர்ச்சி. சுற்றுச்சூழல் அறநெறி மனிதர்கள், பிற உயிரினங்கள், இயற்கை வளங்கள் மற்றும் எதிர்கால தலைமுறைகள் குறித்த நமது பொறுப்புகளை ஆராய்கிறது. சுற்றுச்சூழல் பாதுகாப்பு, சமூக நீதி மற்றும் பொருளாதார நலன் ஆகியவற்றை ஒருங்கிணைத்துப் பார்ப்பது அவசியம். **நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு ஆகியவற்றை ஒருங்கிணைக்கும் உலகளாவிய கட்டமைப்பை வழங்குகின்றன.**

```diff
u1l4.tamil[1]
  தற்போதைய தலைமுறையின் தேவைகளை நிறைவேற்றும் போது ... ஒருங்கிணைத்துப் பார்ப்பது அவசியம்.
+ நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு ஆகியவற்றை ஒருங்கிணைக்கும் உலகளாவிய கட்டமைப்பை வழங்குகின்றன.
```

### New paragraph immediately after current block 1

**Current text:** no Tamil counterpart exists for English block 2's statement that merely transferring environmental harm between communities, places or generations is not a complete solution.

**Proposed new `kind: p` block — USER REVIEW REQUIRED**

> சுற்றுச்சூழல் பாதிப்பை ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது இன்றைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ வெறுமனே மாற்றிவிடும் தீர்வு முழுமையான நிலைத்த தீர்வாகாது.

```diff
u1l4.tamil
@@ immediately after current block 1
+ {
+   "kind": "p",
+   "text": "சுற்றுச்சூழல் பாதிப்பை ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது இன்றைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ வெறுமனே மாற்றிவிடும் தீர்வு முழுமையான நிலைத்த தீர்வாகாது."
+ }
```

## Approval gate

No content change is authorised yet.

After user approval or amendment, the permitted sequence is:

1. Apply only the approved u9l1/u1l4 changes in a **separate content commit**.
2. Re-run Tamil coherence checks.
3. Re-run EN–TA lesson-content parity.
4. Verify that English content, quizzes, figures, UI, navigation, package/version identity and signing configuration are unchanged.
5. Only then may Item 3 move from **OPEN** to **CLOSED**.

Until then:

**RELEASE-CANDIDATE**  
**NOT FINAL**
