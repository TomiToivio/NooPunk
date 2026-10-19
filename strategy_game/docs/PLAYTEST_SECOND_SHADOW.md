# Playtest evidence: *The Second Shadow* (issue #516)

**Status: playtest evidence, not a decision, not a sign-off, and not a rule.** This document
measures the shipped RPG-first case (`strategy_game/casework/`, `python -m strategy_game.casework`)
and reports what it found. It changes no difficulty, no skill, no outcome band, no resolution
requirement and no author decision row. Every rules question it raises is marked as the author's
call; the rows it bears on (D29–D38) stand exactly as they are in
[`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md).

Refs [#516](https://github.com/TomiToivio/NooPunk/issues/516),
[#502](https://github.com/TomiToivio/NooPunk/issues/502),
[#461](https://github.com/TomiToivio/NooPunk/issues/461),
[#482](https://github.com/TomiToivio/NooPunk/issues/482).
Case design record: [`RPG_FIRST_CASE.md`](RPG_FIRST_CASE.md).

Every table below is printed by the harness, pasted unedited; the prose reads them.

---

## 1. Method

One command reproduces every number in this document:

```bash
python -m strategy_game.tools.playtest_second_shadow --seeds 300
python -m strategy_game.tools.playtest_second_shadow --seeds 300 --json playtest.json
```

**300 seeds per route and per policy, seeds 0–299** — about **9,200 runs** in roughly one minute on
one core. The harness drives `CaseSession` / `CaseFile` directly (no shelling out per run) and reads
every number back from the session's own event log and `report()`, so nothing here is narrated.

**The four route replays are `casework.demo.play` itself**, unchanged, including its two
save/reload cycles: `investigate`, `confront --approach pressure`, `confront --approach force`,
`refer`. *Naming note:* the shipped code calls the routes `investigate` / `confront` / `refer` and the
approaches `pressure` / `force`; "close", "refer" and "words" / "force" name the same things
elsewhere. The playtest uses the code's names because it replays the code.

**Policies** model parties rather than scripts:

| policy | what it does |
|---|---|
| `thorough:<ending>` | attempts **every available action in every scene**, then closes on the requested ending; puts the **best available specialist** on each check and spends free invocations |
| `minimal:<ending>` | takes only the actions that ending needs — the floor of check load |
| `random` | uniform choice among the actions on offer, 5% chance per decision of walking away and referring — the dead-end probe |
| `thorough-no-aspects:<ending>` | the thorough party, ignoring free invocations: what the aspect economy is worth |
| `thorough-naive-seats:<ending>` | the thorough party taking the suggested character, then whoever is free, instead of the best specialist |

**Probes:** the thorough party forbidden one skill at a time (6 × 300 runs); every check forced to
fail; every check forced to succeed; a party that skips the caretaker (2 fragments); a party that
skips the caretaker and the stairwell (1 fragment); and one forced lost exchange that pins the
`taken out` state.

**Determinism is not sampled:** all 1,200 route replays and 120 thorough runs are played **twice**
and compared on the full case report *and* the campaign payload, serialised with sorted keys; 120
runs are also saved mid-play, reloaded, finished, and compared with an uninterrupted run. The demo
routes are additionally compared on their **printed transcript**.

**What the harness does not model**, and therefore what these numbers do not measure: Fate-point
spending, rerolls, player judgement beyond "take the best specialist and spend what you have", the
tactical layer, or a campaign across cases. The four agent sheets are the case's own **placeholder
playtest ratings**, so absolute difficulty is a property of *this case with these sheets*, not a
verdict on final characters. Every check in the case is `ActionContext.INDIVIDUAL`: 0 faction-agent
checks, so nothing here tests the strategic roster (D22, D30).

---

## 2. Pace

The case declares five scenes, seventeen actions and three endings. The scripted routes play exactly
five scenes and roll **15 checks** (12 for `refer`); a party that attempts everything rolls **17**.
The floor is **5 checks** for the strongest ending, **6** for the detention, and **1** for the
referral.

| route | runs | ending | degraded | checks mean | checks p10–p90 | rolls mean | 3/3 chain | partial | complications mean | party wounded | party taken out |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `investigate` | 300 | closed_by_evidence (300) | 0.0% | 15.0 | 15–15 | 15.0 | 100.0% | 0.0% | 3.41 | 14.7% | 0.0% |
| `confront:pressure` | 300 | closed_by_confrontation (155), closed_by_withdrawal (145) | 48.3% | 15.0 | 15–15 | 15.52 | 100.0% | 0.0% | 3.41 | 14.7% | 0.0% |
| `confront:force` | 300 | closed_by_confrontation (210), closed_by_withdrawal (90) | 30.0% | 15.0 | 15–15 | 15.7 | 100.0% | 0.0% | 3.41 | 26.7% | 0.7% |
| `refer` | 300 | closed_by_withdrawal (300) | 0.0% | 12.0 | 12–12 | 12.0 | 100.0% | 0.0% | 2.65 | 14.7% | 0.0% |

Outcome of the closing check, per route:

| route | failure | tie | success | style |
|---|---|---|---|---|
| `investigate` | 54 | 54 | 142 | 50 |
| `confront:pressure` | 90 | 55 | 82 | 73 |
| `confront:force` | 43 | 47 | 97 | 113 |
| `refer` | 31 | 34 | 130 | 105 |

Scenes played before the ending:
| policy / requested | scenes per run |
|---|---|
| `thorough:evidence` | 5: 300 |
| `minimal:evidence` | 5: 300 |
| `thorough:confront` | 5: 300 |
| `minimal:confront` | 5: 300 |
| `thorough:refer` | 5: 300 |
| `minimal:refer` | 1: 300 |
| `random` | 1: 40, 2: 50, 3: 26, 4: 23, 5: 161 |
| `thorough-no-aspects:evidence` | 5: 300 |
| `thorough-naive-seats:evidence` | 5: 300 |
| `thorough-no-aspects:confront` | 5: 300 |
| `thorough-naive-seats:confront` | 5: 300 |

No run in any policy ended **later** than five scenes, and none can: `end_scene()` only moves
forward and nothing returns to an earlier scene. The five-scene shape is therefore a ceiling, not a
guarantee: the floor is one scene, and a referral taken in the first scene is a legal, complete
playthrough (`minimal:refer`: 1 scene, 1 check, 0 clues).

Pace inside a policy is uniform because the shape is fixed — every scripted route takes exactly 15
checks, so the p10–p90 span is 0 for every route and every scripted policy. The only variable cost
is the arbitrary party's (2–13 checks).

---

## 3. Lethality and cost

Every scene action declares a **minor** price for a tie and a **serious** price for a failure, and
every one of those prices lands. No clue is ever withheld: a tie and a failure both grant it.

| run family | runs | party wounded | suspect wounded | party taken out | stress boxes mean | any stress | complications mean | named consequence |
|---|---|---|---|---|---|---|---|---|
| `investigate` | 300 | 14.7% | 0.0% | 0.0% | 1.06 | 70.3% | 3.41 | 14.7% |
| `confront:pressure` | 300 | 14.7% | 0.0% | 0.0% | 1.06 | 70.3% | 3.41 | 14.7% |
| `confront:force` | 300 | 26.7% | 70.0% | 0.7% | 1.08 | 71.7% | 3.41 | 26.7% |
| `refer` | 300 | 14.7% | 0.0% | 0.0% | 0.96 | 66.0% | 2.65 | 14.7% |
| `thorough:evidence` | 300 | 19.0% | 0.0% | 0.3% | 1.09 | 68.7% | 3.48 | 19.0% |
| `minimal:evidence` | 300 | 0.0% | 0.0% | 0.0% | 0.48 | 41.0% | 1.2 | 0.0% |
| `thorough:confront` | 300 | 19.0% | 0.0% | 0.3% | 1.09 | 68.7% | 3.48 | 19.0% |
| `minimal:confront` | 300 | 0.0% | 0.0% | 0.7% | 0.53 | 43.7% | 1.38 | 0.0% |
| `thorough:refer` | 300 | 19.0% | 0.0% | 0.3% | 1.09 | 68.7% | 3.48 | 19.0% |
| `minimal:refer` | 300 | 0.0% | 0.0% | 0.0% | 0.0 | 0.0% | 0.0 | 0.0% |
| `random` | 300 | 6.7% | 1.0% | 0.0% | 0.51 | 37.3% | 1.51 | 6.7% |
| `thorough-no-aspects:evidence` | 300 | 19.0% | 0.0% | 0.3% | 1.09 | 68.7% | 3.48 | 19.0% |
| `thorough-naive-seats:evidence` | 300 | 19.0% | 0.0% | 0.0% | 1.49 | 85.7% | 4.42 | 19.0% |
| `thorough-no-aspects:confront` | 300 | 19.0% | 0.0% | 0.3% | 1.09 | 68.7% | 3.48 | 19.0% |
| `thorough-naive-seats:confront` | 300 | 19.0% | 0.0% | 0.0% | 1.49 | 85.7% | 4.42 | 19.0% |

Named consequences written, by character (runs with at least one):

| run family | consequences (runs with at least one) |
|---|---|
| `investigate` | laura_univaara 44 |
| `confront:pressure` | laura_univaara 44 |
| `confront:force` | laura_univaara 44, pc_leader 43 |
| `refer` | laura_univaara 44 |
| `thorough:evidence` | laura_univaara 57 |
| `minimal:evidence` | — |
| `thorough:confront` | laura_univaara 57 |
| `minimal:confront` | — |
| `thorough:refer` | laura_univaara 57 |
| `minimal:refer` | — |
| `random` | laura_univaara 19, pc_leader 1 |
| `thorough-no-aspects:evidence` | laura_univaara 57 |
| `thorough-naive-seats:evidence` | laura_univaara 57 |
| `thorough-no-aspects:confront` | laura_univaara 57 |
| `thorough-naive-seats:confront` | laura_univaara 57 |

Complications written by the thorough party (evidence ending, 300 runs):

| complication | runs | share of runs |
|---|---|---|
| `supervisor-watching` | 121 | 40.3% |
| `clinic-nurse-nervous` | 106 | 35.3% |
| `scene-contaminated` | 105 | 35.0% |
| `clinic-logged-the-scan` | 105 | 35.0% |
| `protection-promised` | 65 | 21.7% |
| `thermal-log-sealed` | 65 | 21.7% |
| `liaison-doubt` | 63 | 21.0% |
| `liaison-impatient` | 63 | 21.0% |
| `nila-guarded` | 59 | 19.7% |
| `personnel-flagged-the-read` | 54 | 18.0% |
| `duty-log-thin` | 51 | 17.0% |
| `stores-clerk-alerted` | 50 | 16.7% |
| `mesh-flagged-the-port` | 44 | 14.7% |
| `witness-frightened` | 32 | 10.7% |
| `deadline-tightened` | 25 | 8.3% |
| `nila-withdraws` | 24 | 8.0% |
| `duty-log-incomplete` | 12 | 4.0% |

Read together: **the case is not lethal, but it is not free.** A party that plays everything pays
about 3.5 named complications and 1.1 stress boxes per run (the scripted routes: 3.4 and 1.1). The
only named consequence in normal play is Hecate's *"A nail behind the eyes"* from a failed psi
reading — 19.0% of thorough runs, 14.7% of the scripted routes (the script reaches that check on a
different dice stream). The only physical injury in the case is the confrontation's `Cutter wound,
left forearm`, which lands on the leader in 14.3% of `force` runs; the same exchange wounds the
suspect in 70.0% of them.

### Fail-forward price, per action (thorough party, all endings, 900 rolls each)

| action | check | rolls | style | success | tie | failure | price charged | named consequence |
|---|---|---|---|---|---|---|---|---|
| `briefing/read_the_duty_log` | COG Fair (2) | 900 | 39.3% | 39.7% | 17.0% | 4.0% | 21.0% | 0.0% |
| `briefing/take_the_liaison_aside` | SAV Average (1) | 900 | 59.3% | 33.0% | 5.3% | 2.3% | 7.7% | 0.0% |
| `briefing/hold_the_attribution` | WIL Average (1) | 900 | 62.7% | 29.0% | 7.3% | 1.0% | 8.3% | 0.0% |
| `victim/interview_nila` | SAV Fair (2) | 900 | 34.0% | 45.0% | 13.0% | 8.0% | 21.0% | 0.0% |
| `victim/scan_the_stack` | COG Good (3) | 900 | 15.0% | 50.0% | 16.7% | 18.3% | 35.0% | 0.0% |
| `victim/ask_the_clinic` | SAV Fair (2) | 900 | 18.0% | 46.7% | 17.7% | 17.7% | 35.3% | 0.0% |
| `victim/promise_protection` | SAV Average (1) | 900 | 39.0% | 39.3% | 14.3% | 7.3% | 21.7% | 0.0% |
| `stairwell/read_the_stairwell` | INT Fair (2) | 900 | 13.0% | 46.7% | 22.7% | 17.7% | 40.3% | 0.0% |
| `stairwell/pull_the_mesh_log` | COG Fair (2) | 900 | 40.7% | 44.7% | 9.3% | 5.3% | 14.7% | 0.0% |
| `stairwell/search_the_landing` | INT Average (1) | 900 | 19.3% | 45.7% | 17.0% | 18.0% | 35.0% | 0.0% |
| `witness/supervise_the_reading` | WIL Good (3) | 900 | 16.7% | 45.3% | 19.0% | 19.0% | 38.0% | 19.0% |
| `witness/check_the_thermal_record` | COG Fair (2) | 900 | 35.0% | 43.3% | 11.3% | 10.3% | 21.7% | 0.0% |
| `witness/ask_her_why_she_stayed` | SAV Average (1) | 900 | 59.3% | 30.0% | 8.7% | 2.0% | 10.7% | 0.0% |
| `resolution/pull_the_batch_signout` | COG Fair (2) | 900 | 39.3% | 44.0% | 9.7% | 7.0% | 16.7% | 0.0% |
| `resolution/read_his_file` | INT Average (1) | 900 | 38.3% | 43.7% | 10.3% | 7.7% | 18.0% | 0.0% |
| `resolution/brief_the_liaison_early` | SAV Fair (2) | 900 | 24.3% | 40.0% | 17.3% | 18.3% | 35.7% | 0.0% |

"price charged" is the tie plus failure rate — the two price bands the case declares. No action is a
dead end and no action is free: the cheapest charges 7.7% of rolls, the most expensive 40.3%.

**Can a character end the case unable to continue?** No — measured, not assumed. At every decision
point of every run (about 9,200), the harness checked for a state with no legal action and no
available ending: **0 blocked states**. A party member was *taken out* in 2 of 300 `force` runs (in
the closing exchange) and in 1 of 300 thorough runs (by a stress overflow mid-case); in every case
the case still closed, and the mid-case takeout did not stop the character acting again. The state is
recorded and nothing consumes it — see F5.

---

## 4. Decision quality

### Every route reaches an ending

| policy / requested | runs | ending | degraded | checks mean | checks p10–p90 | 3/3 | 2/3 | ≤1 | partial | blocked | refused |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `thorough:evidence` | 300 | closed_by_evidence (300) | 0.0% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `minimal:evidence` | 300 | closed_by_evidence (300) | 0.0% | 5.0 | 5–5 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `thorough:confront` | 300 | closed_by_confrontation (187), closed_by_withdrawal (113) | 37.7% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `minimal:confront` | 300 | closed_by_confrontation (179), closed_by_withdrawal (121) | 40.3% | 6.0 | 6–6 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `thorough:refer` | 300 | closed_by_withdrawal (300) | 0.0% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `minimal:refer` | 300 | closed_by_withdrawal (300) | 0.0% | 1.0 | 1–1 | 0.0% | 0.0% | 100.0% | 0.0% | 0 | 0 |
| `random` | 300 | closed_by_withdrawal (273), closed_by_evidence (18), closed_by_confrontation (9) | 0.7% | 7.61 | 2–13 | 14.7% | 32.7% | 52.7% | 13.0% | 0 | 0 |
| `thorough-no-aspects:evidence` | 300 | closed_by_evidence (300) | 0.0% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `thorough-naive-seats:evidence` | 300 | closed_by_evidence (300) | 0.0% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `thorough-no-aspects:confront` | 300 | closed_by_confrontation (187), closed_by_withdrawal (113) | 37.7% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |
| `thorough-naive-seats:confront` | 300 | closed_by_confrontation (187), closed_by_withdrawal (113) | 37.7% | 17.0 | 17–17 | 100.0% | 0.0% | 0.0% | 0.0% | 0 | 0 |

**No route dead-ends, and none can.** `closed_by_withdrawal` declares no requirement at all, so from
any state — including the first scene — at least one ending is legal. The 0 blocked states are the
measurement; the declaration is the reason.

### What actually decides the ending

Only the closing check. A party that plays **17 checks** reaches the detention in 187/300 runs; a
party that plays **6 checks** reaches it in 179/300. The 2.6-point difference is well inside sampling
noise (±4.0 points at one standard error), so eleven extra checks buy **no measurable improvement in
the chance of the strong ending** — they change the price paid, not the odds. Seat choice does the
same: the naive-seat party ends identically (187/300) while paying more (1.49 stress boxes and 4.42
complications against 1.09 and 3.48), because clues are fail-forward and only the closing roll
differs.

### The three endings, side by side

| ending | prerequisite | closing check | measured success | what it writes |
|---|---|---|---|---|
| evidence | the assembled finding (3 fragments, or 2 with `unproven-chain`) | SAV Good, passive | 91.7% with the scene-5 aspect, 81.7% without | objective; `unsa-field-office-trust`, or `…-doubt` on a failure |
| detention | finding **and** `batch-signature` **and** 2 chain facts | SAV Great, opposed — `pressure` (SAV vs SAV) or `force` (attack vs REF) | 51.7% pressure, 70.0% force | objective; trust + `kallio-residents-wary`; `lahtinen-in-custody`; `grey-sleeve-controller` |
| referral | nothing | WIL Average, passive | 89.7% on the shipped route; 96.0% for the one-check early referral (4.0% failure) | objective; `internal-affairs-referral`, plus `case-left-open` on a failure |

The case deliberately **scores none of these**, so "dominated" has no mechanical meaning here: each
records a different objective, reputation set and resource, and nothing ranks them. What can be
measured is cost and risk, and on those the referral is the cheapest and most reliable ending in the
case — available before the first check, one roll, 89.7% — while the detention is the most expensive
(6 checks minimum, and 30% of `force` runs and 48% of `pressure` runs fall back to a referral
anyway). Whether the referral *should* be that cheap is a design question, not a measurement.

### Force versus words

`force` succeeds more often than `pressure` (70.0% vs 51.7%, about 4.7 standard errors apart) and
costs more (26.7% of runs wound a party member, 0.7% take one out; `pressure` adds no injury beyond
the psi scene's own consequence). That reads as a trade-off until the arithmetic is checked: the
force exchange attacks with the resolution's `SAV` rating against Lahtinen's `REF` 2, while the words
contest opposes his `SAV` 3. **Force is therefore not a riskier alternative to words; it is the same
rating against a weaker defence.** See F2.

### Create an advantage

Three actions create an aspect (`Room to work`, `Nila's trust`, `The liaison is listening`).
Measured: **0 checks in 3,300 policy runs spent a free invocation on an action**, because scene
aspects are discarded at every scene boundary and each create-advantage action is the last action in
its scene. The only aspect that can ever be spent is the scene-5 one, offered to the closing check in
193 of 300 thorough runs — and only a *passive* closing check uses it:

| closing check | with the aspect offered | without |
|---|---|---|
| evidence (passive) | failure 8.3%, tie 6.7%, success 35.0%, style 50.0% | failure 18.3%, tie 15.7%, success 42.7%, style 23.3% |
| detention (opposed) | failure 23.3%, tie 14.3%, success 34.3%, style 28.0% | **identical**, 187/300 detention either way |

So "create an advantage" is worth +2 on one roll in the whole case, and worth nothing on the opposed
path. See F4.

---

## 5. Check load

| policy / requested | checks by skill |
|---|---|
| `thorough:evidence` | COG 1500 (29.4%), INT 900 (17.6%), SAV 2100 (41.2%), WIL 600 (11.8%) |
| `minimal:evidence` | COG 600 (40.0%), INT 300 (20.0%), SAV 600 (40.0%) |
| `thorough:confront` | COG 1500 (29.4%), INT 900 (17.6%), SAV 1987 (39.0%), WIL 713 (14.0%) |
| `minimal:confront` | COG 900 (50.0%), INT 300 (16.7%), SAV 479 (26.6%), WIL 121 (6.7%) |
| `thorough:refer` | COG 1500 (29.4%), INT 900 (17.6%), SAV 1800 (35.3%), WIL 900 (17.6%) |
| `minimal:refer` | WIL 300 (100.0%) |
| `random` | COG 545 (23.9%), INT 297 (13.0%), SAV 872 (38.2%), WIL 568 (24.9%) |
| `thorough-no-aspects:evidence` | COG 1500 (29.4%), INT 900 (17.6%), SAV 2100 (41.2%), WIL 600 (11.8%) |
| `thorough-naive-seats:evidence` | COG 1500 (29.4%), INT 900 (17.6%), SAV 2100 (41.2%), WIL 600 (11.8%) |
| `thorough-no-aspects:confront` | COG 1500 (29.4%), INT 900 (17.6%), SAV 1987 (39.0%), WIL 713 (14.0%) |
| `thorough-naive-seats:confront` | COG 1500 (29.4%), INT 900 (17.6%), SAV 1987 (39.0%), WIL 713 (14.0%) |

| policy / requested | checks by scene |
|---|---|
| `thorough:evidence` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |
| `minimal:evidence` | stairwell 300, victim 600, witness 300 |
| `thorough:confront` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |
| `minimal:confront` | resolution 300, stairwell 300, victim 600, witness 300 |
| `thorough:refer` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |
| `minimal:refer` |  |
| `random` | briefing 550, resolution 192, stairwell 356, victim 558, witness 326 |
| `thorough-no-aspects:evidence` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |
| `thorough-naive-seats:evidence` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |
| `thorough-no-aspects:confront` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |
| `thorough-naive-seats:confront` | briefing 900, resolution 900, stairwell 900, victim 1200, witness 900 |

**Four of the six individual skills are exercised; `REF` and `SOM` are never rolled at all** — the
probe that forbids either produces a byte-identical case. `SAV` is the only **mandatory** skill:

| probe | ending | clean finding | partial finding | 3/3 | checks mean | blocked |
|---|---|---|---|---|---|---|
| without `COG` | closed_by_evidence (300) | 100.0% | 0.0% | 100.0% | 11.0 | 0 |
| without `INT` | closed_by_evidence (300) | 100.0% | 0.0% | 100.0% | 14.0 | 0 |
| without `REF` | closed_by_evidence (300) | 100.0% | 0.0% | 100.0% | 17.0 | 0 |
| without `SAV` | closed_by_evidence (300) | 0.0% | 100.0% | 0.0% | 8.0 | 0 |
| without `SOM` | closed_by_evidence (300) | 100.0% | 0.0% | 100.0% | 17.0 | 0 |
| without `WIL` | closed_by_evidence (300) | 100.0% | 0.0% | 100.0% | 15.0 | 0 |

Dropping `COG`, `INT` or `WIL` costs checks (the party must use the other route to a fragment) but
never the clean finding. Dropping `SAV` costs the clean finding outright, because `stack-card` — the
gate on both routes to `stack-manifest` — comes from one SAV action.

---

## 6. The clue chain

| run family | 3/3 | 2/3 | ≤1 | partial finding |
|---|---|---|---|---|
| shipped routes (all four) | 100.0% | 0.0% | 0.0% | 0.0% |
| `thorough:*` (all three endings) | 100.0% | 0.0% | 0.0% | 0.0% |
| `minimal:evidence` / `minimal:confront` | 100.0% | 0.0% | 0.0% | 0.0% |
| `minimal:refer` | 0.0% | 0.0% | 100.0% | 0.0% |
| `random` | 14.7% | 32.7% | 52.7% | 13.0% |

**Assembled, not handed over — including under total failure.** Forcing every check to fail still
yields 3/3 fragments, a **clean** (non-partial) finding and the evidence ending, at the price of 15
complications and one injury; forcing every check to succeed yields the same chain at no price. A
clue never produces the finding: only `assemble()` does, and it refuses below two fragments and names
what is missing.

| run | ending | closing outcome | chain | partial | checks | complications | wounds | taken out | blocked |
|---|---|---|---|---|---|---|---|---|---|
| `every-check-fails` | closed_by_evidence | failure | 3 | False | 17 | 15 | 1 | True | 0 |
| `every-check-succeeds` | closed_by_evidence | success_with_style | 3 | False | 17 | 0 | 0 | False | 0 |
| `two-fragments` | closed_by_evidence | success_with_style | 2 | True | 14 | 1 | 0 | False | 0 |
| `one-fragment` | closed_by_withdrawal | success_with_style | 1 | False | 11 | 0 | 0 | False | 0 |
| `forced-lost-fight` | closed_by_withdrawal | failure | 3 | False | 6 | 0 | 1 | True | 0 |

A two-fragment finding is still assembled, still true, and still closes the case, but the record says
the chain was incomplete (`unproven-chain`, and `case-chain-incomplete` on the faction's books). That
is the property the case claims, measured under failure rather than asserted.

The one structural caveat: the chain's *gate* is a single action. `stack-card` has exactly one
source (`interview_nila`, SAV) and both routes to `stack-manifest` require it, so "every fragment is
reachable two ways" holds from the second check onward but not for the first. A party that never
interviews Nila cannot reach the finding at all, however well it rolls elsewhere. See F9.

---

## 7. Determinism

- Route runs replayed twice and compared on report + campaign payload: **1320** compared, **0** mismatched.
- Mid-play save → reload → finish compared with an uninterrupted run: **120** compared, **0** mismatched.

The same seed is the same story: the same dice, the same clues, the same injuries, the same books,
and — for the demo routes — the same printed log. (An earlier harness revision reported false
mismatches; the cause was the harness's own random temporary save path appearing in the demo's log
text, not the engine. The harness now uses a stable path per run.)

---

## 8. Findings

Each finding is evidence plus the question it raises. **None of them is decided here.** Across
roughly 9,200 runs the harness saw **0 crashes, 0 non-deterministic runs, 0 unreachable routes** and
no state the case could not continue from. One **code defect** was found and fixed (C1); it changed a
recorded boolean, not a rule.

| # | finding | kind |
|---|---|---|
| C1 | **Code defect fixed: the action record said `taken_out: false` when a hit overflowed the stress track.** `CaseSession.act` computed the flag from `self._wounds` — the list of *consequence-bearing* wounds — so a stress overflow with no free consequence slot logged the cost label `"taken out"` while the event and `ActionResult` reported `false`. It now reads the cost labels the action just produced, with a regression test (`test_a_stress_overflow_is_recorded_as_taken_out`). No rule, die, difficulty, skill or state changed: the same hits land on the same boxes, and only the recorded flag is correct. | code defect fixed |
| F1 | **The closing check decides the ending; investigation decides the price.** 17 checks reach the detention in 187/300, 6 checks in 179/300 (within noise). Play before the last roll cannot change which ending is reachable, only what it cost. Whether fifteen checks should carry that little weight is the author's call. | rules question for the author |
| F2 | **`force` attacks with `SAV`, not `REF`.** `RPG_FIRST_CASE.md` §5 describes the force closing check as a "REF opposed attack", but `CaseSession._exchange` uses `spec.skill`, and the confrontation declares `SAV`; only the defender rolls `REF`. With the placeholder sheets that makes force (SAV 4 vs REF 2) straight better than words (SAV 4 vs SAV 3): 70.0% vs 51.7%. Fixing it is a balance change, so it is reported, not changed. | rules question for the author (code and case document disagree) |
| F3 | **A tie on a confrontation is total failure.** `_contest` and `_exchange` degrade on any non-success, so a tie — 18.3% of pressure attempts, 15.7% of force attempts — falls back to a referral instead of "success at a minor cost", which is what every scene action in the same case does. The confrontation has no minor-cost band at all. | rules question for the author (D32) |
| F4 | **The aspect economy is nearly inert.** (a) Scene aspects are discarded at every scene boundary and all three create-advantage actions are last in their scenes, so **0 of 3,300 policy runs spent a free invocation on an action check**; (b) both opposed closing paths ignore `free_invoke` silently, so the one aspect that can be spent moves the passive closing check (failure 18.3% → 8.3%) and does nothing on the opposed one (identical 187/300). | rules question for the author (D31/D32) |
| F5 | **`taken out` is recorded and does nothing.** It is reachable two ways: in the closing exchange (2/300 `force` runs) and mid-case by a stress overflow. In the all-fail probe Harri is taken out at the stairwell and **takes two more actions afterwards** (the thermal record, the batch sign-out), and the case reaches its full evidence ending; 1 of 300 ordinary thorough runs does the same. The word appears in the action record and no rule consumes it — no rule stops the character, no rule changes the roll — so the slice cannot show what "taken out" is meant to mean. | rules question for the author (D34/D36) |
| F6 | **A failed psi reading injures the supervisor, not the witness.** `supervise_the_reading`'s failure writes the mild consequence *"A nail behind the eyes"* on the seat that supervises — Hecate in every scripted run — and it is the only named consequence in normal play: 19.0% of thorough runs, 14.7% of scripted routes. Whether supervising someone else's reading should harm the supervisor is astral-harm territory. | rules question for the author (D36) |
| F7 | **Four of six skills are exercised; `SAV` is mandatory.** `REF` and `SOM` are never rolled, and removing either changes nothing. Removing `SAV` removes the clean finding entirely (partial 100%). The case offers no evidence about two of the six approved skills, and makes one of them load-bearing through a single clue. | rules question for the author (D30) |
| F8 | **The referral is the cheapest ending and is available before play starts.** `closed_by_withdrawal` requires nothing and can be resolved in the first scene: 1 check, 96.0% success (4.0% failure), against 5–6 checks and 51.7–70% for the detention. The case scores no ending, so nothing mechanically rewards investigating. Whether the walk-away should be that cheap is the author's call. | rules question for the author |
| F9 | **The chain has a single gate.** `stack-card` has one source (`interview_nila`) and both routes to `stack-manifest` require it, so "two routes per fragment" holds only from the second check onward, and a party that skips one SAV action cannot reach the finding. The case document's claim that no clue depends on a single action is true of *checks* but not of *access*. | rules question for the author (design-record accuracy) |
| F10 | **The case exercises only the individual layer.** Every check is `ActionContext.INDIVIDUAL`; 0 faction-agent checks. It cannot supply evidence for the strategic roster (D22), the strategic skills, or the RPG→strategy write path beyond the label and id inventory it already writes. | scope note, not a defect |

No rules, dice, difficulties, skills, resolutions or decision rows were changed by this playtest.
`strategy_game/RULEBOOK.md` keeps its **NO RULES APPROVED** status and `RULEBOOK.md` was not touched.

---

## 9. What this suggests for D29–D38

Options and trade-offs only. **Nothing here answers a row.**

- **D29 — which game the ruleset governs.** The playtest exercises the crossover's individual layer
  only: one kernel, six Fate-rated skills, 4dF, four outcomes; no legacy `STAT + Skill + 1d10`
  anywhere. That is consistent with reading (a) *crossover only* in the limited sense that the
  shipped playable case is entirely a crossover artefact. It is not evidence that the legacy kernel
  should stay untouched, because the case never tests a conversion; reading (c), a conversion
  appendix, would need its own playtest of converted material.
- **D30 — six skills, or six attributes and six skills.** The measured surface is narrow: 4 of 6
  skills are rolled, `SAV` carries 35–41% of checks and is the only mandatory one, `REF`/`SOM` are
  never rolled. Option A (six skills) is what the case already plays, and it works at this size.
  Option B (attributes + skills) would add a second number this case never needed in order to say
  "strong but untrained". Option C (tags instead of skills) would remove the ratings the case's
  difficulty is expressed against — and `SAV` does so much work here that a tag-only sheet would
  have to carry it somewhere. The case cannot settle whether six is the right *list*: it was
  authored against these six.
- **D31 — the unified kernel.** All 41,582 policy checks used one 4dF kernel; no second dice
  convention appeared anywhere. The **contest-length sub-choice is untested**: the only opposed
  checks in the case are single exchanges that resolve in one roll, so option A's "first to three"
  has no playtest evidence either way.
- **D32 — is there a distinct success-at-a-cost band.** The case *is* a four-band case for scene
  actions (tie = minor cost, failure = serious cost, both measured landing on 7.7–40.3% of rolls),
  and simultaneously a **two-band case for confrontations** (tie and failure both = total failure).
  Option (b), five bands, would tidy the confrontation and change three modules; option (c),
  player-chosen cost, would matter most exactly where this case is thinnest, since the confrontation
  currently offers the player no cost menu at all.
- **D33 — is "simplified science" a seventh skill.** The case's forensic work is `COG` plus a
  `competence` tag on the specialist: `scan_the_stack`, `check_the_thermal_record` and
  `pull_the_batch_signout` are all COG and all read as specialist work because of who rolls them.
  That is consistent with option (a) and says nothing against (b) — a seventh skill would add a
  number this case never had to distinguish.
- **D34 — tactical combat.** The case shows the floor of what D34 must decide: one opposed exchange,
  no initiative, no action economy, no cover, no round structure, and `taken out` inert. It cannot
  choose between T1/T2/T3 because there is no tactical layer here to weigh. It does show that one
  exchange can carry "dangerous": 26.7% of force runs wound a party member, 0.7% take one out, and
  the case still closes. The case never makes a fight compulsory, so it is consistent with "combat
  never mandatory" but does not test the alternative.
- **D35 — consequences into the strategic layer.** Measured: injuries survive the campaign save and
  reach the faction books only as **named labels and id inventories**
  (`unsa-field-office-trust`, `kallio-residents-wary`, `grey-sleeve-controller`), never a magnitude;
  a closed case writes one provenance-stamped note and is idempotent. That is option (a)'s shape
  already, with the **recovery condition** still absent — nothing here says when a consequence
  clears, because the case has no clock.
- **D36 — a third stress track and a cyberware limit.** No third track was needed: the one cyber
  action (`pull_the_mesh_log`) charges a complication and, on a failure, one mental stress box, and
  the failed psi reading lands on mental stress plus a mild consequence. Option (b) or (c) would add
  a track this case never asked for; option (a) is what it already plays. Cyberware capacity is
  untested — no character in the case carries an implant that matters mechanically.
- **D37 — the sign-off.** This document supplies the **playability** half of "tested for
  playability": pace, lethality, decision quality, check load, chain behaviour and determinism, all
  reproducible. It does not supply the narrative/tactical demonstration, does not test a campaign,
  and does not test the strategic layer. Its numbers are also tied to *placeholder* agent sheets, so
  a sign-off on final sheets would need a re-run of the same command with those sheets. What
  acceptance means for `RULEBOOK.md`, and by whose hand, is untouched.
- **D38 — the tactical renderer.** No evidence either way. The case is text and headless and did not
  need a renderer.

---

## 10. Reproducing

```bash
python -m strategy_game.tools.playtest_second_shadow --seeds 300                # the tables above
python -m strategy_game.tools.playtest_second_shadow --seeds 300 --start 1000   # a different block
python -m strategy_game.tools.playtest_second_shadow --seeds 20 --json out.json  # the raw record
python -m unittest strategy_game.tests.test_playtest_harness
```

Harness: `strategy_game/tools/playtest_second_shadow.py`. Tests:
`strategy_game/tests/test_playtest_harness.py`. The seed block is fixed, so the same command prints
the same numbers; `--start` takes a fresh sample of the same case.
