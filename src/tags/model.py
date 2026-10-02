"""The unified NoöPunk tag model (issue #51 prototype).

One data structure represents every kind of capability or condition: attribute,
skill, gear, cyberware, relationship, condition, ideology, environment. An
**attribute tag is simply a tag with ``category="attribute"``** — there is no
separate attribute subsystem underneath this one, which is the issue's central
constraint ("Attributes are tags too").

Two rules govern what belongs here:

* **The four systems are canonical; the statistics inside them are not.**
  ``RULEBOOK.md`` §5 makes the division into Social / Physical / Psychic /
  Cybernetic canonical (Luhmann, with Cybernetic as NoöPunk's explicit extension),
  and says in the same breath that "the exact individual statistics contained within
  these four groups are **not yet finalized**". So this module pins the four systems
  and refuses to pin an attribute vocabulary.
* **Prototype vocabulary is fixture, not canon.** The issue proposes a candidate
  attribute list (FIT/REF/CHA/SOC/INT/WIL/PSY/CYB/NET). That is a *prototype*, so it
  lives in :data:`PROTOTYPE_ATTRIBUTES`, is marked non-canonical, and is used only
  with ``fixture:`` ids — the route ``docs/SIMULATION_ARCHITECTURE_SPEC.md`` §12
  predicted and ``src/simulation/engine.py`` established for Phase B. Writing it
  into ``data/rules/core.json`` would make a prototype into canon (AGENTS.md §1/§2).

Nothing here finalises the dice mechanic, tag ratings, advancement, or the attribute
count: the issue defers those, so this prototype takes them as explicit inputs or
reports them as unresolved.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class System(str, Enum):
    """The four canonical systems from RULEBOOK §5.

    Analytically distinct, causally entangled — §5 is explicit that the separation
    is an analytical device, not a claim that the systems are separate in the
    fiction. That is why cross-system actions are ordinary here rather than special
    cases.
    """

    PHYSICAL = "physical"
    SOCIAL = "social"
    PSYCHIC = "psychic"
    CYBERNETIC = "cybernetic"


#: Every system, in the rulebook's own order (§5 lists Social, Physical, Psychic,
#: Cybernetic; this follows the issue's Physical/Social/Psychic/Cybernetic grouping
#: for the prototype and does not change what the systems are).
SYSTEMS: tuple[System, ...] = (
    System.PHYSICAL,
    System.SOCIAL,
    System.PSYCHIC,
    System.CYBERNETIC,
)


class Category(str, Enum):
    """What kind of thing a tag describes.

    The issue's category list. The categories exist so applicability can be reasoned
    about reproducibly; they are **not** separate rules subsystems — everything here
    resolves through the same engine.
    """

    ATTRIBUTE = "attribute"
    SKILL = "skill"
    SPECIALIZATION = "specialization"
    BACKGROUND = "background"
    PROFESSION = "profession"
    GEAR = "gear"
    CYBERWARE = "cyberware"
    BIOMOD = "biological_modification"
    PSIONIC = "psionic_ability"
    RELATIONSHIP = "relationship"
    FACTION = "faction"
    REPUTATION = "reputation"
    IDEOLOGY = "ideology"
    CONDITION = "condition"
    INJURY = "injury"
    ENVIRONMENT = "environment"
    ADVANTAGE = "temporary_advantage"


class Source(str, Enum):
    """Where a tag comes from. ``character`` tags are intrinsic; the rest are
    situational and are what make a stack change from scene to scene."""

    CHARACTER = "character"
    EQUIPMENT = "equipment"
    SCENE = "scene"
    RELATIONSHIP = "relationship"
    WORLD = "world"


#: Normal-human attribute-tag range (issue §"Attribute tags"). Zero is ordinary
#: human baseline; beyond +3 is transhuman/posthuman.
HUMAN_ATTRIBUTE_MIN = -3
HUMAN_ATTRIBUTE_MAX = 3

#: Rating scale for non-attribute tags (issue §"Tags should have explicit strength").
TAG_RATING_MIN = 1
TAG_RATING_MAX = 3

#: Prototype attribute vocabulary proposed by the issue. **NOT CANON.** Marked so it
#: cannot be mistaken for the final four-group statistics, which RULEBOOK §5 leaves
#: unfinalised. Names are the issue's own prototype list, and they may change.
PROTOTYPE_ATTRIBUTES: tuple[tuple[str, System], ...] = (
    ("FIT", System.PHYSICAL),   # endurance / force / bodily robustness
    ("REF", System.PHYSICAL),   # coordination / speed / reaction
    ("CHA", System.SOCIAL),     # presence / persuasion / interpersonal force
    ("SOC", System.SOCIAL),     # social awareness / networks / status
    ("INT", System.PSYCHIC),    # cognition / reasoning / analysis
    ("WIL", System.PSYCHIC),    # self-control / resolve / psychic integrity
    ("PSY", System.PSYCHIC),    # psionic sensitivity, where applicable
    ("CYB", System.CYBERNETIC),  # direct interface / machine integration
    ("NET", System.CYBERNETIC),  # network / software / system competence
)

PROTOTYPE_ATTRIBUTE_SYSTEMS: dict[str, System] = dict(PROTOTYPE_ATTRIBUTES)

CANONICALITY_NOTE = (
    "Prototype vocabulary for issue #51. RULEBOOK.md §5 makes the four-system "
    "division canonical but explicitly leaves the statistics inside them "
    "unfinalized, so these names are non-canonical and may change."
)


class TagError(ValueError):
    """A tag violates the model."""


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


@dataclass(frozen=True, slots=True)
class Tag:
    """One unified tag.

    The same structure represents an attribute, a skill, a piece of gear, a
    condition, a relationship or an ideology. What differs is the metadata —
    ``category``, ``system``, ``scope``, ``source`` — not the machinery.
    """

    name: str
    rating: int
    category: Category = Category.SKILL
    system: System | None = None
    scope: tuple[str, ...] = ()
    source: Source = Source.CHARACTER
    #: Free-form provenance for provenance's sake; never consulted by resolution.
    provenance: str = ""

    def __post_init__(self) -> None:
        if not _text(self.name):
            raise TagError("a tag needs a name")
        if isinstance(self.rating, bool) or not isinstance(self.rating, int):
            raise TagError(f"tag {self.name!r} rating must be an integer")
        if self.category is Category.ATTRIBUTE:
            if self.system is None:
                raise TagError(
                    f"attribute tag {self.name!r} must name one of the four systems"
                )
            if not HUMAN_ATTRIBUTE_MIN <= self.rating <= HUMAN_ATTRIBUTE_MAX:
                # Beyond +3 is explicitly allowed for transhuman capability, so this
                # is checked by the caller for ordinary humans rather than forbidden.
                pass
        elif self.rating == 0:
            raise TagError(
                f"non-attribute tag {self.name!r} has no effect at rating 0; "
                "omit it instead of carrying a zero tag"
            )

    @property
    def is_attribute(self) -> bool:
        return self.category is Category.ATTRIBUTE

    @property
    def is_penalty(self) -> bool:
        return self.rating < 0

    def applies_to(self, *facets: str) -> bool:
        """Whether this tag is relevant to at least one named facet.

        Applicability is scope-based so it is reproducible: a tag applies when its
        declared scope intersects what the action asks for. A tag with no scope is
        only ever relevant by explicit inclusion, never by accident.
        """
        if not facets:
            return False
        wanted = {_text(facet).casefold() for facet in facets if _text(facet)}
        return bool(wanted & {s.casefold() for s in self.scope})

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "rating": self.rating,
            "category": self.category.value,
            "system": self.system.value if self.system else "",
            "scope": list(self.scope),
            "source": self.source.value,
            "provenance": self.provenance,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> Tag:
        """Rebuild a tag from serialised state (saves, agent memory, fixtures)."""
        raw_system = _text(payload.get("system"))
        return cls(
            name=_text(payload.get("name")),
            rating=int(payload.get("rating", 0)),
            category=Category(_text(payload.get("category")) or Category.SKILL.value),
            system=System(raw_system) if raw_system else None,
            scope=tuple(_text(item) for item in payload.get("scope", ()) if _text(item)),
            source=Source(_text(payload.get("source")) or Source.CHARACTER.value),
            provenance=_text(payload.get("provenance")),
        )


@dataclass(frozen=True, slots=True)
class SystemPresence:
    """Whether an entity meaningfully exists in each of the four systems.

    The issue is explicit that **an absent layer is not the same as a low score**:
    "Do not automatically assign a normal Psychic score to a non-conscious AI."
    So presence is modelled as its own fact rather than inferred from a number.

    ``None`` means present-but-unspecified; a value of ``False`` means the entity
    does not participate in that system at all, and any action placed there is
    unresolved rather than rolled at a penalty.
    """

    physical: bool = True
    social: bool = True
    psychic: bool = True
    cybernetic: bool = True

    def has(self, system: System) -> bool:
        return bool(getattr(self, system.value))

    def present(self) -> tuple[System, ...]:
        return tuple(system for system in SYSTEMS if self.has(system))

    def absent(self) -> tuple[System, ...]:
        return tuple(system for system in SYSTEMS if not self.has(system))

    @classmethod
    def all_present(cls) -> SystemPresence:
        return cls()

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any] | None) -> SystemPresence:
        if not payload:
            return cls()
        return cls(
            physical=bool(payload.get("physical", True)),
            social=bool(payload.get("social", True)),
            psychic=bool(payload.get("psychic", True)),
            cybernetic=bool(payload.get("cybernetic", True)),
        )

    def as_dict(self) -> dict[str, bool]:
        return {
            "physical": self.physical,
            "social": self.social,
            "psychic": self.psychic,
            "cybernetic": self.cybernetic,
        }


# --------------------------------------------------------------------------- #
# Sample entities -- the issue's "3-5 sample characters" plus absent-layer cases
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class Entity:
    """A character, NPC or agent. Used identically by human PCs and Concordia
    agents (design principle 10: "Simulation-compatible")."""

    entity_id: str
    name: str = ""
    tags: tuple[Tag, ...] = ()
    presence: SystemPresence = field(default_factory=SystemPresence.all_present)
    #: Narrative flags (beliefs, goals, loyalties, relationships) — the issue's
    #: Veil/Sprawl material. Deliberately NOT dice modifiers: they tell the GM and
    #: Concordia what situations matter, per "these are not necessarily added to
    #: every dice roll".
    flags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not _text(self.entity_id):
            raise TagError("an entity needs an entity_id")

    def attribute_tags(self) -> tuple[Tag, ...]:
        return tuple(tag for tag in self.tags if tag.is_attribute)

    def non_attribute_tags(self) -> tuple[Tag, ...]:
        return tuple(tag for tag in self.tags if not tag.is_attribute)

    def attributes(self) -> dict[str, int]:
        return {tag.name: tag.rating for tag in self.attribute_tags()}

    def tag(self, name: str) -> Tag | None:
        wanted = _text(name).casefold()
        for tag in self.tags:
            if tag.name.casefold() == wanted:
                return tag
        return None

    def as_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "presence": self.presence.as_dict(),
            "flags": list(self.flags),
            "tags": [tag.as_dict() for tag in self.tags],
        }


def attribute_tag(name: str, rating: int, *, system: System | None = None,
                  provenance: str = "") -> Tag:
    """Build an attribute tag, resolving its system from the prototype vocabulary.

    This is the "attributes are tags too" constructor: it produces an ordinary
    :class:`Tag` with ``category=attribute``, not a different kind of object.
    """
    resolved = system or PROTOTYPE_ATTRIBUTE_SYSTEMS.get(_text(name).upper())
    if resolved is None:
        raise TagError(
            f"unknown attribute tag {name!r}; the prototype vocabulary is "
            f"{sorted(PROTOTYPE_ATTRIBUTE_SYSTEMS)} (non-canonical, issue #51)"
        )
    return Tag(
        name=_text(name).upper(),
        rating=rating,
        category=Category.ATTRIBUTE,
        system=resolved,
        scope=(resolved.value,),
        source=Source.CHARACTER,
        provenance=provenance,
    )
