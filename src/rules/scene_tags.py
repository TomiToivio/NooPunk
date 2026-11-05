"""The four NoöPunk tag types, without a second character sheet or rules engine.

Social, Goal and Clue are the existing canonical records. Personality is a
descriptive, non-mechanical tag: all persuasion, interrogation, faction and
investigation actions still use the published CWN procedures and established
NoöPunk investigation module. No emotion meters or new dice.
"""
from dataclasses import dataclass

from src.world.graphs import Relationship as SocialTag
from src.rules.goals import Goal as GoalTag
from src.rules.investigation import Clue as ClueTag


@dataclass(frozen=True, slots=True)
class PersonalityTag:
    """A stable playable characterization, not a stat, roll or mind-control switch."""

    owner_id: str
    trait: str
    evidence: str = ""

    def __post_init__(self) -> None:
        if not self.owner_id.strip() or not self.trait.strip():
            raise ValueError("personality tags require an owner and a readable trait")


__all__ = ["SocialTag", "GoalTag", "ClueTag", "PersonalityTag"]
