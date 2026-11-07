# NoöPunk Simulator Graphs

**Home for versioned graph schemas, small inspectable fixtures and graph data defining the NoöPunk world.** This directory is not a second simulation engine. See [issue #1309](https://github.com/TomiToivio/NooPunk/issues/1309).

## Three Simulator graph views (planned)

1. **Social Graph:** actors (persons, organizations, factions) and directed/reciprocal typed social and communication relations. Foundational SNA graph.
2. **Ideology Graph:** demands, claims, political articulations and faction positions. DNA actor–concept–position statements link this view to Social Graph actors. **This is a Simulator-specific projection**, not an unreviewed fifth RPG graph family.
3. **Physical Graph:** navigable Helsinki City Graph (locations and directed routes), optionally nested Location Graphs for rooms and doors later. Initial fixture should be small and verifiable.

Use shared, stable node references and versioned export schemas. The existing [RPG/world Graph and Tag contract](../../docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md) currently defines Physical/Cyber/Social/Story graph families, so document and test mappings rather than changing them silently. Tomi's [Social](../Paper/SOCIAL_GRAPH.md) and [Physical](../Paper/PHYSICAL_GRAPH.md) draft ideas are **read-only primary design inputs**; author-generated summaries belong in `../Rulebook/`. Don't invent Helsinki geocoordinates or social ties.

**Status:** directory scaffold only. Graph fixtures/schemas and Python implementations remain separate incremental tasks tracked in #1309.
