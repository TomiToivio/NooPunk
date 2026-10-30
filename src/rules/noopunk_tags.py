"""NoöPunk tag-based attributes (#821, child of #814).

Authorial draft: every character/game property is a **typed tag**, not a bare number. A tag carries its
type, so `Fitness-2` (attribute modifier −2) and `Shoot-1` (skill level 1) are never confused with
`wounded-1` (a negative status), even though they print alike.

Two things here are not negotiable, and both are pinned by tests:

* **The 3d6 → modifier bands are the draft's**, exactly: 3 → −2, 4–7 → −1, 8–13 → 0, 14–17 → +1,
  18 → +2. "Preserve the 3d6 initial generation bands" is an instruction, not a suggestion.
* **The sheet shows the modifier, never the raw roll.** A generated character stores tags, and the raw
  3d6 result is not part of the character.

The CWN/SWN conversion is deliberately *provisional*. The draft says the mapping is conceptual and that
migrating existing characters needs a ruling, especially where several old attributes feed one new tag
(Strength **and** Constitution → Fitness; Wisdom → Agency/Empathy/Awareness). :func:`propose_conversion`
therefore returns a proposal with its reasoning attached and flags the multi-source cases, rather than
inventing a merge rule and calling it canon.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

#: The seven NoöPunk attributes, in the draft's order.
ATTRIBUTES: tuple[str, ...] = (
    "Fitness",
    "Cognition",
    "Awareness",
    "Agency",
    "Reflexes",
    "Cyber",
    "Empathy",
)

#: Human baseline. Above +2 is transhuman.
ATTRIBUTE_MIN = -2
ATTRIBUTE_MAX_HUMAN = 2

#: The draft's 3d6 → modifier table, as inclusive (low, high, modifier) bands.
ROLL_BANDS: tuple[tuple[int, int, int], ...] = (
    (3, 3, -2),
    (4, 7, -1),
    (8, 13, 0),
    (14, 17, 1),
    (18, 18, 2),
)


class TagType(str, Enum):
    """What a tag *is*. The type, not the spelling, decides how it is read."""

    ATTRIBUTE = "attribute"
    SKILL = "skill"
    STATUS = "status"
    OTHER = "other"


@dataclass(frozen=True)
class Tag:
    """One typed tag.

    ``value`` means different things by type, which is exactly why the type is explicit: an attribute
    tag's value is a modifier, a skill tag's value is a level, a status tag's value is a severity.
    """

    name: str
    tag_type: TagType
    value: int
    permanent: bool = True

    def __post_init__(self) -> None:
        if not str(self.name).strip():
            raise ValueError("a tag needs a name")
        if not isinstance(self.value, int) or isinstance(self.value, bool):
            raise ValueError(f"tag value must be an integer, got {self.value!r}")

    @property
    def is_negative(self) -> bool:
        """True for a value below zero — for statuses this is the usual case, for skills it is not."""
        return self.value < 0

    def display(self) -> str:
        """The sheet syntax: `Name+2`, `Name-1`, `Name` for zero.

        Skills keep the same shape as attributes on purpose — `Shoot-1` means *level 1*, and the type is
        what disambiguates it, per the draft. Readers must not infer meaning from the sign alone.
        """
        if self.value == 0:
            return self.name
        return f"{self.name}{self.value:+d}"


def modifier_for_roll(total: int) -> int:
    """The draft's 3d6 band table. Values outside 3–18 are refused rather than clamped."""
    for low, high, modifier in ROLL_BANDS:
        if low <= total <= high:
            return modifier
    raise ValueError(f"3d6 total {total} outside 3-18")


def roll_3d6(rng: random.Random) -> int:
    return sum(rng.randint(1, 6) for _ in range(3))


def generate_attribute_tags(rng: random.Random) -> dict[str, Tag]:
    """Roll 3d6 for each of the seven attributes and keep only the modifier.

    The raw total is discarded on purpose: the draft requires the sheet to show modifiers, and a stored
    raw value would invite someone to display it.
    """
    tags: dict[str, Tag] = {}
    for attribute in ATTRIBUTES:
        modifier = modifier_for_roll(roll_3d6(rng))
        tags[attribute] = Tag(name=attribute, tag_type=TagType.ATTRIBUTE, value=modifier)
    return tags


def is_transhuman(tags: dict[str, Tag]) -> bool:
    """Above +2 is transhuman; the draft's ceiling for a human."""
    return any(
        tag.tag_type is TagType.ATTRIBUTE and tag.value > ATTRIBUTE_MAX_HUMAN for tag in tags.values()
    )


def attribute_tags(tags: dict[str, Tag]) -> dict[str, Tag]:
    return {name: tag for name, tag in tags.items() if tag.tag_type is TagType.ATTRIBUTE}


def validate_attribute_set(tags: dict[str, Tag]) -> None:
    """A character sheet must carry all seven attributes, and nothing outside the human band."""
    present = set(attribute_tags(tags))
    missing = sorted(set(ATTRIBUTES) - present)
    if missing:
        raise ValueError(f"missing attributes: {missing}")
    for name, tag in attribute_tags(tags).items():
        if not ATTRIBUTE_MIN <= tag.value <= ATTRIBUTE_MAX_HUMAN:
            raise ValueError(
                f"{name}={tag.value} outside {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX_HUMAN} "
                "(above +2 would be transhuman and needs an explicit ruling)"
            )


#: Conceptual CWN/SWN → NoöPunk mapping from the draft. Kept as data so the tests can pin it.
CONVERSION_SOURCES: dict[str, tuple[str, ...]] = {
    "Agency": ("WIS", "CHA"),
    "Empathy": ("WIS", "CHA"),
    "Awareness": ("WIS", "CHA"),
    "Fitness": ("STR", "CON"),
    "Reflexes": ("DEX",),
    "Cognition": ("INT",),
    "Cyber": ("INT",),
}


@dataclass(frozen=True)
class ConversionProposal:
    """A suggested value plus the question it raises, for Tomi to rule on."""

    attribute: str
    suggestion: int
    sources: tuple[str, ...]
    needs_ruling: bool
    reason: str


def propose_conversion(cwn_modifiers: dict[str, int]) -> list[ConversionProposal]:
    """Propose NoöPunk attribute tags from CWN modifiers — explicitly a proposal.

    Single-source tags (Reflexes←DEX, Cognition←INT, Cyber←INT) carry the old modifier directly.
    Multi-source tags keep the **highest** old modifier as the suggestion and are flagged
    ``needs_ruling``: averaging, taking the highest, or letting the player assign are all defensible and
    the draft does not choose between them.
    """
    proposals: list[ConversionProposal] = []
    for attribute in ATTRIBUTES:
        sources = CONVERSION_SOURCES[attribute]
        available = [source for source in sources if source in cwn_modifiers]
        if not available:
            raise ValueError(f"no CWN source modifier for {attribute} (expected one of {sources})")
        values = [cwn_modifiers[source] for source in available]
        suggestion = max(values)
        multi = len(available) > 1
        proposals.append(
            ConversionProposal(
                attribute=attribute,
                suggestion=max(ATTRIBUTE_MIN, min(ATTRIBUTE_MAX_HUMAN, suggestion)),
                sources=tuple(available),
                needs_ruling=multi,
                reason=(
                    f"{len(available)} CWN attributes feed {attribute}; the draft calls the mapping "
                    "conceptual, so the merge rule is Tomi's to choose"
                    if multi
                    else f"{available[0]} maps directly to {attribute}"
                ),
            )
        )
    return proposals
