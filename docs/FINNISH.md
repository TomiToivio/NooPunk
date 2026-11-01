# NoöPunk Finglish and narrative policy (#996; supersedes the localization plans of #992, #980, #981)

> **Binding decision:** the NoöPunk MUD ships in **one canonical language — NoöPunk Finglish — and there will
> be no localizations.** Not Finnish, not English, not any other language. Players learn the vocabulary from
> the game and from an in-game `dictionary`. **Never translate, correct, normalize, or overwrite Tomi-authored
> dialogue, narration or descriptions.**

This is a worldbuilding and literary identity decision, not a temporary translation workflow. Everything that
followed from the old localization plan — translation targets, completeness gates, a promised polished
English edition — is withdrawn. All development documentation, tabletop rulebooks, design documents, code,
tests, logs, internal prompts, issue/PR text and agent instructions remain **plain English**; a rulebook
written in English is not a localized edition of the MUD.

## One game language, not one language per locale

| Surface | Language |
| --- | --- |
| Player-visible MUD text: UI, dialogue, narration, quests, diegetic messages, future Concordia GM/NPC output | **Canonical NoöPunk Finglish** — one text per key. |
| Design docs, issues, PRs, rulebooks, agent instructions, internal prompts, code, tests, logs | **Plain English.** No multilingual styling. |
| Tomi-authored text already in the game | **Byte-for-byte intact.** |
| In-game `dictionary` entries | **English explanations** of unfamiliar terms — an aid, not a translation of scenes. |

There is **no localization pipeline, no translation target, no completeness gate and no alternate-language
edition.** Do not add one, and do not promise one in a comment or a document.

## Finglish is a living contact language

Not a fixed 50/50 split. English, contemporary Finnish, **Stadin slangi**, Swedish, Russian, Chinese and other
borrowings, plus NoöPunk terminology and code-switching — the way a future Helsinki would actually sound.

- Contemporary urban Finnish like **“Wallah!”** or **“Mä vannon!”** belongs when it suits the speaker and the
  moment. Slang is not a costume: do not stereotype speakers or pile it on.
- **Agent-written player text** is normally comprehensible English as the base, with occasional simple Finnish
  and situation-appropriate expressions, or attested/author-approved vocabulary. Tomi may write far more
  fully in Finnish; that material is canonical and his alone.
- **Register is individual.** Romppainen can carry idiosyncratic old and new slang, university vocabulary and
  bureaucratic jargon. An international UNSA agent might mostly speak English with a little clumsy Finnish.
  Helsinki youth and different factions code-switch differently.
- Ordinary English is sometimes the right register. Do not force a slang word into every sentence.
- **Creative influences are method, not text:** *A Clockwork Orange*'s Nadsat and *Blade Runner*'s Cityspeak
  supply the polyglot *technique and atmosphere*. Do not reproduce their invented lexicons or dialogue.

### String storage during migration

`mud/nopunk_mud/i18n.py` currently carries `fi` and `en` catalogues. Under this policy they are **provenance
layers, not supported locales**: `en` holds the agent-written source, `fi` holds Tomi's authored text where it
exists. Neither is a locale a player selects, and neither may be used to translate the canonical writing.
Keep both for save compatibility while the migration to **one canonical Finglish string per content key** is
carried out; see [`I18N_TO_CANONICAL_MIGRATION.md`](I18N_TO_CANONICAL_MIGRATION.md). Do not delete Tomi-authored
material, and do not silently rewrite text a save already points at.

## Dictionary, not translations

The in-game **`dictionary`** / **`lexicon`** command lets a player ask what a word means. See
`mud/nopunk_mud/lexicon.py` and `data/world/lexicon.json`.

- Glosses are **short English explanations** in context, not translated scenes.
- Every entry states **provenance**: attested contemporary or historical usage (which *requires* a source),
  an author neologism by Tomi, or a proposed expression. Speculation is never presented as etymology; the
  loader refuses an `attested` entry that cites nothing.
- **Spoiler-safe.** Public entries are always readable. `dossier` entries unlock through game progress, and a
  locked entry is indistinguishable from an unknown one so the refusal itself cannot confirm a secret.
- Keep core commands and critical feedback clear. Immersion must not make the mechanics unusable; clarify
  important instructions and explain words on demand.

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

Use explicit knowledge gates in scene data and avoid spoilers from UI, achievements, logs, narration, **or the
dictionary**.

## Future Concordia output

Runtime GM and NPC generation is bound by the same rule: **canonical Finglish, speaker-specific register, no
automatic translation**. Those instructions belong in the player-facing output contract, while internal
prompts, reasoning summaries, JSON state, mechanics and logs stay English. Concordia is not a prerequisite for
the solo campaign, which must remain completable with no LLM at all (#950).

## What an agent states when asked

**One NoöPunk MUD language, Finglish. No localizations, ever.** Tomi's text is untouched; agents write
English-led multilingual player text; everything not shown to the player is plain English.
