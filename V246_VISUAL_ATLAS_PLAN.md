# Environmental Studies v2.4.6 — Concept Visual Atlas Phase 1

## Scope
This phase enriches the validated 46-lesson bilingual academic corpus without changing lesson prose, quizzes, package identity, signing, navigation, or existing scientific figures.

## Visual policy
- Scientific mechanism/process explanation: vector SVG diagrams.
- Real-world observation/context: authentic openly licensed educational photographs.
- Visual mix is diagram-led; photographs are used only where real-world observation/context adds instructional value.
- All visual resources are bundled for offline use; there is no runtime network dependency.

## Phase-1 additions
- 46/46 lessons receive at least one new visual.
- 112 new bilingual SVG resources (56 English + 56 Tamil).
- 8 authentic photograph resources shared by the English and Tamil lesson blocks.
- 64 new visual blocks per language.
- Food chains/webs/pyramids, biogeochemical cycles, and water pollution/eutrophication receive multiple specialised diagrams.
- Additional photographs cover pond ecology, Western Ghats biodiversity, Muthupet mangroves, smog, algal bloom/eutrophication, waste segregation, wind energy, and rainwater harvesting.

## Scientific design rules
- Food-chain arrows represent energy/food transfer from resource/prey to consumer.
- Food-web connections avoid decorative arrows and show multiple feeding pathways.
- Pyramid of numbers and biomass are explicitly shown as potentially non-upright; energy pyramid is always upright.
- Eutrophication is shown as nutrient enrichment → algal bloom → reduced light → death/decomposition → oxygen depletion → faunal stress.
- Real photographs are instructional evidence/examples, not decorative backgrounds.

## Accessibility and mobile rules
- 1200×720 SVG viewBox with mobile-readable labels.
- Tamil titles may wrap to three lines; Tamil labels use the bundled Noto Sans Tamil path at runtime.
- Tap-to-enlarge behavior continues through the existing figure viewer.
- Photographs are resized and WebP-compressed during CI to limit APK growth.
- Captions include source/author/licence attribution.

## Release gates
1. Academic corpus input SHA must equal the validated v2.4.6 academic content SHA.
2. All 112 generated SVGs must be well-formed XML.
3. Source-level SVG layout audit must report no text overflow.
4. Exactly 8 manifest photographs must be fetched and converted to valid WebP.
5. Every photograph fetch records the observed transport SHA-256 and the packaged WebP SHA-256. Because Wikimedia thumbnail transport bytes can vary while decoding to the same image, the deterministic packaged WebP SHA-256 is pinned and enforced in the manifest.
6. Release APK/AAB resource integrity must derive expected figure counts from packaged `book_content.json` rather than the old fixed v2.4.5 count.
7. The frozen v2.4.5 AndroidSVG gate remains exactly 46 legacy Tamil plates (`*_ta`); new v2.4.6 SVGs use `_e`/`_t` suffixes and are rendered by a separate 56-plate Tamil atlas gate.
8. Production package identity/signing remain untouched.

## Baseline
Validated academic content SHA-256:
`e0d152e9c51be5bb095ba11c8fdc171467eb594ec75fe17158a9bada0a8ea8d4`
