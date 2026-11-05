# Duplicate-work audit

Agents work in parallel on this repository, often on the same issue, often in the same hour. This document is the
record of what that has produced, what was merged, and what is still two things pretending to be one.

**Rule:** if you build something and find a second implementation of it, the answer is never to leave both and hope.
Decide which is canonical, delete or demote the other, and add a line here.

The working protocol — search commands, claim etiquette, delegation-over-deletion, how to retire a document —
is [docs/design/AGENT_COORDINATION.md](design/AGENT_COORDINATION.md). The canonical document per subject is
[docs/DOCUMENT_REGISTER.md](DOCUMENT_REGISTER.md).

## Resolved in this audit

| Duplicate | What happened | Resolution |
|---|---|---|
| `mud/nopunk_mud/console.py` vs `src/console/session.py` (+ `src/console/play.py`) | Two playable text front ends for the same case | **My console ceded.** `src/console/` is canonical: it has the real case graph, a walkthrough and its own tests. `console.py` and its test were deleted. |
| `BRAINSTORM_1007` pair: `DESIGN_CANON_1007.md` vs `ISSUE_1007_DESIGN_CANON.md` | Looked like two canon documents | **Both kept, cross-linked.** One preserves the author's text; the other is the decision record with `data/world/reveal_ladder.json`. Neither restates the other. |
| `solo_campaign.py` vs `campaign/engine.py` | 58-line prologue and a 464-line engine, both called "the campaign" | **Engine is canonical.** `solo_campaign.py` carries a DEPRECATED header naming the replacement; it survives only because the Evennia command set imports it. Do not add features there. |
| Coverage documents (`CWN_COVERAGE_MATRIX.md`, `CWN_COVERAGE_1068.md`, `CWN_COMPLIANCE_MATRIX_950.md`, `cwn_coverage.json`) | Four overlapping audits and two generators in one day | **One generator, one report: `tools/cwn_parity_audit.py` -> `docs/rules/CWN_COVERAGE_1068.md`** from `data/rules/cwn_traceability.json` + `cwn_compliance_matrix.json`. Deleted the second renderer (`check_cwn_compliance.py --render`, `CWN_COMPLIANCE_MATRIX_950.md`) and the third audit (`cwn_1068_coverage.py`, `cwn_tabletop_audit_1068.json`, `CWN_COVERAGE_1068.md`). `docs/CWN_COVERAGE_MATRIX.md` is historical and points at the canonical report. |
| Two files named as a duplication audit (`DUPLICATION_AUDIT.md`, `DUPLICATION_AUDIT_1053.md`) | One is agent-work; the other is generated rule-level code duplication | Renamed the generated one to `docs/RULES_DUPLICATION_AUDIT_1053.md`; this file remains the work-level audit. |

## Merged in the second pass (#1098, after #1097 landed)

#1097 consolidated the *reporting* duplicates; the rule-layer duplicates its first pass had recorded were
left in place. Deferring them was the mistake: within the same evening the copies diverged, and one of them
was wrong. Each merge below keeps every public name and makes the loser call the winner, so no importer
broke.

| Duplicate | Evidence it had already drifted | Resolution |
|---|---|---|
| `src/rules/cwn_lifestyles.py` (embedded tables) + `data/rules/cwn/{lifestyles,common_wages}.json` + `mud/nopunk_mud/cwn/economy.py` (own JSON reader) | Three copies of one SRD section, with **two id vocabularies** (`middle_class` vs `ordinary`; `oligarchic_elite` vs `oligarchic_elite_of_a_city`) | Numbers live once in `data/rules/cwn/*.json` (bribe costs added as a third file). `cwn_lifestyles` loads them and is the only procedure; the MUD adapter delegates and keeps only its hireling prose. |
| `cwn_spells.overcast_roll/overcast_outcome` vs `cwn_magic.EffortPool.overcast_roll` + `OVERCAST_TABLE` | Two overcasting tables and two arithmetic paths for one roll | `cwn_magic.overcast_total()` is the one arithmetic; `cwn_spells` reads `OVERCAST_TABLE` and keeps only the player-facing wording. |
| `cwn_alienation.SYNDROMES` vs `cwn_cyberware.SYNDROMES` | **Stressed was worth +3 in one and +5 in the other; the SRD says +5** | The optional module reads the base rules' table; `system_cost` and `therapy_week` delegate. `cwn_cyberware` stays canonical and still knows nothing about the optional rule. |
| `cwn_attack_modifiers.ATTACK_MODIFIER_TABLE` vs `data/rules/wn_core.json -> combat.attack_modifiers.table` | Byte-identical today, which is the dangerous case: nothing fails until one side is corrected | The module loads the data table. |
| Nine CWN status documents with counts of 41, 55 and "unverified 16" for the same tree | Six different answers to "how much of CWN is implemented?" | #1097 deleted the two stray generators; this pass put `> **Superseded:**` banners on every surviving status document and recorded the mapping in `docs/DOCUMENT_REGISTER.md`. |

Guards: `tests/test_rule_duplication_merged.py` asserts *equalities between modules*, never literals — a
literal can be copied, an equality cannot be satisfied by a second transcription that drifts.


## Known, not yet merged

These are recorded in `tests/test_no_duplicate_implementations.py` under `KNOWN_COLLISIONS`. They pass the guard
only because the reason is written down here.

### `cwn_core` (`src/rules/cwn_core.py` 462 lines, `mud/nopunk_mud/cwn_core.py` 254 lines)
Two CWN kernels. `src/rules` is canonical by ADR 1054; the MUD copy is imported by the parity probes in `tools/`
and by the campaign engine. **Merge plan:** point the engine and probes at `src/rules.cwn_core`, delete the MUD
copy, and let the parity probe compare the kernel against the SRD rather than against a second kernel. Deferred
because the engine's imports were not verified in this pass — and a half-migrated kernel is worse than a labelled
one.

### `social` (`src/rules/social.py` 220 lines, `mud/nopunk_mud/social.py` 189 lines)
Not duplicates: `src/rules/social.py` is the **provisional** #220 social procedures (`IS_CANONICAL = False`);
`mud/nopunk_mud/social.py` is the **#1008** rank/scoped-reputation/goals overlay. Two different rule sets with one
filename. **Merge plan:** rename the #1008 module (e.g. `faction_social.py`) when something next touches it; until
then the docstrings must keep saying which is which.

### `session` (`src/console/session.py` 371 lines, `mud/nopunk_mud/session.py` 129 lines)
Different layers, not duplicates: the portable case session vs the Evennia adapter over `CampaignEngine`.
The names are the problem, not the code.

<<<<<<< Updated upstream
## Documentation conflicts found while consolidating

The CWN audit pass measured the reader rulebook against the baseline: **15 chapters still teach a
superseded mechanic** (§3.2 attributes, §4.1–4.2 skills/checks, §5.5 combat, §5.8–5.9 and §51 damage and
injury, §7.4 hacking), **17** have related material only and **30** are absent. The authority block at the
top of `RULEBOOK.md` now names CWN and the Without Number baseline, so the chapters are historical — but
they are not rewritten. Do not add a second tabletop audit for this; extend the rulebook chapters or the
traceability `rulebook` column.
=======
## Found by the new detector, deliberately not merged

`tools/find_duplicates.py` now also compares literal tables (dicts/sets of five or more keys) across code
and data. On its first run it reported ten pairs. Four were merged above. The rest are questions with a
design answer, not a merge:

* `src/rules/wn_core.py` `{FIT, CYB, ...}` ↔ `data/rules/core.json` `stats.names` / `stats.layer` — the
  same stat ids in code and in data. Which side is authoritative is a decision about whether the kernel may
  hard-code attribute names at all; merging it silently would answer that question by accident.
* `src/rules/noopunk_tags.py` ↔ `data/rules/noopunk_tags.json` `attributes.meaning` / `skills.list` — same
  question for the tag vocabulary.
* `first_case_drill.py` `{Strength, ...}` ↔ `mud/nopunk_mud/campaign/content.py` and `mud/…/cli.py` — the MUD's
  character sheet repeats the attribute list; likely a real merge, but it lands in the campaign engine, which
  is the collision the first pass deferred.
* `data/rules/core.json difficulties` ↔ `data/rules/fudge_scale_migration.json difficulty_mapping` — the
  same seven DCs, one with names and one with Fudge steps. Complementary, and worth a cross-reference rather
  than a merge.

One reported pair was a false positive of a third kind: `cwn_gear_mods.drone_mods` and
`cwn_vehicles.mods` share their *field names* (`skills`, `cost_percent`, `components`, `effects`) but not a
single row. Shared schema, different rules — the detector compares keys, and two lists of the same shape
always will.

A detector that reports ten things and gets four merged is working as intended: it is a question generator,
and the answer to "these two dicts share keys" is sometimes "they are supposed to".
>>>>>>> Stashed changes

## What the guard enforces

`tests/test_no_duplicate_implementations.py`:

1. At most **one** console/session implementation class (`Console` or `CaseSession`).
2. The live campaign engine exists and `solo_campaign.py`, if present, stays marked deprecated.
3. At most **one** coverage document claims to be canonical.
4. No module name appears under two code roots unless it is a documented collision.
5. Every documented collision has a written reason **and** an entry in this file.

The module is written as `unittest.TestCase` so the root CI (`python -m unittest discover -s tests`)
actually executes it; a pytest-only guard would have been invisible. It now also fails when a second CWN
coverage report, a second generator, or one of the retired audit files reappears.

An audit that cannot fail is not an audit. Test 4 failed on its first run with three collisions; that is the
behaviour that made it worth writing.

## 2026-11-03 follow-up: same-night overlapping PRs

| Deliverable | Competing work | Authoritative result | Avoid repeating |
|---|---|---|---|
| Mod activation registry and validator (#1091) | #1090 (schema 2), #1094 (schema 3), #1096 (alternate schema 3) | **#1094 merged**, extending the existing `src/rules/mod_boundary.py` validator and `data/mods/registry.json`; **#1096 closed unmerged**. Compare its unique design ideas before any future incremental change, never resurrect its incompatible schema as a second contract. | A parallel mod registry, validator, or copy of the schema. |
| AWN Stress tracker (#1083) | #1088 / #1092 and duplicate branch changes noted by #1095 | **#1088 and #1092 merged**; #1095 explicitly removed its overlapping tracker changes before merging. | A second `awn_stress_tracker.py` or copied Stress numbers. |
| Portable agent interface (#1084) and WWN effects (#1085) | Earlier unchecked follow-up tickets versus #1095 | **#1095 merged** `src/console/agent.py` and level-1 effects for 13 spells in `src/rules/wwn_spell_effects.py`; 70 spells remain, and a provider-specific Concordia adapter or graphical UI is not implied complete. | Rebuild agent-action validation, seed replay, or the first 13 spell rows. |
| CWN fidelity audit (#1081) | Historical unchecked chapters 1–5 task versus #1095 | **#1095 merged** eight sourced executable assertions in `tests/test_cwn_ch1_5_fidelity_1080.py`. | Treat those eight as missing again, or pretend they verify every remaining CWN chapter requirement. |

**Operational rule for issue owners:** after every merged PR, update the parent/child issue's completed increments and remaining exact scope *before* another agent takes its unchecked boxes. Search open, merged **and closed-unmerged** PRs, inspect merged paths and code; distinguish whole-issue closure from a partial increment. #1081 is the cross-cutting evidence/integration gate; #1083 owns AWN, #1084 adapters/Tarot, #1085 WWN spells and commands, #1086 author decisions. Their overlap is intentional only when the integration gate **links** the owner, not when it starts a second implementation.

## 2026-11-05: two live implementations of the four graph families (#1178)

Both are merged and both have tests, so this is the "two engines" case rather than a stale copy:

| module | what it is | who uses it |
|---|---|---|
| `src/world/graphs.py` (803 lines) | `LocationNode`/`PhysicalRoute`/`PhysicalGraph`, `DeviceNode`/`CyberGraph`, `SocialNode`/`SocialGraph`, `StoryNode`/`StoryGraph`, `WorldGraphs` bundle, `to_networkx()` | `tests/test_world_graphs_1178.py`; `src/world/helsinki.py` adapts the canonical location data into it |
| `src/rules/four_graphs.py` (408 lines) | its own `Place`/`Route`/`SpatialGraph`/`SocialEntity`/`Relationship`/`StoryNode`/`StoryEdge`/`FourGraphs`, `networkx_view()` | `tools/graph_authoring.py` (the YAML front door) and `tests/test_four_graphs_1178.py`, `tests/test_graph_authoring_1178.py` |

Neither imports the other, the class names differ for the same concepts, and the two validation rules have already
diverged in detail (the world module models cyber as a separate graph from physical; the rules module folds both
into one `SpatialGraph`).

**Recommendation, not yet executed:** keep `src/world/graphs.py` as the runtime model and turn
`src/rules/four_graphs.py` into the authoring/loading layer for it — the YAML front door needs a *parser*, not a
second model. That is a behavioural merge, so it needs its own PR that ports
`tools/graph_authoring.py` and the two authoring test modules onto the world classes and deletes the duplicate
classes; it should not be done silently inside an unrelated change.

**Do not:** add a third model, or copy validation rules between the two. Until the merge lands, new work should
target `src/world/graphs.py` and treat `four_graphs` as the authoring adapter that is pending replacement.
