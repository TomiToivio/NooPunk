# NoöPunk Strategy Game: Rulebook (placeholder)

**Status: NO RULES APPROVED.** Separate from all existing NoöPunk RPG rulebooks. Do not auto-import, copy or reinterpret their mechanics.

## Layer I: Faction leader, narrative RPG
Reserved: attributes, personality trait tags, character decisions, roleplay, resolution. All procedures and values **TBD by author**.

## Layer II: Network-society political simulation
Reserved: Laclaudian ideological articulation, Castellsian communication power, agents, agency, contested meanings and systemic events. All transition mechanisms **TBD by author**.

Data vocabulary only (no rules): `politics.py` carries `Demand`, `Signifier`, `Formation` and `Frontier`; political relations are ordinary `NetworkEdge` records with a relation-layer label, so the field is one multiplex graph. Design record: [docs/POLITICAL_SIMULATOR_MODEL.md](docs/POLITICAL_SIMULATOR_MODEL.md).

The complementary `political.py` vocabulary and [Gate B design proposal](docs/POLITICAL_SIMULATION_DESIGN.md) introduce standalone articulations, signifier roles and communicative ties. These remain separate from the `politics.py` / `WorldState` representation. Both are containers, **not approved mechanics**; integration requires an explicit decision.

## Layer III: Faction strategy
Reserved: organizational assets, faction management, strategic operations, resource allocation, spatial and network presence. All mechanics **TBD by author**.

## Interfaces and integration
Rules must be authored independently for each layer, then explicitly approved before software implementation. The world-map interface displays abstract state and does not itself determine political, social or tactical outcomes.

## Pending decisions
Character attributes and tag semantics; simulation entities and causal assumptions; granularity/time; faction actions; world-map model; human versus Ollama leader controls; challenge and pacing; outcome resolution; scenarios; save/load compatibility.

Reference proposals are not rules: [docs/RULE_SYSTEM_RESEARCH.md](docs/RULE_SYSTEM_RESEARCH.md).
