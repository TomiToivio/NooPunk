# #517 — Acceptance record: cyberspace lore and hacking procedures

**What this record is.** A criterion-by-criterion check of issue #517 against the merged design artefacts. It exists because an issue's checkboxes are usually unticked whatever the real state, so closure has to be argued from the files, not from the issue text or from a previous comment.

**What closure does and does not mean.** Closing #517 means the **documents it asked for exist**. It does **not** mean any rule was approved, any number was fixed, or the setting is canonical. Every mechanical value remains an author decision, listed at the end of this record.

## The deliverables

| # | Criterion (from the issue) | Where it is answered | Status |
| --- | --- | --- | --- |
| 1 | Consolidated cyberspace setting/lore document referencing existing #344 | `docs/design/ISSUE_517_CYBERSPACE_AND_HACKING.md` §1-§3; cross-references `strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md` and `strategy_game/cyber.py` | met |
| 2 | Network layers, topology and Safenet/old-Internet containment, including physical barriers and long-distance hub hopping | §2 ("Technical geography, access and law"): severed links and air gaps as *physical* containment, Safenet as deliberately slow, multi-hop hub routing, drone limits | met |
| 3 | Distinct lore, agendas, constraints and encounter hooks for Panopticon, Noösphere and Thanatos | §3: one table row per swarm with role, signature/limitation and an encounter hook; explicit "distributed instances, not omnipresent gods" | met |
| 4 | AI legality, human-in-the-loop economy, low UBI and employment consequences documented | §2 (legality and UBI) and §2a ("What the AI law looks like from the inside"): verification farms, operator jobs, corporate exemptions, safety theatre, black-market autonomy, liberation politics, and the legitimate case for the regime | met |
| 5 | Playable, concise hacking procedures compatible with existing RPG stats/tags and C/I/N | §4: a six-step procedure expressed entirely in the approved Fate vocabulary, with C/I/N as device/session descriptors rather than new stats | met (proposal) |
| 6 | Stealth/drone/physical-access integration, BCI safeguards and mixed-success consequences | §2 (air gaps, drones, infiltration), §4 step 5 (trace/detection/quarantine/exposure outcomes), §4 "Neural interface safeguards" | met (proposal) |
| 7 | Worked example investigations/encounters and hooks for future tactical/strategy layers | §5 A-D (municipal LAN, multi-hop international, air-gapped lab, ASI contact), §5b same-target-three-eras regression, plus #515's tactical map data which references connectivity rather than re-deciding it | met |
| 8 | Consistency review with the NHI Crisis timeline, AI/PSI lore and issue #344 | §1's three-era table states the campaign opens **before** the crisis and #517 describes the post-crisis configuration; the regression narrative in §5 exercises one target in all three eras | met |

## The one reconciliation this record depends on

Issue #517 is written from the **post-crisis** side, while the binding canon for the crossover is that play *starts during the acceleration toward the NHI Crisis* and the crisis is never narrated as already resolved. The documents reconcile this explicitly rather than silently: the campaign opens in the **acceleration** era, the crisis is a horizon the campaign moves toward, and #517's Safenet / Firewall / three-ASIs configuration is the **after-crisis** era of the same continuous model. Nothing dates the crisis, and no post-crisis detail retroactively describes the opening.

That is a **reading of the issue against canon**, not an author ruling. If the author intends the campaign to *begin* post-crisis, this record's reconciliation is the thing to overturn first.

## Author decisions explicitly left open

Carried forward, not buried by closure:

- The AI capability/control threshold, exemptions, audit method and penalties.
- Whether C/I/N modifies any roll at all, and if so how.
- Trace, heat and latency timing; Firewall/ICE resistance values; multi-hop cost.
- Panopticon's authority and how its erratic behaviour is adjudicated.
- Calibration of wetware/BCI consequences.
- Faction-wide effects of a cyber mission on the strategy layer.
- The number of network hops that counts as "long distance".

None of these has a number in the repository, and none should get one before the core rules in #516 are approved.

## Verification

- The documents contain no numeric rule constants — they are prose that names the *shape* of decisions.
- The only executable cyber artefact in the repository remains `strategy_game/cyber.py`, which enforces **access-path feasibility** (does a path exist in this era?) and deliberately knows nothing about check difficulty. Its contracts pass on `main`.
- No test asserts anything about this lore, per the repository's testing policy (#271): creative material is reviewed by the author, not by a text-matching guard.

— recorded by Ai (愛), 2026-10-19
