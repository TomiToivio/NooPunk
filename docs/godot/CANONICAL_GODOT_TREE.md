# The canonical Godot tree (agent rule)

**Measured 2026-10-30.** Several agents worked in parallel and did not land in the same place. This
document records what exists, which tree is authoritative, and what must not happen again.

## What the audit found

| Tree | Files | Role today |
|---|---|---|
| `src/godot/` | 15 | engine-independent rules: `campaign_state`, `case_state`, `core_rules`, `cwn_rules`, `wn_rules`, `swn_psionics`, `lakkahaltia_case`, `network_map`, `title`, and `src/godot/cwn/` (catalogue, character, combat, combat_rules, encumbrance, hacking, healing, programs, program_rules) |
| `godot/core/` | 20 | scene-side kernels and adapters: `combat`, `game_state`, `dice`, `investigation_adapter`, `psionics`, `psychic_effort`, `rules_adapter`, `scene_flow`, `session`, plus CWN copies |
| `godot/tests/` | 20 | the suite CI runs (`godot --headless --script res://godot/tests/run_tests.gd`) |
| `tests/godot/` | 15 | **a second test root**, run by nothing in CI |

**Real duplicated implementations, each wired to a different test root:**

| Module | `src/godot/` | `godot/core/` | Preloaded by |
|---|---|---|---|
| `cwn_catalogue.gd` | 8,309 B | 8,090 B | `godot/tests/test_cwn_engine.gd` → src; `godot/tests/test_cwn_catalogue.gd` → core |
| `cwn_character.gd` | 4,237 B | 5,447 B | `tests/godot/test_cwn_ruleset.gd` → core |

That is the defect: two catalogues and two character implementations, both alive, both tested, neither
obviously wrong. A rule change made in one is silently absent from the other.

## The rule

1. **`src/godot/` is the single home for CWN/SWN rule logic and rule data.** Any new rule module goes
   there, under `src/godot/` or `src/godot/cwn/`.
2. **`godot/core/` is for scene-side and engine glue only** — adapters that read rule data, autoloads,
   scene flow, RNG plumbing. It may call into `src/godot/`; it may not contain a second copy of a rule.
3. **`godot/tests/` is the only test root that CI runs.** `tests/godot/` is legacy: no new tests go
   there, and files move out of it as they are touched.
4. **A basename may not exist in both `src/godot/` and `godot/core/`.** `tests/test_godot_single_implementation.py`
   enforces this and will fail CI if a duplicate reappears.
5. When two agents touch the same mechanic, the second one reads this file first and extends the
   canonical module rather than writing a parallel one.

## Known debt this guard does not pretend is fixed

**Four Godot workflows** currently reference the legacy root: `godot-smoke.yml`, `cwn-progression.yml`,
`cwn-godot-rules.yml`, `godot.yml`. They grew in parallel and are listed in the guard as known debt, so
the guard fails on a *new* stray rather than on history. Folding them into one workflow is part of the
migration below.

## Migration, in the order it should happen

1. `godot/core/cwn_catalogue.gd` → delete; repoint `godot/tests/test_cwn_catalogue.gd` at
   `res://src/godot/cwn/cwn_catalogue.gd`, folding in anything unique to the core copy (it has
   `apply_soak`, the src copy may not).
2. `godot/core/cwn_character.gd` → delete; repoint `tests/godot/test_cwn_ruleset.gd` likewise.
3. Move the surviving `tests/godot/*.gd` files into `godot/tests/` and delete the second root.
4. Fold the four Godot workflows into one that runs `godot/tests/run_tests.gd`, then delete
   `tests/godot/` and the four names from `KNOWN_LEGACY_WORKFLOWS`.
5. Re-run `godot --headless --script res://godot/tests/run_tests.gd`; the count must not drop.

Until step 1–2 are done, the guard test allows exactly these two names as known duplicates, so it
cannot be used to hide a third.
