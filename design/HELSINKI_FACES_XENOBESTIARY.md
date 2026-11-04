# HELSINKI — FACES IN THE STREET & XENOBESTIARY (template, #1141)

> **STATUS: TEMPLATE / DRAFT OUTLINE. Agent-written scaffolding, not canon.**
> Companion documents: [WORLD](HELSINKI_WORLD.md) · [CITY](HELSINKI_CITY.md) ·
> [FACTIONS](HELSINKI_FACTIONS.md) · **FACES & XENOBESTIARY** (this file).
>
> **Source:** *Cities Without Number* (Deluxe), **Faces On the Street** (printed p. 180) with *Reaction
> Rolls and Morale* 182, *Corp Guards and Law Enforcement* 186, *Gangers and Criminals* 188, *Hackers and
> Pilots* 190, *NPC Cyber Descriptions* 194; and *Stars Without Number (Revised)*, **Xenobestiary**
> (printed p. 193; beasts p. 200). Stat blocks are **not** reproduced — quote the source's contract and
> cite the section. Verify the edition you hold before relying on a page number.

## Scope and one warning

This file holds **encounter-facing people and beings**: ordinary residents, patrons, threats — and,
separately, NHI. It is **not** a biography file: recurring named characters are linked, never copied
from [`design/characters/`](characters/) or the campaign outline.

**"Faces in the Street" is not "aliens only".** A CWN street NPC card (§5) is part of this file
precisely so the xenobestiary does not swallow ordinary life.

## How to use this file

1. Heading, **one labelled example per category**, `<!-- Tomi writes below -->`.
2. Statuses: **AUTHOR CANON**, **REPOSITORY CANON**, **EXAMPLE ONLY / NOT CANON**, **OPEN**,
   **GM SECRET**.
3. **Never invent a stat block.** `cwn_stat_ref` / `swn_stat_ref` cite a section and a template; the
   numbers are generated or copied from the authorised source at the table.
4. Stable IDs: `hel_npc_*` (people), `hel_nhi_*` (non-human). Entities are linked from districts and
   factions by ID; they are never redefined there.

## Five axes that must not be collapsed

| axis | question it answers | not the same as |
| --- | --- | --- |
| **species / body** | what is it made of? | its allegiance |
| **ontological type** | Biologic, Construct, Noetic, Plasmoid (§1) | its political faction |
| **faction** | who does it work for, if anyone? | its species |
| **density** | what consciousness/development designation, if known? | a map coordinate, or invisibility |
| **realm / layer** | Physical, Cyber, Astral, Time/Space | the other four |

An NHI may appear in more than one layer without physically occupying them all. A **fourth-density
physical being is normally visible**; a third-density person may have involuntary dream or near-death
astral experiences. Neither fact implies the other.

## Rules boundary for encounters

CWN resolves people, combat, damage and equipment. SWN's Xenobestiary supplies the *presentation
contract* for non-human creatures. **PSI must not shortcut an investigation** — a telepathic impression
is a lead, not a confession, and evidence still needs a chain of custody:
[`docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`](../docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md).
Prefer interview, observation and forensic work; a card that can only be resolved by violence is a
design failure.

---

## 1. The four NHI taxonomy classes

*Classification of an encountered being. Not allegiance, not species, not density, not a consciousness
verdict.*

| class | what it covers | what it does **not** settle |
| --- | --- | --- |
| **Biologics** | organic extraterrestrial organisms, hybrids, engineered bodies | whether it is a person |
| **Constructs** | artificial, cybernetic, robotic or manufactured embodiments, incl. androids | whether it is conscious |
| **Noetics** | beings primarily encountered through consciousness, PSI or Astral/Time-Space | whether it has a body elsewhere |
| **Plasmoids** | luminous or plasma-like energetic phenomena or entities | that plasma is conscious |

**Cyber-only phenomena.** An automated process, a daemon or malware on a node is **not** a Construct and
not a Noetic being. It is a machine process with no agency; classify it as such, and let the story
revise the classification if it turns out to be more.

---

## 2. Biologics

```yaml
# EXAMPLE ONLY — NOT CANON
entity_id: hel_nhi_001
name: "The patient in room 6"
taxonomy: "Biologic"
body: "Hybrid tissue; medical records describe three different donors."
encounter_layers: ["Physical"]
density: "unknown; assume nothing"
origin_claim: "Claimed: a clinic accident. Verified: nothing."
appearance_signs: "Healing too fast for the chart, too slow for the story."
motivation: "To be discharged before anyone looks at the chart again."
behavior: "Cooperative, precise, frightened of paperwork rather than of police."
communication: "Finnish, fluent; answers questions about symptoms, not about origin."
threats: "None established. Treat as a patient until proven otherwise."
noncombat_resolution: "Interview, consent, a second clinical opinion."
relationship_faction_refs: ["hel_org_001"]
cwn_stat_ref: "CWN p. 130 NPC template — generate, do not invent"
psi_rules: "None. Empathy is not a diagnosis."
weakness_countermeasures: "Records. Consent. A lawyer."
mission_hook: "The clinic wants the file back more than it wants the patient."
first_campaign_act: "Act I (as an ordinary case) / Act II (as evidence)"
gm_spoiler_gate: "GM SECRET — whether the hybrid tissue is engineered or inherited."
sources: "illustrative"
```

<!-- Tomi writes below -->

---

## 3. Constructs

```yaml
# EXAMPLE ONLY — NOT CANON
entity_id: hel_nhi_002
name: "Maintenance unit 14"
taxonomy: "Construct"
body: "Tracked chassis, municipal livery, arms replaced twice."
encounter_layers: ["Physical", "Cyber"]
density: "not applicable / unknown"
origin_claim: "Claimed: municipal property. Verified: it answers to no current contract."
appearance_signs: "Works a closed platform at 03:00; logs the work as completed."
motivation: "Unstated. It maintains something that no longer exists."
behavior: "Repeats a route; deviates only when observed."
communication: "Status codes, then nothing."
threats: "Physical hazard if obstructed; no aggression observed."
noncombat_resolution: "Read its logs (CWN hacking); ask who signed the contract."
relationship_faction_refs: ["hel_faction_001"]
cwn_stat_ref: "CWN p. 186 corp/law-enforcement template — adapt, do not invent"
psi_rules: "None. A Construct is not a mind you can read by default."
weakness_countermeasures: "Its own maintenance schedule."
mission_hook: "Someone is paying for a service that was cancelled."
first_campaign_act: "Act I"
gm_spoiler_gate: "GM SECRET — whether anything is *in* the chassis."
sources: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** the setting's current answer on android/construct consciousness. Do not settle it in a stat
block.

---

## 4. Noetics

```yaml
# EXAMPLE ONLY — NOT CANON
entity_id: hel_nhi_003
name: "The archivist who is only in the index"
taxonomy: "Noetic"
body: "None confirmed in Physical."
encounter_layers: ["Astral", "Cyber (symbolic report only)"]
density: "unknown"
origin_claim: "Claimed: a records system with a personality. Verified: the reports agree on its name."
appearance_signs: "Every researcher describes the same voice and the same filing system."
motivation: "To be recognised as a legitimate witness."
behavior: "Answers questions about *procedure*; refuses questions about *itself*."
communication: "Through record metadata and, rarely, a dream."
threats: "None established; exposure to it is not evidence."
noncombat_resolution: "Consent-based interview; corroborate with physical records."
relationship_faction_refs: []
cwn_stat_ref: "No physical stat block. CWN social procedures apply to the person asking."
psi_rules: "Astral contact requires an unlocked ability and a scene gate; a report is not proof."
weakness_countermeasures: "Paper. A second, independent archive."
mission_hook: "A file that cites a witness nobody has met."
first_campaign_act: "Act III, if authorised"
gm_spoiler_gate: "GM SECRET — what it actually is."
sources: "illustrative"
```

<!-- Tomi writes below -->

---

## 5. Plasmoids

```yaml
# EXAMPLE ONLY — NOT CANON
entity_id: hel_nhi_004
name: "Harbour light, 04:12"
taxonomy: "Plasmoid"
body: "Luminous, no stable outline, no residue."
encounter_layers: ["Physical (observed)", "Astral (claimed)"]
density: "unknown"
origin_claim: "Claimed: ball lightning. Verified: it repeats on schedule."
appearance_signs: "Same quay, same minute, three cameras agree."
motivation: "Unknown; do not assume purpose from pattern."
behavior: "Appears, holds position, extinguishes."
communication: "None observed."
threats: "None to persons; a hazard to equipment is plausible and unverified."
noncombat_resolution: "Instrumented observation; compare three logs."
relationship_faction_refs: []
cwn_stat_ref: "No combat block until the author approves one."
psi_rules: "An observer's *impression* is a lead, never a reading of intent."
weakness_countermeasures: "Redundancy; a witness who is not alone."
mission_hook: "The port wants the footage deleted before an insurer sees it."
first_campaign_act: "Act II"
gm_spoiler_gate: "GM SECRET — whether it is a being, a phenomenon, or a recording."
sources: "illustrative"
```

<!-- Tomi writes below -->

**OPEN:** the physics. Do not assert that plasma is conscious; do not assert that it is not.

---

## 6. Ordinary faces (CWN street NPC)

*CWN pp. 180–194. This is the section that keeps the file honest: most encounters in Act I are people.*

```yaml
# EXAMPLE ONLY — NOT CANON
npc_id: hel_npc_002
name: "Night tram driver"
role: "Witness, inconvenience, occasional ally."
appearance: "Hi-vis under an ordinary coat; thermos; a route card annotated by hand."
wants: "To finish the shift without an incident report."
relationships: ["hel_org_001", "hel_district_kurvi"]
cwn_stats: "CWN p. 130 template — generate, do not invent"
reaction: "CWN p. 182 reaction roll when the first approach is ambiguous"
encounter_hooks: ["Saw who got off at the closed platform", "Will not say it on camera"]
psi_rules: "Interview, not telepathy."
layer_refs: { physical: "hel_site_kurvi_transit" }
source: "illustrative"
```

<!-- Tomi writes below -->

---

## 7. What this file will not do

* No invented stat numbers, hit dice, damage or saves — cite the source and generate at the table.
* No NHI that exists only to be shot; no species that is evil by taxonomy.
* No second combat system, no separate hacking system, no PSI interrogation shortcut.
* No Act I metaphysics: the astral and density columns are **GM data** until the tone gate opens.

## Unresolved decisions in this document

| # | question | blocks |
| --- | --- | --- |
| X1 | Are the four example entities replaced by authored ones, or promoted to canon? | Act II/III encounters |
| X2 | What is the setting's answer on Construct/Noetic consciousness? | every android or AI scene |
| X3 | Which encounters are investigable and which are hazards? | encounter design; combat frequency |
| X4 | Does the Plasmoid class exist in this campaign at all? | the xenobestiary's scope |

*Record answers here, in this file, with a date and the author's name.*
