"""NoöPunk's original, Fate Core SRD-based RPG implementation.

Fate Core System © Evil Hat Productions (CC BY 3.0). See ATTRIBUTION.md.
This code does not reproduce Transhumanity's Fate or Eclipse Phase setting text.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from random import Random
from typing import Mapping


class Action(str, Enum):
    OVERCOME = "overcome"
    CREATE_ADVANTAGE = "create_advantage"
    ATTACK = "attack"
    DEFEND = "defend"


class Outcome(str, Enum):
    FAILURE = "failure"
    TIE = "tie"
    SUCCESS = "success"
    SUCCESS_WITH_STYLE = "success_with_style"


def roll_fate(rng: Random) -> tuple[int, int, int, int]:
    """Roll four Fudge/Fate dice, each one of -1, 0 or +1."""
    return tuple(rng.choice((-1, 0, 1)) for _ in range(4))  # type: ignore[return-value]


@dataclass(frozen=True)
class Resolution:
    action: Action
    dice: tuple[int, int, int, int]
    skill: int
    difficulty: int
    total: int
    shifts: int
    outcome: Outcome

    @property
    def succeeds(self) -> bool:
        return self.shifts > 0


def resolve(
    action: Action,
    skill: int,
    difficulty: int,
    *,
    rng: Random,
    bonus: int = 0,
) -> Resolution:
    """Resolve a declared Fate action; GM adjudicates fictional permissions.

    Failure = negative shifts; tie = zero; success = +1/+2;
    success with style = at least +3 shifts. Consequences of each
    action (boosts, costs, stress) are chosen by scene rules/GM.
    """
    dice = roll_fate(rng)
    total = sum(dice) + skill + bonus
    shifts = total - difficulty
    outcome = (
        Outcome.FAILURE if shifts < 0 else
        Outcome.TIE if shifts == 0 else
        Outcome.SUCCESS_WITH_STYLE if shifts >= 3 else
        Outcome.SUCCESS
    )
    return Resolution(action, dice, skill, difficulty, total, shifts, outcome)


class ResourceError(ValueError):
    """Invalid Fate point, character or stress operation."""


@dataclass
class Consequence:
    name: str
    severity: int
    recovered: bool = False


@dataclass
class Character:
    id: str
    name: str
    aspects: list[str]
    skills: dict[str, int] = field(default_factory=dict)
    stunts: list[str] = field(default_factory=list)
    fate_points: int = 3
    physical_stress: list[bool] = field(default_factory=lambda: [False, False])
    mental_stress: list[bool] = field(default_factory=lambda: [False, False])
    consequences: list[Consequence] = field(default_factory=list)
    gear: list[str] = field(default_factory=list)
    # A biological body is default. A cortical stack is NOT mandatory.
    body: str = "original_biological"
    cortical_stack: bool = False
    resleeved: bool = False
    natural_psi: bool = False
    psi_abilities: list[str] = field(default_factory=list)
    statuses: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id or not self.name:
            raise ResourceError("character id and name are required")
        if self.fate_points < 0:
            raise ResourceError("fate_points cannot be negative")
        if any(not isinstance(v, int) or v < 0 for v in self.skills.values()):
            raise ResourceError("skills must be nonnegative integer ratings")
        if self.psi_abilities and not self.natural_psi:
            raise ResourceError("natural PSI abilities require natural_psi; equipment alone grants no innate PSI")

    def spend_fate_point(self) -> None:
        if self.fate_points < 1:
            raise ResourceError("not enough Fate points")
        self.fate_points -= 1

    def invoke(self, aspect: str, *, free: bool = False) -> int:
        """Invoke an existing aspect for +2. Rerolls are deliberately explicit elsewhere."""
        if aspect not in self.aspects:
            raise ResourceError(f"aspect not on sheet: {aspect}")
        if not free:
            self.spend_fate_point()
        return 2

    def absorb_hit(self, shifts: int, *, mental: bool = False) -> str:
        """Mark one unused stress box that can absorb the incoming shifts.

        Consequences must be chosen separately, rather than fabricated by this
        operation. If no box fits, return 'unabsorbed'.
        """
        if shifts <= 0:
            raise ResourceError("hit must contain positive shifts")
        track = self.mental_stress if mental else self.physical_stress
        for i, checked in enumerate(track):
            if not checked and i + 1 >= shifts:
                track[i] = True
                return f"stress_{i + 1}"
        return "unabsorbed"

    def take_consequence(self, name: str, severity: int) -> None:
        if severity not in (2, 4, 6):
            raise ResourceError("consequence severity must be mild(2), moderate(4), severe(6)")
        if any(c.severity == severity and not c.recovered for c in self.consequences):
            raise ResourceError("consequence slot occupied")
        self.consequences.append(Consequence(name, severity))

    def clear_stress(self) -> None:
        self.physical_stress = [False] * len(self.physical_stress)
        self.mental_stress = [False] * len(self.mental_stress)


def skill_check(
    actor: Character,
    action: Action,
    skill_name: str,
    difficulty: int,
    *,
    rng: Random,
    invoked_aspect: str | None = None,
) -> Resolution:
    """Same resolution mechanism for cyberspace, PSI, dialogue and combat.

    The caller/GM must establish access to the target and whether the proposed
    effect is within the character's ability. No unconditional remote intrusion
    or magical PSI permission is granted by rolling.
    """
    bonus = actor.invoke(invoked_aspect) if invoked_aspect else 0
    return resolve(action, actor.skills.get(skill_name, 0), difficulty, rng=rng, bonus=bonus)


def demo_investigation(seed: int = 42) -> Mapping[str, object]:
    """A compact pre-crisis investigation; no strategy turn mechanics."""
    rng = Random(seed)
    operative = Character(
        id="unspecified-field-agent", name="Field Investigator",
        aspects=["Augmented Forensic Investigator", "Precognitive Impressions"],
        skills={"Investigate": 2, "Technology": 2, "Psi": 1},
        gear=["Secure BCI", "Forensic lens"],
        natural_psi=True, psi_abilities=["precognitive_impressions"],
    )
    # Fiction-first checks: local system access and voluntary PSI observation.
    cyber = skill_check(operative, Action.OVERCOME, "Technology", 2, rng=rng)
    psi = skill_check(operative, Action.CREATE_ADVANTAGE, "Psi", 1, rng=rng)
    return {"character": operative.id, "cyber": cyber, "psi": psi}


def demo_netrunning(seed: int = 7) -> Mapping[str, object]:
    """A compact BCI netrunning scene, resolved by the same engine as any other scene.

    Netrunning invents no second mechanic here: augmentation is where a netrunner starts, and
    **reachability is fiction, not a skill bonus** -- a heavily augmented runner may be skilled and
    still unable to reach a target, which no roll can grant. See ``cyber.py`` and
    ``data/connectivity.json`` for that model; this function only demonstrates that a cyber scene and a
    PSI scene share one resolution path.
    """
    rng = Random(seed)
    netrunner = Character(
        id="field-netrunner", name="Field Netrunner",
        aspects=["Deck-Scarcity Trained", "A Wireless BCI Is an Exposed Endpoint"],
        skills={"Technology": 3, "Notice": 1},
        gear=["BCI rig", "specialist deck"],
        natural_psi=False,
    )
    approach = skill_check(netrunner, Action.OVERCOME, "Technology", 2, rng=rng)
    defend = skill_check(netrunner, Action.DEFEND, "Technology", 1, rng=rng)
    return {
        "character": netrunner.id,
        "reachability": "fiction-first: a reachable path must exist before any roll",
        "approach": approach,
        "defend": defend,
        "psi": "not involved: a BCI rig is an interface, not an innate PSI ability",
    }
