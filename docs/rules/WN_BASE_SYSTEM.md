# The base system: the *Without Number* shape

**Status: the base rules layer for new play, by author direction 2026-10-26.** The legacy
`STAT + Skill + 1d10` layer (`src/rules/core.py`, #111) is **transitional**: it still runs the legacy
game while its consumers are migrated, and it is no longer the description of what NoöPunk *is*.

The instruction this file records, verbatim:

> *For beginning, use CWN/SWN/AWN/WWN system for everything. Make the stats, skills, all rules based on
> them. We will modify later.*

## 1. What the base system is

| element | the base rule | canon |
| --- | --- | --- |
| **Attributes** | six: STR, DEX, CON, INT, WIS, CHA, each **3–18** | `data/rules/wn_core.json` `attributes` |
| **Attribute modifier** | 3 → −2 · 4–7 → −1 · 8–13 → +0 · 14–17 → +1 · 18 → +2 | `attributes.modifier_bands` |
| **Generation** | 3d6 in order, one score may become 14 before final touches; or the array 14, 12, 11, 10, 9, 7 | `attributes.generation` |
| **Skills** | **level 0–4**; level-0 is basic competence; **untrained −1**; starting characters cap at level-1 | `skills` |
| **Skill check** | `2d6 + attribute modifier + skill level ≥ difficulty` | `skill_check` |
| **Difficulty ladder** | **6 · 8 · 10 · 12 · 14** | `difficulties` |
| **Situational modifier** | −2 … +2; aid may add at most **+1** | `situational_modifier_band`, `aid_bonus` |
| **Saving throws** | **1d20 ≥ 16 − level − the higher of two listed attribute modifiers**; natural 1 fails, natural 20 succeeds; types: physical (STR/CON), evasion (DEX/INT), mental (WIS/CHA), luck (no attributes) | `saves` |

Implementation: `src/rules/wn.py`. Contract: `tests/test_wn_core.py` (24 tests, table-exact — a house
rule that moves a band edge, a ladder rung, the untrained penalty or the save formula fails a test
that names it).

## 2. Where the facts come from, and what may be reproduced

- **CWN SRD v1.0 — CC0.** The attribute bands, the 0–4 skill scale, the `2d6` check, the ladder and the
  four saves are taken from it as *facts and procedures*. The code and this page are original
  expression; no SRD sentence is reproduced.
- **SWN / AWN.** No established SRD licence → **shape only**, no text. Verified in
  [`../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`](../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md).
- **WWN SRD — CC0.** May be used later for Effort-shaped procedures; nothing from it is in this layer
  yet.

## 3. What happens to the legacy layer

`src/rules/core.py` keeps working, and is now labelled transitional in the package docstring. Two
conversions live in `wn` for records and logs:

| legacy | base system | conversion |
| --- | --- | --- |
| STAT 1–10 (`FIT/REF/INT/SOC/CYB/PSY`) | attribute 3–18 | `from_legacy_stat()`: linear stretch, 1 → 3, 10 → 18 |
| skill 1–10 | skill level 0–4 | `from_legacy_skill()`: 1–2 → 0, 3–4 → 1, 5–6 → 2, 7–8 → 3, 9–10 → 4 |
| `FIT/REF/INT/SOC` | `STR/DEX/INT/CHA` | `LEGACY_STAT_MAP` |
| `CYB`, `PSY` | fold into `INT`, `WIS` | **deliberate**: cybernetics and psychic capacity become *skills and Edges* rather than attributes — that is a later modification, not a base-system decision |

Nothing in the legacy layer is deleted: tests, scenarios and the deterministic harness keep running, so
a regression is visible rather than buried.

## 4. The migration queue (what "everything" still means)

The base system covers **the sheet and the check**. The rest of the rules are still legacy or
NoöPunk-original, and each row below is a real gap against the author's instruction — tracked, not
quietly assumed done:

| # | remaining subsystem | state | next step |
| --- | --- | --- | --- |
| M1 | **Action economy** | legacy 3 AP per exchange (`rulebook/18`) | decide AP vs the family's Move + Main round (register R4 in the #615 conflict register) |
| M2 | **Combat & injury** | legacy, priced by the #571 lethality lab | port CWN's Shock/Mortal Wound procedure, then re-price with the lab |
| M3 | **System Strain / cyberware** | capability-level, no tolerance track | decide the single track (queue **D36**) — the family's System Strain is the natural candidate |
| M4 | **Skills vocabulary** | 40 NoöPunk skills bound to legacy STAT codes | re-bind each skill to a WN attribute; adopt or reject the family's skill list per skill |
| M5 | **PSI / Effort** | natural PSI with Effort (`src/rules/natural_psi.py`) | keep the ontology, adopt the Effort *shape* (already ruled in #566) |
| M6 | **Hacking** | ubiquitous network (`src/rules/ubiquitous_network.py`) | unchanged by this decision: access stays geographic |
| M7 | **Character generation** | open (`rulebook/14`) | adopt the 3d6/array generation above, or author a NoöPunk variant |
| M8 | **Advancement** | open (`rulebook/14:368`) | the family's XP model is the default candidate; a playtest question |
| M9 | **NPCs** | mixed | NPCs follow the family's stat-line convention (no attribute sheets) |

M1, M3, M7 and M8 are **author decisions**; the rest are mechanical ports. None of them is guessed in
this increment.

## 5. How to play with the base system today

```python
from rules import wn

wn.attribute_modifier(15)                       # +1
wn.resolve_skill_check(attribute="INT", score=15, skill_level=2, difficulty=10, dice=(3, 4))
# SkillCheck(total=10, difficulty=10, success=True)
wn.save_target("mental", level=3, modifiers={"WIS": 1})   # 12
wn.roll_save("physical", level=1, modifiers={"STR": 2}, die=20)  # natural 20 -> success
```

`scripts/mixed_genre_demo.py --system wn` runs the four-environment example on this layer (the default);
`--system legacy` runs it on the transitional `1d10` layer, so the difference is visible side by side.

— Ai (愛)
