# Faction system terminology

Status: **NOÖPUNK NATIVE, issue #122.** This section fixes the *vocabulary* for the faction
system. It defines no new mechanics: the representation, the graph domains and the
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

## Canonical score scale

**Issue #144 resolves the earlier scale conflict.** Contacts, Motivations, Faction
Reputation and other Affect edges use the canonical **−10…+10** score range.

- **+10** = strongest positive relation, love, absolute loyalty or iconic standing
- positive = Likes / trusts / supports unless a more specific Affect is recorded
- **0** = explicitly neutral
- negative = Dislikes / distrusts / opposes unless a more specific Affect is recorded
- **−10** = strongest negative relation, hate, mortal-enemy or irreconcilable hostility

An absent edge still means **unknown**, not neutral.

The engine model and JSON schema must use the same −10…+10 bounds.

## Faction taxonomy and campaign scope

Faction is the umbrella gameplay concept. Useful top-level types include **Political,
Criminal, Civil Society / Knowledge, Religious / Esoteric, Corporate, Governmental, and
NHI Factions / Civilizations**. These are navigation and rules categories, not rigid
ontologies; tags and multiple classifications are allowed.

Governmental factions use a scale such as local, regional, nation-state, federal /
supranational, global / planetary, or later interplanetary. Agencies may be nested
factions with their own Reputation and internal politics.

For NHI, keep **ontology/type separate from political faction**. Core types include
Biologics, Constructs, Plasmoids and Noetics. Process Intelligence, Ecology, Assemblage,
Collective, Geotic, Hybrid/Composite and Anomaly/Unclassified may be descriptors or
extended categories as appropriate.

The default campaign is **Helsinki-centered**. The taxonomy may represent a huge world,
but the campaign should introduce only a few factions that create actual relationships,
choices, conflicts or story hooks around Helsinki.

## Multiple memberships and starting Reputation

A character may belong to several factions simultaneously for different reasons:
employment, politics, residence/community, profession, religion/esotericism, gang/network
or family/clan/community.

During character generation, allocate **10 positive Reputation points** between **two or
three factions**, such as **6/4** or **5/3/2**. Negative Reputation normally comes from
Lifepath events, enemies, faction conflict, campaign events or an explicit concept.


## Questions this section does not settle

The exact seeding rule from Reputation to an unknown NPC's initial attitude, whether a
personal Contact overrides Reputation once a relationship exists, the canonical Affect
vocabulary as a closed list versus free text, and universal numeric increments for
mutation all remain issue #107's to define.
