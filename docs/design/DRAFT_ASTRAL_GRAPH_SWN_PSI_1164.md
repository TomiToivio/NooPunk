# SWN Psionics tweaks and Astral Graph: playable subsystem specification (#1164)

> **Superseded on graph nodes and player-selectable projection by [#1178](https://github.com/TomiToivio/NooPunk/issues/1178).**
> Astral nodes are locations/occupants, not conscious-agent nodes; Astral Projection is scripted
> (sleeping OOBE, NDE, Monroe-style technology), and the Astral Graph is deferred. This file remains
> the historical proposal for the PSI slice.

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED (2026-11-05).** This is a focused, actionable complement to [the five-graph design](DRAFT_GRAPH_SCENES_1164.md), [the prior PSI proposal](DRAFT_NOOPUNK_PSIONICS.md), [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md), and the author's unchanged [Graph Rules](../../design/graphs/RULES.md). **Design only**: no changes to CWN, Python, live game rules, or the author documents. All numerical thresholds marked *provisional* need author approval and playtesting.

## 0. Where the proposal was
The larger graph implementation draft already exists in `docs/design/DRAFT_GRAPH_SCENES_1164.md` (§§4.3, 7–9 and examples B/C). The core Psionics proposal exists in `docs/design/DRAFT_NOOPUNK_PSIONICS.md`. They were easy to miss because the Astral mechanic was divided between two files. This document makes the **Astral/PSI slice independently reviewable**; where another draft disagrees, record the choice for Tomi instead of silently changing approved canon.

## 1. Source rules and modification boundary

| Component | Keep / tweak |
|---|---|
| CWN (immutable) | Skills, saves, initiative, combat actions, damage, equipment, System Strain, hacking permissions and programs unchanged. No new generic PSI roll. |
| SWN Revised psychic | **Preferred baseline:** six disciplines, psychic rank/eligibility, one Effort-accounting engine, commitment and Torching **as implemented** in `src/rules/swn_psionics.py`. Refer to SWN Revised pp. 29–43 and verify editions for actual technique effects and costs. |
| AWN Deluxe Mentalist | Compare as a **balance reference**, especially bounded perception, defence and psychokinesis; do not stack a second Mentalist class, Effort pool or free Arts. |
| WWN magic | Reinterpret particular **author-approved** rituals/Workings as PSI practices when the story calls for them, one cost and one resolver per action; no separate spell-point track. |
| NoöPunk additions | Astral projection modes, graph topology, anchored return, access/consent/visibility, cross-layer link contracts, psychotronics as equipment. |

Existing `src/rules/swn_psionics.py` defines `Psychic`, six disciplines (`Biopsionics, Metapsionics, Precognition, Telekinesis, Telepathy, Teleportation`), Effort reservations for active/scene/day, Torching and snapshots. **Do not replace this.** The present rules do not inherently expose a seventh `Astral Projection` discipline: propose **a named NoöPunk technique/pathway gated by permission** (most plausibly Metapsionics/Teleportation or a *specific* campaign unlock), rather than introducing a free seventh rank. Select one mapping after verifying the source techniques. Source effects do not become official just because an analogy sounds plausible.

## 2. Conscious Agent Network is graph topology, not omnipotent hacking

The **Astral Graph** is a directed, attributed multigraph over *persistent conscious agents, anchors, realms, symbolic sites, boundaries, and noetic links*. Nonlocality is a fictional in-universe relation, **not** arbitrary reach: distance is not the principal gate, but a traversable/attuned **edge** must exist. Physical line of sight may propose a *temporary weak link* only for explicitly allowed verbs; seeing a camera does not confer remote physical or Cyber control. A density value describes an in-fiction category of consciousness, **never position or physical dimensionality**.

**Observe → Experience → Act** is the narrative sequence of any PSI activation:
1. **Observe:** resolve visibility and attunement/target access; a detected signal is not a guaranteed true proposition.
2. **Experience:** surface qualia and distortions as GM description/tags, not an additional mandatory roll or automatic core clue.
3. **Act:** check **one approved ability contract**, published/CWN action economy, one eligible Effort commitment/resource, resistance, target awareness and consequences. If there is no matching contract, action is **DENIED**.

Nodes **reference**, never clone, canonical character/physical/cyber entities. A character's HP, goals, equipment, identity and consent have a single owner. Graph edges are authored possibilities, not permission to ignore character privacy or NPC agency.

## 3. Astral record schemas (proposal, author-editable)

Minimal typed contract, to be imported from Markdown/YAML rather than hand-writing NetworkX:

```yaml
graph_id: astral.helsinki.01
graph_type: astral
version: 1
author_status: draft
nodes:
  - node_id: astral.anchor.europol_clinic
    node_type: anchor                   # agent|anchor|realm|symbolic_site|boundary
    label: Clinic's blue threshold
    physical_ref: physical.helsinki.europol_clinic
    visibility: GM_secret              # public|discovered|GM_secret
    modes: [overlay, projected]
    tags: [stable_anchor]
  - node_id: astral.site.platform_echo
    node_type: symbolic_site
    label: Platform that remembers tomorrow
    visibility: GM_secret
    tags: [symbolic, unstable]
edges:
  - edge_id: astral.route.clinic_platform
    source: astral.anchor.europol_clinic
    target: astral.site.platform_echo
    relation: projection_route         # projection_route|attunement|contact|boundary
    directed: true
    access_condition: act3_projection_unlock
    required_link: clinic_guided
    disclosure: GM_secret
    resistance_ref: null
    reverse_edge_ref: astral.route.platform_clinic
```

Additional optional node fields: `character_ref`, `cyber_ref`, `seity_ref`, `density`, `consciousness`, `identity`, `agency`, `qualia_tags`, `anchor_state`, `legal_access`, `source_claim`. Edge fields: `effect_permission_ids`, `visibility_condition`, `travel_cost`, `return_condition`, `consequences`, `provenance`. Every required reference must resolve; GM-secret nodes never appear in player exports merely because NetworkX has loaded them.

**Cardinalities:** one active physical body anchor per embodied/projected player at a time; a projection references exactly one current astral site, zero or more **discovered** routes, and exactly one current return policy; multiple attunement edges may link the same agents for different purposes. `cross_layer_link` is a separate explicit record, never inferred from similar names.

## 4. Four presence modes and projection state machine

| Mode | Physical participation | Astral participation | Permitted changes |
|---|---|---|---|
| `embodied` | CWN normal | latent only | Ordinary action; defensive implant may respond via approved contract. |
| `overlay` | CWN normal | AR-like bounded perception | One CWN action at a time; no free second astral action or access to hidden memories. |
| `projected` | Body remains at anchor, vulnerable normally | VR-like site traversal, negotiation, perception | No simultaneous embodied physical actions; explicit cross-layer effect required. |
| `manifesting` | Exceptional physical influence | Astral agency remains primary | Late authored technique only; exact effect, defence, limit, visibility and cost required. |

Transitions: `embodied -> overlay` (perception unlock), `embodied/overlay -> projected` (controlled projection permission, stable body anchor, valid entry route, Effort/cost commitment), `projected -> embodied` (return path/trigger, release according to the specified Effort duration), and `projected -> manifesting` only when a rare permission is explicitly granted. Involuntary dreams may show astral *content* without authorizing player-controlled transitions. **The body persists:** discovery, relocation, injury, alarms and rescue remain ordinary Physical scene facts.

`ProjectionState` minimum: `character_ref,mode,physical_anchor_ref,current_astral_node_ref,entry_event_id,route_history,effort_reservation_id,link_strain,return_policy,visibility_scope,scene_id`. Must serialize/replay exactly; never create a second avatar with its own HP or turns.

**Anchored-return mini-rule to review:** a *provisional* 3-box `link_strain` clock, filled by authored interference or overextended scene duration. This is a **navigation/fiction clock**, NOT a replacement Effort pool or additional cost for every PSI activation. At three boxes the player enters a bounded **lost-path scene** with rescue/return alternatives, not permanent imprisonment or automatic death. Existing [Psionics draft](DRAFT_NOOPUNK_PSIONICS.md) proposes a quantified difficulty; **do not activate it before CWN check arbitration and author approval**. At least one recoverable exit is required for every authored scene.

## 5. Small Verb × Target *permission* system

Tentative verbs: `Perceive, Contact, Shield, Project, Influence, Imprint/Modulate, Ritualize, Manifest`. All pairings default **DENIED** without named technique permissions. Example initial whitelist:

| Verb | Target | First playable contract | Explicitly excluded |
|---|---|---|---|
| Shield | self | Europol defensive implant, reactive specified hostile PSI event | Perfect passive immunity; psychic detection of all lies |
| Contact | willing conscious person | Later bounded Telepathy, a short deliberate exchange | Secret mind extraction; involuntary truth reading |
| Perceive | accessible astral site | Later overlay or anchored site view | Hidden investigation core clue or arbitrary classified area |
| Project | known astral route/site | Later controlled entry + safe return | Free projection to any global location |
| Shield | linked ally | Later author-approved extension with range/link and cost | Automatic group shield |
| Imprint/Modulate | inert physical object | Late, specifically named psychokinetic technique, physical effect prewritten | Universal edit/delete of matter or limitless telekinesis |
| Imprint/Modulate | Cyber device | **No default access**; future QIP physical interface/approved operation ONLY | Bypassing CWN hacking credentials, security and action costs |
| Ritualize | anchored symbolic site/group | Specific time-consuming WWN-inspired undertaking | Free prepared spells with a second mana pool |
| Manifest | physical target | Scripted/high-tier explicit contract | Attacking anyone while untargetable |

Targets enumeration: `self, conscious_person, living_biologic, inert_object, construct_device, cyber_node, astral_agent, astral_region, group_link`. **No automatic bonus against 1st/2nd/3rd density**; density may gate affinity/visibility only when a technique says so. Fifth-density StS entities may have stronger authored access/defence but are not infinitely powerful and cannot steal PC agency by decree.

Every allowed `PsiEffect` must state:
```yaml
effect_id: psi.defence.europol_shield
verb: Shield
target_types: [self]
source_system: noopunk_swn_derived
unlock: starting_europol_device
actor_mode: [embodied, overlay]
target_visibility: self
link_basis: self_identity
action_type: REQUIRES_RULES_VERIFICATION # must use CWN action economy
resource_owner: psychic_effort          # or approved device-only charge, never both
cost_ref: SWN_SOURCE_VERIFICATION_REQUIRED
duration_ref: SWN_SOURCE_VERIFICATION_REQUIRED
resistance_ref: hostile_psi_contract
effect: defend_one_named_intrusion
physical_effect: none
cyber_effect: none
investigation_effect: none
knowledge_to_target: technique_specific
failure_consequences: [shield_exposed]
```
The example is **a schema, not a claim that SWN prices or supports this exact power**. Cross-layer links also specify `physical_ref/cyber_ref, access, defence, action, effect, logging`. An explicit cross-layer route is required **even if** an astral agent can perceive a device.

## 6. Cross-layer resolution: no free extra turns

1. One actor, one CWN time/action budget. Astral overlay, implant interface and cyber avatar are *views*, not three turn owners.
2. An astral perception of a physical target conveys only the effect's described information. The normal investigation module still adjudicates lawful access, inquiry, evidence, provenance and indispensable clues.
3. A hostile agent defending against PSI uses its documented defensive contract and ordinary CWN/SWN saves when applicable; the graph score is not a substitute for a save.
4. For Physical/Cyber effects, require a **specific cross-layer bridge**: explicit verb and target type, material interface or attunement, permitted range, cost, defence, activation timing, detection and audit trail. No bridge = no effect.
5. **CWN Hacking stays CWN Hacking.** A QIP-assisted hacker might use a named later technique to identify a *permitted* interface or mitigate a narrowly written obstacle; the subsequent Cyber intrusion still obeys CWN access/program/security mechanics. Astral PSI cannot simply `root` a camera.
6. No extra automatic psychic damage on an ordinary attack. An astral-to-physical attack requires a rare permitted effect and uses ordinary action/save/damage adjudication with a single explicit outcome.

## 7. Psychotronics and awakened power progression

Natural PSI belongs to conscious people; a QIP implant **enables or amplifies** a bounded technique when operated by a conscious person. Ordinary BCI software, recording and neural stimulation do not become PSI by rebranding. Track `operator_ref,ownership,calibration,licence,device_state,privacy_record,enabled_effect_id`. A malfunction may affect access or reliability but never automatically edit the psychic character's identity.

**Campaign gate proposal:** Act I Europol rookie begins with BCI plus a limited reactive defensive implant only; an early dream/flashback can reveal a GM-truth fourth-density status but does not grant player-facing broad psychic powers. Later natural Telepathy/Defence and astral overlay unlock in authored story beats; first controlled projection is tentatively Act III; Higher Self/Wanderer revelations and stronger techniques late; pre-incarnate mission is finale-only. These act numbers are *proposals* pending campaign-author review, not retroactive canon.

**One effect, one payer:** reuse the existing SWN `Psychic` Effort reservation for natural psychic activations. If the design intentionally chooses a device-only cost for one implant defence, define a **mutually exclusive** payment alternative, not Effort + strain + a separate chakra pool. CWN implant installation/System Strain constraints remain applicable where the published rules require them; do not confuse installation costs with per-activation resource charging.

## 8. Three tabletop/engine acceptance examples

**A. Rookie at Kurvi (Act I, overlay denied).** A Europol BCI delivers a mundane authorized sensor feed. A suspected PSI contact triggers the issued defence's **one named response**; no telepathy, projection or remote clue discovery is available. Player is free to use CWN Notice/Know/Program and existing investigation facilities. A false positive leaves a diagnostic tag, not a supernatural clue.

**B. Guided Helsinki clinic projection (later, author-approved unlock).** The agent starts on the clinic's Physical node, declares the prepared anchor, commits exactly one published/approved Effort reservation, enters `astral.anchor.europol_clinic`, follows the visible authorized `projection_route` to `astral.site.platform_echo`, interacts with a consent-capable guide, meets an astral boundary, and safely returns. A failed optional interpretation changes risk or detail but **does not delete the authored indispensable memory**. Body never vanishes from the clinic.

**C. Dual-layer combat + Cyber (late).** In a single CWN round, the PC may take an allowed shield response **only at its specified timing**, or their normal hacking action, or a legal PSI attack; they get **no extra action** merely by having three graph overlays. A hostile 5D contact and a compromised drone have distinct astral and Cyber resistances. Without an explicitly authored QIP-to-drone bridge, the PSI targeting of the drone fails at the permission gate, before any dice.

## 9. Validator and tabletop tests (future implementation; no code in this issue)

- Every node/edge has stable namespaced IDs, valid refs, permitted type, version and visibility; player views redact `GM_secret` content.
- `projected` implies exactly one physical anchor, one astral current node and a return/recovery policy; all transitions preserve one actor/HP/turn.
- Every allowed verb×target pairing has full cost/action/defence/link/detection/knowledge specification; unspecified pairings are rejected.
- A cyber or physical side effect with no explicit bridge is rejected; no bypass of CWN hacking.
- Resource commitment is single-payer, lifecycle-correct, serializable, and replays with identical results.
- No PSI import or clue injection into `src/rules/investigation.py`; core clues remain accessible by valid inquiry regardless of optional check failure.
- A third-density target is not automatically mind-readable; target consent/free will and resistance remain meaningful.
- Gold tests for Act I denial, guided projection/return, hostile contact/defence, cross-layer denial, and three-view single-turn combat.
- A tabletop GM can run all three examples **without a Python engine**, using CWN plus one explicit PSI effect card.

## 10. Author decisions before any rules/code implementation

1. Is Astral Projection a Metapsionics/Teleportation-gated **technique**, a narratively granted permission, or a distinct (costed) discipline? **Recommend technique/permission, no seventh Effort rank.**
2. Confirm the **single resource owner** (SWN Effort) and reconcile optional device-only use with the existing draft's alternative tag/condition costs.
3. Confirm the **return/link-strain clock** or remove it entirely in favor of authored scene tags.
4. Decide earliest controlled projection, overlay, consent-limited Telepathy and advanced manifestations. Keep Act I rookie grounded.
5. Which **specific** WWN-style ritual, if any, is needed in the first campaign? Avoid implementing a general spell catalogue until a scene requires it.
6. Should limited QIP-assisted Cyber effects exist at all? If yes, specify exactly one effect and retain full CWN hacking.
7. Confirm schema naming and whether this focused document should be merged into `DRAFT_GRAPH_SCENES_1164.md` after review.

**Status:** design complete enough for author review, **not approved or implemented**. Keep #1164 **OPEN** until Tomi explicitly approves and requests the implementation phase.
