"""Minimaalinen pelitila vastaanottokeskustelulle.

Vain tähän kohtaukseen tarvittavat tiedot. Ei yleistä järjestelmää.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class EnrollmentStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    ADDITIONAL_SCREENING = "additional_screening"
    REJECTED = "rejected"


@dataclass
class Player:
    """Romppaisen minimaalinen tila tässä kohtauksessa."""

    cover_identity: str = "Emil Romppainen"
    attributes: dict[str, int] = field(default_factory=lambda: {
        "Intelligence": 4,
        "Awareness": 3,
        "Reflexes": 3,
        "Body": 3,
        "Charisma": 3,
        "Willpower": 3,
        "Cybernetics": 3,
    })

    def get_attribute(self, name: str) -> int:
        return self.attributes.get(name, 0)


@dataclass
class Receptionist:
    """Dr. Elin Dahlin paikallinen tila tässä kohtauksessa."""

    name: str = "Dr. Elin Dahl"
    suspicion: int = 0
    trust: int = 0
    mood: str = "läpitunkematon"

    def adjust_suspicion(self, amount: int) -> None:
        self.suspicion = max(0, min(10, self.suspicion + amount))

    def adjust_trust(self, amount: int) -> None:
        self.trust = max(-5, min(10, self.trust + amount))


@dataclass
class Scene:
    """Kohtauksen tila."""

    current_node: str = "test_room"
    enrollment_status: EnrollmentStatus = EnrollmentStatus.PENDING


@dataclass
class ReceptionGame:
    """Koko vastaanottokohtauksen pelitila."""

    player: Player = field(default_factory=Player)
    receptionist: Receptionist = field(default_factory=Receptionist)
    scene: Scene = field(default_factory=Scene)

    @property
    def is_finished(self) -> bool:
        return self.scene.enrollment_status != EnrollmentStatus.PENDING

    def resolve_outcome(self) -> EnrollmentStatus:
        """Laske lopputulos suspicion ja trust perusteella."""
        if self.receptionist.suspicion >= 8:
            return EnrollmentStatus.REJECTED
        if self.receptionist.suspicion >= 5:
            return EnrollmentStatus.ADDITIONAL_SCREENING
        return EnrollmentStatus.ACCEPTED
