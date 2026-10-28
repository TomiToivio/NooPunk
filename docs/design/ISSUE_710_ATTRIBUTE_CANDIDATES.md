# #710 — attribute candidates compared

**Status:** comparison for author decision. **No candidate is accepted here**, and no key, save format or
canonical stat changes. This document is the artifact #710 asks for; the choice itself is row **D704-6**
in `docs/design/ISSUE_704_DECISION_REGISTER.md`.

Governing text: `rulebook/WITHOUT_NUMBER_BASELINE.md` (author decision, 26 October 2026) adopts CWN's six
attributes on a 3–18 scale and states that Physical / Social / Psychic / Cybernetic describe the setting
and do **not** supply extra character attributes.

---

## The three candidates

### A — unchanged CWN

STR, DEX, CON, INT, WIS, CHA; 3–18; modifier `−2 / −1 / 0 / +1 / +2` by band.

- **Comprehension:** mixed. Familiar to anyone from D&D-family games; "WIS" and "CHA" read oddly in a
  near-future investigation game.
- **Source-book lookup:** perfect — every CWN citation maps one-to-one, which matters while the corpus is
  being ported.
- **Mechanical cost:** zero.
- **Migration:** zero.
- **Derived:** unchanged — HP, saves, Effort, load, combat, advancement, NPCs, gear, schemas.

### B — six modern display aliases, keys retained

Same six keys and numbers, different player-facing labels (e.g. Strength→Frame, Dexterity→Reflex,
Constitution→Endurance, Wisdom→Perception, Charisma→Presence; Intelligence unchanged).

- **Comprehension:** better for the setting; the sheet reads like the genre.
- **Source-book lookup:** degraded in print, preserved in data — a reader sees "Frame" where the SRD says
  "Strength", so every lookup needs a translation step unless the book prints both.
- **Mechanical cost:** zero, **provided the aliases are presentation only**. The moment a label implies a
  different scope (e.g. "Perception" absorbing what INT does), it is no longer candidate B.
- **Migration:** none for data; sheets and docs need relabelling; all prose and tests referencing the old
  labels need review.
- **Derived:** unchanged.

**Verdict:** the only genuinely reversible option, because keys and numbers never move.

### C — FIT / REF / INT / SOC / PSY / CYB

The former NoöPunk STAT line, locked under #131 and superseded by the 26 October baseline.

- **Comprehension:** reads best of the three for the genre.
- **Source-book lookup:** broken. FIT merges STR and CON; SOC merges CHA and part of WIS; PSY has no CWN
  axis; CYB has no CWN axis at all.
- **Mechanical cost:** high, and not localised:
  - **FIT merging STR+CON** collapses two distinct axes the CWN chassis uses separately — melee power and
    carrying capacity on one side, HP and System Strain capacity on the other. Every derived value that
    reads CON (HP, Strain, saves) must be re-derived from a merged score.
  - **PSY** risks conflating ordinary judgement (WIS) with trained psionic capacity and BCI telepathy.
    The baseline already warns that psychic complexity lives in the Psychic Systems layer, not in another
    attribute.
  - **CYB** has no CWN source axis. Making it an attribute would penalise unaugmented characters by
    definition — the exact failure #710 asks to avoid.
  - **Saves** map Physical(STR/CON), Evasion(DEX/INT), Mental(WIS/CHA); with FIT and SOC the mapping has
    to be reinvented.
  - **Effort, load, combat, skills, advancement, NPCs, gear, all schemas** each need auditing.
- **Migration:** a redesign, not a rename — new numbers, new derivations, incompatible sheets, and a
  rescaling question for every legacy character.

**Verdict:** rejected as a rename. It is a coherent *different game*, and if it is ever wanted it should
be argued as such, with its own design pass and its own migration plan.

---

## Recommendation

**A now, B later if the table finds the vocabulary distracting.**

Reasoning: the corpus is still being ported, and A keeps every CWN citation checkable at exactly the
moment that matters most. B is available afterwards as a genuinely reversible cosmetic trial — keys,
scores, formulas, saves, packages and existing saves all survive it untouched. C should not be attempted
while the port is incomplete, because it forces a simultaneous redesign of six derived systems.

## CYB, stated explicitly

Cybernetics stays off the attribute sheet. It is three things instead: a **skill domain** (Hardware,
Interface), **installed state** (slots, strain, maintenance), and **device statistics** (COMPUTE /
INTERFACE / NETWORK belong to decks and implants, not to people). This satisfies #710's requirement that
unaugmented characters not be penalised by definition.

## What a decision would unlock

Nothing in this document changes until the author rules. For **A**, nothing needs implementing. For **B**,
presentation-only work plus a relabelling sweep and a check that no existing save or schema stores a
label. For **C**, a separate design issue — not a migration of this one.
