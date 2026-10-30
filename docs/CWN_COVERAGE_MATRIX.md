# CWN / SWN rules coverage matrix (#749, work package A)

**Status:** audit baseline, 2026-10-28. This is *measurement*, not a claim of completeness. Every row
below was produced by enumerating the repository and running the suite on this machine.

**Authority.** `AGENTS.md` and `rulebook/WITHOUT_NUMBER_BASELINE.md` govern: CWN is the chassis, SWN
Revised supplies psionics, and engine code may not invent a rule. Where the two documents and this
matrix disagree, they win.

## How this was measured

```bash
python3.11 -m unittest discover -s tests -p "test_*.py"            # Ran 1452 tests … OK
python3.11 -m unittest discover -s tests -p "test_cwn_*.py"        # Ran 413 tests … OK
python3.11 -m unittest discover -s strategy_game/tests -p "test_*.py"
ls src/rules/cwn_*.py | wc -l                                      # 20
ls godot/tests/*.gd | wc -l                                       # 10
```

`src/rules/` holds **20 CWN modules** (4,349 lines) and every one has a matching
`tests/test_<module>.py`. `godot/` holds **21 GDScript files** and **10 headless test scripts**.

## Matrix

Status vocabulary: **implemented** = procedure exists and is tested; **partial** = the rules object
exists but a documented part of the procedure does not; **absent** = nothing yet.

| CWN area | Module | Tests | Status | Note |
|---|---|---|---|---|
| attributes, modifiers, 2d6 checks, saves | `cwn_core.py` | `test_cwn_core.py` | implemented | |
| character record | `cwn_character.py` | `test_cwn_character.py` | implemented | |
| backgrounds | `cwn_backgrounds.py` | `test_cwn_backgrounds.py` | implemented | |
| edges and foci | `cwn_edges_foci.py`, `cwn_foci.py` | matching | implemented | |
| advancement | `cwn_advancement.py` | matching | implemented | |
| combat: initiative, rounds, attacks | `cwn_combat.py` | matching | implemented | |
| combat actions | `cwn_combat_actions.py` | matching | implemented | |
| attack modifiers / cover | `cwn_attack_modifiers.py` | matching | implemented | |
| damage, armour, trauma, major injury, healing | `cwn_trauma.py`, `cwn_major_injury.py`, `cwn_injury_procedure.py`, `cwn_healing.py` | matching | implemented | |
| equipment, encumbrance, gear mods | `cwn_equipment.py`, `cwn_encumbrance.py`, `cwn_gear_mods.py` | matching | implemented | |
| cyberware strain | `cwn_strain.py` | matching | implemented | |
| drones | `cwn_drones.py` | matching | implemented | |
| vehicles | `cwn_vehicles.py` | matching | implemented | |
| **hacking: Access, security ladder, connection penalties, alert clock, cyberware/drone difficulty** | `cwn_hacking.py` | `test_cwn_hacking.py` | **partial** | see below |
| **hacking: Verbs, Subjects, programs, CPU slots, Access costs, demons/watchdogs** | — | — | **absent** | deliberate deferral, see below |
| SWN Revised psionics | `swn_psionics.py`, `natural_psi.py`, `psionics.py` | matching | implemented | licence caveat below |
| investigation / evidence gating | `investigation.py`, `investigation_evidence.py`, `anomaly_gate.py` | matching | implemented | |

## The one rules gap this issue names, confirmed

`src/rules/cwn_hacking.py` implements the *procedure around* a hack: the Access pool, the 7–12 security
ladder, the wireless (−2) and VR-crown (−1) penalties kept flat rather than folded into circumstances,
`7 + ceil(HD/3)` for cyberware, and the two-failures-per-Alert clock.

It states in its own docstring that Verbs, Subjects, programs, CPU slots, demons and watchdogs are
**not modelled** — "catalogue content, not procedure: a Verb is a row with a cost, an Access cost and a
check modifier… the author has not ruled on" the table.

So #749's requirement — *"implement complete vanilla CWN hacking resolution behind a reusable rules API;
existing connectivity checks alone are insufficient"* — is **not met**, and cannot be met honestly by
invention. It needs the SRD's Verbs/programs table transcribed with section citations, exactly as the
other twenty modules were built. That is the next rules task, and it blocks the hacking UI's legality
checks.

## Godot slice: what exists, and what does not

*(A Godot-side audit is being written separately; this section records only what is measurable from the repository tree.)*

Measured from the tree:

| Element | State |
|---|---|
| `GameState` autoload (seeded RNG, scenario/dialogue/evidence loading, psionics wiring) | present (`godot/core/game_state.gd`) |
| rules bridge reading `data/rules/wn_core.json` | present (`godot/core/rules_adapter.gd`) |
| investigation bridge | present (`godot/core/investigation_adapter.gd`) |
| playable location scenes | **`hospital.tscn` only**; one scenario (`lakkahaltia`) |
| Home / UNSA HQ / test-mission scenes | **absent** |
| node-link hacking screen | **absent** — `rules_adapter.gd` contains no hacking calls at all |
| headless test scripts | 10 (`godot/tests/*.gd`) |
| **ability to run them here** | **no `godot` binary on this host** — the GDScript suite is unverified from this machine |

That last row matters: any GDScript I add from here would be unverifiable, so this pass deliberately
changes no engine code.

## Reuse decision (issue task A3)

Reuse `godot/core/*` adapters, the seeded `GameState`, the `lakkahaltia` scenario data shape and the
headless test harness. Add Home/HQ/mission as **new scenario directories** in the same shape rather than
forking the level builder, so the existing Lakkahaltia slice keeps working.

## Licensing

CWN SRD is CC0 per `data/sources/game_system_rights.json`; no CWN prose is copied, only rules procedures.
SWN Revised **has no verified grant** in the ledger — the psionics module therefore implements mechanics
(not copyrightable) without reproducing text, and distribution review remains open. Recorded here rather
than assumed settled.

## Ordered next increments

1. **Hacking resolution API** — transcribe Verbs/programs/CPU with SRD section citations, extend
   `cwn_hacking.py`, tests first. Unblocks the hacking screen and #749's fourth acceptance criterion.
2. **Home → HQ → mission scenario data** — three scenario directories, dialogue/evidence in the
   existing shape; no engine change needed to reach "playable without console commands".
3. **Node-link hacking screen** — consumes (1); the visual graph is scenario state, the legality check is
   the rules API.
4. **Save/load of mission state** — `GameState` already owns the state; add the serialise/restore path
   and a headless test.
5. **Playtest on a machine with Godot** — required before any acceptance criterion about the running game
   can be marked met.

## What this document does *not* claim

- It does not claim the MVP is playable: only `hospital.tscn` exists, and no windowed run has happened.
- It does not claim full CWN coverage: the hacking catalogue is absent, and the matrix above is the
  evidence for that statement rather than a promise about the rest.
- It does not claim the GDScript tests pass: there is no Godot binary here to run them.
