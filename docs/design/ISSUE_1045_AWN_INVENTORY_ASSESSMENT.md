# Issue #1045 — Ashes Without Number: status assessment and compatibility matrix

Companion to `ISSUE_1045_AWN_INVENTORY.md`, which carries the issue text as source material. That file
states *what must be inventoried*; this one answers it item by item with a status, a source page and a
named gap — the "current implementation status" column the issue asks for and prose cannot guess.

**This is a planning artefact, not an implementation mandate.** It inventories the AWN rulebook against
what NoöPunk already has, assigns P0–P3 priorities, records the gaps that need the book in hand, and
proposes the follow-up backlog. No AWN mechanic is added by this document.

## Licensing position (decides what "implemented" may mean)

AWN has **no verified open licence** in this repository (`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`,
`data/sources/game_system_rights.json`: `blocked-unverified`). The existing `src/rules/awn_survival.py`
already sets the pattern this inventory follows: mechanics are **re-expressed in original wording**,
no source sentence or table heading is reproduced, unimplemented tables are not invented — `forage()`
*takes the difficulty from the caller* and the contract records
`foraging.difficulty_table_transcribed: false`. Every "implemented" below means implemented **under
that constraint**, and every "blocked" means the number is not in the repository and must not be
invented by an agent.

## Status vocabulary

`implemented` — code plus tests exist and are green. `partial` — some of the mechanic exists, with a
named gap. `planned` — specified here, not built. `blocked` — needs a decision or the authoritative
table before code. `deferred` — deliberately not now.

## P0 — usable in NoöPunk's *localized* After the Fall

| AWN source | Mechanic | Status | Where / gap |
|---|---|---|---|
| pp. 56–58 | Stress, Breakdown, Hardening, Addiction, Recovery | **partial** | `awn_survival.py` covers privation → System Strain; the *stress/breakdown/hardening* subsystem of #928 is modelled in `mods/noopunk/stress.gd` (Godot) and **not** ported to the Python rules. Reconcile with #928 before writing a second tracker. |
| pp. 52–55 | Injury, healing, System Strain, Major Injuries, disease, radiation | **partial** | CWN already owns healing and strain (`cwn_healing.py`, `cwn_strain.py`, `cwn_major_injury.py`). AWN's *extensions* (crisis-zone disease/radiation) are not transcribed; the boundary is "add only what CWN lacks". |
| pp. 59–63 | Hunger, thirst, supplies, overland travel, scouting | **implemented** | `awn_survival.py` + `data/rules/awn_survival.json`: travel hours per terrain/mode/road, exposed travel, encounter check, scouting days, going astray, food encumbrance, privation strain, forage (caller-supplied difficulty) |
| pp. 72–75, 102–103 | Tech levels, scrap, damage/repair/build/modify gear, identifying tech | **not started** | CWN owns equipment/combat; AWN's scavenging and improvised repair are additive and unbuilt. Blocked on the book's tables. |
| pp. 104–135 | Enclaves and settlements: Power, Cohesion, Features, Problems, Dominion, Interest, actions, turns, tags | **not started** | Design-relevant for UNSA field bases and quarantine districts. Must be modelled at a **different scale** from SWN factions — see the three-scale table below. |
| pp. 152–189 | Encounter sites: tags, history, features, occupants, hazards, salvage | **not started** | Content data, not rules; best delivered as scenario files once a site format exists. |

## P1 — regional crisis progression

| AWN source | Mechanic | Status | Note |
|---|---|---|---|
| pp. 136–145 | Campaign genres, region creation | **planned** | the two-level world model below is the NoöPunk-side design; AWN supplies procedures, not a world state |
| pp. 146–151 | Building crises: pressure, escalating complications | **planned** | must never force apocalypse; crises escalate only from recorded events |
| pp. 190–201 | Crisis / exploration / social adventures | **planned** | the renewable UNSA case hook |
| pp. 105–135 | Enclave turns, regional state evolution | **deferred** | depends on the enclave model above; and must not duplicate SWN faction turns |
| pp. 49–53 | Chases, pursues, vehicle combat, lethality options | **deferred** | CWN vehicle rules exist; AWN adds only what a broken-infrastructure chase needs |
| pp. 66, 204–205 | GM complications, reaction, morale | **planned** | useful for GM-less single-player NPC reactions; overlaps `mud/systems/agents.py` |

## P2 — selectable capabilities and adversaries

Character creation (pp. 4–35), mutations/stigmas (pp. 16–25), equipment catalogues (pp. 70–103),
creatures (pp. 202–229), Evil Techno-wizards (pp. 255–257), Ash Sorcerer (pp. 258–263), Mentalist
(pp. 264–269), modular power armour (pp. 270–277).

Status: **deferred as a block.** Rationale: each is either a CWN character-generation competitor
(forbidden by the issue), a duplicate of an existing tradition (Ash Sorcerer vs. WWN High Mage as
hermetic PSI, Mentalist vs. SWN psionics — both already implemented), or content that needs an authored
setting decision. Nothing here is a mechanical gap in current play.

## P3 — defer or reject

| AWN source | Item | Decision |
|---|---|---|
| pp. 278–285 | Hub settlement rules | **deferred** — belongs to long-term sandbox play |
| pp. 286–293 | Settlements and mass combat | **deferred** — would make three parallel conflict scales (CWN combat, SWN factions, AWN mass combat) |
| pp. 230–253 | The Albuquerque Death Zone | **rejected as canon** — design example only; no geography, classes or names imported |
| p. 67 onward | Mixing Sine Nomine games | **read on demand** — the conversion guidance is the reference when a cross-system rule is needed |

## Two-level world model (NoöPunk design, not AWN rules)

The issue requires a *region* layer and a *world* layer, so that collapse is per location while the
world keeps functioning.

| axis | region values | world field |
|---|---|---|
| physical infrastructure | `functioning` / `emergency` / `after_the_fall` / `recovering` | share of regions per state |
| public safety | same ladder | global trend |
| supplies | same ladder | trade continuity |
| governance | same ladder + `contested` | treaty/authority status |
| communications | same ladder | network reach |
| NHI/PSI anomaly intensity | `none` / `sporadic` / `persistent` / `breached` | disclosure pressure |
| ontological shock | `none` / `local` / `regional` / `global` | public understanding index |

Rules that follow from the two layers, and that any implementation must respect:

1. A **functioning** region plays as ordinary CWN: no AWN overlays, no scarcity bookkeeping.
2. An **after_the_fall** region activates the AWN overlays this inventory marks P0 (travel/supplies,
   privation strain, site hazards).
3. Transitions are **event-driven and recorded**: a region changes state because a dated event says so
   (a breach, a convoy, a quarantine), never because a clock says so.
4. Recovery is possible and is the point: stabilising interventions move `after_the_fall` →
   `emergency` → `recovering` → `functioning` with the same audit trail.
5. A **Crisis Campaign** is a run of such events, not a scripted apocalypse; the world layer records
   the aggregate, and the player's choices are inputs.

## CWN → AWN compatibility matrix

| AWN mechanic | CWN already has | Verdict |
|---|---|---|
| System Strain | `cwn_strain.py` (max strain, recovery) | **reuse** — AWN privation *adds* strain, it must not add a second pool |
| Healing / Major Injuries | `cwn_healing.py`, `cwn_major_injury.py` | **reuse** — AWN crisis hazards call into these |
| Injury and death | `cwn_injury_procedure.py` | **reuse** |
| Edges and Foci | `cwn_edges_foci.py`, `cwn_foci.py` | **do not port AWN's**; if a regional NPC needs a flavour option, express it as a CWN Focus |
| Combat and vehicles | `cwn_combat*.py`, `cwn_vehicles.py` | **reuse**; AWN chase rules only if a specific need appears |
| Equipment and encumbrance | `cwn_equipment.py`, `cwn_encumbrance.py` | **reuse**; AWN catalogues are additive items, not a new economy |
| Stress / Breakdown / Hardening | partial in `awn_survival.py` + Godot `stress.gd` | **reconcile with #928 first** — a single stress model, not two |
| Enclaves | nothing | **new scale** (see below) |
| Travel/supplies | `awn_survival.py` | **already implemented** |

### Three scales, one world

| scale | owner | turn | changes what |
|---|---|---|---|
| character | CWN | scene | health, strain, standing |
| enclave / settlement | AWN (planned) | day/week | local power, cohesion, supplies |
| faction / institution | SWN | faction turn | assets, credits, influence |

They must share **ids and dates**, not a schema: an enclave belongs to a region, a faction can own an
asset in an enclave, and a CWN mission is evidence that a faction action or an enclave event happened.
Any implementation that merges the three into one turn loop has failed the issue.

## Backlog this implies

1. **Reconcile stress** with #928 before any AWN stress code (P0, small, unblocks the rest).
2. **Region/world state module** with the axes above, dated events and transitions (P0 design → code).
3. **Enclave model** at settlement scale with an explicit mapping to SWN faction assets (P1).
4. **Crisis procedure** (pressure, escalation, stabilisation) driven by events (P1).
5. **Site format** for anomalous encounter locations (P1, content).
6. **Scrap/repair** only if a scenario needs it (P2, blocked on tables).

Nothing in this backlog requires touching CWN, and none of it is started by this document.
