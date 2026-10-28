# Issue #742 — feasibility study: an 8-bit action-RPG variant

**Status: brainstorming and feasibility only.** Nothing here is implemented, no rule is changed, no
direction is chosen, and no Commodore 64 title is assumed as a reference. This document answers the six
deliverables in the issue and ends with a recommendation that is a *proposal for the author*, not a
decision taken on his behalf.

Method: the claims about the tabletop side are **measured against `main`**, not asserted — every function
name in §2 and §3 exists and was read. The claims about the C64, Godot 4 and the reference game are
**sourced** (§1, with the primary pages named). The cost figures are ranges with their assumptions
stated, per the issue's instruction to avoid false precision.

---

## 1. Graphics feasibility

### 1.1 True C64 restrictions versus 8-bit-inspired

These are different products, and the difference decides the whole art budget.

| | true VIC-II restrictions | 8-bit-inspired (deliberately bent) |
| --- | --- | --- |
| palette | **16 colours total**, one global background, and per-attribute colour limits inside cells | 16–32 colours, chosen freely per pixel |
| resolution | 320×200 hi-res, or **160×200** multicolour | 320×200 or 320×180, any pixel |
| character cell | 8×8, **40×25 cells**, one colour pair per cell | no cell limit |
| bitmap colour | 2 colours per 8×8 cell (hi-res); 4 per 4×8 block (multicolour) | unlimited within the palette |
| sprites | **8 hardware sprites**, pattern grid **24×21** bits (504 bits = 63 bytes), 3 colours + transparent, one shared multicolour register | any count, any size |
| scrolling | hard: no fine scroll without raster tricks | free |

The measured consequence for a game like this: **the true restrictions make the UI the problem, not the
characters.** At 2 colours per 8×8 cell, a dialogue box with readable text, a hacking panel and a PSI
effect cannot share a screen without elaborate raster tricks — that work is real, it is per-screen, and
it does not scale to the number of screens a detective game needs. The sprite grid also caps the visible
cast at 8 without raster-interrupt programming.

**Recommendation: 8-bit-*inspired*, with the restrictions that carry the look enforced and the ones that
only carry the cost dropped.** Specifically keep the 16-colour palette, the 320×200 internal grid and the
8×8 tile lattice; drop per-cell colour limits and the 8-sprite cap. This is the "high concept, low
fidelity" trade the reference game makes, and it is what a non-artist can actually ship.

### 1.2 Perspective in Godot 4

Three candidates, and the middle one is a trap worth naming:

- **Top-down, orthogonal** (`TileMapLayer` + `Camera2D`). Cheapest by a wide margin: one draw order, no
  depth sorting, no occlusion problem. Characters are one sprite, not a rig. **Recommended.**
- **Oblique / 3-4 top-down (so-called "faux-isometric")** — the *Zelda*-like 3/4 view. Reads better than
  pure top-down for interiors and faces, costs one extra art pass (south-facing walls need a visible
  face), and still needs no isometric maths. **Acceptable upgrade** if the slice looks flat.
- **True isometric** (diamond tiles, 2:1 projection, depth sorting, occlusion). Highest cost: every tile
  and character needs 4 or 8 directions *and* correct overlap sorting, and the collision maths is a
  second implementation. **Not recommended for a solo, low-art-budget project.**

Godot 4 facilities that matter here, all stable and documented: `TileMapLayer` (the 4.3+ replacement for
the old `TileMap` node), `AnimatedSprite2D`, `Camera2D`, `CanvasItem` shaders, and the project-level
stretch settings `display/window/stretch/mode = viewport` plus integer scaling and pixel snap for a
pixel-perfect presentation. The known failure mode is sub-pixel camera movement producing seam
artefacts between tiles; the fix is to snap the camera's transform and to keep the internal resolution
fixed rather than to fight it with filtering.

Light and occlusion: `PointLight2D` + `CanvasModulate` + `LightOccluder2D` gives the rainy-neon look cheaply, but a soft light pass
over a 16-colour palette can break the palette discipline. Budget one decision here: either quantise the
lit result back to the palette (a shader, some work) or accept that the palette is a *palette of
materials* rather than of final pixels.

### 1.3 Workload, per art category

| category | frames a solo non-artist must own | honest assessment |
| --- | --- | --- |
| player character, 8-direction walk | 8 dirs × 4 frames = **32** at 24×21 | the single biggest original-art job; 4-dir is half |
| NPCs / adversaries | 32 each if animated, 1 if static | static NPCs read badly in an action game — this is a real cost |
| interiors, props | tiles + modular props | **buyable and reusable**; the easy part |
| effects (muzzle, explosion, blood, PSI) | 4–8 frames each | moderate; CC0 packs cover most |
| dialogue portraits | 1 per speaker, 48×48 or 64×64 | cheap, high value, and where the identity actually lives |
| UI, hacking panel, clue log | static, 1–3 screens | cheap, and must be *readable at 320×200* — the real design constraint |

The binding constraint is not tiles, it is **animated characters**, then **effects**, then **readable
typography at 320×200**.

### 1.4 Lawful assets and toolchain

- **Kenney** (`kenney.nl`) — CC0 packs covering tiles, characters, UI, effects; the standard lawful
  starting point. CC0 means no attribution required, though crediting is still good practice.
- **OpenGameArt.org** — CC0 and per-asset licences; **must be checked per asset**, because the site hosts
  CC BY-SA, CC BY-NC and GPL material beside CC0 and the licence is per-file.
- **itch.io** — many free/CC0 packs, but "free" is not "CC0"; the licence is per pack and must be read.
- **Tools**: Aseprite (paid, the industry default) or **LibreSprite** (free fork), **Tiled** for maps,
  Godot's own tile editor, and a palette-locked workflow (a 16-entry `.gpl` palette loaded in the editor
  so no pixel can leave it).

**Licence discipline, which this repository already enforces elsewhere:** keep a `LICENSES.md` per asset
with source URL, licence and any attribution string, and never copy assets out of the reference game.
The repo's existing rights ledger is the precedent to reuse.

### 1.5 The tiny visual style guide

Deliverable-ready, and deliberately small enough that one person can hold it in their head:

```
INTERNAL RESOLUTION   320 × 200   (C64-native, 8:5)
DISPLAY                integer scale only: ×3 = 960×600, ×4 = 1280×800, ×5 = 1600×1000
PALETTE                16 entries, Pepto-family reference values, loaded as a locked palette
                       black #000000  white #FFFFFF  red #880000    cyan #AAFFEE
                       purple #CC44CC green #00CC55  blue #0000AA   yellow #EEEE77
                       orange #DD8855 brown #664400  lightred #FF7777 darkgrey #333333
                       grey #777777   lightgreen #AAFF66 lightblue #0088FF lightgrey #BBBBBB
                       (a Noöpunk subset of 8 will do the work: 3 greys, black, cyan, purple,
                        one warning orange, one highlight yellow)
TILE LATTICE           8 × 8 base, 16 × 16 for level art (2×2 cells)
CHARACTER SPRITE       24 × 21 (the C64 sprite grid) or 16 × 24; one size, no exceptions
ANIMATION BUDGET       4 directions × 4 frames = 16 for the player; 4 × 2 = 8 for NPCs
                       effects 4–8 frames; portraits 1 static frame each
TEXT                   8 × 8 or 8 × 10 font, 40 columns, 25 rows — design the UI to that grid
CAMERA                 fixed orthographic, snapped to whole pixels, no sub-pixel follow
```

**Indicative cost** (ranges, assumptions stated): CC0 packs and LibreSprite/Tiled are **€0** in money;
the real cost is time. A commissioned 24×21 character with 8 directions and 4 frames runs roughly
**€150–400** at typical indie pixel rates; a portrait around **€40–120**; a bespoke 8×8 tile set for one
biome **€300–900**. Time for the *style* itself — palette, lattice, one room, one character — is
**1–2 weeks part-time** for someone not trained in pixel art, which is the figure that matters.

---

## 2. Tabletop mechanics → action mapping

### 2.1 There is already one canonical layer, and it is bigger than expected

Measured on `main`: **61 modules in `src/rules/`** implementing CWN/SWN — combat, trauma, shock, major
injury, attack modifiers, equipment, hacking, psionics, investigation evidence, social, faction
operations — mirrored into GDScript (`39` `.gd` files, `godot/core/rules_adapter.gd`, `src/godot/*.gd`)
over **19 JSON rule data files** in `data/rules/`. An existing Godot project (`project.godot`) and an
existing scenario (`scenes/lakkahaltia`) already run on it.

**The single most important finding of this study: `godot/core/rules_adapter.gd` already exists.**
It exposes exactly the seam an action mode needs:

```
skill_check(attribute_score, skill_level, difficulty, situational, aid)
save_target(category, level, modifiers)
attack_roll(attribute_score, combat_rank, attack_bonus, armor_class, other_modifier)
difficulty_value(...) / difficulty_name(...) / attribute_modifier(...)
reseed(seed) / snapshot() / restore_dice(seed, rolls)
```

`reseed`, `snapshot` and `restore_dice` mean the adapter is **already deterministic and replayable**. An
action mode is therefore not a second game: it is a **second consumer of this adapter**, exactly as the
turn-based controller is the first. That changes the whole cost argument in §4.

### 2.2 The central design question: what the dice still decide

If the player's aim decides whether a shot connects, the six skills become decorative — and the issue's
own guardrail forbids that. If the dice decide whether the shot exists, the player's aim is decorative.
Neither is acceptable, so the split has to be principled:

> **Aim and timing decide *whether the attempt happens at all*. The roll decides *what the attempt
> achieves*. Geometry is the player's; consequence is the character's.**

Concretely, on `attack_roll(...)`:

- the player acquires a target and fires — **the character sheet decides whether that shot is tellable**;
- `attack_modifier(*circumstances)` already encodes geometry as named tokens — `target_half_cover` (−2),
  `target_almost_full_cover` (−4), `beyond_normal_range` (−2), `target_prone_adjacent` (+2),
  `one_handed_gun_in_melee` (−4) — and, decisively, an **impossible** class: `two_handed_gun_in_melee`
  and `target_unseen_position_unknown` raise `AttackImpossibleError` rather than imposing a penalty.

That last class is the most useful thing in the file for this study. The rules already say **you cannot
attack what you cannot perceive**, which is exactly the bridge a real-time mode needs: in the CRPG the
player *declares* the target; in an action mode the player must *acquire* it, and the acquisition is the
same information the turn-based game asks for. Perception stops being a UI affordance and becomes a rule
input — without a single new rule being written.

- the roll resolves as **telling hit / graze / deflection**, using the existing `AttackResult`;
- a miss is rendered as a **visible tracer that goes wide**, so the player can read the roll without a
  number. At 320×200 this is more legible than a to-hit percentage.

Everything else in the combat chapter maps as follows:

| tabletop mechanism | repo artifact | real-time expression | stays probabilistic? |
| --- | --- | --- | --- |
| attack roll vs AC | `rules_adapter.attack_roll`, `cwn_combat.attack_roll` | crosshair + fire; roll resolves effect | **yes** — the roll survives as effect |
| armour class / soak | `cwn_trauma.absorb_with_soak` | armour visibly deflects; sparks vs penetration | yes |
| hit points | `cwn_trauma.resolve_hit` | a bar, but small numbers by design | yes |
| **trauma die** | `is_traumatic`, `major_injury_risk` | any hit can be lethal; **this is the identity, keep it** | **yes** |
| shock (damage on a miss) | `shock_on_miss` | melee pressure even when you miss | yes |
| saving throws | `save_target` | hazard events: gas, a PSI assault, a collapsing floor | yes |
| cover | `target_half_cover` (−2) / `target_almost_full_cover` (−4) | real geometry **and** a roll modifier | both |
| range | `beyond_normal_range` (−2) | falloff + spread | both |
| initiative | — (turn scheduler) | **removed**: reaction time, alert state | no |
| ammo / reload | `cwn_equipment.json` | magazine size, reload as a commitment window | no |
| action economy | `cwn_combat_actions.py` | becomes cooldowns and animation commitment | no |

The two mechanisms that **must not** be player-skill-driven are **trauma** and **shock**: they are what
make a CWN-derived game feel dangerous rather than heroic, and converting them to dodgeable damage
turns NoöPunk into a twin-stick shooter with a coat of paint.

### 2.3 Real-time, real-time-with-pause, or hybrid

- **Real-time (DDS-shaped).** Best fit for hacking-as-power-fantasy and emergent combinations. Worst fit
  for a player who wants to think, and the hardest to make accessible.
- **Real-time-with-pause.** Preserves the tactical reading of the tabletop and is far easier to balance;
  costs the "groovy" feel the issue is chasing, and pause is a second UI mode to build and test.
- **Hybrid (recommended shape):** real-time by default, with a **short tactical slowdown** the player can
  trigger — not a full pause. This is a *perception* affordance, not a rules change: it changes the rate
  at which the same adapter is called, not what it decides. Accessibility becomes a dial: slowdown
  strength, duration, cooldown, or off.

**Accessibility is a design input, not a patch.** If character skill and player skill both matter, then a
player with slow reactions must be able to buy their way out with build choices — and the honest way to
do that is to let the *character* absorb the deficit: aim assist as a character-side stat, slowdown
charges as an ability, auto-cover as a stunt. That keeps the sheet meaningful for everyone.

### 2.4 Keeping the detective half intact

The Gumshoe-inspired principle is that **a clue is never behind a roll**. That survives real-time *better*
than it survives turn-based, because the equivalent of "you searched the room" is simply "you walked to
the right place and used the right tool". The existing `investigation_evidence.py`
(`Evidence`, `CustodyEvent`, `EvidenceLedger`) already models custody and provenance — so a clue found
in action mode enters the same ledger as one found in the CRPG, with the same chain of custody. Nothing
about the evidence model needs a second implementation.

The risk is different and worth naming: in real-time, **the player can simply not look**. The mitigation
is not a roll, it is affordance — the scene must make the interesting thing perceptible (a light, a
sound, a readable silhouette), so missing a clue is a choice rather than a failure of attention.

### 2.5 Hacking and the three telepathy interfaces

`cwn_hacking.py` already supplies the vocabulary: `access_pool`, `security_difficulty`,
`cyberware_difficulty`, `hacking_check`, and — importantly — **`AlertClock`**. That clock is the natural
real-time tension device: intrusion does not fail instantly, it *accumulates*, which is exactly what a
stealth game needs and exactly what a turn-based game cannot express well.

Hacking targets in a room: cameras (vision cone), doors (access), turrets (hostile→neutral), networks
(alarm state), drones (control). `cyberware_difficulty(level_or_hit_dice, has_operator)` already models
hacking a *person*, which is the most distinctive option on the list.

The three interfaces should stay visibly distinct, because that distinction is NoöPunk's, not DDS's:

| interface | expression in action | cost |
| --- | --- | --- |
| **natural psionics** (`natural_psi.py`, `psionics.py`) | an ability on a key, paid in effort (`may_use`, `effort_duration`) | effort/strain, no device needed |
| **psychotronic device** | equipment you must carry, aim and power | occupies a hand/slot; can be taken away |
| **BCI link** | a *jack-in* state: your body stands still and vulnerable while you work | the body is defenceless — the best tension in the design |

### 2.6 Three encounters, solved differently — the same sheet

Each is one character, one room, and the same gear; only the approach differs. These are the acceptance
examples the issue asks for.

1. **The server room.** *Shoot:* engage the two guards, use the racks as cover; trauma die means a clean
   win is unlikely. *Hack:* take the camera, open the far door from the inside, walk out; `AlertClock`
   rises but never trips. *Talk:* the technician is bribable — a social route that costs time, not blood.
2. **The rooftop.** *Fight:* the turret has more armour than you have ammo. *Stealth:* cross under the
   turret's cone using its own hacked camera blind spot. *PSI:* a natural-psi impression makes the guard
   look the wrong way, paid in effort you will want later.
3. **The interview.** *Intimidate:* a visible weapon changes the stakes and closes the cooperative branch.
   *Bluff:* a social check against a fixed difficulty. *Read:* walk the room, collect the two clues that
   the ledger will hold, and let the contradiction do the work — **the only solution with no roll at all**,
   and it should be the most satisfying.

---

## 3. Godot technical architecture sketch

### 3.1 The seam

```
src/rules/*.py            61 modules — THE CANONICAL RULES (Python), the test oracle
        │  mirrored by
        ▼
godot/core/rules_adapter.gd   deterministic GDScript runtime seam
        │  consumed by
        ├── turn-based controller (exists: TurnController / game_state.gd)
        └── ACTION controller (new) — §3.2
```

The two-implementation shape already exists in this repo, and that is a **strength with a known risk**:
Python and GDScript can drift. The mitigation that already fits the repo's habits is a *parity test* —
run the same vectors through both and compare, as the existing Python tests already pin the Python side.

### 3.2 What the action controller owns, and what it must never own

**Owns:** movement, aiming, firing intent, cover queries, hit delivery to the scene, animation state,
perception (vision cones, alert state), and the *cadence* at which the adapter is called.

**Must never own:** damage maths, trauma decisions, hacking difficulty, save targets, evidence validity.
Every one of those is a call into `rules_adapter.gd`. If the action controller ever needs a rule the
adapter does not expose, the correct move is to **add it to the rules layer and its tests**, never to
inline it in the controller — otherwise the two modes diverge at exactly the moment the project cannot
afford it.

### 3.3 Determinism and replay

`reseed(seed)` + `snapshot()` + `restore_dice(seed, rolls)` already make the *rules* replayable. Real-time
input is not deterministic, so replay needs **recorded input**: timestamped input events replayed against
the same seed. This is cheap to build and is the thing that makes balance work possible later — without
it, a bug in a firefight is unreproducible.

### 3.4 The vertical slice as an architectural test

The slice in §5 should be built to prove four seams, not to be fun (fun is the *second* question):

1. the same adapter serves both controllers without modification;
2. one character record drives both modes;
3. the evidence ledger records the same way from both;
4. a replay of the slice reproduces byte-identical rule outcomes.

If those four hold, an action mode is a *content* project. If any fails, it is a *rewrite*, and that is
the go/no-go.

---

## 4. Complexity and risk: turn-based vs action vs hybrid

| dimension | (A) turn-based tactical | (B) real-time top-down | (C) hybrid RTwP |
| --- | --- | --- | --- |
| **already exists?** | yes — `lakkahaltia` runs it | no | no |
| input & aiming | trivial | **high** — feel is a craft, not a feature | high |
| collision & ballistics | trivial | **high** — plus cover geometry | high |
| enemy AI / steering | low (turn order) | **very high** — must read as intentional | very high |
| animation burden | low | **very high** — every state must animate | high |
| balance | medium | high (timing interacts with stats) | **very high** (two modes to balance) |
| determinism / replay | easy | medium (needs input recording) | medium |
| accessibility | easy | **hard** (reaction time is a gate) | medium (pause is the affordance) |
| content cost per encounter | high (authored states) | medium (emergent) | high |
| "groovy" feel | low | **high** | medium |
| hacking power fantasy | medium (menu) | **high** (continuous tension) | high |

**What gets easier in an action version:** no turn scheduler, no initiative ordering, no action-economy
UI, no per-turn state machine, and far fewer authored encounter states — emergence does content work for
free.

**What gets harder:** everything that is a *craft* rather than a feature — feel, timing, feedback, AI that
looks deliberate, animation coverage, and testing a system that never stops moving. Roughly: the
turn-based version costs more *authoring*, the action version costs more *engineering and animation*.

The hybrid is the most expensive of the three, because it inherits both bills and adds a mode switch. It
is worth it only if the slowdown is genuinely the design's spine — and that is a question the slice can
answer cheaply.

---

## 5. Vertical-slice proposal

**One room, one character, one adversary, one hackable camera, one PSI ability, one dialogue/clue
interaction, one nonviolent route** — exactly as the issue specifies. Built to prove §3.4, not to demo.

| work package | assumption | time (part-time solo) |
| --- | --- | --- |
| adapter parity harness (Python↔GDScript vectors) | adapter already exists | 2–4 days |
| action controller: move, aim, fire, cover | no new rules | 4–7 days |
| one adversary with readable AI | one behaviour, one room | 3–5 days |
| hackable camera + `AlertClock` wiring | `cwn_hacking` exists | 2–3 days |
| one PSI ability on effort | `psionics.py` exists | 2–3 days |
| dialogue/clue → `EvidenceLedger` | ledger exists | 2–3 days |
| art pass: palette, room, character, effects | CC0 + minimal original | 5–10 days |
| input recording + replay | seeded adapter | 2–4 days |
| **total** | **one person, existing assets, no fun-polish** | **≈3–6 weeks part-time (or ≈1.5–3 full-time)** |

Money: **€0–400** if CC0 assets carry it and only one character is commissioned; **€1,000–2,500** if a
small bespoke tile set and two or three NPCs are bought. No false precision beyond that.

**Go/no-go criteria** — the slice passes only if *all* of these hold:

1. **One sheet, two modes.** The same character record drives both, with no per-mode fields.
2. **The roll still matters.** A low-skill and a high-skill build resolve the same firefight measurably
   differently.
3. **Nonviolence survives.** The quiet route is at least as effective as the loud one and is not a
   hidden-failure branch.
4. **No forked rules.** The action controller adds zero rule logic; the diff to `src/rules/` is empty or
   additive only.
5. **Replay is exact.** A recorded run reproduces identical outcomes.
6. **The art holds at 320×200.** Clues, dialogue and hacking are legible on a real screen at ×3.

Fail on 1, 2 or 4 → the action mode is a second game and should be **shelved**. Fail on 3 → the design is
wrong, not the technology. Fail on 6 → buy better art or drop to 4 directions; do not redesign the rules.

---

## 6. Recommendation

**Prototype. Do not adopt an optional action mode yet, and do not shelve the research.**

The reasoning, in the order it matters:

1. **The expensive part of this idea is already built.** `rules_adapter.gd` with seeded, snapshot-able,
   restorable dice is precisely the seam an action mode needs, and it exists because the turn-based game
   needed it. That makes the *experiment* cheap in a way this study did not expect to find.
2. **But the risk is not engineering, it is identity.** A shooter that merely borrows the sheet is the
   failure mode the issue's guardrail warns about. The slice exists to answer one question: can a
   CWN-derived, trauma-die game be a real-time game without becoming a twin-stick shooter wearing
   NoöPunk's coat?
3. **The right shape, if it passes, is a hybrid with a slowdown that is a perception dial, not a pause** —
   because that keeps one set of rules, one balance target and one accessibility story.
4. **The order of work is deliberate:** parity harness and determinism *first*, art *last*. If the seams
   do not hold, the art was wasted; if they do hold, the art is a bounded purchase.

What I would **not** do: build a second game, fork the rules layer, adopt a new stat set, or treat the
reference game's mechanics as a specification. It is a reference for *shape*, not for rules.

---

## 7. What would falsify this recommendation

Stated so the study can be wrong on the record:

- If the adapter cannot be called at 60 Hz from GDScript without the rules layer becoming the bottleneck,
  the shared-layer premise fails and the action mode is a separate game.
- If the trauma die makes real-time combat feel arbitrary rather than dangerous (the likely failure), the
  mapping in §2.2 is wrong and needs a different split — not a different engine.
- If the 320×200 grid cannot carry dialogue, hacking and a firefight at once, the aesthetic is the
  constraint and the resolution must rise, which changes the art budget in §1.5.
- If the slice's quiet route is not fun, no amount of engineering fixes it.

## 8. Open questions for the author

1. Which of the three perspectives (§1.2) do you want the slice in — pure top-down, or the 3/4 oblique?
2. Which specific C64-era groovy titles should inform the animation and music vocabulary? (The issue
   deliberately leaves this open; nothing above assumes any.)
3. Is **trauma-die lethality** the identity you want in a real-time mode, or should the action variant be
   explicitly less lethal so that character death is rarer than in the tabletop?
4. Should the action mode be a separate executable/scene, or a mode toggle inside the existing game?
