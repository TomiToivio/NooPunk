# Issue #1053 — architecture survey and migration status

Read with `docs/architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md` (the decision this survey serves).
Every number below was measured in this tree, not estimated.

## 1. Survey: what is where, and how coupled it is

| layer | path | modules / size | imports engines? |
| --- | --- | --- | --- |
| domain rules | `src/rules/` | 73 modules, 15 546 lines | **no** |
| application: campaign engine, world state, console, CWN façade | `mud/nopunk_mud/` | 23 modules, 3 333 lines | **no** |
| Evennia adapter | `mud/typeclasses/` (7), `mud/commands/` (1), `mud/world/` (1), `mud/server/conf/` (1) | 10 modules | yes, by design |
| Godot adapter | `godot/core/` | 52 scripts, 271 functions | yes, by design |
| Godot-side mods | `mods/noopunk/` | 4 scripts (gumshoe, noosphere, psyche, stress) | yes, by design |
| tests | `tests/` + `mud/tests/` | 133 + 27 files | — |

Checks that already exist and what they cover:

| tool / test | question it answers | current state |
| --- | --- | --- |
| `tools/check_engine_boundary.py` (**new in this issue**) | does the domain layer import an engine, UI, database or model provider? | pass — 96 modules scanned, 0 violations |
| `tools/check_godot_rule_duplicates.py` | does GDScript re-implement a domain rule without being tracked? | pass — 0 known duplicate domains, no new ones |
| `tools/rules_constitution_audit.py` | is every rule module classified, and does the baseline import an overlay? | pass — one tier each, no upward import |
| `tools/cwn_coverage_manifest.py` | is every public rule procedure registered for the Godot adapter? | pass — 36 modules, 362 procedures |
| `tests/test_console_case_1053.py` (**new in this issue**) | does a whole UNSA case run, save, load and replay offline with every engine blocked? | pass — 8 tests |

### Findings worth naming

1. **The coupling the issue fears is not present.** `src/rules` and `mud/nopunk_mud` import no
   front-end at all — not Evennia, not Mesa, not a database. The engine boundary was honoured in
   practice before it was written down; this issue makes it enforced.
2. **The real duplication risk is GDScript.** `godot/core/` holds 52 scripts of CWN mechanics beside the
   Python kernel. The mitigation is not deletion (Godot must run) but *tracking*: the duplicate check
   pins which domains are mirrored. Any GDScript rule that diverges becomes a failing check rather than
   a silent second authority.
3. **`mud/nopunk_mud` is the application layer, not an adapter.** It sits under `mud/` for historical
   reasons, so a reader assumes Evennia lives there. It does not; the console, campaign, world state and
   CWN façade are all engine-free. Moving the directory is a packaging decision (deferred); naming the
   fact is not.
4. **Two campaign surfaces exist.** `mud/nopunk_mud/solo_campaign.py` (a four-stage prologue, pure
   transition) and `mud/nopunk_mud/campaign/engine.py` (the full case with seeded RNG, clues, combat,
   save/load). The console runs the second. The prologue is superseded in practice and is noted here
   rather than deleted without a decision.
5. **Import paths are `src.rules.*`, not `noopunk.rules`.** #1054 suggests the latter. Renaming is a
   packaging change touching 133 test files; it is deferred deliberately, and the boundary tool is
   written to work either way.

## 2. What this increment delivered

### Priority 0, item by item

| #1053 P0 requirement | status |
| --- | --- |
| Audit implementations for duplication and engine coupling; map files and tests | **done** — this document, with counts and the check table above |
| Importable, faithful rule packages for CWN + selected SWN/WWN/AWN, plus optional mods | **already true for CWN/SWN/WWN** (`src/rules`, tiered by the constitution); AWN remains partially blocked on verified tables (see `ISSUE_1045_AWN_INVENTORY_ASSESSMENT.md`) |
| Typed engine-independent commands, results, events, versioned state, RNG/clock interfaces | **already true**: `CampaignEngine.command(line) -> str`, `state` dataclass, `SCHEMA_VERSION` + `from_dict` validation, explicit `seed`, mission clock in state |
| Offline plain-text console running the first UNSA investigation without a GM | **already true, extended here**: `python -m nopunk_mud.cli --campaign --seed N --save PATH --load PATH`, resumable, deterministic |
| Tabletop references, printable procedure, golden examples for the slice's subsystems | **delivered**: `docs/tabletop/FIRST_CASE_TABLETOP.md` |
| Automated checks that rules execute without Evennia/Concordia/Pygame | **new**: `tools/check_engine_boundary.py` + a subprocess import test that blocks ten engine/module roots |
| Preserve saves, avoid breaking Evennia | **kept**: campaign save schema unchanged; `cli.py` gained flags only |

### The console slice, demonstrated

```
$ python -m nopunk_mud.cli --campaign --save /tmp/case.json \
    --script "go street,go university,examine terminal,go street,go kurvi,\
talk witness,ask witness badge,examine woman in the raincoat,go street,go safehouse,report"
… Case filed: the researcher, the van, the second badge
{ "ending": "solved", "clues": ["access_log", "witness_badge"], "hp": 6, "turns": 11, "seed": 7 }
```

Resuming works the same way: finish three commands, quit, then `--load /tmp/case.json` and the case
continues to `solved`. Both paths are tests, not anecdotes:
`test_a_complete_case_is_played_and_finished_offline`,
`test_a_saved_case_resumes_where_it_stopped`, `test_the_same_seed_and_commands_replay_exactly`.

## 3. Priority 1 and 2 — not started, and why

| item | status | note |
| --- | --- | --- |
| Evennia adapter uses the shared core | **already the case in part** — commands/typeclasses call `nopunk_mud`, which is engine-free; a dedicated adapter test is still missing | next step: a test that a command resolves through the engine rather than re-implementing a rule |
| Concordia LLM actor/GM adapter | **deferred** (Milestone B) | must submit validated actions through `CampaignEngine.command`; never authoritative |
| Pygame prototype | **deferred** (Milestone B) | after the console slice is complete |
| Cross-adapter seeded scenario tests | **not yet** — only one adapter exists | becomes possible with the Pygame/Concordia adapters |
| GUMSHOE / PbtA / LaclauGPT / AWN / Tarot mods | **partial**: Laclau (ideology + dossier), GUMSHOE investigation, Noösphere and AWN stress exist as modules; Tarot is not started | Tarot needs card definitions + a physical procedure before any code |

## 4. Acceptance conditions, assessed honestly

| condition | verdict |
| --- | --- |
| No engine-specific implementation is the only authority on a rule | **met and now enforced** for Python; Godot is tracked, not authoritative |
| No change to published CWN procedures | **met** — the boundary and constitution checks would expose an overlay inside the baseline |
| Tabletop players can resolve core play without software | **met for the mechanics the slice uses** — see the tabletop procedure; CWN itself is the published book |
| No forced rewrite to change front-end | **met by structure** — adapters call `src.rules` + `CampaignEngine` |
| A complete console case runs, finishes, saves, loads, is tested offline | **met** — 8 tests, including replay and resume |
| Stale Godot-first documentation updated or marked superseded | **partly** — `docs/GODOT*.md` predate this ADR; marking them superseded is a documentation pass, listed below |

## 5. Next increments, in order

1. **Mark pre-ADR Godot-first docs superseded** (one line each, pointing at the ADR) so the repo does not
   teach two architectures.
2. **Evennia adapter test**: a command that must route through `CampaignEngine`, proving no rule is
   re-implemented in the MUD.
3. **Packaging decision** (`src.rules` → `noopunk.rules`) with a deprecation shim, so the import path
   matches the architecture without breaking 133 test files in one commit.
4. **`solo_campaign.py` disposition**: supersede or fold into `campaign/engine.py`.
5. **Tarot mod**: card data + tabletop procedure first, digital representation after.
