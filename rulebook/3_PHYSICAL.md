# Physical

**Status: NOÖPUNK CORE, expanding.** The Physical domain covers bodies, action, harm and
equipment. Light rules and catalog vocabulary live in `RULEBOOK.md`; this chapter is the
per-domain home for the detail.

Canonical resolution is `STAT + Skill + 1d10` against a Difficulty Value
(`RULEBOOK.md` §4.1, §4.2).

## Where things live

- **Harm** — the light wound ladder is `RULEBOOK.md` §51 (Scratched → Wounded → Critical →
  Down), with armor/cover mitigation and First Aid stabilisation. This chapter maps combat
  outcomes **into** that ladder; it does not redefine it. Numeric statistics of items remain
  undefined by design.
- **Equipment** — the top-level vocabulary is `RULEBOOK.md` §52; the full
  availability-and-function catalog is `rulebook/9_FIELD_CATALOGS.md` §2. Numeric statistics
  remain undefined by design.
- **Bodies, augmentation and identity** — the body as biology is here; what is added to it is
  `rulebook/5_CYBERNETIC.md`; what happens when identity itself is at stake is
  `rulebook/6_PSYCHIC.md`.
- **Locations** — a character occupies a larger location (a city) and a current **sublocation**
  (`RULEBOOK.md` §5.4). **Open locations** persist; **quest locations** are temporary mission
  spaces that may exist in Physical space, Cyberspace or Noöspace — and one operation may
  cross all three.
- **The shared clock** — the action economy, initiative order and reaction rule used below are
  the cross-domain contract in [`rulebook/18_CROSS_DOMAIN_STATE.md`](18_CROSS_DOMAIN_STATE.md)
  (issue #225). This chapter consumes it and must not restate it.

## Physical action

Physical action is ordinary interaction with the material world — moving, climbing, carrying,
pursuing, sneaking, attacking, restraining, escaping, first aid. When the outcome is uncertain
and consequential, resolve it with the core engine; otherwise, narrate it.

The physical Skills are **Athletics, Fray, Guns, Melee, Unarmed, Free Fall, Sneak, Pilot**,
with **Perceive** and **Survival** bridging into awareness and environment
(`RULEBOOK.md` §4.1).

## Damage types (vocabulary)

For mitigation, hazards and fiction, distinguish **ballistic**, **kinetic/impact**,
**energy/thermal**, **electrical**, **chemical/toxin**, **radiation**, and
**psychotronic / noetic** effects. Armor is described by what it resists in these terms rather
than by a single number.

---

## Physical conflict

**Status: NOÖPUNK NATIVE — issue #219.** Physical conflict uses the **same core check** as
everything else — `STAT + Skill + 1d10` — and the **same clock** as every other realm. Nothing
below introduces a second resolution system: no dice pools, no damage roll, no hit-point track.
Every number is **PROVISIONAL pending author calibration**.

### What a fight is made of

A physical conflict is a sequence of **exchanges** on the shared clock
([`18_CROSS_DOMAIN_STATE.md`](18_CROSS_DOMAIN_STATE.md)). Each combatant has **3 AP** per
exchange, acts in **descending REF** order, and may **react** at the cost of an AP held or
borrowed from the next exchange.

| Physical AP spend | Cost | Notes |
| --- | ---: | --- |
| **Engage / Disengage / Move a band** | 1 | Leaving an engagement is a Move, and provokes (below) |
| **Attack** (melee, unarmed or ranged) | 1 | One attack per AP; a failed check still spends it |
| **Aim / Brace** | 1 | The physical form of *Prepare*: one difficulty step better on the next attack |
| **Take Cover / Go Prone** | 1 | Establishes a cover state that persists until you move |
| **Fray** (active defence) | 1 | A **reaction**; see *Defence* |
| **Restrain / Stabilise / Drag** | 1 | Non-lethal and rescue actions; see *Non-lethal outcomes* |

### Bands: where everyone is standing

Positioning is banded rather than measured, so it can be played in the theatre of the mind and
rendered by a computer front-end with no hidden state.

- **Engaged** — melee reach. You can attack with Melee or Unarmed.
- **Near** — a few steps; a thrown or short-range shot; a Move.
- **Far** — across a room or street; a normal firearm range; two Moves.
- **Distant** — beyond reliable fire; requires Aim and favourable conditions.

Moving one band costs 1 AP. **Leaving an engagement provokes**: anyone still engaged with you
may spend a **reaction** AP to attack as you go. Disengaging deliberately (spending the Move
*and* declaring a fighting withdrawal) does not provoke; simply running does.

### Attacking

A physical attack is one core check. **Simple mode** resolves it against a fixed target number;
**advanced mode** resolves it as an opposed check against the defender's `REF + Fray` and adds
the tactical options below. **Both modes use the identical arithmetic and the identical effect
bands** — this is asserted by exhaustively enumerating the outcomes in
`tests/test_issue219_physical_combat.py`, not merely claimed here.

| Attack | Check |
| --- | --- |
| **Melee** | `FIT + Melee` vs target |
| **Unarmed** | `FIT + Unarmed` vs target |
| **Ranged** | `REF + Guns` vs target |
| **Thrown / improvised** | `REF + Athletics` vs target |

**Target number (PROVISIONAL).** Simple mode uses the core ladder
(`RULEBOOK.md` §4.2): a **Near** target is Everyday (13), **Far** is Difficult (15),
**Distant** is Professional (17) before aiming. Advanced mode opposes the above instead.

### Cover

Cover is a **difficulty step**, not a stored number. Partial cover is **one step** harder;
substantial cover is **two**. Cover applies to ranged attacks against you while you hold it,
and is lost when you Move. A character already in cover who takes the **Take Cover** action is
**Hidden** to attackers who have not repositioned — they must Move first or shoot blind.

### Armor

Armor is rated by the **damage types** it resists (above), and its effect is a **ladder step**,
never a subtraction. Against a damage type the armor resists, the resulting wound state is
**shifted one step up the ladder** (less severe). Armor that resists nothing mitigates nothing;
armor does not stack with itself, and cover and armor are applied in that order.

> **Armor changes which rung you land on, not how hard the blow was.** This is the same
> one-step vocabulary `RULEBOOK.md` §51 already uses for First Aid, so the two rules compose
> instead of contradicting.

### Wounds: mapping an attack into the recorded ladder

`RULEBOOK.md` §51's ladder — **Scratched → Wounded → Critical → Down** — is preserved exactly.
Combat chooses a rung by the **margin of success** of the attack:

| Margin of success | Effect band | Lands on |
| --- | --- | --- |
| 0 | glancing | **Scratched** |
| 1–4 | solid | **Wounded** |
| 5–8 | severe | **Critical** |
| 9+ | brutal | **Down** |

Then armor mitigation shifts the rung **one step up** (toward Scratched) if the armor resists
that damage type, and **never past Scratched**. Nothing else moves the ladder automatically —
consistent with §51's rule that a wound state is a fictional consequence, not an accumulating
counter.

**Healing and near-death (PROVISIONAL).** **First Aid** stabilises and moves a character one
rung up; **Medicine** treats the underlying injury. A character at **Down** is dying and needs
stabilisation within the scene or they die. A character at **Critical** is out of the fight.
Recovery time is a **scene-level consequence**, deliberately not a numeric track here.

### Suppression and morale

Automatic fire and near-misses break resolve, not bodies. A **suppressing attack** is resolved
as a normal ranged check; on success the target must make a **`PSY + Fray`** check against the
same target number or be **Pinned**: they may not Move toward the source and lose 1 AP to
hesitation. Pinned is a **status**, not a wound, and ends when the suppressive fire stops or
the character passes the check on a later exchange. Suppression never wounds by itself.

### Defence

- **Fray** is the active defence Skill. Spending a **reaction** AP lets a defender oppose an
  incoming attack with `REF + Fray`. Without the AP, the attack resolves against the passive
  target number (simple mode) — that is the entire cost of being surprised or out of AP.
- **Armor and cover are passive** and apply whether or not the character spends AP.
- **Psychic and cybernetic defence in a physical fight:** resisting hostile PSI uses
  `PSY + Psychic Defence` and defending a device uses the cybernetic procedure — both as
  **reactions on the same clock**, so a character cannot simultaneously dodge, resist a
  telepathic probe, and guard a network with 3 AP. That scarcity is deliberate.

### Non-lethal outcomes

Non-lethal force is **first-class, not a penalty mode** — the default campaign is about
investigators who must justify force.

- **Unarmed** and **Melee** attacks may be declared **subduing**: a successful check lands the
  target on the **same ladder** (Scratched/Wounded) but the state is described as *winded,
  pinned, disarmed or restrained* rather than injured. A subdued target is not dying.
- **Restraining** a resisting target is an opposed `FIT + Unarmed` (or `REF + Fray` to escape)
  and can be repeated across exchanges.
- **Down** by non-lethal means means **unconscious and stable**, not dying — a real difference
  at the table and in the after-action report.
- Less-lethal equipment is issued as capability, never as a damage statistic
  (`rulebook/9_FIELD_CATALOGS.md`).

### Drones, vehicles and other machines

A machine has no wound ladder: it has a **function ladder** — **Operational → Impaired →
Disabled → Destroyed** — chosen by the **same margin-of-success bands** and mitigated by armor
in the **same one-step** way. A machine has no Psyche check for suppression and does not bleed,
but a **Destroyed** machine is wreckage, and a **Disabled** one may be repaired or salvaged.
Occupants of a disabled vehicle take the wound band the attack earned — machines and crews are
separate ladders.

### Simple and advanced modes: one core, two dialects

**The numerical core is identical.** Both modes resolve `STAT + Skill + 1d10` against a target
number and both choose the ladder rung from the same margin-of-success table. The difference is
only *where the target number comes from* and *how many options exist*:

| | Simple mode | Advanced mode |
| --- | --- | --- |
| Target number | the core ladder by band, cover and aim | opposed `REF + Fray`, cover and aim as steps |
| Positioning | bands only | bands + engagement, fighting withdrawal, Hidden |
| Reactions | optional | the reaction economy is the tactical layer |
| Suppression | not used | full Pinned procedure |
| Machines | one ladder | function ladder + crew effects |

A character built for simple mode is **not numerically weaker** in advanced play: the same
`FIT + Melee` check, the same bands, the same ladder. Advanced mode adds decisions, not
arithmetic — which is what makes the two modes compatible at one table.

### Worked example (PROVISIONAL)

**A** (`REF 7`, `FIT 6`, `Guns 4`, `Melee 3`, `Fray 3`) is engaged with **B** (`REF 6`,
`Fray 4`, ballistic armor) in a corridor; **C** covers the far end with a rifle and is
**Behind substantial cover**.

| Exchange | Actor | AP | Action | Roll | Result |
| --- | --- | ---: | --- | --- | --- |
| 1 | A | 1 | Attack B (melee) | `FIT 6 + Melee 3 + 1d10(6) = 15` vs B's `REF 6 + Fray 4 + 1d10(3) = 13` | MoS 2 → **Wounded**, band solid |
| 1 | B | 1 | Attack A (melee) | `FIT 5 + Melee 4 + 1d10(4) = 13` vs A's `REF 7 + Fray 3 + 1d10(8) = 18` | miss; the Fray reaction cost B nothing extra |
| 1 | B | 1 | Take Cover | — | **Partial cover** established |
| 1 | C | 1 | Suppress A | `REF 6 + Guns 5 + 1d10(5) = 16` vs 13 | success — A must resist |
| 1 | A | 1 | **React** — resist suppression | `PSY 5 + Fray 3 + 1d10(2) = 10` vs 13 | **fails — Pinned**, loses next Move toward C |
| 2 | A | 1 | Attack B (melee) | `FIT 6 + Melee 3 + 1d10(7) = 16` vs B's partial cover step 15 | MoS 1 → **Wounded** again — but the ladder **does not accumulate**: B is still Wounded |
| 2 | B | 1 | Emergency withdrawal | — | deliberate disengage; A may react, chooses not to spend the AP |

Two things the example is meant to show: **armor and cover change rungs and target numbers, never
damage arithmetic**; and **the ladder is a state, not a counter** — two solid hits do not
"add up" to Critical, which is exactly what `RULEBOOK.md` §51 requires.

## What this chapter deliberately does not do

- **No item statistics.** Weapons, armor and vehicles are described by **function and damage
  type**; per-item ratings stay reserved (`AGENTS.md` §4, #228).
- **No second arithmetic.** No damage roll, no hit points, no dice pool, and no proprietary
  chassis. The core check is the whole system.
- **No cybernetic or PSI subsystem.** Hardware ratings are #221; PSI powers are #223; the
  astral procedure is #224.
- **No redefinition of §51.** The wound ladder is quoted and mapped into, not edited.
- **No calibration.** Every number above is PROVISIONAL; the author owns the final values.
