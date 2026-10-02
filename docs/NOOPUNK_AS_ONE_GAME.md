# NoöPunk is one computer RPG / social simulation

> **Status: author-specified architecture (#48), which revises the multi-product
> framing discussed in #40.** This document is the canonical statement of the
> target shape. Where older documents imply separate tabletop, simulation and
> videogame products, this document wins.

## The rule

**There is only one NoöPunk RPG/simulation.**

Do not maintain separate products called "the tabletop RPG", "the Concordia
simulation" and "the Godot game". There is one game with one ruleset, one world
model and one evolving game state.

> **NoöPunk is one Python RPG/social simulation whose mechanics are written with
> the clarity of a tabletop RPG, whose agents can be driven by Concordia/LLMs, and
> whose first user interface is text.**

```text
Human player
     │
     ▼
Text interface
     │
     ▼
NoöPunk rules  ──────────────┐
     │                       │
     ▼                       ▼
Concordia GM          Concordia agents
     │                       │
     └──────────┬────────────┘
                ▼
           World state
                │
          events / memory
                │
         social simulation
                │
           changed world
                │
                ▼
            next scene
```

## Tabletop-style rules are not a second product

The rules may **read** like tabletop RPG rules, and they are documented in a
human-readable rulebook, because that makes them:

- human-readable
- mechanically explicit
- easy to test
- suitable for a rulebook
- usable by human players
- usable by Concordia agents
- usable by deterministic simulation code
- portable to future interfaces

But there is **no separate tabletop implementation to maintain**. `RULEBOOK.md` is
the documentation of this game's mechanics — not evidence of a second product. A
human must be able to understand the mechanics without reading Python.

## One rule model, two notations

The human-readable rule and the simulation rule are the **same conceptual
mechanic**:

```text
attribute + skill + equipment + context
        vs
difficulty + opposition + environment
```

with a stochastic resolver. The human-facing representation may use 3d6; simulation
code may sample the equivalent distribution directly.

The goal is not:

```text
tabletop rules + different simulation rules
```

but:

```text
        ONE RULE MODEL
              │
   ┌──────────┴──────────┐
   ▼                     ▼
human-readable      Python
RPG notation      implementation
```

**LLMs choose, interpret, converse and narrate. Rules resolve.** Where a canonical
rule exists, deterministic Python calculates the outcome. Prompt text never
overrides or invents a numeric outcome.

## What this revises, and what survives, from #40

#40 correctly identified that NoöPunk combines RPG play, generative social
simulation, LaclauGPT-style analysis and PCM-style experimentation. That analysis
survives. What #48 revises is #40's **multi-product framing**.

| Carried forward from #40 | Revised by #48 |
|---|---|
| one shared world state + event log as the spine | the "three views" framing: there is **one game**, not three views over it |
| simulation data rigorously separated from empirical data | — (unchanged, still binding) |
| deterministic resolution with the LLM outside the rules path | — (unchanged) |
| the DEFER register's author-owned decisions | the assumption that tabletop, Concordia and Godot are separate deliverables |
| event envelope, replay, branching | — (unchanged; already implemented) |

The implemented Phase B core (`src/simulation/`) is unaffected: it is one world
state with one event log, which is exactly the shape #48 wants.

## Runtime sequence

Text first. A graphical engine is explicitly **deferred** — Godot, Arcade, Ursina,
Pygame and similar: do not choose one until the text game loop works.

```text
Phase 1  Concordia + text
Phase 2  richer terminal / TUI
Phase 3  web UI
Phase 4  optional graphical client
```

A future graphical or web client wraps the existing simulation rather than forcing
a rewrite. The underlying NoöPunk game remains the same application throughout.

**Godot's status changes under #48.** It remains a *possible future frontend*, and
the existing `src/godot/` scaffold is preserved rather than deleted
(`AGENTS.md` §10: prefer reversible architecture), but it is no longer a planned
parallel runtime that rules must be ported to.

## Documentation obligations

- `RULEBOOK.md` — core mechanics: attributes, skills, checks, combat, social
  mechanics, hacking, cybernetics, psionics, examples.
- `WORLDBOOK.md` — setting: timeline, factions, technologies, Noösphere, AI/AGI,
  cybercapitalism, PCM, NHI/UAP material, institutions, locations, scenario seeds,
  theory references.
- Both are documentation for the **same computer RPG/simulation**.

`WORLDBOOK.md` does not exist yet. Creating it is author-owned setting work, not an
agent deliverable: `AGENTS.md` §1 forbids inventing setting material, so this
repository records the requirement without fabricating the content.

## What this does not authorise

- It does not license inventing the rulebook's unfinished mechanics. Which
  mechanics exist remains author-specified; see `RULEBOOK.md` and `AGENTS.md` §4.
- It does not authorise fabricating worldbook content.
- It does not make Concordia required to run the game: the deterministic core must
  remain usable without an LLM being reachable.

## See also

- [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) — the three balances
- [`SIMULATION_ARCHITECTURE_SPEC.md`](SIMULATION_ARCHITECTURE_SPEC.md) — state model and event spine
- [`SIMULATION_CORE.md`](SIMULATION_CORE.md) — the implemented deterministic core
- [`../AGENTS.md`](../AGENTS.md) — binding agent rules
