"""Normalize interface character sheets before calling immutable CWN save rules.

This is an adapter, not an alternate save implementation. Attribute inputs are
*scores* (3..18), not already-computed modifiers. The published formula lives
exclusively in :mod:`rules.wn_core`.
"""
from __future__ import annotations

from collections.abc import Mapping

from . import wn_core

_CANONICAL = {
    name.lower(): code for name, code in zip(wn_core.ATTRIBUTES, wn_core.ATTRIBUTE_CODES)
}
_CANONICAL.update({code.lower(): code for code in wn_core.ATTRIBUTE_CODES})


def normalize_attribute_scores(attributes: Mapping[str, int]) -> dict[str, int]:
    """Return code-keyed modifiers from full, abbreviated or lowercase score keys.

    Missing scores remain missing; a save involving them is rejected rather
    than silently assuming an attribute modifier of zero. Multiple aliases
    for an attribute must agree.
    """
    scores: dict[str, int] = {}
    for name, score in attributes.items():
        key = _CANONICAL.get(str(name).lower())
        if key is None:
            raise wn_core.WnError(f"unknown attribute {name!r}")
        if key in scores and scores[key] != score:
            raise wn_core.WnError(f"conflicting values for {key}")
        scores[key] = score
    return {code: wn_core.attribute_modifier(score) for code, score in scores.items()}


def save_target(kind: str, *, level: int, attributes: Mapping[str, int]) -> int:
    """Resolve a CWN save using the canonical formula for any sheet spelling."""
    key = kind.lower()
    if key not in wn_core.SAVE_ATTRIBUTES:
        raise wn_core.WnError(f"unknown save type {kind!r}")
    if not 1 <= level <= 10:
        raise wn_core.WnError(f"character level must be 1..10, got {level}")
    modifiers = normalize_attribute_scores(attributes)
    missing = [name for name in wn_core.SAVE_ATTRIBUTES[key] if name not in modifiers]
    if missing:
        raise wn_core.WnError(f"missing attributes for {key} save: {', '.join(missing)}")
    return wn_core.save_target(key, level=level, modifiers=modifiers)
