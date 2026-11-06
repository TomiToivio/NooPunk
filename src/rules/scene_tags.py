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

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.trait.strip():
            raise ValueError("psyche tags require an owner and a readable trait")


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

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.fact.strip():
            raise ValueError("astral tags require an owner and a readable fact")


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
