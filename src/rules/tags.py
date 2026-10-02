"""The unified tag model for NoöPunk (issue #51).

> **Status: prototype. This module defines no canon.**
>
> Issue #51 states the core design constraint — **attributes are tags too** — and
> asks for a prototype, not for final rules. `RULEBOOK.md` §5 says the individual
> statistics inside the four groups are **not yet finalized**, and #51 says "do not
> lock the final attribute names or exact count yet". So this module implements the
> *mechanism* and marks every prototype value as such.

The important structural rule from #51 principle 2 is **one tag engine**: an
attribute tag, a skill tag, a gear tag and a condition tag are the same kind of
object, differing in metadata rather than living in separate subsystems. This module
enforces that — there is exactly one :class:`Tag` type.

Composition with the canonical resolver
---------------------------------------
#51 principle 9 is *deterministic core, generative surface*, and the canonical
resolution rule is already fixed by `RULEBOOK.md` §4 and implemented in
`src/rules/core.py`:

    total = 2d6 + skill level + attribute modifier  vs  difficulty

Tags must therefore **feed** that check, not replace it. :func:`compose_check` maps a
stack of tags onto `rules.resolve_check` — the attribute tag supplies the attribute
modifier, the primary skill tag supplies the skill level, and every other relevant
tag becomes an extra modifier — so there is one engine and one dice mechanic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

# --------------------------------------------------------------------------- #
# Prototype vocabulary — NOT canon
# --------------------------------------------------------------------------- #
#: The four Luhmannian groups named as canonical by RULEBOOK.md §5.
#:
#: The *groups* are author-specified. What sits inside them is not, so this list is
#: the canonical part and everything below it is prototype.
FOUR_SYSTEMS = ("physical", "social", "psychic", "cybernetic")

#: **Prototype vocabulary — not canon.** Issue #51 proposes these as a starting
#: point and explicitly says not to lock names or count yet. `RULEBOOK.md` §5 keeps
#: the six legacy attributes "temporarily" while the four-group architecture is
#: redesigned, so these six are reused here purely so the prototype runs against
#: the existing implementation rather than inventing a seventh stat.
PROTOTYPE_ATTRIBUTE_TAGS: tuple[str, ...] = ("FIT", "REF", "INT", "CHA", "CYB", "PSY")

#: Which canonical four-group system each prototype attribute belongs to.
#: **Prototype mapping**, taken from #51's own worked example.
PROTOTYPE_ATTRIBUTE_SYSTEMS: Mapping[str, str] = {
    "FIT": "physical",
    "REF": "physical",
    "INT": "psychic",
    "CHA": "social",
    "CYB": "cybernetic",
    "PSY": "psychic",
}

#: Ordinary-human attribute-tag range (RULEBOOK.md §5.2, and #51 principle 3).
#: Values beyond this are reserved for genuinely transhuman capability.
HUMAN_ATTRIBUTE_MIN = -3
HUMAN_ATTRIBUTE_MAX = 3

#: **Prototype scale for non-attribute tags** (#51 "tags should have explicit
#: strength"). The issue lists 1-3 magnitude for other tags and asks whether that
#: should always hold — that question stays open, so the bounds are here and pinned
#: by a test rather than assumed silently.
TAG_RATING_MIN = -3
TAG_RATING_MAX = 3

#: Prototype: the largest number of tags that may contribute to one check.
#:
#: #51 lists "maximum number of tags that may contribute to one roll" as an open
#: question. A cap exists because unlimited stacking is the documented tag-inflation
#: risk; the *value* is a prototype placeholder, not a decision.
PROTOTYPE_MAX_CONTRIBUTING_TAGS = 5

#: Attribute tags are always present and broad; every other category is situational.
ATTRIBUTE_CATEGORY = "attribute"


# --------------------------------------------------------------------------- #
# System presence (RULEBOOK.md §5.2)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class SystemPresence:
    """Which of the four systems an entity meaningfully participates in.

    ``RULEBOOK.md`` §5.2 is explicit that a system can be **absent / not applicable**
    and that "absence is not the same as a low score": a physically present but frail
    entity may hold a Physical attribute of -3, while a disembodied/noetic entity has
    **no meaningful Physical participation at all**, and a non-conscious AI has **no
    meaningful Psychic participation**.

    Without this, the only thing an entity could express is a very low rating, which
    collapses those two very different statements into one. Presence is therefore a
    fact about the entity, not a tag rating and not a modifier:

    * an absent system is **not rollable**, and the resolver says so explicitly
      rather than resolving at a penalty (a "-3 roll" would assert a capability the
      entity does not have);
    * it does **not** force an attribute value for a system the entity lacks.

    Default is full participation in all four systems, so an ordinary character is
    unaffected and older call sites keep working.
    """

    participation: Mapping[str, bool] = field(
        default_factory=lambda: {system: True for system in FOUR_SYSTEMS}
    )

    def __post_init__(self) -> None:
        unknown = set(self.participation) - set(FOUR_SYSTEMS)
        if unknown:
            raise TagError(
                f"unknown system(s) {sorted(unknown)}; the four canonical groups are "
                f"{list(FOUR_SYSTEMS)}"
            )
        for system, value in self.participation.items():
            if not isinstance(value, bool):
                raise TagError(f"presence for {system!r} must be a bool, got {value!r}")

    def has(self, system: str) -> bool:
        """Whether the entity meaningfully participates in ``system``."""
        wanted = _text(system).casefold()
        if wanted not in FOUR_SYSTEMS:
            raise TagError(f"unknown system {system!r}")
        return bool(self.participation.get(wanted, True))

    def absent(self) -> tuple[str, ...]:
        """The systems this entity does not participate in, in canonical order."""
        return tuple(system for system in FOUR_SYSTEMS if not self.has(system))

    def as_dict(self) -> dict[str, bool]:
        return {system: self.has(system) for system in FOUR_SYSTEMS}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> SystemPresence:
        return cls({system: bool(payload.get(system, True)) for system in FOUR_SYSTEMS})

    @classmethod
    def absent_systems(cls, *systems: str) -> SystemPresence:
        """Presence with the named systems absent and the rest participating.

        Convenience for the cases §5.2 names: ``SystemPresence.absent_systems("psychic")``
        is a non-conscious AI, ``absent_systems("physical")`` is a noetic entity.
        """
        missing = {_text(system).casefold() for system in systems}
        unknown = missing - set(FOUR_SYSTEMS)
        if unknown:
            raise TagError(f"unknown system(s) {sorted(unknown)}")
        return cls({system: system not in missing for system in FOUR_SYSTEMS})


#: How an action resolved, including the case where it could not.
RESOLVED = "resolved"
#: The action sits in a system this entity does not participate in (RULEBOOK §5.2).
UNRESOLVED_ABSENT_SYSTEM = "unresolved_absent_system"


class TagError(ValueError):
    """A tag is malformed, or a tag stack violates the prototype contract."""


# --------------------------------------------------------------------------- #
# The single tag type
# --------------------------------------------------------------------------- #

def _text(raw: Any) -> str:
    if raw is None:
        return ""
    text = str(raw).strip()
    return "" if text.lower() in {"nan", "none", "<na>"} else text


@dataclass(frozen=True, slots=True)
class Tag:
    """One tag. Attributes are tags with ``category="attribute"`` (#51).

    ``scope`` is what makes applicability checkable rather than a matter of mood:
    #51 principle 6 is "tags are defined enough for code", and principle 7 keeps
    fiction meaningful. A tag applies when the action's scopes intersect its own.
    """

    name: str
    rating: int
    system: str
    category: str = "skill"
    scope: tuple[str, ...] = ()
    source: str = "character"

    def __post_init__(self) -> None:
        if not _text(self.name):
            raise TagError("tag name must be non-empty")
        if not isinstance(self.rating, int) or isinstance(self.rating, bool):
            raise TagError(f"tag rating must be an int, got {self.rating!r}")
        if self.system not in FOUR_SYSTEMS:
            raise TagError(
                f"unknown system {self.system!r}; the four canonical groups are "
                f"{list(FOUR_SYSTEMS)}"
            )
        if self.category == ATTRIBUTE_CATEGORY:
            if not (HUMAN_ATTRIBUTE_MIN <= self.rating <= HUMAN_ATTRIBUTE_MAX):
                # Transhuman values are allowed, but they must say so explicitly:
                # silently exceeding the human range would make "ordinary human
                # -3..+3" unverifiable.
                raise TagError(
                    f"attribute tag {self.name!r} rating {self.rating} is outside the "
                    f"ordinary-human range {HUMAN_ATTRIBUTE_MIN}..{HUMAN_ATTRIBUTE_MAX}; "
                    "pass transhuman=True for genuinely posthuman capability"
                )
        else:
            if not (TAG_RATING_MIN <= self.rating <= TAG_RATING_MAX):
                raise TagError(
                    f"tag rating {self.rating} outside prototype range "
                    f"{TAG_RATING_MIN}..{TAG_RATING_MAX}"
                )
        if self.rating == 0 and self.category == ATTRIBUTE_CATEGORY:
            # 0 is the ordinary-human baseline and a legitimate attribute value.
            return
        object.__setattr__(self, "scope", tuple(_text(s).casefold() for s in self.scope))

    @property
    def is_attribute(self) -> bool:
        return self.category == ATTRIBUTE_CATEGORY

    def applies_to(self, action_scopes: Iterable[str]) -> bool:
        """Whether a *situational* tag is fictionally and mechanically relevant.

        Attribute tags are **always applicable**: #51 describes them as "always
        present; broad rather than situational", and which attribute applies is the
        caller's choice of ``attribute=``, not a scope match. Filtering them here was
        a bug — action scopes are things like ``combat``, not the four system names,
        so a valid attribute tag was rejected and the check could not resolve.

        A situational tag applies only when a scope matches, which is what stops a
        Pistol tag from helping a negotiation.
        """
        if self.is_attribute:
            return True
        wanted = {_text(s).casefold() for s in action_scopes if _text(s)}
        if not self.scope:
            # A scoped tag with no scope cannot be checked, so it never applies by
            # default rather than applying to everything.
            return False
        return bool(wanted & set(self.scope))


@dataclass(frozen=True, slots=True)
class TranshumanTag(Tag):
    """An attribute tag beyond the ordinary-human range.

    Separate on purpose: #51 asks how transhuman capability should interact with the
    §5.2 human ceiling, and making it a distinct type means the range stays
    verifiable instead of being quietly widened.
    """

    def __post_init__(self) -> None:
        object.__setattr__(self, "category", ATTRIBUTE_CATEGORY)
        if not isinstance(self.rating, int) or isinstance(self.rating, bool):
            raise TagError(f"tag rating must be an int, got {self.rating!r}")
        if abs(self.rating) <= HUMAN_ATTRIBUTE_MAX:
            raise TagError(
                f"{self.name!r} is within the ordinary-human range; use Tag, not "
                "TranshumanTag"
            )
        if self.system not in FOUR_SYSTEMS:
            raise TagError(f"unknown system {self.system!r}")


def transhuman_attribute(
    name: str, rating: int, system: str, *, source: str = "character"
) -> TranshumanTag:
    return TranshumanTag(
        name=name, rating=rating, system=system, category=ATTRIBUTE_CATEGORY,
        scope=(), source=source,
    )


# --------------------------------------------------------------------------- #
# Stacks
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class TagStack:
    """The tags that contributed to one check, with the reasons they were admitted.

    Keeping the rejected tags and the reason is deliberate: #51 principle 6 wants
    tag applicability to be checkable, and a hidden rejection is indistinguishable
    from a tag that was never considered.
    """

    contributed: tuple[Tag, ...]
    rejected: tuple[tuple[Tag, str], ...] = ()
    capped: tuple[Tag, ...] = ()

    @property
    def total(self) -> int:
        return sum(tag.rating for tag in self.contributed)

    def explain(self) -> list[str]:
        """Human-readable audit line per tag, for the debug log and for a GM."""
        lines = [f"{tag.rating:+d}  {tag.name} ({tag.category}/{tag.system})" for tag in self.contributed]
        for tag, reason in self.rejected:
            lines.append(f" ---  {tag.name} rejected: {reason}")
        for tag in self.capped:
            lines.append(f" ---  {tag.name} dropped: at the contributing-tag cap")
        return lines


def _key(tag: Tag) -> str:
    """Identity for duplicate detection: same name and system is the same cause."""
    return f"{tag.system}|{tag.name.casefold()}"


def build_stack(
    tags: Sequence[Tag],
    *,
    action_scopes: Iterable[str] = (),
    max_contributing: int = PROTOTYPE_MAX_CONTRIBUTING_TAGS,
) -> TagStack:
    """Resolve which tags contribute, in a deterministic order.

    Anti-abuse rules from #51, all enforced here rather than left to the caller:

    - only directly relevant tags count (:meth:`Tag.applies_to`);
    - **duplicate or synonymous tags do not stack** — same name + system is one
      cause, whatever its source, so "Pistol +2" from a skill and "Pistol +2" from
      gear cannot both apply;
    - a cap on how many tags contribute.

    Ordering is by descending absolute rating then name, so the cap drops the least
    significant tag deterministically instead of depending on input order.
    """
    # Attribute tags are the baseline and are never scope-filtered or capped; only
    # situational tags compete for contributing slots.
    attributes = [tag for tag in tags if tag.is_attribute]
    situational = [tag for tag in tags if not tag.is_attribute]

    applicable = [tag for tag in situational if tag.applies_to(action_scopes)]
    irrelevant = [tag for tag in situational if not tag.applies_to(action_scopes)]

    best: dict[str, Tag] = {}
    duplicates: list[tuple[Tag, str]] = []
    for tag in applicable:
        key = _key(tag)
        existing = best.get(key)
        if existing is None:
            best[key] = tag
        else:
            # Keep the stronger of the two; record the weaker as rejected so the
            # stack is auditable.
            if abs(tag.rating) > abs(existing.rating):
                duplicates.append((existing, f"duplicate of {tag.name!r}, weaker"))
                best[key] = tag
            else:
                duplicates.append((tag, f"duplicate of {existing.name!r}, not additive"))

    ordered = sorted(best.values(), key=lambda t: (-abs(t.rating), t.name.casefold()))
    contributed = tuple(attributes) + tuple(ordered[:max_contributing])
    capped = tuple(ordered[max_contributing:])

    rejected = [(tag, "not relevant to the action") for tag in irrelevant] + duplicates
    return TagStack(contributed=contributed, rejected=tuple(rejected), capped=capped)


# --------------------------------------------------------------------------- #
# Composition with the canonical resolver
# --------------------------------------------------------------------------- #

def attribute_modifier(tags: Sequence[Tag], attribute: str) -> int:
    """The attribute tag's rating, for the canonical check's attribute slot."""
    wanted = _text(attribute)
    for tag in tags:
        if tag.is_attribute and tag.name.casefold() == wanted.casefold():
            return tag.rating
    raise TagError(
        f"no attribute tag {attribute!r} in the stack; the canonical check needs a "
        "relevant attribute modifier (RULEBOOK §4)"
    )


@dataclass(frozen=True, slots=True)
class TagCheckInput:
    """The values the canonical resolver needs, derived from a tag stack.

    ``outcome`` is ``"resolved"`` for an ordinary check and
    ``"unresolved_absent_system"`` when the entity does not participate in the
    action's system (RULEBOOK §5.2); in the latter case ``absent_system`` names it and
    the numeric fields are zeroed because nothing was rolled.
    """

    attribute_modifier: int
    skill_level: int
    extra_modifiers: tuple[int, ...]
    stack: TagStack
    outcome: str = RESOLVED
    absent_system: str = ""

    @property
    def resolved(self) -> bool:
        return self.outcome == RESOLVED

    def explain(self) -> list[str]:
        return [
            f"attribute modifier: {self.attribute_modifier:+d}",
            f"skill level:        {self.skill_level:+d}",
            f"other tags:         {sum(self.extra_modifiers):+d} "
            f"({len(self.extra_modifiers)} tag(s))",
            *self.stack.explain(),
        ]


def compose_check(
    tags: Sequence[Tag],
    *,
    attribute: str,
    skill: str = "",
    action_scopes: Iterable[str] = (),
    max_contributing: int = PROTOTYPE_MAX_CONTRIBUTING_TAGS,
) -> TagCheckInput:
    """Map a tag stack onto the canonical `rules.resolve_check` parameters.

    This is the whole point of the prototype: **no new dice engine**. #51 principle 2
    is one tag engine and principle 9 is a deterministic core, so tags are converted
    into the arguments `src/rules/core.py` already accepts:

    - the named attribute tag becomes ``attribute_modifier``;
    - the skill tag matching ``skill`` becomes ``skill_level`` (its rating clamped
      to the canonical 0..4 scale, because a tag's magnitude and a skill level are
      not the same scale — see the note below);
    - every remaining contributed tag becomes an entry in ``extra_modifiers``.

    Note on scales: the canonical skill level is 0..4 (`RULEBOOK` §5.3) while a
    prototype tag rating is -3..+3. Clamping is therefore a **prototype bridge**, and
    the mismatch is recorded as an open question rather than hidden.
    """
    stack = build_stack(tags, action_scopes=action_scopes, max_contributing=max_contributing)
    modifier = attribute_modifier(stack.contributed, attribute)

    skill_level = 0
    extras: list[int] = []
    skill_used = False
    for tag in stack.contributed:
        if tag.is_attribute:
            continue
        if skill and not skill_used and tag.name.casefold() == _text(skill).casefold():
            skill_level = max(0, min(4, tag.rating))
            skill_used = True
            continue
        extras.append(tag.rating)

    return TagCheckInput(
        attribute_modifier=modifier,
        skill_level=skill_level,
        extra_modifiers=tuple(extras),
        stack=stack,
    )


def resolve_tag_check(
    tags: Sequence[Tag],
    *,
    attribute: str,
    difficulty: int,
    skill: str = "",
    action_scopes: Iterable[str] = (),
    has_skill: bool = True,
    max_contributing: int = PROTOTYPE_MAX_CONTRIBUTING_TAGS,
    presence: SystemPresence | None = None,
    system: str = "",
    rng: Any = None,
    dice_total: int | None = None,
) -> tuple[Any, TagCheckInput]:
    """Resolve a tag-based action through the canonical 2d6 engine.

    Returns ``(CheckResult, TagCheckInput)`` so a caller can see both the mechanical
    outcome and the tag audit that produced it. Dice are supplied by the deterministic
    layer, never by an LLM (#51 principle 9).

    ``presence`` (RULEBOOK §5.2) guards the case where the entity does not participate
    in the action's system. The action's system is ``system`` when given, and otherwise
    the system of the nominated attribute tag. When the system is absent the engine
    refuses: the result carries ``outcome="unresolved_absent_system"`` and no check is
    rolled, because rolling at a penalty would assert a capability the entity does not
    have. ``CheckResult`` has no outcome field, so the outcome is attached to the
    returned object and the refusal is reported through the audit input.
    """
    if presence is not None:
        target_system = _text(system).casefold() or _system_of_attribute(tags, attribute)
        if target_system and not presence.has(target_system):
            composed = TagCheckInput(
                attribute_modifier=0,
                skill_level=0,
                extra_modifiers=(),
                stack=TagStack(contributed=()),
                outcome=UNRESOLVED_ABSENT_SYSTEM,
                absent_system=target_system,
            )
            return AbsentSystemResult(system=target_system), composed

    composed = compose_check(
        tags,
        attribute=attribute,
        skill=skill,
        action_scopes=action_scopes,
        max_contributing=max_contributing,
    )
    from rules import resolve_check  # imported lazily: keeps this module import-light

    result = resolve_check(
        attribute_modifier=composed.attribute_modifier,
        target=difficulty,
        skill_level=composed.skill_level,
        has_skill=has_skill,
        extra_modifiers=composed.extra_modifiers,
        rng=rng,
        dice_total=dice_total,
    )
    return result, composed


def _system_of_attribute(tags: Sequence[Tag], attribute: str) -> str:
    """The four-system domain of the named attribute tag, or "" when not found."""
    wanted = _text(attribute)
    for tag in tags:
        if tag.is_attribute and tag.name.casefold() == wanted.casefold():
            return tag.system
    return ""


@dataclass(frozen=True, slots=True)
class AbsentSystemResult:
    """The refusal returned when an action sits in a system the entity does not have.

    It is deliberately **not** a ``CheckResult``: there is no dice total, no target and
    no success, because nothing was rolled. A caller that wants one number for "did it
    work" must handle absence explicitly instead of reading a default.
    """

    system: str
    outcome: str = UNRESOLVED_ABSENT_SYSTEM
