# Issue #346 — acceptance record (re-verified after the second reopening)

**State: LEFT OPEN, deliberately, with the reason per criterion below.** This issue was reopened twice,
the second time from PR #400 (documentation-only, carrying a `Closes` line). Re-checked on current
`origin/main` by **exercising** the code (`python -m unittest`, importing the modules), not by reading
the earlier PR bodies.

| # | Criterion | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 1 | Faction-creation flow + first playable academic-founder template | **MET** | the seven-step flow and the Cosmist International template in `data/faction_creation.json`; `data/founding_story.json` records the founder edge |
| 2 | Faction + lightweight character sheets on existing stat/TAG conventions | **MET for tags** | the typed kind vocabulary (`TAG_KINDS`) is reused across cards and edges; the leader's *attribute set* stays author-defined (D1/D2 open, D7 refuses the six legacy STATs) |
| 3 | Nonprofit / patron / council / court / field-agent distinctions, unified roster with overlapping roles | **MET in substance** | a patron edge is structurally distinct from faction property; the roster question (*exactly four* vs *four deployed of more*) stays flagged on #323 and here, not resolved |
| 4 | The four card types (character, organization, research, government) with minimal effects and interactions | **MET as structure, effects OPEN** | `faction_cards.py` + `data/faction_cards.json` + `tests/test_faction_cards.py` declare `CARD_TYPE_IDS`, the control vocabulary, six declared interactions (`enforced: false`) and a projection onto the shared `Card`; what each interaction *changes* is a `pending_author_decisions` entry |
| 5 | Random low-level NPC creation without individual management | **MET** | the archetype family and `instantiate()` in `character_cards` |
| 6 | Four field-agent deployments per turn **with abstract mission resolution** | **NOT MET** | the four-move cap is refused by name in `council.py`; *resolution* is a rule: `data/council.json`'s `mission.resolution` is `declared: false` and `MissionDeclaration.outcome` is an uninterpreted field |
| 7 | Pre-crisis world state **and first-turn resource constraints** | **NOT MET** | the world state is documented; the resource constraints are an **economy**, reserved to the author. Now expressible: `first_turn` names the issue's own candidate field slots with `values_declared: false` and its reason |
| 8 | Two contrasting factions created with the same rules | **MET** | three comparative examples plus the seven authored factions, all validating through one vocabulary |
| 9 | Cross-reference and reconcile existing strategy/faction/character issues | **MET** | `consumes` blocks in both data files and the cross-links in both documents |

## Precisely what is blocked, and on which author decision

- **Criterion 6 — abstract mission resolution.** Blocked on an author ruling for *how a declared mission
  is resolved and what its outcome means*. Gates A (leader RPG) and C (strategy) are open in
  `docs/RULE_SYSTEM_RESEARCH.md`, `AGENTS.md` §4 reserves resolution and thresholds, and #389 approved
  the **RPG layer only**, which does not license a strategy resolution rule. The ruling is recorded
  **once**, as `mission_resolution` in `data/council.json`'s `pending_author_decisions`; this issue's data
  file points at it rather than restating it.
- **Criterion 7 — first-turn resource constraints.** Blocked on an author ruling for *starting resources
  / an economy*. `AGENTS.md` §4 reserves economies to the author and `strategy_game/RULEBOOK.md` still
  says **NO RULES APPROVED**, so no agent may supply one.

Both are also rows in `docs/design/AUTHOR_DECISION_QUEUE.md`, so an answer converts directly into a
criterion check and a close.

## What landed for this issue in this session

- `strategy_game/data/faction_creation.json`: the `first_turn` **container** (the issue's own candidate
  faction-sheet field names, `values_declared: false` with its reason) and a `pending_author_decisions`
  list carrying the two blocked criteria — one of them by reference, so the resolution ruling has one home.
- `strategy_game/faction_creation.py`: `first_turn`, `first_turn_fields()`, `first_turn_problems()`
  (refuses a value where none is approved), `pending_decisions()` and `unreasoned_decisions()`.
- `strategy_game/tests/test_faction_creation.py`: 12 further code-only contracts.
- `strategy_game/docs/FACTION_CREATION.md` §7 for this container, and a correction of the stale bullet
  claiming the recruitment event's content is still unauthored (PR #426 authored it).

`strategy_game/RULEBOOK.md` was **not touched**; no rule, magnitude, threshold, cost, die, action set,
turn cadence or win condition appears anywhere in this work; no test asserts prose ([#271]).

## What is explicitly not claimed

The two blocked criteria are **not** met, not deferred-and-closed, and not waived. This issue stays open
until the author rules on resolution (criterion 6) and on starting resources (criterion 7), or explicitly
folds them into another issue.


---

## Re-verification (later session): the records above stand, and criterion 7's container now exists

This record is **kept as written** — its two deferrals are correctly *stated as deferred*, which is the
condition the defer-and-close rule sets, so the close it supported is honest and is **not** re-litigated
here. What this session adds is the structure that was still missing under criterion 7, plus a
measurement of the whole layer on current `main` by **executing** it (`python -m unittest`, importing the
modules) rather than by reading a PR body.

**Criterion 7's container is now landed.** *"Pre-crisis world state and first-turn resource
constraints"*: the world-state half was documented, and the resource-constraints half is an **economy**,
which `AGENTS.md` §4 reserves to the author. So `data/faction_creation.json` now carries `first_turn` —
the **issue's own** candidate faction-sheet field names (ideology/doctrine, legitimacy,
membership/support, influence/reputation, funding, research, intelligence, organisation/facilities,
security, network ties, corporate-patron access, strategic objectives) — with `values_declared: false`
and the reason it is false. `faction_creation.py` adds `first_turn_fields()`, `first_turn_problems()`
(which refuses a field carrying **anything but its name**, a blank or repeated identifier, a numeric
label, a container that does not say whether values are declared, and an empty container with no reason),
`pending_decisions()` and `unreasoned_decisions()`. **The criterion is still not met** — a container is
not a rule — and the ruling it waits for is queue row **D11**.

**The resolution ruling has one home.** Criterion 6's ruling is `mission_resolution` in
`data/council.json`'s `pending_author_decisions`; this file's `pending_author_decisions` **points at it**
rather than restating it, so the same decision is not tracked in two vocabularies.

**And the criterion-6 gap on #323 is closed as structure.** #323's minimum data model lists an `Event`
record (`trigger, participants, choice options, state effects, short narrative text`) and nothing in the
package declared one; `data/council.json`'s `character_events` now does, with `event_problems()` /
`event_reports()` in `council.py` and a projection onto the shared tabletop `Card`. That is #323's
criterion, but it is the same gate as #346's criterion 6, which is why it is noted here.

**Measured on `main` at this session's base (`16fcb69`), both suites green:** the strategy suite
**1119 → 1151** tests with this work (32 new code-only contracts, [#271]), the root suite **509**,
`python -m strategy_game` emits its pinned key set, and `NoQuantifiedPoliticsTests` passes. No rule,
magnitude, threshold, cost, die, action set, cadence or win condition appears anywhere in it;
`strategy_game/RULEBOOK.md` is untouched.
