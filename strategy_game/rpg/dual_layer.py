"""Two scales of action sharing the established Fate resolver.

No strategy economy, political model or TI numeric rules are defined here.
Fate Core System © Evil Hat Productions, CC BY 3.0; see ATTRIBUTION.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from random import Random

from .fate import Action, Character, Resolution, ResourceError
from .scene import Check, Scene, check

INDIVIDUAL_SKILLS = ("COG", "INT", "REF", "SAV", "SOM", "WIL")

# Design candidates, NOT adopted NoöPunk strategic skill canon.
PROPOSED_STRATEGIC_SKILLS = (
    "Persuasion", "Investigation", "Espionage", "Command",
    "Administration", "Science", "Security",
)


class Scale(str, Enum):
    RPG = "individual"
    STRATEGY = "faction_agent"


@dataclass
class DualLayerCharacter:
    """One Fate sheet, two skill namespaces; never infer one from the other."""
    character: Character
    individual_skills: dict[str, int] = field(default_factory=dict)
    strategic_skills: dict[str, int] = field(default_factory=dict)
    capabilities: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if set(self.individual_skills) != set(INDIVIDUAL_SKILLS):
            raise ResourceError("individual sheet requires exactly COG INT REF SAV SOM WIL")
        for domain in (self.individual_skills, self.strategic_skills):
            if any(type(value) is not int or not 0 <= value <= 4 for value in domain.values()):
                raise ResourceError("skill ratings must be integer Fate ratings 0..4")
        if any(not key.strip() for key in self.strategic_skills):
            raise ResourceError("strategic skills need nonempty names")

    def rating(self, scale: Scale, skill: str) -> int:
        if scale is Scale.RPG:
            if skill not in INDIVIDUAL_SKILLS:
                raise ResourceError(f"{skill!r} is not an individual RPG skill")
            return self.individual_skills[skill]
        if scale is Scale.STRATEGY:
            if skill not in self.strategic_skills:
                raise ResourceError(f"{skill!r} is not configured for strategic missions")
            return self.strategic_skills[skill]
        raise ResourceError("unknown action scale")

    def act(
        self, scale: Scale, action: Action, skill: str, difficulty: int, *,
        rng: Random, scene: Scene | None = None,
        invocation: str | None = None, free: bool = False, reroll: bool = False,
        required_capability: str | None = None, permitted: bool = True,
    ) -> Check:
        if required_capability and required_capability not in self.capabilities:
            raise ResourceError(f"special action requires {required_capability!r}")
        # The legacy Fate Character stores broad skills. Use a temporary
        # exact skill view so context selection never mutates the underlying sheet.
        rating = self.rating(scale, skill)
        temporary = Character(
            id=self.character.id, name=self.character.name,
            aspects=self.character.aspects, skills={skill: rating},
            stunts=self.character.stunts, fate_points=self.character.fate_points,
            physical_stress=self.character.physical_stress,
            mental_stress=self.character.mental_stress,
            consequences=self.character.consequences, gear=self.character.gear,
            body=self.character.body, cortical_stack=self.character.cortical_stack,
            resleeved=self.character.resleeved, natural_psi=self.character.natural_psi,
            psi_abilities=self.character.psi_abilities, statuses=self.character.statuses,
            tags=self.character.tags,
        )
        result = check(temporary, action, skill, difficulty, rng=rng,
                       scene=scene, invocation=invocation, free=free,
                       reroll=reroll, permitted=permitted)
        self.character.fate_points = temporary.fate_points
        return result


@dataclass(frozen=True)
class StrategicOrder:
    agent_id: str
    action: Action
    skill: str
    difficulty: int
    required_capability: str | None = None


@dataclass
class CouncilTurn:
    """One leader + four agents, maximum one declared order each turn.

    This is an action-count guard, not an implementation of faction mission
    scheduling, travel, or world-state effects.
    """
    leader: DualLayerCharacter
    agents: tuple[DualLayerCharacter, ...]
    orders: dict[str, StrategicOrder] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.agents) != 4:
            raise ResourceError("council must contain four agents plus its leader")
        ids = [x.character.id for x in (self.leader, *self.agents)]
        if len(ids) != len(set(ids)):
            raise ResourceError("council character ids must be unique")

    def assign(self, order: StrategicOrder) -> None:
        member = self.member(order.agent_id)
        member.rating(Scale.STRATEGY, order.skill)
        if order.required_capability and order.required_capability not in member.capabilities:
            raise ResourceError("agent lacks special mission capability")
        if order.agent_id in self.orders:
            raise ResourceError("agent already has an order this turn")
        self.orders[order.agent_id] = order

    def member(self, identifier: str) -> DualLayerCharacter:
        for member in (self.leader, *self.agents):
            if member.character.id == identifier:
                return member
        raise ResourceError(f"unknown council agent {identifier!r}")

    def resolve_orders(self, *, rng: Random) -> dict[str, Resolution]:
        # Does not apply mission effects, mutate worlds, or clear orders.
        return {
            identifier: self.member(identifier).act(
                Scale.STRATEGY, order.action, order.skill, order.difficulty,
                rng=rng, required_capability=order.required_capability,
            ).resolution
            for identifier, order in self.orders.items()
        }

    def next_turn(self) -> None:
        self.orders.clear()
