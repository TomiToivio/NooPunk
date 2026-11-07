# Prompt: PSI scope, Astral Projection as scripted events, and the four graph families

- **Date:** 2026-11-05
- **Topic:** issue #1178
- **Source:** Tomi's own issue text in NooPunk, <https://github.com/TomiToivio/NooPunk/issues/1178>
- **Archive status:** original author prompt, retained verbatim for future reuse. It is **not** an approved canon or
  implementation specification by itself, and archiving it does not authorize work on a frozen subproject.

## Original prompt (verbatim issue text, transport formatting normalised)

# Goal

Simplify and clarify the NoöPunk **SWN Psionics, psychotronics and graph architecture**. Treat the decisions below as **author direction** that supersedes conflicting proposals in [#1164](https://github.com/TomiToivio/NooPunk/issues/1164), [the Astral Graph/PSI draft](https://github.com/TomiToivio/NooPunk/blob/main/docs/design/DRAFT_ASTRAL_GRAPH_SWN_PSI_1164.md), and [the general graph proposal](https://github.com/TomiToivio/NooPunk/blob/main/docs/design/DRAFT_GRAPH_SCENES_1164.md), where those drafts disagree.

**Priority:** Implement **Physical, Cyber, Social and Series/Story graphs now**. **Defer the Astral Graph** until scripted Astral Projection is introduced. The remaining mechanical changes can be implemented separately later. Do not turn this issue into an implementation of a full real-time Astral subsystem.

## 1. Simplify playable SWN psychic powers

- The **player character may select only Telepathy and Telekinesis** from the SWN psychic disciplines/powers. Do not offer the PC the other SWN psychic disciplines through ordinary advancement or free technique selection.
- Other PSI abilities can exist for NPCs and as **scripted story events**, not as extra player-selectable SWN psychic powers.
- Use **SWN Psychic Training Focus** for advancement in allowed SWN psychic abilities, retaining its published prerequisites, level benefits and Effort increases, rather than inventing a new NoöPunk PSI skill tree or generic Verb × Target advancement system.
- **Psychic Training Focus** (SWN, paraphrased implementation requirements; consult the authorized rulebook for full wording):
  - **Eligibility:** Psychic, or Adventurer with Partial Psychic option; a Partial Psychic's training is restricted to its chosen discipline. The Focus is normally acquired only once.
  - **Level 1:** Bonus psychic skill; if this brings it to skill level 1, select an eligible level-1 technique; maximum Effort +1.
  - **Level 2:** On each character level-up, allocate one additional skill point toward improving the chosen psychic skill or learning a technique from it. Retrospective points accrue when taking this Focus later; unspent points may be banked for later purchases.
  - **No loophole:** For the PC, both the bonus skill and new techniques must remain in Telepathy or Telekinesis; do not allow a second discipline through the Focus.
- Preserve SWN-derived accounting/requirements where applicable; CWN remains the immutable baseline for ordinary skills, combat and hacking. Confirm edition-specific mechanics against the source before coding.

**Scope distinction:** The restriction above concerns **PC selections from the SWN psychic discipline system**. The additional AWN Mentalist and CWN Spellcaster/Summoner Edges listed below are distinct opt-in character features using their respective published mechanics. Resolve any overlap with SWN class prerequisites explicitly; do not silently grant a new SWN discipline.

## 2. Astral Projection is scripted, not a standard selectable SWN power

Astral Projection occurs via **authored scenes**, including:
1. Spontaneous out-of-body experiences (**OOBEs**) while sleeping.
2. **NDEs** (near-death experiences).
3. Events induced by **special technology inspired by Robert Monroe-style projection methods**.

These events may show Astral/Time-Space locations and enable authored interactions, but do **not** require a freely activated player-selected Astral Projection technique, a seventh SWN discipline, a general projection skill tree, or a constantly running Astral Graph.

Keep Astral Projection/Noöspace lore, visions, dreams and scripted scenario capabilities available to the storyteller. **Build the Astral Graph only later**, when such scenes need their own navigable graph. Until then a scripted event can be represented as a Story/Series scene with tags and descriptive links, rather than constructing a premature Astral subsystem.

**Psychotronics:** Devices are **cybernetic implants and other pieces of equipment that grant psionic abilities**. They use the relevant equipment/Edge/ability contract; do not invent an obligatory second universal psychotronic power subsystem. Devices may grant abilities outside the PC's *selectable SWN discipline* list when specifically authorized by their own equipment rules or a scripted event; they must not accidentally make prohibited SWN disciplines freely selectable.

## 3. AWN Mutant Edge: Mutants, with uncertain origins

Use the **AWN Mutant Edge** for **Mutants**, not for a class of characters definitively identified as alien Hybrids. **Mutant** is the broad in-world category for people with mutations; **Hybrid** is a possible origin or interpretation, not a synonym or a fact automatically revealed by the Edge.

- Most Mutants **may in fact be human–NHI Hybrids**, including those associated with Greys, but neither the player nor investigators should automatically know who is a Hybrid, which NHI is involved, or whether an observed mutation has an entirely different explanation.
- As the NHI Crisis and its aftermath unfold, expect **many kinds of mutation**: genetic engineering, environmental or technological exposure, unusual developmental changes, anomalous PSI-related effects, unknown causes and potential hybrid ancestry. Treat these as possible fictional explanations, not established diagnoses.
- **Mutations do not prove alien ancestry or psychic ability.** Use the AWN Mutant mechanics for variable traits and Stigmas without automatically making every Mutant psychic. A particular confirmed Hybrid lineage may be psychic according to its NPC design.
- **Mutant Edge remains NPC-only**: the player character cannot select it. Mutants can be witnesses, suspects, allies, adversaries and ordinary civilians, not only infiltrators.
- Don't conflate apparent appearance with identity, origin or legal status. Investigative evidence should be needed to infer ancestry or cause; unreliable evidence, stigma and competing explanations suit the campaign.
- AWN positive, negative, Pseudo-Psychic and Stigma tables can be used as published for specific NPCs. The older proposed **mandatory Hybrid-only mutation packages** (baseline two-positive-mutation path, recognizable-alien Stigma path, compulsory Grey-DNA PSI and universal Hybrid registration assumptions) are **superseded**, not default requirements for all Mutants. Particular Hybrid subtypes may be defined later as lore or optional NPC templates.
- Confirm AWN table and roll details against the published rules when implementing a specific template, without inventing extra probabilities.

## 4. Additional character Edge options

- **AWN Mentalist Edge:** may be selected to become a **Mentalist**. Use the actual AWN Mentalist rules rather than reconstructing them as SWN techniques.
- **CWN Spellcaster Edge:** may be selected to become a **Spellcaster**. Use the CWN Edge rules.
- **CWN Summoner Edge:** may be selected to become a **Summoner**. Use the CWN Edge rules.
- **Ontology:** **Magick is PSI, and PSI is Magick.** These are different traditions/interfaces for the same in-universe phenomenon, but their published **game mechanics and resource costs remain distinct unless an explicit conversion is approved**. No free spellcasting or summoning from simply knowing Telepathy.
- Check prerequisites and interactions among CWN Edges, SWN Psychic/Partial Psychic classes, the Psychic Training Focus and AWN Mentalist. Avoid double-dipping or accidental unrestricted SWN discipline access. Respect any limits the source rules put on class/Edge combinations.

## 5. Correct the graph model: spatial vs relational nodes

**Important correction:** In **Physical and Astral graphs, nodes are LOCATIONS, not characters or conscious agents.** PC/NPC entities **occupy** location nodes and **move through edges** between them. Characters at the same node may interact subject to normal scene conditions. A character may be referenced from a node's occupancy list but is not itself a spatial node.

| Graph | Nodes | Edges | Characters / movement |
|---|---|---|---|
| **Physical** | Places: world/city/district/location/room or other appropriate-scale **locations** | Routes, doors and travel connections | PC/NPCs occupy a physical location node and traverse edges; co-location enables ordinary interaction. Use CWN movement/exploration/combat. |
| **Cyber** | Devices/computers/services, including cameras, turrets and hosts linked to a Physical node; **also navigable destinations for hacker avatars** | Network links between devices/services | A cyber avatar is located at a Cyber node and traverses network edges under CWN Hacking. Devices can themselves act as machines while also functioning as avatar-visit-able nodes. A physical character remains at its Physical node. |
| **Social** | **Characters or factions** | Social connections, including −4…+4 relationships | Characters/factions **are** the nodes; social links are *not* routes for physical travel. |
| **Series / Story** | Series, Episodes and Scenes (with appropriate hierarchy) | Sequence, dependency, prerequisite and possible transitions | Scenes reference physical/cyber/social entities and character occupants; scenes are not extra spatial locations. |
| **Astral (later)** | Astral **locations**, including realms, symbolic sites and waypoints | Astral pathways/connections | Projected PC/NPCs **occupy** an Astral location and move along edges; conscious agents are occupants, not location nodes. |

**Key invariants:**
- Distinguish **entity** (`character_id`), **place** (`node_id`), **occupancy** (`character_id, graph_id, node_id`) and **movement** (traversal of a valid edge).
- Physical and Cyber location links are references, **not copies**: a turret/CCTV can have `physical_location_ref` and also be a Cyber node. A Cyber node may perform device actions *and* serve as an avatar's current node.
- Moving an avatar in Cyber does not teleport its operator's physical body.
- Social characters and factions remain network nodes, regardless of their current Physical location.
- One canonical actor record/HP/inventory; no duplicated PC or NPC instances when the same character participates in multiple graphs.
- In a scene with multiple overlays, apply a single CWN action economy, the existing permission checks and the established investigation clue boundary.
- Design author-editable Markdown/YAML and derive NetworkX views from these data, as in #1164, **but correct all schemas, examples and validation tests that erroneously treat Astral conscious agents as spatial nodes**.

## 6. Scope and sequencing

### Implement now: first playable graph slice

- [ ] Audit current graph/navigation models and relevant #1164 drafts for assumptions that Physical/Astral agents are graph nodes.
- [ ] Implement the **Physical location graph** (locations/edges, occupant positions, valid movement, co-location interaction) with vanilla CWN movement, exploration and combat.
- [ ] Implement the **Cyber device/network graph** (device nodes, network edges, location references, avatar occupancy/navigation and device actions) with vanilla CWN Hacking.
- [ ] Implement the **Social character/faction graph**, signed −4…+4 edges, compatibility with existing personality/goals/reputation data, without creating a new social combat resolver.
- [ ] Implement the **Series → Episode → Scene graph**, prerequisites, alternatives, goals, scene type metadata and links to Physical/Cyber/Social records; reuse current goal/investigation mechanisms.
- [ ] Add stable IDs, author-friendly source formats, graph validation/serialization, and tabletop + Python acceptance tests for the **four** current graph families.
- [ ] Test: two NPCs meet when both occupy the same Physical node; movement follows an allowed edge; a camera is a Cyber node with a Physical location; a hacker avatar moves between devices without moving its body; Social ties persist across physical travel; a scene transition depends on a goal/flag.
- [ ] Keep graph architecture compatible with adding **Astral location nodes and projected occupant positions** later, but do not implement Astral navigation yet.

### Later, as separate approved work

- [ ] Adapt PC-selectable SWN Psychic Training Focus/Telepathy/Telekinesis restrictions after published-rule verification.
- [ ] Implement the AWN Hybrid/Mutant Edge and mutation/Stigma selection rules; resolve explicit table/path ambiguity first.
- [ ] Integrate AWN Mentalist and CWN Spellcaster/Summoner Edges with proper prerequisites.
- [ ] Implement device-granted psionic effects using existing equipment and psi accounting where applicable.
- [ ] Add **Astral Graph** only when an authored Astral Projection story scene requires navigation; projected characters occupy Astral location nodes.

**Out of scope now:** freeform Astral Projection, general consciousness-as-node graph, a second all-purpose PSI Verb × Target rules engine, a replacement for CWN Hacking, and sweeping rewrites of CWN/SWN/AWN/WWN systems.

## 7. Documentation and compatibility

Update derived design documents and examples to reflect these **newer author decisions** when implementing. Preserve the historical drafts with a clear superseded-by link rather than silently treating their earlier proposed Astral agent-node schema or freely activated projection rules as current design. Keep the author's source design readable; note the corrected node semantics explicitly. Cross-reference [#1164](https://github.com/TomiToivio/NooPunk/issues/1164) rather than closing or conflating the two issues.

**Acceptance criterion:** the four currently scoped graph families are testable and playable independently of an Astral Graph. The new character options and scripted Astral features are accurately recorded as future tasks without accidentally being implemented in this pass.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

This issue is the record of the author's decisions; I did **not** create a second one. Two additions and one conflict worth naming before anyone implements.

## 1. The Europol line, kept as fiction

The author's phrasing is sharper than §3's legal paragraph and should survive as the in-world rule: **Europol has to *prove* a person is a Hybrid before it may use lethal force on them.** That is not a combat permission — it is a burden of proof that makes every hybrid investigation a procedural problem, which is the whole point. Proposed wording for the rulebook: *suspicion of hybrid ancestry is grounds for investigation and detention under applicable law, never for summary force; an unregistered hybrid who has committed no crime is a regulatory and civil-rights case, not a target.*

## 2. Psychic Training is paraphrased on purpose

§1 paraphrases the SWN Focus rather than reproducing it. That is deliberate — the book's text is not reproduced in this repository (`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`). Implementers verify the exact Level 1/Level 2 wording and Effort increase from the authorised edition; the paraphrase is the requirement, the book is the wording.

## 3. A conflict this decision creates, flagged now

§1 restricts **player-selectable** SWN powers to **Telepathy and Telekinesis**. Two existing drafts give the rookie more than that:

| draft | what it currently says | what this issue implies |
|---|---|---|
| [#1137 Psionics](https://github.com/TomiToivio/NooPunk/blob/main/docs/design/DRAFT_NOOPUNK_PSIONICS.md) | three playable abilities: Astral Projection, bounded Telepathy, **Psychic Defence** | Astral Projection becomes scripted (§2 here); **Psychic Defence is not a SWN discipline**, so as a *player power* it has no home — it becomes a property of the psychotronic implant (equipment) or a scripted event |
| [#1174 rookie build](https://github.com/TomiToivio/NooPunk/blob/main/docs/design/DRAFT_EUROPOL_ROOKIE_BUILD_1174.md) | Freak's start = empathy or **defence**; Level 1 awakening grants **defence + empathic reading**; Level 2 grants telepathy | the Freak's start must come from **Telekinesis or Telepathy** (or from the implant), and the awakening ladder must stop granting Defence as a selectable power |

Not a reason to change this issue — the author's decision wins. But the two drafts need a `Superseded-by #1178` note on those specific rows when they are next touched, or the next agent will implement defence as a player power and call it canon.

## 4. On the graph correction

§5's invariant list is the right fix, and the error it names is real: the #1164 proposal's Astral schema had `agent` as a **node type**. Under the corrected model an astral agent is an **occupant** of a location node, exactly like a character in a physical room. Two consequences worth writing into the validator:

* an **occupancy** record (`character_id, graph_id, node_id`) must be the only way a character is "in" a graph; a character record must never be usable as a node id;
* a **Cyber** node is both a device (it can act) and a place (an avatar can be located there) — so the projection must allow node kinds to carry both `device_actions` and `occupancy`, and moving an avatar must never move the operator's physical occupancy.

Astral Graph deferred, four graphs now, exactly as stated.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

First graph slice implemented and merged in #1182 (`f415ed52`). **Issue stays open** for the later psionics/Hybrid/Edge/Astral work.

**Delivered:**
- `src/world/graphs.py` — Physical locations + occupants/routes; Cyber devices as avatar-addressable nodes; Social character/faction nodes with −4…+4 directed ties; Story Series → Episode → Scene with prerequisites and gated transitions.
- Corrected node semantics: Physical locations hold occupants; Cyber avatars move without moving the body; Social ties are not routes; Story scenes are not locations.
- `WorldGraphs` validation/serialization, optional `to_networkx()` view, and YAML-compatible dict interchange.
- `docs/rules/WORLD_GRAPHS_1178.md` and 22 acceptance tests in `tests/test_world_graphs_1178.py`.
- Superseded-by banners on the #1164 drafts and `ASTRAL_PSI_1164.md`.

**Deferred, as the issue says:** Astral Graph/Projection, Psychic Training Focus, Hybrid/Mutant, Mentalist/Spellcaster/Summoner Edges and the PC Telepathy/Telekinesis restriction. No CWN/SWN/WWN/AWN rule changed.

Verification: 22 graph tests OK; full suite 2648 OK (3 skipped); `cwn_parity_audit --check` up to date.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## Implemented first playable four-graph slice in PR #1181

PR: https://github.com/TomiToivio/NooPunk/pull/1181 (branch `feat/1178-four-graphs`).

**Delivered:** `src/rules/four_graphs.py` adds Physical locations/occupancy and edge movement, Cyber devices with Physical references and avatar positions, Social character/faction relationship edges (-4..+4), and Series/Episode/Scene containment and condition-gated transitions. `src/rules/graph_authoring.py` compiles human-readable Markdown/YAML domain records; `src/rules/graph_text_bridge.py` derives a read-only Physical view from the existing text-game World without stealing actor ownership. Versioned serialization, optional NetworkX projection, strict graph/ref validation, and dedicated tests have been added. All new `src/rules` overlays are classified in the rules constitution. Design/authoring notes: `docs/design/FOUR_GRAPH_IMPLEMENTATION_1178.md`.

**Explicitly deferred:** SWN Psychic Training Focus/PC Telepathy-Telekinesis restriction as runnable character-generation mechanics, AWN Hybrid/Mutant and Mentalist, CWN Spellcaster/Summoner integration, psychotronic equipment rules, and the Astral Graph. Astral Projection remains a scripted-story concept. The old Astral draft is superseded by #1178 where contradictory. CWN Hacking/Combat/Investigation code and author-owned graph source documents are unchanged.

**Verification:** The initial Python suite revealed a missing rules-constitution registration, now fixed. New tests cover occupancy, movement gates, relationship symmetry/direction, story conditions, serialization and text-game parity. The latest PR CI jobs are running. **Keep issue OPEN for later phases; do not imply all deferred options are implemented.**

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## The four graphs are implemented (#1180 → `6bd8edd5`)

`src/rules/four_graphs.py` (408 lines) now models the four families with your corrected semantics, and `tests/test_four_graphs_1178.py` proves them. **The Astral Graph is not in it** — `place`/`move` for that layer is refused with a pointer to this issue, exactly as you scoped it.

### The correction is enforced, not just documented

| Graph | Nodes | Characters |
|---|---|---|
| **Physical** | places (`location`, `room`, …) | **occupy** a node, move along routes |
| **Cyber** | devices — cameras, turrets, hosts — each carrying `physical_ref` | an **avatar** is at a node; `move_avatar()` explicitly leaves the operator's body untouched |
| **Social** | characters and factions | are the nodes themselves; scores `-4..+4`, direction matters, an unknown pair is *not* neutral |
| **Story** | Series / Episode / Scene | scenes carry `references`, `goal_refs`, `all_flags`, `all_goals`, `contains`/`transition` |

`FourGraphs.__post_init__` refuses a cyber device whose `physical_ref` is not a real Physical node, and refuses a scene reference that resolves to nothing. An actor id used as a place is rejected at the gate.

### What I added on top

Two things, both verified:

1. **`src/rules/four_graphs.py` was unclassified in `module_tiers`** — the branch failed a required gate:
   ```
   - src/rules/four_graphs.py: in the tree but not in the constitution — classify it
   ```
   Now `noopunk-mod`; the gate passes.

2. **`tools/graph_authoring.py`** — a YAML front door. The rules module correctly does no file I/O, but you should not hand-write `noopunk.four_graphs` JSON. `--check`, `--json` and `--example`; the YAML is not a second format, `--json` emits exactly `FourGraphs.to_json()`.

### Honest note on duplication

I had written my own `src/rules/graphs.py` before discovering the sibling branch. **Theirs is better** — gate/lock handling, directional social semantics, an explicit `avatars` operator map, a NetworkX projection — so I deleted mine unpublished and extended theirs. No rival module.

### Verified

- `unittest discover -s tests` → **2664 tests, OK** (3 skipped), including 8 four-graph tests and 8 authoring tests
- all five repo gates green, including `rules_constitution_audit` which was failing before
- CI: the first run failed on `ModuleNotFoundError: yaml`; fixed by installing `PyYAML==6.0.2` in the test job rather than letting those tests skip — green-by-absence would have hidden exactly the negative cases that matter
- ruff clean

### Still open, as you said

The psionics restriction (PC limited to Telepathy + Telekinesis via Psychic Training), the Hybrid/Mutant Edge with its mutation and Stigma rolls, and the Mentalist/Spellcaster/Summoner Edges remain **later, separately approved work**. So does the Astral Graph, which waits for scripted Astral Projection (OOBE, NDE, Monroe-style technology).

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

The four-graph slice is implemented and on `main`; CI green (**2,669 tests, 2 skipped**). Summary of what actually landed, and the one real problem it left behind.

## Implemented

**`src/world/graphs.py`** — `PhysicalGraph` (locations + routes + occupancy), `CyberGraph` (devices that are also places an avatar enters; `location_ref` to the physical graph), `SocialGraph` (character/faction nodes, signed −4…+4 relationships, never routes), `StoryGraph` (series → episode → scene, flag-gated transitions), and a `WorldGraphs` bundle with JSON round-trip and an optional NetworkX projection. Tests: `tests/test_world_graphs_1178.py` — two actors meet only when co-located; movement follows one edge; a directed route is one-way; an avatar moves without moving its body; a camera is a cyber node with a physical location; social ties survive physical travel; a transition depends on its flag; no Astral key exists.

**`src/world/helsinki.py`** (#1183, mine) — loads the canonical `data/world/helsinki_locations.json` into `PhysicalGraph`: six real places, districts as `parent_id`, `start_location()` from the file, route endpoints validated at load. Routes come from the caller because the file has none — inventing Helsinki geography inside a loader would put fiction in a data adapter.

**`src/rules/astral.py`** — marked as a deferred prototype, not runtime authority, consistent with §2 and §6 here.

## The problem: there are now two implementations of the same four families

`src/world/graphs.py` (803 lines, #1182) and `src/rules/four_graphs.py` (408 lines, #1180) are both merged, both tested, and **neither imports the other**. Same four families, different class names for the same concepts (`LocationNode` vs `Place`, `PhysicalGraph`+`CyberGraph` vs one `SpatialGraph`), and validation that has already diverged in detail.

That is the "two engines" case the duplication audit exists for, so I recorded it in `docs/DUPLICATION_AUDIT.md` (#1185) with a recommendation rather than silently picking a winner: **keep `src/world/graphs.py` as the runtime model and turn `src/rules/four_graphs.py` into the authoring layer for it** — the YAML front door needs a parser, not a second model. That port is a behavioural change (move `tools/graph_authoring.py` and two test modules onto the world classes, delete the duplicates), so it should be its own PR. Until it lands: new work targets `src/world/graphs.py`.

## Also reported, because it happened

I wrote a second implementation of the same slice in parallel and **closed it unmerged** (#1179) once #1182 appeared — two versions of the four families would have been the exact duplication above. Only its Helsinki adapter survived, as #1183.

## Still open from this issue

The later list is untouched: PC Telepathy/Telekinesis-only enforcement, the SWN **Psychic Training** focus, the AWN **Mutant** → CWN **Hybrid** Edge with its mutation/Stigma paths, AWN Mentalist, CWN Spellcaster/Summoner, and the psychotronic-device contract. And the **Astral Graph** stays deferred by design — `astral.py` is a prototype, and a scripted astral scene is a story scene with tags for now.

One item from my earlier comment still needs a decision before those land: #1137's psionics draft and #1174's rookie build both grant the PC **Psychic Defence**, which is not a SWN discipline. Under §1 it has to become an implant property or a scripted event.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

Landed the access policy: **PR #1191, merged `6afa4523`**, verified on `main` (17 unittest cases pass, module + doc present, both drafts carry their notes).

## What this adds

`src/rules/psi_access.py` — an **access layer, not a rules engine**. No Effort costs, no technique lists, no discipline ranks; those stay with the published rules. What it decides is who may choose what:

- **Telepathy** and **Telekinesis** are the only disciplines a player character may select
- the other four SWN disciplines are NPC and scripted material
- **Astral Projection is scripted** — OOBE, NDE, psychotronic event — not a power
- **Mutant is NPC-only**; **Mentalist / Spellcaster / Summoner** stay selectable with their own published mechanics
- Magick is PSI in the fiction; **the resource costs stay distinct**

Two loopholes closed by construction: a **Psychic Training Focus cannot open a second discipline**, and a **device grant can never become a selectable option** (`Grant.selectable` is always false; constructing one with `selectable=True` raises).

## Drafts corrected

Both drafts that granted Psychic Defence as a player power now carry superseded-by notes **on those specific rows**:
- `DRAFT_NOOPUNK_PSIONICS.md` (banner: AP is scripted, defence is not a discipline)
- `DRAFT_EUROPOL_ROOKIE_BUILD_1174.md` (the Level-1 awakening row: defence comes from the implant or a scripted event)

Per your note, defence now has exactly one home: **the implant's equipment rules or a scripted event.** It is not a discipline tree, so it does not leak into the PC option list.

## Still open on this issue — deliberately

| Remaining | Blocked on |
| --- | --- |
| Psychic Training Focus levels and Effort increases | the printed SWN text; `PSYCHIC_TRAINING_FOCUS_AVAILABLE = False` keeps the omission visible in code |
| Discipline technique lists and costs | same |
| AWN hybrid/mutation/Stigma tables; Mutant NPC templates | the book, plus a specific NPC to implement |
| Astral Graph | deferred until an authored projection scene needs a navigable graph |

The issue stays open. The Europol burden-of-proof rule (prove hybrid ancestry before lethal force) is recorded in §5 of `docs/rules/PSI_ACCESS_1178.md` with your proposed rulebook wording — it is a legal constraint on the fiction, not a combat permission, which is exactly what makes hybrids a procedural problem rather than a target list.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## The duplication is gone — one graph model, and the node semantics are enforced in it

Merged as `db60ea72` (PR #1192). `docs/DUPLICATION_AUDIT.md` recorded the one real problem the graph slice left behind: `src/world/graphs.py` and `src/rules/four_graphs.py` were both live implementations of the same four families, neither importing the other. The audit recommended keeping the world model and making the rules module its authoring layer. Done.

**Deleted:** `src/rules/four_graphs.py`, and `tests/test_four_graphs_1178.py` — its behavioural coverage was already in `tests/test_world_graphs_1178.py`. **Ported:** `graph_authoring.py` and `graph_text_bridge.py` now compile and project into `WorldGraphs` / `PhysicalGraph`; `tools/graph_authoring.py` keeps `--check`, `--json`, `--example`, and its snapshot format is `noopunk.world.graphs` v1.

### Two things the merge would have silently dropped, so I moved them instead

1. **`Action` is now enforced by the runtime model.** `SCENE_TYPES` lives in `src/world/graphs.py`, and `StoryNode` refuses `Combat` with a message that explains why (#1184). Matching is case-insensitive because authored data already says `social`.
2. **"An actor is never a node"** — the correction §5 of this issue is actually about. `PhysicalGraph` now refuses an occupant id that is also a location; `CyberGraph` refuses an avatar id that is also a device. The old rules model enforced this, the world model did not, and merging naively would have lost precisely the invariant you flagged.

Both are covered by negative tests, not just prose.

**Verified:** `Ran 2673 tests … OK (skipped=3)`; `rules_constitution_audit` OK (131 modules, one tier each); `check_engine_boundary` 0 violations; ruff clean; CWN matrix regenerated because the test inventory changed.

### Still open, and untouched by this PR

The **later list** in §6 is not started: PC Telepathy/Telekinesis-only enforcement, the SWN **Psychic Training Focus** (paraphrase is the requirement, the book is the wording — confirmed against `docs/licenses/`), the AWN **Mutant** Edge with its mutation/Stigma paths, AWN **Mentalist**, CWN **Spellcaster/Summoner**, and the psychotronic-device contract. The **Astral Graph** stays deferred with `astral.py` as a prototype.

And the decision I flagged earlier is still pending from you: **#1137's psionics draft and #1174's rookie build both grant the PC "Psychic Defence"**, which is not a SWN discipline. Under §1 it has to become a psychotronic-implant property or a scripted event before either draft is touched again, or the next agent will implement it as a player power and call it canon.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

Follow-up fix opened in #1193: the PSI access layer previously rejected selecting both Telepathy and Telekinesis even for a full Psychic. The new patch allows both approved disciplines for a full Psychic while preserving a Partial Psychic's single-discipline restriction, with tests and documentation updates. Does not implement printed Focus mechanics or the deferred Astral/Mutant/Edge systems. **Keep #1178 open** for those remaining tasks.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

2026-11-05 CWN-first simplification: see PR #1194. Existing `src/world/graphs.py` already provides Physical, Cyber, Social and Story; Astral remains deferred. PR #1194 adds lightweight Social/Goal/Clue/Personality tag interface and five-scene action routing to canonical CWN/investigation authorities. Data Collection (OSINT, Panopticon, HUMINT) and Data Analysis are Investigation modes; Interrogation is Social+Investigation, without emotion mechanics. This is a partial implementation only: console/Evennia/GUI dispatch-to-resolver integration and end-to-end playable case tests are still pending. Do not revive WWN or the five-graph Astral engine from older issues.

---

## Follow-up in the same thread (2026-11-05)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## Closing — the acceptance criterion is met, and the deferred work now has its own home

> *"the four currently scoped graph families are testable and playable independently of an Astral Graph."*

Verified on `main` at `4fdfb35e`: **2690 tests OK (skipped=3)**.

### "Implement now" — every box, with its evidence

| Box | Where |
| --- | --- |
| Audit for agent-as-node assumptions | `docs/design/FOUR_GRAPH_IMPLEMENTATION_1178.md` § *Node-semantics audit* — the Astral draft's `node_type: agent` was the one real instance; it is superseded, and the author's "character traveling" shorthand is recorded as occupancy |
| Physical location graph | `src/world/graphs.py`; `tests/test_world_graphs_1178.py::test_characters_meet_only_when_they_occupy_the_same_location`, co-location, one-route movement, one-way routes |
| Cyber device/network graph | same file; `test_devices_at_a_physical_location_are_the_same_devices_an_avatar_visits`, `test_avatar_moves_through_network_edges_without_moving_the_body` |
| Social character/faction graph, −4…+4 | `test_nodes_are_characters_or_factions_and_scores_are_signed`, `test_relationships_are_directed_and_replaceable`, `test_social_nodes_are_not_spatial_routes` |
| Series → Episode → Scene, prerequisites, scene types | `test_hierarchy_is_series_episode_scene`, `test_scene_entry_respects_prerequisites_and_transition_condition`, `test_episode_transition_requires_its_flag` |
| Stable IDs, author formats, validation, serialization | `tools/graph_authoring.py` (Markdown/YAML frontmatter), `tests/test_graph_authoring_1178.py`, versioned JSON roundtrips in all four families, cross-reference validation (`test_cyber_device_must_reference_a_real_physical_location`) |
| The seven named behaviour tests | all seven exist — see the names above plus `test_social_ties_survive_physical_travel` and `test_avatar_movement_does_not_move_the_operator_body` |
| Astral compatibility without Astral implementation | Astral nodes are documented as locations with occupants; no Astral graph exists in the code |

**New in #1195:** the paper half. `docs/tabletop/WORLD_GRAPHS_1178.md` lets a table run the model with
index cards in ten minutes — including the check software most often fails, *one actor, one sheet,
across all views*.

### One correction worth naming

The implementation doc still carried a stale paragraph saying the AWN Mutant Edge "becomes a
human–alien Hybrid Edge" and required a selected plus a rolled positive mutation. #1178 §3 supersedes
exactly that, so the doc now says what the issue says: **Mutant** is the broad category, **Hybrid** is
one possible origin, the mandatory Hybrid-only packages are withdrawn, mutation proves neither ancestry
nor PSI, and the Edge is NPC-only.

### Deferred work, carried rather than dropped

[#1196](https://github.com/TomiToivio/NooPunk/issues/1196) carries the "Later" list: the Astral Graph
(only when a scripted scene needs navigation), AWN Mutant templates after the edition check, Mentalist /
Spellcaster / Summoner integration with prerequisites, device-granted psionic effects, the SWN Psychic
Training Focus itself, and runtime wiring of the graphs into console/Evennia.

`src/rules/psi_access.py` (#1191) already enforces who may choose what; the Focus's own accounting is
explicitly listed as not implemented, rather than implied to be done.
