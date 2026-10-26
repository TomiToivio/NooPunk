"""Cities Without Number: Major Injury outcomes.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``),
``rules-of-the-game/injury-healing-system-strain/major-injuries/``.

## The procedure around this table

A character reduced to zero hit points by lethal damage in the same scene as a Traumatic Hit must make
a **Physical save**. Passing still leaves them Mortally Wounded but stabilisable; failing means they
roll **1d12** on this table. A roll below 1 counts as 1 and a roll above 12 counts as 12.

``src/rules/cwn_trauma.py`` owns the *risk* (``major_injury_risk``) and ``cwn_core`` owns the save.
This module owns the outcome and the consequences a runtime has to apply: death, coma, blindness,
ruined limbs, damaged cyber locations, and which injuries need Prosthetic Cyber (or clone replacement)
before the character functions again.

## What is data and what is behaviour

Where the SRD names cyber without naming a body location (eye damage names cybereyes and their
implants, not "Head"), no location is invented here.

The twelve rows are content and live in :data:`MAJOR_INJURY_TABLE` so a campaign can reword or
localise them without touching arithmetic. The *questions a runtime asks* — is this lethal, does it
require prosthetics, which cyber locations are destroyed — are methods, because those are the rules.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: SRD: "a roll less than 1 still counts as 1, and one more than 12 still counts as 12".
MIN_ROLL = 1
MAX_ROLL = 12

#: SRD: Internal Damage (2) and Gut Wound (5) kill within an hour without a street doc.
HOURS_TO_DEATH_WITHOUT_CARE = 1


@dataclass(frozen=True)
class MajorInjury:
    """One row of the d12 table, with the consequences expressed as flags."""

    roll: int
    id: str
    label: str
    summary: str
    lethal: bool = False
    dies_within_hours: int | None = None
    coma_until_prosthetic: bool = False
    blinded_until_cybereyes: bool = False
    ruined_limb: str | None = None
    damaged_cyber_locations: tuple[str, ...] = field(default_factory=tuple)
    damaged_most_expensive_implant: bool = False
    requires_prosthetic: bool = False
    flesh_wound: bool = False

    @property
    def is_permanent_without_treatment(self) -> bool:
        """Whether ordinary stabilisation is not enough to restore the character."""
        return (
            self.lethal
            or self.coma_until_prosthetic
            or self.blinded_until_cybereyes
            or self.ruined_limb is not None
            or self.damaged_most_expensive_implant
        )


#: The twelve outcomes. ``11`` and ``12`` share one row in the SRD.
MAJOR_INJURY_TABLE: dict[int, MajorInjury] = {
    1: MajorInjury(1, "instant-death", "Instant Death",
                   "Dead; no recovery.",
                   lethal=True),
    2: MajorInjury(2, "internal-damage", "Internal Damage",
                   "Coma until a Prosthetic Cyber is installed; dead in an hour without a street doc.",
                   coma_until_prosthetic=True,
                   dies_within_hours=HOURS_TO_DEATH_WITHOUT_CARE,
                   damaged_cyber_locations=("Body", "Nerves"),
                   requires_prosthetic=True),
    3: MajorInjury(3, "brain-damage", "Brain Damage",
                   "Coma until a Prosthetic Cyber is installed.",
                   coma_until_prosthetic=True,
                   damaged_cyber_locations=("Head", "Nerves"),
                   requires_prosthetic=True),
    4: MajorInjury(4, "eye-damage", "Eye Damage",
                   "Blind until cybereyes; existing cybereyes and their implants are destroyed.",
                   blinded_until_cybereyes=True,
                   # The SRD names cybereyes and "implants in them" but no body location; the
                   # table therefore does not claim one.
                   requires_prosthetic=True),
    5: MajorInjury(5, "gut-wound", "Gut Wound",
                   "-1 to the Con modifier until a Prosthetic Cyber is installed; dead in an hour "
                   "without a street doc.",
                   dies_within_hours=HOURS_TO_DEATH_WITHOUT_CARE,
                   requires_prosthetic=True),
    6: MajorInjury(6, "right-leg", "Right Leg Ruined",
                   "Can crawl at best once stabilised.",
                   ruined_limb="right leg",
                   damaged_cyber_locations=("right leg",),
                   requires_prosthetic=True),
    7: MajorInjury(7, "left-leg", "Left Leg Ruined",
                   "Can crawl at best once stabilised.",
                   ruined_limb="left leg",
                   damaged_cyber_locations=("left leg",),
                   requires_prosthetic=True),
    8: MajorInjury(8, "right-arm", "Right Arm Ruined",
                   "One functional hand only.",
                   ruined_limb="right arm",
                   damaged_cyber_locations=("right arm",),
                   requires_prosthetic=True),
    9: MajorInjury(9, "left-arm", "Left Arm Ruined",
                   "One functional hand only.",
                   ruined_limb="left arm",
                   damaged_cyber_locations=("left arm",),
                   requires_prosthetic=True),
    10: MajorInjury(10, "system-damage", "System Damage",
                    "The most System Strain-expensive implant is critically damaged.",
                    damaged_most_expensive_implant=True),
    11: MajorInjury(11, "flesh-wound", "Just a Flesh Wound",
                    "Not as bad as it looked.",
                    flesh_wound=True),
    12: MajorInjury(12, "flesh-wound", "Just a Flesh Wound",
                    "Not as bad as it looked.",
                    flesh_wound=True),
}


def resolve_major_injury(roll: int, *, modifier: int = 0) -> MajorInjury:
    """Apply the table, clamping the adjusted roll into 1..12 as the SRD requires."""
    adjusted = roll + modifier
    if adjusted < MIN_ROLL:
        adjusted = MIN_ROLL
    if adjusted > MAX_ROLL:
        adjusted = MAX_ROLL
    return MAJOR_INJURY_TABLE[adjusted]


def requires_prosthetic(injury: MajorInjury) -> bool:
    """Whether a Prosthetic Cyber (or cloned tissue) is needed to restore function."""
    return injury.requires_prosthetic


def damaged_cyber_locations(injury: MajorInjury) -> tuple[str, ...]:
    """Cyber locations the injury critically damages (empty when none are named)."""
    return injury.damaged_cyber_locations


def is_lethal(injury: MajorInjury) -> bool:
    """Instant death, the one outcome no treatment undoes."""
    return injury.lethal


def dies_without_care_within(injury: MajorInjury) -> int | None:
    """Hours to death if the character never reaches a street doc, or ``None``."""
    return injury.dies_within_hours
