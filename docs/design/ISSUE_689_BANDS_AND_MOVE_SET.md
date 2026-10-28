# The narrative layer on 2d6: bands, the closed move set, and what happened to the legacy artifacts

**Issue #689, stages 0 and 1.** This note records the two decisions the code now implements and the
fate of the three legacy artifacts the re-anchoring had to settle. It changes no other rule, and it
does not reopen the design questions that belong to the author (§5).

---

## 1. The re-anchoring, and why it is not a redesign

`rulebook/19_NARRATIVE_LAYER.md` (#229) states the optional narrative layer: bounded aspects, three
effect classes, one ladder step per aspect, one invoke per roll, a compel economy, GM moves read off
the band. The 2026-10-26 baseline replaced its core with the Without Number check, and left the
chapter and the module describing a `1d10` ladder that no longer exists.

Re-anchoring means the layer now speaks the game's actual dice:

| | retired | now |
| --- | --- | --- |
| check | `STAT + Skill + 1d10` vs a DV | `2d6 + attribute modifier + skill rank` vs 6 / 8 / 10 / 12 / 14 |
| save | `1d10` band | `1d20` against the save target |
| step | one rung of a directed −3…+3 ladder | `+1` — `2d6`'s own granularity |
| bands | `brutal / severe / solid / glancing` | `miss / cost / clean / style` |
| moves | `reward / cost / complication / escalate` | `escalate / cost / reward / reward_and_aspect` |

No invariant moved. The cap is still one invocation per roll; an aspect still cannot produce a
rating; the pool is still bounded at 0–3 and still unnamed (that name is the author's to write).

## 2. The band arithmetic, measured

`margin = total − difficulty`. Boundaries: **miss** ≤ −1, **cost** 0–1, **clean** 2–4, **style** ≥ 5.

| modifier (DV 8) | miss | cost | clean | style |
| --- | --- | --- | --- | --- |
| +0 | 21/36 (58.3%) | 9/36 (25.0%) | 6/36 (16.7%) | 0 |
| +1 | 15/36 (41.7%) | 11/36 (30.6%) | 9/36 (25.0%) | 1/36 (2.8%) |
| +2 | 10/36 (27.8%) | 11/36 (30.6%) | 12/36 (33.3%) | 3/36 (8.3%) |

Three properties the boundaries were chosen to have, each of them a test rather than a taste:

1. **One step is worth a whole difficulty step.** +2 at DV 8 succeeds exactly as often as +0 at DV 6
   (26/36). That is the argument for the cap being *one*: a second invocation would buy a difficulty
   step, and a third would make failure look arbitrary rather than dangerous.
2. **One step is +16.7 percentage points at the standard difficulty**, which is #691's independently
   measured figure, re-derived here from the bands so the two cannot drift apart.
3. **The layer cannot rescue an impossible check.** At DV 14 a +2 is worth 2.8 pp. An aspect is
   leverage on a real chance, not a substitute for one.

`band_distribution()` in `src/rules/narrative_layer.py` enumerates all 36 outcomes; the tests pin the
four shares and the two properties above.

## 3. The closed move set

Eight procedures, each a trigger plus the four banded outcomes, each rolled with an existing skill or
an existing save: *Read a situation*, *Read a person*, *Apply pressure*, *Hold steady*, *Cross a
threshold*, *Set up*, *Ground yourself*, *Contact the noösphere*.

Why eight and not a catalogue: a move list is content that has to be maintained, translated and
tested, and every entry is a promise that the fiction will keep resolving that way. Eight procedures
cover the case types the first playable slice actually has (investigate, interrogate, pressure,
endure, infiltrate, prepare, recover, contact). `CLOSED_SET_SIZE` asserts the number, so a ninth move
must change the constant and the chapter together — the friction is the point.

Grants are banded and deliberately narrow: questions, aspects, cancelled conditions. **No grant is a
modifier**, because a modifier is what an invocation is, and it is capped.

## 4. Disposition of the three legacy artifacts

| Artifact | Decision | Why |
| --- | --- | --- |
| `src/rules/narrative_layer.py` | **MODIFY** (done here) | the layer's gate is still the right gate; only its band vocabulary and its step arithmetic were stale. Everything load-bearing is unchanged: `invoke_step()` returns 1 and takes no honourable parameter, `can_invoke()` refuses a second invocation, `validate_proposal()` refuses an LLM-proposed modifier. |
| `src/rules/aspects_prototype.py` | **RETIRE from play, keep as evidence** | it is the 4dF measurement that justified the cap (63% within ±1, four stacked aspects reaching 100%). Its numbers are no longer the game's numbers; its *method* is why the rules exist. Nothing in play imports it. |
| `strategy_game/rpg/fate.py` | **KEEP as a labelled legacy prototype** | it is the crossover strategy game's 4dF engine, which the baseline explicitly calls a legacy prototype rather than an exception. Porting it is a separate decision and is not part of this layer. |

The old band keys are refused rather than aliased: `gm_move(band="brutal")` raises. An alias would
let a stale caller keep working while meaning something the chapter no longer says.

## 5. What this does not decide

P1–P11 in #689 remain open, and this note settles none of them: whether the layer survives as canon
at all (P1) is still the author's call — this work makes the question *answerable* by making the
layer runnable on the real dice; bands default-on versus opt-in (P2); the pool's name or its removal
(P4); The Veil's states (P5); the mind system's shape (P3); and the automation bar (P11).

The mind system (stage 3) and the two-axis paradigm ledger (stage 2) are **not** implemented here.
They need their own chapter text first, per the tabletop-first gate.

## 6. Licensing

Everything in this stage is *shape*: band boundaries, a closed procedure list, and a resolver. No
text, table or stat block from Apocalypse World, *The Sprawl*, *The Veil*, Fate Core,
*Transhumanity's Fate* or Eclipse Phase is reproduced; the outcome sentences are written for NoöPunk.
The one borrowed idea named in the chapter — reading a margin into graded outcomes — is a mechanic,
not an expression. See #615 §"Public SRDs, free rules references, and licensing sources" for the
rights audit and `docs/sources/GAME_SYSTEM_RIGHTS.md` for the per-source ledger.
