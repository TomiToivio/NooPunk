# Issue #217 AC2: the open resolution semantics

**Status: PROPOSAL — a prototype, not a migration.** `src/rules/issue217_resolution.py` is marked
`IS_CANONICAL = False`, `src/rules/core.py` is untouched, and the shipped `STAT + Skill + 1d10`
check still resolves exactly as before. This issue's own AC3 requires a tabletop specification and
an author decision *before* any runtime migration, so nothing is migrated here.

## What was already done, so it is not restated here

AC2 names five things. Three already existed, and re-implementing them would have created a second
definition of the same rule:

| AC2 item | State | Where |
| --- | --- | --- |
| tie / opposed checks | **done** | `kernel_prototype.opposed_ladder` — equal totals stay an unresolved tie; `core.compare_opposed` pins the same rule for the shipped engine |
| bounded modifiers | **done** | `resolve_ladder(cap_situational=True)` caps situational steps at `MAX_SITUATIONAL_STEPS` (±2) |
| action points | **not this issue** | cross-domain, owned by #225 |
| **trained / untrained −1** | **open → implemented here** | nothing implemented it: `rating_step` maps a Skill straight onto the ladder with no notion of training |
| **partial successes** | **open → defined here** | the prototype's bands were `failure` / `success` / `success_with_style`; no partial existed |

Two more AC2 notes before implementing anything: AC1 (*compare the 4dF combination candidates*) is
also already satisfied by #209/#215 — three named candidates, a recorded recommendation, and
probability tests — so this work starts from AC2, not AC1.

## 1. Trained / untrained −1

An untrained Skill applies **one ladder step** (`UNTRAINED_STEP_PENALTY = -1`), applied **after**
the candidate combines STAT and Skill.

The order is a design decision, not an implementation detail: training is a property of the
*character*, so it must compose identically with candidates A, B and C. Folding it into one
candidate would quietly make the rule candidate-specific, and the guard fails if the penalty is
folded anywhere.

**Measured cost of being untrained** (exact, 81 outcomes, no simulation):

| Configuration | Trained | Untrained | Cost |
| --- | ---: | ---: | ---: |
| any candidate, STAT 5 / Skill 5, difficulty 0 | 61.7% | 38.3% | **23.5 points** |

The penalty is worth roughly a quarter of the success chance at the midpoint — noticeable without
being disqualifying, which is the stated intent of a −1.

**And it separates competence in the direction #200 asks for.** An untrained brute (STAT 9,
Skill 1) against a trained specialist (STAT 5, Skill 9), both at difficulty 0:

| Candidate | Untrained brute | Trained specialist |
| --- | ---: | ---: |
| A additive | 18.5% | 93.8% |
| B averaged | 38.3% | 81.5% |
| **C skill-primary** | **6.2%** | **93.8%** |

Under C the trained specialist is at 93.8% while the untrained brute is at 6.2%; under B the brute
is at 38.3%. That is the same finding the kernel prototype recorded — *"an untrained brute does not
keep parity under C"* — now measured **with** the untrained rule rather than against a
same-named-but-absent one.

## 2. Partial success, off by default

Where a partial band *should* sit is a design decision, so the module measures the readings instead
of picking one silently. Exact distributions, candidate C, STAT 5 / Skill 5, difficulty 0:

| Policy | failure | partial | success | success with style |
| --- | ---: | ---: | ---: | ---: |
| `off` (today) | 38.3% | — | 55.6% | 6.2% |
| **`at_minus_one` (recommended)** | 18.5% | **19.8%** | 55.6% | 6.2% |
| `at_zero` | 38.3% | 23.5% | 32.1% | 6.2% |

- **`at_minus_one`** adds a band without touching the boundary of success: every margin −1 result
  becomes a partial with a cost instead of a failure. Nothing that used to succeed stops
  succeeding.
- **`at_zero`** makes full success **strictly harder** (55.6% → 32.1%) by turning a bare success
  into a partial. That is a balance change wearing a vocabulary change's clothes, which is exactly
  why it is not the default.
- **`off`** reproduces the shipped bands for every margin, asserted — the "off" setting is the
  current behaviour, not a near-miss of it.

The recommendation is `at_minus_one`. **The author owns it**, and `partial="off"` reproduces
today's bands exactly for anyone who disagrees.

## 3. Verification

`tests/test_issue217_resolution.py`, 15 tests: the penalty composes with every candidate, never
raises a step, clamps at the ladder floor, and its measured cost equals the probability difference;
the 4dF distribution is exact (81 outcomes, mean 0, symmetric, `P(0) = 19/81`); bands sum to exactly
1 over a sweep; `p_success_at_least` agrees with the off policy's success bands, which pins the
success threshold itself; probability is monotone in difficulty; and the shipped 1d10 check still
resolves identically.

**Sabotage 8/8**, byte-identical restore: the penalty becoming a bonus, the penalty folded into one
candidate, `off` quietly converting a one-step miss, `at_zero` swallowing a bare success, a
mis-scaled 4dF distribution, the style boundary ignored, the clamp dropped, and the success
threshold made strict.

## 4. What is still open on #217

- **AC3** — the runtime migration (Python/Godot/Concordia) waits on the author selecting a
  candidate and the partial-success policy. The tabletop rules are the source of truth.
- **AC4** — legacy save conversion with round-trip loss measurement is untouched.
- **The author's two decisions**: the candidate (the prototype recommends **C, skill-primary**) and
  the partial policy (this document recommends **`at_minus_one`**).
