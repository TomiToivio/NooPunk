# Issue #229 — the narrative layer: aspects, consequences and GM moves

**Status: PROPOSAL landed as a bounded layer, not a calibration.** `rulebook/19_NARRATIVE_LAYER.md`
is the canonical optional layer; `src/rules/narrative_layer.py` enforces its two safety rules in
code, with `IS_CANONICAL = False`.

Cross-links: #200 (epic), #233 (the prototype canonised), #219/#220 (the realms it sits on),
#226 (investigation, untouched).

## This canonises a measured prototype rather than starting again

`docs/design/ISSUE_200_ASPECTS_PROTOTYPE.md` (#233) already answered *what a tag, a cost and a
consequence are allowed to do*, under #200's own constraint: **"no tag-only character sheets …
avoid uncapped numerical exploits."** Two of its measurements decided this design, and both are
quoted in the chapter and asserted by the guard:

1. **A +2 invoke is not "bounded".** On a 4dF core, 63% of outcomes fall within ±1, so a +2 moves
   the odds by **+32.1pp** — turning "likely" into "near-certain". A single step moves **+19.8pp**.
2. **The per-roll cap is load-bearing.** Without it, **four stacked aspects reach exactly 100%** —
   auto-success, bought with four tags.

## The two rules, and why they are expressed the way they are

> An aspect grants **ONE ladder step**, never a number of its own.
> Invocations are capped at **one per roll**.

The bound is expressed as **one step on the core ladder** rather than a fixed `+1`, which is a
deliberate choice: the repo's scale is mid-migration (`-3…+3` directed, with the d10 runtime still
the shipped adapter), and a fixed numeral would silently change meaning when the scale lands. A
*step* means the same thing under either arithmetic, and the layer adds no arithmetic of its own —
consistent with the one-step vocabulary already used for armor (#219), reputation (#220) and First
Aid (`RULEBOOK.md` §51).

## Enforced as capability absence, not as prose

- **`invoke_step()` takes and ignores `*args`/`**kwargs`.** A caller cannot pass a "bigger"
  invocation; the guard asserts the function has **no named parameter**, so an edit that honoured
  one would have to change the pinned signature.
- **`can_invoke()` is the cap**, and `assert_can_invoke()` is the refusal path.
- **`effect_class_may_produce_a_rating()` returns False for every class, and `EffectClass` has no
  `RATING` member.** The guard additionally asserts that `Aspect` carries **no numeric field**
  (`rating`/`score`/`value`/`bonus`/`stat`) and that no `aspect_rating`/`stat_from_aspect` API
  exists — the "tag-only character" failure cannot be reached by accident.
- **Spending more points never buys a bigger step**: `ResourcePool.invoke()` returns the constant
  step regardless of the spend, and `earn()` is capped at the pool bound.

## Deterministic precedence

Roll first; the core resolves; the margin selects the band; **at most one aspect moves the result
one step**; a GM move is read from the band. Only then does an LLM narrate. `validate_proposal()`
**rejects** a proposed numeric modifier outright and rejects a malformed aspect rather than
narrating it into existence — the same seam #220 established, reused.

## GM moves are descriptions, not modifiers

`GM_MOVES` are prose; the guard asserts none of them contains a digit, so a move cannot smuggle a
modifier. The move is chosen from the band the core already produced, so **partial success is a
band, not a second roll** — asserted explicitly.

## Agency

The chapter states, and the guard asserts: *"A compel is never a punishment and never a loss of
control"*, a compel *"cannot dictate a choice"*, and *"the player decides what the character does"*.
A compel changes the situation and pays for it.

## GNS parity made structural

`styles_share_one_core()` returns True because all three styles map to the **same** core string, and
the guard additionally asserts `social.band_for_margin is physical_combat.band_for_margin` — parity
is only real if the realm modules actually share the function, so the test checks the identity
rather than the claim.

## AC mapping

| AC | Where |
| --- | --- |
| 1 — optional bounded tag layer over separate Attributes/Skills, with permissions, modifiers, duration, cancellation | §*Aspect anatomy*, §*The two rules*; `Aspect`, `EffectClass` |
| 2 — relationship consequences, difficult choices, drives, narrative resources, invokes/compels, partial-success/GM moves | §*Narrative resources*, §*Invokes, compels, and difficult choices*, §*GM moves and partial success*, §*Character drives* |
| 3 — agency and numerical precedence; no tag-only characters, no hidden LLM modifiers | §*Numerical precedence*, §*Agency*; `validate_proposal`, `NoRatingTests` |
| 4 — playtest investigation / intrigue / combat with GNS parity | §*Worked examples* (all three), §*GNS parity*; `ParityTests` |
| 5 — cross-links, tests, comment | cross-links; `tests/test_issue229_narrative_layer.py`; the PR |

## Deliberately not done

- **No resource name** — naming is canon and the prototype declined it; the chapter specifies the
  mechanics and leaves the name to the author.
- **No numeric stress track** — `RULEBOOK.md` §51 is a fiction-first consequence vocabulary and harm
  does not advance by arithmetic, so a stress track would contradict canon rather than extend it.
- **No new Skills, STATs or derived statistics**; no rating from an aspect.
- **No realm procedure redefined** (#219/#220/#226 own those).
- **No calibration** — every value PROVISIONAL; module non-canonical.

## Verification

- Full suite green (see PR); `ruff` clean.
- `tests/test_issue229_narrative_layer.py` — 46 tests, sabotage-proven **26/26 caught, 4/4 controls
  clean, byte-identical restores**.
- The sabotage round found **two real weaknesses in my own guard**: a phrase that survived in a
  section heading, and another that survived in a second sentence elsewhere in the chapter. Both
  were tightened to assert the *specific sentence* rather than the bare phrase, before shipping.
