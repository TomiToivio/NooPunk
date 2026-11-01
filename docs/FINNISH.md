# NoöPunk MUD language and narrative policy (issues #980 and #981)

> **Binding rule for every AI agent:** Tomi writes Finnish. Agents write English only. Never generate, translate into, correct, or improvise Finnish player-facing prose. Do not overwrite Tomi's authored Finnish. This rule applies to the MUD, not the English tabletop rulebook or general repository documentation.

## Language of the first release

The **official primary language is Finnish, including natural Finglish**. The first playable release is allowed, and expected, to be **mixed-language**: for example 50% Tomi-authored Finnish and 50% agent-authored English. There is **no minimum translated percentage**, purity requirement, or release gate demanding fully Finnish text. Do not characterize English lines in the Finnish-first build as defects.

**Tomi is the only author/editor of the Finnish dialogue and story.** Agents author new UI, dialogue, quest and narrative drafts **in English only**. Tomi may eventually rewrite these in his own Finnish. The later polished **English localization is a separate milestone**; agent drafts are not automatically approved English translations. English remains the language of code, commit messages, issues, documentation, and tabletop rulebooks.

Avoid an ambiguous instruction to "translate to English first": agents already write the draft in English, and Tomi adapts it into Finnish when he chooses. Do not automatically translate existing Finnish into English either.

### Required content workflow

1. Agents create an **English draft** with a stable, locale-neutral content ID and intent/context/voice metadata. Do not invent Finnish text.
2. The Finnish-primary client can display a **Tomi-authored Finnish line** where one exists, otherwise the original **English draft**. Mixed-language scenes and screens are allowed, even at 50/50.
3. Track provenance and status, for example `author: "agent"`, `source_lang: "en"`, `status: "awaiting_tomi"`; or `author: "Tomi"`, `source_lang: "fi"`, `status: "approved"`. Never write an English fallback into a Finnish field or delete Finnish when changing a draft.
4. Tomi writes or revises authentic Finnish in his own voice. AI agents must not perform this step or edit those lines without an explicit narrow instruction from Tomi that overrides this repository workflow.
5. Eventually a human-reviewed English edition may be maintained independently. **Do not block the MUD MVP on it.**

Keep quest states, IDs and saves independent of language; test deterministic fallback, UTF-8, preservation of authored content, and save compatibility. An agent may **quote existing approved terms as data** (for example proper names), but must not compose Finnish sentences, example dialogue, or localized strings.

### Voice and glossary

Tomi's voice is conversational Helsinki **Stadin slangi + Finglish**, with Russian loanwords, and retrofuturist inspiration from Nadsat and bureaucratic Doublespeak. A substantial portion of speech can be English. No percentages are imposed, and agents must not counterfeit a Finnish sociolect. Preserve variation by setting and NPC: street, university, UNSA bureaucracy, security, corporate, online, and the Noösphere. Avoid copying distinctive passages or invented phrasing from other authors.

The shared glossary is [HELSINKI_SLANG_GLOSSARY.md](world/HELSINKI_SLANG_GLOSSARY.md). Agents contribute **English definitions and context only**; Finnish usage examples, inflections, original neologisms and creative wording are reserved for Tomi. Established genre vocabulary (such as *cyberspace*) may be used normally.

## Narrative revelation: grounded Helsinki first

Initially sell an intelligible **Nordic/European cyberpunk police investigation**, not a cosmic encyclopedia. The new UNSA rookie is a moral blank slate. Start with familiar crimes, cyberware, AI slop, AR/VR and bureaucracy; introduce strange evidence ambiguously and reveal **NHI/PSI, the emerging conscious Noösphere, and the ontological crisis** in stages through clues, decisions, and consequences. Keep author-only truth and UNSA classified files separate from the player's knowledge. Romppainen knows more than he tells rookies, and even UNSA does not know everything.

Worldbuilding heuristic, **not deterministic NPC assignment**: ~50% deny or normalize the paradigm shift, ~25% turn doomer/bioconservative, ~25% accelerationist. The denial sustains day-to-day society and its *Don't Look Up* satirical mood. Ubiquitous AI and AR/VR make undeniable anomalies dismissible as slop or misinformation.

The Noösphere initially appears technological, though consciousness, psychic experience and ideological struggle ultimately complicate that account. UNSA sincerely values transparency, open science and citizen participation yet classifies destabilizing discoveries for fear of public panic. It fears becoming an MJ-12 analogue while gradually assuming global-government functions. Treat this as a tension, not a simplistic good/evil reveal.

Do not force a moral alignment: let the player develop heroic, compassionate, cynical, compromised, corrupt, traitorous, or self-destructive tendencies through choices and sustained consequences.

### Spoiler discipline

- **Opening:** grounded Helsinki casework; anomalies have mundane explanations available.
- **Investigative escalation:** contradictory records, suspicious AR/AI phenomena, partial classified disclosures.
- **Later:** PSI/NHI evidence and the Noösphere become increasingly difficult to explain away.
- **Late revelations:** the full ontological stakes and geopolitical/NHI background, when earned by play.

Use explicit knowledge gates in scene data and avoid spoilers from UI, achievements, logs, or narration.

## Scope

These directives apply to **MUD player-facing UI, story and dialogue only**. Leave tabletop rulebooks and all other documentation **in English**. This document is written in English on purpose: agents must be able to follow it. Both #980 and #981 are a **single consolidated workstream**, not competing language specifications.
