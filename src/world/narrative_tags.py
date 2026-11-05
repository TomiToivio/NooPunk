"""Narrative tags: the only addition NoöPunk makes to the CWN core (#1178, scene proposal).

CWN stays immutable. This module adds four *narrative* tag families — Social, Goal, Clue and
Personality — and nothing else:

| Tag | What it records | What it may do |
| --- | --- | --- |
| **Social** | a standing between two parties: membership, obligation, protection, rivalry, informant | open a door, change who will talk to you, make a scene possible |
| **Goal** | an intent with a horizon and a status | gate a scene, record progress, never award a bonus |
| **Clue** | a fact someone believes, with provenance and strength | prove a link on the case board, contradict another clue |
| **Personality** | a disposition that explains behaviour | tell the GM and the player *how* an NPC acts, never *what wins* |

Three rules make this an addition rather than a second game:

1. **They carry no rating.** A tag is a statement, not a modifier. Numeric modifiers stay in CWN's
   skills and in `src/rules/tags.py` (attributes, skills, statuses). A Clue does not add +2 to
   anything; it exists so a scene can *require* it.
2. **Provenance is not promotable.** A clue enters the world in one of four registers — `observed`,
   `claimed`, `disputed`, `hypothesis`. Moving up that ladder requires an explicit authority (a
   scene, a document, a lab) recorded in the tag's history; nothing is promoted by elapsed time.
3. **Tags gate fiction, never outcomes.** A scene contract may require a Social tag for a meeting to
   happen at all. Whether the meeting *succeeds* is still a CWN check.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from typing import Any

__all__ = [
    "NARRATIVE_TAG_KINDS",
    "REGISTERS",
    "ClueTag",
    "GoalTag",
    "NarrativeTag",
    "NarrativeTagError",
    "NarrativeTags",
    "PersonalityTag",
    "SocialTag",
]


NARRATIVE_TAG_KINDS = ("social", "goal", "clue", "personality")

#: Evidence registers, weakest first (#1184 §4). `observed` is the only one that is first-hand.
REGISTERS = ("hypothesis", "disputed", "claimed", "observed")

CLUE_STRENGTHS = ("core", "supporting", "weak")
SOCIAL_RELATIONS = ("member", "owe", "owed", "protect", "rival", "informant", "family")
GOAL_HORIZONS = ("scene", "episode", "series")
GOAL_STATUSES = ("active", "met", "failed", "abandoned")


def _stable(value: str, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NarrativeTagError(f"{what} must be a non-empty string")
    if any(character.isspace() for character in value.strip()):
        raise NarrativeTagError(f"{what} must be a stable id without spaces: {value!r}")
    return value.strip()


class NarrativeTagError(ValueError):
    """A narrative tag would claim more than its provenance allows."""


@dataclass(frozen=True)
class NarrativeTag:
    """One statement about the world, with where it came from."""

    id: str
    kind: str
    label: str
    subject: str
    detail: str = ""
    register: str = "observed"
    source_ref: str = ""
    refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _stable(self.id, "tag id")
        _stable(self.subject, "tag subject")
        if self.kind not in NARRATIVE_TAG_KINDS:
            raise NarrativeTagError(f"unknown tag kind {self.kind!r}; expected {NARRATIVE_TAG_KINDS}")
        if not isinstance(self.label, str) or not self.label.strip():
            raise NarrativeTagError("tag label must be a non-empty string")
        if self.register not in REGISTERS:
            raise NarrativeTagError(f"unknown register {self.register!r}; expected {REGISTERS}")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.refs):
            raise NarrativeTagError("refs must be non-empty ids")
        object.__setattr__(self, "refs", tuple(self.refs))


@dataclass(frozen=True)
class SocialTag(NarrativeTag):
    """A standing between two parties. Valence mirrors the Social graph's -4..+4, but adds no roll."""

    kind: str = field(default="social", init=False)
    relation: str = "member"
    valence: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.relation not in SOCIAL_RELATIONS:
            raise NarrativeTagError(f"unknown relation {self.relation!r}; expected {SOCIAL_RELATIONS}")
        if not isinstance(self.valence, int) or isinstance(self.valence, bool):
            raise NarrativeTagError("valence must be an int")
        if not -4 <= self.valence <= 4:
            raise NarrativeTagError("valence must stay inside the Social graph's -4..+4")


@dataclass(frozen=True)
class GoalTag(NarrativeTag):
    """An intent. It gates scenes; progress lives in `src/rules/goals.py`, not here."""

    kind: str = field(default="goal", init=False)
    horizon: str = "episode"
    status: str = "active"
    goal_ref: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.horizon not in GOAL_HORIZONS:
            raise NarrativeTagError(f"unknown horizon {self.horizon!r}; expected {GOAL_HORIZONS}")
        if self.status not in GOAL_STATUSES:
            raise NarrativeTagError(f"unknown status {self.status!r}; expected {GOAL_STATUSES}")


@dataclass(frozen=True)
class ClueTag(NarrativeTag):
    """A fact with provenance. `core` clues must never be gated behind a roll (see scenes.py)."""

    kind: str = field(default="clue", init=False)
    strength: str = "supporting"
    contradicts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.strength not in CLUE_STRENGTHS:
            raise NarrativeTagError(f"unknown clue strength {self.strength!r}; expected {CLUE_STRENGTHS}")
        # Provenance discipline belongs to evidence, not to dispositions: a clue may only be
        # `observed` if something actually observed it.
        if self.register == "observed" and not self.source_ref:
            raise NarrativeTagError(
                f"{self.id!r} is registered as observed but names no source; "
                "first-hand status needs a document, scene or device that saw it"
            )
        object.__setattr__(self, "contradicts", tuple(self.contradicts))
        if self.id in self.contradicts:
            raise NarrativeTagError("a clue cannot contradict itself")


@dataclass(frozen=True)
class PersonalityTag(NarrativeTag):
    """A disposition. It explains behaviour and never adds a modifier."""

    kind: str = field(default="personality", init=False)
    trait: str = ""
    pressure: str = "steady"

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.trait.strip():
            raise NarrativeTagError("a personality tag needs a trait, e.g. 'procedural'")
        if self.pressure not in ("steady", "strained", "breaking"):
            raise NarrativeTagError("pressure must be steady, strained or breaking")


@dataclass
class NarrativeTags:
    """The tag store for a world. Ids are unique across all four families."""

    tags: dict[str, NarrativeTag] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for key, tag in self.tags.items():
            if key != tag.id:
                raise NarrativeTagError(f"tag key {key!r} does not match id {tag.id!r}")
        self._check_references()

    # -- access ---------------------------------------------------------- #
    def add(self, tag: NarrativeTag) -> NarrativeTag:
        if tag.id in self.tags:
            raise NarrativeTagError(f"tag {tag.id!r} already exists")
        candidate = dict(self.tags) | {tag.id: tag}
        # Validate before committing: a rejected tag must not poison the store.
        self._check_references(candidate)
        self.tags = candidate
        return tag

    def of_kind(self, kind: str) -> tuple[NarrativeTag, ...]:
        return tuple(tag for tag in self._sorted() if tag.kind == kind)

    def for_subject(self, subject: str) -> tuple[NarrativeTag, ...]:
        return tuple(tag for tag in self._sorted() if tag.subject == subject)

    def get(self, tag_id: str) -> NarrativeTag:
        try:
            return self.tags[tag_id]
        except KeyError:
            raise NarrativeTagError(f"unknown tag {tag_id!r}") from None

    # -- the discipline --------------------------------------------------- #
    def verify(self, tag_id: str, *, authority: str) -> NarrativeTag:
        """Promote a clue after an authority has actually checked it.

        `authority` is required and recorded in `source_ref`; there is no path that promotes a claim
        with no verifier, which is the whole point of #1184's evidence registers.
        """
        tag = self.get(tag_id)
        if not isinstance(tag, ClueTag):
            raise NarrativeTagError("only clues carry a verifiable register")
        if not authority.strip():
            raise NarrativeTagError("verification needs an authority: scene, document or device")
        order = {name: index for index, name in enumerate(REGISTERS)}
        if order["observed"] <= order[tag.register]:
            return tag
        verified = replace(tag, register="observed", source_ref=authority)
        self.tags = dict(self.tags) | {tag_id: verified}
        return verified

    def core_clues(self) -> tuple[ClueTag, ...]:
        return tuple(tag for tag in self.of_kind("clue") if isinstance(tag, ClueTag) and tag.strength == "core")

    def contradictions(self) -> tuple[tuple[str, str], ...]:
        pairs = set()
        for tag in self.of_kind("clue"):
            assert isinstance(tag, ClueTag)
            for other in tag.contradicts:
                pairs.add(tuple(sorted((tag.id, other))))
        return tuple(sorted(pairs))

    # -- serialization ---------------------------------------------------- #
    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "noopunk.narrative_tags",
            "version": 1,
            "tags": [self._tag_to_dict(tag) for tag in self._sorted()],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> NarrativeTags:
        tags: dict[str, NarrativeTag] = {}
        for raw in payload.get("tags", ()):
            tag = _tag_from_dict(raw)
            if tag.id in tags:
                raise NarrativeTagError(f"duplicate tag id {tag.id!r}")
            tags[tag.id] = tag
        return cls(tags)

    # -- internals -------------------------------------------------------- #
    def _sorted(self) -> list[NarrativeTag]:
        return [self.tags[key] for key in sorted(self.tags)]

    def _check_references(self, tags: Mapping[str, NarrativeTag] | None = None) -> None:
        selected = self.tags if tags is None else tags
        ids = set(selected)
        for tag in selected.values():
            if isinstance(tag, ClueTag):
                missing = [other for other in tag.contradicts if other not in ids]
                if missing:
                    raise NarrativeTagError(f"{tag.id!r} contradicts unknown clues {missing}")

    @staticmethod
    def _tag_to_dict(tag: NarrativeTag) -> dict[str, Any]:
        raw: dict[str, Any] = {
            "id": tag.id,
            "kind": tag.kind,
            "label": tag.label,
            "subject": tag.subject,
            "detail": tag.detail,
            "register": tag.register,
            "source_ref": tag.source_ref,
            "refs": list(tag.refs),
        }
        if isinstance(tag, SocialTag):
            raw |= {"relation": tag.relation, "valence": tag.valence}
        elif isinstance(tag, GoalTag):
            raw |= {"horizon": tag.horizon, "status": tag.status, "goal_ref": tag.goal_ref}
        elif isinstance(tag, ClueTag):
            raw |= {"strength": tag.strength, "contradicts": list(tag.contradicts)}
        elif isinstance(tag, PersonalityTag):
            raw |= {"trait": tag.trait, "pressure": tag.pressure}
        return raw


def _tag_from_dict(raw: Mapping[str, Any]) -> NarrativeTag:
    tag_id = str(raw["id"])
    label = str(raw["label"])
    subject = str(raw["subject"])
    detail = str(raw.get("detail", ""))
    register = str(raw.get("register", "observed"))
    source_ref = str(raw.get("source_ref", ""))
    refs = tuple(str(ref) for ref in raw.get("refs", ()))
    kind = str(raw.get("kind", ""))
    if kind == "social":
        return SocialTag(tag_id, label, subject, detail, register, source_ref, refs,
                         relation=str(raw.get("relation", "member")),
                         valence=int(raw.get("valence", 0)))
    if kind == "goal":
        return GoalTag(tag_id, label, subject, detail, register, source_ref, refs,
                       horizon=str(raw.get("horizon", "episode")),
                       status=str(raw.get("status", "active")),
                       goal_ref=str(raw.get("goal_ref", "")))
    if kind == "clue":
        return ClueTag(tag_id, label, subject, detail, register, source_ref, refs,
                       strength=str(raw.get("strength", "supporting")),
                       contradicts=tuple(str(other) for other in raw.get("contradicts", ())))
    if kind == "personality":
        return PersonalityTag(tag_id, label, subject, detail, register, source_ref, refs,
                              trait=str(raw.get("trait", "")),
                              pressure=str(raw.get("pressure", "steady")))
    raise NarrativeTagError(f"unknown tag kind {kind!r}; expected {NARRATIVE_TAG_KINDS}")


def tag_ids(tags: Iterable[NarrativeTag]) -> frozenset[str]:
    return frozenset(tag.id for tag in tags)
