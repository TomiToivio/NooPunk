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
from dataclasses import dataclass, field
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
    duration: str = "permanent"
    stacking: str = "replace"
    exclusive_with: tuple[str, ...] = ()

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
        """The sheet syntax the draft specifies, by type.

        * attribute → `Cognition+2`, `Fitness-2`, `Agency+0`
        * skill → `Firearms-1` — the number is the **rank**, never a sign
        * status → `wounded-1` — the number is the **severity**, stored negative
        * other → the bare name

        The type, not the spelling, decides how it is read; printing a skill rank as `Firearms+1`
        would be worse than ambiguous, because it would look like a bonus to a roll.
        """
        if self.tag_type is TagType.SKILL:
            return f"{self.name}-{self.value}"
        if self.tag_type is TagType.ATTRIBUTE:
            return f"{self.name}{self.value:+d}"
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


def validate_attribute_set(tags: dict[str, Tag], *, allow_transhuman: bool = False) -> None:
    """A character sheet must carry all seven attributes.

    By default nothing may sit outside the human band, which is the creation rule. ``allow_transhuman``
    permits a tag above +2 for a character that has already crossed that line — the draft calls such a
    character transhuman and sets no ceiling, so refusing to *store* one would be inventing a rule.
    """
    present = set(attribute_tags(tags))
    missing = sorted(set(ATTRIBUTES) - present)
    if missing:
        raise ValueError(f"missing attributes: {missing}")
    for name, tag in attribute_tags(tags).items():
        if tag.value < ATTRIBUTE_MIN:
            raise ValueError(f"{name}={tag.value} is below the human floor {ATTRIBUTE_MIN}")
        if allow_transhuman:
            continue
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

# -- skills, checks and statuses ---------------------------------------------------------------
#
# #823 landed the attribute half: typed tags, the draft's bands, generation and the conversion
# proposal. The draft also makes skills and statuses tags, and a tag model that cannot answer a check
# is not yet a game. This half is additive: the same `Tag`, the same `TagType`, no second vocabulary.

#: The draft's skill list: attribute, the CWN skill it replaces or renames, and its status.
SKILLS: dict[str, dict[str, object]] = {
    "Administer": {"attribute": "Cognition", "cwn": "Administer"},
    "Connect": {"attribute": "Empathy", "cwn": "Connect", "pending": True},
    "Drive": {"attribute": "Reflexes", "cwn": "Drive"},
    "Strength": {"attribute": "Fitness", "cwn": "Exert"},
    "Stamina": {"attribute": "Fitness", "cwn": "Exert"},
    "Hardware": {"attribute": "Cyber", "cwn": "Fix"},
    "Wetware": {"attribute": "Empathy", "cwn": "Heal"},
    "Software": {"attribute": "Cyber", "cwn": "Program"},
    "Noöware": {"attribute": "Empathy", "cwn": None},
    "Research": {"attribute": "Cognition", "cwn": "Know"},
    "Know": {"attribute": None, "cwn": "Know", "pending": True},
    "Lead": {"attribute": "Agency", "cwn": "Lead"},
    "Notice": {"attribute": "Awareness", "cwn": "Notice"},
    "Unarmed": {"attribute": "Reflexes", "cwn": "Punch"},
    "Melee": {"attribute": "Reflexes", "cwn": "Stab"},
    "Firearms": {"attribute": "Reflexes", "cwn": "Shoot"},
    "Sneak": {"attribute": "Awareness", "cwn": "Sneak"},
    "Survive": {"attribute": "Agency", "cwn": "Survive"},
    "Talk": {"attribute": "contextual", "cwn": "Talk", "options": ("Empathy", "Agency")},
    "Trade": {"attribute": "Agency", "cwn": "Trade"},
    "Work": {"attribute": None, "cwn": "Work", "pending": True},
}

SKILL_MAX = 4
#: An untrained action is attempted at -1 until Tomi rules which skills are impossible instead.
UNTRAINED = -1
#: Skills that cannot be attempted untrained. Empty on purpose: the draft leaves this open.
IMPOSSIBLE_UNTRAINED: tuple[str, ...] = ()
#: Empathy -3 is outside the human range: not human, not a player character.
EMPATHY_FLOOR = -3


def skill_tag(name: str, rank: int) -> Tag:
    """A skill tag. ``rank`` is 0-4 and is a level, not a bonus."""
    if name not in SKILLS:
        raise ValueError(f"unknown NoöPunk skill {name!r}")
    if not 0 <= rank <= SKILL_MAX:
        raise ValueError(f"skill rank must be 0..{SKILL_MAX}, got {rank}")
    return Tag(name=name, tag_type=TagType.SKILL, value=rank)


def status_tag(name: str, severity: int, *, duration: str = "scene", source: str = "",
               stacking: str = "highest", exclusive_with: tuple[str, ...] = ()) -> Tag:
    """A status tag. ``severity`` is given as a penalty (1 = one point worse) and stored negative."""
    if severity < 0:
        raise ValueError("pass the severity as a positive penalty; the tag stores it negative")
    return Tag(name=name, tag_type=TagType.STATUS, value=-severity, permanent=duration == "permanent",
               duration=duration, stacking=stacking, exclusive_with=exclusive_with)


@dataclass
class Sheet:
    """Attribute tags plus skill, status and other tags — the whole character, serialisable."""

    attributes: dict[str, Tag] = field(default_factory=dict)
    skills: dict[str, Tag] = field(default_factory=dict)
    statuses: list[Tag] = field(default_factory=list)
    others: list[Tag] = field(default_factory=list)

    def __post_init__(self) -> None:
        for name, tag in self.attributes.items():
            if tag.tag_type is not TagType.ATTRIBUTE:
                raise ValueError(f"{name} is not an attribute tag")
        for name, tag in self.skills.items():
            if tag.tag_type is not TagType.SKILL:
                raise ValueError(f"{name} is not a skill tag")

    # -- eligibility ---------------------------------------------------------------------------
    @property
    def empathy(self) -> int:
        return int(self.attributes["Empathy"].value) if "Empathy" in self.attributes else 0

    @property
    def is_human(self) -> bool:
        return self.empathy > EMPATHY_FLOOR

    @property
    def pc_eligible(self) -> bool:
        """Empathy -3 is outside the human range: no longer a player character."""
        return self.is_human

    @property
    def is_transhuman(self) -> bool:
        return is_transhuman(self.attributes)

    # -- tags ----------------------------------------------------------------------------------
    def all_tags(self) -> list[Tag]:
        return (list(self.attributes.values()) + list(self.skills.values())
                + list(self.statuses) + list(self.others))

    def sheet_lines(self) -> list[str]:
        return sorted(tag.display() for tag in self.all_tags())

    def status_penalty(self) -> int:
        """The summed penalty, honouring stacking.

        One mode governs one status name: the mode of the newest application. Mixing modes across
        applications is therefore never ambiguous — re-applying a status under a different mode
        restates how all of its live tags count.
        """
        grouped: dict[str, list[Tag]] = {}
        for tag in self.statuses:
            grouped.setdefault(tag.name, []).append(tag)
        total = 0
        for tags in grouped.values():
            mode = tags[-1].stacking
            if mode == "stack":
                total += sum(tag.value for tag in tags)
            elif mode == "highest":
                total += min(tag.value for tag in tags)  # values are negative: the worst is lowest
            else:
                total += tags[-1].value
        return -total

    def add_status(self, tag: Tag) -> None:
        if tag.tag_type is not TagType.STATUS:
            raise ValueError("add_status takes a status tag")
        self.statuses = [other for other in self.statuses
                         if tag.name not in other.exclusive_with
                         and other.name not in tag.exclusive_with]
        self.statuses.append(tag)

    def expire(self, duration: str) -> list[Tag]:
        """Drop the statuses whose duration ran out. Permanent tags never expire."""
        if duration == "permanent":
            return []
        gone = [tag for tag in self.statuses if tag.duration == duration]
        self.statuses = [tag for tag in self.statuses if tag.duration != duration]
        return gone

    # -- checks --------------------------------------------------------------------------------
    def attribute(self, name: str) -> int:
        if name not in self.attributes:
            raise ValueError(f"unknown attribute {name!r}")
        return int(self.attributes[name].value)

    def skill_rank(self, name: str) -> int:
        return int(self.skills[name].value) if name in self.skills else UNTRAINED

    def check(self, attribute: str, skill: str | None, roll: int, *, difficulty: int = 8,
              situational: int = 0) -> dict[str, object]:
        """2d6 + attribute tag + skill rank + situational - status penalties.

        Rule refusals come back as a result with ``ok: False`` and a ``reason`` — the engine returns the
        same shape, so callers do not have to catch an exception on one side and check a field on the
        other.
        """
        if not 2 <= roll <= 12:
            return {"ok": False, "reason": "a_2d6_check_is_2_12"}
        rank = 0
        if skill is not None:
            entry = SKILLS.get(skill)
            if entry is None:
                return {"ok": False, "reason": "unknown_skill", "skill": skill}
            options = tuple(entry.get("options", ()))
            if entry.get("attribute") == "contextual" and attribute not in options:
                return {"ok": False, "reason": "contextual_skill_wrong_attribute", "skill": skill}
            if skill not in self.skills and skill in IMPOSSIBLE_UNTRAINED:
                return {"ok": False, "reason": "trained_only", "skill": skill}
            rank = self.skill_rank(skill)
        total = roll + self.attribute(attribute) + rank + situational - self.status_penalty()
        return {"ok": True, "total": total, "success": total >= difficulty,
                "difficulty": difficulty, "rank": rank, "attribute_value": self.attribute(attribute)}

    # -- serialisation -------------------------------------------------------------------------
    def to_dict(self) -> dict[str, object]:
        return {
            "attributes": {name: tag.value for name, tag in self.attributes.items()},
            "skills": {name: tag.value for name, tag in self.skills.items()},
            "statuses": [{"name": t.name, "value": t.value, "duration": t.duration,
                          "stacking": t.stacking, "exclusive_with": list(t.exclusive_with)}
                         for t in self.statuses],
            "others": [{"name": t.name, "value": t.value} for t in self.others],
        }

    @staticmethod
    def from_dict(data: dict[str, object]) -> "Sheet":
        sheet = Sheet(
            attributes={name: Tag(name, TagType.ATTRIBUTE, int(value))
                        for name, value in dict(data.get("attributes", {})).items()},
            skills={name: skill_tag(name, int(value))
                    for name, value in dict(data.get("skills", {})).items()},
        )
        for entry in data.get("statuses", ()):  # type: ignore[union-attr]
            sheet.statuses.append(Tag(name=entry["name"], tag_type=TagType.STATUS, value=-abs(entry["value"]),
                                      duration=entry.get("duration", "permanent"),
                                      permanent=entry.get("duration", "permanent") == "permanent",
                                      stacking=entry.get("stacking", "replace"),
                                      exclusive_with=tuple(entry.get("exclusive_with", ()))))
        return sheet


def generate_sheet(rng: random.Random) -> Sheet:
    """Seven 3d6 attributes as a sheet. The generator cannot reach the non-human floor."""
    return Sheet(attributes=generate_attribute_tags(rng))
