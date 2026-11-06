# Campaign documents

One campaign, one outline. If a second file starts describing the same campaign, it is a duplicate: extend this
one or supersede it.

| Campaign | Document | Status |
|---|---|---|
| **01 — The Rookie, the Awakening and the Wanderer** | [`CAMPAIGN_01_EUROPOL_ROOKIE.md`](CAMPAIGN_01_EUROPOL_ROOKIE.md) | **DRAFT** — Act III is a proposal pending the author (#1132) |
| **Dreams — the writing worksheet** | [`DREAMS.md`](DREAMS.md) | **TEMPLATE** — the single canonical home for dream scenes (#1152); Phase 2 belongs to the author |
| **Tony German — lifepath** | [`TONY_GERMAN_LIFEPATH.md`](TONY_GERMAN_LIFEPATH.md) | **AUTHOR DRAFT** — Tomi writes the branchable history (#1218); agents implement only after approval |
| **Player briefing — first day** | [`PLAYER_BRIEFING.md`](PLAYER_BRIEFING.md) | **AUTHOR DRAFT / TEMPLATE** — author-owned first-session briefing (#1216) |
| **Episode 0 — first day** | [`EPISODE_00_FIRST_DAY.md`](EPISODE_00_FIRST_DAY.md) | **AUTHOR DRAFT** — Tomi writes the opening script (#1218); agents implement only after approval |
| **Opening flow — build then wake** | [`OPENING_FLOW_1217.md`](OPENING_FLOW_1217.md) | **IMPLEMENTED JOIN** — answers → Lifepath → first-day session + kit (#1217); blocked on two transcriptions |

Related but separate:

- [`../design/AUTHOR_WRITING_QUEUE_1216.md`](../design/AUTHOR_WRITING_QUEUE_1216.md) — author queue; [`../design/AUTHOR_APPROVALS_1216.md`](../design/AUTHOR_APPROVALS_1216.md) — explicit decision register

- [`../design/`](../design/) — design decisions, issue records
- [`../world/`](../world/) — world canon (institutions, timeline, locations)
- [`../law_of_one/`](../law_of_one/README.md) — a **separate game**, not a NoöPunk chapter

## #1217: Tony German's first-day mechanical scaffold (not approved fiction)

The canonical `src.console.world_session.WorldSession` and the thin
`src.console.first_day` adapter implement the explicitly requested sequence:
nightmare / wake in Sörnäinen, graduation uniform, inspection and abstract
connection of the eight issued items, Dispatch check-in, Adlerwerke commute,
arrival at Ratakatu 12 and reporting to Romppainen. The player can complete
it without dice or an LLM. Flags and graph occupancy round-trip through
`WorldSession.to_snapshot()/from_snapshot()`; there is no second session or
separate combat or hacking engine. `tests/test_actor_registry_1196.py` includes the #1217 first-day checks.

**Not authored or approved yet:** Tony's choose-your-lifepath memory tree,
CWN Edge/Focus assignments, the nightmare's prose, dialogue beyond the quoted
Dispatch line, the first investigation, and any detailed city route. Tomi
owns those in #1216/#1218. This adapter is not the full campaign scenario,
does not change CWN rules, does not instantiate an AWN Mutant or Mentalist,
and should not be presented as a finished Evennia/GUI integration.

The existing campaign outline above still contains older provisional
character details; for the opening, the latest **Tony German / Europol**
brief in #1218 takes precedence. Do not rewrite Tomi's prose to match an
agent-generated placeholder.
