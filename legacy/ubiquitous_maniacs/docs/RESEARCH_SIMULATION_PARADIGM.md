# Noopunk Research and Simulation Paradigm

This document records a conceptual paradigm for later design work.

It does not authorize implementation work.

In particular, this document does not by itself justify:

- new functional code;
- refactoring existing modules;
- changing current simulations;
- adding dependencies;
- changing the current directory structure;
- treating speculative assumptions as research findings.

## Three Levels

Noopunk combines three conceptual levels, but only the first belongs to the project's current mainstream academic core.

The levels are:

1. Critical AI Studies / mainstream social science
2. Quantum Mind / speculative ontology
3. NHI / speculative actor ontology

These levels must not be treated as having the same epistemological status.

Levels 2 and 3 are currently speculative extensions, not official empirical premises of the research core.

## 1. Mainstream Academic Core

The first level forms the actual academic core of the project.

Its current mainstream framework is Critical AI Studies, especially in relation to Simon Lindgren's work and the broader social-scientific study of AI as a social phenomenon.

This core is supported by older base theories, especially:

- Manuel Castells: network society, information, power, and networks;
- Ernesto Laclau and Chantal Mouffe: discourse, hegemony, articulation, and the construction of political identities.

At this level the project can examine, for example:

- AI as a societal phenomenon;
- AI and AGI discourses;
- power;
- capitalism;
- ideology;
- data;
- digital networks;
- social networks;
- political actors;
- institutions;
- discourses;
- sociotechnical systems.

This level must remain fully usable as an ordinary social-scientific research project without levels 2 or 3.

Conceptually:

```text
Critical AI Studies
        +
Castells
        +
Laclau & Mouffe
        ↓
Mainstream social science
```

This is the project's academic core.

If all speculative layers are removed, this core must still remain a coherent research project.

## 2. Quantum Mind as Speculative Ontology

The second level draws especially on Alexander Wendt's quantum mind and quantum social science direction, together with other possible speculative theories of consciousness ontology.

This level asks questions such as:

- what if a classical physicalist account of mind is insufficient?;
- what if agency should be modeled in a way that takes alternative ontologies of consciousness seriously?;
- how would such an ontology alter the modeling of social systems?

This level must not currently be treated as an empirically demonstrated premise of the project.

Its role is to enable speculative simulation.

Its core methodological form is:

```text
IF ontology X is assumed,
THEN what kind of social system follows?
```

Simulation does not prove the ontology true.

It is used to examine the consequences of the ontological assumption.

At this stage, this level belongs primarily to the author's broader Weltanschauung, philosophical experimentation, and the speculative layer of Noopunk.

## 3. NHI as Speculative Actor Ontology

The third level expands the question of what kinds of entities can count as social actors at all.

This includes Wendt's UAP and NHI direction together with Noopunk's broader speculative actor ontology.

Relevant questions include, for example:

- must a social actor be assumed to be human?;
- how would a social system change if it included intelligent non-human actors?;
- how might biological, technological, or otherwise speculative actors form networks?;
- how could relations among humans, AI systems, and possible NHI actors be simulated?

This level also does not belong to the empirical assumptions of mainstream academic research.

It remains speculative:

```text
IF non-human actors of type X exist,
THEN how might social systems behave?
```

The goal is not to use simulation to prove NHI hypotheses.

The goal is to build explicit models of what different actor ontologies would imply.

## Relation Between the Three Levels

Levels 2 and 3 speculatively extend the first level.

They are not prerequisites for the first level.

Conceptually:

```text
1. CRITICAL AI STUDIES
   What happens when AI becomes part of society?
                 │
                 │
                 ▼
2. QUANTUM MIND
   What if our ontology of mind and agency changes?
                 │
                 │
                 ▼
3. NHI
   What if the set of possible social actors changes?
```

The relation is therefore:

```text
MAINSTREAM CORE
      │
      ├─────────────── standalone
      │
      ▼
SPECULATIVE EXTENSION
      │
      ▼
FURTHER SPECULATIVE EXTENSION
```

Not:

```text
Quantum mind + NHI
        ↓
premises required by mainstream research
```

## Cyberpunk to Noopunk

Within the project, the first level forms the cyberpunk side:

```text
AI
data
capitalism
networks
power
discourse
cyberspace
```

Levels 2 and 3 extend this into Noopunk:

```text
Cyberpunk
    +
mind / consciousness / alternative ontology
    +
expanded non-human agency
    ↓
Noopunk
```

This is a project-internal conceptual and creative metaphor.

It must not be presented as if "cyberpunk = Lindgren" or "Noopunk = Wendt" were literal claims about those scholars' own work.

## Simulation as a Philosophical Laboratory

One important principle is that simulation can also be used to study philosophical assumptions without claiming that those assumptions are true.

For example:

```text
baseline model
    ↓
mainstream social simulation

+ speculative ontology
    ↓
alternative model

+ speculative actors
    ↓
alternative model
```

Comparing such models can help clarify what different ontological assumptions change.

This must still be kept distinct from empirical hypothesis testing.

The output of a speculative simulation is not empirical evidence for the metaphysical premises used by that simulation.

## Modularity Requirement

This paradigm should later also appear in the software architecture.

Mainstream components must be able to operate without speculative components.

Conceptually, for example:

```text
MAINSTREAM
    social graph
    cyber graph
    agents
    discourse
    networks
    simulation
        │
        ▼
SPECULATIVE EXTENSIONS
    quantum/noetic models
        │
        ▼
    NHI / expanded actor models
```

This document does not define concrete module names or directory names.

It only records the requirement that speculative ontologies must remain detachable extensions.

The mainstream academic core must not depend on them.

This also follows the broader modularity principle of the project:

- social graph;
- cyber graph;
- later RPG graph;
- speculative or noetic systems.

These may later form an assemblage, but they must remain separable modules.

## Epistemological Firewall

The project must maintain an explicit epistemological firewall between mainstream research and speculative layers.

The project may contain, side by side:

- empirical claims;
- theoretical interpretations;
- simulation assumptions;
- philosophical speculation;
- fictional worldbuilding.

Their epistemological status must not be collapsed into one another.

In particular:

```text
simulation output ≠ empirical observation

speculative premise ≠ research finding

worldbuilding ≠ scientific claim
```

This distinction should later remain visible in documentation, code, and simulation design.

## Summary

The current structure is:

1. Critical AI Studies as the mainstream academic core;
2. Quantum Mind as a speculative ontological extension;
3. NHI as a further speculative extension of actor ontology.

The mainstream core must stand on its own.

The speculative layers may be used for philosophical and simulation-oriented exploration, but they must remain detachable both conceptually and architecturally.
