# Environmental Studies v2.3.0 — Visual, Continue & Narrated Animation Provenance

## Baseline
- Repository: `rameshgascngl-create/Environmental-studies`
- Validated branch: `feature/v2.2.5-lesson-navigation-20261001`
- Baseline HEAD: `7fbdf3b80250649b4c3776bee12e1771d0ae4fb5`
- v2.2.5 CI run: `36827856713`
- Frozen lesson payload SHA-256: `1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40`

## Feature branch
`feature/v2.3.0-visual-audio-learning-20261001`

## Version
- versionName: **2.3.0**
- versionCode: **20300**

## Controlled upgrade
This phase changes learning UX and visual/animation source only:
- per-unit last-read lesson persistence and Continue / தொடர்க markers;
- richer environmental context artwork on unit cards and unit openings;
- six additional animated environmental-process pages;
- audio explanation using Android TextToSpeech in both English and Tamil;
- climate animation audio controls.

The 46-lesson English/Tamil content payload, figure routing, scientific SVGs, privacy behaviour and offline application contract remain frozen.

## Visual policy
Labelled scientific diagrams remain schematic where diagrammatic clarity is pedagogically superior. Realism is added as contextual scene art and richer animated process rendering rather than by converting every scientific figure into a decorative photograph.

## Audio policy
Narration uses Android platform TTS and requires no INTERNET permission. English/Tamil voice availability depends on the device's installed TTS language data.

## Gate
STATIC SOURCE AUDIT → LINT/TEST/BUILD → APK/OFFLINE CONTRACT → PHYSICAL DEVICE VISUAL/AUDIO QA → FREEZE.
