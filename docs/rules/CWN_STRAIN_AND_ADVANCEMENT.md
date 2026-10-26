# CWN: System Strain and character advancement

Two subsystems from the **Cities Without Number SRD** that the kernel described in
`docs/rules/WN_BASE_SYSTEM.md` did not yet implement. Both are transcribed from the SRD, with the
section URL recorded next to each rule so a reader can check the code against the source rather than
against this document.

| subsystem | module | contract key | tests |
| --- | --- | --- | --- |
| System Strain | `src/rules/cwn_strain.py` | `strain` | `tests/test_cwn_strain.py` |
| Advancement | `src/rules/cwn_advancement.py` | `advancement` | `tests/test_cwn_advancement.py` |

The contract (`data/rules/wn_core.json`) states the same numbers; `tests/test_wn_core_contract.py`
fails if the two drift apart.

## System Strain

Source: <https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/system-strain/>

| SRD rule | implementation |
| --- | --- |
| Maximum is the Constitution score | `SystemStrain.maximum`, `MAXIMUM_ATTRIBUTE` |
| Starts at zero; cannot exceed the maximum | `__post_init__` refuses an over-maximum construction |
| Cyberware adds **permanent** Strain, which may be fractional | `install_cyber()` / `remove_cyber()` |
| An addition that would pass the maximum cannot be used — no cyber activation, no drug benefit | `absorb()` returns `False` and changes nothing |
| A forced overflow knocks the subject out for at least an hour | `absorb(..., forced=True)` clamps at the maximum and sets `unconscious_hours` |
| One point is lost after a qualifying night's rest (warm, fed, comfortable, 8 h uninterrupted) | `rest_night()` |

Two decisions worth stating, because the SRD leaves room to misread them:

* **Permanent Strain is not recovered by rest.** The SRD says a character loses one point of
  *accumulated* Strain per night; permanent implant Strain only goes away when the implant does.
  `rest_night()` therefore reduces `temporary` only.
* **A forced overflow does not raise the total above the cap.** The SRD says the total "cannot
  accumulate more than this maximum", so the overflow is represented by unconsciousness, not by a
  strain debt above the maximum.

## Character advancement

Source: <https://cwn.quadrifons.com/rules-of-the-game/character-advancement/>

| SRD rule | implementation |
| --- | --- |
| Levels 1–10; XP totals accumulate and do not reset | `MIN_LEVEL`, `MAX_LEVEL`, `level_for_xp()` |
| Fast and slow tracks | `XP_FOR_LEVEL["fast" \| "slow"]`, `xp_for_next_level()` |
| Three XP for an average successful mission | `DEFAULT_XP_PER_MISSION` |
| Three skill points per level, four with Educated | `skill_points_for_level()` |
| Ranks bought in order, 1/2/3/4/5 points, gates at levels 1/1/3/6/9, maximum rank 4 | `skill_point_cost()`, `total_skill_cost()`, `skill_rank_allowed()` |
| Attribute boosts cost 1, 2, 3, 4, 5; five in total; gated at levels 1/1/3/6/9 | `attribute_boost_cost()`, `attribute_boost_allowed()` |
| Focus picks at levels 2, 5, 7, 10; third Edge at 5 | `focus_picks_at()`, `has_third_edge()` |
| Attack bonus is half level (full level with On Target) | `attack_bonus()` |
| Saves are `16 − level` before attribute modifiers (15 at level 1) | `save_target()` — attribute modifiers stay in `cwn_core.save_target()` |
| HP: 1d6 per level (+2 per die with Hard to Kill) + CON modifier per die, no die below 1; take the roll only if it beats the current maximum, otherwise +1 | `hit_points_rolled()`, `new_maximum_hit_points()` |

The HP rule is two steps on purpose: the SRD rolls one total and *then* compares it with the current
maximum, so a low roll still grants exactly one point rather than a second, separate die.

## Deliberately not transcribed yet

These remain open, and are listed rather than quietly approximated:

* **First aid, poisons and natural healing rates.** Their SRD subsections are not yet transcribed;
  only the Strain economy around them is. `docs/rules/CWN_CONVERSION.md` tracks the gap.
* **The Major Injury d12 table.** `src/rules/cwn_trauma.py` already decides *whether* a Major Injury
  is risked (`major_injury_risk()`); the table's twelve outcomes are content and are not modelled.
* **Edge and Focus text.** Only the levels at which picks happen and the fifth-level Edge are
  arithmetic; the benefits themselves are content.
* **The Underdog Rule** and other optional character-creation variants.

## Rights

The CWN SRD is **CC0**; the rights entry is in `data/sources/game_system_rights.json` and the standing
matrix is `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`. The implementation is our own code; the
prose above is written for this repository. No SRD text is reproduced beyond the short rule statements
needed to state what the code does.
