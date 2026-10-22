"""Data models for the standalone narrative RPG module."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


CANONICAL_ATTRIBUTES = (
    "Intelligence",
    "Awareness",
    "Reflexes",
    "Body",
    "Charisma",
    "Willpower",
    "Cybernetics",
)


class ResultTier(StrEnum):
    CRITICAL_SUCCESS = "critical_success"
    SUCCESS = "success"
    COSTLY_SUCCESS = "costly_success"
    FAILURE = "failure"
    CATASTROPHIC_FAILURE = "catastrophic_failure"


@dataclass
class Character:
    id: str
    name: str
    attributes: dict[str, int]
    skills: dict[str, int] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)
    aspects: set[str] = field(default_factory=set)
    conditions: set[str] = field(default_factory=set)
    consequences: list[str] = field(default_factory=list)
    stunts: set[str] = field(default_factory=set)
    resources: dict[str, int] = field(default_factory=dict)
    reputation: dict[str, int] = field(default_factory=dict)
    advancement: int = 0
    ego: dict[str, Any] = field(default_factory=dict)
    morph: dict[str, Any] = field(default_factory=dict)
    psyche: dict[str, Any] = field(default_factory=dict)
    cyber: dict[str, Any] = field(default_factory=dict)

    def attribute(self, name: str) -> int:
        return self.attributes.get(name, 0)

    def skill(self, name: str | None) -> int:
        return self.skills.get(name, 0) if name else 0


@dataclass(frozen=True)
class SkillCheck:
    attribute: str
    difficulty: int
    skill: str | None = None
    specialization_tags: frozenset[str] = frozenset()
    bonus_tags: frozenset[str] = frozenset()
    bonus_aspects: frozenset[str] = frozenset()
    situational_modifier: int = 0


@dataclass(frozen=True)
class CheckResult:
    tier: ResultTier
    dice: tuple[int, int, int, int]
    roll: int
    attribute: int
    skill: int
    tag_bonus: int
    aspect_bonus: int
    situational_modifier: int
    total: int
    difficulty: int
    margin: int


@dataclass
class Outcome:
    text: str = ""
    add_conditions: set[str] = field(default_factory=set)
    remove_conditions: set[str] = field(default_factory=set)
    add_consequences: list[str] = field(default_factory=list)
    set_flags: dict[str, Any] = field(default_factory=dict)
    add_information: set[str] = field(default_factory=set)
    relationship_changes: dict[str, int] = field(default_factory=dict)
    next_scene: str | None = None
    next_dialogue: str | None = None
    reset_session: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Interaction:
    id: str
    label: str
    description: str = ""
    check: SkillCheck | None = None
    outcomes: dict[ResultTier, Outcome] = field(default_factory=dict)
    automatic_outcome: Outcome | None = None
    requires_tags: set[str] = field(default_factory=set)
    blocked_by_tags: set[str] = field(default_factory=set)
    requires_aspects: set[str] = field(default_factory=set)
    requires_conditions: set[str] = field(default_factory=set)
    blocked_by_conditions: set[str] = field(default_factory=set)
    requires_flags: dict[str, Any] = field(default_factory=dict)
    repeatable: bool = False
    resolver: str = "4df"


@dataclass(frozen=True)
class Choice:
    interaction_id: str
    text: str


@dataclass
class DialogueNode:
    id: str
    speaker: str
    text: str
    choices: list[Choice] = field(default_factory=list)


@dataclass
class Scene:
    id: str
    title: str
    description: str
    location: str
    participants: list[str]
    interactions: dict[str, Interaction]
    dialogue: dict[str, DialogueNode] = field(default_factory=dict)
    opening_dialogue: str | None = None
    phase: str | None = None
    entry_flags: dict[str, Any] = field(default_factory=dict)
    exit_flags: dict[str, Any] = field(default_factory=dict)


@dataclass
class Scenario:
    id: str
    title: str
    entry_scene: str
    scenes: dict[str, Scene]
    terminal_scenes: set[str] = field(default_factory=set)
    locations: dict[str, "Location"] = field(default_factory=dict)


@dataclass(frozen=True)
class Location:
    """A named place with NPCs and investigation threads (Helsinki campaign frame).

    B's scenarios previously used free-text ``Scene.location`` strings. ``Location``
    makes places addressable entities so a campaign can declare them once and
    reference them by id. ``Scene.location`` remains a string for backward
    compatibility; it may hold a location id when the scenario declares locations.
    """

    id: str
    name: str
    description: str = ""
    district: str = ""
    npcs: list[str] = field(default_factory=list)
    threads: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RPGEvent:
    type: str
    payload: dict[str, Any]


@dataclass
class RPGState:
    current_scene: str
    current_character: str
    current_dialogue: str | None = None
    scene_flags: dict[str, Any] = field(default_factory=dict)
    campaign_flags: dict[str, Any] = field(default_factory=dict)
    conditions: set[str] = field(default_factory=set)
    consequences: list[str] = field(default_factory=list)
    known_information: set[str] = field(default_factory=set)
    completed_interactions: set[str] = field(default_factory=set)
    relationships: dict[str, int] = field(default_factory=dict)
    graph_effects: list[GraphEffect] = field(default_factory=list)


@dataclass(frozen=True)
class GraphEffect:
    """A portable request to change one edge or node in a domain graph."""

    domain: str
    operation: str
    source: str
    target: str | None = None
    key: str = "value"
    value: int | float | str | bool | None = None


@dataclass(frozen=True)
class InteractionResult:
    interaction_id: str
    outcome: Outcome
    check: CheckResult | None = None

