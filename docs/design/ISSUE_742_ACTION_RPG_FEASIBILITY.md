# Issue #742: 8-bit action-RPG feasibility study (proposal, not an implementation decision)

**Status:** research complete; optional prototype is **not approved**. This is about the legacy RPG, **not** the separate LaclauGPT crossover strategy game.

## Executive recommendation

**Prototype a small optional real-time action adapter only after the tabletop procedures and one coherent investigation scene are stable. Do not replace the turn-based/narrative-first RPG.** Share character/scenario data and investigative outcomes; keep combat presentation and controls replaceable. Avoid promising that one tabletop attack roll can be converted *exactly* into aiming a mouse: identical probabilities require an explicit abstraction, which may feel less responsive.

Repository grounding (as reviewed 2026-10-28):
- `AGENTS.md` requires tabletop-first, author approval for new mechanics, and tests of executable code only.
- `rulebook/WITHOUT_NUMBER_BASELINE.md` (current authority): CWN primary; SWN specialist PSI; AWN crisis and WWN exploration; STR/DEX/CON/INT/WIS/CHA; 2d6 skill checks and d20 attack/save rules. **Do not reuse retired FIT/REF/PSY/CYB or old 1d10 adaptation.**
- `docs/GODOT.md` describes the existing Godot 4.5.1 Lakkahaltia detective slice, with movement, dialogue, evidence, rules adapter and save state, **without** combat or a full hacking/PSI system.
- `docs/CWN_SRD_GODOT_IMPLEMENTATION.md` includes generic attack resolution and hacking *eligibility* only: neither constitutes full combat/hacking gameplay. The source-book rules are not all implemented.
- This proposal must preserve the Lakkahaltia slice, its narrative outcomes and the two-games-one-world boundary.

## 1. Art direction: low-fi is a budget strategy, not automatically a low-cost game

**Suggested visual target for an experiment (not canon):** top-down orthographic 2D, 320×180 virtual resolution upscaled by integer factors when possible; 16×16 or 24×24 world tiles (choose one after a readability test); 16–32 px actors with **4 directional poses** and an initial 2–4 frame walk animation. Limit the initial palette to a curated **16–24 colors** inspired by C64, while allowing accent colors for health, interactables, holograms and PSI legibility. Make sprites/tiles yourself only where store assets do not match. Avoid pure C64 hardware compliance; it adds color-cell/sprite constraints without much design benefit. True C64-style restricted palette remains a possible optional art challenge.

**Perspective trade-off:**

| Camera | Pros | Costs | Recommendation |
|---|---|---|---|
| Strict top-down | Fewest sprite orientations, readable shots/cover | Less architectural drama | **First experiment** |
| Oblique / three-quarter | Stronger interiors and character identity | More sprites, collision/occlusion care | Later |
| Faux-isometric | Stylish landscapes and architecture | Art, movement, aiming and collision harder | Not for first slice |

**Budget by asset class:** map walls/floors/props are low-medium with reusable tile sets; directional character animations medium-high; death, recoil, impact and status effects medium; dialogue portraits high if many individualized NPCs; elaborate noetic dreamscapes high unless procedural shaders are restrained. UI and type readability should be tested at desktop and laptop scales.

**Godot 4.5 route:** `TileMapLayer` + `TileSet` for floors/walls, `CharacterBody2D` and `CollisionShape2D` for movement, `AnimatedSprite2D` or `Sprite2D` for actors, `Camera2D` for framing, `Area2D` for interaction, `RayCast2D` for visibility; `CanvasLayer` for crisp UI; sparing `GPUParticles2D` / shader effects for powers. Configure nearest texture filtering, pixel snapping and integer-friendly window scaling. Test camera jitter when character positions land between logical pixels. Use separated canvas/UI rendering if retro-scale text becomes unreadable.

**Legally reusable asset candidates (verify exact files, licenses and redistribution at acquisition):**
- [Kenney Top-down Shooter](https://kenney.nl/assets/top-down-shooter): source page reports **580 files, CC0**. Good for a mechanical placeholder; visual harmony with C64 style not guaranteed.
- [Kenney catalog](https://kenney.nl/assets): explore UI, audio, 2D tiles; verify each pack.
- [LibreSprite](https://github.com/LibreSprite/LibreSprite): free pixel editing/animation and palette work; editor's GPL license is **not** automatically a restriction on original sprites drawn with it.
- [Pixelorama](https://github.com/Orama-Interactive/Pixelorama): alternative Godot-based pixel art editor; verify its current release/license before use.
- [Tiled](https://www.mapeditor.org/): optional external map editor; native Godot TileMapLayer may suffice.
- [Godot official docs: TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html).
- [Godot official docs: 2D pixel art](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html).

Avoid importing DDS code, sprites, narrative, sound or named abilities. Its *design pattern* (emergent interaction between guns, hacks, powers and lethal opposition) is inspiration, not an asset license. No particular C64 game has been named by the author: leave candidate titles undecided. A few characteristic inspirations to assess *only as open examples* are top-down legibility, raster-like glitching, economical looping music and hardware-implied rhythm; do not falsely attribute the author's favorite titles.

**Suggested art exercise:** make one ward corridor, a character silhouette facing four directions, one gun, a security camera, a door, a clue highlight and an understated PSI distortion. Compare using placeholders, customized CC0 assets and original low-resolution art. Do not purchase assets before a windowed readability test.

## 2. Shared tabletop contract, optional digital action translation

The authoritative *tabletop* actions and resource rules remain governed by `rulebook/WITHOUT_NUMBER_BASELINE.md` and the source books. The following are **interface research questions and candidate adapters, not adopted rules**.

| Tabletop / narrative source | Potential digital action expression | Fidelity and risks |
|---|---|---|
| CWN STR/DEX/CON etc., Edges, Foci, gear | One versioned character record consumed by either combat UI | Never convert historical 1–10 stats automatically |
| CWN Shoot, armor, d20 attacks | Crosshair + line-of-sight and range; resolve impact via canonical attack procedure **or** offer a skill-influenced hit model | Mouse precision and dice accuracy are different; compare both openly |
| CWN HP, injury, saves, ammo | Hit feedback and death/stagger states; data-driven resource accounting | Keep lethality and injury as tabletop-owned decisions |
| Initiative / action economy | Real-time cooldown/readiness meter or real-time-with-pause scheduling | Not automatically probability-equivalent to turns |
| Cover and tactical positioning | Collision, occlusion and cover tags with tabletop-defined modifiers | Must test line-of-sight vs raycast disagreements |
| Sneak / Notice | Sight cones, sound zones, alert escalation using documented checks | Never turn all successes into twitch reflex tests |
| Program / hacking (CWN) | Select camera/door/turret; validate connection, access and costs using source rules; show consequences | Existing code supports precheck only; **no invented one-click omnipotence** |
| SWN Telepathy, Precognition, Telekinesis etc. | Explicit commands with source-defined eligibility and cost; pause to select targets | Avoid inventing effects or automatic PSI availability |
| BCI / psychotronics vs natural PSI | Three distinct interfaces/fictional approaches to interaction | No new numeric stat or unauthorized PSI discipline |
| Clues / evidence board | Guaranteed access to core clues after appropriate fictional investigation; optional roll produces bonus or complication | No twitch gate in front of essential clues |
| Talk / social conflict / ideology | Dialogue UI, stateful relationships and network/faction consequences | Violence cannot be required to finish the case |

**Two alternative hit models to test:** (A) mouse click designates attack target, CWN d20 determines hit (strong tabletop fidelity, may feel unfair when apparently on target); (B) physics determines whether a projectile touches target and CWN checks govern shot dispersion/recoil/weapon effectiveness, with explicit, quantified divergence from tabletop outcomes. A third mode, **pause-and-designate**, can retain d20 resolution while providing high-action movement. Do not silently claim all three have the same odds.

**Accessibility:** remappable controls; optional aim support and tactical pause; consistent keyboard-only targeting; adjustable combat tempo; ability-driven outcomes instead of requiring fast reactions; no time pressure for dialogue and clue reading.

**Noncombat goals preserved:** always require at least one authored nonviolent solution to a representative mission. Example encounter designs (illustrative only; not canon):
1. **Ward corridor:** armed guard blocks a medical record. Shoot, discuss access, or find a maintenance key; record remains obtainable by investigation.
2. **Security hub:** avoid patrol by examining logs, bypass via approved Program/hardware access, or fight; network ownership changes the route, not the clue's existence.
3. **Anomalous room:** optional unusual perception interaction adds information or complications without confirming an ontological explanation; plain detective investigation can still close the case.

## 3. Architecture: share state, never fork the whole story

```text
Tabletop rulebook + versioned scenario/character data
      |
      +-- rules kernel / canonical events and outcomes
      |     character, abilities, tags, equipment, resources
      |     checks, attacks, saves, authorized hacking/PSI
      |
      +-- persistent case state / clues / dialogue / world flags
      |
      +-- turn-based tactical presentation (future)
      |
      +-- optional real-time presentation (experiment)
              input -> movement/aim -> action request
              -> kernel validation/result -> effects/animation
```

**Crucial boundary:** don't put numeric CWN rules in Godot weapon scripts. Godot should send an action request (actor, target, source, equipment, context) and consume a canonical result (legal, dice/result, resource changes, clue/flag changes). Visual collision may report eligibility or target contact, but it must not *silently override* rules. Preserve `src/godot/wn_rules.gd`, `cwn_rules.gd`, `case_state.gd` as relevant existing layers; review before adding adapters. Treat hacking, PSI and combat as future plug-ins until their tabletop procedures are sufficiently documented. Shared JSON cases enable physical tabletop adjudication.

**Suggested Godot node sketch (design only):**
```text
ActionExperiment (Node2D)
  World (Node2D)
    Ground (TileMapLayer)
    Obstacles (TileMapLayer)
    Interactables (Node2D)
    Actors (Node2D: CharacterBody2D descendants)
  ProjectilesOrHitScans (Node2D)
  Camera2D
  CanvasLayer: dialogue/evidence/ability wheel/pause
```
Use dependency-injected state/rules interfaces rather than writing to the canonical save from an experimental scene. Do not create any of these scripts as part of issue #742.

## 4. Complexity and feasibility matrix

| Dimension | Narrative + turn-based tactical | Real-time top-down action | Real-time-with-pause |
|---|---|---|---|
| Input responsiveness / aiming | Low | **High** | Medium-high |
| Action scheduling | **Medium-high** | Medium | **High** (two clocks) |
| Enemy AI / path / cover | Medium | **High** | High |
| Animation and feedback | Medium | **High** | High |
| Character-rules fidelity | High / straightforward | **Complicated** | Medium-high |
| Timing / collision / balancing | Medium | **High** | **High** |
| Detective dialogue/content | **Same substantial workload** | **Same substantial workload** | **Same** |
| Solo-dev art burden | Medium | Medium-high | Medium-high |
| Debuggability/determinism | Easier | Harder | Hardest if mixed modes |

**A small pure shooter can be simpler than a full tactical game** because it need not implement turn order, movement grids or elaborate action menus. But a DDS-like *RPG* requires combat feel, frame-timing, enemy behavior, multiple power combinations and narrative state. Those are not cheap. A hybrid that preserves both modes can be the highest-cost option despite looking like a compromise.

**Very rough time-boxes, not forecasts:** single experienced Godot/Python programmer, existing narrative slice, CC0 placeholders, no multiplayer or custom engine, part-time context switching excluded:
- Art/readability experiment: **2–5 focused workdays**.
- One-room mechanical action proof (movement, aim, enemy, collision, mocked weapon feedback; not canonical rules): **5–15 focused workdays**.
- A proper representative micro-slice with shared character and case state, alternative nonviolent completion, a bounded hacking interaction and PSI interface mock: **15–40+ focused workdays**, *only once source-defined mechanics are available*.
- Production-quality DDS-like feel, systemic enemy AI, content, sound and polish: **months**, not an issue-sized add-on.
- Turn-based one-room tactical equivalent: **8–25 focused workdays** (scheduling/UI vs simpler timing); comparing these ranges is indicative only, not a measured benchmark.
- Commercial art/audio: **€0 for a placeholder study** using verified CC0/reusable licenses; later purchases variable and approval-gated.

Biggest risks: branching gameplay × feedback polish × animation load; inability to preserve tabletop odds under manual aiming; feature creep from hacking bullets/time and extensive power interactions; inconsistent story results across modes.

## 5. Proposed vertical-slice experiment (NOT authorized for this issue)

**One location, 3 completion paths, 1 controlled actor, 1 NPC opponent, 1 security device, 1 clue, 1 dialogue, 1 source-defined PSI capability where permissible.** Start from fictional ward-like geometry but **do not change the existing Lakkahaltia scene**.

1. Record tabletop character/gear and scenario state as a fixture.
2. Build **the same encounter** in a tactical turn presentation and a separate real-time presentation.
3. Ensure core clue and at least one peaceful conclusion remain reachable in both.
4. Report implementation hours by programming, UI, sprites, sound, debugging and source-rule interpretation.
5. Compare hit outcome distributions (e.g. 1000 simulated trials for dice-driven variants), UI readability, input feel and scenario-state consistency.
6. Obtain human playtest feedback for perceived agency and fairness. Automated tests only for **executable behavior**, not design text/lore (per `AGENTS.md`).

**Go/no-go gates for an optional *future* prototype:**
- Can be built without altering approved tabletop mechanics or existing campaign endings.
- Can reuse canonical character/state schema instead of migrating it.
- Core clues cannot become inaccessible due solely to shooter reflexes.
- Basic movement/combat demonstrably readable at chosen resolution.
- A beginner can resolve encounter through at least two substantially different approaches.
- Measured prototype labor and maintenance are acceptable to the author; no full second product is implied.

## 6. Decision

**Recommend: document and potentially time-box a top-down action micro-prototype; keep the narrative/turn-based path primary.** If action controls are satisfying yet d20-on-click feels bad, investigate a pause-and-designate combat adapter before modifying the tabletop math. Revisit only after the source-rule combat/hacking gaps are addressed and author approves the slice. Do not simultaneously maintain two full game branches.

### Source and license verification log

Checked 2026-10-28:
- DDS gameplay/design claims: https://store.steampowered.com/app/1545990/Deadeye_Deepfake_Simulacrum/ (official store description).
- Godot TileMapLayer API: https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html (Godot 4 replacement for deprecated TileMap).
- Kenney Top-down Shooter: https://kenney.nl/assets/top-down-shooter (CC0, 580 files on publisher's page).
- LibreSprite: https://github.com/LibreSprite/LibreSprite (GPLv2 editor).
- Baseline and runtime status: repository files listed at top. Other asset/tool candidates are leads, not fully audited packs.

**Out of scope:** gameplay code, locked visual canon, new RPG stats, external asset purchases, repo-wide changes, NHI ontology rulings, and any promise of identical real-time/tabletop probability without experimental evidence.
