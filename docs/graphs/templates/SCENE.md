---
id: scene.invoice.interview
kind: scene
episode_id: episode.invoice
types: [social, investigation]
graph_refs:
  physical: [physical.kurvi.office.room2]
  cyber: []
  social: [social.actor.maki]
  astral: []
goal_ids: [goal.short.verify_invoices]
lead_ids: [lead.invoice.depot_route]
evidence_ids: [evidence.invoice.workshop_log]
visibility: player
entry_flags: [case.open]
transitions:
  - to: scene.invoice.depot
    when: flag.ledger_read
author_status: draft
---

# Opening
<!-- Tomi writes -->

# Player-visible situation
<!-- Tomi writes -->

# Core leads / evidence / access
<!-- Tomi writes: name the competence, the access and the declared inquiry for each -->

# NPC intentions and relationship choices
<!-- Tomi writes -->

# CWN checks for risky actions (never for indispensable clue discovery)
<!-- Tomi writes -->

# Outcomes and next scenes
<!-- Tomi writes -->

# GM-only information
<!-- Tomi writes -->
