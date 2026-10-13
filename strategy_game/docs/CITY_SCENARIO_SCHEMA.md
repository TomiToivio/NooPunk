# City-and-environs scenario schema

A city scenario is **data**, not engine code. This document and
[`data/city_scenario_schema.json`](../data/city_scenario_schema.json) make that formal: any city
that conforms can be played through the same model, and the only Ukweli-specific thing in the repo
is the configuration file itself.

- Schema: [`data/city_scenario_schema.json`](../data/city_scenario_schema.json)
- Validator: [`scenario_schema.py`](../scenario_schema.py)
- Reference instance: [`data/ukweli_local.json`](../data/ukweli_local.json)
- Tests: [`tests/test_scenario_schema.py`](../tests/test_scenario_schema.py)

`strategy_game/docs/LOCAL_SLICE_RULES_PROVISIONAL.md` listed a *formal scenario schema validator*
among its known omissions. This closes that omission. Nothing here is approved gameplay: the schema
checks **shape, references and counts**, derives nothing, and applies no rule. The provisional
playtest assumptions stay in `local_slice.py` where they were recorded.

## What a scenario contains

| Section | Shape | Notes |
| --- | --- | --- |
| `format`, `year`, `setting` | strings / integer | the scenario's own name for itself |
| `locations` | 5–8 records: `id`, `label`, optional `pressure`, `tags`, `island`, `access` | abstract playable districts, not a tactical map; `island` marks an island node and `access` (`open` / `restricted` / `prohibited`) marks it open or closed, both as scenario structure, not rules |
| `routes` | pairs of location ids | **abstract adjacency**: direction, cost and control carry no meaning |
| `parties` | `id`, `name`, `leader_ids` (exactly four), optional `claims` and resources | four leaders per party is the leader system's own number (#323), not a schema invention |
| `leaders` | `id`, `name`, `faction`, `location`, `portfolio` (+ optional `skill`, `traits`, `status`) | `faction` must be a party id, `location` a location id, `portfolio` one of the four council portfolios |
| `relationships` | `a`, `b`, optional `trust`, `tags` | endpoints must be leader ids |
| `shocks` | at least a `title` | the event deck's entries |

Constraints the validator enforces: unique ids within each collection, 5–8 locations, exactly four
leaders per party, every party's `leader_ids` matching the leaders whose `faction` is that party,
route endpoints that exist and differ, relationship endpoints that are leaders, and **unknown record
fields are reported** so a typo cannot pass silently.

The four portfolios are **consumed from the engine** (`local_slice.PORTFOLIOS`) rather than restated
in a second copy, and a test asserts the schema's declared list still equals the engine's.

## Adding a city

1. Write `strategy_game/data/<your_city>.json` following the table above. Nothing in the schema names
   Ukweli, Finland, the United States or any institution: geography, culture and politics are
   scenario data, never engine assumptions.
2. Validate it:

```python
from strategy_game.scenario_schema import load_scenario, build_local_game

data, problems = load_scenario("strategy_game/data/<your_city>.json")
print(problems)                 # () means it conforms

game = build_local_game("strategy_game/data/<your_city>.json")   # validated, then built
print(game.snapshot())
```

3. Play the seeded slice: `python strategy_game/local_slice.py --turns 12 --seed 2027`.
4. Render it: `python -m strategy_game.render --world <a WorldState JSON>` draws the board, and
   `--json` prints the `MapProvider` payload for another renderer.

A second city is a *scenario*, not a code change: the test suite includes a synthetic five-location,
two-party city that validates through the same bridge and builds a playable `Game`, which is how the
schema's reusability is proven rather than asserted.

## What the schema deliberately is not

- **Not a rule system.** No value, cost, threshold or outcome is computed anywhere in it.
- **Not canon.** The Ukweli instance is scenario data; the reuse note
  (`docs/design/ISSUE_324_UKWELI_CANON_REUSE.md`) records which parts are recovered lore and which
  are newly proposed.
- **Not country-specific.** It would be a defect for the schema to name a real electoral structure,
  and the tests keep the country-agnostic claim honest.
