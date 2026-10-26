# Playable slice — Etsivä Romppainen ja Lakkahaltian Salaisuus

First playable vertical slice for [#631](https://github.com/TomiToivio/NooPunk/issues/631).
The level is **built in code**; this file is checked by a headless run rather than an editor session.

## Requirements

- **Godot 4.3** (tested: `4.3.stable.official.77dcf97d8`, Linux x86_64). No addons.
- No network, no LLM, no external service. Fully offline.

## Run

```bash
godot --path .                       # the project's default scene (unchanged: scenes/main.tscn)
godot --path . scenes/case/lakkahaltia.tscn
```

Or open the project in the editor and press **F6** on `scenes/case/lakkahaltia.tscn`.

## Controls

| Key | Action |
| --- | --- |
| `W A S D` | move |
| `E` | talk to the nearest person |
| `1`…`3` | choose a dialogue topic |
| `0` / `Esc` | leave the conversation |
| `J` | evidence journal |
| `F5` / `F9` | save / load (`user://lakkahaltia_save.json`) |
| `P` / `C` | publish / contain — only once the evidence threshold is met |

## What the slice contains

- A small ward level: floor, walls, reception desk, corridor pillar, three conversational NPCs
  (ward physician, night nurse, patient in room 12).
- Branching topics; picking one records **evidence** and marks the topic visited.
- Two topics carry a **skill check** resolved on the approved Without Number kernel
  (`2d6 + attribute modifier + skill level` vs difficulty) with the dice and result shown.
- Evidence journal listing what the investigator can actually substantiate.
- Versioned JSON save/load that refuses a save from another case or version.
- **Two ambiguous endings** — publish or contain — neither of which explains the anomaly.

## Tests

```bash
godot --headless --path . --script res://tests/godot/run_tests.gd
```

31 checks: case state (evidence, flags, save/load, version and case guards), the rules adapter
(modifier bands, explicit-dice arithmetic, seeded replay), the case data (three NPCs, clues, two
endings, Without Number attribute names), and a scene smoke test that instantiates the level.

Exits non-zero on failure, so CI can gate on it.

## Rules

Resolution uses `src/godot/wn_rules.gd` — the adapter added in **#632** over
`data/rules/wn_core.json`. It implements the **approved** Without Number baseline
(`docs/design/RULING_2026-10-26_WN_BASELINE.md`): attributes 3–18, modifier bands −2..+2,
`2d6 + modifier + skill level` vs difficulty.

> **Known discrepancy, recorded rather than hidden:** `src/godot/core_rules.gd` still implements the
> superseded `STAT + Skill + 1d10` kernel over `data/rules/core.json`. Both exist; the slice uses the
> approved one. Migrating `core_rules.gd` (or retiring it) is follow-on work, not part of this slice.

## Assets

No third-party assets are committed. All geometry is Godot primitives (`BoxMesh`, `CapsuleMesh`)
and the UI is built from stock `Label`/`ColorRect`. An asset manifest is therefore trivially
public-repo-safe; when CC0 or purchased packs are added, record **source, licence, attribution and
redistribution rights per pack** here and keep purchased assets out of the public repository unless
their licence explicitly permits it.

## Known limitations

- Camera is fixed behind the player; no mouse look, no isometric toggle.
- Movement has no animation, no doors, no navigation mesh — collision and a flat floor only.
- `_process` polls keys directly, so the project's InputMap is unused and rebinding is not possible.
- Headless runs print `mesh_get_surface_count` errors from Godot's dummy renderer; they are
  renderer noise in `--headless`, not script errors.
- Combat, hacking, BCI, PSI and factions are **deliberately absent** — they are extension seams,
  not half-built features.
