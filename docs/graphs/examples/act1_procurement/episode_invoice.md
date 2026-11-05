---
id: episode.invoice
kind: episode
series_id: series.europol01
title: "The Tuesday Complaint"
scene_ids: [scene.invoice.briefing, scene.invoice.interview, scene.invoice.depot]
goal_ids: [goal.medium.close_the_complaint]
entry_flags: [case.open]
exit_flags: [case.ledger_read]
required_scenes: [scene.invoice.briefing, scene.invoice.interview]
alternative_episode_ids: []
author_status: draft
---

# What this episode is about

A courier company is billing Helsinki's social services for deliveries that never happened, and the officer who
notices is three months out of the academy. Nobody is in danger. That is the point: the first thing she learns is
that fraud is boring, and that boring fraud is protected by people who are not boring at all.

# The mandatory spine

* The briefing grants `lead.invoice.duplicate_account` (Administer, access `office`).
* The interview grants `lead.invoice.depot_route` (Talk, declared interview).
* The depot scene is reachable from that lead regardless of how the interview went.

# What can go differently

A botched interview costs trust and a day; a botched depot visit costs a warrant and a week. Neither removes a
mandatory scene.

# What this episode must not do

No astral perception, no telepathy, no magical warrant, no skipped chain of custody. The only anomaly is a bad
dream at the end and a maintenance log that does not quite add up.

# GM-only information

The van in the depot's night log is the same one that appears in Act II. Nothing here names it.
