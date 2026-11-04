# Helsinki: The City (author worksheet)

> **DRAFT OUTLINE / EXAMPLE ONLY / NOT CANON** | Issue [#1141](https://github.com/TomiToivio/NooPunk/issues/1141) | Phase 1 of 3. **Tomi owns all final prose.** None of the invented examples below is approved. **No rules or engine implementation authorized.**

**Status legend:** `AUTHOR CANON` = Tomi-approved authored text; `REPOSITORY CANON` = linked existing authority; `EXAMPLE ONLY / NOT CANON` = disposable illustration; `OPEN` = unresolved author choice; `GM SECRET` = gated knowledge, not player-facing. Examples remain non-canon even when they quote a canon setting premise.

**Source/edition:** *Cities Without Number*, Deluxe (2023), **Creating Your Dystopia**, Creating the City p.118 and Building Your Districts p.125; CWN Hacking pp.96–108; additional dimensional terminology is NoöPunk **draft lore only**, not new CWN mechanics. See [Without Number baseline](../rulebook/WITHOUT_NUMBER_BASELINE.md), [CWN section inventory](../docs/rules/CWN_RULE_INVENTORY.md), and [document register](../docs/DOCUMENT_REGISTER.md). Refer to printed source procedures and tables; do not copy them or manufacture stat values.

**Contents:** Timeline · Megacorps · Groups · Ethos · Government · Crime · Social relationships · Districts · Three-layer architecture · Open decisions

**Cross-reference contract:** `district_id`, `site_id`, `faction_id`, `npc_id`/`entity_id`, `scene_id`, `layer` and `source_ref` are stable *author-chosen* keys. Cross-link a canonical record instead of copying its biography or mechanics. Example IDs start with `example_` and must be replaced before approval.

**Canon anchors:** [Greater Helsinki author draft](GREATER_HELSINKI_2045.md), [ZONES author proposals](ZONES.md), [Europol campaign authority](../docs/world/EUROPOL_HELSINKI_1114.md), [Fortress Europe](../docs/world/CANON_FORTRESS_EUROPE_1113.md), [alternate timeline](../docs/world/ALTERNATE_HISTORY_1114.md), [NHI factions](../docs/world/NHI_FACTIONS_922.md), and [rookie campaign draft](../docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md). Prefer these over obsolete UNSA-player or world-government assumptions. Conflicts remain **OPEN**, never silently resolved.

## 1. A Timeline of Collapse
**EXAMPLE ONLY / NOT CANON** | `event_id: example_ledger_outage` | **Order:** after an unspecified Crisis disruption (**no invented date**). **Event:** transit records unavailable for one shift. **Regional impact:** commuters queue; **reliability:** witness account, unverified; **evidence:** retained physical ticket. **Canon refs:** [chronology](../docs/world/CANON_FORTRESS_EUROPE_1113.md), [alternate history](../docs/world/ALTERNATE_HISTORY_1114.md). **Status:** OPEN.
<!-- Tomi writes below -->

## 2. The Megacorps
**EXAMPLE ONLY / NOT CANON** | `corp_ref: example_civic_access_vendor` | **Footprint:** fictional maintenance desk. **Services:** identity access. **Faction_ref:** OPEN. **Physical:** repair depot; **Cyber:** credential server controlled by ordinary CWN hacking; **Astral:** no verified presence. Do not add a duplicate corporation sheet: [World index](HELSINKI_WORLD.md#5-megacorps).
<!-- Tomi writes below -->

## 3. Other Groups and Organizations
**EXAMPLE ONLY / NOT CANON** | `org_id: example_city_liaison_desk` | **Kind:** hypothetical municipal liaison. **Jurisdiction:** request/referral only, powers to be authored. **Relationships:** Europol request routed to Finnish police for any Finnish search/arrest; [Europol limits](../docs/world/EUROPOL_HELSINKI_1114.md). **Existing organizations to reference, not redefine:** Helsingin Poliisi, Suomen Poliisi, Supo, Europol, UNSA, Eurodef, municipal services, unions/cooperatives and alien diplomatic institutions. Special zones in [ZONES](ZONES.md) are author-authored proposals; exact competence OPEN.
<!-- Tomi writes below -->

## 4. The Ethos of the City
**EXAMPLE ONLY / NOT CANON** | `ethos_id: example_efficiency_paradox` | **Claimed value:** frictionless efficiency. **Contradiction:** six incompatible authorization forms. **Street manifestation:** tram inspector and investigator queue at the same kiosk. **Comedy:** procedure is credible, not a joke about suffering. **Campaign consequence:** negotiate evidence sharing.
<!-- Tomi writes below -->

## 5. The City Government
**EXAMPLE ONLY / NOT CANON** | `government_case_id: example_shared_stairwell` | **Question:** who authorizes a building entry after a cross-border alarm? **Municipal:** premises/services, authority OPEN. **Finnish national:** police/prosecutorial permission; **EU:** Europol coordination, not independent arrest/search; **UN/X-risk:** UNSA involvement only where mandated. **REPOSITORY CANON:** [Europol](../docs/world/EUROPOL_HELSINKI_1114.md); **AUTHOR CANON source:** [ZONES](ZONES.md); [governance author-only draft](GREATER_HELSINKI_2045.md) remains blank. No new legal citations.
<!-- Tomi writes below -->

## 6. Crime and Punishment
**EXAMPLE ONLY / NOT CANON** | `offense_id: example_stolen_access_log` | **Allegation:** stolen transit access data. **Lead agency:** OPEN pending jurisdiction; Europol coordinates only. **Institution:** Finnish investigative authority to be selected by author. **Cyber:** CWN hacking evidence is not a warrant. **PSI/hybrid registration:** consult [BIONICS](BIONICS.md), do not invent law. **Enforcement condition:** proper legal authorization. **Consequence:** logs inadmissible or case delayed if procedure bypassed.
<!-- Tomi writes below -->

## 7. Social Relationships in the City
**EXAMPLE ONLY / NOT CANON** | `network_id: example_kurvi_neighbor_circle` | **People:** roommate, porter and corner-shop worker (all placeholders). **Tie:** shared stairwell maintenance. **Institution:** tenant board. **Class/solidarity:** tenants pool repairs. **Reputation:** hearsay not a mechanical SWN stat. **Hook:** someone asks the rookie to check a bill without invoking Europol power.
<!-- Tomi writes below -->

## 8. The Districts of the City
**CWN district source:** *Building Your Districts*, printed p.125. The author must consult the actual printed prompts/tables; the schema below is an **adapted worksheet**, not a transcription of CWN generator tables.

**EXAMPLE ONLY / NOT CANON** | `district_id: example_kurvi` | **Name:** Kurvi (real neighborhood, fictional 2045 details). **Character:** crowded transport/residential crossroads. **District traits/tags:** commuter junction, tenant solidarity (fictional choices; verify against source generator). **Assets:** transit hub and services. **Problems/risks:** access-record inconsistency. **Landmarks:** public street corner (not an invented entrance). **Faction presence:** `example_city_liaison_desk` (provisional). **NPC refs:** `example_night_clerk`. **Encounter:** request for a duplicated receipt. **Mission:** check ticket provenance. **Layer links:** `example_kurvi_station` for Physical/Cyber/Astral. **CWN fields/rolls:** OPEN until author selects printed table results.
<!-- Tomi writes below -->

## 9. Physical / Cyber / Astral: spatial and access architecture
Three **player-visible capable** layers per `site_id`; their visibility and access can differ. **Physical** is navigable material topology; **Cyber** is BCI/AR overlays and network topology governed by unchanged CWN hacking; **Astral** is an experiential/noetic domain and is *not* automatically a software network or a camera into private rooms. Physical geometry and digital graph edges must never be conflated. See [draft Psionics](../docs/design/DRAFT_NOOPUNK_PSIONICS.md) (NOT approved).

**Tunnels:** real metro passages, service tunnels, utilities, caves and restricted infrastructure need individually verified geometry and access. **No real restricted route is declared public or traversable here.** Every invented 2045 tunnel must carry `fictional_2045: true`. Reference actual access research before any future authored entrance is enabled.

**Space/Time versus Time/Space:** physical embodied experience versus nonphysical/metaphysical experience (Law of One fictional model). A visualization of Time/Space is not a transit permission. **Third/Fourth Density** classify consciousness/development, not another map axis; an embodied fourth-density being is not automatically invisible. Dreams/NDEs may be involuntary phenomena; *deliberate* astral travel requires explicit approved ability. **Interdimensional Hypothesis** is an in-world contested explanation: test reports, compare alternate readings and record uncertainty without canonizing one origin for all NHI.

**EXAMPLE ONLY / NOT CANON**:
```yaml
site_id: example_kurvi_station
district_id: example_kurvi
physical_site: {visible: true, geometry: "public station frontage", routes: ["public street"]}
cyber_site: {visible: "with authorized BCI", access: "CWN hacking; actual credentials"}
astral_site: {visible: false, gm_only: true, access: "scripted/unlocked only"}
realm: {player: space_time, gm_possible: time_space}
density_access: {third: "ordinary physical", fourth: "not a map coordinate"}
known_tunnels: [{description: "no underground traversal presumed", verified_public_access: false}]
visibility: {act_i: ["physical", "authorized cyber"], later: "author-gated"}
transition_rule: "No physical-to-astral transition absent an approved ability"
scripted_reveal_gate: "GM SECRET: later act only, not implemented"
interdimensional_hypothesis: "OPEN; competing in-world explanation"
GM_secrets: "not written"
scene_id: example_receipt_interview
```
<!-- Tomi writes below -->

## Open decisions
- **OPEN:** CWN district table outcomes, approved district map, precise arrest/search competence and municipal powers.
- **OPEN:** Verified public-access tunnel sources; exact underground site connectivity remains disabled until sourced.
- **OPEN:** Whether any scene grants deliberate projection, what it costs, and whether the Interdimensional Hypothesis fits the authored cosmology.
- **GM SECRET:** Act I must show only grounded cyberpunk scenes; no automatic cosmic lore leakage.
