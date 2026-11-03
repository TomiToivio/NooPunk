# CWN ↔ WWN ↔ SWN ↔ AWN compatibility (#1101, Phase 0)

What this document is: the answer to *"when a WWN rule is needed in NoöPunk, does CWN already provide it,
does it need a WWN-native variant, or has nobody looked?"* — one row per concern, with the evidence that
decided the answer.

What it is not: a claim that the four Sine Nomine games share a mechanics set. They share a chassis and they
diverge, and the divergences are the whole reason this table exists. **Precedence, as the author has fixed
it: CWN wins.** It is the primary character-scale game; WWN, SWN and AWN are complementary packages whose
procedures apply where their own material says they do.

Status vocabulary matches `data/rules/wwn_traceability.json`:
`verified` · `verified_reuse` · `partial` · `unverified` · `missing` · `not_applicable`.

| concern | WWN source | NoöPunk implementation | status | note |
|---|---|---|---|---|
| Attribute scale and modifiers | WWN p.8 | `src/rules/wn_core.py` → `attribute_modifier` | **verified_reuse** | Identical bands (3 → −2, 4–7 → −1, 8–13 → +0, 14–17 → +1, 18 → +2), pinned by `tests/test_wwn_shared_chassis.py`. One table, both games. |
| Skill checks | WWN pp.9, 41 | `src/rules/wn_core.py` → `skill_check` | **verified_reuse** | 2d6 + skill level + attribute modifier, −1 untrained, success on ≥ difficulty. Tabletop and digital pass the same dice through the same resolver. |
| Skill vocabulary | WWN p.10 | CWN's skill list | **not_applicable** | CWN's list is authoritative for CWN characters. WWN-only skills (e.g. its crafts) apply inside a WWN-native procedure, never as a second rank of an existing CWN skill. |
| Saving throws | WWN p.40 (printed values) | `src/rules/cwn_core.py` → `save_target` (16 − level − attribute modifier) | **unverified** | The two formulas are shaped differently and nobody has compared them row by row. Do not claim WWN saves are "already handled" until a test does. |
| Combat, AC, Shock, Trauma | WWN pp.42–47 | `src/rules/cwn_combat.py`, `cwn_attack_modifiers.py` | **unverified** | CWN's combat is the resolver for NoöPunk. WWN's Shock and combat tables have not been checked against it; where they genuinely differ, a WWN-native supplement belongs next to — not inside — the CWN procedure. |
| System Strain and healing | WWN p.48 | `src/rules/cwn_core.py` (`Strain`, `strain_maximum`) | **unverified** | CWN's strain is implemented and tested; WWN's healing and recovery text has not been compared with it. |
| Encumbrance | WWN p.32 | `src/rules/cwn_encumbrance.py` | **unverified** | CWN implements Readied/Stowed; WWN's numbers are not compared. |
| Classes and advancement | WWN pp.18–21, 54 | — | **missing** | Warrior / Expert / Mage / Adventurer and partial classes have no implementation, and CWN's progression must not be overwritten to host them. They must arrive as opt-in WWN-native packages. |
| Foci | WWN p.22 | — | **missing** | No CWN equivalent; a WWN-only character-option subsystem. |
| Arcane Effort (WWN) vs Psychic Effort (SWN) vs System Strain (CWN) | WWN pp.66–86; SWN psi | `src/rules/wwn_high_mage.py` (`effort_max`), `src/rules/swn_*` | **partial** | Three different pools. WWN High Mage Effort is implemented and must never share a pool with SWN psychic Effort; CWN System Strain is untouched. A caster with both is two pools, added, not merged. |
| High Magic spells and Arts | WWN pp.64–74 | `src/rules/wwn_spells.py`, `wwn_high_mage.py` | **verified** | 52 High Magic spell identities catalogued with the learning procedure; the High Mage class procedure (Effort, preparation, recovery, Arts) implemented. |
| Spell effect resolution | WWN pp.68–74 | `src/rules/wwn_spell_effects.py` | **partial** | 13 level-1 High Magic effect rows resolve; 70 remain (#1085's increments). `untranscribed()` reports them rather than inventing numbers. |
| Elementalist / Necromancer / Healer / Vowed traditions | WWN pp.76–86 | spell identities only | **partial** / **missing** | The 31 non-High-Magic spell identities are catalogued; no tradition class procedure is implemented. |
| Spell research, magical workings, item creation | WWN pp.88–92 | — | **missing** | All three are cost/time procedures and none is implemented. |
| Major projects | WWN p.336 | `src/rules/wwn_projects.py` | **verified** | Difficulty, adventure share and allied-faction share implemented with seeded tests. |
| Faction turn | WWN pp.324–334 | SWN faction engine (`src/rules/swn_faction_*.py`) | **missing** (WWN) | SWN's faction engine is a **different** system with different assets and turns. It is not a substitute and the two must not be collapsed into one engine; WWN's own turn is unimplemented. |
| Creatures and stat blocks | WWN pp.280–320 | — | **missing** | No WWN creature model. CWN's NPC reaction/morale values exist but are not the WWN procedure. |
| Reaction and morale | WWN pp.296–297 | `src/rules/cwn_npcs.py`-adjacent procedures | **unverified** | CWN has reaction/morale values; WWN's 2d6 bands are not compared. |
| Deluxe: Arts of the Gyre, Heroic classes, Legates, Iterums, GM tools | WWN pp.344–391 | — | **missing** | The source is now section-indexed (`data/rules/wwn_sections.json`), so these are citable rather than guessed at — but no procedure is implemented. |
| Survival, stress, enclaves (AWN) | AWN rules | `src/rules/awn_*.py` | **partial** | AWN's stress and survival clocks are their own procedure and must not be represented as CWN System Strain. |
| Cross-game qualifications ("Mixing Sine Nomine Games Together") | CWN Free Edition, printed p.218 onward | — | **unverified** | The cited page has not been transcribed into this repository, so the compatibility rules above are NoöPunk's engineering reading, not a quotation of that section. Recording them from the actual page is open work on this issue. |

## The two WWN registers, and why there are two

| register | granularity | question it answers | generated by |
|---|---|---|---|
| `data/rules/wwn_register.json` → [WWN_COVERAGE_1101.md](WWN_COVERAGE_1101.md) | one row per tracker subsystem (A1…K1) | "is this piece of issue #1101's checklist done?" | `tools/wwn_register_audit.py` |
| `data/rules/wwn_traceability.json` → [WWN_SECTION_COVERAGE_1101.md](WWN_SECTION_COVERAGE_1101.md) | one row per printed section (138 rows) | "is this heading in the book implemented?" | `tools/wwn_parity_audit.py` |

They are not duplicates: the subsystem register is where the tracker's acceptance criteria live, and the
section register is what the book actually contains — 138 headings, extracted from its own running heads.
The section view is what keeps the subsystem view honest: a subsystem row marked `missing` can be checked
against the number of sections behind it, and a section row can never be "covered" by a chapter title.

## What this table refuses to do

* **It will not mark a row verified because a CWN function looks similar.** Six rows above are `unverified`
  for exactly that reason: a resolver exists, and nobody has shown it returns WWN's printed numbers.
* **It will not merge the faction engines.** SWN's and WWN's faction systems are both published, both
  valid, and structurally different. The integration point is shared identity/date/event data, not a
  shared turn loop.
* **It will not let a NoöPunk mod masquerade as a WWN rule.** The Mythos, Ideology, Investigation and
  Noösphere mods live in `mods/noopunk/` and change nothing about the published procedures above.

## How to move a row out of `unverified`

1. Find the WWN printed numbers for the concern (the section index gives you the page).
2. Write a test that takes those numbers *from the page* and asserts the shared function returns them —
   the shape of `tests/test_wwn_shared_chassis.py`.
3. If it fails, the resolver is wrong for WWN: implement a WWN-native supplement beside the CWN
   procedure, cite the page, and leave CWN untouched.
4. Update `data/rules/wwn_traceability.json`, then `python3 tools/wwn_parity_audit.py`.
