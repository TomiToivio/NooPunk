# HELSINKI — CITY (template, #1141)

> **STATUS: TEMPLATE / DRAFT OUTLINE. Agent-written scaffolding, not canon.**
> Companion documents: [WORLD](HELSINKI_WORLD.md) · **CITY** (this file) ·
> [FACTIONS](HELSINKI_FACTIONS.md) · [FACES & XENOBESTIARY](HELSINKI_FACES_XENOBESTIARY.md).
>
> **Source:** *Cities Without Number* (Deluxe), **The City** (printed pp. 196–217): *A Timeline of
> Collapse* 198 · *The Megacorps* 200 · *Other Groups and Organizations* 203 · *The Ethos of the City*
> 204 · *The City Government* 206 · *Crime and Punishment* 207 · *Social Relationships in the City*
> 208 · *Gender and Identity* 209 · *The Districts of the City* 210 (sample districts 212–217).
> Creation procedure: **Creating The City** 114, **Building Your Districts** 121. Field names follow
> those sections; the printed tables are not reproduced. Check the edition you hold before citing a
> page.

## How to use this file

1. Each section below is a **heading + one fictional example + `<!-- Tomi writes below -->`**. Replace
   the example; it exists to show the format.
2. Statuses: **AUTHOR CANON**, **REPOSITORY CANON**, **EXAMPLE ONLY / NOT CANON**, **OPEN**,
   **GM SECRET**.
3. **One concern per document.** Districts are *cards* here; their factions live in
   [FACTIONS](HELSINKI_FACTIONS.md), their people in [FACES](HELSINKI_FACES_XENOBESTIARY.md), their
   world context in [WORLD](HELSINKI_WORLD.md). Link by ID; never restate a record.
4. **Act I tone gate.** The three-layer material in §9–§10 is a **GM model**. Nothing astral, noetic
   or density-related may appear in player-facing Act I text.

## Canon this file must not contradict

* City governance, X-Risk jurisdiction levels, ESZs and embassies — **author's**
  [`GREATER_HELSINKI_2045.md`](GREATER_HELSINKI_2045.md) and [`ZONES.md`](ZONES.md). Neither is filled
  in by an agent; if a section needs a jurisdictional answer, it links there and stops.
* Europol's powers and limits — [`docs/world/EUROPOL_HELSINKI_1114.md`](../docs/world/EUROPOL_HELSINKI_1114.md):
  Europol coordinates and analyses; it does not arrest or search.
* Chronology — [`docs/world/CANON_FORTRESS_EUROPE_1113.md`](../docs/world/CANON_FORTRESS_EUROPE_1113.md),
  [`docs/world/ALTERNATE_HISTORY_1114.md`](../docs/world/ALTERNATE_HISTORY_1114.md).
* Existing city data — [`data/world/helsinki_locations.json`](../data/world/helsinki_locations.json),
  [`helsinki_map.json`](../data/world/helsinki_map.json), [`lexicon.json`](../data/world/lexicon.json).

---

## 1. A Timeline of Collapse

*CWN p. 198. In-universe events the city still lives inside. **Do not invent dates that canon leaves
open** — write "undated" or give an order instead.*

**Fields.** `event_id`, `event`, `date_or_order`, `regional_impact`, `reliability`, `physical_evidence`

```yaml
# EXAMPLE ONLY — NOT CANON
event_id: hel_city_collapse_001
event: "The port reopens under extraterrestrial freight rules"
date_or_order: "undated in canon; after the Quarantine's end"
regional_impact: "Customs work triples; three municipal departments lose their reason to exist."
reliability: "Official history; contested by the stevedores' union"
physical_evidence: "Two sets of gate hardware bolted one over the other; a form in two alphabets"
source: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** which events are public knowledge, which are school-curriculum simplifications, and which are
deliberately vague in-world.

---

## 2. The Megacorps

*CWN p. 200. Helsinki footprint and local leverage. The corporation's **archetype and hooks** belong in
[WORLD](HELSINKI_WORLD.md) §5; only its **city presence** is written here.*

```yaml
# EXAMPLE ONLY — NOT CANON
corp_id: hel_corp_001
city_footprint: "Port gates, two archives, the municipal payroll system."
services: ["biometric access", "records custody", "payroll"]
local_connections: ["hel_faction_001"]
social_reach: "Its HR department is faster than the police."
cyber_reach: "Gate logs are CWN hacking targets with ordinary defenses."
astral_reach: "none established"
source: "illustrative"
```

<!-- Tomi writes below -->

---

## 3. Other Groups and Organizations

*CWN p. 203. Record **legal competence**, not just a name: who may arrest, search, compel, or refuse.*

| field | meaning |
| --- | --- |
| `org_id`, `name` | stable ID and the name used in play |
| `kind` | police / agency / municipality / union / cooperative / diplomatic / religious / NGO |
| `jurisdiction` | what it may lawfully do, and where |
| `canon_ref` | the file that already defines it, if any |

```yaml
# EXAMPLE ONLY — NOT CANON
org_id: hel_org_001
name: "Helsingin Poliisi, Kurvi patrol unit"
kind: "police"
jurisdiction: "Arrest and search under Finnish law, within Helsinki; no EU mandate."
canon_ref: "ZONES.md (jurisdiction levels)"
source: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** which organisations are canon (Europol, SuPo, UNSA, municipal bodies, unions) and which are
invented for play; where their competences actually collide.

---

## 4. The Ethos of the City

*CWN p. 204. Public values, the contradictions underneath them, and how it looks on the street.*

**Fields.** `value`, `contradiction`, `street_manifestation`, `comedy_note`, `campaign_implication`

```yaml
# EXAMPLE ONLY — NOT CANON
value: "Competence is a moral virtue"
contradiction: "The systems that prove competence are the ones nobody can maintain"
street_manifestation: "People apologise for their own forms."
comedy_note: "The absurdity is sincere, never cruel: everyone is trying very hard."
campaign_implication: "An incompetent order is obeyed more slowly, not refused."
source: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** the city's self-image (accelerationist? social-democratic? both, badly?) and what the
campaign wants to satirise without contempt.

---

## 5. The City Government

*CWN p. 206, but **deferred to the author**.*

```yaml
# EXAMPLE ONLY — NOT CANON
authority_ref: "GREATER_HELSINKI_2045.md"
zones_ref: "ZONES.md"
note: "Municipal, national, EU and UN layers are defined there. This file links; it does not decide."
```

<!-- Tomi writes below -->

**OPEN (author):** the merger of Helsinki/Espoo/Vantaa, the ESZ administrations, and which body answers
for an incident that is simultaneously a crime and an X-risk.

---

## 6. Crime and Punishment

*CWN p. 207. What is an offence, who enforces it, and what a competent officer can actually do.*

| field | meaning |
| --- | --- |
| `offence`, `classification` | ordinary crime / cyber / PSI-related / X-risk / administrative |
| `enforcement` | police, Europol, SuPo, UNSA, or nobody |
| `evidence_standard` | what a report needs to survive review |
| `consequence` | what the player risks |

```yaml
# EXAMPLE ONLY — NOT CANON
offence: "Unregistered psychotronic augmentation"
classification: "administrative, escalating to criminal on harm"
enforcement: "Finnish police; Europol may only advise"
evidence_standard: "Device serial plus a licensed inspection; a scan alone is not proof."
consequence: "The owner loses the implant, not the case."
source: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** whether PSI registration is a health record, a weapons licence, or both — this changes every
Act II scene and belongs to the author.

---

## 7. Social Relationships in the City

*CWN p. 208 (and *Gender and Identity* p. 209). Where the rookie's life happens when no case is open.*

```yaml
# EXAMPLE ONLY — NOT CANON
relationship_id: hel_social_001
who: "The neighbour across the stairwell"
where: "Kurvi company housing"
basis: "Shared laundry, mutual silence, one favour owed"
what_they_want: "To not be asked about the night shift"
how_it_changes: "Becomes an informant, a liability, or a friend — never all three at once."
source: "illustrative"
```

<!-- Tomi writes below -->

---

## 8. The Districts of the City

*CWN pp. 210–217. A **full district card** for the starting district; a short index row for the rest.
Do not invent canonical neighbourhoods, populations, or a complete atlas.*

```yaml
# EXAMPLE ONLY — NOT CANON
district_id: hel_district_kurvi
name: "Kurvi"
traits: ["TBD — two traits per CWN p. 122"]
character: "Tram crossroads, nightlife, working-class memory, constant rebuilding."
assets: ["TBD"]
risks: ["TBD"]
landmarks: ["The platforms", "A bar that has changed owners four times"]
faction_presence: ["hel_faction_001"]     # link, do not describe
npcs: ["hel_npc_001"]                     # link, do not describe
encounters: ["TBD"]
mission_hooks: ["TBD"]
layer_refs: { physical: "hel_site_kurvi_transit", cyber: "hel_site_kurvi_transit_cyber", astral: "hel_site_kurvi_transit_astral" }
source: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** which districts exist, and which of them are playable rather than named.

---

## 9. Three layers at every location (lore/data model, not new rules)

The city is modelled as **three player-visible layers plus two classification axes**. This is a
**data model for scenes**, not a second exploration or combat engine: physical actions use CWN, cyber
access uses CWN hacking, astral access requires an unlocked ability and a scripted gate.

| layer | what it is | how it is resolved | Act I visibility |
| --- | --- | --- | --- |
| **Physical** | streets, transit, harbour, buildings, utilities, tunnels | CWN movement, Notice, combat, equipment | visible |
| **Cyber** | the BCI/AR overlay, software and security spaces | **CWN hacking** (no parallel city-net system) | visible through a BCI |
| **Astral** | shared/noetic overlays, symbolic landmarks, nonphysical entities | a PSI procedure, once unlocked; **never** automatic spying on a room you cannot enter | **locked** (GM only) |

Two axes that are **not** places on the map:

* **Space/Time vs Time/Space** — embodied material experience versus nonphysical temporal–spatial
  experience. A scene must say which one it is in; a Time/Space scene is not "the same street at night".
* **Third vs Fourth density** — a designation of consciousness/development, **not** a spatial
  dimension and **not** invisibility. A fourth-density being on a Helsinki street is physically visible;
  a third-density person may have involuntary dream or near-death astral experiences, while deliberate
  projection needs its rules permission.

**Interdimensional hypothesis** stays an **in-world explanation and research controversy** until the
author approves a cosmology. It may be argued about, tested and disbelieved in play; it may not be used
as a blanket explanation of every NHI encounter.

### Underground Helsinki

Real tunnels, service passages, metro and harbour infrastructure exist and are **not automatically
traversable**: verify actual public access before making any real location enterable, and mark every
2045 addition as fictional. A tunnel that exists is not a tunnel the player may walk into.

---

## 10. Layered site record

One record per place, referenced from the district card, the faction sheet and the encounter card.

```yaml
# EXAMPLE ONLY — NOT CANON
site_id: hel_site_kurvi_transit
district_ref: hel_district_kurvi
physical: { visible: true, scene: "platform and stairwell", routes: ["street", "metro"], access: "public" }
cyber: { visible: "via BCI", access: "ordinary CWN hacking permissions", node_ref: null }
astral: { player_visible: false, gm_only: true, entry: "scripted reveal, Act II or later" }
realm: "space_time (embodied); time_space is a different scene"
density_access: "not a map coordinate; fourth-density beings are visible here"
transition_rule: "physical -> cyber needs a BCI; physical -> astral needs an unlocked ability and the scene gate"
scripted_reveal_gate: "Act I: astral locked. Act II: one scripted glimpse. Act III: procedure available."
known_tunnels: "none verified; do not assert service access"
visibility: { player_knows: ["platform", "stairwell"], gm_only: ["what the maintenance door leads to"] }
gm_secrets: "GM SECRET — author only"
source: "illustrative"
```

**Stable keys.** `hel_site_*`, `hel_district_*`, `hel_faction_*`, `hel_npc_*`, `hel_nhi_*`,
`hel_corp_*`, `hel_gang_*`, `hel_org_*`. A later Python adapter must be able to load **one record per
entity** and resolve every cross-reference; no entity may be defined in two files.

---

## Unresolved decisions in this document

| # | question | blocks |
| --- | --- | --- |
| C1 | Which real Helsinki districts are playable, and what are their two CWN traits? | every mission location |
| C2 | What are the city's two main problems (CWN p. 114)? | the campaign's background pressure |
| C3 | Is PSI registration a health record, a weapons licence, or both? | Act II's central conflict |
| C4 | Which organisations are canon, and where do their competences actually collide? | every jurisdiction scene |
| C5 | Which underground locations may the player enter, and which are merely referenced? | traversable map, safety of real-place claims |
| C6 | Does the astral layer exist in this campaign's cosmology at all, or only in rumours? | the Act III gate |

*Record answers here, in this file, with a date and the author's name.*
