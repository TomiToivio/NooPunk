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

#: SWN Revised, Torching (printed p.31): the die tells you what the burn costs.
TORCHING_TABLE: dict[int, str] = {
    1: "wisdom", 2: "wisdom",
    3: "constitution", 4: "constitution",
    5: "choice",
    6: "none",
}
#: A psychic whose Wisdom falls below 3 is feral; any other attribute below 3 is death.
ATTRIBUTE_FLOOR = 3
TORCH_GRANTED_EFFORT = 1
#: Which packages are unrestricted, and which are pinned to one discipline.
RESTRICTED_PACKAGES = frozenset({"swn_partial_psychic"})


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
    #: A Partial Psychic may master exactly one discipline; empty means unrestricted.
    restricted_discipline: str = ""
    #: Effort gained by torching. It may exceed the maximum and lasts only for the scene.
    torch_bonus: int = 0
    torched_round: int = -1

    def __post_init__(self) -> None:
        attribute_modifier(self.wisdom)
        attribute_modifier(self.constitution)
        for name, rank in self.disciplines.items():
            if name not in DISCIPLINES or not isinstance(rank, int) or not 0 <= rank <= 4:
                raise PsiRulesError(f"invalid psychic discipline/rank: {name}={rank}")
        if self.restricted_discipline and self.restricted_discipline not in DISCIPLINES:
            raise PsiRulesError(f"unknown restricted discipline {self.restricted_discipline!r}")
        if self.torch_bonus < 0:
            raise PsiRulesError("torched Effort cannot be negative")

    @property
    def capacity(self) -> int:
        """SWN Revised Effort: 1 + best(WIS, CON) modifier + highest discipline rank.

        A qualified psychic always has at least one Effort available; character
        creation packages and techniques remain separate requirements. Torched Effort is added on
        top and lasts only for the scene.
        """
        # A psychic burned below the attribute floor is feral or dead: no usable pool, and the
        # kernel refuses to price a score below 3, so this returns 0 rather than raising.
        if self.wisdom < ATTRIBUTE_FLOOR or self.constitution < ATTRIBUTE_FLOOR:
            return 0
        highest = max(self.disciplines.values(), default=0)
        base = max(1, 1 + max(attribute_modifier(self.wisdom), attribute_modifier(self.constitution)) + highest)
        return base + self.torch_bonus

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
        # Torched Effort was paid for with an attribute point; it lasts only for its scene.
        self.torch_bonus = 0

    def rest(self) -> None:
        self.reservations.clear()
        self.torch_bonus = 0

    def can_learn(self, discipline: str) -> bool:
        """Whether this psychic may study the discipline at all.

        An unrestricted psychic (the Psychic package) may raise any of the six. A restricted one
        (the Partial Psychic package) may master a single discipline and may not raise another.
        """
        if discipline not in DISCIPLINES:
            return False
        return not self.restricted_discipline or discipline == self.restricted_discipline

    def torch(self, *, die: int, round_number: int, choice: str = "") -> dict:
        """Burn past the Effort limit, once per round, and pay the table's price.

        Returns the effect and the resulting status: ``ok``, ``feral`` (Wisdom below 3) or ``dead``
        (any other attribute below 3). There is no cure.
        """
        if not 1 <= die <= 6:
            raise PsiRulesError(f"the torching die is a d6, got {die}")
        if round_number == self.torched_round:
            raise PsiRulesError("this character has already torched this round")
        effect = TORCHING_TABLE[die]
        if effect == "choice":
            if choice not in ("STR", "DEX", "CON", "INT", "WIS", "CHA"):
                raise PsiRulesError("a choice result needs one of the six attributes")
        self.torched_round = round_number
        self.torch_bonus += TORCH_GRANTED_EFFORT
        lost = ""
        if effect == "wisdom":
            self.wisdom -= 1
            lost = "WIS"
        elif effect == "constitution":
            self.constitution -= 1
            lost = "CON"
        elif effect == "choice":
            lost = choice
            if choice == "WIS":
                self.wisdom -= 1
            elif choice == "CON":
                self.constitution -= 1
        # Only Wisdom and Constitution are modelled here because they are the two attributes Effort
        # is computed from. A "choice" result naming another attribute is reported so the sheet can
        # apply it; this module never invents a second copy of the character.
        status = "ok"
        if self.wisdom < ATTRIBUTE_FLOOR:
            status = "feral"
        elif self.constitution < ATTRIBUTE_FLOOR:
            status = "dead"
        return {"granted": TORCH_GRANTED_EFFORT, "effect": effect, "attribute_lost": lost,
                "status": status, "capacity": self.capacity,
                "sheet_must_apply": lost if lost not in ("WIS", "CON") else ""}

    def snapshot(self) -> dict:
        return {
            "wisdom": self.wisdom, "constitution": self.constitution,
            "disciplines": dict(self.disciplines), "permissions": sorted(self.permissions),
            "scene": self.scene,
            "restricted_discipline": self.restricted_discipline,
            "torch_bonus": self.torch_bonus,
            "torched_round": self.torched_round,
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
            restricted_discipline=str(state.get("restricted_discipline", "")),
            torch_bonus=int(state.get("torch_bonus", 0)),
            torched_round=int(state.get("torched_round", -1)),
        )
        for key, raw in state.get("reservations", {}).items():
            psychic.reservations[str(key)] = (int(raw["amount"]), Duration(raw["duration"]))
        if any(a <= 0 for a, _ in psychic.reservations.values()) or psychic.free < 0:
            raise PsiRulesError("invalid persisted Effort commitments")
        return psychic
