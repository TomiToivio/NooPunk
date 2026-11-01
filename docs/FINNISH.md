# NoöPunk MUD Finglish and narrative policy (#992; updates #980/#981)

> **Binding boundary:** Player-visible NoöPunk MUD text is primarily **English with occasional simple, contextual Finnish and other loanwords**: our distinctive Finglish. Everything else written by agents is **plain English**. **Never translate, correct, overwrite, or imitate Tomi-authored Finnish/Finglish passages.**

## Where the policy applies

| Surface | Agent language |
| --- | --- |
| Text directly shown to the MUD player: UI, dialogue, descriptions, quests, in-world messages, narrative | **English-dominant Finglish**. Mostly English, occasionally short and basic Finnish expressions and suitable Swedish, Russian, Chinese or other borrowings. |
| Future Concordia LLM GM and NPC responses **shown to the player** | Same **English-dominant Finglish** rule, tuned to the speaker and situation. |
| Design documents, issues, PRs, tabletop rules, agent instructions, internal LLM prompts, code, comments, tests, technical documents and other non-player-visible content | **Plain English**. Do not insert multilingual stylistic flourishes. |
| Tomi-authored dialogue, descriptions, or UI text already present in the game | **Preserve verbatim**, including Finnish, English, slang, punctuation and code-switching. No automatic translation or rewriting. |

**This is a player-visibility boundary, not an author-identity boundary.** Agents may write *limited* Finnish within otherwise English player-visible prose; they must **not** try to produce fluent Finnish, counterfeit Tomi's Helsinki voice, or automatically translate his copy. When uncertain, default to natural English. Do not impose a percentage, require a non-English word in every message, or make informational UI unclear.

## Voice and vocabulary

- The intended agent voice is a foreigner who knows just a little simple, sometimes imperfect Finnish: brief greetings, interjections and commonplace phrases rather than long Finnish sentences. Do not manufacture errors mechanically.
- Occasionally reuse **Tomi-authored/approved** Stadin slangi and Finglish vocabulary in character-appropriate contexts. Consult [the glossary](world/HELSINKI_SLANG_GLOSSARY.md) and relevant Tomi-authored design/game text before using it; do not silently promote unverified vocabulary into canon.
- Russian- and Chinese-influenced borrowings, Swedish and other languages are welcome when justified by a character, place, or situation. This is **Nadsat-inspired linguistic texture**, not permission to reproduce distinctive invented Nadsat words, passages or dialogue from *A Clockwork Orange*.
- Register matters: Romppainen, UNSA personnel, Helsinki locals, international agents, NHI-facing specialists, and corporate NPCs need not code-switch in identical ways. Keep text comprehensible and avoid exoticizing speakers.
- Bureaucratic institutional double-speak can influence style without reproducing another author's prose.
- A substantial percentage of the **overall game** can still be original Finnish written by Tomi. No translation-completeness threshold blocks release.

## Authoring, provenance and runtime

1. Tomi owns his own authored text. Reproduce it faithfully when implementing a design document: do not translate, fix, polish, modify or overwrite Finnish/Finglish. Changes require his explicit authorization.
2. Agents author new player-facing MUD strings in **English-dominant Finglish**, preserving stable, locale-neutral IDs and attribution/source metadata. Agent-originated English-dominant Finglish is **not** a Finnish translation and should not be misrepresented as Tomi-authored `fi` content.
3. Existing `mud/nopunk_mud/i18n.py` locale machinery can use an English-source field containing occasional loanwords; preserve the separately authored Finnish field, and any fallback markers or language metadata. Do not circumvent provenance checks by mislabeling agent content as Tomi's.
4. The finished MUD may intentionally contain mixed Tomi-Finnish and agent-Finglish; this is a feature, not a localization defect. A polished English-only edition is a separate later milestone.
5. **Future Concordia LLM GM/NPC implementation:** include these instructions in the runtime *player-facing output contract* and test sample outputs. Internal prompts, reasoning summaries, JSON state, mechanics and logs remain English. Keep the first deterministic UNSA single-player campaign usable without Concordia/LLM GM (#950).
6. Keep quest state, game identifiers and save formats language-neutral. Test fallback, UTF-8 round-tripping and preservation of Tomi's authored material when localization machinery changes.

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

The Finglish exception applies **only to text shown to the MUD player**, including future Concordia GM/NPC output. Documentation, rules, design documents, and all internal agent/code text remain plain English. This policy supersedes the old absolute English-only language restriction in #980/#981 while retaining the protection for Tomi-authored text.
