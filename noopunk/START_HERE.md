# NoöPunk — START HERE

Two canonical artefacts, one development path. **Every rule or scenario issue targets these paths and
no others.** The legacy rulebook (`rulebook/`), the legacy Godot project (`godot/`, root
`project.godot`) and the Python kernels (`src/rules/`) are reference material and are never edited by a
NoöPunk issue.

| what | canonical path |
| --- | --- |
| tabletop rulebook | `noopunk/rulebook/RULEBOOK.md` |
| Godot top-down RPG | `noopunk/game/` (project root; main scene `character_creation.tscn`) |
| the shared numbers | `noopunk/game/data/attributes.json` — read by the game, quoted by the rulebook |

## Run the game

```bash
godot --path noopunk/game                     # opens character creation, then the room
godot --headless --path noopunk/game --script res://tests/character_test.gd
godot --headless --path noopunk/game --script res://tests/smoke.gd
```

Flow: character creation opens first and rolls seven 3d6 values as soon as it loads. **Roll again**
replaces the sheet. **Continue into the room** switches to the walking scene, which keeps showing the
rolled sheet. **WASD** or the **arrow keys** move the player; the camera follows.

## What exists, and what does not

Exists: seven attributes with the 3d6 conversion table, a minimal UNSA-rookie sheet, the difficulty
scale as reference data, a walking scene, and two headless tests.

Not defined: any resolution mechanic, skills, checks, combat, injury, inventory, experience,
encounters, equipment, specialisations, professions, classes, backgrounds, NPCs, LLM integration or
saves. None of it is added until Tomi supplies it.

## The tests

- `tests/character_test.gd` — the conversion table at every boundary total (3, 4, 5, 6, 7, 8, 9, 10, 11,
  12, 13, 14, 15, 16, 17, 18), totals outside 3–18 refused, exactly seven attributes in the author's
  order, every value inside −3…+3, rerolls producing a fresh sheet, the same seed reproducing the same
  sheet, difficulty labels from the same contract, the creation scene rolling on open and offering
  **Continue**, and the sheet surviving into the walking scene with the player still able to move.
- `tests/smoke.gd` — the walking scene loads, the player is scripted, moves at 120 px/s in every
  direction including diagonals, is still when idle, and has its camera and collision.

Both print `... OK` and exit 0, or name each failure and exit 1.

## How a child issue runs

1. **Tomi** supplies one small rule, interaction or scenario fragment.
2. It is written into `noopunk/rulebook/RULEBOOK.md`, in the section it belongs to.
3. The same change implements its playable counterpart in `noopunk/game/`.
4. Its behaviour is covered by `tests/character_test.gd` or `tests/smoke.gd` (or a new test in the same
   folder) and the tests are run and reported.
5. Review, merge, and close **only the child issue**. The parent meta-issue (#827) stays open.

A child issue must name what changes in **both** artefacts. If a change touches only one, it says why
(a rulebook-only clarification, or a presentation-only difference).

## Rules of the road

- The same decisions appear in both artefacts; platform-only differences are documented.
- No new standalone rulebook, no second Godot prototype, no parallel implementation of one rule.
- Small, isolated, reversible changes. Never a destructive reset of the existing repository.
