# The campaign clock and the event queue (#1230 Phase 1)

> **Status: Phase 1 of the phased plan, and only Phase 1.** A deterministic game clock, a due-event queue that fires
> each event at most once, and a save that restores both together. No daily loop, no tasks, no dreams, no factions.

The issue's Phase 1 is *"Clock + scheduler + event log; basic deterministic time advancement, save/load."* The event log
already exists — `src/simulation/events.py` has the canonical envelope with deterministic ids and turn-based ordering.
This adds the two things it deliberately does not own: **what time it is** and **what becomes due**.

## The clock — `src/simulation/clock.py`

| property | rule | why |
|---|---|---|
| no wall clock | constructed with an explicit start, moves only on `advance` | a game that reads the host clock cannot be replayed, and replay is how a save is tested |
| monotonic | a negative advance is **refused**, not clamped | a silent clamp hides the bug that produced it |
| timezone-aware | always; Europe/Helsinki by default | the setting is Helsinki, and naive datetimes are how appointments land in the wrong hour |
| honest about DST | a local time that does not exist raises `ClockError` | Helsinki springs forward at 03:00 on the last Sunday of March; 03:30 never happens, and silently choosing an offset moves the appointment somewhere invisible |
| immutable | `advance()` returns a new clock | a clock that mutates underneath a caller is a bug waiting for a second caller |

`minutes_until(moment)` is signed, so a caller can tell "in 45 minutes" from "45 minutes ago" without a second method.

## The queue — `src/simulation/scheduler.py`

* **Ordering is `(due, id)`.** Two events in the same minute fire in a stable order on any machine.
* **One id, one occurrence.** Scheduling an identical event again is a no-op — that is what makes resume safe — and
  scheduling the same id with *different* content is an error, because silently replacing a pending appointment is how
  a save loses an event.
* **At most once, even when the handler breaks.** The event is removed and recorded *before* the handler is called, so a
  crashing handler cannot cause the same world event to fire twice on the next resume.
* **No repeats.** A recurring obligation enqueues its next occurrence itself. "Every morning" is the daily loop's
  decision, not a hidden interval in the queue.
* **Open vocabulary.** `kind` and `payload` are strings and a mapping. #1230 names briefings, task completions,
  appointments and faction ticks, but the author has not frozen that list, and an enum here would turn a proposal into
  canon.

## The save — one file, two halves

`Scheduler.save(path, clock)` writes `{"version": 1, "clock": …, "scheduler": …}` and `Scheduler.load(path)` returns both.
A save that restores the queue but not the clock (or the reverse) is not a save: it lets a resumed session replay a
window it has already lived through. `load` refuses an unknown version and refuses a file that lists the same event as
both pending and fired.

## What Phase 1 deliberately leaves out

| Phase | subject | where it belongs |
|---|---|---|
| 2 | tasks, daily briefing, interruptions | a daily loop on top of this queue |
| 3 | arcs, templates, story director | the story graph (`src/world/graphs.py`) |
| 4 | Dream Scenes | authored scenes + #1152 |
| 5 | AWN hunger/thirst | `src/rules/awn_survival.py`, already present; needs the book's values verified |
| 6 | SWN factions | the phase after the clock has proved itself |
| 7 | NPC loop, AWN enclaves | last, as the issue says |

The **clock has no opinion about the calendar**: which days are workdays, when the Europol briefing is, how long a
shift lasts — all of that is the daily loop's, because it is setting content and the author has not specified it in
code. The clock can say "it is Tuesday 07:40"; it cannot say "briefing in twenty minutes".

## Tests

`tests/test_clock_scheduler_1230.py` — **23 tests**, organised by the issue's own acceptance criteria:

* clock: start where told, naive refused, forward-only, no mutation, `advance_to` refuses the past, signed
  `minutes_until`, **DST spring-forward refused**, save/load round trip;
* queue: `(due, id)` ordering, future events not due, an event due exactly now fires, idempotent re-scheduling,
  conflicting re-scheduling refused, a fired id cannot be re-armed, naive due time refused, cancellation;
* idempotency: same window twice fires nothing, a raising handler still consumes the event, **a save resumed mid-window
  does not re-fire**, a corrupt/unknown save is refused;
* three days: morning briefings plus one appointment fire in order, once each, and `next_due()` supports fast-forward
  without simulating every minute.

## Not claimed

Nothing here implements a day, a task, an appointment *type* or a night. The queue is the part Phase 2 stands on, and
the tracker's remaining phases stay unchecked until each has its own increment — absence of a feature is not a feature.
