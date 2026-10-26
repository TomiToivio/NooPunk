# CWN movement, craft and crisis layer: what landed, and where the gaps are

> **Status:** implementation record for #564 / #652, 2026-10-26. This is a
> *procedure* document: it describes code that exists and the SRD section each
> part comes from. It does not introduce a rule the contracts do not carry.

The rules authority is `rulebook/WITHOUT_NUMBER_BASELINE.md`. The contract is
data: `data/rules/cwn_vehicles.json`, `data/rules/cwn_gear_mods.json`,
`data/rules/awn_survival.json`, `data/rules/wwn_projects.json`. The kernels are
`src/rules/cwn_vehicles.py`, `cwn_gear_mods.py`, `awn_survival.py`,
`wwn_projects.py`. Nothing else may restate these numbers.

## 1. What this increment adds to the chassis

Before this change the ported CWN procedures were attributes, checks, saves,
attacks, Shock/Trauma, mortal and Major Injuries, System Strain, healing,
encumbrance, advancement, cyberware, hacking, drones, Edges/Foci and the
equipment catalogue. The chapters that had no home were the *movement* layer and
the *craft* layer:

| Subsystem | Governing source | Module |
| --- | --- | --- |
| Hull table, fittings, vehicle mods, vehicle-only weapons | CWN 3.7 | `cwn_vehicles` |
| Vehicle combat: moving/stationary AC, Armor, destruction, crashes, ramming, vehicle Traumatic Hits | CWN 2.5.1 | `cwn_vehicles` |
| Foot and vehicle chases | CWN 2.6.1 / 2.6.2 | `cwn_vehicles` |
| Crafting, gear mods, mod maintenance, factory mods | CWN 2.8 | `cwn_gear_mods` |
| Weapon, armour, drone and cyberdeck mods | CWN 3.1.3, 3.4.5, 3.8.2, 3.9.1 | `cwn_gear_mods` |
| Crisis-zone travel, supplies, privation, foraging | AWN: travel, supplies, privation | `awn_survival` |
| Major projects (Renown) | WWN: Major Projects | `wwn_projects` |

## 2. The four rules that were easy to flatten

1. **Armor comes off after the Trauma multiplier.** A Traumatic Hit multiplies
   the whole damage roll; only then does the hull's Armor subtract. Computing
   `(damage - armor) x 3` under-damages every armoured vehicle by two thirds of
   its Armor.
2. **A tie in a chase is an escape.** Both chase procedures require the pursuer
   to *strictly* exceed the fleeing total, so `>=` would turn every tie into a
   capture.
3. **Min. Size is a floor and Power/Mass are budgets.** `fit_out()` raises on an
   over-budget build rather than clamping it, because a silently trimmed build
   hides the gun that was never mounted.
4. **Mod bonuses to hit, damage and Shock cap at +3 combined**, and Shock Burst's
   2d6 is explicitly outside that cap. The kernel reports it as a separate
   `uncapped_damage` value instead of folding it into `damage_bonus`.

## 3. What is deliberately not modelled

- **Vehicle chase distance.** The SRD abstracts it; every vehicle in a fray is
  in shooting range. There is no grid and no facing.
- **The AWN forage-difficulty-by-terrain table.** It was not transcribed, so
  `forage()` takes the difficulty from the caller and the contract records the
  gap (`foraging.difficulty_table_transcribed: false`).
- **The WWN money-per-Renown ladder.** Not transcribed either;
  `wwn_projects.money_purchase_is_modelled()` returns `False` rather than
  inventing prices. A referee who wants cash-for-progress supplies their own.
- **Equipment, Focus and Edge text.** These are author content, not procedure.

## 4. Licence boundary

| Source | Terms | What was done |
| --- | --- | --- |
| CWN SRD | CC0, verified | Tables transcribed as data; prose written fresh |
| WWN SRD | CC0, verified | The Renown procedure re-expressed; no source sentences |
| SWN Revised | no verified SRD licence | Psionic *shape* only; the technique catalogue is authored NoöPunk content |
| AWN | no verified open licence | Procedure re-expressed independently; no text, table heading or hazard list copied |

The rights record is `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`; the
similarity audit is `tools/audit_without_number_expression.py`.

## 5. The first case: making "all of it" falsifiable

`data/scenarios/lakkahaltia/chassis_drill.json` names one beat per subsystem and
`src/rules/first_case_drill.py` runs them through the real kernels on one seed.
`tests/test_first_case_drill.py` asserts that no required subsystem is missing,
that a typo'd tag cannot fake coverage, that every beat has a handler and every
handler a beat, that one seed reproduces the whole log, and that the sheet can
actually make the checks the drill asks for (a skill the sheet lacks would
otherwise resolve as untrained, `-1`, in silence).

Run it directly:

```bash
PYTHONPATH=. python3 -c "from src.rules.first_case_drill import run_drill; print(run_drill().log())"
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_first_case_drill.py"
```

That drill is the *coverage* path. The Godot slice
(`godot/scenarios/lakkahaltia/`) remains the player-facing path, and the Godot
side still needs the same beats wired into its dialogue graph.
