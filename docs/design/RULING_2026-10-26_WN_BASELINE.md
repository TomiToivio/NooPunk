# Author ruling 2026-10-26 — the Without Number baseline

**This is a superseding ruling. Read it before the records it supersedes.**

> *"For beginning, use CWN/SWN/AWN/WWN system for everything. Make the stats, skills, all rules
> based on them. We will modify later."*

## What it changes

| Was | Now |
| --- | --- |
| **#566 / D40:** `1d10` stays for layer A; the WN family is consulted for *procedures* | The **Without Number engine is the baseline for the tabletop layer**: `2d6 + attribute modifier + skill level` against a difficulty |
| Attributes `FIT / REF / INT / SOC / CYB / PSY` | **`Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma`** (3–18, modifiers −2..+2) |
| NoöPunk skill list | **WN skill list** |
| `ISSUE_615_RULES_BASELINE.md` §3 rows 1–3 (kernel stays, SOC survives) | Superseded by this ruling. The *procedure-vs-kernel* distinction in that document no longer governs the kernel |

## What it does not change

- **Licensing still binds.** *Cities Without Number* and *Worlds Without Number* SRDs are CC0 and
  verified; **Stars Without Number and Ashes Without Number remain `blocked-unverified`** (#569).
  Adopting "the WN system" therefore means implementing the engine from the **CWN/WWN SRDs**, and
  treating SWN/AWN as design references. It never means reproducing their text.
- **No canon invention.** Anything the SRD states is implemented as stated. Anything it does not
  state is left out and named as absent.
- **The strategy/RPG crossover layer** (`strategy_game/`, Fate `4dF`, #389/#482) is untouched by
  this ruling until a separate decision addresses it.
- **Approved rulings on setting** — panpsychic PSI, pre-Fall canon, no classes-as-slots — are not
  game-mechanical and are unchanged.

## What is implemented so far

`src/rules/wn_core.py` + `tests/test_wn_core.py` (19 tests), containing only what was **verified**
against the SRD:

- six attributes on 3–18 and the modifier bands (SRD 1.1.2);
- skill check `2d6 + attribute modifier + skill level` vs difficulty (SRD 2.3.0);
- difficulties `6 / 8 / 10 / 12 / 14` (SRD 2.3.1);
- circumstances bounded `−2..+2`, aid capped at `+1` (SRD 2.3.1, 2.3.3);
- opposed checks: higher roll wins, **ties reported as undefined** because the SRD gives no
  tie-break and inventing one would be a rule no source supports (SRD 2.3.4).

**Still absent, and named rather than faked:** saving throws, classes and Edges, Foci, Effort,
Shock/Trauma, equipment, progression. Each needs its own verified reading. That is the next work,
not an oversight.

## Sequence

This ruling is **Stage A→B** of the roadmap in `ISSUE_615_RULES_BASELINE.md` §8: adopt the
baseline transparently now, modify later. "We will modify later" is the author's own framing and it
is recorded as such, so a later divergence is a planned stage rather than a contradiction.

## Superseded records

- `docs/design/ISSUE_566_ACCEPTANCE.md` — the "layer A only / `1d10` stays" scope answer
- `docs/CWN_CHASSIS.md` — the CONFIRMED four answers
- `docs/design/ISSUE_615_RULES_BASELINE.md` §3 rows 1–3
- `docs/design/AUTHOR_DECISION_QUEUE.md` — D40 moves from *answered* to *superseded*
