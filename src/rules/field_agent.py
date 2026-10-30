"""NoöPunk field-agent generation on the CWN chassis (#809).

The author's direction: NoöPunk customises CWN/SWN more than a literal port, but the mechanics that do
exist stay CWN's until an explicit replacement is written down. This module is that boundary for
character generation.

**What is CWN, unchanged.** Six attributes on 3–18, rolled 3d6 in order, with the book's single
optional swap of two results; level 1 to start; a background that supplies skills; 2d6 skill checks
elsewhere in the rules.

**What is NoöPunk.** The character is a **law-enforcement field agent** — Suojelupoliisi, Europol or
UNSA — and the agency is a real choice with a skill consequence, not a label. Romppainen is *not*
generated here: he is a senior NPC, and making him a level-1 player character would be the exact
mistake the design reversed.

Determinism matters more than variety: the same seed must produce the same agent, because a save that
cannot be replayed is not a save. All randomness arrives through an injected ``random.Random``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

ATTRIBUTES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
ATTRIBUTE_MIN = 3
ATTRIBUTE_MAX = 18

#: SRD/CWN: a starting character is level 1.
STARTING_LEVEL = 1

#: The three services the player may belong to. The agency grants one trained skill; it does not
#: alter attributes, because that would be a rule change rather than a background choice.
AGENCIES: dict[str, str] = {
    "supo": "Suojelupoliisi — domestic security; the agency grants Investigate-0",
    "europol": "Europol — cross-border enforcement; the agency grants Connect-0",
    "unsa": "UNSA — the academy route; the agency grants Know-0",
}

AGENCY_SKILLS: dict[str, str] = {"supo": "Investigate", "europol": "Connect", "unsa": "Know"}


class GenerationError(ValueError):
    """A generation request the rules do not allow."""


@dataclass(frozen=True)
class FieldAgent:
    """A level-1 law-enforcement field agent."""

    name: str
    agency: str
    attributes: dict[str, int]
    skills: dict[str, int] = field(default_factory=dict)
    level: int = STARTING_LEVEL
    background: str = ""

    @property
    def is_player_character(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "name": self.name,
            "agency": self.agency,
            "attributes": dict(self.attributes),
            "skills": dict(self.skills),
            "level": self.level,
            "background": self.background,
            "is_player_character": True,
        }


def roll_attributes(rng: random.Random) -> dict[str, int]:
    """3d6 in order, per the CWN character-creation procedure."""
    return {attribute: sum(rng.randint(1, 6) for _ in range(3)) for attribute in ATTRIBUTES}


def swap_attributes(
    attributes: dict[str, int], first: str, second: str
) -> dict[str, int]:
    """The book's single optional swap of two attribute results."""
    if first not in attributes or second not in attributes:
        raise GenerationError(f"unknown attribute in swap: {first!r}/{second!r}")
    if first == second:
        raise GenerationError("a swap needs two different attributes")
    swapped = dict(attributes)
    swapped[first], swapped[second] = attributes[second], attributes[first]
    return swapped


def generate_field_agent(
    *,
    name: str,
    agency: str,
    rng: random.Random,
    background: str = "",
    swap: tuple[str, str] | None = None,
) -> FieldAgent:
    """Create a level-1 field agent for one of the three services.

    Attributes are CWN's; the agency contributes its trained skill. Nothing here makes the character
    psychic — psionics remain a separate, explicit character option.
    """
    if not name.strip():
        raise GenerationError("a field agent needs a name")
    key = agency.strip().lower()
    if key not in AGENCIES:
        raise GenerationError(f"unknown agency {agency!r}; expected one of {sorted(AGENCIES)}")

    attributes = roll_attributes(rng)
    if swap is not None:
        attributes = swap_attributes(attributes, *swap)

    for attribute, value in attributes.items():
        if not ATTRIBUTE_MIN <= value <= ATTRIBUTE_MAX:
            raise GenerationError(f"{attribute}={value} outside {ATTRIBUTE_MIN}-{ATTRIBUTE_MAX}")

    skills = {AGENCY_SKILLS[key]: 0}
    return FieldAgent(
        name=name.strip(),
        agency=key,
        attributes=attributes,
        skills=skills,
        background=background.strip(),
    )


def is_field_agent_record(record: dict) -> bool:
    """Guard for save data: only a generated agent may occupy the player-character slot."""
    return bool(record.get("is_player_character")) and record.get("agency") in AGENCIES
