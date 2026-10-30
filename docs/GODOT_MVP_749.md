# Romppainen MVP — playable vertical slice (#749)

Home → UNSA HQ → the Kallas warehouse → debrief. One controllable detective, one optional fight,
one network to break into, save/load.

**This is an increment, not the finished MVP.** §5 states exactly what is missing.

## Running it

```bash
godot --headless --path . --import                      # once per checkout: builds the class cache
godot --path . res://godot/ui/mvp_game.tscn              # play
godot --headless --path . --script res://godot/tests/run_tests.gd   # 239 checks
```

The title screen also carries a **“Romppainen — MVP”** button; it is added beside the existing
case entry rather than replacing it.

## Controls

| Key | Action |
| --- | --- |
| WASD / arrows | Move on the grid |
| E | Interact — leave a room, take a briefing, use the terminal, close the network view |
| H | Toggle the network view (mission only) |
| C | Start the optional encounter / attack / end the turn |
| F5 / F9 | Save / load `user://mvp_romppainen.json` |

## What the slice does

**Home.** Romppainen's flat. Interacting with the desk reports the kit; walking to the bottom-right
tile and pressing E goes to HQ.

**UNSA HQ.** One interaction takes the briefing and opens the mission — the mission is locked until
it does.

**The Kallas warehouse.** A guard and a terminal. Three ways through:

- **Investigative:** reach the `manifest` node through the network (`shipping` → `manifest`,
  `query` verb) and leave. No fight.
- **Tactical:** the optional encounter against one guard.
- **Mixed:** either order.

Leaving resolves the mission and records which approach was used. A resolved mission can be
debriefed; an unresolved one cannot be left.

## The rules boundary

No rule lives in the scene. `godot/core/session.gd` composes four kernels:

| Kernel | Responsibility |
| --- | --- |
| `rules_adapter.gd` | Difficulty values, 2d6 skill checks, d20 attacks, and the single seeded RNG every other kernel draws from |
| `combat.gd` | 1d8+DEX initiative, Move + Main action, Chebyshev movement, cover as an AC bonus, damage and down state, encounter end |
| `hacking.gd` | Connectivity → access → program → CPU → trace → alarm |
| `scene_flow.gd` | Home/HQ/Mission/Debrief transitions, objectives, resolution, serialisation |

`mvp_game.gd` draws rectangles and forwards keys. If a rule ever needs changing, it changes in one
of those four files, not in the scene.

## Coverage this increment adds

Against `docs/GODOT_MVP_AUDIT.md`:

| Area | Before | Now |
| --- | --- | --- |
| Initiative / turn order | absent | **ported** (`combat.gd`) |
| Grid movement / action economy | absent | **ported** (Move + Main) |
| Cover | absent | **ported** (AC bonus) |
| HP and down state | absent | **ported** (single damage pool, no Trauma/Shock) |
| Hacking procedure | absent | **ported** (procedure; costs are calibration) |
| Scene chain Home→HQ→Mission→Debrief | absent | **ported** |
| Save/load of slice state | partial (case only) | **ported** (`session.gd`, version 1) |
| Romppainen's CWN record | absent | **drafted**, player choices marked |
| Gear / inventory / reload | absent | **still absent** |
| Trauma/Shock, mortal injury, cyberware, vehicles, advancement | absent | **still absent** in Godot |
| SWN psionics in play | partial | unchanged — Romppainen is not a psychic |

## Calibration vs source

The **procedures** follow the CWN sequence. The **numbers** are slice calibration and are marked as
such in `godot/scenarios/mvp_romppainen/mission.json`:

- CPU costs, trace increments, alarm threshold, node security targets, guard HP and cover.

They are not presented as source rules. Before this is called a CWN-faithful implementation, each
number needs a citation from the SRD (CC0, `data/sources/game_system_rights.json`) — see #747's
change matrix for the method.

## Rights

- Rules: Cities Without Number SRD (CC0) — procedures are implemented, no rulebook prose is copied.
- SWN: `blocked-unverified`; nothing is reproduced, and Romppainen is not given SWN powers.
- Art: none imported. Every tile, marker and line is drawn procedurally in `mvp_game.gd`, so the
  slice's look is original by construction and carries no asset licence.

## Known gaps (next increments)

1. **Windowed playtest on Ubuntu** — readability and controls have not been checked in a real
   window. Headless checks prove the logic, not that the palette is legible.
2. **Dialogue** — the NPC interactions are one-line announcements; branching conversation and the
   journal are still the existing Lakkahaltia systems, not wired into this slice.
3. **Inventory and gear** — no equipment screen, no reload, no encumbrance. The character record
   lists gear but nothing consumes it.
4. **Combat depth** — no ranged range bands, no automatic fire, no suppressive fire, no morale,
   no Trauma/Shock. Deliberately deferred rather than half-implemented.
5. **Party support** — `combat.gd` is side-aware and would take allies, but no selection UI exists.
6. **Hacking UI** — the graph is drawn but actions are keyboard-driven; node cost/security readouts
   are minimal.
7. **Mission content** — one small mission. The world canon of Lakkahaltia is not yet used here.
