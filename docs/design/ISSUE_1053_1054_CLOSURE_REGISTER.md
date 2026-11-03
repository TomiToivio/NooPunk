# Closing #1053 and #1054 — what is proven, what was fixed, what is deferred

Both architecture issues are closed on 2026-11-03. This is the acceptance record: each condition with
the artefact that satisfies it, the two defects found while checking, and the residue that is now
tracked as decisions or follow-up issues rather than as an open umbrella.

## Acceptance, condition by condition

### #1054

| condition | evidence on `main` |
| --- | --- |
| A repository-visible decision declares CWN immutable and defines SWN/WWN/AWN supplementation | `docs/architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md`; `docs/rules/CWN_IMMUTABLE_CORE_1068.md`; enforced by `tools/check_cwn_lock_1068.py`, the SHA pin in `data/rules/cwn_baseline_sha256.json` and `tests/test_cwn_traceability_1068.py` |
| Core mechanics and mods are independently importable, with no engine imports in the domain layer | `tools/check_engine_boundary.py --check` (0 violations, `ast`-parsed), `tools/rules_constitution_audit.py --check` (tier per module, no upward import), `tests/test_engine_independence_1053.py` (subprocess with ten engine roots blocked) |
| A documented stable API supports CLI and future adapters | `mud/nopunk_mud/session.py` (`Action → ActionResult` with events derived from a state diff) and `src/console/session.py` (versioned state, injected RNG); both exercised by replay tests |
| A complete UNSA single-player campaign runs with no online service or GM | `python scripts/noopunk_case.py --script docs/examples/lakkahaltia_walkthrough.txt --seed 7` plays `data/scenarios/lakkahaltia/case_graph.json` to `solved`; save/load/resume pinned by `tests/test_console_case_session_1053.py` |
| Tests verify canonical CWN behaviour, mod isolation, seeded reproducibility and save portability | root suite plus `mud/tests`; the seeded run is byte-identical twice; `to_dict()` copies (a real snapshot bug found and fixed by the parity test) |
| The existing Evennia frontend calls the shared core | `CmdSolo` routes through `CampaignSession`; `mud/tests/test_session_adapter_1053.py` compares state documents across engine, session and command |
| Each rule/mod provides manual tabletop instructions and printable aids | **added by this pass**: `docs/tabletop/PRINTABLE_SHEET_1053.md` (character sheet, procedure card, paper equivalent of the save file, worked example) and `docs/tabletop/FIRST_CASE_TABLETOP.md` |
| SWN faction strategy and advanced multiplayer are postponed | `src/rules/swn_faction_engine.py` exists but nothing depends on it; Milestone C remains deferred, now in #1084's scope note |
| Documentation contains a coverage matrix, roadmap, licensing notes and migration plan | `docs/rules/CWN_RULE_INVENTORY.md` (book-level, 65 rows), `docs/rules/CWN_COVERAGE_1068.md`, `docs/duplication`/`docs/RULES_DUPLICATION_AUDIT_1053.md`, `docs/licenses/`, `docs/design/ARCHITECTURE_AUDIT_1053.md` |
| Every rule/mod has rulebook instructions, Python and tests, updated together | reviewer obligation plus the executable half: `tools/cwn_parity_audit.py --check`, `tools/cwn_coverage_manifest.py --check`, `tools/cwn_rule_inventory_audit.py --check`. Prose cannot be asserted (#271), and that limitation is stated in the coverage report |

### #1053

| condition | evidence |
| --- | --- |
| No engine-specific implementation is the only authority on a rule | the tier audit names one owner per module; the Godot tree cannot add a duplicate domain without failing `tools/check_godot_rule_duplicates.py` |
| No change to published CWN procedures | cwn SHA pin, `tools/check_cwn_lock_1068.py`, `--check` green; nothing in this pass edited a pinned file |
| Tabletop players can resolve all core gameplay without software | `docs/tabletop/PRINTABLE_SHEET_1053.md` (this pass) + `docs/PORTABLE_CONSOLE_CASE.md` + the corrected `FIRST_CASE_TABLETOP.md` |
| No forced rewrite to change front end | `portable_noopunk` is a façade over the one session; browser/Textual/NiceGUI adapters call it |
| A complete console case runs, saves, loads, and is tested offline | as above |
| Stale Godot-first documentation updated or marked superseded | `docs/GODOT*.md` carry the superseded banner pointing at the ADR |
| Architecture survey of duplication and engine coupling | `docs/design/ARCHITECTURE_AUDIT_1053.md`, `docs/RULES_DUPLICATION_AUDIT_1053.md`, `docs/RULES_PARITY_1053.md` |

## Two defects found while checking the parity claim

1. **The tabletop page printed the wrong attribute bands.** `docs/tabletop/FIRST_CASE_TABLETOP.md`
   listed `13–15 → +2, 16–17 → +3, 18 → +4` — the WWN/SWN bands — while its own character table and
   `rules.wn_core.attribute_modifier` use the CWN bands (`3 → −2, 4–7 → −1, 8–13 → +0, 14–17 → +1,
   18 → +2`, printed p. 5). A table following the page would have rolled a different game from the
   one the software plays. Corrected, with the correct bands now also on the printable sheet.
2. **`CaseSession.risk()` computed the check itself** — 2d6 + rank, dropping the attribute modifier
   that CWN's skill check includes ("roll 2d6 and add the most applicable attribute modifier and skill
   level", printed p. 31). That is an adapter owning a rule, which #1054 forbids, and the arithmetic
   was wrong as well. It now delegates to `rules.wn_core.skill_check`; the default attribute score is
   10 (+0), so every existing replay keeps its totals, and a named attribute contributes its real
   modifier. Pinned by `SharedRuleTests` in `tests/test_console_case_session_1053.py`.

Neither fix changes a published rule. Both move the repository towards the book.

## The residue, and why it is not on this issue any more

| residue | where it lives now |
| --- | --- |
| Which CWN core survives in the MUD (`cwn_core.py` vs `cwn/`) | decision **D72** in `docs/design/AUTHOR_DECISION_QUEUE.md` — an author call, because it picks a call convention |
| Which discourse model is canonical (`ideology.py` vs `discourse_network.py`) | decision **D73**, same queue |
| Side quests for the first case | decision **D74** — authoring, and inventing canon was called out as a failure mode by these very issues |
| Concordia and Pygame adapters, Tarot mod | issue **#1084** (Milestone B, deferred by the issues themselves) |
| AWN enclave/crisis/encounter-site work and the Python Stress tracker | issue **#1083** |
| WWN spell effect resolver and the in-game practitioner commands | issue **#1085** |
| The first episode, the party roster, the authored characters | issue **#1086** (with D70/D71) |

Closing an umbrella issue is not a claim that its deferred milestones shipped. It is a claim that the
condition this issue was opened to establish — one immutable core, one engine-neutral library, one
playable case, and a table that can play it with paper — is now true and checked, and that everything
else has a named owner.
