# Printable sheet and procedure card (#1053, #1054)

The tabletop-first requirement is an acceptance condition, not a sentiment: *"Every core rule and mod
must remain playable at a physical table with a rulebook, pencils, paper character sheets, and physical
dice."* This page is the artefact that makes that true for the playable slice. Print it, or copy the
fields onto index cards.

Everything numeric here is checked against the code, and where the two disagreed the code won — see
"Parity corrections" at the bottom.

---

## Page 1 — the character sheet

```
┌──────────────────────────────────────────────────────────────────────────┐
│ OPERATOR ______________________________   PLAYER ______________________  │
│ BACKGROUND ____________________________   LEVEL ____  XP ____            │
├──────────────────────────────────────────────────────────────────────────┤
│ STR ___ (   )   DEX ___ (   )   CON ___ (   )                            │
│ INT ___ (   )   WIS ___ (   )   CHA ___ (   )                            │
├──────────────────────────────────────────────────────────────────────────┤
│ HP ____ / ____        SYSTEM STRAIN ____ / ____     EFFORT ____ / ____   │
│ AC ____   ATTACK BONUS ____   MOVE ____   SAVES  P ___ E ___ M ___ L ___ │
├──────────────────────────────────────────────────────────────────────────┤
│ SKILLS                                                                   │
│  Administer __   Connect __   Drive __    Exert __    Fix __             │
│  Heal __         Know __      Lead __     Notice __   Perform __         │
│  Program __      Shoot __     Sneak __    Stab __     Survive __         │
│  Talk __         Trade __     Work __     Punch __    Sail __            │
├──────────────────────────────────────────────────────────────────────────┤
│ CYBERWARE (system, System Strain cost)                                   │
│  1. ____________________________  SS ____    2. __________________  ____ │
├──────────────────────────────────────────────────────────────────────────┤
│ GEAR / ENCUMBRANCE  ____ / ____ readied, ____ / ____ stowed              │
└──────────────────────────────────────────────────────────────────────────┘
```

### The two tables you actually need at the table

**Attribute modifiers (CWN, printed p. 5).** Copy these once and stop looking them up:

| score | 3 | 4–7 | 8–13 | 14–17 | 18 |
| --- | --- | --- | --- | --- | --- |
| modifier | −2 | −1 | +0 | +1 | +2 |

*These are not the WWN/SWN bands.* If you are carrying a modifier table over from another Without
Number game, it is the wrong one — that mistake was already printed once in
`docs/tabletop/FIRST_CASE_TABLETOP.md`, and this table is the corrected version.

**Level 1 baseline (printed p. 19).** Saving throws **15+** on 1d20 for all four categories, attack
bonus **+0**, hit dice 1d6 (1d6+2 for a Hard to Kill focus). A save target drops by 1 per level and by
the better of the two modifiers the category names:

| save | subtract the better of | |
| --- | --- | --- |
| Physical | Strength, Constitution | poison, exhaustion, bodily suffering |
| Evasion | Intelligence, Dexterity | pits, blasts, catching a falling comrade |
| Mental | Wisdom, Charisma | neurological hacking, mental effects |
| Luck | *nothing* | blind luck; no attribute modifies it |

---

## Page 2 — the procedure card

### Checks

```
2d6 + most applicable attribute modifier + skill level   ≥   difficulty
```

* Untrained (no level-0 in the skill): **−1**.
* Difficulty bands: trivial 6 · **routine 8** · demanding 10 · **hard 12** · formidable 14.
* A clue is never gated on a roll. Rolls decide danger, time and quality.

### Saves, attacks, damage

```
SAVE      1d20 ≥ (15 − level − best named attribute modifier)
ATTACK    1d20 + attack bonus + attribute modifier   ≥   target AC
DAMAGE    weapon die + attribute modifier
SHOCK     if the attack misses and the weapon's Shock ≥ target AC: Shock damage,
          + attribute modifier, never a Traumatic Hit
TRAUMA    roll the Trauma Die; on a hit, multiply damage by the Trauma Rating
```

### Injury and strain

```
0 HP, lethal, Traumatic Hit this scene  → Major Injury roll
0 HP, non-lethal                        → unconscious, stable
SYSTEM STRAIN  caps cyberware; over the cap, the character cannot act until it drops
```

### Running the investigation case by hand

| step | what happens | mechanic |
| --- | --- | --- |
| 1 | Briefing; the referee hands over the folder | none |
| 2 | Search the scene | none — a competent investigator finds the core clue. Read the clue text aloud |
| 3 | Do something under pressure | 2d6 + attribute + skill vs 8 / 10 / 12 |
| 4 | Each player keeps a theory board: clue → *supports / contradicts / neutral* | that is the player's reading, not the system's |
| 5 | The table states its answer | write it down. The mystery belongs to the table |

The case needs **both** of its two decisive clues before it can be answered; anything else is filed
`incomplete` with the consequence `insufficient_evidence`. The console enforces exactly this, and the
referee should too — otherwise the paper version is easier than the software one.

### The paper equivalent of the save file

The console saves one JSON document (`state_version: 1`). Nothing in it is unavailable to a table:

| JSON field | write it down as |
| --- | --- |
| `investigator.ratings` | the skill ranks on page 1 |
| `scene`, `visited` | a location list; cross one off when you leave |
| `discovered` | the clue list, with the scene it came from |
| `evidence` | the theory board (clue × hypothesis × supports/contradicts/neutral) |
| `theory` | the hypothesis currently written at the top of the board |
| `turns`, `seed`, `rng_state` | turn count; the seed only matters if you want to replay |
| `concluded`, `conclusion` | the answer you wrote down and its date |

### Worked example (the console's default seed, reproducible by hand)

The case's terminal search is a **Notice** check at routine difficulty. The recruit has Notice 1 and
Wisdom 10 (+0):

| 2d6 | arithmetic | total | vs 8 |
| --- | --- | --- | --- |
| 3 + 4 | 7 + 0 (Wisdom) + 1 (Notice) | **8** | success, by exactly zero |
| 1 + 1 | 2 + 0 + 1 | 3 | failure |
| 6 + 5 | 11 + 0 + 1 | 12 | success |

Same character, a Strength 3 check: 2d6 + (**−2**) + 1 — the attribute modifier is part of the rule,
which is why the console now takes it as a parameter instead of adding only the dice and the rank.

---

## Parity corrections made while writing this sheet

1. **The modifier bands were wrong** in `docs/tabletop/FIRST_CASE_TABLETOP.md`: it printed the WWN/SWN
   bands (`13–15 → +2`), which contradicted its own character table and `rules.wn_core`. Corrected to
   the CWN bands above.
2. **The console dropped the attribute modifier.** `CaseSession.risk()` summed 2d6 + rank only — a
   second implementation of the check, and a wrong one. It now delegates to
   `rules.wn_core.skill_check`; the default attribute score is 10 (+0), so existing replays produce the
   same totals while a named attribute contributes its real modifier. Pinned by
   `tests/test_console_case_session_1053.py::SharedRuleTests`.
3. **No new rule.** Both fixes move the repository *towards* the book; neither changes a CWN procedure.
