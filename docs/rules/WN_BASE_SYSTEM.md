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
| Skills | level **0–4**; level-0 is competence; **−1 untrained**; **−2 untrained attack** | `skills` | `SKILLS`, `PSIONIC_SKILLS`, `skill_check(..., skill_level=None)` |
| Skill check | **2d6 + attribute modifier + skill level ≥ difficulty** | `skill_check` | `skill_check()` → `Check` |
| Ladder | **6 · 8 · 10 · 12 · 14** | `difficulty_*` constants | `DIFFICULTY_SIMPLE` … `DIFFICULTY_EXTREME` |
| Situational / aid / flat | −2 … +2 · aid ≤ +1 · connection and gear modifiers unclamped | `modifiers` | `clamp_situational()`, `clamp_aid()`, `Check.misc` |
| Saves | **1d20 ≥ 16 − level − the higher of the pair**; natural 1 fails, 20 succeeds | `saves` | `save_target()`, `roll_save()` |
| Attack | 1d20 + attack bonus + attribute modifier + combat skill vs Melee/Ranged AC | `combat.attack` | `attack_roll()` |
| Damage, Shock, Trauma | weapon dice + attribute modifier; Shock on a qualifying miss; Trauma multiplies | `combat.damage/.shock/.trauma` | `resolve_attack()`, `DamageSoak` |
| Mortal injury and Major Injuries | 6 rounds, `8 + rounds` to stabilize, d12 table after a failed Physical save | `combat.mortal_injury/.major_injury` | `MortalWound`, `major_injury()` |
| System Strain and healing | maximum is CON; first aid `1d6 + Heal` and one Strain; natural healing is the level | `strain`, `healing` | `SystemStrain`, `first_aid_healing()`, `natural_healing()` |
| Hacking | Access = INT mod + Program + deck; security 7–12; wireless −2, VR crown −1; two failures per alert action | `hacking` | `access_pool()`, `hacking_difficulty()`, `hacking_check()`, `AlertCounter` |
| Cyberware | installation bands by Strain, 5% monthly upkeep, optional alienation | `cyberware` | `cyberware_installation()`, `installation_outcome()` |
| Encumbrance | Stowed = STR, Readied = STR/2, two overload stages | `encumbrance` | `stowed_capacity()`, `overload_stage()` |
| Advancement | fast/slow XP, 3 skill points per level, level//2 attack bonus, HP reroll rule | `advancement` | `level_for_xp()`, `skill_point_cost()`, `hit_points_gain()` |
| Psionics | Effort = 1 + better WIS/CON modifier + best psionic skill; commit for scene/day; torch on a d6 | `psionics` | `src/rules/psionics.py` |

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

The base system now covers **the sheet, the check, the saves, combat, injury, Strain, hacking,
cyberware, encumbrance, advancement and psionics**. These remain legacy or NoöPunk-original, and each is
a real gap rather than an assumed success:

| # | subsystem | state | next step |
| --- | --- | --- | --- |
| **M1** | Action economy | **in the contract** (`combat.actions`: Main/Move/On Turn/Instant, 10 m) | the legacy 3-AP exchange still runs the old game; retire it with the rest of the legacy runtime |
| **M2** | Combat & injury | **ported** (`attack_roll`, `resolve_attack`, `MortalWound`, Major Injuries) | re-price the #571 lethality lab against the new procedure |
| **M3** | System Strain / cyberware | **ported** (`SystemStrain`, installation bands, maintenance) | author decision D36 is now answered by the source: one Strain track |
| **M4** | Skill vocabulary | **ported** (`SKILLS` = the CWN 19; psionic disciplines separate) | re-bind legacy characters as they are rebuilt |
| **M5** | PSI / Effort | **ported** (`src/rules/psionics.py`, Effort + commitment + torching) | the technique catalogue is provisional; the author owns its numbers |
| **M6** | Hacking | **ported** (Access, security levels, connection penalties, alerts) | the ubiquitous-network framing stays NoöPunk; the procedure is CWN's |
| **M7** | Character generation | **in the contract** (`generation`: 3d6 or the array, 2 Edges, 1 Focus) | Edges and Foci text is author content |
| **M8** | Advancement | **ported** (`advancement`) | the legacy runtime still awards Fate advances; do not run both |
| **M9** | NPCs | **ported convention** + stat lines in the first scenario | the family's stat-line shape is now the level data's shape |

What is still missing is content rather than procedure: the equipment catalogue, the Edge and Focus
lists, drones, vehicles, faction turns, and the AWN/WWN survival and exploration modules. Each is listed
with its reason in [`CWN_CONVERSION.md`](CWN_CONVERSION.md) §3.

## 5. Licence note

The bands, the 0–4 scale, the 2d6 check, the ladder, the four saves, combat, injury, Strain, cyberware
and hacking are **CWN SRD facts (CC0)**, and the implementation here is original expression — no SRD
sentence is reproduced. The Effort pool pattern is from the **WWN SRD (CC0)**. **Nothing from SWN or AWN
is reproduced**: neither has an established SRD licence
([`../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`](../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md)), so
the psionic mechanics are an independent re-expression of the shape and the technique catalogue is
authored NoöPunk content.

— Ai (愛)
