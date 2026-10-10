# Social and ideological mechanics

Status: NOÖPUNK NATIVE, issue #107.

NoöPunk uses one representation for Factions, Motivations, Reputation and Contacts:

Target | Affect | Affect Score

Affect is the semantic relation, for example Knows, Likes, Trusts, Supports, Identifies With, Loves, Protects, Pursues, Fears, Distrusts, Hates, or Opposes. Affect Score is an integer from -10 to +10. Positive means positive investment, negative means negative investment, and zero is an explicit neutral relation. No edge means unknown. Unknown is therefore not the same as a stored zero.

The label and score both matter. Fears -7, Hates -7 and Opposes -7 have similar polarity but different meaning. Multiple labelled edges may connect the same source and target, so a character can support and fear AGI at the same time. All edges are directional.

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

Reputation is a directional Affect edge from a faction or social actor to a character. It is not the character's opinion of that faction. Character -> faction Likes +7 and faction -> character Distrusts -3 may coexist. NoöPunk does not preserve the EP2 reputation-network list wholesale; reputation contexts emerge from NoöPunk factions and institutions.

## Contacts

A Contact is a specific PC or NPC known personally or socially. Positive and negative relations use the same graph. Unknown people have no Contact edge; a numeric subsystem may use 0 as fallback without creating a zero-valued edge.

Character creation should start with a small playable graph of NoöPunk's own design: a few appropriate contacts such as a close friend, professional contact, family/community tie, patron or mentor, and optionally an enemy. Each contact records identity, role, faction if known, relationship, Affect label/score, why you know them, what they may want, what they can realistically do, and reciprocity. Exact counts and random tables remain future character-generation design.

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

## UNSA campaign frame

The default NoöPunk campaign is centered on **Helsinki** and organized around the
**United Nations Security Administration (UNSA)**. The PC works for UNSA while potentially
belonging to several other political, cultural, national, professional, ideological,
religious, community or social factions.

UNSA pools member-state law-enforcement, intelligence, counterintelligence, military,
scientific and technical assets for NHI and other X-Risk response. In Helsinki, the
practical institutional chain is **Suojelupoliisi → Europol → UNSA**.

UNSA also has a major civilian side: science, diplomacy, civil defence, development,
humanitarian response, disaster relief and reconstruction. It is a major engine of the
UN's evolution toward a federal world government.

The default campaign should expose only a **small number of factions relevant to
Helsinki-area play**. Add distant or global factions when a scenario actually makes them
matter.

Disclosure drives two contradictory processes at once: ontological shock, fragmentation,
cult formation, xenophobic/doomer backlash and PSI-enabled hybrid infiltration on one
side; global unification and planetary institutions on the other. Both are canonical.

Character creation grants **10 positive Faction Reputation points** divided between **two
or three factions** (for example **6/4** or **5/3/2**). See RULEBOOK.md Chapter 9 and
rulebook/8_FACTIONS.md.

---

# Social procedures

**Status: NOÖPUNK NATIVE — issue #220.** Social play uses the **same core check** as every other
realm — `STAT + Skill + 1d10` — the **same clock** and the **same margin bands** as physical
conflict ([`rulebook/18_CROSS_DOMAIN_STATE.md`](18_CROSS_DOMAIN_STATE.md), #225; `rulebook/3_PHYSICAL.md`, #219).
Nothing below adds a second arithmetic. Every number is **PROVISIONAL pending author calibration**.

## The one rule that governs the whole chapter

> **A social check changes what a character can *achieve*. It never changes what a target
> *believes*.**

This is the load-bearing constraint. Everything else here — deception, coercion, Kinesics, PSI —
is a consequence of taking it seriously. A social system fails when a good roll silently rewrites a
person, because at that point the NPC has stopped being an agent and become a difficulty number
with a face.

## Social contests

A social contest is **opposed**. The acting character rolls the Skill the method implies; the target
resists with the Skill its own competence implies.

| Method | Acting check | Typical resistance |
| --- | --- | --- |
| **Negotiation** (`Talk`) | `SOC + Talk` | `SOC + Talk` or `INT + Know (the subject)` |
| **Deception** (`Deceive`) | `SOC + Deceive` | `SOC + Kinesics`, or `INT + Investigation` when evidence is in play |
| **Coercion** (`Provoke`) | `SOC + Provoke` | `PSY + Psychic Defence` (resolve) |
| **Command** (`Lead`) | `SOC + Lead` | `PSY +` resolve, or `SOC + Lead` in a contest of authority |
| **Reading a person** (`Kinesics`) | `SOC + Kinesics` | `SOC + Deceive` when the target is actively concealing |
| **Hostile PSI** | `PSY + Telepathy/Psychokinesis` | `PSY + Psychic Defence` (`RULEBOOK.md` §4.1) |

**The consequence vocabulary is social, and the arithmetic is shared.** The margin of success is
read through the same four bands as physical conflict, but the bands mean something different
(band thresholds are **PROVISIONAL**):

| Margin | Band | Social consequence |
| --- | --- | --- |
| ≤ 0 | — | **Unmoved.** Nothing changes. |
| 0 | glancing | **Heard.** They listen; no concession. |
| 1–4 | solid | **Leaning.** A partial concession, and it costs them something. |
| 5–8 | severe | **Convinced.** They act on it while the reasons hold. |
| 9+ | brutal | **Committed.** They make it their own — within their own motives. |

**A consequence is a state, not a counter.** Like the physical ladder, a social outcome does not
accumulate: two good arguments do not add up to a converted ideologue. Repeating a pitch on the
same grounds is **not** easier the second time, and the GM may rule it harder.

## The hard limits: what social success cannot do

These are assertions, not advice, and the guard tests them as positives.

- **Kinesics reads cues, not truth.** A successful reading tells you the target is *uncomfortable,
  eager, rehearsed or frightened* — never "they are lying". Certainty about another mind is not a
  Skill outcome.
- **There is no guaranteed lie detection.** Deception beats detection unless **independent
  evidence** contradicts it, and even then the liar may have believed their own version.
- **A successful `Deceive` does not rewrite memory or ideology.** It changes what the target
  currently believes was said, within the band above. Contradicting evidence reopens it.
- **Coercion is not persuasion.** `Provoke` moves **behaviour under threat**; it does not move
  belief. Every coercion outcome creates a **Grievance** consequence (below). A coerced NPC
  complies now and remembers.
- **A social result cannot overwrite a Motivation.** NPCs hold their own US/FRONTIER and Motivation
  edges. A social outcome may **add or modify edges only through an author-specified procedure** —
  and since the exact increments are reserved (`AGENTS.md` §4, #107), this chapter specifies the
  **shape**, not the numbers.
- **PSI does not shortcut intent.** Telepathy can surface content, and it is resisted, uncertain and
  not admissible as proof (`rulebook/6_PSYCHIC.md`; #226's evidence rule).

## Contacts and the social graph

Contacts are **Contact edges** on the one heterogeneous graph (above), never a separate list.

- **Finding someone** is `SOC + Connect` against a difficulty set by **social distance** — how many
  hops away they are on the graph, and how much they do not want to be found. PROVISIONAL: a direct
  contact is Everyday, a friend-of-a-friend is Difficult, a stranger in the network is
  Professional, and a stranger outside it is Heroic.
- **Being a broker is derived, never stored.** Betweenness and reach are properties **computed**
  from the graph (the seven SNA layers, `rulebook/8_FACTIONS.md`), not a stat a character carries.
- **An introduction is a new Contact edge** with its own label and score, created by play, not
  granted by a roll alone — the person must actually agree.

## Relationship statuses: derived from the Affect graph, never a second store

A relationship **status** is a **read-out** of the existing Affect edges between two nodes
(label + score). It is computed, not written down beside the graph, so the two can never disagree.

| Status | Derived condition (PROVISIONAL) |
| --- | --- |
| **Unknown** | no edge exists |
| **Acquainted** | an edge exists, score near 0 |
| **Trusted** | a positive edge at +5 or higher |
| **Indebted** | a reciprocal obligation edge (a favour, not an emotion) |
| **Estranged** | a formerly positive edge now near 0 with a negative label |
| **Hostile** | a negative edge at −5 or lower |

Because it is derived, **changing a status means changing an edge** — with provenance — not editing
a status field. `Unknown` is *not* a stored zero: the chapter's original rule that "no edge means
unknown, and unknown is not the same as a stored zero" is preserved exactly.

## Group interactions

Leadership is the Skill; the group is a modifier, and the modifier is **bounded**.

- A group acting together rolls the **leader's check** (`SOC + Lead`), with a **+1 per supporting
  member up to +2** (the bound is **PROVISIONAL**). The bound is the same ±2 situational cap the
  resolution pass recorded (#217), so a crowd cannot be converted into an unbounded bonus.
- **Group resistance** works the same way in reverse: a crowd resists as its leader plus the same
  bounded support.
- **An audience changes the stakes, not the arithmetic.** A public social outcome may also move a
  **Reputation edge** (the `reputation` Affect domain) by **one step** — the same one-step
  vocabulary physical armor uses — and only when the exchange was genuinely witnessed.

## Bounded narrative aspects

Social play uses the **aspect layer that already exists** (`docs/design/ISSUE_200_ASPECTS_PROTOTYPE.md`,
#233) rather than introducing a second one. An aspect is bounded by construction:

- it has a **scope** (which person, group, place or situation it attaches to);
- it has a **duration or a use condition**, never an indefinite free bonus;
- it is **cancellable** — evidence, a changed situation or an explicit counter removes it;
- it is **not a substitute for a STAT or Skill**: an aspect gives permission or a bounded modifier,
  never a rating.

**Grievance** is the canonical social consequence of coercion: a bounded negative aspect attached
to the coercer, which a later scene can act on. It exists so that coercion has a cost that survives
the scene in which it worked.

## Worked examples

### Tabletop: the receptionist

**D** (`SOC 5`, `Talk 4`, `Kinesics 3`) needs a visitor log. The receptionist (**R**) is loyal to
her employer (`Talk 4`) and has been told to refer all enquiries upward; she has a Motivation edge
*Protects the clinic's patients* at +6.

| Exchange | Actor | AP | Action | Roll | Result |
| --- | --- | ---: | --- | --- | --- |
| 1 | D | 1 | Prepare — read R | `SOC 5 + Kinesics 3 + 1d10(6) = 14` vs R's `SOC 4 + Deceive 2 + 1d10(4) = 10` | **read succeeds** — D reads *rehearsed politeness*, not a lie |
| 1 | D | 1 | Negotiate | `SOC 5 + Talk 4 + 1d10(5) = 14` vs R's `SOC 4 + Talk 4 + 1d10(3) = 11` | MoS 3 → **Leaning** — she concedes *something that costs her*: the sign-in sheet, not the log |
| 1 | D | 1 | Hold | — | — |
| 1 | R | 1 | **React** — resist the follow-up | `SOC 4 + Talk 4 + 1d10(7) = 15` vs D's press | **Unmoved** — she stops conceding |

Three things the example shows: the read produced **cue knowledge, not truth**; a **Leaning** result
is a *real but partial* concession that costs the target something; and **R's own Motivation edge
was never overwritten** — she did not become pro-D, she gave ground she could afford.

### Ollama / Concordia: who rolls?

In the digital runtime the **LLM narrates and chooses; it never rolls and never sets state**
(`AGENTS.md` §12).

1. The engine resolves the contest **deterministically** — Skill, target, d10, margin, band — and
   writes the result to the event log.
2. The LLM receives the **resolved outcome** ("D: Leaning — the receptionist slides the sign-in
   sheet across") and may narrate *how* it happened and what the NPC says, **consistent with her
   US/FRONTIER and Motivations**.
3. The LLM may **propose** an aspect (a Grievance, a favour) as a structured suggestion.
4. The engine **validates** the proposal against the bounded-aspect rules, applies it, and records
   it. A proposal that would rewrite a Motivation, invent a score, or exceed the aspect bounds is
   **rejected**, not narrated into existence.

The seam is the whole point: narration is generated, **numbers are not**.

# What this chapter deliberately does not do

- **No persuasion formulas, no Affect-score increments, no propagation algorithm.** These stay
  reserved (`AGENTS.md` §4, #107); the shape is specified, the arithmetic is the author's.
- **No new Skills, STATs or derived statistics** — the procedures use the canonical vocabulary.
- **No second graph and no second aspect layer** — statuses are derived from the Affect graph, and
  aspects come from #233.
- **No investigation or evidence procedure** — that is #226.
- **No calibration.** Every value above is PROVISIONAL.

