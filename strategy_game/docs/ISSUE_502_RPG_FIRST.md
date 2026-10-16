# Issue #502: RPG-first implementation roadmap

**Sequence:** X-Files investigative RPG → X-COM organizational play → Terra Invicta faction grand strategy.

The **PC is always the faction leader**, not a rookie agent. The rest of the party are four faction agents. This sequence is for **development**, not an in-fiction progression ladder.

## Implemented Phase 1 vertical slice

The existing Fate Core RPG engine in `strategy_game/rpg/` and the five-seat roster (#482) are reused. A new noncanonical, local example case has a briefing, two investigative paths, two alternative evidence-handling choices, and a final faction-leader decision. It exposes:
- selected leader/agent party participants;
- optional seeded individual RPG checks through the approved Fate engine, where the GM supplies difficulty and permission;
- persistent narrative choices, evidence and an event ledger with a faction identifier;
- JSON save/load and an independent interactive terminal runner.

Run: `python -m strategy_game.rpg.investigation_cli --save /tmp/noopunk-case.json`.
Tests: `python -m unittest strategy_game.tests.test_issue502_investigation`.

This is a **functional proof of architecture, not a complete authored campaign**. The example's fictional events and placeholder character ratings are not canon, and no dice outcome silently determines story consequences.

## Phase 1: the shared strategic-project engine and research (#506)

The same RPG-first increment now carries the **one** incremental-action mechanic every faction
operation will use — *agent-lead check → faction resource throughput → multi-turn progress clock* —
in [`projects.py`](../projects.py), with research as its first instance in
[`research.py`](../research.py): `ResearchProject`, `TechNode`/`Capability`, `ProjectClock`,
`FactionCapacity` and `ProjectResult`, on four new books of the shared `Campaign`
(`projects`, `tech_nodes`, `capabilities`, `capacities`). The lead's check is a **faction-agent**
`science` check through the one Fate kernel with the **proposed** roster passed in, and the proposal
is not promoted: without a roster the kernel still refuses it. Discovery, prototype and manufacture
are separate grants rather than one bar, and one non-research task (an organising programme on
`stewardship`) runs on the same engine. A noncanonical slice with a mission-sourced artefact, an alien
reverse-engineering example, a mundane technology-transfer example and save/load runs with
`python -m strategy_game.research_slice`. The design record is
[`RESEARCH_PROJECTS.md`](RESEARCH_PROJECTS.md); the contracts are
`strategy_game/tests/test_research_projects.py`. The numbers it uses are tuning parameters, carried
as rows D27 and D28 of [`docs/design/AUTHOR_DECISION_QUEUE.md`](../../docs/design/AUTHOR_DECISION_QUEUE.md).

## Future gates (not implemented yet)

**Phase 1 completion:** connect authored scenes, established characters, real permission gates and campaign content to the scene framework. Integrate saved RPG character changes and a durable shared world store rather than treating the case ledger as a world simulation. Review #389 and #482.

**Phase 2:** once Phase 1 gameplay works, build a small mission board with assignments, leads, resources and reactions. The RPG emits events; *only an author-approved strategy adapter* may interpret them into faction effects. Do not infer cost or action values from the examples.

**Phase 3:** once organizational play works, add an abstract-country political layer that consumes the same events. No Laclau/Castells-based effect algorithm or ideology score is approved yet.

The legacy RPG and its rules remain separate from the NoöPunk × LaclauGPT crossover as directed in AGENTS.md (#306). Do not silently import the legacy attributes or unapproved strategic roster.

This work respects `docs/archive/DESIGN_PRINCIPLES.md` and the repo policy that code tests validate executable behavior, not lore text. Agent instructions reviewed: `AGENTS.md`. No external/private instruction files were accessible or edited.
