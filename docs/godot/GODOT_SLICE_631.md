# Godot hospital slice — issue #631

The root Godot project now launches a small offline hospital investigation. Tested
with **Godot 4.5.1 stable**, Linux x86_64, using the headless compatibility renderer.
This is a playable prototype with primitive geometry, not a finished art/pacing pass.
Graphical desktop playtesting and the target 10–15 minute duration remain unverified.

## Run from a clean checkout

Install the standard (non-.NET) Godot 4.5.1 editor from
https://github.com/godotengine/godot/releases/tag/4.5.1-stable . No Python, addons,
LLM, credentials or network connection is needed at runtime.

```sh
godot --path . --editor --import
# Open project.godot in the editor and press F6/F5, or:
godot --path .
# Automated executable tests:
godot --headless --path . --editor --quit
godot --headless --path . --script tests/godot/test_slice.gd
godot --headless --path . --quit-after 120
```

Use the actual engine executable name if it is not installed as `godot`.
Select New case. WASD/arrows move relative to the isometric camera. Approach a
labelled person/object and press E. Mouse selects dialogue choices. J opens the
scrollable evidence journal, C the demo sheet, F5 saves, F9 loads, Escape opens
the menu. Movement pauses while a panel is open. No controller support yet.

Walkthrough: doctor in the records room (northwest), nurse at reception
(southwest), patient in consultation (northeast). Each offers two interview
branches, and leaving an interview is allowed. Inspect the records-room terminal:
INT/Program against 8 displays the dice and locks that attempt. Success adds a
clock-comparison clue; failure directs you to the nurse and never blocks finishing.
After the patient interview and record inspection, visit the consultation-room
window for the possible Lakkahaltia encounter. File a mundane or anomalous
working hypothesis at the report desk (southeast). All three interviews plus the
record are required; the anomalous route also requires the window encounter.
You can continue investigating and revise the report afterwards.

Saves: `user://lakkahaltia-v1.json` in Godot's application user-data directory.
The schema stores character, interviews, evidence, journal, check result, ending
and player location. Write-to-temp then rename avoids replacing a good save with
a partially written one. Missing, malformed and unsupported saves leave the
current case intact. Legacy Python/Fate/d10 saves are deliberately not imported.

## Audit and reuse

Read root `AGENTS.md`, `RULEBOOK.md` and its current baseline override,
`rulebook/WITHOUT_NUMBER_BASELINE.md`, `docs/archive/DESIGN_PRINCIPLES.md`,
`docs/design/ISSUE_626_ROMPPAINEN_EUROPOL_UNIT.md`, #564 timeline and #615.
No nested instructions apply to the changed directories. No private/external
NoöPunk-specific agent skill file was available in this workspace to update.
Tests exercise executable behavior only; no prose/canon tests or gates were added.

PR #632 already supplied `src/godot/wn_rules.gd`; this implementation extends it
and the existing root `project.godot` / `scenes/main.tscn`, rather than introducing
a competing project. Existing Python, Concordia and crossover runtimes remain.
The superseded `core_rules.gd` stays available to legacy consumers.

The latest explicit author override adopts STR/DEX/CON/INT/WIS/CHA, 3–18 scores,
and 2d6 checks. #564's historical restrictions do not override that later decision.
The adapter reads the existing `wn_core.json` contract; investigation resolution
uses it directly. The demonstration character uses the baseline's illustrative
attributes, not a newly specified character-creation system. Only skills needed
for this slice are exposed. No combat, progression or psychic ability is implied.

## Structure and scope

- `data/scenarios/lakkahaltia.json`: original draft scenario, interview branches,
  evidence and competing interpretations, endings, minimal demonstration sheet.
- `src/godot/investigation/case_state.gd`: authoritative case state, quest gates,
  rules call, versioned persistence. Independent of scene nodes.
- `src/godot/investigation/hospital.gd`: primitive 3D layout, collision, orthographic
  camera, proximity interaction and UI; presentation separated from case logic.
- `tests/godot/test_slice.gd`: deterministic checks, both success/failure routes,
  endings, persistence, invalid save, real scene and button wiring, collision.
- `.github/workflows/godot-slice.yml`: pinned engine import/tests/launch.

Scenario dialogue is an editable demonstration authored for #631, not a new
universal canon ruling. Uses #626's consent/corroboration procedure and pre-crisis
hospital frame. No illness-as-proof-of-PSI mechanic, truth detector or supernatural
classification. The requested podcast is an inspiration reference only: its
contents were not transcribed or independently verified for this implementation.

## Asset manifest

| Asset | Source | Rights / attribution | Redistribution |
|---|---|---|---|
| Hospital, props, people | Godot BoxMesh/CapsuleMesh primitives constructed by original project code | No third-party art files | Safe to include as code |
| Interface font | Godot built-in default | Distributed with Godot; retain Godot distribution notices in builds | No font copied into repo |
| Dialogue, evidence | Original draft JSON for #631 | Project-authored, no source-book expression | No purchased or external art |

No external asset packs or addons are included. Future Kenney/Quaternius/etc. pack
selection must record the exact pack license before import. No publisher art,
book PDFs or purchased assets were committed. Without Number is by Kevin Crawford /
Sine Nomine Publishing; this unofficial project is not endorsed by the publisher.

## Follow-on milestones

1. Desktop playtest, responsive UI, reusable authored room/prop scenes, licensed
   art, accessibility and expanded investigation pacing.
2. CWN hacking/cybernetics behind case actions, with access prerequisites.
3. SWN PSI only through the approved package/technique adapter; keep testimony
   separate from mechanical evidence. WWN exploration and AWN survival when needed.
4. Tactical combat, then global strategy through explicit shared-rule adapters.
