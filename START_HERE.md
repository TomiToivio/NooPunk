# START HERE — NoöPunk (issue #848)

**The vanilla CWN/SWN baseline and the one Godot RPG.** Issue #848 supersedes the blank-rulebook
restart (#827, #835): the tabletop rules are published Cities Without Number, the game is the
repository-root Godot project, and no second prototype is current.

## Canonical artifacts

| What | Where |
| --- | --- |
| Tabletop authority | CWN SRD <https://cwn.quadrifons.com/> (primary); SWN Revised SRD for psionics |
| Rules record in-repo | [`docs/rules/`](docs/rules/) — coverage and procedure notes; [`data/rules/`](data/rules/) — machine-readable |
| Godot project | [`project.godot`](project.godot) (repository root) |
| Startup scene | [`scenes/main.tscn`](scenes/main.tscn) → `godot/ui/main_menu.gd` |
| Rules kernel | [`godot/core/`](godot/core/) (canonical owner; `src/godot/` is legacy) |
| Godot tests CI runs | [`godot/tests/run_tests.gd`](godot/tests/run_tests.gd) |
| Decision record | [`docs/design/ISSUE_848_BASELINE.md`](docs/design/ISSUE_848_BASELINE.md) |

**Baseline commit:** `36092a5`. Rebase on `main`; name the canonical module you extend in the PR.

**Archived, do not extend:** `noopunk/` (blank rulebook and seven-attribute sheet), `restart/`
(history only), the #821 seven-attribute tags until Tomi reauthorizes them. Their files and history
stay; they are not the current design.

## Run the game

```sh
godot --path .            # from the repository root
```

The window opens at `scenes/main.tscn` (main menu). Existing play routes: the ward/campaign scenes
reachable from that menu. The top-down gameplay scene is the next implementation slice, not yet on
`main` — see the decision record.

Headless checks CI runs:

```sh
godot --headless --path . --import
godot --headless --path . --script res://godot/tests/run_tests.gd
```

Current result at the baseline: **760 checks, 0 failed.**

## Rules boundaries

CWN governs attributes, creation, classes, skills, checks, saves, combat, equipment, cyberware,
hacking and progression. SWN Revised governs psionics whole (Psychic class, disciplines, Effort).
Do not blend the two inside one procedure, and do not reintroduce custom mechanics as if they were
published rules.

## How work arrives

One small piece from Tomi at a time, implemented in `godot/core/` and the root project, with the
tabletop procedure it follows named in the PR. If it departs from published CWN/SWN, it is a tracked
deviation, not silent design. **#848 stays open** until alignment and migration are verified.
