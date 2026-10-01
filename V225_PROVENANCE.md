# Environmental Studies v2.2.5 — Lesson Navigation UX Provenance

## Baseline
- Branch: `correction/v2.2.4-tamil-naturalisation-20261001`
- Successful baseline HEAD: `27e6035bbdb3611d7dfd6a07042e6e89ad1408ed`
- Successful v2.2.4 CI run: `36822489640`
- Authoritative book SHA-256: `1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40`

## Feature branch
`feature/v2.2.5-lesson-navigation-20261001`

## Scope
Navigation/UI only. No lesson text, Tamil terminology, English content, figures, scientific assets, permissions, privacy behaviour or application architecture may change.

## Required behaviour
- Home and Unit Contents are distinct destinations.
- Home always opens the application dashboard.
- Unit opens the current unit's contents page.
- Previous and Next switch lessons without constructing a lesson-by-lesson back history.
- Android Back from a lesson returns to the current unit page.
- Print and Save PDF remain available but are secondary actions under the lesson More menu.
- Wide-layout lesson side navigation remains unchanged.

## Version
- versionName: **2.2.5**
- versionCode: **20205**

## Release gate
STATIC NAVIGATION ASSERTIONS → LINT/TEST/BUILD → APK IDENTITY/OFFLINE CHECK → PHYSICAL-DEVICE NAVIGATION QA → CONTENT FREEZE.
