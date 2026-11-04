# Helsinki: Faces in the Street / Xenobestiary (author worksheet)

> **DRAFT OUTLINE / EXAMPLE ONLY / NOT CANON** | Issue [#1141](https://github.com/TomiToivio/NooPunk/issues/1141) | Phase 1 of 3. **Tomi owns all final prose.** None of the invented examples below is approved. **No rules or engine implementation authorized.**

**Status legend:** `AUTHOR CANON` = Tomi-approved authored text; `REPOSITORY CANON` = linked existing authority; `EXAMPLE ONLY / NOT CANON` = disposable illustration; `OPEN` = unresolved author choice; `GM SECRET` = gated knowledge, not player-facing. Examples remain non-canon even when they quote a canon setting premise.

**Source/edition:** *Cities Without Number*, Deluxe (2023), **Creating NPCs** p.134, **Faces On the Street** pp.186–194; *Stars Without Number Revised*, Deluxe (2017), **Xenobestiary / Beasts** p.200 and relevant alien/creature sections; source stat formatting must be checked before filling any numeric block. See [Without Number baseline](../rulebook/WITHOUT_NUMBER_BASELINE.md), [CWN section inventory](../docs/rules/CWN_RULE_INVENTORY.md), and [document register](../docs/DOCUMENT_REGISTER.md). Refer to printed source procedures and tables; do not copy them or manufacture stat values.

**Contents:** Street NPC · Biologic · Construct · Noetic · Plasmoid · Taxonomy and evidence · Open decisions

**Cross-reference contract:** `district_id`, `site_id`, `faction_id`, `npc_id`/`entity_id`, `scene_id`, `layer` and `source_ref` are stable *author-chosen* keys. Cross-link a canonical record instead of copying its biography or mechanics. Example IDs start with `example_` and must be replaced before approval.

**Canon anchors:** [Greater Helsinki author draft](GREATER_HELSINKI_2045.md), [ZONES author proposals](ZONES.md), [Europol campaign authority](../docs/world/EUROPOL_HELSINKI_1114.md), [Fortress Europe](../docs/world/CANON_FORTRESS_EUROPE_1113.md), [alternate timeline](../docs/world/ALTERNATE_HISTORY_1114.md), [NHI factions](../docs/world/NHI_FACTIONS_922.md), and [rookie campaign draft](../docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md). Prefer these over obsolete UNSA-player or world-government assumptions. Conflicts remain **OPEN**, never silently resolved.

The four NHI **encounter taxonomies** below are **not** factions, species, ontological certainties, Density ranks or allegiances. Use `body_type`, `ontology_claim`, `faction_ref`, `density`, `realm`, `encounter_layers` as distinct fields. A cyber-only script may be non-conscious malware, not a Construct or a Noetic. Existing biographies and NHI civilization descriptions live in [NHI factions](../docs/world/NHI_FACTIONS_922.md) and the [document register](../docs/DOCUMENT_REGISTER.md); these cards only link.

## 1. Ordinary CWN street face
**EXAMPLE ONLY / NOT CANON**:
```yaml
npc_id: example_night_clerk
name: "[invented shift clerk]"
role: "transit maintenance witness"
body_type: "ordinary human"
appearance: "reflective orange work jacket"
wants: "keep their rota intact"
behavior: "guarded until formal interview"
relationships: [{npc_id: "TBD", type: "colleague"}]
encounter_layers: [Physical, "Cyber (authorized job account)"]
district_id: example_kurvi
site_id: example_kurvi_station
scene_id: example_receipt_interview
cwn_stat_ref: "TBD: use actual CWN NPC template, printed pp.134, 186-194"
morale_reaction: "TBD by printed CWN procedure; no invented values"
hook: "witness saw a duplicate timestamp"
noncombat_resolution: "request testimony; check physical ticket provenance"
sources: ["EXAMPLE ONLY / NOT CANON"]
```
<!-- Tomi writes below -->

Each NHI example carries an **empty printed SWN Xenobestiary stat contract**, not fabricated alien hit dice or attack statistics. A source-authored non-combat entity may use only encounter tags; if combat is later approved, delegate attacks/damage to the matching authorized CWN/SWN stat record instead of creating an NHI combat engine.

## 2. Biologics
**EXAMPLE ONLY / NOT CANON** | `entity_id: example_biologic_moth` | **Name:** unnamed engineered pollinator; **taxonomy:** Biologic; **body/status:** physical organic body, origin unverified; **encounter_layers:** Physical; **density:** unknown; **realm:** Space/Time; **origin_claim:** “offworld laboratory” (rumor); **verified:** sample is biological, no provenance. **Signs:** iridescent powder. **Motivation:** shelter. **Behavior:** avoids lights. **Communication:** movement. **Threat:** accidental contamination (not asserted lethal). **Noncombat:** collect discarded material with consent/precautions. **Faction_ref:** none verified. **Stats:** `swn_xenobestiary_stat_ref: TBD SWN Revised Xenobestiary/Beasts p.200`; **PSI:** none verified; **countermeasure:** distance and protective handling; **mission_hook:** lab labels disagree; **first_campaign_act:** II, if approved; **GM_spoiler_gate:** no confirmed alien origin; **sources:** fictional placeholder.
<!-- Tomi writes below -->

## 3. Constructs
**EXAMPLE ONLY / NOT CANON** | `entity_id: example_service_automaton` | **Name:** maintenance automaton; **taxonomy:** Construct (manufactured body, consciousness **unknown**); **body/status:** robot; **encounter_layers:** Physical, Cyber (authenticated maintenance console); **density:** unknown/not inferred; **realm:** Space/Time; **origin_claim:** vendor certification, **verified:** serial number only. **Signs:** patched panels. **Motivation:** assigned service route, not proof of subjective intention. **Behavior:** repeats a corridor inspection. **Communication:** recorded prompts. **Threat:** collision, accidental evidence erasure. **Noncombat:** isolate account lawfully, obtain logs. **Faction_ref:** OPEN. **Stats:** `cwn_stat_ref: TBD` or `swn_xenobestiary_stat_ref: TBD` only if approved; **PSI:** none assumed; **countermeasure:** authorized maintenance shutdown, never free hacking access; **hook:** timestamps differ; **act:** I; **GM gate:** none beyond investigation; **sources:** fictional placeholder. **Cyber-only process test:** if only a server script exists, classify `software_process`, **not conscious Construct**.
<!-- Tomi writes below -->

## 4. Noetics
**EXAMPLE ONLY / NOT CANON** | `entity_id: example_archivist_echo` | **Name:** archivist echo; **taxonomy:** Noetic; **body/status:** no physical embodiment confirmed; **encounter_layers:** Astral, Cyber (only a symbolic written report, not digital occupancy); **density:** unknown; **realm:** Time/Space claimed, not verified; **origin_claim:** a witness attributes the sign to a nonphysical visitor; **verified:** testimony only. **Signs:** repeated diagram in dreams. **Motivation:** recognition. **Behavior:** answers ambiguously. **Communication:** negotiated dream symbol. **Threat:** unreliable memory. **Noncombat:** consent-based interview, compare independent evidence. **Faction_ref:** none verified. **Stats:** `swn_xenobestiary_stat_ref: TBD`; **PSI:** refer to [unapproved draft](../docs/design/DRAFT_NOOPUNK_PSIONICS.md), projection locked; **countermeasure:** psychic boundaries and ordinary corroboration; **hook:** witness recalls inconsistent notation; **act:** III only if authorized; **GM gate:** Astral inaccessible in Act I; **sources:** fictional placeholder.
<!-- Tomi writes below -->

## 5. Plasmoids
**EXAMPLE ONLY / NOT CANON** | `entity_id: example_luminous_drift` | **Name:** luminous drift; **taxonomy:** Plasmoid (appearance-based, not proof of a conscious plasma being); **body/status:** light/energy-like phenomenon, organism status OPEN; **encounter_layers:** Physical observation; possible Astral interpretation not fact; **density:** unknown; **realm:** unverified; **origin_claim:** electrical anomaly vs NHI visitor, competing readings; **verified:** instrument trace. **Signs:** brief light over equipment. **Motivation:** unknown. **Behavior:** intermittent. **Communication:** no confirmed signal. **Threat:** equipment fault. **Noncombat:** isolate sensor errors, compare witnesses. **Faction_ref:** none verified. **Stats:** `swn_xenobestiary_stat_ref: TBD if entity confirmed`; **PSI:** unverified; **countermeasure:** safe distance/instrument validation; **hook:** two independent recordings differ; **act:** II; **GM gate:** entityhood unresolved; **sources:** fictional placeholder.
<!-- Tomi writes below -->

## 6. Investigation, source boundaries and actor classification
**Evidence first:** Europol can interview, compare logs and seek national police/prosecutor cooperation; it cannot independently search/arrest. A PSI power is never a free core clue or unlimited telepathic interrogation. Consult [PSI/investigation boundary](../docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md). An NHI present in several layers is **not** physically present everywhere. Mark claims with `verified_fact`, `origin_claim`, `observer`, `confidence`, and `source_ref`.
<!-- Tomi writes below -->

## Open decisions
- **OPEN:** Approve taxonomy per being; select printed NPC/creature stat formats and actual numerical entries, if necessary.
- **OPEN:** Which existing NPCs/NHI factions receive encounter refs? Which clues, authority and diplomatic permissions can the player actually obtain?
- **GM SECRET:** reserve spoiler gates for acts II–IV and keep Act I mundane.
