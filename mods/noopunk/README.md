# NoöPunk overlays

Everything here is an **overlay on Cities Without Number**, per
[`docs/design/FOUNDATIONAL_LOCK_897.md`](../../docs/design/FOUNDATIONAL_LOCK_897.md). Overlays colour the
game; they do not resolve it.

## The three rules

1. **No imports from `godot/core/` into `mods/`.** A mod may not compute core resolution — no dice, no
   attribute modifiers, no attack or save arithmetic. If a mod needs a roll, the caller asks the core and
   passes the result in.
2. **Return data, never mutate a core result in place.** Store overlay state beside the core value.
3. **Every overlay is optional and flagged.** Delete the folder and a table running CWN notices nothing
   missing.

`tests/test_foundational_lock_897.py` enforces rule 1 and the folder's existence; the overlay's own tests
cover its behaviour (`godot/tests/test_noopunk_psyche.gd`, `godot/tests/test_noopunk_investigation.gd`).

**Where a rule already has a home, the overlay does not repeat it.** GUMSHOE discovery is implemented
once, in `godot/core/investigation_adapter.gd` (#718) and `src/rules/investigation.py`; the investigation
overlay carries only what those do not — interpretation, which stays the player's act.

## What lives here

| Module | Overlay | Status |
| --- | --- | --- |
| `psyche.gd` | Noösphere exposure, Psyche tiers, recovery, active-PSI gate | implemented |
| *ideology* | Laclau-style identification, faction drift, antagonism | design only — needs a rule reference and tests before code |
| *obligations* | contact trust, debts, institutional standing | design only |
| `investigation.gd` | clue-forward framing: the system names evidence, the player decides | implemented (interpretation; discovery stays in `godot/core/investigation_adapter.gd`, #718) |

A new overlay is accepted when it has: a rule reference, examples, tests, and a flag that turns it off.
"Needs a mechanic" is not enough — the matrix in `docs/design/CORE_VS_MOD_MATRIX_897.md` gets the row
first.
