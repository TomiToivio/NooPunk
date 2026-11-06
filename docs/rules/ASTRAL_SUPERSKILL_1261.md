# Astral Projection as an Astral-domain superskill (#1261)

> **Status: the rank table and its gates, implemented; ranks 2–4 are design-only.** `src/rules/astral_ranks.py` adds the
> author's 2026-11-06 revision — *understanding, perception, capability* — on top of the body rules in
> [`astral_body.py`](../../src/rules/astral_body.py) and the graph invariants in `astral.py`. It does not replace
> either, and it does not create a second body, sheet, HP pool or combat skill.
>
> **Read alongside:** [tabletop/ASTRAL_1261.md](../tabletop/ASTRAL_1261.md) (perception filter, targeting, entry
> triggers) · [rules/ASTRAL_PSI_1164.md](ASTRAL_PSI_1164.md) (the prototype record) · [#1178](../design/DRAFT_NOOPUNK_PSIONICS.md)
> (why the PC may not take SWN Precognition or Teleportation).

## The design principle, as implemented

Astral Projection is a **superskill inside the Astral**. It gives very little direct power in Physical or Cyber
scenes; inside Noöspace it is the primary ability for projecting, moving, perceiving and — at the top ranks — touching
information. Each rank is three things at once, and the module stores all three:

| rank | understanding | perception | actions |
|---|---|---|---|
| **0 Disorientation** | no QIP or Law of One model; assumes physics still applies; may not tell dream from projection | Near Astral only, physical world visible but warped and symbolic | separate, walk, basic encounters, return |
| **1 Lucidity** | the astral does not obey ordinary geometry; QIP grasped in practice | dreams visibly constructed from quantum information, still unreliable | fast flight, Lower Astral, enter constructed dream worlds |
| **2 Conscious Agent Network** | astral objects are quantum information exchanged between agents | agents as information-bearing structures | **ROTE** (transmit/receive organised thought); **learn Ident** |
| **3 Authorised informational agency** | appearance distinguished from the information underneath | wave functions and collapse in NoöPunk's own idiom | **Use Ident**; edit quantum information *within an authorised scope* |
| **4 Cosmological research** | Noöspace as a fictionally interpreted Hilbert space; dim timelines | higher-plane interpretations, uncertain and incomplete | Devachanic, Etheric, Buddhic; Akashic research |

Capabilities are **cumulative**: rank 3 keeps everything rank 2 had. `has(rank, Capability.X)` is the only supported way
to ask, so no caller can invent a capability by reading the table directly.

## Scope: rank 0–1 at creation, and only that

`starting_rank()` **refuses** 2–4 rather than clamping. A character created at rank 3 is not a balance problem to be
tuned; it is a scope violation, and the refusal says so:

> *the opening allows Astral Projection 1 or lower at creation; rank 3 is design-only until an authorised campaign
> needs it*

The test that pins this is deliberately blunt: if a later change raises `CAMPAIGN_MAX_STARTING_RANK`, the checklist in
the issue has been reopened without anyone saying so.

## Durations are provisional, and marked

| rank | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| provisional cap | 10 min | 60 min | 10 h | 48 h | 7 days |

These are carried over from earlier comments because the author has not approved or replaced them, and the latest
direction makes **understanding and perception** the governing axis. `DURATIONS_ARE_PROVISIONAL = True` exists so that
a future reader can see the numbers are not balance. Do not tune against them.

## Editing is permission, not power

`InformationPattern(pattern_id, owner_id, mutable)` plus `may_edit()` encode the author's rule:

* **mutable = False → nobody edits it**, at any rank. Banks, identities and atoms do not move because a scene's scenery
  was editable.
* **rank 3, own pattern → allowed.**
* **another agent's pattern → needs a mutable pattern *and* an authored mandate.** Rank 4's plane access does not
  change this; the test asserts that explicitly, because "he is a cosmologist now" is exactly the reasoning that would
  otherwise creep in.
* `require_edit()` refuses with the reason: not editable / another agent's / this rank cannot edit.

## What it does not do, and each is a test

* **No second body or sheet.** The module exports no `Projection`, no `Combatant`, no combat class; the body model stays
  in `astral_body.py`, and `astral_body.ASTRAL_DAMAGE_BRIDGE_APPROVED` remains `False`, so astral damage is still not a
  mechanic.
* **No physical power at any rank.** A rank-4 projector still cannot take a physical action while projected — it is a
  navigator, not a poltergeist.
* **No SWN Teleportation, and no Telepathy smuggling.** ROTE and Ident are asserted *absent* from the SWN technique
  catalogue: they are Astral techniques, not disciplines.
* **No automatic time travel, no historical editing, no objective omniscience.** Rank 4 perceives timelines
  "dimly and incompletely"; nothing in the module grants a mechanical effect on the past.
* **No real-world physics claim.** QIP, consciousness-caused collapse and split-and-remerge timelines are NoöPunk's
  fictional research programme, as the issue requires.

## Still design-only, and deliberately not implemented

Ranks 2–4 have their **capabilities** listed because the issue's checklist names them, but no scene machinery exists
for ROTE interpretation, Ident learning, timeline observation or Akashic research — and the issue says to keep them
design-only until an authorised campaign needs them. When it does, each gets its own increment with its own tests.

Two questions remain the author's:

1. **Duration and Effort.** Does a projection cost SWN Effort, and how much, per rank? The caps are provisional and
   nothing here charges Effort.
2. **Entering a dream world vs switching Space/Time ↔ Time/Space.** Rank 1 grants the former; the issue warns not to
   silently treat that as the latter. This module grants `DREAM_ENTRY` and does **not** grant a general mode switch —
   `astral_body.Projection.shift_mode()` still requires an authored transition.
