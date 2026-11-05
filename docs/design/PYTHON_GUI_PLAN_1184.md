# Python graphical interface — plan (#1184)

> **Status: proposal for approval.** No dependency is added and no code is written by this document
> beyond the sketch in §13, which is illustrative.
>
> **Companion:** [`ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md`](ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md).

**The brief, restated:** a Python front end with **minimalistic retro indie graphics**, **a lot of text
but not text-only**, and **graphs everywhere** — NetworkX is already the world model. References:
**Citizen Sleeper** (stillness, text weight, one screen at a time), **Hacknet** (a map of systems you
inhabit), **Cyber Manhunt** (evidence pinned to a board until it clicks).

---

## 1. Stack decision

| Layer | Choice | Why |
| --- | --- | --- |
| Window, input, drawing | **pygame-ce** | Mature, small, pixel-exact, no shader requirement, trivial on Linux, and it draws whatever we tell it — which is exactly right for a 4-colour game |
| Graph model and layout | **NetworkX** (already in use) | The world *is* a graph; `spring_layout`/`kamada_kawai_layout` give a first pass, hand-tuned positions are stored |
| Fonts | one monospace family, two sizes, SIL/OFL licensed (e.g. IBM Plex Mono, JetBrains Mono, or a 5×7 bitmap face drawn in code) | Retro look without a font licence trap |
| Packaging | the existing Python package, extra `noopunk-gui` entry point | No second runtime; the CLI, Evennia and GUI share the library |

**Rejected, and why:**

- **Arcade** — nicer API, heavier dependency, and it invites shaders and sprites we do not want.
- **Dear PyGui / Tkinter** — desktop-tool feel; text widgets fight a pixel aesthetic.
- **Textual** — excellent for a text client, but the brief explicitly says text-only is not enough. It
  stays valuable as the *CLI* layer, not the graphical one.
- **Godot** — already in the repo for other work; using it for this would make the "Python front end"
  a Godot project with Python in it. The boundary is in §12.

**One rule that matters more than the stack:** the renderer draws a **view state** produced by the
engine-neutral core. It never computes a rule, never rolls dice, never decides what is true.

---

## 2. Art direction: four colours and a lot of paper

- **Resolution** 960×540, integer-scaled to the window (2×, 3×). Nothing is drawn at fractional scale.
- **Palette** 4–6 colours per scene, from a fixed set: near-black paper, bone, amber, cyan, one alarm
  red. Astral scenes shift the palette rather than adding effects.
- **Lines** 1 px. Borders 1 px. No gradients, no soft shadows, no blur.
- **Dither** only as a pre-made 2×2 pattern for fills; never as a runtime shader.
- **Motion** is sparse: cursor blink, a 90 ms typewriter reveal, a slow pulse on the selected node,
  a 200 ms slide between screens. Nothing bounces.
- **Scanlines** optional, off by default — a toggle, not an identity.

**Text is the artwork.** The typographic hierarchy does most of the visual work: a heading at 2× the
body size, body at 16 px, captions at 12 px, generous line spacing, 68–76 characters per line, and
margins wide enough that a text panel reads like a page rather than a console dump.

---

## 3. Screen anatomy

```
┌──────────────────────────────────────────────────────────────┐
│  CASE 2045/114 · PROVENANCE OF A RECORD        Tue 03 Nov  │  status strip
├───────────────────────────────┬──────────────────────────────┤
│                               │  EVIDENCE                    │
│        G R A P H              │  ▪ death certificate (pinned)│
│     (nodes and edges)         │  ▪ pension record            │
│                               │  ▪ analyst note (claim)      │
│                               ├──────────────────────────────┤
│                               │  TEXT                        │
│                               │  The clerk says the stamp is  │
│                               │  genuine. She says it twice.  │
├───────────────────────────────┴──────────────────────────────┤
│ [1] examine  [2] present  [3] pin  [Tab] view  [Esc] back   │  action bar
└──────────────────────────────────────────────────────────────┘
```

- **Graph pane** — 45–55 % of the screen, never less. It is the thing the game is about.
- **Text pane** — the current scene's prose and dialogue, with the typewriter reveal.
- **Evidence tray** — what the player holds, always visible, keyboard-selectable.
- **Status strip / action bar** — time, act, location; and the verbs available right now.

**Why the layout is fixed:** a fixed frame is what makes a low-budget interface feel composed. The
player learns one geometry and the game spends its novelty on content.

---

## 4. The graph, drawn

### 4.1 Node vocabulary

Nodes are 12×12 glyphs, drawn as shapes rather than icons, with a label underneath only when selected
or when the graph is sparse:

| Glyph | Entity |
| --- | --- |
| ● | person |
| ▣ | place |
| ◈ | document |
| ⌗ | system / service |
| ◌ | claim or rumour |
| ✶ | anomaly — used sparingly |

**Shape carries meaning, colour carries state.** A person is always a circle; a person who is
*contradicted* is a circle with a red outline. This keeps the interface readable in greyscale and for
colour-blind players.

### 4.2 Edge semantics

| Style | Meaning |
| --- | --- |
| solid | verified relation |
| dashed | claimed relation (a source says so) |
| dotted | hypothesis — the player's, explicitly provisional |
| red, doubled | contradiction |
| arrow | direction matters (says →, employs →, located →) |

**This is the investigation model made visible**: the five categories in the architecture doc
(truth / claim / evidence / knowledge / hypothesis) become line styles the player can read at a glance.

### 4.3 Layout stability

NetworkX layouts are **precomputed and stored**, not recomputed at runtime. A case carries its layout
in data; the renderer applies an offset and a zoom. If a live layout is needed for a generated scene,
run `spring_layout` once with a fixed seed and cache it.

*Reason:* a graph that rearranges itself when a node is added is a graph the player cannot remember,
and memory is the whole interface.

### 4.4 Scale

- Up to ~40 nodes: everything labelled.
- 40–120: labels on hover and on the selection path only; the rest are glyphs.
- Beyond 120: cluster into district/agency supernodes; drill down.

---

## 5. Scene patterns

### Investigation / OSINT — the board
Split view: documents on the right, graph on the left. Opening a document reveals entities; **pinning**
an entity adds it to the graph with its source attached. Comparing two claims draws a contradiction
edge if the player notices it. No timer, no score.

### Dialogue / interrogation — the evidence tray
No portraits. A name, a one-line descriptor, the text, and the evidence tray at the bottom. The verbs
are *ask*, *present*, *press*, *leave*. Presenting the right document unlocks a statement; the wrong one
costs goodwill, not progress. **No emotion meter, no lie detector.**

### Cyber — the map you are inside
A Hacknet-shaped view: nodes for hosts, edges for links, a command line at the bottom that accepts the
verbs CWN hacking already defines. Access state is drawn on the node (locked, open, owned). Rolling is
the core's; the renderer only shows the result.

### Action — pressure, not a battlefield
No grid. A small ring of abstract positions (engaged / near / far / cover / contained), a **pressure
track** for the scene (escalation, bystanders, time, backup), and a log of what has happened. Verbs:
*command*, *restrain*, *move*, *use cover*, *call backup*, *de-escalate*, *withdraw*. Firearms are a
separate, deliberate choice with consequences that outlive the scene.

**Pursuits** are the graph again: road nodes, closing distance, hazards, radio coverage. A chase is a
path problem under time pressure.

### Dream / Astral
The same renderer with the palette shifted, the grid slightly wrong, and text that does not quite
answer. Scripted scenes only; no free-roam astral simulation.

---

## 6. Interaction

- **Keyboard first**: arrows/WASD to move the cursor, Enter to select, 1–9 for verbs, Tab to cycle
  views (Physical / Cyber / Social / Investigation), Esc to back out, `?` for the key map.
- **Mouse optional**: hover for a tooltip card, click to select, drag to pan, wheel to zoom.
- **Never require the mouse.** The tabletop and CLI players must not be second-class, and a keyboard
  interface is faster for text-heavy play anyway.

---

## 7. Data contract

The core produces one structure per frame; the renderer is a pure function of it.

```
ViewState
  scene_id, act, location, time
  headline, body_text[], choices[]
  graph: nodes[label, kind, state, x, y], edges[src, dst, kind, style]
  evidence: items[id, label, source, pinned]
  pressure: optional track for action scenes
  palette: key
```

**This is the testability hinge.** With the renderer taking a plain state object, the layout can be
tested headlessly, golden-state snapshots can be compared without a display, and the same state can be
rendered by the CLI as text. No test needs a window.

---

## 8. Performance

- 60 FPS target, but the game is mostly static: redraw only when state changes.
- Cache rendered text surfaces per string; do not re-render prose every frame.
- Pre-render the 4–6 colour palette and the glyph atlas once.
- Graph redraw only when the graph or the selection changes.
- A 960×540 surface is 2 MB; there is no reason for this game to be heavy.

---

## 9. Accessibility

- **Shape encodes kind, colour encodes state** — readable in greyscale.
- Text scale option (1×/1.5×/2×) that reflows panels rather than shrinking text.
- Full keyboard navigation; no timers on dialogue or investigation.
- A "plain text" mode that dumps the current ViewState as prose — the CLI, by another name.
- No colour-only contradictions: red edges are also doubled.

---

## 10. Boundary with the other clients

| Client | Role |
| --- | --- |
| **Tabletop** | The authority for rules text; the GUI never invents a rule |
| **CLI / text game** | Same library, textual rendering; the accessibility fallback and the test surface |
| **Evennia web client** | Multiplayer/social layer, same core |
| **This Python GUI** | Single-player narrative and investigation client — the "one screen at a time" experience |
| **Godot** | Not replaced by this plan. If a spatial 3D/2D action game is built, it stays a separate client of the same core — **decide this boundary explicitly before either grows** |

---

## 11. Milestones

| # | Deliverable | Done when |
| --- | --- | --- |
| **M0** | Static mock | One hard-coded screen draws at 960×540 with the palette, typography and frame — no logic |
| **M1** | Graph renderer | A stored NetworkX layout draws with glyphs, edge styles, pan/zoom, hover cards |
| **M2** | Investigation view | The existing invoice case renders: documents, pinning, contradiction edges |
| **M3** | Dialogue + evidence tray | Presenting evidence unlocks a statement; wrong evidence costs goodwill |
| **M4** | Cyber view | CWN hacking calls the core; the map shows access state |
| **M5** | Action scenes | Arrest and pursuit prototypes with the pressure track; CWN resolves |
| **M6** | Polish | Palette shifts, transitions, optional scanlines, text-scale option |

**M0–M2 is the whole proof.** If the graph and the prose do not feel right together on one screen,
no amount of later polish saves it.

---

## 12. Risks

| Risk | Mitigation |
| --- | --- |
| The graph becomes decorative | Every node must be *actionable*: clicking it offers a verb or a fact. A node you cannot act on or learn from is not drawn |
| Scope creep into a tactical map | The Action scene has abstract positions by design; a grid is explicitly out of MVP scope |
| Layout instability | Stored positions; seeded layouts; never re-layout on node insertion |
| Font licensing | OFL/SIL fonts only, or a hand-drawn bitmap face |
| Two clients diverging | One `ViewState`, one core; the GUI must never hold a rule |
| Too much text on screen | 68–76 characters per line, one screen at a time, typewriter reveal; the text *is* the game, but a wall of it is not |

---

## 13. Illustrative sketch (not committed code)

```python
# 60 lines that prove the shape, not the game.
import pygame, networkx as nx

W, H = 960, 540
INK, BONE, AMBER, ALARM = (18, 18, 20), (232, 226, 210), (214, 158, 46), (196, 62, 52)

def load_scene(state):
    g = nx.Graph()
    for n in state["nodes"]:
        g.add_node(n["id"], **n)
    g.add_edges_from((e["src"], e["dst"], e) for e in state["edges"])
    return g

def draw_graph(screen, g, font, selected=None):
    for src, dst, data in g.edges(data=True):
        a, b = g.nodes[src], g.nodes[dst]
        pygame.draw.line(screen, BONE if data["style"] == "solid" else INK,
                         (a["x"], a["y"]), (b["x"], b["y"]), 1)
    for node_id, node in g.nodes(data=True):
        r = 6
        pygame.draw.circle(screen, AMBER if node_id == selected else BONE,
                           (node["x"], node["y"]), r, 1)
        if node_id == selected:
            screen.blit(font.render(node["label"], True, BONE),
                        (node["x"] + 10, node["y"] - 6))

def wrap(text, width=72):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line); line = w
        else:
            line = f"{line} {w}".strip()
    return out + [line]
```

**Why this is worth writing down:** it shows the whole bet in one screen — a NetworkX graph, a
one-pixel line style carrying meaning, and prose wrapped to a readable measure. If that reads well,
the rest is content.

---

## 14. What this plan does not do

- It does not add pygame, NetworkX or a font to the dependency list. That is a separate, explicit
  decision.
- It does not write the renderer, the scene data or the assets.
- It does not change a rule, a scene kind's mechanics, or the text client.
