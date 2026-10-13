# Faction creation: five axes, typed tags, and NHI diplomacy (issue #346)

**PROPOSAL. Not locked rules, and not a locked taxonomy** — the issue's own words mark every tag family
"examples, not a locked taxonomy". `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/faction_creation.json` | the vocabulary, transcribed from the issue |
| `strategy_game/faction_creation.py` | the reader, the draft validator and the player/GM split |
| `strategy_game/tests/test_faction_creation.py` | 28 executable contracts (issue #271: code only) |
| `strategy_game/data/founding_story.json` | the founder and the patron as edges: roles, named states, declared costs, open questions |
| `strategy_game/founding_story.py` | builds those edges, validates a story, and keeps the pending-decision registry |
| `strategy_game/tests/test_founding_story.py` | 30 executable contracts for the founding layer |

**Consumed, not restated (the founding layer):** the stateful edge itself lives in
[`../relationships.py`](../relationships.py), the six quantities in [`../quantities.py`](../quantities.py),
and the court half in [`LEADER_COUNCIL_SYSTEM.md`](LEADER_COUNCIL_SYSTEM.md). The static
`Relationship` on a character card is **consumed, never replaced**: `from_card_relationships` upgrades
the card's declared tie into a stateful edge that keeps its ids and its direction.

**Consumed, not restated:** `data/global_factions.json` already declares the two conventional axes
(`economic` left↔right, `social` conservative↔liberal, with the "do not conflate economic liberalism
with social liberalism" note), the `additional_dimensions`, and the **#329 paradigm positions** (`agi`,
`psi`, `nhi`, `confederacy_accession`, `sovereignty_agency_consent`) with the note that two factions can
share a compass cell and still differ entirely. [`LEADER_COUNCIL_SYSTEM.md`](LEADER_COUNCIL_SYSTEM.md)
owns the court half: the four field agents, their portfolios, missions and relationships. This record
adds only what neither carries.

## 1. Named positions first, numbers only after playtesting

The five dimensions the issue names — economic Left↔Right, cultural Liberal↔Conservative, AGI and
technological transformation, NHI contact and integration, and PSI and consciousness ontology — are
expressed as **named qualitative positions**: strongly or moderately toward either pole, or neutral.
`numeric_scale_approved` is `false` in the data, and the validator refuses a number where a named
position belongs, saying why. The issue's own precision is kept: *"liberal/conservative" is a cultural
axis, the conventional Political Compass second axis is authoritarian/libertarian, and they are not
interchangeable* — so governance positions live in governance tags instead.

Two standing warnings are carried in the data: an ideology is **not** a personality, an intelligence, a
moral grade, a psychic power or a predetermined loyalty, and a faction's **publicly advertised position
can differ from its hidden agenda**.

## 2. The typed tag system

The type of a tag is what keeps the vocabulary honest. Belief, competence, equipment, relationship,
asset and goal are declared as kinds, so a `MATERIALIST` doctrine is never read as a `REMOTE_VIEWER`
capability — a materialist trained remote viewer is a contradiction the system *permits* rather than
one it silently forbids. Families are suggested, covering political doctrine, technology doctrine,
consciousness and PSI doctrine, PSI capability, NHI policy, social and governance doctrine, goals and
histories, and organisational assets.

**One definition, different contexts:** `REMOTE_VIEWING_TEAM` is a faction **asset**; `REMOTE_VIEWER` is a
character **competence**. Scopes are declared per tag, the model filters by scope, and a scope that no
vocabulary declares is reported rather than accepted.

## 3. NHI policy is not NHI diplomacy

The issue is emphatic that NHI cannot be captured by one scalar: *"avoid forcing 'pro-NHI' to equal
pro-Confederacy or pro-Orion"*. So there are two fields, and nothing derives one from the other:

- **Policy** is a position on the NHI axis — how welcoming a faction is toward contact in general.
- **Diplomacy** is a separate relation to *each named polity* — hostility, contact, trading, alliance,
  dependence or resistance.

A pro-contact faction may be hostile to both major blocs and still seek relations with independent
origins, and a xenophobic hardliner may seek the extermination of both. Both validate cleanly, and the
sabotage for that guard — adding a rule that refuses a pro-contact faction a hostile relation — turns
the suite red, which is how the separation is proven rather than asserted.

## 4. Fog of war

The starting UI must not reveal classified author canon. `player_view()` withholds the hidden agenda
entirely rather than summarizing it, and a polity the faction does not yet know about is **absent** from
its relations. The pre-generated Cosmist International template carries the issue's proposed positions
and tags, marked as proposed settings rather than frozen stats, and *he* does not begin knowing the
hidden Soviet, Confederacy or Orion history.

## 5. The founding story as a mechanical input: two edges, two different costs

Steps 2 and 4 of the creation flow — the academic founder and the corporate patron — are the part of
the story that has to *do* something. Before this layer a draft held a single `leader` string and the
patron had no field at all, and `relationship` and `goal` existed only as **static card tags**: a label
with no condition attached, which cannot diverge, be captured or be severed. Both roles are therefore
carried as **relationship edges** with their own goals and a mutable **named** state — never a number,
because `numeric_scale_approved` is still `false`.

| | **Pre-crisis academic founder** | **Corporate patron** |
| --- | --- | --- |
| edge | `founded_by` | `patron_of` |
| gives | legitimacy and access earned *before* the paradigm shifts: citation capital, students, institutional standing, a doctrine still taken seriously | means: cash, facilities, personnel, data, equipment, organisational access, corporate reach |
| costs | legitimacy hostage to one reputation the paradigm shifts have just made contested: obsolescence, discredit, schism | dependence, a captured agenda, reputational contamination, and the step-4 ladder ally → council member → rival power centre → usurper |
| kind of cost | **concentrated and non-purchasable** — one person, and no money buys the standing back | **diffuse and replaceable** — many assets, and another patron could in principle replace this one |
| quantities (§7) | institutional access and articulation: a *source* of legitimacy | membership/resources and the *rented* part of access — never opinion or seats |
| named states | `ascendant / contested / discredited / superseded / departed` | `aligned / divergent / conditional / withdrawing / captured / severed` |

The asymmetry is the point: **the founder is where the faction's legitimacy comes from; the patron is
the biggest threat to it.** A faction can be killed by its founder being wrong *and* by its patron being
right — the patron's business model being exactly what the faction exists to oppose.

**The patron edge carries a goal the faction need not share**, and validation *permits* that divergence,
because the divergence is the mechanic: the canon case is a patron whose declared goal is not his
party's doctrinaire base, and the gap is what produces the party's stated internal contradictions. A
check refusing it would be the defect rather than the guard.

**Belief is not capability, and the founder is where that earns its keep.** A founder may hold a belief
that is false in the fiction while still being a competent researcher, so *"wrong but rigorous"* and
*"right but a fraud"* are two different games: the discredit failure is not "the founder was
incompetent". The check is executable — an id that `faction_creation.json` files as a `belief` and that
is attached as a `competence` is reported by name, and the sabotage that flips one turns the suite red.

**The state is mutable and the transition is not judged.** `reassign_state()` moves an edge and logs
the previous condition; *which* transition is legitimate is a rule the author has not given, so
`transitions.declared` is `false` with a reason, and a severed edge is **read, not deleted** — whether
a severed patron can be replaced is one of the open questions below.

## 6. What the author still has to decide

- **The StO bloc's official label.** #348 locks **UCCC** and says not to revert to older
  Confederation/Orion Group names as official labels; this issue's text says **"Confederacy/Zookeepers"**.
  The data uses the locked name and records the other as notation, with the conflict flagged rather than
  decided.
- **The cultural axis**: liberal/conservative alone, or a distinct authoritarian/libertarian value as
  well. `global_factions.json` currently records authoritarian/libertarian under `additional_dimensions`.
- **Whether an ordered scale is ever approved**, and if so its range.
- **The authored diplomacy/recruitment event.** Now **authored** (PR #426, 2026-10-13): `event_seed` holds
  "The Neutral Laboratory" with its cast, three beats and three choices, marked
  `authored_narrative_prototype_no_resolution_rules`. What is still the author's is the **resolution** —
  the seed's own `outcome_policy` refuses an automatic success, a fixed resource change and a forced
  recruitment, and no code reads it.
- **Any affinity or tension mechanic**: this module deliberately computes none, because the issue allows
  broad cues only as a later, author-approved aid.

### Open in the founding layer

- **Is the founder one of the four leaders, or a fifth authority over them?** The same tension is raised
  on #323 as "four leaders" versus "four field deployments"; it is flagged on both issues and resolved on
  neither.
- **Does a patron sit on the council or outside the four leaders?** Step 4 names all four positions —
  ally, council member, rival power centre, usurper — and fixes none of them as the default.
- **Can a severed patron edge be replaced, or is the loss permanent?**
- **Which transition between named positions is legitimate?** Structural only: the record moves and logs.
- **May a patron or founder be NHI-aligned, or an NHI entity itself be a patron?** `TAG_SCOPES` has no
  NHI/entity scope even though `data/world/faction_taxonomy.json` declares the `nhi` faction type.
  Recorded as a dependency, not extended here.
- **Any ordered scale for an edge's condition** — none is proposed, and `numeric_scale_approved` stays
  `false`.
- **The authored secret of any specific patron**: the cards leave `gm_notes` to the author, and this
  layer adds no secret to any named character.

## 7. Acceptance criterion 7: the first-turn container, and why it holds no value

Criterion 7 asks to *"define pre-crisis world state and first-turn resource constraints"*. The
**world state** half is documented (the acceleration period, partial disclosure with no public contact
yet, commercial PSI). The **resource constraints** half is an **economy**, and an economy is reserved
to the author (`AGENTS.md` §4) while `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**.

So what landed is the container a ruling would occupy, and nothing else:

| Field | Content |
| --- | --- |
| `first_turn.id` | `first_turn_resource_constraints` |
| `first_turn.candidate_sheet_fields` | the **issue's own** candidate faction-sheet list, transcribed as names only: ideology/doctrine, legitimacy, membership/support, influence/reputation, funding, research, intelligence, organisation/facilities, security, network ties, corporate-patron access, strategic objectives |
| `first_turn.values_declared` | `false`, with the reason it is `false` |
| `first_turn.list_source` | says the list is the issue's and is **not** an approved sheet |

`first_turn_problems()` refuses only what stops the container being a container: a field with no
identifier, a repeated identifier, a field carrying **anything but its name** (a value there would be an
invented one), a numeric label, a container that does not say whether values are declared, and an empty
container that gives no reason for being empty. It computes nothing, prices nothing and reads no clock.

**The resolution half of criterion 6 stays open next to it**, and it is recorded **once**: the ruling is
`mission_resolution` in `data/council.json`'s `pending_author_decisions`, and this file's
`pending_author_decisions` points at it rather than restating it.

