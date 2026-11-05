# The graphical client — a plan for Python, minimal and graph-first (#1184)

> **Status: implementation plan, not implementation.** Companion to
> [`ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md`](ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md). The GUI is
> **optional**: the tabletop sheet, the text CLI and the Evennia client stay first-class, and the game
> must be completable without a single pixel.
>
> **Visual basis:** [`docs/art/ART_BIBLE_1974.md`](../art/ART_BIBLE_1974.md),
> [`docs/art/design_tokens.json`](../art/design_tokens.json), and the older
> [`ISSUE_447_RETRO_UI_PROTOTYPE.html`](ISSUE_447_RETRO_UI_PROTOTYPE.html) — which is the look this plan
> makes buildable in Python.

## 1. What the client is

A **retro-minimal, text-heavy, graph-first window onto the same world state** the CLI reads. Lots of
reading, small amount of moving picture. The graphics exist to make **structure** visible — who is where,
what links to what, what you have proved — not to render a world in 3D.

Three reference points, each contributing one thing:

| Touchstone | What we take | What we do **not** take |
| --- | --- | --- |
| **Citizen Sleeper** | Static illustrated panels, a text column, a visible cycle/pressure rhythm, restrained animation | Its dice-allocation economy (NoöPunk has CWN) |
| **Hacknet** | Node-link maps, terminals as objects, traces with timers | Its bespoke intrusion mechanics (CWN hacking already exists) |
| **Cyber Manhunt** | Investigation board: evidence pins, string links, contradictions made visible | Its puzzle minigames and point economy |
| **hackmud** | A command-driven terminal that feels like an in-world tool: OSINT, messages, logs and intrusion as things you *type at*, with no chrome around them | Its multiplayer structure and its own command grammar — NoöPunk's commands are the CLI's, resolved by CWN |

**The text interface comes first, not last.** Following *hackmud* (README, #1184), the terminal is a
diegetic in-world tool rather than a fallback for players without a GPU: the same command vocabulary
drives the GUI's command line, the text CLI and the Evennia client, so a player who prefers the
terminal loses no content and gains no advantage. The window is the illustrated form of the same
verb set.

**One rule above all:** the client renders **player-known** state. A node the character has not
discovered is not drawn greyed-out — it is not there. "Greyed out" leaks the shape of the answer.

## 2. The look

**Retrofuturist 1974, not glossy cyberpunk.** Hawkwind concert, VALIS transmission, Zardoz and
Barbarella rather than neon-and-rain. Aesthetic constraints that keep it cheap and coherent:

* **Internal resolution 384×216**, integer-scaled ×3 or ×4 to the window. Everything is drawn at that
  resolution; the OS does the scaling. No sub-pixel text, no font smoothing.
* **Palette of six to eight colours**, defined once in `theme.py` from the design tokens: bone paper,
  amber phosphor, dim green CRT, ink, rust, one saturated accent (magenta) reserved for
  *anomalous/psychic* content — if magenta is on screen, something is wrong with the world.
* **Two bitmap fonts:** a narrow 5×7 for UI, a wider 8×12 for prose. Both monospace-ish, both bundled
  as licence-clean bitmaps (or generated from a permissive source).
* **Dithering instead of gradients.** A 2×2 ordered pattern gives depth without alpha blending.
* **Motion is frugal:** a blinking cursor, a two-frame flicker on anomalous nodes, a slow scanline pass
  over the graph panel. Nothing bounces.
* **Sound (later):** one ambient loop per screen, three or four UI clicks, no music stings.

## 3. Technology: Pygame-ce, behind the existing boundary

**Choice: `pygame-ce`** (community edition), with `numpy` for surface work and **NetworkX** for layouts.
Python 3.11, the same interpreter as the rest of the stack.

Why Pygame-ce rather than the alternatives:

| Option | Verdict |
| --- | --- |
| **pygame-ce** | Mature, bitmap-native, trivially matches a 384×216 pixel canvas, ships wheels for Linux/Windows/macOS, no GPU assumptions. **Chosen.** |
| Arcade / pyglet | Nicer text and OpenGL, but pulls in a heavier rendering model than a pixel canvas needs, and its strengths (sprites, shaders) are things this UI deliberately avoids. |
| Textual / Rich (TUI) | Excellent for the terminal client we already have — not a graphical client. Keep it as the CLI, not as the answer here. |
| Godot | Already demoted to maintenance (#950); a second engine for a UI would fork the project's attention. |
| Tkinter / Qt | Wrong idiom: a widget toolkit fights a drawn pixel canvas. |

**Packaging:** an optional extra (`pip install .[gui]`), so a headless server or the CLI install never
drags in a graphics stack. The domain layer must remain importable with `pygame` absent, and a test
asserts it (see §11).

## 4. Package layout

```
src/ui/
  app.py          # main loop, screen stack, input dispatch, fixed 60 Hz tick
  theme.py        # palette, fonts, spacing, from data/design tokens
  canvas.py       # 384×216 surface, integer scaling, dithering helpers, text runs
  graphview.py    # NetworkX -> layout -> screen coords, ego-graph focus, hit-testing
  textbox.py      # wrapping, typewriter reveal, scroll, paging
  screens/
    board.py      # investigation board (hub)
    place.py      # physical location
    cyber.py      # cyber graph + terminal pane
    dialogue.py   # portraits + text + evidence tray
    action.py     # arrest / pursuit / standoff
    dossier.py    # CWN character sheet as a card
  assets/         # glyphs, fonts, later commissioned art
```

**No rule lives here.** `app.py` builds an `Action` and hands it to the existing session
(`src/console/session.py` or `nopunk_mud.session`); the returned `ActionResult` is rendered. If the GUI
needs a fact, the result must carry it.

## 5. Drawing graphs with NetworkX

Almost everything is a graph, so graph rendering is the core craft, not a feature.

* **Layout.** `nx.spring_layout(..., seed=…)` on the *player-known subgraph only*, cached per (case,
  view, evidence-revision). Determinism matters: the board must not rearrange itself while the player is
  thinking. `kamada_kawai_layout` for small dense boards; `nx.multipartite_layout` for series/episode/
  scene chains; layered manual layout for the story graph.
* **Focus + context.** Draw the **ego-graph** of the selected node (radius 2), not the whole network.
  The rest is a single dimmed dot field. This is what keeps a 384×216 screen readable with 200 nodes.
* **Node glyphs are a taxonomy,** not decoration: person (dot), place (square), device (diamond), claim
  (small hollow ring), evidence (filled ring), hypothesis (dashed ring), unknown (question mark only if
  player-authored). Shape carries kind; colour carries state (known / contested / contradicted).
* **Edges:** solid = established, dotted = inferred, red = contradiction, arrowheads only where direction
  is meaningful. Width never encodes strength — that would imply a mechanic we do not have.
* **Labels** on hover/selection only; always-on labels are the fastest way to make a graph unreadable.
* **Interaction:** pan by drag, zoom by wheel with a single integer step, click to focus, `Tab` to cycle
  neighbours, keyboard-first throughout.
* **Performance budget:** rebuild layout only when the known-set changes; cache to disk keyed by revision;
  target 60 fps at 384×216 with ≤ 60 drawn nodes; the full graph is never drawn.

## 6. Screens

```
┌ BOARD ─────────────────────────────┐   ┌ PLACE ──────────────────────────────┐
│  ●────◆        ○                   │   │  Kurvi · stairwell B                │
│  │     │        ╲                  │   │  ─────────────────────────────────  │
│  ●     ●         ○───○             │   │  Exits: street ↑  roof ⨯  cellar ↓  │
│  evidence 3 · leads 2              │   │  [ look ] [ listen ] [ knock ]      │
└────────────────────────────────────┘   └─────────────────────────────────────┘
```

1. **Board** — the hub. Evidence graph + a running case log. Entering any other screen from here.
2. **Place** — room card: short prose, exits as keys, visible objects, who is present.
3. **Cyber** — split view: device graph above, terminal transcript below. Traversal and CWN hacking
   verbs; trace/timer drawn as a thin bar, never as a big red alarm.
4. **Dialogue** — portrait block (~64×64), text column, an **evidence tray** at the bottom for
   presenting documents. Contradiction states are shown as *the witness's claim struck through*, not as
   a "lie" meter.
5. **Action** — see §7.
6. **Dossier** — the CWN sheet as a card: attributes, skills, strain, gear, Tags, implants. Read-only in
   play except where the rules allow a change.
7. **Dream / astral** — a distinct visual register (magenta accent, inverted palette, no graph chrome):
   a scripted scene, deliberately unlike the rest of the interface so the player feels the difference.

## 7. The action screen (arrest, pursuit, standoff)

**No tactical grid.** Action scenes are rendered as **range bands and clocks**, per CWN's abstract
combat:

```
┌ ACTION — arrest, Kurvi stairwell ────────────────────────────┐
│  you ●        him ●        bystander ○        exit →          │
│  CLOSE ────── NEAR ────── FAR ────── GONE                     │
│                                                               │
│  time  ▮▮▮▯▯▯   (neighbours are filming)                      │
│  force  presence → verbal → physical → less-lethal → firearm  │
│  [ command ] [ close ] [ restrain ] [ call backup ] [ stop ]  │
└───────────────────────────────────────────────────────────────┘
```

* **Bands** (close/near/far/gone) replace distance measurement; movement is a decision, not a walk.
* **Clocks** carry pressure: response time, bystander attention, the suspect's patience, the supervisor's
  patience. A clock filling is a *consequence*, not a fail state.
* **The force ladder is always on screen**, with the current rung highlighted, so escalation is a
  deliberate act the player can see themselves choosing.
* **Pursuit** swaps the ladder for a route choice row (straight / cut through / stop and contain) and a
  vehicle-damage strip.
* **Legal consequence panel** after the scene: what was done, what was seen, what will be asked later.
  This is where *Hill Street Blues* lives — the paperwork is the epilogue.

## 8. Text, accessibility, language

* **Typewriter reveal** with an instant-complete key; a speed setting; a "no animation" mode.
* **Contrast and size:** two font sizes minimum, a high-contrast palette variant, and a
  colour-blind-safe mode in which the magenta accent is replaced by a shape marker.
* **Keyboard-first**, mouse optional; every action has a key.
* **Language:** player-visible text follows the Finglish policy (`docs/FINNISH.md`, #996) — English-led
  with contextual Finnish, never machine-translated Tomi-authored prose. UI chrome (buttons, labels)
  stays plain English; the *fiction* carries the Finnish.

## 9. Art pipeline

Start **procedural**: shapes, glyphs and dithering from `theme.py`, so no commissioned asset blocks a
build. Then a small, consistent set:

1. **Palette + fonts** (week 1) — from the art bible and tokens.
2. **Glyph sheet** — the node taxonomy above, 8×8 each; readable at 1× or 2×.
3. **Portrait frames** — 64×64, two-tone, one per recurring character; generated placeholders until art
   exists, and never a photograph.
4. **Commissioned art** — static panels in the Citizen Sleeper register: one per major location, one per
   act. Optional; the game must look intentional without them.

## 10. Milestones

| Milestone | Delivers | Acceptance |
| --- | --- | --- |
| **M0 — canvas** | `app.py`, `theme.py`, `canvas.py`; window opens at 384×216 scaled; text renders | Runs headless under SDL dummy; a screenshot test proves a known frame |
| **M1 — board** | Investigation board from a fixture case; ego-graph layout; keyboard navigation | Same case state renders identically twice (deterministic layout) |
| **M2 — place + dialogue** | Room cards, evidence tray, contradiction display | A scripted interview is completable mouse-free |
| **M3 — action** | Bands, clocks, force ladder, consequence panel | An arrest and a pursuit are playable, and both can end without injury |
| **M4 — polish** | Astral register, dossier card, accessibility modes | Full first case playable in the GUI and in the CLI from the same save |

## 11. Testing a graphical client without becoming a graphics project

* **Headless by default:** `SDL_VIDEODRIVER=dummy`; the app must construct and tick in CI.
* **Deterministic layouts:** layout seed derived from case id + revision; a test asserts two runs agree.
* **State snapshot tests:** the *state* after an action is compared, not the pixels — pixels are checked
  only for a handful of golden frames.
* **Boundary test:** importing `src.ui` without `pygame` installed must fail cleanly, and importing the
  domain layer must never import `src.ui`.
* **No rules in the client:** a test greps `src/ui` for rule modules; the import check already exists in
  spirit at `tests/test_engine_independence_1053.py`.

## 12. Risks, stated plainly

| Risk | Mitigation |
| --- | --- |
| Graph rendering becomes the project | Ego-graph + fixed glyph taxonomy + no free camera; M1 is the smallest thing that can be called a board |
| GUI drifts into a second rules engine | Actions go through the session API; a static check refuses rule imports in `src/ui` |
| Art becomes a dependency | Procedural first; commissioned art optional and never blocking |
| Text-heavy UI ages badly | Bitmap fonts at fixed sizes and integer scaling do not rot the way shaders do |
| Scope creep into a tactical game | Action scenes are bands and clocks; a grid is explicitly out of scope |
