"""Lethality lab for issue #571 — measure how deadly each chassis is, do not assert it.

Issue #571 asks for the combat/injury/trauma comparison to be **measured** rather than
argued: "the probability that a single exchange removes a character, per system, at
comparable competence". This module is that measurement. It decides nothing and approves
nothing; every constant stays PROVISIONAL and author-owned (see `AGENTS.md` §4).

Three models are enumerated, each from *published text*, never from memory:

**A — layer A, the legacy NoöPunk RPG.** One attack is one `STAT + Skill + 1d10` check
against a Difficulty Value (`src/rules/core.py`, `data/rules/core.json`). The margin of
success selects exactly one rung of the §51 ladder — Scratched / Wounded / Critical / Down
— and armour shifts that rung one step *up*, never past Scratched
(`src/rules/physical_combat.py`, `rulebook/3_PHYSICAL.md`). There is no hit-point pool, so
the state is not cumulative.

**B — layer B, the crossover game.** `4dF + skill` against the Fate ladder, four outcome
bands (`strategy_game/rpg/fate.py`). Its harm enters as stress and consequences, whose
depth is authored in `strategy_game/RULEBOOK.md`, not here — so this lab reports layer B's
*outcome* distribution only and makes no damage claim about it.

**C — CWN as published.** Attack: `1d20 + base attack bonus + attribute modifier + combat
skill level` vs the target's Melee or Ranged Armor Class
(https://cwn.quadrifons.com/rules-of-the-game/combat/attacks-in-combat/). Damage: weapon
die + relevant attribute modifier, reduced by Damage Soak
(https://cwn.quadrifons.com/gear-vehicles-cyberware/weapons/weapon-stats-and-definitions/).
On a lethal hit a Trauma Die is rolled against the victim's Trauma Target (usually 6); a
Traumatic Hit multiplies the hit's total damage by the weapon's Trauma Rating
(https://cwn.quadrifons.com/rules-of-the-game/combat/damage-trauma-shock/). A character
falls at zero hit points; a Mortally Injured PC dies at the end of the sixth round unless
stabilised (https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/mortal-injury-stabilization/).

Everything is **exact enumeration over `fractions.Fraction`**, not sampling: the tool is
deterministic by construction, so a reported number is a property of the published rules
rather than of a seed.

Recorded assumptions, all explicit and all overridable from the CLI:

* layer A simple mode defaults to the *engaged/near* band (DV 13, "Everyday") from
  `rulebook/3_PHYSICAL.md` §Attacking; advanced mode opposes `REF + Fray + 1d10`.
* CWN's soak is applied **after** the Trauma multiplier, because the SRD computes the
  hit's total damage first and says soak subtracts "incoming weapon damage". Pass
  `--soak-before-trauma` for the other reading; both are reported in the record.
* CWN hit points are a flat input (`--hp`), because CWN rolls 1d6 + CON per level and this
  lab compares *shapes*, not one character build.

Usage::

    python3 tools/issue571_lethality_lab.py
    python3 tools/issue571_lethality_lab.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Mapping

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.rules import physical_combat  # noqa: E402  (path set above)
from src.rules import core as layer_a_core  # noqa: E402

#: The rungs that remove an actor from a fight, per `rulebook/3_PHYSICAL.md`:
#: Critical is "out of the fight without immediate help", Down is "dying or dead".
REMOVING_RUNGS: tuple[str, ...] = ("Critical", "Down")

LADDER = physical_combat.LADDER


# --------------------------------------------------------------------------- #
# Layer A — the legacy NoöPunk ladder
# --------------------------------------------------------------------------- #

def layer_a_distribution(
    attack_bonus: int,
    target_number: int,
    *,
    armor_steps_applied: int = 0,
    dice_sides: int | None = None,
) -> dict[str, Fraction]:
    """Exact distribution over the four §51 rungs for one simple-mode attack.

    `attack_bonus` is `STAT + Skill`; the die comes from `data/rules/core.json` so the lab
    cannot drift from the canonical kernel.
    """
    sides = dice_sides or layer_a_core.CHECK_DICE_SIDES
    counts: Counter[str] = Counter()
    for roll in range(1, sides + 1):
        rung = physical_combat.wound_state(
            attack_bonus + roll,
            target_number,
            armor_steps_applied=armor_steps_applied,
        )
        counts[rung] += 1
    return _normalize(counts)


def layer_a_opposed_distribution(
    attack_bonus: int,
    defender_ref: int,
    defender_fray: int,
    *,
    armor_steps_applied: int = 0,
    dice_sides: int | None = None,
) -> dict[str, Fraction]:
    """Advanced mode: the target number *is* the defender's own `REF + Fray + 1d10`."""
    sides = dice_sides or layer_a_core.CHECK_DICE_SIDES
    counts: Counter[str] = Counter()
    for attacker_roll in range(1, sides + 1):
        for defender_roll in range(1, sides + 1):
            target = physical_combat.opposed_target_number(
                defender_ref, defender_fray, defender_roll
            )
            rung = physical_combat.wound_state(
                attack_bonus + attacker_roll,
                target,
                armor_steps_applied=armor_steps_applied,
            )
            counts[rung] += 1
    return _normalize(counts)


def layer_a_removal_probability(distribution: Mapping[str, Fraction]) -> Fraction:
    """Probability that one attack removes the target from the fight."""
    return sum((p for rung, p in distribution.items() if rung in REMOVING_RUNGS), Fraction(0))


def layer_a_attacks_to_removal(distribution: Mapping[str, Fraction]) -> Fraction | None:
    """Expected attacks before one removes the target, or None when it cannot happen.

    Layer A's ladder is a state, not a counter: a non-removing attack leaves the target
    exactly as it was, so successive attacks are independent and the expectation is the
    geometric mean `1/p`.
    """
    p = layer_a_removal_probability(distribution)
    return None if p == 0 else 1 / p


# --------------------------------------------------------------------------- #
# Layer B — the crossover's outcome shape only (no damage claim)
# --------------------------------------------------------------------------- #

def layer_b_outcome_distribution(skill_rating: int, opposition: int) -> dict[str, Fraction]:
    """Exact distribution over Fate's four outcomes for `4dF + skill` vs opposition."""
    dice: Counter[int] = Counter()
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            for c in (-1, 0, 1):
                for d in (-1, 0, 1):
                    dice[a + b + c + d] += 1
    counts: Counter[str] = Counter()
    for total, n in dice.items():
        shift = skill_rating + total - opposition
        if shift >= 3:
            band = "success with style"
        elif shift >= 1:
            band = "success"
        elif shift == 0:
            band = "tie (succeed at a minor cost)"
        else:
            band = "failure"
        counts[band] += n
    return _normalize(counts)


# --------------------------------------------------------------------------- #
# CWN — hit points, Damage Soak and the Trauma Die
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class CwnWeapon:
    """One line of the CWN firearm table, in the SRD's own terms."""

    name: str
    damage_dice: int
    damage_sides: int
    damage_plus: int = 0
    trauma_die: int = 8
    trauma_rating: int = 3


@dataclass(frozen=True)
class CwnTarget:
    """The three numbers CWN actually consults: Armor Class, Soak and Trauma Target."""

    label: str
    ranged_ac: int
    soak: int
    trauma_target: int = 6


#: Firearm and armour lines transcribed from the CWN SRD (accessed 2026-10-25).
CWN_WEAPONS: tuple[CwnWeapon, ...] = (
    CwnWeapon("Heavy Pistol", 1, 8, trauma_die=6, trauma_rating=3),
    CwnWeapon("Rifle", 1, 10, damage_plus=2, trauma_die=8, trauma_rating=3),
    CwnWeapon("Shotgun", 3, 4, trauma_die=10, trauma_rating=3),
)

CWN_TARGETS: tuple[CwnTarget, ...] = (
    CwnTarget("Ordinary Clothing (AC 10, Soak 0)", ranged_ac=10, soak=0),
    CwnTarget("Armored Clothing (AC 16, Soak 5, TT +1)", ranged_ac=16, soak=5, trauma_target=7),
    CwnTarget("Light Armored Suit (AC 16, Soak 5, TT +2)", ranged_ac=16, soak=5, trauma_target=8),
)


def cwn_hit_probability(attack_bonus: int, ranged_ac: int) -> Fraction:
    return Fraction(sum(1 for roll in range(1, 21) if roll + attack_bonus >= ranged_ac), 20)


def cwn_damage_distribution(
    weapon: CwnWeapon,
    target: CwnTarget,
    *,
    attribute_modifier: int = 1,
    soak_before_trauma: bool = False,
) -> dict[int, Fraction]:
    """Exact damage-per-hit distribution for one weapon against one target.

    Keys are whole points of damage actually taken; the value is the probability *given a
    hit*, so it sums to 1.
    """
    counts: Counter[int] = Counter()
    for roll_total, n in _dice_sums(weapon.damage_dice, weapon.damage_sides).items():
        base = roll_total + weapon.damage_plus + attribute_modifier
        if soak_before_trauma:
            base = max(0, base - target.soak)
        for trauma_roll in range(1, weapon.trauma_die + 1):
            damage = base * weapon.trauma_rating if trauma_roll >= target.trauma_target else base
            if not soak_before_trauma:
                damage = max(0, damage - target.soak)
            counts[damage] += n
    return _normalize(counts)


def cwn_traumatic_hit_probability(weapon: CwnWeapon, target: CwnTarget) -> Fraction:
    return Fraction(max(0, weapon.trauma_die - target.trauma_target + 1), weapon.trauma_die)


def cwn_down_in_one_hit_probability(
    weapon: CwnWeapon,
    target: CwnTarget,
    *,
    attack_bonus: int,
    hp: int,
    attribute_modifier: int = 1,
    soak_before_trauma: bool = False,
) -> Fraction:
    """P(one attack takes the target from full hit points to zero)."""
    hit = cwn_hit_probability(attack_bonus, target.ranged_ac)
    damage = cwn_damage_distribution(
        weapon, target,
        attribute_modifier=attribute_modifier,
        soak_before_trauma=soak_before_trauma,
    )
    lethal = sum((p for dmg, p in damage.items() if dmg >= hp), Fraction(0))
    return hit * lethal


def cwn_expected_damage_per_attack(
    weapon: CwnWeapon,
    target: CwnTarget,
    *,
    attack_bonus: int,
    attribute_modifier: int = 1,
    soak_before_trauma: bool = False,
) -> Fraction:
    """Expected damage per *attack* (hits and misses), in hit points."""
    hit = cwn_hit_probability(attack_bonus, target.ranged_ac)
    damage = cwn_damage_distribution(
        weapon, target,
        attribute_modifier=attribute_modifier,
        soak_before_trauma=soak_before_trauma,
    )
    return hit * sum((Fraction(dmg) * p for dmg, p in damage.items()), Fraction(0))


def cwn_expected_attacks_to_down(
    weapon: CwnWeapon,
    target: CwnTarget,
    *,
    attack_bonus: int,
    hp: int,
    attribute_modifier: int = 1,
    soak_before_trauma: bool = False,
) -> Fraction | None:
    """Exact expectation over the hit-point states, by backward induction.

    `E[h] = 1 + sum over non-removing damage d of p(d) * E[h - d]`, with `E[0] = 0`.
    Returns None if the target is unkillable (every hit is soaked to zero).
    """
    per_hit = cwn_damage_distribution(
        weapon, target,
        attribute_modifier=attribute_modifier,
        soak_before_trauma=soak_before_trauma,
    )
    hit = cwn_hit_probability(attack_bonus, target.ranged_ac)
    miss = 1 - hit
    expectation: list[Fraction] = [Fraction(0)]
    for level in range(1, hp + 1):
        # An attack that misses, or is soaked to nothing, leaves the state unchanged but
        # still consumes the attack. Every other non-removing hit advances the state.
        no_progress = miss + hit * per_hit.get(0, Fraction(0))
        denominator = 1 - no_progress
        if denominator <= 0:
            return None  # every attack either misses or is fully soaked: unkillable
        subtotal = Fraction(0)
        for damage, p in per_hit.items():
            if damage == 0:
                continue  # unchanged state, already in `no_progress`
            if damage >= level:
                continue  # this attack removes the target; contributes 0 further attacks
            subtotal += hit * p * expectation[level - damage]
        expectation.append((1 + subtotal) / denominator)
    return expectation[hp]


# --------------------------------------------------------------------------- #
# The hybrid the matrix proposes — Trauma on top of the ladder
# --------------------------------------------------------------------------- #

def layer_a_with_trauma(
    attack_bonus: int,
    target_number: int,
    *,
    trauma_die: int = 8,
    trauma_target: int = 6,
    armor_steps_applied: int = 0,
    dice_sides: int | None = None,
) -> dict[str, Fraction]:
    """Layer A's rung selection, then CWN's Trauma Die escalating a non-glancing hit.

    This is the "import Trauma as injury adjudication" proposal in
    `ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` row 7, expressed executably so its effect can be
    read off rather than assumed. Escalation is two rungs, mirroring a `x3` multiplier's
    effect on a four-rung ladder.
    """
    sides = dice_sides or layer_a_core.CHECK_DICE_SIDES
    counts: Counter[str] = Counter()
    for roll in range(1, sides + 1):
        rung = physical_combat.wound_state(
            attack_bonus + roll,
            target_number,
            armor_steps_applied=armor_steps_applied,
        )
        index = LADDER.index(rung)
        for trauma_roll in range(1, trauma_die + 1):
            escalated = index
            if trauma_roll >= trauma_target and index > 0:
                escalated = min(len(LADDER) - 1, index + 2)
            counts[LADDER[escalated]] += 1
    return _normalize(counts)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _dice_sums(count: int, sides: int) -> Counter[int]:
    """Exact distribution of `count`d`sides`, by enumeration."""
    sums: Counter[int] = Counter({0: 1})
    for _ in range(count):
        nxt: Counter[int] = Counter()
        for total, n in sums.items():
            for face in range(1, sides + 1):
                nxt[total + face] += n
        sums = nxt
    return sums


def _normalize(counts: Mapping[object, int]) -> dict:
    total = sum(counts.values())
    return {key: Fraction(n, total) for key, n in sorted(counts.items())}


def _pct(value: Fraction) -> str:
    return f"{float(value) * 100:5.1f}%"


def _attacks(value: Fraction | None) -> str:
    return "cannot" if value is None else f"{float(value):5.2f}"


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def build_report(
    *,
    layer_a_bonus: int = 10,
    cwn_attack_bonus: int = 3,
    cwn_hp: int = 5,
    cwn_attribute_modifier: int = 1,
    soak_before_trauma: bool = False,
) -> dict:
    """Everything the record in `docs/design/ISSUE_571_COMBAT_INJURY_TRAUMA.md` cites."""
    ladder_rows = []
    for target_number in physical_combat.DIFFICULTY_LADDER:
        dist = layer_a_distribution(layer_a_bonus, target_number)
        ladder_rows.append({
            "mode": "simple",
            "target_number": target_number,
            "distribution": {rung: float(p) for rung, p in dist.items()},
            "removal": float(layer_a_removal_probability(dist)),
            "down": float(dist.get("Down", Fraction(0))),
            "attacks_to_removal": _json_fraction(layer_a_attacks_to_removal(dist)),
        })

    opposed = layer_a_opposed_distribution(layer_a_bonus, defender_ref=5, defender_fray=5)
    opposed_rows = [{
        "mode": "advanced (opposed)",
        "defender": "REF 5 + Fray 5",
        "distribution": {rung: float(p) for rung, p in opposed.items()},
        "removal": float(layer_a_removal_probability(opposed)),
        "down": float(opposed.get("Down", Fraction(0))),
        "attacks_to_removal": _json_fraction(layer_a_attacks_to_removal(opposed)),
    }]

    cwn_rows = []
    for weapon in CWN_WEAPONS:
        for target in CWN_TARGETS:
            cwn_rows.append({
                "weapon": weapon.name,
                "target": target.label,
                "hit": float(cwn_hit_probability(cwn_attack_bonus, target.ranged_ac)),
                "traumatic": float(cwn_traumatic_hit_probability(weapon, target)),
                "expected_damage_per_attack": float(cwn_expected_damage_per_attack(
                    weapon, target,
                    attack_bonus=cwn_attack_bonus,
                    attribute_modifier=cwn_attribute_modifier,
                    soak_before_trauma=soak_before_trauma,
                )),
                "down_in_one_hit": float(cwn_down_in_one_hit_probability(
                    weapon, target,
                    attack_bonus=cwn_attack_bonus,
                    hp=cwn_hp,
                    attribute_modifier=cwn_attribute_modifier,
                    soak_before_trauma=soak_before_trauma,
                )),
                "attacks_to_down": _json_fraction(cwn_expected_attacks_to_down(
                    weapon, target,
                    attack_bonus=cwn_attack_bonus,
                    hp=cwn_hp,
                    attribute_modifier=cwn_attribute_modifier,
                    soak_before_trauma=soak_before_trauma,
                )),
            })

    hybrid_rows = []
    for target_number in (13, 15, 17):
        plain = layer_a_distribution(layer_a_bonus, target_number)
        with_trauma = layer_a_with_trauma(layer_a_bonus, target_number)
        hybrid_rows.append({
            "target_number": target_number,
            "plain_down": float(plain.get("Down", Fraction(0))),
            "trauma_down": float(with_trauma.get("Down", Fraction(0))),
            "plain_removal": float(layer_a_removal_probability(plain)),
            "trauma_removal": float(layer_a_removal_probability(with_trauma)),
        })

    layer_b = layer_b_outcome_distribution(skill_rating=3, opposition=2)

    return {
        "format": "noopunk.issue571.lethality_lab",
        "version": 1,
        "issue": 571,
        "is_canonical": False,
        "method": "exact enumeration over fractions.Fraction; no sampling",
        "inputs": {
            "layer_a_attack_bonus": layer_a_bonus,
            "cwn_attack_bonus": cwn_attack_bonus,
            "cwn_hp": cwn_hp,
            "cwn_attribute_modifier": cwn_attribute_modifier,
            "soak_before_trauma": soak_before_trauma,
        },
        "layer_a": {
            "removing_rungs": list(REMOVING_RUNGS),
            "simple": ladder_rows,
            "advanced": opposed_rows,
        },
        "layer_b": {
            "note": "outcome shape only; harm depth is authored in strategy_game/RULEBOOK.md",
            "skills": 3,
            "opposition": 2,
            "distribution": {band: float(p) for band, p in layer_b.items()},
        },
        "cwn": {
            "weapons": [asdict(w) for w in CWN_WEAPONS],
            "targets": [asdict(t) for t in CWN_TARGETS],
            "rows": cwn_rows,
        },
        "hybrid": hybrid_rows,
    }


def _json_fraction(value: Fraction | None) -> float | None:
    return None if value is None else float(value)


def format_report(report: Mapping) -> str:
    lines: list[str] = []
    inputs = report["inputs"]
    lines.append(
        "Lethality lab — issue #571 (exact enumeration; not canon; PROVISIONAL)\n"
        f"layer A attack bonus {inputs['layer_a_attack_bonus']} (STAT 5 + Skill 5), "
        f"CWN attack bonus {inputs['cwn_attack_bonus']} (L1 BAB +1, attr +1, skill 1), "
        f"CWN hit points {inputs['cwn_hp']}\n"
    )

    lines.append("A. Layer A, simple mode — where the ladder puts one attack")
    header = f"{'DV':>4}  {'Scratched':>9} {'Wounded':>8} {'Critical':>9} {'Down':>6}  {'removal':>8} {'attacks':>8}"
    lines.append(header)
    for row in report["layer_a"]["simple"]:
        d = row["distribution"]
        attacks = "cannot" if row["attacks_to_removal"] is None else format(row["attacks_to_removal"], "5.2f")
        scratched = _pct(Fraction(d.get("Scratched", 0)).limit_denominator(10**6))
        wounded = _pct(Fraction(d.get("Wounded", 0)).limit_denominator(10**6))
        critical = _pct(Fraction(d.get("Critical", 0)).limit_denominator(10**6))
        down = _pct(Fraction(d.get("Down", 0)).limit_denominator(10**6))
        lines.append(
            f"{row['target_number']:>4}  {scratched:>9} {wounded:>8} {critical:>9} {down:>6}"
            f"  {row['removal'] * 100:7.1f}% {attacks:>8}"
        )

    for row in report["layer_a"]["advanced"]:
        d = row["distribution"]
        attacks = "cannot" if row["attacks_to_removal"] is None else format(row["attacks_to_removal"], ".2f")
        lines.append(
            f"\n   advanced mode vs {row['defender']}: "
            + ", ".join(f"{rung} {p * 100:.1f}%" for rung, p in d.items())
            + f" -> removal {row['removal'] * 100:.1f}%, attacks {attacks}"
        )

    lines.append("\nB. Layer B (crossover) — outcome shape only, 4dF + 3 vs 2")
    for band, p in report["layer_b"]["distribution"].items():
        lines.append(f"   {band:<32} {p * 100:5.1f}%")

    lines.append("\nC. CWN as published — hit points, Damage Soak and the Trauma Die")
    lines.append(
        f"{'weapon':<13} {'target':<42} {'hit':>6} {'trauma':>7} {'dmg/atk':>8} {'down 1':>7} {'attacks':>8}"
    )
    for row in report["cwn"]["rows"]:
        attacks = "cannot" if row["attacks_to_down"] is None else format(row["attacks_to_down"], "6.2f")
        lines.append(
            f"{row['weapon']:<13} {row['target']:<42} {row['hit'] * 100:5.1f}%"
            f" {row['traumatic'] * 100:6.1f}% {row['expected_damage_per_attack']:8.2f}"
            f" {row['down_in_one_hit'] * 100:6.1f}% {attacks:>8}"
        )

    lines.append("\nD. The proposed import — CWN Trauma die on top of the ladder (x3 read as +2 rungs)")
    lines.append(f"{'DV':>4} {'plain Down':>11} {'+Trauma Down':>13} {'plain removal':>14} {'+Trauma removal':>16}")
    for row in report["hybrid"]:
        lines.append(
            f"{row['target_number']:>4} {row['plain_down'] * 100:10.1f}% {row['trauma_down'] * 100:12.1f}%"
            f" {row['plain_removal'] * 100:13.1f}% {row['trauma_removal'] * 100:15.1f}%"
        )
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    parser.add_argument("--layer-a-bonus", type=int, default=10, help="STAT + Skill for layer A")
    parser.add_argument("--cwn-attack-bonus", type=int, default=3, help="CWN attack bonus")
    parser.add_argument("--cwn-hp", type=int, default=5, help="CWN hit points to remove")
    parser.add_argument("--cwn-attribute-modifier", type=int, default=1, help="CWN attribute modifier")
    parser.add_argument("--soak-before-trauma", action="store_true", help="subtract soak before the Trauma multiplier")
    args = parser.parse_args(list(argv) if argv is not None else None)

    report = build_report(
        layer_a_bonus=args.layer_a_bonus,
        cwn_attack_bonus=args.cwn_attack_bonus,
        cwn_hp=args.cwn_hp,
        cwn_attribute_modifier=args.cwn_attribute_modifier,
        soak_before_trauma=args.soak_before_trauma,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
