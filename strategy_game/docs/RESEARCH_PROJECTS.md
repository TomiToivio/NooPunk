# Research, science and technology on the shared project engine

**Issue #506, Phase 1** — the branching research/science/technology system of the NoöPunk ×
LaclauGPT crossover, built on the **one** incremental-action engine the rest of the strategy layer
will use: *agent-lead skill check → faction resource throughput → multi-turn progress clock*.

**Status of this record.** Design record and implementation notes. It approves nothing: the numbers
it describes are marked as tuning parameters, and every open ruling is carried to
`docs/design/AUTHOR_DECISION_QUEUE.md` (rows D27 and D28). Phases 2–3 of #506 are roadmap and stay
unbuilt.

## 1. What was built

| file | what it holds |
| --- | --- |
| `strategy_game/projects.py` | the **universal engine**: `ProjectStage`, `ProjectClock`, `Prerequisites`, `Allocation`, `FactionCapacity`, `StrategicProject`, `ProjectResult`, `ProjectCompletion`, `ProgressCause`, `advance_project`, `pause_project`, `resume_project`, `reassign_project`, `complete_project`, `clock_for_difficulty`, `unsatisfied_prerequisites` |
| `strategy_game/research.py` | the **research vocabulary on top of it**: `ResearchProject`, `TechNode` / `Capability`, `FactionResearchCapacity`, `ResearchYield`, `ResearchCompletion`, `RpgOption`, `RESEARCH_LEAD_SKILL`, `RESEARCH_PROJECT_KINDS`, `complete_research`, `prohibitions_for`, `rpg_options` |
| `strategy_game/research_slice.py` | the **noncanonical vertical slice**: one mission-sourced artefact, one alien reverse-engineering example, one mundane technology-transfer example, one non-research task, save/load, a seeded JSON report (`python -m strategy_game.research_slice`) |
| `strategy_game/campaign/state.py` | four new books on the one world model: `projects`, `tech_nodes`, `capabilities`, `capacities` |
| `strategy_game/tests/test_research_projects.py` | 69 executable contracts (`python -m unittest discover -s strategy_game/tests -p "test_research_projects.py"`) |

Research is the **first instance** of the engine, not a special case of it: a construction, an
organising programme, a diplomatic campaign or a covert operation is the same `StrategicProject`
record with another `lead_skill` and another `resource_kind`.

## 2. Which layer the project check uses, and why

Issue #506 says the lead researcher rolls a **SCIENCE** skill check. In this crossover `science` is
a **strategic agent skill**: one of the seven proposed in
`strategy_game/data/strategic_skills.json`, whose `status` is `PROPOSAL` because issue #482 approved
the RPG foundation and the six *individual* skills (**COG, INT, REF, SAV, SOM, WIL**) and
deliberately did not approve a strategic roster (row D22).

So the project check is:

* an `ActionContext.FACTION_AGENT` check, reading `Character.strategic_skills` — **not** an
  individual scene check;
* resolved by `strategy_game.rpg.skills.check`, the context-checked API, with the **proposed roster
  passed in by the caller**, so free invocations, rerolls, aspect invokes and the capability gate
  all behave exactly as they do in a scene. Nothing about it is a second RPG engine;
* still a **proposal everywhere**: `RESEARCH_LEAD_SKILL` is not promoted, the loader still refuses a
  roster whose status is not `PROPOSAL` (`strategic_skills.roster_from_dict`), and a check with no
  roster supplied is refused as *pending author approval* rather than rated at zero. Two tests pin
  that, and one asserts the refusal happens **before any dice** (the RNG's state is unchanged).

**Domain TAGs are optional.** The author simplified all research to one SCIENCE skill.
Subjects such as Forensics, Parapsychology and Engineering are not separate skills; when
relevant, a project may name descriptive domain TAGs. A domain TAG is a
`competence` tag in issue #346's vocabulary, read through `rpg.skills.capabilities_of`. It is
**reported** — the result carries `domain_tags_matched` and `domain_tags_missing` — and it is never
rated: no tag moves the check or the throughput, because `rpg.skills.specialist_supplement` already
fixes that rule for the sheet ("it grants no bonus, because a tag that moved a roll would be an
unapproved mechanic"). A test compares two runs that differ only in the matched tags and asserts
identical shifts and identical segments. Projects without any domain TAGs are valid and
require no waiver flag.

"Particular expertise" is a different mechanism and is the kernel's own: `StrategicProject.
required_capability` is handed to `rpg.skills.check(..., required_capability=...)`, so the #482 gate
refuses an uncapable lead before any dice.

## 3. Discovery, prototype and manufacturing are three grants, not one bar

Issue #506 forbids conflating them, and the schema enforces it rather than trusting a caller's
memory:

* `ProjectStage` names the six stages in the issue's own words — `known_principles`,
  `scientific_understanding`, `engineering_prototype`, `reproducible_manufacture`,
  `deployment_infrastructure`, `society_wide_adoption`;
* a project's `stage` is the **one** stage its *completion* produces, and completing it grants
  exactly that `TechNode` into `Campaign.capabilities` — the faction's held capabilities;
* reaching the next stage is a **separate project** whose prerequisite is the node the first one
  granted (`Prerequisites.node_ids`), and `complete_research` **refuses** to grant a capability
  whose declared requirement is not held. A factory cannot arrive before the understanding it
  depends on;
* a node's `branch` and `hybrid_of` are free descriptive labels (the issue: "branch identity is
  *descriptive*, not a rigid class"), so a hybrid pathway is a node that names both of its parents
  and nothing derives a taxonomy from them.

## 4. The turn, in order

`advance_project(campaign, project_id, *, rng, turn, roster=…)` is the whole turn:

1. **a completed project is closed** — it reports `ALREADY_COMPLETE`, adds nothing, appends nothing
   to its log and rolls no dice (pinned by comparing the RNG's state before and after);
2. **a paused project stays paused** and repeats its reason;
3. **prerequisites are read before dice.** A project that has never started and does not satisfy
   them is **refused loudly** (`ProjectError`): an unfunded wish is not a programme. A project
   already in progress whose prerequisite was *lost* — the lab raided, the specimen reclaimed — is
   **paused**, with the missing ids named and every completed segment preserved. That is the issue's
   "project interruption" and "resource shortage", and it is why losing a prerequisite does not
   erase work;
4. **the lead's check** through the one kernel, in the faction-agent context, with the proposed
   roster;
5. **success is gated; throughput is not.** Failure ⇒ zero segments. A **tie** ⇒ zero segments, with
   the reason shown: Fate Core's tie is "succeed at a minor cost", and no cost rule is approved, so
   the cost stays a scene decision and the clock takes nothing. Success ⇒ the faction's **committed
   throughput** (`FactionCapacity.allocated(project_id)`), plus one segment on a success *with
   style*;
6. **no capacity, no work.** A successful check with nothing committed advances nothing and reports
   `NO_CAPACITY`: individual competence keeps a programme on track, institutional resources decide
   its scale.

`filled` never decreases: `ProjectClock.add` is the only mutator, it refuses a negative and it clamps
at the total, so no operation in the engine loses progress and none can overfill a clock. The
opportunity cost of a stalled round is the lead's action for the turn — already the structure
`rpg.roster.TurnLedger` enforces (one action per character per turn) — so the engine invents no
second price for failure.

`ProjectResult` carries `cause` (`advanced` / `completed` / `check_failed` / `tie` / `no_capacity` /
`paused` / `already_complete`), the outcome, the segments added, the clock's state, the committed
throughput, the domain tags matched and missing, and `notes` — the same facts in sentences. That is
issue #506's *"the player should see why progress did or did not happen"*.

## 5. Tuning parameters (not canon)

Issue #506 states that "exact dice bands, capacity normalization and duration balance should be
aligned with existing rules and tested". Four numbers are needed and every one is named `TUNING_`
so no reader mistakes a convention for a rule:

| constant | value | what it does |
| --- | --- | --- |
| `TUNING_CLOCK_BASE_SEGMENTS` | 8 | the segments a clock starts from |
| `TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY` | 2 | the segments each step of the check's difficulty adds |
| `TUNING_CLOCK_MAX_SEGMENTS` | 20 | the ceiling, so a major project stays finite (the issue forbids double-penalising until it becomes impossible) |
| `TUNING_STYLE_BONUS_SEGMENTS` | 1 | the extra segment a success *with style* adds, deliberately smaller than the committed throughput of the worked examples |

`clock_for_difficulty(d)` = `min(8 + 2d, 20)`, so difficulty 2 gives **12 segments** — issue #506's
own worked example ("progress becomes 3/12, then 6/12"). A project may also state its own
`work_required` directly, which is how an author's own number reaches the engine.

Rows **D27** and **D28** of the author decision queue carry these conventions and the two related
questions (whether a tie should ever grant progress; whether a matched domain TAG or a named
ideological prohibition should ever *do* anything).

## 6. The worked examples

`strategy_game/research_slice.py` is noncanonical fixture content — the faction, the artefact, the
lab, the archive, the node ids and every rating are fixtures, in the same spirit as `rpg/fate.demo_*`
and `global_slice.py`. Run it with `python -m strategy_game.research_slice`; the report is JSON.

**One mission-sourced artefact.** The recovered propulsion component enters the faction's books
through `campaign.missions.apply_mission_outcome` and nothing else; the reverse-engineering project
advanced *before* the mission is refused by name. A test pins both halves.

**The alien reverse-engineering example.** `project-nhi-propulsion`: kind `reverse_engineering`, lead
`a-1`, `science` (proposal) at difficulty 2, **12 segments**, three `research` units committed a turn.
With `DEMO_SEED` its first turn is a **failed check** — zero segments, everything preserved — and the
clock fills at 12/12 on turn 5. Completion grants **scientific understanding**: a capability, an
investigation clue (`clue:propulsion-anomaly`, written into the campaign's intel book and the case's
evidence inventory), and an RPG option — and **no equipment at all**, because understanding a
recovered drive is not a drive plant.

**The mundane technology-transfer example.** `project-archive-terminal-transfer` industrialises a
technology whose principles are already known: it discovers nothing, its prerequisite is the archive
the organising programme won, and its completion grants **reproducible manufacture** and a piece of
equipment (`equipment:field-archive-terminal`, on the lead's sheet). The two programmes are
deliberately not one progress bar.

**The non-research task.** `project-archive-access` is the organising programme on the *same* engine:
lead skill `stewardship`, resource kind `personnel`, no capability, no discovery — and its completion
is what the transfer programme depends on. `ResearchProject` refuses a non-`science` lead by name, so
the distinction is in the types rather than in a comment.

**Ideological prohibitions.** The alien node declares `prohibited_by=("doctrine:butlerian-retrenchment",)`,
one fixture member holds that belief, and the completion **reports** the contradiction
(`prohibitions_for`, and `prohibitions` in the completion and its audit note). Nothing is blocked:
whether a faction that believes this should be *stopped* is row D28's ruling, not this code's.

The documented run (`DEMO_SEED`, eleven turns) and the exact per-turn segments are asserted line by
line in `test_the_slice_reproduces_the_documented_run`, so the constant cannot drift from the claims
made here.

## 7. Where the state lives

The four books are fields on **`Campaign`** — the one world model of `strategy_game/campaign/`
(#505), not a second state file:

| book | meaning |
| --- | --- |
| `projects` | the declared projects and their clocks, by project id |
| `tech_nodes` | the capability nodes the world's data **declares** (the graph Phase 3 grows) |
| `capabilities` | the nodes the faction **holds** — one stage at a time, each granted by a completion |
| `capacities` | one `FactionCapacity` ledger per faction id: per-turn units by kind, and what is committed to which project |

`campaign-save-1` is **not** bumped: the four books are new optional fields with empty defaults, so a
snapshot written before them still loads and every field it did carry is read back unchanged. Nothing
is reinterpreted and nothing is guessed; a change that gave an existing field a new meaning, or that
made an old snapshot unreadable, is what the marker exists for. A test loads a payload with the four
books removed and asserts the rest survives.

`Campaign.structural_problems()` reports the referential defects a project book can have — a lead
with no sheet, a faction with no ledger, a ledger that declares no capacity of the kind the project
draws on, a held capability whose declared requirement is not held, a declared node whose requirement
is not declared — and `Campaign.__post_init__` **refuses** to be built around a project of a faction
it does not have, a ledger keyed to a faction that is not there, or a held capability the world's
data does not declare.

## 8. What is deliberately not here

* **No technology DAG UI or data-driven branching network** (#506 Phase 3): `tech_nodes` is the seam,
  and the branch labels are descriptive data.
* **No concurrent projects, no personnel assignment loop, no rival-faction ledgers, no facility
  upgrades, no opposition sabotage** (#506 Phase 2). One lead advances one project per turn on one
  ledger; a second project's commitment is a capacity decision the ledger already refuses to
  over-promise.
* **No second price for failure** beyond the lead's action for the turn.
* **No numeric bonus from a domain TAG, no enforced ideological gate.** Both are reports (row D28).
* **No approved numbers.** Every figure is a `TUNING_` parameter, a fixture, or the author's own.
* The **legacy RPG** (`RULEBOOK.md`, `rulebook/`) is untouched and its mechanics are still not the
  crossover's (`AGENTS.md` §0).

## 9. How to verify

```bash
python -m unittest discover -s strategy_game/tests -p "test_research_projects.py"   # the new contracts
python -m unittest discover -s strategy_game/tests -p "test_*.py"                    # the whole strategy suite
python -m unittest discover -s tests -p "test_*.py"                                  # the root suite
python -m strategy_game.research_slice --seed 117                                    # the JSON slice report
ruff check strategy_game/projects.py strategy_game/research.py \
           strategy_game/research_slice.py strategy_game/tests/test_research_projects.py
```

— Ai (愛)
