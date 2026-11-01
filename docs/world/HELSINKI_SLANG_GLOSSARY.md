# Helsinki slang glossary — moved

**The vocabulary list that used to live here is now the root [`GLOSSARY.md`](../../GLOSSARY.md), which is the
single source of truth (#1000).** Everything unique to this file was migrated there under *Migrated from the
older secondary glossary*; nothing was dropped.

Do not add words here. A second word list is a second authority, and the two drift. The in-game `dictionary`
is generated from `GLOSSARY.md` by `tools/glossary_to_lexicon.py`, so a term that is not in the glossary does
not exist as far as the game is concerned.

## Provenance rules (kept here because they are editorial, not vocabulary)

| Provenance | Means | Requires |
| --- | --- | --- |
| `documented` | documented contemporary or historical usage | a **source** |
| `tomi` | supplied or approved by Tomi | his authorship |
| `agent_proposed` | recorded for consideration, not yet canon | nothing — but must not be described as established |

An agent must never present a guess as authentic slang or an invention as etymology. Where Tomi's own
introduction says *some* headwords are NoöPunk inventions without saying which, they stay classified as
attested-modern and the gap is recorded in `GLOSSARY.md` rather than filled by guesswork.

## Player-facing behaviour

The dictionary gives short English explanations in context — never translated scene text — and shows the term's
provenance so the game does not pass a guess off as established usage. Knowledge-gated terms stay silent until
the story unlocks them, and a gated lookup answers exactly as an unknown word does, so the refusal cannot
confirm that a secret exists. See [`docs/FINNISH.md`](../FINNISH.md) for the language policy.
