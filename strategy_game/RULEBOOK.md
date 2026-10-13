# NoöPunk Strategy Game: Rulebook (placeholder)

**Status (issue #389): Fate Core RPG foundation approved.** An original, bounded Fate-based Python RPG implementation and a tabletop-playtest manual now exist at [rpg/RULEBOOK.md](rpg/RULEBOOK.md). This is a playable RPG slice, not a complete Transhumanity's Fate reproduction; further NoöPunk conversions remain pending. **Faction strategy and political simulation rules are not yet approved.** Separate from existing NoöPunk legacy RPG rules; do not automatically import their mechanics.

## Layer I: Faction leader, narrative RPG
**Author-selected baseline:** Fate Core four actions, 4dF + skill, character aspects, stunts, Fate points, stress and consequences. First Python slice: [`rpg/fate.py`](rpg/fate.py); licensing and gaps: [`rpg/README.md`](rpg/README.md). PSI is natural and not virus-derived. Most humans remain in original biological bodies: cortical stacks and resleeving are optional, new and rare. NoöPunk lore does not inherit Eclipse Phase's setting. Exact NoöPunk skill lists, stunts, equipment permissions, full Fate implementation and future conversions remain to be designed.

**Unapproved design proposal (#295):** [leader/NPC micro-rule example](docs/LEADER_MICRO_RULES_PROPOSAL.md). The worked 2d6 example and all attribute names, numbers and interfaces are for author review only; **none is a rule of this game**.

## Layer II: Network-society political simulation
Reserved: Laclaudian ideological articulation, Castellsian communication power, agents, agency, contested meanings and systemic events. All transition mechanisms **TBD by author**.

Data vocabulary only (no rules): `politics.py` carries `Demand`, `Signifier`, `Formation` and `Frontier`; political relations are ordinary `NetworkEdge` records with a relation-layer label, so the field is one multiplex graph. Design record: [docs/POLITICAL_SIMULATOR_MODEL.md](docs/POLITICAL_SIMULATOR_MODEL.md).

The complementary `political.py` vocabulary and [Gate B design proposal](docs/POLITICAL_SIMULATION_DESIGN.md) introduce standalone articulations, signifier roles and communicative ties. These remain separate from the `politics.py` / `WorldState` representation. Both are containers, **not approved mechanics**; integration requires an explicit decision.

## Layer III: Faction strategy
Reserved: organizational assets, faction management, strategic operations, resource allocation, spatial and network presence. All mechanics **TBD by author**.

**Global factions (author canon, #328/#329):** the seven paradigm factions and their evidence model are recorded in [docs/GLOBAL_FACTIONS.md](docs/GLOBAL_FACTIONS.md) and [`data/global_factions.json`](data/global_factions.json). Setting canon only — the roster defines no mechanics.

## Interfaces and integration
Rules must be authored independently for each layer, then explicitly approved before software implementation. The world-map interface displays abstract state and does not itself determine political, social or tactical outcomes.

## Pending decisions
Character attributes and tag semantics; simulation entities and causal assumptions; granularity/time; faction actions; world-map model; human versus Ollama leader controls; challenge and pacing; outcome resolution; scenarios; save/load compatibility.

Reference proposals are not rules: [docs/RULE_SYSTEM_RESEARCH.md](docs/RULE_SYSTEM_RESEARCH.md).
