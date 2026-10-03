"""Deterministic interaction mechanics for the EP2-homebrew prototype.

This module deliberately implements a compact playable subset rather than copying
rulebook prose. Concordia agents choose structured actions; Python resolves the
contest and mutates explicit harm state.

The opposed-test tie breaker is a prototype adapter rule: successful tests beat
failed tests, stronger result degrees beat weaker ones, then the higher successful
roll wins; an exact tie favors the defender/status quo. This is intentionally
isolated so later EP2 fidelity work or NoöPunk-native rules can replace it.
"""

from __future__ import annotations

from dataclasses import dataclass

from .core import EP2TestResult, resolve_test


_SUCCESS_RANK = {
    "failure": 0,
    "superior_failure": 0,
    "two_superior_failures": 0,
    "success": 1,
    "superior_success": 2,
    "two_superior_successes": 3,
    "critical_success": 4,
}
_FAILURE_RANK = {
    "critical_failure": -3,
    "two_superior_failures": -2,
    "superior_failure": -1,
    "failure": 0,
}


@dataclass(frozen=True, slots=True)
class EP2OpposedResult:
    attacker: EP2TestResult
    defender: EP2TestResult
    winner: str
    margin: int

    @property
    def attacker_wins(self) -> bool:
        return self.winner == "attacker"


@dataclass(slots=True)
class EP2HarmState:
    """Small persistent body/mind harm record for the first playable slice."""

    durability: int
    wound_threshold: int
    lucidity: int
    trauma_threshold: int
    damage: int = 0
    wounds: int = 0
    stress: int = 0
    traumas: int = 0

    def __post_init__(self) -> None:
        for name in ("durability", "wound_threshold", "lucidity", "trauma_threshold"):
            if int(getattr(self, name)) <= 0:
                raise ValueError(f"{name} must be positive.")
        for name in ("damage", "wounds", "stress", "traumas"):
            if int(getattr(self, name)) < 0:
                raise ValueError(f"{name} must be non-negative.")

    @property
    def incapacitated(self) -> bool:
        return self.damage >= self.durability

    @property
    def overwhelmed(self) -> bool:
        return self.stress >= self.lucidity

    def apply_damage(self, amount: int) -> int:
        amount = int(amount)
        if amount < 0:
            raise ValueError("Damage must be non-negative.")
        before = self.damage // self.wound_threshold
        self.damage += amount
        after = self.damage // self.wound_threshold
        gained = max(0, after - before)
        self.wounds += gained
        return gained

    def apply_stress(self, amount: int) -> int:
        amount = int(amount)
        if amount < 0:
            raise ValueError("Stress must be non-negative.")
        before = self.stress // self.trauma_threshold
        self.stress += amount
        after = self.stress // self.trauma_threshold
        gained = max(0, after - before)
        self.traumas += gained
        return gained


@dataclass(frozen=True, slots=True)
class EP2InteractionResult:
    kind: str
    opposed: EP2OpposedResult
    effect_applied: bool
    effect_amount: int = 0
    threshold_events: int = 0


def _result_rank(result: EP2TestResult) -> int:
    if result.success:
        return _SUCCESS_RANK[result.degree]
    return _FAILURE_RANK.get(result.degree, 0)


def resolve_opposed_test(
    *,
    attacker_target: int,
    defender_target: int,
    attacker_modifier: int = 0,
    defender_modifier: int = 0,
    attacker_roll: int | None = None,
    defender_roll: int | None = None,
) -> EP2OpposedResult:
    """Resolve a compact two-sided contest with deterministic tie handling."""
    attacker = resolve_test(
        target=attacker_target, modifier=attacker_modifier, roll=attacker_roll
    )
    defender = resolve_test(
        target=defender_target, modifier=defender_modifier, roll=defender_roll
    )

    if attacker.success != defender.success:
        winner = "attacker" if attacker.success else "defender"
    else:
        attacker_rank = _result_rank(attacker)
        defender_rank = _result_rank(defender)
        if attacker_rank != defender_rank:
            winner = "attacker" if attacker_rank > defender_rank else "defender"
        elif attacker.success and attacker.roll != defender.roll:
            winner = "attacker" if attacker.roll > defender.roll else "defender"
        else:
            winner = "defender"

    return EP2OpposedResult(
        attacker=attacker,
        defender=defender,
        winner=winner,
        margin=abs(attacker.roll - defender.roll),
    )


def resolve_combat_attack(
    *,
    attacker_target: int,
    defender_target: int,
    damage: int,
    defender_harm: EP2HarmState,
    attacker_roll: int | None = None,
    defender_roll: int | None = None,
    attacker_modifier: int = 0,
    defender_modifier: int = 0,
) -> EP2InteractionResult:
    """Resolve an attack contest and apply caller-supplied damage on a hit."""
    opposed = resolve_opposed_test(
        attacker_target=attacker_target,
        defender_target=defender_target,
        attacker_modifier=attacker_modifier,
        defender_modifier=defender_modifier,
        attacker_roll=attacker_roll,
        defender_roll=defender_roll,
    )
    amount = int(damage)
    if amount < 0:
        raise ValueError("Damage must be non-negative.")
    threshold_events = defender_harm.apply_damage(amount) if opposed.attacker_wins else 0
    return EP2InteractionResult(
        kind="combat",
        opposed=opposed,
        effect_applied=opposed.attacker_wins,
        effect_amount=amount if opposed.attacker_wins else 0,
        threshold_events=threshold_events,
    )


def resolve_social_action(**kwargs) -> EP2InteractionResult:
    """Resolve a social contest without inventing narrative consequences.

    ``kwargs`` forwards to :func:`resolve_opposed_test`, whose roll parameters accept
    ``None`` to mean "roll it"; a narrower ``int`` annotation here would be wrong and
    would reject a legitimate caller passing an injected-or-random roll.
    """
    opposed = resolve_opposed_test(**kwargs)
    return EP2InteractionResult(
        kind="social",
        opposed=opposed,
        effect_applied=opposed.attacker_wins,
    )


def resolve_hack_action(**kwargs) -> EP2InteractionResult:
    """Resolve an attacker-vs-system/operator mesh contest."""
    opposed = resolve_opposed_test(**kwargs)
    return EP2InteractionResult(
        kind="mesh",
        opposed=opposed,
        effect_applied=opposed.attacker_wins,
    )
