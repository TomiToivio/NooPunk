# Social and ideological mechanics

Status: NOÖPUNK NATIVE, issues #107 and #144.

NoöPunk uses one representation for Factions, Motivations, Reputation and Contacts:

```text
Target | Affect | Affect Score
```

Affect is the semantic relation, for example Knows, Likes, Trusts, Supports, Identifies
With, Loves, Protects, Pursues, Fears, Distrusts, Hates, or Opposes. **Affect Score is an
integer from -10 to +10.** Positive means positive investment, negative means negative
investment, and zero is an explicit neutral relation. No edge means unknown.

The label and score both matter. Fears -7, Hates -7 and Opposes -7 have similar polarity
but different meanings. Multiple labelled edges may connect the same source and target.
All edges are directional.

## General edge

Fields: source, source_type, target, target_type, affect, affect_score, domain, metadata.
Domains are faction_us, faction_frontier, motivation, reputation, and contact. Metadata
may record evidence, origin, inherited_from, created_at and updated_at.

The engine-neutral reference model is `src/simulation/affect.py`; schema metadata lives in
`data/world/social_affect_schema.json`.

## Factions: US + FRONTIER

NoöPunk represents each faction as a changing discourse:

```text
Faction = US^(positive or constitutive affects) + FRONTIER^(negative or antagonistic affects)
```

This adapts the Formula of Populism as a general faction/discourse model. It is not a
populism classifier. US may contain demands, identities, allied factions, individuals,
technologies and signifiers. FRONTIER accepts the same target types but marks the
constitutive outside. Mere disagreement or dislike is not automatically a frontier.

The canonical faction types, generic faction schema, NHI ontology/faction distinction,
government scale ladder and Helsinki campaign scope are in `rulebook/8_FACTIONS.md`.

## Motivations and faction inheritance

A Motivation is a personal demand, commitment, value, goal, identity or object of affective
investment represented by the same edge.

Faction membership supplies starting conditions, not mind control. For multiple factions,
copy non-conflicting edges; combine the same target plus Affect label by arithmetic mean;
retain different labels toward the same target as explicit ambivalence; let an explicit
personal Motivation override an inherited edge with the same target plus label; retain
`inherited_from` provenance.

## Reputation

Reputation is a directional Affect edge from a faction or social actor to a character. It
is not the character's opinion of that faction. A character may belong to several factions
at once.

During character creation, the player receives **10 positive Reputation points** divided
between **two or three factions**, such as **6 / 4** or **5 / 3 / 2**. Default UNSA
membership is supplied by the campaign template; the player may still assign some of the
10 points to UNSA to represent stronger standing. Negative Reputation normally arises from
Lifepath events, enemies, conflicts, campaign events or an explicit concept.

## Contacts

A Contact is a specific PC or NPC known personally or socially. Positive and negative
relations use the same -10…+10 graph. Unknown people have no Contact edge.

Character creation starts a small playable graph of friends, professional contacts,
family/community ties, patrons/mentors and possible enemies. Each Contact records identity,
role, faction if known, relationship, Affect label/score, why you know them, what they want,
what they can realistically do and reciprocity.

## Unified social/discourse graph

Factions, Motivations, Reputation and Contacts are domains of one heterogeneous graph.
It supports friends-of-friends, brokers, introductions, alliances, frontiers, faction
memberships, social distance, reputation propagation, party formation, mission hooks and
discourse-network analysis.

## Theory in RPG terms

The model borrows a relational vocabulary from Laclau and Mouffe: articulation,
equivalence/difference, antagonism, nodal/floating/empty signifiers, political subjects,
affective investment and hegemony. Co-occurrence is not articulation; difference is not
antagonism; ambiguity is not emptiness; sentiment is not affective investment; frequency is
not hegemony.

## Change over time

Affects are mutable state. Missions, betrayal, rescue, propaganda, ideological conversion,
trauma, faction schism, Disclosure, relationships, war and new evidence may change them.
Deterministic mechanics own numeric mutation when procedures define it; LLM narration may
explain resolved change but must not invent scores.

See `FACTIONS.md` for starter content and `docs/design/GAMEPLAY_LOOP.md` for the
text-RPG architecture.

## UNSA campaign frame

The default NoöPunk campaign is organized around **UNSA, the United Nations Security
Agency**. Player characters are UNSA agents and may simultaneously belong to other
political, cultural, national, professional, ideological, religious or social factions.

UNSA pools member-state law-enforcement, counterintelligence, intelligence, military,
scientific and civilian capabilities for NHI and X-Risk response. In Helsinki the practical
institutional chain is **Suojelupoliisi → Europol / EU federal structures → UNSA**.

UNSA also coordinates science, diplomacy, civil defence, development, emergency logistics,
disaster relief, reconstruction and post-crisis governance. Its growth is one of the main
mechanisms pushing the United Nations toward an emerging federal world government.

For the full institution, Disclosure politics and campaign framing, see RULEBOOK.md §38.
