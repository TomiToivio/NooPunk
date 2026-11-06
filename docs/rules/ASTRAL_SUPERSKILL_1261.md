# Astral Projection as a superskill — ranks 0–4, MVP 0–1 (#1261)

> **Status: author-directed draft; the issue stays OPEN.** Astral Projection is an **astral-domain
> superskill**: very little direct power in Physical or Cyber scenes, and the primary ability for
> projection, movement, perception and — at higher ranks — understanding inside Noöspace.
>
> **Ranks 2–4 are design-only.** The initial campaign allows rank **0 or 1** only. The runtime gates in
> [`src/rules/astral_progression.py`](../../src/rules/astral_progression.py) refuse the rest by name.
>
> **This supersedes the earlier plane-access ladder** that put Devachanic/Etheric/Buddhic at rank 2.
> Present-day physics does not establish consciousness-caused collapse, objective Akashic records, or
> timelines that split and re-merge: those are the setting's research claims, inspired by the Law of One.

## 1. What a rank states

Three things at once, and a rank is not "more minutes outside the body":

1. **The character's model of reality** — the QIP and Law of One framework she actually holds.
2. **What she can perceive and interpret.**
3. **What she is permitted to do.**

The table is data: [`data/rules/astral_progression_1261.json`](../../data/rules/astral_progression_1261.json).

## 2. The ladder

| Rank | Understanding | Reach and permissions |
| --- | --- | --- |
| **0 — Disorientation** | No Astral familiarity, no QIP, no Law of One. Assumes physical laws still apply; may not know whether she is dreaming. | Near Astral only, with the physical world visible but warped. Separation, walking, observing, basic encounter and return. **No flight, no Lower Astral.** |
| **1 — Lucidity and dream navigation** | Realises that geometry and inertia do not govern Noöspace; begins to grasp QIP in practice; understands that dreams are built from quantum information. | Fast movement and flight without locomotion. Deliberate entry to the **Lower Astral**, constructed dreams and collective-unconscious places. No ROTE, no Ident work, no editing. |
| **2 — Conscious Agent Network** | Recognises that solid-looking astral objects are rendered quantum information exchanged among Conscious Agents. | **Transmit Information (ROTE)** — send and receive organised conceptual packages, inside the Astral only. **Learn Ident** — acquire and recognise a known agent's persistent identity. Still cannot *use* it. |
| **3 — Authorised informational agency** | Understands that the interface renders information, energy and matter differently; begins to perceive wave functions and collapse as the setting depicts them. | Read, write, edit and delete **quantum information within her own authorised scope** — normally her own, plus limbo worlds whose ownership the scene states. **Use Ident** — instant astral travel to a known agent's presence, not physical teleportation. |
| **4 — Cosmological research** | Noöspace as a fictionally interpreted infinite-dimensional Hilbert space; Law of One higher planes; dim alternative timelines and dimensions. | **Devachanic, Etheric and Buddhic planes**, Akashic research, authored timeline observation — uncertain and incomplete. No time travel, no historical editing, no omniscience, no compulsory access to another agent's information. |

**Permission is the governing distinction.** Rank 3 may edit what it owns or what a scene explicitly says is
malleable. It may not write to another agent, a protected mind, a physical system, a secured Cyber node or
shared reality. Editable symbolic scenery is not an edited bank record.

## 3. MVP: ranks 0 and 1

**Rank 0 — unfamiliar Astral Body.**

- Entry is voluntary-with-ability or scripted (sleep, NDE, psychotronics, authored event). The body stays
  where it was and stays vulnerable.
- She sees the **Near Astral with its physical overlay**: right room, wrong light. Physical objects look
  warped or symbolic; astral occupants appear according to the perception filters.
- She may try walking, touching doors, talking and observing as if ordinary physics applied; the real
  effects are resolved by the physical-versus-astral target restrictions that already exist in
  [`astral_body.py`](../../src/rules/astral_body.py).
- Disorientation is narration; **player agency is not removed**. Investigate a nearby anomaly or return.
- Nothing unlocks flight, the Lower Astral or ROTE at rank 0.

**Rank 1 — lucid navigator.**

- Flight and fast movement without physical locomotion; **no SWN Teleportation, no physical flying**.
- Deliberate entry to the **Lower Astral**, personal dream worlds and collective-unconscious places; she can
  watch a sleeping agent construct a dream out of quantum information.
- She perceives the *process* of dream construction but **cannot read or write arbitrary information and
  cannot send a ROTE**.
- The GM keeps three things apart in the data: an actual conscious agent, a generated dream avatar, and
  symbolic imagery. Lower planes can be hostile; CWN unarmed astral interaction applies; retreat is a
  choice.
- **The two-scene test:** an awkward bedroom OOBE with the real room visible, then lucid flight over
  near-Astral Helsinki into a dream landscape. Afterwards the body is still anchored and no investigation
  shortcut has been produced.

## 4. Ranks 2 and 3: ROTE and Ident

- **ROTE (rank 2)** is an **Astral Projection** technique, not Telepathy: a packet of condensed thought,
  concept, image, feeling and memory. Experientially a download rather than a sentence. Packets can be
  misread, and interpreting one into ordinary language takes time.
- **Learn Ident (rank 2)** acquires a persistent noetic identity: not a name, a body or an address. Knowing
  it reveals neither the target's physical position nor their consent.
- **Use Ident (rank 3)** relocates the Astral Body instantly to a *known* agent's astral presence, within
  approved plane access and subject to AntiPSI and agency constraints. It is not SWN Teleportation and it
  does not move the body.
- **Rank 3 edit rights** are permissions over quantum information the character is authorised to touch.
  Every scene that offers them must say **who owns the pattern**.

## 5. Durations

The provisional ceilings are **retained as provisional only**: 10 minutes at rank 0, 60 at rank 1, 10 hours
at 2, 48 at 3, 7 days at 4. The author has not approved them, and a longer projection must never be
mistaken for more reliable knowledge. They live in the data file with an explicit
`duration_status: "provisional caps"`, and the module returns them without implying finality.

## 6. What the interface looks like as rank rises

Rank 0 renders a near-physical headset with hallucinations. Rank 1 renders thought-responsive dream
construction. Rank 2 renders self-transforming conscious-agent meshes and ROTEs. Rank 3 renders
informational permissions and editable limbo. Rank 4 renders high-dimensional timelines and Akashic
patterns. PSI stays primary; Magick is the secondary, culturally conditioned interpretation of the same
phenomenon.

## 7. Boundaries that do not move

- **No physical or Cyber power at any rank.** No hacking, no root access, no teleporting the body.
- **No second Astral Combat skill and no astral hit-point pool.** Astral unarmed combat is CWN Punch; the
  damage bridge to the CWN body is still unapproved (`ASTRAL_DAMAGE_BRIDGE_APPROVED = False`).
- **No evidence shortcut**: an astral observation is a lead, never proof.
- **No free write access** to another agent, a protected mind or a secured system.
- **No automatic time travel, resurrection or omniscience** at rank 4.

## 8. What is implemented, and what is not

| Concern | Where | Status |
| --- | --- | --- |
| Rank table, names, understanding, permissions | `data/rules/astral_progression_1261.json` | data |
| Gates: 0–4 range, MVP cap, starting rank, technique minimums, plane access, duration caps, domain check | `src/rules/astral_progression.py` | implemented |
| Tests for every gate above | `tests/test_astral_progression_1261.py` (16) | implemented |
| Body, perception filters, targeting, manifestation | `src/rules/astral_body.py` (#1262) | implemented |
| ROTE, Learn Ident, Use Ident as playable techniques | — | **design-only, refused by gate** |
| Ranks 2–4 scene content, planes, Akashic research | — | **design-only** |
| Astral damage bridge | `astral_body.apply_astral_damage` refuses | awaiting author approval |

## 9. Open decisions

1. **Durations.** Keep the provisional ceilings, or replace them with a scene-based cost?
2. **Effort.** Which SWN commitment mode does a projection use, and does a device-level rank 0 cost Effort at
   all?
3. **Rank 1 and Time/Space.** Rank 1 enters dream worlds that *resemble* Time/Space. Is deliberate switching
   a rank 3 permission, or a rank 1 one with a narrower scope?
4. **Ident consent.** What does a target feel when an Ident is learned, and does AntiPSI detect it?
5. **Rank-3 edit ownership.** Who audits a character who edits their own information, and what does the
   evidence look like afterwards?

## 10. Sources

- Issue #1261: the body and perception work (#1262), the graph invariants (#1263), the author comments of
  2026-11-06 — provisional durations (15:42), **Transmit Information / ROTE** (15:47), **Use Ident** (15:57),
  and the governing superskill update (16:35).
- Robert Monroe — projection phenomenology used as narrative description, never as a rank ladder.
- The Law of One — the metaphysical frame the setting's researchers hold; a claim in a source, not physics.
- Faggin (quantum-information panpsychism) and Hoffman (conscious agents) — vocabulary for the in-world
  model of perception and identity.

## Editing quantum information is permission, not power

Rank 3's "authorised informational agency" is the one place where a rank could quietly become a licence, so it is a
gate on the *pattern* rather than a capability on the rank (`astral_progression.InformationPattern`, `may_edit`,
`require_edit`):

* **an immutable pattern is editable by nobody**, at any rank — bank records, identities and atoms do not move because
  a scene's scenery is malleable;
* **rank 3 edits its own information**;
* **another agent's pattern needs a mutable pattern *and* an authored mandate**; rank alone never grants it, and rank
  4's plane access does not change the rule;
* a refused edit says which of the three reasons applies, so a table can argue with the ruling instead of guessing.

Tests: `tests/test_astral_ranks_1261.py` (the permission gate and the no-duplicate invariants — no second body, no
second combat system, astral damage still gated, ROTE/Ident absent from the SWN catalogue).
