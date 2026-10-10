# Kernel prototype: the Fudge/Fate candidate core (issue #200)

A tested prototype of the kernel #200's §5 asks for — **Fudge / Psi-Punk / Fate /
Transhumanity's Fate-inspired, six STATs plus separate Skills, Fudge-style dice** — with the
numbers that decide it, and an honest account of what it does *not* settle.

**Status: prototype. Not canonical. Nothing migrated.**

- `data/rules/core.json` and `src/rules/core.py` remain the authored `STAT + Skill + 1d10`
  check. This work does not change them.
- `AGENTS.md` §13.9 and §15.2 fix that baseline as active, and §13.8 forbids silently
  redesigning the balances. **A prototype is not a migration.** Nothing here may be wired into
  a runtime until you record a decision.
- #200 says the numerical migration must be **"tested before locking exact formulas"**. This is
  that test, not the lock.

Reproduce every figure below:

```
PYTHONPATH=src python3 tools/issue200_kernel_report.py
```

Dice probabilities are **exact** (rational arithmetic, no seed); lethality is sampled at
40,000 trials with seed `20261010`. The sibling resolution lab in PR #207 computes exact
probabilities too, and this file **adopted that method**; the sampled figures it replaced agreed
with the exact ones to within sampling error.

**Companion prototype:** [ISSUE_200_ASPECTS_PROTOTYPE.md](ISSUE_200_ASPECTS_PROTOTYPE.md) covers the
other half of #200's kernel request — what aspects, narrative costs and consequences may do around
this roll. This file answers how a roll resolves; that one answers what a tag is allowed to change,
and measures the cap that stops aspects from reaching automatic success.

## The one thing that must survive any candidate

**Attributes and Skills stay separate.** #200 is explicit that Fudge's attribute/skill
distinction is not optional, so all three candidates keep the six STATs (FIT/REF/INT/SOC/CYB/PSY)
and a separate 1–10 Skill rating. They differ **only** in how the two combine — and that
difference is the whole question.

## The ladder

Seven steps, centred on zero. The *shape* is Fudge's trait ladder; the wording is NoöPunk's own,
because a ladder of named steps is a procedure while its labels are expression the rights ledger
has to keep clear of.

| rating | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| step | −3 | −2 | −2 | −1 | +0 | +0 | +1 | +1 | +2 | +3 |
| label | Abysmal | Poor | Poor | Weak | Unremarkable | Unremarkable | Capable | Capable | Strong | Peak |

Dice are 4dF — four dice of −1/0/+1:

| roll | −4 | −3 | −2 | −1 | +0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chance | 1.23% | 4.94% | 12.35% | 19.75% | **23.46%** | 19.75% | 12.35% | 4.94% | 1.23% |

A 1d10 gives every face 10% and swings ±9 at the tails. 4dF puts nearly a quarter of all rolls
on zero and makes the extremes **eight times rarer than the centre** — the curve is the point.

## The three candidates

| candidate | rule |
| --- | --- |
| **A `additive`** | `step(STAT) + step(Skill)` — the naive reading of "Attribute + Skill" |
| **B `averaged`** | `step(round-half-up((STAT + Skill) / 2))` — one number from two |
| **C `skill-primary`** | `step(Skill) + clamp(step(STAT), −1, +1)` — the Skill carries, the STAT nudges |

## 1. The migration benchmark still works

`data/rules/core.json` records Novice (STAT 4 + Skill 1) at DV 9/13/15 as **0.7 / 0.3 / 0.1**.
Re-measured through the canonical engine:

| DV | recorded | measured |
| --- | --- | --- |
| 9 | 0.70 | 70.0% |
| 13 | 0.30 | 29.6% |
| 15 | 0.10 | 10.1% |

The benchmark **delegates** to `src/rules/core.py` rather than reimplementing it, so a comparison
against it cannot drift from the shipped engine. Testing the benchmark first is what makes every
legacy number below trustworthy. The test suite checks **all five recorded profiles against all
seven DVs** — 35 recorded values — not just the headline one.

## 2. Additive scaling — the pathology #200 warns about

How many of the 100 possible (STAT, Skill) pairs land on each step:

| candidate | −3 | −2 | −1 | +0 | +1 | +2 | +3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **A** | 19 | 13 | 14 | 14 | 14 | 10 | 16 |
| **B** | 1 | 14 | 13 | **36** | 26 | 7 | 3 |
| **C** | 14 | 12 | 18 | 16 | 16 | 14 | 10 |

All three reach every step, so reachability distinguishes nothing. The **unclamped** range does:

| candidate | raw range | pairs needing the clamp | pairs collapsed to an extreme |
| --- | --- | --- | --- |
| **A** | −6 … +6 | **19 of 100** | **35 of 100** |
| **B** | −3 … +3 by construction | 0 of 100 | 4 of 100 |
| **C** | −4 … +4 | 8 of 100 | 24 of 100 |

**A wants a ±6 range on a ±3 ladder.** Nearly a fifth of its pairs are clamped and about a third
are flattened onto the extremes — at which point the ladder's ends stop being the top and
become "anything high". That is the additive-scaling failure mode, measured rather than asserted.

## 3. Where the candidates stop differing — and where they don't

Effective step per profile, before any roll:

| candidate | weak 2+1 | competent 5+5 | mixed 10+1 | specialist 8+8 | top 10+10 |
| --- | --- | --- | --- | --- | --- |
| **A** | −3 | +0 | **+0** | +2 | +3 |
| **B** | −2 | +0 | +0 | +1 | +3 |
| **C** | −3 | +0 | **−2** | +2 | +3 |

P(success) at step 0:

| candidate | weak 2+1 | competent 5+5 | mixed 10+1 | specialist 8+8 | top 10+10 |
| --- | --- | --- | --- | --- | --- |
| **A** | 6.2% | 61.7% | **61.7%** | 93.8% | 98.8% |
| **B** | 18.5% | 61.7% | 61.7% | 81.5% | 98.8% |
| **C** | 6.2% | 61.7% | **18.5%** | 93.8% | 98.8% |

At the extremes the clamp makes the candidates converge; **the middle is where the design lives.**
The `mixed 10+1` column *is* the question: a character with a peak Attribute and no training.
Under C that character sits at 18.5% success; under A and B, 61.7%.

For comparison, the canonical engine on the same profiles:

| DV (ladder) | weak 2+1 | competent 5+5 | mixed 10+1 | specialist 8+8 | top 10+10 |
| --- | --- | --- | --- | --- | --- |
| 9 (−3) | 50.2% | 100.0% | 100.0% | 100.0% | 100.0% |
| 13 (−2) | 10.0% | 79.7% | 89.7% | 100.0% | 100.0% |
| 15 (−1) | 0.0% | 59.7% | 69.7% | 100.0% | 100.0% |
| 17 (+0) | 0.0% | 40.3% | 50.3% | 100.0% | 100.0% |
| 21 (+1) | 0.0% | 0.0% | 9.9% | 59.8% | 100.0% |
| 24 (+2) | 0.0% | 0.0% | 0.0% | 29.6% | 69.6% |
| 29 (+3) | 0.0% | 0.0% | 0.0% | 0.0% | 20.0% |

The legacy engine **saturates hard**: at DV 13–17 a specialist succeeds every time and a weak
character never can. The ladder's bounded curve is the reason to consider this at all.

## 4. Opposed checks

| candidate | equal 5+5 vs 5+5: win | tie | specialist 8+8 vs 5+5: win | mixed 10+1 vs 5+5: win |
| --- | --- | --- | --- | --- |
| **A** | 41.6% | 16.9% | 73.9% | **41.6%** |
| **B** | 41.6% | 16.9% | 58.4% | **41.6%** |
| **C** | 41.6% | 16.9% | 73.9% | **14.1%** |

Two findings. Equal opponents win ~41.6% with a **16.9% tie band** — 4dF-vs-4dF ties about one roll
in six, against 1d10-vs-1d10's 10%, so an opposed-check procedure needs to say what a tie *means*.
And the last column is the whole decision: under A and B an untrained brute **stays at parity**
with a competent character, while under C training is decisive.

## 5. Modifier stacking — why a cap exists

Competent 5+5 at step 0, capped at ±2 steps versus uncapped:

| situational | capped | uncapped |
| --- | --- | --- |
| +0 | 61.7% | 61.7% |
| +1 | 81.5% | 81.5% |
| +2 | 93.8% | 93.8% |
| +3 | 93.8% | 98.8% |
| +4 | 93.8% | **100.0%** |
| +6 | 93.8% | **100.0%** |

Uncapped, a +6 bonus is worth **more than every die in the roll** and guarantees success. The cap
is not flavour text; without it the dice stop mattering.

## 6. Lethality — pace, not a wound model

Expected exchanges to fill a 4-box stress track, defending at Everyday (DV 13):

| engine | weak 2+1 | competent 5+5 | mixed 10+1 | specialist 8+8 | top 10+10 |
| --- | --- | --- | --- | --- | --- |
| legacy 1d10 | 40.5 | 5.0 | 4.5 | 4.0 | 4.0 |
| **A** | 10.2 | 3.3 | 3.3 | 2.4 | 2.1 |
| **B** | 6.0 | 3.3 | 3.3 | 2.7 | 2.1 |
| **C** | 10.2 | 3.3 | **6.1** | 2.4 | 2.1 |

#200 leaves the light wound ladder in place until it is reconciled, so this measures **pace**, not
a proposed wound system. Two things worth seeing: the legacy engine resolves a fight for a
competent character in 5 exchanges and then **cannot go faster** (4.0 at the top — the d10 is
noise next to a +20), while C's untrained brute takes 6.1 because his skill is genuinely poor.

## 7. What the measurements say

**Recommendation: candidate C, skill-primary**, with two caveats the author owns.

C is the only candidate that makes training matter: a trained specialist beats an untrained
brute **73.9% / 14.1%**, where A and B leave it a coin-flip at 41.6%. It needs the clamp for only 8 of 100 pairs
(A: 22; 38 collapse to the extremes), so the ladder's ends stay meaningful. And it keeps the
Attribute mechanically real — the ±1 nudge plus STAT-as-governing-attribute — without
double-counting it into a ±6 range.

**A is the option #200 warns about, and the data says why.** Its ±6 range loses 38% of all rating
pairs to the extremes and makes "peak Attribute, zero training" as good as competence. If
additive is chosen deliberately, the ladder has to widen with it.

**B is the narrowest and the least interesting.** It never clamps and it is the most stable, but
averaging one number out of two makes the Attribute/Skill split largely decorative.

**What this does not settle, and should not be presented as settled:**

- **The DV collapse this prototype first reported is FIXED.** Its own draft divisor mapped
  21 Heroic, 24 Incredible and 29 Legendary all onto +3. #213 supplied an author-directed table
  and this prototype now **consumes** it, so all seven authored DVs map onto seven distinct steps.
- **The rating and DV mappings are consumed, not invented.** Per `AGENTS.md` §13, where a shared
  specification exists it is consumed rather than re-declared in a second runtime — so changing
  `data/rules/fudge_scale_migration.json` moves these numbers and the tests will say so.
- **A DV outside the authored seven falls back to the nearest one**, stated rather than silently
  interpolated.
- **Ratings 1 and 10 are partly wasted under any candidate**, since both already sit on ±3 alone.
- **Aspects, stress, consequences, compels and scene stakes are not prototyped here.** #200 asks
  for them and they need their own prototype and their own playtest; this kernel is the
  arithmetic underneath them.
- **No playtest has happened.** These are simulated distributions. #200's bar is "test before
  locking", and simulation is the first half of that.

## Reproducing

`src/rules/kernel_prototype.py` holds the engine and `IS_CANONICAL = False`;
`tools/issue200_kernel_report.py` regenerates this document's numbers;
`tests/test_issue200_kernel_prototype.py` pins the properties that must hold whatever the author
chooses — including the legacy benchmark matching the recorded canon, the canonical files staying
untouched, and the rating/DV tables matching the author-directed file.

**The rating and difficulty mappings are consumed from
`data/rules/fudge_scale_migration.json`** (issue #213, author-directed) rather than re-declared
here, per `AGENTS.md` §13's rule that a shared specification is consumed rather than restated in a
second runtime. A first revision of this prototype carried its own draft divisors and, as a
result, collapsed six of the seven authored DVs onto one step. Change the author's file, not this
one, and the tests will tell you which numbers moved.
