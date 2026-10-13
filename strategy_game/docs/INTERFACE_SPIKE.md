# Interface spike: what draws the board

**Status: a spike record and a working text view. It decides tooling, not rules.** Nothing here
approves a mechanic, and Gates A–D in `docs/RULE_SYSTEM_RESEARCH.md` stay open. The choice of
renderer is a decision record; the *game's* tooling for the shipped indie release stays the
author's call.

Issue #347 asked for "a renderer / interface shell" and recorded that nothing currently draws the
board. This spike answers that with a working view, and states the criteria that bind any renderer
that follows.

## The criteria (binding, from the issue, `VISION.md` §7a and the plan on the issue)

1. Buildable and runnable from source: **offline, no account, no service.**
2. **No proprietary engine.** Godot is MIT, so reusing the legacy scaffold passes; a paid engine
   would not.
3. **No rule written twice.** If Godot renders, it is a *view*: the Python engine stays
   authoritative and the UI animates the engine's recorded result. No rule belongs in a scene script.
4. **No model provider in the default import graph.** Switching the model off must leave a complete
   game.
5. A renderer consumes declared state through the reserved **`MapProvider`** seam and **infers no
   borders, travel, control or ownership** (the port's own docstring).
6. The pinned display projections are not widened: `view.board_view`'s five keys are asserted by
   tests and a CI smoke step, and `strategy_game/__init__.py`'s `__all__` by its own tests.

## Options assessed

| Option | Verdict |
| --- | --- |
| **A. Standard-library text/terminal view** | **Chosen now.** Zero dependencies, deterministic, testable, and it draws the only complete local content today. |
| **B. Browser/HTML view over the same payload** | **Next step.** The provider already emits a portable payload (`--json`), so a second renderer needs no engine change and no new rule. |
| **C. The legacy Godot scaffold as a pure view** | **Preserved as an option** (`AGENTS.md` §3: do not delete). Legitimate under criteria 2 and 3 — as a *view* only. |
| D. A web framework / game engine / hosted server | Rejected: adds a runtime dependency and a service, breaking criterion 1. Nothing the MVP needs requires one. |

## What was built (evidence, not a plan)

`strategy_game/render/` — its own subpackage with its own `__init__` and `__main__`, exactly as
`tabletop/` did, so neither pinned entry point is widened.

- `TextMapProvider.describe(state)` fills the reserved `MapProvider` seam and returns the board
  projection plus a renderer version. Its payload adds **no** inferred key.
- `render_board_text(state)` — the board as deterministic text.
- `render_roster_text(roster)` — card faces, reusing the character-card layer's front renderer,
  which never prints `gm_notes`.
- `state_from_local_slice()` — a **view adapter** for `data/ukweli_local.json`: locations, parties
  and leaders copied as declared, each route pair becoming an unlabelled-layer edge. No transition,
  no turn, no rule.
- `python -m strategy_game.render [--world FILE | --empty] [--cards] [--json]`.

Measured output on the local slice:

```
board [scaffold-1] — 8 locations, 3 nodes, 7 routes, 0 assets, 12 leaders
locations: Old Harbor, Civic and Commercial Centre, Mixed Neighborhoods, University and Hospital,
           Industrial Logistics Port, Outer Island Communities, Airfield Island, Coastal Hinterland
routes (declared edges; direction, meaning and control are not implied): 7
cards [render-text-1] — 17 in the roster
```

**Tests:** 14 in `tests/test_render_text.py`, all executable-code assertions per #271:
determinism; every location and route rendered; the empty state says so; the adapter copies
declared content only; no forbidden inference key anywhere in the payload; the pinned board key set
is unchanged; card faces never print GM notes; the CLI runs; **and a §7a guard that imports every
crossover module in a subprocess whose `sys.path` carries no third-party distributions** — so
"runnable from source, offline" is protected by a test rather than by intention.

Suite state at the time of writing: `strategy_game` tests **450 OK**, root tests **509 OK**,
`python -m strategy_game` view-model smoke OK.

## Recommendation

**Text-first now, browser next, Godot as a view if the author wants it.** The reasons are the
criteria, not taste: the text view has no dependency to break criterion 1, cannot contain a rule
because it only formats declared state, and is deterministic enough to test. Because the provider
already emits a portable payload, option B is an additive renderer rather than a second engine —
and option C remains available precisely because the engine is authoritative and the UI would only
animate recorded results.

## What this does not decide

- No rule, threshold, resolution, cadence or effect. Gates A–D untouched.
- Not the shipped game's tooling: that is the author's decision, and this spike gives them a
  working reference and a payload contract to judge it against.
- No canon, no lore, no numeric design.

## Suggested next small steps (each independently landable)

1. A browser/HTML renderer over the same `describe()` payload.
2. Board **positions** as declared data, kept apart from topology (the `tabletop` layer already
   separates `Layout` from the graph, so this is data, not a rule).
3. The RPG scene — behind Gate A, and therefore not before the author rules.
