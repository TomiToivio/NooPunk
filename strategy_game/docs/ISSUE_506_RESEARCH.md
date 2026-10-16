# Issue #506: science programmes and branching technologies

**Scope:** implement the author's research clock as a deliberately small RPG-first prototype, without overriding the still-provisional wider strategic skill roster in #482. This slice uses the *existing Fate 4dF resolution* from `strategy_game.rpg.fate`; `SCIENCE` is explicitly authorised by #506 for this operation. It does not import Transhumanity's Fate lore.

An assigned lead's SCIENCE rating checks whether the programme is productive. On a successful Fate **overcome** result with positive shifts, the clock fills by the faction's **allocated research work units**, capped at the remaining work. On failure or tie the programme stalls with no progress; work already completed remains. A paused, unfunded or prerequisite-blocked project does not roll. There is no invented economy or spending rule: resource allocation is a caller-supplied integer, not a balance automatically deducted from campaign resources.

Use `python -m unittest strategy_game.tests.test_issue506_research` to verify this vertical slice. From a Python REPL, `from strategy_game.research import demo_research; print(demo_research())`.

The fictional example is a recovered NHI drive component requiring `crash_fragment` mission evidence, 12 work units, 3 research capacity each productive turn. Its completion adds *principles understood* and unlocks an RPG inspection option, **not** manufacture of spacecraft. Another data-authored node may represent well-known engineering transferred to faction workshops. Each node may be labelled with multiple branches (cyberpunk, psipunk, solarpunk, biopunk, nanopunk, quantumpunk, alien-derived), and policy restrictions can rule out projects for specific factions. Dependencies are checked as a directed acyclic graph, not a compulsory single path.

### Integration contract and remaining work

- `ResearchState.add_evidence(id)` is the explicit mission-to-research seam; a completed research node exposes `unlocked_rpg_options` for the authoring/UI layer to consume. This prototype is not yet wired into `Campaign` saves, `MissionOutcome`, or playable CLI scenes.
- Research saves are versioned independent JSON payloads; next step is persist a research payload in the shared campaign's existing extension boundary without breaking `campaign-save-1`.
- Assignments, staff availability, faction resource inventories and political doctrine must be validated against campaign state by a future integration adapter; this pure domain module does **not** claim such checks happen.
- The universal `StrategicProject` engine for diplomacy, construction, intelligence, etc., has not been implemented. The research clock is the first specific behavior from which that shared abstraction can be extracted after playtesting.
- The strategic roster outside SCIENCE, check difficulty values, faction work capacity values and authored technology paths require explicit author choices. Example numbers and node identifiers are **non-canonical fixtures**.
- The issue's X-COM- and Terra-Invicta-scale stages remain open. No ASI rediscovery is implied as an unavoidable end node.

Principle: **the individual keeps the project productive, the institution provides throughput, and choices determine which futures are pursued.**
