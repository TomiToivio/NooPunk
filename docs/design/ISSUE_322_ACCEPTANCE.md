# Issue #322 — acceptance record

**Basis for closing.** The author authorised defer-and-close on 2026-10-13, provided the record states
a deferred item as deferred rather than met. This record does that, and it credits the design work
that made it possible: [`ISSUE_322_MVP_LOCAL_CITY.md`](ISSUE_322_MVP_LOCAL_CITY.md) walks the same
criteria in detail (PR #388, repaired by #391) and is not duplicated here. **The design half is
landed; what remains is authorial, and it is recorded as such.**

## The issue's acceptance criteria

| # | Criterion | Position |
| --- | --- | --- |
| 1 | One city and environs only; playable locations from **generic configurable templates** | **met** — `city_scenario_schema.json` + `scenario_schema.py` validate and build a city through the engine (`test_scenario_schema`, 11 tests OK); locations are data, and a synthetic second city builds through the same bridge |
| 2 | Each faction has **four active named characters**, including the player's leader; NPC factions use the same model | **deferred** — the structure is complete and on `main`: three factions × four seats × four portfolios, all twelve seats present, one move each, NPC factions on the same model. The *people* are not named: `ukweli_leaders.json` still carries **14 fields marked "requires author specification"**, and the roster reads as seats and offices — the executed history names a leader as `CPU Chair`, not as a person. Inventing twelve people is author work (`AGENTS.md` §1) |
| 3 | A party can change organisational form and tactics within one consistent model | **deferred** — independent dimensions as tags and event-driven transitions exist as structure; the rules are M4, which is exactly what the author is being asked to approve |
| 4 | Global events influence the local sim; local research **imports/adapts**; no international politics simulated | **half met, half deferred** — the influence half is executed, not merely designed: an offline 12-turn run records a global shock on every turn (`Game.history`, turn 1: *"Global frontier AI model released"*). The research/adoption mechanic is M3, deferred |
| 5 | Discourse, communication networks and institutions present as small, **testable** mechanics | **partly met, partly deferred** — the six quantities, the council layer and the sparse relationship edges are landed and tested (`test_council`, 54 tests OK); the action vocabulary that would make them mechanics awaits the rules ruling |
| 6 | Deterministic headless Python run, no LLMs, short scenario, **inspectable turn-by-turn history** | **met** — `local_slice.play(turns=12, seed=2027) -> Game`. Replaying the same seed yields an identical game (repr sha256 `93fafa1d99ee1521`, identical on replay), a different seed differs, and `Game.history` is a 12-entry record carrying turn, shock, and each action's leader, faction, mission and location. Nothing in the path needs a model provider |
| 7 | Out of scope: tactical combat, detailed economics, national elections, individual citizens, planetary or global maps | **met** — recorded as permanent scope and nothing of the sort exists in the code |

## Milestones as the issue words them

- **M0 (design note) — met.** `MVP_LOCAL_CITY_M0.md`, PR #335.
- **M1 (deterministic vertical slice) — met.** One configurable city, three factions × four seats, serialization, a turn resolver, CLI text output, no Ollama.
- **M2 (core politics) — partly met, partly deferred** as criterion 5.
- **M3 (outside world & technology) — deferred** as criterion 4's second half.
- **M4 (organisational evolution) — deferred** as criterion 3.
- **M5 (playtest) — scenario, history and reproducibility met; rival-faction AI, win/loss criteria deferred** — the AI must obey rules that are not approved.

## What is explicitly not claimed

No rule is approved. Nothing here replaces the design doc, and no leader is named. The deferred items
are the author's: the twelve people, the rules M4/M5 depend on, and the research mechanic. Each is
listed in the decision queue (`AUTHOR_DECISION_QUEUE.md`, rows D1–D2) so they cannot be lost by this
closure.

**A note on a sibling's earlier position.** An earlier comment on this issue declined to close it,
reading two criteria as unmeetable without the author. That reading was correct on the facts, and this
closure does not contradict it: it relies on the author's later ruling that an explicitly recorded
deferral is a legitimate basis for closing. If that ruling changes, reopening restores the previous
state with no loss.

— Ai (愛)
