# #728 follow-up: Godot implementation blueprint for the tabletop-compatible detective CRPG

**Status:** implementation **plan** and asset due-diligence shortlist, not a claim that systems/assets were installed, tested or purchased. 2026-10-28.  
**Targets:** NoöPunk legacy RPG; Godot **4.7.2**, Compatibility renderer, project root `project.godot`. Preserve the existing hospital playable case. Do not modify independent `strategy_game/`.  
**Prerequisites:** [#728 influence review](../design/ISSUE_728_COMPUTER_GAME_INFLUENCES.md), [#724 synthesis](../design/ISSUE_724_CRPG_DESIGN_SYNTHESIS.md), [#704 GUMSHOE research](../design/ISSUE_704_GUMSHOE_INVESTIGATION.md), [CWN/SWN baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md), [architecture audit](ARCHITECTURE_CONSOLIDATION.md), [asset inventory](ASSETS.md).

## Design commitment: RPG, detective adventure and hacking are *one game*, not separate minigames

All activities use the same actor sheet (CWN STR/DEX/CON/INT/WIS/CHA; skill ranks; Edges/Foci; equipment; SWN psychic packages when authorized), one mutable case/party world state, and the **published source procedure** for uncertainty, combat and cyber actions. The tabletop GM and Godot execute equivalent decisions, permissions, resources, rolls and consequences.

Three **presentations** over the same action/event/state ledger:

- **Social/investigative RPG view:** isometric location, dialogue panel, witness source cards, journal, task checks and consequences. Shadowrun: Dragonfall + Disco Elysium / Citizen Sleeper are *experiential* references.
- **Detective case view:** evidence board (documents, witnesses, timestamps, contradictions, alternative hypotheses and leads), GUMSHOE-inspired reachable essential observations, optional skill-gated interpretation and costs. Blade Runner, Observer and Song of Farca are UI/scene references.
- **Hacking view:** selectable devices/hosts/connections, credentials and reachable links; command palette of permitted **CWN hacking procedures**. DROP and Midnight Protocol inspire graph legibility, **not** a reflex-based mini-game or homemade cyber rules.
- **Optional tactical view:** same actors and equipment, CWN initiative, movement/action types, rolls, cover, injury, alternate retreat/negotiation paths, on a modest isometric grid. No separate Shadowrun combat engine.

## Current repo reality (audit before coding)

`project.godot` declares Godot 4.7.2-stable, GL Compatibility, a default `res://scenes/main.tscn`, and autoload `GameState` from `godot/core/game_state.gd`. Existing `godot/` directories: `core/`, `narrative/`, `scenarios/`, `scenes/`, `tests/`, `ui/`. `docs/godot/ARCHITECTURE_CONSOLIDATION.md` documents multiple overlapping hospital-case entry points (`godot/`, `scenes/`, `src/godot/`) with drift and some old d10 behavior. **Do not delete, port, or redirect any working entry point without a separate migration PR and executable regression coverage.** Build new UI slices against the canonical `godot/` runtime only after verifying the current scene wiring.

Existing `docs/godot/ASSETS.md`, `ASSET_SHORTLIST_2026-10-26.md` and `data/assets/manifest.json` are asset registers. Extend them with actual downloads and license receipts rather than creating a second definitive asset inventory.

## Proposed system architecture (interfaces, not yet approved APIs)

```text
Case content data (scene IDs, evidence, witness claims, leads, hosts, permissions)
           │
  Player intent (talk, inspect, access, hack, negotiate, move, attack)
           ↓
Action / permission / turn coordinator
   ├── authoritative CWN/SWN rules adapter (existing rules data + source procedures)
   ├── character/equipment/PSI resources
   ├── case evidence + source provenance + hypothesis distinction
   ├── access/security graph (known != reachable != authorized != compromised)
   ├── NPC/institution/ideology consequences + time/deadlines
   └── action result → event log → single versioned GameState
           ↓
    UI subscriptions (not alternative rules)
   ├── dialogue / scene interaction
   ├── investigation journal + evidence graph
   ├── cyber graph + action/command palette
   └── optional tactical map + turn inspector

Parallel: tabletop referee packet (same scenario JSON in human-readable sheets)
```

**Action envelope (conceptual data contract):**
```json
{
  "id": "action_017",
  "actor_id": "investigator",
  "intent": "inspect_audit_log",
  "target_id": "ward_terminal",
  "route_id": "staff_permission",
  "declared_stakes": ["staff_trust", "deadline"],
  "rules_reference": "CWN: relevant published procedure",
  "random_input": null
}
```
This is **example interface data**, not an implemented command or new source rule. An eventual result includes eligibility and source permission, dice (if any), resource and time deltas, evidence IDs, changed access, repercussions and a log explanation. No client may directly set `evidence_found`, `hack_success` or `npc_trust` without an adjudicated event. The same event sequence and input dice must recreate equivalent tabletop/engine outcomes.

**Implementation boundaries (suggested Godot paths; inspect before creating):**
- `godot/core/action_coordinator.gd`: validates intent/access and calls existing source-faithful `rules_adapter.gd`, never defines new dice.
- `godot/core/case_ledger.gd`: evidence/provenance, hypotheses, leads, permissions, witnesses, authored deadlines, relations; serializable data.
- `godot/core/network_topology.gd`: graph of devices and conditional access, *not* the hacking dice system.
- `godot/ui/case_board.tscn`, `godot/ui/hacking_graph.tscn`, `godot/ui/dialogue_case_panel.tscn`, `godot/ui/tactical_view.tscn`: presentation and intent dispatch only.
- `godot/scenarios/lakkahaltia/`: add noncanonical pilot dataset **only with author approval**; no overwritten existing case content.
- `godot/tests/`: executable behavior and parity/replay tests for actual code; **never doc-text assertions**.

Prefer **one common graph data type** for case links and network links, but keep link semantics distinct: an evidence association is not proof, and a physical network edge is not permission. Use pure data exported to a GM/reference sheet and Godot. Avoid an external web service or LLM in the core game loop.

### Godot scene nodes / MVP interaction sketches

**Investigation:** `Control` → `SplitContainer` with source list (`ItemList` / `Tree`), evidence detail (`RichTextLabel`), and case connections (`GraphEdit` + `GraphNode`). `GraphEdit` is an editor-oriented Godot UI primitive, so disable free connections/repositioning unless investigation rules explicitly allow them; only events created through the action coordinator add or expose evidence. Provide a **linear list mode** with keyboard navigation and a non-color status legend.

**Hacking:** `Control` → `GraphEdit` representing devices and links plus inspector and command palette. Node select → reveal *known* attributes → choose permitted program/operation → ask adjudicator → show result and route/alarm/resource changes. Never interpret a drawn edge as virtual access. For a stylized terminal offer a textual command alias for the *same* action. A digital player cannot win by dragging wires or typing secret strings that have no tabletop procedure.

**Dialogue/social:** keep current JSON narrative runner until tested need justifies adopting a plugin. Options are authored choices with prerequisites and event outputs; if a CWN Talk/Connect etc. check is needed, the runner invokes the adapter. `Dialogue Manager` or `Dialogic` may later author text, but must not become a second state/rules authority. Journal stores speaker, when/where obtained, exact *claim*, and inferred hypotheses separately.

**Tactics:** `Node3D` scene with `Camera3D` orthographic/isometric view, `GridMap` or custom cell navigation, selectable unit and action inspector. Translating CWN ranges, movement, cover and action types to tiles **requires explicit scale and source chapter audit** before implementing. The first slice can omit combat entirely or show a small optional confrontation; never substitute an action-time cooldown system.

**3D look:** one small near-contemporary hospital ward and street, modular GLB assets, simple lighting and selective uncanny/cyberpunk set dressing; fixed/rotatable isometric orthographic camera, geometry fade for occlusion. This is *halfway* between recognizable reality and cyberpunk/weird, not a full neon future metropolis.

## Tabletop → Godot parity worksheet (acceptance examples)

| Moment | Tabletop GM procedure | Godot interface | Pass condition |
| --- | --- | --- | --- |
| Examine accessible intake record | Grant core observation with appropriate method/access; check only uncertain consequential follow-up | click record → source card | Same evidence and no arbitrary gate roll |
| Ask witness for sensitive detail | CWN Talk/Connect if meaningful uncertain stakes; roleplay possible failure consequence | dialogue options + shown roll | Same roll threshold, changes, witness statement |
| Compare dates | Establish two independent observed timestamps; the player's hypothesis remains labelled inference | link E-01/E-02 on case board | No automatic canonization of anomaly |
| Gain terminal access | Demonstrate reachability, valid permissions, deck/program prerequisites per CWN | select ward device, inspect authorization | UI never bypasses source limits |
| Intrude toward protected host | Perform **specific** published CWN cyber procedure; GM/engine assess legal route, costs, security and outcome | command on GraphNode, system log | Identical action, roll/resources/alarm |
| Beat deadline | GM's explicit scheduled event plus elapsed actions | journal clock | Same event order in either format |
| Negotiate vs fight | Resolve negotiation with ordinary checks or fight with CWN combat where warranted | choice of dialogue/tactical screen | Neither route becomes forced |

**Proposed deterministic replay test after code exists:** fixed character sheets + authored case state + ordered action intents + externally supplied dice → identical expected event ledger in a headless Godot test and a manually audited tabletop example. Test failed cyber access, source provenance after save/load, optional clues, non-blocking core clues, and tactical refusal/retreat. Do not compare prose wording or freeze lore in CI.

## Implementation backlog in dependency order

**Phase 0: source truth and inventory (blocking).** Confirm current actual main-scene wiring and one canonical case runtime. Trace `GameState`, `rules_adapter.gd`, current JSON content, save format and existing tests. Check source-book coverage against *real* CWN hacking chapter: deck/programs, actions, access, range, protections, alert response. Record source citations and restrictions without copying protected rulebook passages. Choose minimal case scenes with GM sign-off.

**Phase 1: tabletop reference case.** Write a one-page GM procedure and paper packet for briefing → nurse interview → intake log → technician/terminal → audit contradiction → reporting decision, with two independent routes to every essential lead. State existing CWN check triggers, actual deck/program examples from owned books, when time advances, and legitimate access. No new numerical mechanics.

**Phase 2: canonical shared state/events.** Add versioned evidence/witness/hypothesis/access and deadline records to the existing `GameState` pathway; migrate safely with compatibility for existing saves. Add an action dispatcher reusing the approved rules adapter; no new dice engine. Tests: events, save/reload, access denial, evidence provenance, same input rolls = same outcome.

**Phase 3: detective view.** Implement an evidence list/journal first, then `GraphEdit` case board with provenance, lead status, hypothesis separation and accessible list alternative; dialogue choices call action coordinator. Test mandatory clue discovery without a skill-roll dead end, including a lawful alternative to unauthorized data access.

**Phase 4: cyber graph view.** Build 3-node test network (deck → ward terminal → protected audit host → optional backup), distinguish unknown/known/reachable/authorized. Every command maps to a verified CWN hacking action with action requirements and state consequences. Show action log, source rules inspector and failed-access escape route. Only add a visual terminal aesthetic after parity works.

**Phase 5: world and visual integration.** Test GLB art in one hospital room, isometric Camera3D, obstruction fade, click-to-interact, lighting readability and save/resume. Preserve default working FPS scene until the replacement is playable; expose the slice as a separate scene/menu entry for comparison.

**Phase 6: optional tactics + full vertical slice.** Small room, two interactable obstacles, negotiation/retreat or an encounter using CWN rounds and gear; close case with two different consequences and no combat requirement. Shared state and paper parity across transitions. Author approves movement scale and source conversion before coding.

**Acceptance:** six-scene end-to-end path; accessible crucial evidence; one meaningful social check; restricted cyber route and independent alternative; one ideological/institutional choice; optional tactical branch; save/reload; same game rule and consequences in tabletop and Godot; no purchased content required.

## Asset and addon sourcing: shortlist, not automatic dependencies

As of this writing, **nothing below was newly purchased, installed or runtime-tested by this follow-up**. The repository already maintains more extensive asset details in [ASSETS.md](ASSETS.md) and [ASSET_SHORTLIST_2026-10-26.md](ASSET_SHORTLIST_2026-10-26.md). Confirm versions against **Godot 4.7.2**, GL Compatibility, platform exports and actual download license before use; plugin release pages may only certify earlier engine versions.

| Need | Free/open-source option and source | Commercial/paid candidate | Plan / caveat |
| --- | --- | --- | --- |
| Branching conversations | [Dialogue Manager](https://github.com/nathanhoad/godot_dialogue_manager) (MIT per prior repo audit); [Dialogic](https://github.com/dialogic-godot/dialogic) (MIT per prior audit) | No paid tool needed initially | **First reuse existing JSON runner**. Spike one addon only if authoring becomes painful; require event bridge to authoritative GameState |
| Evidence linking & cyber topology | Godot built-in [GraphEdit/GraphNode](https://docs.godotengine.org/en/stable/classes/class_graphedit.html) | None needed | Same graph renderer can share widgets, *not* link semantics. Build accessible list view and action inspector |
| Camera and small isometric scenes | [Phantom Camera](https://phantom-camera.dev/overview/installation) (open-source; inspect license/version) or native Camera3D | No paid dependency | Prototype native orthographic first; addon only for camera blending/occlusion complexity |
| NPC AI (later) | [LimboAI](https://github.com/limbonaut/limboai) MIT, select release by exact Godot version | No paid AI pack needed | Overkill for 4–6 scripted NPCs; only if tactical/ambient AI needs a behavior tree. 4.7 compatibility must be checked |
| Environments: hospital | [Kenney Furniture Kit](https://kenney.nl/assets/furniture-kit) CC0; [Quaternius characters](https://quaternius.com/packs/ultimatedanimatedcharacter.html) CC0 | Optional bespoke hospital props | Start with CC0 geometry, matched import scale and shared materials |
| Street and cyber props | [Quaternius Cyberpunk Game Kit](https://quaternius.com/packs/cyberpunkgamekit.html) CC0; [Kenney City Kit](https://kenney.nl/assets/city-kit-commercial) CC0 | [monogon Voxel Cyberpunk City](https://maxparata.itch.io/cyberpunkcity-monogon); [monogon Voxel Noir](https://maxparata.itch.io/voxelnoir); [Synty POLYGON Sci-Fi City](https://syntystore.com/products/polygon-sci-fi-city) | monogon CC BY-ND/modification ambiguity recorded in prior audit: **do not purchase/import to release pipeline until written clarification**; Synty license and Godot version check |
| UI, icons & audio | [Kenney UI Pack](https://kenney.nl/assets/ui-pack) + [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds), CC0 | Buy bespoke portraits/UI only after the interaction prototype | Digital case board and hacking screen are UX-heavy: custom Control theme likely more valuable than a giant model pack |
| Voxel authoring | [Quaternius Cube World Kit](https://quaternius.com/packs/cubeworldkit.html) CC0; [Zylann godot_voxel](https://github.com/Zylann/godot_voxel) MIT (repo audit) | [MagicaVoxel](https://ephtracy.github.io/) free proprietary tool | Prefer static chunky GLB meshes; voxel runtime terrain is not necessary for a compact isometric case |
| Texture/ambience | [Poly Haven](https://polyhaven.com/license), [ambientCG](https://ambientcg.com/license) CC0 | Licensed premium environmental sound/portraits as required | Original visual identity through restrained lighting + consistent shader/material style |

**Purchase gate:** 1) test free substitutes in the actual GL Compatibility scene; 2) choose a coherent scale, palette, material style and build target; 3) check vendor EULA for commercial use, redistribution in game builds, modification, source/public-repo inclusion and credit; 4) record URL, version, license copy, acquisition date and path in `data/assets/manifest.json`; 5) keep paid source files out of public Git history. Old price figures in asset shortlist are *historical*, not fresh quotations. No purchase authorization implied.

**Plugin gate:** no third-party addon can own rule resolution, save state or emit undebounced consequences without the shared coordinator. Keep candidate versions pinned, opt out cleanly, and headless-test export/scene import after adding.

## Graph hacking that *is* the CWN procedure, not a minigame beside it

The rule already exists in this repository: `src/rules/cwn_hacking.py`. Its docstring is the design
constraint for the whole hacking view —

> "Verbs, Subjects, programs, CPU slots, demons and watchdogs are catalogue content, not procedure…
> The network's node graph is scenario state, not a rules object."

So the graph is **content**, and every affordance on it must map to a symbol that already exists.
Nothing in the UI may compute a difficulty, a modifier or a result.

| UI affordance | Rules symbol (`src/rules/cwn_hacking.py`) | Tabletop equivalent |
| --- | --- | --- |
| deck + Program + INT shown as a budget | `access_pool(intelligence_modifier, program_skill, deck_bonus)` | the Access pool written on the sheet; refreshed by an hour of reprogramming, once a day |
| host badge "security 8/10/12" | `SECURITY_LEVELS` (7, 8, 9, 10, 12 — nothing between them) | the referee's security note; values between are a referee call |
| "important device" / "alerted" / "informant" toggles | `security_difficulty(…, alerted, important_device, tech_quality, inside_info)` | the modifiers the referee applies before the roll |
| wireless edge | `WIRELESS_PENALTY = -2`, **and it cannot leave the entry node** | the −2 the referee states, plus the reachability limit |
| command palette entry | a Verb row: Access cost + check modifier, passed to `hacking_check(…)` | the same row read off the catalogue |
| outcome and alarm state | `AlertClock`: two failed checks = one alert action; two alert actions = alerted (+1 difficulty) | two tick marks, then the second, on paper |

Four node states, and the UI must never collapse them: **unknown** (not rendered), **known** (shown,
no interaction), **reachable** (an edge the deck can traverse — wireless stops at the entry node),
**authorized** (a permission the character actually holds). Dragging a wire can therefore never
grant access; only an adjudicated action can. Each node click reveals *known* attributes only, and a
failed action logs its consequence rather than hiding it.

### One paper node example, and its digital twin

Paper, three hosts and a link, written on a card:

```
[deck] --wired--> [ward terminal, sec 8] --wired--> [audit host, sec 10, important device]
   \--wireless(-2, entry node only)--> [backup spool, sec 9]
INT +2, Program 1, deck Bonus Access 1  ->  Access pool 4
```

The tabletop procedure: the player says what they want and which Verb; the referee states the
difficulty (`8`, or `10 + 1` for the important device), the connection (`wired`, or `wireless` at
−2 and confined to the entry node), and the Access cost; the check is `2d6 + INT mod + Program +
Verb modifier + connection penalty`; two failures mean one alert action, two alert actions mean the
network is alerted and every further difficulty is +1.

In Godot the *same* numbers are rendered: the pool on the deck panel, the badge on the node, the
−2 on the wireless edge, the two-part alarm indicator, and a log line that names the Verb and the
difficulty. The interaction differs — clicking instead of describing — and the arithmetic does not.

## Verified addon and asset register (2026-10-28)

The shortlist above said "per prior audit" and "inspect license/version". Checked today:

| Candidate | Licence, and how it was verified | Engine | Verdict |
| --- | --- | --- | --- |
| [Dialogue Manager](https://github.com/nathanhoad/godot_dialogue_manager) | **MIT** — GitHub API `license.spdx_id`, repo pushed 2026-10-25 | Godot 4 | **spike only if authoring hurts**; keep the JSON runner as the only rules authority |
| [Dialogic](https://github.com/dialogic-godot/dialogic) | **MIT** — GitHub API, pushed 2026-08-30 | Godot 4 | same; it owns its own state, so it may never become the case ledger |
| [LimboAI](https://github.com/limbonaut/limboai) | **MIT** — GitHub API, pushed 2026-10-26 | Godot 4 | **not needed** for 4–6 scripted NPCs |
| [godot_voxel](https://github.com/Zylann/godot_voxel) | **MIT** — GitHub API, pushed 2026-10-01 | Godot 4 | **refuse for the slice**; static chunky GLB only |
| [Phantom Camera](https://github.com/ramokz/phantom-camera) | **MIT** — GitHub API, pushed 2026-10-27 | Godot 4 | optional, after a native orthographic camera is proven |
| [Kenney furniture kit](https://kenney.nl/assets/furniture-kit) | **CC0** — stated on the asset page | any | **preferred** hospital props |
| [Quaternius Cyberpunk Game Kit](https://quaternius.com/packs/cyberpunkgamekit.html) | **CC0** — stated on the pack page | any | **preferred** street/props |
| [Poly Haven](https://polyhaven.com/license) | **CC0** — licence page reachable; terms re-read at download | any | textures and HDRI, preferred |
| [monogon Voxel Cyberpunk City](https://maxparata.itch.io/cyberpunkcity-monogon) | **CC BY-ND 4.0** — stated on the itch page | any | **refuse as-is**: NoDerivatives, and importing/rescaling/materials is a derivative. Paid clarification required before it can be used at all |
| [Synty POLYGON Sci-Fi City](https://syntystore.com/products/polygon-sci-fi-city) | commercial — page reachable; EULA **not** fetched this session | Godot-friendly FBX/GLB | **defer to Phase 5**, and buy only if the CC0 substitutes fail in the actual scene |

**Decision, so the plan does not drift:** the slice ships with **zero paid dependencies and zero
third-party addons**. Every candidate above is either CC0/MIT with a named fallback, or it waits for
the purchase gate. A paid pack is a *visual* decision, and it must not arrive before Phase 4 makes
the interaction legible.

## The parity harness, as a thing that can be built

Parity is claimed in the worksheet above; this is how it gets *checked* once code exists, without a
second rules implementation:

1. **One scenario file, two consumers.** `godot/tests/parity/<case>.json` holds an ordered list of
   intents, the character sheets involved, and the dice supplied to each roll. The Python side runs
   the same intents through `src/rules/` and emits the expected event ledger; the Godot runner
   replays them headlessly and must produce the same ledger, field for field.
2. **Runner:** `godot --headless --path . --script res://godot/tests/parity_runner.gd`. Same pattern
   as the existing `run_tests.gd`, so the CI job that already boots headless keeps working.
3. **What the ledger must contain** (and therefore what the coordinator must emit): action id,
   intent, eligibility and the source permission that allowed it, dice if any, the resulting total
   and success, Access/resources spent, time advanced, evidence ids granted, access/security state
   changes, alarm state, and the consequence list. If a field is absent from both sides it cannot be
   compared, so the ledger shape *is* the contract.
4. **A drift audit, not a test:** `tools/audit_godot_rules.py` — a non-CI operator tool in the same
   spirit as the corpus audits — fails if a `.gd` file outside `godot/core/*_adapter.gd` contains
   dice construction (`RandomNumberGenerator`, `randi`), the outcome band names, or a difficulty
   literal from `SECURITY_LEVELS`. The repository's test policy (#271) keeps prose out of CI; this
   keeps *arithmetic* out of the presentation layer, and it is run by hand before a merge.

What the harness cannot prove, and the plan should say so: that the *table* experience is the same.
That is the Phase 1 paper packet plus a human running both, which is why Phase 1 exists before
Phase 2.

## Remaining decisions and honest verification status

- **Document completed:** subsystem plan, implementation order, controls/nodes, tabletop equivalence, sourcing priorities, licensing checks, and parity acceptance.
- **Not completed:** live import or paid-asset purchase; current-version vendor license audit of every candidate; hands-on reference game comparisons; exact source-text CWN hacking mapping; implementing Godot scenes or changing rules; cross-platform builds.
- **Requires author/source review:** exact CWN cyber procedure mapping, scene-specific legal/social access, whether evidence board is player-rearrangeable, movement grid mapping, time advancement, and whether future story choices require numerical reputation.

**Recommendation:** implement Phase 0 + Phase 1 first, then a fully headless-tested shared ledger. A polished neon hacking UI without source-accurate access semantics is seductive but would create two games with different rules.
