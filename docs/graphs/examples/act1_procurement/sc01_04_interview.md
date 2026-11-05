---
record: scene
scene_id: sc01_04_interview
title: The interview
types: [social, investigation]
series: campaign01
episode: ep01_the_tuesday_complaint
participants: [character:rookie, npc:maki]
nodes: [physical:kurvi_office_room2, social:npc_maki]
spoiler_gate: act1
available_actions:
  - ask_about_invoices
  - ask_about_shift_swap
  - show_credentials
clues:
  - id: clue_invoice_gap
    kind: core
    competency: Administer
    access: office
    inquiry: search
    fact: Two invoice numbers share one delivery
  - id: clue_shift_swap
    kind: core
    competency: Talk
    access: interview
    inquiry: interview
    fact: The dispatcher swapped the Tuesday shift
    leads_to: [physical:vallila_depot]
  - id: clue_motive_gossip
    kind: optional
    competency: Talk
    access: interview
    inquiry: interview
    fact: He is protecting a cousin
    benefit: he names the cousin
    benefit_cost: a Talk check and a favour owed
transitions:
  - to: sc01_05_depot
    when: flag:ledger_read
flags: [interview_done]
links: []
---

# The interview

## Setting

A shared office in the Kurvi building, second floor, radiator too warm. The dispatcher, Maki, has been
seconded from the depot for the afternoon and has decided in advance that this is a waste of his time.

## What the player can do

* **Read the file with him** — Administer with access `office`. No roll: the two invoices share a delivery.
* **Ask about the Tuesday shift** — Talk, declared as an interview. No roll for the fact that the shift was
  swapped; the *reason* is the optional clue.
* **Show the credentials** — permission, not compulsion. It gets a request considered; it does not get a
  confession.
* **Press him about the cousin** — a Talk check. Success names the cousin; failure costs a favour and a
  relationship note.

## The clues

`clue_invoice_gap` and `clue_shift_swap` are **core** and cannot be missed: they are granted for competence plus
declared access and inquiry. `clue_motive_gossip` is optional — it improves what the case looks like later, and
its price is a roll plus an obligation.

## What happens if it goes wrong

If Maki shuts down, the scene ends with `interview_done` and a relationship note of −1. The depot scene is still
reachable, because `clue_shift_swap` was already granted. What is lost is time and goodwill — never the case.
