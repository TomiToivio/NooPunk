# Issue #338 closeout: Global design and implementation handoff

**Status:** Close the original exploratory/design thread as **superseded**, not as a claim that the entire Global strategy RPG is playable. The current author decisions and acceptance criteria in [#309](https://github.com/TomiToivio/NooPunk/issues/309), [#347](https://github.com/TomiToivio/NooPunk/issues/347), and [#344](https://github.com/TomiToivio/NooPunk/issues/344) remain open and govern future implementation. This file records a handoff, **not** new mechanics or canon.

## Landed evidence

- Global design and comparative proposals: [`docs/design/NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md), [`strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md`](../../strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md), the source ledger and supplement. See PRs #339–#342.
- An **experimental**, deterministic, standard-library-based Global slice with city hubs, discoverable incident sites, agents, passive resources, choices, an illustrative check and political consequence log: [`strategy_game/global_slice.py`](../../strategy_game/global_slice.py) and [`strategy_game/tests/test_global_slice.py`](../../strategy_game/tests/test_global_slice.py), PR #343. Its separate state, sample numbers and dice procedure are **not approved rules** and must not be described as the final engine.
- Long-term framing: [`docs/design/VISION.md`](VISION.md) treats one crossover game with multiple zoom levels, and deliberately distinguishes the strategy game from the legacy RPG.

## Binding/latest issue directions to carry forward

1. The scenario opens around 2027 before the NHI Crisis. UN world government/UNSA is **not already fully consolidated at scenario start**; older contradictory #338 passages are historical explorations, not the default. Start with a curated ideological faction and named people, operating from Helsinki/Finland while other city hubs remain abstract.
2. Factions are political/ideological movements, **not playable nation-states**. Nation-states and emerging UN institutions remain influential NPC institutions. Simultaneous AGI/NHI/PSI paradigm shifts, contested sovereignty and branching character/faction/world stories provide pressure.
3. One shared campaign state underlies the global board, faction management, global politics and narrative/RPG events. Agents activate otherwise passive faction resources; physical, astral and cyber operations use a **common abstract assignment/check/consequence interface**, not three mandatory minigames. Numbers, balances and mechanics require the appropriate approval gate.
4. Cyber access is **not inferred from Castellsian social links**. On-prem, limited and isolated targets need credible physical or logical footholds. [#344](https://github.com/TomiToivio/NooPunk/issues/344) owns the cyberspace scenario/constraints.
5. A tactical investigation/adventure/combat view is **planned for later**, not part of the initial MVP. Preserve a modular mission/outcome contract for eventual zoom-in resolution. Do not say tactics will never exist.
6. Convert mechanics to small, auditable board/card/dice/RPG actions. The game is digitally delivered; physical tabletop manufacturing limits do not apply. No mandatory LLM, paid service or proprietary engine.

## Unfinished work and owner

| Unfinished deliverable | Continued tracking |
| --- | --- |
| One playable, offline, integrated Global board + character choice + faction turn + ideology/politics state + save/replay | [#347](https://github.com/TomiToivio/NooPunk/issues/347), with milestone/scope coordination in [#309](https://github.com/TomiToivio/NooPunk/issues/309) |
| Pregenerated faction/character roster; linked character, faction and world event chains; authority/legitimacy versus militias and state sovereignty | [#309](https://github.com/TomiToivio/NooPunk/issues/309), implemented through the #347 integrated vertical slice; reconcile canon before writing numeric rules |
| One unified, validated mission resolver for investigation, field operations, abstract assault, PSI and cyber access, sharing consequences with the campaign | [#347](https://github.com/TomiToivio/NooPunk/issues/347) and [#309](https://github.com/TomiToivio/NooPunk/issues/309); cyber constraints in [#344](https://github.com/TomiToivio/NooPunk/issues/344) |
| Connectivity gate, on-prem research-facility infiltration and non-remote air-gap constraint | [#344](https://github.com/TomiToivio/NooPunk/issues/344), consumed by #347 |
| Architecture fork: integrate/retire `global_slice.py`'s independent state rather than create a second production engine | [`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md) + #309/#347 |
| UI spikes, actual playtest evidence, accessibility, performance, and eventual tactical-view bridge | #347 (UI/playtest), #309 (longer-term stages) |

## Closure semantics

Closing #338 removes a sprawling, duplicate **exploration tracker** from the open-issues queue. It **does not mark its unchecked implementation acceptance criteria as completed**, approve arbitrary mechanics, silently choose among old scenario alternatives, or close #309/#347/#344. Any new implementer should begin with the current acceptance criteria of those active issues and the present repository code, not the 95-KB historical issue description.
