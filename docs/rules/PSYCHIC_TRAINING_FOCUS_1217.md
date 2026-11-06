# The Psychic Training focus, implemented (#1217 line 11)

> **Status: implemented mechanics, prose not reproduced.** `src/rules/psychic_training.py` composes the existing SWN
> modules to deliver the focus the author quoted in #1178 §1. It changes no rulebook formula and invents no table.

For weeks this repository refused to implement this focus, and the refusal was right: the level benefits are printed
rules, and `psi_edges` gates them behind a `Citation` so that a remembered table could not be passed off as a read one.
The author then quoted the focus in full. That removes the reason for the gate — and does **not** remove the licence
rule. So the code holds the *mechanics*, and `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md` still governs the
prose. `psi_access.PSYCHIC_TRAINING_FOCUS_AVAILABLE` is now `True`, with a reason that names both the source and the
licence.

## What the focus does, in code

| printed rule | implementation |
|---|---|
| prerequisite: a Psychic, or an Adventurer with the Partial Psychic option | `take_focus(..., partial=True)` requires `Psychic.restricted_discipline` to be set |
| a Partial Psychic trains only the discipline they chose | refused with a message naming both disciplines |
| taken once only | `already_taken=True` refuses |
| level 1: gain any psychic skill as a bonus | `psychic.disciplines[discipline] += 1`, capped at rank 4 |
| level 1: if that reaches rank 1, choose a free level-1 technique of that discipline | `choose_technique()` — the technique must belong to the discipline and have `min_skill ≤ 1` |
| level 1: maximum Effort +1 | `effort_max(psychic, training)` = `psychic.capacity + 1` |
| level 2: one point per level gained, toward the skill or a technique of it, bankable | `advance_to_level_two()` banks `character_level - 1` points; `spend_point()` spends them |
| level 2: points are awarded retroactively | `retroactive_points(character_level)` |

## The three decisions a reader should argue with

1. **The Effort increase is a property of the focus, not a mutation of the psychic.** `Psychic.capacity` is SWN's own
   arithmetic; patching a bonus into it would fork a published formula. `effort_max()` sums instead.
   Note the arithmetic a table will meet: raising the discipline to rank 1 already raises `capacity` by one *by the SWN
   rule*, so the focus takes a rank-0 character from 2 to 4, not from 2 to 3. The test says so explicitly.
2. **"Retroactively" is read as one point per character level already gained** — a character who takes level 2 at
   character level 5 receives four points at once. The book states the award is retroactive without printing a formula;
   this is the plain reading and the one item here that needs Tomi's confirmation rather than a test.
3. **The technique grant is a permission, not a discount.** Using the free technique still costs its Effort and still
   requires its check. Nothing in this module rolls dice.

## What it deliberately does not do

* It does **not** touch `psionics.py`, `swn_psionics.py` or `psi_access.py`'s decision functions — it composes them.
* It does **not** add the focus to the CWN Focus list. CWN Foci (`cwn_foci.FOCI`) and the SWN focus are different
  systems; a character takes one or the other, and the lifepath builder's `foci` argument stays CWN-only.
* It does **not** grant a Mentalist anything. The AWN Mentalist holds **arts** and its own Effort pool and carries no
  SWN discipline map; line 10 of the tracker is satisfied by `psi_access.PC_EDGES` + `rookie_build` + `awn_mentalist`,
  and the test module asserts that separation rather than inventing a bridge.
* It does **not** open Precognition, Biopsionics, Metapsionics or Teleportation to players. The focus still refuses a
  discipline outside `PC_DISCIPLINES`.

## Tests

`tests/test_psychic_training_1217.py` — **24 tests**: selection (bonus skill, existing rank improved, once-only,
non-player discipline refused, Partial Psychic restriction both ways, rank-4 cap), technique selection (correct,
wrong discipline, too high a rank, unknown), level 2 (retroactive counts, banking, double-advance refused, spending on
skill and on a technique, spending without points, spending on another discipline), and the Mentalist separation.

Every technique name comes from `data/rules/psionics_techniques.json` at test time — no technique is hard-coded, so a
catalogue change cannot leave a stale assertion passing.

## Still open on this line

The tracker's line 11 also says *"verify published rules then implement"* — that is done for the focus. What is not
done, and cannot be done from the repository alone:

* the **retroactive formula** needs one word from Tomi (see §"three decisions", item 2);
* the **Partial Psychic** option itself (the Adventurer's restricted-discipline package) is modelled only as
  `Psychic.restricted_discipline`; whether the character-creation flow offers it is part of the lifepath work.
