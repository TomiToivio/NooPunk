# Genre, tone, agent ecology and tabletop aesthetic (#303)

**Status: PROPOSAL — design only.** No numeric scale, no causal rule, no exact typology: this issue
reserves those to the author, and none is proposed here. `strategy_game/RULEBOOK.md` still says
**NO RULES APPROVED**. This document answers the issue's four work items; item 2 also lands as an
executable ontology (`strategy_game/data/agent_ontology.json`, `strategy_game/agents.py`,
`tests/test_agent_ontology.py`), because a *"single common Agent/Card interface"* is better specified
as data with a validator than as prose alone.

The shorthand this serves: **one minute Department of Sociology; next minute Department of
Parapsychology.**

---

## 1. Tone guide — one event, told three ways

The rule that makes this work: **tone is a register of narration, not a statement about the world.**
The same event carries the same facts in all three tellings; only the framing changes. Nothing below
asserts that anything anomalous is real.

**The event:** a district clinic reports that eleven patients independently described the same
unfamiliar room. Two staff members corroborate. The clinic's instruments recorded nothing unusual.

### As social science fiction

Read it as an institution under strain. Eleven accounts arriving in one week is a *pattern claim*; the
interesting facts are administrative. Which district, which catchment, who has access to the building
after hours, whether the clinic is understaffed, whether the reported descriptions converge because the
patients shared a waiting room. The scene's work is showing how an institution decides what counts as
data: the clinic must classify the report before it can act on it, and the classification is a decision
about *what kind of thing a person's account is*. No conspiracy is needed to make this compelling, and
nobody has to be lying for the accounts to be unreliable. **Le Guin register: the pressure is the
system, not the villain.**

### As New Weird

The same eleven accounts, told from inside. The waiting room's fluorescent hum acquires a duration. The
room the patients describe is described *consistently enough to be a place* — and the consistency is
the horror, because consistency is what an artefact has and what a dream does not. The clinic's
instruments recording nothing is the wrong kind of reassurance: not "nothing happened" but "the
instruments are not the kind of thing that could notice." **No reveal.** New Weird is the primary
NoöPunk genre precisely because its horror is ontological rather than moral: the fear is that the
categories were always wrong, not that someone is evil.

### As bureaucratic science-fiction comedy

The register is a **legally existing phenomenon problem.** The clinic reports it to the health
authority; the health authority has no code for it; the code system requires a code to open a file;
the file cannot be opened without the code. A ministry official writes *"pending classification"* in
the correct field. A committee is convened to decide whether the phenomenon requires a committee.
Someone is genuinely trying to help and is defeated by a dropdown menu. **Dick register: the absurdity
is administrative, and the people inside it are not fools.**

### The rules that keep all three honest

- **No permanent comedy filter.** A scene may be grim, funny, or both at once, and **different agents
  may read the same event in different registers**. That divergence is a feature of the fiction.
- **Never make everyone a fool, and never erase consequences.** Comedy is a register, not a difficulty
  setting. A catastrophe narrated absurdly still killed people.
- **Serious disasters get respectful treatment.** Mass-casualty events, atrocities and real historical
  suffering are not comedy material. Satire aims at institutions and at the powerful; it does not aim
  at victims.
- **Epistemic distinctions survive the joke.** A satirical UFO hearing is not evidence about UFOs in
  reality. In-world assertion, rumour, disputed phenomenon, established fictional fact, actual
  historical research and game-generated outcome stay distinguishable in every register.
- **No imported canon.** *The Dispossessed*, *Don't Look Up*, *Idiocracy*, *Maniac*, *Brazil*,
  Orwell's ministries and PKD's paranoia are **tonal inspirations, not settings, plots or rules.**

---

## 2. The agent/card ontology — one interface, and where the line is

Landed as data with a validator. The load-bearing decision:

> **Agent kinds and interpretive contexts are two disjoint sets.**
> An agent may be asked *"what do you do now?"* A context may only be asked *"how does this read?"*

| Agent kinds (`is_agent: true`) | Interpretive contexts (`is_agent: false`) |
| --- | --- |
| **population_segment** — constituency card: pensioners, feminists, fishermen, religious communities, labour groups, conspiracy movements | **function_systems** — Luhmannian politics, law, economy, science, media |
| **location** — area card: capital, port, small city, countryside, coast | **communication_networks** — Castellsian ties; a tie is a channel and nothing else |
| **organization** — corporation, police department, university, broadcaster, regulator, court | **discourse** — Laclau signifiers, demands, formations, frontiers |
| **faction_leader** — inherits `core.Leader`/`core.Faction` and #323's four-seat economy | |

**The validator fails if a function system is ever declared as an agent kind.** That single check is
the difference between a setting where *"the Law"* acquires a turn and one where law is an operating
context that people act within. Every context must also state **why** it is not an agent and **how** it
acts anyway — through organisations and people who carry its code.

**One shared card shape, deliberately not one shared algorithm.** Every card carries `kind`,
`identity` and `provenance` (required) plus `relationships`, `location_associations`,
`system_associations` and `scenario_tags` (optional). An **organisation participating in several
function systems is one card with several associations, not several organisations.**

### Overlap and aggregation — the issue's explicit worry

Segments and areas are **cross-cutting, not a hierarchy.** A local constituency belongs to an area but
may communicate across regions. The rules: one support is **attributed once**, at whichever level the
scenario declares; an organisation's multi-system participation is one card; a leader belongs to one
faction and holds at most one portfolio. This is what stops the same political support being counted
twice.

### Vocabulary discipline — no third spelling

`V1_DISCOURSE_AND_NETWORK.md` §2.3 bans a synonym for the unclassified signifier role, and §2.2 routes
the `politics.py` / `political.py` fork to the author. This ontology therefore uses `politics.py`'s
`unspecified` when it means that enum member and says **absent** when it means no value was recorded,
introduces no third term, and **resolves neither the fork nor the frontier's node-vs-edge question.**
A test asserts that merely *discussing* the ban is not itself a violation — only using a banned
spelling as a value is.

### No numbers

No numeric value appears in any kind or context. Capacity, accountability, coercion, commercial
influence and institutional fragmentation stay **conceptually separable axes awaiting author-approved
scales** — the same discipline `tests/test_political_layer.py` already enforces on the political
records.

---

## 3. Country-profile thought experiment — one bizarre event, five regimes

The same event as §1, run through different scenario configurations, **keeping the core model
identical**. Only the configuration changes. No scale is implied; these are descriptions, not scores.

| Configuration | Who can act on the report | What happens | What the player learns |
| --- | --- | --- | --- |
| **High-capacity welfare democracy** | a health authority with real reach and a legal duty to investigate | a file is opened, a code is invented for it, an epidemiologist is assigned, and the finding is published as *"no environmental cause identified"* | capacity produces **legibility**, and legibility can settle a question wrongly |
| **Privatised cyberpunk political economy** | the clinic's corporate owner, whose interest is liability | the report is bought and buried; a private contractor is paid to produce a reassuring study; the story leaks from a competitor | the *market* decides what a fact is, and disclosure becomes a commercial weapon |
| **Fragmented low-capacity state** | nobody, effectively | the report is filed in three offices, none of which have jurisdiction; the district handles it by custom | absence of capacity is not absence of politics |
| **Authoritarian surveillance state** | the security service, which reads it as a **legitimacy** problem | the patients are reclassified as a public-order matter; the room is investigated for who met there | an anomalous event is metabolised as dissent |
| **Hybrid: high-tech, unequal, patronage-linked** | a regulator captured by the patron | a *commission* is announced, staffed by the patron's foundation, and reports after the election | institutions can be simultaneously capable and captured |

**The finding worth stating:** in all five, the *facts* of §1 are unchanged — eleven accounts, two
corroborations, no instrument reading. What differs is **which institution can convert an account into
a record**, and that determines the outcome far more than the anomaly does. This is the Luhmannian
point made playable: **function systems do not agree on what an event is**, and the disagreement is
the game.

Sweden, Japan, the US, Somalia and North Korea appear here only as *tonal reference points*, never as
labels, stereotypes or mechanical presets — and no exact typology is adopted.

---

## 4. Physical tabletop inventory

**Tabletop-first, software-second, graphics later.** Every component below is something a person could
put on a table, and the digital version must be able to reproduce the same decisions.

| Component | Count (first session) | Purpose |
| --- | --- | --- |
| **Board** | 1 | 5–8 abstract locations; no parcel geography, no street grid |
| **Faction sheets** | 3 | deliberately resembling **bureaucratic spreadsheets** — the aesthetic is the interface |
| **Leader cards** | 12 | four per faction, per #323; each shows one portfolio |
| **Segment cards** | ~8 | constituency cards, deliberately overlapping |
| **Organization cards** | ~6 | institutions that can act within a mandate |
| **Discourse cards** | ~6 | signifiers and demands, with the empty signifier as a card that anyone may try to fill |
| **Event deck** | ~20 | one global-to-local shock per turn; a seeded shuffle, deterministic given the seed |
| **Dice** | 2–3 | the only randomness beyond the seeded deck |
| **Tokens** | a small tray | support, access, presence — quantities that are *bounded* and visible on the table |
| **Ledger pad** | 1 | where the game is actually played: the paperwork *is* the mechanic |
| **Report slip** | 1 per turn | the short consequential event report |

**First-session configuration:** three factions, five locations, one event, one leader action each,
one ledger page. If the first session needs a second page of rules, the rules are wrong.

**Deliberately absent:** minis-based combat, resource-conversion chains, tech trees, and any
component that requires a hundred rules to be readable. A **very thick eventual rulebook is a
long-term aspiration, not permission to add rules now** — the answer is modular expansions, not
overengineering the prototype.

---

## 5. Coordination and scope

Preserved rather than restated: `core.py` (`Leader`/`Faction`/`Asset`/`Location`/`NetworkEdge`/
`Event`/`WorldState`), `politics.py` (the four political records and `RelationLayer`),
`INTEGRATION_BOUNDARIES.md` (provenance separated; adapters read-only), `V1_FACTION_MANAGEMENT.md`,
`V1_DISCOURSE_AND_NETWORK.md`, and `ISSUE_302_COUNTRY_AGNOSTIC_SOCIETY_V0.md`. Nothing is duplicated
and no existing file is rewritten. **No default LLM dependency:** population and area cards must work
with scripted or table-driven responses.

## 6. Open questions for the author

1. **Which register is the default** for narration when a scene could be read three ways?
2. **Are population and area agents scripted aggregates or independent actors?** The issue says decide
   after prototypes, so this record decides nothing.
3. **Is the `Organization` record of #302 adopted** — which would make it a stored record rather than a
   card kind?
4. **How much absurdity is too much** in a scene with real casualties? The tone guide sets principles,
   not a limiter.
5. **Which components are actually required** for the first playable session?
