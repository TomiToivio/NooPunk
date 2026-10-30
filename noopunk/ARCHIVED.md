# ARCHIVED — do not extend

**Status: archived 2026-10-30 by the directive in #848.** This directory is the blank-rulebook restart
(#827, #835 and follow-ups) — a blank rulebook, a minimal top-down starter, a seven-attribute character
sheet and a set of small Godot tests. It was a legitimate experiment and it is kept for its history,
its tests and the parts worth porting.

It is **not** a game, **not** a second project and **not** canonical. The canonical game is the
repository-root Godot project (`project.godot`, startup scene `scenes/main.tscn`) implementing
**vanilla CWN** with **vanilla SWN Revised** where CWN defers, under
`rulebook/WITHOUT_NUMBER_BASELINE.md`.

## What #848 changed about the direction

| then (this directory) | now (canonical) |
|---|---|
| blank rulebook, rules authored one at a time | `rulebook/WITHOUT_NUMBER_BASELINE.md`: published CWN/SWN procedures |
| seven attributes: Fitness, Reflexes, Cognition, Cyber, Awareness, Agency, Empathy | STR, DEX, CON, INT, WIS, CHA, 3–18 |
| 3d6 converted to −3…+3 | 2d6 checks against published target numbers |
| a minimal starter room as the game | the root top-down RPG slice with CWN kernels |

## What is worth porting, and where it goes

1. **The tests that assert behaviour** — `game/tests/character.gd`, `attributes_smoke.gd`, `smoke.gd`
   are compact and headless; their shape is reusable for CWN character generation parity checks in
   `godot/tests/`.
2. **The creation-screen pattern** — a scene that shows a generated sheet before play. The canonical
   equivalent must generate a CWN character (attributes, background, Edges, Foci, skills), not seven
   custom attributes.
3. **Nothing else.** The seven-attribute model, its band table and the sheet layout are archived
   reference, not a design to continue.

## Rules for agents

- Do not add features here. Do not fix bugs here. Do not copy this directory into a third project.
- If something here is genuinely useful, port it into the canonical paths in the *same* reviewed change
  that tests it, and say what you took.
- Do not delete this directory without an audited migration that preserves these tests in git history.
