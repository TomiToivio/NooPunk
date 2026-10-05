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

## Open question: the score scale

**Issue #122 specifies scores on a −10…+10 scale**, with `+10` as the strongest positive
relation and `−10` as the strongest negative. The examples in that issue use that range
throughout (`+8 Loves`, `−9 Hates: Orion infiltration`).

**The live issue #107 implementation uses −100…+100** — `MIN_AFFECT`/`MAX_AFFECT` in
`src/simulation/affect.py`, the `score_range` in `data/world/social_affect_schema.json`,
and the "integer from −100 to +100" wording in `rulebook/4_SOCIAL.md`.

Both are author-specified, and they are not the same scale. This is recorded here rather
than silently reconciled:

* every rule in this section is expressed in **relative** terms, so it holds on either scale;
* **which scale is canonical is the author's decision**, and until it is made, no test,
  example or data file should assume both are interchangeable;
* a 10× rescale is not cosmetic — it changes every stored score, the schema bounds and the
  validation in `affect.py`, so it should land as one deliberate change across all three.

## Questions this section does not settle

The exact seeding rule from Reputation to an unknown NPC's initial attitude, whether a
personal Contact overrides Reputation once a relationship exists, the canonical Affect
vocabulary as a closed list versus free text, and universal numeric increments for
mutation all remain issue #107's to define.
