# NoöPunk Simulator — the social-science track

> **Independent of the RPG and of the story runtime.** It can be run, tested and versioned without a CWN
> character sheet, a scene, or an engine.

## What it is

A social-science simulator grounded in LaclauGPT's methodology: social actors, institutions and factions,
communications and discourse, relations, and dynamic social processes — with provenance, and with human-reviewable
mappings wherever a LaclauGPT analysis informs the simulation.

**Methodological reference:** [LaclauGPT Phase 1 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md).
The paper supplies the theory and method; it does **not** supply a complete simulation engine, and this subproject
must not claim that it does. The locked paper and `THEORY.md` are read-only.

**Scope gate:** the repository's active directive (root `AGENTS.md`, 2026-11-07) freezes RPG work and points
agents at the simulator. This subproject is where that work belongs.

## What is here now, and where it goes

| Concern | Lives today | Destination |
| --- | --- | --- |
| Simulator package | `src/social_sim/` | `NooPunk-Simulator/` at migration |
| LaclauGPT-informed adapters | `src/social_sim/` modules | same, once the contract is stable |
| Shared tag/graph contract | `data/schema/subproject_contracts_1295.json` | unchanged |

No files have been moved yet: the migration is staged, and the simulator is under active development. Moving it
mid-flight would cost more than the tidier tree is worth.

## Interfaces

- **In:** source material and analysis output from LaclauGPT, with provenance labels.
- **Out:** social-world state expressed in the shared **tag/graph** contract — the same contract the Story Graph
  and the RPG use.
- **Never:** CWN character sheets, scene runtimes, or the manuscript.

The contract is deliberately small: node kinds, edge kinds, stable ids, schema version. A simulator that needs a
richer vocabulary extends the contract version, not its own private format.
