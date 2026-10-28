# Godot implementation plan: RPG + investigation + hacking on one rules engine (#728)

**Plan only. No Godot code is added by this document.** It states how the three modes are built,
what each mode reads, and how the build is prevented from inventing a rule the table cannot run.

Companion: `ISSUE_728_GODOT_ASSETS.md` (what we can use, and what it costs).

---

## 1. The constraint that decides the architecture

> *Rules must work on both tabletop and computer.*

Everything below follows from refusing one thing: **a mechanic that exists only in Godot.** If the
build needs it, the paper rules must be able to express it first — otherwise it is a second game
wearing the first game's character sheet.

## 2. What already exists (and must not be re-invented)

| layer | artefact | state |
|---|---|---|
| rules kernel | `data/rules/wn_core.json`, `src/rules/wn_core.py` | implemented, tested |
| CWN procedures | `src/rules/cwn_*.py` (core, combat, trauma, healing, strain, hacking, character) | implemented, tested |
| investigation | `src/rules/investigation.py`, `anomaly_gate.py` | implemented, tested |
| mind/conditions | `src/rules/mental_load.py` | implemented, tested |
| case data | `data/scenarios/lakkahaltia/case_graph.json` | validated by `CaseGraph` |
| Godot adapters | `godot/core/rules_adapter.gd`, `investigation_adapter.gd` | implemented, tested headless |
| Godot slice | `godot/scenes/hospital.tscn`, `level_builder.gd`, `player.gd` | playable rooms, doors |

**The rule of this plan: no new rule module.** Every mode is a *presentation* over the above.

## 3. Node and autoload structure

```
res://
  autoload/
    GameState.gd        # the single authoritative state (exists: godot/core/game_state.gd)
    RulesAdapter.gd     # 2d6 checks, d20 saves (exists)
    InvestigationAdapter.gd  # case graph reads (exists)
    ClockService.gd     # action budget + scene clocks (NEW: presentation of mission time)
  ui/
    CaseBoard.tscn      # evidence pins and links
    DialoguePanel.tscn  # portrait + text + check preview
    CheckPreview.tscn   # shows modifier and target BEFORE the roll
    NetworkGraph.tscn   # hacking node map
    TacticalHUD.tscn    # action economy, initiative, cover
  scenes/
    hospital.tscn       # exists
    network_node.tscn   # one node in the hacking graph
```

**`ClockService` is the only new autoload, and it is a presentation of something the table
already has**: mission time. It must not become a second clock beside CWN's turn structure.

## 4. The three modes, each a view over one state

### 4.1 Investigation — case board

- Reads: `case_graph.json` + `GameState.discovered_clues`.
- Writes: nothing except `GameState.hypotheses` **when the player edits it**.
- **Forbidden:** suggesting links, highlighting a hypothesis, showing a match the player has not
  made. The board is an externalised memory, not a solver.
- Discovery calls `InvestigationAdapter.discover(scene, sheet, access, inquiry)` — the same call
  the table referee resolves by reading the same JSON.

### 4.2 Dialogue — the social mode

- Reads: `data/scenarios/<case>/dialogue.json`, `GameState` conditions.
- A social action is a **CWN check**: `RulesAdapter.check(skill, difficulty, modifiers)`.
- The **check preview shows the target and the modifier before the roll** — inspectable, per the
  memo's rule — and the roll uses the adapter's seeded dice, so a save/reload cannot reroll into
  a better outcome.
- Failure **costs an action, or time, or a condition** — never "nothing happens".

### 4.3 Hacking — the node graph

- Reads: a `network_graph.json` (nodes, edges, access class, trace threshold) — a **new data
  file, not a new rule**: CWN already has access classes and trace.
- The player gets **two actions per turn** from `ClockService`; the network responds after them.
- Every gate is a CWN check via `RulesAdapter`. The graph never computes an outcome.
- **Paper equivalence:** six nodes on an index card, a token, two actions a round, a trace die.
  If a table cannot run it, the Godot version is wrong.

### 4.4 Tactical combat

- Reads: `GameState` actors; resolves through `src/rules/cwn_combat.py` semantics.
- Grid, initiative, cover, action economy — all **presentation** of existing rules.
- Combat is **opt-in or failure-forced** (#724), never the path of least resistance.

## 5. How the build is prevented from inventing rules

Three enforcement mechanisms, in increasing strength:

1. **Adapter-only access.** No scene script may call `randi()`, compute a modifier, or compare a
   total to a difficulty. A grep-based lint (`tools/check_godot_rule_leak.py`) fails the build if a
   `res://scenes/**` or `res://ui/**` script references dice or difficulty constants.
2. **Contract tests.** `godot/tests/` asserts that every difficulty in a scenario exists in the
   kernel, every competency exists in the skill list, and every case scene is leavable — the same
   assertions the Python suite makes.
3. **Round-trip test.** One case is played twice — once through the Python API headless, once
   through the Godot adapter — and the two transcripts must match action for action. **This is
   the test that actually proves "same rules"**, and it is the acceptance criterion for the slice.

## 6. Milestones

| id | scope | done when |
|---|---|---|
| **M0** | `ClockService` + action budget, no UI | a headless test shows N actions then a cycle advance |
| **M1** | Case board over `case_graph.json` | player can traverse all four rooms; no scene blocked; board shows only found clues |
| **M2** | Dialogue with check preview | a social check is rolled through `RulesAdapter`, cost applied on failure |
| **M3** | Network graph | two actions/turn, one gate check, trace escalates; paper version documented and playable |
| **M4** | Tactical encounter, optional | the same case completes **with combat skipped**, and the round-trip test passes |

**Stop rule:** no milestone begins until the previous one has a headless test. The failure mode
this avoids is a beautiful UI over rules that quietly drifted.

## 7. Save/load

- One save file = `GameState` serialised, versioned (`save_version`).
- **Never** rescale or invent values on load; a v1 save loads as v1 or refuses.
- Seeded dice state is saved, so reload cannot be used as a reroll.

## 8. Performance and scope budget (small team)

| budget | target |
|---|---|
| rooms in the slice | 4 |
| props | ~30 voxel models, reused across rooms |
| characters | 6 (player + 5 NPCs), portraits only for dialogue |
| simultaneous lights | ≤ 4 per scene, baked where possible |
| target hardware | integrated GPU, 60 fps at 1080p |

## 9. What this plan does not include

Open-world navigation, crowd simulation, facial animation, voice acting, multiplayer, procedural
cases. All are out of scope for the slice and none is required to prove the three modes coexist.

## 10. The open decision this plan waits on

**Is the action budget one economy across hacking, social and tactical, or does hacking get its
own clock?** (#728 §10.) M0 is written so either answer is a data change, not a rewrite — but the
answer decides whether `ClockService` is one service or two, and I will not guess it.
