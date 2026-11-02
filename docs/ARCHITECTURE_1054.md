# Architecture decision: immutable tabletop core, engine-independent Python rules (#1054)

**Status: binding.** This records the decision in #1054 and the executable first slice from #1053. It does not
authorize rewriting any published rule.

## The five constraints

1. **Published rules are immutable.** CWN is the permanent primary ruleset and is never modified, reinterpreted,
   rebalanced or replaced. SWN, WWN and AWN are supplementary rulesets implemented faithfully and mounted as
   optional modules, with precedence and compatibility boundaries written down where books overlap.
2. **NoöPunk is additive.** Setting data, variant configuration and optional mods live apart from the canonical
   core. A mod may be *simpler* than CWN; it may never silently override a CWN procedure.
3. **Tabletop is the reference implementation.** Every core rule and mod must be playable with a rulebook,
   pencils and paper. Software that cannot be replaced by a table is software that has quietly become the game.
4. **No engine owns a rule.** Gameplay logic lives in plain Python packages. CLI, Evennia, Concordia and Pygame
   are adapters over the same API, never the place where a rule is implemented.
5. **A playable game beats speculative platform work.** The single-player UNSA campaign comes first; strategy and
   multiplayer are postponed until it is playable without either.

## What exists today (measured, not planned)

| Piece | Where | State |
|---|---|---|
| Rules kernel (attributes, checks, combat, strain, saves) | `mud/nopunk_mud/cwn_core.py` | implemented, tested |
| Campaign engine (commands, state, endings, save/load) | `mud/nopunk_mud/campaign/engine.py` | implemented, tested |
| **Console slice** — plain text, no engine | `mud/nopunk_mud/console.py` | **new in this change** |
| Social layer (rank, scoped reputation) | `mud/nopunk_mud/social.py` | implemented, tested |
| Ideology layer (DA/DNA/SNA) | `mud/nopunk_mud/ideology.py` | implemented, tested |
| Evennia adapter | `mud/commands/`, `mud/typeclasses/` | exists, **not the owner of any rule** |

## The console slice, and why it is the architectural test

`python -m nopunk_mud.console` plays the first UNSA investigation end to end with **no Evennia, no Concordia, no
Pygame, no LLM and no network**. A test blocks `evennia` at import time and runs the rules anyway; another plays
the published winning chain to a `solved` ending and asserts both clues are held. If an engine ever becomes
load-bearing for a rule, that first test fails — which is the cheapest possible alarm.

```
go street → go kurvi → ask witness badge → examine badge
          → go street → go university → examine terminal
          → go street → go safehouse → report        ⇒ solved
```

## Adapter contract

An adapter may: read player input, render text/graphics, persist state through the documented save format, and
schedule time. An adapter may **not**: compute a check, decide damage, resolve a clue, or hold a rule that the
plain-Python package does not also expose.

Cross-adapter parity is tested by replaying the same seeded script through two adapters and comparing the
resulting state documents — not by comparing prose.

## Mod contract

Each mod declares, in one place: what it adds; where it hooks into CWN; its **tabletop procedure**; its input and
output state; its dependencies; and how to switch it off. A mod that cannot be played with dice and paper is not
a mod yet.

## Coverage matrix and licensing

The rules-coverage matrix lives in `docs/rules/` and records, per subsystem: rulebook section (with printed page),
implementation, tests, and licence basis. A row without a page reference is a guess, and a guess does not go in
the matrix.

**Rule for every future change:** a rule and its tests change together, in the same pull request, and the matrix
row moves with them. A rule change that does not update its row is a silent divergence from the tabletop game.

## Migration of existing engine-specific code

Evennia commands and typeclasses stay, as adapters. Nothing is deleted to satisfy the diagram. Where a rule is
found inside an adapter, it moves to the plain package and the adapter keeps the presentation. The Godot
project is secondary/legacy per #950 and is not a target for new rules work.
