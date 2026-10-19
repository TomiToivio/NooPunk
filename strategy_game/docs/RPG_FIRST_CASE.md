# The RPG-first vertical slice: one complete case (issue #502, Phase 1)

**Status:** playable, tested, non-canonical scenario content on the approved rules kernel. Refs
[#502](https://github.com/TomiToivio/NooPunk/issues/502),
[#461](https://github.com/TomiToivio/NooPunk/issues/461),
[#482](https://github.com/TomiToivio/NooPunk/issues/482),
[#516](https://github.com/TomiToivio/NooPunk/issues/516).

This is the delivery step the author directed to come first: *a playable, tested narrative /
investigation RPG — one coherent lightweight character and rules engine, dialogue, investigation,
physical / cyber / astral and PSI actions, dangerous but optional combat, persistent consequences, and
a short complete scenario* — for the faction-leader PC and four agents. No strategy simulation, tech
tree, global map or tactical UI is a prerequisite of it, and none is used here.

```bash
python -m strategy_game.casework                    # play the whole case headless
python -m strategy_game.casework --route confront --approach force
python -m strategy_game.casework --json             # the same run as one JSON record
python -m unittest strategy_game.tests.test_casework_spec \
                   strategy_game.tests.test_casework_session
```

## 1. What the case is

*The Second Shadow* — Helsinki, 2045, the Quarantine in force. A Reptilian raid hits a UNSA relocation
building in Kallio: two dead, one injured, one raider dead on the rear stair. A resident, Nila Ahola,
is in the secure ward carrying a Grey cortical stack she says she never agreed to. The building's
night caretaker insists there was a **second figure** on the stair, one no camera recorded.

The UNSA liaison wants `raider infiltration` signed before the noonday briefing. The player leads the
faction from the Helsinki Field Office, and the four agents are the canonical first-case party of
`rulebook/NEW_EDITION.md` — Laura Falk (*Minerva*), Dr. Harri Romppainen (*Dirty Harry*), Sebastian
Virtanen (*Ukuli*) and Laura Univaara (*Hecate*).

**The frame is canon; the incident is not.** The 2045 campaign present, the Field Office, UNSA, the
post-Crisis network and the Reptilian raids are the setting's own (`rulebook/20_…` §5 beat 9,
`rulebook/22_…`). The people, the building, the crime and its outcome are scenario fiction written for
this slice, and the agents' sheets are **placeholder playtest ratings** — the same status the rulebook
gives its own first case. Nothing here promotes a name, date or event into canon.

The opening dilemma is the rulebook's own: *"a credible victim of a Reptilian raid possesses a Grey
cortical stack, while the first independent psi-sensitive witness remembers an event that never
appeared on any camera. UNSA must determine what can be proved and what decisions can be made before
proof is complete."*

## 2. Structure: five scenes, five seats, one morning

A scene is one **turn** of the five-seat ledger: every character may attempt one thing, and leaving
the scene opens the next turn. No action is locked to a character — the `suggested_actor` is
presentation only, because a clue must never depend on one seat's action.

| # | Scene | Where | What can be attempted (skill, band) | What it yields |
|---|---|---|---|---|
| 1 | The Kallio stairwell | Field Office, 06:20 | duty log vs raid clock (COG Fair); the liaison aside (SAV Average); refuse to sign (WIL Average, create advantage) | `raid-log`, `liaison-deadline`, aspect *Room to work* |
| 2 | The woman with the stores unit | Meilahti clinic, 07:05 | sit with Nila (SAV Fair); scan the unit (COG Good); ask the clinic (SAV Fair); promise protection (SAV Average, create advantage) | `stack-card`, **`stack-manifest`** ×2 routes, *Nila's trust* |
| 3 | Forty-one seconds | the rear stair, 08:10 | walk and time it (INT Fair); pull the mesh log (**cyber gate** + COG Fair); search the landing (INT Average) | **`camera-gap`** ×2 routes, `claw-mark` |
| 4 | A shape worn like a coat | the caretaker's flat, 09:00 | supervise the reading (**PSI gate** + WIL Good); thermal record (COG Fair); ask why she stayed (SAV Average) | **`impression-double`** ×2 routes, `witness-fear` |
| 5 | Before noon | Field Office / loading bay, 11:40 | assemble the chain (no dice); pull the batch sign-out (COG Fair); read the file (INT Average); brief the liaison (SAV Fair, create advantage) | the **finding**, `batch-signature`, `lahtinen-file` |

Checks use **four skills of the character layer** — COG, INT, SAV, WIL — and every one is a plain Fate
overcome or create-advantage through `rpg.skills.check(..., ActionContext.INDIVIDUAL)`. The two special
layers are the ones that already exist, not new mechanics:

* **Cyber.** `pull_the_mesh_log` first asks
  `cyber.ConnectivityModel.resolve_access("local_only", "after_crisis", "field_netrunner")`. The mesh
  cannot be reached remotely in any era (the old Internet is behind the Blackwall); with a field port
  in the basement it is reachable, and only then is a COG check rolled. The reachability question is
  answered *before* the dice, which is issue #344's whole point.
* **PSI.** The reading is gated by `rpg.skills.require_capability(witness, "TELEPATH")` — a named
  `competence` TAG on the **witness's** sheet, refused before any dice. The party supervises; it does
  not thereby gain a psi capability, and no canonical agent is declared a telepath.

## 3. The clue chain is assembled, not handed over

Three facts, each reachable two ways, and none of them is the answer:

```
stack-manifest   the unit is a decommissioned stores telemetry unit, not a personal backup
camera-gap       the 41 missing seconds are the building's own logged maintenance window
impression-double a third figure on the stair, with no breath and no body heat
        │
        └── assemble → finding-empty-sleeve
            "an empty Grey sleeve, driven up the building's own service mesh during a real
             raid, to put a recorder into a woman nobody would believe"
```

`assemble()` is an action in scene 5 and a session operation. With all three fragments it is clean.
With two it can still be assembled — the case then carries the **`unproven-chain`** complication, the
finding is marked partial, and the faction's record says so (`case-chain-incomplete`). With fewer it
refuses and names exactly what is missing. A player who skips the lab, the mesh or the witness still
gets a weaker true story rather than a dead end.

The `claw-mark` clue exists to protect the other half of the reasoning: the raid itself was real.
Without it the chain would read as "nothing happened", which the evidence does not support.

## 4. Fail-forward, priced per action

The rulebook says *never make an essential clue depend on one successful check*; Fate says a failed
overcome may succeed at a serious cost, and a tie succeeds at a minor cost. The case file declares the
price of each:

| Result | What happens |
|---|---|
| success with style | clue/intel granted; a create-advantage aspect gets **two** free invocations |
| success | clue/intel granted; aspect gets one free invocation |
| tie | clue/intel granted, **minor cost** (a complication, or a point of stress) |
| failure | clue/intel still granted, **serious cost** (a complication plus stress, or a named consequence) |
| create-advantage failure | no aspect; the declared cost only — the clue never depended on it |

Costs are recorded, not narrated away: `nila-withdraws`, `liaison-doubt`, `clinic-logged-the-scan`,
`supervisor-watching`, `mesh-flagged-the-port`, `stores-clerk-alerted`, `personnel-flagged-the-read`,
`protection-promised`, `unproven-chain`. They are case-level flags, read by nothing as a number.

## 5. Three ways out, and combat is optional and dangerous

| Resolution | Needs | Closing check | Writes |
|---|---|---|---|
| **Close it on the record** | the assembled finding | SAV Good (passive) | objective *closed on the record*; `unsa-field-office-trust` (or `…-doubt` on a failed press); the corrected-statement intel |
| **Take it to the loading bay** | the finding or two fragments, **and** `batch-signature` | SAV Great **opposed** by Lahtinen (words) or REF **opposed** attack (force) | objective *closed with a detention*; trust + `kallio-residents-wary`; `lahtinen-in-custody`; the sleeve controller as a resource |
| **Refer it and walk away** | nothing | WIL Average | objective *referred to Internal Affairs*; `internal-affairs-referral` (or `…` + `case-left-open` on a failure) |

Combat is **one opposed exchange** — attack versus defence, then `rpg.scene.apply_hit`. There is no
initiative, no action economy, no cover, no round structure and no death rule: those are the author's
open rows **D34/D36**, and this slice does not decide them. A lost exchange writes a named mild
consequence (`Cutter wound, left forearm`) through the approved hit procedure, the suspect gets away,
and the case **still ends** — on the referral, with the injury on the sheet. That is what makes the
fight dangerous rather than decorative. Walking away is always available; the case can always be
closed without a fight.

## 6. What persists, and through which writer

Play never writes faction state. Two things persist mid-case, and both are already the campaign's:

* **injuries and stress** on the character sheets the campaign holds by identity — so `save_campaign`
  carries them;
* the **case ledger** (`clues`, `findings`, `complications`, `events`) in the session save.

The faction's books are written **once**, at `resolve()`, through the one tested writer
`campaign.missions.apply_mission_outcome`:

| Book | Example after the investigation ending |
|---|---|
| `objectives` | `Kallio raid case closed on the record` |
| `intelligence_ids` | `finding-empty-sleeve`, `stores-batch-serial`, `mesh-maintenance-window`, … |
| `reputation_labels` | `unsa-field-office-trust` |
| `resources` | `grey-sleeve-controller` (confrontation ending only) |
| the case's `evidence_ids` | every clue the party actually obtained |
| `campaign_notes` | one provenance-stamped audit entry per completed case |

Completion is **idempotent**: a second `resolve()` returns the record already applied and writes
nothing — no duplicate note, no duplicated evidence. That is a test, not a promise.

What a consequence *means* strategically (row **D35**) is deliberately not decided. The injury is a
named Fate consequence on a sheet; the faction-visible consequence is a named label or an id, never a
magnitude. No number is computed for reputation, intel or injury.

## 7. Save, load, determinism

`CaseSession.save()` writes one JSON document: the campaign payload (via `Campaign.to_dict`), the
scene index, the turn and who acted, used actions, clues, intel, findings, partials, complications,
events, wounds, scene aspects, the applied outcome — and the **dice state**
(`Random.getstate()`), so a case saved between scenes resumes into the same subsequent rolls and the
same ending an uninterrupted run produces. A save with a foreign `schema_version`, a different
`case_id` or an out-of-range scene index is refused rather than guessed into shape.

## 8. What is reused, and what is not invented

| Reused | From |
|---|---|
| one action per character per scene; five seats | `rpg.roster.TurnLedger`, `default_seats` (#461/#482) |
| checks, six individual skills, 4dF, outcomes | `rpg.skills.check`, `rpg.fate` (#389/#482) |
| free invocations, aspects, rerolls | `rpg.scene.Scene` |
| stress, consequences, hits | `rpg.scene.apply_hit` |
| cyber reachability and illegality classes | `cyber.resolve_access` (#344) |
| PSI capability gate | `rpg.skills.require_capability` (#482) |
| faction books and the audit trail | `campaign.state.Campaign`, `campaign.missions` (#502) |
| the case worksheet vocabulary | `campaign.case.Case` |

Not invented here: no new skill, no seventh attribute, no new dice, no new outcome rung, no combat
round, no initiative, no damage model, no recovery clock, no reputation number, no XP, no tech tree, no
mission board, no tactical UI. `strategy_game/RULEBOOK.md` keeps its **NO RULES APPROVED** status and
was not touched.

**Open author rows untouched:** D22 (strategic roster), D23 (allocation/advancement), D27 (project
dice band), D28 (what a domain TAG does), D29–D37 (the core-ruleset decisions), D34 (combat economy),
D35 (RPG→strategy propagation), D36 (cyber/astral harm tracks). The only numbers added are **difficulty
bands per action**, which Fate leaves to the GM — marked tuning in `casework/spec.py`.

## 9. Deliberately left out

* **Tactical layer.** No tile map, no renderer, no movement. The renderer row is **D38**; the tactical
  spike is `strategy_game/tactical/` and is separate.
* **Organisation and faction operations.** No mission board, assignment loop, resource economy,
  recruitment or project clock is used by the case. `projects.py`/`research.py` were not needed: the
  case has no artefact-sourced project, and inventing one to "reuse" the engine would be scope.
* **Character advancement, recovery and resleeving.** A consequence stays on the sheet; when and how
  it clears is not decided here.
* **Canonical character sheets.** The four agents' ratings are placeholders; issue #264's brief is not
  in this repository, and inventing ratings as canon would be inventing characters.
* **A campaign.** This is one complete case, not a case series. It is replayable (three endings, two
  routes to each fragment, dice) but it is one morning.

## 10. Files

```
strategy_game/casework/spec.py       the case declaration: scenes, actions, checks, clues, findings, resolutions
strategy_game/casework/session.py    the playable session: seats, ledger, checks, gates, chain, resolutions, save/load
strategy_game/casework/kallio.py     the packaged case, the party, the campaign builder
strategy_game/casework/demo.py       the headless play-through and its text report
strategy_game/casework/__main__.py   python -m strategy_game.casework
strategy_game/tests/test_casework_spec.py      declaration, campaign and gate contracts
strategy_game/tests/test_casework_session.py   play, fail-forward, three endings, save/load, determinism
```
