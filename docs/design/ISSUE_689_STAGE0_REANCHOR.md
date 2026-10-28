# Stage 0 — re-anchoring the narrative layer to the 2d6 kernel (#689)

**Deliverable of Stage 0 in #689.** Research and disposition only: this document changes no rule, no
number and no code. It answers one question — *what in the existing narrative layer survives the move
from `1d10` to `2d6 + attribute modifier + skill`?* — and it answers it with computed probabilities
rather than intuition.

The one-line answer: **the layer survives, but "one step" does not mean what it meant.**

---

## 1. The kernel it must fit

From `src/rules/wn_core.py` and the 2026-10-26 ruling:

- check: `2d6 + attribute modifier + skill level` against a difficulty;
- attributes are 3–18, modifiers −2…+2; skills 0–4, so a total modifier of **0–6**;
- difficulties **6 / 8 / 10 / 12 / 14**.

`rulebook/19_NARRATIVE_LAYER.md` still reads `STAT + Skill + 1d10`. On a flat die every +1 is worth
exactly 10 percentage points, which is why the original one-step rule could be written without a table.
On 2d6 that is no longer true, and the difference is large.

## 2. Measurement

Exact enumeration of the 36 outcomes (no simulation).

**P(2d6 + total modifier ≥ target)**

| total mod | DV 6 | DV 8 | DV 10 | DV 12 | DV 14 |
|---:|---:|---:|---:|---:|---:|
| 0 | 72.2 % | 41.7 % | 16.7 % | 2.8 % | **0.0 %** |
| 1 | 83.3 % | 58.3 % | 27.8 % | 8.3 % | **0.0 %** |
| 2 | 91.7 % | 72.2 % | 41.7 % | 16.7 % | 2.8 % |
| 3 | 97.2 % | 83.3 % | 58.3 % | 27.8 % | 8.3 % |
| 4 | 100.0 % | 91.7 % | 72.2 % | 41.7 % | 16.7 % |
| 5 | 100.0 % | 97.2 % | 83.3 % | 58.3 % | 27.8 % |
| 6 | 100.0 % | 100.0 % | 91.7 % | 72.2 % | 41.7 % |

**What one step is worth (percentage points), by total modifier**

| total mod | DV 6 | DV 8 | DV 10 | DV 12 | DV 14 |
|---:|---:|---:|---:|---:|---:|
| 0 | 11.1 | **16.7** | 11.1 | 5.6 | 0.0 |
| 1 | 8.3 | 13.9 | 13.9 | 8.3 | 2.8 |
| 2 | 5.6 | 11.1 | 16.7 | 11.1 | 5.6 |
| 3 | 2.8 | 8.3 | 13.9 | 13.9 | 8.3 |
| 4 | 0.0 | 5.6 | 11.1 | 16.7 | 11.1 |
| 5 | 0.0 | 2.8 | 8.3 | 13.9 | 13.9 |

Three facts fall out of this, and each one changes a rule:

**2.1 A step is worth most when the check is contested.** The value peaks at ≈16.7 pp where the odds
sit near 50 % and collapses to **zero** where the character is already capped. On 1d10 a step was a
constant; on 2d6 it is a function of the situation. This is *good* for NoöPunk: an invoked aspect is
worthless on a check you would pass anyway and decisive on a knife-edge one, which is exactly the
narrativist behaviour we want without a special rule to produce it.

**2.2 A numeric +1 step becomes worthless at the top of the ladder.** At DV 14 with total modifier 0
or 1 the check is **impossible before and after** the step (0.0 % both ways) — you cannot invoke your
way past a difficulty the dice cannot reach. So "one step" must be defined as **one band**, not
`+1`: `miss → cost → clean`. Band arithmetic keeps its meaning across the whole curve, whereas a
numeric step silently evaporates at DV 12–14. **This is the single required change to the layer.**

**2.3 The stacking cap is still necessary, and now provably so.** Two stacked steps at DV 8 from total
modifier 0 would be **+30.5 pp** (41.7 % → 72.2 %) — the cap is what stops the narrative economy from
buying the roll outright. KEEP the cap unchanged.

**2.4 DV 14 is a skill gate, not a modifier gate.** It is unreachable below total modifier +2 and
effectively a coin-flip only at +6. That is consistent with the Without Number ladder (14 is "heroic")
but should be stated in the layer, so a referee does not read a 0 % as a broken encounter.

## 3. Disposition of the artifacts

| artifact | disposition | why |
|---|---|---|
| `rulebook/19_NARRATIVE_LAYER.md` (171 lines) | **MODIFY** | The only file that names `1d10`. Needs: the 2d6 band table of §2, "one step = one band" in place of "+1", and the DV-14 note. Everything else in it — resolution order, "the core wins", LLM proposes and never picks a modifier — is correct and survives untouched. |
| `src/rules/narrative_layer.py` (230 lines) | **KEEP**, one semantic change | Dice-agnostic: it owns `can_invoke`, the one-invoke cap, the point pool, `BAND_TO_MOVE` and `gm_move`. It never rolls. Only the meaning of `invoke_step()` needs to become band-movement, and that is a docstring plus one mapping, not a rewrite. |
| `src/rules/aspects_prototype.py` (279 lines) | **MODIFY — keep the model, retire the 4dF maths** | The aspect/pool model is sound and should be the base. But its probability helpers (`success_probability`, `value_of_bonus`, `spread_of_the_roll`, `stacked_success_probability`) are exact **4dF** functions, and its own docstring states a 4dF truth that is false on 2d6: *"a +2 is not a modifier, it is most of the roll."* On 2d6 a +2 is 30.5 pp at DV 8 — substantial, not dominant. Those helpers must be re-derived or deleted, never left as a second, contradictory model of the same rules. |
| `strategy_game/rpg/fate.py` (288 lines) | **KEEP AS-IS** | The 4dF crossover layer, explicitly out of scope for this register (#689 §11). It is internally consistent because it is a *Fate* game. Nothing here touches it. |
| `docs/design/ISSUE_229_NARRATIVE_LAYER.md`, `ISSUE_200_ASPECTS_PROTOTYPE.md` | **KEEP as history** | Design records. They explain why the layer has the anti-exploit rule at all; superseding them would delete the reasoning without replacing it. |

## 4. What this means for the register's open decisions

- **P1 (disposition of `19_NARRATIVE_LAYER`)** — answered by §3: re-anchor, do not retire. Retiring it
  would delete the only measured anti-exploit rule in the repository.
- **P2 (bands on by default?)** — unaffected by this memo; still the author's call.
- **P4 (the pool)** — unaffected; note only that §2.3 now gives a numeric reason to keep the cap.
- **P8 (closed move set)** — Stage 1's job, not this one.

## 5. What Stage 0 does not do

- No rulebook edit, no code change, no tests, no new numbers adopted. §3 is a *disposition*, not an
  implementation.
- No playtest evidence: §2 is arithmetic, and arithmetic is not a playtest. Stage 4 is where that
  happens.

## 6. Reproduction

Every figure in §2 is exact enumeration of `2d6`, not a simulation:

```python
from collections import Counter
import itertools
c = Counter(a + b for a, b in itertools.product(range(1, 7), repeat=2))
p = lambda total, dv: sum(n for s, n in c.items() if s + total >= dv) / 36
```

Anyone can re-derive the tables in a few lines, which is the point: a design claim that cannot be
re-derived is a preference.
