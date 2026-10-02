# Environmental Studies v2.4.5 — Item 3 Tamil editorial proposal

Status: **PROPOSAL ONLY — NOT APPLIED**

This file records the exact proposed changes for the two student-facing Tamil content defects identified by the v2.4.5 audit. Array indexes below are **zero-based indexes within the lesson's `tamil` block list**. No change to `book_content.json` is authorised by this proposal.

## u9l1 — duplicated Tamil case-study material

### Evidence

- Tamil block **2** (`kind: table`) already contains the Indian case-study set: Bhopal gas disaster, Ganga Action Plan, Silent Valley, Chipko movement and Delhi–NCR air pollution.
- Tamil block **6** (`kind: supplemental`) repeats four of those cases in prose: Bhopal, Ganga Action Plan, Silent Valley and Chipko.
- Tamil block **4** (`kind: summary`) states that the purpose of a case study is to analyse causes, impacts, stakeholders, responses and lessons.
- Tamil block **7** (`kind: summary`) repeats the same core conclusion in shorter form.

### Proposed deletion

Delete Tamil block **6** in full:

> **கற்றலுக்கு பயன்படும் இந்திய சுற்றுச்சூழல் வழக்குகள்**  
> போபால் வாயுப் பேரிடர் (Bhopal gas disaster) — 2–3 டிசம்பர் 1984: தொழிற்சாலை பாதுகாப்பு, மெத்தில் ஐசோசயனேட் (methyl isocyanate) வெளிப்பாடு, அவசரநிலைத் தயார்நிலை மற்றும் சுற்றுச்சூழல் சுகாதாரம். கங்கை செயல் திட்டம் (Ganga Action Plan) — 1985: ஆற்றுமாசு கட்டுப்பாடு, கழிவுநீர் சிகிச்சை மற்றும் நிறுவன மேலாண்மைச் சவால்கள். சைலன்ட் வேலி (Silent Valley) — 1970கள்–1980கள்: கேரளாவின் வெப்பமண்டல எப்போதும் பசுமையான காடு மற்றும் முன்மொழியப்பட்ட நீர்மின் திட்டத்தைச் சுற்றிய பாதுகாப்புப் போராட்டம். சிப்கோ இயக்கம் (Chipko movement) — 1970கள்: இமயமலைப் பகுதிகளில் சமூக அடிப்படையிலான காடு பாதுகாப்பு இயக்கம்.

Delete Tamil block **7** in full:

> முக்கியக் கருத்து: நிகழ்வாய்வுகள் சுற்றுச்சூழல் கருத்துக்களை உண்மையான முடிவுகளுடன் இணைக்கின்றன.

**Reason:** block 2 already preserves the case-study content in a clearer tabular form, and block 4 already provides the more complete summary. These two deletions remove repetition without deleting a unique scientific concept.

### Reviewable diff

```diff
 u9l1.tamil
@@
 [2] table — keep unchanged
 [3] think_apply — keep unchanged
 [4] summary — keep unchanged
 [5] depth — keep unchanged
-[6] supplemental — DELETE entire block
-[7] summary — DELETE entire block
```

## u1l4 — two concepts omitted from Tamil

### Omission A — Sustainable Development Goals framework

English block 1 contains:

> The Sustainable Development Goals provide a global framework linking poverty reduction, health, education, equality and environmental protection.

Proposed Tamil sentence to append to Tamil block **1** (`kind: explanation`):

> **நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பை ஒன்றோடொன்று தொடர்புடைய உலகளாவிய செயல் வடிவமாக இணைக்கின்றன.**

### Omission B — shifting environmental harm is not a complete solution

English block 2 states that a solution is incomplete when it merely transfers environmental harm between communities, places or generations.

Proposed new Tamil paragraph immediately after Tamil block **1**:

> **ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது தற்போதைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ சுற்றுச்சூழல் பாதிப்பை மாற்றிப் போடுகின்ற தீர்வு முழுமையான நிலைத்த தீர்வாகாது.**

### Reviewable diff

```diff
 u1l4.tamil
@@ block 1: explanation
  ... சுற்றுச்சூழல் பாதுகாப்பு, சமூக நீதி மற்றும் பொருளாதார நலன் ஆகியவற்றை ஒருங்கிணைத்துப் பார்ப்பது அவசியம்.
+ நிலைத்த வளர்ச்சி இலக்குகள் (SDGs) வறுமை ஒழிப்பு, சுகாதாரம், கல்வி, சமத்துவம் மற்றும் சுற்றுச்சூழல் பாதுகாப்பை ஒன்றோடொன்று தொடர்புடைய உலகளாவிய செயல் வடிவமாக இணைக்கின்றன.

+ new paragraph after block 1:
+ ஒரு சமூகத்திலிருந்து மற்றொரு சமூகத்திற்கோ, ஒரு இடத்திலிருந்து மற்றொரு இடத்திற்கோ, அல்லது தற்போதைய தலைமுறையிலிருந்து எதிர்கால தலைமுறைக்கோ சுற்றுச்சூழல் பாதிப்பை மாற்றிப் போடுகின்ற தீர்வு முழுமையான நிலைத்த தீர்வாகாது.
```

## Decision required

- **u9l1:** approve / revise / reject the two deletions.
- **u1l4:** approve / revise / reject each proposed Tamil addition.

Until approved and applied, Item 3 remains **OPEN** and v2.4.5 must remain **RELEASE-CANDIDATE**, not FINAL.
