# Political Simulator: Small, Abstract, Gamified (design direction)

**Status:** #282 scope clarification and **non-canonical design proposal**, not approved rules. This document does not define turn cadence, scores, numerical effects, agent decisions, win conditions or setting canon.

## Prime directive

**Build a NoöPunk political strategy game inspired by LaclauGPT's theories. Do not import or recreate LaclauGPT.**

The LaclauGPT research project is an analytic framework and data-processing system, **not a game engine** and **not a validated generator of political change**. Its research pipeline (collectors, text classifiers, embedding/vector search, databases, multilingual processing, data science notebooks, dashboards, LLM interpretation, DNA/SNA pipelines) is **outside the strategy game's runtime scope**. No coupling to LaclauGPT repositories, services, schemas or infrastructure.

Translate only selected *ideas* into legible board-game concepts. Separate theoretical interpretation, hypothetical game rules and claims about empirical social reality.

## Three complementary layers, one compact experience

1. **Leader RPG:** a named political actor, small character card and personality trait tags; character dilemmas and political relationships are foregrounded. Remain independent of the larger NoöPunk RPG system.
2. **Political simulator:** players encounter contested demands, signifiers, articulations, antagonistic frontiers, temporary alliances/hegemonic formations and networks of communication. These are **design vocabulary**, not automatic causal laws or approved algorithms.
3. **Faction strategy:** visible faction relationships, institutions, organisational assets, influence opportunities and constrained strategic choices on an abstract board. No detailed administrative micromanagement.

Integrate the layers through **consequential narrated events**: a leader-level choice has legible political and faction-level repercussions *once rules are separately designed and approved*. Prefer dense, eventful play to Terra Invicta's long idle stretches. Prefer Dune House-scale dilemmas and CK3 leader politics over simulation sprawl.

## Game abstraction versus research model

| Research inspiration | Candidate player-facing abstraction (not rules) | Explicitly not required |
| --- | --- | --- |
| Laclau: articulation of demands | a small set of visible political issues/demand cards and public claims | discourse annotation or classification pipeline |
| Laclau: empty/floating signifiers, nodal points | contested labels around which factions assemble narratives | vector embeddings, generative semantic dynamics |
| Laclau: equivalence/difference, antagonistic frontier | changing coalition and opposition relationships | full discourse network analysis extraction |
| Laclau: hegemony, contingent formations | understandable political situation and faction positions | claiming a scientific 'hegemony score' |
| Castells: communication power, network programming/switching | an abstract graph of organisations, media and institutional access | reconstructing real-world social graphs |
| LaclauGPT: provenance and uncertainty | clear **fictional / simulated / sourced** labels on events | production-grade RAG, MongoDB, Ollama, Mesa, CSC |

Graph representation is useful because access and relationships need not follow state borders. **NetworkX may be an optional implementation detail**; a standard-library edge list must remain enough to display and save the first game.

## Design constraints for a first playable vertical slice

- **Small before sophisticated:** one short illustrative, non-canonical scenario, a few clearly distinguishable actors and tensions; values, specific factions and events require separate author approval.
- **Show causality, not black boxes:** any eventual game rule needs an understandable explanation linking a choice to its effects. Never treat LaclauGPT's analytical categories as proven transition laws.
- **Board-game clarity:** high-level political map/network and faction cards; event text and leader choices, rather than detailed geography, movement or bureaucracy.
- **One consequential decision at a time:** keep decisions sparse and interesting; skip idle turns, endless notifications and repetitive agent activity.
- **Python standard library core, deterministic/replayable rules after approval**; optional LLM only for flavour/proposals, never necessary for gameplay and never authoritative over state.
- **No historical truth confusion:** real source material, speculative alternate-history canon, generated proposals and simulated events have distinct provenance.
- **Three independent approval gates:** author defines leader RPG mechanics, political transition assumptions and faction-strategy actions before implementing a playable loop. Cross-layer integration is a fourth review.

## Separately reviewable political-simulation design questions

1. What minimal *representation* of a demand, signifier, articulation, formation and communication tie is visible and fun? Which elements can remain narrative tags?
2. How should a player *see* a shift in a coalition or antagonistic frontier without reducing political identity to fixed parties or a spurious research metric?
3. What role do media/institutions/network gatekeepers play in the board game, without conflating reach with persuasion?
4. Which player-facing choices should connect discourse, network access and faction strategy? Define outcomes and their causes **explicitly as fiction/game mechanics**, not scientific predictions.
5. What is the smallest playable scenario with meaningful consequences and a short session length?

## Explicitly deferred

No transplant of Phase 1 LaclauGPT code, models, empirical taxonomies as causal equations, DNA/SNA research workflow, Mongo/Redis/Allas, Mesa population simulator, LLM agent swarms, free-form agent autonomy, global research datasets or massive multi-decade geopolitical simulation.

**A useful test for scope:** if a feature does not help the player understand or make an interesting political decision within a short session, it probably belongs to the research project, not to the first NoöPunk strategy game.
