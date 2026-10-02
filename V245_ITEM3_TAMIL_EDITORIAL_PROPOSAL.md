# Environmental Studies v2.4.5 — Item 3 Tamil editorial proposal

Status: **PROPOSAL ONLY — NOT APPLIED**

This file records the exact proposed changes for the two student-facing Tamil content defects identified by the v2.4.5 audit. Array indexes below are **zero-based indexes within the lesson's current `tamil` block list**. No change to `book_content.json` is authorised by this proposal.

## u9l1 — duplicated Tamil case-study material

### Evidence from the reconstructed RC content

- Tamil block **2** (`kind: table`) already contains the Indian case-study set: Bhopal gas disaster, Ganga Action Plan, Silent Valley, Chipko movement and Delhi–NCR air pollution.
- Tamil block **6** (`kind: supplemental`) repeats four of those cases in prose: Bhopal, Ganga Action Plan, Silent Valley and Chipko.
- Tamil block **4** (`kind: summary`) repeats the analytical purpose already stated in Tamil block 1: causes, impacts, stakeholders, responses and lessons.
- Tamil block **7** (`kind: summary`) must be **retained**. It is the direct Tamil counterpart of English block 3, “Case studies connect concepts with real decisions.”
- Therefore deleting blocks 6 and 7, as an earlier draft proposed, would remove a valid EN–TA counterpart and create a new content-parity defect.

### Proposed deletion A — Tamil block 4

Delete Tamil block **4** in full:

> பாடச்சுருக்கம்: ஒரு நிகழ்வாய்வின் நோக்கம் நிகழ்வை மட்டும் நினைவில் வைத்துக்கொள்வது அல்ல; அதன் காரணங்கள், தாக்கங்கள், சம்பந்தப்பட்ட தரப்புகள், மேற்கொள்ளப்பட்ட நடவடிக்கைகள் மற்றும் அதிலிருந்து பெறப்படும் பாடங்களைப் பகுப்பாய்வு செய்வதாகும்.

**Reason:** the same analytical framework is already present in Tamil block 1, while Tamil block 7 is the correct counterpart to the English summary and should remain.

### Proposed deletion B — Tamil block 6

Delete Tamil block **6** in full:

> **கற்றலுக்கு பயன்படும் இந்திய சுற்றுச்சூழல் வழக்குகள்**  
> போபால் வாயுப் பேரிடர் (Bhopal gas disaster) — 2–3 டிசம்பர் 1984: தொழிற்சாலை பாதுகாப்பு, மெத்தில் ஐசோசயனேட் (methyl isocyanate) வெளிப்பாடு, அவசரநிலைத் தயார்நிலை மற்றும் சுற்றுச்சூழல் சுகாதாரம். கங்கை செயல் திட்டம் (Ganga Action Plan) — 1985: ஆற்றுமாசு கட்டுப்பாடு, கழிவுநீர் சிகிச்சை மற்றும் நிறுவன மேலாண்மைச் சவால்கள். சைலன்ட் வேலி (Silent Valley) — 1970கள்–1980கள்: கேரளாவின் வெப்பமண்டல எப்போதும் பசுமையான காடு மற்றும் முன்மொழியப்பட்ட நீர்மின் திட்டத்தைச் சுற்றிய பாதுகாப்புப் போராட்டம். சிப்கோ இயக்கம் (Chipko movement) — 1970கள்: இமயமலைப் பகுதிகளில் சமூக அடிப்படையிலான காடு பாதுகாப்பு இயக்கம்.

**Reason:** block 2 already preserves these case studies in a clearer, fuller table and additionally includes Delhi–NCR air pollution. The supplemental prose adds no unique scientific concept.

### Reviewable diff

```diff
 u9l1.tamil  # current/original indexes
@@
 [0] key_terms — keep unchanged
 [1] explanation — keep unchanged
 [2] table — keep unchanged
 [3] think_apply — keep unchanged
-[4] summary — DELETE entire block
 [5] depth — keep unchanged
-[6] supplemental — DELETE entire block
 [7] summary — KEEP; direct counterpart of English block 3
```

## u1l4 — Sustainable Development Goals and harm-shifting omissions

### Evidence from the reconstructed RC content

- English block **0** lists **SDGs** as a key term; Tamil block 0 does not.
- English block **1** explicitly states that the Sustainable Development Goals link poverty reduction, health, education, equality and environmental protection; Tamil block 1 has no counterpart.
- English block **2** states that a solution is incomplete when it merely shifts environmental harm between communities, places or generations; the Tamil lesson has no direct counterpart.

### Proposed addition A — Tamil block 0 key term

Change Tamil block **0** from:

> முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · சுற்றுச்சூழல் அறநெறி

to:

> முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) · சுற்றுச்சூழல் அறநெறி

### Proposed addition B — append to Tamil block 1

Append this sentence to Tamil block **1** (`kind: explanation`):

> **நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு ஆகியவற்றை ஒருங்கிணைக்கும் உலகளாவிய கட்டமைப்பை வழங்குகின்றன.**

This is a closer and more natural college-level Tamil rendering of the English “global framework” sentence than the earlier draft phrase “உலகளாவிய செயல் வடிவம்”.

### Proposed addition C — new Tamil paragraph after block 1

Insert a new `kind: p` block immediately after current Tamil block **1**:

> **சுற்றுச்சூழல் பாதிப்பை ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது இன்றைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ வெறுமனே மாற்றிவிடும் தீர்வு முழுமையான நிலைத்த தீர்வாகாது.**

### Reviewable diff

```diff
 u1l4.tamil
@@ block 0: key_terms
- முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · சுற்றுச்சூழல் அறநெறி
+ முக்கியக் கலைச்சொற்கள்: நிலைத்த வளர்ச்சி · தலைமுறைகளுக்கிடையேயான சமநீதி · நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) · சுற்றுச்சூழல் அறநெறி

@@ block 1: explanation
  ... சுற்றுச்சூழல் பாதுகாப்பு, சமூக நீதி மற்றும் பொருளாதார நலன் ஆகியவற்றை ஒருங்கிணைத்துப் பார்ப்பது அவசியம்.
+ நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு ஆகியவற்றை ஒருங்கிணைக்கும் உலகளாவிய கட்டமைப்பை வழங்குகின்றன.

+ new kind:p block immediately after current block 1:
+ சுற்றுச்சூழல் பாதிப்பை ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது இன்றைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ வெறுமனே மாற்றிவிடும் தீர்வு முழுமையான நிலைத்த தீர்வாகாது.
```

## Post-approval application gate

If this proposal is approved or amended:

1. Apply only these approved changes to `book_content.json` in a **separate content commit**.
2. Re-run the Tamil coherence audit.
3. Re-run EN–TA lesson-content parity checks.
4. Confirm no unrelated English, quiz, figure, navigation, package, signing or release configuration changed.
5. Only then may Item 3 move from **OPEN** to **CLOSED**.

Until that separate content commit passes its checks, v2.4.5 remains:

**RELEASE-CANDIDATE**  
**NOT FINAL**
