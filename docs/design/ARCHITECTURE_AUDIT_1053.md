# Architecture survey for #1053 (Priority 0, first bullet)

> **Superseded:** [ISSUE_1053_ARCHITECTURE_SURVEY.md](/docs/architecture/ISSUE_1053_ARCHITECTURE_SURVEY.md) is the one document kept up to date for this
> subject. This file is kept as history — it is a second answer to a question that already had one,
> and the counts in it disagree with the audited ones. Do not update it; update the canonical file.


Status: survey of `main` at the time of the console-slice pull request. Measured, not remembered —
the counts below come from the tree, and the commands that produce them are quoted so the next agent
can re-run them instead of trusting this file.

```
ls src/rules/*.py | wc -l                       -> 73
ls src/rules/cwn_*.py | wc -l                   -> 26
ls src/rules/swn_*.py | wc -l                   -> 9
find . -name '*.gd' -not -path './.git/*' | wc -l -> 179   (godot/core: 52)
find mud -name '*.py' | wc -l                   -> 74
ls tests/test_*.py | wc -l                      -> 133
```

## What already exists, and where the authority sits

| area | location | state | authority |
| --- | --- | --- | --- |
| CWN rules (combat, injury, strain, cyberware, hacking, equipment, advancement, mission time, NPCs, vehicles, drones) | `src/rules/cwn_*.py` (26 modules) | implemented, extensively tested (`tests/test_cwn_*.py`) | **canonical** |
| SWN supplements (psionics, faction turns, sector, starships, transhuman) | `src/rules/swn_*.py` (9) | implemented where the first campaign needs them | **canonical for those rules** |
| AWN | `src/rules/awn_survival.py` | one survival module | **canonical for that rule** |
| NoöPunk mods (tags, narrative moves, Noösphere projection, crisis contact, social extensions, mod boundary) | `src/rules/noopunk_*.py`, `narrative_*` (8) | additive layer | **canonical** |
| Investigation layer (GUMSHOE core-clue principle on the CWN chassis) | `src/rules/investigation.py`, `investigation_evidence.py`, `anomaly_gate.py` | implemented, case graph on disk | **canonical** |
| Text engine (actions, events, actors, persistence, sheets) | `src/text_game/`, `src/simulation/` | implemented; fixture/prefall scenarios | canonical for the loop |
| Evennia MUD | `mud/` (74 modules) | live adapter **plus its own CWN port** (`mud/nopunk_mud/cwn/`) | port, kept honest by `tests/test_cwn_mud_parity_1025.py` (ADR #946) |
| Godot edition | `godot/` (52 rule scripts in `godot/core/`) | legacy/reference; rules duplicated in GDScript | **not authoritative** (DESIGN_PRINCIPLES §4) |
| Archived Godot edition | `noopunk/game/` | archive | not authoritative |
| Crossover strategy game | `strategy_game/` | documentation only, **NO RULES APPROVED** | not authoritative |

So the rules are not missing: they exist, they are extensive, and they are tested. What was missing was
a way to *reach* them.

## Duplication found (and what keeps it honest)

1. **`mud/nopunk_mud/cwn/combat.py`, `initiative.py`** re-implement attribute modifiers, saves, HP and
   Strain instead of importing `src/rules`. This is a deliberate ADR #946 decision — the MUD is its own
   deployment unit — and it is policed by a parity test that compares the three implementations.
   It is still a second copy of the same rule, and it is the first thing the new package boundary can
   retire: now that the rules install (`pip install -e .`), a MUD that imports them no longer couples
   anything it does not already depend on.
2. **`godot/core/*.gd`** carries 52 rule scripts (combat, strain, alienation, stress…). Reference only;
   no parity harness of the same rigour. Any revived Godot edition needs an adapter/interop strategy,
   not a fourth implementation.
3. **`src/eclipse_phase_homebrew/`** is a quarantined NC-SA prototype: imported by the text game and
   Concordia runtime, listed in `data/licenses/release_packaging_policy.json`. Not a rules duplicate,
   but it must never leak into a redistributable bundle.

## Engine coupling found

* `src/rules/**` imports **no** engine. Verified by the console test that asserts importing the rules
  and the console leaves `evennia`, `pygame` and `concordia` out of `sys.modules`.
* `mud/` imports `src.rules` in exactly one place (`cwn_mission_time`), and otherwise uses its own port:
  the coupling is one-directional and narrow.
* Five files in `src/` and `scripts/` still put `src/` on `sys.path` by hand at import time. That is the
  symptom the packaging work fixes: those are executable entry points that could not be imported.

## Gaps this pull request closes

| gap from #1053 / #1054 | before | after |
| --- | --- | --- |
| importable, distributable package | only runnable from a checkout with hand-inserted `sys.path` | `pyproject.toml` (setuptools, `src/` layout) → `pip install -e .`, `noopunk-case` console script |
| engine-independent action/session API with versioned state | the engine had actions/events, but no versioned *campaign* state a save could round-trip | `src/console/session.py`: `STATE_VERSION`, `to_dict`/`from_dict`, refuses unknown versions and foreign cases |
| deterministic RNG interface | seeding existed in the engine; the case layer had none | `random.Random` injected; its exact state is saved and restored (test: resumed run == uninterrupted run) |
| a console slice that plays the **case**, not a room fixture | `scripts/noopunk_text.py` plays `prefall` / `issue74` / `fixture` rooms; the Lakkahaltia case existed only as rules + data | `scripts/noopunk_case.py` / `python -m console` plays `data/scenarios/lakkahaltia/case_graph.json` end to end |
| automated proof that rules import and run with no engine | no such test | `tests/test_console_case_1053.py` (22 tests), including a subprocess import check |
| a complete playable path with save/load | not for the case layer | scripted walkthrough (`docs/examples/lakkahaltia_walkthrough.txt`), save at any turn, resume |

## Gaps this pull request does **not** close (deferred, explicitly)

1. **`noopunk.rules` naming.** The installable distributions are still top-level `rules`, `console`,
   `text_game`… The target namespace in `docs/DESIGN_PRINCIPLES.md` §4 is `noopunk.*`. Renaming 73 rule
   modules in the same PR as the first playable slice would bury the slice in import churn; it needs its
   own PR with a compatibility shim (`noopunk.rules` re-exporting, tests asserting object identity).
2. **Retiring the MUD's CWN port.** Now feasible; not done here, because it changes the MUD deployment
   unit and needs its own parity run.
3. **Evennia / Concordia / Pygame adapters over the new session API.** The session is deliberately
   engine-neutral and JSON-serialisable so an adapter only has to map commands to it; none is written yet.
4. **Cross-adapter equivalence test** (same seed, same actions, identical outcomes in console and MUD).
   Requires (3).
5. **Rulebook ↔ code synchronisation** (§6 of #1054). The walkthrough file is the first artefact of it —
   it is the same command sequence a table plays — but the full mapping table is not written.
6. **SWN faction strategy / board/card conversions** (Milestone C). Untouched, per prioritisation.

## A second surface that had to be consolidated

`portable_noopunk/` and `mud/nopunk_mud/portable*.py` landed on `main` in the same minutes as this
slice, each with its own idea of a playable case. `portable_noopunk` was a self-contained narrative
prototype — invented locations (`unsa_hq`, `hospital`, `library`), invented clues (`anomalous_clock`,
`witness_statement`) and a sidequest that exists nowhere in the case material — i.e. a second game that
also invented canon. It is now a façade over `console.session.CaseSession` (see
`docs/PORTABLE_CONSOLE_CASE.md`), with its frontends unchanged. `mud/nopunk_mud/portable.py` still drives
the MUD's own campaign and its CWN port; retiring that is item 3 below.

## Order of work this survey recommends

1. (this PR) installable package + engine-independent session + console slice + tests.
2. `noopunk.*` namespace with re-export shims; delete the shims' need by rewriting imports in one sweep.
3. Evennia adapter over the session API; then retire `mud/nopunk_mud/cwn/` behind the parity test.
4. Rulebook walkthrough table (§6) generated from the same example scripts the tests replay.
5. Concordia and Pygame adapters; then the cross-adapter equivalence suite.
