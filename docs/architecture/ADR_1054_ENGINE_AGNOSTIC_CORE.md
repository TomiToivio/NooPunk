# ADR 1054 — immutable CWN tabletop core, optional mods, one engine-agnostic Python rules engine

**Status:** accepted (binding for all future NoöPunk work)
**Issues:** #1054 (decision), #1053 (executable migration), #1006 (rules constitution), #1025 (CWN parity)
**Enforced by:** `tools/check_engine_boundary.py`, `tools/check_godot_rule_duplicates.py`,
`tools/rules_constitution_audit.py`, `tests/test_console_case_1053.py`,
`mud/tests/test_session_adapter_1053.py`, `tests/test_rules_constitution_modules.py`

## Decision

1. **CWN is immutable.** No change to published Cities Without Number mechanics — not to rebalance,
   simplify, reinterpret or replace. SWN/WWN/AWN are supplementary rule modules with documented
   precedence; NoöPunk additions are **additive mods**, never forks.
2. **One Python rules engine is the only authority.** Rules live in importable modules; no front-end
   (Evennia, Concordia, Pygame, a browser, a Godot scene) may hold a mechanic that the library does not.
3. **Front-ends are adapters.** Adding an engine must mean adding an adapter, never rewriting a rule.
4. **Tabletop first.** Every rule and mod must be playable with a rulebook, paper and dice. Software is
   convenience, not a prerequisite.
5. **Rulebook ↔ Python synchronization is a merge gate.** A rule change updates documentation, code and
   tests in the same pull request.

## Where the decision already holds in this repository

The decision is not aspirational; the repository's shape already implements most of it. Measured at the
time of writing:

| layer | location | size | engine imports |
| --- | --- | --- | --- |
| domain rules | `src/rules/` | 73 modules, ~15.5k lines | **none** |
| application (campaign, world state, console) | `mud/nopunk_mud/` | 23 modules, ~3.4k lines | **none** |
| Evennia adapter | `mud/typeclasses/`, `mud/commands/`, `mud/server/conf/`, `mud/world/` | 10 modules | Evennia (expected) |
| Godot adapter | `godot/core/` | 52 GDScript modules, 271 functions | Godot (expected) |
| Godot-side mods | `mods/noopunk/*.gd` | 4 scripts | Godot (expected) |

Two facts follow, and both are checkable rather than asserted:

- `src/rules` and `mud/nopunk_mud` import **no** engine, UI, storage or model package. That is what
  `tools/check_engine_boundary.py --check` proves on every run, and what
  `test_the_domain_layer_imports_with_every_engine_blocked` proves in a subprocess whose import hook
  refuses evennia, twisted, pygame, mesa, streamlit, sqlalchemy, pymongo, redis, openai and anthropic.
- Godot holds a parallel GDScript implementation of CWN mechanics. That is *permitted* as an adapter
  only because it is tracked: `tools/check_godot_rule_duplicates.py` reports `0 known duplicate domains,
  no new ones`, so a GDScript rule that diverges from `src/rules` fails a check instead of drifting.

## Component inventory (what exists today, not what is planned)

| piece | where | state |
| --- | --- | --- |
| rules kernel (attributes, checks, combat, strain, saves) | `mud/nopunk_mud/cwn_core.py` + `src/rules/` | implemented, tested |
| campaign engine (commands, state, endings, save/load, seeded RNG) | `mud/nopunk_mud/campaign/engine.py` | implemented, tested |
| typed adapter boundary (`Action` → `ActionResult` + events) | `mud/nopunk_mud/session.py` | implemented, tested |
| console slice (plain text, no engine) | `mud/nopunk_mud/cli_console.py`, flags in `cli.py` | implemented, tested |
| social layer (rank, scoped reputation) | `mud/nopunk_mud/social.py` | implemented, tested |
| ideology layer (DA/DNA/SNA) | `mud/nopunk_mud/ideology.py` | implemented, tested |
| Evennia adapter | `mud/commands/`, `mud/typeclasses/` | exists, owns no rule |

## The boundary rule, stated so it can be broken visibly

> A module under `src/rules/` or `mud/nopunk_mud/` may import the standard library, other rule modules,
> and `src.rules.*` / `nopunk_mud.*`. It may not import an engine, a UI toolkit, a database driver, or a
> model provider.

Violations are reported with `file:line: imports <package>` and exit non-zero. Forbidden roots are listed
in one place (`FORBIDDEN` in the tool) precisely so the rule can be widened — adding a new front-end is a
one-line change to the boundary, not a refactor.

## Mods contract

A mod is a module that declares:

| requirement | today |
| --- | --- |
| activation | explicit construction/injection; nothing is registered globally |
| conflict handling | a mod may **not** write into a CWN calculation; it reads state and returns advisory results |
| state changes | through the campaign/engine transition function, never by mutating another layer's objects |
| serialization | the mod's state lives in the campaign snapshot, versioned with it |
| tests | each mod ships its own tests; a mod without tests is not a mod, it is a sketch |
| tabletop equivalent | documented manual procedure, or the mod may not claim to be playable |

The constitution already classifies every `src/rules` module by tier (`cwn-core`, `swn-companion`,
`optional-source`, `noopunk-mod`, `legacy`) and refuses an unclassified one — `tools/
rules_constitution_audit.py`. That is the enforcement half of "mods are additive": a `cwn-core` module
importing a `noopunk-mod` module fails the audit, so no overlay can hide inside the baseline.

## Stable API surface (what adapters may call)

| concern | entry point |
| --- | --- |
| domain rules | `src.rules.*` — pure functions and dataclasses, no global state |
| campaign orchestration | `nopunk_mud.campaign.CampaignEngine` — `command(line)` in, text out; state in `engine.state` |
| typed adapter boundary | `nopunk_mud.session.CampaignSession.execute(Action) -> ActionResult(text, events, state, finished)`; events are derived from the state transition, never from prose |
| persistence | `CampaignEngine.to_dict()` / `.from_dict()` — versioned schema, RNG state included |
| determinism | `CampaignEngine(seed=…)` — the same seed and commands replay exactly |
| console adapter | `python -m nopunk_mud.cli --campaign [--seed N] [--save PATH] [--load PATH] [--script …]` |
| Evennia adapter | `mud/typeclasses`, `mud/commands` call the same engine; they hold no rules |
| Godot adapter | `godot/core` reads the shared kernel; parity tracked by the duplicate check |

Adding Concordia or Pygame therefore means: a new adapter directory, calls into the two rows above, and a
seeded cross-adapter test. Nothing in `src/rules` changes.

## Consequences

- A rule implemented *only* in an adapter is a bug: the boundary check and the duplicate check both fail.
- A rule change that does not touch the rulebook is incomplete (see the traceability matrix in
  `docs/rules/`, and `RULES_CONSTITUTION.md` for the source precedence).
- The console slice is the reference implementation of the API; if the console cannot play a case, the
  API is not finished, whatever the other adapters do.
- Performance work happens in the rules layer, once, for every front-end.

## What this ADR does not settle

- **Packaging/distribution names** (`noopunk.rules` vs the current `src.rules`): the import path is a
  packaging decision deferred to the packaging increment; the boundary holds either way, and today's
  modules are importable exactly as they are.
- **Concordia/Pygame adapters**: deferred until the console campaign milestone is met, per #1054 §5
  Milestone B.
- **SWN faction strategy**: deferred to Milestone C.
