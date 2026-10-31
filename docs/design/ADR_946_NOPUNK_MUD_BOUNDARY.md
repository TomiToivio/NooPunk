# ADR: NoöPunk MUD as a second game (#946)

**Status:** accepted for milestone 1. **Scope:** the boundary, the directory decision, the contracts. No Evennia
runtime is introduced by this ADR.

## Context

NoöPunk has one game today: the Godot RPG at the repository root. #946 asks for a second one — a persistent,
text-only, multiplayer sandbox — sharing the universe and the CWN rules but **nothing of the runtime**.

The failure mode this ADR exists to prevent is the one the repository has already paid for twice: two
implementations of the same thing drifting apart, and agents editing whichever copy they found first. The
answer is not "be careful". It is a boundary a test can check.

## Decisions

### D1 — The MUD lives in `mud/`, in this repository

A separate repository would give cleaner isolation, but it would also split the canon: `data/rules/`,
`data/world/` and the scenario files are shared inputs, and a second repo would immediately need a sync
mechanism for them. The repository already ships a Godot game that does not depend on the MUD, and a Python
package that does not depend on Godot; one more directory with its own `pyproject.toml` is enough separation.

**If** the MUD ever grows a deployment cadence that hurts Godot releases, the split becomes worth revisiting.
That decision is not taken here.

### D2 — Nothing is imported across the boundary

| Direction | Rule |
|---|---|
| `mud/` → Godot | never: no `.gd`, no `res://`, no `project.godot` |
| Godot → `mud/` | never: the Godot tree does not import Python MUD modules |
| `mud/` → repo canon | **read-only**, by path (`data/rules/`, `data/world/`), never edited from MUD code |
| `mud/` → CWN engine | through `rules_contract.py` only — a protocol the host implements |

Enforced by `mud/tests/test_boundary.py`, which also fails if the MUD tree contains a Godot reference or the
Godot tree imports `nopunk_mud`.

### D3 — CWN authority is a contract, not a copy

The MUD does not re-implement CWN. `rules_contract.RulesEngine` is a Protocol: the host supplies a resolver,
and `rules_contract` supplies the *shared facts* (difficulty bands, untrained modifier, attribute range) read
from the repository's canonical `data/rules/without_number.json`. A conformance test fails if the MUD's idea
of the rules drifts from the canon file — which is how the Godot tree and the tabletop stay honest too.

### D4 — LLM agents propose; they never decide

`llm_gateway` returns **proposals** with a declared action type. `world_state.apply()` accepts only known
event types with validated payloads. A narrator that invents a rifle, a successful roll, or a player action
produces a rejected proposal, not state. With the LLM disabled, a deterministic fallback runs — the
simulation is not allowed to require a provider to be playable.

### D5 — Mesa summarises; it never writes

The simulation emits `SimEvent`s (population, scarcity, faction pressure). `sim_bridge` reconciles them into
the authoritative state through clamped deltas and records both the proposal and the applied change. A
simulation that could set a player's health directly would make the world state advisory.

### D6 — Separate everything operational

Own dependency environment (`mud/pyproject.toml`), own test command, own CI job path, own documentation, own
issue scope. `mud/` must not be needed to run Godot, and Godot must not be needed to run the MUD.

## Consequences

- The first MUD milestone is playable without Evennia installed: the core (`world_state`, `rules_contract`,
  `llm_gateway`, `sim_bridge`) is plain Python and is what Evennia will host.
- Persistence is JSON on disk with an event log, so a restart test is a file round-trip rather than a claim.
- Adding a faction, an event type or a sim signal requires touching the schema and its test — deliberately,
  because that is where an unvalidated path would otherwise appear.

## What this ADR does not decide

Evennia's own object model and command syntax, the browser client, the LLM provider, and the size of the
Helsinki map. Those are milestones 2–5 of #946 and belong in their own records.
