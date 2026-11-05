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
evidence_ids: []
visibility: player
entry_flags: [case.open]
transitions:
  - to: scene.invoice.depot
    when: flag.ledger_read
author_status: draft
---

# Opening

A shared office in the Kurvi building, second floor, radiator too warm. The dispatcher, Maki, has been seconded
from the depot for the afternoon and has decided in advance that this is a waste of his time.

# Player-visible situation

The invoices are on the table between you. Maki's jacket is still wet. He has not asked what this is about.

# Core leads / evidence / access

* **`lead.invoice.duplicate_account`** — core. Competence **Administer**, access `office`, inquiry `search`.
  No roll: two invoice numbers share one delivery. This is the fact the whole case rests on.
* **`lead.invoice.depot_route`** — core. Competence **Talk**, access `interview`, inquiry `interview`.
  No roll: the Tuesday shift was swapped. It points at `location.vallila.depot`.
* **`evidence.invoice.cousin_name`** — optional. Competence **Talk**; a check; the price is a favour owed.

# NPC intentions and relationship choices

Maki is protecting a cousin who drives for the company. He will trade the name if he believes the officer already
knows it. Relationship starts at 0 (`professional`); pressing him and failing moves it to −1, and he remembers.

# CWN checks for risky actions (never for indispensable clue discovery)

* Press him on the cousin: **Talk** vs the difficulty the GM sets from his loyalty.
* Search the office while he watches: **Sneak** — and if it fails, the relationship, not the case, is what breaks.
* Anything administrative (a formal request, a record of the interview): **Work (Europol Agent)**.

# Outcomes and next scenes

On `flag.ledger_read`, `scene.invoice.depot` opens. A failed check ends the interview with `interview_done` and a
relationship note; the depot is *still* reachable, because `lead.invoice.depot_route` was already granted.

# GM-only information

Maki's cousin signed the delivery sheet that does not exist. That is not in this scene unless the optional
evidence is obtained; the depot scene reveals it either way.
