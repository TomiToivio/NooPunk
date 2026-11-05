---
id: helsinki.physical
kind: physical
version: 1
source_doc: design/graphs/README.md
author_status: draft
---

# Nodes

```yaml
nodes:
  - id: physical.kurvi.home
    canonical_ref: location.kurvi.home
    node_type: room
    scale: location
    parent_id: physical.helsinki
    visibility: player
    tags: [housing]
    coordinates: null
edges:
  - id: route.kurvi.home.to.street
    from: physical.kurvi.home
    to: physical.kurvi.street
    type: traverse
    directed: false
    access: resident
    cost: cwn_travel
```

# Cross-layer references

```yaml
links:
  - id: cross.kurvi.home.bci
    from: physical.kurvi.home
    to: cyber.kurvi.bci
    relation: control_device
    requires: {abilities: [cwn_hacking_authorized_device_access], gate: bci_paired}
    effect: {type: provide_status, does_not_grant: [core_clue, physical_lock_bypass]}
    visibility: discovered
```
