---
record: graph_domain
graph_id: physical:helsinki
graph_type: physical
version: 1
source_doc: design/graphs/README.md
author_status: author
---

# Helsinki — physical graph (example nodes)

A subset, to show the shape. The canonical opening node data already exists in
`data/world/helsinki_locations.json`; this file is the **authoring format**, not a second source.

## Nodes

```yaml
- node_id: physical:kurvi_company_flat
  node_type: location
  label: Kurvi company flat
  parent_id: physical:helsinki
  layer: physical
  coordinates: {map: [0.66, 0.34]}
  tags: [housing, agency_owned]
  visibility: discovered
  unlock_act: 1
  legal_restriction: null
  source_claim: "campaign #1132 — company housing in Kurvi (conflicts with design/graphs/README.md's Sörnäinen home)"
- node_id: physical:europol_helsinki
  node_type: location
  label: Europol Helsinki
  parent_id: physical:helsinki
  coordinates: {map: [0.55, 0.62]}
  tags: [workplace, law_enforcement]
  visibility: discovered
  unlock_act: 1
  legal_restriction: finnish_authority_gate
  source_claim: "address flagged for author review: Ratakatu per design/graphs/README.md, employer Europol per campaign #1132"
- node_id: physical:vallila_depot
  node_type: location
  label: Vallila tram depot
  parent_id: physical:helsinki
  coordinates: {map: [0.72, 0.42]}
  tags: [industrial]
  visibility: GM_secret
  unlock_act: 1
  prerequisites: [flag:shift_swap_known]
```

## Edges

```yaml
- edge_id: edge:kurvi_to_europol
  source: physical:kurvi_company_flat
  target: physical:europol_helsinki
  relation: route
  directed: true
  access_condition: null
  travel_cost: scene
  knowledge_gate: flag:knows_office
  provenance: campaign #1132
- edge_id: edge:europol_to_vallila
  source: physical:europol_helsinki
  target: physical:vallila_depot
  relation: route
  directed: true
  access_condition: credential:europol
  travel_cost: scene
  knowledge_gate: flag:shift_swap_known
  provenance: episode ep01
```

## Cross-layer references

```yaml
- node: physical:europol_helsinki
  cyber_ref: cyber:europol_network
  astral_ref: null
```
