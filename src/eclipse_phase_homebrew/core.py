"""Minimal Eclipse Phase 2E-derived deterministic rules kernel.

Implements a small EP2 homebrew subset for the NoöPunk Concordia prototype:
d100 tests, 33/66 superior results, critical doubles, defaulting, modifiers,
and common Insight/Moxie/Vigor/Flex pool test effects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Mapping, Protocol


class DiceSource(Protocol):
    def randint(self, a: int, b: int) -> int: ...


class PoolKind(str, Enum):
    INSIGHT = "insight"
    MOXIE = "moxie"
    VIGOR = "vigor"
    FLEX = "flex"


class PoolSpend(str, Enum):
    NONE = "none"
    ADD_20 = "add_20"
    IGNORE_MODIFIERS = "ignore_modifiers"
    FLIP_FLOP = "flip_flop"
    UPGRADE_SUCCESS = "upgrade_success"
    DOWNGRADE_CRITICAL_FAILURE = "downgrade_critical_failure"


@dataclass(slots=True)
class EP2PoolState:
    maximum: Mapping[PoolKind, int] = field(default_factory=dict)
    current: dict[PoolKind, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        maximum = {PoolKind(k): int(v) for k, v in dict(self.maximum).items()}
        current = ({PoolKind(k): int(v) for k, v in self.current.items()}
                   if self.current else dict(maximum))
        for kind, max_value in maximum.items():
            if max_value < 0:
                raise ValueError("Pool maxima must be non-negative.")
            value = current.get(kind, max_value)
            if not 0 <= value <= max_value:
                raise ValueError(f"{kind.value} pool must be in 0..{max_value}.")
            current[kind] = value
        self.maximum = maximum
        self.current = current

    def spend(self, kind: PoolKind) -> None:
        kind = PoolKind(kind)
        if self.current.get(kind, 0) < 1:
            raise ValueError(f"No {kind.value} pool points remain.")
        self.current[kind] -= 1

    def short_recharge(self, points: int) -> int:
        remaining = max(0, int(points))
        restored = 0
        for kind in PoolKind:
            if remaining <= 0:
                break
            maximum = self.maximum.get(kind, 0)
            missing = maximum - self.current.get(kind, 0)
            add = min(missing, remaining)
            if add:
                self.current[kind] = self.current.get(kind, 0) + add
                restored += add
                remaining -= add
        return restored

    def long_recharge(self) -> None:
        self.current = dict(self.maximum)


@dataclass(frozen=True, slots=True)
class EP2Character:
    name: str
    skills: Mapping[str, int] = field(default_factory=dict)
    aptitudes: Mapping[str, int] = field(default_factory=dict)
    morph: str = ""
    durability: int | None = None
    wound_threshold: int | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Character name must not be empty.")
        for label, mapping in (("skill", self.skills), ("aptitude", self.aptitudes)):
            for key, value in mapping.items():
                if not str(key).strip():
                    raise ValueError(f"{label} names must not be empty.")
                if not 0 <= int(value) <= 100:
                    raise ValueError(f"{label} ratings must be in 0..100.")


@dataclass(frozen=True, slots=True)
class EP2TestResult:
    roll: int
    base_target: int
    modifier: int
    target: int
    success: bool
    critical: bool
    critical_success: bool
    critical_failure: bool
    superior_successes: int
    superior_failures: int
    defaulted: bool
    pool_kind: PoolKind | None
    pool_spend: PoolSpend

    @property
    def degree(self) -> str:
        if self.critical_success:
            return "critical_success"
        if self.critical_failure:
            return "critical_failure"
        if self.success and self.superior_successes:
            return "two_superior_successes" if self.superior_successes == 2 else "superior_success"
        if (not self.success) and self.superior_failures:
            return "two_superior_failures" if self.superior_failures == 2 else "superior_failure"
        return "success" if self.success else "failure"


def roll_d100(rng: DiceSource | None = None) -> int:
    source = rng if rng is not None else random
    return source.randint(0, 99)


def flip_flop(roll: int) -> int:
    if not 0 <= int(roll) <= 99:
        raise ValueError("d100 roll must be in 0..99.")
    tens, ones = divmod(int(roll), 10)
    return ones * 10 + tens


def _is_double(roll: int) -> bool:
    return roll // 10 == roll % 10


def resolve_test(*, target: int, modifier: int = 0, defaulted: bool = False,
                 roll: int | None = None, rng: DiceSource | None = None,
                 pools: EP2PoolState | None = None,
                 pool_kind: PoolKind | None = None,
                 pool_spend: PoolSpend = PoolSpend.NONE) -> EP2TestResult:
    """Resolve one EP2-style d100 test."""
    base_target = int(target)
    if not 0 <= base_target <= 100:
        raise ValueError("Base target must be in 0..100.")

    spend = PoolSpend(pool_spend)
    kind = PoolKind(pool_kind) if pool_kind is not None else None
    if spend is not PoolSpend.NONE:
        if pools is None or kind is None:
            raise ValueError("A pool spend requires both pools and pool_kind.")
        pools.spend(kind)

    net_modifier = max(-60, min(60, int(modifier)))
    if spend is PoolSpend.IGNORE_MODIFIERS:
        net_modifier = 0
    effective_target = base_target + net_modifier
    if spend is PoolSpend.ADD_20:
        effective_target += 20
    effective_target = max(0, effective_target)

    actual_roll = roll_d100(rng) if roll is None else int(roll)
    if not 0 <= actual_roll <= 99:
        raise ValueError("d100 roll must be in 0..99.")
    if spend is PoolSpend.FLIP_FLOP:
        actual_roll = flip_flop(actual_roll)

    auto_success = actual_roll == 0
    auto_failure = actual_roll == 99
    success = auto_success or (not auto_failure and actual_roll <= effective_target)
    critical = _is_double(actual_roll)
    critical_success = critical and success
    critical_failure = critical and not success

    if defaulted and critical_success:
        critical_success = False
        critical = False

    superior_successes = 0
    superior_failures = 0
    if not critical_success and not critical_failure:
        if success:
            if actual_roll >= 66:
                superior_successes = 2
            elif actual_roll >= 33:
                superior_successes = 1
        else:
            if actual_roll <= 33:
                superior_failures = 2
            elif actual_roll <= 66:
                superior_failures = 1

    if spend is PoolSpend.UPGRADE_SUCCESS and success and not critical_success:
        superior_successes = min(2, superior_successes + 1)
    if spend is PoolSpend.DOWNGRADE_CRITICAL_FAILURE and critical_failure:
        critical_failure = False
        critical = False

    return EP2TestResult(
        roll=actual_roll, base_target=base_target, modifier=net_modifier,
        target=effective_target, success=success, critical=critical,
        critical_success=critical_success, critical_failure=critical_failure,
        superior_successes=superior_successes, superior_failures=superior_failures,
        defaulted=bool(defaulted), pool_kind=kind, pool_spend=spend,
    )
