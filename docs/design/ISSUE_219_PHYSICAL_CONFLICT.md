# Issue #219 — physical conflict: combat, wounds and tactical actions

**Status: PROPOSAL landed as a procedure, not a calibration.** `rulebook/3_PHYSICAL.md` now carries
the playable physical-conflict procedure; `src/rules/physical_combat.py` executes its arithmetic
with `IS_CANONICAL = False`. Every number is the author's to set.

Cross-links: #200 (epic), #225 (the shared clock this consumes), #228 (#221's hardware and the
equipment catalog stay reserved), §51/§52 (mapped into, not edited).

## The two constraints that shaped the design

### 1. `RULEBOOK.md` §51 is guarded as NON-NUMERIC

`tests/test_issues171_180_chapter_consolidation.py::test_harm_rules_stay_non_numeric` fails the
build if §51 gains dice notation or a `damage = N` form. §51 is a **fiction-first consequence
vocabulary** — Scratched → Wounded → Critical → Down — and it explicitly says exact transition
rules, damage values and initiative "remain explicit design questions".

So the combat procedure **maps into** that ladder from `rulebook/3_PHYSICAL.md` and does not touch
§51. The mapping is the specified artefact; the ladder is quoted verbatim in both the chapter and
the module (`LADDER`), and the guard asserts the two agree.

### 2. The ladder is a state, not a counter

§51 says a wound state is "already established by the fiction … not a hidden damage engine" and
that "repeated harm does not automatically step a character along the list". A conventional
accumulating damage track would quietly contradict that.

The design therefore makes the effect function **stateless**: `wound_state(total, target)` takes no
previous state, so two solid hits cannot add up to Critical. The guard proves this twice — once
behaviourally (two calls with the same inputs give the same rung) and once structurally (the
function's signature has no `previous`/`current`/`prior` parameter, so an accumulating track could
not be added without changing the interface the guard pins).

## Design decisions

### Armor and cover are expressed in the vocabulary the chapter already had

- **Armor** is rated by the **damage types** the chapter already lists (ballistic, kinetic,
  energy, electrical, chemical, radiation, psychotronic). Its effect is **one ladder step**, never
  a subtraction, and it never stacks with itself. This composes with §51's existing rule that
  First Aid moves a wound "one step up the ladder" — one vocabulary, two rules.
- **Cover** is a **difficulty step** on the authored §4.2 ladder, so simple mode can never invent a
  target number. `simple_target_number()` is asserted to return only values from
  `(9, 13, 15, 17, 21, 24, 29)`.

### Initiative and AP are consumed, not redefined

`rulebook/18_CROSS_DOMAIN_STATE.md` (#225, merged `92283d4`) already fixes one clock, 3 AP per
actor per exchange, descending-REF order and the borrow-for-a-reaction rule. This chapter adds only
what is physical — bands, engagement, Provoke-on-disengage, cover states — and states that
consuming it "must not restate it". The guard asserts the module's costs agree with
`cross_domain_state.AP_COSTS` so the two can never drift.

The scarcity is the design: with 3 AP, a character **cannot** simultaneously dodge, resist a
telepathic probe and defend a network. That is stated explicitly rather than left implicit.

### AC3 — simple and advanced modes on one numerical core, proved by enumeration

This was the acceptance criterion most likely to be discharged with prose. Instead, **mode parity is
a property of a function and is tested exhaustively**: for all 861 combinations of `total ∈ [0,40]`
and `target ∈ [9,29]`, both modes return the same rung — because both call the *same*
`wound_state()`, and the modes differ only in where the target number came from. Monotonicity
(a better roll never yields a less severe rung), armor monotonicity, and exhaustive band coverage
are tested the same way.

### Machines get a function ladder, not a wound ladder

Drones and vehicles have no biology, so the same bands drive **Operational → Impaired → Disabled →
Destroyed**. `machine_state()` shares the band and mitigation code with `wound_state()`, so the two
ladders cannot diverge. Crew and machine remain separate ladders.

### Suppression never wounds

`resist_suppression()` returns a boolean and has no ladder output at all; the guard asserts its
result is never a member of `LADDER`. Pinned is a status — losing AP and movement toward the source
— not an injury, which is what keeps morale pressure from being a stealth damage system.

## AC mapping

| AC | Where |
| --- | --- |
| 1 — initiative, AP, movement, positioning, melee/ranged, cover, armor, suppression, reaction/defence, non-lethal | `3_PHYSICAL.md` §*Physical conflict* (bands, cover, armor, suppression, defence, non-lethal) |
| 2 — preserve + reconcile the wound ladder; damage, healing, near-death, drones/vehicles, embodied cyber/PSI | §*Wounds: mapping an attack into the recorded ladder*, §*Healing and near-death*, §*Drones, vehicles and other machines*, §*Defence* |
| 3 — simple + advanced on one core; adversary examples; mathematical tests | §*Simple and advanced modes*, §*Worked example*; `ModeParityTests` (exhaustive) |
| 4 — independent CC-compatible wording, no proprietary chassis | no proprietary system named; no alternative dice; guard asserts both |
| 5 — cross-links, tests, PR comment | cross-links; `tests/test_issue219_physical_combat.py`; the PR |

## What was deliberately not done

- **No per-item statistics.** Weapons/armor/vehicles are function and damage type only; per-item
  ratings stay reserved (`AGENTS.md` §4, #228). The guard asserts the chapter says so.
- **No second arithmetic** — no damage roll, no hit-point track, no dice pool, no alternative die.
- **No cybernetic or PSI subsystem** — #221/#223/#224 consume this.
- **No edit to §51**, and no calibration of any PROVISIONAL number.

## Verification

- Full suite green (see PR); `ruff` clean.
- `tests/test_issue219_physical_combat.py` — 37 tests, sabotage-proven (mutate → guard fails →
  restore byte-identical).

## Authorisation note

`AGENTS.md` §4 reserves "combat resolution; damage, health, wounds, armor, or initiative". **Issue
#219 is the author explicitly opening that area** and prescribing its scope; the reservations that
remain (per-item equipment statistics, cybernetic hardware, PSI powers, the astral procedure) are
respected above and asserted by the guard.
