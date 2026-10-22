# #515 acceptance record — the tactical-map spike

**Date:** 2026-10-22. **Status:** acceptance record for the spike as scoped. **No renderer is
approved, no tactical rule is approved, and no canonical content is added by this record.**

## What the issue asks, and what the issue itself says about it

The acceptance criterion is:

> A four-agent squad can finish a short tile-based mission featuring movement, at least one
> investigation/dialogue interaction and optional tactical combat; its outcome is reflected in
> persistent character/faction state.

Two parts of that criterion are governed by the issue's own scope, and both are honoured here
rather than quietly dropped:

1. **"optional tactical combat"** — the issue's own priority line says *"no alternate tactical
   engine or mandatory combat"*, and the author work order (2026-10-19) keeps #515
   **optional/future** until #516's RPG core is usable. The spike therefore implements the
   *optional* hook, not a battle system: a `CONFRONTATION` interaction resolves one approved Fate
   check and **wounds the character on failure** instead of merely leaving the clue unread. A
   firefight is not implemented, and the mission layer says so in its own words: *"No initiative, no
   combat round, no enemy, no line of sight, no cover, no stealth, no PSI, no dice."*
2. **The graphical map** — the goal is an 8-bit pixel-art renderer. The spike is deliberately
   **renderer-neutral** and headless: the mission layer produces a JSON state report and a chosen
   renderer projects it. Choosing that renderer is the author's decision (**D38**), and the tile
   interchange format is part of that same row.

## Criterion-by-criterion

| # | Criterion part | Where it lives | How it was verified |
| --- | --- | --- | --- |
| 1 | A four-agent squad | `strategy_game/tactical/session.py` — `MissionSession.seats`, `seat_ids()` | The packaged fixture mission seats four agents; `python -m strategy_game.tactical --json` shows all four with positions |
| 2 | Can finish a short tile-based mission | `strategy_game/tactical/session.py` — `MissionSession.complete()` | The demo plays the mission to completion; `complete()` returns the applied `MissionOutcome` |
| 3 | Movement | `MissionSession.request_move()` | The demo log records four moves with step counts (`agent_1 move to (9,9) -> (9,9) (14 steps)`) |
| 4 | An investigation/dialogue interaction | `strategy_game/tactical/mission.py` — `InteractionKind.DIALOGUE` / `CLUE` / `CONFRONTATION` | The demo log records `agent_1 interviews the duty clerk -> outcome no check` and `agent_2 reads the annex ledger -> outcome success_with_style` |
| 5 | Optional tactical combat | `InteractionKind.CONFRONTATION` — one approved Fate check; failure wounds | A confrontation is the optional hook. There is no battle system, by the issue's own scope. |
| 6 | Outcome reflected in persistent character/faction state | `strategy_game/tactical/session.py` — `complete()` → `campaign.missions.apply_mission_outcome()` | The mission's `MissionOutcome` is written into the campaign's four books (objectives, intelligence, resources, reputation labels) and appended to `campaign_notes` as a provenance-stamped audit entry |
| 7 | No second ruleset | The session resolves checks through the **approved** Fate kernel (`strategy_game.rpg.fate`) | `complete()` refuses when no decisive check produced an outcome, rather than inventing an aggregation rule |

## Reproducible checks

```bash
python3 -m strategy_game.tactical --json
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## Open items carried forward, not buried

- **D38 — the renderer, and the tile interchange with it.** The spike is renderer-neutral; picking
  the playable UI is the author's.
- **D34 — tactical combat's action economy, and whether a fight is ever compulsory.** The spike
  implements the optional confrontation hook, not the combat rules.
- **D35 — whether mission consequences persist into the strategic layer, and who writes them.**
  The session writes the mission's own four books and the case's evidence inventory; it does not
  write political arithmetic.
- **The map size** is the issue's ~20×20 figure; the spike's fixture is 20×20.

## What closure of #515 does and does not mean

It means the **spike milestone** is delivered and verified: a four-agent squad completes a
tile-based mission with movement, dialogue and a check, and the result reaches persistent state
through the campaign's own books.

It does **not** mean: a renderer was chosen, 8-bit art exists, a combat system was designed, the
tactical map was promoted to a required part of the game, or that the author approved anything
here. The issue's own "Future:" framing and the RPG-first work order both keep the graphical
tactical map **optional** — this record closes the spike, not the feature.
