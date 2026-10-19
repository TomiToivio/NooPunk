# Tactical map spike: renderer, tile format and mission-data schema

**Status: a technical-spike record. It decides nothing; it makes a decision cheap.**

Issue [#515](https://github.com/TomiToivio/NooPunk/issues/515) asks for a minimalist top-down
8-bit tactical map serving **both** X-COM-style squad combat and Shadowrun-style investigation
quests, and it says plainly that this is *"a future enhancement, not a blocker for the current
text/narrative-first MVP"*. Its first milestone is a spike: **choose renderer, grid/tile format and
mission-data schema.**

This record is that spike. Two of the three items are **answered as engineering, not as rulings**:

| #515's spike item | Where this milestone lands it |
| --- | --- |
| **Mission-data schema** | **Built and tested**: `strategy_game/tactical/mission.py`, the packaged fixture `data/tactical/spike_mission.json`, and the headless session that reads it |
| **Grid/tile format** | **Built and tested**: ASCII `.`/`#`/`+` rows in JSON, `strategy_game/tactical/grid.py` (§9) |
| **Renderer** | **Evaluated, not chosen** — this record's recommendation is §8, and the choice is queued as **row D29** of [`docs/design/AUTHOR_DECISION_QUEUE.md`](../../docs/design/AUTHOR_DECISION_QUEUE.md) |

Nothing here approves a rule. `strategy_game/RULEBOOK.md` keeps its **NO RULES APPROVED** status, no
enemy, combat round, line of sight, cover, stealth, PSI or hacking mechanic exists in the prototype,
and no engine is installed or added as a dependency.

## 1. What is being decided, exactly

One question, in the form the author can answer it:

> **What draws the tactical board — Godot 4's tilemap, or Python/Pygame over Tiled data — and in what
> tile interchange format is a map authored?**

It is **not** #309's engine question, and this record does not reopen it.
[`docs/design/ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md`](../../docs/design/ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md)
recommends a Python-authoritative runtime with a browser view next and Godot as a *view*; row **D13**
of the decision queue carries that pick. This spike answers the narrower question #515 asks, and it is
deliberately built so that either answer remains available: the mission layer is renderer-independent
(§11), so choosing Godot later does not require rewriting it, and choosing Pygame later does not
require rewriting the map data.

## 2. The criteria that actually bind here

### 2.1 The repository's five existing tests (T1–T5)

These are already land and are **hard requirements**, not preferences: `VISION.md` §7a (offline,
no account, no service, nothing proprietary), §7b (*no engine work; 2D or text-readable overhead map
only*), §8, and `INTERFACE_SPIKE.md`'s criteria for anything that renders.

| Test | Restated for a tactical map |
| --- | --- |
| **T1** | Runs from source, offline, without an account and without a service |
| **T2** | No proprietary engine, no live service, no paid provider |
| **T3** | **No rule written twice in two languages** — a renderer is a *view* over the Python engine's recorded results, and no rule lives in a scene script |
| **T4** | The presentation ceiling it reaches inside §7b's *2D map only, no art production* cap |
| **T5** | The packaging, platform and provenance cost it adds to an offline, buildable-from-source release |

### 2.2 The tactical-map criteria #515 adds

| Test | What it asks |
| --- | --- |
| **R** — rules and state reuse | Does the candidate consume the **existing** Python kernel (`rpg/`, `campaign/`) in-process, or does it force a port, a copy or a bridge? |
| **I** — iteration speed | How fast can one mission, one interaction or one pathfinding rule be changed and seen? |
| **P** — tile and pathfinding support | Tilesets, layers, grid navigation, and a pathfinder that respects walls and doors |
| **H** — headless testability | Can the mission layer be tested by `unittest` in this repository's CI, with no window, no editor and no engine binary? |
| **A** — 8-bit art pipeline | Small sprites, a simple tileset, sparse animation; clarity over art |

**R, H and T3 are the same requirement seen from three sides**, and they are the ones that decide this
comparison. Everything else is cost.

## 3. The options

| Option | What it is |
| --- | --- |
| **A. Python + Pygame, Tiled as the editor** | A small renderer drawing the mission's grid to a window; Python remains the only rules implementation; Tiled authors the tileset and (later) the map |
| **B. Godot 4 tilemap as a view over the Python engine** | Godot renders; the Python session stays authoritative; the two talk over a structured interface |
| **C. Godot with the rules in GDScript** | The rules are reimplemented (or forked) in the engine's language |
| **D. Tiled alone** | Not a renderer: an editor and a data format that both A and B consume (§7) |

### 3.1 Comparison

| Criterion | A. Python + Pygame | B. Godot as a view | C. Godot, rules in GDScript |
| --- | --- | --- | --- |
| **T1** offline from source | Pass; `pip install pygame` is an ordinary dependency (a wheel), the same position `requirements.txt` already takes | Pass with a documented export/build path; the engine is a build tool, not a service | Pass |
| **T2** nothing proprietary | Pass (Pygame is LGPL-2.1; dynamic use plus notices is the normal path — the project's own licence is row **D10** and is untouched either way) | Pass (Godot is MIT; already recorded in `INTERFACE_SPIKE.md`) | Pass |
| **T3** no rule written twice | **Pass by construction** — one process, one rules implementation, no second language | **Pass only if the bridge is disciplined**; every "just this animation" is a place a rule can be re-derived in GDScript | **FAIL** — the second ruleset #515 explicitly forbids |
| **R** rules/state reuse | **Direct import**: `rpg.skills.check`, `rpg.roster.TurnLedger`, `rpg.scene.apply_hit`, `campaign.apply_mission_outcome` | Same Python kernel, but across a process boundary: the view must ship state out and requests in | A port of the Fate kernel, the two skill layers, stress/consequences and the campaign books |
| **I** iteration speed | One language, one test runner, `python -m strategy_game.tactical`; a renderer change is a file save | Engine start, scene reload, and a bridge protocol to keep in step for every state change | Two languages to change for one rule |
| **P** tiles/pathfinding | **None built in**: tiles are blits against a tileset, pathfinding is ours (already written and tested, §9) | **Strongest**: `TileSet`/`TileMapLayer`, terrain autotiling, `AStarGrid2D`, navigation layers, an editor | Same as B |
| **H** headless testability | **Pass**: the mission layer imports no renderer at all, so 95 tests run in ~2 s under `unittest` in the existing CI; a renderer smoke test can use SDL's dummy video driver | **Partial**: Godot's `--headless` runs the engine, but GDScript logic needs GUT/gdUnit4 *and* a Godot binary in CI — a toolchain this repository does not have (`.github/workflows/python-scaffold.yml` is Python-only) | Same toolchain cost, plus the tests would be testing a copy of the rules |
| **A** 8-bit art | Fine: a PNG tileset and `blit`; every 8-bit tileset in existence is consumable | Fine, and better tooling: atlas import, animation frames, a tile editor | Fine |
| **T4** ceiling | 2D pixel map, icons, panels — inside §7b | Higher ceiling than §7b allows today, which is a *scope* risk rather than a benefit | Same |
| **T5** packaging | PyInstaller/Nuitka per platform, plus SDL; moderate | Export templates per platform; the heaviest of the three, and a scene/asset provenance surface | Heaviest, plus a duplicated rules implementation to keep in parity |

**Finding.** A and B both pass T1, T2 and T4. They separate on **T3/R/H**: A keeps the rules in one
language and in one process by construction, while B keeps them in one language but across a seam that
must be *maintained*; C fails T3 outright and is therefore not a candidate at all.

### 3.2 Why C is disqualified rather than merely expensive

`AGENTS.md` §0 keeps the legacy RPG and the crossover apart, §3 makes the rules/worldbook the canonical
source and requires that *"game logic should therefore remain data-driven and engine-independent where
practical"*, and §13 makes a rules difference between runtimes a **defect**. #515 says the same thing
in its own words: *"Reuse NoöPunk's existing Fate-inspired stats, tags, actions, wounds and mission
consequences wherever feasible; avoid inventing a second full ruleset."*

The repository has already paid for this lesson once: `src/godot/core_rules.gd` is a GDScript adapter
that re-implements the **legacy** 1d10 core so the Godot scaffold can read `data/rules/core.json`. It
reads its numbers from data, which is the right instinct, but it is still a second implementation of a
resolution procedure in a second language — and it is legacy-RPG scaffolding, not the crossover's Fate
kernel. Adding a *third* rules implementation for the tactical layer is the failure mode this test
exists to catch.

## 4. Option A in detail — Python/Pygame, Tiled as the editor

**What the renderer would be.** Perhaps 400–800 lines: load the tileset, blit the grid from the
mission's `rows`, blit four agent sprites at their cells, draw a selection ring, translate a click into
`session.request_move(...)`, and render the returned `MoveResult.reason` when a move is refused. It
reads `session.report()`; it computes nothing.

**Where it wins.** R, T3 and H, decisively and permanently: there is no seam at which a rule can drift
into the view, because the view is in the same process as the rules and has no reason to duplicate
them. Iteration is one language. The mission layer's 95 tests already exist and already run headless.

**What it costs, stated plainly.** Pygame supplies **no tilemap, no tile editor, no pathfinding, no
scene graph and no export pipeline**. Every one of those is either ours (the pathfinder already is,
§9), Tiled's (authoring), or a packaging chore (PyInstaller per platform, T5). A Pygame tactical map is
a *renderer you own*, not a framework you adopt — which is exactly right for a board this small and
exactly wrong if the map grows into an editor-driven content pipeline with dozens of levels.

## 5. Option B in detail — Godot 4 tilemap as a view

**What it would be.** The mission JSON stays authoritative. A Godot scene loads the tileset, builds a
`TileMapLayer` from the mission's `rows`, and asks Python for state: either a short-lived
`python -m strategy_game.tactical --json`-style exchange per turn, or a long-lived subprocess speaking
a documented line-oriented JSON protocol. Requests (select, move, interact, end turn) go in; recorded
results come out. **No rule in GDScript.**

**Where it wins.** P and A: Godot's tile editor, terrain autotiling and `AStarGrid2D` are better than
anything this repository would hand-roll, and the engine also gives camera, input, animation and
self-contained exports for free. If the tactical layer becomes the *product's* main surface, with
authored maps and a level designer, Godot is the better long-term home.

**What it costs.** T3 becomes a discipline instead of a structure — the bridge must be the only path
into state, and every GDScript convenience is a chance to re-derive a rule. H gets worse: the mission
layer's tests stay in Python (good), but anything expressed in the scene cannot be tested without a
Godot binary in CI, which this repository does not have. T5 is the highest of the live options: export
templates, scene and asset provenance, a heavier repository. And an extra moving part exists in every
play session: two processes that must agree about a turn.

## 6. What is *not* on the table

- **A second rules engine** (C) — see §3.2.
- **A required service**: a hosted map server, a managed backend, or a browser canvas served by a
  Python process. `VISION.md` §7a line 7 excludes it by name and
  `ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md` already disqualified the family.
- **A proprietary engine or paid toolkit.**
- **3D, isometric or a cinematic pipeline** — #515 asks for the opposite.
- **An engine installed or vendored by this PR.** No engine is added; nothing in
  `requirements.txt` changes.

## 7. Tiled is an editor, not a renderer

Tiled deserves a separate line because it is easy to mistake for an option. It **authors** tilesets and
maps and writes TMX/JSON; it draws nothing at play time and decides nothing. That makes it *compatible
with both* live options, and it changes the recommendation only in the tile-interchange column (§9).

Two honest notes: the Tiled editor is GPL-2.0, but a map file is data, not a derivative work of the
editor, and no Tiled code needs to ship — the mission loader reads JSON directly, so `libtiled` is not
a dependency. And Tiled's own JSON format would be an *authored-map* format for a level designer; the
spike's ASCII rows are the smaller thing that is enough today.

## 8. Recommendation — a proposal, not a decision

> **Recommended: Option A — Python/Pygame rendering the mission layer in-process, with Tiled as the
> map editor when authored maps are needed. Keep Godot as a documented view option (Option B), not as
> the tactical layer's runtime.**

The trade-off this buys, stated in one sentence: **you give up Godot's tile editor, built-in grid
pathfinding and self-contained exports, and you take on a small renderer you own plus per-platform
Python packaging — in exchange for a tactical layer that cannot fork the rules, that is testable
headlessly in the CI this repository already runs, and that survives the author choosing a different
renderer later.**

Why that trade is the right way round *for this project, now*:

1. **The binding constraint is T3, and only A satisfies it structurally.** #515 says "reuse … avoid
   inventing a second full ruleset"; the cheapest way to guarantee that is to have nowhere to put a
   second one.
2. **The expensive part of a tactical map is the part already built.** Movement, interactions,
   objectives, outcome → persistent state and the schema are renderer-agnostic and done (§10–§11).
   What remains for A is drawing, which is the small part.
3. **H is not a preference here, it is the repository's test policy.** `AGENTS.md` requires executable
   tests for executable code; a Godot-expressed mission layer would need a toolchain the CI does not
   have.
4. **It does not foreclose Godot.** Because the mission layer exposes plain JSON state, B remains a
   renderer swap rather than a rewrite — and that is precisely what the author may prefer if the
   tactical board becomes the product's main surface.

**This is a recommendation with a named cost, not a ruling.** The author's answer is row D29.

## 9. Grid and tile format

**Chosen for the spike, and recommended for the schema regardless of renderer:**

```
"grid": {
  "width": 20, "height": 20,
  "legend": {".": "floor", "#": "wall", "+": "door"},
  "rows": ["####################", "#..................#", ...],
  "closed_doors": [[6, 10]]        // optional; omitted when every door is open
}
```

- **One glyph per cell, one string per row.** A 20x20 map is 20 lines of 20 characters — readable in a
  diff, editable without a tool, and trivially a Tiled layer, a Godot `TileSet` layer or a Pygame blit
  loop. The `legend` is declared rather than implied, so a project can add glyphs without the loader
  guessing.
- **Doors are a tile kind, and shut doors are declared state.** Pathfinding respects `closed_doors`;
  nothing in the prototype opens one, because *what opening a door costs* is a rules decision (§12).
- **Pathfinding is four-neighbour BFS with a fixed neighbour order**, so a path is shortest and
  reproducible; refusals name the cause (*wall*, *closed door*, *outside the grid*, *no route*).
- **If Tiled is adopted** (row D29), the production interchange for *authored* maps is Tiled's JSON
  (`.tmj`) with the same three tile classes mapped in a tileset; the ASCII form stays the test fixture
  format and the smallest way to write a map by hand.
- **If Godot is adopted**, the same JSON becomes a `TileSet` + `TileMapLayer` at load time; the mission
  file does not become a scene file.

## 10. The mission-data schema

One JSON object per mission, `format: noopunk.tactical.mission`, `schema_version: tactical-mission-1`.
Full definition: `strategy_game/tactical/mission.py`; worked example:
`strategy_game/data/tactical/spike_mission.json`.

| Field | Meaning |
| --- | --- |
| `mission_id`, `case_id`, `title` | Identity. `case_id` binds the campaign's `Case`, which is where evidence lands |
| `status` | `SPIKE_FIXTURE` for the packaged example — so a fixture is never read as canon |
| `note` | Free text for a human; no rule reads it |
| `grid` | The map, §9 |
| `deploy_cells` | **Exactly four** cells, bound to the faction's four **agent seats in seat order** (#461/#482). The leader chairs the faction and does not deploy |
| `interactions[]` | `id`, `kind` (`dialogue` / `clue` / `confrontation`), `at`, `label`, `text`, optional `action`/`skill`/`difficulty`, `requires`, `evidence`, `intel`, `objectives`, `optional`, `consequence` |
| `objectives[]` | `id`, `label` (what reaches `faction.objectives`), `required` |

**Why it is renderer-independent.** It says what is *true on the board* and nothing about how the board
looks or how the world works:

- **No presentation fields exist, and the loader refuses them.** Unknown keys are a defect at the
  document and interaction level, so a `sprite`, `tile_id`, `pixel`, `colour`, `layer`, `camera` or
  `animation` field cannot be smuggled in later "just for the view". Tests assert both the refusal and
  a recursive scan of the serialized document.
- **No rendering library is imported.** `strategy_game/tactical/` imports the standard library and
  `strategy_game` only; a test parses every module's imports and a second test imports the package in a
  subprocess with `site` disabled.
- **It resolves nothing itself.** A mission names a Fate action and one of the six **individual**
  skills; the check runs through `rpg.skills.check` in `ActionContext.INDIVIDUAL`, and the skill name is
  validated at load time, so a strategic skill or an invented attribute is refused by name.
- **It carries no second ruleset.** No damage, movement cost, line of sight, cover, stealth,
  initiative, enemy or PSI field exists (§12).
- **State comes back as plain JSON.** `MissionSession.report()` is the whole interface a renderer needs:
  seats, cells, resolved hooks, objective state, evidence, intel, wounds. `request_move` and `interact`
  take a seat id and a cell or a hook id, and return a result or a legible refusal.

## 11. What the prototype proves (and how)

`strategy_game/tactical/` — `grid.py`, `mission.py`, `session.py`, `demo.py`, `__main__.py` — plus the
fixture `data/tactical/spike_mission.json`.

**Reuse, by identity rather than by imitation.** The session builds its seats from
`rpg.roster.default_seats` and filters to the four **agent** seats; its turn structure *is*
`rpg.roster.TurnLedger`, and a second move in one turn is refused with the ledger's own wording. A
check is `rpg.skills.check`. A failed confrontation applies `rpg.scene.apply_hit` (stress box + mild
consequence), so the wound is on the sheet `save_campaign` writes. The mission's outcome is a
`campaign.MissionOutcome` written by `campaign.apply_mission_outcome`, the one tested writer of faction
books.

**What the fixture mission exercises.** A 20x20 map with walls and two doors, four agents, a walk that
must route through the annex door, a check-free dialogue, a clue behind the interview prerequisite, an
optional confrontation that wounds on failure, two required objectives, and completion that writes
objectives, intel, case evidence and an audit note into the campaign.

**Evidence at the time of writing** (measured, not estimated):

- new tests: **95** across `test_tactical_grid.py` (26), `test_tactical_mission.py` (31) and
  `test_tactical_session.py` (38);
- `strategy_game` suite: **1460 tests, OK** (1365 before this change); root suite: **585 tests, OK**;
- `ruff check` clean on every file this change touches;
- `python -m strategy_game.tactical` plays the fixture mission headless and prints the state it wrote.

## 12. What this milestone deliberately does not do

- **No rendering, no art, no tileset, no sprite.** Nothing is drawn.
- **No engine choice, no engine installed, no rendering dependency added.**
- **No enemy, combat round, line of sight, cover, stealth, PSI or hacking.** #515's later milestones.
- **No movement cost.** One move is one action regardless of length; pricing a step is an author
  decision.
- **No door-opening action.** A shut door blocks; what opening one costs is undecided.
- **No occupancy rule beyond the destination.** Routes may pass through allies; two agents may not end
  on one cell. Stated as a spike convention, not a rule.
- **No tie rule.** A Fate tie grants nothing and wounds nobody; "succeed at a minor cost" is an author
  decision (the same open question as row D27 for projects).
- **No mission-outcome aggregation.** The report carries the `Outcome` of the check that completed the
  last required objective; a mission with no decisive check refuses to complete rather than inventing a
  summary rule.
- **No canon.** The fixture's names, place and ids are prefixed `spike`/`Fixture` and marked
  `SPIKE_FIXTURE`; #515 stays open, and nothing here says the tactical map exists in the game.

## 13. What would change the recommendation

Falsifiers, so this does not become folklore:

1. **The tactical board becomes the product's main surface**, with authored multi-level maps and a
   designer workflow → Godot's editor and export pipeline outweigh the bridge cost; revisit D29.
2. **PyInstaller-class packaging proves unacceptable** for the intended platforms (consoles, mobile,
   storefront requirements under D14) → Godot's exports become the cheaper distribution path.
3. **Python-for-Godot embedding turns out to be reliable and maintained** for the engine version in use
   → Option B's bridge becomes cheap enough that T3 is a code-review question rather than an
   architecture one. This would need verification before it could be planned on.
4. **The mission layer grows a mechanic the engine must evaluate at frame rate** (continuous movement,
   physics, real-time stealth cones) → a Python-per-turn loop stops being sufficient, whichever
   renderer is chosen.

— Ai (愛), issue #515 technical spike
