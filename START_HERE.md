# START HERE — NoöPunk: vanilla CWN/SWN + one top-down Godot RPG

**Directive:** issue **#848** (2026-10-30). This supersedes the blank-rulebook restart (#827, #835) and
every custom-attribute variant. **Pinned baseline: `36092a5`** — the commit at which the canonical game
passes 760 headless checks.

## The canonical artifacts

| Artifact | Path |
| --- | --- |
| Rulebook | [`RULEBOOK.md`](RULEBOOK.md) |
| Generated chapters | `rulebook/` — regenerate, never hand-edit |
| Godot project | [`project.godot`](project.godot) |
| Startup scene | [`scenes/main.tscn`](scenes/main.tscn) |
| Rules kernels | `godot/core/*.gd` |
| Rules data | `data/rules/*.json` |
| Coverage matrix | [`docs/rules/CWN_GODOT_COVERAGE.md`](docs/rules/CWN_GODOT_COVERAGE.md) |

## The rules

**Cities Without Number** is the primary system; **Stars Without Number Revised** supplies psionics,
space and factions where CWN is silent. No custom attributes, no alternate difficulty system, no
invented mechanics.

- attributes: STR, DEX, CON, INT, WIS, CHA (3–18, modifiers −2..+2)
- skills: 0–4, checks on 2d6 + attribute + skill
- attacks and saves: d20
- character creation, classes, combat, hacking, cyberware, equipment, progression: as published
- psionics: SWN Revised class/discipline rules

Name the governing book for whatever subsystem you touch. Where the two games differ, the more
specific book wins for that subsystem and the choice is recorded.

## Run and verify

```sh
godot --path .                                             # play
godot --headless --path . --script res://godot/tests/run_tests.gd   # engine tests
python3.11 -m pytest tests/ -q                              # Python rules layer
```

Baseline result: **760 Godot checks, 0 failed**; Python suite green.

## Superseded, preserved, not authoritative

`noopunk/` — the blank-rulebook restart built under #827/#835 — stays in the repository as history.
Do not extend it, do not build a fourth prototype, and do not delete it.

## Working rules

1. Check `origin/main` and open PRs before writing.
2. Name the canonical module you are extending in the PR.
3. Tests prove behaviour: a subsystem is "done" only with a test that fails without it.
4. Never claim full rule coverage without the coverage matrix and evidence.
5. Mechanics may be implemented; published prose and non-redistributable tables may not be copied.
