# Architecture decision #1054 — moved

The canonical decision record is
[`docs/architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md`](architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md).
It carries the layer map with measured sizes, the enforced engine boundary, the component inventory,
the mods contract and the adapter API. This file is kept as a pointer so older links keep working.

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

The survey behind the numbers, and the tabletop procedure with golden examples, sit beside it:
`architecture/ISSUE_1053_ARCHITECTURE_SURVEY.md` and `tabletop/FIRST_CASE_TABLETOP.md`.
