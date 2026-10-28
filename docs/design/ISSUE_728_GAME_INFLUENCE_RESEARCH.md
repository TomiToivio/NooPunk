# Computer-game influences: research and influence matrix (#728)

**Research and design only. Nothing implemented, no rule changed.**

> **Method, stated first because it bounds every claim below.** The listed games were
> **researched from public sources** — store pages, published reviews, and a developer
> interview — **not played** for this issue. Claims about their mechanics are therefore
> second-hand and should be treated as hypotheses to verify by play, not as field notes. Where
> a claim is a reviewer's opinion rather than a system description, it is marked.

---

## 1. The finding that organises everything else

The two hacking references and Citizen Sleeper arrive at the **same primitive** from different
directions:

| game | primitive |
|---|---|
| **Midnight Protocol** | **two actions per turn**, then the network responds |
| **DROP – System Breach** | **threads** = how many operations run at once; time is the wall |
| **Citizen Sleeper** | an **action budget** per cycle |
| **CWN combat** | an action economy per round |

**The shared primitive is the action budget, not the node graph.** The graph is a *presentation*
of where actions may be spent; the budget is the rule. That single realisation lets hacking,
social scenes and tactical combat share one engine instead of three minigames — which is the
non-negotiable principle this issue states.

## 2. Influence matrix

| game | subsystem it informs | verdict | tabletop procedure | Godot presentation | complexity / licensing |
|---|---|---|---|---|---|
| **Shadowrun: Dragonfall** | tactical missions, party builds, hub dialogue | **adopt structure** | CWN initiative/actions/cover; party of 2–4 | turn-based isometric map | high art cost; proprietary — mechanics only |
| **Disco Elysium** | dialogue, ideology, psychological characterisation | **adapt as presentation** | social checks; conditions (#698) | voice layer over CWN skills | text volume is the cost, not code; proprietary |
| **Citizen Sleeper** | time economy, clocks, scarcity | **adopt** | mission time as the scarce resource; clocks | clock widgets, cycle advances | low; proprietary |
| **DROP – System Breach** | graph hacking: nodes, threads, trace, firewall | **adapt** | node diagram + tokens; one check per action | interactive node graph | medium; proprietary — mechanics only |
| **Midnight Protocol** | hacking as turn-based node traversal; ICE, SysOp | **adapt** | same diagram, 2 actions/round, ICE as opposed check | grid with command line | medium; proprietary |
| **Blade Runner (EE)** | clue trails, atmosphere, interrogation | **investigate further** | interrogation as social check with cost | dialogue + scene reconstruction | adventure-game scope risk |
| **Observer: System Redux** | psychological investigation, environmental storytelling | **adapt atmosphere** | perception checks reveal what a room *means* | first-person scanning (out of scope for voxel top-down) | high production cost |
| **Song of Farca** | evidence board, remote camera investigation, deduction | **adopt the board** | evidence board as a shared table artefact | board UI with links | low-medium; proprietary |
| **Cyberpunk 2077** | city atmosphere, faction density | **avoid scope** | — | reference only | budget incompatible |
| **Deadeye Deepfake Simulacrum** | visual density at small scale | **adopt as visual target** | — | restrained palette, readable silhouettes | indie-scale, closest feasible |
| **Cloudpunk** | voxel city mood | **adopt as atmosphere reference** | — | voxel blocks + fog + neon | feasible for a small team |

**Licensing note, binding:** every game above is proprietary. Mechanics and systems are not
copyrightable; **text, dialogue, art, UI layouts and audio are.** No line of dialogue, no asset,
no copied interface layout. This is the same rule the rulebook sources already follow.

## 3. Graph hacking mapped onto CWN, with a paper example

CWN already has hacking as an action set with access states and risks. The graph games add
**spatial legibility**, not new rules.

| graph-game element | CWN equivalent | rule or presentation? |
|---|---|---|
| node | a host or device on the network | **presentation** of an existing access map |
| edges | connectivity (#344) | presentation |
| gate / lock | an access class requiring a check | **rule** — already exists |
| firewall health | trace/notice accumulating | **rule** — already exists |
| threads / concurrent ops | how many actions before the trace responds | **rule** — the action budget |
| ICE | an opposed check against a defender | **rule** |
| timer | mission time | **rule** |

**Paper version.** Draw six nodes on an index card: `entry — router — (cameras, records,
security)`. Place a token on `entry`. Each round the player gets **two actions**: move one node,
or use one node's action. Every action after the first two adds a trace die; at three trace the
security responds with an opposed check. The records node requires an access check. The whole
thing is played with a token, a die and the existing hacking rules.

**Digital version.** The same JSON: nodes, edges, access class, trace threshold. The Godot
scene draws it and lets the pointer spend the same two actions. **No rule is implemented twice**
— the adapter reads the map, the Python rules answer the checks.

## 4. Investigation workflow, identical in both media

Already built (#704): a **core clue** is obtained without a roll by a competent investigator;
**access** and **declared inquiry** are separate gates; **benefits** cost time, credits or a
favour; **hypotheses are the player's** and confidence is never system-set.

What the case-board games add is a **presentation**: evidence pins, links, and a place for the
player's own reasoning. All three references (Song of Farca's board, Observer's scanning, Blade
Runner's trail) are doing the same thing — **externalising the player's memory into the UI**.

**The rule this must not break:** the board shows *what the player has found*, never *what it
means*. A board that draws a suggested link has solved the case.

## 5. Shared-rules architecture

```
              data/rules/*.json  +  data/scenarios/*/case_graph.json
                              │
                    src/rules/* (authoritative)
                     │            │            │
        tabletop procedure   Python API    Godot adapters
         (paper, dice)      (tests, CI)   (rules_adapter, investigation_adapter)
                                              │
                                        presentation only
```

**Three invariants:**

1. **One state model.** A character, a scene, a network and a case are the same objects in the
   table and the game. `game_state.gd` holds them; `src/rules/*` decides them.
2. **Rules are authoritative; UIs are replaceable.** If two UIs disagree, the rule wins and the
   UI is wrong.
3. **No mechanic may exist only in the game.** If the Godot build needs something the paper
   rules cannot express, that is a **new rule** and must be specified, tested and written for
   the table first (AGENTS.md §14 order).

**What is legitimately UI-only:** camera, animation, tooltips, check previews *before* the roll
(never after-the-fact difficulty reveal in the table's favour), logs, convenience automation of
bookkeeping, sound.

## 6. Integrated vertical slice, rule by rule

**The night at Lakkahaltia**, one pass through every mode.

| beat | tabletop | Godot | shared rule |
|---|---|---|---|
| brief | referee reads the case; player picks skills | case file screen | `case_graph.json` |
| social | `2d6 + CHA mod + Talk` vs 8; pressing costs an action | dialogue with check preview | `wn_core.check` |
| clue analysis | core clue free with competence; benefit costs time | evidence board, no auto-links | `investigation.discover` |
| network intrusion | 2 actions/round on the token map; access check | node graph, same budget | hacking rules + budget |
| ideological choice | no check; a condition follows | three-option dialogue | `mental_load` (#698) |
| optional tactical | CWN combat | turn-based map | `cwn_combat` |

**Acceptance:** every row above is executable on paper with a die and a token; the digital build
adds only presentation; a zero-combat run completes the case.

## 7. Visual direction, feasible for a small team

- **Cloudpunk** is the mood reference, not the fidelity reference: **voxel blocks, fog, neon
  spill, heavy silhouette contrast**. Its readability at distance is what makes it affordable.
- **Deadeye Deepfake Simulacrum** shows the density achievable at indie scale: a restrained
  palette and strong shapes carry more atmosphere than texture count.
- **Concrete target for the slice:** one hospital interior, four rooms, a fixed camera per
  room, ~30 voxel prop models, emissive signs, one weather/fog pass. No open world, no crowd
  simulation, no facial animation — dialogue is portraits and text.
- **Readability rule:** every interactive node must be identifiable by **shape and icon**, not
  colour alone (also an accessibility requirement).

## 8. What would need *new* NoöPunk rules (not just a UI)

| proposed thing | is it new? | why |
|---|---|---|
| concurrent operations (DROP's *threads*) | **yes** | CWN has no concurrency concept; needs a rule and a table equivalent |
| network responding between turns | **partly** | CWN has trace, but not a per-turn escalation clock |
| evidence board auto-linking | **no** | presentation only — and should be refused |
| skill voices | **no** as presentation; **yes** if they become stats (see #716) |
| case-board scoring of hypotheses | **yes** | and it contradicts #704's rule that the system never judges a theory |

## 9. Cross-references

- **#724** — the CRPG design memo (loop, tactics-vs-narrative, slice). This document is the
  *influence* layer beneath it.
- **#704** — the GUMSHOE investigation layer, implemented and tested.
- **#719** — NoöPunk-original systems (faction ideology, noösphere, paradigm ladder).
- **#716** — attribute decision: A retained, which is why the slice above uses CWN codes.

## 10. Open questions for the author

1. Is the **action budget** the single economy across hacking, social and tactical — or does
   hacking get its own clock?
2. Are **concurrent operations** in scope at all? They are the one genuinely new rule the
   hacking references imply.
3. Is a **turn-based hacking map** the right presentation, or should hacking stay a list-based
   procedure with the graph as an optional aid?
4. Does the **case board** belong in the tabletop product, or only the digital one?
