# Issue #564 / D40 — measuring the three candidate kernels

**Status: measurement and decision support. Not a ruling, not a proposal, no rule changed.**

Queue row **D40** (and issue **#566**) asks which core check NoöPunk's playable rules should use. The
compatibility specification argues the options qualitatively
([`ISSUE_564_RULES_COMPATIBILITY_SPEC.md`](ISSUE_564_RULES_COMPATIBILITY_SPEC.md) §6, K1–K3). This
file adds the numbers those options turn on, from one executable tool:

```bash
python3 tools/issue564_kernel_comparison.py         # the tables below
python3 tools/issue564_kernel_comparison.py --json  # the same numbers, machine-readable
```

Contracts: [`tests/test_issue564_kernel_comparison.py`](../../tests/test_issue564_kernel_comparison.py)
(12 code tests, #271). Everything is **exact enumeration over `fractions.Fraction`** — no sampling, so
a figure is a property of the dice and not of a seed. `src/rules/core.py` is consumed for layer A's
die and DV ladder, never restated.

---

## 1. The three kernels, as published

| | die | bonus | ladder | source |
| --- | --- | --- | --- | --- |
| **A** layer A (legacy) | `1d10` | `STAT + Skill`, 2..20 | DV 9 / 13 / 15 / 17 / 21 / 24 / 29 | `data/rules/core.json`; `src/rules/core.py` |
| **W** Without Number family | `2d6` | attribute modifier (−2..+2) + skill level (0..4) | difficulty 6 / 8 / 10 / 12 / 14+ | CWN SRD `rules-of-the-game/skill-checks/`; identical in WWN/AWN |
| **F** layer B (crossover) | `4dF` | Fate skill, −1..+4 | opposition, plus four outcome bands | `strategy_game/rpg/fate.py`; #389/#482 |

## 2. Method, and why the axis is `bonus − target`

The ladders and scales differ, so comparing "DV 13" with "difficulty 8" is meaningless. The comparable
quantity is **the margin**, `bonus − target`, and the probability of success as a function of it.

One detail matters and is easy to get wrong: with a die whose minimum is not zero, a character whose
bonus *equals* the target succeeds on **every** roll (`1d10 + 10 ≥ 13` is always true). The contested
region is therefore `delta ≤ −2` for layer A, `≤ −2` for 2d6, and straddles `0` for 4dF. The tool
computes each kernel's contested window rather than assuming a shared one.

Typical competences used below: layer A `+10` (STAT 5 + Skill 5 — a competent professional on the
1..10 scales), WN `+2` (+1 attribute modifier, skill-1), Fate `+3` (a "Good" skill).

## 3. Results

### 3.1 The curves

| `bonus − target` | A `1d10` | W `2d6` | F `4dF` |
| ---: | ---: | ---: | ---: |
| contested window | −10 … −2 | −12 … −3 | −4 … +3 |
| far edge | 10 % | 2.8 % | 1.2 % |
| mid-low | 60 % (−5) | 58 % (−7) | 62 % (0) |
| near edge | 90 % (−2) | 97 % (−3) | 99 % (+3) |

### 3.2 What one point of competence is worth

| kernel | gain per +1 | at the steepest point | shape |
| --- | ---: | ---: | --- |
| A `1d10` | **exactly 10.0 pp everywhere** | 10.0 pp | flat |
| W `2d6` | 5.6 – 16.7 pp | 16.7 pp (at requirement 7) | bell |
| F `4dF` | 4.9 – 23.5 pp | 23.5 pp (at the tie) | triangle |

### 3.3 Size: competence range, contested band, ladder

| kernel | competence range | contested band (`delta`) | ladder | does the ladder fit the die? |
| --- | ---: | ---: | --- | --- |
| A `1d10` | **18 steps** (2..20) | **9 steps** | 7 rungs spanning 20 DV points | **no — the ladder is ~2× the band, and the competence range 2× again** |
| W `2d6` | 8 steps (−2..+6) | 11 steps | 5 rungs spanning 8 points | yes — the ladder and the range are sized to the bell |
| F `4dF` | 5–6 steps | 8 steps | 4 outcome bands, continuous opposition | yes |

### 3.4 At their own ladders (typical competence)

| kernel | target : probability |
| --- | --- |
| A `+10` | DV 9 **100 %** · 13 **80 %** · 15 **60 %** · 17 **40 %** · 21 / 24 / 29 **0 %** |
| W `+2` | TN 6 **92 %** · 8 **72 %** · 10 **42 %** · 12 **17 %** · 14 **3 %** |
| F `+3` vs 2 | failure 18.5 % · tie 19.8 % · success 43.2 % · success with style 18.5 % |

## 4. Findings

1. **The centre is the same; the slope is not.** "A competent professional at a moderate task" lands at
   **72–82 %** in all three (A: DV 13 at +10 → 80 %; W: TN 8 at +2 → 72 %; F: +3 vs 2 → 81.5 % counting
   the tie). Choosing a kernel is not choosing how competent a professional feels — it is choosing
   how much the *next* point of competence buys.
2. **`1d10` is ruthlessly linear.** Every +1 is worth exactly 10 percentage points, everywhere. That is
   maximum transparency (a table can do the arithmetic in its head, and a digital runtime can print
   the odds) and zero texture: there is no "the middle matters more".
3. **The bells make the middle the game.** `2d6` pays 5.6–16.7 points per step and `4dF` 4.9–23.5, so
   competence is worth most exactly where most contests sit — and cheap at the edges, which is why a
   master rarely botches.
4. **The tails differ by an order of magnitude.** The smallest non-zero success chance is **10 %** on
   `1d10`, **2.8 %** on `2d6`, **1.2 %** on `4dF`. On layer A's die a novice always has a one-in-ten
   chance and a master always has a one-in-ten failure; the bells make "impossible" and "certain"
   actually reachable.
5. **Layer A's scale, not its die, is what produces #571's pathology.** Its competence range is 18
   steps and its DV ladder spans 20 points, but a given character's contested band is only **9** steps
   — so the ladder is mostly saturated: for a `+10` character, DV 9 is automatic, DV 21+ is impossible,
   and there is **no rung at all** between 40 % (DV 17) and 0 % (DV 21). The same saturation produces
   #571's finding that at DV 17+ no *wound* of removing severity can be dealt
   (`ISSUE_571_COMBAT_INJURY_TRAUMA.md` §5.2). **Swapping the die would not fix that** — re-sizing the
   scale and the ladder would.
6. **The family's numbers are sized to its die, which is why they look "tight".** An 8-step competence
   range and a 5-rung ladder against an 11-step contested band means every rung is a real decision and
   no rung is free.
7. **Fate's tie band has no counterpart on the other two dice.** 19.8 % of matched contests sit on the
   tie, and that is exactly where the approved "succeed at a minor cost" rule lives. Reproducing it on
   `1d10` or `2d6` requires an *extra* rule (margin-of-zero band), not a different die.

## 5. What this adds to K1 / K2 / K3

The compatibility specification's three options, now priced in arithmetic rather than prose:

- **K1 — stay on `4dF` (#389/#482).** Keeps the tie band (finding 7) and needs no ladder work: the
  four outcome bands already absorb difficulty differences. Cost: the crossover's competence range is
  the narrowest of the three (5–6 steps), so breadth has to come from aspects and stunts.
- **K2 — move to `2d6`.** Buys the bell and the tight ladder, but the measurement shows the *scale*
  must move with it: 1..10 STATs plus 1..10 skills give an 18-step range against an 11-step band,
  i.e. the same mismatch finding 5 identifies. A die swap alone would create a new pathology.
- **K3 — two kernels plus a conversion appendix.** Honest about the fact that the repository already
  runs two; costs a third document and a permanent "which die am I rolling?" question at the table.

**The one thing none of the three does** is fix layer A's scale. If D40 answers "keep `1d10`", the
ladder and the STAT+Skill range still need a re-sizing decision (which is a rule change, not a
conversion), and the measurement above says exactly how wide they should be: **about 8–9 points of
contested margin**, not 18.

## 6. Matched-feel translation (for authors writing examples)

To reproduce a layer A result on another kernel, use this, not the target numbers:

| want | layer A | Without Number | Fate |
| --- | --- | --- | --- |
| a competent professional at a moderate task (≈80 %) | DV 13 at +10 (80 %) | TN 8 at +2 (72 %) | opposition = skill − 1 (81 %) |
| a genuinely hard task (≈40–60 %) | DV 15–17 at +10 (60 % → 40 %) | TN 10 at +2 (42 %) | opposition = skill (62 % incl. tie) |
| a task a professional usually fails (≈3–20 %) | **no rung does this**: the ladder jumps 40 % → 0 % | TN 12–14 at +2 (17 % → 3 %) | opposition = skill + 2 … + 3 (6 % → 1 %) |

## 7. What this file does not do

- It does not choose a kernel, and it changes no rule, rulebook section or runtime path.
- It does not model situational modifiers, gear, aid, or the crossover's aspects/stunts; those shift
  the bonus and therefore move a row on the curves, but do not change the shapes in §3.2.
- It does not re-open #389/#482, and it does not pre-answer #566's scope question (which *layer* #564
  governs) — it only prices the die question that sits inside it.

— Ai (愛)
