# Case mechanics: aspects, a lossy chain, and two skills that were decorative

**Status: implementation record and measurement, not a rule and not a decision.** This document
reports what three mechanics of the shipped case now do, and what each *alternative* would cost, over
the same seed block. It answers no author question: the rows the playtest raised
([`PLAYTEST_SECOND_SHADOW.md`](PLAYTEST_SECOND_SHADOW.md) §8, and D29–D39 in
[`../../docs/design/AUTHOR_DECISION_QUEUE.md`](../../docs/design/AUTHOR_DECISION_QUEUE.md)) stand
exactly as they were, and where a mechanic could go two ways the case keeps the reading it had and the
other reading is built by [`casework/options.py`](../casework/options.py) and measured here.

Refs [#516](https://github.com/TomiToivio/NooPunk/issues/516),
[#502](https://github.com/TomiToivio/NooPunk/issues/502),
[#482](https://github.com/TomiToivio/NooPunk/issues/482).

Every table in §3 and §4 is printed by the harness, pasted unedited:

```bash
python -m strategy_game.tools.playtest_second_shadow --seeds 300
python -m strategy_game.tools.playtest_second_shadow --seeds 300 --json playtest.json
```

---

## 1. What was wrong, in the evidence's own words

The playtest measured three things the case claimed and did not do:

| finding | what the harness saw (before this change) |
|---|---|
| **F4** | **0 of 3,300 policy runs** spent a free invocation on an action check. Scene aspects were discarded at every scene boundary, every create-advantage action was the last action in its scene, and both opposed closing paths **ignored `free_invoke` silently**. |
| §6 | The chain reached **3/3 in 100%** of scripted and thorough runs **even with every check forced to fail** — "assembled, not handed over" held only in the sense that fragments arrived with complications. |
| **F7** | `REF` and `SOM` were **never rolled**; the probe that forbade either produced a byte-identical case. `SAV` was the only mandatory skill. |

None of those was a decision. They were mechanics that could not express what the case already said.
Three changes fix the machinery; §4 measures every alternative the machinery can now express.

## 2. What the mechanics do now

### 2.1 Aspects are on the scene, and every check can invoke one

* A scene declares its **situation aspects** in the case file (`SceneSpec.aspects`) — *"The night
  report is already too clean"*, *"Forty-one seconds nobody saw"*, *"A loading bay until twelve"*.
  They are on the scene register from the first moment, with **no** free invocation, because a free
  invocation is what a create-advantage action earns and nothing else.
* Any check in that scene may invoke one: `act(..., free_invoke=name)` spends a free invocation,
  `act(..., invoke=name)` spends a **Fate point** of the character attempting it. Both add **+2** in
  `rpg/scene.py`, the resolver that already existed. Nothing re-derives an outcome.
* `resolve(..., free_invoke=…/invoke=…)` reaches the closing check on **every** path. The opposed
  paths (`_contest`, `_exchange`) now hand the actor's half to `rpg.skills.check` with the invocation
  attached, exactly as the passive path always did — one resolver, not two.
* A free invocation that does not exist is **refused with its reason** rather than quietly turned
  into a Fate-point spend or ignored; a paid one needs a Fate point on that character.
* The NPC opposition invokes nothing. Giving NPCs Fate points would be a rules decision, so the
  measurement of what the *party's* aspects are worth uses an uninvoked defence as its floor.

### 2.2 The chain can end short, and says what is missing

* `ActionSpec.withhold_on_failure` (labelled `TUNING_CHAIN_WITHHOLD`) is the case's declaration that
  a **failed** check does not hand over its fragment. The failure still charges its declared price.
* The shipped case sets it on the **six** actions that yield a chain fragment, and on nothing else.
  Every fragment still has **two** routes, so a failure removes one route, never the last one.
* Fail-forward is kept on three counts, each measured in §3: the price lands; the other route is still
  on offer in the same scene; and a short chain still assembles a **partial** finding with its gap
  named (`FindingResult.missing`, `report()["findings"][i]["missing"]`) or, below the partial floor,
  closes on the weaker resolution with `ResolutionResult.gaps` and a detail line that names every
  fragment the party never obtained.
* A **tie** still grants the fragment (Fate's "success at a minor cost"). The line between the two
  bands is the whole mechanic, and it is pinned by a test.
* The faction books are unchanged: `case-chain-incomplete` is still written only when a *partial*
  finding is what closes the case. The gap itself lives on the record, not on a new reputation label.

### 2.3 `REF` and `SOM` have a natural tool

* `stairwell/hold_the_hatch` — **SOM**, create advantage: hold a jammed service shutter at shoulder
  height while the tag on the frame is read. Creates *"A shoulder under the hatch"* (1 free invocation,
  2 on a style), and its failure is the case's only non-combat *physical* stress.
* `resolution/get_to_the_bay_first` — **REF**, create advantage: a foot race to the loading bay before
  the shift lets out. Creates *"First to the loading bay"*, which the closing check can invoke — so REF
  now feeds the one roll that decides a detention.
* Both are create-advantage actions and **neither yields a clue**, on purpose: making REF or SOM
  chain-bearing would have been a different change, and F9 (one SAV action gating the chain) is the
  author's to answer, not something to paper over. `SAV` keeps its centrality; §3 measures it.
* The confrontation's attack skill is **not** changed. `ResolutionSpec.force_attack_skill` names the
  alternative (the case document's *"REF opposed attack"*) and the shipped case leaves it empty, so the
  exchange still attacks with `SAV`. §4 measures both.

## 3. Before and after, on every finding

Same command, same seed block (0–299, 300 seeds per route and policy), same case content otherwise.
"Before" is `origin/main` as the previous evidence document measured it.

### 3.1 F4 — the aspect economy

| run family | runs invoking on an action check | invokes/run | runs spending one on the closing check |
|---|---|---|---|
| `thorough:evidence` (before) | **0 / 300** | 0.00 | 193 (offered, **dropped**) |
| `thorough:evidence` (after, free spent as they come) | **300 / 300** | 6.23 | 73 |
| `thorough:evidence` (after, one kept for the close) | 281 / 300 | 2.11 | **275** |
| `thorough:evidence` (after, free and paid) | 300 / 300 | 17.91 | 158 |
| `thorough:evidence` (after, ignoring invocations) | 0 / 300 | 0.00 | 0 |
| the four shipped routes (after) | 0 (the demo spends only at the close) | 0.00 | 211–213 of 300, free |

The single number that mattered most is the seventh column of the old document's table: an aspect was
worth **+2 on one passive roll** and **nothing** on the opposed one. It is now worth +2 on both:

| closing path | before: aspect offered | before: no aspect | after: aspect offered (kept for the close) | after: no aspect |
|---|---|---|---|---|
| `closed_by_evidence` (passive SAV) | failure 8.3%, style 50.0% | failure 18.3%, style 23.3% | failure 1.7%, style 59.7% | failure 17.3%, style 16.3% |
| `closed_by_confrontation` (opposed, `pressure`) | **identical to no aspect** (187/300 detention) | 187/300 detention | **230/300 detention** | **158/300 detention** |

The same table for the four **shipped routes**, which now spend the aspect they earn at the close:

| route | chain 3/3 | partial | a gap recorded | the closing check invoked | ending |
|---|---|---|---|---|---|
| `investigate` | 289/300 | 11 | 11 | 213 | evidence 300 |
| `confront:pressure` | 289/300 | 11 | 11 | 211 | detention 241, referral 59 |
| `confront:force` | 289/300 | 11 | 11 | 211 | detention 271, referral 29 |
| `refer` | 289/300 | 0 | 11 | 0 (the referral needs no aspect) | referral 300 |

The opposed row is the fix: before, the free invocation was accepted and dropped, so the aspect moved
nothing; now it moves 72 detentions per 300 runs.

### 3.2 The chain is lossy

| run family | 3/3 | 2/3 | ≤1/3 | partial finding | runs with a recorded gap |
|---|---|---|---|---|---|
| shipped routes (before) | 100.0% | 0.0% | 0.0% | 0.0% | — |
| shipped routes (after) | 96.3% | 3.7% | 0.0% | 3.7% | 3.7% |
| `thorough:*` (before) | 100.0% | 0.0% | 0.0% | 0.0% | — |
| `thorough:*` (after) | 95.0% | 5.0% | 0.0% | 5.0% | 5.0% |
| `minimal:evidence` (before) | 100.0% | 0.0% | 0.0% | 0.0% | — |
| `minimal:evidence` (after) | 62.3% | 31.3% | 6.3% | 31.3% | 37.7% |
| `random` (before) | 14.7% | 32.7% | 52.7% | 13.0% | — |
| `random` (after) | 10.0% | 27.7% | 62.3% | 12.3% | 90.0% |

(The route figures differ from the policy figures above because the demo script is a *fixed* route: it
takes the same actions in the same order on every seed, and the dice decide whether a fragment comes
back. A policy that takes everything has more routes to lose.)

The extreme the old document quoted:

| run | ending | closing outcome | chain | partial | checks | complications | gaps recorded |
|---|---|---|---|---|---|---|---|
| `every-check-fails` (before) | closed_by_evidence | failure | 3 | False | 17 | 15 | — |
| `every-check-fails` (after) | **closed_by_withdrawal** | failure | **0** | False | 17 | 15 | `stack-manifest`, `camera-gap`, `impression-double` |
| `every-check-succeeds` (after) | closed_by_evidence | success_with_style | 3 | False | 19 | 0 | — |
| `two-fragments` (after) | closed_by_evidence | success_with_style | 2 | **True** | 16 | 1 | `impression-double` |
| `one-fragment` (after) | closed_by_withdrawal | success_with_style | 1 | False | 12 | 0 | `camera-gap`, `impression-double` |

A party that fails everything still **closes the case, pays 15 complications, is never blocked, and
carries a record that names all three missing fragments** — it just cannot claim the finding. That is
the difference between "fail-forward" and "the chain is never lossy": both are now true.

Which fragments go missing, and how often, in the thorough party (300 runs):

| fragment | withheld by a failure (300 runs) | still missing at close |
|---|---|---|
| `impression-double` | 72 | 7 |
| `camera-gap` | 54 | 3 |
| `stack-manifest` | 28 | 5 |

The second column is why the flag is on *both* routes of a fragment: a single failure withholds often
(154 times per 300 runs) and costs the chain rarely (15 runs), because the second route usually saves
it. That is the two-routes-per-fragment claim doing work for the first time.

### 3.3 F7 — the skill surface

| run family | `REF` rolls | `SOM` rolls |
|---|---|---|
| every route and policy, before | **0** | **0** |
| every route and policy, after | 300 per family | 300 per family |

| probe (thorough, evidence) | before: clean finding | after: clean finding | after: partial | after: checks mean |
|---|---|---|---|---|
| without `REF` | 100.0% | 95.0% | 5.0% | 17.97 (18.97 baseline) |
| without `SOM` | 100.0% | 95.3% | 4.7% | 17.97 |
| without `SAV` | 0.0% | **0.0%** | 97.3% | 10.0 |
| without `COG` | 100.0% | 65.7% | 29.0% | 13.0 |

**`SAV` is still the only mandatory skill, and that is a finding, not a bug.** Dropping it costs the
clean finding outright (0.0% clean in both runs) because `stack-card` still has one source. What
changed is that dropping `REF` or `SOM` is no longer *free*: each removes an action, its aspect, and —
in the case of `REF` — a free invocation the closing check would otherwise have had.

Removing `REF` moved the detention rate 156→159 per 200 (`pressure`, aspect kept for the close) in an
earlier 200-seed sample, i.e. **within noise**. The honest statement is: `REF` and `SOM` are rolled,
their aspects are spent, and their removal is measurable in the *check load* and in the *closing-check
invocation rate*, not in the ending distribution. They are no longer decorative; they are not
load-bearing on the chain, and this document does not pretend otherwise.

## 4. Options: each author question, measured both ways

Built by [`casework/options.py`](../casework/options.py) — a `dataclasses.replace` copy of the
declaration, played on the same campaign and the same seeds. The **first row of every block is the
shipped setting**, so no row is a recommendation, and the difference between rows is the option.

### Does a failure withhold the fragment? (`TUNING_CHAIN_WITHHOLD`)

| setting | ending | 3/3 | partial | gap recorded | complications mean |
|---|---|---|---|---|---|
| yes — shipped | closed_by_evidence (300) | 95.0% | 5.0% | 5.0% | 2.90 |
| no — every check grants its clue (the previous behaviour) | closed_by_evidence (300) | 100.0% | 0.0% | 0.0% | 2.85 |

At the extreme (every check forced to fail): shipped closes on a **referral with three named gaps**;
the alternative closes on the **evidence ending with a clean chain**. A cost of ~0.05 complications
per run in normal play, and a completely different answer at the tail.

### Which skill does a force exchange attack with? (`TUNING_OPPOSED_ATTACK_SKILL`)

| setting | detention | withdrawal | party wounded (runs) |
|---|---|---|---|
| the resolution's own — `SAV` (code, shipped) | **228 / 300 (76.0%)** | 72 | 96 / 300 (32.0%) |
| `REF` — the case document's "REF opposed attack" | **133 / 300 (44.3%)** | 167 | 154 / 300 (51.3%) |

That gap is F2's whole size: `force` currently attacks with `SAV` 4 against Lahtinen's `REF` 2, which
is why it beats `pressure` (`SAV` 4 vs `SAV` 3). Reading `REF` as the document says makes force the
*worse* option and adds 58 wounded parties per 300 runs. Both readings are now one flag apart; the choice is the
author's, and the shipped case does not make it.

### Is a tie on a confrontation total failure? (`TUNING_CONFRONTATION_TIE`)

| approach | tie = total failure (shipped) | tie stands, priced by nothing here |
|---|---|---|
| `pressure` | detention 180 / 300 (60.0%) | detention **228 / 300 (76.0%)** |
| `force` | detention 228 / 300 (76.0%) | detention **256 / 300 (85.3%)** |

The option moves the *shape* of D32 and deliberately prices nothing: what a tie should cost is the
author's call, and inventing a cost here would have been answering it.

### How much of the aspect economy does the party spend?

| setting | 3/3 | partial | invokes/run | closing invoke | complications mean |
|---|---|---|---|---|---|
| nothing | 92.0% | 8.0% | 0.00 | 0% | 4.48 |
| free, spent as they come | 95.0% | 5.0% | 6.23 | 24.3% | 2.90 |
| free, one kept for the close | 92.0% | 8.0% | 2.11 | 91.7% | 3.96 |
| free and paid (Fate points too) | 100.0% | 0.0% | 17.91 | 52.7% | **0.66** |
| free, created after the checks it would help | 93.3% | 6.7% | 0.67 | 57.7% | 4.59 |

On the confrontation, the same question is worth 72 detentions per 300 (158 without aspects, 230 with
one kept for the close). The paid row is the ceiling of what Fate points buy: 2,897 points across 300
runs — the party is *spending its refresh*, and the case has no clock to charge for it.

### The floor of check load

| setting | ending | 3/3 | partial | gap | complications mean |
|---|---|---|---|---|---|
| withholds on failure — shipped | evidence 281, withdrawal 19 | 62.3% | 31.3% | 37.7% | 1.51 |
| always grants — as before | evidence 300 | 100.0% | 0.0% | 0.0% | 1.20 |

## 5. What changed in existing behaviour, deliberately

Nothing here is a rule, a die, a difficulty band or an author decision, but four things a reader of the
old evidence would notice:

1. **The case grew two actions.** 17 → 19 actions, 16 → 18 checks, so a thorough run rolls 19 checks
   (18 + the closing check) instead of 17. This is the cost of §2.3 and it is the only reason the
   "checks mean" column moved.
2. **The demo routes now spend the aspect they create.** `confront:pressure` reaches a detention in
   **241/300** runs where it reached **155/300**, and `confront:force` in **271/300** where it reached
   **210/300**. That is the size of the bug F4(a) described: the free invocation was there, offered,
   and silently dropped. `investigate` still reaches the evidence ending in **300/300**, but 11 of
   those runs hold a **partial** finding with a named gap, which is the lossiness working.
3. **`demo.play` no longer raises** when the requested ending needs something the party did not get.
   It notes the refusal and closes on the weaker record — the difference between a demo that shows a
   lossy chain and one that crashes on it. The interactive front end (`casework/play.py`, merged in
   #542) now spends the closing aspect the same way, so a played run and a scripted one still produce
   the same record.
4. **Records gained fields, nothing lost:** `report()["chain"]["missing"]`,
   `report()["findings"][i]["missing"]`, `ResolutionResult.gaps`, `ActionResult.withheld/invoked`,
   and `withhold_on_failure` / `force_attack_skill` / `tie_is_not_total_failure` / `aspects` in the
   declaration's `to_dict()`. A saved session still loads (the aspect register round-trips) and the
   determinism checks are unchanged: **1,320** route replays, **0** mismatches; **120** save/reload,
   **0** mismatches.

`RULEBOOK.md`, `strategy_game/RULEBOOK.md` (still **NO RULES APPROVED**) and the legacy tabletop rules
are untouched. No dice convention, skill, outcome band, difficulty or ending requirement changed.

## 6. What this does not do

* **It does not answer D29–D39 or F1–F9.** F1 (the closing check decides the ending) is untouched: a
  short chain still does not move the closing roll, only the record and the fallback.
* **F9 is untouched.** `stack-card` still has one source, and `SAV` is still mandatory. The
  withholding flag is on chain fragments, not on that gate, precisely so the single gate stays visible
  and measurable rather than being quietly duplicated.
* **F5/F6/F8 are untouched** (`taken out` still inert, the psi consequence still lands on the
  supervisor, the referral is still the cheapest ending available in scene one).
* **No NPC Fate points.** The opposition never invokes, so the party's aspects are measured against an
  uninvoked defence.
* **No tie price.** `tie_is_not_total_failure` changes whether a tie ends the attempt, not what it
  costs.
* **Aspects are still scene-scoped.** They are not carried across a scene boundary; Fate's situation
  aspects last as long as the situation does, and making "Room to work" follow the party to the
  loading bay would be a different mechanic.
* **The individual layer only.** Every check is still `ActionContext.INDIVIDUAL`; no faction-agent
  check, no tactical layer, no campaign across cases.
* **No skill or rule was added.** Two case actions were added, both using skills and a resolution shape
  that already existed.

## 7. Reproducing

```bash
python -m strategy_game.tools.playtest_second_shadow --seeds 300   # §3 and §4, verbatim
python -m unittest strategy_game.tests.test_case_aspects_and_chain \
                   strategy_game.tests.test_playtest_harness \
                   strategy_game.tests.test_casework_session
```
