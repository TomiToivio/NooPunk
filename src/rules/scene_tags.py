"""The five NoöPunk tag families, without a second character sheet or rules engine.

Clue, Social and Goal are the existing canonical records. **Psyche** (formerly
Personality) is a descriptive, non-mechanical tag: it records a character's
inner life — traits, values, fears, habits and temporary states. **Astral** is a
descriptive fact about the Noösphere: what someone can perceive, attempt or
change through PSI, Magick, psychotronics, panpsychism or Law of One phenomena.
Neither adds a modifier, an emotion meter or a new dice procedure. The host RPG
(CWN by default, another cyberpunk RPG by agreement) still resolves action.
"""

from dataclasses import dataclass

from src.rules.goals import Goal as GoalTag
from src.rules.investigation import Clue as ClueTag
from src.world.graphs import Relationship as SocialTag


@dataclass(frozen=True, slots=True)
class PersonalityTag:
    """A Psyche tag: a stable or temporary inner-life fact, not a stat or mind-control switch.

    The class keeps its historical name for save compatibility. New text should
    call the family **Psyche** and use :data:`PsycheTag`.
    """

    owner_id: str
    trait: str
    evidence: str = ""
    #: The distinction #1283 draws: *protective of sources* endures across cases; *shaken after the ambush* passes.
    #: A word, not a timer — nothing here expires a tag, and nothing rolls for it.
    duration: str = "enduring"   # enduring | temporary

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.trait.strip():
            raise ValueError("psyche tags require an owner and a readable trait")
        if self.duration not in ("enduring", "temporary"):
            raise ValueError("a psyche tag is 'enduring' or 'temporary'")


#: What an Astral tag may act on — the three the author named in #1283.
ASTRAL_DOMAINS = ("perceive", "attempt", "change")

#: What each starting family records, keyed by the lowercase family name. ``TAG_FAMILIES`` above is the author-facing
#: list; this is the same five, written out, so ``register_family`` can add a sixth without editing a table here.
TAG_FAMILY_MEANINGS: dict[str, str] = {
    "clue": "Something the investigators can follow up, with its source.",
    "social": "A relationship fact that affects an interaction: trust, obligation or access.",
    "goal": "An outcome a character or faction is pursuing.",
    "psyche": "A character's inner life: enduring traits, values, fears, habits and temporary states.",
    "astral": "A Noösphere fact that affects what someone can perceive, attempt or change.",
}


class TagFamilyError(ValueError):
    """A family that cannot be added: no name, no meaning, or already present."""


def register_family(name: str, meaning: str) -> str:
    """Add a tag family to the open list, refusing an empty name, an empty meaning or a duplicate.

    The author said the five are a starting vocabulary, not a closed list (#1283). Growth is therefore a supported
    operation: the display name joins :data:`TAG_FAMILIES` and the meaning joins :data:`TAG_FAMILY_MEANINGS`, so a later
    reader can still tell what the family records. An unnamed family is a bug; a re-used name would mean two things.
    """
    global TAG_FAMILIES
    key = name.strip().lower()
    if not key:
        raise TagFamilyError("a tag family needs a name")
    if not meaning.strip():
        raise TagFamilyError(f"the {key!r} family needs a one-line meaning")
    if key in TAG_FAMILY_MEANINGS:
        raise TagFamilyError(f"the {key!r} family already exists")
    TAG_FAMILY_MEANINGS[key] = meaning.strip()
    TAG_FAMILIES = TAG_FAMILIES + (name.strip().title(),)
    return key


#: The author-facing name from #1283. ``PersonalityTag`` remains the serialized class name so
#: existing lifepath saves and dossiers do not fork.
PsycheTag = PersonalityTag


@dataclass(frozen=True, slots=True)
class AstralTag:
    """A fact about the Noösphere attached to a person, place, device or relationship.

    ``fact`` is what is true in the fiction (for example “someone is still waiting here”).
    ``subject`` optionally names what the fact is about; ``evidence`` records how the character
    learned it. The tag creates no rank, point pool, power list or automatic effect: a table reads
    it to establish what is possible, then uses the host RPG's procedure if the outcome is uncertain.
    """

    owner_id: str
    fact: str
    subject: str = ""
    evidence: str = ""
    #: What the fact lets someone do, from the three the author named. Closed on purpose: a fourth kind of claim
    #: belongs in a new family, not in a quiet amendment to this one.
    domain: str = "perceive"   # perceive | attempt | change

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.fact.strip():
            raise ValueError("astral tags require an owner and a readable fact")
        if self.domain not in ASTRAL_DOMAINS:
            raise ValueError(f"an astral tag acts on perceive, attempt or change, not {self.domain!r}")


#: The starting families from the author decision (#1283). The list is open: new families are
#: named when a campaign needs them, not invented in advance.
TAG_FAMILIES: tuple[str, ...] = ("Clue", "Social", "Goal", "Psyche", "Astral")

__all__ = [
    "TAG_FAMILIES",
    "AstralTag",
    "ClueTag",
    "GoalTag",
    "PersonalityTag",
    "PsycheTag",
    "SocialTag",
]
