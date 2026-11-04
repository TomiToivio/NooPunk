# HELSINKI — WORLD (template, #1141)

> **STATUS: TEMPLATE / DRAFT OUTLINE. Agent-written scaffolding, not canon.**
> Four documents exist for this setting: **WORLD** (this file), [CITY](HELSINKI_CITY.md),
> [FACTIONS](HELSINKI_FACTIONS.md), [FACES & XENOBESTIARY](HELSINKI_FACES_XENOBESTIARY.md).
> One concern per document: this one holds **global and setting-wide context that the Helsinki
> campaign needs**, not the district atlas, not faction statistics, not creature stat blocks.
>
> **Source:** *Cities Without Number* (Deluxe), "Creating Your Dystopia" — **Cyberpunk Themes**
> (printed p. 108), **Creating The World** (printed p. 110), **Creating The City** (p. 114),
> **Building Your Districts** (p. 121), **Creating Megacorps** (p. 126), **Creating Gangs**
> (p. 128), **Creating NPCs** (p. 130). Field names here follow those sections; the printed tables
> are **not** reproduced. Verify the edition you hold before relying on a page number.

## How to use this file

1. Every section has a heading, **one deliberately fictional example**, and a
   `<!-- Tomi writes below -->` placeholder. Replace or delete the example; it is scaffolding.
2. Statuses: **AUTHOR CANON** (you ruled it), **REPOSITORY CANON** (already in a cited file),
   **EXAMPLE ONLY / NOT CANON** (agent-written illustration), **OPEN** (needs your decision),
   **GM SECRET** (exists for the GM, not the player).
3. Do not fill author placeholders. An empty section is an invitation, not a gap to be closed.
4. **Act I is grounded cyberpunk.** Nothing in this file may put astral, density or NHI-crisis
   material into early player-facing scenes; the tone ramp is set in
   [`docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md`](../docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md).

## Canon this file must not contradict

| subject | authority |
| --- | --- |
| 2045 setting, NHI Crisis, the Quarantine's end | [`rulebook/10_SINGULARITY_CRISIS.md`](../rulebook/10_SINGULARITY_CRISIS.md) |
| Fortress Europe, chronology, what stays unresolved | [`docs/world/CANON_FORTRESS_EUROPE_1113.md`](../docs/world/CANON_FORTRESS_EUROPE_1113.md), [`docs/world/ALTERNATE_HISTORY_1114.md`](../docs/world/ALTERNATE_HISTORY_1114.md) |
| Europol as the player's employer, and its limits | [`docs/world/EUROPOL_HELSINKI_1114.md`](../docs/world/EUROPOL_HELSINKI_1114.md) |
| City government, X-Risk jurisdictions, ESZs, embassies | **author's**: [`GREATER_HELSINKI_2045.md`](GREATER_HELSINKI_2045.md), [`ZONES.md`](ZONES.md) |
| Faction landscape | [`docs/world/NHI_FACTIONS_922.md`](../docs/world/NHI_FACTIONS_922.md) |
| The rules chassis | [`rulebook/WITHOUT_NUMBER_BASELINE.md`](../rulebook/WITHOUT_NUMBER_BASELINE.md) |

**Do not resolve** the Soviet timeline, the Mandela Effect, or Greater Helsinki's constitutional
status here. They are open by design and belong to the files above.

---

## 1. Cyberpunk Themes

*CWN: "Cyberpunk Themes" (p. 108). One row per theme: what it is, where Helsinki expresses it, what it
costs the player, and a case hook.*

**Fields.** `theme_id`, `theme`, `city_expression`, `player_consequence`, `case_hook`, `rules_reference`, `source`

```yaml
# EXAMPLE ONLY — NOT CANON
theme_id: hel_world_theme_001
theme: "Bureaucratic cyberpunk"
city_expression: "Two EU agencies hold valid credentials for the same archive, and neither can be revoked without the other's signature."
player_consequence: "A lawful request needs a national-police liaison present, or it becomes inadmissible."
case_hook: "A case is closed not because it is solved but because the paperwork expired."
rules_reference: "CWN: INT+Administer / CHA+Connect; no new procedure"
source: "illustrative"
```

<!-- Tomi writes below -->

**Unresolved:** which themes are actually Helsinki's, and which are generic cyberpunk furniture to cut.

---

## 2. The World

*CWN: "Creating The World" (p. 110). The 2045 external conditions that a Europol officer in Helsinki
actually feels — not a global history.*

**Fields.** `world_id`, `condition`, `canon_source`, `what_residents_know`, `what_is_disputed`, `case_hook`

```yaml
# EXAMPLE ONLY — NOT CANON
world_id: hel_world_condition_001
condition: "Psionics is public, regulated and unevenly believed."
canon_source: "rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md §4 (REPOSITORY CANON)"
what_residents_know: "Registration exists; nobody agrees whether it is a health record or a weapons licence."
what_is_disputed: "Whether registered sensitives are safer or merely easier to find."
case_hook: "A witness's PSI testimony is real, admissible, and worth less than a door log."
source: "illustrative"
```

<!-- Tomi writes below -->

**Unresolved:** how much of the NHI Crisis a *rookie in 2045* takes for granted; which disasters are
common knowledge, and which are still contested.

---

## 3. The City (index only)

*CWN: "Creating The City" (p. 114) picks the seed city and its two main problems; the detailed
Helsinki material lives in [`HELSINKI_CITY.md`](HELSINKI_CITY.md). **This section is a pointer and an
elevator pitch, never a second city essay.***

```yaml
# EXAMPLE ONLY — NOT CANON
city_id: hel_city
name: "Helsinki (Greater Helsinki)"
pitch: "An accelerationist harbour city that sold itself to the extraterrestrial economy and now administers the consequences."
main_problems: ["TBD — two, per CWN p. 114, authored by Tomi"]
detail_document: "design/HELSINKI_CITY.md"
source: "illustrative"
```

<!-- Tomi writes below -->

---

## 4. Districts (index only)

*CWN: "Building Your Districts" (p. 121). One row per district, pointing at the full district card in
[`HELSINKI_CITY.md`](HELSINKI_CITY.md) §8. Do not describe a district twice.*

```yaml
# EXAMPLE ONLY — NOT CANON
district_id: hel_district_kurvi
name: "Kurvi"
one_line: "Tram crossroads, nightlife, working-class memory, and the rookie's front door."
card: "HELSINKI_CITY.md#8-the-districts-of-the-city"
source: "illustrative"
```

<!-- Tomi writes below -->

**Unresolved:** the district list itself. CWN wants a handful of playable districts, not an atlas.

---

## 5. Megacorps

*CWN: "Creating Megacorps" (p. 126). An archetype plus its leverage. If a corporation becomes a
mechanical actor, its sheet belongs in [`HELSINKI_FACTIONS.md`](HELSINKI_FACTIONS.md) — link it, do not
restate it.*

**Fields.** `corp_id`, `archetype`, `helsinki_operations`, `public_image`, `leverage`, `hooks`, `faction_ref`

```yaml
# EXAMPLE ONLY — NOT CANON
corp_id: hel_corp_001
archetype: "Logistics contractor with a state monopoly on continuity"
helsinki_operations: "Runs the port's biometric gate system and three municipal archives."
public_image: "Boring, reliable, Finnish."
leverage: "Whoever holds the archive holds the evidence."
hooks: ["A gate log that cannot be subpoenaed", "A strike the city cannot afford"]
faction_ref: null   # link a HELSINKI_FACTIONS.md record only if it acts mechanically
source: "illustrative"
```

<!-- Tomi writes below -->

**Unresolved:** which corporations are real Helsinki employers in 2045 and which are invented; whether
any of them is an Orion proxy (that answer changes the campaign).

---

## 6. Gangs

*CWN: "Creating Gangs" (p. 128). Street-level organisations. **Not every gang is a SWN faction** — a
gang is a faction only when it takes faction turns, holds assets, and competes for influence.*

**Fields.** `gang_id`, `archetype`, `turf`, `method`, `members_want`, `case_hook`, `is_faction`

```yaml
# EXAMPLE ONLY — NOT CANON
gang_id: hel_gang_001
archetype: "Evidence brokers"
turf: "Two blocks around the Kurvi platforms"
method: "They do not steal data; they sell the *absence* of data."
members_want: "To be treated as a service, not a threat."
case_hook: "A witness's file was never deleted — it was rented out."
is_faction: false
source: "illustrative"
```

<!-- Tomi writes below -->

**Unresolved:** which street organisations are local, which are Orion- or Confederacy-adjacent, and
where the line between gang and political movement falls.

---

## 7. NPCs

*CWN: "Creating NPCs" (p. 130) and "Faces On the Street" (p. 180). A character card, not a biography.
Recurring named characters who already exist in the repository must be **linked**, never re-created:
[`design/characters/`](characters/), [`docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md`](../docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md).*

**Fields.** `npc_id`, `name`, `role`, `appearance`, `wants`, `relationships`, `cwn_stats`, `encounter_hooks`, `location_ref`

```yaml
# EXAMPLE ONLY — NOT CANON
npc_id: hel_npc_001
name: "A receptionist who has worked three agencies in one building"
role: "Gatekeeper; institutional memory; the only person who knows which door is real."
appearance: "Badge lanyard with three logos, reading glasses, a terminal older than her career."
wants: "For somebody to fix the archive before she retires."
relationships: "Knows every cleaner, resents every consultant."
cwn_stats: "TBD — generate with CWN p. 130; do not invent numbers"
encounter_hooks: ["She remembers a name that is not in the system", "She can be bribed with competence"]
location_ref: "hel_site_office_ratakatu"
source: "illustrative"
```

<!-- Tomi writes below -->

**Unresolved:** the actual Helsinki cast. The campaign outline already names a unit; this file must not
quietly field a second one.

---

## Unresolved decisions in this document

| # | question | blocks |
| --- | --- | --- |
| W1 | Which three to five cyberpunk themes are *Helsinki's*, not generic? | every district and case hook |
| W2 | What does a 2045 rookie take for granted about the NHI Crisis? | the tone ramp, every briefing scene |
| W3 | Which corporations and gangs exist, and which are Orion/Confederacy fronts? | Act II's antagonists |
| W4 | Which named NPCs are canon, and which are placeholders? | the cast, and the campaign outline's own list |

*Record answers here, in this file, with a date and the author's name — not in a commit message.*
