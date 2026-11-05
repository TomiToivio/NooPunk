# The Python graphical interface — a graph-first, text-heavy plan (#1184)

> **Status: proposal for implementation, not yet built.** It adds an *optional* front end. The CWN
> core, the tabletop and the text CLI remain the requirement; this is the window.
>
> **Depends on:** [gameplay interfaces](GAMEPLAY_INTERFACES_1184.md) (what each screen is allowed to
> do), [four graph layers](FOUR_GRAPH_IMPLEMENTATION_1178.md) (`src/rules/four_graphs.py`),
> [the 1974 interface study](ISSUE_447_RETRO_UI_PROTOTYPE.html) (the palette this plan reuses).

## 1. The shape of the thing

**One window, one case, six apps.** The player is sitting at a Europol Helsinki workstation in 2045.
The interface is diegetic: a case board, a records terminal, a system console, an interview recorder,
a field notes pane, a report form. It is not a cockpit and not a HUD.

**Almost everything is a graph** — and the graphs are *the* interface, not decoration:

| App | Graph it shows | Player verb |
| --- | --- | --- |
| **CASE** | Investigation graph: evidence, claims, people, places, contradictions | Link, compare, hypothesise |
| **OSINT** | Records and media as a link graph of sources | Search, open, collect |
| **TERMINAL** | Cyber graph: services, access, devices | Move an avatar, breach |
| **INTERVIEW** | Social graph, but *filtered to what is proven* | Ask, present, confront |
| **FIELD** | Physical graph: the location the scene is in | Move, search, act |
| **REPORT** | Story graph: what the case still needs | File, close, lie by omission |

**Reference points, precisely.** *Citizen Sleeper*: a static illustration, a wall of text, a small set
of consequential choices, no animation. *Hacknet*: a terminal where typing is the interface and the
network is a map you learn by traversing. *Cyber Manhunt*: a fake desktop where each window is an
investigative tool, and evidence is assembled by cross-referencing windows. Take the *layout
discipline* of all three, the *text density* of the first, and none of their mechanics.

**What it must feel like:** a 1974 terminal that someone bolted a case board next to. Slow, legible,
amber on near-black, with the sound of a keyboard and nothing else.

## 2. Stack, and why

| Concern | Choice | Reason |
| --- | --- | --- |
| Windowing / drawing | **`pygame-ce` 2.5+** | Mature, minimal, integer scaling, no scene graph to fight; the repo already contemplates pygame in the text-game path |
| Graph layout | **`networkx` 3.x** | `four_graphs.networkx_view()` already derives a `MultiDiGraph`; layouts are the only thing we need beyond it |
| Text shaping | pygame's `Font` with a bundled OFL pixel face | Licence-clean, crisp at integer scale, no system font dependency |
| Persistence | JSON snapshots (existing) | The GUI reads a snapshot; it never owns state |
| Packaging | **optional extra**, not a core dependency | `pyproject.toml` keeps `dependencies = []`; add `gui = ["pygame-ce>=2.5", "networkx>=3"]` and a `noopunk-gui` script |

**Hard rule:** `import pygame` and `import networkx` live only under `src/gui/`. Core rules, the CLI
and the tabletop library must keep importing neither — there is already a test that guards engine
independence, and this plan does not weaken it.

## 3. Layout logic: the screen is three columns

```
┌─────────────────────────────────────────────────────────────────────┐
│ NOÖPUNK // EUROPOL HELSINKI      CASE 2045-0417     04:12  ▮▮▯▯      │  status strip (1 line)
├───────────────────────────┬─────────────────────────────────────────┤
│                           │                                         │
│  TEXT COLUMN              │   GRAPH PANEL                           │
│  (dialogue, document,     │   (case board / cyber map / location)   │
│   terminal output)        │                                         │
│  ~44 % width              │   ~56 % width, always a graph           │
│                           │                                         │
├───────────────────────────┴─────────────────────────────────────────┤
│ > command line / action bar (typed, and mirrored as buttons)         │
└─────────────────────────────────────────────────────────────────────┘
```

- **Internal resolution 1280×720**, integer-scaled to the window. One pixel grid, no subpixel text.
- **Text column** is the primary surface: 60–72 characters per line, monospace, 15–18 px at 1×.
  Documents are paginated, never scrolled arbitrarily; every page is numbered as a document would be.
- **Graph panel** never competes for text: node labels appear only for the selected/hovered node, and
  a side legend carries the register colours.
- **Command line is the floor.** Every action is a typed verb with an alias button. Typed-first means
  parity with the CLI is structural rather than aspirational, and it gives keyboard-only play for
  free.

## 4. The visual language (reusing #447's palette)

| Role | Colour | Reuse |
| --- | --- | --- |
| Background | `#201d31` | existing study |
| Panel | `#302b43` | existing study |
| Ink / body text | `#f9e9bd` | existing study |
| **Observed** (evidence, verified) | `#9dd9bc` mint | existing study — *this is the important one* |
| **Inferred** (claim, hypothesis) | `#f6a55b` orange | existing study |
| **Fictional / disputed** (rumour, Mandela-effect material) | `#b29be7` violet | existing study |
| Terminal screen | `#101e22` on `#bcf4ca` | existing study |
| Alert | one additional red, used *only* for harm and warrants | new, sparingly |

**Graph semantics ride on this palette**, which is the whole point:

| Element | Encoding |
| --- | --- |
| Node shape | kind: circle = person, square = place/device, diamond = document, triangle = claim |
| Node fill | register: mint = verified, orange = claimed, violet = disputed, hollow = hypothesis |
| Edge line | solid = established, dashed = asserted by one source, dotted = the player's guess |
| Edge width | 1 px, always; hierarchy comes from layout, never from thickness |
| Hidden nodes | **not drawn at all** — the map is knowledge, not truth |

**Motion budget:** a 2-frame blink for the cursor, a 120 ms fade when a node is discovered, nothing
else. No parallax, no particles, no tweened cameras. If an effect does not carry information, it is
cut — that is the "minimalist retro indie" discipline, and it is also the performance budget.

**One illustration per location, not per scene.** A 320×180 hand-authored 1-bit dither panel in the
FIELD app, in the spirit of *Citizen Sleeper*'s static art, reused across scenes. Ten good panels beat
a hundred procedural ones.

## 5. Graph rendering that survives a real case

`networkx` layout is O(n²)-ish and unstable across runs; treat it as an offline step with a cache.

1. **Layout once, per graph version.** `spring_layout(seed=…)` or `kamada_kawai_layout`, computed when
   the snapshot changes, saved beside it (`<snapshot>.layout.json`), keyed by `graph.version`.
2. **Incremental reveal.** Discovery never re-lays-out the board. A new node is placed in the free
   sector radially nearest its strongest known neighbour, and the previous positions are kept —
   so the player's mental map stays valid, which is the entire point of a case board.
3. **Positions are the player's.** Let the player drag nodes and persist the arrangement in the save;
   nothing destroys orientation faster than a board that rearranges itself.
4. **Budget:** 200 nodes / 400 edges on screen at 60 fps in pure pygame is comfortable if each frame
   only blits cached text surfaces. Beyond that, cluster by district and expand on click.
5. **Determinism for tests:** layouts are fixtures, not live computation, in CI.

## 6. Module plan

```
src/gui/
  __init__.py          # the only place that imports pygame
  app.py               # main loop, fixed timestep, screen stack, quit/scale handling
  theme.py             # palette, fonts, metrics — one file, no magic numbers elsewhere
  text.py              # wrapping, pagination, typewriter reveal, cached surfaces
  graph_view.py        # NetworkX -> screen; pan/zoom, hit-testing, reveal animation
  widgets.py           # panel, button, list, command line, legend (~400 lines total)
  screens/
    case.py            # investigation board (the default screen)
    osint.py           # records/search
    terminal.py        # cyber graph + typed commands
    interview.py       # dialogue with evidence chips
    field.py           # location + illustration + actions
    report.py          # story graph, case closure
  viewmodels.py        # snapshot -> plain data the screens draw (no pygame types)
  headless.py          # screenshot harness for tests
```

**The boundary that keeps this cheap:** `viewmodels.py` converts an authoritative snapshot into
plain dicts (`{"title": …, "lines": […], "nodes": […], "edges": […]}`, all colours resolved to
register *names*). Screens draw view models. Tests assert view models. Rendering bugs become layout
bugs, not logic bugs — and none of it can touch game state.

## 7. Actions, and the one resolver

Every player action from any app becomes a `Command` — the same vocabulary the CLI uses — and goes to
the existing Python library. The GUI never rolls dice, never compares a skill, never decides an
outcome.

```python
# illustrative, not implemented
cmd = Command(verb="present", actor="pc", target="evidence.tram_ticket", context="interview:driver")
result = session.dispatch(cmd)          # existing library; CWN resolution happens here
view = viewmodel.from_result(snapshot, result)   # plain data
app.push(view)
```

**Action scenes in this interface.** No grid, no initiative strip:

- **Arrest** = a short list of CWN-resolvable choices in the text column (approach, identify, restrain,
  wait for backup) with the graph showing who is where, and cover as fiction.
- **Pursuit** = the physical graph redrawn as a chase: nodes are corners and yards, the edge the
  quarry took is highlighted, and a small lead counter is the only "HUD" element in the game.
- **Containment** = the graph with a cordon drawn as a closed line around a subset of nodes; doors
  become gates the player must argue about.

This is where the Finnish tone lives: an arrest is a procedure with failure modes, and the interface
makes procedure legible instead of making violence fun.

## 8. Milestones (each one shippable)

| # | Deliverable | Done when |
| --- | --- | --- |
| **M0** | Window, theme, text column, command line, one static case board from a fixture snapshot | Runs at 1280×720, 60 fps, no pygame import outside `src/gui` |
| **M1** | CASE app: reveal-on-discovery, drag, persist layout, register legend | A player can solve the tutorial case's link puzzle |
| **M2** | OSINT + INTERVIEW apps with evidence chips and the present/contradict verb | Interview scene playable end to end with CWN Talk checks |
| **M3** | FIELD app: location graph, illustration panel, arrest and search actions | The rookie case's physical act is playable |
| **M4** | TERMINAL app: cyber graph, avatar movement, CWN hacking | The case's limited hack is playable |
| **M5** | REPORT app + case closure; save/load; CLI parity check | The #1184 rookie case is finishable three ways: GUI, CLI, table |
| **M6** | Polish: typewriter pacing, scanline toggle, reduced-motion, colour-blind audit | Accessibility checklist passes |

**Explicitly deferred:** animated sprites, 3D, tactical maps, procedural art, voice, music, and any
minigame.

## 9. Testing and CI

- **`tests/test_gui_viewmodels.py`** — pure logic, no pygame: snapshot → view model → assertions about
  registers, hidden nodes and ordering. This is where most coverage lives.
- **`tests/test_gui_headless.py`** — `SDL_VIDEODRIVER=dummy`, run each screen once, assert no exception
  and that the frame has non-background pixels; optional golden hashes for the layout, marked
  `xfail`-tolerant so font rendering changes do not block CI.
- **Parity test** — dispatch the same three commands through the CLI and the GUI view model, assert the
  same resulting snapshot. This is what stops the GUI becoming a second game.
- **Dependency test** — assert `pygame` and `networkx` are absent from core imports (the existing engine
  independence test, extended).

## 10. Risks, stated honestly

| Risk | Mitigation |
| --- | --- |
| The GUI quietly becomes a second rules engine | One dispatcher, one resolver, parity test in CI |
| NetworkX layout instability breaks the player's mental map | Layout cached per version, player drag persisted, incremental placement |
| Pixel fonts and Unicode (ПРОГРАММА, Finnish ä/ö, Cyrillic) | Choose a face with Latin-1 + Cyrillic coverage before M0; fallback to a second face |
| Palette fails colour-blind users | Register is also encoded by shape and dash pattern — never colour alone |
| Packaging drift: GUI deps leak into core | Optional extra + import test |
| Text becomes wallpaper | Pagination, per-document page counts, and a hard rule that no screen shows more than one screenful of new prose at a time |

## 11. What "minimalistic retro indie" means here, concretely

- One font, three sizes. One palette, six colours. One 1-px line weight.
- Every screen is a panel and a graph. No chrome, no shadows, no gradients.
- Text is the content; the graph is the *shape* of the content. Neither is decoration for the other.
- Nothing animates unless it tells the player something changed.
- If a scene can be played in the text CLI without loss, the GUI's job is to make it *easier to see*,
  not to make it different.
