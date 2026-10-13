# Issue #324 — acceptance record

**What this file is.** The criterion-by-criterion verification that issue #324's work is done, at the
point of closing it. It adds no design content: it records where each requested deliverable lives,
how it was verified, and what stays open.

**What closed the last gap.** This record accompanies one piece of work: the **generic city-and-environs
scenario schema and its validator** (`strategy_game/data/city_scenario_schema.json`,
`strategy_game/scenario_schema.py`, `strategy_game/tests/test_scenario_schema.py`,
`strategy_game/docs/CITY_SCENARIO_SCHEMA.md`), plus the README and site links criterion G asks for.
`strategy_game/docs/LOCAL_SLICE_RULES_PROVISIONAL.md` listed *"formal scenario schema validator"*
among its known omissions, and `docs/scenarios/REPUBLIC_OF_UKWELI.md` already claimed that "the model
and mechanics accept any scenario conforming to the JSON schema" while no schema existed. Both are now
true rather than intended.

**What closure does not mean.** No rule is approved, no canon changed, and the provisional playtest
assumptions in `local_slice.py` stay provisional. The schema checks shape, references and counts; it
derives no value and applies no rule.

## Deliverables A–G

| # | Requested | Where it is met | Status |
| --- | --- | --- | --- |
| A | Lore audit and a concise setting canon/reuse note with provenance | `docs/design/ISSUE_324_UKWELI_CANON_REUSE.md`; `docs/scenarios/REPUBLIC_OF_UKWELI.md` ("recover and reconcile the existing…"); `docs/world/PEOPLES_REPUBLIC_OF_UKWELI.md` | met |
| B | Scenario document with the 2027 starting conditions | `docs/scenarios/REPUBLIC_OF_UKWELI.md` | met |
| C | **Reusable generic city-and-environs location schema** plus one Ukweli configuration with 6–8 locations, routes and tags | `strategy_game/data/city_scenario_schema.json` (generic schema), `strategy_game/scenario_schema.py` (validator + builder), `strategy_game/data/ukweli_local.json` (the Ukweli configuration: 8 locations, 7 routes, tags) | **met by this work** — the schema is country-agnostic and a test proves it with a synthetic second city that validates *and* builds a playable `Game` |
| D | Three factions × four leaders, important non-leader NPCs, a small set of polarising issues | `ukweli_local.json`: 3 parties × 4 leaders = 12 leaders, 2 relationships; polarising issues via the party `claims` and the five shocks; non-leader NPCs through the character-card catalogue (`strategy_game/data/character_cards.json`: Sir Mars Eldrich as a canonical non-leader NPC plus twelve generic archetypes) | met |
| E | A small local/global event deck | `ukweli_local.json` `shocks` (5); the global event seeds in `strategy_game/data/global_factions.json`; the three NHI/AGI/PSI vignettes in `strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md` §8 | met (small by design, as the issue asks) |
| F | Playable 10–12-turn seeded deterministic text/CLI scenario | `strategy_game/local_slice.py`: `play(turns=12, seed=2027)` and an argparse CLI (`--turns`, `--seed`); verified directly — same seed yields an identical 28 981-byte transcript, a different seed differs | met |
| G | Link the setting in the README, site and scenario launcher once it exists; keep generic templates available | `strategy_game/README.md` (new paragraph), `docs/index.html` (new scenario card under *04 / The Game*), and the generic route as the schema + its docs | **met for README and site**; see the carried-forward note on the launcher |

## The four general criteria

| Requested | Where | Status |
| --- | --- | --- |
| Search the repository, history, archived lore and issues for the Republic of Ukweli material | `docs/design/ISSUE_324_UKWELI_CANON_REUSE.md` (the search and its results) | met |
| Canon-reuse inventory: retain / adapt / retire, source links, conflicts flagged | same file, with the conflicts carried as OPEN items | met |
| Preserve distinctive lore while adapting continuity to the ~2027 pre-NHI-Crisis setting | `REPUBLIC_OF_UKWELI.md` and the reuse note's per-element decisions | met |
| Record new design decisions separately from recovered canon | `REPUBLIC_OF_UKWELI.md` marks the eight playable location labels, leader placeholders and event cards as **"Newly proposed … None are claimed as recovered canon"** | met |

## The eight acceptance bullets

| Bullet | Evidence | Status |
| --- | --- | --- |
| Ukweli is the default named local scenario; the separate UNSA Helsinki RPG scenario is not overwritten | README + site now name it as the default; no file of the UNSA/Helsinki scenario material was modified | met |
| One modern city, multiple islands, 6–8 simple locations, no national/global playable map | `ukweli_local.json`: 8 locations including two island locations and a coastal hinterland; the schema caps locations at 8 and knows no map beyond the city | met |
| Indian Ocean influences recognizable without one-to-one copying or stereotypes | `REPUBLIC_OF_UKWELI.md` geographic and aesthetic brief (Mombasa, Zanzibar, Mumbai, Singapore as urban and institutional dynamics, "not replicas or demographic stereotypes") | met |
| Existing lore checked for continuity, preserved/revised elements documented and attributed | the reuse note's per-element retain/adapt/retire with project sources | met |
| Three factions × four leaders run the same mission/portfolio system as #323 | `ukweli_local.json` leaders carry `portfolio` from the four council portfolios; the schema consumes `local_slice.PORTFOLIOS` rather than restating them, and a test asserts the two agree | met |
| External global events affect local dynamics; local decisions primarily affect the city and islands | `shocks` in the scenario data, resolved by the slice; scope statement in `REPUBLIC_OF_UKWELI.md` | met |
| Deterministic Python prototype, no LLMs, supports a short meaningful playtest | `local_slice.py` is standard-library only; the seeded 12-turn run is reproducible; `tests/test_local_slice.py` | met |
| Geography, culture and politics remain scenario data, not engine assumptions | **now provable**: the validator is country-agnostic, and a test validates and builds a synthetic second city through the same bridge | met |

## Carried forward — not settled here

- **A separate "scenario launcher" artifact does not exist.** The repository has no launcher file; the
  site (`docs/index.html`) is the entry point a readme-and-site link can reach, and the scenario is
  reachable from the README. If the author wants a real launcher (a scenario picker), that is a new
  deliverable, not a missing file — `LOCAL_SLICE_RULES_PROVISIONAL.md` also lists "UI scenario picker"
  among its known omissions.
- **The third party's name** — ULP in the issue and the data files, LFP in the #325 brief and #326.
  Tracked in the #324 reuse note (§4.2) and carried in the #327 acceptance record.
- **The restricted island's legal autonomy** — OPEN, reuse note §4.3.
- **The state's formal name** — OPEN, reuse note §4.1; a new setting bible exists at
  `docs/world/PEOPLES_REPUBLIC_OF_UKWELI.md`.

## Verification method

Read of each named artifact on `main`, plus direct execution for the two claims that are executable:
the schema validated the merged Ukweli configuration with **no problems**, and the seeded slice was
run twice to confirm determinism. Nothing was edited to make a criterion pass; a gap would have been
reported instead of closed.
