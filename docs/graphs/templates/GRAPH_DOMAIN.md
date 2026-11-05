---
record: graph_domain
graph_id: physical:helsinki
graph_type: physical
version: 1
source_doc: design/graphs/README.md
author_status: author
---

# <Domain> graph — <place>

One file per graph domain. Nodes and edges only; no prose rules. A node may be described in the location
document and referenced here by id.

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
  cwn_ref: null
  source_claim: "campaign #1132: company housing in Kurvi"
```

## Edges

```yaml
- edge_id: edge:kurvi_to_office
  source: physical:kurvi_company_flat
  target: physical:europol_helsinki
  relation: route
  directed: true
  access_condition: credential:europol
  travel_cost: scene
  knowledge_gate: flag:knows_office
  provenance: campaign #1132
```

## Cross-layer references

```yaml
- node: physical:kurvi_office_room2
  cyber_ref: cyber:office_terminal
  astral_ref: astral:kurvi_office_region
```
