# Narrative layer: aspects, consequences and GM moves

**Status: NOÖPUNK NATIVE — issue #229.** This is the canonical, **optional** narrative layer. It
sits **on top of** the numeric core and never replaces it: STATs and Skills stay readable, and an
aspect is never a rating. Every number is **PROVISIONAL pending author calibration**.

It canonises the tested prototype (`docs/design/ISSUE_200_ASPECTS_PROTOTYPE.md`, #233) rather than
starting again; the measurements there are the reason for the two design rules below.

## The two rules that make the layer safe

Both come from measurement, not taste, and both are asserted by the guard.

> **1. An aspect grants ONE ladder step — never a number of its own.**
> **2. Invocations are capped at one per roll.**

The prototype measured why. On a 4dF core, 63% of all outcomes fall within ±1, so a **+2** invoke
moves the odds by **+32.1 percentage points** — turning "likely" into "near-certain" — while a
single step moves them **+19.8**. And **without the per-roll cap, four stacked aspects reach exactly
100%: auto-success, with no roll that can fail.** That is the "uncapped numerical exploit" #200
names, and it costs a player four tags to buy.

Because the step is expressed as **one step on the core ladder** rather than a fixed number, the
rule survives the pending scale migration intact: it means the same thing whether the die is the
current d10 or the directed -3…+3 core. The layer adds no arithmetic of its own.

## Aspect anatomy

An aspect is a **bounded, cancellable tag** with five parts. Every part is required; an aspect
missing one is not a valid aspect (the guard enforces each).

| Part | Meaning |
| --- | --- |
| **Statement** | the fiction, in words: *"Owes D a favour"*, *"Wanted in Turku"* |
| **Scope** | *who or what it attaches to* — a character, a group, a place, a situation, or a single scene |
| **Duration / use condition** | when it ends: a scene, until the favour is repaid, until contradicted |
| **Effect class** | **Permission**, **Modifier**, or **Consequence** — never a rating |
| **Cancellation** | what removes it: evidence, a changed situation, an explicit counter, or being compelled |

### The three effect classes, and what they may do

- **Permission** — the aspect makes something *possible* that otherwise was not (you may attempt
  entry because *"You know the night porter"*). Permission never adds a number.
- **Modifier** — **one ladder step**, once per roll, capped per the rule above.
- **Consequence** — a state the fiction now has to live with: an injury, a **Grievance**
  ([`rulebook/4_SOCIAL.md`](4_SOCIAL.md), #220), a debt, a reputation. A consequence is a **state,
  not a counter**: consequences do **not** accumulate into a worse state by arithmetic, exactly as
  `RULEBOOK.md` §51 requires of the harm ladder.

**An aspect may never produce a rating.** There is no "Aspect 3". The guard asserts there is no code
path from an aspect to a STAT or Skill value, because "tag-only characters" is the failure this
whole section exists to prevent.

## Numerical precedence: the deterministic order

When an aspect and the core disagree about a number, the core wins. Always. The resolution order is
fixed:

1. **The core check resolves** — `STAT + Skill + 1d10` against its target (or the opposed roll).
2. **The margin is read into its band** — the one band arithmetic shared by physical
   ([`rulebook/3_PHYSICAL.md`](3_PHYSICAL.md), #219) and social ([`rulebook/4_SOCIAL.md`](4_SOCIAL.md), #220).
3. **At most one invoked aspect applies**, moving the result **one step**.
4. **A GM move is chosen from the band** — see below.
5. **An LLM may narrate** the resolved outcome and **propose** aspects or consequences.

Steps 1–4 are **deterministic**. Only step 5 is generated. An LLM never chooses a modifier, never
rolls, and never writes state: it proposes, and the engine validates or **rejects**. This is the same
seam #220 established, reused rather than restated.

> **Aspect first, or roll first?** Roll first. An aspect changes what a roll *means* or what it may
> attempt; it does not retroactively decide what the dice said.

## Narrative resources

The layer needs a spendable economy so an invoke has a cost. The **mechanics** are specified here;
the **name** of the pool is deliberately left to the author (the prototype declined to name it, and
naming is canon).

- A pool holds a small whole number of points, **PROVISIONAL: 0–3**, refilled at a defined beat
  (a scene boundary or a session), not per roll.
- **Invoking** an aspect costs one point.
- **Compelling** an aspect — accepting a complication the aspect implies — **earns** a point, and is
  the only way to gain one mid-scene.
- The pool is **per character**, never shared, and **cannot be spent to exceed the one-step bound**:
  spending more points does not buy a bigger modifier. That is the anti-exploit rule in its final
  form.
- A character with no aspects is **fully playable** — the layer is optional, and a zero-aspect
  character simply never invokes.

## Invokes, compels, and difficult choices

- **Invoke** — spend a point, take **one step** on a roll that the aspect plausibly bears on. The
  player must say *how*; a generic "I use my aspect" is refused.
- **Compel** — the GM (or the player, self-compelling) names how an aspect makes life harder, and
  the character **earns** a point. A compel cannot remove a character's agency, cannot dictate a
  choice, and cannot be used to force a player's hand; it presents a complication, and the player
  decides what the character does.
- **Difficult choice** — a compel aimed at a **drive** rather than a situation: the character's own
  commitments create the dilemma. The mechanic is the same point economy; the content is the
  character's own Motivation edges ([`rulebook/8_FACTIONS.md`](8_FACTIONS.md)).

**A compel is never a punishment and never a loss of control.** It changes the situation and pays
for it. If a table treats compels as the GM overriding a player, the layer has failed — and the
guard asserts the chapter says so.

## GM moves and partial success

GM moves are **read off the band** the core already produced — the layer adds no new randomness.

| Outcome | GM move (PROVISIONAL) |
| --- | --- |
| **Success, wide margin** | *Reward* — a clean win, plus an aspect in the character's favour |
| **Success, narrow margin** | *Cost* — they get it, but something is spent, owed or noticed |
| **Partial / tie** | *Complication* — they get it **and** a consequence; a difficult choice may be offered |
| **Failure** | *Escalate* — the situation worsens, an aspect turns against them, or a new threat appears |

The moves are **descriptions of what the fiction does next**, not modifiers. A "partial success" is
a band result, not a second roll, and it never silently changes the number that was rolled.

## Character drives

A **drive** is a Motivation edge the player wants the story to press on
([`rulebook/8_FACTIONS.md`](8_FACTIONS.md)). Drives are how the layer stays **Narrativist** without
becoming arbitrary: the compel economy pays the player for letting their own commitments complicate
the mission. A drive is **not** a new stat, and its strength is the Affect score it already has.

## GNS parity: why all three readings resolve on one core

The layer is explicit that it does not privilege one creative agenda (design invariant, `AGENTS.md`
§13):

- **Narrativist** — the aspect and compel economy, drives, difficult choices.
- **Simulationist** — the same core check and the same bands; consequences persist as state.
- **Gamist** — a bounded, spendable resource with a real opportunity cost, and a cap that prevents
  the auto-success exploit.

The **parity property is executable**: whatever the play style, the numeric result is produced by the
same function, and the guard tests the three styles through one core rather than asserting the claim
in prose.

## Worked examples

### Investigation (Simulationist)

**K** is searching a flat with *"Methodical"* as an aspect. The core resolves the search; the margin
band is narrow, so the GM move is **Cost** — K finds the ledger, and a **Consequence** aspect
*"Tripped the alarm"* attaches. K's player later **compels** *"Methodical"* to argue K photographs
everything before leaving, and **earns** a point for the delay.

### Ideology / social intrigue (Narrativist)

At a Helsinki demonstration, **V** holds *"Trusted by the co-op"*. On a social contest resolved per
`rulebook/4_SOCIAL.md`, V **invokes** it: **one step**, once. A narrow success draws the **Cost**
move — the co-op is now visibly aligned with V's faction, and a Reputation edge moves one step.

### Combat (Gamist)

**A** is pinned and invokes *"Never leaves anyone behind"* to reach a downed teammate: **one step**,
once, and the point is spent. If A had four aspects, A still gets **one step** — the cap is what
keeps the fight a fight.

## What this chapter deliberately does not do

- **No new Skills, STATs or derived statistics**, and no rating may come from an aspect.
- **No name for the resource pool** — that is the author's canon to write.
- **No numeric stress track.** `RULEBOOK.md` §51 is a fiction-first consequence vocabulary and harm
  does not advance by arithmetic, so a stress track would contradict canon rather than extend it.
- **No replacement for any realm's procedure** — physical combat is #219, social is #220,
  investigation is #226.
- **No LLM in the numeric loop** — the engine resolves, validates and rejects.
- **No calibration.** Every value is PROVISIONAL.
