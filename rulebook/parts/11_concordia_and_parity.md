# Reference: Concordia, Adaptation, Persistence and Parity

> Generated, verbatim segment of [RULEBOOK.md](../../RULEBOOK.md) (the extended-canon run). The rulebook file is canonical; this part and its section numbers are unchanged so that cross-references keep resolving. Regenerate with `python3 tools/split_rulebook.py --apply`.

## 22. Structured actions for Concordia

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Whenever practical, agents should choose from structured legal actions rather than asking an LLM to invent arbitrary mechanical commands.

Example:

```json
{
  "action": "hack",
  "actor": "character-id",
  "target": "system-id",
  "method": "credential_attack"
}
```

The rules engine validates and resolves the action.

The GM/narrator then converts the result into prose.

This separation is important for reproducibility and social-science simulation.

---

## 23. Persistence and reproducibility

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

World state and agent memory must persist.

Simulation tests should be reproducible.

Where randomness is involved:

- allow a seeded RNG;
- record important rolls/results;
- make save/load round trips testable;
- avoid hidden LLM-generated numeric state changes.

The same saved state plus the same deterministic inputs should reproduce the same mechanical results.

---

## 24. Lighter rules escape hatches

**Status: EXPERIMENTAL REFERENCES.**

EP2 is an influence and a legacy prototype source, quarantined from the intended CC release surface (see docs/licenses/ISSUE_200_CC_RELEASE_GATE.md); it is not a chassis.

If a subsystem is too cumbersome for Concordia, compare lighter approaches including:

- Transhumanity's Fate,
- Neon City Overdrive-style EP conversions (proprietary; a comparison only, not a source),
- Powered by the Apocalypse-style EP conversions,
- later native NoöPunk mechanics.

The design lesson may be:

> preserve the useful world-model concept while radically compressing the mechanic.

Do not switch the entire game system casually. Replace subsystems deliberately and record the change here.

---

## 25. Rules adapter contract

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Concordia should communicate with an abstract rules interface rather than hard-coded EP classes.

Conceptually:

```python
class RulesEngine:
    def check(...): ...
    def attack(...): ...
    def defend(...): ...
    def social_check(...): ...
    def hack(...): ...
    def damage(...): ...
```

This allows the implementation to evolve from:

```text
EP2
  ↓
simplified EP2
  ↓
mixed EP2 / NoöPunk
  ↓
native NoöPunk
```

without replacing the simulation architecture.

---

## 26. Rule-change procedure

Every meaningful mechanical change should follow this sequence:

1. **Identify the current rule.**
2. **Mark its provenance:** EP2 baseline, modified EP2, NoöPunk native, experimental, or deferred.
3. **Write the new human-readable rule in RULEBOOK.md.**
4. **Record what it replaces.**
5. **Update structured data/code.** The per-subsystem status record for this step is
   [`data/rules/conversion_matrix.json`](data/rules/conversion_matrix.json), explained
   in [`docs/rules/EP2_CONVERSION_MATRIX.md`](docs/rules/EP2_CONVERSION_MATRIX.md):
   update the row for the subsystem you changed, so the inherited / modified /
   replaced / deferred picture stays readable in one place rather than only in this
   ledger's prose.
6. **Add or update deterministic tests.**
7. **Update Concordia adapters/prompts only after the rule is stable enough to execute.**
8. **Record licensing/provenance if EP-derived material or external data is involved.**

Do not leave important canonical mechanics only in issue comments or commits.

---

## 27. Change ledger

Use this table to track major mechanical mutations.

| Date | Subsystem | From | To | Status / reason |
| --- | --- | --- | --- | --- |
| 2026-10-03 | Overall chassis | Original-from-scratch NoöPunk rules reset | EP2 homebrew foundation with evolutionary replacement | **Current direction.** Issue #60 supersedes the archived reset for active development. |
| 2026-10-03 | Runtime priority | Tabletop-first staged ports | Concordia-first playable RPG/simulation using tabletop-readable rules | **Current direction.** The rulebook remains canonical documentation, while Concordia is the immediate playable target. |
| 2026-10-03 | Setting continuity | Separate NoöPunk world progressively replacing Eclipse Phase | **Alternate Eclipse Phase timeline before the Fall; year 20XX; Earth intact; EP technology baseline** | **Current direction.** Preserve EP concepts by default and document deliberate timeline divergences. |
| 2026-10-03 | Layer ontology | Four layers treated implicitly across §15–§19 | **Explicit four-layer ontology with structural couplings (§36)** | Issue #78. Couplings made explicit because the interfaces are where the gameplay is; no mechanics defined. |
| 2026-10-04 | AGI catastrophe structure | Earlier drafts used named contemporary AI companies for a four-disaster cascade | **Multiple rogue-AGI disasters with fictionalized 20XX actors and no fixed global sequence (#98)** | Issue #98 supersedes the named-company chronology. Detailed named variants are archived; active canon keeps the disasters structural and unordered. |

| 2026-10-04 | Theory sections | Four-layer ontology and bibliography deleted by a stale-branch clobber (`901ba05`) | **Restored as §36 (four NoöPunk systems) and §37 (theoretical sources)** | The clobber removed 703 lines; the glossary kept `## 34.`, so number-keyed guards read the wrong section and the loss was silent. Restored by heading text; §27 number stays with the glossary. |
| 2026-10-04 | Sources list | Two competing sources sections (#99 landed twice as §35 and §38) | **Merged into a single §35; the duplicate §38 removed** | Issue #101. The union of both copies is kept: the fuller fiction and RPG entries from §38, the broader field list and preambles from §35. §35 now declares itself the design-facing map beside the §37 theory bibliography, and §33.2's Wendt citation is re-pointed from the stale §35.5 to §36.5. |
| 2026-10-06 | Default affiliation and Affect-graph prose | In-world `UNHSS` naming and a `-100 to +100` Affect/Contact/Reputation score in `RULEBOOK.md` prose | **`UNSA` everywhere in-world; the Affect graph reads `-10 to +10`** | Issue #149 was rebased to `rulebook/8_FACTIONS.md` alone before merge (`40e10a5`), so the rename and rescale reached the chapter, schema, runtime and data but not the canonical prose — the book contradicted its own §38 and `8_FACTIONS.md`. Residue cleared; the separate Law-of-One **Polarization** axis (§9.3, `-100 ... 0 ... +100`) is a different subsystem and keeps its wider band. |

Add rows whenever a major subsystem is replaced or substantially reskinned.

---

## 28. Immediate rulebook work

As the first playable vertical slice is implemented, expand this file with concise executable descriptions of:

- [ ] exact EP2-derived test procedure used by code;
- [ ] opposed test procedure;
- [ ] pools/resources actually implemented;
- [ ] damage/wound procedure;
- [ ] stress procedure;
- [ ] combat sequence;
- [ ] basic mesh/hacking procedure;
- [ ] social action procedure;
- [ ] embodiment/morph rules used by the prototype;
- [ ] inventory/gear rules;
- [ ] character creation subset;
- [ ] save/load relevant state;
- [ ] structured action vocabulary exposed to agents.

Only document mechanics that we actually intend to use. The purpose is not to rewrite Eclipse Phase.

---

## 29. Definition of a healthy rulebook

This document is healthy when a developer, player, or agent can answer:

- What rules are we currently using?
- Which ones still come from EP2?
- Which have been changed?
- Which are native NoöPunk?
- Which systems are intentionally unfinished?
- What does the deterministic code resolve?
- What is left to Concordia/LLM judgment?
- Where did an imported rule or dataset come from?
- Why did a major mechanic change?

If the answer requires spelunking through old commits, Discord-like issue archaeology, or guessing from Python, update this rulebook.

---

## 30. Governing principle

**Build first. Play it. Simulate it. Observe what Concordia actually needs. Then simplify and mutate the rules.**

NoöPunk should remain playable throughout its transformation.

The destination is **not a separate setting wearing borrowed EP mechanics**.

The destination is a playable **alternate pre-Fall Eclipse Phase timeline** in which NoöPunk's paradigm shifts reshape an intact Earth and wider transhuman civilization. Rules may still mutate through use, but the Eclipse Phase continuity and technology baseline are now intentional parts of the premise.

## 36. The four NoöPunk systems: Physical, Psychic, Social and Cybernetic

**Status: NOÖPUNK NATIVE THEORETICAL ONTOLOGY; author-specified in issue #78.**

This section states *why* NoöPunk divides its world into four systems. It is the
theory-side companion to the character architecture in §9 and the canon in §33. It
**defines no statistics and adds no mechanics**: the four-way division names what a
character (or any agent) participates in, not what it rolls.

For the character-statistics application of this ontology — the four-way division of
basic statistics, the nested-participation table, and the psychic-fundamentality
direction — see the theoretical registry entry
[`docs/archive/THEORETICAL_SOURCES.md`](docs/archive/THEORETICAL_SOURCES.md#luhmannian-four-system-character-architecture),
which remains the per-rule grounding map required by §26.

### 36.1 Luhmann's baseline and the NoöPunk extensions

The starting point is **Niklas Luhmann's systems theory**. In simplified form, Luhmann
distinguishes operationally distinct kinds of *autopoietic* systems by what they
reproduce:

- **biological / living systems** reproduce life;
- **psychic systems** reproduce consciousness / thought;
- **social systems** reproduce communication.

These systems are operationally distinct but **structurally coupled**. In particular,
language must **not** be modelled as a separate ontological layer: language is one of
the central media and structural couplings through which psychic and social systems
relate, while social systems themselves reproduce through communication.

NoöPunk deliberately **modifies and extends** that baseline for the 20XX setting. The
extensions below are the author's, and none of them is attributed to Luhmann:

| Luhmann baseline | NoöPunk for 20XX | Why |
| --- | --- | --- |
| biological / living system | **Physical** layer | in 20XX not every person is a straightforward biological organism (see below) |
| psychic system | **Psychic** layer | retained, and made the metaphysically fundamental domain |
| social system | **Social** layer | retained as communication; language stays inside it |
| — (no fourth domain) | **Cybernetic** layer | proposed fourth autonomous systems domain |
| — | no separate **Linguistic** layer | language is a medium of communication, not its own ontology |

**Physical instead of Biological.** NoöPunk should not make "biological" a fundamental
layer because in 20XX many persons are no longer straightforward biological organisms.
Characters may be heavily augmented cyborgs; resleeved into different biological morphs;
resleeved into synthetic morphs; partially or wholly artificial; instantiated as
infomorphs / software; or distributed across multiple physical substrates. This follows
the Eclipse Phase-inspired premise that personal identity and agency need not coincide
with one biological organism. NoöPunk therefore generalizes Luhmann's living/biological
system into a broader **Physical** layer. This does **not** claim that Luhmann made the
substitution; it is a NoöPunk adaptation required by the setting.

**Cybernetic as a proposed fourth domain.** Luhmann did not treat computer systems as an
additional autopoietic domain equivalent to life, consciousness and communication; for
most of the period in which the theory developed, computers were tools and environmental
structures rather than systems reproducing their own meaningful operations. NoöPunk asks
whether that remains adequate in 20XX, when systems containing autonomous AI/AGI agents,
persistent machine memory, self-maintaining software services, agent-to-agent
communication, autonomous planning, code generation and modification, automated
deployment, distributed machine economies, cybernetic infrastructure, robots and BCIs may
plausibly be treated — **at least for game/simulation purposes** — as a fourth type of
operationally autonomous, autopoietic-like system. This is explicitly a **NoöPunk
theoretical extension, not something Luhmann claimed**. A useful recent systems-theory
discussion is "From intelligence to autopoiesis: rethinking artificial intelligence
through systems theory," *Frontiers in Communication* (2025),
https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1585321/full

**No separate Linguistic layer.** Language must **not** be split off as a parallel
ontological layer from Social. Language belongs inside the Social layer because it is
part of communication and functions as a medium / structural coupling between psychic and
social systems. Splitting "social" and "linguistic" into parallel layers would work
against the Luhmannian foundation.

### 36.2 The four layers

The four layers should **not** be treated as four disconnected databases. Each names a
domain of participation and a set of operations; much of the interesting play happens at
their interfaces (§36.8).

#### 36.2.1 Physical

**Core question:** *Where and in what substrate does an entity exist?*

The Physical layer contains ordinary spacetime and embodiment:

- location and movement;
- biological morphs;
- synthmorphs;
- cyborg bodies;
- implants and prostheses;
- machines and habitats;
- server hardware supporting infomorphs;
- physical damage, energy, heat, hunger, sleep, repair, and similar constraints where
  applicable.

In 20XX the distinction between "human body" and "machine" is often historically
interesting but mechanically secondary. A person can change substrate, combine
substrates, or be partly embodied and partly virtual. This layer needs the least
metaphysical elaboration: it is the ordinary physical world, represented in play
primarily by **maps, places, objects and movement**.

#### 36.2.2 Psychic

**Core question:** *What is the state and structure of consciousness?*

This is where NoöPunk develops its strongest theoretical synthesis. The Psychic layer
records things such as:

- consciousness state;
- attention;
- valence;
- memory;
- intention;
- altered states;
- subjective continuity;
- PSI capacity;
- non-local entanglement / resonance with other conscious systems.

The theoretical background of this layer is set out in §36.3–§36.5.

#### 36.2.3 Social

**Core question:** *What communications, relationships, institutions and power structures
reproduce themselves?*

This is the most directly Luhmannian layer. Social systems consist of **communication**,
not individual human minds; the Psychic and Social layers therefore remain separate even
though they depend on and structurally couple to one another. The Social layer includes:

- interpersonal ties;
- groups and organizations;
- institutions;
- corporations;
- states;
- factions;
- rhizomes;
- discourse and ideology;
- language;
- vocabularies and specialist jargon;
- reputation and trust;
- power;
- communication networks;
- media;
- collectively reproduced expectations.

**Do not create a separate Linguistic layer** (§36.1). Language belongs here.

NoöPunk's Social layer combines two compatible emphases:

- **Niklas Luhmann:** society is constituted by communication. Persons / psychic systems
  are not components *inside* the social system; consciousness and communication are
  operationally distinct but structurally coupled. Language belongs here as a medium of
  communication rather than as an independent ontological layer.
- **Manuel Castells:** contemporary society is organized increasingly through **networks
  and flows**. Power operates through the ability to constitute networks, program them,
  connect or disconnect actors, and shape communication. See
  [*The Rise of the Network Society*](https://doi.org/10.1002/9781444319514) and
  *Communication Power* in §36.

This gives NoöPunk a Social layer that is simultaneously a **communication system + a
network society**: it can represent discourse, institutions, organizations and meaning
while giving the simulation concrete nodes, ties, flows, brokers, exclusions and power
relations. Likely game representation: **social / rhizomatic communication graphs** plus
Concordia state and narrative.

#### 36.2.4 Cybernetic

**Core question:** *What computational / machine systems reproduce their own operations,
and how are they coupled to the physical, psychic and social systems?*

This is the major NoöPunk extension of Luhmann (§36.1). By the near future, systems with
autonomous AI/AGI agents, persistent machine memory, self-maintaining software services,
agent-to-agent communication, autonomous planning, code generation and modification,
automated deployment, distributed machine economies, cybernetic infrastructure, robots,
and BCIs and human-machine assemblages may be treated as a fourth
autonomous/autopoietic-like domain.

**Haraway: humans were already cyborgs.** Donna Haraway's **"A Cyborg Manifesto"** is a
central inspiration for this layer. The cyborg dissolves simple boundaries between
human/animal, organism/machine and physical/non-physical categories. NoöPunk extends this
in a practical direction: humans have always extended cognition and agency through tools,
symbols, infrastructures and machines; in 20XX that coupling becomes explicit and
continuous.

**The Stack and the Mesh.** Benjamin Bratton's **The Stack** models planetary computation
as a vertically and horizontally integrated megastructure connecting Earth, cloud
infrastructure, cities, addresses, interfaces and users — not merely a collection of
personal devices. In NoöPunk, nearly every ordinary transhuman character has a **Mesh
Insert**, a persistent wireless BCI linked to a **Cranial Computer**. The Cranial Computer
normally runs a **Muse**, the character's personal AI agent. Characters are therefore
literal components in planetary machine networks rather than external users occasionally
"going online." The **Mesh** should feel like a synthesis of:

- a technically plausible successor to the real Internet;
- William Gibson's cultural idea of **cyberspace** as a lived network environment;
- Eclipse Phase's ubiquitous mesh;
- Bratton's planetary-scale computational infrastructure;
- Ray Kurzweil's Singularity as a transformation produced by increasingly intimate
  networking of humans and machines, rather than one isolated superintelligence.

The Mesh Insert / Cranial Computer / Muse default coupling is also recorded in §15 and is
the point at which the Cybernetic layer meets the character sheet.

### 36.3 Natural PSI, the awakening Noösphere, and the Law of One

In NoöPunk, **PSI is not produced by an alien virus or infection** (§16.1). It is a
natural capacity of human consciousness; all humans have some latent PSI potential,
though for most people it is weak, noisy or difficult to use intentionally. During the
NHI Crisis the **Noösphere is awakening**: what older psychology described metaphorically
as a collective unconscious is becoming increasingly coupled, accessible and in some
cases consciously experienced. Stronger PSI is therefore part of a planetary transition
rather than a pathogen.

The setting also borrows explicitly from the **Law of One / Ra Material** as fictional
cosmology. The canonical in-world statement is §33.6; this subsection states the same
material as the Psychic layer's ontology. In this model:

- many humans are beginning a transition associated with **fourth density**;
- awakened fourth-density humans can exhibit substantially stronger PSI;
- increasingly connected consciousnesses can form a **Social Memory Complex**, which
  NoöPunk identifies with the emerging **Noösphere**;
- fourth-density development involves **polarization** toward **Service to Others (StO)**
  or **Service to Self (StS)**;
- Earth is caught in a struggle between positive and negative polarization;
- the end of the Zookeeper quarantine is interpreted through the Law-of-One-inspired
  image of a **Council of Saturn**;
- two broad NHI alignments / factions are now active around Earth, corresponding loosely
  to positive/StO and negative/StS orientations;
- humanity's collective polarization influences which wider NHI alignment Earth develops
  toward;
- most humans remain third-density. In this fictional cosmology, those who do not make
  the transition will eventually die as Earth changes and later reincarnate in another
  third-density environment.

This is **NoöPunk lore inspired by an esoteric/religious text**, not a statement of
established science or a claim about real human destiny. Primary inspiration: Don Elkins,
Carla L. Rueckert & Jim McCarty, *The Law of One / The Ra Material* (L/L Research,
sessions beginning 1981), public archive: https://www.llresearch.org/channeling/ra-contact

**Evolution, quarantine, and advanced consciousness.** NoöPunk adopts an optimistic
metaphysical rule: **sufficiently advanced consciousness ultimately tends toward
benevolence because increasing consciousness means increasing participation in, and
recognition of, the Source / whole.** Danger therefore concentrates in beings near the
human, transhuman and early-posthuman range, where intelligence and power can grow faster
than integration, empathy or awareness of unity. The Zookeeper quarantine exists because
young technological species would otherwise be vulnerable to predation or destruction by
somewhat more advanced but still polarized civilizations. Extremely advanced conscious
beings no longer behave as simple cosmic predators. Planetary quarantine protects
developing civilizations until they reach a threshold at which open participation in the
wider ecology of consciousness becomes possible. Humanity has just crossed that threshold
in 20XX: **the quarantine is over.** This is a **setting axiom**, not a scientific
inference from the consciousness theories below.

### 36.4 Dean Radin: entanglement, PSI, and magic

Dean Radin's ***Entangled Minds: Extrasensory Experiences in a Quantum Reality*** is a key
inspiration for how NoöPunk connects quantum-consciousness ideas to psionics. The canonical
in-world statement of professional PSI and the PSI/magic overlap is §16.6; this subsection
places that material in the Psychic layer's ontology. Radin argues
that quantum entanglement offers a way to conceptualize PSI as a natural consequence of an
interconnected reality rather than as a supernatural exception to physics. In NoöPunk this
becomes part of the in-setting scientific genealogy that leads from quantum consciousness
to practical psionics, and it supports an important setting rule:

> **PSI is not a rare curse, infection, or anomalous superpower. It is a natural capacity
> of consciousness that has become technically understood, trainable, augmentable, and
> professionally usable.**

By 20XX, psionics have become a **common professional service** in many societies. NoöPunk
should evoke the everyday normalization of psychic labour seen in **Philip K. Dick's
*Ubik***: telepaths, precognitives, anti-psi specialists, psychic security, investigators,
consultants, therapists, intelligence operatives and other PSI professionals can be hired
just as one would hire a hacker, lawyer, medic or engineer.

Radin's later work also directly links PSI and traditions historically described as
**magic**. In *The Science of Magic* (2025), and earlier in *Real Magic* (2018), he treats
phenomena categorized as magic, intention effects, divination, telepathy, precognition and
related practices as belonging to the same broad empirical/parapsychological territory
rather than as fundamentally separate ontologies. For NoöPunk this becomes:

> **PSI and magic are different cultural vocabularies for overlapping consciousness-based
> phenomena.**

A ritual magician, laboratory parapsychologist, noetic engineer and fourth-density psychic
may use very different theories, symbols and practices while interacting with the same
underlying noetic reality. This does **not** mean Radin's interpretations are scientific
consensus in the real world; in NoöPunk they are fictionalized as one of the precursor
research traditions that eventually contributed to a mature science and technology of PSI.

### 36.5 The theoretical background of the Psychic layer

The Psychic layer is grounded in a body of speculative quantum-consciousness work. NoöPunk
treats these as **precursor theories** that, in the alternate future of 20XX, contribute to
a successful science of quantum consciousness — not as established science.

- **Seth Lloyd — the universe as quantum computation.** Lloyd argues that physical
  interactions can be understood informationally: physical systems process quantum
  information, and the universe can in this sense be described as a universal quantum
  computer. This supplies the broad information-physical background in which matter,
  computation and quantum information are not cleanly separable domains. Source:
  *Programming the Universe* (Knopf/Vintage, 2006/2007).

- **Penrose & Hameroff — Orch OR.** **Orchestrated Objective Reduction (Orch OR)**
  proposes that consciousness depends on biologically orchestrated quantum processes
  associated with neuronal microtubules and objective reduction of quantum states.
  NoöPunk need not treat Orch OR as established science; it is one important precursor
  theory. Source: “Consciousness in the universe: A review of the ‘Orch OR’ theory,”
  *Physics of Life Reviews* 11(1), 2014, 39–78, https://doi.org/10.1016/j.plrev.2013.08.002

- **Faggin & D'Ariano — Quantum Information Panpsychism (QIP).** They develop a
  quantum-information-based panpsychism in which consciousness is fundamental and quantum
  information has an intrinsically experiential aspect. This makes consciousness and
  quantum information two sides of one ontology rather than treating consciousness as a
  late emergent property of classical computation. For the setting it provides a
  theoretical basis for: consciousness as a quantum information field/process; PSI as
  manipulation or coupling of conscious quantum information; non-local psychic links via
  entanglement; and a principled distinction between ordinary classical computation and
  conscious quantum information. Source: “Hard Problem and Free Will: An
  Information-Theoretical Approach,” in *Artificial Intelligence Versus Natural
  Intelligence* (Springer, 2022, pp. 145–192),
  https://doi.org/10.1007/978-3-030-85480-5_5

- **Donald Hoffman — Conscious Realism.** Hoffman takes **conscious agents**, rather than
  spacetime objects, as fundamental; in his formalism spacetime and physical objects can
  emerge from interactions among conscious agents. Hoffman's theory is **not itself simply
  a quantum theory of consciousness**, and NoöPunk should not present it as one. But it
  combines naturally at the setting level with Faggin's QIP: Faggin supplies a
  quantum-information ontology of consciousness, Hoffman supplies a formal framework in
  which interacting conscious agents are fundamental and perceived spacetime is
  derivative / interface-like. This pairing is especially useful for the Psychic layer,
  because it lets psychic relations have **their own topology** rather than being reducible
  to physical distance. Source: “Objects of consciousness,” *Frontiers in Psychology*
  5:577, 2014, https://doi.org/10.3389/fpsyg.2014.00577

- **Alexander Wendt — Quantum Mind and Social Science.** Wendt brings quantum
  consciousness explicitly into social theory, challenging the assumption that
  consciousness and social life can be fully described in classical physical terms. For
  NoöPunk this is the key **bridge from theories of quantum consciousness into sociology**
  and motivates, for the simulation: social actors cannot be reduced to classical
  utility-maximizing agents; subjectivity, meaning and agency are theoretically
  fundamental; entanglement/non-separability can motivate models of social connection not
  reducible to spatial proximity; psychic and social systems remain distinct, but their
  coupling can be theorized in explicitly quantum terms. Source: *Quantum Mind and Social
  Science* (Cambridge University Press, 2015), https://doi.org/10.1017/CBO9781316005163

### 36.6 Extended mind and the collective-intelligence principle

**Cross-layer principle: consciousness and agency are more important than raw
computational scale.**

A contemporary or near-future AI is rarely an isolated "machine mind." NoöPunk's useful
unit of analysis is an assemblage such as:

> **HUMAN + LLM + LANGUAGE + INTERNET**

Likewise, a human mind is never completely isolated: cognition is extended through
language, artifacts, institutions, media, memories stored outside the skull, other people
and machine systems. Intelligence is therefore frequently **distributed and collective**,
while agency emerges from assemblages crossing the four layers. Raw compute is not the
decisive variable; **consciousness and agency matter more**. Language itself can be treated
as executable cognitive infrastructure: when humans or machines instantiate and transform
linguistic structures, language participates in cognition rather than functioning as a
passive container.

This should shape the simulation:

- do not equate compute with consciousness;
- do not equate an LLM with the entire AI assemblage in which it participates;
- represent tools, language and networks as constitutive parts of practical cognition;
- allow collective intelligence to emerge from coupled psychic, social and cybernetic
  systems;
- reserve questions of phenomenal consciousness for the Psychic layer rather than
  inferring consciousness from benchmark performance.

Relevant source: Andy Clark & David Chalmers, “The Extended Mind,” *Analysis* 58(1),
1998, 7–19, https://doi.org/10.1093/analys/58.1.7

### 36.7 Structural coupling between the layers

The four layers should not be treated as four disconnected databases. Much of the
interesting gameplay happens at their interfaces:

| Interface | Examples |
| --- | --- |
| Physical ↔ Psychic | embodiment, anesthesia, drugs, injury, neural substrate |
| Psychic ↔ Social | thought/communication, ideology, persuasion, language |
| Social ↔ Cybernetic | algorithmic governance, platforms, corporations controlling AGIs, AGIs participating in organizations |
| Cybernetic ↔ Physical | robots, sensors, infrastructure, morphs |
| Psychic ↔ Cybernetic | BCI, uploaded minds, AI-consciousness questions |
| Psychic ↔ Psychic | PSI, telepathy, remote perception, non-local entanglement |
| all four | NHI artifacts, cyber-psi interfaces, collective intelligence, Noösphere phenomena |

**Coupling is not collapse.** The layers remain operationally distinct even as they
interact:

- the **Psychic** and **Social** layers stay separate even though they depend on each
  other — consciousness and communication are different operations (§17);
- **language is not a separate layer**: it belongs to the Social layer as a medium of
  communication and a structural coupling between psychic and social systems (§36.2.3);
- cybernetic connectivity is **not** psychic entanglement: a character may be
  cybernetically disconnected yet psychically entangled, or connected to millions of
  systems with no psychic relationship at all (§15).

### 36.8 Candidate simulation representations

Keep the ontology theoretically rich but computationally simple at first:

| Layer | Main representation |
| --- | --- |
| Physical | spatial map / location graph |
| Social | social / rhizomatic graph |
| Psychic | internal state + non-local noetic / entanglement graph or hypergraph |
| Cybernetic | computer/network graph + autonomous software agents |

The Psychic layer should **not** use physical distance as its fundamental metric. If PSI
requires entanglement with a target (§16.2), psychic accessibility is based on
entanglement / coherence / resonance rather than kilometres.

### 36.9 Relationship to the modular worldbook chapters

The modular worldbook under [`rulebook/`](rulebook/) carries one chapter per layer
([`3_PHYSICAL.md`](rulebook/3_PHYSICAL.md), [`4_SOCIAL.md`](rulebook/4_SOCIAL.md),
[`5_CYBERNETIC.md`](rulebook/5_CYBERNETIC.md), [`6_PSYCHIC.md`](rulebook/6_PSYCHIC.md)), plus
[`2_ATTRIBUTES.md`](rulebook/2_ATTRIBUTES.md) for the character-statistics side,
[`7_TIMELINE.md`](rulebook/7_TIMELINE.md) for the background paradigm shifts and
[`8_FACTIONS.md`](rulebook/8_FACTIONS.md) for faction terminology. Those chapters are the
per-layer companion to this section; this section is the authoritative statement of the
ontology, and the chapters should summarize it rather than fork it. §33 records the
in-world canon that the ontology frames.

The reference chapters that follow the same pattern, and that the author requested on
2026-10-07, are:

| Chapter | Contents | Source issues |
| --- | --- | --- |
| [`10_SINGULARITY_CRISIS.md`](rulebook/10_SINGULARITY_CRISIS.md) | The Singularity Crisis, the three surviving ASI outcomes (Noösphere / Panopticon / Thanatos), cyborgist intelligence theory and the two Singularities | #177, #178, #180 |
| [`11_ONTOLOGY.md`](rulebook/11_ONTOLOGY.md) | The seven densities, vehicle-vs-entity, cryptoterrestrials, plasmoids, thought-forms, the Higher Self and the Sphere Network | #179 |
| [`12_BEINGS.md`](rulebook/12_BEINGS.md) | The working catalogue of kinds of being, hybrids, the identity-verification procedure and the class conflict | #171, #172, #179, #180 |
| [`13_EQUIPMENT.md`](rulebook/13_EQUIPMENT.md) | Equipment, cybernetic implants and psychotronic devices — descriptive lists, no statistics | #180 and the author directive |
| [`14_CHARACTER_GENERATION.md`](rulebook/14_CHARACTER_GENERATION.md) | The character-generation section: origins, backgrounds, training paths and the character-as-assemblage summary | #144 and the author directive |
| [`15_XENOPOLITICS.md`](rulebook/15_XENOPOLITICS.md) | Xenopolitics after the NHI Crisis: two-faction situation, reconstruction, the Confederacy religious explosion, the Orion hybrid panic, human reactions and campaign hooks | #187 |

These chapters are **descriptive lists with light descriptions, as the author specified**;
they define no numeric statistics and no new subsystems.

### 36.10 Issue #74 Concordia / EP2 experiment

**Status: EXPERIMENTAL.**

Issue #74 adds a deliberately tiny playable proof of concept rather than another rules
subsystem. The scenario lives in `src/text_game/issue74.py` and is launched with:

```bash
python scripts/noopunk_text.py --scenario issue74
python scripts/noopunk_text.py --scenario issue74 --ollama --llm-gm
```

The experiment reinforces the current architecture:

- **deterministic Python owns mechanics and state**: legal actions, ratings, dice,
  modifiers, opposed checks, harm/stress, inventory and objective completion;
- **Concordia/LLMs own bounded agency and language**: dialogue, natural-language intent
  translation, high-level choice among legal actions and narration of already-resolved facts;
- **simple scripted/background NPCs may coexist with LLM NPCs** in the same world;
- the first useful EP2 subset is small: percentile skill tests, a few opposed tests,
  inspectable character state and explicit world-state changes;
- large catalogs and detailed subsystems should not be imported merely because EP2 contains
  them. Add them only when a playable scenario demonstrates a need;
- **psionics remain mechanically deferred** in this prototype. Existing setting lore is
  not a license for an implementer to invent a psi rules subsystem.

A practical design rule follows:

> Concordia is the agency and narrative layer around the RPG kernel, not the authority
> that decides the rules.

The worked experiment, example playthrough and licensing note are documented in
`docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md`.

---

---

## 37. Theoretical sources and inspirations

This bibliography distinguishes **real-world theories and texts that inspire NoöPunk** from
the fictional conclusions the setting draws from them. Inclusion here does not mean that a
theory is scientifically established or that the source's author would endorse NoöPunk's
synthesis.

#### Systems, communication, networks, cyborgs, and extended mind

- **Ernesto Laclau & Chantal Mouffe.** *Hegemony and Socialist Strategy*, 2nd ed., 2001. Articulation, equivalence/difference, antagonism and hegemony ground §17.
- **Ernesto Laclau.** *Emancipation(s)* (1996) and *On Populist Reason* (2005). Empty/floating signification, collective subjects, equivalential chains and affective investment.
- **Emilia Palonen.** *The Birth and Death of Liberal Democracy in Hungary* (2025). Source for the Formula of Populism heuristic generalized by issue #107 beyond populism.
- **Tomi Toivio.** *LaclauGPT: Ideological contestation over AI*. Source for computational articulation, demands, signifier roles, frontiers, affects, provenance, and safeguards against reducing discourse to sentiment.

- **Niklas Luhmann.** *Social Systems*. Stanford University Press, 1995. English
  translation of *Soziale Systeme* (1984).
- **Niklas Luhmann.** *The Reality of the Mass Media*. Stanford University Press, 2000.
- **Raf Vanderstraeten.** “Autopoiesis and socialization: on Luhmann's
  reconceptualization of communication and socialization.” *British Journal of Sociology*
  51(3), 2000. https://doi.org/10.1111/j.1468-4446.2000.00581.x
- **Manuel Castells.** *The Rise of the Network Society*, 2nd ed. Wiley-Blackwell, 2010.
- **Manuel Castells.** *Communication Power*. Oxford University Press, 2009.
- **Donna Haraway.** “A Cyborg Manifesto: Science, Technology, and Socialist-Feminism in
  the Late Twentieth Century.” In *Simians, Cyborgs, and Women*. Routledge, 1991
  (original essay 1985).
- **Andy Clark & David Chalmers.** “The Extended Mind.” *Analysis* 58(1), 1998, 7–19.
  https://doi.org/10.1093/analys/58.1.7
- **Benjamin H. Bratton.** *The Stack: On Software and Sovereignty*. MIT Press, 2015/2016.

#### Cosmism, AGI, patternism, Global Brain, and mindplexes

- **Ben Goertzel.** *A Cosmist Manifesto: Practical Philosophy for the Posthuman Age*. Humanity+ Press, 2010. Major source for NoöPunk's constructive posthuman/cosmic horizon: joy, growth and freedom/choice; patternism; panpsychism and Universal Mind; AGI; uploading; BCI; human-AI merging; Global Brains and mindplexes; synthetic realities; nanotechnology; post-scarcity; alien and potentially extradimensional minds; PSI; meditation; psychedelics; post-religion; and "building gods."
- **Ben Goertzel.** "Glocality of Self and Memory as a Possible Foundation for Understanding Psi" (2008), https://www.goertzel.org/dynapsyc/2008/glocal_psi.pdf. A speculative glocal model of self/memory offered as a conceptual framework for precognition, telepathy and remote viewing; useful as an in-setting precursor/competing theory, not real-world confirmation of PSI.
- **Ben Goertzel.** "Patterns of Awareness: A Pattern-Theoretic, Panpsychist Solution to the Hard Problem of Consciousness" (2004), https://www.goertzel.org/dynapsyc/2004/HardProblem.htm. Source for patternist/panpsychist approaches to awareness and selfhood.
- **Ben Goertzel.** "Chance and Consciousness" (1995/1996), https://www.goertzel.org/dynapsyc/1995/GOERTZEL.html. Speculative source connecting consciousness, spontaneity/randomness, altered states and creativity.
- **Ben Goertzel.** "Evolutionary Quantum Computation: Its Role in the Brain, Its Realization in Electronic Hardware, and Its Implications for the Panpsychic Theory of Consciousness" (1997), https://www.goertzel.org/dynapsyc/1997/Qc.html. Speculative precursor for quantum-noetic computation and "systemic consciousness."
- **Ben Goertzel.** "Mindplexes: The Potential Emergence of Multiple Levels of Focused Consciousness in Communities of AIs and Humans" (2003), https://www.goertzel.org/dynapsyc/2003/mindplex.htm. Direct inspiration for nested collective persons, human-AI collectives and possible Noöspheric higher-order minds.
- **Ben Goertzel.** "The WorldWideBrain: Using the WorldWideWeb to Implement Globally Distributed Cognition" (1996), https://www.goertzel.org/papers/wwb.html. Early source for the cybernetic Global Brain lineage.
- **Ben Goertzel.** "Toward a Formal Model of Cognitive Synergy" (2017), https://arxiv.org/abs/1703.04361. Inspiration for intelligence emerging from complementary cognitive processes rather than raw compute alone.
- **Ben Goertzel.** "The General Theory of General Intelligence: A Pragmatic Patternist Perspective" (2021), https://arxiv.org/abs/2103.15100. Patternist AGI, metagraph knowledge representation, cognitive synergy, machine consciousness and machine ethics.
- **Ben Goertzel, Ted Goertzel & Zarathustra Goertzel.** "The global brain and the emerging economy of abundance: Mutualism, open collaboration, exchange networks and the automated commons." *Technological Forecasting and Social Change* 114 (2017), 65–73. Source for the Global Brain / commons / abundance side of NoöPunk's post-scarcity-versus-cyberpunk-inequality tension.

#### Quantum information, consciousness, and quantum social theory

- **Seth Lloyd.** *Programming the Universe: A Quantum Computer Scientist Takes on the
  Cosmos*. Knopf, 2006; Vintage, 2007.
- **Stuart Hameroff & Roger Penrose.** “Consciousness in the universe: A review of the
  ‘Orch OR’ theory.” *Physics of Life Reviews* 11(1), 2014, 39–78.
  https://doi.org/10.1016/j.plrev.2013.08.002
- **Giacomo Mauro D'Ariano & Federico Faggin.** “Hard Problem and Free Will: An
  Information-Theoretical Approach.” In *Artificial Intelligence Versus Natural
  Intelligence*. Springer, 2022. https://doi.org/10.1007/978-3-030-85480-5_5
- **Donald D. Hoffman & Chetan Prakash.** “Objects of consciousness.” *Frontiers in
  Psychology* 5:577, 2014. https://doi.org/10.3389/fpsyg.2014.00577
- **Alexander Wendt.** *Quantum Mind and Social Science: Unifying Physical and Social
  Ontology*. Cambridge University Press, 2015.
  https://doi.org/10.1017/CBO9781316005163

#### Psionics and esoteric / noöspheric inspirations

- **Dean Radin.** *The Conscious Universe*. HarperOne, 1997, and later experimental and
  popular work on psi/anomalous cognition. These claims remain scientifically contested in
  the real world.
- **Dean Radin.** *Entangled Minds: Extrasensory Experiences in a Quantum Reality*.
  Paraview Pocket Books / Simon & Schuster, 2006. Inspiration for NoöPunk's
  entanglement-based model of PSI.
- **Dean Radin.** *Real Magic: Ancient Wisdom, Modern Science, and a Guide to the Secret
  Power of the Universe*. Harmony, 2018. Inspiration for treating magic and PSI as
  overlapping cultural descriptions of anomalous consciousness phenomena.
- **Dean Radin.** *The Science of Magic*. 2025. Further inspiration for NoöPunk's
  integration of PSI, ritual, intention, and noetic phenomena.
- **John J. Rodger.** “Luhmann's theory of psychic systems and communication in social
  work practice.” *Journal of Social Work* 22(3), 2022.
  https://doi.org/10.1177/14680173211008107. A secondary introduction to the psychic
  system's relation to communication (§36.1).
- **Don Elkins, Carla L. Rueckert & Jim McCarty.** *The Law of One / The Ra Material*
  (L/L Research, sessions beginning 1981). Public archive:
  https://www.llresearch.org/channeling/ra-contact
- **Pierre Teilhard de Chardin.** *The Phenomenon of Man*. English translation, Harper,
  1959. Historical inspiration for the concept of the **Noösphere**.

#### Cosmology, UFO/NHI, temporality, and Disclosure inspirations

- **Philip K. Dick.** *VALIS*. Bantam, 1981. Inspiration for the non-linguistic activation signal, fragmented revelation, and the sense that information itself can transform consciousness.
- **Jacques Vallée.** Especially *Passport to Magonia* and later work on the control-system / interdimensional dimensions of UFO phenomena. Inspiration for NoöPunk's refusal to reduce all UAP to extraterrestrial spacecraft.
- **D. W. Pasulka.** Work on UFOs, religion, technology, AI, visionary experience, and contemporary belief, especially *American Cosmic* and *The Others*. Inspiration for the convergence of Disclosure, AI, religion, and the Noösphere.
- **Michael P. Masters.** Work on the extratempestrial hypothesis. Inspiration for future-human / temporal interpretations of some UFO occupants.
- **Mac Tonnies.** *The Cryptoterrestrials*. Inspiration for hidden terrestrial intelligences as one real component of the NoöPunk phenomenon.
- **Freeman Dyson.** Dyson-sphere / swarm concepts as background for technosignatures, while NoöPunk explicitly rejects energy use as a universal measure of intelligence.
- **Nikolai Kardashev.** Historical inspiration for energy-use classifications of civilizations; treated in-setting as useful but anthropocentric and incomplete.

#### Fictional psionics and normalized psychic services

- **Philip K. Dick.** *Ubik*. Doubleday, 1969. Primary fictional inspiration for a society
  in which psychic abilities, counter-psi, and paranormal professional services are
  commercialized and mundane.

#### Cyberspace, planetary computation, and collective human-machine intelligence

- **William Gibson.** *Neuromancer*. Ace, 1984. Fictional/cultural source for
  **cyberspace**.
- **Ray Kurzweil.** *The Singularity Is Near*. Viking, 2005.
- **Ray Kurzweil.** *The Singularity Is Nearer*. Viking, 2024.
- **Benjamin H. Bratton.** *The Stack: On Software and Sovereignty*. MIT Press, 2015/2016.
- **Donna Haraway.** “A Cyborg Manifesto,” 1985/1991.
- **Max Talanov et al.** "Neuropunk Revolution. Hacking Cognitive Systems towards Cyborgs 3.0." arXiv:2205.06538, 2022, https://arxiv.org/abs/2205.06538. Source for closed-loop biological/cybernetic integration, real-time neurosimulation as middleware, BCI/neurointerfaces, spiking and memristive hardware, neurostimulation and biohybrid cyborg systems.
- **Douglas Engelbart.** *Augmenting Human Intellect: A Conceptual Framework* (1962), and **J. C. R. Licklider.** "Man-Computer Symbiosis" (1960). Foundational Intelligence Augmentation sources for human-tool and human-computer cognitive assemblages.
- **Martin Dresler et al.** "Non-pharmacological cognitive enhancement." *Neuropharmacology* 64 (2013). Broad real-world review of non-pharmacological enhancement methods.
- **Kenta Kitamura.** "Assessing Human Intelligence Augmentation Strategies Using Brain Machine Interfaces and Brain Organoids in the Era of AI Advancement" (2025), https://arxiv.org/abs/2503.15508. Speculative comparison of BMI, brain-organoid and hybrid augmentation strategies.

#### RPG and setting baseline

- **Posthuman Studios.** *Eclipse Phase, Second Edition* and the openly available EP2 rules
  resources linked in §5. NoöPunk is an alternate pre-Fall homebrew continuity and must
  preserve the applicable Creative Commons attribution and ShareAlike obligations for
  EP-derived material.

#### Interpretation rule

When the rulebook says a real-world theory **makes something possible in 20XX**, that is a
fictional extrapolation unless explicitly stated otherwise. In particular, NoöPunk treats
QIP, Orch OR, PSI, fourth density, Social Memory Complexes, non-local psychic entanglement,
conscious AGI via quantum processors, uploading continuity and the Council of Saturn as
elements of its fictional world model, not as settled descriptions of the real world.

---
