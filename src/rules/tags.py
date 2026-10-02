"""Generic four-system tag model for NoöPunk issue #51.

Implements only author-specified design decisions:
- attributes are tags;
- relevant tags have signed integer ratings and stack;
- entities participate in Physical, Social, Psychic and Cybernetic systems;
- an absent system differs from a low attribute value.

It does not choose final attribute names, skills, combat, social mechanics,
psionics, or automatic tag applicability.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class SystemDomain(str, Enum):
    PHYSICAL = "physical"
    SOCIAL = "social"
    PSYCHIC = "psychic"
    CYBERNETIC = "cybernetic"


class TagCategory(str, Enum):
    ATTRIBUTE = "attribute"
    SKILL = "skill"
    SPECIALIZATION = "specialization"
    BACKGROUND = "background"
    PROFESSION = "profession"
    GEAR = "gear"
    CYBERWARE = "cyberware"
    BIOLOGICAL_MODIFICATION = "biological_modification"
    PSIONIC = "psionic"
    RELATIONSHIP = "relationship"
    FACTION = "faction"
    REPUTATION = "reputation"
    IDEOLOGY = "ideology"
    CONDITION = "condition"
    INJURY = "injury"
    ENVIRONMENT = "environment"
    NARRATIVE_FLAG = "narrative_flag"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Tag:
    """One mechanically or fictionally meaningful descriptor."""

    name: str
    rating: int
    category: TagCategory
    system: SystemDomain | None = None
    scopes: tuple[str, ...] = ()
    source: str = "character"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Tag name must not be empty.")
        if not isinstance(self.rating, int) or isinstance(self.rating, bool):
            raise TypeError("Tag rating must be an integer.")
        object.__setattr__(self, "scopes", tuple(self.scopes))

    @property
    def is_attribute(self) -> bool:
        return self.category is TagCategory.ATTRIBUTE

    @property
    def is_normal_human_attribute_value(self) -> bool:
        return self.is_attribute and -3 <= self.rating <= 3


@dataclass(frozen=True, slots=True)
class SystemState:
    """Participation in one of the four NoöPunk systems."""

    domain: SystemDomain
    present: bool = True
    tags: tuple[Tag, ...] = ()

    def __post_init__(self) -> None:
        tags = tuple(self.tags)
        if not self.present and tags:
            raise ValueError("An absent system cannot carry active system tags.")
        for tag in tags:
            if tag.system is not None and tag.system is not self.domain:
                raise ValueError(
                    f"Tag {tag.name!r} belongs to {tag.system.value}, not {self.domain.value}."
                )
        object.__setattr__(self, "tags", tags)

    def attribute_tags(self) -> tuple[Tag, ...]:
        return tuple(tag for tag in self.tags if tag.is_attribute)


@dataclass(frozen=True, slots=True)
class EntityState:
    """Minimal engine-independent state for a character or simulated entity."""

    entity_id: str
    systems: dict[SystemDomain, SystemState]
    global_tags: tuple[Tag, ...] = ()
    narrative_flags: tuple[Tag, ...] = ()

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id must not be empty.")
        systems = dict(self.systems)
        if set(systems) != set(SystemDomain):
            missing = sorted(domain.value for domain in set(SystemDomain) - set(systems))
            extra = sorted(str(domain) for domain in set(systems) - set(SystemDomain))
            raise ValueError(f"Entity must define all four systems; missing={missing}, extra={extra}")
        for domain, state in systems.items():
            if state.domain is not domain:
                raise ValueError(f"System mapping key {domain.value} does not match state domain.")
        object.__setattr__(self, "systems", systems)
        object.__setattr__(self, "global_tags", tuple(self.global_tags))
        object.__setattr__(self, "narrative_flags", tuple(self.narrative_flags))

    def system_present(self, domain: SystemDomain) -> bool:
        return self.systems[domain].present

    def tags_for(self, domain: SystemDomain) -> tuple[Tag, ...]:
        return self.systems[domain].tags


@dataclass(frozen=True, slots=True)
class TagStack:
    """Transparent sum of tags already judged relevant."""

    tags: tuple[Tag, ...]
    total: int


def stack_relevant_tags(tags: Iterable[Tag]) -> TagStack:
    """Sum ratings without inventing semantic applicability rules."""
    selected = tuple(tags)
    return TagStack(tags=selected, total=sum(tag.rating for tag in selected))


def absent_system(domain: SystemDomain) -> SystemState:
    """Explicit absence, not an attribute score of -3 or lower."""
    return SystemState(domain=domain, present=False, tags=())


def present_system(domain: SystemDomain, *tags: Tag) -> SystemState:
    return SystemState(domain=domain, present=True, tags=tuple(tags))


__all__ = [
    "EntityState",
    "SystemDomain",
    "SystemState",
    "Tag",
    "TagCategory",
    "TagStack",
    "absent_system",
    "present_system",
    "stack_relevant_tags",
]
