# Narrative layer: aspects, consequences and GM moves

**Status: NOÖPUNK NATIVE — issue #229, re-anchored on the Without Number die by issue #689.** This
is the canonical, **optional** narrative layer. It sits **on top of** the numeric core and never
replaces it: STATs and Skills stay readable, and an aspect is never a rating. Every number is
**PROVISIONAL pending author calibration**.

The dice are the baseline's: `2d6 + attribute modifier + skill rank` against difficulty 6, 8, 10,
12 or 14, and `1d20` for saves. The chapter's earlier `1d10` figures, its directed `−3…+3` ladder and
its `brutal / severe / solid / glancing` band names describe the retired core and are no longer used
anywhere in play.

It canonises the tested prototype (`docs/design/ISSUE_200_ASPECTS_PROTOTYPE.md`, #233) rather than
starting again; the measurements there are the reason for the two design rules below.

## The two rules that make the layer safe

Both come from measurement, not taste, and both are asserted by the guard.

> **1. An aspect grants ONE ladder step — never a number of its own.**
> **2. Invocations are capped at one per roll.**

Both rules were re-measured on the die the game actually uses, because a safety rule nobody can
re-derive is a rule the first inconvenient table erodes. On `2d6` at the standard difficulty (8),
success with a modifier of 0 is 15 of 36 outcomes (41.7%); one step takes it to 21 of 36 (58.3%),
which is **+16.7 percentage points** — and two steps land exactly where an unmodified roll lands at
difficulty 6. So **one step is worth a whole difficulty step**: the layer can move a check one notch,
which is what it is for, and cannot move it two, which is what the cap is for.

Stacking would no longer reach certainty — four steps reach 91.7% at difficulty 8, not 100% — and
that is *worse*, not better: a table that stacks would win nearly every standard check and still lose
one in twelve for no visible reason, which reads as bad luck rather than as a broken rule. The ban on
stacking therefore survives the kernel change, with a new reason.

Because `2d6` has ±1 granularity, the step is literally `+1`: `invoke_step()` returns 1 and no
argument can raise it. The layer adds no arithmetic of its own.

**An aspect's worth is difficulty-dependent, and the text must say so.** The same one step is worth
**+16.7 pp at difficulty 8**, +11.1 pp at 10, +5.6 pp at 12 and **+0.0 pp at difficulty 14** — at
14 with a modifier of 0 or 1 the check is impossible before the invoke and impossible after it.
That is not a bug: an aspect rescues a *contested* check and cannot manufacture a roll the dice
cannot make. But it means any sentence that converts an aspect to "about +X" is wrong by a factor of
two unless it names the difficulty, and a referee who prices an invoke at a high difficulty will feel
cheated by a rule that promised more than the die can deliver.

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

1. **The core check resolves** — `2d6 + attribute modifier + skill rank` against its difficulty
   (or the opposed check), or `1d20` for a save.
2. **The margin is read into its band** — the one band table this chapter states, below.
3. **At most one invoked aspect applies**, moving the result **one step** (`+1`).
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

The band is read off the **margin** — total minus difficulty. It is never a second roll.

| Margin | Band | GM move (PROVISIONAL) |
| --- | --- | --- |
| −1 or less | **miss** | *Escalate* — the situation worsens, an aspect turns against them, or a new threat appears |
| 0–1 | **cost** | *Cost* — they get it, but something is spent, owed or noticed |
| 2–4 | **clean** | *Reward* — they get it cleanly |
| 5 or more | **style** | *Reward and an aspect* — they get it, and an aspect goes in their favour |

The boundaries are measured rather than chosen for flavour. At difficulty 8 with a modifier of 0 the
thirty-six outcomes fall **21 miss / 9 cost / 6 clean / 0 style**; one step moves six outcomes out of
miss. `band_distribution()` in `src/rules/narrative_layer.py` recomputes those shares, so the table
cannot drift away from the dice without a test failing.

The moves are **descriptions of what the fiction does next**, not modifiers. A band is a reading of
the roll, not a second roll, and it never silently changes the number that was rolled. The referee's
judgement enters here and only here: a *cost* is a licence to spend something the fiction has already
put on the table, not a tariff.

## The closed move set

Eight procedures, and no ninth without an argument. Each is a **trigger** plus the four banded
outcomes above; none of them adds a die, a modifier or a currency. They exist so the referee has a
shared vocabulary instead of nine improvised rulings, and so the digital runtime can resolve a
narrative action without a language model.

| Move | Roll | Trigger |
| --- | --- | --- |
| **Read a situation** | `Notice` + INT check | you take a moment and ask what is really going on |
| **Read a person** | `Talk` + CHA check | you watch someone under pressure and want the truth |
| **Apply pressure** | `Talk` + CHA check | you push with leverage you actually hold |
| **Hold steady** | mental save (`1d20`) | what you are seeing contradicts what you know |
| **Cross a threshold** | `Sneak` + DEX check | you get past a barrier that is actively guarded |
| **Set up** | any check the preparation uses | you spend your action preparing rather than acting |
| **Ground yourself** | `Heal` + WIS check | you take a scene to come back to yourself |
| **Contact the noösphere** | `Know` + WIS check | you open your mind to the Noösphere and let it answer |

Three of them buy **questions** (one on a *cost*, two or three on a *clean* or *style* hit), *set up*
buys an **aspect**, and *ground yourself* **cancels** a temporary condition. Nothing grants a
modifier: that is what an invocation is for, and it is capped at one per roll.

A save-based move is rolled on `1d20` against the save target and its margin is read into the same
four bands. It is not a `2d6` check and must not be turned into one.

The catalogue is `data/rules/narrative_moves.json`; the resolver is `src/rules/narrative_moves.py`;
the bands live in `src/rules/narrative_layer.py`. A move that is not in the catalogue does not exist,
and the catalogue's size is asserted, so a ninth move has to change this chapter too.

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
- **No second dice mechanic.** Checks are `2d6 + modifier + rank`, saves are `1d20`. A move never
  changes either, and a grant is never a bonus.
- **No resurrection of the retired core.** `src/rules/aspects_prototype.py` (the 4dF measurement),
  `strategy_game/rpg/fate.py` (the 4dF crossover engine) and the d10 band names are legacy, kept as
  evidence of how the rules were derived, not as mechanics in play.
- **No name for the resource pool** — that is the author's canon to write.
- **No numeric stress track.** `RULEBOOK.md` §51 is a fiction-first consequence vocabulary and harm
  does not advance by arithmetic, so a stress track would contradict canon rather than extend it.
- **No replacement for any realm's procedure** — physical combat is #219, social is #220,
  investigation is #226.
- **No LLM in the numeric loop** — the engine resolves, validates and rejects.
- **No calibration.** Every value is PROVISIONAL.
