# Social and ideological mechanics

Status: NOÖPUNK NATIVE, issue #107.

NoöPunk uses one representation for Factions, Motivations, Reputation and Contacts:

Target | Affect | Affect Score

Affect is the semantic relation, for example Knows, Likes, Trusts, Supports, Identifies With, Loves, Protects, Pursues, Fears, Distrusts, Hates, or Opposes. Affect Score is an integer from -100 to +100. Positive means positive investment, negative means negative investment, and zero is an explicit neutral relation. No edge means unknown. Unknown is therefore not the same as a stored zero.

The label and score both matter. Fears -70, Hates -70 and Opposes -70 have similar polarity but different meaning. Multiple labelled edges may connect the same source and target, so a character can support and fear AGI at the same time. All edges are directional.

## General edge

Fields: source, source_type, target, target_type, affect, affect_score, domain, metadata. Domains are faction_us, faction_frontier, motivation, reputation, and contact. Metadata may record evidence, origin, inherited_from, created_at and updated_at. Useful node types include character, faction, institution, nationality, species, ideology, demand, signifier, technology, place and concept.

The engine-neutral reference model is src/simulation/affect.py and the schema metadata is data/world/social_affect_schema.json.

## Factions: US + FRONTIER

NoöPunk keeps the EP2 idea that a character can belong to social formations, but represents each faction as a changing discourse:

Faction = US^(positive or constitutive affects) + FRONTIER^(negative or antagonistic affects)

This adapts Emilia Palonen's Formula of Populism as a general faction/discourse model. It is not a populism classifier. Populist and non-populist formations alike may articulate collective subjects, demands, affective investments and antagonistic frontiers.

US may contain demands, identities, allied factions, individuals, technologies and signifiers. Signifier roles may be marked nodal_point, floating_signifier, empty_signifier or ordinary_signifier only when their articulated role warrants it. Ambiguity alone never makes a signifier floating or empty.

FRONTIER accepts the same target types but marks the constitutive outside through which the formation defines itself. Mere disagreement or dislike is not automatically an antagonistic frontier.

## Motivations and faction inheritance

A Motivation is a personal demand, commitment, value, goal, identity or object of affective investment represented by the same edge.

Faction membership supplies starting conditions, not mind control. For one faction, copy its ideological US/FRONTIER Affects into starting Motivations. For multiple factions: copy non-conflicting edges; combine the same target plus Affect label by arithmetic mean; retain different labels toward the same target as explicit ambivalence; let an explicit personal Motivation override an inherited edge with the same target plus label; retain inherited_from provenance.

Thus Support AGI and Fear AGI remain two edges rather than being averaged into a meaningless single opinion.

## Reputation

Reputation is a directional Affect edge from a faction or social actor to a character. It is not the character's opinion of that faction. Character -> faction Likes +70 and faction -> character Distrusts -30 may coexist. NoöPunk does not preserve the EP2 reputation-network list wholesale; reputation contexts emerge from NoöPunk factions and institutions.

## Contacts

A Contact is a specific PC or NPC known personally or socially. Positive and negative relations use the same graph. Unknown people have no Contact edge; a numeric subsystem may use 0 as fallback without creating a zero-valued edge.

Character creation should start with a small playable graph inspired by Cyberpunk RED social hooks: a few appropriate contacts such as a close friend, professional contact, family/community tie, patron or mentor, and optionally an enemy. Each contact records identity, role, faction if known, relationship, Affect label/score, why you know them, what they may want, what they can realistically do, and reciprocity. Exact counts and random tables remain future character-generation design.

Meaningful encounters may add, modify, relabel or remove Contact edges. Issue #107 intentionally does not fix universal numeric increments yet.

## Unified social/discourse graph

Factions, Motivations, Reputation and Contacts are domains of one heterogeneous graph, not four databases. It supports friends-of-friends, brokers, introductions, alliances, frontiers, faction memberships, social distance, reputation propagation, party formation, mission hooks and discourse-network analysis.

The simulation must support adding/removing edges, modifying labels/scores, inheritance/override, faction split/merge, alliances/frontiers, and history/provenance. Exact persuasion, propagation and score-update formulas remain later design.

## Theory in RPG terms

The model borrows a relational vocabulary from Laclau and Mouffe: articulation, equivalence/difference, antagonism, nodal/floating/empty signifiers, political subjects, affective investment and hegemony. NoöPunk preserves LaclauGPT's safeguards: co-occurrence is not articulation; difference is not antagonism; ambiguity is not emptiness; sentiment is not affective investment; frequency is not hegemony.

Palonen's Us^Affects + Frontier^Affects therefore becomes a compact representation of political/social identification and antagonism beyond populism, while remaining an interpretive structure rather than a mathematical classifier.

## Change over time

Affects are mutable state. Missions, betrayal, rescue, propaganda, ideological conversion, trauma, faction schism, Disclosure, personal relationships, war, campaigning and new evidence may change them. Deterministic mechanics own numeric mutation when later procedures define it; LLM narration may explain resolved change but must not invent scores.

See FACTIONS.md for the NoöPunk starter content library and docs/design/GAMEPLAY_LOOP.md for the text-RPG architecture.

## UNHSS / Firewall campaign frame

The default NoöPunk campaign is organized around the **United Nations Human Security
and Survival Organization (UNHSS)**. Player characters are Firewall field agents
inside UNHSS and simultaneously belong to another political, cultural, national,
professional, ideological, or social faction.

Firewall is the classified operational culture and intelligence network within UNHSS,
not a separate extra-governmental conspiracy. UNHSS combines civilian science and
diplomacy, international law enforcement and intelligence, civil defence and disaster
relief, and UN Peacekeeper rapid-response military capabilities.

The United Nations is becoming a contested federal world government with universal
Earth-state membership, possible off-world member states, a UN President, Prime
Minister and Parliament, and four-year global elections. UNHSS is a major engine of
that federalization.

For the full organization, jurisdiction, forces, democratic safeguards, Wallfacers,
mission structure, and political tensions, see RULEBOOK.md § “UNHSS / Firewall:
default campaign institution” and issue #108.
