# Psionics module supersession: #648 → #652

**Author decision, 2026-10-26:** the psionic subsystem lives in **`src/rules/psionics.py`** (Python) and
**`godot/core/psionics.gd`** (Godot). The model merged in #648 — `src/rules/swn_psionics.py`,
`godot/core/psychic_effort.gd`, `godot/tests/test_psychic_effort.gd` — is **superseded and removed**.

This page exists so the removal is a decision with a record, not a quiet deletion: #648 was merged to
`main` before this change landed, so its files had callers, tests and a status row in the design ledger.

## Why one module

Two modules means two Effort formulas, two commitment lifecycles and two places for a save format to
drift. The repository has already paid for that once: `docs/rules/WN_BASE_SYSTEM.md` §1 exists because a
contract and a kernel disagreed about the saving-throw base. Psionics is small enough that a single home
is cheap and large enough that a fork is not.

## What was carried over (nothing was dropped)

Everything #648 actually implemented now lives in the surviving module, with its assertions ported:

| #648 behaviour | Where it now lives |
| --- | --- |
| Effort capacity `1 + best(WIS, CON) modifier + highest discipline rank` | `psionics.max_effort()`, `NoopunkPsionics.max_effort()` |
| Named commitment keys, unique per pool | `EffortPool.reservations`, `EffortPool.commit(key, duration)` |
| Unique-key protection (a second `commit` on the same key is an error) | `PsiError("… is already committed")`, `false` in Godot |
| `ACTIVE` / `SCENE` / `DAY` durations | `psionics.Duration`, `EffortPool.DURATIONS` |
| Scene/day Effort cannot be refunded early | `EffortPool.release()` raises for non-`ACTIVE`; Godot returns `false` |
| `end_scene()` frees scene and active, keeps day | `EffortPool.end_scene()` |
| `rest()` frees everything | `EffortPool.rest()` (and `night_rest()` as the alias `GameState` calls) |
| Snapshot / restore with committed Effort preserved | `EffortPool.snapshot()`, `EffortPool.from_snapshot()`, `EffortPool.restore()` in Godot |
| Malformed restore rejected, never silently reset | `from_snapshot()` raises `PsiError`; Godot `restore()` returns `false` |
| Discipline rank prerequisite on a commitment | `Practitioner.may_use()` / `learn()` — now a *training gate* rather than a per-commit check |
| Foreign discipline and out-of-range scores rejected | `Practitioner.__post_init__` |

Their Python tests were replaced, not deleted: every assertion above has an equivalent in
`tests/test_swn_psionics.py`, in the classes `CommitmentLifecycleTests` and `SnapshotTests`. The Godot
suite `godot/tests/test_psychic_effort.gd` was folded into `godot/tests/test_psionics.gd`.

## What is new

- **A technique catalogue** (`data/rules/psionics_techniques.json`): six discipline cores and 18
  techniques with minimum skill levels, Effort costs, durations and effect text. This is original NoöPunk
  content, marked `provisional`; the author owns its numbers.
- **The training gate at use time**: `may_use()` is a permission check, so an untaught character takes
  the failure branch instead of rolling a hard check (the SWN shape, the NoöPunk ontology).
- **Torching**, with its d6 attribute price and the feral threshold.
- **Scenario wiring**: a psionic dialogue choice in the first case, gated before the dice, with the
  reading recorded as an impression rather than a finding.
- **Save integration**: `GameState` stores `effort_pool.snapshot()` and restores it, refusing a malformed
  record instead of resetting the pool.

## What was deliberately *not* taken from SWN

SWN Revised has **no verified SRD licence**
([rights matrix](../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md)). The catalogue is not SWN's technique
list: no power name, table or sentence from the book is reproduced. Where a technique's *numbers*
resemble another game's, that is unprotected mechanics expressed independently. A table that owns the
book should use its technique text for effects; this repository supplies the procedure, the pool and the
gate.

The design ledger's earlier note — *"technique prerequisites, effects, overexertion: not implemented;
must be sourced from the purchased book, not improvised"* — is still true of **SWN's own list**. What
exists here is a NoöPunk catalogue of our own making, which is why it is marked provisional and why
`IS_CANONICAL` is absent by design: the author decides when a technique becomes canon.

## Migration for a caller

```python
# before (#648)
from rules.swn_psionics import Psychic, Duration
psychic = Psychic(wisdom=14, constitution=10, disciplines={"Telepathy": 1})
psychic.commit("contact", "Telepathy", duration=Duration.ACTIVE)
psychic.free

# after (#652)
from rules.psionics import Practitioner, Duration
character = Practitioner(attributes={..., "WIS": 14, "CON": 10}, skills={"Telepathy": 1})
character.pool.commit("contact", Duration.ACTIVE)
character.pool.available
```

In Godot:

```gdscript
# before (#648)
var psi := PsychicEffort.new(14, 10, {"Telepathy": 1})
psi.commit("contact", "Telepathy", 0, "active")

# after (#652)
var psi := NoopunkPsionics.new()
var pool := NoopunkPsionics.EffortPool.new(3)
pool.commit("contact", "active")
psi.use("thread", {"Telepathy": 1}, pool)
```

— Ai (愛)
