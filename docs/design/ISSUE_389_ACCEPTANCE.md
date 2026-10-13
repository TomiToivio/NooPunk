# Issue #389 — acceptance record

**What this file is.** The criterion-by-criterion verification behind closing *"Implement Fate Core /
Transhumanity's Fate-inspired Creative Commons RPG layer for NoöPunk Global Strategy"*, whose last
criterion is *"close this issue only after all acceptance items genuinely hold"*.

**Work attribution, stated plainly because two sessions converged on the same gaps.**

- **PR #392** (a sibling session, merged first) delivered the three items the first slice had left
  undone: `rpg/ATTRIBUTION.md`, `rpg/ports.py` — the adapter boundary to the strategy layer — and
  `demo_netrunning`, with `tests/test_rpg_boundary.py`.
- **This PR** delivers the acceptance item that remained open after #392: criterion 1's **"aspects/TAGs"**.
  `Character.tags` now uses issue #346's shared typed vocabulary through the same `Tag` type the
  faction and card layers use, with a duplicate guard and `tags_of_kind()`, and
  `tests/test_rpg_character_tags.py` adds 8 tests — including the one that matters most: **a TAG must
  not be a hidden modifier**, so two characters with identical skills and different tags roll
  identically for the same seed.
- **A duplicate was closed as superseded.** PR #393 built the attribution, boundary and netrunning
  items independently and in parallel with #392; it conflicted and was closed rather than force-landed.
  Nothing from it is claimed here beyond the TAG work re-landed in this PR.

## The nine acceptance criteria

| # | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| 1 | Independent `strategy_game/rpg/` package with documentation, Fate attribution, character identity, aspects/**TAGs**, skills, stress/consequences, Fate points, stunts, gear and bodily state | `rpg/{__init__,fate,ports}.py`, `rpg/README.md`, `rpg/ATTRIBUTION.md` (#392) + **typed TAGs this PR**: `Character.tags`, `tags_of_kind()`, duplicate and type guards, `tests/test_rpg_character_tags.py` | met |
| 2 | 4dF and the four actions, pure seeded deterministic resolution, outcomes/ties/shifts, scene pacing and GM judgment explicit | `roll_fate`, `Action`, `resolve` with `Outcome` and computed `shifts`; docstrings keep adjudication with the caller | met (first slice, PR #390) |
| 3 | Natural PSI separate from disease/infection/enhancement/tech; psychic investigation **and BCI netrunning** examples | `natural_psi` + `psi_abilities` guard; `demo_investigation` (cyber + PSI, one engine); `demo_netrunning` (#392) models the foothold first, per #344 | met |
| 4 | Biological body default; optional rare stack/resleeving, never mandated; no Eclipse Phase canon | `body="original_biological"`, `cortical_stack=False`, `resleeved=False`; `ATTRIBUTION.md` and `README.md` restate the no-EP-canon rule | met |
| 5 | Unit tests: dice bounds, seeded reproducibility, aspect invocation accounting, stress/consequence processing, no auto-PSI-by-virus, no forced stack/resleeving | `tests/test_fate_rpg.py` (#390) + `tests/test_rpg_boundary.py` (#392) + `tests/test_rpg_character_tags.py` (this PR); the RPG-area globs run **33 OK** | met |
| 6 | One short investigation scene resolving a cyber check and a PSI check on the same engine | `demo_investigation`, asserted reproducible per seed and using `Action.OVERCOME` for cyber, `Action.CREATE_ADVANTAGE` for PSI | met |
| 7 | A clean adapter boundary separating faction strategy/simulation, without inventing its mechanics | `rpg/ports.py` (#392) — sheets and seeded, replayable checks outward, with the exclusions declared and nothing joined to `WorldState` | met |
| 8 | `strategy_game/RULEBOOK.md` and README accurate: Fate approved **for the RPG layer**, strategy/political pending | `RULEBOOK.md` status line; `strategy_game/README.md` #389 paragraph; `rpg/README.md`. No strategy or political rule was added by any of this work | met |
| 9 | Git commit, PR, tests; close only when every item holds | this PR + #392 + #390; verified with real runs: **`strategy_game` package 943 OK**, root **509 OK**, RPG-area globs **33 OK** | met |

## Measured state at closure

```
strategy_game/tests (CI step, -p "test_*.py")      943 OK
tests/ (root CI step, -p "test_*.py")              509 OK
RPG-area globs (fate, rpg_boundary, rpg_character_tags)  33 OK
```

An earlier run of this layer showed **8 failures in `tests/test_board_local_projection.py`** — the
board-projection regression that **PR #391** fixed. They are recorded here because they were real at
the time, and they are now green on `main`; none of them ever touched the RPG layer.

## Not claimed

- The layer is an **MVP slice**. `rpg/README.md` keeps its "not yet implemented" list (reroll
  invocations, full four-action outcome tables, complete damage/concession exchange, full character
  generation, cyber/PSI countermeasure requirements). Those are future work tracked by #344, #345,
  #347 and #323 — not unmet criteria of #389, and nothing presents them as done.
- **No strategy or political mechanic is approved** by this closure.
- **No Eclipse Phase or Transhumanity's Fate text, art or setting content is reproduced**, and the
  licence under which NoöPunk distributes its own code remains the author's decision (gate #200),
  not the agent's.
