# Issue #153 — Long-term layer: faction strategy and political management game

> **For Hermes:** planning only. No RULEBOOK, code, `data/`, or `requirements.txt` changes land
> until the author clears the GATES in §0. Issue #153 is an umbrella that stays open; this plan
> covers the **faction-sheet specification, the strategic turn, and the bridges to the RPG and to
> #152**. Read beside its sibling `2026-10-06_145230-issue152-social-simulation.md`: the two
> long-term layers share one state engine and must be designed together, but land separably.

**Goal:** add an **optional** strategy-game layer above the ordinary RPG, where PCs can become
leaders of factions, institutions, corporations, agencies, movements, cults, states or networks —
**characters first, factions second** (Crusader Kings, not Civilization). Strategy decisions create
missions, dilemmas and consequences for individual characters; adventure outcomes feed back into
faction state.

**Architecture:** the layer is a **facing over the existing deterministic state**, not a new world.
It consumes and emits the same **event log** the RPG and the #152 simulation use
(`src/simulation/events.py`, `world_state.py`), the same **Affect graph**
(`src/simulation/affect.py`), the same **faction taxonomy** (`data/world/faction_taxonomy.json`,
`rulebook/8_FACTIONS.md`) and the same **ideological model** (`data/world/ideology.json`). Strategy
state that is *derived* (network position, leverage in play) is recomputed from the log, never
stored as a private canon file. Optional and off by default.

**Tech stack:** Markdown canon for the faction sheet; `data/world/` JSON/YAML for the
machine-readable sheet; stdlib Python + `unittest` for any deterministic helper; the NetworkX
multiplex graph from #152 for network strategy; `gh` for the PR/comment. No new engine, no parallel
rule system (`AGENTS.md` §13.3, §14).

---

## 0. Decision gates (nothing lands before these)

| Gate | Decision | Owner | Options |
| --- | --- | --- | --- |
| **GATE 1** | The **stat set** — how many faction capabilities, and which | author | **4–6 broad stats** (recommended for MVP: e.g. Wealth / Force / Influence / Network / Legitimacy / Cohesion) **vs** the issue's full 11 (Wealth, Resources, Influence, Network Power, Security, Force, Intelligence, Legitimacy, Cohesion, Reach, Status) **vs** derive stats from Domains+Holdings so no abstract stat exists |
| **GATE 2** | Where the faction sheet lives | author | `rulebook/9_STRATEGY.md` (new chapter) + `data/world/faction_sheet_schema.json` (recommended) **vs** append to `rulebook/8_FACTIONS.md` **vs** `docs/design/` only |
| **GATE 3** | Do player factions use the **same** rules as NPC factions? | author | **yes, symmetric** (recommended — one sheet, one resolver) **vs** asymmetric (PC factions get PC-facing options) |
| **GATE 4** | How much of the strategic turn **auto-resolves** vs becomes an **RPG adventure** | author | auto-resolve small, escalate high-stakes to a scenario (recommended) **vs** resolve everything abstractly **vs** play everything out at character scale |
| **GATE 5** | Internal factions / succession — required at MVP? | author | **defer to Phase B**, ship a unitary faction first (recommended) **vs** build subfactions + succession into MVP |
| **GATE 6** | Interface to #152 | author | **shared event log + schema, separable** (recommended — already agreed in #153's own text) **vs** strategy layer runs standalone with manual world import |

GATE 1 and GATE 4 are coupled: more stats means more to auto-resolve, which raises the bookkeeping
cost the issue itself warns against ("how do we model internal factions without drowning the game
in bookkeeping").

---

## 1. Verified current state (measured on `origin/main` @ `40e10a5`)

Everything below was read from the repo. Tip is `40e10a5`; suite green at **801 tests OK**.

| Fact | Where it lives | Status |
| --- | --- | --- |
| Faction = `US^(constitutive affects) + FRONTIER^(antagonistic affects)`; US/FRONTIER are Affect edges | `rulebook/4_SOCIAL.md`, `rulebook/8_FACTIONS.md` | **Canonical.** This *is* the "hegemonic project + antagonistic frontier + key signifiers" the faction sheet's Identity block asks for — reuse it, do not re-declare. |
| Faction taxonomy: Political / Criminal / Civil Society / Religious / Corporate / Governmental / NHI; NHI type kept separate from political faction; multi-faction membership; **10 starting Reputation points across 2–3 factions (6/4 or 5/3/2)** | `data/world/faction_taxonomy.json`, `RULEBOOK.md` §43 | **Canonical** (#144). The "type" field of the faction sheet already exists. |
| Reputation, Contacts, Motivations are all Affect edges, scale **−10…+10**, directional | `src/simulation/affect.py` | **Canonical** (#107, rescaled #144). The sheet's "Reputation" and "favors/leverage" must map here, not to a new store. |
| Ideology is a **cross-product of paradigm-shift positions**, categorical not numeric | `data/world/ideology.json` | **Canonical** (#8). Do not reduce a faction to a scalar ideology score. |
| Seven SNA layers, numbered; layer 7 (Faction↔Faction) **derived from US/FRONTIER overlap, not stored** | `rulebook/8_FACTIONS.md` | **Canonical** (#122/#144). "Network position has strategic consequences" maps onto this. |
| Multiplex network layer (alliance/antagonism/funding/info-flow/penetration…) | **proposed** in the #152 plan | Phase A of #152. Strategy layer **consumes** it; it does not fork it. |
| Event log is the single source of truth; reducer stores no derived scalar | `src/simulation/events.py`, `world_state.py` | **Canonical.** Faction stats must therefore be **event-sourced or derived**, never bare stored numbers (§3). |
| Default campaign Helsinki-centred, small faction network | `RULEBOOK.md` §9.3, `FACTIONS.md` | Canonical. MVP is Helsinki-only, per the issue. |
| No faction-sheet schema, no strategy chapter, no offices/ventures model anywhere | — | Measured: this is genuinely unimplemented. |

**Key consequence:** the Identity + Reputation halves of the proposed faction sheet **already exist**
as canon (US/FRONTIER, taxonomy, Affect reputation). Only **Strategic capabilities, Domains,
Holdings, Boons/favors, Ventures/Projects, Offices, Internal factions** are genuinely new — and the
new parts must not contradict the "no stored derived scalars" invariant.

---

## 2. Verified source facts this plan depends on

- **Dune: Adventures in the Imperium** is the design reference for "the political organization as a
  playable object" (House sheet: domains, wealth/resources, holdings, favors/boons, ventures,
  status). NoöPunk adapts the **general ideas, not Dune-specific terminology** (the issue says so).
  Dune is a licensed product — **adapt concepts, copy no text or names** (cf. the house licensing
  discipline in `docs/licenses/` and the #104 plan's licensing note).
- **Crusader Kings** is the reference for character-centred politics: offices grant authority and
  create duties/rivals; succession is a source of drama; **characters stay central**.
- **LaclauGPT / Laclau-Mouffe / Palonen** supply the ideological-strategy content. Its normative
  invariants (`INV_ANTAGONISM`, `INV_AFFECT`, `INV_HEGEMONY_CORPUS`, `INV_RELATIONAL`,
  `INV_DYNAMIC_LABELS`) mean a strategic "hegemony" action cannot be a bare influence spend — it
  must be an **articulation** (linking demands into a chain around a signifier), which is exactly
  what NoöPunk's US/FRONTIER model already represents.
- **`AGENTS.md` §14** (tabletop-first gate): the faction sheet and the strategic turn must be
  **specified and playable on paper** before any Godot/Concordia implementation. This plan stops at
  the tabletop specification.

---

## 3. The central design crux (why GATE 1 and GATE 4 exist)

The issue lists **11 strategic capabilities** and immediately says "do not assume all of these
survive playtesting… probably use fewer, broader values". Meanwhile the repo's architecture says
**do not store a derived number you have not specified** (`world_state.py`). These pull in opposite
directions:

- If faction stats are **stored abstract numbers**, the project gains a second canon scoreboard that
  will drift from the event log and the Affect graph — the failure mode `test_issue122` exists to
  prevent.
- If faction stats are **fully derived** from events + the network graph, some of the issue's
  intended stats (Legitimacy, Cohesion, Status) have no canonical source yet and would be
  **invented mechanics**.

The resolution this plan proposes (GATE 1): **few, broad, event-sourced stats**, each of which is
either (a) an aggregate of existing logged events, or (b) an explicit author-specified rule. Anything
that is neither is **deferred**, not invented. The "Network Power" stat in particular should be a
**computed view** over the #152 multiplex graph, not a stored number.

---

## 4. Conflict register — findings that must be decided, not silently resolved

| # | Conflict | Why it matters | Gate |
| --- | --- | --- | --- |
| C1 | Issue lists 11 stats; issue also says use fewer; architecture forbids unspecified stored numbers. | Three-way tension. | GATE 1 |
| C2 | "Favors/boons leverage" is inherently **temporary goodwill** (Dune), but the Affect graph's scores are durable relations with semantic labels. | Modeling a favour as an Affect edge with a label like `owes` may work — but it must not overload the Affect domains meant for faction_us/frontier. | GATE 1 / GATE 6 |
| C3 | "Network Power" as a **stat** vs network position as a **derived property**. | Storing it duplicates the graph. | §3 |
| C4 | Internal factions + succession are a lot of structure (CK-style) that the issue's MVP does **not** list. | Scope. | GATE 5 |
| C5 | The strategy layer's state must be readable by #152 without a second store. | Coupling. | GATE 6 |
| C6 | Dune "Domains" are territorial; NoöPunk says "a faction can be powerful in a domain without owning territory". | The term must be reinterpreted, and Territory (an issue field) must not be assumed. | GATE 1 |

---

## 5. Proposed faction sheet (proposal, pre-GATE 1/2)

**Not canon until the gates clear.** Identity + Reputation rows **reuse existing canon**; the rest
are proposals.

| Block | Fields | Representation | Canon source |
| --- | --- | --- | --- |
| **Identity** | name, type, ideology/hegemonic project, core demands, key signifiers, antagonistic frontier, official narrative, hidden agenda, territory/jurisdiction, HQ, leadership structure | type → `faction_taxonomy.json`; demands/frontier/signifiers → US/FRONTIER **edges**; narrative/agenda → prose + a GM-only flag | `8_FACTIONS.md`, `4_SOCIAL.md`, `ideology.json` |
| **Strategic capabilities** | GATE 1 set (≤6 recommended) | **event-sourced aggregates or derived views**, each with a stated source rule; no bare scalars | §3 |
| **Domains** | Security, Intelligence, Finance, Media, Cyberspace, AI, Biotech, Psionics, Labor, Crime, Logistics, … | a faction's **structural capacity** in an area — a *rating or presence flag*, not territory | GATE 1 |
| **Holdings / Assets** | offices, safehouses, data centres, media outlets, labs, militias, intelligence cells, archives, psionic facilities … | **entities** in the event log owned/controlled by the faction; provide **hooks**, not passive bonuses | `events.py` |
| **Boons / favors / leverage** | favors owed, kompromat, guarantees, coalition support, intel-sharing, recognition, NHI channels | **expendable** edges; model as Affect edges with a dedicated label, or a small favour ledger — GATE 6 | `affect.py` (C2) |
| **Ventures / Projects** | build X, infiltrate Y, launch Z, seize a chokepoint … | long-running **event-sourced projects**; cost time/resources; emit hooks while in progress | GATE 1 |
| **Reputation** | competent/corrupt/humane/ruthless/… as **per-audience** reputations | Affect **reputation** domain edges, direction = audience → faction | `affect.py` |
| **Offices / roles** | leader, security chief, treasurer, comms chief, strategist, … | roles a PC or NPC **holds**; each grants authority, controls actions, creates duties/rivals | GATE 3 |
| **Internal factions** | wings/blocs/departments + succession paths | **Phase B** (GATE 5) | — |

---

## 6. Proposed work order (after gates clear)

### Phase 0 — the decision record (no code)
Write `docs/design/FACTION_STRATEGY.md`: the faction sheet, the strategic turn, the stat-source
rules, the RPG↔strategy bridges, and the #152 interface. Post the GATE answers as a comment on #153.

### Phase A — minimal viable (the issue's own "start tiny")
- 3–5 factions, **Helsinki only**, **one PC-controlled faction**, **4–6 stats** (GATE 1), 3 domains,
  a small set of holdings, favors/leverage, **1–2 strategic actions per campaign turn**, ideological
  actions using a **very small LaclauGPT subset** (articulate a demand / redefine the frontier /
  promote a signifier).
- The **strategic turn** (issue §"Strategic turn structure", 9 steps) specified on paper, with
  steps (1) and (8) wired to the event log.
- Results generate **RPG missions** — the whole point; a strategy action that produces no
  character-scale hook is a design failure.
- Guarded by `tests/test_issue153_strategy.py` (structure pins; no game engine dependency in CI).

### Phase B — internal politics
Subfactions, offices in conflict, succession (elections/appointment/coup/schism/…), cohesion, and
the "characters lose/gain office" loop. Persistent campaign state via the SQLite log.

### Phase C — scale
Transnational factions, global institutions (UNSA as a full faction sheet), NHI/AI/psionic
factions that **bend** the assumptions of ordinary political organizations (the issue's own open
question).

---

## 7. Relationship to #152 (design together, land separately)

Per the issue's own section: **one state engine, two facings**.

| Direction | Contract |
| --- | --- |
| #152 → #153 | the simulation's **world-delta events** + GM digest are the strategic layer's "World update" (turn step 1) |
| #153 → #152 | strategic decisions are emitted as **events** back into the log (turn step 8), updating faction/network state |
| shared | the event log, the Affect graph, the multiplex network, `faction_taxonomy.json`, `ideology.json` |

**Design rule:** no private state file. If a Phase-A prototype needs a field #152 cannot read (or
vice versa), that is a schema bug to fix in the shared schema, not a new store. The MVP can run with
#152 absent (manual world import) — the layers are separable by construction.

---

## 8. Player-scale ↔ faction-scale bridges (issue §"Player character ↔ strategy scale")

These are the mechanical heart of "characters first". Each must be a **stated rule** (GATE 4),
specified on paper before any code:

| RPG outcome | Faction effect (proposed) |
| --- | --- |
| successful infiltration | + Intelligence capacity / a new intel edge |
| persuading a key official | a new multiplex network edge |
| exposing corruption | − Legitimacy, possible scandal event |
| sabotaging infrastructure | remove a Holding entity |
| winning a televised debate | shift a contested signifier / per-audience reputation |
| assassinating a leader | succession event, possible schism (Phase B) |
| saving a district | + local support / reputation edge |
| failed covert op | scandal + diplomatic cost |

And the reverse: faction resources let PCs requisition equipment, request intelligence, obtain legal
authority, call in contacts, deploy specialists, etc. — each a **tabletop-facing** benefit.

---

## 9. Files likely to change

| File | Change | When |
| --- | --- | --- |
| `docs/design/FACTION_STRATEGY.md` | **new** — sheet, turn, bridges, #152 interface | Phase 0 |
| `rulebook/9_STRATEGY.md` | **new chapter** (GATE 2) — the player-facing faction sheet + turn | Phase 0/A |
| `data/world/faction_sheet_schema.json` | **new** — machine-readable sheet | Phase 0/A |
| `data/world/faction_taxonomy.json` | **possibly extend** (Domains enum) — GATE 1 | Phase A |
| `src/simulation/strategy.py` | **new** — deterministic stat-source helpers (aggregates/derived views) | Phase A |
| `tests/test_issue153_strategy.py` | **new** — structure guard | Phase A |
| `RULEBOOK.md` (Contents + a pointer to §9_STRATEGY) | **minimal** — linkage only | Phase A |
| `rulebook/8_FACTIONS.md` | **only** a cross-reference to the new chapter | Phase A |

---

## 10. Verification

- The **existing** suite (801 tests) stays green — the strategy layer must not move the core RPG.
- New guard `tests/test_issue153_strategy.py` pins: (a) the sheet spec exists with each block;
  (b) Identity/Reputation reuse the canon artefacts (taxonomy, Affect) rather than re-declaring
  them; (c) no stored derived scalar without a stated source rule; (d) the layer is optional (core
  imports no strategy module); (e) the #152 interface is named.
- **Sabotage-test** every guard before claiming it works (house convention).
- Any new `rulebook/` chapter must keep the numbering/contiguity guards green
  (`test_issue101_sources_dedup.py`, `test_issue78_four_layers.py`).

---

## 11. Risks, tradeoffs, open questions

- **Biggest risk:** turning NoöPunk into a detached grand-strategy board game — the issue explicitly
  forbids this. Mitigation: GATE 4 + the RPG↔faction bridge table (§8) as a hard requirement.
- **Bookkeeping risk:** 11 stats + domains + holdings + favors + projects is a spreadsheet. Mitigate
  with GATE 1 (fewer, broader stats) and Phase A's tiny scope.
- **Licensing risk:** Dune/CK are proprietary. Adapt concepts only; no copied names or text.
- **Theory risk:** an ideological "hegemony" button that ignores `INV_ANTAGONISM`/`INV_AFFECT` would
  betray the LaclauGPT core. Articulation must be the mechanic.
- **Symmetry risk (GATE 3):** asymmetric PC/NPC rules are harder to balance and to explain.
- **Open (author):** GATE 1–6. **Open (design):** the issue's ten research questions.

## 12. Deliberately NOT in this plan

- Implementing any phase before GATEs clear (this is planning only, per the author).
- Internal factions / succession in the MVP (Phase B).
- Global scope (Phase C) — MVP is Helsinki-only.
- The simulation layer's own engine — that is the #152 plan.
- Any Godot/Concordia implementation (`AGENTS.md` §14 — tabletop first).
- Any change to `AGENTS.md`, the design invariants, or §33 world-canon.
