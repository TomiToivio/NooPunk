"""The NPC-side tag families (#1164, #1184): social, goal, clue and psyche (formerly personality).

CWN's own tag model already covers what a character *is* — attributes, skills, statuses and
equipment. These families describe something different: how the world stands toward the
character, what the character is trying to do, what the character has found out, and what an NPC will
do under pressure.

Three rules keep them from becoming a second rules engine:

1. **A tag is a fact, not a modifier.** Nothing here adds a number to a roll. A tag is either true or
   it is not, and the rules that read it decide what truth buys. This is the same discipline as
   ``src/rules/psi_access.py``: an option is admissible or it is not.
2. **No invented vocabulary.** Social polarity and goal state reuse words the repository already
   uses; clue reliability reuses the evidence ladder from the Helsinki gazetteer.
3. **The families stay apart.** A goal is not a clue, a clue is not proof, and an NPC's personality
   is not a social stance. Keeping them separate is what makes "what do I know?" answerable.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from enum import Enum


class NarrativeTagError(ValueError):
    """A tag is malformed, or two tags contradict each other."""


def _text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NarrativeTagError(f"{label} must be a nonempty string")
    return value.strip()


class Polarity(str, Enum):
    """How a social fact stands. Not a score: a fact can be favourable and still be small."""

    FAVOURABLE = "favourable"
    UNFAVOURABLE = "unfavourable"
    NEUTRAL = "neutral"


#: The evidence ladder the Helsinki gazetteer already uses, weakest to strongest. A clue's
#: reliability is one rung of it; the ladder is deliberately not a number, because "authenticated"
#: is a different kind of claim from "witnessed", not a bigger one.
EVIDENCE_LADDER: tuple[str, ...] = (
    "witness",
    "public",
    "authenticated",
    "conflicting",
    "anomalous",
)

#: How a clue came into the character's hands. Informant work and surveillance are separate on
#: purpose: the first is a person's word, the second is a record.
CLUE_ROUTES: tuple[str, ...] = (
    "observed",
    "told",
    "document",
    "forensic",
    "surveillance",
    "informant",
)


class GoalState(str, Enum):
    OPEN = "open"
    BLOCKED = "blocked"
    DONE = "done"
    ABANDONED = "abandoned"


@dataclass(frozen=True, slots=True)
class SocialTag:
    """A fact about how someone stands toward someone. Not a reputation score."""

    id: str
    holder: str  # who holds the attitude
    target: str  # about whom
    fact: str  # "owes a favour", "suspects me of leaking", "under investigation"
    polarity: Polarity
    source: str = ""  # the scene or clue that created it
    expires: str = ""  # episode or scene ref after which it is no longer true

    def __post_init__(self) -> None:
        _text(self.id, "social tag id")
        _text(self.holder, "holder")
        _text(self.target, "target")
        _text(self.fact, "fact")
        if self.holder == self.target:
            raise NarrativeTagError("a social tag relates two different parties")
        if not isinstance(self.polarity, Polarity):
            raise NarrativeTagError("polarity must be a Polarity")


@dataclass(frozen=True, slots=True)
class GoalTag:
    """Something a character is trying to do, and what is in the way."""

    id: str
    text: str
    owner: str
    state: GoalState = GoalState.OPEN
    blocked_by: tuple[str, ...] = ()
    clue_refs: tuple[str, ...] = ()
    scene_ref: str = ""

    def __post_init__(self) -> None:
        _text(self.id, "goal tag id")
        _text(self.text, "goal text")
        _text(self.owner, "goal owner")
        if not isinstance(self.state, GoalState):
            raise NarrativeTagError("state must be a GoalState")
        if self.state is GoalState.BLOCKED and not self.blocked_by:
            raise NarrativeTagError("a blocked goal must name what blocks it")
        if self.state is not GoalState.BLOCKED and self.blocked_by:
            raise NarrativeTagError(
                "only a blocked goal carries blockers; clear them when the state changes"
            )


@dataclass(frozen=True, slots=True)
class ClueTag:
    """A clue a character actually holds, with its provenance and its rung on the ladder.

    The clue's *content* stays in the case file (``src/rules/investigation.py``); this tag records
    that a particular character has it, how they got it, and how far it can be trusted.
    """

    id: str
    clue_id: str
    holder: str
    fact: str
    route: str
    reliability: str
    scene_ref: str = ""
    contradicts: tuple[str, ...] = ()
    #: Parties the clue is *about*. A document mentioning nobody is evidence of an act, not
    #: leverage over a person; naming who it concerns is what makes it usable in a conversation.
    bears_on: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.id, "clue tag id")
        _text(self.clue_id, "clue id")
        _text(self.holder, "holder")
        _text(self.fact, "fact")
        if self.route not in CLUE_ROUTES:
            raise NarrativeTagError(f"unknown clue route {self.route!r}")
        if self.reliability not in EVIDENCE_LADDER:
            raise NarrativeTagError(f"unknown reliability rung {self.reliability!r}")

    @property
    def rung(self) -> int:
        """Index on the ladder, so a caller can compare without re-implementing the order."""
        return EVIDENCE_LADDER.index(self.reliability)


@dataclass(frozen=True, slots=True)
class PersonalityTag:
    """A Psyche tag for an NPC: what they are like, what moves them, and what they will not do.

    ``PersonalityTag`` is kept as the serialized class name; ``PsycheTag`` is the #1283 name.
    """

    id: str
    npc: str
    trait: str
    lever: str
    under_pressure: str
    taboo: str = ""

    def __post_init__(self) -> None:
        _text(self.id, "personality tag id")
        _text(self.npc, "npc")
        _text(self.trait, "trait")
        _text(self.lever, "lever")
        _text(self.under_pressure, "under_pressure")

    def to_family_tag(self):
        """The portable Psyche tag for scene use: the owner, the trait, and where the record came from."""
        try:
            from src.rules.scene_tags import PsycheTag as portable
        except ModuleNotFoundError:  # pragma: no cover - installed with src/ on PYTHONPATH
            from rules.scene_tags import PsycheTag as portable  # type: ignore[no-redef]
        return portable(owner_id=self.npc, trait=self.trait, evidence=self.id)


@dataclass(frozen=True, slots=True)
class AstralTag:
    """A fact about the Noösphere attached to an NPC, place, device or relationship (#1283)."""

    id: str
    owner: str
    fact: str
    subject: str = ""
    evidence: str = ""

    def __post_init__(self) -> None:
        _text(self.id, "astral tag id")
        _text(self.owner, "astral tag owner")
        _text(self.fact, "astral tag fact")


#: #1283 author-facing name; the serialized field and class name remain ``PersonalityTag``.
PsycheTag = PersonalityTag


@dataclass
class TagBook:
    """The NPC-side tag families for one campaign, with cross-references checked together.

    A ``TagBook`` is deliberately small: one dictionary per family and the joins between them. It is
    not a character sheet (CWN owns that) and not a knowledge base (the case file owns that).
    """

    social: dict[str, SocialTag] = field(default_factory=dict)
    goals: dict[str, GoalTag] = field(default_factory=dict)
    clues: dict[str, ClueTag] = field(default_factory=dict)
    personality: dict[str, PersonalityTag] = field(default_factory=dict)
    astral: dict[str, AstralTag] = field(default_factory=dict)

    # -- adding ------------------------------------------------------------------------------
    def add_social(self, tag: SocialTag) -> SocialTag:
        if tag.id in self.social:
            raise NarrativeTagError(f"duplicate social tag id {tag.id!r}")
        self.social[tag.id] = tag
        return tag

    def add_goal(self, tag: GoalTag) -> GoalTag:
        if tag.id in self.goals:
            raise NarrativeTagError(f"duplicate goal tag id {tag.id!r}")
        for blocker in tag.blocked_by:
            if blocker not in self.goals:
                raise NarrativeTagError(
                    f"goal {tag.id!r} blocked by unknown goal {blocker!r}"
                )
        self.goals[tag.id] = tag
        return tag

    def add_clue(self, tag: ClueTag) -> ClueTag:
        if tag.id in self.clues:
            raise NarrativeTagError(f"duplicate clue tag id {tag.id!r}")
        self.clues[tag.id] = tag
        return tag

    def add_personality(self, tag: PersonalityTag) -> PersonalityTag:
        if tag.id in self.personality:
            raise NarrativeTagError(f"duplicate psyche tag id {tag.id!r}")
        self.personality[tag.id] = tag
        return tag

    def add_psyche(self, tag: PersonalityTag) -> PersonalityTag:
        """#1283 name for the same family; no second dictionary or serialization key."""
        return self.add_personality(tag)

    def add_astral(self, tag: AstralTag) -> AstralTag:
        if tag.id in self.astral:
            raise NarrativeTagError(f"duplicate astral tag id {tag.id!r}")
        self.astral[tag.id] = tag
        return tag

    # -- reading -----------------------------------------------------------------------------
    def stance(self, holder: str, target: str) -> tuple[SocialTag, ...]:
        return tuple(
            t for t in self.social.values() if t.holder == holder and t.target == target
        )

    def has_leverage(self, actor: str, subject: str) -> bool:
        """Whether ``actor`` has anything to move ``subject`` with.

        A lever is either an existing social fact between the two of them, or a clue the actor holds
        that is *about* the subject. A clue about a warehouse is not leverage over a clerk.
        """
        if self.stance(subject, actor) or self.stance(actor, subject):
            return True
        return any(
            clue.holder == actor and subject in clue.bears_on
            for clue in self.clues.values()
        )

    def goals_for(self, owner: str) -> tuple[GoalTag, ...]:
        return tuple(g for g in self.goals.values() if g.owner == owner)

    def open_goal_ids(self) -> frozenset[str]:
        return frozenset(g.id for g in self.goals.values() if g.state is GoalState.OPEN)

    def completed_goal_ids(self) -> frozenset[str]:
        """The shape ``StoryGraph.available(completed=...)`` expects."""
        return frozenset(g.id for g in self.goals.values() if g.state is GoalState.DONE)

    def clues_for(self, holder: str) -> tuple[ClueTag, ...]:
        return tuple(c for c in self.clues.values() if c.holder == holder)

    def strongest_rung(self, holder: str) -> int:
        """How far up the ladder this holder has actually climbed; -1 when they hold nothing."""
        tags = self.clues_for(holder)
        return max((t.rung for t in tags), default=-1)

    def psyche_of(self, npc: str) -> PersonalityTag | None:
        return self.personality_of(npc)

    def astral_of(self, owner: str) -> tuple[AstralTag, ...]:
        return tuple(t for t in self.astral.values() if t.owner == owner)

    def personality_of(self, npc: str) -> PersonalityTag | None:
        for tag in self.personality.values():
            if tag.npc == npc:
                return tag
        return None

    # -- integrity ---------------------------------------------------------------------------
    def validate(
        self,
        *,
        known_places: Iterable[str] = (),
        known_characters: Iterable[str] = (),
        known_scenes: Iterable[str] = (),
    ) -> None:
        """Check the joins a caller can afford to check. Unknown sets are simply not enforced."""
        places = set(known_places)
        characters = set(known_characters)
        scenes = set(known_scenes)
        for tag in self.social.values():
            for who in (tag.holder, tag.target):
                if characters and who not in characters:
                    raise NarrativeTagError(
                        f"social tag {tag.id!r} names unknown party {who!r}"
                    )
            if tag.source and scenes and tag.source not in scenes:
                raise NarrativeTagError(
                    f"social tag {tag.id!r} cites unknown scene {tag.source!r}"
                )
        for tag in self.clues.values():
            if characters and tag.holder not in characters:
                raise NarrativeTagError(
                    f"clue tag {tag.id!r} held by unknown character"
                )
            if tag.scene_ref and scenes and tag.scene_ref not in scenes:
                raise NarrativeTagError(
                    f"clue tag {tag.id!r} cites unknown scene {tag.scene_ref!r}"
                )
        for tag in self.personality.values():
            if characters and tag.npc not in characters:
                raise NarrativeTagError(
                    f"psyche tag {tag.id!r} names unknown NPC {tag.npc!r}"
                )
        for tag in self.astral.values():
            if characters and tag.owner not in characters:
                raise NarrativeTagError(
                    f"astral tag {tag.id!r} names unknown owner {tag.owner!r}"
                )
        for tag in self.goals.values():
            if characters and tag.owner not in characters:
                raise NarrativeTagError(
                    f"goal tag {tag.id!r} owned by unknown character"
                )
        if places:
            # Places are only meaningful for clues that were found *somewhere*.
            for tag in self.clues.values():
                where = tag.scene_ref
                if where and where.startswith("loc.") and where not in places:
                    raise NarrativeTagError(
                        f"clue tag {tag.id!r} found at unknown place {where!r}"
                    )

    def to_dict(self) -> dict[str, list[dict]]:
        return {
            "social": [
                asdict(t) | {"polarity": t.polarity.value} for t in self.social.values()
            ],
            "goals": [
                asdict(t)
                | {
                    "state": t.state.value,
                    "blocked_by": list(t.blocked_by),
                    "clue_refs": list(t.clue_refs),
                }
                for t in self.goals.values()
            ],
            "clues": [
                asdict(t)
                | {"contradicts": list(t.contradicts), "bears_on": list(t.bears_on)}
                for t in self.clues.values()
            ],
            "personality": [asdict(t) for t in self.personality.values()],
            "astral": [asdict(t) for t in self.astral.values()],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Iterable[Mapping]]) -> TagBook:
        book = cls()
        for raw in data.get("social", ()):
            item = dict(raw)
            item["polarity"] = Polarity(item["polarity"])
            book.add_social(SocialTag(**item))
        for raw in data.get("goals", ()):
            item = dict(raw)
            item["state"] = GoalState(item["state"])
            item["blocked_by"] = tuple(item.get("blocked_by", ()))
            item["clue_refs"] = tuple(item.get("clue_refs", ()))
            book.add_goal(GoalTag(**item))
        for raw in data.get("clues", ()):
            item = dict(raw)
            item["contradicts"] = tuple(item.get("contradicts", ()))
            item["bears_on"] = tuple(item.get("bears_on", ()))
            book.add_clue(ClueTag(**item))
        for raw in data.get("personality", ()):
            book.add_personality(PersonalityTag(**dict(raw)))
        for raw in data.get("astral", ()):
            book.add_astral(AstralTag(**dict(raw)))
        return book
