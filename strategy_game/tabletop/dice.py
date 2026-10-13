"""Dice machinery: notation, an injectable seeded RNG, a per-die breakdown and a replayable log.

Issue #347 asks for "dice result breakdown, modifiers, advantage/opposed checks only if explicitly
approved; never silently decide the canonical core resolution system". This module is therefore the
**machinery and nothing else**:

* no success/failure threshold, no difficulty, no target number;
* no advantage/disadvantage, no opposed resolution, no exploding dice, no "keep highest";
* no modifier cap, and no opinion about which die the game uses.

A caller who wants to compare a total to a number writes that comparison itself. :attr:`RollResult.total`
is an integer, not a judgement: this module never decides what a result *means*.

Two properties matter for a game that must be replayable and auditable:

* **The RNG is injectable and seeded.** :func:`roll` accepts a ``random.Random`` or a seed, so a test
  and a replay can reproduce a roll exactly.
* **The log is self-contained.** :class:`RollLog` stores the individual die faces as rolled, so
  :meth:`RollLog.replay` reconstructs every result from the record without re-running the RNG at all.
  Replay therefore does not depend on the stability of any particular random implementation.

Serialization is plain JSON: :meth:`RollResult.to_dict` carries the faces, ``+1`` is explicit, and
``sort_keys=True`` makes output byte-stable.

Reserved by the rule-authoring gates (``strategy_game/docs/RULE_SYSTEM_RESEARCH.md``) and by
``AGENTS.md`` §4: the resolution procedure, the canonical die, difficulties and thresholds.
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Any


class DiceNotationError(ValueError):
    """Raised for text that is not a supported dice notation."""


#: Supported notation: an optional count, ``d``, the sides, and an optional signed modifier.
#: ``d6``, ``2d6``, ``3d8+1``, ``1d20-2``. Deliberately no keep/reroll/explode syntax: those are
#: resolution rules, and which of them the game uses is not this module's decision.
_NOTATION = re.compile(r"^\s*(?:(?P<count>\d+)\s*)?[dD]\s*(?P<sides>\d+)\s*(?P<modifier>[+-]\s*\d+)?\s*$")


@dataclass(frozen=True)
class DicePool:
    """A pool of identical dice plus a flat modifier. A notation, not a rule.

    ``modifier`` is a flat integer added to the sum. Nothing here bounds it: a cap on modifiers is a
    resolution rule, and one already exists elsewhere in the design rather than in this container.
    """

    count: int = 1
    sides: int = 6
    modifier: int = 0

    def __post_init__(self) -> None:
        if self.count < 1:
            raise DiceNotationError(f"a pool needs at least one die, got count={self.count}")
        if self.sides < 2:
            raise DiceNotationError(f"a die needs at least two sides, got sides={self.sides}")

    @property
    def notation(self) -> str:
        """Canonical text form, round-trippable through :func:`parse_notation`."""
        base = f"{self.count}d{self.sides}"
        if self.modifier:
            base += f"{self.modifier:+d}"
        return base

    @property
    def min_total(self) -> int:
        """Lowest possible sum. Arithmetic, not a difficulty."""
        return self.count * 1 + self.modifier

    @property
    def max_total(self) -> int:
        """Highest possible sum. Arithmetic, not a target number."""
        return self.count * self.sides + self.modifier

    def to_dict(self) -> dict[str, Any]:
        return {"count": self.count, "sides": self.sides, "modifier": self.modifier}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DicePool:
        return cls(
            count=int(data.get("count", 1)),
            sides=int(data.get("sides", 6)),
            modifier=int(data.get("modifier", 0)),
        )


def parse_notation(text: str) -> DicePool:
    """Parse ``d6`` / ``2d6`` / ``3d8+1`` / ``1d20-2`` into a :class:`DicePool`.

    Raises :class:`DiceNotationError` for anything else, including the resolution syntax this project
    has not approved (keep-highest, reroll, exploding). Failing loudly is the point: silently reading
    ``4d6kh3`` as ``4d6`` would let an unapproved rule enter through a notation string.
    """
    match = _NOTATION.match(str(text))
    if match is None:
        raise DiceNotationError(
            f"{text!r} is not a supported dice notation; expected e.g. 'd6', '2d6', '3d8+1'. "
            "Keep/reroll/explode syntax is a resolution rule and is not parsed here."
        )
    count = int(match.group("count") or 1)
    sides = int(match.group("sides"))
    raw_modifier = match.group("modifier")
    modifier = int(raw_modifier.replace(" ", "")) if raw_modifier else 0
    return DicePool(count=count, sides=sides, modifier=modifier)


@dataclass(frozen=True)
class RollResult:
    """One recorded roll: the pool, the individual faces, the modifier and the sum.

    The faces are stored, not just the total, because that is what makes the record auditable and the
    log replayable without the RNG.
    """

    pool: DicePool
    dice: tuple[int, ...] = ()
    #: The seed used, when the caller supplied one. Recorded for provenance; replay uses :attr:`dice`.
    seed: int | None = None
    #: Optional caller-supplied label (which check, which scene). Never interpreted here.
    label: str = ""

    def __post_init__(self) -> None:
        if len(self.dice) != self.pool.count:
            raise DiceNotationError(
                f"pool {self.pool.notation} needs {self.pool.count} face(s), got {len(self.dice)}"
            )
        for face in self.dice:
            if not 1 <= face <= self.pool.sides:
                raise DiceNotationError(f"face {face} is outside 1..{self.pool.sides}")

    @property
    def modifier(self) -> int:
        return self.pool.modifier

    @property
    def total(self) -> int:
        """The sum of the faces plus the modifier. The caller decides what to do with it."""
        return sum(self.dice) + self.pool.modifier

    @property
    def breakdown(self) -> str:
        """Readable per-die breakdown, for the visible dice log the issue asks the UI to show."""
        faces = ", ".join(str(face) for face in self.dice)
        if self.pool.modifier:
            return f"{self.pool.notation} -> [{faces}] {self.pool.modifier:+d} = {self.total}"
        return f"{self.pool.notation} -> [{faces}] = {self.total}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "notation": self.pool.notation,
            "pool": self.pool.to_dict(),
            "dice": list(self.dice),
            "modifier": self.pool.modifier,
            "total": self.total,
            "seed": self.seed,
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RollResult:
        pool = DicePool.from_dict(data.get("pool") or {"count": 1, "sides": 6})
        return cls(
            pool=pool,
            dice=tuple(int(face) for face in (data.get("dice") or ())),
            seed=None if data.get("seed") is None else int(data["seed"]),
            label=str(data.get("label", "")),
        )


def roll(pool: DicePool, rng: random.Random | None = None, *, seed: int | None = None,
         label: str = "") -> RollResult:
    """Roll ``pool`` and record every face.

    The RNG is **injectable**: pass ``rng=`` to share one stream, or ``seed=`` for a reproducible
    single roll. Passing neither uses a fresh, unseeded :class:`random.Random`, which is what a live
    game wants — and the returned :class:`RollResult` still carries its faces, so even an unseeded roll
    is fully auditable afterwards.
    """
    if rng is None:
        rng = random.Random(seed)
    faces = tuple(rng.randint(1, pool.sides) for _ in range(pool.count))
    return RollResult(pool=pool, dice=faces, seed=seed, label=label)


@dataclass
class RollLog:
    """Append-only roll history. The dice audit trail the issue asks for."""

    entries: list[RollResult] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.entries)

    def record(self, result: RollResult) -> RollResult:
        """Append a roll and return it, so ``log.record(roll(pool))`` reads in one line."""
        self.entries.append(result)
        return result

    def replay(self) -> tuple[RollResult, ...]:
        """Rebuild every result from the recorded faces, without touching the RNG.

        This is the proof that the log is self-contained: it re-derives each total from the stored
        faces, so replay is exact even if the random implementation changes between versions.
        """
        return tuple(
            RollResult(
                pool=entry.pool,
                dice=entry.dice,
                seed=entry.seed,
                label=entry.label,
            )
            for entry in self.entries
        )

    @property
    def totals(self) -> tuple[int, ...]:
        return tuple(entry.total for entry in self.entries)

    def to_dict(self) -> dict[str, Any]:
        return {"entries": [entry.to_dict() for entry in self.entries]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RollLog:
        return cls(entries=[RollResult.from_dict(item) for item in (data.get("entries") or [])])
