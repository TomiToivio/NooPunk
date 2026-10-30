> **See also:** [`CWN_SRD_PARITY_858.md`](CWN_SRD_PARITY_858.md) — the four-column audit (code / tested / playable / verified SRD parity) required by #858. This matrix lists what is implemented; that file asks whether it is *right* and *reachable*.

# CWN / SWN rules coverage matrix (#749 work package A, refreshed for #848)

**Status:** measured audit, 2026-10-30, against baseline commit `d2992fc`. This is *measurement*, not
a claim of completeness. Every number below came from enumerating the repository and running the
suites on this machine.

**Authority.** `rulebook/WITHOUT_NUMBER_BASELINE.md` governs the rules (CWN is the chassis; SWN Revised
supplies psionics, space operations and faction turns; AWN crisis survival; WWN exploration and
projects), and `AGENTS.md` governs how agents work. Where this matrix disagrees with either, they win.

## How this was measured

```bash
python3 -m pytest tests -q                                  # 1598 passed, 2998 subtests
python3 -m pytest tests -q -k "cwn"                          #  459 passed, 1139 deselected
ls src/rules/cwn_*.py | wc -l                               #   21 modules (4,569 lines)
ls godot/core/*.gd | wc -l                                  #   28 kernels
ls godot/tests/*.gd | wc -l                                 #   28 suites

godot --headless --path . --script res://tools/run_godot_tests.gd
                                                            # 89 tests, 595 checks, 0 failures
godot --headless --path . --script res://godot/tests/run_tests.gd
                                                            # 760 checks, 0 failed
godot --headless --path . --quit-after 90                   # launches into scenes/main.tscn, no errors
```

`data/rules/cwn_coverage.json` is the machine registry of implemented procedures: **30 modules, 285
procedures**, regenerated and checked by `tests/test_cwn_coverage_manifest.py`. Presence in that
registry is code coverage, not SRD parity.

## Matrix

Status vocabulary: **implemented** = procedure exists and is tested; **partial** = the rules object
exists but a documented part of the procedure does not; **absent** = nothing yet.

| CWN area | Python module | Godot kernel | Tests | Status |
|---|---|---|---|---|
| attributes, modifiers, 2d6 checks, saves | `cwn_core.py`, `wn_core.py` | `cwn_character.gd`, `rules_adapter.gd`, `dice.gd` | `test_cwn_core.py`, `test_wn_core.py`, `test_rules_adapter.gd` | implemented |
| character creation: scores, backgrounds, Edges, Foci, skills | `cwn_character.py`, `cwn_backgrounds.py`, `cwn_edges_foci.py`, `cwn_foci.py` | `cwn_character.gd`, `field_agent.gd` | `test_cwn_character.py`, `test_cwn_backgrounds.py`, `test_cwn_edges_foci.py`, `test_cwn_foci.py`, `test_cwn_party.gd` | implemented |
| advancement and attack bonus | `cwn_advancement.py` | `cwn_progression.gd` | `test_cwn_advancement.py` | implemented |
| attack resolution, modifiers, cover, suppression | `cwn_combat.py`, `cwn_attack_modifiers.py`, `cwn_combat_actions.py` | `combat.gd`, `cwn_combat_rules.gd`, `cwn_combat_actions.gd` | `test_cwn_combat.py`, `test_cwn_attack_modifiers.py`, `test_cwn_combat_actions.py`, `test_combat.gd` | implemented |
| Shock, Trauma, mortal injury, stabilization | `cwn_trauma.py`, `cwn_major_injury.py`, `cwn_injury_procedure.py`, `cwn_healing.py` | `cwn_injury.gd`, `cwn_healing.gd`, `cwn_combat_rules.gd` | `test_cwn_trauma.py`, `test_cwn_major_injury.py`, `test_cwn_injury_procedure.py`, `test_cwn_healing.py`, `test_cwn_injury.gd` | implemented |
| gear, weapons, armour, prices, encumbrance | `cwn_equipment.py`, `cwn_encumbrance.py`, `cwn_gear_mods.py` | `cwn_catalogue.gd`, `cwn_encumbrance.gd` | `test_cwn_equipment.py`, `test_cwn_encumbrance.py`, `test_cwn_gear_mods.py`, `test_cwn_catalogue.gd` | implemented |
| cyberware, installation, Strain, maintenance | `cwn_strain.py` | `cwn_strain.gd` | `test_cwn_strain.py` | implemented |
| hacking: Access, security ladder, connection penalties, alert clock | `cwn_hacking.py` | `cwn_hacking.gd`, `hacking.gd` | `test_cwn_hacking.py`, `test_cwn_hacking_contract.py`, `test_hacking.gd` | implemented |
| decks, Verbs, Subjects, programs, CPU slots, cost | `cwn_program_catalogue.py` | `cwn_programs.gd`, `cwn_program_rules.gd` | `test_cwn_program_catalogue.py`, `test_cwn_program_rules.gd` | implemented |
| drones | `cwn_drones.py` | `cwn_catalogue.gd` | `test_cwn_drones.py` | implemented |
| vehicles, fittings, vehicle combat, chases | `cwn_vehicles.py` | — | `test_cwn_vehicles.py` | Python implemented; **no Godot kernel** |
| psionics: disciplines, techniques, Effort, overexertion | `swn_psionics.py` | `psionics.gd`, `psychic_effort.gd` | `test_psionics_catalogue.py`, `test_psionics_gate.py` | implemented (SWN Revised) |
| psychic advancement | `swn_progression.py` | `swn_progression.gd` | `test_swn_progression.py`, `test_swn_progression_contract.py` | implemented (SWN Revised) |
| factions and faction turns | `swn_faction_operations.py`, `swn_faction_turn.py` | — | `test_swn_faction_operations.py` | partial — `swn_faction_turn.py` has no test |
| starships and space combat | `swn_starships.py` | — | `test_swn_starships.py` | Python implemented; **no Godot kernel** |
| sector generation | `swn_sector.py` | — | none | **partial — untested** |
| transhuman and true-AI procedures | `swn_transhuman.py`, `swn_true_ai.py` | — | none | **partial — untested** |
| AWN crisis survival, supplies, hazards | `awn_survival.py` | — | `test_awn_wwn_campaign_procedures.py` | Python implemented; no Godot kernel |
| session state: initiative, turns, save/load | — | `session.gd`, `game_state.gd`, `party.gd`, `scene_flow.gd` | `test_game_state.gd`, `test_session.gd`, `test_cwn_party.gd` | implemented — save v1 with `save_to_file`/`load_from_file` |
| top-down RPG slice: main menu → scenario → mission scene | — | `scenes/main.tscn`, `godot/ui/main_menu.gd`, `godot/ui/mvp_game.gd`, `godot/ui/hud.gd` | `godot/tests/run_tests.gd` (760 checks) | implemented and launchable headless |
| node-link hacking screen | — | — | — | **absent** — the rules API exists; no UI consumes it |
| tactical grid combat screen (CWN initiative, Move/Main economy) | — | kernels only | — | **absent** — the rules are implemented, the tactical presentation is not |

Scenarios on disk: `godot/scenarios/lakkahaltia` (hospital case) and `godot/scenarios/mvp_romppainen`.
Scenes: `scenes/main.tscn` (entry), `scenes/campaign.tscn`, `scenes/lakkahaltia/ward.tscn`,
`scenes/lakkahaltia/prototype.tscn`.

## Corrections to the 2026-10-28 audit

The earlier version of this document recorded three things that are no longer true, and #848 asks for
measurement rather than assertion:

1. **"Hacking catalogue absent."** It is implemented: `cwn_program_catalogue.json`,
   `cwn_program_catalogue.py`, `cwn_programs.gd`, `cwn_program_rules.gd`, plus
   `test_cwn_program_catalogue.py` and `test_cwn_program_rules.gd`.
2. **"GDScript tests not run — no Godot binary."** They run here: 89 tests / 595 checks and 760 checks,
   both zero failures, on Godot 4.7.2-stable.
3. **Module and suite counts.** 21 CWN Python modules (not 20), 28 Godot kernels (not 21), 28 Godot
   suites (not 10), 1598 Python tests (not 1452).

## Backlog: what is actually left

Ordered by what blocks a playable, source-faithful slice:

1. **Tactical grid combat screen** — CWN initiative, Move/Main economy, cover and suppression are
   implemented as kernels but have no playable presentation. This is the largest gap between
   "kernels tested" and "CWN as a game".
2. **Node-link hacking screen** — consumes the finished hacking/program API; the visual graph is
   scenario state, the legality check is the rules API.
3. **Godot kernels for vehicles, starships and AWN survival** — Python procedures exist and are tested;
   the engine cannot yet run them.
4. **Tests for `swn_faction_turn.py`, `swn_sector.py`, `swn_transhuman.py`, `swn_true_ai.py`** — four
   modules in the registry with no matching test file.
5. **Scenario spine** — Home → HQ → mission data in the existing shape; `lakkahaltia` and
   `mvp_romppainen` exist, a campaign-opening trio does not.
6. **Windowed playtest** — every claim above is from headless runs. A human has to play it before
   "playable" is asserted.

## What this document does not claim

- It does not claim SRD parity for every row. Status **implemented** means the procedure exists and is
  tested, not that a reviewer has compared it line by line against the source chapter.
- It does not claim the game is complete: the tactical combat screen and the hacking screen do not
  exist, and three subsystems are Python-only.
- It does not claim windowed behaviour. All Godot evidence here is headless.
