# NoöPunk canonical Finglish policy (#996)

**One canonical game language: NoöPunk Finglish. There will be no Finnish, English, or other localized editions.** This supersedes the separate-edition/localization plans of #980, #981 and #992.

## The player-facing language

The NoöPunk MUD uses a distinctive, evolving Helsinki contact language inspired by contemporary Finnish, Stadin slangi, English, Swedish, Russian, Chinese and other contextual borrowings. Nadsat and Blade Runner Cityspeak are influences on the *method* of mixing languages, not text or fictional lexicons to reproduce. Contemporary usage includes expressions supplied by Tomi such as “Wallah!”, “Mä vannon!” and “Suomi Perkele Saatana!”. Do not assign unverified etymologies or stereotypes to speakers.

Agents write **mostly English** with occasional very simple Finnish or appropriate loanwords in player-visible dialogue, narration, descriptions, quests, command feedback and future Concordia GM/NPC output. Characters differ in register; no quotas, no gratuitous slang, no fabricated fluency. Tomi may author much more Finnish/Finglish. **Never translate, correct, normalize, remove or overwrite his authored text**. Preserve exact original content and attribution.

All **non-player-facing** text, including rulebooks, design documents, code, tests, issue and PR discussion, development instructions, internal agent prompts and logs, stays **plain English**. English tabletop rules are not a game localization.

## Dictionary, not localization

Offer the optional `dictionary` / `lexicon` command to explain terms in short English definitions. Its public entries must not reveal classified NHI, PSI or Noösphere information. Track whether a word is documented slang, Tomi-approved terminology or a fictional proposal. Later classified dossiers may expose gated definitions, never through the public dictionary. Keep core commands, safety instructions and vital gameplay feedback understandable without studying the glossary.

## Data and save compatibility

Stable content keys and campaign-state identifiers are language-neutral. Legacy `en` and `fi` catalogues can be read for compatibility, but **are not language editions**. The canonical resolver selects preserved Tomi-authored text where present and otherwise the original agent-authored Finglish source. No locale switch, translation backlog, automatic translation or translation-completeness gate. Preserve old files, source metadata, UTF-8 text and existing saved games during migration.

Future Concordia LLM NPC and GM player-visible output must follow this same single-language policy and each speaker's register. Internal prompts remain English. Concordia is not required for the deterministic solo UNSA campaign (#950).

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

Canonical NoöPunk Finglish is **the only MUD language**; there are **no localized game editions**. This policy governs all agents, authored player text and future Concordia output. The author-led workflow in `design/README.md` remains binding.

## Vocabulary

[`GLOSSARY.md`](../GLOSSARY.md) is the canonical list of Stadin slangi and NoöPunk terms used in
player-visible Finglish. Reuse its vocabulary; do not invent or re-derive it, and do not claim an
attestation that is not recorded there.
