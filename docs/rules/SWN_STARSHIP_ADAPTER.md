# SWN starship adapter for NoöPunk

Source reference: Kevin Crawford, *Stars Without Number Revised* (2017), **Starships**, printed pp. 93–120. This module implements original reusable game abstractions inspired by its starship customization and combat domains; it does not claim to reproduce SWN's proprietary hull, fitting, weapon or ship-combat tables.

## Scope

`src/rules/swn_starships.py` supports hull capacity (mass/power/hardpoints), fittings, ship hit points, defenses, armor, a deterministic d20 weapon-hit resolver, and snapshot round-tripping. Installation is atomic: exceeding any capacity leaves the build unchanged. Attacks require an installed fitting and two operational ships.

**Design boundary:** `src/rules/swn_sector.py` manages route travel, fuel and time. The new module manages ship construction and simple encounters. NoöPunk personal combat remains governed by CWN, and this simplified vessel encounter is a NoöPunk placeholder, **not the authentic SWN bridge-department action system**.

## Scenario use

In the opening Helsinki investigations, use this only for unusual craft and remote probes when the plot needs mechanical resolution. Interstellar play can expand later after the NHI Crisis. Keep alien craft capability ambiguous: a local investigator need not know its exact hull stats.

## Still missing

* Complete SWN hull/fitting/weapon catalogue with independently drafted descriptions and carefully verified values
* Command points, bridge roles and round-by-round ship combat actions
* Ship crises, maintenance, repair, pursuit and travel integration
* Godot adapter and complete Godot smoke tests
* Sector generator, creature encounters, faction asset combat, AI and transhuman rules

## Test

`python -m unittest tests.test_swn_starships`
