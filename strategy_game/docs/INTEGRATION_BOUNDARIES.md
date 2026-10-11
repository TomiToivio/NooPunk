# Strategy-game integration boundaries (proposal, not game rules)

Status: **architecture note for #282**. This document does not define canon, attributes, turns, actions, factions, simulation equations, or outcomes. The separate strategy game must not import existing NoöPunk RPG rules or modify its rulebooks.

## State and authority

- The strategy game's `WorldState` is the serializable record of **declared** data, not a simulation engine. UI and map adapters should consume read-only representations; they must not silently mutate world state.
- Keep observed/source-supported discourse distinct from fictional authored events, generated text, and hypothetical simulation results. Preserve source references and transformation metadata; absence of provenance must remain visibly unknown, not be silently upgraded into evidence.
- The LaclauGPT Phase 1 analytical taxonomy describes discourse. Do not convert its labels to causal transition formulas by default. A future simulation rule must separately state its assumptions and receive author approval.
- Optional LLM agents may offer proposals or prose, never automatically authoritative updates to the canonical state. Replaying saved state and drawing maps must work without model credentials, services, or network.

## Interface ownership

| Boundary | Input | Allowed output before rule approval | Must not do |
| --- | --- | --- | --- |
| Leader view | World-state snapshot | identity, attributes as uninterpreted data, trait tags | resolve abilities or make decisions |
| Discourse/network view | evidence-labelled records and declared graph data | observations and map/network overlays | derive political outcomes from labels |
| Faction view | faction/asset/location records | faction cards and locations | assign actions, resources or victories |
| Map provider | abstract location and network view model | portable visualization representation | infer borders, travel, control or ownership |
| Agent adapter | explicit context and capabilities | optional draft proposal | apply direct state mutations |

## Scenario import (future contract only)

Propose a **separate import/validation stage**, not a direct runtime dependency on the NoöPunk RPG. It should record input source, version, import mapping, author approval and whether every imported element is real history, fictional canon or illustrative sample. Imported actor or place references do not imply game mechanics. A failed or unapproved import leaves the existing snapshot unchanged.

## Replay and verification

Executable tests may check round-trip JSON serialization, stable output ordering, empty-state rendering, no required optional dependencies and nonmutation by presentation adapters. Later reproducibility checks should account for explicit inputs and versions. **Do not test lore/rulebook text, freeze canon in tests, or interpret LLM determinism as guaranteed.**

## Collaboration checkpoint

Before implementing actual rules, open three separate author-review discussions: (A) leader roleplay semantics, (B) political-simulation causal assumptions and validation, (C) faction-management choices and resolution. Integrate these only after their interfaces and approval gates are settled. Related #152 is background RPG simulation, not the strategy game's replacement.

This note complements `docs/RULE_SYSTEM_RESEARCH.md` and should be reconciled with improvements from other agents rather than used to replace their work.
