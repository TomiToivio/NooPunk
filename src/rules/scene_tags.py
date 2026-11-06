"""The portable tag families, as decided in #1283.

NoöPunk's default tabletop system is **Cities Without Number**: CWN resolves skills, action, combat, equipment and
hacking, and nothing here replaces any of it. On top of that sits a *portable* layer of tags describing the people,
places and situations that matter, so the same authored scene can be run under CWN or under another cyberpunk RPG.

Five families are in play from the start (#1283, author decision 2026-11-07):

| family | records |
|---|---|
| **Clue** | something the investigators can follow up, with its source |
| **Social** | a relationship fact that affects an interaction — trust, obligation, access |
| **Goal** | an outcome a character or faction is pursuing |
| **Psyche** | a character's inner life: enduring traits, values, fears, habits, temporary states |
| **Astral** | a Noösphere fact that affects what someone can perceive, attempt or change |

**The list is open.** :data:`TAG_FAMILIES` holds the five starting families and :func:`register_family` adds another by
name: a family is a name and a one-line meaning, not an enum that forbids the sixth. What must *not* grow is the number
of models — this module defines the portable records, and :mod:`src.world.narrative_tags` keeps the richer per-NPC
record with a bridge back into these.

**Psyche** replaces the earlier name *Personality*. ``PersonalityTag`` stays as a deprecated alias so older code and
documents keep working; new code says ``PsycheTag``.

No tag is a stat, a roll, a meter or a mind-control switch. A tag says something true in the fiction; when an outcome is
uncertain, the host RPG's procedure resolves it.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.rules.goals import Goal as GoalTag
from src.rules.investigation import Clue as ClueTag
from src.world.graphs import Relationship as SocialTag

__all__ = [
    "ASTRAL_DOMAINS",
    "AstralTag",
    "ClueTag",
    "GoalTag",
    "PersonalityTag",
    "PsycheTag",
    "SocialTag",
    "TAG_FAMILIES",
    "TagFamilyError",
    "register_family",
]


class TagFamilyError(ValueError):
    """A family that cannot be added: no name, no meaning, or already present."""


@dataclass(frozen=True, slots=True)
class PsycheTag:
    """A character's inner life: an enduring trait, or a state that will pass.

    ``duration`` is the distinction the author drew in #1283: *protective of sources* shapes an agent across cases;
    *shaken after the ambush* fades as events unfold. It is a word, not a timer — nothing here expires a tag on its own,
    and nothing rolls for it.
    """

    owner_id: str
    trait: str
    evidence: str = ""
    duration: str = "enduring"   # enduring | temporary

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.trait.strip():
            raise ValueError("a psyche tag needs an owner and a readable trait")
        if self.duration not in ("enduring", "temporary"):
            raise ValueError("a psyche tag is 'enduring' or 'temporary'")


#: Deprecated alias, kept so code and documents written before #1283 keep working. New code says ``PsycheTag``.
PersonalityTag = PsycheTag


#: What an Astral tag may act on. The author's sentence — "affects what someone can perceive, attempt or change" —
#: names exactly three, so the field is closed on purpose: a fourth kind of claim belongs in a new family, not in a
#: quiet amendment to this one.
ASTRAL_DOMAINS = ("perceive", "attempt", "change")


@dataclass(frozen=True, slots=True)
class AstralTag:
    """A fact about the Noösphere, and what it lets its holder notice, try or alter.

    ``source`` matters as much as the fact: an entity's testimony and an independently verified observation are
    different evidence, and #1283 asks that a clue's source be recorded once so a later scene can tell them apart. The
    tag never proves its own truth; it states what the fiction holds to be so.
    """

    owner_id: str
    fact: str
    domain: str = "perceive"
    source: str = ""

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.fact.strip():
            raise ValueError("an astral tag needs an owner and a readable fact")
        if self.domain not in ASTRAL_DOMAINS:
            raise ValueError(f"an astral tag acts on perceive, attempt or change, not {self.domain!r}")


#: The five starting families (#1283). Open: :func:`register_family` adds more.
TAG_FAMILIES: dict[str, str] = {
    "clue": "Something the investigators can follow up, with its source.",
    "social": "A relationship fact that affects an interaction: trust, obligation or access.",
    "goal": "An outcome a character or faction is pursuing.",
    "psyche": "A character's inner life: enduring traits, values, fears, habits and temporary states.",
    "astral": "A Noösphere fact that affects what someone can perceive, attempt or change.",
}


def register_family(name: str, meaning: str) -> str:
    """Add a tag family to the open list, refusing an empty name, an empty meaning or a duplicate.

    The author said the list is open, so growth is a supported operation rather than an edit to this file. It is still
    named and described: an unnamed family is a bug, and a re-used name would silently mean two things.
    """
    key = name.strip().lower()
    if not key:
        raise TagFamilyError("a tag family needs a name")
    if not meaning.strip():
        raise TagFamilyError(f"the {key!r} family needs a one-line meaning")
    if key in TAG_FAMILIES:
        raise TagFamilyError(f"the {key!r} family already exists")
    TAG_FAMILIES[key] = meaning.strip()
    return key
