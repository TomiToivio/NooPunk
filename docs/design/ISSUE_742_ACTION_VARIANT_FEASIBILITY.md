# 8-bit action-RPG variant: feasibility study (issue #742)

**Status: brainstorming / feasibility only. This is not a decision, and it does not replace the
narrative-first turn-based NoöPunk RPG.** Nothing here is canon, no mechanic is approved, and no second
game is created by this document. Marks used throughout: **FACT** (verifiable, cited or arithmetic),
**PROPOSAL** (mine, for the author to accept or refuse), **UNVERIFIED** (stated so it is not mistaken
for research I did).

The issue asks five things: a graphics memo, a tabletop-to-action mapping, a Godot architecture sketch,
a complexity/risk matrix, and a vertical-slice proposal with go/no-go criteria. That is the order below.

---

## 1. Graphics: what the aesthetic actually costs

### 1.1 Two different things are called "8-bit", and only one is affordable

**FACT — true C64 constraints** (the machine, not the vibe): a 320×200 display, a fixed **16-colour**
palette, an 8×8 character cell, hardware sprites of 24×21 pixels (12×21 in multicolour), and a
**160×200 multicolour mode** where each 4×8 cell may use only 3 colours plus transparent. Colour choice
is shared per cell, not per pixel.

**PROPOSAL — use 8-bit-inspired, not hardware-exact.** The hardware rules are where most of the art cost
lives: per-cell colour sharing makes every redraw a puzzle, and the restrictions forbid exactly the
effects this issue asks for — light/occlusion, PSI effects, particles, weapon feedback. A "groovy C64
aesthetic" can be had with the *palette discipline and chunky silhouette* of the era while bending its
limits, which is what most modern retro games do.

### 1.2 Numbers that make the style guide reproducible

**FACT (arithmetic):** an internal resolution of **384×216** is exactly 16:9 and scales by an integer
**5×** to 1920×1080 — pixel-perfect on the most common display, no filtering, no shimmer.

**PROPOSAL — the style constraint set:**

| Constraint | Value | Why |
| --- | --- | --- |
| Internal resolution | **384×216** | exact 16:9; integer 5× to 1080p |
| Tile size | **24×24** | 16 tiles across, 9 down — clean map maths |
| Character sprite | **24×32** (feet on a 24×24 tile) | body taller than tile without breaking the grid |
| Palette | **16–32 colours**, 3 ramps (shadow/mid/highlight) | C64 discipline without per-cell pain |
| Directions | **4** (N/E/S/W), not 8 | see 1.3 |
| Perspective | **top-down**, slight 3/4 camera offset | cheapest readable option |

### 1.3 The animation budget is the real cost, not the palette

**PROPOSAL (estimate).** With 4 directions and the minimum readable set — idle 2, walk 4, shoot 2,
hurt 1 — a character is **36 frames**. Five playable characters plus ten distinct NPCs is 15 × 36 =
**540 frames** at 24×32. That is a real but survivable workload for a non-artist using a strict base
sprite and palette swaps. **8 directions doubles it to ~1,080 frames**, which is why 4 is the
recommendation; faux-isometric triples the drawing problem again and is not recommended for a solo
developer.

### 1.4 Toolchain and assets

**FACT/PROPOSAL:**
- **Godot 4**: `TileMapLayer` (4.3+; the older `TileMap` node is deprecated), `AnimatedSprite2D`,
  `Camera2D`, `Light2D` + `Occluder2D` for the occlusion the issue mentions, `GPUParticles2D` for
  effects, and the project settings `rendering/textures/canvas_textures/default_texture_filter =
  Nearest`, `snap_2d_transforms_to_pixel`, `snap_2d_vertices_to_pixel`. Stretch mode `canvas_items` or
  `viewport` gives the integer scaling above.
- **Asset sources**: Kenney packs are **CC0** (verify per pack); OpenGameArt is **mixed-licence** and
  must be checked asset by asset; itch.io packs vary. **Do not copy Deadeye Deepfake Simulacrum
  assets** — the issue says so and it is correct.
- **Tools**: Aseprite or LibreSprite for sprites and animation; Tiled if a tile pipeline outside Godot
  is wanted (Godot's own TileMapLayer is usually enough).
- **UNVERIFIED**: exact licence text of any specific pack, and whether a chosen pack's style matches the
  palette above. Both are per-pack checks, not assumptions.

### 1.5 What this memo does not claim

It does not claim a non-artist can produce a *finished* 8-bit game cheaply. It claims the **style** can
be constrained so that the art is enumerable (a palette, a tile size, a frame budget), which is the
difference between "I could try" and "I can estimate it".

---

## 2. Tabletop to action: one sheet, one ruleset, a different controller

### 2.1 The governing rule

**PROPOSAL — the character sheet stays authoritative; the action layer is a controller, not a second
ruleset.** The same CWN + SWN + NoöPunk data (stats, skills, gear, cybernetics, psionics, injuries,
social and investigative progress) feeds both a turn-based and an action presentation. If a value
exists only in the action mode, it is a bug.

### 2.2 Mapping table

| Tabletop concept | Action-mode expression | Who decides the outcome |
| --- | --- | --- |
| Attack roll vs AC | Player aims; a **shot window** opens whose width derives from the character's attack bonus; a hit inside the window resolves the roll | Rules layer (seeded) |
| Damage roll | Unchanged; applied on a resolved hit | Rules layer |
| HP / trauma | Same pools; no action-only health | Rules layer |
| Armour | Same damage reduction; no dodge-stat substitute | Rules layer |
| Saving throws | Timed prompt (dive for cover, resist PSI) whose **window** scales with the save | Rules layer |
| Range and cover | **Geometry, not abstraction** — the one place the action mode is richer than the table | Real space |
| Initiative | Turn order disappears; simultaneity replaces it (or pause restores it) | Mode |
| Ammo / reload | A real input beat, not a bookkeeping line | Player |
| Lethality | Unchanged — and the strongest argument for real-time-with-pause | Rules layer |
| Hacking | A held action on a device/network; success still rolled | Rules layer |
| PSI | A resource-limited verb; resistance still rolled | Rules layer |

### 2.3 What must stay probabilistic, and what may become player skill

**PROPOSAL.** Keep probabilistic: to-hit, damage, saves, PSI resistance, hacking success, clue
discovery. Allow player skill: positioning, when to take the shot, target choice, cover use, when to
initiate a hack, route selection.

**The fairness rule that makes this honest:** player skill must not silently replace character skill.
Express character competence as **window width, not hidden bonuses** — a highly skilled character gets a
wider aim/save window and a longer reaction allowance; a low-skill character gets a narrow one. The
player's skill decides whether they *use* the window, not whether the character is competent. Without
this rule an action version invalidates every non-combat build.

**Accessibility/difficulty:** real-time-with-pause, bullet-time, and difficulty expressed as
window-width and reaction-time multipliers — **never** as silent stat inflation, which would break
tabletop parity.

### 2.4 What must survive from the current design

- **Gumshoe-inspired clue reliability**: a clue is never gated behind an action check. The action layer
  may change *how* you reach a clue, never *whether* the investigation can proceed.
- **Dialogue, social and ideological conflict** remain first-class; combat is one tool.
- **Nonviolent resolution** must be reachable in the same encounter geometry.
- **The three telepathy interfaces stay distinct**: natural psionics, psychotronic devices, BCI links —
  three verbs with different failure modes, not one "magic" button.
- **Hackable world**: cameras, doors, turrets, networks, drones; optionally enemies and projectiles.
  Astral/noetic encounters are a **separate mode**, not a shooter reskin.

### 2.5 Same sheet, three solutions (illustrative, not canon)

1. **The lobby.** Two guards, a camera, a locked door. *Combat:* shoot both, take the risk of alarms.
   *Hack:* take the camera, loop it, walk past. *Social:* the concierge can be talked into a delivery
   pretext. All three consume the same turn/action budget in tabletop terms.
2. **The server room.** A turret and a trapped corridor. *Combat:* destroy the turret, eat the damage.
   *Hack:* turn the turret's IFF against its owner. *PSI:* remote-view the room first, then route around
   the trap. The character sheet is identical in each.
3. **The square.** A protest, a police line, an NHI observer. *Combat:* provocation, escalation.
   *Ideological:* reframe the demand to split the coalition. *Investigation:* expose who funded the
   counter-protest. No shots fired, same mechanical weight.

---

## 3. Godot architecture sketch

**PROPOSAL — a shared rules core with a swappable combat controller.**

```
data/            character, gear, cybernetics, psi, injuries   (one source of truth)
rules/           resolution: attack, skill, save, hack, psi    (pure, seeded, testable)
controllers/     TurnBasedController  |  ActionController  |  RTwPController
presentation/    tilemap, sprites, UI, dialogue, effects
```

- Both controllers call the **same** `resolve_*` functions. The action controller supplies *intent*
  (target, shot-window quality, cover state, hack initiation) and receives the *outcome* from the rules
  layer. It never rolls its own damage.
- **Determinism**: a seeded RNG plus an input log makes an action session replayable, which is how
  tabletop parity stays testable — the same seed and the same recorded inputs must reproduce the same
  outcomes.
- **Do not fork the project.** The canonical tabletop/CRPG code stays the data and rules authority; the
  action variant is a presentation adapter over it. A second full codebase is the failure mode this
  section exists to prevent.

---

## 4. Complexity and risk: turn-based vs action vs hybrid

Assumptions, stated so the ranges mean something: **one solo developer, part-time, limited art skill,
existing lawful assets, shared rules layer already built, no netcode.**

| Area | A: turn-based | B: real-time | C: RTwP |
| --- | --- | --- | --- |
| Rules layer | shared | shared | shared |
| Turn scheduler / initiative | **high** | none | none |
| Input feel / aiming | low | **high** | medium |
| Ballistics, collision, LOS | medium | **high** | high |
| Enemy AI / steering | medium | **high** | medium (pause absorbs pressure) |
| Animation volume | medium | **high** | high |
| Level design | medium | high | high |
| Balance (player skill confound) | low | **high** | medium |
| Determinism / replay / save | medium | **high** | medium |
| Accessibility | low | medium | **low (built in)** |
| Estimated relative effort | **1.0×** | **1.8–2.5×** | **1.5–2.0×** |

**What gets easier in an action version:** no turn scheduler, no initiative bookkeeping, fewer modal UI
screens, and emergent situations replace some authored encounter scripting.
**What gets harder:** input feel, ballistics, AI steering, cover logic, animation volume, balancing
(player skill confounds character build), replay determinism, and debugging timing bugs.

**PROPOSAL — the read.** B is not "A plus a shooter". It is a different cost profile: cheaper on
bookkeeping, much more expensive on feel and content. **C (real-time-with-pause) is the best
fidelity-per-effort point**, because pause removes reaction-time pressure from the AI and from the
player, keeps lethality survivable, and leaves the rules layer almost untouched. These ranges are
estimates with assumptions, not promises.

---

## 5. Vertical slice, and the criteria that would kill it

**PROPOSAL — exactly the slice the issue describes, nothing more:** one room, one controllable
character, one adversary, one hackable camera or turret, one PSI ability, one dialogue/clue
interaction, one nonviolent route. **The same character and gear data file is loaded by both the
turn-based and the action mode.**

Measure, per mode: development hours actually spent; readability (can a new player tell what is
happening?); enjoyment; and **tabletop-outcome fidelity** — the same character against the same
adversary should produce the same *distribution* of outcomes over seeded trials.

**Go / no-go criteria (falsifiable):**

- **Go** if the slice is playable in both modes from one data file, and the action mode's outcome
  distribution is within a stated tolerance of the turn-based one over ≥200 seeded trials.
- **Go** if a low-combat character remains viable: a build that wins the turn-based encounter must not
  become unable to win the action one.
- **No-go** if the slice exceeds roughly **60–120 hours** of solo work, if the two modes need separate
  character data, or if the action mode cannot express the nonviolent route without new mechanics.
- **No-go** if "feel" cannot be reached without a dedicated animation budget the project does not have.

**Rough range:** 60–120 hours for the slice, dominated by input feel and animation, not by rules code.
Coarse on purpose — the issue asks for no false precision.

---

## 6. What I could not verify

- **Deadeye Deepfake Simulacrum's actual mechanics.** I have not played it; the description above
  follows the issue's own characterisation (real-time shooting, stealth, hacking-driven emergent
  combinations). Any claim about *how* DDS implements those would need hands-on play. Its **mechanics
  must not be copied**, per the issue; only the emergent-combination *idea* is borrowed.
- **Specific C64-era titles.** The issue says they are to be chosen later; I have not chosen them.
- **Per-pack asset licences**, and whether any pack's art matches the palette.
- **The project's actual Godot version**, which decides whether `TileMapLayer` (4.3+) or the older
  `TileMap` applies.

---

## 7. Measured baseline (added later)

Sections 1–6 were written as a design study. This section is different in kind: it was produced by
reading `main` and running its suites, and it exists because two of the questions §6 lists as
unverifiable are in fact verifiable here — and because the answer changes the cost estimate in §5.

**Engine, settled.** `project.godot` declares `config_version=5` and
`config/features = ("4.7", "GL Compatibility")`, and both Godot workflows pin **4.7.2-stable**. So the
`TileMapLayer` (4.3+) question in §6 resolves to *`TileMapLayer`*, and there is no `TileMap` in any
scene to migrate — the project currently uses **no tilemap node at all**, so a tile-based view costs
nothing in migration.

**The shared seam already exists.** §3 proposes sharing state rather than forking. The repository already
does this for one consumer: `godot/core/rules_adapter.gd` is the GDScript runtime seam over the Python
rules, and it already exposes `attack_roll`, `skill_check`, `save_target`, `difficulty_value` and
`attribute_modifier` — plus `reseed(seed)`, `snapshot()` and `restore_dice(seed, rolls)`, which make the
rules layer **already deterministic and replayable**. An action mode is therefore a *second consumer of
an existing seam*, not a new layer to build. The inventory behind it: **61 modules in `src/rules/`,
mirrored into 39 `.gd` files, over 19 JSON datasets in `data/rules/`**, with the turn-based scenario
(`lakkahaltia`) already driving it.

**The rules already say what the action mode needs them to say.** Four findings, each read rather than
assumed:

- `cwn_attack_modifiers.py` encodes geometry as named tokens — `target_half_cover` (−2),
  `target_almost_full_cover` (−4), `beyond_normal_range` (−2), `target_prone_adjacent` (+2),
  `one_handed_gun_in_melee` (−4) — **and it has an impossible class**: `two_handed_gun_in_melee` and
  `target_unseen_position_unknown` raise `AttackImpossibleError` instead of applying a penalty. So
  *"you cannot attack what you cannot perceive"* is already a rule, which is precisely the bridge
  between a declared target in turn-based play and an acquired target in real time. No new rule is
  needed to make perception load-bearing.
- `cwn_hacking.AlertClock` already models intrusion as **accumulation** rather than a single check —
  the tension device real-time stealth needs and turn-based play cannot express well.
- `psionics.py` already prices abilities in effort (`may_use`, `effort_duration`), so the three telepathy
  interfaces can differ by cost rather than by new subsystems.
- `investigation_evidence.py` already provides `Evidence`, `CustodyEvent` and `EvidenceLedger`, so a clue
  found in action mode enters **the same chain of custody** as one found in the turn-based game.
- `cwn_trauma.py` provides `is_traumatic`, `shock_on_miss`, `major_injury_risk`, `absorb_with_soak` and
  `resolve_hit` — the trauma mechanism that §2.3 rightly identifies as the identity that must stay
  dice-driven rather than dodgeable.

**Consequence for §5.** The *engineering* half of the slice is materially cheaper than §5's range
implies, because the adapter, the determinism and the rule vocabulary already exist; the remaining risk
is concentrated where §5 already puts it — input feel and animation coverage. That does not alter the
recommendation, which is the same one this section would make: **prototype the slice; adopt nothing,
shelve nothing.**

**What is still genuinely unverifiable here:** how Deadeye Deepfake Simulacrum actually implements its
mechanics (§6, first bullet). That remains a hands-on-play question.

**Note on duplication.** Two documents now exist for this issue —
`ISSUE_742_ACTION_RPG_FEASIBILITY.md` and this one — written independently in the same window. They cover
the same six deliverables and should be collapsed into one by the author rather than maintained in
parallel. This section is additive and preserves the rest of this document verbatim.

— Ai 愛
