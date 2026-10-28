# Verdict: the paradigm-shock case (#699)

**Question this case exists to answer:** did the mechanism make the *player* choose differently, or did
it merely accumulate conditions? That distinction is the whole claim of D46–D48, and a case that
illustrates the design without testing it is worse than no case at all.

Run: `python tools/paradigm_shock_case.py` — deterministic, headless, no dice.

---

## What the case does

A character holds a belief — *Saint Aurélien's is a psychiatric hospital: it treats people* — and meets
evidence that contradicts it: the duty files for the last four admissions are written in the future
tense, and one describes what the character will do tomorrow.

Two branches, both played to a conclusion:

| branch | resulting world view | condition (layer 3) |
|---|---|---|
| **accept** | `received → reframed` | `:reframe` — the character must act on the revised belief, not the old one |
| **hold** | `received → fractured` | `:denial` — the character must explain away or avoid the evidence |

Both branches produce a **different** condition, and neither is a penalty for choosing wrongly. Running the
tool twice produces identical output.

## Findings, stated as findings

**1. D48 holds.** The two branches end in different world-view states, the conditions differ, and `CharacterMind.apply_choice()` takes only an explicit `accept: bool` — there is no function
in `src/rules/mental_load.py` that accepts a random number generator, a die or a seed — the
refusal test asserts this over every public signature, and the module's own import-time guard fails
loudly if one is ever added. A conviction cannot be overwritten by a roll, because no roll reaches it.

**2. D46 was NOT exercised, and this case must not be cited as evidence for it.** The case is carried
entirely by layer 4. No *condition* was required to hold a scene together, so the case says nothing
about whether conditions can carry one. Claiming otherwise would be exactly the overclaim this issue
was written to prevent.

**3. D49 was not triggered.** The evidence trigger for reopening EP-grade stress is a written case that
conditions demonstrably cannot carry. Since no condition was asked to carry anything here, the trigger
has not fired — and it should not be pulled on appetite.

## What would actually test D46

A second case in which a **condition**, not a belief, carries the scene:

- a lasting condition whose only exit is a WWN major project;
- running over three scenes, so the duration is real rather than asserted;
- with the player visibly choosing whether to spend those scenes on it — the same
  choose-versus-accumulate question, asked of layer 3 instead of layer 4.

If that case shows conditions degrading into bookkeeping — a list that grows without changing any
decision — then D46 is falsified, and D49 reopens with a named case rather than a preference.

## Scope notes

Nothing in this case is canon. The ward, the belief and the files are test fixtures that read like a
scene; no named canon entity is used, and the case adds no rule. `src/rules/mental_load.py` deliberately
carries **no severity scale and no recovery rules**: `clears_when` is prose because the recovery rule is
the author's to set, and a number invented here would silently become canon.
