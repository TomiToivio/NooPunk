# Issue #447: visual prototype and editorial acceptance refresh (2026-10-15)

## What ships

Open [the standalone HTML prototype](./ISSUE_447_RETRO_UI_PROTOTYPE.html) in a browser. It contains a responsive, keyboard-operable mock interface for a punch-card/teletype **LLM scene**, an illustrated **Event Card**, the explicit observed/hypothesis/prophecy legend, and paired Pilgrim-versus-editorial text. One button cycles through three illustrative AI responses. No external assets, scripts, licensed music, source artwork, backend, or game data are loaded.

The punch-card machine is **representation, not simulation fact**. The Event Card is a **visual sample, not an authored card/deck or gameplay rule**. The short faux-period prose is an **editorial example**, not the author's reserved Tommy Pilgrim introduction.

## Lightweight art bible / implementation tokens

- **Look:** *made in the seventies, not set in the seventies*. Psychedelic period SF film, indie 2D comics/illustration and deliberately theatrical props. Retain *Zardoz* as film #1; Philip K. Dick as literature #1; Hawkwind *Space Ritual* as soundtrack #1. Mœbius and Christin/Mézières' *Valérian et Laureline* inform graphic grammar, not copied artworks.
- **Palette (prototype values, not immutable canon):** night plum `#201d31`, panel violet `#302b43`, paper cream `#f9e9bd`, amber `#f6a55b`, mint `#9dd9bc`, cosmic violet `#b29be7`. Dark paper-ink purple `#2a2536` on parchment `#f5dfab`.
- **Type:** system sans for operational UI, Georgia/serif for pulp headers, system monospace for the teletype. No font bundles or paid dependencies.
- **Illustration:** original 2D silhouettes, simple forms, inking, cardstock edges, printed-paper overlays. Use no copied panels or proprietary film/album images.
- **Information hierarchy:** readable heading → verifiable data → clear evidence status → fictional apparatus. Reality/proposal/prophecy labels must be textual, not color-only.
- **Accessibility:** layouts down to narrow screens; semantic sections; focus-visible button; status announcements; no flashing/scroll animation; reduced-motion override. Check screen-reader/contrast behavior manually before shipping a production UI.
- **Sound:** *Space Ritual*, Neu!, early Amon Düül II and *Phaedra* are aesthetic references; no recordings are included or assumed licensed.
- **Scope guardrail:** no new gameplay statistics, NHI or PSI truths, political facts, timeline changes, or replacement of either the legacy/crossover rulebook.

## Audit of the expanded issue

The pre-expansion criteria remain documented in [ISSUE_447_ACCEPTANCE.md](./ISSUE_447_ACCEPTANCE.md), alongside the authored rulebook introduction and deferred Event Card mechanic details. The later issue-body expansion adds a seventies-film framing, Mœbius/Valérian, production graphics, 1970s writing/technology and source chronology. These are present in [ISSUE_447_PILGRIM_PRESENTATION_SPEC.md](./ISSUE_447_PILGRIM_PRESENTATION_SPEC.md), notably sections 1–3, 5–7 and 10. This change closes the previously *unbuilt* visual-prototype deliverable.

**Editorial reservations:** The author still writes Tommy Pilgrim's actual prologue; the standalone prototype needs author/art review before adoption in a game; any real game UI integration and art assets are future implementation tasks. The choice of eventual rulebook owner for the introductory framing and Event Cards, and whether *The Iron Dream* joins the locked in-universe influence hierarchy, remain author decisions. **Do not describe these as decided.** The Event Cards' mechanical design remains explicitly deferred.

## Verification

Static/manual code review: standalone HTML has no remote dependencies and script updates only terminal text on an explicit button click. No engine/game source, authored canon, scenario, rulebook rules, or compiled assets are touched. This document is an editorial acceptance note, **not an automated lore test**.