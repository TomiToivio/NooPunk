# Helsinki: The World (author worksheet)

> **DRAFT OUTLINE / EXAMPLE ONLY / NOT CANON** | Issue [#1141](https://github.com/TomiToivio/NooPunk/issues/1141) | Phase 1 of 3. **Tomi owns all final prose.** None of the invented examples below is approved. **No rules or engine implementation authorized.**

**Status legend:** `AUTHOR CANON` = Tomi-approved authored text; `REPOSITORY CANON` = linked existing authority; `EXAMPLE ONLY / NOT CANON` = disposable illustration; `OPEN` = unresolved author choice; `GM SECRET` = gated knowledge, not player-facing. Examples remain non-canon even when they quote a canon setting premise.

**Source/edition:** *Cities Without Number*, Deluxe (2023), **Creating Your Dystopia**, printed pp.112 Cyberpunk Themes, 114 Creating the World, 118 Creating the City, 125 Building Your Districts, 130 Creating Megacorps, 132 Creating Gangs, 134 Creating NPCs. See [Without Number baseline](../rulebook/WITHOUT_NUMBER_BASELINE.md), [CWN section inventory](../docs/rules/CWN_RULE_INVENTORY.md), and [document register](../docs/DOCUMENT_REGISTER.md). Refer to printed source procedures and tables; do not copy them or manufacture stat values.

**Contents:** Cyberpunk Themes · The World · The City · Districts · Megacorps · Gangs · NPCs · Open decisions

**Cross-reference contract:** `district_id`, `site_id`, `faction_id`, `npc_id`/`entity_id`, `scene_id`, `layer` and `source_ref` are stable *author-chosen* keys. Cross-link a canonical record instead of copying its biography or mechanics. Example IDs start with `example_` and must be replaced before approval.

**Canon anchors:** [Greater Helsinki author draft](GREATER_HELSINKI_2045.md), [ZONES author proposals](ZONES.md), [Europol campaign authority](../docs/world/EUROPOL_HELSINKI_1114.md), [Fortress Europe](../docs/world/CANON_FORTRESS_EUROPE_1113.md), [alternate timeline](../docs/world/ALTERNATE_HISTORY_1114.md), [NHI factions](../docs/world/NHI_FACTIONS_922.md), and [rookie campaign draft](../docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md). Prefer these over obsolete UNSA-player or world-government assumptions. Conflicts remain **OPEN**, never silently resolved.

## 1. Cyberpunk Themes
**EXAMPLE ONLY / NOT CANON** | `theme_id: example_credential_gridlock` | **Theme:** Bureaucratic cyberpunk. **Helsinki expression:** incompatible EU and local credentials delay access to a transit log. **Player consequence:** the Europol rookie needs a Finnish liaison; Europol cannot search independently. **Case hook:** two authenticated reports disagree. **CWN reference:** Cyberpunk Themes p.112; ordinary checks unchanged.
<!-- Tomi writes below -->

## 2. The World
**EXAMPLE ONLY / NOT CANON** | `world_context_id: example_border_manifest` | **2045 condition:** post-Crisis security checks disrupt ordinary trade. **Canon reference:** [Fortress Europe](../docs/world/CANON_FORTRESS_EUROPE_1113.md). **Residents know:** packages are delayed. **Disputed claim:** a supplier blames NHI interference; this is testimony, not fact. **Hook:** compare manifests without resolving the Soviet timeline or Mandela Effect.
<!-- Tomi writes below -->

## 3. The City
**EXAMPLE ONLY / NOT CANON** | `city_ref: greater_helsinki` | **Pitch:** a Europol rookie investigates competing records across a merged metropolis. **Detailed authority:** [City worksheet](HELSINKI_CITY.md); municipality and special zones remain governed by [ZONES](ZONES.md) and [Greater Helsinki author draft](GREATER_HELSINKI_2045.md). No new city facts here.
<!-- Tomi writes below -->

## 4. Districts (index only)
**EXAMPLE ONLY / NOT CANON** | `district_id: example_kurvi` | **Index label:** Kurvi neighborhood; **focus:** housing, shops and an ordinary missing-parcel complaint; **full record:** [City district sheet](HELSINKI_CITY.md#8-the-districts-of-the-city). A reference, not a second district definition.
<!-- Tomi writes below -->

## 5. Megacorps
**EXAMPLE ONLY / NOT CANON** | `corp_id: example_civic_access_vendor` | **Archetype:** municipal credential contractor, fictional and unnamed. **Operations:** access badge maintenance. **Public image:** dependable public service. **Leverage:** controls repair scheduling, *not* police powers. **Conflict:** contract disputes produce evidence delays. **CWN reference:** Creating Megacorps p.130. **Local faction_ref:** OPEN; most corporations need not get SWN mechanical turns.
<!-- Tomi writes below -->

## 6. Gangs
**EXAMPLE ONLY / NOT CANON** | `group_id: example_resale_ring` | **Archetype:** street-level resale crew. **Turf:** hypothetical Kurvi marketplace. **Method:** selling salvaged credentials. **Motivations:** rent, loyalty, easy money. **Case hook:** a receipt matches a cross-border fraud report. **CWN reference:** Creating Gangs p.132. **Mechanical faction:** none by default.
<!-- Tomi writes below -->

## 7. NPCs
**EXAMPLE ONLY / NOT CANON** | `npc_id: example_night_clerk` | **Role:** invented night-shift clerk. **Appearance:** orange repair jacket. **Want:** keep their job. **Relationship:** knows the transit porter. **Relevant stats:** `cwn_stat_ref: TBD`, choose source-accurate NPC stats from CWN Creating NPCs p.134 and Faces On the Street pp.186–194; **never infer numbers here**. **Hook:** shares a timestamp if lawfully interviewed. **Location_ref:** `example_kurvi`. **Scene_ref:** `example_receipt_interview`.
<!-- Tomi writes below -->

## Open decisions
- **OPEN:** Which Helsinki-specific cyberpunk themes matter to the campaign?
- **OPEN:** Which companies and gangs are author-established? Which earn SWN faction scale?
- **OPEN:** Which existing character records should the NPC index point to instead of duplicating?
- **GM SECRET:** The cause of any contradictory manifest is undecided and hidden until authored.
