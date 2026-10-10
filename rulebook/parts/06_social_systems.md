# Social Systems: Interaction, Ideology and Simulation

> Generated, verbatim segment of [RULEBOOK.md](../../RULEBOOK.md) (the core and extended-canon runs). The rulebook file is canonical; this part and its section numbers are unchanged so that cross-references keep resolving. Regenerate with `python3 tools/split_rulebook.py --apply`.

## 6. Social Systems

### 6.1. Social Interactions

A **Social Interaction** is a conversation between two or more characters. It may be:

- face-to-face;
- online;
- telepathic.

With human-controlled characters or LLM agents, conversation should remain primarily free-form. Scripted NPCs may expose a more limited interaction space.

A Social Interaction may include social skill checks, use of psionics, cybernetic hacking or other cross-system actions. It can escalate into physical combat, shift into Cyberspace, or continue telepathically through Noöspace.

### 6.2. Social skill checks

When uncertainty matters, social actions use the same core engine as other actions:

```text
Social STAT + relevant Skill + 1d10 vs DV
```

or an opposed roll against another character's appropriate STAT + Skill.

The roll resolves the uncertain mechanical question. It does not replace free-form dialogue or dictate a human player's beliefs.

### 6.3. Trading

Trading covers buying, selling, exchanging, bargaining and other economic interaction. It may use money, contracts, access, favors, reputation, barter or other setting-specific forms of value.

### 6.4. Romance

Romance is a special form of intimate Social Interaction. It is handled through the same general relationship framework as other Contacts, with free-form role-play taking priority over mechanical coercion.

### 6.5. Contacts

**Contacts** are a character's personal social connections.

A Contact has a signed relationship score from **-10 to +10** and may include a specific **Affect**.

- **+10** = Love
- **0** = Neutral / no meaningful Affect
- **-10** = Hate
- if no more specific Affect is needed, positive edges default to **Likes** and negative edges to **Dislikes**

A Contact is a personal relationship, not general standing with a group.

Contacts form a **Social Network Graph**: characters are nodes and relationships are signed, weighted edges with optional Affect labels. This graph can be combined with Motivation, Reputation and Faction graphs for analysis and visualization.

### 6.6. Factions

A Faction is an organized social or ideological formation. NoöPunk models Faction ideology using LaclauGPT's Formula of Populism:

- **US** contains actors, goals, empty signifiers and other objects the Faction identifies with, supports or treats as part of its political/social identity.
- **FRONTIER** contains actors, goals and signifiers the Faction defines itself against, opposes, fears or rejects.

US/FRONTIER is a structured ideological boundary, not a flavor-text alignment field.

### 6.7. Reputation

**Faction Reputation** measures a character's standing with a Faction on the same **-10 to +10** signed scale and may include a specific Affect.

Reputation matters especially when meeting somebody who does not yet know the character personally. An unknown NPC may initially react according to the character's Reputation with the NPC's Faction. Once a personal Contact relationship exists, that relationship can diverge from inherited Faction attitudes.

### 6.8. Motivations

**Motivations** describe what a character desires, supports, seeks, resists or opposes.

They use the same **-10 to +10** signed scale:

- positive values represent desire, attraction, support or commitment;
- negative values represent opposition, aversion or rejection.

Motivations may carry a specific Affect such as **Dreams of**, **Supports**, **Desires**, **Opposed to** or **Hates**.

### 6.9. Encounters

An Encounter begins when the character unexpectedly meets somebody who starts a Social Interaction, or when somebody contacts the character remotely.

Encounters may arrive through physical presence, messaging, calls, telepresence, augmented reality or telepathic/Noetic contact. They can become conversations, negotiations, investigations, hacking situations, psychic confrontations or combat.

---

## 17. Social and ideological mechanics: Affect, Factions, Motivations, Reputation and Contacts

**Status: NOÖPUNK NATIVE, issue #107.**

NoöPunk uses **one Affect graph** for Factions, Motivations, Reputation and Contacts. The detailed specification is [rulebook/4_SOCIAL.md](rulebook/4_SOCIAL.md); the engine-neutral representation is [src/simulation/affect.py](src/simulation/affect.py). The canonical **terminology** for the faction system — Contacts, Motivations, Faction Reputation, US / FRONTIER and the graph layers — is [rulebook/8_FACTIONS.md](rulebook/8_FACTIONS.md).

Every relation has a Target, semantic Affect label, and Affect Score from -10 to +10 (issue #144). Labels such as Knows, Trusts, Supports, Loves, Fears, Distrusts, Hates and Opposes are not collapsed into generic sentiment. Multiple labelled relations toward one target are allowed, all relations are directional, and an absent edge means unknown rather than neutral.

Factions are changing discursive formations represented as US^(positive/constitutive Affects) + FRONTIER^(negative/antagonistic Affects). This adapts Emilia Palonen's Formula of Populism as a general model of political/social identification, not a populism classifier. US and FRONTIER may articulate demands, signifiers, identities, factions, institutions, technologies and individuals.

Character Motivations use the same edge representation. Faction membership supplies starting Affects, not mind control. Multiple factions preserve different labels as ambivalence; matching target+label edges are combined; explicitly personal Motivations can override inherited matching edges while provenance is retained.

Reputation is directional from the evaluating faction/actor toward the character. Contacts are person-to-person social edges, including friends, acquaintances, professional ties and enemies. The default UNSA affiliation is represented through the same system alongside the character's personal faction identity, and the score scale is **−10…+10** ([rulebook/8_FACTIONS.md](rulebook/8_FACTIONS.md)).

At the architecture level, face-to-face, text/chat, voice/video, Mesh and PSI communication are channels over the same social layer. The first playable interaction model is text-forward and hub-based, documented in [docs/design/GAMEPLAY_LOOP.md](docs/design/GAMEPLAY_LOOP.md), with a small Asteroid Belt/station slice as the preferred initial scope.

---

## 21. Social-science simulation layer

**Status: NOÖPUNK NATIVE.**

NoöPunk is an RPG **and** a social simulation.

The simulation should eventually model some combination of:

- organizations,
- factions,
- ideologies,
- discourse,
- social networks,
- institutions,
- resources,
- political economy,
- collective action,
- technological diffusion,
- public opinion,
- hegemonic struggle,
- social change.

These systems are not substitutes for individual RPG mechanics.

Keep explicit boundaries between:

- RPG mechanics,
- agent cognition,
- social simulation,
- world simulation,
- narration.

Let them exchange state through defined interfaces.

---
