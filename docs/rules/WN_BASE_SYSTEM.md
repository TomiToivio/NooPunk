# The base system: the *Without Number* shape, as implemented

**Status: implementation contract for the base rules layer.** The decision itself is recorded in
[`RULES_FOUNDATION_POLICY.md`](RULES_FOUNDATION_POLICY.md) (#615) and the kernel baseline in
`ISSUE_615_*.md`; this page is the part a caller needs: what the code does, what the canon data says,
and what is still legacy.

Author direction, 2026-10-26:

> *For beginning, use CWN/SWN/AWN/WWN system for everything. Make the stats, skills, all rules based on
> them. We will modify later.*

## 1. The rules the code implements

| element | rule | canon | code |
| --- | --- | --- | --- |
| Attributes | six, **3–18** | `attributes` | `ATTRIBUTES`, `ATTRIBUTE_CODES`, `attribute_modifier()` |
| Modifier bands | 3 → −2 · 4–7 → −1 · 8–13 → +0 · 14–17 → +1 · 18 → +2 | `modifiers` | `attribute_modifier()` |
| Skills | level **0–4**; level-0 is competence; **−1 untrained** | `skills` | `skill_check(..., skill_level=None)` |
| Skill check | **2d6 + attribute modifier + skill level ≥ difficulty** | `skill_check` | `skill_check()` → `Check` |
| Ladder | **6 · 8 · 10 · 12 · 14** | `difficulty_*` constants | `DIFFICULTY_SIMPLE` … `DIFFICULTY_EXTREME` |
| Situational / aid | −2 … +2 · aid ≤ +1 | `modifiers` | `clamp_situational()`, `clamp_aid()` |
| Saves | **1d20 ≥ 16 − level − the higher of the pair**; natural 1 fails, 20 succeeds | `saves` | `save_target()`, `roll_save()` |
| Attack | 1d20 + attack bonus vs AC | `combat` | *(canon only so far)* |

Save categories and their pairs: **physical** STR/CON, **evasion** DEX/INT, **mental** WIS/CHA,
**luck** none (target `16 − level`).

```python
from src.rules import wn_core as wn

wn.attribute_modifier(15)                                             # +1
wn.skill_check(attribute_score=15, skill_level=2, difficulty=10, dice=(3, 4)).total       # 10
wn.skill_check(attribute_score=10, skill_level=None, difficulty=8, dice=(2, 3)).total     # 4, untrained
wn.save_target("mental", level=3, modifiers={"WIS": 1})               # 12
wn.roll_save("physical", level=1, modifiers={"STR": 2}, die=20).success                   # True
```

## 2. Two corrections this contract records

Both were found by reading the source, not by preferring a number:

1. **Saving throws.** The canon file had `base 15` and no level term. CWN SRD 2.02 says the target is
   **16 minus character level and the highest of the two listed attribute modifiers**. Corrected in
   `data/rules/wn_core.json` and implemented in `save_target()`, with a natural 1/20 rule.
2. **Untrained skills.** The kernel accepted only `skill_level >= 0`, which cannot express "no level-0
   at all". The SRD applies **−1** there, and level-0 is *basic competence* — the two states are not
   the same. `skill_level=None` now means untrained, and `Check.untrained` makes it visible.

## 3. Migration from the transitional layer

`src/rules/core.py` (`STAT + Skill + 1d10`, #111) is **transitional**: it still runs the legacy game
and its 2500-test suite. Conversions for records and logs:

| legacy | base | conversion |
| --- | --- | --- |
| STAT 1–10 | attribute 3–18 | `from_legacy_stat()` — linear stretch, 1 → 3, 10 → 18 |
| skill 1–10 | level 0–4 | `from_legacy_skill()` — 1–2 → 0, 3–4 → 1, 5–6 → 2, 7–8 → 3, 9–10 → 4 |
| `FIT/REF/INT/SOC` | `STR/DEX/INT/CHA` | `LEGACY_STAT_MAP` |
| `CYB`, `PSY` | fold to `INT`, `WIS` | **deliberate**: cybernetic and psychic capacity become skills, Edges and permissions (step M4) |

## 4. What "everything" still means — the migration queue

The base system now covers **the sheet, the check and the saves**. These remain legacy or
NoöPunk-original, and each is a real gap rather than an assumed success:

| # | subsystem | state | next step |
| --- | --- | --- | --- |
| **M1** | Action economy | legacy 3 AP per exchange | author decision: AP vs Move + Main round |
| **M2** | Combat & injury | legacy, priced by the #571 lethality lab | port the Shock/Mortal-Wound procedure, then re-price |
| **M3** | System Strain / cyberware | capability-level, no tolerance track | decide the single track (**D36**) |
| **M4** | Skill vocabulary | 40 skills bound to legacy STAT codes | re-bind each skill to an attribute; adopt or reject the family list per skill |
| **M5** | PSI / Effort | natural PSI with Effort | keep the ontology, adopt the Effort shape (#566) |
| **M6** | Hacking | ubiquitous network | unchanged: access stays geographic |
| **M7** | Character generation | open | adopt 3d6/array, or author a NoöPunk variant |
| **M8** | Advancement | open | the family's XP model is the default candidate |
| **M9** | NPCs | mixed | the family's stat-line convention (no attribute sheets) |

M1, M3, M7 and M8 are **author decisions**; the rest are mechanical ports.

## 5. Licence note

The bands, the 0–4 scale, the 2d6 check, the ladder and the four saves are **CWN SRD facts (CC0)**, and
the implementation here is original expression — no SRD sentence is reproduced. **Nothing from SWN or
AWN is used**: neither has an established SRD licence
([`../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`](../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md)).
WWN (CC0) is available for later Effort-shaped procedures and is not used yet.

— Ai (愛)
