---
id: helsinki.physical
kind: physical
version: 1
source_doc: design/graphs/README.md
author_status: draft
---

# Helsinki — physical nodes (example subset)

The canonical opening node data already exists in `data/world/helsinki_locations.json`; this file shows the
**authored record shape**, not a second source. Note the two `source_claim` lines: they are how a documented
conflict stays visible instead of being settled by an agent.

```yaml
nodes:
  - id: physical.kurvi.home
    canonical_ref: location.kurvi.home
    node_type: room
    scale: location
    parent_id: physical.helsinki
    visibility: player
    tags: [housing, agency_owned]
    coordinates: null
    source_claim: "campaign #1132 — company housing in Kurvi; conflicts with the Sörnäinen home in design/graphs/README.md"
  - id: physical.europol.office
    canonical_ref: location.europol.helsinki
    node_type: location
    scale: location
    parent_id: physical.helsinki
    visibility: player
    tags: [workplace, law_enforcement]
    coordinates: null
    source_claim: "employer Europol per campaign #1132; ADDRESS [OPEN] — Ratakatu per design/graphs/README.md"
  - id: physical.vallila.depot
    canonical_ref: location.vallila.depot
    node_type: location
    scale: location
    parent_id: physical.helsinki
    visibility: gm_secret
    tags: [industrial]
    coordinates: null
    source_claim: "episode.invoice"
edges:
  - id: route.kurvi.home.to.europol
    from: physical.kurvi.home
    to: physical.europol.office
    type: traverse
    directed: false
    access: null
    cost: cwn_travel
  - id: route.europol.to.vallila
    from: physical.europol.office
    to: physical.vallila.depot
    type: traverse
    directed: true
    access: credential.europol
    cost: cwn_travel
    blocked_by: flag.ledger_read
```

# Cross-layer references

```yaml
links:
  - id: cross.europol.office.terminal
    from: physical.europol.office
    to: cyber.europol.case_service
    relation: control_device
    requires: {abilities: [cwn_hacking_authorized_device_access], gate: duty_credential}
    effect: {type: provide_case_data, does_not_grant: [core_clue, physical_lock_bypass]}
    visibility: discovered
  - id: cross.kurvi.home.echo
    from: physical.kurvi.home
    to: astral.kurvi.echo
    relation: astral_perceive
    requires: {abilities: [psi_overlay_perception], gate: awakened}
    effect: {type: atmosphere_only, does_not_grant: [clue, travel]}
    visibility: gm_secret
```
