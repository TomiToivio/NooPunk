# The first UNSA case at a physical table

Every mechanic the console case uses, with the manual procedure and the same worked numbers the
software produces. This document is the tabletop half of the rulebook ↔ code parity requirement in
#1054: if a number here disagrees with the code, one of them is wrong and the disagreement is a bug.

**You need:** the published CWN rules (skills, saves, damage), the NoöPunk case text, two dice for
checks (2d6), percentile dice for saves, paper, pencil.

## 1. The character

Play the UNSA recruit the console uses, so examples carry over:

| attribute | score | modifier |
| --- | --- | --- |
| Strength | 10 | +0 |
| Dexterity | 12 | +0 |
| Constitution | 11 | +0 |
| Intelligence | 13 | +1 |
| Wisdom | 10 | +0 |
| Charisma | 9 | +0 |

Skills: **Notice 1**, **Administer 1**, **Talk 0**. Hit points 4 (a level-1 die rolled 4). System
Strain capacity **11**. Saves: Physical 15, Evasion 15, Mental 15, Luck 15.

Modifiers are the published CWN bands (**printed p. 5**): 3 → −2, 4–7 → −1, 8–13 → +0, 14–17 → +1,
18 → +2. These are *not* the WWN/SWN bands (which run 6–8 → 0, 9–12 → +1, 13–15 → +2, 16–17 → +3,
18 → +4); an earlier revision of this page printed those, which contradicted both the table above and
`rules.wn_core.attribute_modifier`. The code was right and the page was wrong; `tests/test_wn_core.py`
pins the bands, and `tests/test_console_case_session_1053.py::SharedRuleTests` pins that the console
passes the attribute modifier through instead of dropping it.

This character's 13 in Intelligence is the only modifier that is not +0, which is why every example
below is easy to check by hand.

## 2. Checks — 2d6 + attribute + skill vs difficulty

Difficulty bands: trivial 6, **routine 8**, demanding 10, hard 12, formidable 14.

**Worked example (the case's first clue).** *Examine the terminal* is a Notice check at routine
difficulty. Nothing is added from Intelligence — Notice is a Wisdom skill, and Wisdom's modifier is 0.

| 2d6 | arithmetic | total | vs 8 |
| --- | --- | --- | --- |
| 3 + 4 | 7 + 0 (Wisdom) + 1 (Notice) | **8** | success — barely |
| 1 + 1 | 2 + 0 + 1 | 3 | failure |
| 6 + 5 | 11 + 0 + 1 | 12 | success |

That first row is the console's default seed: it succeeds by exactly zero margin. If you want the
tension the software has by default, take that roll.

## 3. The case itself, as a table procedure

The console's command verbs map one-to-one onto table conversation; the GM reads the same content file.

| step | what happens | mechanic |
| --- | --- | --- |
| 1 | Briefing at the safehouse, Romppainen hands over the folder | none |
| 2 | Travel to the university, examine the terminal | Notice, routine (8) → clue **access_log** |
| 3 | Travel to Kurvi, talk to the witness | no check; roleplay |
| 4 | Ask her about the badge | she remembers; grants the **badge** line — without asking, the second clue cannot be read |
| 5 | Examine the woman in the raincoat | requires the badge line → clue **witness_badge** |
| 6 | Return to the safehouse and report | the case closes |

**Ending rule, exactly as implemented:** `solved` requires **both** `access_log` and `witness_badge`;
any other report is filed as `incomplete` and adds the consequence `insufficient_evidence`. Fleeing an
encounter adds `fled_encounter`. There is no partial credit and no hidden third clue.

**Time.** Each action advances the mission clock; the console counts mission minutes separately from
the number of commands. At the table, count minutes the same way: travel and searches cost time,
talking costs little.

## 4. Harm, strain and privation

- **Damage**: published CWN procedure; the character has 4 HP, so a 1d6 weapon can drop them in one hit.
  The console kills the character at 0 HP and ends the case as `killed`.
- **System Strain**: capacity 11. Strain is spent by psionics and by privation, and recovers with rest.
- **Privation** (AWN, `data/rules/awn_survival.json` — the numbers the software actually uses):

| situation | strain |
| --- | --- |
| first day without food | 0 |
| each further day without food | +1 |
| first day without water | +2 |
| each further day without water | +3 |
| night without adequate shelter | 0 |
| harsh night without shelter | +1 |

Privation also blocks natural healing, and overflowing capacity calls for a Physical save
(success: helpless until rescued or dead). A character at 0 gained strain from privation is not injured
by it — the numbers are in the contract file, not in prose, so a table can quote them exactly.

## 5. Determinism, for table and machine alike

The console seeds its dice (`--seed 7` by default) and saves the generator state, so a playthrough can be
replayed roll for roll. At a table the equivalent is recording the rolls: the numbers in §2 are exactly
what seed 7 produces, and writing them down gives you the same audit trail the save file gives the
software.

## 6. What is software-only, and honestly so

Nothing in the case *requires* the computer: steps 1–6 are a conversation plus two checks. What the
console adds is bookkeeping — the clue set, the clock, the save file and the deterministic dice. If a
mechanic cannot be run with a pencil, it does not belong in the case.
