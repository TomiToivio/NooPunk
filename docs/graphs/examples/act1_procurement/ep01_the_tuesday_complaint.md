---
record: episode
episode_id: ep01_the_tuesday_complaint
series: campaign01
act: 1
title: The Tuesday Complaint
scenes:
  - sc01_01_briefing
  - sc01_03_ledger_room
  - sc01_04_interview
  - sc01_05_depot
medium_goals:
  - goal:close_the_complaint
entry_conditions:
  - flag:campaign_started
exit_conditions:
  - flag:ledger_read
required_scenes:
  - sc01_01_briefing
  - sc01_04_interview
alternates: []
---

# The Tuesday Complaint

## What this episode is about

A courier company is billing Helsinki's social services for deliveries that never happened, and the officer who
notices is three months out of the academy. Nobody is in danger. That is the point: the first thing she learns is
that fraud is boring, and that boring fraud is protected by people who are not boring at all.

## The mandatory spine

* The briefing gives her `clue:invoice_gap` (Administer, access `office`).
* The interview gives her `clue:shift_swap` (Talk, declared interview) and a lead to the depot.
* The depot scene can then be reached with or without a good roll — the *lead* is granted, not the success.

## What can go differently

A botched interview costs trust and a day; a botched depot visit costs a warrant and a week. Neither changes the
mandatory spine.

## What this episode must not do

No astral perception, no telepathy, no magical warrant. The only anomalies are a bad dream at the end and a
maintenance log that does not quite add up.
