# NoöPunk rules reset memo: four Luhmannian systems

> **Status:** exploratory design memo for issue #32. **Nothing here is finalized.**
> **Authority:** this document does not override `RULEBOOK.md` or author-specified
> decisions. It selects no attribute structure, no dice mechanic, and no skill.
> **Purpose:** answer the ten questions in #32 and lay a theoretical foundation
> that a later author decision can build on.
>
> **Direction (author, #32):** NoöPunk develops an **original** rules system.
> Existing games may be consulted as comparative references, but none defines the chassis or supplies default mechanics. The system grows outward from the four
> Luhmannian systems below.

---

## 1. The starting question: what is a character?

Most RPGs answer this without asking it. A character is a **unified agent**: one
sovereign box with an attribute list, a skill list, and equipment attached. Social
ability is a skill on the same chassis as combat. Technology is gear. The
character is the unit of agency and everything else is a modifier.

The NoöPunk reset starts from a different answer, taken from Luhmann:

> **A character is not a unified agent. A character is a temporary, unstable
> coupling of several operationally distinct systems.**

Luhmann's claim is that biological, psychic, and social systems are not layers of
one entity. They are separate autopoietic systems, each reproducing its own
operations in its own medium — life, consciousness, communication — and none of
them can perform another's operations for it. They are **structurally coupled**:
they can perturb each other constantly, but a perturbation is not a command. A
thought cannot digest your lunch. A conversation cannot think.

NoöPunk adds a fourth domain, the **Cybernetic** (§6). The design bet is that
networked computation, autonomous software, and machine-to-machine communication
now behave enough like an operational domain of their own that the game should
treat them as one.

The consequence for play is not flavour. It is mechanical: **capacity in one
system does not transfer into another system.** A superb body does not win an
argument. A brilliant mind does not repair a broken leg. A powerful social
position does not survive a network intrusion that erases the record of it.

---

## 2. The four systems

| System | Medium / operation | What it governs in play |
| --- | --- | --- |
| **Social** | communication | relationships, reputation, persuasion, institutions, organizations, networks, collective meaning, participation in social systems |
| **Physical** | life / bodily process | body, movement, endurance, perception, injury, biological limits, embodiment |
| **Psychic** | consciousness | cognition, attention, imagination, memory, will, and — later and separately — anomalous cognition |
| **Cybernetic** | machine communication | software, hacking, implants, AI systems, distributed cognition, cybernetic extensions of agency |

Two things to hold onto:

- **These are domains, not a synonym for attributes.** The issue calls them the
  *starting architecture*. Whether each becomes one number, several numbers, or a
  number plus a resource is the open question in §5 — deliberately unresolved.
- **They are entangled even where they are analytically distinct.** Luhmann's
  point is not that the systems are isolated. It is that they are *operationally
  closed and causally coupled* — which is exactly what makes interaction between
  them interesting rather than additive (§4, §7).

---

## 3. What each system represents in play

Each system answers a different question about a character:

- **Physical** — *what can this body do, and what can it survive?*
- **Psychic** — *what can this mind hold, notice, intend, and endure?*
- **Social** — *what can this person move other people to do, and what will they
  be believed about?*
- **Cybernetic** — *what can this character do through machines and networks, and
  what can be done to them through those same channels?*

Note the fourth question is deliberately **two-sided**. The cybernetic domain is
the only one where being capable and being exposed are the same fact: to be deeply
networked is to be reachable.

---

## 4. How interactions between systems should work

The theory gives one hard constraint and one productive looseness.

**Hard constraint — no direct substitution.** You cannot spend Physical capacity
to solve a Social problem. Resolution stays inside the acting system.

**Productive looseness — coupling.** Crossing domains is not a modifier; it is
its own step. A character does something *in* one system in order to perturb
another. The perturbation can work, partially work, or fail — independently of
whether the originating action succeeded.

That yields the interaction vocabulary the rest of the design can use:

- **Direct action** — act within one system. Resolve in that system's medium.
- **Coupling** — act in one system to perturb another (say something to change a
  body's state; take a drug to change a mind; interface to change a social record).
- **Contest** — two characters act in the same system, and the stronger position
  in *that* system decides.
- **Cascade** — a successful perturbation makes the target system act differently,
  which can then perturb a third. This is where "strange consequences" live.

A cascade is the mechanical home of the setting's strangeness: change a record and
you change what people believe; change what people believe and you change what the
body is allowed to do.

---

## 5. Proposed ultra-minimal attribute structures (comparison, not selection)

Four candidate structures, all ≤ 8 numbers, all derived from the four systems
rather than borrowed from any existing game. **These are presented for comparison.
None is selected. No dice mechanic is implied by any of them.**

### Structure A — Pure four (4 numbers)

One rating per system. Nothing else. The character sheet is four numbers.

- *Strength:* absolute floor of complexity; makes the "no substitution" rule
  visible at a glance; trivial to port to Godot and Concordia.
- *Cost:* cannot express a system that is powerful but fragile, which is central
  to the asymmetric-posthumanism tone; every distinction must be re-invented
  inside a single number.

### Structure B — Four systems plus one shared medium (4 + 1 numbers)

One rating per system, plus a single shared pool representing the character's
available **meaning / attention** — the thing all four draw on when they couple.

- *Strength:* makes coupling cost something, so crossing domains is a real
  decision rather than a free route around a weak system; one pool is very little
  arithmetic at the table.
- *Cost:* introduces a resource that has to be tracked and refreshed, which is a
  step back toward conventional bookkeeping; the pool must be justified in the
  fiction or it becomes an abstract counter.

### Structure C — Four systems plus interface ratings (4 + up to 6 numbers)

One rating per system, plus a rating for each **coupling path** a character has
developed. In its leanest form a character has only the interfaces they have
actually built, so a starting character might carry four numbers and no
interfaces at all.

- *Strength:* the theory lives directly in the sheet — systems are closed, and
  what you actually own is the *paths between* them; makes cascade play concrete;
  scales up by adding paths, not by inflating numbers.
- *Cost:* the most conceptually demanding option; risks becoming a graph rather
  than a character sheet; needs a firm cap to stay simple.

### Structure D — Reach and coherence per system (4 × 2 numbers)

Each system has a **reach** (what it can affect) and a **coherence** (how well it
holds together under stress). A character can be formidable and brittle in the
same domain.

- *Strength:* models operational closure honestly — a system under stress stops
  being able to operate in its own medium; directly produces the "extraordinary in
  one domain, ordinary in another" texture the design wants; gives a natural,
  non-hit-point way to represent damage per domain.
- *Cost:* eight numbers is the most proposed here, and the two axes invite
  derived-stat creep, which the guardrails forbid.

### Comparison

| | Numbers | Best at | Main risk |
| --- | --- | --- | --- |
| **A** | 4 | simplicity, portability | cannot express asymmetry or fragility |
| **B** | 5 | making coupling cost something | resource bookkeeping |
| **C** | 4–10 | expressing coupling as the core idea | conceptual weight, graph creep |
| **D** | 8 | expressing closure and fragility | derived-stat creep |

A, B and C share one number per system and differ only in whether coupling is
free, paid for, or rated; D changes the meaning of the number itself. The choice
between them is a choice about **what the game is about** — cheap and clean (A),
costly crossing (B), or coupling-as-identity (C) — and that is an author decision,
not an agent one.

**A and B are the two most likely to satisfy "extremely simple".** C is the most
distinctively NoöPunk. D is the most expressive and the most dangerous.

---

## 6. The cybernetic question

Luhmann distinguished biological, psychic, and social systems. NoöPunk adds
cybernetic. The design task is to say whether that is justified, not to assume it.

The case **for** treating it as a fourth operational domain:

- machine-to-machine communication now runs continuously without a human
  participant in the loop, which is the structural feature Luhmann used to
  separate social systems from psychic ones;
- the domain has its own medium (the network / the machine interface) and its own
  closure — a network can act on itself in ways no participant fully authorizes;
- it is the only domain a character can be *extended into* and *exposed through*
  simultaneously, which is genuinely unlike the other three;
- it is where the setting's cyberpunk half actually lives mechanically, rather
  than as equipment attached to a unified agent.

The case **against**:

- the domain may be better modelled as an *interface between* Social and Physical
  than as a fourth system;
- "machines communicate" may be a metaphor rather than a real operational closure;
- a fifth domain invites a sixth, and the system grows rather than shrinks.

**Recommendation: keep it, as a hypothesis under test.** It is the single most
NoöPunk thing in the architecture, and the issue asks for exactly this
exploration. But it should be treated as the system most likely to be revised,
and any mechanic built on it should be the most reversible.

---

## 7. Can the whole core mechanic emerge from these four systems?

Probably, and in a way that is genuinely minimal — but the issue's guardrail
applies, so this is a sketch of *shape*, not a proposal.

The emergent shape is:

1. **An action names its system.** Resolution happens in that system's medium.
2. **Success is resolved inside that system**, using only that system's rating
   (and whatever the later author decision adds — skills, if any).
3. **Crossing domains requires a coupling step**, which is separate and can fail
   on its own.
4. **Cascades follow from successful couplings**, not from special rules.

If that holds, then the entire core is: *one resolution procedure, applied four
times, plus one coupling procedure.* That is a very small core.

**What must not be locked in:** the dice mechanic, the rating scale, whether
ratings are single numbers or pools, and whether coupling is a check, a cost, or
a rating. Those are author decisions and the issue explicitly forbids finalizing
them.

---

## 8. The absolute minimum number of numbers

**Four** — one per system (Structure A).

That is the floor, and it is worth stating plainly because it is the strongest
argument that the design is genuinely simple: four numbers and a coupling rule is
enough to be a playable *architecture*, even if later decisions add to it.

Everything above four must earn its place individually. The memo's own
recommendation is that if a fifth number is added, it should be the shared medium
(Structure B) or a coupling path (Structure C) — because those express the theory
— and **not** a conventional derived statistic.

---

## 9. What remains explicitly undefined

The reset deliberately leaves these open. Agents must not fill them.

- the dice mechanic, and whether there is one
- rating scale, range, and generation
- whether systems carry one number, several, or a number plus a resource
- skills: existence, list, levels, and how they bind to systems
- character creation and starting values
- advancement / experience
- combat resolution, damage, health, wounds, armour, initiative
- how the Physical system represents injury in play
- psionic powers and psionic mechanics
- how anomalous cognition couples to the other systems
- cyberware and augmentation rules
- equipment statistics and economy
- the Noösphere as a mechanical object
- everything about NHI
- hacking / cyberspace subsystems
- factions, professions, geography, quests
- how the three runtimes represent coupling and cascade
- whether the cybernetic system survives review (§6)

---

## 10. What makes this structurally different from conventional RPG stats

1. **The unit is not a unified agent.** Conventional sheets describe one agent
   with many facets. Here the character *is* several systems, imperfectly joined.
2. **Capacity does not transfer between domains.** No single scalar, no point
   buy, and no "main stat" — the classic optimization target does not exist.
3. **Asymmetry is structural, not a build choice.** A character is *necessarily*
   strong in some domains and weak in others; that is a property of the model,
   not a balancing knob.
4. **Social is a system, not a skill.** Communication has its own medium and its
   own closure, so social conflict is not combat with different words.
5. **Technology is an operational domain, not equipment.** Cybernetics governs
   what a character can do *through* machines and what can be done *to* them.
6. **Crossing domains is a procedure, not a modifier.** Coupling can succeed while
   the originating action fails, which is a genuinely unusual resolution shape.
7. **Consequence travels by cascade.** Effects propagate between systems rather
   than accumulating on one track.

---

## 11. Layering later material without rewriting the core

The reset is worth little if Law of One, the Noösphere, or psionics force a core
rewrite later. The architecture above is designed to avoid that, because **every
one of them is a coupling phenomenon** — and coupling is already in the core.

- **Psionics** — a *mode of coupling*: acting in the Psychic system to perturb
  another system without the ordinary medium. That is a coupling path with unusual
  properties, not a fifth attribute. Psionics can therefore be added by declaring
  a new *kind* of coupling, leaving the four systems untouched.
- **The Noösphere** — a *shared system* that characters couple to, rather than a
  property of a character. It is collective, so it belongs with Social and
  Cybernetic at the level of the world, not on the sheet.
- **Law of One / social memory complex** — a *fusion rule*: what happens when two
  or more characters' Social and Psychic systems couple hard enough to form a
  single operationally closed system. This is why "entanglement may become
  mechanically important" (issue), and the architecture already has a place for it.
- **Vallée-style interdimensional material** — a *source of coupling that is not
  another character*: the thing on the other side of the coupling is what changes,
  not the four systems.

The requirement this places on the core is modest and worth stating as a design
constraint: **the core must name the four systems and the coupling procedure, and
must not name psionics, the Noösphere, or any metaphysical layer.** If those
appear only as *kinds of coupling*, they can be layered on indefinitely — which is
the "small core, strange consequences" target and the modularity the issue asks for.

---

## 12. Open theoretical questions

1. Is the cybernetic domain a genuine fourth operational system, or an interface
   between existing ones? (§6)
2. Is coupling best modelled as cost, check, or rating? (§5)
3. Does operational closure need per-system fragility (Structure D), or is that
   expressible through coupling failure alone?
4. Where does **agency** live if the character is a coupling of systems? A
   distributed character may act in several systems at once — is that one turn or
   several?
5. What does *damage to a social system* or *damage to a cybernetic system*
   mean without importing hit points by another name?
6. Can cascade be bounded so it produces strangeness without producing
   bookkeeping?
7. Does the Noösphere belong on the character sheet at all, or only in the world?
8. What is the character sheet's *smallest honest* form for each of the three
   runtimes — tabletop, Godot, Concordia?

---

## 13. What this memo does not do

- It does not remove or replace `RULEBOOK.md`. The legacy rules currently in
  force remain in force until the author revises them.
- It does not select an attribute structure, a dice mechanic, or a skill list.
- It does not import mechanics from any existing game.
- It did not modify `AGENTS.md` or `docs/DESIGN_PRINCIPLES.md` at the time of writing.
  That tension has since been **resolved by the author**: invariant 9 and `AGENTS.md` §15
  are now "Original NoöPunk rules only", so no external game supplies default mechanics
  or a chassis. This memo no longer needs an author decision on that point.
- It does not touch the Godot or Concordia runtimes.
