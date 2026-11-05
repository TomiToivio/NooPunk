---
record: scene
scene_id: sc01_04_interview
title: The interview
types: [social, investigation]      # Investigation | Exploration | Combat | Social | Cyber | Astral
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
    benefit_cost: a Talk check, and a favour owed
transitions:
  - to: sc01_05_depot
    when: flag:ledger_read
outcomes: []
flags: []
links: []                            # cross-layer effects, one block each; see the proposal §4
---

# The interview

## Setting
Where this happens, what it smells like, who is uncomfortable.

## What the player can do
Plain prose plus the CWN skill that governs each action. No new skills.

## The clues
Which are mandatory, which are extra, and what each costs.

## What happens if it goes wrong
Failure here changes time, trust and risk. It does not remove a mandatory scene.
