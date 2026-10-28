# CRPG design memo: old-school tactics + modern narrative (#724)

**Design memo and matrix. Nothing implemented, no rule changed.** Grounded in what the
repository already has rather than in a wish list.

---

## 1. The core loop

The single decision that shapes everything else: **is the investigation the game, or is the
tactical mission the game?** NoöPunk answers *investigation is the game, and violence is one of
its outcomes.*

```
  ARRIVE  →  OBSERVE  →  INTERPRET  →  ACT  →  CONSEQUENCE
   scene      clues        hypothesis     check      world state
                                    ↘  occasionally: TACTICAL ENCOUNTER
```

The loop is a **scene graph with a hypothesis layer on top**, which is exactly what
`data/scenarios/lakkahaltia/case_graph.json` already is (`entrance → corridor → reception →
patient_room`), and what `strategy_game.casework` already plays as a session.

**The loop must be playable without combat.** A full session in which no shot is fired has to
be a legitimate run, not a failure state — that is the Dragonfall/Disco split, and NoöPunk sits
closer to Disco while keeping Dragonfall's tactical option available.

## 2. When tactics, when everything else

| situation | resolution | why |
|---|---|---|
| finding a fact the character is competent for | **automatic** (GUMSHOE, #704) | a missed clue must never stop the game |
| reading what a fact means | **player inference, no check** | the pleasure of the genre |
| persuasion, deception, intimidation | **CWN `2d6` check**, with time and relationship cost | social is a full system, not a cutscene |
| stealth, access, forensics under pressure | **CWN `2d6` check**, failure costs time/Strain/notice | concrete stakes |
| violence that cannot be avoided or is chosen | **turn-based tactical**, CWN combat rules | Dragonfall's inheritance |
| a decision with no right answer | **no mechanic** — the player chooses, the world records it | ideology is not a skill check |

**The guardrail:** tactical combat is **opt-in or failure-forced**, never the default way to
advance. If a scene can be resolved by either, the narrative route must not be strictly worse.

## 3. Making a CWN-first engine readable

The table engine is correct and dense; a CRPG cannot show all of it. The rule is **inspectable,
not omnipresent**:

- **Always visible:** HP, System Strain, Effort, the current scene's discovered clues, the
  player's own hypotheses, time spent.
- **On inspection:** skill ranks, modifiers, the difficulty of a check *after* it is rolled,
  the derivation of the number.
- **Never shown:** the hidden truth of the case, the anomaly discriminator's answer, other
  characters' internal states.

That matches `game_state.gd` + `rules_adapter.gd` already: state is authoritative, the adapter
resolves, the UI reads.

## 4. Disco Elysium — what to study, what to refuse

| mechanic | verdict | note |
|---|---|---|
| skills as *voices* that interrupt with opinions | **adapt** | our skills are CWN's 19; a voice layer can be **presentation** over them, not 24 new stats |
| conversation skill checks that can fail forward | **adapt, scoped** | partial success only in dialogue (D50), never in the core kernel |
| thought cabinet / ideology as a build | **investigate** | closest analogue to the Laclaudian faction layer (#719) |
| the detective's body as a character | **adopt** | conditions (#698) already model this |
| total narrative dominance, combat effectively absent | **refuse** | guardrail: CWN tactical depth stays |

The important distinction: **Disco's voices are a presentation technique**, not a rules engine.
Adopting them as new stats would be a second attribute system (see #716).

## 5. Citizen Sleeper — the clock economy

| mechanic | verdict | note |
|---|---|---|
| **action economy per cycle** (limited actions before time advances) | **adopt** | maps cleanly onto CWN mission time, already a cost in #704 |
| **clocks** (multi-segment progress with visible pressure) | **adopt** | PbtA clocks, already permitted by D50 |
| **resource scarcity** (you cannot do everything) | **adopt** | time is the primary scarce resource, not money |
| **relationship arcs as mechanical** | **adapt** | a contact's state should gate options, not just flavour |
| dice-as-workers, a bespoke economy | **refuse** | second economy; CWN already has Effort/Strain/credits |

**The single most valuable import is the action budget.** It makes investigation feel like
pressure without adding a single new stat: you get N actions before the night moves on.

## 6. GUMSHOE in a computer game

Digital is where GUMSHOE's rule is *easier* than at a table (**the game can simply not generate
a stallable state**), and where it is easier to break:

- The engine must not hide a core clue behind a check it generated. `CaseGraph` validation
  already refuses a dead-ended scene at load time — that check moves from the referee's head
  into the build.
- **Do not auto-solve.** A game that highlights the correct hypothesis has removed the game.
  `Hypothesis` confidence is player-set (#704) precisely so the UI cannot nudge it.
- **The anomaly gate must be able to return "inconclusive"** — an attempted discriminator that
  does not decide is a result, not a failure.

## 7. Fate and PbtA in dialogue, quests and factions

| tabletop | digital expression | boundary |
|---|---|---|
| aspect | a tag on a character, scene or faction the player can invoke | one tag per action; no stacking (D42) |
| compel | a dialogue option that costs the character something to refuse | must be a *choice*, never an automatic penalty |
| PbtA clock | quest/faction progress with visible segments | never a second progress system beside case time |
| GM move | authored escalation triggered by a failed check or elapsed clock | authored, not generated |

**No LLM may decide a modifier.** `narrative_layer.validate_proposal` already enforces this in
Python; the CRPG inherits the rule.

## 8. Ideology, noösphere, psi, cybernetics, NHI — feeding both modes

| system | narrative mode | tactical mode |
|---|---|---|
| Laclaudian factions (#719) | who will talk to you, what a signifier buys | who shows up, what they are armed with |
| noösphere field (#719) | what is sayable in a place | PSI difficulty modifier, bounded −2..+2 |
| PSI (#572) | what you can perceive without instruments | Effort as a tactical resource |
| cybernetics | what you can interface with, what it costs in Strain | equipment and Strain ceiling |
| NHI phenomena | the ambiguity that must survive to the end | an encounter you may not be able to fight |

The design constraint: **each system must have a non-combat expression**, or the game collapses
into a combat game with lore attached.

## 9. Shared rules vs presentation

| shared, identical | presentation-only |
|---|---|
| `src/rules/*` (checks, combat, injury, investigation, conditions) | skill voices, dialogue framing |
| `data/scenarios/*/case_graph.json` | camera, map, portraits |
| `data/rules/*.json` contracts | tooltips, check previews |
| `godot/core/investigation_adapter.gd`, `rules_adapter.gd` | animation and timing |

**Rule:** if it changes a number, it lives in `src/rules/` and both the table and the game read
it. If it only changes how a number is *shown or heard*, it lives in the Godot layer.

## 10. Mechanics-to-inspiration matrix

| mechanic | source | verdict | tabletop | CRPG | slice | kind |
|---|---|---|---|---|---|---|
| core clue, competence-as-competence | GUMSHOE | **adopt** | yes | yes | **yes** | core |
| action budget per cycle | Citizen Sleeper | **adopt** | yes | yes | **yes** | core |
| clocks | PbtA | **adapt** | yes | yes | **yes** | core |
| conditions, four-layer exposure | EP → #698 | **adopt** | yes | yes | **yes** | core |
| turn-based tactical combat | CWN / Dragonfall | **adopt** | yes | yes | **yes** (optional) | core |
| skill voices | Disco Elysium | **adapt** | no | yes | later | presentation |
| thought cabinet | Disco Elysium | **investigate** | maybe | maybe | no | core (maybe) |
| aspect invoke | Fate | **adapt** | yes | yes | no | core |
| compel as dialogue cost | Fate | **adapt** | yes | yes | **yes** | core |
| investigative pool | GUMSHOE | **avoid** | — | — | — | core |
| dice-as-workers economy | Citizen Sleeper | **avoid** | — | — | — | core |
| sanity/stability track | CoC | **avoid** | — | — | — | core |
| procedural case generation | — | **investigate** | no | later | no | core |

## 11. Vertical slice — concrete and small

**One night in Lakkahaltia. Four scenes, one optional fight, one choice that has no right answer.**

Reuses what exists; nothing new is invented.

1. **Entrance** — `case_graph.json` scene 1. Clue is passive (the sign-in sheet), so the player
   gets it on arrival. One dialogue with the night nurse; a `2d6` check decides whether she
   volunteers the rota change, and *time* is the cost of pressing her.
2. **Corridor → Reception** — the action budget bites: the player can search the corridor, read
   the rota, or question the porter, but not all three before the shift changes.
3. **Patient room 16** — an **ideological/psychological choice** with no correct answer: confront
   the patient, refer them, or record the anomaly. Each sets a different condition (#698) and a
   different faction disposition.
4. **Optional tactical encounter** — if the player forced entry or confronted without
   preparation, a short turn-based scene follows using CWN combat. It is **avoidable** and, if
   avoided, the case is still completable.

**Acceptance for the slice:** a full run with zero combat is possible; the anomaly stays
ambiguous at the end; no core clue is ever gated behind a roll.

## 12. Atmosphere: a grounded world, and the Weird as evidence (issue question 9)

The atmosphere is the one thing a *presentation* decision can destroy while every rule stays
correct. The rule that keeps it: **the world is rendered ordinary, and the Weird arrives only as
evidence and consequence.** Nothing in the fiction is strange until a clue says it is.

| constraint | why |
| --- | --- |
| **No ambient strangeness.** Lighting, sound and art stay hospital-corridor ordinary; the palette does not "go weird" as a mood signal. | A mood shift pre-announces the answer, which is the presentation version of the anomaly gate being bypassed. |
| **The anomaly is rendered only after a discerner is attempted.** `src/rules/anomaly_gate.py` records attempts; the presentation layer may shift only on a recorded clue, never on elapsed time or a dice result. | The gate exists so the weird reading must be *earned*; the renderer must not do the earning for the player. |
| **The mundane must stay renderable at every moment.** Every anomalous beat has a visible ordinary counterpart in the same scene: a power cut beside a figure in the mirror, a filing error beside a second birth date. | If the ordinary reading cannot be staged, the case is not ambiguous — it is a reveal with a delay. |
| **The reader's vocabulary is clinical and institutional, not gothic.** Nurses write rosters; doctors write amendments; the state writes referral forms. | The horror in *Riget* and *Maniac* is bureaucratic before it is supernatural. |
| **One Weird beat per case, at most, that costs the player something.** | Scarcity is what makes it land; a second one turns the setting into fantasy. |
| **High-stakes tactical is a consequence, never a random encounter.** Violence follows a chosen confrontation or a forced entry, and the case remains completable without it. | The memo's loop rule: a session with no shot fired must be a legitimate run. |

Two dials, both data rather than prose:

1. **The case's hypothesis families** (`case_graph.json`) determine what the UI may show as
   contested: while mundane, deliberate, psychological and anomalous are all open, every scene is
   presented as an ordinary institutional problem.
2. **The paradigm ledger** (#689 stage 2, still a document) would set the *world's* baseline: how
   much of the Weird is publicly admissible in this district at this time. Until that lands, the
   default is "publicly: none, privately: rumour", which is what the Lakkahaltia case already
   assumes.

The test of the atmosphere, in one line: **a player who never resolves the anomaly should still be
able to describe the case as a hospital records scandal that bothered them.**

Companion reading: [`ISSUE_724_CRPG_DESIGN_SYNTHESIS.md`](ISSUE_724_CRPG_DESIGN_SYNTHESIS.md)
(#726) covers the influence synthesis; this section covers how it is *rendered*.

---

## 13. What this memo does not decide

Numbers (action budgets, clock lengths, condition severities), whether the thought cabinet
belongs, and whether procedural cases are ever in scope. All are author decisions.
