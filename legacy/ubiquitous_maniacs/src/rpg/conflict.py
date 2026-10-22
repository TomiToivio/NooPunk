"""One lightweight conflict procedure for every action domain."""

from __future__ import annotations

from dataclasses import dataclass, field

from .actions import ActionResult, ActionType
from .traits import Consequence


@dataclass
class Conflictant:
    id: str
    stress_capacity: int = 3
    stress: int = 0
    consequences: list[Consequence] = field(default_factory=list)
    conceded: bool = False

    @property
    def taken_out(self) -> bool:
        return not self.conceded and self.stress >= self.stress_capacity

    @property
    def out_of_conflict(self) -> bool:
        return self.conceded or self.taken_out

    def absorb_with_consequence(self, consequence: Consequence, shifts: int) -> int:
        if shifts < 0:
            raise ValueError("Shifts cannot be negative")
        self.consequences.append(consequence)
        return max(0, shifts - consequence.severity)

    def take_hit(self, shifts: int, consequence: Consequence | None = None) -> int:
        """Apply one hit after optionally absorbing shifts with a consequence."""
        if shifts < 0:
            raise ValueError("Shifts cannot be negative")
        remaining = (
            self.absorb_with_consequence(consequence, shifts)
            if consequence is not None
            else shifts
        )
        self.stress += remaining
        return remaining


@dataclass
class Conflict:
    domain: str
    participants: dict[str, Conflictant]
    round: int = 1

    def apply_exchange(
        self,
        attacker: str,
        defender: str,
        attack: ActionResult,
        defense: ActionResult,
        consequence: Consequence | None = None,
    ) -> int:
        if attacker not in self.participants or defender not in self.participants:
            raise KeyError("Both conflictants must be registered")
        attacker_state = self.participants[attacker]
        defender_state = self.participants[defender]
        if attacker_state.out_of_conflict or defender_state.out_of_conflict:
            raise ValueError("An exchange cannot include a participant who has left the conflict")
        if attack.action is not ActionType.ATTACK:
            raise ValueError("The attacking result must use the Attack action")
        if defense.action is not ActionType.DEFEND:
            raise ValueError("The defending result must use the Defend action")
        shifts = max(0, attack.check.total - defense.check.total)
        return defender_state.take_hit(shifts, consequence)

    def concede(self, participant: str, consequence: Consequence | None = None) -> None:
        actor = self.participants[participant]
        if actor.out_of_conflict:
            raise ValueError("Participant has already left the conflict")
        if consequence is not None:
            actor.consequences.append(consequence)
        actor.conceded = True
