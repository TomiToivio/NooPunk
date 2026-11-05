# DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED

# Graph-based NoöPunk scenes: five graph families, three reality layers, Series → Episodes → Scenes

> **Phase: design/research only (#1164).** This document proposes. It changes no rule, no code, no tabletop text.
> Tomi's [`design/graphs/README.md`](../../design/graphs/README.md) and [`RULES.md`](../../design/graphs/RULES.md)
> are **read verbatim and left untouched**. Implementation requires a separate, explicit instruction.
>
> **Proposed location:** `docs/design/DRAFT_GRAPH_SCENES_1164.md`. If Tomi prefers
> `docs/graphs/GRAPH_RULES_PROPOSAL.md`, it moves — the content is the same.

---

## 0. Preflight: what already exists

Read before proposing anything, because most of this issue is **not** greenfield.

| Thing | Where | State |
|---|---|---|
| Author's graph design | `design/graphs/README.md` | Five families, −4…+4 social edges, World/City/Location, Series/Episode/Scene, Luhmann mapping |
| Author's rules brief | `design/graphs/RULES.md` | The detailed asks: Know vs Work, interrogation, PSI verbs, density targets, QIP terminology |
| CWN skill list (verbatim) | `src/rules/without_number.py`, `data/rules/without_number.json` | **Administer, Connect, Drive, Exert, Fix, Heal, Know, Lead, Notice, Perform, Pilot, Program, Punch, Shoot, Sneak, Stab, Survive, Talk, Trade, Work** |
| GUMSHOE → CWN mapping (**#932**) | `data/rules/gumshoe_investigative.json` | **16 abilities already mapped** to CWN skills — *and nothing consumes the file* |
| Core-clue resolver | `src/rules/investigation.py` | `discover()` grants clues by **competence + declared access + inquiry, no roll**; `ClueKind.CORE/OPTIONAL`, `obscure`, `passive`, `benefit`/`benefit_cost` |
| PSI boundary | `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md` + 11 tests | The resolver has no psychic input; psi may not grant clues or open exits |
| Goals (**#1119**) | `src/rules/goals.py` | `Goal`, `Progress`, `Award`, `GoalLog`, `record_progress`, `award_xp`, `paper_line` |
| Tags | `src/rules/tags.py` (#51), `noopunk_tags.py` (#821) | Unified tag model, stacking, tag-based attributes |
| Legacy graph code | `legacy/ubiquitous_maniacs/src/{physical,cyber,noetic,social}/graph.py` | **Comparative evidence only** — not the current engine |
| Campaign canon | `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` §2.1–2.3 | Fixed dossier, **company housing in Kurvi**, open attribute array |
| Europol frame | `docs/world/EUROPOL_HELSINKI_1114.md` §3 | "Europol opens doors; national officers walk through them" |

### Two conflicts, resolved as questions rather than silently

1. **Home location.** `design/graphs/README.md` puts the PC's home in **Sörnäinen** and Europol HQ on **Ratakatu**.
   Newer campaign canon gives **company housing in Kurvi**. → Proposal: a **versioned starting-state profile**
   (`start_profile: campaign01-v1`) in which the newer author choice wins (Kurvi), while the README's Sörnäinen
   location remains available for other profiles. **Sörnäinen stays canonical elsewhere** — it is the PSI prison
   (`design/BIONICS.md`), which is a different thing from the home.
2. **HQ address.** Ratakatu is not contradicted by the campaign doc, only by silence. → **Flag for author review**;
   the proposal carries `hq_address: "Ratakatu (provisional — confirm)"`.

### Three findings that change the proposal

- **`Convince` does not exist as a CWN skill.** The brief's list includes it; the source list does not. Social
  checks therefore use **Talk, Connect, Lead** — and the proposal must not invent a skill.
- **It is `Administer`, not "Administration".** `data/rules/gumshoe_investigative.json` already uses the correct
  spelling.
- **The GUMSHOE work is done but unwired.** 16 abilities → CWN skills already exist. Proposing a *new*
  `InvestigationCapability` tag system would duplicate it. The proposal therefore **uses** that file.

---

## 1. Architecture: vanilla CWN vs small mods

| Graph family | Nodes / edges | Rules owner | New rules needed |
|---|---|---|---|
| **Physical** | `world → city → district → location → room`; routes, doors, access | **Vanilla CWN** — movement, Notice/Exert/Sneak/Survive, combat | None. Coordinates and `parent_id` are data, not rules |
| **Cyber** | `device / network / service / account / data / security` | **Vanilla CWN Hacking** | None. Nodes are *targets*, not a second resolver |
| **Astral** | `agent / anchor / realm / symbolic_site / boundary / noetic_link` | **PSI mod** (SWN-derived shape + WWN magic as one ontology) + **psychotronics** | Yes — bounded, §5 |
| **Social** | `person / faction`, edges −4…+4 | **CWN social checks + tag mods** | Small: relationship vs reputation vs ideology must not merge |
| **Story** | Series → Episode → Scene | **Existing Goals (#1119) + scene tags** | Small: horizon field, scene typing |

**Scene type is a separate field from graph family.** A `combat` scene can touch all three layers; a `cyber` scene
is one activity inside a `location` node. Nothing about the graph type changes the action economy.

---

## 2. Schemas (design only)

### 2.1 Shared base

```yaml
# node
node_id:     "hel:kallio:kurvi:apartment"     # namespaced, stable
graph_type:  physical | cyber | astral | social | story
node_type:   <family-specific, §2.2-2.6>
label:       "The Kurvi apartment"
layer:       physical | cyber | astral
visibility:  public | discovered | gm_secret   # gm_secret is never emitted to a rookie view
prerequisites: []          # node ids or flags
unlock_act:  1
tags:        []
refs:        {cwn: null, faction: null, character: null, location: null}
source:      "docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md §2.1"
author_status: draft

# edge
edge_id:     "hel:kallio:kurvi:apartment->hel:kallio:street"
source:      <node_id>
target:      <node_id>
relation:    contains | route | door | access | controls | knows | relationship | transition | layer_link
directed:    true
access_condition: null      # e.g. "keycard", "warrant", "consent"
travel_cost:  null          # scene-level, not metres
knowledge_gate: null        # node must be discovered first
layer_transition: null      # only for layer_link edges
consequences: []
```

**Validation contract (runnable in principle):** every `source`/`target` resolves; every `layer_link` names both
layers and an explicit effect; `gm_secret` nodes are absent from any player-facing projection; `relationship`
edges are integers in −4…+4; a `story` transition may not target a node from another series.

### 2.2 Physical

```yaml
node_type: world | city | district | location | room
parent_id: <node_id or null>
coordinates: {x: 60.19, y: 24.95}    # optional, for map overlay
terrain: urban | indoor | forest | underground
legal:     public | restricted | private   # decides whether entry needs a lawful basis
encounters: []
cyber_ref:  <node_id or null>
astral_ref: <node_id or null>
```

Hierarchy is authored **only as deep as play needs**. Act I does not get a world graph — the README is explicit
that the world map "will only become available when the character has to travel".

### 2.3 Cyber

```yaml
node_type: device | network | service | account | data | security
cwn_hacking_ref: "<published CWN procedure/verb>"   # edition-verified before use
privilege: none | user | admin | root
detection: passive | active | alarm
credential_ref: <node_id or null>
```

**Hard rule:** a cyber node is a *target for CWN Hacking*, never a new hacking verb. Cyber actions do not change
physical HP or astral state except through an authored, explicit cross-layer effect.

### 2.4 Astral

```yaml
node_type: agent | anchor | realm | symbolic_site | boundary | noetic_link
seity_ref: null          # Faggin/author term, used as authored flavour
density: 1..7            # metaphysical state; NEVER a spatial dimension
agency: {experience: 0..3, identity: 0..3, autonomy: 0..3}   # Faggin axes as tags, not attributes
mode: overlay | projected | manifesting
return_rule: "<explicit, e.g. anchor_intact or scene_end>"
psi_permission: "<verb list, §5>"
links: [{to: <physical/cyber node>, effect: "<typed>"}]
```

**Density is not dimension, and an astral location never implies physical access.** That is enforced by the
`links` contract: without a typed link, an astral node cannot reach a physical one.

### 2.5 Social

```yaml
node_type: person | faction
sheet_ref: <character/faction id>
edges:
  - relation: relationship
    relationship_score: -4..+4      # interpersonal
    relationship_kind: ally | rival | family | professional | ...
    evidence: "<source event id>"
    mutual: true|false
    known_to: [agent ids]
  - relation: reputation          # per-faction, NOT the same field
    reputation_score: -4..+4
    audience: public | institutional
  - relation: ideological_affinity
    affinity: -2..+2              # distinct score; agreement ≠ friendship
```

**Three scores, three meanings.** Interpersonal relationship, faction reputation, and ideological affinity are
separate fields with separate ranges. Collapsing them is the single most likely design error here.

### 2.6 Story

```yaml
series: {series_id, episode_refs, long_goals, completion}
episode: {episode_id, scene_refs, medium_goals, entry_conditions, exit_conditions, alternates}
scene:
  scene_id: "ep1.sc2"
  types: [investigation, social]        # may overlap
  graph_node_refs: [...]
  participants: [...]
  short_goals: [...]
  leads: [...]; evidence: [...]
  available_actions: [...]
  transitions: [{condition, to_scene}]
  outcomes: [{id, effects, flags}]
  spoiler_gate: <flag>
```

**Goal horizon mapping:** `short` = scene or episode, `medium` = act, `long` = series. Proposal: add a `horizon`
field to the existing `goals.Goal`; **do not** build a second goal model.

---

## 3. CWN crosswalk — where the core applies unchanged

| Activity | CWN mechanism | Proposal |
|---|---|---|
| Exploration | Notice, Exert, Sneak, Survive; equipment | Unchanged. Graph supplies adjacency and access, not new checks |
| Combat | One initiative order, attacks, damage, saves, movement | Unchanged. **Layer actions share the same turn economy** — no free astral or cyber turns |
| Cyber | CWN Hacking verbs, programs, permissions, detection | Unchanged. Graph nodes are targets |
| Social | Talk, Connect, Lead | Unchanged; tags add colour, not a second social engine |
| Investigation | `discover()` — competence + access + inquiry, no roll | Unchanged; §4 extends by mapping, not replacing |

**One action economy.** A character in combat who projects, hacks and shoots spends *one* turn doing one of them.

---

## 4. Investigation: use what already exists

### 4.1 The mapping is already written

`data/rules/gumshoe_investigative.json` (#932) holds 16 abilities → CWN skills:

| Kind | Abilities (CWN skill) |
|---|---|
| Academic | Research (Know), Textual Analysis (Administer), History (Know), Law (Administer), Occultism (Know), Forensic Pathology (Heal), Biology (Heal) |
| Technical | Cryptography (Program), Data Retrieval (Program), Evidence Collection (Notice), Ballistics (Fix), Chemistry (Fix) |
| Interpersonal | Interrogation (Talk), Reassurance (Talk), Streetwise (Connect), Bureaucracy (Administer) |

**Recommendation: adopt model B, not model A.** Model A (invent Investigation Ability tags by specialty) duplicates
this file. Model B uses the existing CWN skills and treats the 16 abilities as **descriptors** of what a skill
covers — no new currency, no second resolver. The only new thing needed is a **lookup** from ability id to skill,
which is already in the JSON.

### 4.2 Why no roll is needed for the core clue

`discover()` already does the GUMSHOE thing: a competent investigator declaring a supported examination of an
accessible scene **gets the core clue**. `obscure` clues cannot be the sole exit, and `access`/`inquiry` are
declared. The invariant the issue asks for — *"failure on a clue-finding skill check must not erase an
indispensable core clue"* — is therefore already true, and worth a test that pins it at the graph level.

### 4.3 Leads, evidence and capability

- **Lead** — a pointer to a person or site. Lives on the scene as `leads: [node_id]`; it is a transition, not a check.
- **Evidence** — an authenticated artifact or observation with provenance (`evidence_ledger` already exists in
  `src/rules/investigation_evidence.py`). Reuse it; do not invent an evidence object.
- **Investigation capability** — *eligibility to inquire*, expressed as: academy training, the CWN skill itself,
  BCI sensory capture, a permitted AI/human controller, or Europol laboratory support. It is a **permission and a
  constraint** (connectivity, consent, chain of custody, legal clearance, time), never a free +N.

### 4.4 BCI / controller / laboratory

| Channel | What it gives | Constraint |
|---|---|---|
| BCI sensory capture | A record of what the officer saw and heard, streamable | Only *authorised* sensory feed; consent and privacy law |
| Human/AI controller | Off-scene analysis, cross-referencing, lab tasking | Connectivity, queueing time, EU AI restrictions; the controller is a person with a caseload |
| Europol laboratory | Forensic depth | Chain of custody; the lab answers in hours, not scenes |

**No unilateral powers.** Europol coordinates; Finnish authorities arrest and search (`EUROPOL_HELSINKI_1114.md` §3).

### 4.5 Know vs Work — the naming question

`Work (Europol Agent)` = practical procedure: scene management, interagency liaison, lawful process, interview
conduct. `Know` = theoretical education. Proposed specialities:

| Option | Reads as | Verdict |
|---|---|---|
| `Know (Europol Studies)` | Institution-specific, narrow | Clear but parochial |
| **`Know (Law & Intelligence)`** | The actual curriculum: EU law, criminal/intelligence theory, analysis | **Recommended** — covers the brief's four knowledge areas |
| `Know (Security & X-Risk Studies)` | The exotic fourth area | Best as a *second* speciality, not the default |

**Arbitration example:** knowing *that* an EU regulation permits a cross-border data request is `Know (Law &
Intelligence)`; actually filing it through the liaison before the deadline is `Work (Europol Agent)`.

### 4.6 Interview scenes — fiction-safe

**Do not build a lie detector.** The psychotronic interview proposes:

- A **very small emotion-state tag** on the interviewee, in the *Veil* register: `fearful`, `guarded`,
  `overwhelmed`, `cooperative`. Four states, no numbers.
- Device output is a **noisy estimate** — it may be wrong, and the fiction says so.
- The scene runs on CWN `Talk` (and `Interrogation` as a descriptor), with lawful constraints: consent, counsel,
  recorded interview, human rights.
- **No compelled mind reading.** Coercion is evidence of misconduct — a case, not a mechanic.

---

## 5. Astral: the bounded PSI mod

### 5.1 Three modes

| Mode | Body | Perception | Can act physically? |
|---|---|---|---|
| `overlay` | Awake, embodied | Astral perceived as AR over the physical | No |
| `projected` | Anchored elsewhere | Immersive, disembodied | No, except `manifesting` (§5.4) |
| `manifesting` | Anchored, costly | Both | Rare, explicit, limited |

### 5.2 Verb × target matrix — **DENIED by default**

| Verb | self | conscious_person | living_biologic | inert_object | cyber_node | astral_agent | astral_region |
|---|---|---|---|---|---|---|---|
| **Perceive** | — | deny | deny | deny | allow* | allow | allow |
| **Contact** | — | allow** | deny | deny | deny | allow | deny |
| **Shield** | allow | allow | deny | deny | deny | allow | allow |
| **Project** | allow | — | — | — | — | — | allow |
| **Influence** | deny | deny*** | deny | deny | deny | deny | deny |
| **Imprint/Modulate** | deny | deny | deny | later | later | deny | deny |
| **Ritualize** | allow**** | allow**** | deny | deny | deny | allow**** | allow |
| **Manifest** | — | deny | deny | later | later | deny | allow |

\* only on a node the character is already legitimately connected to. \*\* consent, or a defended intrusion that can
fail and be detected. \*\*\* scripted, never routine. \*\*\*\* group scene, one shared cost.

Every `allow` requires, in the authored record: `source_system, attunement, target_visibility, link_basis,
action_economy, cost_resource, range_or_anchor, duration, resistance, investigation_boundary, physical_effect`.

**Only one governing resource per activation.** SWN-shape Effort *or* an approved chakra conversion — never both.

### 5.3 Density as target class, not as level

| Density | What it is in NoöPunk | Consequence |
|---|---|---|
| 1st | Panpsychic matter; **all Cyber, constructs, drones, cameras** | PSI is unusually effective against technology — which is why psychotronic hardening and hacker-PSI hybrids exist as *defences* |
| 2nd | Living biologics | Perception/communication permissions; not programmable devices |
| 3rd | Unawakened humans (most people) | Weaker active PSI, **full agency and consent**; never "helpless" |
| 4th | Awakened humans; emerging SMC | The PCs. More defence and more ability, plus polarization consequence |
| 5th | Advanced NHI; Orion Mantid leadership | Power asymmetry handled by **containment, defence, retreat, intervention** — never an unresistable one-roll kill |
| 6th/7th | Non-player scale | Author-controlled scenes only; no stat inflation, no playable upgrade |

### 5.4 Manifestation, return, and the boundary

Return requires an intact anchor. A broken anchor is a **scene problem**, not instant death. Manifestation
(`ectoplasm`) is rare, unmistakable, costly, and never a free combat form.

**Investigation boundary holds:** no verb grants a core clue or opens an exit. A `Perceive` on a scene can produce
a *lead to investigate*, never the answer.

### 5.5 QIP glossary — with honest evidence tiers

| Term | Correct scientific meaning | NoöPunk premise | Play limitation |
|---|---|---|---|
| Nonlocality | Correlations that cannot signal faster than light | Entanglement is the basis of remote PSI | Requires a named link; finite scope; **no free signalling** |
| Entanglement | A joint state, not something created by looking | Line of sight = entangled | Author rule, stated as fiction |
| Superposition | Amplitude combination | Unsettled potential | Not "occupy all scenes" |
| Collapse / measurement | Interpretation-dependent | Two agents contest the outcome | Resolved by **published CWN/SWN defence**, never "stronger mind wins" |
| It from Qubit | Quantum information as fundamental | Panpsychic qualia | Do not conflate information, energy and agency |
| Wave–particle | Measurement-context-dependent behaviour | — | No invulnerability switch |
| **Interference** (not *inference*) | Addition and cancellation of amplitudes | Coherence/discord tag in contested noetic scenes | Not a damage multiplier |
| Consciousness / Identity / Agency | Faggin's three axes | `experience / identity / autonomy` tags on entities | **Not** CWN attributes |
| Observe–Experience–Act | Hoffman/Faggin loop | Fictional resolution narrative | **Not** a three-roll tax |
| Density 1–7 | — | Developmental state | **Not** spatial dimensions |

**Source boundary, stated plainly:** standard physics does not permit superluminal signalling via entanglement
(see NIST and the information-causality literature cited in the issue). Hoffman, Faggin, Radin and the Law of One
are separate frameworks and are **not** evidence that Hilbert-space states are editable by intention. The rule
language is fictional metaphysics using honest vocabulary.

---

## 6. Worked scenes

### 6.1 Act I — grounded Helsinki (no paranormal content)

*Procurement fraud at a Kallio medical supplier.* Nodes: `kurvi:apartment` → `kallio:street` → `supplier:lobby` →
`supplier:office`; cyber: `supplier:workstation`, `supplier:invoices`. Social: `witness:clerk`.

- **Lead** obtained from the Europol file (Know/Law descriptor, no roll).
- At the office: `Notice` finds the invoice anomaly — **core clue, no roll**, because she is competent, has
  `access: office` and declares `inquiry: search`.
- The clerk's cooperation is a `Talk` check; failure costs **time and goodwill**, never the clue: the invoice is
  also obtainable via `Program` on the workstation.
- BCI streams the sensory feed to a controller; the controller's reply takes a scene.

**Nothing here needs a graph-drawing tool, an LLM, or a PSI rule.**

### 6.2 Act III — layered encounter (proposed)

*Corridor, opponent, camera.* One CWN turn economy.

| Actor | Physical | Cyber | Astral |
|---|---|---|---|
| PC | Shoot | — | Shield (overlay) |
| Ally | Move | Program: open door | — |
| Opponent | Shoot | — | Contact (denied — no link) |

The astral `Contact` is **denied** because there is no link; the matrix does its job. The PC cannot take a physical
action and an astral action in the same turn.

### 6.3 Act IV — 5th-density intrusion

A 5th-density StS entity reaches the Wanderer through an existing noetic link (established in Act II).

1. **Detection** — the QIP implant reports an anomaly (noise, not truth).
2. **Defence** — `Shield`; the entity's attack is resisted by published defence, not by narrative fiat.
3. **Escalation** — the entity's scale is expressed as *pressure on the scene*: the anchor weakens, bystanders are
   affected, the exit gets harder.
4. **Help** — party members act in the **same** turn economy; the SMC link (if formed) allows coordinated defence.
5. **Outcome** — retreat, containment or escape. **No unresistable kill, no infinite-range control.**

---

## 7. Author-facing format: one Markdown file per unit

```markdown
---
id: ep1.sc2
kind: scene
types: [investigation, social]
episode: ep1
graph_nodes: [hel:kallio:supplier_office, cyber:supplier_workstation]
participants: [pc, clerk_hiltunen]
short_goals: [find the invoice anomaly]
visibility: gm_secret      # remove this line when the player may see it
---

## Setting
The supplier's back office, 08:40. Rain on the window; a kettle nobody has switched off.

## What the player can do
- Search the desk — Notice; the anomaly is a **core clue, no roll**.
- Question the clerk — Talk; failure costs time, not the clue.
- Ask the controller to run the invoices — Program/Talk; answers next scene.

## Clues
| id | kind | competency | access | inquiry |
|---|---|---|---|---|
| invoice_anomaly | core | Notice | office | search |
| clerk_evasion | optional | Talk | | interview |

## Transitions
- `invoice_anomaly` → ep1.sc3
- `clerk_evasion` → ep1.sc3 (with the clerk as a witness)

## Consequences
- If the clerk is frightened: tag `clerk_distrust` −2 reputation with `helsinki_police`.
```

**One file per Series / Episode / Scene.** No large single YAML, no Python dictionaries. The validator reads the
frontmatter; NetworkX is an **in-memory projection**, not the source of truth.

---

## 8. Phase plan

| Phase | Deliverable | Depends on |
|---|---|---|
| 1 | **CWN-only traversal**: Physical graph, scene/series skeleton, validator | Nothing |
| 2 | Social tags + Goals horizon field | #1119 existing model |
| 3 | Investigation: wire the 16 GUMSHOE descriptors to `discover()` | Phase 1 |
| 4 | Bounded Astral / PSI + cross-layer links | #1137 drafts approved |

Each phase must be playable **without** graph drawing, an LLM or Mesa/Concordia.

---

## 9. Open decisions for Tomi

1. **Document location** — `docs/design/DRAFT_GRAPH_SCENES_1164.md` (current) or `docs/graphs/GRAPH_RULES_PROPOSAL.md`?
2. **HQ address** — Ratakatu confirmed? (README says so; campaign canon is silent.)
3. **Home** — Kurvi wins in `campaign01-v1`; should Sörnäinen remain the home in any profile?
4. **Know speciality** — `Know (Law & Intelligence)` recommended; or `Europol Studies`?
5. **Investigation model** — adopt B (existing skills + the 16 descriptors) or insist on A (new ability tags)?
6. **Emotion tags** — the four-state Veil-lite model, or none at all?
7. **`Influence` verb** — keep it denied entirely, or allow it under strict consent/defence for later acts?
8. **Manifest/Imprint** — defer to Act IV+, or cut?
9. **Density 1 vs constructs** — if PSI is unusually effective against all Cyber, do psychotronic hardening rules
   become mandatory in Act I, or only when the first hostile psychic appears?

## 10. Not done here, by design

No `src/` change, no rulebook change, no MUD runtime change, no edit to `design/graphs/README.md` or `RULES.md`.
No SWN/WWN numbers invented — where a cost is needed and unverified, this document says "edition-verify first".

## 11. Bibliography

- `design/graphs/README.md` and `design/graphs/RULES.md` (author; read verbatim, untouched).
- `src/rules/without_number.py`, `data/rules/without_number.json` — the actual CWN skill list used above.
- `data/rules/gumshoe_investigative.json` (#932) — 16 GUMSHOE abilities, GUMSHOE SRD (OGL).
- `src/rules/investigation.py`, `src/rules/investigation_evidence.py`, `src/rules/goals.py` (#1119),
  `src/rules/tags.py` (#51), `src/rules/noopunk_tags.py` (#821).
- `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md`, `docs/world/EUROPOL_HELSINKI_1114.md`,
  `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`, `docs/rules/CWN_IMMUTABLE_CORE_1068.md`.
- Drafts: `docs/design/DRAFT_NOOPUNK_{PSIONICS,PSYCHOTRONICS,BIONICS,CHARACTER_TAGS,EUROPOL_CHARACTER_GENERATION}.md`.
- `design/BIONICS.md` (author) — PSI sources, QIP operator requirement, Sörnäinen prison.
- NIST, "Rush hour in the light-wave..." (2014) and the information-causality literature cited in #1164 — for the
  no-superluminal-signalling boundary.
- Faggin (QIP/Seity), Hoffman (conscious realism), Lloyd (*Programming the Universe*), Penrose–Hameroff (Orch-OR),
  Radin (parapsychology), Gallimore (*Alien Information Theory*), Monroe (astral projection) — all as the issue
  lists them, as **fictional-ontology sources**, with their real epistemic status stated in §5.5.
