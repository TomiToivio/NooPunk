"""The generic tag resolver: one engine for every domain (issue #51 prototype).

```text
relevant tags -> sum -> resolution roll -> mechanical outcome -> narrative interpretation
```

There is **no privileged attribute layer**. The attribute tag is usually in the
stack because it is broad baseline capability, but mechanically it is one tag among
the others, which is the issue's "Attributes are tags too" constraint expressed in
code.

Design rules this module enforces rather than documents:

* **Only directly relevant tags count** (issue §"Tags stack"). A tag applies when
  its declared scope intersects the action's facets, so applicability is
  reproducible instead of depending on a GM's or LLM's mood.
* **Duplicate/synonymous tags do not stack**, and tags must be distinct *causes*
  (the issue's anti-abuse rules). Enforced two ways: identical ``(name, category)``
  collapses to the strongest, and at most one tag per ``category`` may contribute as
  a "cause" — so "Pistol +2" and "Handgun +2" cannot both pay out.
* **Absent systems do not roll.** An entity with no Psychic layer gets an explicit
  UNRESOLVED for a psychic action, not a −3 or a zero (issue: "an absent layer is
  not the same thing as a very low attribute").
* **Python resolves; the LLM does not.** Dice are rolled here or injected by a
  deterministic caller. Nothing in the stack comes from model output.

Deliberately **not** decided here, because the issue defers them: the exact dice
mechanic, whether negative tags subtract or raise difficulty, and the final cap. The
dice come from the shared ``rules`` layer (2d6 canon, RULEBOOK §4) so this prototype
does not fork the engine, and the cap is a prototype parameter, not canon.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from rules import AttributeSet, CheckResult, resolve_check

from .model import Category, Entity, System, SystemPresence, Tag

#: Prototype default cap on how many tags may contribute. The issue lists the cap as
#: an open question ("Define a reasonable cap if testing shows tag inflation"), so
#: this is a *prototype* value, not canon, and is injectable.
STACK_CAP_DEFAULT = 6

#: The prototype difficulty ladder's middle rung, used only by sample fixtures. The
#: ladder itself lives in the shared canon (RULEBOOK §4); this constant exists so the
#: fixtures do not scatter magic numbers that look like canon.
SAMPLE_DIFFICULTY = 10


class StackingError(ValueError):
    """The stack cannot be built as requested."""


class Outcome(str, Enum):
    RESOLVED = "RESOLVED"
    #: The action sits in a system this entity does not participate in.
    UNRESOLVED_ABSENT_SYSTEM = "unresolved_absent_system"
    #: The action names no facets, so no tag can be judged relevant.
    UNRESOLVED_NO_FACETS = "unresolved_no_facets"
    #: An attribute tag the stack depends on does not exist on the entity.
    UNRESOLVED_MISSING_ATTRIBUTE = "unresolved_missing_attribute"


@dataclass(frozen=True, slots=True)
class AppliedTag:
    """One tag that contributed to a stack, with why it counted."""

    tag: Tag
    counted: bool
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {**self.tag.as_dict(), "counted": self.counted, "reason": self.reason}


@dataclass(frozen=True, slots=True)
class Stack:
    """The assembled modifier stack for one action.

    ``total`` is the sum of the counted tags. ``excluded`` records every tag that was
    *not* counted and why, which is what makes the number auditable rather than
    merely reported — the issue's "mechanically transparent" requirement.
    """

    action: str
    system: System | None
    counted: tuple[Tag, ...] = ()
    excluded: tuple[AppliedTag, ...] = ()
    total: int = 0
    cap: int = STACK_CAP_DEFAULT

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "system": self.system.value if self.system else "",
            "total": self.total,
            "counted": [
                {"name": tag.name, "rating": tag.rating, "category": tag.category.value}
                for tag in self.counted
            ],
            "excluded": [item.as_dict() for item in self.excluded],
            "cap": self.cap,
        }

    def explanation(self) -> str:
        parts = [f"{tag.name} {tag.rating:+d}" for tag in self.counted]
        return " ".join(parts) + f" = {self.total:+d}" if parts else f"no tags = {self.total:+d}"


@dataclass(frozen=True, slots=True)
class Resolution:
    """The mechanical result, ready for the narrative layer to interpret."""

    outcome: Outcome
    action: str
    stack: Stack
    check: CheckResult | None = None
    reason: str = ""
    narrative_hint: str = ""

    @property
    def resolved(self) -> bool:
        return self.outcome is Outcome.RESOLVED

    @property
    def success(self) -> bool | None:
        return self.check.success if self.check else None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "outcome": self.outcome.value,
            "action": self.action,
            "stack": self.stack.as_dict(),
            "reason": self.reason,
        }
        if self.check is not None:
            payload["check"] = {
                "dice_total": self.check.dice_total,
                "modifier_total": self.check.attribute_modifier,
                "target": self.check.target,
                "total": self.check.total,
                "success": self.check.success,
            }
        return payload


# --------------------------------------------------------------------------- #
# Stacking
# --------------------------------------------------------------------------- #

def build_stack(
    entity: Entity,
    *,
    action: str,
    facets: Sequence[str],
    system: System | None = None,
    attribute: str = "",
    include_categories: Iterable[Category] | None = None,
    exclude_names: Iterable[str] = (),
    cap: int = STACK_CAP_DEFAULT,
) -> Stack:
    """Assemble the modifier stack for one action.

    Relevance is scope-intersection for ordinary tags and system-match for attribute
    tags (see the comment in the body), so the same entity yields a different stack
    for a different action without the caller re-deciding what "counts" each time.

    ``attribute`` nominates the single attribute tag the action depends on, following
    RULEBOOK §4's rule that the GM selects the attribute that fits the action.

    Anti-inflation, applied in this order:
    1. a tag must be relevant (facet intersection, or system match for attributes);
    2. ``(name, category)`` duplicates collapse to the strongest;
    3. at most one tag per category may contribute, so synonymous causes do not pay
       twice (the issue's "duplicate/synonymous tags do not stack");
    4. the total number of counted tags is capped.
    """
    wanted = tuple(facet for facet in (_clean(f) for f in facets) if facet)
    if not wanted:
        return Stack(action=action, system=system, cap=cap)
    nominated_attribute = attribute

    allowed = {c for c in include_categories} if include_categories is not None else None
    blocked = {_clean(name).casefold() for name in exclude_names if _clean(name)}
    noted: list[AppliedTag] = []

    # 1. relevance + exclusions
    #
    # Relevance is scope intersection, with one deliberate exception for attribute
    # tags. An attribute tag's scope is its *system* ("physical", "social", ...)
    # because that is what it describes, not the action facets ("ranged", "combat").
    # Requiring facet intersection would therefore exclude every attribute tag from
    # every stack -- which is exactly what this prototype must not do, since the
    # issue's rule is that "the attribute tag is simply one of the tags in the stack".
    #
    # So an attribute tag is relevant when its system matches the action's system.
    # `nominated_attribute` additionally pins the single attribute the caller chose,
    # because RULEBOOK §4 says the GM picks the attribute that fits the action and an
    # action rarely depends on all attributes of a system at once.
    candidates: list[Tag] = []
    nominated = _clean(nominated_attribute).upper()
    for tag in entity.tags:
        if tag.name.casefold() in blocked:
            noted.append(AppliedTag(tag, False, "explicitly excluded"))
            continue
        if allowed is not None and tag.category not in allowed:
            noted.append(AppliedTag(tag, False, f"category {tag.category.value} not in scope"))
            continue
        if tag.is_attribute:
            if system is not None and tag.system is not system:
                tag_system = tag.system.value if tag.system else "none"
                noted.append(
                    AppliedTag(tag, False, f"attribute for the {tag_system} system, not {system.value}")
                )
                continue
            if nominated and tag.name.upper() != nominated:
                noted.append(AppliedTag(tag, False, "not the attribute the action nominates"))
                continue
            candidates.append(tag)
            continue
        if not tag.applies_to(*wanted):
            noted.append(AppliedTag(tag, False, "scope does not intersect the action"))
            continue
        candidates.append(tag)

    # 2. identical name+category collapses to the strongest
    best_by_name: dict[tuple[str, Category], Tag] = {}
    for tag in candidates:
        key = (tag.name.casefold(), tag.category)
        current = best_by_name.get(key)
        if current is None:
            best_by_name[key] = tag
        else:
            winner = tag if abs(tag.rating) > abs(current.rating) else current
            loser = current if winner is tag else tag
            best_by_name[key] = winner
            noted.append(AppliedTag(loser, False, "duplicate name; strongest kept"))

    # 3. one cause per category -- the anti-synonym rule
    by_category: dict[Category, Tag] = {}
    for tag in sorted(best_by_name.values(), key=lambda t: (-abs(t.rating), t.name)):
        if tag.category in by_category:
            noted.append(
                AppliedTag(tag, False, f"another {tag.category.value} tag already contributes")
            )
            continue
        by_category[tag.category] = tag

    # 4. cap
    ordered = sorted(by_category.values(), key=lambda t: (-abs(t.rating), t.name))
    counted = tuple(ordered[: max(0, cap)])
    for tag in ordered[len(counted):]:
        noted.append(AppliedTag(tag, False, f"stack cap of {cap} reached"))

    return Stack(
        action=action,
        system=system,
        counted=counted,
        excluded=tuple(noted),
        total=sum(tag.rating for tag in counted),
        cap=cap,
    )


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


# --------------------------------------------------------------------------- #
# Resolution
# --------------------------------------------------------------------------- #

def resolve_action(
    entity: Entity,
    *,
    action: str,
    facets: Sequence[str],
    system: System | None = None,
    attribute: str = "",
    difficulty: int | None = None,
    include_categories: Iterable[Category] | None = None,
    exclude_names: Iterable[str] = (),
    cap: int = STACK_CAP_DEFAULT,
    dice_total: int | None = None,
    rng: Any = None,
) -> Resolution:
    """Resolve one tagged action with the shared 2d6 engine.

    ``facets`` names what the action is about ("network_access", "security", ...).
    ``difficulty`` is required when the caller has one; when it is absent the action
    is reported UNRESOLVED rather than given a default, because assigning difficulty
    is a tabletop decision (AGENTS.md §4).

    ``dice_total`` is for deterministic callers (replay, tests). The LLM never
    supplies it.
    """
    if system is not None and not entity.presence.has(system):
        return Resolution(
            outcome=Outcome.UNRESOLVED_ABSENT_SYSTEM,
            action=action,
            stack=Stack(action=action, system=system, cap=cap),
            reason=(
                f"entity {entity.entity_id!r} has no {system.value} system; an absent "
                "layer is not a low score, so this action is not rollable here"
            ),
        )

    cleaned_facets = tuple(facet for facet in (_clean(f) for f in facets) if facet)
    if not cleaned_facets:
        return Resolution(
            outcome=Outcome.UNRESOLVED_NO_FACETS,
            action=action,
            stack=Stack(action=action, system=system, cap=cap),
            reason="the action names no facets, so no tag can be judged relevant",
        )

    stack = build_stack(
        entity,
        action=action,
        facets=cleaned_facets,
        system=system,
        attribute=attribute,
        include_categories=include_categories,
        exclude_names=exclude_names,
        cap=cap,
    )

    if difficulty is None:
        return Resolution(
            outcome=Outcome.UNRESOLVED_MISSING_ATTRIBUTE,
            action=action,
            stack=stack,
            reason=(
                "no difficulty was supplied; assigning one is a tabletop decision, "
                "so this prototype does not default it"
            ),
        )

    # The stack total is the modifier; the shared rules layer owns the dice and the
    # ladder, so the prototype cannot fork the resolution engine.
    check = resolve_check(
        attribute_modifier=stack.total,
        target=int(difficulty),
        dice_total=dice_total,
        rng=rng,
    )
    return Resolution(
        outcome=Outcome.RESOLVED,
        action=action,
        stack=stack,
        check=check,
        narrative_hint=(
            "the mechanical result is fixed; what it means for the character is the "
            "narrative layer's job, and it may not change this number"
        ),
    )


# --------------------------------------------------------------------------- #
# Sample entities (the issue's "3-5 sample characters")
# --------------------------------------------------------------------------- #

def sample_entities() -> dict[str, Entity]:
    """Five synthetic characters plus the absent-layer cases the issue requires.

    All ids use the ``fixture:`` prefix, which ``src/simulation/engine.py``
    established as deliberately non-canonical. Nothing here is setting material: the
    names and tags are placeholders chosen to exercise the engine, not lore.
    """
    def attribute_set(**values: int) -> tuple[Tag, ...]:
        from .model import attribute_tag

        return tuple(attribute_tag(name, rating) for name, rating in values.items())

    return {
        # A street operator: physical and cybernetic, weak socially.
        "fixture:runner": Entity(
            entity_id="fixture:runner",
            name="Runner (prototype)",
            tags=(
                *attribute_set(FIT=1, REF=2, CHA=-1, SOC=0, INT=1, WIL=1, PSY=0, CYB=1, NET=1),
                Tag("Pistol", 2, Category.SKILL, System.PHYSICAL, ("combat", "ranged")),
                Tag("Parkour", 2, Category.SKILL, System.PHYSICAL, ("movement", "urban")),
                Tag("Smartlink", 1, Category.CYBERWARE, System.CYBERNETIC, ("ranged", "aim")),
                Tag("Wanted by a corporation", -2, Category.REPUTATION, System.SOCIAL,
                    ("legal", "social_risk")),
            ),
            flags=("Belief: corporate debts should be uncollectable",),
        ),
        # A negotiator: social and psychic, poor physically.
        "fixture:negotiator": Entity(
            entity_id="fixture:negotiator",
            name="Negotiator (prototype)",
            tags=(
                *attribute_set(FIT=-1, REF=0, CHA=2, SOC=2, INT=1, WIL=2, PSY=1, CYB=0, NET=0),
                Tag("Union organizer", 2, Category.PROFESSION, System.SOCIAL,
                    ("negotiation", "labour", "persuasion")),
                Tag("Corporate etiquette", 1, Category.SKILL, System.SOCIAL,
                    ("negotiation", "corporate")),
                Tag("Meditative discipline", 1, Category.SKILL, System.PSYCHIC,
                    ("resolve", "concentration")),
            ),
            flags=("Loyalty: Mesh Commune +2", "Belief: AGIs deserve political personhood"),
        ),
        # A researcher: cognition, weak social presence.
        "fixture:researcher": Entity(
            entity_id="fixture:researcher",
            name="Researcher (prototype)",
            tags=(
                *attribute_set(FIT=0, REF=0, CHA=-1, SOC=1, INT=3, WIL=1, PSY=1, CYB=0, NET=1),
                Tag("Investigative journalist", 2, Category.PROFESSION, System.SOCIAL,
                    ("investigation", "research", "interview")),
                Tag("Pattern recognition", 2, Category.SKILL, System.PSYCHIC,
                    ("investigation", "analysis")),
                Tag("Old colleague", 1, Category.RELATIONSHIP, System.SOCIAL,
                    ("interview", "trust")),
            ),
            flags=("Goal: expose a cognition-research programme",),
        ),
        # Heavy cyborg: strongly cybernetic, socially compromised.
        "fixture:cyborg": Entity(
            entity_id="fixture:cyborg",
            name="Cyborg (prototype)",
            tags=(
                *attribute_set(FIT=2, REF=1, CHA=-2, SOC=-1, INT=0, WIL=1, PSY=-1, CYB=3, NET=2),
                Tag("Synthetic muscles", 2, Category.BIOMOD, System.PHYSICAL, ("force", "combat")),
                Tag("Neural interface", 2, Category.CYBERWARE, System.CYBERNETIC,
                    ("network_access", "interface")),
                Tag("Exploit development", 3, Category.SKILL, System.CYBERNETIC,
                    ("network_access", "security", "hacking")),
            ),
        ),
        # Psionic: strong psychic, no cybernetic competence.
        "fixture:psion": Entity(
            entity_id="fixture:psion",
            name="Psion (prototype)",
            tags=(
                *attribute_set(FIT=0, REF=0, CHA=1, SOC=0, INT=1, WIL=2, PSY=3, CYB=-1, NET=-1),
                Tag("Telepathy", 2, Category.PSIONIC, System.PSYCHIC,
                    ("mind", "detection", "influence")),
                Tag("Noösphere attunement", 1, Category.SKILL, System.PSYCHIC,
                    ("mind", "collective")),
            ),
        ),
        # --- absent-layer cases the issue requires (item 15) --- #

        # Non-conscious AI: no Psychic layer at all.
        "fixture:utility-ai": Entity(
            entity_id="fixture:utility-ai",
            name="Utility AI (prototype, non-conscious)",
            tags=(
                Tag("CYB", 2, Category.ATTRIBUTE, System.CYBERNETIC, ("cybernetic",)),
                Tag("NET", 3, Category.ATTRIBUTE, System.CYBERNETIC, ("cybernetic",)),
                Tag("Protocol analysis", 2, Category.SKILL, System.CYBERNETIC,
                    ("network_access", "analysis")),
            ),
            presence=SystemPresence(physical=False, social=True, psychic=False, cybernetic=True),
        ),
        # Disembodied noetic being: no Physical layer.
        "fixture:noetic": Entity(
            entity_id="fixture:noetic",
            name="Noetic entity (prototype)",
            tags=(
                Tag("PSY", 3, Category.ATTRIBUTE, System.PSYCHIC, ("psychic",)),
                Tag("WIL", 2, Category.ATTRIBUTE, System.PSYCHIC, ("psychic",)),
                Tag("Pattern sensing", 2, Category.SKILL, System.PSYCHIC, ("mind", "detection")),
            ),
            presence=SystemPresence(physical=False, social=True, psychic=True, cybernetic=False),
        ),
        # VR agent: social and cybernetic, no direct physical presence in the scene.
        "fixture:vr-agent": Entity(
            entity_id="fixture:vr-agent",
            name="VR agent (prototype)",
            tags=(
                Tag("CHA", 1, Category.ATTRIBUTE, System.SOCIAL, ("social",)),
                Tag("CYB", 2, Category.ATTRIBUTE, System.CYBERNETIC, ("cybernetic",)),
                Tag("Platform manipulation", 2, Category.SKILL, System.CYBERNETIC,
                    ("network_access", "influence")),
            ),
            presence=SystemPresence(physical=False, social=True, psychic=False, cybernetic=True),
        ),
    }


def attribute_set_for(entity: Entity) -> AttributeSet:
    """Adapt an entity's attribute tags to the shared ``AttributeSet``.

    This is the seam that keeps "attributes are tags" compatible with the shared
    rules layer without giving attributes a privileged subsystem: the attributes are
    read *out of* the tag list, and anything the shared layer needs that the entity
    does not have is filled with 0 only where the entity participates in that system.
    """
    from .model import PROTOTYPE_ATTRIBUTE_SYSTEMS

    values = {name: 0 for name in PROTOTYPE_ATTRIBUTE_SYSTEMS}
    for tag in entity.attribute_tags():
        values[tag.name] = tag.rating
    return AttributeSet(values)
