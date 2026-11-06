# Living campaign loops — implemented slice (#1230)

**Status: phases 1, 2 and 4 of #1230 implemented; issue remains open for the faction, enclave and NPC loops.**
This is a deterministic orchestration layer over existing rules. It does not change CWN, SWN, AWN or
WWN mechanics and does not add an action-dice economy.

## What is implemented

| Phase | Module | Contract |
| --- | --- | --- |
| 1. Clock + scheduler + event log | `src/campaign/clock.py` | `GameTime`, `Scheduler`, `EventLog`, `GameClock`; event-driven fast-forward, stable IDs, idempotent replay, save/load |
| 2. Tasks + daily loop | `src/campaign/tasks.py`, `src/campaign/daily.py` | pausable tasks that consume in-game time; CWN check supplied only where uncertainty matters; failure costs time/quality, not all progress; structural day schedule without mandatory meal narration |
| 3. Story arcs | `src/campaign/story.py` | persistent `Arc` states, event activation/progress/resolution, spoiler-safe active list; no railroad |
| 4. Dream Scenes | `src/campaign/dreams.py` | no-dream/ordinary/memory/telepathic/spontaneous precognition/psychic attack/ontological shock selection; deterministic by night/seed; narrative context only |

`DailyLoop` schedules wake, morning briefing, work start, default lunch, work end, leisure and sleep.
Meals and ordinary sleep auto-resolve; the player can skip or change them. `fast_forward()` jumps
from event to event, not minute by minute.

## Deliberately not implemented in this slice

- **SWN faction loop** and the Europol-vs-extremist example. The existing `src/rules/swn_faction_*`
  modules remain the faction rules; this slice does not wrap them yet.
- **AWN enclave loop** and hunger/thirst integration beyond the existing `src/rules/awn_survival.py`.
- **NPC Character Loop** with autonomous schedules and goals.
- UI, Godot/MUD adapters, LLM narration and any tabletop chapter.

The issue remains the integration tracker for those phases; do not treat this module as a second
ruleset.

## Integrity properties

1. One authoritative clock; `GameClock` cannot move backwards.
2. Scheduled event IDs are unique; firing an already logged ID is a no-op.
3. Save/load preserves the clock, pending queue and event log; replay cannot duplicate an event.
4. Tasks distinguish estimated duration from actual elapsed time and never double-spend minutes.
5. Dream selection is deterministic by night and seed; spontaneous precognition does **not** require
   the SWN Precognition ability and does not promise a fixed future.
6. The Story Director never exposes arc internals in the spoiler-safe view and never forces a player
   choice.

## Use

```python
from src.campaign import GameClock, GameTime, DailyLoop, Task, TaskBoard

loop = DailyLoop(GameClock(GameTime(1, 0)))
loop.schedule_day(1)
loop.advance(8 * 60)                 # morning briefing fires
board = TaskBoard()
board.add(Task("report", "Write the report", 240, difficulty=10))
board.start("report")
board.advance("report", 120, check_total=12)
dream = loop.sleep(forced_dream="lifepath_memory")
```

Run `python3.11 -m unittest tests.test_living_campaign_1230`.

## Related

- Existing faction rules: `src/rules/swn_faction_engine.py`, `swn_faction_turn.py`.
- Existing AWN survival: `src/rules/awn_survival.py`, `awn_world.py`.
- Existing story/scene material: `docs/scenarios/CAMPAIGN_ROADMAP_1120.md`,
  `docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md`.
- Dreams worksheet: `docs/campaign/DREAMS.md` (#1152).
