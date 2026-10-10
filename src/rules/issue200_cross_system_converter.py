"""Lossy, noncanonical cross-system conversion research for NoöPunk issue #200.

This is independently authored code for *rating labels*, not copied external
mechanics or an authorized rules migration. Converting values never changes
the active d10 resolver, skill names, or physical/psychic/cyber game state.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

Family = Literal["noopunk", "fudge", "fate", "eclipse_phase", "without_number"]
Kind = Literal["attribute", "skill", "difficulty"]

# Experimental representative *ordinal* bands; not assertions of equivalent
# game mechanics. External systems do not share a single definition of ability.
BANDS: dict[tuple[str, str], tuple[int, ...]] = {
    ("noopunk", "attribute"): tuple(range(1, 11)),
    ("noopunk", "skill"): tuple(range(1, 11)),
    ("fudge", "attribute"): tuple(range(-3, 4)),
    ("fudge", "skill"): tuple(range(-3, 4)),
    ("fate", "attribute"): tuple(range(-2, 9)),  # not a standard Fate Core attribute!
    ("fate", "skill"): tuple(range(-2, 9)),
    ("eclipse_phase", "attribute"): tuple(range(5, 41, 5)),  # aptitude proxy only
    ("eclipse_phase", "skill"): tuple(range(0, 101, 5)),  # percentile test target
    ("without_number", "attribute"): (-2, -1, 0, 1, 2),  # modifier, NOT 3d6 score
    ("without_number", "skill"): (-1, 0, 1, 2, 3, 4),
    ("noopunk", "difficulty"): (9, 13, 15, 17, 21, 24, 29),
    ("fudge", "difficulty"): tuple(range(-3, 4)),
    ("fate", "difficulty"): tuple(range(-2, 9)),
    ("eclipse_phase", "difficulty"): (90, 75, 60, 45, 30, 20, 10),
    ("without_number", "difficulty"): (6, 8, 10, 12, 14, 16, 18),
}

# An EP percentile high test target means EASIER, opposite typical DV. This
# explicitly ordered list avoids silently reversing difficulty.
DIFFICULTY_EASIEST_TO_HARDEST = {
    family: (tuple(reversed(bands)) if family == "eclipse_phase" else bands)
    for (family, kind), bands in BANDS.items() if kind == "difficulty"
}


@dataclass(frozen=True)
class ConvertedRating:
    source: str
    target: str
    kind: str
    source_value: int
    target_value: int
    source_quantile: Fraction
    lossy: bool = True
    status: str = "EXPERIMENTAL_ORDINAL_NOT_RULE_EQUIVALENCE"


def _bands(family: str, kind: str) -> tuple[int, ...]:
    if kind == "difficulty":
        try:
            return DIFFICULTY_EASIEST_TO_HARDEST[family]
        except KeyError as exc:
            raise ValueError(f"Unsupported difficulty family: {family}") from exc
    try:
        return BANDS[(family, kind)]
    except KeyError as exc:
        raise ValueError(f"Unsupported rating: {family}/{kind}") from exc


def convert(value: int, source: Family, target: Family, kind: Kind) -> ConvertedRating:
    """Map ordinal rank (inclusive endpoints); exact rationals, ties round down.

    This is a *semantic* crosswalk only, not a claim that percentile, 4dF,
    2d6, and d10 probabilities can be matched with a single linear formula.
    """
    if type(value) is not int:
        raise TypeError("A rating must be an integer, never bool or float")
    source_values, target_values = _bands(source, kind), _bands(target, kind)
    if value not in source_values:
        raise ValueError(f"{source} {kind} value {value} is outside supported anchors")
    if source == target:
        return ConvertedRating(source, target, kind, value, value,
                               Fraction(source_values.index(value), len(source_values)-1),
                               lossy=False)
    quantile = Fraction(source_values.index(value), len(source_values) - 1)
    # Round ties toward the lower ordinal rank deterministically.
    position = quantile * (len(target_values) - 1)
    idx = (2 * position.numerator + position.denominator - 1) // (2 * position.denominator)
    return ConvertedRating(source, target, kind, value, target_values[idx], quantile)


def compare_all(value: int, kind: Kind, source: Family = "noopunk") -> dict[str, ConvertedRating]:
    return {family: convert(value, source, family, kind) for family in
            ("noopunk", "fudge", "fate", "eclipse_phase", "without_number")}


def conversion_loss(value: int, source: Family, target: Family, kind: Kind) -> bool:
    """Whether a round trip loses the original ordinal anchor."""
    intermediate = convert(value, source, target, kind)
    return convert(intermediate.target_value, target, source, kind).target_value != value
