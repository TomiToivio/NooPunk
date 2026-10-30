# Godot CWN hacking-verb increment (2026-10-30)

Source: https://cwn.quadrifons.com/hacking/programs/program-verbs/ and https://cwn.quadrifons.com/hacking/programs/

The new `godot/core/cwn_program_rules.gd` records all 24 listed vanilla CWN verbs with target family, Access cost, check modifier and self-termination. It validates loaded Verb/Subject availability, compatible targets, remaining Access, CPU and the Defend ally requirement; resolves expenditure and persistent slot accounting after the caller supplies a check result; and exposes disconnect termination decisions.

Test: `godot --headless --path . --script godot/tests/test_cwn_program_rules.gd`.

This increment **does not** implement the entire CWN rulebook or finished Godot gameplay. It does not implement subject catalog data, detailed effects for every verb (e.g. Kill, Glitch, Sabotage), opponent checks, deck preparation, ICE/Watchdogs, inventory/cyberware screens or battle integration. The host must combine this preflight with `CwnHackingRules.hacking_check()` and game state, only committing the result after validation. The community mirror itself omits optional rules and NPCs. Remaining coverage must be tested end-to-end in Godot before claiming completion.
