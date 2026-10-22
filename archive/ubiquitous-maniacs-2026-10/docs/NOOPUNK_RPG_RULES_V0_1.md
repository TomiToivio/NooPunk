# Noöpunk RPG Rules v0.1

## Status

This is the first playable rules subset for *Noöpunk: Ubiquitous Maniacs*. It is
an original RPG with a lightweight 4dF interface influenced by Fudge, Fate Core,
*Transhumanity's Fate* and *Psi-punk*. It is not a Fate implementation, a Fudge
conversion or a reproduction of any source game. Noöpunk's seven attributes,
Psyche/CAN model, provenance, consent boundaries and multilayer graphs define
its own mechanical identity.

The rule for expansion is: **no subsystem exists until play needs it**.

## 1. Core resolution

When an uncertain outcome matters, roll:

`4dF + attribute + skill + explicit bonuses` against a difficulty.

Each Fate die is `−`, blank or `+`, worth −1, 0 or +1. Four dice therefore produce −4…+4. For an opposed action, the opponent's total is the difficulty.

| Margin | Result | Meaning |
|---:|---|---|
| +3 or more | Critical success | Succeed and gain an important extra benefit |
| 0…+2 | Success | Achieve the intent |
| −1…−2 | Costly success | Progress with a condition, exposure, reduced effect or hard choice |
| −3…−4 | Failure | The intent fails, but the scene must still move |
| −5 or less | Catastrophic failure | Serious consequence; never a missing-content dead end |

`Costly success` counts as progress and therefore permits the intended aspect or
graph effect, but its cost is mandatory. In the Python API this is
`succeeded=True`, `clean_success=False` and `requires_cost=True`. Attack shifts
remain zero on a negative margin.

Use the familiar ladder as descriptive language: Terrible (−2), Poor (−1), Mediocre (+0), Average (+1), Fair (+2), Good (+3), Great (+4), Superb (+5), Fantastic (+6) and Legendary (+7 or more).

Do not roll for ordinary conversation, obvious information or choices whose interesting part is the decision itself.

## 2. Characters

A player character consists of:

- seven attributes;
- a manageable skill list;
- aspects and stunts;
- conditions, stress and consequences;
- abstract resources and reputation where needed;
- distinct Ego, Morph and Psyche descriptions when relevant.

### Attributes

The existing Ubiquitous Maniacs model remains canonical for v0.1:

- **Intelligence:** reasoning, memory and analysis;
- **Awareness:** perception, intuition and reading situations;
- **Reflexes:** speed, coordination and immediate response;
- **Body:** strength, endurance and embodied resilience;
- **Charisma:** expression, presence and interpersonal initiative;
- **Willpower:** self-control, psychic integrity and resistance;
- **Cybernetics:** embodied technical fluency with implants, BCIs and machines.

Psyche is not reduced to a single attribute. In v0.1, Psyche is a changing character layer whose active resistance normally uses Willpower and whose perception commonly uses Awareness.

### Skills

Day 1 currently uses the compact *Transhumanity's Fate*-derived list: Athletics, Civ Rep, Cover, Cred, Deceive, Eye Rep, Fight, Hardware, Infiltrate, Infosec, Investigate, Kinesics, Medicine, Notice, Pilot, Program, Provoke, Rapport, Shoot, Somatics, Survival, Will, Xeno-Contact and X-Risks.

Ranks run from +0 to +4. A specialization or explicitly relevant tag normally grants +1. The list may later change, but v0.1 does not introduce a second skill system.

## 3. Character creation

For a starting protagonist:

1. Write a high concept and trouble as aspects.
2. Add three aspects for history, relationships, ideology, trauma or anomalous circumstance.
3. Assign the seven attributes as appropriate to the scenario. Day 1 characters are data-driven rather than built from a universal point budget.
4. Assign 25 skill ranks, with no skill above +4 and no narrower high-rank column than the rank below it.
5. Write one stunt.
6. Record current conditions and any existing consequences.
7. Describe Ego, Morph and Psyche only to the level the scenario needs.

### Example: Emil Romppainen, Day 1

- High concept: **Brilliant investigator buried under Sven-Olof**
- Trouble: **UFAB Hunger**
- Other aspects: **Hidas peitepersoona**, **Totuus puskee halkeamista**, **Somebody Else's Memories**
- Example stunt: **Institutional Paranoia:** +2 when overcoming institutional concealment with Notice once the fiction establishes a specific inconsistency.

Romppainen's complete ratings remain in the scenario character data rather than being duplicated here.

### Example NPC: Dr. Elin Dahl

For a supporting NPC, choose one focus attribute, one focus skill and competence +1 to +4. Everything else defaults to +0 until the fiction needs it. Dahl can begin with Awareness +2, Kinesics +2 and the aspect **Institutional compassion under bureaucratic pressure**.

## 4. Aspects and stunts

An **aspect** is a true and mechanically relevant phrase about a person or situation. When a scripted check names a matching aspect, it grants +1. An aspect may also grant or deny fictional permission without a roll.

A **stunt** is a narrow exception: usually +2 to one action in a clearly defined
circumstance. V0.1 does not yet implement a general narrative currency;
therefore freeform invocation, compels and refresh remain future work. If such a
currency is playtested, its Noöpunk working name is **Agency**: it may alter the
player character's roll or negotiated cost but cannot override another Psyche's
consent or settle metaphysical truth.

## 5. Stress, conditions and consequences

**Stress** is short-term pressure within a conflict. A normal participant has three stress capacity. Stress clears when the conflict and immediate danger end.

**Conditions** are named ongoing states such as `orientation_migraine`, `identity_afterimage` or `ufab_special_observation`. They change available actions and clear only through an appropriate fictional recovery.

**Consequences** absorb or record lasting harm:

- mild 2;
- moderate 4;
- severe 6.

Consequences may be physical, social, cybernetic or noetic. A player may concede before being taken out and negotiate a consequence that preserves agency while accepting loss.

Concession and taken out are distinct states. A conceding participant accepts
the agreed stakes and leaves the conflict before forced defeat; being taken out
hands disposition of the stated stakes to the opposition within the established
consent and safety boundaries.

## 6. The four actions and four layers

Use the same four actions in physical, social, cyber and noetic play:

- **Overcome:** remove an obstacle, gain access or complete a task;
- **Create Advantage:** discover or create an aspect, opening or graph relation;
- **Attack:** impose stress or force a concession;
- **Defend:** prevent an attack or advantage.

Actions may create a portable graph effect. A graph effect names its domain, operation, source, target, key and value. The narrative RPG stores it; NetworkX-based simulations can apply it later without coupling the modules.

## 7. Social interaction

Relationships may track trust, attraction, suspicion, hostility, loyalty, fear and influence from −100 to +100. Only dimensions actually used by a scene need to exist.

Choices may change a relationship directly. Roll only when the response is meaningfully uncertain. The momentary attitude of a scene and the persistent relationship are different: an ally can be angry now and an enemy can cooperate briefly.

Day 1 already applies direct relationship changes with Ingrid. The RPG state now also records each such change as a social graph effect.

## 8. Unified conflict

1. Establish the domain, stakes and participants.
2. Each active side chooses one of the four actions.
3. Attack and Defend are opposed totals.
4. Positive difference becomes stress.
5. A consequence may absorb 2, 4 or 6 shifts.
6. At stress capacity, the participant is taken out unless they concede first.

Being taken out means losing the stated stakes, not automatic death, mind control or deletion of the character's identity. The framework can run a fistfight, argument, chase, institutional hearing, intrusion or psychic struggle.

## 9. Cyber actions

Cyber is initially ordinary action resolution:

`4dF + Cybernetics + Infosec` against system difficulty.

Success may create an `access` edge, reveal a node, create an advantage or modify graph state. Failure may add Trace, alert an autonomous agent or expose an implant. Detailed network topology belongs to the separate hacking simulator and is added to RPG scenes only when play requires it.

## 10. Psi actions

Noöpunk PSI is **trajectory steering in the Conscious Agent Network**. It does not create arbitrary effects: it makes an already possible cognitive, social, cybernetic, noetic or physical trajectory easier to enter.

Resolve PSI with the normal action system:

`4dF + relevant attribute + relevant skill + trajectory modifier` against difficulty or opposition.

The scene establishes seven context ratings from 0 to 4:

- semantic distance;
- existing corridor strength;
- bifurcation openness;
- affective salience;
- composite-agent coherence;
- instrumentality, meaning pressure to behave like deterministic telecoms;
- local noise.

Corridor, openness, salience and coherence support the action. Distance, instrumentality and noise resist it. The difference is halved toward zero and limited to −4…+4. This is the **wu wei rule**: steering a system along a path it was almost taking is easier than forcing an alien trajectory.

### General PSI operations

| Operation | Typical action | Default approach |
|---|---|---|
| Intuition or precognition | Create Advantage | Awareness + Notice |
| Telepathy or resonance | Create Advantage | Charisma + Rapport |
| Remote perception | Overcome | Awareness + Notice |
| Synchronicity or reconnaissance | Create Advantage / Overcome | Awareness + Investigate |
| Psychokinesis | Overcome an unstable physical trajectory | Willpower + Will |
| Ritual or shared dream | Create Advantage | Charisma + Rapport |
| Psychosurgery | Overcome or conflict action | Intelligence + Medicine |
| Psychic hacking | Attack | Willpower + Will |
| Noetic defense | Defend | Willpower + Will |

These are defaults, not a closed power list. A scene may use another approach when the fiction clearly supports it.

### Effects

A successful PSI action normally creates or changes one graph relation, reveals an attractor, creates an aspect, opens a route or defends an agent boundary. Critical success strengthens the graph effect. Psychokinesis targets a physical trajectory; other initial modes normally target the noetic proxy graph.

Only effects from a successful action may be applied. PSI does not prove whether the event came from non-local consciousness, BCI mediation, a shared dream, psychotronic intervention or another layer.

### Wendt constraints

When PSI is the scene's central investigation or conflict, record:

- the **basis** of the question, such as threat, attachment, identity, location,
  historical truth or therapeutic meaning;
- the mode: **read**, **participate** or **steer**;
- the character's intention and already possible target trajectory;
- any institutional-field aspect shaping what can be actualized.

Repeated PSI probes are not independent scans. An incompatible second basis may
raise difficulty by one, change the available information or add Instability,
because the first intervention has already changed the context. Never use this
rule to erase a successful clue.

Telepathic and resonance results normally separate `source_intention`,
`shared_structure`, `receiver_actualization` and `residual_ambiguity`. Direct
experience is not infallible mind-reading. Group PSI requires shared intention,
reciprocal attention, a semantic frame, a corridor/interface and a voluntary way
to leave; it creates a temporary `composite_actor`, not proof of group qualia.

Full rationale and data fields are in
[`WENDT_PSI_RULES.md`](WENDT_PSI_RULES.md).

### Pressure

PSI creates three inspectable pressures rather than a mana pool:

- **Psyche Load:** immediate experiential and psychological strain;
- **Noetic Trace:** a route by which another agent or system can follow the action back;
- **Instability:** growing uncertainty in identity, layer boundaries or the local trajectory landscape.

Success normally creates a little load. Costly or failed steering creates more pressure. Strong instrumentality particularly increases Trace. Conditions and consequences give the pressure its concrete fictional form; detailed recovery tracks are added only when play requires them.

### Cross-layer PSI

A PSI action may request a typed cross-layer effect through an interface such as a BCI:

`Cyber → Physical → Noetic` or `Noetic → Social/Cyber`.

The effect records source and target layers, interface, trigger, provenance hypotheses, consent requirement and reversibility. A successful roll does not authorize a consent-required identity change when consent is absent. Hostile influence must use conflict stakes and cannot silently replace the target's agency.

### Example

Romppainen attempts resonance with Ingrid during an open shared-dream bifurcation. Their history, emotional salience and existing corridor support the action; local noise resists it. On success the action creates a `resonance` graph effect. The session also records Psyche Load. If Romppainen attempted to extract an arbitrary serial number from a stranger, semantic distance and instrumentality would strongly resist the action and increase the risk of Trace and Instability.

## 11. Psychosurgery

A psychosurgery session may:

- reveal a hidden aspect;
- integrate or replace an aspect with consent;
- add a condition;
- heal a consequence with consent and suitable care;
- reveal a memory without declaring it historically true;
- create a noetic resonance edge;
- destabilize identity as a consequence.

Consent is a mechanical boundary. Observation and involuntary harm can occur in the fiction, but beneficial identity editing and consequence treatment require consent in the generic API. The session log records effects without deciding whether the experienced layer was dream, psychedelic state, VR or astral projection.

## 12. Resources and reputation

Money, favors, access, bandwidth and institutional standing are integer ratings or tags only when a scene spends or tests them. Reputation is stored per network or institution. V0.1 has no detailed accounting, gear prices or universal economy.

### Structural-semantic actions

Concepts, narratives and institutional classifications may be represented as
typed subgraphs in the Social, Cyber or Noetic layer. This does not add a fifth
layer or a new dice system. Use the normal four actions:

- **Read local structure** (Create Advantage, Intelligence + Investigate) reveals
  relevant relations around a sign or concept;
- **Find an invariant** (Create Advantage, Intelligence + Program or Investigate)
  compares two local maps without declaring them identical or true;
- **Refine / meet** and **generalize / join** (Create Advantage) construct a
  narrower or broader concept from explicit attributes;
- **Rearticulate** (Overcome or Attack) changes a relation, framing or subject
  position; involuntary identity change is always an explicit conflict;
- **Defend meaning** (Defend, Willpower + Will) resists imposed framing and
  preserves the agent's own account.

A successful action normally reveals or changes one edge and records provenance
and confidence. Costly outcomes may create `semantic_drift`, `false_invariant`,
`frame_capture` or `provenance_loss`. If the action crosses into a noetic or
psychosurgical target, also apply consent, Psyche Load, Noetic Trace and
Instability rules. Structural similarity never by itself proves truth,
understanding, consciousness or a noetic connection.

The research basis, philosophical limits and expanded operation table are in
[`LLM_STRUCTURALISM_AND_NOOPUNK.md`](LLM_STRUCTURALISM_AND_NOOPUNK.md).

### Context, recognition and infrastructural power

Wendt, Critical AI, The Stack, Protocol and xenofeminism add uses for existing
actions without adding a new dice engine:

- **Contextual actualization:** when a scene genuinely makes an identity or
  preference context-dependent, record the prior potential, intervention,
  institutional context and actualized result. This is not a free reroll or
  proof of physical quantum effects.
- **Recognition conflict:** an AGI, upload, NHI or collective agent may contest
  classification as person, property, phenomenon or threat. The stakes name who
  has classification authority and which jurisdiction applies.
- **Critical AI audit:** trace extractivism, automation, essentialism,
  surveillance and containment through data, labor, energy, ownership and
  governance edges. Failure may create `ethics_washing`,
  `classification_capture` or `infrastructural_dependency`.
- **Protocol action:** negotiate, fork, exploit or refuse a protocol. Outcomes
  affect interoperability, addressability, access and jurisdiction rather than
  generic system hit points.
- **Xenofeminist repurposing:** overcome a naturalized role or infrastructural
  barrier by opening, forking, collectivizing or redesigning technology.
  Voluntary transformation preserves agency; coerced normalization is an Attack,
  never treatment.

These operations are detailed in
[`WENDT_CRITICAL_AI_THREE_PARADIGM_SHIFTS.md`](WENDT_CRITICAL_AI_THREE_PARADIGM_SHIFTS.md),
[`THE_STACK_PROTOCOL_AND_CYBERSPACE.md`](THE_STACK_PROTOCOL_AND_CYBERSPACE.md)
and [`XENOFEMINISM_AND_NOOPUNK.md`](XENOFEMINISM_AND_NOOPUNK.md).

## 13. Advancement

At a significant milestone, gain one advancement point. Spend one point to raise one skill by +1, to a maximum of +4. Aspect revision, new stunts and recovery from major consequences require an appropriate story milestone. Attributes do not rise in v0.1.

## 14. Factions

A faction needs only:

- a goal;
- influence and resources;
- relevant assets and relationships;
- one or more project clocks.

Between game days, advance at most one relevant project by one step unless player action changes it. When a project completes, express the result through scenes, news, rumors or graph changes. Ubiquitous Maniacs initially needs only UFAB and scenario-relevant external actors; it does not simulate the entire solar system.

## 15. Worked example in three forms

### Tabletop

Romppainen studies a UFAB terminal for an inconsistency. The GM sets difficulty Fair (+2), then raises it to Great (+4) for institutional concealment. Romppainen rolls 4dF = 0, adds Awareness +2 and Notice +2: total +4, a success. He discovers that the patient file changed names and creates the advantage **UFAB record mismatch**.

### Python

```python
result = resolve_action(
    romppainen,
    attribute="Awareness",
    skill="Notice",
    difficulty=4,
    action=ActionType.CREATE_ADVANTAGE,
    roll=0,
    created_aspect="UFAB record mismatch",
)
```

`roll=0` is the predetermined total of the four Fate dice. Omitting it performs a random roll.

### Graph update

```python
effect = GraphEffect(
    domain="cyber",
    operation="set_edge",
    source=romppainen.id,
    target="ufab_patient_registry",
    key="access",
    value="observed_metadata",
)
apply_graph_effect(ufab_graph, effect)
```

The same fictional action therefore has a tabletop result, a deterministic test representation and an inspectable graph consequence.

## 16. Ubiquitous Maniacs validation

Day 1 already exercises:

- Dr. Dahl intake through Deceive, Kinesics and persistent assessment flags;
- direct and checked social choices with Ingrid;
- aspects, conditions and consequences;
- investigation and information persistence;
- relationship changes and social graph effects;
- therapy and ambiguous shared experience;
- cyber/noetic concepts without a separate minigame;
- fail-forward results and a safe terminal scene.

The new generic conflict, PSI, cyber, psychosurgery and faction APIs are deliberately not forced into every Day 1 choice. They are available for Days 2–3 when an actual scene needs them.

## 17. Influences, simplifications and open questions

### Mechanical ancestry

- Fate/Fudge family: 4dF, ladder, aspects, stunts, consequences and four actions;
- *Transhumanity's Fate* and *Eclipse Phase*: transhuman identity questions and the Ego/Morph distinction;
- *Psi-punk*: PSI as social and technological infrastructure;
- *Shadowrun*: overlapping physical, cyber and anomalous operational layers;
- *Cities/Stars Without Number*: compact NPCs, tags, projects and faction motion;
- *The Expanse*: material consequences, social pressure and character-centered science fiction.

### Deliberately simplified

- one resolution engine;
- no tactical initiative or movement grid;
- no full Fate point economy;
- no detailed gear, money or reputation economy;
- no mandatory PSI resource pool;
- no complete morph, fork or resleeving subsystem;
- no integrated autonomous faction simulation;
- no claim about the ultimate ontology of Psyche.

### Intentionally undefined until play demands it

- final attribute and skill advancement economy;
- exact Noetic Effort / Psyche Load model;
- detailed consent rules for hostile psychic conflict;
- fork and continuity procedures;
- spaceflight and habitat conflict;
- Heat, Trace and Instability pressure tracks;
- full interaction between the RPG, social simulation and hacking simulation.
