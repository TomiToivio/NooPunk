"""SWN-inspired psychic resource accounting on NoöPunk's CWN chassis.

Original implementation of the numerical mechanics referenced in SWN Revised,
Psionics (pp. 29-43). Refer to the purchased rulebook for the actual technique
effects and prerequisites. No protected ability descriptions are embedded here.
Natural human psionics are learned in the NoöPunk setting, but the selected
psychic character package must authorize access to techniques.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from .wn_core import attribute_modifier

DISCIPLINES = ("Biopsionics", "Metapsionics", "Precognition", "Telekinesis", "Telepathy", "Teleportation")


class PsiRulesError(ValueError):
    pass


class Duration(str, Enum):
    ACTIVE = "active"           # released when the technique ends
    SCENE = "scene"             # held through the scene
    DAY = "day"                 # held until rest


@dataclass
class Psychic:
    """Effort is reserved rather than expended; different reservations recover at different times."""

    wisdom: int
    constitution: int
    disciplines: dict[str, int] = field(default_factory=dict)
    permissions: set[str] = field(default_factory=set)
    reservations: dict[str, tuple[int, Duration]] = field(default_factory=dict)
    scene: int = 0

    def __post_init__(self) -> None:
        attribute_modifier(self.wisdom)
        attribute_modifier(self.constitution)
        for name, rank in self.disciplines.items():
            if name not in DISCIPLINES or not isinstance(rank, int) or not 0 <= rank <= 4:
                raise PsiRulesError(f"invalid psychic discipline/rank: {name}={rank}")

    @property
    def capacity(self) -> int:
        """SWN Revised Effort: 1 + best(WIS, CON) modifier + highest discipline rank.

        A qualified psychic always has at least one Effort available; character
        creation packages and techniques remain separate requirements.
        """
        highest = max(self.disciplines.values(), default=0)
        return max(1, 1 + max(attribute_modifier(self.wisdom), attribute_modifier(self.constitution)) + highest)

    @property
    def free(self) -> int:
        return self.capacity - sum(amount for amount, _ in self.reservations.values())

    def knows(self, discipline: str, minimum_rank: int = 0) -> bool:
        return discipline in self.disciplines and self.disciplines[discipline] >= minimum_rank

    def commit(self, key: str, discipline: str, *, minimum_rank: int = 0,
               duration: Duration = Duration.SCENE, amount: int = 1) -> None:
        if not key or key in self.reservations:
            raise PsiRulesError("commitment key must be unique and nonempty")
        if not self.knows(discipline, minimum_rank):
            raise PsiRulesError("technique is not accessible at this psychic skill rank")
        if not isinstance(duration, Duration):
            raise PsiRulesError("invalid effort duration")
        if amount <= 0 or amount > self.free:
            raise PsiRulesError("insufficient uncommitted Effort")
        self.reservations[key] = (amount, duration)

    def release(self, key: str) -> bool:
        """Only active commitments can be voluntarily freed immediately."""
        if key not in self.reservations:
            return False
        if self.reservations[key][1] is not Duration.ACTIVE:
            raise PsiRulesError("scene/day Effort cannot be prematurely refunded")
        del self.reservations[key]
        return True

    def end_scene(self) -> None:
        self.scene += 1
        self.reservations = {k: v for k, v in self.reservations.items()
                             if v[1] is Duration.DAY}

    def rest(self) -> None:
        self.reservations.clear()

    def snapshot(self) -> dict:
        return {
            "wisdom": self.wisdom, "constitution": self.constitution,
            "disciplines": dict(self.disciplines), "permissions": sorted(self.permissions),
            "scene": self.scene,
            "reservations": {k: {"amount": a, "duration": d.value}
                             for k, (a, d) in self.reservations.items()},
        }

    @classmethod
    def from_snapshot(cls, state: dict) -> "Psychic":
        psychic = cls(
            wisdom=int(state["wisdom"]), constitution=int(state["constitution"]),
            disciplines=dict(state.get("disciplines", {})),
            permissions=set(state.get("permissions", [])),
            scene=int(state.get("scene", 0)),
        )
        for key, raw in state.get("reservations", {}).items():
            psychic.reservations[str(key)] = (int(raw["amount"]), Duration(raw["duration"]))
        if any(a <= 0 for a, _ in psychic.reservations.values()) or psychic.free < 0:
            raise PsiRulesError("invalid persisted Effort commitments")
        return psychic
