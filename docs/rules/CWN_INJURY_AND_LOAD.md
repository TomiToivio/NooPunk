# CWN: Major Injuries and encumbrance

Two more SRD subsystems, both previously listed as unported. The injury chain is now complete from
risk to consequence; encumbrance gives the runtime the load tiers and movement effects the SRD defines.

| subsystem | module | contract key | tests |
| --- | --- | --- | --- |
| Major Injury outcomes | `src/rules/cwn_major_injury.py` | `combat.major_injury` | `tests/test_cwn_major_injury.py` |
| Encumbrance | `src/rules/cwn_encumbrance.py` | `encumbrance` | `tests/test_cwn_encumbrance.py` |

Sources (CWN SRD, CC0):

* <https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/major-injuries/>
* <https://cwn.quadrifons.com/rules-of-the-game/encumbrance/>

`tests/test_wn_core_contract.py` fails if either the table or the numbers drift from
`data/rules/wn_core.json`.

## The injury chain

The kernel now covers every step the SRD's injury section states, across three modules:

1. **A Traumatic Hit happens** — `cwn_core.trauma_damage`, `cwn_trauma.is_traumatic`.
2. **The character reaches 0 HP in that scene** — `cwn_trauma.major_injury_risk` says whether the
   Major Injury risk applies.
3. **A Physical save** — `cwn_core.saving_throw("Physical", ...)`; passing leaves the character
   Mortally Wounded but stabilisable.
4. **1d12 on the table** — `cwn_major_injury.resolve_major_injury`, clamped to 1..12 as the SRD
   requires, and exposing what a runtime must apply: death, coma, blindness, a ruined limb, damaged
   cyber locations, the most Strain-expensive implant, or "just a flesh wound".

Two faithfulness notes:

* Row 4 (eye damage) names **cybereyes and their implants**, not a body location, so the table does
  not invent a location for it.
* Rows 2 and 5 kill **within an hour** without a street doc; that is recorded as data
  (`dies_within_hours = 1`), not as prose the runtime has to parse.

## Encumbrance

| SRD rule | implementation |
| --- | --- |
| Stowed points = Strength score | `stowed_capacity()` |
| Readied points = half Strength, rounded down | `readied_capacity()` |
| One push past the limit: +2 Readied, +4 Stowed, Move cut 30 % (10 m → 7 m) | `tier_for()` → `heavy`, `move_speed()` |
| A second push: Move cut 50 % (10 m → 5 m) | `tier_for()` → `overloaded` |
| More than that cannot be hauled a significant distance | `tier_for()` → `immobile`, `can_haul()` |
| Three small items bundle into one point | `bundled_points()` |
| 25 kg ≈ 10 points for a back-carried pack | `kilograms_to_points()` |

The module does not track items or judge whether an object is 0/1/2/5+ points; the SRD leaves
ambiguous objects to the GM.

## Still not transcribed

* **Mortal Injury and Stabilization** and **Natural Healing, First Aid and Poisons** — their SRD
  sub-pages did not load for me (404 from the site's own table of contents slugs), so the
  stabilisation difficulty, the dying-round count and the first-aid recovery rates are not
  implemented. The Strain and Major Injury halves of that section are.
* **CWN's hacking procedures.** The SRD's hacking chapter is transcribed and available, but
  `docs/rules/SUBSYSTEM_UBIQUITOUS_NETWORK.md` records the author's decision that NoöPunk's
  ubiquitous network does **not** import CWN's host-centric Access/Verb/Subject procedures. Only the
  network security levels and connection penalties would be compatible, and those are not ported
  here either.
* **Equipment, vehicles and cyberware catalogues** as data, and Edge/Focus text.
