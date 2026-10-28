# Decision record: the narrative layer and the mind system (#689)

**This closes the design gate. It approves no implementation.** It records what the
evidence settles, what the author's closing direction settles, and what stays explicitly
open. Decisions that exceed measurement are marked **provisional and reversible in one
sentence**, which is the house convention.

Inputs: #686 / #687 / #688 (consolidated), the 2d6 calibration merged as `a460c5f4`, the
Without Number baseline ruling of 2026-10-26, and the existing canon in
`rulebook/19_NARRATIVE_LAYER.md` with `src/rules/narrative_layer.py`.

---

## 1. The state that had to be reconciled

| artifact | state found | consequence |
|---|---|---|
| `rulebook/19_NARRATIVE_LAYER.md` | states the core as `STAT + Skill + 1d10`, speaks of "the directed −3…+3 core", cites 4dF arithmetic | **stale against the baseline; the layer's prose must be rewritten, not extended** |
| `src/rules/narrative_layer.py` | `BAND_TO_MOVE` keys are `brutal / severe / solid / glancing` | the retired d10 band vocabulary; the gate logic is sound, the vocabulary is not |
| `src/rules/aspects_prototype.py` | measured 4dF | superseded by `tools/narrative_layer_2d6_calibration.py` |
| `strategy_game/rpg/fate.py` | 4dF engine, green tests | correctly labelled legacy by the baseline; untouched by this record |
| `strategy_game/data/genre_paradigms.json` | six genres, three domains, `lenses_that_spawn_a_system()` must stay empty | alive, and it already forbids the mistake a genre-module proposal would make |

The important correction from #689 stands: **the narrativist layer is not a proposal. It is
canon, it is optional, and it is stale.** The work was never "should aspects enter" — it was
"does the existing layer survive the new kernel, and what must be re-anchored".

## 2. What the evidence settles

**D41 — The layer survives, re-anchored on 2d6.** The two safety rules were justified by
arithmetic on a retired kernel. Re-measured on the real one, they hold: a +2 invoke at
DV 8 is worth **+30.6 pp** against 4dF's **+32.1 pp**. The layer is therefore not
inherited on faith; it is re-derived. *Implementation implication:* rewrite
`rulebook/19_NARRATIVE_LAYER.md` against `2d6 + attribute modifier + skill` / `6·8·10·12·14`,
and replace the band keys in `src/rules/narrative_layer.py`.

**D42 — One invoke per roll; aspects never stack.** With one invoke the ceiling is +30.6 pp
at the standard difficulty. With four stacked steps it is **91.7%** — not certainty, which
is *worse*: the table wins nearly every standard check and occasionally loses one, so
failure reads as bad luck rather than as a broken rule. The ban stands, for a new reason.

**D43 — An aspect's worth is difficulty-dependent and must be priced that way.** +16.7 pp at
DV 8, **+0.0 pp at DV 14**. Any rule that converts an aspect to "about +X" must name the
difficulty, or it is wrong by a factor of two.

**D44 — No second dice system.** Checks resolve on `2d6`; attacks and saves on the CWN
`d20`; `4dF` survives only inside `strategy_game/` as legacy. This closes **C1**.

**D45 — Fate is retired as a baseline, not as vocabulary.** Its aspect/compel *shape* is
kept; its kernel is not. This closes **C5**, and it means every "Fate Core is the approved
kernel" note predates the ruling of 2026-10-26 and must not be reapplied by implication.

## 3. What the author's closing direction settles

**D46 — Mental load is Option A: conditions, not a track. (PROVISIONAL)**
The mind is modelled as *conditions with mechanical teeth*, not as a depleting pool. Reasons:
it needs no canon override, it does not create a second harm track beside CWN's
Trauma/Frail/Strain, and it keeps the character sheet legible. A condition constrains
choices; it does not subtract numbers from a bar.

**D47 — The four-layer exposure model is adopted. (PROVISIONAL)**
`observable event → acute response → persistent condition → worldview state`. This is #686's
contribution and it is the right shape for the PKD / *Maniac* / *Riget* register: it
distinguishes what happened, what it did at the time, what it left behind, and what the
character now believes.

**D48 — Worldview change is a player decision, never a failed save.**
A shock that contradicts a held belief presents a **choice with two different costs** —
accept the reframe and take its consequence, or hold the belief and take a different one
(denial, obsession, withdrawal). A roll may never overwrite a character's convictions. This
is the single non-negotiable all four sibling issues reached independently.

**D49 — Option C (EP-grade Stress → Trauma → Disorder + psychosurgery) is deferred, not
rejected.** Revisit when a written case demonstrably cannot be carried by conditions — with
the case named, not as a general preference. The trigger is evidence, not appetite.

**D50 — PbtA contributes clocks and nothing else yet.** Clocks for investigations and
faction fronts. **Moves-as-catalogue is refused**: it is commercial content, a second
rulebook to maintain, and `lenses_that_spawn_a_system()` already sets the precedent that a
module may not claim its own system. **Partial success is not adopted**; if it ever is, it
is scoped to declared social/psychic actions and defined once, in one table.

## 4. What stays open (and is not decided here)

- Whether the 0–3 aspect pool becomes a spendable currency. **Current direction: no** — it
  must never compete with Effort on the same roll.
- The exact condition list, their severities and their recovery rules. **No numbers are
  proposed.**
- Whether worldview state lives on the character sheet or only in the case journal.
- Tabletop ↔ CRPG parity for the condition layer.
- Any genre-dial numeric setting.

## 5. What happens next

Implementation is **not** authorized by this record. Follow-up issues, each with executable
tests:

1. Re-anchor `rulebook/19_NARRATIVE_LAYER.md` and `src/rules/narrative_layer.py` on 2d6.
2. Implement Option A conditions as data, with the four-layer exposure model and no
   numeric pool.
3. Write the first case that exercises a paradigm shock end to end, and use it as the
   falsification test for D46–D48.

If a follow-up finds D46 or D47 wrong, it comes back here as a one-sentence reversal rather
than being quietly extended.
