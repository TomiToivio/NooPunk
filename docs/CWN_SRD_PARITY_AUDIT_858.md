# CWN SRD parity audit ledger (issue #858)

> **Unverified until procedure-level evidence exists.** This is the first audit slice, not a completion certificate. It compares the public [CWN SRD navigation](https://cwn.quadrifons.com/) with the repository's measured [coverage matrix](CWN_COVERAGE_MATRIX.md). A tested kernel does not imply a playable interface or verbatim rules parity.

## Evidence rubric

For each named SRD procedure, record **four independent checks** before checking it off in #858:

1. **Code:** exact canonical `godot/` path and method; shared data path if used.
2. **Procedure test:** Godot test name with deterministic success, failure, limit and resource-spending cases, plus CI result for the *current* commit.
3. **Playable route:** canonical scene / keyboard or pointer interaction that allows a player or referee to invoke the procedure without scripting.
4. **SRD verification:** direct SRD chapter/anchor, reviewer comparison, and explicit exclusions. Python-only evidence does not count as Godot implementation.

Use `absent` when no Godot mechanism is found, `partial` when one or more required steps or UI routes are missing, and `pass` **only** when all four checks are demonstrated. Leave cells `unverified` when not individually inspected. Never infer pass from a module's name.

## Initial audit: highest-priority playable gaps

| SRD chapter / procedure | Code evidence on main at initial inspection | Test evidence | Player/referee route | Parity verdict |
|---|---|---|---|---|
| [Combat Initiative](https://cwn.quadrifons.com/the-rules-of-the-game/combat/combat-initiative/) | `godot/core/cwn_combat_actions.gd`, `godot/core/session.gd` (verify methods) | Godot suites exist; individual procedure not yet verified | No dedicated tactical interface in the matrix | **partial / unverified** |
| [Combat Actions](https://cwn.quadrifons.com/the-rules-of-the-game/combat/combat-actions/) | `godot/core/cwn_combat_actions.gd` | Individual action branches not yet mapped | `godot/ui/mvp_game.gd` exposes only C to start/advance an encounter | **partial / unverified** |
| [Attacks in Combat](https://cwn.quadrifons.com/the-rules-of-the-game/combat/attacks-in-combat/) | `godot/core/cwn_combat_rules.gd`, `godot/core/combat.gd` | `godot/tests/test_combat.gd` (not exhaustive) | No tactical targeting UI demonstrated | **partial / unverified** |
| [Hacking Mechanics](https://cwn.quadrifons.com/hacking/hacking-mechanics/) | `godot/core/cwn_hacking.gd` | `tests/test_cwn_hacking_contract.py` and Godot hacking tests | `godot/ui/mvp_game.gd` draws linked nodes but provides no node selection / verb execution route | **partial / unverified** |
| [Cyberspace Actions](https://cwn.quadrifons.com/hacking/cyberspace-actions/) | `godot/core/cwn_program_rules.gd` has preflight and resolution | `godot/tests/test_cwn_program_rules.gd` | No playable program selector or execution interface demonstrated | **partial / unverified** |
| [Vehicles](https://cwn.quadrifons.com/gear-vehicles-and-cyberware/vehicles/) | PR #856 merged `godot/core/cwn_vehicles.gd` | 21 checks were authored but **not run** in PR #856 environment | No vehicle deployment/repair/chase UI demonstrated | **partial / unverified** |

The preexisting coverage matrix's "implemented" statuses describe primarily *kernel coverage*. They must not be promoted to parity passes. PR #856 is now merged, so its Godot vehicle kernel must be inspected before further work instead of being rewritten.

## Remaining SRD navigation checklist for source-by-source verification

These are **unverified**, even where the coverage matrix names a corresponding kernel:

- **Character Creation:** Attributes; Skills; Backgrounds; Contacts; Edges; Foci; Focus Gear Budget; Final Character Creation Steps.
- **Rules of the Game:** Scenes, Rounds, and Mission Time; Saving Throws; Skill Checks; The Combat Sequence; Damage, Trauma, and Shock; Special Combat Maneuvers; Vehicle Combat; Mortal Injury and Stabilization; System Strain; Natural Healing, First Aid, and Poisons; Major Injuries; Chases and Pursuit; Character Advancement; Crafting Gear; Modifying Gear; Maintaining Mods; Factory Mods (the mirror spells it “Fcatory”); Encumbrance.
- **Gear, Vehicles, and Cyberware:** Mission Gear; Lifestyle Costs; Common Wages; Bribe Costs; Armor Terms, Types, Accessories and Mods; Weapon Stats, Firearms, Melee/Thrown Weapons, Heavy Weapons and Mods; Pharmaceuticals and Street Drugs; Installing Cyberware; Implant Complications; Cyberdoc Tools; Removing Cyberware; Concealing and Detecting Cyberware; Cyberware Maintenance; Skillplugs; Cyberware Mods; Body, Head, Skin, Limb, Sensory, Medical and Nerve Cyberware; Cyberware Alienation; Cyberdecks; Drones.
- **Hacking:** Cyberspace Basics; Acquiring and Writing Programs; Program Subjects; Program Verbs; Programs; Demons and Watchdogs.

The SRD mirror explicitly excludes some optional rules and the Antagonists & NPCs section. Record those as **out of scope for this mirror-based issue** rather than making up substitutes. If the repository later adopts the complete published SRD as a separate source, amend this ledger with the precise edition and decision.

## Work sequencing and safeguards

1. Complete one minimal vertical slice: initiative, Move/Main/On Turn/Instant action budget, targeting, cover, attack, Shock/Trauma, and finish/end turn. Call the already established CWN kernels. Add Godot deterministic tests and a canonical scene interaction, without a parallel project.
2. Complete a second slice: selectable node-link graph, loaded program/verb/subject, Access and CPU spending, legality preflight and check resolution; persist changes through existing session/save state. Do not invent graph networking or ICE rules.
3. Continue by SRD chapter with one small PR per cohesive procedure family; add evidence for every subsection rather than summarizing large chapters as complete.
4. Run both Godot headless suites and the launch smoke test on the candidate commit, then perform a **human windowed playtest** before asserting a playable pass.

Commands, from repository root:

```sh
godot --headless --path . --script res://tools/run_godot_tests.gd
godot --headless --path . --script res://godot/tests/run_tests.gd
godot --headless --path . --quit-after 90
python3 -m pytest tests -q
```

No test execution is claimed for this documentation-only audit PR. Keep #858 **open** until all non-optional published procedures are implemented, source-reviewed, exercised in Godot, and verified.
