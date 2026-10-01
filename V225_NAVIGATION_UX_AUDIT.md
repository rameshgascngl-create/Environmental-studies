# Environmental Studies v2.2.5 — Lesson Navigation UX Audit

The v2.2.4 reader already used a single route value rather than a true lesson stack, so Previous/Next did not technically create one history entry per lesson. The usability problem was that lesson pages hid the main bottom navigation and exposed only a generic Back action; returning to Home therefore required retreating through higher-level screens.

v2.2.5 corrects the user-facing navigation model rather than introducing another back stack.

## Implemented
- **Home** is directly available while reading a lesson and always targets the dashboard.
- **Unit** targets the current unit's contents page, not the global units list.
- **Previous / Next** remain direct lesson replacement routes.
- A persistent mobile lesson navigation bar provides Previous · Unit · Home · Next.
- Android Back from a lesson resolves to the current unit contents.
- Wide screens retain the existing 300 dp lesson side list; the redundant persistent lesson bar is suppressed there.
- Print and Save PDF remain functional but move from a prominent two-button footer to the lesson-level More menu.

## Frozen content
The exact v2.2.4 `book_content.json` SHA-256 must remain:
`1bf866f457cdb7c2590469b32d692f56b5000a58ff76eba1604b0ad158962f40`

No English, Tamil, figure routing or scientific visual content is authorised to change.

## Device-QA checks
1. Read Lesson 1 → Next → Next; Home must reach the dashboard in one tap.
2. From any lesson, Unit must open that same unit's lesson list in one tap.
3. System Back from any lesson must open the current unit contents, never the previous lesson.
4. Previous and Next must change lessons and restore each lesson's saved scroll position.
5. First lesson disables Previous; final lesson disables Next.
6. Print and Save PDF must work from More.
7. Portrait, landscape and large-text modes must not clip the four lesson navigation items.
8. Wide/tablet layout must keep the side lesson list and must not duplicate the bottom lesson navigation bar.
