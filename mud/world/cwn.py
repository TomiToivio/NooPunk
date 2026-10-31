"""The CWN rules the MUD shares with the rest of NoöPunk (#946).

**This module owns no arithmetic.** It imports the pure-Python kernel the tabletop and
Godot rules were built from — ``<repo>/src/rules`` — which never imports Godot and never
needs a running engine. A second copy of the check formula here would be a second rules
system, which is the one thing #897's foundation lock forbids.

Deliberately **no Evennia import**: the sheet and the check must be testable without a
server, and the number a MUD command reports is the same number a table would report.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

#: `<repo>/src`, so the MUD can import the shared kernel from a plain checkout.
SHARED_RULES = Path(__file__).resolve().parents[2] / "src"
if str(SHARED_RULES) not in sys.path:  # pragma: no cover - import plumbing
    sys.path.insert(0, str(SHARED_RULES))

from rules.cwn_character import ARRAY, assign_array  # noqa: E402
from rules.wn_core import (  # noqa: E402
    ATTRIBUTES,
    DIFFICULTY_EXPERT,
    DIFFICULTY_SIGNIFICANT,
    DIFFICULTY_SIMPLE,
    Check,
    attribute_modifier,
    skill_check,
)

#: CWN's fixed array, in the order the kernel declares the attributes. A MUD character
#: takes the array route (one legal creation path, deterministic and replayable) rather
#: than rolling 3d6 on every connect.
DEFAULT_ATTRIBUTES: dict[str, int] = dict(zip(ATTRIBUTES, ARRAY))

#: A starting spread. Level 1 in two skills, level 0 in two, everything else untrained —
#: the SRD's own shape, and the -1 untrained penalty is the kernel's business.
DEFAULT_SKILLS: dict[str, int] = {"Notice": 1, "Survive": 1, "Talk": 0, "Fix": 0}

#: Every check in the MUD names one of these, so a difficulty is never an invented number.
DIFFICULTIES: dict[str, int] = {
    "simple": DIFFICULTY_SIMPLE,
    "significant": DIFFICULTY_SIGNIFICANT,
    "expert": DIFFICULTY_EXPERT,
}

ATTRIBUTE_FOR_SKILL: dict[str, str] = {
    "Administer": "Intelligence", "Connect": "Charisma", "Drive": "Dexterity",
    "Exert": "Constitution", "Fix": "Intelligence", "Heal": "Intelligence",
    "Know": "Intelligence", "Lead": "Charisma", "Notice": "Wisdom", "Perform": "Charisma",
    "Program": "Intelligence", "Punch": "Strength", "Shoot": "Dexterity", "Sneak": "Dexterity",
    "Stab": "Strength", "Survive": "Constitution", "Talk": "Charisma", "Trade": "Charisma",
    "Work": "Strength",
}


class SheetError(ValueError):
    """A sheet was asked for something the CWN rules do not allow."""


class Sheet:
    """A character's CWN numbers: six attributes, a skill map, and the check.

    Nothing here is stored by Evennia — the typeclass keeps ``to_dict()`` and reads it
    back, so a save is data rather than pickled Python.
    """

    def __init__(
        self,
        attributes: Mapping[str, int] | None = None,
        skills: Mapping[str, int] | None = None,
    ) -> None:
        try:
            self.attributes = assign_array(dict(attributes or DEFAULT_ATTRIBUTES))
        except Exception as exc:  # the kernel's own CharacterRulesError
            raise SheetError(str(exc)) from None
        self.skills = {str(name): int(level) for name, level in (skills or DEFAULT_SKILLS).items()}

    def modifier(self, attribute: str) -> int:
        if attribute not in self.attributes:
            raise SheetError(f"unknown attribute {attribute!r}")
        return attribute_modifier(self.attributes[attribute])

    def check(
        self,
        skill: str,
        *,
        difficulty: str = "significant",
        situational: int = 0,
        aid: int = 0,
        dice: Sequence[int] | None = None,
        rng: Any = None,
    ) -> Check:
        """One CWN skill check, on the shared kernel. This is the MUD's only resolution."""
        if skill not in ATTRIBUTE_FOR_SKILL:
            raise SheetError(f"unknown skill {skill!r}")
        if difficulty not in DIFFICULTIES:
            raise SheetError(f"unknown difficulty {difficulty!r}; the MUD names one of the bands")
        return skill_check(
            attribute_score=self.attributes[ATTRIBUTE_FOR_SKILL[skill]],
            skill_level=self.skills.get(skill),
            difficulty=DIFFICULTIES[difficulty],
            situational=situational,
            aid=aid,
            dice=dice,
            rng=rng,
        )

    def to_dict(self) -> dict[str, Any]:
        return {"attributes": dict(self.attributes), "skills": dict(self.skills)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Sheet":
        return cls(data.get("attributes"), data.get("skills"))

    def to_text(self) -> str:
        """The same rendering a table would read off a sheet, in one column."""
        rows = [f"{name:<13}{self.attributes[name]:>3}  ({self.modifier(name):+d})" for name in ATTRIBUTES]
        trained = sorted(
            (name, level) for name, level in self.skills.items() if level > 0
        )
        skills = ", ".join(f"{name} {level}" for name, level in trained) or "none"
        return "\n".join(rows) + f"\nSkills: {skills}"
