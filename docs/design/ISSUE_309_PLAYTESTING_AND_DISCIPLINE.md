# #309 §8 — playtesting criteria, and keeping the vision from eating the prototype

**Scope:** the last two §8 artifacts. Item 9 — *"establish playtesting criteria: engagement per minute,
meaningful consequences per turn, clarity of power shifts, replayability and operational cost"*. Item 10
— *"check long-term vision against the simplified three-layer strategy prototype so immediate
development remains disciplined"*.

**What this is.** Criteria for judging a prototype, and a discipline check.

**What this is not.** Not a mechanic, a rule, a balance number or a canon ruling. **The criteria below
measure the game; they are not part of it.** No threshold here may be lifted into `RULEBOOK.md`, and
nothing here authorizes implementation (rules gate: row **D11**).

---

## 1. Playtesting criteria (item 9)

Five criteria, each with a question the tester answers and a signal that says the prototype is not ready.
They are deliberately **readable counts and yes/no judgements**, not scores: a score would invite
optimising the metric instead of the game.

### 1.1 Engagement per minute

- **Question:** in a session, how many minutes pass with no decision, no new information and no
  consequence? Call those *dead minutes*.
- **Signal of failure:** the tester can name a stretch of dead minutes longer than a couple of minutes.
  `VISION.md` §7b's own prohibition — *"little dead air"*, no *"turns spent waiting"* — is the standard;
  Terra Invicta's pacing is the named thing we are not reproducing.
- **Why a count, not a feeling:** testers reliably under-report boredom and over-report excitement.
  Counting dead minutes is something a tester can actually do while playing.

### 1.2 Meaningful consequences per turn

- **Question:** for a given turn, name **one thing that changed** and **why it changed**. Repeat across
  the session.
- **Signal of failure:** a turn where the honest answer is "nothing changed" or "it changed but I cannot
  say why". The second is worse than the first: an unexplainable change is a bug in legibility, not a
  pleasant surprise.
- **The bar:** every turn must yield a nameable change. If turns routinely yield none, the turn is too
  small or the systems are not connected — and #309's §7b test applies: if the three pillars are
  disconnected mini-games, the MVP has failed even though all three exist.

### 1.3 Clarity of power shifts

- **Question:** after a shift, can the tester **explain it back** unprompted — who gained, who lost, and
  through what? This is the criterion `VISION.md` §7b states as *"they can explain why power shifted"*,
  and the architecture document turns into a constraint (*a layer may be coarse, never opaque*).
- **Signal of failure:** the tester describes power as a bar that moved, or attributes the change to the
  interface rather than to a cause. If the only available explanation is a number, the discourse layer is
  not doing its job.
- **Strongest form of the test:** show the shift, then close the panel, then ask. A change that survives
  the panel being closed is understood; one that does not was merely displayed.

### 1.4 Replayability

- **Question:** on a second run, does the tester make a **different decision for a reason** — or the same
  decision because nothing suggested an alternative?
- **Signal of failure:** a second run identical to the first with no alternative visible. Note the
  asymmetry: replay value comes from *legible alternatives*, not from randomness. A different outcome
  from the same choice is a dice roll; a different choice from the same situation is a decision.
- **Floor for S1-a:** one scenario is allowed to be finite (`VISION.md` §7b caps it at a single sitting
  with a real ending). Replayability is required in the sense of *a second run being worth starting*, not
  in the sense of infinite content.

### 1.5 Operational cost

- **Question:** what does it cost to **run** and to **change** this prototype — hours to prepare a
  session, dependencies to install, and the cost of one content edit?
- **Signal of failure:** a playtest that needs a service, an account, a model, a database or a network
  connection. Each is disqualifying on its own, not merely expensive: `VISION.md` §7a forbids *"no
  feature may require a live service, proprietary engine or paid model provider"*, and every stage must
  run offline from source.
- **The edit test:** change one line of scenario content and re-run. If that requires touching engine
  code, the data/code boundary has failed — which is also what `test_scenario_schema`,
  `test_tabletop_primitives` and `test_map_spec` exist to protect.

---

## 2. The discipline check (item 10)

§8's item 10 asks that the long-term vision be checked **against the simplified three-layer prototype**,
so that immediate development stays disciplined. The check is a set of questions with the failure mode
named, to be run whenever the vision and the prototype start to drift apart.

| Vision says | Prototype must show | Drift looks like |
| --- | --- | --- |
| One game, one God's-eye view | one board, no mode change | a second camera, a separate screen, a "mode" |
| Three pillars feed each other | one loop, all three present | three features sharing a menu |
| Deliberately simple politics | moves the player can explain | a hidden meter or an opinion score |
| Indie scope, small team | content in handfuls | a content list longer than a page |
| Offline, no required service | runs from source with nothing running | any install-time service or key |
| New Weird first, cyberpunk secondary | anomaly before hardware | spaceships as the strangest thing |
| Every stage shippable alone | S1-a is a game, not a demo | "it will be good once S2 lands" |

**The one-line test, applied to any proposal:** *does this make the current stage more playable, or does
it make a later stage more plausible?* Only the first belongs in the current stage. The second is how a
small open-source project acquires an architecture it cannot finish — the exact failure `VISION.md` §7
names, and the reason §7b's explicit out-of-scope list exists.

**Where a proposal fails this test legitimately.** Some work is genuinely preparatory and must still
happen: the licensing decision (D10), the renderer pick (D13) and the rules gate (D11) are all blocking
and none of them makes the prototype more playable. The distinction is that those **unblock** a stage;
a space layer, an economy or a mod UI would **replace** one.

---

## 3. What this does not do

- **It sets no balance number.** The criteria judge the game; they are not difficulty tuning.
- **It approves no rule and no canon.** D11 and D12 still govern.
- **It promises no second scenario.** S1-a is explicitly one finite campaign.
- **It is not a test suite.** These are human judgements; the repository's automated tests cover
  executable code only (#271), and none of the above is code.
