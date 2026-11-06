# Tracker #1217 — derived status

> **Generated.** `python3 tools/tracker_1217_status.py` rewrites this page; `--check` fails when it is stale or when a row's evidence file has disappeared. Every status below is a claim about files that exist right now, not about a commit message.

**Totals:** 7 done · 7 partial · 4 blocked · 1 deferred.

| # | tracker item | status | evidence | note |
|---|---|---|---|---|
| 1 | Opening: audit creation, background, edges, foci, tags, inventory | **DONE** | `src/rules/cwn_character.py`<br>`src/rules/cwn_edges_foci.py`<br>`src/rules/cwn_foci.py`<br>`src/rules/cwn_backgrounds.py`<br>`src/rules/scene_tags.py`<br>`src/world/items.py`<br>`docs/design/TRACKER_1217_AUDIT.md` | the audit page records what exists and what each module owns; no parallel engine was added |
| 2 | Opening: deterministic lifepath builder for Tony German | **PARTIAL** | `src/rules/europol_lifepath.py`<br>`tests/test_europol_lifepath_1217.py`<br>`docs/rules/EUROPOL_LIFEPATH_1217.md` | builder core done: fixed facts, three routes, delegated budgets, 26 legality tests. The player-facing flow still needs a verified CWN Edge catalogue to offer, and the tag offer lists are an authoring decision |
| 3 | Opening: scripted first day (nightmare to Ratakatu 12) | **DONE** | `src/console/first_day.py`<br>`src/console/world_session.py` | every authored step exists as a session transition; no forced roll to reach work |
| 4 | Opening: first approved investigation on the graphs | **BLOCKED** | `docs/scenarios/CAMPAIGN_ROADMAP_1120.md`<br>`docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` | no case has been author-approved yet; #1120 delivers a complete case awaiting that decision |
| 5 | Opening: runtime adapters, one canonical actor id and sheet | **PARTIAL** | `src/world/actor_registry.py`<br>`src/console/first_day.py`<br>`src/world/graphs.py` | console and graphs share `tony.german`; the Evennia side does not yet reference the authored actor, so parity is unproven rather than done |
| 6 | Opening: kit as a legible diagnostic puzzle, failure cannot softlock | **DONE** | `src/world/items.py`<br>`src/console/first_day.py` | issue/fault/activate states, FIRST_DAY_REQUIRED, and a fault path that still reaches the office |
| 7 | Opening: companion interaction once D71 is resolved | **BLOCKED** | — | D71 is an open author decision; implementing a companion now would invent its personality and refusal rules |
| 8 | Opening: deterministic offline regression tests | **PARTIAL** | `tests/test_clock_scheduler_1230.py`<br>`tests/test_europol_lifepath_1217.py` | first-day, lifepath legality, save/resume and graph tests exist; branch coverage of every authored choice and cross-platform parity are not yet covered |
| 9 | Rules: AWN Mutation Edge for PCs, independent of ancestry and PSI | **PARTIAL** | `src/rules/awn_mutant.py`<br>`src/rules/psi_edges.py` | build rules are enforced (Europol approval, no automatic Hybrid, independence). The mutation tables are not registered: they are printed content, and transcribing them is an author/licence decision |
| 10 | Rules: AWN Mentalist selectable, no SWN discipline smuggled in | **DONE** | `src/rules/awn_mentalist.py`<br>`src/rules/psi_access.py`<br>`src/rules/rookie_build.py`<br>`tests/test_psychic_training_1217.py` | arts, Effort accounting and the Mentalist/Spellcaster bar are enforced; the Edge is a PC option |
| 11 | Rules: SWN Psychic Training Focus | **DONE** | `src/rules/psychic_training.py`<br>`tests/test_psychic_training_1217.py`<br>`docs/rules/PSYCHIC_TRAINING_FOCUS_1217.md` | implemented from the author's quotation in #1178; prose not reproduced; the retroactive formula is a reading awaiting confirmation |
| 12 | Rules: device-granted PSI | **DONE** | `src/rules/psi_edges.py`<br>`src/rules/psi_access.py`<br>`src/rules/swn_psionics.py`<br>`docs/design/ISSUE_1196_DEVICE_PSI.md` | a grant lives and dies with the device, reserves Effort only when the equipment says so, and never becomes a selectable discipline |
| 13 | Rules: AWN environmental and social procedures | **PARTIAL** | `src/rules/awn_survival.py`<br>`src/rules/awn_stress_tracker.py`<br>`src/rules/awn_region.py`<br>`src/rules/cwn_pharmaceuticals.py`<br>`src/rules/cwn_combat.py` | survival, stress, region and pharmaceuticals exist; radiation, vehicle combat and chases have no dedicated module yet — they are CWN/AWN procedures that must be verified against the book before any code |
| 14 | Rules: verify tags, clues and investigation overlays | **DONE** | `src/rules/investigation.py`<br>`src/rules/scene_tags.py`<br>`tests/test_scene_tags_20261105.py`<br>`tests/test_investigation_access_and_inquiry.py`<br>`tests/test_goals_1119.py` | four tag types, one clue model and the investigation procedures are implemented and tested |
| 15 | Rules: Astral graph | **DEFERRED** | — | deferred by #1178 and #1230 until an authored scene needs navigable astral locations |
| 16 | Data: Greater Helsinki jurisdictions and zones | **BLOCKED** | `src/world/helsinki.py`<br>`data/world/helsinki_locations.json` | the canonical places load; the four jurisdiction levels, economic and diplomatic zones and protection regions are setting data awaiting author approval (#1121) |
| 17 | Data: recurring clues, provenance, restrained social reactions | **PARTIAL** | `src/rules/investigation.py`<br>`docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` | clue provenance exists; the 50/25/25 reaction envelope is documented but not encoded, because it is a table the author has not approved |
| 18 | Data: Galactic Machine War and Nordic history as discoverable material | **BLOCKED** | `docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md` | material exists as a design memo; turning it into discoverable files before a case needs them is exactly what the issue forbids — it waits for an author-approved case that needs the material |
| 19 | Review: persistence, canon vs event log, reproducible tests, docs | **PARTIAL** | `src/simulation/events.py`<br>`src/simulation/scheduler.py`<br>`docs/DUPLICATION_AUDIT.md`<br>`docs/DOCUMENT_REGISTER.md` | event log, clock/queue persistence and the document register exist; a full audit of every save path is still outstanding |

## What "blocked" means here

A blocked row needs a decision that is not an agent's to make: an approved case, an approved data table, a resolved author question (D71), or a licence decision about transcribing printed tables. Blocked is not unstarted — it is *started to the edge of the decision* and then stopped on purpose.

## What "partial" means here

The mechanism exists and is tested; a named piece of scope does not. The note says which piece, so the row can be finished without re-reading the issue.
