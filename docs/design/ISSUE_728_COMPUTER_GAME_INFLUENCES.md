# #728 — computer-game influences and the shared rules-to-interface architecture

**Status:** research and design. Not an implementation request, not canon, no code changed.

Companion documents: `ISSUE_724_CRPG_DESIGN_MEMO.md` and `ISSUE_724_CRPG_DESIGN_SYNTHESIS.md` (the CRPG
baseline: loop, Disco/Citizen Sleeper study, Fate/PbtA in dialogue, vertical slice), and
`ISSUE_704_GUMSHOE_INVESTIGATION.md` (the investigation layer). This document does not repeat them; it
adds the **game-specific** research and the **interface architecture** they do not cover.

---

## 0. Method, and what "observed" means here

No listed title was played for this issue. Notes are drawn from published descriptions, store pages and
reviews, so:

- **OBSERVED** — a documented feature of the shipped game (mechanic or UX pattern that reviews and
  official descriptions agree on).
- **PROPOSED** — NoöPunk's adaptation. Always labelled, never presented as a fact about the source game.
- **AVOID** — a feature that would break the one-engine rule or the licence.

Any claim about how a game *feels* is PROPOSED, not OBSERVED. The value of the matrix is the mapping, not
a review score.

---

## 1. Influence matrix

| game | what it demonstrably does (OBSERVED) | NoöPunk subsystem | verdict | tabletop procedure | Godot presentation | risk |
|---|---|---|---|---|---|---|
| **Shadowrun: Dragonfall** | turn-based squad combat on a grid; action points; a separate node-based Matrix layer for hacking; dialogue options gated by character tags | tactical encounters; hacking; party | **ADAPT** | CWN initiative, actions, attack/skill checks on a grid drawn on paper | tactical map, AP pips, same rolls surfaced in a log | the Matrix as a *second* ruleset — see §3 |
| **Disco Elysium** | 24 skills that speak as voices; white/red checks; Thought Cabinet; health and morale as two pools | social/narrative checks; inner voices | **ADAPT (voice only)** | referee voices the highest-relevant skill; checks already exist | skill-voice barks over dialogue | a second mental-damage economy — #698 conditions already own this |
| **Citizen Sleeper** | dice allocated to actions each cycle; clocks and drives; a time economy driven by scarcity | pressure and clocks | **AVOID the dice economy**; adopt clocks | existing clocks; one turn = one scene | clock ring + cycle summary | dice-as-actions is a second engine |
| **DROP – System Breach** | node-graph intrusion; breach nodes, escalate, trace/alert | hacking UI | **ADAPT (view only)** | nodes drawn as boxes, edges as links | interactive graph, same actions | inventing actions the rules do not have |
| **Midnight Protocol** | terminal/keyboard interface; commands typed against a network; stealth vs force | hacking *feel*; command vocabulary | **ADAPT (vocabulary)** | players speak the command verbs aloud | terminal overlay, tab-complete | a bespoke command grammar that is not CWN's verbs |
| **Blade Runner (1997)** | real-time adventure; photo enhancement as evidence tool; a KIA-style clue linker; multiple endings from evidence choices | case board; evidence analysis | **ADAPT (case board)** | index cards + string | case board over existing state | pixel hunting / adventure-game logic |
| **Observer** | interrogation and "dream-eater" sequences; psychological investigation | interrogation; psychic evidence | **ADAPT (scene framing)** | a scene with a stated risk | first-person-ish interrogation framing | making PSI a minigame |
| **Song of Farca** | hacker-protagonist investigation; surveillance and evidence assembly under time pressure | surveillance; time pressure | **ADAPT (situations)** | clocks + evidence ledger | camera/log views | scripted deductions |
| **Cyberpunk 2077** | dense city, factions, braindance reconstruction | atmosphere; braindance as evidence | **AVOID the combat model**; adapt braindance | a reconstruction is a `Forensics` check producing a fact | scene playback | production values mistaken for design |
| **Deadeye Deepfake Simulacrum** | dense, stylised low-budget presentation | visual density | **ADAPT (scope model)** | — | tight palette, few assets, high contrast | imitating its action gameplay |
| **Cloudpunk** | voxel city, neon fog, driving-through-mood presentation | city mood | **ADOPT (primary visual reference)** | — | voxel blocks + fog + light | open-world driving scope |

---

## 2. The one-engine rule, stated as an architecture

> **Rules are authoritative; interfaces are replaceable.**

One canonical game state; every interface — paper sheet, GM procedure, Godot panel — reads and writes
*that* state and nothing else. A UI may add **affordances** (camera, animation, logs, auto-bookkeeping,
sorting, search). A UI may not add **choices, probabilities, costs or consequences**.

| activity | canonical state | rules (authoritative) | paper affordance | digital affordance |
|---|---|---|---|---|
| tactical confrontation | positions, initiative order, HP/Strain, conditions | CWN initiative, actions, attack/save/skill checks | grid sketch, tokens, scratch HP | map, AP pips, hover ranges, roll log |
| conversation / ideology | disposition, faction standing, conditions, known facts | CWN social checks; #719 hegemony tracks | index card per faction | dialogue UI, standing meter |
| time / pressure | clocks, turn count, deadlines | existing clocks; one scene = one turn | ticks on paper | clock ring, cycle summary |
| hacking | nodes, access state, alert clock, trace | `src/rules/cwn_hacking.py` | node diagram + tokens | clickable graph |
| investigation | facts found, discriminators attempted, hypotheses | `src/rules/investigation.py`, `anomaly_gate.py` | case board, string | case board view, filters |
| exploration | scene graph, discovered exits, danger state | CWN movement/perception checks | map + notes | scene navigation |

**The test for any proposed feature:** could a table run it with paper and the same numbers? If no, it is
a new rule and goes through design review — not into a UI.

---

## 3. Graph hacking, mapped onto CWN rather than beside it

`src/rules/cwn_hacking.py` already owns the mechanics: `access_pool(intelligence_modifier, program_skill,
deck_bonus)`, `security_difficulty(...)`, `hacking_check(...)` with a flat `WIRELESS_PENALTY = -2` and
`VR_CROWN_PENALTY = -1`, and an `AlertClock` where `FAILURES_PER_ALERT = 2` and
`ALERT_ACTIONS_TO_ALERT = 2`.

**A host is a graph; the graph is a picture of that state.** Nodes are devices, accounts, daemons and
archives. Edges are connections you must already have permission or a successful action to cross. Nothing
in the graph introduces a roll the module does not already make.

### Paper example — one node, one action

```
[Reception terminal] --1--> [Ward server] --2--> [Patient records]
         |                        |
       (camera)                (daemon)
```

1. The decker is on the reception terminal. Crossing **edge 1** to the ward server requires a
   `security_difficulty` for the server; the player rolls `hacking_check(...)`.
2. A failure records `AlertClock.record_failure()`; two failures raise one alert action, two alert actions
   raise the alert — the clock is on the table as two boxes.
3. The daemon on the ward server may spend its action to `record_alert_action()`.

Everything on that diagram is a rule that already exists. The diagram is how a table remembers it.

### Digital equivalent

The same JSON — nodes, edges, security values, daemon flags — rendered as boxes; clicking an edge runs the
same `hacking_check` through the same adapter pattern as `godot/core/rules_adapter.gd`. **What the UI may
add:** hover reveals the check's inputs; the clock animates; the log shows each roll. **What it may not
add:** a reflex component, a timing bar, or an action the module lacks.

DROP and Midnight Protocol are valuable for *legibility* (what a breach looks like) and for *verb
vocabulary* (what you say you are doing). They are not the source of the rules.

---

## 4. Investigation, shared

`src/rules/investigation.py` gives the fact to a competent declaration and never rolls for it;
`anomaly_gate.py` records attempted discriminators and refuses an anomalous conclusion while any core
discriminator is unrun. The case board is a **view of that state**: facts found, discriminators attempted,
hypotheses live. Blade Runner's clue-linker and Song of Farca's evidence assembly are good *presentations*
of exactly this state and bad *sources of it* — a board that draws a connection the table has not
established would be the UI inventing a fact.

Pixel hunting is excluded by the same rule: a fact that exists must be reachable by a declared competent
inquiry, not by clicking the right pixel. If the game needs a highlight to make a fact findable, that is an
affordance, and it must never be the only route.

---

## 5. Vertical slice — briefing → social → clue → intrusion → ideology → tactics

| beat | what happens | rule | where it lives |
|---|---|---|---|
| 1. Briefing | the case, the client, the clock | clock + scene framing | tabletop: GM; digital: briefing screen |
| 2. Social | the ward administrator refuses records | CWN `Talk`/`Connect` check vs a stated difficulty | same check both sides |
| 3. Clue analysis | the roster gap and the future-tense file | guaranteed fact (competent declaration) + `Forensics`/`Know` check for the reading | `investigation.py` |
| 4. Intrusion | the ward server, one daemon | `hacking_check` + `AlertClock` | `cwn_hacking.py` |
| 5. Ideological choice | whose account the evidence serves | #719 hegemony: Articulation / Legitimacy / Frontier | tabletop: faction card; digital: standing panel |
| 6. Optional tactics | a security response | CWN initiative, actions, attack and save checks | grid / map |

Every row is one rule executed twice through different interfaces. The slice is deliberately small: two
rooms, three NPCs, one network, one possible fight.

---

## 6. Visual direction, at small-team scale

**Primary reference: Cloudpunk** — voxel blocks, heavy fog, saturated neon, wet reflections, a city read
mostly at distance and in motion. **Secondary: Deadeye Deepfake Simulacrum** — density bought with palette
and contrast rather than asset count.

What that actually means for scope:

- **isometric or fixed-angle 3D**, not first person; the camera does the atmosphere, the team does not;
- **voxel/proxy geometry** for exteriors, hand-authored interiors only where play happens;
- **one city block per chapter**, not a city; fog and lighting hide the boundary;
- **2D portraits + text** for conversation — the cheapest depth in the genre;
- **UI-first subsystems**: the case board and the node graph are 2D panels and are where the game looks
  most like itself;
- **no driving, no crowds, no open world** — those are where Cloudpunk's budget went, and they buy mood,
  not decisions.

Atmosphere is cheap; *scale* is expensive. The design should spend on density of meaning, not square
kilometres.

---

## 7. What would require NEW NoöPunk rules

This is the list that matters, because everything else is a UI.

| idea | source | needs a new rule? | why / what it would be |
|---|---|---|---|
| Thought Cabinet / internalising ideas | Disco Elysium | **YES** | a second progression track; would need its own design (and would collide with #698 conditions) |
| dice-as-actions per cycle | Citizen Sleeper | **YES** | a new action economy beside CWN turns; rejected as a second engine |
| braindance reconstruction | Cyberpunk 2077 | **NO** | a `Forensics` check producing a fact through the existing clue layer |
| clue-linker / KIA | Blade Runner | **NO** | a view over `investigation.py` state |
| node-graph hacking | DROP / Midnight Protocol | **NO** | a view over `cwn_hacking.py` |
| ideology standing | Disco Elysium / #719 | **YES (already proposed)** | #719's Articulation/Legitimacy/Frontier; needs acceptance before any UI |
| psychological "voices" | Disco Elysium | **NO (presentation)** | referee/UI voices the relevant skill; the check is unchanged |
| real-time pressure | Blade Runner / Song of Farca | **NO** | clocks already exist; real time is an affordance, not a rule |

Everything marked NO is safe to prototype. The two marked YES must not enter a UI before the rule exists,
or the interface will become the rules.

---

## 8. Acceptance criteria, mapped

1. **Game-by-game mechanics/UX/limitations** → §1 matrix, OBSERVED/PROPOSED separated, method stated in §0.
2. **Influence matrix with adopt/adapt/avoid** → §1, including the tabletop procedure and Godot presentation columns.
3. **Shared-rules architecture** → §2, with the affordance/choice test.
4. **Graph hacking vs CWN, paper example + digital** → §3, mapped onto real constants in `cwn_hacking.py`.
5. **Investigative workflow, identical both sides** → §4.
6. **One integrated vertical slice, rule-by-rule** → §5.
7. **Restrained visual direction, small-team scope** → §6.
8. **What needs new rules** → §7.
9. **Cross-references, no duplication** → header; #724 covers the CRPG loop, #704 the investigation layer, #719 the ideology tracks.

## 9. What this document does not decide

No new rule is adopted; #719's hegemony tracks remain proposals; the visual direction is a constraint, not
an art bible; and no Godot work starts from this document. The next step, if any, is a single vertical-slice
prototype issue that reuses `godot/core/rules_adapter.gd` and adds no mechanics.
