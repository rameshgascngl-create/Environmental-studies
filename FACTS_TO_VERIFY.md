# Environmental Studies v2.4.0 — Facts to Verify

This file records external facts introduced or relied upon during the v2.4.0 hardening work. It is not a source of new Environmental Studies lesson claims.

## C3 — bundled Tamil font

- **Noto Sans Tamil source:** Google Fonts repository, `ofl/notosanstamil/NotoSansTamil[wdth,wght].ttf`.
  - Upstream Git blob: `cb08d499b2d05ef6fd8e470c36c2be47ff368f0d`.
  - Google Fonts metadata identifies the family as **Noto Sans Tamil**, designer **Google**, licence **OFL**, and lists Tamil plus Latin/Latin-ext subsets.
  - Metadata source: `google/fonts/ofl/notosanstamil/METADATA.pb`.
- **Font licence:** SIL Open Font License 1.1 from `google/fonts/ofl/notosanstamil/OFL.txt`.
  - Upstream Git blob: `677d559b94ba7c63d41a7bf6ffa0a3eb11f2de95`.
- **AndroidSVG resolver API:** the repository commit `9b908a107286ef328f30cc3ea0155d808d904a6e` (“Updated version number to 1.4”) exposes `SVGExternalFileResolver.resolveFont(String, int, String)`; AndroidSVG documents `SVG.registerExternalFileResolver(...)` for external font resolution.

No lesson scientific statement is changed by Task C3.
