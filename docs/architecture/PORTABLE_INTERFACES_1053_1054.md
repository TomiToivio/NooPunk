# NoöPunk interfaces: one library, multiple presentations (#1053, #1054)

**Binding dependency direction:** UI/engine adapter → portable NoöPunk Python game library. **Evennia is one optional MUD adapter, never the foundation for other UIs.** CWN remains immutable; selected SWN/WWN/AWN rules and optional NoöPunk mods belong in shared Python implementations, not client code.

## Historical prototype interfaces (not the production integration target)

The portable example campaign is an **original rules-neutral prototype**, not a complete CWN conversion. It already supports a headless session, an optional library-record side quest, two clues, completion, and versioned save/load.

From repository root (Python 3.10+):

| Interface | Run | Dependencies |
|---|---|---|
| Plain console | `python -m portable_noopunk.console` | Python standard library |
| Local browser | `python -m portable_noopunk.interfaces.web` then visit `http://127.0.0.1:8765/` | Python standard library |
| Illustrated browser starter | `pip install ".[web]"` then `python -m portable_noopunk.interfaces.nicegui` | NiceGUI |
| Enhanced terminal starter | `pip install ".[textual]"` then `python -m portable_noopunk.interfaces.textual` | Textual |

The standard-library web UI intentionally binds to **127.0.0.1 only** and keeps a single process-local shared session. It has **no authentication or multi-user isolation** and must not be deployed publicly. The NiceGUI/Textual implementations are minimal exploratory views, not claims of polished artwork or feature-complete clients.

## Earlier adapter candidates (superseded for the graphical MVP by #1184)

- **Evennia MUD:** move/bridge the active MUD code to calls into a single authoritative Python rules and campaign package; preserve existing command behavior and save migration. Do not claim completion until parity tests demonstrate it.
- **Arcade 2D** (or existing Pygame): presentation of scene/map/sprites and tactical interaction on top of shared action results, never another rules implementation.
- **Ursina 3D**: optional later prototype.
- **Concordia:** agent/GM action proposer/integration, *not* an authoritative engine or a player-facing UI.

## Historical prototype contract and acceptance

`portable_noopunk.campaign.Game` handles validation and game-state changes. `portable_noopunk.adapters.LocalAdapter` accepts commands, returns library `Outcome`, exposes legal actions and detached snapshots. Frontends may render text, buttons, images and maps, but must never decide clues, combat, CWN rolls or faction effects.

Run the core/adapter regression tests:

```bash
python -m unittest discover -s tests -p 'test_portable_*.py'
```

**Limitations:** Existing `src/rules`, `mud/nopunk_mud`, and `portable_noopunk` still contain multiple historical models. The authoritative CWN migration, comprehensive tabletop parity, a fully fledged single-player UNSA campaign and Evennia conversion are *not* completed by these UI samples. See `docs/design/ISSUE_1053_ENGINE_INDEPENDENCE_AUDIT.md`.

**Rulebook sync:** This patch only adds presentation behavior, so it adds no tabletop mechanics. If shared rules/mods change later, update the tabletop rulebook, code, coverage matrix and golden tests together.


## Unified gameplay architecture (#1184, 2026-11-05)

**Current direction:** NoöPunk is **apocalyptic cyberpunk science fiction**, with minimalist retro indie graphics and substantial text. The graphical client is a real deliverable; a text-only release does not satisfy this interface direction. Tabletop, CLI and Evennia remain supported ways to exercise the same rules. The sections above describe historical prototypes, not an instruction to build another campaign on `portable_noopunk.Game`.

This section implements the architecture-summary scope of [#1184](https://github.com/TomiToivio/NooPunk/issues/1184). It specifies the GUI plan, not a shipped GUI. CWN is immutable; interfaces expose shared state and invoke existing rules. No WWN material is required merely to complete a genre checklist. Existing WWN implementations are not deleted.

### One world, several useful views

Physical, Cyber, Social and Story are graph families; Investigation is a view of discovered evidence and relationships, not a duplicate world. Astral navigation remains deferred until authored projection scenes need it. Physical/Astral nodes are locations with occupants; Cyber avatars can occupy devices while their operators' bodies stay elsewhere. Reuse stable entity IDs across all views and keep character state in its existing owner.

| Player activity | Presentation and inspirations | Resolution boundary |
| --- | --- | --- |
| Exploration | Location graph, short scene description, sparse illustration, people and exits; Citizen Sleeper and Disco Elysium as presentation references | CWN exploration, movement and applicable skills |
| Online investigation / OSINT | Searchable records, messages, dossiers and evidence board; Cyber Manhunt, Orwell and Song of Farca | Appropriate inquiry discovers essential clues; CWN checks govern risk, cost and additional detail. Restricted access uses CWN hacking |
| Dialogue / interrogation | Transcript, questions, evidence tray, attributed statements and contradictions; Silicon Dreams and Blade Runner | Social, Goal and Personality Tags provide context; appropriate CWN checks resolve uncertain actions. No emotion meters, automatic lie detection or interrogation point economy |
| Cyber / hacking | Linked devices, access state, terminal transcript and contextual program actions; Hacknet, Midnight Protocol and DROP | Existing CWN hacking programs, checks and timing; no imported hacking minigame |
| **Action** | Schematic positions/routes, current objective, people at risk, dialogue and legal available actions; Finnish police procedural with Hill Street Blues ensemble tension | Arrests, foot/car pursuits, containment, rescue, withdrawal and de-escalation use applicable CWN procedures. Combat is one possible activity within an Action scene |
| Scripted dream / anomaly | Authored scene graph, sparse altered imagery and descriptive text | Scripted events and permitted published effects; no freeform projection, teleportation or precognition simulator |

**Scene vocabulary:** Investigation, Exploration, **Action**, Social, Cyber and Astral. Several labels can apply to a scene. Replace the *scene category* Combat with Action in new design and player-facing labels. Keep “combat” where it names an actual CWN rule, procedure or module. Existing serialized `combat` labels require a compatibility alias/migration when the runtime adopts `action`; this documentation change does not pretend to migrate saves.

The dramatic baseline is police work in Finland: coordination, interviewing, arresting suspects, protecting bystanders and making decisions under pressure. Routine civilians are not assault-rifle enemies. A dangerous armed encounter must be specifically authored, not generated as the default filler. Violence has consequences; killing is not the default objective or success measure. Use the established [Europol/Finnish authority split](../world/EUROPOL_HELSINKI_1114.md) rather than giving Europol universal arrest powers.

Action scenes show the objective before any attack option. An arrest may end in surrender, safe custody, escape or withdrawal; a pursuit may end through losing contact or a safe stop. Describe these with existing scene flags and consequences, not a new pursuit currency or morality meter. A future implementation must identify the relevant CWN procedure for each uncertain action; an uncovered procedure remains an explicit gap rather than a UI-invented rule. Abstract space is sufficient; a tactical grid is not required.

### Evidence, knowledge and tags

Maintain distinct concepts: canonical world truth; a source's claim; an acquired evidence item with source/provenance; the player's recorded knowledge; and a working hypothesis with supporting or contradicting evidence. A witness statement stays attributed even when it unlocks a lead. Neither confidence styling nor a graph edge makes a claim true.

Reuse the investigation rules and `CaseSession` discovery/evidence/hypothesis facilities. Extend missing provenance as metadata in those owners; do not add another investigation resolver or GUMSHOE point system. The existing GUMSHOE/CWN mapping is a design reference, not authorization to introduce a second player skill list. Core clues follow appropriate access and inquiry; discretionary failure creates consequences or alternate approaches rather than blocking the only case route.

Filter the player projection **before** layout, search, tooltips, exports and accessibility descriptions. Hidden nodes must not leak through edge counts, unexplained gaps, labels or layout movement. A suspected link is visibly a hypothesis; source claims and confirmed observations use distinct labels/shapes, not color alone. Dialogue yields testimony, documents, admissions, contradictions and leads. No emotional scoring.

Tags record simple narrative state, temporary/permanent modifiers or permitted abilities. They must remain CWN-compatible and usable on paper. Reuse existing GoalLog horizons for Scene/Episode/Series goals; do not create a parallel progression or social simulation engine.

### PSI/Magick access policy

Magick is PSI and PSI is Magick in the fiction. These accepted source systems do not require a new compatibility or balancing subsystem.

| Source / phenomenon | Access boundary |
| --- | --- |
| SWN Psionics / Psychic Training Focus | PC choices limited to **Telepathy and Telekinesis** |
| AWN Mentalist Edge | Accepted PSI route; PC effects remain within Telepathy/Telekinesis |
| AWN Mutant Edge | **NPC-only**. Call them Mutants; Hybrid ancestry is one possible, potentially unknown explanation |
| CWN Spellcaster / Summoner Edges | Included as PSI/Magick expressions; NPC/exceptional use does not grant PCs a loophole around the stated restrictions |
| Psychotronic devices / implants | Technological delivery of effects under the same PC restrictions |
| Astral Projection | Scripted dreams/spontaneous OOBEs, NDEs or special Monroe-style technology events |
| Teleportation, Precognition and other out-of-scope powers | NPC or authored events; no selectable general PC power |

No duplicate progression and no automatic stacking of Edge benefits. Law of One is **lore, not rules**. Fourth Density awakening explains psionics narratively; it adds no Density level, polarization meter or mechanical gate. This is an access specification for [#1178](https://github.com/TomiToivio/NooPunk/issues/1178), not a claim that all restrictions are enforced in current code. It supersedes broader PSI options in the older #1164 proposal.

### Python graphical interface plan

**Recommended first implementation: PySide6 / Qt Widgets with QGraphicsScene and QGraphicsView, using NetworkX for graph projections and layout.** This is a proposed implementation choice within the requested Python direction; validate it in the first spike. Qt supplies text widgets and an interactive 2D scene, reducing the need to build text selection, scrolling and focus handling inside a game renderer. NetworkX supplies graph structure/algorithms, not the entire UI.

The earlier Arcade/Pygame candidates in [#1084](https://github.com/TomiToivio/NooPunk/issues/1084) remain fallback options if the spike fails; do not build competing clients simultaneously. The strategy game's #309/#347 renderer discussion has separate scope and does not decide this RPG interface.

| Screen region | Content and behavior |
| --- | --- |
| Header | Case, location, current objective and relevant status; no omniscient story spoilers |
| Main graph pane, roughly 40% width | Clickable nodes/edges, pan/zoom, focus on selected neighborhood, layer selector and a text-list equivalent |
| Reading pane, roughly 60% width | Scene text, dialogue, documents and selected evidence, with adjustable font and selectable text |
| Context area | Short legal-action list and evidence presentation; explain an unavailable action without revealing hidden requirements |
| Collapsible lower transcript | Action results, radio/terminal output, roll explanations when applicable; never steal reading position |

Ratios are an adjustable starting point, not fixed pixel requirements. Resize down to a stacked layout and provide keyboard navigation, search, readable focus and adjustable contrast. Text remains immediately readable; typewriter effects and CRT distortion are optional and off by default. Screen-reader access requires the semantic list/tree beside the graphical scene, not merely a canvas.

Use charcoal backgrounds, warm off-white text, violet/pink accents and restrained terminal green. Use thin vector lines, simple geometric icons, a few silhouettes/portraits and occasional static location art. Preserve the 1970s psychedelic retrofuturist character. Citizen Sleeper informs text and illustration balance; Hacknet informs the network/terminal relationship; Cyber Manhunt informs documents, identities and evidence connections. These are design inspirations, not copied assets, layouts or rules.

**Layout strategy:** Physical graphs use authored coordinates where available; otherwise show explicitly schematic routes. Cyber uses stable network neighborhoods; Social/Investigation use pinned or seeded layouts with expandable clusters. Story shows only discovered objectives/leads, never the GM's full branching solution. Astral reuses the renderer when scripted content warrants it. Start with tens of visible nodes; collapse large neighborhoods rather than drawing the whole universe. Cache positions by graph/version and keep camera/selection separate from game saves. Dragging a node changes presentation only, never geography or evidence.

**Adapter boundary:** UI intent → existing validated session action → shared resolver/state transition → detached player-visible projection → Qt widgets. Do not parse narration to recover state, expose raw omniscient snapshots, or mutate NetworkX projections to change the world. Only game actions advance simulation time; resizing and reading do not.

Reuse `src/console/session.py` for the initial portable case and `src/console/agent.py` for its existing validated action vocabulary/observations where appropriate. The campaign path already uses `mud/nopunk_mud/session.py` over `campaign/engine.py`; these APIs are not interchangeable. Choose one session owner per running case and bridge missing observations there. Never run two sessions in parallel or start a third one to connect them.

Place the future Qt adapter outside domain packages (proposed `src/interfaces/qt/`, after the normal overlap check), with a window/view module and a thin presenter. Keep PySide6 an optional dependency; add its import root to the existing engine-boundary guard when implementation begins. No Qt imports in rules, session state or graph models. Preserve versioned JSON saves and seeded RNG through existing serializers; UI preferences are separate. Render on the UI thread; any slow layout worker gets a detached filtered projection and returns coordinates only.

Official implementation references, checked 2026-11-05:
- [Qt for Python Graphics View](https://doc.qt.io/qtforpython-6/overviews/qtwidgets-graphicsview.html): scene/items/view support for interactive 2D graphics.
- [NetworkX drawing and layout](https://networkx.org/documentation/stable/reference/drawing.html): graph layouts; NetworkX itself recommends dedicated visualization tools.

### Delivery sequence and verification

1. **Read-only GUI spike:** existing case text plus a filtered graph; select nodes, inspect evidence, pan/zoom and use the keyboard/list view. Validate font scaling, long documents and responsive resizing. No new game content or rules.
2. **Playable case adapter:** wire the same validated actions and existing save/load. Compare seeded action sequences and final state documents against the CLI. Verify invalid/hidden targets are rejected in the session, not just disabled in the GUI.
3. **First Helsinki rookie investigation:** adapt the existing [campaign outline](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) into an author-approved slice: briefing → public record → interview → physical lead → limited hacking → report to Romppainen. Add one optional Action branch (safe arrest or pursuit) with a nonviolent route. These are implementation beats, not newly authored mission canon.
4. **Additional views:** connect Social and case-board relationships; demonstrate a combined Physical/Cyber Action scene without two time economies. Add scripted Astral presentation later.
5. **Packaging and playtest:** offline launch, no LLM/API requirement, optional GUI dependencies, keyboard-only completion, long-text usability and restart/save parity. Run existing boundary, duplication and applicable rules/adapter checks; test graphics on a real display as well as headless widgets.

First-case handoff: every scene identifies its graph references, entry condition, player-known text, allowed actions, essential clue and provenance, alternate lead/failure consequence, existing resolver, exit flags and report contribution. Interrogation returns evidence; the final report records the player's interpretation without declaring an unsupported theory objectively true. All tracks must reach the core evidence. Reuse the #1164 templates only with this updated vocabulary and access policy.

GUI acceptance: complete the same case through GUI and CLI with matching state, render only player-known facts, preserve save/load and RNG, use no UI-owned rolls, show Action outcomes beyond violence, and remain usable with enlarged text and keyboard controls. The GUI is not complete merely because a graph image renders.

### Overlap ledger and remaining work

Inspected against main `1e736f69b84b272fa3141285c7ca9b7cd78ffb9f` on 2026-11-05.

| Existing owner | Evidence / reuse | Remaining work |
| --- | --- | --- |
| `src/world/graphs.py`, `src/world/helsinki.py` | #1182/#1183, `tests/test_world_graphs_1178.py`, `tests/test_helsinki_graph_adapter_1178.py` | Player visibility projection and GUI integration; do not create a third graph model |
| Graph authoring and text-world adapters | #1180/#1181; #1179 closed unmerged | Reconcile with world model under #1178; [duplication audit](../DUPLICATION_AUDIT.md) records the competing implementations |
| `src/console/session.py`, investigation rules and `src/console/agent.py` | Existing case state and #1095 validated actions | Provenance/observation gaps and new adapter parity, not a replacement session |
| `mud/nopunk_mud/session.py`, `campaign/engine.py` | Existing campaign adapter boundary | Integration only after selecting the case's authoritative session |
| #1084 | Existing adapter tracker; no open PR found during this review | Qt spike and GUI milestones above; Concordia/Tarot remain separate |
| #1178 / #1164 | Graph implementation and historical design proposal | PSI enforcement and scripted Astral remain tracked there; neither issue is closed by this document |

This issue's deliverable is the consolidated design and explicit implementation handoff. Runtime Action-label migration, GUI construction, end-to-end case integration and full PSI enforcement are **not implemented by this documentation change**. No published rule or tabletop numeric procedure changes.
