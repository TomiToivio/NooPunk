# Faction system terminology

Status: **NOÖPUNK NATIVE, issues #107, #122 and #144.**

This chapter defines the canonical vocabulary and faction taxonomy used by the rulebook,
character data, faction data, NPC generation, code and visualization.

## The one relationship shape

Every social and ideological fact in NoöPunk is a signed, labelled, directional edge:

```text
relationship = { source, target, score, affect? }
```

| Layer | Meaning |
| --- | --- |
| **Contact** | a personal social connection |
| **Motivation** | what a character desires, supports, seeks, resists or opposes |
| **Faction Reputation** | a faction's or actor's standing toward a character |
| **Faction US / FRONTIER** | a formation's ideological support or opposition |

All relevant social scores use the canonical **-10 to +10** range.

- **+10** = Love, absolute loyalty, or iconic standing
- **positive** = likes, trusts, supports
- **0** = explicit neutrality
- **negative** = dislikes, distrusts, opposes
- **-10** = hate, mortal-enemy status, or irreconcilable hostility

No edge means **unknown**, not neutral. A stored 0 is consciously neutral.

## Contacts

A **Contact** is a specific person the character knows personally or socially. A Contact
has a score and optionally a specific **Affect**. Where no specific Affect is needed,
positive values default to **Likes** and negative values to **Dislikes**.

Contacts are personal relationships, not general standing with a group.

## Motivations

**Motivations** describe what a character desires, supports, seeks, resists or opposes.
They use the same -10…+10 scale and may carry a specific Affect such as **Dreams of**,
**Supports**, **Fears** or **Opposed to**.

## Faction Reputation

**Faction Reputation** is a faction's or social actor's standing toward a character. It is
directional and is not the character's own opinion of the faction.

Reputation matters especially when a new contact does not know the character personally.
Faction Reputation can seed an initial attitude; a later personal Contact relationship may
diverge. Faction membership supplies starting conditions, not mind control.

## Characters and multiple factions

A character may belong to several factions simultaneously for different reasons: employer,
political support, place of residence, profession, university, religion, movement, gang,
community or another social tie. Institutional membership does not imply ideological loyalty.

During character creation, a player receives **10 positive Faction Reputation points** and
splits them between **two or three factions**, for example **6 / 4** or **5 / 3 / 2**.
In the default campaign, UNSA employer membership is granted by the campaign template;
the 10-point pool represents the character's actual standing and may include UNSA.
Negative Reputation normally comes from Lifepath events, enemies, faction conflicts,
campaign events or an explicit character concept rather than from spending this pool.

## Faction taxonomy

**Faction** is the umbrella gameplay concept. The following types are an expandable
navigation taxonomy, not a demand to populate the setting with hundreds of organizations.

1. **Political Factions** — parties, electoral coalitions, ideological and activist
   movements, insurgencies, lobbying blocs and political think tanks.
2. **Criminal Factions** — gangs, mafias, cartels, smugglers, hacker gangs, black markets
   and criminal mercenary networks.
3. **Civil Society and Knowledge Factions** — NGOs, universities, research institutes,
   foundations, professional associations, scientific networks, advocacy groups and media.
4. **Religious and Esoteric Factions** — churches, religions, denominations, cults,
   mystery schools, occult orders, new religious movements and psychic schools.
5. **Corporate Factions** — corporations, conglomerates, startups, cooperatives,
   corporate alliances, platforms, private military/security companies and megacorps.
6. **Governmental Factions** — governments and agencies, with jurisdiction represented
   by **scale**: Local, Regional, Nation-state, Federal/Supranational, Global/Planetary,
   and later Interplanetary/Solar System where useful.
7. **NHI Factions / Civilizations** — civilizations, polities, coalitions, swarms, hives,
   machine polities, Noetic collectives, expeditions, orders, commercial networks,
   dissident movements and other NHI organizations.

Types may be combined or tagged. A cooperative and a megacorporation can both be Corporate;
a political-criminal hybrid can carry both labels. The primary type is for navigation and
rules, not a rigid ontology.

Government agencies can be nested factions with their own Reputation and politics:
Finland may contain Suojelupoliisi; the EU may contain Europol; the UN contains UNSA.

## NHI ontology is not NHI allegiance

An NHI's **type / ontology** and its **faction / political organization** are separate.
Substrate never determines political allegiance.

Core NHI types:
- **Biologics**
- **Constructs**
- **Plasmoids**
- **Noetics**

Useful extended categories/descriptors:
- **Process Intelligences** — intelligence primarily exists as an ongoing process;
- **Ecologies** — an ecosystem is the relevant intelligent entity;
- **Assemblages** — intelligence emerges from heterogeneous components;
- **Collectives** — swarm, hive, civilization-scale or distributed minds;
- **Geotics** — intelligence instantiated in ordinary matter or planetary/stellar structures;
- **Hybrids / Composite entities** — combinations across substrate classes;
- **Anomalies / Unclassified** — ontology cannot yet be established reliably.

Process Intelligence is the strongest candidate for a future additional formal class.
Assemblage, Collective, Hybrid, Distributed and similar terms are usually cross-cutting
descriptors.

Examples:
- Confederacy Garden Mind 7 = Noetic + Process + Collective + Distributed
- Orion reconnaissance probe = Construct + Individual + Embodied
- sentient Jovian plasma ecology = Plasmoid + Ecology + Distributed
- Earth Noösphere = Noetic + Process + Collective + Planetary
- unresolved Ö-Mappi case = Anomaly / classification disputed

## Generic faction schema

A faction may record:
- Name
- Faction type
- Scale
- Territory / domain
- Members / constituents
- Ideology
- Motivations
- Reputation
- Contacts
- Allies
- Enemies
- Network position
- Institutional resources
- Parent faction
- Subfactions
- Relevant tags

NHI factions may additionally record dominant NHI substrate/type,
civilization/species/lineage, polarization or ethical orientation, relationship to humanity,
and relationship to quarantine/disclosure.

## Faction ideology: US and FRONTIER

A faction is modelled as a changing discourse, not a personality package:

```text
Faction = US  (constitutive, positive affects)
        + FRONTIER (antagonistic, negative affects)
```

**US** contains Goals, Empty Signifiers, Actors and other objects the formation identifies
with, supports or treats as part of its collective subject.

**FRONTIER** contains the same object kinds when the formation defines them as a
constitutive outside. Mere disagreement or dislike is not automatically a frontier.

This adapts the Formula of Populism as a general faction/discourse model. It is **not a
populism classifier**.

## Affect vocabulary

**Affect** is the semantic label on an edge. The canonical set includes `Knows`, `Likes`,
`Trusts`, `Supports`, `Identifies With`, `Loves`, `Protects`, `Pursues`, `Fears`,
`Distrusts`, `Hates` and `Opposes`.

The label and score both matter. `Fears -7`, `Hates -7` and `Opposes -7` have the same
polarity but different meanings. Multiple labelled edges may connect the same source and
target.

Signifier roles — `nodal_point`, `floating_signifier`, `empty_signifier`,
`ordinary_signifier` — are marked only where an articulated role warrants it.
Ambiguity alone never makes a signifier floating or empty.

## Social network representation

1. **Character ↔ Character** — Contact graph.
2. **Character ↔ Motivation** — individual desires and opposition.
3. **Character ↔ Faction** — Faction Reputation and membership.
4. **Faction ↔ Actor** — actors in US or FRONTIER.
5. **Faction ↔ Goal** — goals supported or opposed.
6. **Faction ↔ Empty Signifier** — signifiers attached to US or FRONTIER.
7. **Faction ↔ Faction** — alliances, affinities, rivalries and antagonisms derived from
   overlaps and conflicts in US/FRONTIER rather than stored as a separate opinion field.

## Default-campaign scope

The default campaign is centered on **Helsinki** and its Finnish, Nordic, EU and UNSA
operational environment. Keep the active faction roster deliberately small and socially
dense. Prioritize factions that employ, assist, investigate, oppose or otherwise matter to
the PCs. Do not add organizations merely to fill taxonomy slots.

The recurring institutional spine is **Suojelupoliisi → Europol / EU structures → UNSA**.
One or two additional local political, scientific, corporate, criminal, activist or
religious/esoteric factions may enter when a scenario actually needs them. NHI factions
should likewise become named campaign actors only when relevant.

## Questions this section does not settle

The exact numeric procedure for seeding an unknown NPC's attitude from Reputation, universal
score increments for relationship change, and whether the Affect vocabulary becomes a closed
list remain later design questions.
