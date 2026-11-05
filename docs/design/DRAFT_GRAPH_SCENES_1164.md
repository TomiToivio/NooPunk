# DRAFT — Graph scenes: five graph families, Series → Episodes → Scenes, and the layer contracts

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED**
>
> Proposal for [#1164](https://github.com/TomiToivio/NooPunk/issues/1164), which asks for an implementation proposal
> for the author's [`design/graphs/README.md`](../../design/graphs/README.md) and
> [`design/graphs/RULES.md`](../../design/graphs/RULES.md). **Design/research only.** No Python, no rulebook, no
> CWN change, and **the author's two graph documents are untouched** — this file is a separate proposal.
>
> Templates and a filled example live in [`docs/graphs/templates/`](../graphs/templates/) and
> [`docs/graphs/examples/`](../graphs/examples/). Nothing there is loaded by the game.

**Evidence key:** **[a]** verified in this repository's code or published source · **[b]** experimental /
contested · **[c]** fiction (author canon or 2045 extrapolation) · **[?]** open decision for Tomi.

---

## 0. What this proposal is, in one paragraph

The author's model is **five graph families** — Physical, Cyber, Astral, Social, Story — where the first three are
**layers of one situation**, and Story is the **Series → Episodes → Scenes** hierarchy that decides which
situation you are in. The proposal below keeps **CWN as the only resolver**, treats NetworkX as an **in-memory
projection of hand-authored Markdown + YAML**, and makes every cross-layer action an **explicit typed record**
rather than an implicit permission. The three things that must be true for this to be playable are: (1) one actor
state shared by all layers, (2) one turn economy in a mixed scene, (3) no cross-layer effect without a written
link record.

---

## 1. The author's documents, and the conflicts a proposal may not silently resolve

Read verbatim and summarised, not paraphrased away:

* **Five graphs**; Physical/Cyber/Astral are "three levels of reality" that may be shown as an overlay; Social
  edges score **−4…+4**; Story is Series → Episodes → Scenes with scene types Investigation, Exploration, Combat,
  Social, Cyber, Astral, and overlapping types are explicitly expected.
* **Physical** is hierarchical: World → City → Location (rooms/doors; outdoors, places/paths), with map
  coordinates and addresses, and travel only opening up when the story needs it.
* **Astral** is a Conscious Agent Network; PSI works *through* it whether the character is embodied or projecting;
  astral is an **AR overlay on the Physical** or **immersive VR during an OOBE**; the aesthetic is Gallimore's
  DMT hyperspace.
* **Social**: nodes are important characters and factions, edges are the same as Social tags on the sheet.
* **RULES.md** adds the design instructions: CWN for Physical/Cyber/Combat/Exploration; tag systems for Social,
  Goals, Personality; a GUMSHOE-inspired investigation system with Leads, Evidence and Investigation abilities;
  psychotronic interrogation with an emotion model "similar to The Veil"; a **Verb × Target** PSI system modelled
  on CWN hacking; Psychotronics as amplifiers, **PSI as natural**; and the 1st–7th density model.

### Documented conflicts — flagged, not decided

| conflict | author README / data says | newer canon says | proposal |
|---|---|---|---|
| **The character's home** | "Player's home in the Sörnäinen District"; `data/world/helsinki_locations.json` has `home_helsinginkatu` in Sörnäinen/Kallio, "a modest UNSA-provided flat" | campaign #1132: Europol employment, **company housing in Kurvi** | a **versioned starting-state profile** (§2.3): `start_profile: campaign01@v2` selects Kurvi housing; the older Sörnäinen flat stays available as `campaign01@v1`. **Author decides which is canon.** |
| **The employer** | data says UNSA, "UNSA Helsinki Field Office · Ratakatu" | campaign: **Europol** Helsinki; UNSA is a limited partner | the profile records `employer: europol` and the node is renamed in the proposal only; **the Ratakatu address is flagged for author review** (is Europol in the UNSA building, next door, or elsewhere?) |
| **"Inference" vs interference** | RULES.md: "Constructive and Destructive Inference" | quantum interference is addition/cancellation of amplitudes; *inference* is a conclusion from evidence | keep the **conception**, correct the **word**: `noetic_interference` (§7 glossary), with `constructive`/`destructive` as the two modes |

---

## 2. Preflight: what exists, what is vanilla CWN, what is a gap

### 2.1 Code audit (verified by reading the modules, not by filename)

| area | what actually exists | consequence |
|---|---|---|
| **Graph runtime** | *Legacy only*: `legacy/ubiquitous_maniacs/src/{physical,cyber,noetic,social}/graph.py` and `graph_serialization.py` — NetworkX, `domain` attribute, social graph with `relationship` edges in −4…+4, export to dict/DOT/GEXF. Physical/cyber/noetic are empty builders. | **comparative evidence, not the engine.** The legacy social graph validates duplicate people and duplicate pairs — that validation is worth keeping. **No current runtime graph module exists.** |
| **Current locations** | `data/world/helsinki_locations.json` v2 — nodes with `map_position`, `actions`, `requires`, `reveals`, `start`; `docs/world/` descriptions | already a **physical graph in JSON**, with reveal gating. The proposal should *adopt* it rather than invent a second location model. |
| **Investigation** | `src/rules/investigation.py` — `Clue(id, scene_id, kind=core|optional, competency, fact, leads_to, obscure, passive, access, inquiry, benefit, benefit_cost)`, `Scene`, `Case`, `CaseGraph`, `discover()`, `load_case_graph()` | **the GUMSHOE-lite model already exists**: competence + declared access + declared inquiry, core clues that cannot be missed, optional clues that enrich, benefits with a CWN cost. The issue's "Lead / Evidence / Capability tags" are **mostly a vocabulary** over this, not a new system. |
| **Goals** | `src/rules/goals.py` — `Goal`, `Progress`, `Award`, `GoalLog`, `add_goal`, `record_progress`, `award_xp`, `paper_line`; `docs/rules/GOAL_TAG_1119.md` | horizons **already exist**; the Story schema must reference them, never re-implement. |
| **Tags** | `data/rules/noopunk_tags.json` — kinds `attribute/skill/status/other`; `src/rules/noopunk_tags.py`, `src/rules/tags.py` | social/personality/reputation tags extend this model (§6), as proposed in `DRAFT_NOOPUNK_CHARACTER_TAGS.md`. |
| **CWN** | `src/rules/cwn_hacking.py` (access pool, security difficulty, `AlertClock`), `cwn_combat.py`, `cwn_combat_actions.py`, `cwn_investigation`-adjacent skills in `data/rules/cwn/skills.json` | **vanilla** owns physical, cyber and combat. No new resolver anywhere in this proposal. |
| **PSI** | `src/rules/swn_psionics.py` (disciplines, Effort, reservations, torching), `src/rules/psionics.py`; no astral module | astral **permissions** are proposed here; the Effort engine is the comparative pattern, and `DRAFT_NOOPUNK_PSIONICS.md` is the companion proposal. |
| **NetworkX** | not in `requirements.txt` / `pyproject.toml` | adding it is an **implementation-phase** decision; the authored format must be readable without it. |

### 2.2 Baseline vs missing-mod matrix

| capability | owner | status |
|---|---|---|
| physical moves, doors, travel costs, obstacles, combat | **CWN vanilla** | exists |
| cyber access, intrusion, detection, alert clock | **CWN vanilla** (`cwn_hacking`) | exists |
| clue discovery without dice, core clues never missable | **existing mod** (`investigation.py`) | exists |
| goals with short/medium/long horizons | **existing mod** (`goals.py`) | exists |
| social relationships −4…+4 | **legacy pattern + tags** | partial: needs a current home |
| Series/Episode/Scene structure | **missing** | this proposal |
| typed cross-layer links | **missing** | this proposal |
| astral overlay/projection/permission | **missing** | companion PSI draft |
| Lead/Evidence as first-class authored objects | **missing vocabulary** over existing clues | this proposal |
| emotion estimate for interviews | **missing** | this proposal, optional |

### 2.3 Versioned starting state

```yaml
start_profile: campaign01@v2        # what the game loads
profiles:
  campaign01@v1:                    # author graph README, still valid
    home: physical/home_helsinginkatu     # Sörnäinen flat, "UNSA-provided"
    employer: unsa
    hq: physical/unsa_hq_ratakatu
  campaign01@v2:                    # campaign #1132 canon
    home: physical/kurvi_company_flat     # agency-owned housing
    employer: europol
    hq: physical/europol_helsinki         # address ? (Ratakatu address flagged)
    supersedes: campaign01@v1
```

A profile is **data, not code**: moving the start state later means adding a profile, never editing a scene.

---

## 3. The five graph schemas

Shared base, applied to every node and edge. Authored fields are marked **A**; computed fields are marked **C**
and must never be written by hand.

```python
# design only — no module is created by this proposal
GraphHeader = {
  "graph_id": "physical:helsinki",      # A  namespaced, stable
  "graph_type": "physical|cyber|astral|social|story",
  "version": 3,                          # A  bumped when an authored record changes shape
  "source_doc": "design/graphs/README.md",  # A
  "author_status": "author|agent_proposal", # A
}

Node = {
  "node_id": "physical:kurvi_company_flat",  # A  <family>:<slug>
  "node_type": "city|district|location|room|…",  # A  per family
  "label": "Kurvi company flat",         # A
  "description": "…",                    # A
  "layer": "physical|cyber|astral",      # A
  "coordinates": {"map": [0.69, 0.31]},  # A  optional; map position, not physics
  "tags": ["housing", "agency_owned"],   # A
  "visibility": "public|discovered|GM_secret",  # A
  "prerequisites": [],                   # A  permission to perceive/enter
  "unlock_act": 1,                       # A
  "cwn_ref": "cwn_hacking:security_difficulty",  # A  the rule that governs it here
  "faction_ref": "social:europol",       # A  optional
  "character_ref": None,                 # A  optional
  "source_claim": "author README: 'Europol HQ on Ratakatu'",  # A  provenance for disputed facts
  "computed": {"degree": 3, "reachable": True},  # C  never authored
}

Edge = {
  "edge_id": "edge:physical:kurvi_to_office",  # A
  "source": "physical:kurvi_company_flat", "target": "physical:europol_helsinki",  # A
  "relation": "route|door|access|control|perceive|relationship|transition|link",  # A
  "directed": True,                      # A
  "weight": None,                        # A  only where the owner rule defines one
  "access_condition": "credential:europol",  # A
  "travel_cost": "scene",                # A  scenes, not metres
  "knowledge_gate": "flag:knows_office", # A
  "layer_transition": None,              # A  filled only by §5 link records
  "consequences": [],                    # A
  "provenance": "author README",         # A
}
```

**Validation contract** (runs in the implementation phase; the rules are stated here so Tomi can object to them):

1. every `edge.source`/`target` resolves to an existing node **in the same family**, unless the edge is a
   `layer_transition` declared in a link record;
2. `node_id` and `edge_id` are unique across the whole package, not just per file;
3. `visibility: GM_secret` nodes may not appear in any player-facing projection, action list or transition
   description — a **test** must attempt a leak and fail;
4. `relationship_score` is an integer in −4…+4 and only on `social` edges;
5. every `cwn_ref` names a symbol that exists in `src/rules/` (the same AST check the CWN audits use);
6. **no scene may be reachable only through a clue** (see §7.3): each Episode's required scenes are listed in its
   `entry_conditions`, and a validator refuses an episode whose mandatory scene is reachable solely via a roll.

### 3.1 Physical

Hierarchical: `world | city | district | location | room`. `parent_id` gives the containment tree; routes are
edges, and a route may be city-level (`district → district`) or room-level (`room → room`, a door). Optional
`map_position` matches the existing `data/world/helsinki_locations.json` convention (normalised 0..1, x east,
y south) — **not** a tactical grid. `legal_restriction` names the authority that may forbid entry
(`finish_police_warrant`, `europol_credential`), and `cyber_ref`/`astral_ref` point at nodes in the other layers
that occupy the same fiction.

### 3.2 Cyber

Node types `device | network | service | account | data | security`. Edges are `link` (there is a technical path),
`control` (one node operates another) and `access` (a credential reaches a service). **Every node carries the CWN
hacking prerequisites**: reachability (physical contact, authorized connection, proxied link) before any check.
Cyber nodes may not damage physical hit points or astral consciousness directly; that requires a link record (§5).

### 3.3 Astral

Node types `agent | anchor | realm | symbolic_site | boundary | noetic_link`. Fields per the issue, kept
deliberately non-numeric: `astral_mode: overlay | projected | manifesting`, `return_rule`, `psi_permission`,
`psi_defence`, plus `identity/agency/qualia_tag` as **permission axes** (§7.4) rather than creature stats.
**Density is not a spatial dimension** and astral location grants no physical access.

### 3.4 Social

Nodes `person | faction`, referencing character/faction sheets. Edge fields:

```yaml
relationship_score: -2          # integer −4…+4, interpersonal
relationship_kind: professional # professional|familial|romantic|political|institutional
mutual: false                   # asymmetric when false
known_to: [player, npc:maki]    # who is aware of this relation
evidence: "scene:sc01_04_interview"
goal_refs: [goal:repair_trust_with_partner]
ideological_affinity: null      # NOT the same as relationship
```

**Missing ≠ neutral.** "No relationship recorded" and "recorded at 0" are different states; the schema allows
absence and the projection must show it as absence. Faction **reputation** is a different field on a different
record (§6.3) — conflating them is the mistake the issue warns about.

### 3.5 Story

```
series → episodes[] → scenes[]
```

* **Series**: `series_id, title, episode_refs, long_term_goals (refs to goals.py), completion_conditions,
  start_profile`.
* **Episode**: `episode_id, scene_refs, medium_goals, entry_conditions, exit_conditions, alternates,
  required_scenes` (the anti-railroad and anti-missable fields).
* **Scene**: `scene_id, types[], graph_node_refs[], participants[], short_goals, leads[], evidence[],
  available_actions[], transitions[], outcomes[], flags[], spoiler_gate`.

**Graph type and scene type are different fields.** `Cyber` is a graph family *and* a scene type; a scene may be
`types: [combat, cyber, astral]` while referencing nodes from three families. One actor state, one turn.

---

## 4. Cross-layer links: the only way an action crosses a layer

A link is a **record**, not a permission implied by co-location.

```yaml
link_id: link:sc03_corridor:astral_warning
scene: story:sc03_corridor
from_layer: astral
to_layer: physical
verb: perceive             # one of §7.1's verbs
target_node: physical:sc03_corridor
actor: character:rookie
requires: [psi_permission:overlay_perception, node:astral:sc03_corridor]
cost: condition:pale       # one payer, named
defence: none              # or: psychic_defence / cwn_save:<name>
visibility: actor_only
knowledge: "the player learns a presence is near, not who"
effect: "the GM may reveal that the corridor is occupied"
consequences: [flag:warned]
```

Rules the implementation must enforce (each is a test in the later phase):

1. **No default links.** A scene with no link records permits **no** cross-layer action, even if nodes coincide.
2. **One payer.** A link names exactly one cost resource; a second resource may be *required* but not *charged*.
3. **Same turn.** A cross-layer action consumes the actor's CWN action in the shared turn — never a free parallel
   turn.
4. **Investigation boundary.** No link may grant a clue, open an exit, or bypass declared access and inquiry
   (`docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`).
5. **Psychic → Cyber is not root.** A psi-assisted intrusion still satisfies every CWN hacking prerequisite
   unless an approved technique explicitly changes one, and the link says which.

---

## 5. The authored format: Markdown with YAML frontmatter

One file per Series, Episode, Scene, plus one per graph domain. Tomi writes prose and a short header; the loader
turns records into NetworkX; **nobody edits Python dictionaries or raw graph files.**

```markdown
---
record: scene
scene_id: sc01_04_interview
types: [social, investigation]
series: campaign01
episode: ep01_the_tuesday_complaint
participants: [character:rookie, npc:maki]
nodes: [physical:kurvi_office_room2, social:npc_maki]
spoiler_gate: act1
---

# The interview

## Setting
…

## What the player can do
- Ask about the invoices → `Talk` + declared `interview`
- Show the warrant card → permission, not compulsion

## Clues
- `clue:ledger_gap` — core, competency `Administer`, access `office`, inquiry `search`
- `lead:courier_route` — points at `physical:vallila_depot`

## Transitions
- to `sc01_05_depot` when `flag:ledger_read`
```

The full set is in [`docs/graphs/templates/`](../graphs/templates/) (`SERIES`, `EPISODE`, `SCENE`, `GRAPH_DOMAIN`),
with a filled example in [`docs/graphs/examples/act1_procurement/`](../graphs/examples/act1_procurement/).

**Why YAML frontmatter and not a big YAML file:** a scene is something a human writes in one sitting; a 3 000-line
YAML graph is something only a tool can edit. The loader merges many small records into one projection, which is
exactly the split the issue asks for (authored source ≠ runtime projection).

---

## 6. Vanilla CWN, and where a mod is genuinely needed

### 6.1 Physical, exploration and combat — **vanilla, no mod**

Movement, doors, obstacles, searches: CWN's own skills — **Notice** (spot), **Exert** (force, climb, carry),
**Sneak** (avoid), **Survive** (terrain), **Fix** (mechanism), **Drive** (vehicle). Combat is CWN's: one
initiative, one action economy, attacks/damage/saves. Mixed scenes do **not** get extra turns; a cyber or astral
action inside combat costs the same action.

### 6.2 Cyber — **vanilla CWN Hacking, no second resolver**

Graph nodes map to legitimate targets. The scene's `available_actions` cite the hacking procedure, and the alert
clock is CWN's (`AlertClock` in `cwn_hacking.py`). The graph adds **reachability** (a path must exist) and
**knowledge** (you must know the node exists) — it does not add dice.

### 6.3 Social — **CWN social skills + tag mod**

Verified CWN skill names (from `data/rules/cwn/skills.json`, 19 skills): **Administer, Connect, Drive, Exert, Fix,
Heal, Know, Lead, Notice, Perform, Program, Punch, Shoot, Sneak, Stab, Survive, Talk, Trade, Work**.

* **There is no "Convince" and no "Administration".** The author's informal terms map as: *Administration* →
  **Administer**; *Convince* → **Talk** (persuade), **Lead** (command/direct), or **Connect** (find the person who
  can), depending on the action. The design must not invent a skill.
* Relationship and reputation are **different fields**: `relationship_score` (−4…+4, interpersonal, on a social
  edge) and `reputation` (−4…+4, per-faction perception, on a reputation record). A faction can respect her
  (+2) while her partner distrusts her (−2).
* Ideology is neither: `ideological_affinity` is a *goal/position* comparison, and the campaign's whole point is
  that political agreement is not friendship.

### 6.4 Investigation — the existing resolver already does the job

| issue's proposed tag | what already exists | proposal |
|---|---|---|
| **Investigation Capability** ("ability to find leads/evidence automatically") | `Clue.competency` + `access` + `inquiry`; `discover()` grants without a roll when all three are declared | **do not add an ability list.** Capability = the competency the scene names, and the *means* (training, BCI feed, lab, controller) is fiction that can grant `access`, not a new stat |
| **Lead** | `Clue.leads_to` (scene ids) | extend to `leads_to: [node:…]` so a lead can point at a person/site node, not only a scene |
| **Evidence** | `Clue.fact` + `scene_id` | add optional `provenance` and `authenticated_by` (a lab, a chain of custody, a witness) — **evidence is an artifact with provenance, a clue is a fact** |
| core vs optional | `ClueKind.CORE/OPTIONAL`, `obscure`, `passive` | unchanged; **the invariant that a core clue cannot be missed already holds** |

**Two models compared, as the issue asks:**

* **(A) Investigation Ability tags by specialty** — a new list (Forensics 1, Data Analysis 2, …). It duplicates
  what CWN skills already express and adds a second ladder.
* **(B) Existing skills + authored access** — the scene says which competency, which access, which inquiry. A BCI
  feed is `access: bci_feed`; a Europol lab is `access: lab_analysis`; a human controller is `access:
  controller_review`, each with a cost and a legal constraint.

**Recommendation: B.** It is already implemented, already tested, and already respects the no-missed-core-clue
invariant. A adds a ladder the campaign does not need.

### 6.5 Work vs Know — naming for the Europol academy

The issue asks for a name for the academy speciality of **Know** and a definition of **Work (Europol Agent)**.

| skill | what it answers | example tasks |
|---|---|---|
| **Work (Europol Agent)** | *how to do the job*: procedure, paperwork, chain of custody, interagency etiquette, field craft | file a cross-border request; secure a scene without contaminating it; draft a warrant application in the right form; run an authorised interview |
| **Know (?)** | *what is known*: law, institutions, theory, analysis | which authority can compel a phone record; what a money-laundering typology looks like; what an AGI containment regime permits; what PSI research claims |

Proposed names, ranked:

1. **`Know (Law & Intelligence)`** — covers EU law and rights, criminal/intelligence theory, data analysis and
   the institutional map. **Recommended.**
2. `Know (Europol Studies)` — accurate but narrow; it names the school, not the knowledge.
3. `Know (Security & X-Risk Studies)` — best for the AGI/NHI/X-risk material, worst for ordinary casework.

**Arbitration rule:** if the question is *"what does the law/institution/theory say?"* it is **Know**; if it is
*"how do I actually do this, here, now, without fouling it up?"* it is **Work**. A sample: *"May I read this
suspect's BCI log?"* is Know (the legal basis) followed by Work (the request, the form, the seal). The same
question resolved by a roll is a Work check with a Know-based permission.

### 6.6 Interview scenes and the optional emotion model

The issue proposes a psychotronic empathic-responsivity model "similar to The Veil", and asks whether to have one
at all.

**Proposal: four emotion tags, device-estimated, never a truth detector.**

```
affect: fearful | guarded | overwhelmed | cooperative     # the device's estimate
confidence: low | medium | high                            # the device's own reliability
```

* The GM sets `affect` from the fiction; the device shows an **estimate** with a confidence, and `low` may be
  simply wrong. A wrong estimate is the most useful result in the game.
* **It never answers "is he lying?"** No tag, no roll, no device tells truth from falsehood. That is what
  `Talk` + evidence + a contradiction is for.
* Consent and law apply: an interview is lawful questioning; a forced read is misconduct and a case-breaking
  fact, not a shortcut (see `DRAFT_NOOPUNK_PSYCHOTRONICS.md` §4.3).

---

## 7. Astral: the layer that needs the most restraint

### 7.1 Three modes, not three games

| mode | what the character is | what the player may do |
|---|---|---|
| **overlay** | embodied; astral perceived as an AR layer on the physical | perceive, contact, shield — never travel |
| **projected** | awareness in an astral body; physical body anchored and vulnerable | perceive, contact, shield, traverse astral, return |
| **manifesting** | projected, spending to be seen/heard physically | one bounded physical-perception effect, at a cost |

A character in `projected` mode is **not** in the physical scene and cannot act there, except through a link record.

### 7.2 The Verb × Target matrix (default DENIED)

Nine targets: `self, conscious_person, living_biologic, inert_object, construct_device, cyber_node,
astral_agent, astral_region, group_link`.
Eight verbs, from RULES.md and the issue: `perceive, contact, shield, project, influence, imprint, ritualize,
manifest`.

| verb \ target | self | person | biologic | object | device | cyber | astral_agent | region | group |
|---|---|---|---|---|---|---|---|---|---|
| perceive | — | ✓ Act II | ✓ | ✗ | ~ link | ~ link | ✓ | ✓ | ✗ |
| contact | — | ✓ Act II | ~ 2nd density | ✗ | ✗ | ✗ | ✓ | ✗ | ~ SMC |
| shield | ✓ | ✓ | ✗ | ✗ | ~ implant | ✗ | ✓ | ✗ | ~ group rite |
| project | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| influence | ✗ | **restricted** | ~ | ✗ | ✗ | ✗ | **restricted** | ✗ | ✗ |
| imprint | ✗ | ✗ | ✗ | ~ rare | ~ rare | ~ via hacking | ✗ | ✗ | ✗ |
| ritualize | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ~ | ✓ prepared |
| manifest | ✓ | ✗ | ✗ | ~ late | ✗ | ✗ | ✗ | ✗ | ✗ |

`✓` allowed with a written link/technique; `~` allowed only through a named mod and an authored record; `✗`
denied; **`restricted` requires author approval and is scripted by default**. Every permitted cell must supply:
`source_system, required_attunement, target_visibility, link_basis, action_economy, cost_resource, range_or_anchor,
duration, resistance, investigation_boundary, physical_effect, actor_knowledge, target_knowledge`.

**One resource per activation.** Published SWN Effort *or* an author-approved chakra conversion — never both, and
never a second pool for the same effect.

### 7.3 The no-railroad / no-oracle invariants

1. **A core clue is never behind a roll.** Already enforced by `investigation.py`; the graph validator must refuse
   a scene whose only route to a mandatory scene is a skill check.
2. **Astral perception never yields a clue.** It may yield a *lead* (a place to go, a person to ask) at most, and
   a lead is not evidence.
3. **GM-secret nodes never leak.** A `GM_secret` astral node is invisible to player-facing projections, action
   lists and transitions, even when the player is projecting into the same region.

### 7.4 Density, identity and agency — permission axes, not stats

The author's model distinguishes **Consciousness (qualia)**, **Identity (self-awareness)** and **Agency (free
will)**. Proposal: three **tags** on an entity record, each a short enum, so that defence and consent can be
reasoned about without turning people into character sheets:

```
experiential_complexity: minimal | biological | personal | collective
self_identity: absent | emerging | present
agency: none | reactive | choice
```

A camera is `minimal/absent/none`; a dog is `biological/present/reactive`; an unawakened human is
`personal/present/choice`; an SMC is `collective/present/choice`. **Agency gates consent** — and consent is what
makes `influence` restricted rather than free.

### 7.5 Density interaction matrix (1st–7th)

| density | what it is in the author's model | draft consequence |
|---|---|---|
| **1st** | panpsychic matter, and **all ordinary technology**: robots, drones, turrets, cameras, AIs | PSI interfaces with matter/devices through **named techniques only**; "extremely effective against constructs" is an **author premise**, balanced by cyber security, isolation, QIP countermeasures and the fact that a camera has `agency: none` and cannot resist — but also cannot be *persuaded* |
| **2nd** | living biologics, up to chimpanzees | perceive and calm, not command; species-appropriate resistance; **never** "programmable animals" |
| **3rd** | unawakened humans — most people | latent PSI, full personal agency. Weaker *active* PSI does **not** mean no defence or no consent |
| **4th** | awakened humans, emerging SMC | the PC's stage. Unlocks defences and abilities; polarisation consequences; the protagonist is **always StO** |
| **5th** | advanced NHI, including StS Orion leadership (Mantids) | power asymmetry handled by **threat, containment, defence, help and retreat** — never a one-roll instant kill, never ad hoc invulnerability |
| **6th/7th** | far higher | author-controlled scenes and contacts only; **not playable**, no stat inflation |

**Higher density does not remove consent or agency from lower-density beings.** That single sentence is the
design's ethical spine, and it is also what keeps 5th-density antagonists frightening without making them
unbeatable.

---

## 8. Glossary: the fiction's vocabulary with honest science beside it

| term | correct scientific meaning | the author's metaphysical premise **[c]** | rule field / interaction |
|---|---|---|---|
| **Nonlocality** | quantum correlations that cannot carry a controllable signal; "spooky action" is not communication | an entangled conscious agent can interact at any distance | requires a named `link_basis`; finite range unless a technique says otherwise |
| **Entanglement** | a joint state with no separable description; not produced by looking at something | line-of-sight creates a working link | `link_basis: line_of_sight` for same-room targets — **author rule**, not physics |
| **Superposition** | amplitudes combining until measurement context fixes an outcome | a person may be in competing possible states | optional `uncertain` tag for competing outcomes; **never** a free "be in all scenes" action |
| **Collapse / measurement** | interpretation-dependent; decoherence explains why macroscopic states are stable | consciousness collapses it; two agents contest the collapse | contested intention resolved by **published defences**, not by "stronger mind wins" |
| **It from qubit** | quantum information as a framework in physics; not a claim that matter is conscious | information is fundamental and has simple qualia | fictional ontology only; do not conflate information, energy and agency |
| **Wave–particle duality** | complementary descriptions depending on measurement context | — | no mechanical effect; explicitly **not** "switch to invulnerable" |
| **Constructive / destructive interference** | addition or cancellation of amplitudes — *not* "inference" | two agents' intentions can add or cancel | `noetic_interference: constructive|destructive` as a contested tag, never a damage multiplier |
| **Consciousness / Identity / Agency** | Faggin's three axes; contested as physics | gradations from matter to SMC | §7.4 tag axes; **not** character attributes |
| **Observe–Experience–Act** | a proposed loop for conscious agents | the resolution sequence for PSI | fiction only; **not** an extra action phase or a triple roll |
| **Prana / chakras / Kabbalah / polarisation** | traditions and Law of One narrative | energy and polarity vocabulary | named permissions only, when first used; **no duplicate expenditure** with SWN Effort |
| **Astral projection / remote viewing** | no established mechanism | the Seity leaves the body | §7.1 modes; projection needs anchor + return rule; **precognition is scripted-only** for the rookie |
| **1st–7th density** | — | developmental/metaphysical states | §7.5; **never** spatial dimensions or combat levels |

**Source boundary, stated once:** quantum nonlocality is not superluminal signalling under standard physics
(Pawłowski et al., *Nature* 461:1101–1104, 2009; NIST's 2014 release on the same limit); interference is not
inference; and Hoffman, Faggin, Radin and the Law of One are **separate frameworks**, not evidence that
Hilbert-space states are editable by intention. NoöPunk's rules are **fiction with honest vocabulary**.

---

## 9. Three worked scenes

### 9.1 Act I — grounded: *the Tuesday complaint* (physical + cyber + social)

**Graph records used:** `physical:kurvi_office`, `physical:kurvi_office_room2`, `physical:vallila_depot`;
`cyber:depot_gate_controller`; `social:npc_maki` (relationship +0, professional).

| step | declaration | resolution |
|---|---|---|
| 1 | the rookie reads the complaint file | **Administer**, access `office` — no roll; the core clue `clue:invoice_gap` is granted |
| 2 | she asks the depot's gate controller for the last 30 days | **Work (Europol Agent)** to file the request properly; the *permission* is a credential, not a roll. Result: `evidence:gate_log` with `provenance: controller`, `authenticated_by: controller_firmware` |
| 3 | she interviews the dispatcher | **Talk** + declared `interview`; the clue `clue:shift_swap` (core) is granted without a roll; the *optional* clue `clue:motive_gossip` needs a Talk check |
| 4 | she wants the camera feed analysed | `access: lab_analysis` — a scene, a cost, a chain of custody; the lab returns `lead:night_van`, not a conclusion |

**Know vs Work in play:** *"Can I compel the gate log?"* is **Know (Law & Intelligence)** — the answer is no
without a Finnish warrant; *"Get me a lawful request in front of the right office today"* is **Work (Europol
Agent)**. Failure on either never removes `clue:invoice_gap`; it changes time, cost, and who is annoyed.

**No PSI. No anomaly. That is the point of Act I.**

### 9.2 Act III — layered: the corridor (physical + cyber + astral, one turn)

**Records:** `physical:sc03_corridor` (opponent, camera), `cyber:sc03_camera_feed`,
`astral:sc03_corridor_region`, links: `link:perceive_warning` (astral→physical), `link:cyber_alert_suppress`
(psi-assisted intrusion).

Turn 1, the player must choose **one**:

* **shoot** — CWN attack, vanilla;
* **hack the camera** — CWN hacking; the psi-assisted variant *still* needs the same access prerequisites and
  adds `cost: condition:pale` — it is a link record, not a shortcut;
* **shield** — psychic defence, holding an action;
* **perceive astrally** — gains `knowledge: someone else is in the corridor`, gains nothing about *who*.

The player cannot do all four: **one turn, one action**, and the astral overlay does not grant extra time. If the
camera is hacked and the presence perceived in the same scene, that is two actions over two turns, and the alert
clock advances in between.

### 9.3 Act IV — high-density intrusion (5th-density StS contact)

**Record:** `astral:sc09_orion_mantid` (`experiential_complexity: collective`, `agency: choice`), link
`link:sc09_contact` (`verb: contact`, `defence: psychic_defence`, `cost: condition:…`, `visibility: actor_only`).

1. **Detection** — the character perceives an arrival (a sensory fact, not a roll); the GM states the fiction.
2. **Defence** — one `shield` action; success reduces the intrusion to a *cost*, not a nullification.
3. **Help** — a party member's QIP implant can grant a second defence **at the implant's own cost** (single payer).
4. **Bystanders** — protecting them is a CWN action, and it competes with defending herself. That tension is the
   scene.
5. **Escape or return** — the projection's return track (§ companion draft) or an ordinary physical retreat.
6. **Consequence** — a condition tag, a memory fragment, a relationship change. Never instant death, never
   invulnerability.

**Scripted vs active:** the Mantid's *arrival*, its *words*, and the *revelation* are scripted; the player's
defence, her choice to protect a bystander, and her escape are active. A 5th-density entity may win any contest it
is written to win — but the scene must leave the PC an action, or it is not a scene.

---

## 10. Phase plan (for later authorisation — **not** this issue)

| phase | delivers | needs |
|---|---|---|
| **0** | the authored format + validator (no runtime) | this proposal's approval |
| **1** | Physical graph traversal on vanilla CWN; the existing `helsinki_locations.json` becomes the first domain record | CWN + the format |
| **2** | Story hierarchy (Series/Episode/Scene) with goals wired to `goals.py`; no astral, no cyber mods | phase 1 |
| **3** | Social graph + reputation records; interview scene with emotion estimate | phase 2 + tags decision |
| **4** | Cyber graph over CWN hacking (reachability + knowledge only) | phase 3 |
| **5** | Astral graph, overlay/projection, the first link records | the PSI draft's approval |
| **6** | Cross-layer effects, psi-assisted hacking, manifesting | phase 5 + explicit approval per effect |

Each phase ends with: authored example → tabletop procedure → Python implementation → tests, **in the same PR**,
per `AGENTS.md`.

---

## 11. Open decisions for Tomi

1. **Home and employer:** Kurvi company housing + Europol (newer canon), or Sörnäinen flat + UNSA (graph README
   and `helsinki_locations.json`)? Both profiles are written; which is `campaign01@v2`?
2. **The Europol HQ address** — is it the Ratakatu building, a floor in it, or somewhere new?
3. **Investigation model:** B (existing skills + authored access, recommended) or A (ability tags)?
4. **`Know` speciality name:** `Law & Intelligence`, `Europol Studies`, or `Security & X-Risk Studies`?
5. **Emotion model:** four tags with a confidence, or none at all? And does a wrong device estimate ever reach the
   player?
6. **Verb scope:** is `influence` approved at all (scripted only), and is `imprint` ever playable?
7. **One PSI resource:** SWN Effort, or a chakra conversion — and if the latter, is it a conversion of Effort or a
   replacement?
8. **Density premise:** is "PSI is extremely effective against 1st-density technology" a rule or a flavour line?
   It changes how dangerous a hacker with PSI is.
9. **The link-record overhead:** one YAML block per cross-layer effect is explicit but wordy. Would one line in
   the scene header (`links: [...]`) be enough?
10. **Where the drafts live:** `docs/design/` (current) or `docs/graphs/`? The templates are already under
    `docs/graphs/`.
11. **NetworkX:** a runtime dependency now, or a projection built only when a tool needs it?
12. **GM-secret leaks:** is a hard validator failure enough, or do you want the projection to be *physically
    incapable* of representing a secret node to the player view?

---

## 12. What this proposal does not do

* It does not modify `design/graphs/README.md` or `design/graphs/RULES.md`.
* It does not add Python, change CWN, or touch `RULEBOOK.md`.
* It does not merge the Law of One RPG, or promote the #1137 drafts to approved mods.
* It does not claim that any cited theory demonstrates PSI.

## 13. Sources, with verification status

| source | status in this pass |
|---|---|
| `design/graphs/README.md`, `design/graphs/RULES.md` | read verbatim; **unchanged** |
| `src/rules/investigation.py`, `goals.py`, `noopunk_tags.py`, `cwn_hacking.py`, `swn_psionics.py` | read; symbols cited above exist |
| `data/world/helsinki_locations.json` v2; `data/rules/cwn/skills.json` (19 skills) | read |
| `legacy/ubiquitous_maniacs/src/*/graph.py`, `graph_serialization.py` | read; comparative only |
| `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`, `CWN_IMMUTABLE_CORE_1068.md`, `GOAL_TAG_1119.md` | read |
| `docs/design/DRAFT_NOOPUNK_{PSIONICS,PSYCHOTRONICS,CHARACTER_TAGS,EUROPOL_CHARACTER_GENERATION}.md` | cross-referenced |
| Pawłowski et al., *Nature* 461:1101–1104 (2009) — information causality | citation confirmed by the issue's link; body not read in this pass |
| NIST, "Rush Light Wave and You'll Break Its Data" (2014) | cited from the issue; not re-verified |
| Hoffman & Prakash (2014); Faggin (arXiv:2012.06580); Radin; Law of One | cited as **frameworks**, with no empirical claim; primary texts not re-read here |
