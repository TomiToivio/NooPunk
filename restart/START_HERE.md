# NoöPunk restart — START HERE

Two canonical artefacts, one development path. **Every restart issue targets these paths and no
others.** Nothing here replaces or edits the legacy rulebook, the legacy Godot project or the Python
kernels; those stay readable reference.

| what | canonical path |
| --- | --- |
| tabletop rulebook | `restart/rulebook/RULEBOOK.md` (index: `restart/rulebook/README.md`) |
| Godot top-down RPG | `restart/game/` (Godot project, main scene `main.tscn`) |

## Run the game

```bash
# from the repository root, with a Godot 4.7.x binary
godot --path restart/game            # opens the test room
godot --headless --path restart/game --script res://tests/smoke.gd   # smoke test
```

Controls: **WASD** or the **arrow keys** move the player. The camera follows. Four walls bound the
room.

The headless smoke test checks what the milestone promises: the main scene loads into the room, the
player carries its script, movement is a pure function of the input vector (straight line = 220 px/s,
diagonal the same speed rather than √2 faster, idle is still), the camera exists on the player, and the
four bounds are present. It prints `SMOKE OK` and exits 0, or names each failure and exits 1.

## The first milestone: what exists and what does not

Exists: one room, one visible player placeholder, keyboard movement, bounds, a following camera, one
hint label, and the smoke test.

Deliberately absent: attributes, skills, dice, combat, injury, inventory, dialogue, quests, NPCs or
NPC AI, LLM integration, world simulation, saves. **None of it is added until Tomi asks for it**, one
piece at a time.

## How a child issue runs

1. **Tomi** supplies one small rule, interaction or scenario fragment.
2. The rule goes into `restart/rulebook/RULEBOOK.md`, in the section it belongs to.
3. The same change implements its observable counterpart in `restart/game/`, playable immediately.
4. Consistency is checked — the rulebook says what the game does, and the smoke test grows with the
   mechanic.
5. Review and merge. **Only the child issue is closed.**

A child issue must name its changes to **both** artefacts. If a change touches only one, it says why
(for example: a rulebook-only clarification, or a presentation-only difference such as a camera tweak).

## Rules of the restart

- The same decisions appear in both artefacts; platform-only differences are documented.
- Vertical slices in playable order: move around first, then whatever Tomi picks next.
- No new standalone rulebook, no second Godot prototype, no parallel implementation of the same rule.
- Keep changes small, isolated and reversible. No destructive resets of the existing repository.
- This milestone's meta-issue (#827) stays **open**; only child issues close.
