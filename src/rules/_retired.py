"""Retired compatibility surface, kept so the migration is deliberate.

Issue #111 made NoöPunk an independent system and replaced the resolution kernel with

    STAT + Skill + 1d10  vs  DV

That rewrote ``rules.core``. Several symbols the *old* kernel exported were dropped with
it, but they are still imported by runtimes and guards that have not finished migrating —
``test_concordia_runtime``, ``test_issue40_resolver_seam`` and parts of
``test_issue51_tag_system``. Dropping them silently removed whole test modules from the
suite at import time, which is how a green build hid the loss.

Nothing here is canonical mechanics. This module exists ONLY so the migration can proceed
deliberately: the canonical check remains STAT + Skill + 1d10 vs DV, and no value in this
file changes what a check resolves to. Each name is either a compatibility alias or the
retired 3d6 *generation* helper, retained because character generation is still an open
design area (AGENTS.md §4) and the helper is referenced by the tag prototype's fixtures.

Do not extend this module. Port the caller to the #111 kernel and delete the entry.
"""

from __future__ import annotations

import json
import random
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol

_CANON_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "core.json"
_CANON = json.loads(_CANON_PATH.read_text(encoding="utf-8"))

ATTRIBUTE_DEFINITIONS = tuple(_CANON.get("attributes", ()))
ATTRIBUTE_IDS = tuple(item["id"] for item in ATTRIBUTE_DEFINITIONS)

#: Historical modifier bounds from the retired situational-modifier scale. The #111
#: kernel deliberately leaves modifiers unresolved (RULEBOOK §10.3).
SITUATIONAL_MODIFIER_MIN = -2
SITUATIONAL_MODIFIER_MAX = 2

#: Historical cap on the aiding bonus from the retired kernel.
AID_BONUS_CAP = int(_CANON.get("aiding", {}).get("cap", 2))

#: Historical penalty applied to an unskilled attempt in the retired kernel.
UNSKILLED_PENALTY = -1

_HUMAN_MODIFIERS = {
    int(k): int(v)
    for k, v in _CANON.get("human_3d6_generation", {}).get("modifier_table", {}).items()
}


class DiceSource(Protocol):
    def randint(self, a: int, b: int) -> int: ...


class SkillAccess(str, Enum):
    """Whether an action can be attempted without the relevant skill.

    Retired by issue #111: the independent kernel does not gate checks on skill
    access. Kept for callers still passing it; the kernel ignores it.
    """

    UNSKILLED_ALLOWED = "unskilled_allowed"
    TRAINED_ONLY = "trained_only"


@dataclass(frozen=True, slots=True)
class HumanAttributes:
    """A generated ordinary-human attribute set: raw 3d6 rolls plus modifiers.

    Character generation is an open design area (AGENTS.md §4); issue #111 did not
    define it, so the previous 3d6 generator is retained here rather than deleted,
    and is explicitly NOT the canonical procedure.
    """

    raw_rolls: Mapping[str, int]
    modifiers: object

    def __post_init__(self) -> None:
        raw = dict(self.raw_rolls)
        if ATTRIBUTE_IDS and set(raw) != set(ATTRIBUTE_IDS):
            raise ValueError(f"Raw rolls must be exactly: {', '.join(ATTRIBUTE_IDS)}")
        if any(roll < 3 or roll > 18 for roll in raw.values()):
            raise ValueError("Human 3d6 attribute rolls must be in 3..18.")
        object.__setattr__(self, "raw_rolls", raw)


def human_modifier(raw_3d6: int) -> int:
    """Map a 3d6 attribute *generation* roll to its modifier."""
    try:
        return _HUMAN_MODIFIERS[raw_3d6]
    except KeyError as exc:
        raise ValueError("Human attribute generation requires a 3d6 total in 3..18.") from exc


def generate_human_attributes(rng: DiceSource | None = None) -> HumanAttributes:
    """Generate ordinary-human attributes: 3d6 per attribute, then the table.

    Retired generation procedure kept for compatibility only.
    """
    source = rng if rng is not None else random
    raw = {attribute_id: sum(source.randint(1, 6) for _ in range(3))
           for attribute_id in ATTRIBUTE_IDS}
    from .core import AttributeSet

    return HumanAttributes(
        raw_rolls=raw,
        modifiers=AttributeSet(
            {attribute_id: human_modifier(roll) for attribute_id, roll in raw.items()}
        ),
    )
