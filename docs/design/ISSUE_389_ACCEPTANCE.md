# Issue #389 — acceptance record

**What this file is.** The criterion-by-criterion verification that the Fate Core RPG layer for
NoöPunk Global Strategy holds, at the point of closing the issue. The issue's own last criterion is
*"close this issue only after all acceptance items genuinely hold"*, so this record exists to make
that checkable rather than asserted.

**What closed the remaining gaps.** Three acceptance items were genuinely unmet by the first slice
(PR #390) and are delivered here:

1. **Fate attribution was dangling.** `rpg/fate.py` pointed at `ATTRIBUTION.md`, which did not exist,
   and the attribution lived only in prose. Now: [`rpg/ATTRIBUTION.md`](../../strategy_game/rpg/ATTRIBUTION.md)
   plus machine-readable constants in [`rpg/attribution.py`](../../strategy_game/rpg/attribution.py), so a
   test asserts the Fate Core attribution, the unofficial notice and the upstream licence distinctions
   are present. **The distribution licence is deliberately not chosen** — that is the author's decision
   (licence gate #200).
2. **Shared typed TAGs were missing** from the character model (criterion 1 asks for "aspects/TAGs").
   `Character.tags` now uses issue #346's vocabulary through the same `Tag` type the faction and card
   layers use, with a duplicate guard and `tags_of_kind()`.
3. **No adapter boundary existed** (criterion 7). [`rpg/boundary.py`](../../strategy_game/rpg/boundary.py)
   fills the reserved `strategy_game.ports.LeaderRPG` seam — the same move the text renderer makes for
   `MapProvider` — and declares in code what the layer is not. It joins nothing to `WorldState`, so no
   Gate D decision is performed.

Also added: a **netrunning example** (`demo_netrunning`) that models the foothold first and the
intrusion second, because criterion 3 asks for a BCI netrunning example alongside psychic
investigation, and issue #344 requires a credible connection rather than assumed remote access.

## The nine acceptance criteria

| # | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| 1 | Independent `strategy_game/rpg/` package with documentation, Fate attribution, character identity, aspects/TAGs, skills, stress/consequences, Fate points, stunts, gear and bodily state | `rpg/{__init__,fate,attribution,boundary}.py`, `rpg/README.md`, `rpg/ATTRIBUTION.md`; `Character` carries id, name, aspects, **tags**, skills, stunts, gear, fate_points, physical/mental stress, consequences, body/cortical_stack/resleeved | met (TAGs added here) |
| 2 | Standard Fate dice (4dF) and the four actions with pure seeded deterministic resolution and outcomes/ties/shifts; scene pacing and GM judgment left explicit | `roll_fate`, `Action` (overcome, create advantage, attack, defend), `resolve` with `Outcome` failure/tie/success/success-with-style and computed `shifts`; docstrings state that GM/scene adjudication is the caller's | met |
| 3 | Natural PSI kept separate from disease, infection, enhancements and tech; examples for psychic investigation **and BCI netrunning** | `natural_psi` + `psi_abilities` guarded so equipment alone grants no innate PSI; `demo_investigation` resolves a BCI cyber check and a PSI check on one engine; `demo_netrunning` adds the foothold-then-intrusion example | met (netrunning example added here) |
| 4 | Original NoöPunk context: biological body default, optional rare stack/resleeving, never mandated, no Eclipse Phase canon | `body="original_biological"` default, `cortical_stack=False`, `resleeved=False`; README and ATTRIBUTION restate the no-EP-canon rule | met |
| 5 | Unit tests for runtime behaviour: dice bounds, seeded reproducibility, aspect invocation accounting, stress/consequence processing, no auto-PSI-by-virus, no forced stack/resleeving | `tests/test_fate_rpg.py` (the first slice) **plus** `tests/test_fate_rpg_boundary.py`: 29 tests in the RPG glob, all passing | met |
| 6 | One short investigation scene resolving a cyber check and a PSI check with the same engine | `demo_investigation`, asserted to be reproducible per seed and to use `Action.OVERCOME` for cyber and `Action.CREATE_ADVANTAGE` for PSI | met |
| 7 | A clean future adapter boundary separating faction strategy/simulation, without inventing its mechanics | `rpg/boundary.py`: `LeaderRpgLayer.describe()` fills the reserved `ports.LeaderRPG` signature; `NOT_THIS_LAYER` names what is excluded; a test asserts the payload has no strategic key and that the modules import none of the unapproved layers | met (added here) |
| 8 | `strategy_game/RULEBOOK.md` and README updated accurately: Fate basis approved **for the RPG layer**, strategy and political layers pending | `RULEBOOK.md` status line ("Fate Core RPG foundation selected by author … faction strategy and political simulation rules are not yet approved"); `strategy_game/README.md` #389 paragraph; `rpg/README.md`; no strategy or political rule was added by any of this work | met |
| 9 | Git commit, PR, tests; close only after all acceptance items hold | this PR; the RPG test glob is **29 OK** and the root suite **509 OK**; every item above verified rather than summarised. **Honest caveat:** the whole `strategy_game` package suite currently has 8 failures, all in `tests/test_board_local_projection.py` — the board-projection regression that open PR #391 fixes — and none of them touch the RPG layer. This closure does not claim a green package suite. | met |

## Not claimed, and not part of these criteria

The layer is an **MVP slice**, and `rpg/README.md` keeps a "not yet implemented" list (reroll
invocations, the full four-action outcome tables, complete damage/concession exchange, full character
generation, cyber/PSI countermeasure requirements, and the strategy/political layers themselves).
Those are future work tracked in other issues (#344, #345, #347, #323) — they are **not** unmet
acceptance items of #389, and nothing here presents them as done. No rule of the strategy or
political layer is approved by this closure, and no Eclipse Phase or Transhumanity's Fate text, art
or setting content is reproduced.

## Verification method

Read of each named artifact on `main`, plus execution for every claim that is executable: the RPG test
glob was run (29 tests, OK), the two demos were checked for seed-reproducibility, and the two
separation checks are runtime/source assertions rather than prose. Three of my own tests failed first
and were corrected — the payload scan had matched the payload's own *declared exclusions*, and the
import check had accused the layer of a dependency created by the package `__init__`; the corrected
tests assert keys and a source-level import boundary, which is what the criterion actually means.
