# Helsinki: Local Factions (author worksheet)

> **DRAFT OUTLINE / EXAMPLE ONLY / NOT CANON** | Issue [#1141](https://github.com/TomiToivio/NooPunk/issues/1141) | Phase 1 of 3. **Tomi owns all final prose.** None of the invented examples below is approved. **No rules or engine implementation authorized.**

**Status legend:** `AUTHOR CANON` = Tomi-approved authored text; `REPOSITORY CANON` = linked existing authority; `EXAMPLE ONLY / NOT CANON` = disposable illustration; `OPEN` = unresolved author choice; `GM SECRET` = gated knowledge, not player-facing. Examples remain non-canon even when they quote a canon setting premise.

**Source/edition:** *Stars Without Number Revised*, Deluxe (2017), **Factions, Assets, and Turns** printed pp.212–227 (actions p.214, buying/assets p.216, Cunning p.218, Force p.220, Wealth p.222, examples p.227). Compare *Worlds Without Number* (2021) faction/major-project guidance and *Ashes Without Number* (2025) Enclaves only when source verified. See [Without Number baseline](../rulebook/WITHOUT_NUMBER_BASELINE.md), [CWN section inventory](../docs/rules/CWN_RULE_INVENTORY.md), and [document register](../docs/DOCUMENT_REGISTER.md). Refer to printed source procedures and tables; do not copy them or manufacture stat values.

**Contents:** Qualification · Faction record · Assets · Worked turn · WWN/AWN delegation · Open decisions

**Cross-reference contract:** `district_id`, `site_id`, `faction_id`, `npc_id`/`entity_id`, `scene_id`, `layer` and `source_ref` are stable *author-chosen* keys. Cross-link a canonical record instead of copying its biography or mechanics. Example IDs start with `example_` and must be replaced before approval.

**Canon anchors:** [Greater Helsinki author draft](GREATER_HELSINKI_2045.md), [ZONES author proposals](ZONES.md), [Europol campaign authority](../docs/world/EUROPOL_HELSINKI_1114.md), [Fortress Europe](../docs/world/CANON_FORTRESS_EUROPE_1113.md), [alternate timeline](../docs/world/ALTERNATE_HISTORY_1114.md), [NHI factions](../docs/world/NHI_FACTIONS_922.md), and [rookie campaign draft](../docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md). Prefer these over obsolete UNSA-player or world-government assumptions. Conflicts remain **OPEN**, never silently resolved.

## 1. Who qualifies?
The local Europol campaign sees municipal departments, police agencies, neighborhood organizations, corporations, gangs, NHI cells and unions. **Only strategically autonomous actors with campaign-scale assets/goals need an SWN faction record.** Ordinary street gangs and contacts remain CWN organizations/NPCs. Global/galactic entities get only a local presence reference; no rival galactic encyclopedia. When CWN's city creation gives actors but not a full faction turn, **SWN supplies the faction turn**, without replacing CWN adventure rules.

## 2. SWN faction record
**EXAMPLE ONLY / NOT CANON** | Hypothetical municipal infrastructure unit; no actual authority, budget or SWN ratings are asserted.
```yaml
faction_id: example_helsinki_infrastructure_cell
name: "[illustrative municipal infrastructure unit]"
scope: "Greater Helsinki local operations"
source_system: "SWN Revised Deluxe 2017, Factions pp.212-227"
mode: swn_faction
home_site_id: example_kurvi_station
jurisdiction: "OPEN; no independent police search/arrest powers"
visibility: "Act I, mundane service contacts"
relations: [{faction_id: "TBD", stance: "OPEN"}]
agenda: "Keep public services operating"
faction_goal: {source_goal_id: "TBD from printed SWN", objective: "restore an approved service"}
force: "TBD by SWN procedure"
cunning: "TBD by SWN procedure"
wealth: "TBD by SWN procedure"
faccreds: "TBD (SWN currency; NOT euros)"
experience: "TBD by SWN goal procedure"
hit_points: "TBD by SWN faction creation"
homeworld_or_base: "Helsinki; choose legal base/location"
faction_tags: [{source_tag: "TBD from printed SWN", note: "verify effect"}]
force_assets: [{source_asset_id: "TBD from SWN Force p.220", location_id: "TBD", stats: "TBD"}]
cunning_assets: [{source_asset_id: "TBD from SWN Cunning p.218", location_id: "TBD", stats: "TBD"}]
wealth_assets: [{source_asset_id: "TBD from SWN Wealth p.222", location_id: "TBD", stats: "TBD"}]
pc_interaction: "interview liaison; gather documentary evidence"
character_reputation_tag_ref: "OPEN; #1137 proposal, NOT faction rating"
source_ref: "EXAMPLE ONLY / NOT CANON"
```
<!-- Tomi writes below -->

## 3. Three source-accurate category slots
**Cunning asset example:** `example_cunning_asset`, source category **Cunning** (SWN p.218), source name/stat fields **TBD from printed entry**, local location **TBD**, proposed purpose covert information, *not a free investigative clue*.

**Force asset example:** `example_force_asset`, source category **Force** (SWN p.220), exact asset and numbers **TBD**, location **TBD**, proposed purpose physical site protection, *not automatic arrest powers*.

**Wealth asset example:** `example_wealth_asset`, source category **Wealth** (SWN p.222), exact asset and numbers **TBD**, location **TBD**, proposed purpose maintenance contracting, *not a second money wallet*. These are **category placeholders**, not asserted published asset names.

**Cross-check against the repository's verified catalogue.** The three slots above are placeholders. The
repository already holds 68 printed asset rows extracted from the book
([`data/rules/swn_faction_assets.json`](../data/rules/swn_faction_assets.json), generated by
`tools/swn_faction_assets.py`, with the printed page recorded per row and spot-checked in
`tests/test_swn_faction_assets_1105.py`). One verified row per category, taken from that file — still **not
owned by any faction** until the author says so:

| category | `source_asset_id` | name (as printed) | cost | HP | page recorded in the repo |
| --- | --- | --- | --- | --- | --- |
| Cunning | `false_front` | False Front | 1 | 2 | 219 |
| Force | `hitmen` | Hitmen | 2 | 1 | 221 |
| Wealth | `franchise` | Franchise | 2 | 3 | 223 |

**OPEN — page numbering must be reconciled before promotion.** This worksheet cites Cunning p. 218,
Force p. 220, Wealth p. 222 and the chapter at pp. 212–227; the repository's extraction records 219, 221,
223 and places the chapter at p. 211 (`docs/rules/SWN_COVERAGE_1105.md`). One of the two is off by a
page. The asset **names, costs and HP** above are the verified values; the page number is the one thing
to check against the edition you hold, because a citation that is confidently wrong is worse than one
marked TBD.
<!-- Tomi writes below -->

## 4. One faction turn: worked process (no invented results)
**EXAMPLE ONLY / NOT CANON**, consult SWN pp.212–216:
1. **Start:** author records current Force/Cunning/Wealth ratings, FacCreds, home/base, asset locations and chosen SWN faction goal. All values **TBD**.
2. **Declare:** example municipal cell proposes **one legal SWN faction action**, precise published action name **TBD** after book check, targeting `example_kurvi_station`; confirm prereqs, asset position, cost and range.
3. **Resolve:** use **only SWN** prescribed action/contest/asset mechanics, track source-based result **TBD**, costs and any retaliatory/consequential effects. No automatic gain or free concurrent WWN/AWN action.
4. **End:** apply SWN turn's goal progress/XP and resource changes as the printed procedure requires, log a fictional service interruption as the *narrative* outcome only after numerical resolution. **No dice or point totals have been guessed.**
<!-- Tomi writes below -->

## 5. Delegation, not multiplication
| Mode | When to use | Exclusivity |
| --- | --- | --- |
| `swn_faction` | Local strategic faction with Force/Cunning/Wealth and asset turns (SWN Revised 2017 pp.212–227) | Default |
| `wwn_project` | A major project whose relevant WWN (2021) procedure is author-selected and verified | Separate delegate, never a bonus free SWN action |
| `awn_enclave` | A post-Crisis settlement requiring AWN (2025) Enclave resource/survival simulation | Separate settlement delegate, **not** another SWN treasury |

**EXAMPLE ONLY / NOT CANON** | `delegate_id: example_crisis_shelter`, `mode: awn_enclave`, `parent_faction_ref: example_helsinki_infrastructure_cell`, `resources: TBD by AWN printed Enclave rules`, `turn_accounting: delegated, no duplicate income/action`. WWN equivalent: `example_waterworks_project`, `mode: wwn_project`, `goal: replace filters`, `procedural_cost: TBD`. Treat both as alternatives until exact edition/section verified.
<!-- Tomi writes below -->

## Open decisions
- **OPEN:** Which local organizations qualify as factions? Source-verified faction goals/tags/asset names, numerical ratings and action choices.
- **OPEN:** Verify WWN and AWN *printed* headings and any major-project/Enclave cost scheme before promotion from placeholder.
- **OPEN:** Reconcile the SWN page numbers above (218/220/222/212–227 vs the repository's 219/221/223/211) against the edition held, then delete this note.
- **GM SECRET:** hidden factions, secret ownership and SWN asset identities remain author-controlled.
