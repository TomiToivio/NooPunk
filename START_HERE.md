# START HERE — NoöPunk vanilla CWN/SWN baseline (issue #848)

> **CURRENT DIRECTIVE (2026-10-30).** Issue [#848](https://github.com/TomiToivio/NooPunk/issues/848) supersedes the blank-rulebook and seven-attribute restart (#827, #835). Follow [AGENTS.md](AGENTS.md) and [the baseline decision record](docs/NOOPUNK_BASELINE_848.md). Do not resume the restart or create another Godot project.

## Canonical entry points

- **Pinned baseline SHA:** `36092a56a7637145c805129511eb2b6b688f6ca0` (audited main snapshot; not a rollback instruction).
- **Tabletop rules:** [`rulebook/00_INDEX.md`](rulebook/00_INDEX.md), with vanilla **Cities Without Number** as the primary mechanics and vanilla **Stars Without Number Revised** governing psionics. Use published STR/DEX/CON/INT/WIS/CHA, classes, character generation, checks, combat, hacking, equipment and progression. No NoöPunk-specific statistical modifications.
- **Godot:** repository-root [`project.godot`](project.godot), startup `res://scenes/main.tscn`. Target **2D top-down turn-based** play, not a parallel action RPG.
- **Source-of-truth implementation:** `godot/`, with `src/godot/` compatibility modules audited before consolidation. Existing lore, scenarios, alternate prototypes and history are retained for reference, not promoted into a second rules authority.
- **Superseded:** `noopunk/game/project.godot`, `noopunk/rulebook/RULEBOOK.md` and custom seven-attribute/typed-tag systems. They remain on disk as archive/reference only.
- **Scope exception:** independently authorized `strategy_game/` is not part of this Godot consolidation.

## Run and verify

From the repository root with the project-pinned Godot version (see `project.godot`):

```sh
godot --headless --path . --import
godot --headless --path . --script res://godot/tests/run_tests.gd
godot --path .
```

These are verification commands, **not** a claim that they passed in this documentation change. A passing test suite cannot establish complete CWN/SWN coverage. Record missing procedures and their authoritative published source in the coverage matrix.

## Work on one shared baseline

Before editing, inspect issue #848, `AGENTS.md`, `docs/NOOPUNK_BASELINE_848.md`, and overlapping PRs. Preserve saves and existing gameplay. Implement and test one vanilla, book-traceable subsystem at a time in the canonical root game and tabletop documentation. Every related PR must record its baseline SHA, canonical paths, rules authority, superseded work and actually run tests. **Keep #848 open** until the migration and playable vertical slice are verified.
