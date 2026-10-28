# The narrative layer on 2d6: recalibration and what it decides

**Status: measurement and design note. No rule changed, nothing in `src/` or `rulebook/`
edited by this document.** It answers one of #689's open questions with arithmetic
instead of inheritance.

Companion script: `tools/narrative_layer_2d6_calibration.py` (exact enumeration, not a
simulation; rerun it and you get the same table).

---

## 1. Why this had to be redone

`rulebook/19_NARRATIVE_LAYER.md` states two safety rules and justifies them arithmetically:

1. **one ladder step per aspect** - aspects do not stack bonuses;
2. **one invoke per roll** - a roll may be modified once.

Those rules were derived on **4dF**, where 63% of outcomes fall within ±1, so a +2 invoke
moved the odds by **+32.1 percentage points** and four stacked aspects reached **100%**.

The 2026-10-26 ruling replaced that kernel with the Without Number check:
`2d6 + attribute modifier + skill` against `6 / 8 / 10 / 12 / 14`. The *rules* may still
be right. The *derivation* no longer applies to the game's actual dice, and a safety rule
nobody can re-derive is a rule that will be eroded by the first table that finds it
inconvenient.

## 2. The measurement

P(success) on 2d6, bonus from aspects alone, at each WN difficulty:

| DV | +0 | +1 | +2 | +3 | +4 | shift at +1 | +2 | +4 |
|---|---|---|---|---|---|---|---|---|
| 6 | 72.2% | 83.3% | 91.7% | 97.2% | 100.0% | **+11.1** | +19.4 | +27.8 |
| 8 | 41.7% | 58.3% | 72.2% | 83.3% | 91.7% | **+16.7** | +30.6 | +50.0 |
| 10 | 16.7% | 27.8% | 41.7% | 58.3% | 72.2% | **+11.1** | +25.0 | +55.6 |
| 12 | 2.8% | 8.3% | 16.7% | 27.8% | 41.7% | **+5.6** | +13.9 | +38.9 |
| 14 | 0.0% | 0.0% | 2.8% | 8.3% | 16.7% | **+0.0** | +2.8 | +16.7 |

## 3. What it says

### 3.1 The retired 4dF figure transfers almost exactly - at the standard difficulty

A **+2** aspect bonus at **DV 8** is worth **+30.6 pp** on 2d6, against **+32.1 pp** on
4dF. That is a difference of 1.5 points, and it is the strongest single result here: the
justification for *one invoke per roll* survives the kernel change essentially intact,
**provided the standard difficulty is the reference point**. The rule is not inherited; it
is re-derived, and it holds.

### 3.2 Stacking is still fatal, but no longer by reaching certainty

Four stacked steps (+4) reach **91.7%** at DV 8, not 100%. It is 1-in-12 failure rather
than impossibility - which is *worse*, not better: a table that stacks aspects will still
win nearly every standard check, but will occasionally and inexplicably lose one, which
reads as bad luck rather than as a broken rule. The ban on stacking remains justified, and
the reason has changed from "it breaks the ceiling" to "it makes failure look arbitrary".

### 3.3 The lever is strongest exactly where the game is most often played

At DV 8 a single step is +16.7 pp; at DV 14 it is **+0.0 pp**; at DV 6 it is +11.1 pp on
an already-72% base. So the aspect layer moves the needle **most at the standard
difficulty and least at the extremes** - which is the behaviour a narrativist layer should
have. It cannot rescue an impossible check, and it is not needed for an easy one. That is
a property worth stating in the rulebook, because it answers the common table objection
"why bother invoking when I am already likely to succeed".

### 3.4 One consequence for the difficulty ladder

Because a +2 at DV 12 is only +13.9 pp while a +2 at DV 8 is +30.6 pp, an aspect bonus is
**not a fixed quantity of advantage**. Any future rule that converts an aspect into "worth
about +X" must specify the difficulty it is being priced at, or it will be wrong by a
factor of two depending on where it is applied.

## 4. What this does not decide

- Whether the narrative layer **survives at all** against the WN baseline (that is a
  decision, not a measurement; the layer is currently stale on `1d10` in
  `rulebook/19_NARRATIVE_LAYER.md` and on retired band keys in
  `src/rules/narrative_layer.py`).
- Whether the 0-3 aspect pool becomes a real currency or stays an unnamed counter.
- Whether mental load is modelled as conditions, two pans, or EP-grade stress (options
  A / B / C in #689 §5).
- Any number for a mental track. **None is proposed here.**

## 5. The narrow claim this note supports

> *On the current 2d6 kernel, one aspect invoke is worth up to +30.6 pp at the standard
> difficulty, stacking four reaches 91.7%, and the effect shrinks to nothing at the
> hardest difficulty. The two safety rules in `19_NARRATIVE_LAYER` are therefore still
> correct, and are now re-derived from the game's own dice rather than inherited from a
> retired one.*

Everything else in the layer stays open.
