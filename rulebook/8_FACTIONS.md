# Faction system terminology

Status: **NOÖPUNK NATIVE, issue #122; extended by issue #144.** This section fixes the
*vocabulary* for the faction system and, since #144, the faction **taxonomy**, the generic
faction **schema**, multi-faction membership, and the canonical **−10…+10** score scale.
It defines no resolution mechanics: the representation, the graph domains and the
inheritance rules are issue #107 and live in `rulebook/4_SOCIAL.md` and
`src/simulation/affect.py`.

Its purpose is that the same terms mean the same thing in the rulebook, character data,
faction data, NPC generation, code and visualization.

## The one relationship shape

Every social and ideological fact in NoöPunk is one signed, labelled, directional edge:

```text
relationship = { source, target, score, affect? }
```

The **layer** decides what the edge means:

| Layer | Meaning |
| --- | --- |
| **Contact** | a personal social connection |
| **Motivation** | what a character desires, supports, seeks, resists or opposes |
| **Faction Reputation** | a faction's or actor's standing toward a character |
| **Faction US / FRONTIER** | a formation's ideological support or opposition |

A score of **0** is an explicit **neutral** relation. **No edge is not the same thing as a
stored 0**: an absent edge means *unknown* (the actor has no relation to the target at all),
while a stored 0 means a relation that is consciously neutral. This distinction is canon
(issue #107) and is why the score is a labelled, directional edge rather than a single
sentiment axis.

## Contacts

A **Contact** is a specific person the character knows personally or socially.

A Contact carries a score and optionally a specific **Affect**. Where no specific Affect is
needed, the default is **Likes** for a positive score and **Dislikes** for a negative one.

Contacts are **personal relationships**, not general standing with a group. Standing with a
group is Faction Reputation, below.

## Motivations

**Motivations** describe what a character desires, supports, seeks, resists or opposes:
demands, commitments, values, goals, identities and objects of affective investment. They
use the same score scale and may carry a specific Affect.

## Faction Reputation

**Faction Reputation** is the standing a character has **with a Faction**. It is not the
character's opinion of that faction: `character → faction Likes` and `faction → character
Distrusts` can both hold, because the edge is directional.

Reputation matters most when meeting **new contacts who do not know the character
personally**. In that case the NPC may initially react according to the character's
Faction Reputation with the NPC's faction, and a personal Contact relationship may later
diverge from that inherited attitude. Issue #107 owns the exact seeding rule.

## Faction ideology: US and FRONTIER

A faction is modelled as a changing discourse, not a personality package:

```text
Faction = US  (constitutive, positive affects)
        + FRONTIER (antagonistic, negative affects)
```

**US** holds what the formation identifies with, supports, demands or treats as part of
its collective subject: **Goals**, **Empty Signifiers**, **Actors**, and other canonical
objects.

**FRONTIER** holds what the formation defines itself against — the same object kinds,
marked as the constitutive outside. Mere disagreement or dislike is not automatically a
frontier.

This adapts the Formula of Populism as a general faction/discourse model. It is **not a
populism classifier**: populist and non-populist formations alike articulate collective
subjects, demands, affective investments and antagonistic frontiers. The distinction is a
structured ideological boundary, not a flavour-text alignment field.

## Affect vocabulary

**Affect** is the semantic label on an edge. The canonical set includes `Knows`, `Likes`,
`Trusts`, `Supports`, `Identifies With`, `Loves`, `Protects`, `Pursues`, `Fears`,
`Distrusts`, `Hates` and `Opposes`.

The label and the score both matter. `Fears −7`, `Hates −7` and `Opposes −7` share a
polarity but differ in meaning, so an Affect is never reducible to its score. Multiple
labelled edges may connect the same source and target, which is how a character can support
and fear AGI at once.

Signifier roles — `nodal_point`, `floating_signifier`, `empty_signifier`,
`ordinary_signifier` — are marked only where an articulated role warrants it. Ambiguity
alone never makes a signifier floating or empty.

## Social network representation

The faction system projects into these graph layers:

1. **Character ↔ Character** — the Contact graph, signed weighted edges with optional Affect labels.
2. **Character ↔ Motivation** — what individuals desire or oppose.
3. **Character ↔ Faction** — Faction Reputation, directional.
4. **Faction ↔ Actor** — actors in US or FRONTIER.
5. **Faction ↔ Goal** — goals supported or opposed.
6. **Faction ↔ Empty Signifier** — signifiers attached to US or FRONTIER.
7. **Faction ↔ Faction** — alliances, affinities, rivalries and antagonisms, derived from
   overlaps and conflicts in US/FRONTIER rather than stored as a separate opinion field.

These project into actor-to-actor, faction-to-faction or mixed multilayer networks for
analysis and visualization.

## Canonical score scale: −10…+10

**Canonical: every Faction, Reputation, Contact, Motivation and relationship score uses
`−10…+10`.** Issue #144 makes the author's decision, which issue #122 had recorded as open.

| Score | Generic meaning |
| --- | --- |
| **+10** | love / absolute loyalty / iconic standing |
| positive | likes, trusts, supports |
| **0** | neutral, unknown, or no meaningful relationship |
| negative | dislikes, distrusts, opposes |
| **−10** | hate / mortal enemy / irreconcilable hostility |

The two ends are deliberately symmetrical, and the range sits visually next to NoöPunk's
1–10 STAT and Skill scale.

**Affect overrides the generic wording.** The label carries the meaning, not the number:
`Contact +6 Trusts`, `Contact −7 Fears`, `Faction Reputation +5`, `Motivation +8 dreams of`,
`Motivation −6 opposed to` are all canon examples. `Fears −7`, `Hates −7` and `Opposes −7`
share a polarity and differ in meaning.

A stored **0** is an explicit *neutral* relation; **no edge** means *unknown*. The two are
never the same thing (see above).

### Why this replaced the older 100-point band

The earlier implementation used a wider 100-point relationship band (`MIN_AFFECT`/`MAX_AFFECT` in
`src/simulation/affect.py`, the `score_range` in `data/world/social_affect_schema.json`, and
the wording in `rulebook/4_SOCIAL.md`). Issue #144 replaces that scale, so this landed as
**one deliberate change across all three** rather than a cosmetic 10× divide: every stored
score, the schema bounds and the runtime validation moved together.

Negative Reputation is not bought with the positive starting pool. It arises from Lifepath
events, enemies, faction conflicts, traits and campaign events (see the Character Generation
chapter).

## Questions this section does not settle

The exact seeding rule from Reputation to an unknown NPC's initial attitude, whether a
personal Contact overrides Reputation once a relationship exists, the canonical Affect
vocabulary as a closed list versus free text, and universal numeric increments for
mutation all remain issue #107's to define.


## Faction taxonomy

**Faction** is the umbrella gameplay concept. Every faction uses the same core machinery —
Reputation, Contacts, Motivations, Affect, ideology, allies and enemies, network position,
institutional resources, and parent/subfaction relationships — whatever its organizational
form. The type is a **navigation label**, not a different rules system.

The taxonomy below defines the **types the system can represent**. It is expandable, and the
rulebook must not turn the default campaign into an encyclopedia: see *Campaign scope* below.

### 1. Political

Political parties, electoral coalitions, ideological movements, activist movements,
revolutionary or insurgent movements, lobbying blocs, and think tanks when they act primarily
as political actors. Political factions may be institutional or informal.

### 2. Criminal

Street gangs, mafias, cartels, smuggling networks, hacker gangs, black-market organizations,
and criminal mercenary networks. Hybrid political/criminal factions are allowed.

### 3. Civil society and knowledge

NGOs, universities, research institutes, foundations, professional associations, scientific
networks, advocacy organizations, and media organizations. `academic`, `research` and
`knowledge` are **tags**, not separate top-level types.

### 4. Religious and esoteric

Churches, religions, denominations, cults, mystery schools, occult orders, new religious
movements, and psychic schools. In NoöPunk some groups socially classified as "cults" may have
genuine interaction with Noetics or other NHI, while major religions may interpret the same
phenomena through very different frameworks. Nothing about this type decides whether a group
is right.

### 5. Corporate

Corporations, conglomerates, startups, cooperatives, corporate alliances, platform companies,
private military/security companies, and megacorporations. **Organizational type does not
imply ideology**: a cooperative and a megacorp are both corporate factions.

### 6. Governmental

Model jurisdiction with a **scale** field rather than a second system:

| Scale | Example |
| --- | --- |
| Local | Helsinki |
| Regional | Uusimaa |
| Nation-state | Finland |
| Federal / supranational | the EU |
| Global / planetary | the UN |
| Interplanetary / Solar System | reserved for later |

Government agencies are frequently **independent nested factions** with their own Reputation,
conflicts, alliances and internal politics. Finland is a faction; Suojelupoliisi is a faction
inside Finland. The EU is a faction; Europol is a faction inside the EU structure. The UN is a
faction; **UNSA** is a faction inside it.

### 7. NHI: type is not faction

**NHI ontology and NHI politics are separate fields.** An NHI's substrate or type does not
determine its political allegiance, and a single type contains many unrelated factions.

Core types:

- **Biologics**
- **Constructs**
- **Plasmoids**
- **Noetics**

Extended categories and descriptors:

- **Process Intelligences** — intelligence exists primarily as an ongoing process rather than
  a discrete organism. The strongest candidate for a further **formal class**.
- **Ecologies** — an ecosystem, not an organism, is the relevant intelligent entity.
- **Assemblages** — intelligence emerges from heterogeneous interacting components.
- **Collectives** — swarm minds, hive minds, civilization-scale or distributed consciousness.
- **Geotics** — intelligence instantiated in apparently ordinary matter or in planetary or
  stellar structures.
- **Hybrids / composite entities** — combinations across substrate classes.
- **Anomalies / unclassified** — phenomena whose ontology cannot be established reliably.

Assemblage, collective, hybrid and distributed are best treated as **cross-cutting
descriptors** rather than further top-level classes. Categories may always be combined.

Worked examples:

| Entity | Classification |
| --- | --- |
| Confederacy Garden Mind 7 | Noetic + Process + Collective + Distributed |
| Orion reconnaissance probe | Construct + Individual + Embodied |
| Sentient Jovian plasma ecology | Plasmoid + Ecology + Distributed |
| Earth Noösphere | Noetic + Process + Collective + Planetary |
| Unresolved Ö-Mappi case | ANOMALY / classification disputed |

## Generic faction schema

Fields every faction may carry. Multiple classifications and tags are allowed.

| Field | Meaning |
| --- | --- |
| Name | canonical name, plus aliases and nicknames |
| Faction type | one or more of the seven types above |
| Scale | local → planetary (see Governmental) |
| Territory / domain | where it operates |
| Members / constituents | who belongs |
| Ideology | its US and FRONTIER (see above) |
| Motivations | what it pursues, supports, resists |
| Reputation | standing, directional (`−10…+10`) |
| Contacts | key people and their relationship to the faction |
| Allies | aligned factions |
| Enemies | opposed factions |
| Network position | connectivity, reach, centrality |
| Institutional resources | what it can actually deploy |
| Parent faction | the faction that contains it |
| Subfactions | factions inside it |
| Relevant tags | free descriptors (`academic`, `law-enforcement`, …) |

NHI factions additionally carry: dominant NHI substrate/type, civilization/species/lineage,
polarization or ethical orientation, relationship to humanity, and relationship to
quarantine/disclosure.

Examples:

- **Europol** = Governmental / Supranational / Law Enforcement / Intelligence
- **Psychic UFO cult** = Religious / Noetic / Transnational / Networked

The primary category is for rules and navigation, **not a rigid ontology**.

## Characters belong to multiple factions

A character may simultaneously belong to several factions, for different reasons:

- the faction they **work for** (in the default campaign, UNSA — see §38)
- a faction they **personally support**
- a faction based on **where they live**
- a professional or academic faction
- a religion, cult or movement
- a gang or social network
- a family, clan or community, if later modelled as factions

**Membership is not ideological loyalty.** A character can belong institutionally to one
faction, support a second, and dislike a third. Faction Reputation is directional and is
tracked per faction and per actor, so these coexist without contradiction.

## Starting Reputation allocation

During character generation the player receives **10 positive Reputation points** to divide
between **two or three factions**, for example **6 / 4** or **5 / 3 / 2**.

Employer membership is **granted separately** by the campaign template rather than bought
from this pool: in the default campaign the character is a UNSA agent by default (§38) and
spends the 10 points on the personal, local, professional or ideological ties that make them
an individual rather than a uniform.

**Negative Reputation is not bought with the positive pool.** It emerges from Lifepath
events, enemies, faction conflicts, traits and campaign events. The exact negative side is
the author's to define.

## Campaign scope

The default NoöPunk campaign is centred on **Helsinki** and its Finnish / Nordic / EU
operational environment, so the rulebook introduces only a **small number of factions
directly relevant to play there**. Prioritize factions that:

- employ, command, assist or investigate the player characters;
- are physically or politically active in Helsinki;
- provide useful Contacts, Reputation or Motivations;
- are likely allies, rivals, suspects or adversaries in early scenarios;
- connect Helsinki operations to Finland, the EU and UNSA.

Distant governments, corporations, NHI civilizations, cults and political movements are
**added when a scenario, campaign arc or supplement needs them** — not pre-populated here
merely because the model can represent them. The default campaign should feel socially dense
but legible: a small network of recurring factions around Helsinki, with the larger world
visible behind them.

Named factions are therefore **not** listed in this chapter. They live in `FACTIONS.md` and in
scenario documents, where a specific campaign can justify them.
