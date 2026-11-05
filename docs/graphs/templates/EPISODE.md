---
record: episode
episode_id: ep01_the_tuesday_complaint
series: campaign01
act: 1
title: The Tuesday Complaint
scenes:
  - sc01_01_briefing
  - sc01_02_depot
  - sc01_03_ledger_room
  - sc01_04_interview
medium_goals:
  - goal:close_the_complaint
entry_conditions:
  - flag:campaign_started
exit_conditions:
  - flag:ledger_read
required_scenes:            # never gated behind a roll
  - sc01_01_briefing
  - sc01_03_ledger_room
alternates: []              # other episodes this one may hand over to
---

# <Episode title>

## What this episode is about
One paragraph. The human situation, not the plot machinery.

## The mandatory spine
The scenes and facts that must happen for the episode to be honest. Everything else is optional.

## What can go differently
The branches, and what they change — flags, relationships, later scenes.

## What this episode must not do
The shortcuts it must not offer: no astral clue, no magical warrant, no skipped chain of custody.
