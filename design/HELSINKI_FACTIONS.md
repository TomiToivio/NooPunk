# Helsinki 2045: Factions
**Human-readable RPG worksheet for Tomi | #1141 Phase 1 | Examples are NOT CANON**

This document is for writing about **local groups that shape the Helsinki campaign**. Write the description as you would for a tabletop sourcebook. You do not need to write YAML, JSON, Python, IDs or machine-readable statistics. Agents will convert approved prose into data and code in **Phase 3**, after adding it to the rulebook.

**Rules inspiration:** *Stars Without Number Revised* (SWN), *Factions* (approximately printed pp. 211–227), especially faction goals, Force, Cunning, Wealth, FacCreds and assets. *Worlds Without Number* (WWN) major projects and *Ashes Without Number* (AWN) enclaves are alternatives where appropriate, not extra actions for the same organization. Use *Cities Without Number* (CWN) as the immutable character-level system.

**Scope:** Describe local participants in the first Europol rookie campaign. A gang, union, corporation or agency is **not automatically a mechanical faction**. If it does not manage assets and take strategic faction turns, give it a readable organization description in [The City](HELSINKI_CITY.md) instead. Galactic organizations get a Helsinki-facing presence here only if play needs one. Existing global factions remain in [NHI factions](../docs/world/NHI_FACTIONS_922.md).

**Status labels used in this file.** `AUTHOR CANON` — written and approved by you. `REPOSITORY CANON` —
already established elsewhere in this repository; follow the link rather than restating it. `EXAMPLE ONLY /
NOT CANON` — scaffolding, to be overwritten. `OPEN` — an undecided question. `GM SECRET` — true in the GM's
notes, withheld from the players.

**Contents**

1. How to use the worksheet
2. 1. A faction's identity and situation
3. 2. SWN faction characteristics
4. 3. Cunning, Force and Wealth assets
5. 4. A faction turn at the tabletop
6. 5. Choosing SWN, WWN or AWN
7. 6. Relationships, reputation and campaign visibility

## How to use the worksheet

Each example is invented and **NOT CANON**. Replace it with your own prose. Where tabletop numbers help, a **simple RPG-style stat line or table** is fine. Agents verify printed mechanics and write the structured data later. Do not guess rulebook figures. The author can explicitly label material **Author canon**, **Open**, or **GM secret**.

## 1. A faction's identity and situation

**Example only: Helsinki Municipal Infrastructure Unit (NOT CANON)**

**Who they are:** A fictional municipal group entrusted with keeping power, water and transit systems working during emergencies. Its employees believe they do thankless but essential work. Politicians treat the unit as both a public service and a convenient scapegoat.

**What they want:** A reliable emergency network and fewer contractors with hidden obligations.

**Where they operate:** Greater Helsinki infrastructure and public-service facilities.

**Who they rely on:** Municipal officials, local technicians, labor unions and selected commercial contractors.

**Who opposes them:** Rival suppliers and anyone profiting from disruption.

**How people see them:** Unremarkable until something breaks. Then everybody suddenly becomes an expert on their work.

**Current trouble:** The unit discovers that an obsolete access contract still authorizes a private organization to touch its systems.

**Campaign hook:** A Europol liaison asks the player to trace the contract without turning a routine infrastructure dispute into a jurisdictional incident.

**Possible SWN game role:** A strategic faction only if Tomi wants this actor to own assets, pursue faction goals and participate in the faction turn. Otherwise it remains a normal city organization.

**Your version (Tomi writes here):**

<!-- Tomi writes below -->

*Faction name, background, purpose, people, territory, allies, adversaries, public image, secret interests, current agenda and relationship to the investigators.*

---

## 2. SWN faction characteristics

Use **Force, Cunning and Wealth**, the published SWN faction goals, tags, assets and FacCreds. These are game mechanics, not a substitute for the story. Only choose values after checking the appropriate SWN source. A reputation score on a character sheet is **not** a faction statistic: the faction's statistics
describe its **strength**, while its opinion of a person is a separate note written in words.

**Example only: The infrastructure unit as a game piece (NOT CANON)**

| SWN item | Example of what Tomi would decide |
| --- | --- |
| **Goal** | Keep essential services functioning through a major crisis |
| **Force** | To be chosen from the printed SWN rules |
| **Cunning** | To be chosen from the printed SWN rules |
| **Wealth** | To be chosen from the printed SWN rules |
| **FacCreds** | To be assigned using SWN faction procedures |
| **Faction tags** | Public mandate; dependent on contractors (fictional descriptors, not automatically published SWN tags) |
| **Base of Influence** | To be chosen when the author decides where the group can act |
| **Assets** | To be chosen from published lists if this becomes a mechanical faction |

**Writing prompts:** How powerful is this group? What resources does it control? What can it plausibly achieve in one strategic turn? Does its influence differ between districts? Which exact published faction tags match it?

**Your version (Tomi writes here):**

<!-- Tomi writes below -->

*Describe the faction's practical strengths and weaknesses. Add a plain SWN stat line when you want to choose numbers. Agents will later validate and encode it.*

---

## 3. Cunning, Force and Wealth assets

**Assets are not mere adjectives.** SWN treats them as game pieces with published abilities, costs and hit points. The following three are real named catalogue examples recorded in the repository's SWN asset reference; they are **not assigned to any Helsinki faction**. Consult the printed edition before making final purchases.

| Type | Printed asset example | Illustrative role | Recorded cost / HP |
| --- | --- | --- | --- |
| **Cunning** | False Front | A concealed network or organization | Cost 1; HP 2 |
| **Force** | Hitmen | An armed clandestine asset | Cost 2; HP 1 |
| **Wealth** | Franchise | Economic presence or expansion | Cost 2; HP 3 |

*Source note:* Local SWN asset extraction in [data/rules/swn_faction_assets.json](../data/rules/swn_faction_assets.json), with recorded printed pages 219, 221 and 223 respectively. Use the actual SWN text for abilities and conditions; do not infer them from this table.

**Example only: Assets as a story (NOT CANON)**

A fictional infrastructure organization worries that an unknown competitor has a hidden corporate front in Kurvi. At the table, a GM *might* represent the hidden front with a SWN **False Front** asset, if the published rules and the final faction setup permit it. Its location and ownership would be chosen by Tomi, not automatically assigned by this example.

**Writing prompts:** What does this faction own or control? Which assets are political, covert, armed or economic? Where are they located? What do they look like in the story? Which are actually SWN assets and which are ordinary narrative resources?

**Your version (Tomi writes here):**

<!-- Tomi writes below -->

*List the faction's resources in ordinary prose. Add printed asset names and costs only if you want them to matter in faction turns.*

---

## 4. A faction turn at the tabletop

A turn takes **one action** — expand, attack, defend or use an asset — after income is collected.

**Example only: One strategic decision (NOT CANON)**

1. **Situation:** The fictional infrastructure unit learns that its archive may be compromised.
2. **Goal:** Protect the integrity of the system.
3. **Resources:** The GM checks the group's actual SWN statistics, assets and available FacCreds.
4. **Action:** The faction chooses one legal action under the published SWN turn procedure.
5. **Resolution:** The table makes the required rolls and applies the appropriate printed asset and action rules. No outcome is assumed here.
6. **Consequences:** Record what changed and how the event becomes a player-facing rumor, case lead or political development.

**Writing prompts:** Does the campaign use a faction turn from Act I or only later? Which actors move during downtime? How does a strategic event become a rumor, mission or change in district life? Do not give an organization extra actions by simultaneously running SWN and AWN or WWN as separate wallets.

**Your version (Tomi writes here):**

<!-- Tomi writes below -->

*Write a short example turn as a narrative and specify the intended SWN action, assets and rulebook references if chosen.*

---

## 5. Choosing SWN, WWN or AWN

Not every political or social activity should be forced into SWN faction warfare.

| If the story is about… | Consider… | Why |
| --- | --- | --- |
| Organizations competing for strategic influence, assets and goals | **SWN faction turn** | The principal local strategic model |
| A long-term project such as building a bridge or securing a treaty | **WWN major project** | Tracks the endeavor rather than a second faction economy |
| A struggling settlement in an area hit by the NHI Crisis | **AWN enclave** | Tracks survival, resources and community concerns |

**Example only: A crisis settlement (NOT CANON)**

A settlement near an exclusion area is chiefly concerned with medicine, energy, food and safety. It may make more sense to describe it as an AWN enclave than as a SWN faction competing for galactic influence. It cannot collect an entire second set of free SWN actions merely by changing labels.

**Writing prompts:** Which scale of play best captures each organization? If two systems describe it, what distinct subjects do they model, and how will agents prevent double-counting?

**Your version (Tomi writes here):**

<!-- Tomi writes below -->

*Name the group and explain which strategic system, if any, is useful.*

---

## 6. Relationships, reputation and campaign visibility

**Reputation is not a faction statistic.** The faction's numbers describe its strength; how it feels about a
particular person is a separate note, written in words.

**Example only: A damaged relationship (NOT CANON)**

After an investigation embarrasses a municipal supervisor, the rookie is no longer welcome at a particular office. This is a story consequence and could later be represented by a character reputation tag if that optional NoöPunk rule is approved. It does **not** reduce the municipal organization's SWN Force score.

**Writing prompts:** What does the faction think of the player? What does the player know about its real aims? What is concealed until a later campaign act? What changes when the organization wins or loses?

**Your version (Tomi writes here):**

<!-- Tomi writes below -->

*Faction relationships, public and private reputations, reveal schedule, and GM secrets.*

---

## Open author decisions

- Which Helsinki organizations are true mechanical SWN factions?
- Which groups are ordinary local organizations rather than faction-turn actors?
- At what point in the campaign do faction turns begin?
- Which actors have links to Orion, the Confederacy, the Soviet Union or other larger powers?
- Which WWN projects or AWN enclaves are needed, without double-counting resources?

**Author's answers (Tomi writes here):**

*Once approved, your prose goes into the tabletop rulebook first. Agents then create machine-readable faction records and Python behavior, preserving the printed rules and your intended story.*

---

## Unresolved decisions

Answer in this column, in ordinary language, then delete the row.

| Question | Record answers here |
|---|---|
| Which local actors are factions, and which are scenery? | |
| How many factions does the first campaign need? | |
| Does the protagonist's own office take faction turns, and who decides? | |
| Are there non-human actors with local interests, and do they act on the same clock? | |
| Which actors use SWN factions, WWN projects or AWN enclaves? | |
| How does a player character learn that a faction acted? | |

**Answers are prose.** An agent can structure them later, in Phase 3, only if you ask — you never
have to write a data format.
