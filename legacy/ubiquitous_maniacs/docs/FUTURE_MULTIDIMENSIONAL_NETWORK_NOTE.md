# Future planning note: multidimensional network

Date: 2026-07-26  
Status: idea only — not approved for implementation

## Core idea

A later version of Noöpunk could treat its network as a **multiplex spatiotemporal network** rather than embedding every relationship in one ordinary Euclidean space. A connection would have a mode describing the geometry through which it operates.

Possible conceptual layers:

- **Spatial:** physical proximity, travel, institutions, violence and face-to-face interaction. Constrained by geography and ordinary time.
- **Cybernetic:** telecommunications, BCI connections, AI systems and cyberspace. These remain physically implemented and propagate at finite, relativistic speeds, but their socially effective distance is determined more by latency, bandwidth and network topology than kilometres.
- **Temporal:** memories, archives, predictions, simulations, precognition or other links between different temporal layers.
- **Noetic / non-local:** synchronicity, archetypal overlap, collective-unconscious structures, PSI or entanglement-like relations for which ordinary spacetime distance may be irrelevant or undefined.

The important distinction is:

> **Cybernetic is not physically non-local.** It can create effective social non-locality while still depending on causal signals moving through spacetime.

One possible abstract notation is:

```text
G = (V, E_spatial, E_cybernetic, E_temporal, E_noetic)
```

However, the preferred conceptual refinement may be **three spaces × time**—spacetime, cyberspace and noöspace each with temporal structure—rather than four unrelated network types. Exceptional temporal links could connect different time layers.

The same pair may be connected in several layers simultaneously. For example, Romppainen and Ingrid could be physically co-located, cybernetically connected through BCI, temporally connected through memories or simulations, and noetically connected through overlapping archetypal structures. The useful question would become:

> Through which geometry are these nodes connected?

Different layers need not share a distance metric. Noöspace may be purely topological; assigning it coordinates or “noömetres” may be a category error.

## Refined model: domain × relation geometry

The cleaner Noöpunk metaphysical model separates two independent dimensions instead of treating every concept as an equivalent layer.

### Domain

```text
D ∈ {Physical, Cyber, Noetic}
```

The domain states **where or in what ontological register** a relation exists.

### Relation geometry

```text
R ∈ {Spatial, Temporal, Nonlocal}
```

The geometry states **how the relation traverses its domain**. An edge can therefore be described abstractly as:

```text
e = (A, B, D, R)
```

Possible combinations include:

| Domain | Geometry | Example |
| --- | --- | --- |
| Physical | Spatial | walking, physical proximity, transport or violence |
| Cyber | Spatial | packets traversing physical infrastructure |
| Physical | Temporal | causal persistence or speculative physical time travel |
| Cyber | Temporal | archives, delayed messages, backups or simulations of past states |
| Noetic | Temporal | dreams, memories, precognition or archetypes persisting across periods |
| Noetic | Nonlocal | synchronicity, PSI or collective-unconscious relations |

This preserves the distinction between ontology and geometry. `Cyber` does not mean nonlocal, and `Noetic` does not automatically mean temporal.

## Time as explicit topology

A conventional network often assumes that connected nodes occupy the same implicit temporal slice:

```text
A(t) → B(t)
```

A later Noöpunk graph could instead allow explicit temporal connections:

```text
A(t1) → B(t2)
```

Time would then be part of graph topology rather than merely an edge timestamp. For example:

```text
Romppainen[2045]
       │
       │ temporal: memory
       ▼
Romppainen[2026]
       │
       │ noetic: archetypal association
       ▼
Jung[1916]
```

Temporal relations would not all assert literal backwards causation. Distinct relation types could include:

- ordinary causal influence;
- memory;
- archive or historical record;
- historical influence;
- delayed communication;
- simulation of a past or future state;
- prediction;
- alleged precognition;
- synchronicity.

Illustrative distinctions:

```text
ordinary causality: A(t1) ──time──▶ B(t2)
memory:             A(t2) ──time──▶ A(t1)
prediction:         A(t1) ──time──▶ B(t2)
precognition?:      A(t1) ──?─────▶ B(t2)
synchronicity?:     A(t1) ──noetic── B(t1)
cyber connection:   A(x1,t) ──cyber──▶ B(x2,t+20ms)
```

The question mark is intentional. The graph may record an observed or narrated relation without settling its metaphysical explanation.

## Epistemic status

Relations could eventually carry a separate epistemic classification, such as:

```text
observed → inferred → hypothesized → anomalous → fictional/speculative
```

This would let rigorous empirical relations and Noösphere claims use a compatible structural vocabulary without treating them as equally established. Epistemic status would describe the evidence for an edge, not its domain or geometry.

The resulting conceptual skeleton has three independent questions:

1. **Domain:** Physical, Cyber or Noetic?
2. **Geometry:** Spatial, Temporal or Nonlocal?
3. **Epistemic status:** observed, inferred, hypothesized, anomalous or speculative?

This refinement is preferred for later discussion, but it remains an unresolved planning idea rather than a schema decision.

## Possible later technical fit

If this idea is ever approved for implementation, a NetworkX `MultiDiGraph` could represent multiple simultaneous relations. Possible future metadata might include `domain`, `geometry`, `relation_type`, `time`, `latency`, `distance`, `epistemic_status`, `confidence` and `causal`.

This is only a conceptual note. These types, attributes and graph structures do not exist in the active project.

## Current boundary

**Step 1 remains unchanged:** one simple undirected `networkx.Graph` containing only 8 patients and 8 staff members, with node roles `patient | staff` and one numeric `relationship` value per edge.

Do not add multiplex layers, temporal edges, cybernetic edges, noetic edges, `MultiDiGraph`, coordinates or related scaffolding to Step 1.
