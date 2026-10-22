# The organisation around the project engine — #506 Phase 2

**Issue #506, Phase 2** of the research/strategy work, carried by issue **#532**. Phase 1 built the
engine (*agent-lead skill check → faction resource throughput → multi-turn progress clock*) and its
research instance; Phase 2 builds the **organisation that runs several of those at once**: concurrent
projects, personnel assignment, facility and capacity upgrades, bottlenecks and recruitment,
opposition sabotage, and the mission↔research loop.

**Status of this record.** Design record and implementation notes. It approves nothing: no dice band,
no work scale, no investment magnitude and no sabotage severity is canon, every number the engine
needed is a `TUNING_` parameter derived from a quantity that already existed, and the ruling is
carried as row **D39** of `docs/design/AUTHOR_DECISION_QUEUE.md`. Rows **D27** (the Phase-1 dice band
and work scale) and **D28** (what a domain TAG or an ideological prohibition should *do*) are
**untouched**: the Phase-1 constants are imported and used exactly as they stand, no new dice band is
defined, and nothing here reads a domain TAG or a prohibition. Phase 3 — the branching technology
DAG, faction divergence, trade and espionage — is not here.

Companion record: [`RESEARCH_PROJECTS.md`](RESEARCH_PROJECTS.md) (Phase 1). This file does not
replace it; it extends it.

## 1. What was built

| file | what it holds |
| --- | --- |
| `strategy_game/operations.py` | the Phase-2 organisation: `AvailabilityState`, `PersonnelAvailability`, `PersonnelReport`, `personnel_availability`, `assign_support`, `project_personnel`, `InvestmentKind`, `CapacityInvestment`, `InvestmentResult`, `apply_investment`, `invested_units`, `RemedyKind`, `Remedy`, `remedies_for`, `Shortfall`, `AllocationPlan`, `plan_allocations`, `ProjectTurnKind`, `ProjectTurn`, `FactionTurnReport`, `run_faction_turn`, `SABOTAGE_LEAD_SKILL`, `SabotageConsequenceKind`, `SabotageAttempt`, `SabotageReport`, `resolve_sabotage`, `MissionOption`, `available_missions`, `ProjectInput`, `project_inputs` |
| `strategy_game/operations_slice.py` | the **noncanonical headless slice**: four concurrent projects, a shortage, a sabotage, an injured lead and three remedies, and the mission→research→mission loop (`python -m strategy_game.operations_slice`) |
| `strategy_game/projects.py` | **extended, not replaced**: `StrategicProject.support_ids` (supporting personnel), its validation, `reassign_project` settles the support list when a supporter is promoted, and the save payload carries the field |
| `strategy_game/campaign/state.py` | two new books on the one world model: `capacity_investments`, `sabotages` |
| `strategy_game/tests/test_operations_phase2.py` | **83 executable contracts** (`python -m unittest discover -s strategy_game/tests -p "test_operations_phase2.py"`) |

The one Phase-1 engine is still the only engine. No project in this module advances by any path other
than `strategy_game.projects.advance_project`, and no mission result is written by anything other than
`strategy_game.campaign.missions.apply_mission_outcome`.

## 2. Concurrent projects, and the per-turn capacity accounting

`run_faction_turn(campaign, *, turn, ledger, rng, roster, order=…, demands=…)` is one faction turn
across every project it attempts. The order of checks is the design:

1. **the ledger and the turn number must agree** — a report that says turn 4 while the ledger is on
   turn 7 is a lie about when something happened, so it is refused;
2. **capacity is planned first** when `demands` is given (`plan_allocations`), so no project is handed
   throughput the faction does not have;
3. then, per project, in the caller's `order` — which *is* the faction's stated priority — one of
   seven legible outcomes that **spend no action**: closed, paused, no sheet, unseated, busy,
   unavailable, blocked;
4. only then is the lead's action declared on `rpg.roster.TurnLedger` and the project advanced.

`TurnLedger` is reused verbatim. The rule it enforces is one action **per character** per turn
(#461/#482), so a lead assigned to two projects drives **one**: the first project in the order runs,
the second reports `busy` with the sentence the ledger itself would raise, and the second's clock does
not move. There is no second roster and no second turn counter.

`plan_allocations(campaign, faction_id, demands)` is where a shortage becomes a fact:

* it **releases** the demands' previous commitments first, so re-planning is a decision about *this*
  turn rather than an accumulation on top of the last one;
* it grants `min(request, what is left)` in the declared order.
  `FactionCapacity` already **refuses** an over-commitment, so the plan cannot quietly over-promise:
  the invariant is the ledger's, not a rule this module remembers;
* it reports every `Shortfall` (requested, granted, short, free-after, remedies), the faction-wide
  `unmet` units per kind, and any **stranded** capacity — units still committed to a programme whose
  clock is full, which is the most common real bottleneck and is the faction's own decision to
  release.

The worked case, from the slice's first turn: four projects, four `research` units, demands of 3, 3,
1 and 2 (the last on `personnel`). Grants: **3, 1, 0, 2**; unmet `research: 3`; free `research: 0`.
The field protocol asked for three and was granted one, so a successful check would have advanced it by
one — which is what the institution could actually give it — and the report says so in a sentence
rather than reporting a bare zero. (In the documented run that check then *ties*, which is a different
fact again: a tie adds nothing, and the run reports it as a tie, not as a shortage.)

## 3. Personnel assignment

A project needs a lead and may name **supporting personnel** (`StrategicProject.support_ids`, set
through `assign_support`). Supporters are character ids on the campaign's own roster: a name without a
sheet is refused (*"inventing one would be inventing a character"*), the lead cannot be its own
support, and a duplicate is refused.

**Support is assignment, not a bonus.** No supporter moves the check, the throughput or the
difficulty, because a supporter who did would be an unapproved mechanic — the same reasoning
`rpg.skills.specialist_supplement` already applies to competence tags, and the open question is
stated in row D39. What support buys today is legibility:

* `project_personnel` reports the lead's and every supporter's availability;
* the turn report says who is on the programme and who can still act;
* `remedies_for` can name a supporter as the concrete candidate for a reassignment when the lead
  cannot act.

`personnel_availability` reads only facts the repository already owns: Fate's own *taken out*
condition (every stress box of a track ticked), an **unrecovered** `Consequence` (a consequence is by
definition an injury that persists until it is recovered), and the turn ledger's record of who has
already acted. No severity threshold is invented — a severity-based reading would be a new number, and
that is row D39's to decide.

## 4. Facility and capacity upgrades, and recruitment

`apply_investment(campaign, investment, *, turn)` is the **bounded, explicit, costed** raise that
issue #506 asks for instead of a magic multiplier:

* one investment raises **one** resource kind by `TUNING_CAPACITY_INVESTMENT_UNITS` (= 1) — derived
  from Phase 1, where the worked examples commit three units a turn, so one investment is a third of
  a turn's throughput;
* the ceiling on capacity **added by investment** is
  `TUNING_CAPACITY_INVESTMENT_CEILING_SEATS` (= 4 = `AGENT_CAPACITY`, the approved one-leader-plus-
  four-agents roster): the faction's own seats are the bound on how far it can grow by its own action,
  and a bigger organisation is an author decision about the roster;
* the **cost is charged**: `cost_resource_ids` must be held, and are removed from the faction's
  inventory — the same id-level transition `apply_mission_outcome` performs, so a cost is a real loss
  of a held thing rather than an invented currency;
* an investment applies **once** (its id is the key), so a replayed turn charges nothing twice;
* the raise is validated as a ledger — the new units go through a fresh `FactionCapacity`, so
  "commitments never exceed units" is re-checked rather than assumed.

Two kinds, deliberately distinct: `InvestmentKind.FACILITY` raises a material kind (a lab, a workshop,
an instrument bench) and `InvestmentKind.RECRUITMENT` raises `personnel`. Crossing them is refused, so
a caller cannot buy research throughput by hiring or hire by buying a machine.

**Recruitment raises capacity, not the roster.** `CampaignFaction` refuses more than four agent
members (#461/#482), and this module does not widen that: recruiting staff adds `personnel` units and
leaves `member_ids` untouched. Turning a new employee into a *seat* is author content, not a number.

## 5. Bottlenecks, and the four remedies

A shortage is not a dead end. `remedies_for(campaign, project_id, shortfall_units=…, ledger=…)`
returns the concrete choices, each with the consequence it would have and the real numbers in it:

| remedy | what it does | what it costs |
| --- | --- | --- |
| `RECRUIT` | raises `personnel` capacity by one unit (personnel shortage only) | the declared cost ids, and ceiling room |
| `UPGRADE_FACILITY` | raises the project's own resource kind by one unit | the declared cost ids, and ceiling room |
| `REASSIGN_LEAD` | hands the project to a **named, free, seated** character; the clock and every completed segment move with it | that character's action, now and next turn |
| `PAUSE` | stops the clock at *n*/total, preserves every completed segment, releases the committed units | the programme stops |
| `RELEASE_STRANDED` | takes back units a **completed** programme is still holding | nothing — which is why it is offered first when it exists |

Only offered when it would actually help: `REASSIGN_LEAD` appears only when a free seated candidate
exists, `RELEASE_STRANDED` only when some finished programme is really holding units. Everything is
*reported, never applied*: each is a decision with a cost.

## 6. Opposition sabotage, and the progress invariant

`resolve_sabotage(campaign, attempt, *, rng, turn, roster)` runs one check by the saboteur through the
one Fate kernel (faction-agent context, the proposal roster passed in, `SABOTAGE_LEAD_SKILL` =
`security`), then records a consequence the project cannot hide.

**The Phase-1 invariant is kept, and this is the whole design.** `ProjectClock.filled` never
decreases, so a set-back cannot be "you lose three segments". It is instead a **longer road**: the
clock's `work_required` grows by `TUNING_SABOTAGE_SETBACK_SEGMENTS` (= 1, derived from
`TUNING_STYLE_BONUS_SEGMENTS`, the smallest amount by which the engine already moves a clock), so every
completed segment stays completed and the programme has further to go. Three consequence kinds:

| kind | effect | progress |
| --- | --- | --- |
| `SETBACK` | `work_required += 1` | untouched, and the road is longer |
| `COMPLICATION` | the project is paused with a stated reason; `resume_project` restarts it | untouched |
| `ALLOCATION_LOSS` | the units committed to the project return to the pool; the next plan shows the shortage | untouched |

How many land is the **approved** Fate ladder's business, not a new band:
`TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME` maps failure/tie → 0, success → 1, success with style → 2,
drawn from the attempt's declared menu in order.

Three guards, in three places:

1. `SabotageReport.__post_init__` **refuses to exist** with `filled_after != filled_before` or with a
   shorter `work_required` — a report that described lost progress could not be constructed;
2. `resolve_sabotage` refuses a **completed** project (a closed programme accumulates no work, so
   there is nothing to lengthen and no progress to pretend to preserve);
3. the attempt is keyed by id in `Campaign.sabotages`, so a replayed turn applies nothing twice, and
   every attempt appends one audit note with `filled_before == filled_after` in it.

The proof that the guard is real is in the task record: the set-back line was mutated to subtract a
completed segment and the report guard disabled, `test_sabotage_never_erases_completed_progress` and
three sibling contracts failed (`AssertionError: 4 != 5`), the file was restored byte-identically
(`sha256sum -c` OK) and all 83 contracts passed again.

## 7. The loop: research opens missions, missions feed research

Both directions are **read-only projections**; the writers are Phase 1's.

* `available_missions(campaign)` — every mission the faction's held capabilities open, derived from
  `Campaign.capabilities` and stored nowhere else. A capability opens a mission only when the author's
  node names an `option` in its yield (`ResearchYield.option`); a node without one changes what a
  character can do in a scene, and inventing a mission id for it would be inventing content.
* `project_inputs(campaign, report)` — which of the faction's projects a resolved mission has just made
  possible, read **after** `apply_mission_outcome`. It checks the ids the mission reported against the
  faction's inventory *and* each project's `requires.resource_ids`, so an id counts only if the faction
  now **holds** it: a report that was never applied shows as *not ready*, which is the honest answer.
  It writes nothing (pinned by comparing `campaign.to_json()` before and after).

The slice closes the loop end to end: a mission brings home the artefact → the understanding programme
completes and opens `option:nhi-propulsion-model` → that mission is played through
`apply_mission_outcome` and brings home `data:propulsion-telemetry` → the second programme
(**manufacture**, whose declared prerequisite is the understanding node *and* the telemetry) becomes
startable, completes, and opens `option:propulsion-manufacture-programme`.

## 8. Tuning parameters — not canon (row D39)

| constant | value | derived from | what it does |
| --- | --- | --- | --- |
| `TUNING_CAPACITY_INVESTMENT_UNITS` | 1 | Phase 1's three-unit throughput: an investment is a third of a turn | units one investment adds |
| `TUNING_CAPACITY_INVESTMENT_CEILING_SEATS` | 4 | `AGENT_CAPACITY` (one leader + four agents, #461/#482) | ceiling on units added by investment, per kind |
| `TUNING_SABOTAGE_SETBACK_SEGMENTS` | 1 | `TUNING_STYLE_BONUS_SEGMENTS` | segments a set-back adds to the total work |
| `TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME` | 0/0/1/2 | the **approved** Fate ladder's four steps | how many consequences land |

Nothing else is new. The Phase-1 constants (`TUNING_CLOCK_BASE_SEGMENTS`,
`TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY`, `TUNING_CLOCK_MAX_SEGMENTS`, `TUNING_STYLE_BONUS_SEGMENTS`)
are imported and used unchanged, and **row D27 is not touched**: no dice band, difficulty, work total
or duration is stated here. **Row D28 is not touched**: no domain TAG and no prohibition is read.

Row **D39** carries the four questions this build creates: whether an investment should be one unit or
another magnitude; whether the ceiling should really be the roster size; how hard a sabotage should
land; and whether assigned **support personnel** should ever bound a project's usable throughput (today
they are reported only).

## 9. Where the state lives, and the save format

Two new books on **`Campaign`** (the one world model), both additive with empty defaults:

| book | meaning |
| --- | --- |
| `capacity_investments` | the bounded raises applied, by investment id — what was bought, for what cost, on which turn |
| `sabotages` | every resolved attempt, by attempt id — keyed so a replay cannot double-apply, stored whole so the record survives a save |

`campaign-save-1` is **not** bumped, for the reason Phase 1 gave: the books are new optional fields with
empty defaults, so a snapshot written before them still loads and every field it did carry is read back
unchanged. `StrategicProject.support_ids` is the same kind of growth, and defaults to `()`. A test
saves and reloads a campaign carrying an investment, a sabotage, supporting personnel and a set-back
clock and asserts the two payloads are identical.

`Campaign.__post_init__` refuses an investment keyed to a faction the campaign does not have, a
sabotage naming a project it does not have, and a project whose supporter has no sheet;
`structural_problems()` reports an investment whose faction has no ledger to raise.

## 10. The worked run

`python -m strategy_game.operations_slice`, seed 6, seven turns. Noncanonical fixture content, in the
same spirit as `research_slice.py` and `global_slice.py`; the run's own numbers are asserted line by
line in `SliceTest`, so the claims below cannot drift from the code.

| turn | what happens |
| --- | --- |
| 1 | four projects on one pool: artefact **3/12** (+3), field protocol **0/10** (a *tie* — zero segments, preserved), civic index **3/10** (+2 personnel plus the style bonus), laboratory outreach **`busy`** (its lead `a-1` already acted). Plan grants 3 / 1 / 0 / 2, unmet `research: 3` |
| 1 | the Bureau's operative **succeeds with style** at the disruption: `SETBACK` + `COMPLICATION` — work 12 → **13**, filled **3 → 3**, paused with the reason, then resumed |
| 2 | `a-3` is taken out (both physical boxes ticked): the field protocol reports `unavailable` and spends no action |
| 2 | the faction takes three remedies: reassign the field protocol to `a-4`, upgrade `research` 4 → 5 (instrumentation grant), recruit `personnel` 3 → 4 (staffing appropriation); and pauses the outreach |
| 3–5 | the artefact programme finishes at **13/13**; completion grants *scientific understanding*, and `option:nhi-propulsion-model` opens |
| 5 | the opened mission is played through `apply_mission_outcome`; it brings home `data:propulsion-telemetry` |
| 6–7 | the manufacture programme (prerequisite: the understanding node and the telemetry) runs to **8/8**, completing into *reproducible manufacture* and `option:propulsion-manufacture-programme` |

End state: research capacity 4 → 5, personnel 3 → 4, both investments charged and logged, one sabotage
recorded with `progress_preserved: true`, `structural_problems == []`, and the reload identical to the
run's own snapshot. One programme (the field protocol) is deliberately left mid-clock at **7/10**, so
the slice shows a clock in progress rather than a tidy end.

## 11. What is deliberately not here

* **No Phase 3.** No branching technology DAG, no data-driven network, no faction divergence, no trade
  or espionage. `campaign.tech_nodes` stays the declared seam it was in Phase 1.
* **No rival-faction simulation.** The opposition exists as a faction with an operative and can attempt
  one disruption; it gets no ledger, no turn, no AI and no plan of its own.
* **No numeric bonus from supporters, no severity threshold for injury, no approval gate on
  ideology** — all three are reports (rows D28, D39).
* **No new canonical numbers.** Every figure is a `TUNING_` parameter, a fixture, or the author's own.
* **No UI.** The slice is headless text; the renderer questions are rows D13/D38, and #506's
  "small coherent city/organization-scale UI" remains unbuilt rather than pre-empted.
* **No mission *board***: missions are still declared where the RPG layer declares them; this module
  only derives which ones a capability opens.
* **The legacy RPG** (`RULEBOOK.md`, `rulebook/`) and `strategy_game/RULEBOOK.md`'s "no rules approved"
  status are untouched.

## 12. How to verify

```bash
python -m unittest discover -s strategy_game/tests -p "test_operations_phase2.py"   # 83 contracts
python -m unittest discover -s strategy_game/tests -p "test_*.py"                   # 1620, all green
python -m unittest discover -s tests -p "test_*.py"                                 # 585, all green
python -m strategy_game.operations_slice --seed 6                                   # the JSON slice report
ruff check strategy_game/operations.py strategy_game/operations_slice.py \
           strategy_game/projects.py strategy_game/tests/test_operations_phase2.py
```

— Ai (愛)
