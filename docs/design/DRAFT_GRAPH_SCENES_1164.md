# NoöPunk Graph Rules and Scene Authoring: implementation proposal (#1164)

> **Partially superseded by [#1178](https://github.com/TomiToivio/NooPunk/issues/1178) (2026-11-05).**
> Physical and Astral nodes are **locations**, not conscious agents; the Astral graph is deferred
> until scripted Astral Projection needs it. The current implementation is
> [`docs/rules/WORLD_GRAPHS_1178.md`](../rules/WORLD_GRAPHS_1178.md). This file remains the historical
> design record and is not current schema authority.

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** 2026-11-05.
> **Scope:** architecture, five typed graph schemas, six scene types, three worked scenes and a Markdown/YAML authoring format. **This document changes no published CWN mechanics, game engine, tabletop rulebook, or user-authored graph README.** It does not authorize implementation.
> **Authority:** [author's five-graph design](../../design/graphs/README.md) → [CWN baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md) → canonical [Europol campaign](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md). Related unapproved drafts: [Psionics](DRAFT_NOOPUNK_PSIONICS.md), [Character Tags](DRAFT_NOOPUNK_CHARACTER_TAGS.md), [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md).
> **Labels:** **[AUTHOR]** explicit author intent; **[EXISTING]** current repository capability; **[PROPOSAL]** design subject to editing; **[FICTION]** NoöPunk's in-universe ontology, not established physics; **[OPEN]** author decision. **GM_SECRET** must never leak to player interfaces.

## 1. Decision summary

**Five graphs are separate views of one persistent world.** Each node has a stable ID and references canonical records; an actor never gets independent HP, inventory or memories because it appears on three graphs. Scenes compose graph references and select **one governing CWN action economy**. NetworkX is the **derived in-memory representation** of small author-written Markdown/YAML records, not a requirement that Tomi write Python or serialized NetworkX objects.

| Graph / purpose | Edges | Vanilla CWN or mod | Status |
|---|---|---|---|
| **Physical**, world→city→district→location→room | traversable routes, doors, nested maps | CWN movement, exploration, skills, combat, gear | [PROPOSAL] adapter |
| **Cyber**, machines and services | network routes, access rights, control | CWN Hacking and existing communications, no new hack dice | [PROPOSAL] adapter |
| **Astral**, conscious agents and symbolic realms | noetic links, bounded projection routes | selected SWN Psi/Effort + authored Astral mod; WWN ritual only when needed | [PROPOSAL] future optional mod |
| **Social**, characters and campaign-local factions | directed relationship, trust/ideology/goal ties | CWN Talk/Connect/Lead/other verified checks + personality/goal/reputation tags | [PROPOSAL] adapter |
| **Story**, Series→Episodes→Scenes | prerequisite/branch transitions | existing GoalLog and scene flags, no second XP engine | [PROPOSAL] adapter |

**Six scene kinds:** Exploration, Cyber, Action, Social, Investigation and Astral. ("Action" replaced "Combat" in #1184: a Finnish police scene is an arrest, a pursuit or a forced entry, and the name should not promise a firefight.) `scene.types` can hold several. A Cyber scene is *not* the Cyber graph itself; a Combat scene may refer to all three spatial layers. **A graph is persistent topology; a scene is an episode of play referencing parts of topology.**

**Recommended build order after separate approval:** physical & cyber views → story/goal link → social relationship view → investigation metadata adapter → bounded Astral + explicit cross-layer permissions. Do not implement all at once, or delay playable Act I until Astral is complete.

## 2. Source/code audit: reuse, do not duplicate

| Existing file | Read finding and implication |
|---|---|
| `design/graphs/README.md` | [AUTHOR] declares exactly **Physical, Cyber, Astral, Social and Story**, −4...+4 social relations, Physical World/City/Location scales and Series→Episodes→Scenes. Keep this document **unaltered**. |
| `src/rules/investigation.py` | [EXISTING] `Clue`, `Scene`, `Case`, `Investigator`, `discover`, `CaseGraph`, `load_case_graph`. Core clues are acquired through competency plus declared access/inquiry **without a discovery roll**; interpretation is the player's, action risk uses CWN. New Lead/Evidence/Capability tags must be **metadata/adapters**, not a new `discover` implementation. |
| `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md` | [EXISTING] regression boundary and tests: don't add psychic parameters/imports to the investigation resolver; no PSI auto-clues or exits. |
| `src/rules/goals.py` | [EXISTING] `Goal`, `Progress`, `Award`, `GoalLog`, `record_progress`, `award_xp`, `paper_line`; **already has horizons short/medium/long** and anti-farming event keys. Therefore **do not propose adding a second Goal class or a horizon field**. Scene/Episode/Series are **references and editorial conventions** to the existing goal horizon, not schema migration. |
| `src/rules/tags.py`, `src/rules/noopunk_tags.py` | [EXISTING, LEGACY/PROTOTYPE] parts still document an old d10 / alternative tag-stat chassis. **Do not call these universal CWN-canonical tag resolvers** or connect their old roll formulas to new scenes. Add simple metadata tags alongside CWN; consider a very small adapter only after review. |
| `src/rules/swn_psionics.py`, `src/rules/psionics.py` | [EXISTING] SWN-inspired Effort commitments, psychic authorization and provisional techniques; no source-complete published power catalogue. **Reuse authorization/Effort** for one new approved Astral effect rather than inventing parallel PSI accounting. |
| `docs/design/ISSUE_704_GUMSHOE_INVESTIGATION.md` | [EXISTING] earlier GUMSHOE-lite draft and crosswalk; use its principles but check up-to-date engine instead of creating a competing investigation module. |
| `docs/design/ISSUE_220_SOCIAL_PROCEDURES.md` | [EXISTING PROTOTYPE] social consequences should not rewrite beliefs/motivations; older rule-version artifacts may not be CWN authoritative. |
| `legacy/ubiquitous_maniacs/src/{physical,cyber,noetic,social}/graph.py` and `graph_serialization.py` | [LEGACY] examples of NetworkX types and persistence only. **Audit compatibility before any reuse**. Not the primary MUD/engine-neutral implementation. |
| `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` and `docs/world/EUROPOL_HELSINKI_1114.md` | [CANON/author draft] rookie Europol officer, **Kurvi** corporate housing, standard BCI + defensive implant; Europol coordinates, Finnish authorities wield arrests/searches. Older graph README Sörnäinen home/Ratakatu HQ are legacy or unresolved location claims. Don't silently relocate the character. |

**Rule source target verification:** *Cities Without Number* (2023) for normal skills/combat/exploration/hacking; *Stars Without Number Revised* for Psychic Effort; *Worlds Without Number* for rare rituals/Workings; *Ashes Without Number Deluxe* for bounded Mentalist design comparison. Confirm printed section/edition and exact program/technique timing against authorized books **before implementing**. This draft never sets unverified numeric costs.

## 3. Shared graph and cross-layer data contract

**[PROPOSAL] One canonical ID per thing, several typed projections.** Define `EntityRegistry` for identities and a `GraphProjection` for per-layer presence. Nodes may be **sites**, **entities**, **factions**, **devices**, **narrative scenes** or **conceptual links**; canonical actor state is stored once.

```yaml
# SCHEMA SKETCH, not live implementation or source-of-truth data
graph:
  id: helsinki.physical
  kind: physical             # physical | cyber | astral | social | story
  version: 1
  source_doc: design/graphs/README.md
nodes:
  - id: physical.kurvi.home
    canonical_ref: location.kurvi.home
    node_type: room
    visibility: player       # player | discovered | gm_secret
    tags: [housing]
    coordinates: null       # optional; no invented tunnel coordinates
edges:
  - id: route.home.to.street
    from: physical.kurvi.home
    to: physical.kurvi.street
    type: traverse
    directed: false
    access: resident
    cost: cwn_travel         # descriptive resolver reference, not invented stat
```

**Validation:** `graph.kind` one of five; IDs unique within a namespace; references exist; route endpoints are valid; bidirectional physical passage explicitly stated; no duplicate physical actors; relationship scores integers −4..+4; story edges have resolvable flags and no impossible mandatory-only cycles; every secret projection has explicit gate; every **cross-layer** link has a named permission and typed effect. No graph drawing dependency.

### 3.1 Cross-layer link (must be explicit)

```yaml
id: cross.kurvi.cam.to.terminal
from: cyber.kurvi.camera
to: physical.kurvi.street
relation: observe_video       # observe_video | control_device | astral_perceive | psi_affect | manifest
requires:
  abilities: [cwn_hacking_authorized_device_access]
  gate: camera_powered
effect:
  type: provide_sensory_feed
  does_not_grant: [core_clue, physical_lock_bypass, auto_telepathy]
visibility: discovered
cost_ref: published_cwn_hacking_procedure
```

A Cyber camera can provide authorized footage of a physical corridor; it does not automatically grant access to the corridor, thoughts of an occupant or hidden astral beings. A projected astral agent's symbolic impression of a camera does not automatically confer firmware control. Cross-layer PSI must cite an approved **verb + target** effect and satisfy action, cost, resistance and gate contracts.

## 4. Five graph schemas

### 4.1 Physical graph

`PhysicalNode{id,canonical_ref,scale:world|city|district|location|room,node_type,parent_id?,coordinates?,terrain?,access?,legal_authority?,encounter_refs[],cyber_refs[],astral_refs[],visibility}`.
`PhysicalEdge{id,from,to,route_type:street|door|passage|transport|tunnel,access,travel_ref,blocked_by?,directed?,visibility}`.

**Example:** `physical.kurvi.home` and `physical.kurvi.street` connected by an ordinary exit; `physical.europol.office` requires professional credentials. World graph may remain unloaded in Act I. Genuine Helsinki tunnels require evidence of existence and access; future fictional tunnels must be visibly marked.

**CWN:** unmodified travel, Notice, Exert, Sneak and combat; checks for uncertainty and stakes, not every walk to the shop. No new grids.

### 4.2 Cyber graph

`CyberNode{id,canonical_ref,type:device|network|service|account|data|security,owner,network_ref?,credential_scope?,cwn_hacking_ref,security_state?,visibility}`.
`CyberEdge{id,from,to,type:linked|trusted|data_flow|control,access_level,requires,traceability?,effect_ref?}`.

**Example:** `cyber.europol.bci` → secure `cyber.europol.case_service` with valid duty-bound credential. A compromised service may alter information, not CWN physical HP directly. Hacking uses published CWN Programs and security rules; no new percentile intrusion test.

### 4.3 Astral graph

`AstralNode{id,canonical_ref?,type:agent|anchor|realm|symbolic_site|boundary|noetic_link,density?,consciousness?,identity?,agency?,qualia_tags[],realm_state?,projection_gate?,physical_refs[],cyber_refs[],visibility}`.
`AstralEdge{id,from,to,type:attunement|projection_route|consented_contact|intrusion_attempt|return_to_anchor,entanglement_basis,verb_required,defence_ref?,cost_ref?,visibility}`.

**State machine [PROPOSAL]:** `embodied` → `overlay` (limited astral sensing while in Physical) → `projected` (disembodied Seity anchored to body) → `returned`; `manifesting` is separate rare ability, not automatically implied by projection. In overlay, the **same actor** observes two layers but still has one CWN turn. In projection, the physical body stays on its node and remains vulnerable; body and projected perspective share the same canonical actor state. Return to explicit anchor or approved fallback.

**Example:** a dream-symbol `astral.kurvi.echo` exists GM-only in Act I. It is **not** an Act I playable route. It becomes visible only after the applicable scripted dream or awakened projection milestone. Third-density dreams/NDEs may include involuntary projection in fiction, not unrestricted travel.

### 4.4 Social graph

`SocialNode{id,canonical_ref,type:person|faction,goal_refs[],personality_tags[],ideology_tags[],reputation_refs[],visibility}`.
`SocialEdge{id,from,to,relationship:-4..4,kind:friendship|hostility|trust|allegiance|professional|family|other,directed:true,known_to[],source_event,goals_in_common[],goal_conflicts[],visibility}`.

**Example:** the rookie `actor.rookie` → `actor.liaison` has `relationship=+1` after lawfully protecting evidence; the reverse edge may be `0` or absent. `unknown` ≠ known-neutral `0`. Relationship ≠ **faction reputation**; neither equals SWN Force/Cunning/Wealth, moral polarity or character ability score. Reputation may use its own author-proposed −4..+4 scale (stored on the reputation record, not overwritten on the relationship edge).

**Goals matter** because two agents may support the same civic reform while disliking one another, or love one another while prioritizing competing factions. Model `ideology_tags` descriptively as recurring discourse identities/coalitions, never automatic political persuasion. CWN Talk/Connect/Lead and suitable social actions stay authoritative.

### 4.5 Story graphs: Series → Episode → Scene

**Existing GoalLog supports `short|medium|long` already.** Attach `goal_id` references; do not create a second goal class or second XP reward path.

`Series{id,episode_refs[],long_goal_ids[],required_finale?,visibility}`.
`Episode{id,series_id,scene_refs[],entry_flags[],medium_goal_ids[],exit_conditions[],alternative_episode_ids[]}`.
`Scene{id,episode_id,types:[investigation|exploration|combat|social|cyber|astral],physical_refs[],cyber_refs[],astral_refs[],social_refs[],participants[],short_goal_ids[],lead_ids[],evidence_ids[],entry_flags[],transitions[],outcomes[],spoiler_gate}`.
`StoryEdge{from,to,condition,priority?,fallback?,effects[],disclosure_policy}`.

**Illustrative progress:** short goal `file the invoice case` closes in an episode or a scene; medium `earn colleagues' trust` develops across several episodes; long `serve humanity` continues across Series and may never be marked complete. Those names refer to existing `Goal` IDs; each event is only awarded once according to existing goals logic. Mandatory truths have redundant paths and are never gated by one failed die roll.

## 5. Vanilla CWN scene rules and non-CWN extensions

| Scene type | Input graph(s) | Core action | Minimal extra record |
|---|---|---|---|
| **Exploration** | Physical (+ optional Cyber view) | Move, locate, question, climb, examine, sneak using CWN | Map node access, scene gate, environmental tags |
| **Cyber** | Cyber (may link Physical) | Published CWN Hacking prerequisites, actions/programs, consequences | Security node refs and credential scope, no new hack skill |
| **Combat** | Physical; optional Cyber/Astral interactions | **Single CWN** initiative, attacks, saves, movement, injury, cover | Action-consuming typed cross-layer effects |
| **Social** | Social plus Physical co-presence | CWN social skills and negotiation; NPC agency retained | `relationship_delta`, personality, reputation, goal evidence |
| **Investigation** | Any accessible location/sensor node | Existing `discover` competence + access + inquiry; roll for risky action only | Lead/Evidence/Capability **descriptors**, chain-of-custody and optional hypothesis |
| **Astral** | Astral, possibly overlays Physical/Cyber | SWN-inspired Effort/permission + original bounded projection procedure | Anchor, route, verb, target, defenses, return gate |

**One shared turn:** if the PC fires a gun in the corridor, controls a turret via cyber, or uses psychic shielding, each requires its published or separately approved action timing. There is no free action in a second graph simply because the character sees that layer. If two agents operate separately, each spends its own CWN turn. A single effect cannot charge SWN Effort and a new Chakra pool unless a later author-approved conversion explicitly replaces the cost.

## 6. Investigation: Lead, Evidence and Capability as thin tags

### 6.1 Keep the existing resolver

**[EXISTING]** `src/rules/investigation.py` already separates (1) automatic discovery for competent, appropriately present/access-authorized inquiry, (2) player interpretation, and (3) CWN rolls for risky/contested action. `CaseGraph` already exists. **Do not invent a `GUMSHOECheck`, new point pool or psychic-discovery resolver.**

**[PROPOSAL] Metadata only:**
- `Lead{id,from_scene,to_scene_or_entity,description,source_evidence_id?,mandatory?,status:unknown|available|followed}`: actionable direction, not confirmed fact.
- `Evidence{id,scene_ref,description,provenance,capture_method,chain_of_custody,access,authenticity:unknown|contested|verified,interpretation_refs[]}`: an artifact or observation, not automatically proof of one theory.
- `InvestigationCapability{id,provider:academy|agent_skill|BCI_sensor|human_controller|AI_controller|lab,skill_ref?,service_ref?,permission,latency?,reliability?,limitations[]}`: **means of competent inquiry**, not extra statistics. Plug into existing `Investigator` competence/access/inquiry only through an explicit adapter after author approval.
- `EmotionCue{observed:guarded|fearful|agitated|calm|unknown,confidence:low|medium|high,source:human|sensor,consent_status}` is **optional**; avoid a second The Veil-like numeric emotion economy until scenarios require it.

**GUMSHOE contrast:** (A) special investigative skill tags duplicate current CWN skill and eligibility records; (B) academy `Work/Know/Notice/Administer/Connect` plus equipment/controller/lab access cover the same competency. **Recommend B**, and use Capability tags **only for delegated services or specialized tools** not already represented.

**[EXISTING] The GUMSHOE mapping is already written — and nothing consumes it.** `data/rules/gumshoe_investigative.json` (#932) maps **16 GUMSHOE investigative abilities** onto CWN skills, sourced from the GUMSHOE SRD (OGL):

| Kind | Abilities (CWN skill) |
|---|---|
| academic | Research (Know), Textual Analysis (Administer), History (Know), Law (Administer), Occultism (Know), Forensic Pathology (Heal), Biology (Heal) |
| technical | Cryptography (Program), Data Retrieval (Program), Evidence Collection (Notice), Ballistics (Fix), Chemistry (Fix) |
| interpersonal | Interrogation (Talk), Reassurance (Talk), Streetwise (Connect), Bureaucracy (Administer) |

A repository search finds **no module, test or tool** referencing the file. That settles the A-versus-B question with more than an argument: model A would re-derive a taxonomy that is already authored and sitting unused, spelled correctly (`Administer`, not "Administration"), and already mapped to the published skill list. **The work is to wire this file, not to write another one.** If a later phase needs `InvestigationCapability`, it should resolve `skill_ref` through this mapping rather than introduce new ability labels.

### 6.2 Europol academic versus practical specialities

| Task | Candidate CWN skill and context | Training/source |
|---|---|---|
| Preserve scene, chain of custody, field arrest-coordination | **Work (Europol Agent)** [author proposed specialization] or Administer for bureaucracy | Applied academy and on-the-job practice; exact Work specialization semantics verify from CWN Deluxe |
| Know EU criminal law, legal standards or intelligence doctrine | **Know (Law & Intelligence)** [recommended label] or **Know (Europol Studies)** [alternative] | Theoretical Europol Academy course; no new skill |
| Interpret X-Risk/PSI/NHI/AGI scientific report | Know with an appropriate theory specialty; possible existing expert/lab | Theory, not automatic supernatural knowledge |
| Analyze intelligence dataset | Know (analysis theory) vs Program (actual computational task) | Distinguish question from tool execution |
| Notice concealed physical evidence | Notice, with access and inquiry | Sensory competence |
| File forms, coordinate authorization and chain-of-custody administration | **Administer** (verify source name, not “Administration”) | Procedure |
| Interview and gain rapport | Talk, Connect, and possibly Lead when organizing others | Social approach, not a built-in “Convince” skill |
| Access file through hacked system | **CWN Hacking/Program** | No free access from an AI controller |

**Arbitration principle:** `Work` = a professional **doing** a police/intelligence task, `Know` = **explaining/interpreting underlying law, science or intelligence theory**. The same scene may grant a fact through either where supported; don't force two rolls for one mandatory clue. Specific CWN specialization grammar and exact skill list must be verified at implementation.

### 6.3 BCI, AI/human controller, labs and interviews

The rookie may request **authorized** remote analysis of BCI sensor feeds. `ControllerRequest{sensor_ref,question,consent_or_warrant,connectivity,provider,turnaround,analysis_result,evidence_ref}` represents assistance. A network outage, restricted clearance or tool uncertainty changes **time, risk and source reliability**; it never grants guaranteed omniscience. EU AI policy in the setting permits narrowly controlled human-in-the-loop systems, not an unsupervised rogue AGI oracle.

**Psychotronic empathy helmet:** an interview device may estimate physiological **emotional responses**, with calibration, false positives, privacy and consent. It does **not** provide a machine-verified lie verdict or compelled memory extraction. Interrogation stories can involve rights abuses as events to investigate, never provide operational instructions for coercion. Finnish police retain national enforcement powers; Europol may coordinate, not unilaterally arrest or search.

## 7. Astral as a conscious-agent-network: mechanics proposal

**[FICTION]** Adopt the author's metaphysical premise: a multilayer Conscious Agent Network underlying Physical/Cyber/Astral, in which consciousness is primary, natural PSI exists, and QIP Psychotronics amplifies (but does not originate) PSI for a conscious operator. Hoffman and Faggin's theoretical views are distinct and unverified as an empirical mechanism; Law of One serves fictional canonical metaphysics. Quantum physics does **not** demonstrate human mind-reading, quantum-based remote signalling or consciously editable wave functions.

### 7.1 Observe → Experience → Act

| Stage | What the player describes | What the rule needs |
|---|---|---|
| **Observe** | Focus on a present target, a consented mind link, or known astral route | Sensory/contact permission, target ID, gate; physical line-of-sight may count as *in-setting* attunement, not literal quantum entanglement |
| **Experience** | Perceive subjective qualia/meaning; may be distorted or symbolic | Fictional description and optional `Misread Symbol` tag; **not** another mandatory die roll |
| **Act** | Choose approved PSI Verb on eligible Target | One CWN-timed action; unlocked technique, one Effort resource, duration, range/anchor, resistance, consequences |

**Permission first**. In a contested interaction, target autonomy, its psychic defences and any link gates determine what is possible; a "higher consciousness" score cannot silently seize all targets. Consciousness/Identity/Agency are descriptive **axes**, not replacements for CWN STR/DEX/WIS/CHA etc.

### 7.2 Verb × Target permissions (draft; all unspecified cells DENIED)

Legend: **A** = proposed pre-authored active effect once unlocked; **S** = scripted or NPC-only; **D** = deny without separate authored rule. All A entries still need cost, source technique, limits and resistance checked.

| Verb → / Target ↓ | Self / anchor | Person | Animal / biologic | Inert matter | Cyber device/node | Astral agent/realm | Group link |
|---|---|---|---|---|---|---|---|
| **Perceive** | A | A bounded / consent | A bounded | A ordinary senses | A with granted interface | A after projection | S |
| **Contact** | A | A bounded telepathy | S | D | D unless named QIP interface | A with consent/defence | S |
| **Shield** | A | A when protecting named ally | S | D | A only named defensive hardware | A | S |
| **Project** | A enter/return | D | D | D | D | A travel known route | S |
| **Influence** | A self-regulation | S contested | S | D | D | S | S |
| **Imprint/Modulate** | D | S | S | S rare telekinesis | S rare PSI-assisted cyber effect | S | D |
| **Ritualize** | S | S | S | S | S | S | S |
| **Manifest** | S | D | D | S | S | S | S |

**Example permission record:**
```yaml
psi_permission:
  verb: shield
  target_types: [self, person]
  governing_source: swr_psionics_approved_technique_ref
  unlock_event: campaign.act2.awakening
  action_timing: verify_source
  cost_ref: verify_source
  connection: co_present_or_explicit_link
  resistance: approved_psi_defence
  effects: [mitigate_named_psychic_intrusion]
  grants_investigation_clue: false
  scripted_only: false
```
When targeting a Cyber node, **CWN hacking stays authoritative**. A special PSI-to-Cyber permission might, after author approval, help *detect* or *temporarily interfere* with one device, but may not automatically seize a network, bypass credentials or grant unlimited combat actions. Ordinary first-density machinery is **not** an unprotected free-control surface by default.

### 7.3 Astral projection: embodied, overlay, projected and manifesting

- **Embodied:** character in physical spacetime, normal CWN actions. Physical/Cyber may already be visible through BCI. No access to sealed astral zones.
- **Overlay:** partial Astral perception while embodied; observer remains vulnerable and has one CWN turn. May sense eligible noetic entities but cannot traverse as a disembodied Seity.
- **Projected:** Seity is phenomenally disembodied; the PC's **body anchor** persists at an actual Physical node. Permitted astral route and safe-return requirement mandatory. Directed action across Physical or Cyber requires a separately defined link/effect. Full projected experience is distinct from unrestricted reality editing.
- **Manifesting:** rare late authored ability allowing tightly defined physical consequences. Not an automatic extension of being projected.
- **Third-density dream/NDE:** [FICTION] some normal humans involuntarily project in dreams/NDEs; these are scripted scenes, not controllable PSI privileges.
- **Time/Space vs Space/Time:** different fictional experiential structures, **not** one coordinate tuple; density ≠ spatial geometry; Physical/Cyber/Astral ≠ 3rd/4th density.
- **Higher Self/reveals:** scripted information only. Precognition stays scripted for the rookie. Wanderer identity revealed in Act IV; precise pre-incarnation service disclosed only at the finale.

**Counterplay:** defensive Attunement, consent/intent boundaries, actor awareness, detection, psychotronic shields (require a conscious operator for QIP), severing a named connection, seeking a prepared safe room, retreat and returning to anchor. No free permanent trapped-in-astral state, infinite-range harassment, or standard third-density helplessness.

## 8. Scientific vocabulary, fictional interpretation and rule consequence

| Term | Established science / relevant theoretical status | NoöPunk [FICTION] | Proposed bounded game hook |
|---|---|---|---|
| **Nonlocality** | Quantum correlations can be nonlocal, but **do not enable controllable faster-than-light communication** | Some consciousness relations reach beyond ordinary distance | A **named** contact/attunement link and cost, not universal infinite-range targeting |
| **Entanglement** | Correlated quantum state; **looking at an object does not automatically entangle it** | In fiction, line-of-sight creates local noetic *addressability* | `link_basis=line_of_sight` or explicit trusted relationship; target still resists |
| **Superposition** | Linear combination of quantum amplitudes; coherence is fragile for macroscopic states | Several possible subjective interpretations/paths coexist until resolved | Symbolic `Unresolved Possibility` scene flag, not multiple free characters |
| **Wave-function collapse/measurement** | Interpretation-dependent quantum update; **no scientific consensus that human consciousness causes collapse** | Agent–agent encounters can participate in narrative realization | Contested success uses existing defences; neither agent edits physical history automatically |
| **It from Qubit** | Quantum-information-first conceptual programme, not validated conscious matter | Panpsychic quantum information precedes physical appearances | Distinguish experiential node, self-identifying agent and an autonomous choice-maker |
| **Waves vs particles** | Measurement context exhibits wave-like interference or localized detections; not switchable invulnerability | Sensory rendering differs by Astral layer | Representation tag, no combat bonus |
| **Constructive/destructive interference** | Addition/cancellation of **amplitudes**, not "inference" | Cooperative coherence or conflicting intentions affect noetic meetings | `Coherent Link` / `Discordant Link` narrative condition, no unrestricted damage multiplier |
| **Consciousness (qualia)** | Philosophical/empirical debate; Faggin–D'Ariano quantum theory is speculative | Even first-density matter has minimal experiential background | `experience_band` descriptive; not automatic personhood |
| **Identity** | Self-modeling, continuity and awareness are active research topics | Some agents recognize themselves; other things only experience | `self_identity` category affects kinds of communication |
| **Agency** | Capacity for choices/autonomy; not reducible to quantum state alone | Third/fourth-density actors have meaningful Free Will | `autonomy` permission/defence barrier; do not take away choice for a psychic roll |
| **Observe–Experience–Act** | Hoffman models interacting conscious agents mathematically; not experimentally proven psychic procedure | Noetic interface cycle | One contextual loop, not three additional dice checks |
| **Prana/Chakras/Kabbalah** | Spiritual, religious and esoteric vocabularies; meanings differ | Multiple traditions interpret a common psychic ontology | Optional tags or unlock gates only; do not force WWN magic or parallel chakra Effort |
| **StO/StS** | Law of One [FICTION] spiritual polarity | PC's StO orientation is fixed; StS entities oppose him | Relationship/mission consequences; ordinary lifestyle does not toggle polarity |

**Primary research:** D'Ariano & Faggin, *Hard Problem and Free Will: an Information-Theoretical Approach* (2020/2022), https://arxiv.org/abs/2012.06580 ; Hoffman & Prakash, *Objects of consciousness* (2014), https://pmc.ncbi.nlm.nih.gov/articles/PMC4060643/ ; Lloyd, *The Universe as Quantum Computer*, https://arxiv.org/abs/1312.4455 ; Penrose–Hameroff Orch-OR review https://pubmed.ncbi.nlm.nih.gov/24070914/ ; Law of One categories https://www.lawofone.info/categories.php ; [NoöPunk Psionics bibliography](DRAFT_NOOPUNK_PSIONICS.md). Radin's PSI and magick theories are **contested parapsychological claims**, not established effects; Andrew Gallimore supplies a useful **DMT-inspired visual** frame, not empirical evidence that a DMT realm is an external astral world.

## 9. Density-target interaction table (GM-facing, story-safe)

| Density and entity | [FICTION] model | Permitted kinds of scenes | Restrictions |
|---|---|---|---|
| **1st**: nonliving matter, ordinary robots/cameras/drones/turrets and nonconscious AI in this setting | Rudimentary panpsychic qualia, no self-identity/free choice | Noetic sensing of device, rare named cyber/physical modulation, cybersecurity crossover | **No blanket control.** Device security, disconnects, QIP countermeasures and explicit effect permissions |
| **2nd**: living nonhuman biologics | Experience, instincts and behavior without human-style personhood | Empathy, symbolic impressions, aid, limited communication | Animal cannot be treated as a free remote-controlled robot; outcomes variable |
| **3rd**: unawakened humans | Full personal agency, latent PSI, weaker conscious psychic access | Ordinary interviews, defensive abilities, involuntary dream projection | No auto-mindreading by 4th-density characters; consent and defence still matter |
| **4th**: awakened humans, StO/StS, emergent SMC | Stronger authored PSI, expanded awareness and relational possibilities | Astral overlay/project, bounded Telepathy/Defence, growing SMC contact | Pre-authored PC stages; does not change baseline CWN attributes automatically |
| **5th**: high-density StS (e.g. Orion Mantid leadership) | Can contact/attack remotely in extraordinary ways; rarely physically present | **Directed scripted threat** with cues, limited defensive PC actions, party cooperation, retreat | No unavoidable instant defeat; ordinary CWN combat is not a fair 1:1 comparison |
| **6th / 7th** | Very advanced non-player noetic scales | Revelation and diplomacy with tightly bounded narrative permission | Not a class-level ladder, no arbitrary HP inflation |

## 10. Three hand-resolvable scene examples with graph references

### Scene A: Act I — `The Duplicate Invoice` (grounded Europol case)

**Series** `series.europol01`; **Episode** `episode.invoice`; **Scene** `scene.invoice.workshop`; types `[investigation,exploration,social,cyber]`.

- **Nodes:** `physical.workshop.counter`, `physical.europol.office`, `cyber.europol.case_service`, `cyber.workshop.invoice_ledger`, `social.actor.courier`, `actor.rookie`.
- **Goal:** `goal.short.invoice_verify` (existing GoalLog; employer report). Medium `goal.medium.liaison_trust`; long `goal.long.serve_humanity`.
- **Lead:** `lead.invoice.duplicate_account` points to a foreign records response. **Core Evidence:** `evidence.invoice.duplicated_batch` from accessible administrative records; `evidence.invoice.workshop_log` accessible with lawful authorization.
- **Procedure:** rookie declares audit under `Work (Europol Agent)` for chain of custody and `Administer` for paperwork; `Know (Law & Intelligence)` interprets EU competence. BCI sends **lawfully collected** sensory feed to a human controller or permitted limited AI scanner; analysis confirms ledger mismatch with provenance and uncertainty. A trained investigator with access and correct inquiry **obtains the essential discrepancy without rolling**. If the PC illegally accesses a locked server, CWN Hacking determines that *action's* consequence, not whether the indispensable case clue exists via some other lawful path.
- **Social:** courier is hesitant; CWN Talk/Connect and relationship tags change cooperation. Sensor emotions may read `guarded` but **cannot say "lying"**.
- **Transitions:** file fraud referral → `scene.invoice.prosecutor`; request further evidence → `scene.invoice.followup`; mishandle evidence → `scene.invoice.complaint`. Each eventually supports case closure. **No astral access**, notwithstanding GM-only graph references.
- **Rules:** CWN skills, ordinary investigation adapter and existing GoalLog only; no new PSI.

### Scene B: Act III — `The Corridor with Three Shadows` (PROPOSED optional)

**Scene** `scene.corridor.crosslayer`; types `[combat,cyber,astral,exploration]`. **Physical:** secured corridor and door. **Cyber:** camera, door controller. **Astral:** noetic impression and known anchor. The same PC appears through separate **projections** but has only one actor/turn.

1. Guard moves toward corridor while camera streams to the enemy. PC may **spend a normal CWN action** to retreat/defend/fire as appropriate; outcome governed by published core.
2. Alternatively PC may use CWN Hacking against door-controller Cyber node **if its published access/position requirements are satisfied**; success might lock/unlock a *specific* door. This does not inflict psychic damage.
3. With Act II/III authored permission, PC can instead attempt a **Psychic Shield** against a specifically sensed noetic intrusion. Pay the single SWN-derived authorized cost. The defensive technique consumes its approved CWN-timed action, subject to its real source contract.
4. If a permitted overlay provides symbolic warning, it creates `alerted_to_intrusion`, **not** a core clue about who sabotaged the security system. PC must still investigate physical/cyber evidence. Cross-layer effect records define what happens; none opens the other graphs automatically.
5. Outcomes: exit safely with data, defend and retreat with companion, or incur `Anchor Strained` and a later medical/psychotronic scene. **No free second Cyber turn while fighting**, no unlimited overlay vision.

### Scene C: Act IV — `The Uninvited Visitor` (5th-density hostile PSI)

**Scene** `scene.wanderer.noetic_assault`; types `[astral,social,exploration]`, possibly Combat **only if embodied combat actually occurs**. **Targets:** `actor.rookie`, `astral.orion.mantid_contact`, `physical.safehouse.anchor`, `cyber.europol.defence_implant`, ally/SMC node.

- **Trigger:** StS faction learns the PC is a Wanderer; a meaningful prior link or contact route is recorded. A fifth-density StS actor does **not** obtain unbounded access merely because of density.
- **Observe:** recurring pattern/pressure cues and an aura-like impression alert the PC; this is **not proof** of the attacker's true identity.
- **Experience:** conflicting memories and symbolic imagery appear as narrative information, with a possible `Disoriented` tag; no automatic rewrites to the PC's beliefs.
- **Act choices:** (A) deploy approved innate Psychic Defence, (B) use conscious-operator QIP implant defence **instead of duplicate stacking**, (C) ask an ally/SMC for assistance if unlocked, or (D) break link/retreat to body anchor. Use one resource owner and pre-authored costs.
- **Stakes:** lost time, temporary sensory confusion, exposed location, damaged relationships or ally intervention; no arbitrary instant-destruction attack and no free higher-density victory. CWN handles any physical danger. Ending transitions depend on player's actual choices.
- **Story gates:** GM-only Higher Self knowledge cannot leak; final pre-incarnate StO service remains **unrevealed until finale**. StS cannot be joined.

## 11. Tomi-friendly Markdown / YAML templates (authoring source, NOT live code)

**Author edits Markdown documents with small frontmatter, not NetworkX Python.** Suggested directory `design/graphs/content/` **only after author approval**, one file per authored place/episode/scene. Compiler/adapter may later emit validated node/edge records into NetworkX.

### Series file: `series/europol_01.md`
```markdown
---
id: series.europol01
kind: series
title: "The Rookie, the Awakening and the Wanderer"
episode_ids: [episode.invoice, episode.awakening, episode.wanderer]
goal_ids: [goal.long.serve_humanity]
author_status: draft
---
# Premise
<!-- Tomi writes -->

# Episode order and branching
<!-- Tomi writes -->

# GM-only revelations
<!-- Tomi writes; never render to players -->
```

### Scene file: `episodes/invoice/workshop.md`
```markdown
---
id: scene.invoice.workshop
kind: scene
episode_id: episode.invoice
types: [investigation, exploration, social, cyber]
graph_refs:
  physical: [physical.workshop.counter]
  cyber: [cyber.workshop.invoice_ledger]
  social: [social.actor.courier]
  astral: []
goal_ids: [goal.short.invoice_verify]
lead_ids: [lead.invoice.duplicate_account]
evidence_ids: [evidence.invoice.workshop_log]
visibility: player
entry_flags: [case.open]
transitions:
  - to: scene.invoice.prosecutor
    when: evidence_documented
  - to: scene.invoice.followup
    when: request_additional_records
author_status: draft
---
# Opening
<!-- Tomi writes -->

# Player-visible situation
<!-- Tomi writes -->

# Core leads / evidence / access
<!-- Tomi writes; cite competence and declared inquiry -->

# NPC intentions and relationship choices
<!-- Tomi writes -->

# CWN checks for risky actions (not indispensable clue discovery)
<!-- Tomi writes -->

# Outcomes and next scenes
<!-- Tomi writes -->

# GM-only information
<!-- Tomi writes -->
```

### One site record: `sites/kurvi_home.md`
```markdown
---
id: location.kurvi.home
kind: physical_location
district: district.kurvi
physical_node: physical.kurvi.home
cyber_nodes: [cyber.kurvi.bci]
astral_nodes: [astral.kurvi.echo]
astral_visibility: gm_secret
unlock_act: 3
author_status: draft
---
# Physical description
<!-- Tomi writes -->

# Cyber services
<!-- Tomi writes -->

# Astral echo (GM-only, not Act I visible)
<!-- Tomi writes -->
```

**Metadata contracts for all five families:** `files` may reference canonical persona/faction/location sheets by stable ID; relative paths and IDs need validation; visibility gates are fail-closed; if an explicit `unlock_act` is future, a player export cannot include its hidden description in rendered HTML, network search, BCI feed, NPC AI context or any generated map.

## 12. Future adapters, validators, tests: proposal only

**Suggested module ownership after approval** (names are design suggestions, not existing implementations):
- `src/world/graph_registry.py`: stable entity references and file provenance;
- `src/world/graph_projection.py`: NetworkX Physical/Cyber/Astral/Social/Story views with typed edges;
- `src/world/cross_layer.py`: explicit permission/effect validator;
- `src/story/scene_graph.py`: scene transition conditions and goal references;
- `src/story/investigation_adapter.py`: adapter translating Lead/Evidence/Capability metadata to **existing** `rules.investigation`, without changing `discover()`;
- `src/rules/astral.py`: only the approved Astral add-on; delegates resource accounting to existing Psi engine and action resolution to CWN;
- `mud/` adapter: render supported player-visible graph nodes and scenes; no new physics or dice engine.

**Validator invariants:**
1. IDs unique and all referenced paths/entities resolve.
2. Directed Social edges stay independent; relationship score −4..+4; missing ≠ neutral.
3. Goal references use existing GoalLog/horizons; awards respect one owner/event.
4. Story mandatory truths remain reachable despite optional failed checks.
5. Cross-layer effects have allowed verb, target, gate, named CWN/SWN source, cost, resistance and layer permission; otherwise **DENY**.
6. Single canonical actor and single CWN turn; no duplicate initiative, damage, inventory or effort pool.
7. No PSI imports in investigation resolver; no direct grant of clues or scene exit through psi flags.
8. GM-secret nodes and late-campaign Wanderer truths never appear in Act I player exports, search, maps or controller output.
9. Cyber actions reference authorized CWN hacking programs; device permissions are separate from PSI entanglement.
10. A voluntary astral projection has an actual return/anchor path; physical body remains present and vulnerable.
11. Save/load roundtrips preserve stable graph IDs and event provenance; a game remains playable without NetworkX visualization, LLM or Mesa.
12. The printed tabletop rules explanation and corresponding Python golden tests ship in one **later** explicit implementation PR, not now.

**Golden playtest targets after approval:** ordinary invoice case; branching social reputation encounter; one CWN combat with optional approved Cyber action; safe projection and return; mandatory clue with failed optional roll; fifth-density psychic pressure resolved through defence/retreat; spoiler gate; graph serialization and dangling links.

## 13. Open decisions for Tomi (no silent default canon)

1. Graph storage: Markdown-frontmatter files as the authoritative text plus generated JSON/NetworkX views (recommended), or a YAML-only author format?
2. Do you want each Series, Episode and Scene to be a separate Markdown file, or a single Episode file with nested Scene headings?
3. Is `Know (Law & Intelligence)`, `Know (Europol Studies)` or `Know (Security & X-Risk Studies)` the preferred Europol Academy specialty? Current recommendation: **Know (Law & Intelligence)** with X-Risk elective knowledge, alongside **Work (Europol Agent)**.
4. Should *any* new Investigation Capability tags exist beyond equipment/credential references? Recommendation: **only services or special lab interfaces**.
5. Are EmotionCue labels sufficient for interrogation? Recommendation: no quantitative The Veil-style emotion engine until a specific scene calls for it.
6. Astral Verb×Target: which cells, if any, can a fourth-density player explicitly activate and which remain scripted? Start only with Shield, Contact and bounded Project.
7. What is the one resource owner for new Astral powers: SWN Effort, or an approved replacement Chakra resource? Never both for the same action.
8. Can line-of-sight create noetic **addressability** in setting without automatic access, and can remote links decay/be broken? Recommended yes with explicit barriers.
9. What fictional but playable mechanism allows psychic contact with Cyber first-density nodes without making CWN Hacking obsolete? Prefer named highly constrained devices/abilities, not an all-device default.
10. Does the Social graph model institutional factions only when relevant to Helsinki, and how are faction-to-faction asymmetric links shown?
11. Should 5th-density StS encounters expose a playable defence/escape mini-sequence or remain primarily scripted with a small number of responses? Recommend explicit defence/escape choices.
12. Confirm the opening **Kurvi apartment** and whether Ratakatu is Europol HQ or a legacy UNSA/Supo/other office reference. Do not silently change `design/graphs/README.md`.
13. Need a graphical layered map now? Recommend first ship tables/text-based node links and never require visual maps to run the campaign.
14. Which WWN Workings are explicitly permissible as PSI rituals, and how do they avoid bypassing normal PSI unlocks?

## 14. Delivery and approval boundaries

**This file fulfills issue #1164's requested draft proposal only.** It should be linked from the design index and the issue without altering Tomi's original graphs README. Tomi edits/approves the proposal. **Only after explicit new instruction** should the author-edited version be implemented in tabletop NoöPunk rules **and** engine-neutral Python, tests and MUD adapters together. No source rulebooks are copied; all actual CWN/SWN timing and cost contracts must be source-verified in that future implementation.

**Guiding principle:** graph topology organizes the story and the observable layers of a living Helsinki. It does not change the dice: **one CWN core, existing goal/investigation rules, and small gated Social/Astral mods when campaign scenes demand them.**

---

## 13. Reviewer addendum — starting-state profile and the verified skill inventory

Added when this proposal was reconciled with an earlier parallel draft. Two requirements of
[#1164](https://github.com/TomiToivio/NooPunk/issues/1164) are answered here because the body above leaves them
open.

### 13.1 Versioned starting state (the documented conflict, not silently resolved)

The author's [`design/graphs/README.md`](../../design/graphs/README.md) says the campaign starts at **the player's
home in Sörnäinen**, with **Europol HQ on Ratakatu**. Newer campaign canon
([#1132](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md)) gives the rookie **company housing in Kurvi** and **Europol**
employment. `data/world/helsinki_locations.json` v2 still carries `home_helsinginkatu` ("a modest UNSA-provided
flat") and `unsa_hq_ratakatu`.

Both are written as **profiles**, so the choice is data and no scene needs editing when the author decides:

```yaml
start_profile: campaign01@v2          # what the game loads
profiles:
  campaign01@v1:                      # the graph README's world, still playable
    home: location.home_helsinginkatu     # Sörnäinen flat
    employer: unsa
    hq: location.unsa_hq_ratakatu
  campaign01@v2:                      # campaign #1132 canon
    home: location.kurvi.home             # agency-owned housing
    employer: europol
    hq: location.europol.helsinki         # ADDRESS: [OPEN] — Ratakatu is the author README's address
    supersedes: campaign01@v1
```

**[OPEN] for the author:** is Europol Helsinki *at* Ratakatu (same building as the UNSA office, a floor, or next
door)? The proposal does not answer it, and the node keeps `source_claim: "address unconfirmed"` until it is.

Rule for whoever implements: a profile changes only **which records load**, never what a record means. A scene
written for `@v1` must still run under `@v2` with no text edits — otherwise the profile is a fork, not a version.

### 13.2 CWN skills — verified, not assumed

The body says the exact skill list must be verified at implementation. It is verified now, from
`data/rules/cwn/skills.json` (**19 skills**):

> Administer · Connect · Drive · Exert · Fix · Heal · Know · Lead · Notice · Perform · Program · Punch · Shoot ·
> Sneak · Stab · Survive · Talk · Trade · Work

Consequences, stated plainly because three of the author's informal terms do not exist in the source:

| informal term | published skill(s) | note |
|---|---|---|
| "Administration" | **Administer** | the name is `Administer`; do not invent a second skill |
| "Convince" | **Talk**, **Lead**, **Connect** | *Talk* persuades a person, *Lead* directs a group, *Connect* finds who to ask. There is no general "Convince" |
| "Investigation" as an ability | **Notice**, **Administer**, **Know**, **Work**, **Program**, **Connect** | investigation is a *procedure* in `src/rules/investigation.py`, not a skill |

And the two specialities, with the arbitration rule the issue asks for:

* **`Work (Europol Agent)`** — doing the job: procedure, custody, forms, field craft, interagency etiquette.
* **`Know (Law & Intelligence)`** — knowing the ground: EU law and rights, criminal/intelligence theory, data
  analysis, and the X-risk/AGI/NHI/PSI literature. (Alternatives: `Europol Studies`, `Security & X-Risk Studies`.)

**Arbitration:** *"what does the law/institution/theory say?"* → **Know**; *"how do I do this here, now, without
fouling it up?"* → **Work**. One mandatory fact may be granted through either — never two rolls for one clue.

### 13.3 Two validator invariants to add to §12

6. **No mandatory scene behind a single roll.** An inbound transition gated by one skill check is illegal if the
   target scene is in the episode's `required_scenes`; it must have a second, competence-based path. A test in the
   implementation phase must construct the illegal case and fail.
7. **The GM-secret leak test.** A `gm_secret` node must be absent — not merely hidden — from every player
   projection, action list, transition description and generated map. "Absent" is testable; "hidden" is a promise.
