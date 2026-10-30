"""NoöPunk's tag-based attributes, skills and statuses (#821).

Tomi's draft is the authorial source of truth; this module is its executable form and is pinned to
``data/rules/noopunk_tags.json`` by ``tests/test_noopunk_tags_contract.py``. CWN/SWN supply the 3d6
chassis and the 0–4 skill scale; the seven attributes, their meanings and the skill names are
NoöPunk's own.

What the draft binds here:

* **Everything is a typed tag.** Attributes, skills, statuses and traits share one record with an
  explicit ``kind`` and ``sign``, so ``Shoot-1`` (skill rank 1) can never be read as a penalty.
* **Only the modifier is stored.** Generation rolls 3d6 and keeps the band value; the raw score is
  never written to a sheet.
* **The bands are the draft's.** 3 → -2, 4–7 → -1, 8–13 → 0, 14–17 → +1, 18 → +2, and no other
  distribution is generated.
* **Empathy -3 is not human and not a player character.** The generator cannot produce it.
* **Skills are tags at rank 0–4**, and an untrained action follows the draft's two cases.

Undecided in the draft, and therefore *not* decided here: which skills are impossible untrained, the
Connect design, the remaining Know/Work uses, alignment thresholds, and how existing characters
migrate. ``open_questions`` in the contract lists them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

CONTRACT_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "noopunk_tags.json"

ATTRIBUTES: tuple[str, ...] = (
    "Fitness", "Cognition", "Awareness", "Agency", "Reflexes", "Cyber", "Empathy",
)
SKILL_MAX = 4


class TagError(ValueError):
    """A tag, check or status that the draft's rules refuse."""


def _contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


CONTRACT = _contract()
#: (score, modifier) lower bounds, exactly as the draft tabulates them.
BANDS: tuple[tuple[int, int], ...] = tuple((int(s), int(m)) for s, m in CONTRACT["attributes"]["generation"]["bands"])
HUMAN_MIN, HUMAN_MAX = (int(v) for v in CONTRACT["attributes"]["human_range"])
#: What a sheet may *store*: -3 is the non-human floor the draft names, +6 is a serialisation guard
#: (the draft sets no transhuman ceiling). Human range is enforced only where humanity is at issue.
STORE_MIN = int(CONTRACT["attributes"]["storage_range"]["min"])
STORE_MAX = int(CONTRACT["attributes"]["storage_range"]["max"])
EMPATHY_FLOOR = int(CONTRACT["attributes"]["empathy_floor"]["value"])
UNTRAINED = int(CONTRACT["skills"]["untrained"]["penalty"])


class Kind(str, Enum):
    ATTRIBUTE = "attribute"
    SKILL = "skill"
    STATUS = "status"
    TRAIT = "trait"


class Duration(str, Enum):
    PERMANENT = "permanent"
    SCENE = "scene"
    DAY = "day"
    UNTIL_REST = "until_rest"


class Stacking(str, Enum):
    STACK = "stack"
    REPLACE = "replace"
    HIGHEST = "highest"


#: 3d6 → the draft's stored modifier. No other distribution is generated.
def modifier_for_score(score: int) -> int:
    if not 3 <= score <= 18:
        raise TagError(f"a 3d6 attribute score is 3..18, got {score}")
    value = BANDS[0][1]
    for lower, band in BANDS:
        if score >= lower:
            value = band
    return value


def roll_score(rng: Any) -> int:
    """Three d6 from a `random.Random`-shaped object."""
    return sum(rng.randint(1, 6) for _ in range(3))


@dataclass(frozen=True)
class Tag:
    """One typed tag: attribute, skill, status or trait.

    ``value`` is the tag's number and ``sign`` says how to read it, which is what keeps
    ``Shoot-1`` (rank 1) distinct from ``wounded-1`` (a penalty).
    """

    kind: Kind
    name: str
    value: int = 0
    sign: str = "+"
    duration: Duration = Duration.PERMANENT
    source: str = ""
    stacking: Stacking = Stacking.REPLACE
    exclusive_with: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name or self.name != self.name.strip():
            raise TagError("a tag needs a name without surrounding whitespace")
        if self.sign not in {"+", "-", ""}:
            raise TagError(f"sign must be '+', '-' or '' (neutral), got {self.sign!r}")
        if self.kind is Kind.SKILL and not 0 <= self.value <= SKILL_MAX:
            raise TagError(f"a skill tag is rank 0..{SKILL_MAX}, got {self.value}")

    @property
    def display(self) -> str:
        """The sheet syntax the draft specifies."""
        if self.kind is Kind.TRAIT:
            return self.name
        if self.kind is Kind.ATTRIBUTE:
            return f"{self.name}{self.sign}{abs(self.value)}"
        return f"{self.name}-{self.value}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value, "name": self.name, "value": self.value, "sign": self.sign,
            "duration": self.duration.value, "source": self.source,
            "stacking": self.stacking.value, "exclusive_with": list(self.exclusive_with),
        }

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "Tag":
        return Tag(
            kind=Kind(str(data.get("kind", ""))),
            name=str(data.get("name", "")),
            value=int(data.get("value", 0)),
            sign=str(data.get("sign", "+")),
            duration=Duration(str(data.get("duration", "permanent"))),
            source=str(data.get("source", "")),
            stacking=Stacking(str(data.get("stacking", "replace"))),
            exclusive_with=tuple(str(v) for v in data.get("exclusive_with", ())),
        )


def attribute_tag(name: str, value: int) -> Tag:
    if name not in ATTRIBUTES:
        raise TagError(f"unknown NoöPunk attribute {name!r}")
    if not STORE_MIN <= value <= STORE_MAX:
        raise TagError(f"{name} {value} is outside the storable range {STORE_MIN}..{STORE_MAX}")
    return Tag(Kind.ATTRIBUTE, name, value, "+" if value >= 0 else "-")


def skill_tag(name: str, rank: int) -> Tag:
    if name not in CONTRACT["skills"]["list"]:
        raise TagError(f"unknown NoöPunk skill {name!r}")
    return Tag(Kind.SKILL, name, rank, "+")


def status_tag(name: str, penalty: int, *, duration: Duration = Duration.SCENE,
               source: str = "", stacking: Stacking = Stacking.HIGHEST,
               exclusive_with: Iterable[str] = ()) -> Tag:
    if penalty < 0:
        raise TagError("a status penalty is a positive number carried with the '-' sign")
    return Tag(Kind.STATUS, name, penalty, "-", duration, source, stacking, tuple(exclusive_with))


@dataclass
class Sheet:
    """The seven attribute tags plus skill, status and trait tags, in one serialisable record."""

    attributes: dict[str, int] = field(default_factory=lambda: {name: 0 for name in ATTRIBUTES})
    skills: dict[str, int] = field(default_factory=dict)
    statuses: list[Tag] = field(default_factory=list)
    traits: list[Tag] = field(default_factory=list)

    def __post_init__(self) -> None:
        for name in self.attributes:
            if name not in ATTRIBUTES:
                raise TagError(f"unknown attribute tag {name!r}")
        for name, value in self.attributes.items():
            attribute_tag(name, int(value))  # the storable range, not the human one
        for name, rank in self.skills.items():
            skill_tag(name, int(rank))  # validates name and rank

    # -- eligibility ---------------------------------------------------------------------------
    @property
    def empathy(self) -> int:
        return int(self.attributes.get("Empathy", 0))

    @property
    def is_human(self) -> bool:
        return self.empathy > EMPATHY_FLOOR

    @property
    def is_transhuman(self) -> bool:
        """Any tag above the human baseline of +2. The draft sets no ceiling and no further rule."""
        return any(int(value) > HUMAN_MAX for value in self.attributes.values())

    @property
    def pc_eligible(self) -> bool:
        """Empathy -3 is outside the human range: not a player character."""
        return self.is_human

    # -- tags ----------------------------------------------------------------------------------
    def tags(self) -> list[Tag]:
        out = [attribute_tag(name, int(value)) for name, value in self.attributes.items()]
        out += [skill_tag(name, int(rank)) for name, rank in self.skills.items()]
        return out + list(self.statuses) + list(self.traits)

    def sheet_lines(self) -> list[str]:
        return sorted(tag.display for tag in self.tags())

    def status_penalty(self) -> int:
        """Summed penalty of the status tags, honouring stacking.

        One mode governs one status name: the mode of the newest tag for that name. Mixing modes
        across applications of the same status is therefore not ambiguous — re-applying a status
        under a different mode restates how *all* of its live tags count.
        """
        grouped: dict[str, list[Tag]] = {}
        for tag in self.statuses:
            grouped.setdefault(tag.name, []).append(tag)
        total = 0
        for tags in grouped.values():
            mode = tags[-1].stacking
            if mode is Stacking.STACK:
                total += sum(tag.value for tag in tags)
            elif mode is Stacking.HIGHEST:
                total += max(tag.value for tag in tags)
            else:
                total += tags[-1].value
        return total

    def add_status(self, tag: Tag) -> None:
        if tag.kind is not Kind.STATUS:
            raise TagError("add_status takes a status tag")
        for other in self.statuses:
            if tag.name in other.exclusive_with or other.name in tag.exclusive_with:
                self.statuses.remove(other)
        self.statuses.append(tag)

    def expire(self, duration: Duration) -> list[Tag]:
        """Drop the statuses whose duration has run out; permanent tags never expire."""
        if duration is Duration.PERMANENT:
            return []
        gone = [tag for tag in self.statuses if tag.duration is duration]
        self.statuses = [tag for tag in self.statuses if tag.duration is not duration]
        return gone

    # -- checks --------------------------------------------------------------------------------
    def attribute(self, name: str) -> int:
        if name not in self.attributes:
            raise TagError(f"unknown attribute {name!r}")
        return int(self.attributes[name])

    def skill_rank(self, name: str) -> int:
        return int(self.skills.get(name, UNTRAINED))

    def check(self, attribute: str, skill: str | None, roll: int, *, difficulty: int = 8,
              situational: int = 0) -> dict[str, Any]:
        """2d6 + attribute tag + skill rank + situational, against a difficulty.

        An untrained action uses the draft's untrained penalty. A skill the draft marks impossible
        without training refuses the check instead of rolling it.
        """
        if not 2 <= roll <= 12:
            return {"ok": False, "reason": "a_2d6_check_is_2_12"}
        rank = 0
        if skill is not None:
            entry = CONTRACT["skills"]["list"].get(skill)
            if entry is None:
                return {"ok": False, "reason": "unknown_skill", "skill": skill}
            options = entry.get("attribute_options", [])
            if entry.get("attribute") == "contextual" and attribute not in options:
                return {"ok": False, "reason": "contextual_skill_wrong_attribute", "skill": skill}
            if skill not in self.skills and skill in CONTRACT["skills"]["untrained"]["impossible_without"]:
                return {"ok": False, "reason": "trained_only", "skill": skill}
            rank = self.skill_rank(skill)
        total = roll + self.attribute(attribute) + rank + situational - self.status_penalty()
        return {"ok": True, "total": total, "success": total >= difficulty,
                "difficulty": difficulty, "rank": rank, "attribute_value": self.attribute(attribute)}

    # -- serialisation -------------------------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "attributes": dict(self.attributes),
            "skills": dict(self.skills),
            "statuses": [tag.to_dict() for tag in self.statuses],
            "traits": [tag.to_dict() for tag in self.traits],
        }

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "Sheet":
        return Sheet(
            attributes={str(k): int(v) for k, v in dict(data.get("attributes", {})).items()},
            skills={str(k): int(v) for k, v in dict(data.get("skills", {})).items()},
            statuses=[Tag.from_dict(t) for t in data.get("statuses", ())],
            traits=[Tag.from_dict(t) for t in data.get("traits", ())],
        )


def generate(rng: Any) -> Sheet:
    """Seven 3d6 rolls, stored as the draft's band modifiers.

    The generator cannot produce the non-human floor: the worst band a 3d6 roll reaches is -2, which
    is why a human character is always PC-eligible and an Empathy -3 must come from somewhere else.
    """
    attributes = {name: modifier_for_score(roll_score(rng)) for name in ATTRIBUTES}
    if attributes["Empathy"] <= EMPATHY_FLOOR:  # unreachable by construction; asserted, not assumed
        raise TagError("the human generator produced a non-human Empathy")
    return Sheet(attributes=attributes)


def migrate_from_cwn(cwn_attributes: Mapping[str, int]) -> dict[str, Any]:
    """The draft's conceptual CWN mapping, with its derivation made explicit.

    Returns the proposed attribute tags plus, per new tag, which old attributes produced it. This is
    a *proposal*: the draft leaves the multi-source case to an author ruling, so nothing here
    rewrites a character or a save on its own.
    """
    from .wn_core import attribute_modifier

    sources: dict[str, list[str]] = {name: [] for name in ATTRIBUTES}
    for old in ("Wisdom", "Strength", "Constitution", "Dexterity", "Intelligence", "Charisma"):
        for new in CONTRACT["migration_from_cwn"].get(old, []):
            if new in sources and old in cwn_attributes:
                sources[new].append(old)
    proposal = {
        new: max((attribute_modifier(int(cwn_attributes[old])) for old in olds), default=0)
        for new, olds in sources.items()
    }
    return {"attributes": proposal, "derivation": sources, "status": CONTRACT["migration_from_cwn"]["status"]}
