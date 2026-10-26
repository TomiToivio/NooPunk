# The Godot slice — running the Lakkahaltia case

Native **Godot 4** project, GDScript, no RPG-in-a-Box step and no external service. This is the
first playable vertical slice of #631: a detective case in the NoöPunk ward, playable offline. The target ten-minute pacing needs a desktop playtest.

## Tested engine and platforms

| | |
| --- | --- |
| verified engine | **Godot 4.5.1.stable** (`4.5.1.stable.official.f62fdbde1`), Linux x86_64, headless |
| project renderer | `gl_compatibility` (set in `project.godot`) |
| expected elsewhere | use 4.5.1 with the Compatibility renderer; desktop visual verification remains outstanding |

## Run it

```sh
# from the repository root
godot --path .                     # opens the title screen
godot --path . --editor            # opens the project in the editor
```

Press **Begin the case**. The case saves to `user://lakkahaltia_save.json` (on Linux,
`~/.local/share/godot/app_userdata/NoöPunk/`).

### Controls

| key | action |
| --- | --- |
| `W A S D` / arrows | move Romppainen |
| `E` | talk to the nearest NPC, or examine the nearest object |
| `1`–`9` | pick a dialogue choice (buttons also work) |
| `J` | evidence board: clues, notes, complications |
| `R` | close the case once the record is found |
| `F5` / `F9` | save / load |
| `Esc` | close a dialogue or the evidence board |

## What the slice contains

* Four connected ward zones — entrance, corridor, reception, patient room — built from
  primitives, with a follow camera and collision.
* Three conversational NPCs: Dr. Aino Kivi, Nurse Väinö Salmi, Patient 16. Branching dialogue
  with conditions on flags and clues; choices set flags, record clues and add journal notes.
* Two mechanically meaningful checks, resolved as **2d6 + attribute modifier + skill vs difficulty** with the roll
  shown: the medical record (`INT / Program`, difficulty 8) and the mirror (`WIS / Notice`,
  difficulty 8, only after speaking to the patient). Failure still moves the case forward with a
  complication. The ward uses a fixed roll seed (`20261026`) so a run is reproducible.
* Four clues and an evidence board (`J`).
* An optional Lakkahaltia encounter behind the mirror check.
* Two ambiguous endings — close the case on the record, or refer the anomaly upward — with no
  "supernatural confirmed" label; the second is only offered if the encounter happened, and the
  mundane ending remains available either way.
* Save/load of clues, flags, journal, complications and the ending, in a versioned JSON file.
  The title screen offers **Resume** when a save exists.

## Rules basis (important)

The current author override in `AGENTS.md` and `rulebook/WITHOUT_NUMBER_BASELINE.md`
supersedes the historical #566 ruling: standard STR/DEX/CON/INT/WIS/CHA, scores
3–18, skills 0–4 (untrained −1), 2d6 checks. The active ward now calls
`wn_rules.gd` over `wn_core.json`. The old d10 adapter remains only for legacy consumers.
The demo uses the baseline's illustrative attributes and only investigation skills;
it is not a complete generated operator. The character is visible in the journal.

Save version 2 persists the character, position, completed check results and case
state. Old d10 version-1 saves are rejected instead of reinterpreting their numbers.
Each object check is rolled once per case; subsequent inspections and reloads reuse
its result. A failed check continues through its authored complication route.

## Layout

```
project.godot                     existing project, tested with 4.5.1
scenes/main.tscn                  title screen (script: src/godot/title.gd)
scenes/lakkahaltia/ward.tscn      the case scene (script: scenes/lakkahaltia/ward.gd)
src/godot/wn_rules.gd             rules adapter over data/rules/wn_core.json
src/godot/case_state.gd           authoritative state: clues, flags, journal, endings, save
src/godot/title.gd                title screen
data/scenarios/lakkahaltia/       case.json + dialogue.json — portable, no code
tests/godot/                      headless gameplay tests
tools/run_godot_tests.gd          test runner
tools/godot_smoke.sh              import + tests + scene smoke
```

The data files are deliberately plain JSON: a tabletop GM can run the same case, and a later
tactical or strategy layer can read the same clues and locations.

## Tests and verification

```sh
GODOT=/path/to/godot tools/godot_smoke.sh
```

That runs three things:

1. a headless import (rebuilds the class cache),
2. `tools/run_godot_tests.gd` — **20 tests, 264 checks** covering the rules adapter, the case
   state, dialogue navigation integrity and an end-to-end playthrough of both endings,
3. the ward scene loaded headless, asserting the `WARD_READY` marker and no script errors.

CI runs the same script in `.github/workflows/godot.yml`.

**What is not verified:** the headless runners have no renderer, so there is **no automated
visual check** of the scene — layout, lighting and readability were not machine-reviewed. The
`mesh_get_surface_count` warnings printed under `--headless` are dummy-renderer noise for
primitive meshes, not failures. Do a manual windowed run before calling the build presentable.

## Assets

No third-party asset is committed. Everything visible is built from Godot primitives in
`ward.gd`. `data/assets/manifest.json` records that decision and the packs considered
(Kenney, Quaternius, Poly Haven, and Synty as optional commercial) with their licence terms, so
a later art pass starts from a reviewed list rather than an assumption. Do not commit purchased
packs to this public repository unless their licence explicitly permits redistribution.
The full research is in [`docs/godot/ASSETS.md`](godot/ASSETS.md): every free pack with the licence read off
its own page (Quaternius Cyberpunk Game Kit and Cube World Kit, Kenney Furniture/City/UI/audio, KayKit,
Poly Haven, ambientCG), the paid packs with the prices seen on the store on 2026-10-26 (KayKit Complete
EUR 150 as the one CC0 purchase worth committing; Synty Sci-Fi City / Sci-Fi Horror / City Pack for the
art pass, never committable), the Godot tooling that decides what art is cheap (godot_voxel,
godot_dialogue_manager, phantom-camera), and the order to do it in: free kits and a proven camera first,
purchases only after the framing works.

## Known limitations (deliberate, for the next milestones)

* **No combat, hacking, BCI, PSI system or factions** — these are extension seams, per the issue;
  the case needs only the investigation loop.
* Placeholder visuals: primitives, no animation, no audio, no portrait art.
* Dialogue is linear-with-branches, not a general scripting language.
* One case, one pre-generated character (Romppainen); no character creation or advancement yet
  (blocked on the author's D23 rulings, see `docs/design/AUTHOR_DECISION_QUEUE.md`).
* No localisation: the case text is English with Finnish names; a Finnish pass is a content
  decision, not an engine one.

## Follow-on milestones

1. A second case using the same data/state contract, proving the content pipeline.
2. Cybernetics and hacking on the ubiquitous-network module (`src/rules/`), exposed in the ward.
3. PSI as a learnable ability, using the natural-PSI rules already implemented in Python.
4. X-COM-style tactical missions over the same character data.
5. The Terra-Invicta-like faction layer, reading the same scenario JSON.
