# Indie Retro Visual Slice — issue #447

**Status:** runnable, **noncanonical** visual/UX prototype. Open `strategy_game/render/retro_1974.html` in a local browser. Offline; no dependencies or asset pipeline, data access, AI service, licensed music, or game mechanics. This is not a substitute for the future in-engine UI.

## Production direction

**Indie retro is the medium; psychedelic 1970s cinema and European SF comics are the art direction.** NoöPunk looks **made in 1974, not set in 1974**. Keep the original fictional future-history/canonical technology intact: a punch-card LLM is a retro illustration, not a change to network/compute capabilities.

- **Primary cinematic reference:** *Zardoz* (1974). Supporting period film: *A Clockwork Orange* (1971). *The Man Who Fell to Earth* (1976) is a later-adaptation visual reference.
- **Graphic design:** Mœbius's cosmic linework, architecture and silhouette language; *Valérian et Laureline*'s colorful inhabited alien worlds and detailed vehicles. Make **original** graphics, not copies.
- **Retro indie delivery:** original flat-color 2D illustrations and sprites, crisp dark strokes, paper/poster-inspired titles, stylized map views, dossier and event-card layouts, restrained pixel or dithering textures where legible. Support asset variants for UI scale, low hardware requirements and accessible contrast. Do not require photorealism, 3D environments or expensive animation.
- **Sound inspirations (not bundled audio):** Hawkwind / *Space Ritual* first, Neu!, Tangerine Dream / *Phaedra*, early Amon Düül II. Recordings require independent licenses; do not ship them by default.
- **Writing:** intelligent 1974-era political/social/technological futurology, flashes of psychedelia and irony, occasional technological misreadings and *rare* minor alternate-history slips. Later editorial notes label these as discrepancies rather than changing scenario facts.
- **Historical texture:** *Future Shock* (1970), *The Limits to Growth* (1972), Hynek's *The UFO Experience* (1972), 1974 Targ/Puthoff remote-viewing claims; Vallée's *The Invisible College* (1975) and the 1978 Marks/Kammann critique belong only in later marginalia or modern references. UFO/PSI reports are claims, not independently proven discoveries.

## Prototype

The one-file HTML mockup demonstrates four visual elements: an original geometric psychedelic poster, Tommy Pilgrim's archival voice, a punch-card-era **illustration** of an intelligent language interface, and a non-mechanical sample event card. Its two accessible view buttons contrast a 1974 prophetic text with a 2026 editorial correction. All scenario detail in the sample is **fictional placeholder copy**, not an established event.

**Accessibility:** headings, text, keyboard-operable native buttons, visible focus, responsive single-column layout, a skip link, text alternatives and reduced-motion accommodation. Avoid purely decorative color encoding of evidence strength or gameplay state in later UIs.

**Next asset milestones (not implemented here):** 2D sprite and portrait sheet; reusable readable card layout; physical/cyber/astral UI variants; Godot-compatible assets; optional original kosmische-style loops; art/editorial review before promotion of mock-up text into canon. This prototype imposes no visual framework on the existing renderer and never modifies strategy mechanics.

See [presentation spec](../../docs/design/ISSUE_447_PILGRIM_PRESENTATION_SPEC.md), [rulebook](../../RULEBOOK.md), and [issue #447](https://github.com/TomiToivio/NooPunk/issues/447).
