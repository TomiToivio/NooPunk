"""CWN 6.4 — Magical items: identification and linking (issue #1068).

Two mechanics, both small and both load-bearing:

* **Identification** (6.4.1). Any magically-active observer can feel that an object is magical by touch, but not
  what it does. Discerning the effect needs either the item's minimum magic skill level, or — for an item without
  one — a day's study by anyone with Cast-0 or Summon-0.
* **Linking** (6.4.2). A Main Action, one **permanent** point of System Strain while linked, and for mages and
  summoners an additional **permanently committed Effort point** that returns the morning after the link ends.

The rule people forget: a non-arcanist without Cast or Summon skill cannot link an item unaided. They need someone
with a magical Edge to do it or to guide them — purely intellectual knowledge of the process is enough, so the
guide does not have to be an active caster.
"""
from __future__ import annotations

from dataclasses import dataclass


class MagicItemError(ValueError):
    """A rule was about to be broken."""


def can_sense_magic(*, has_magical_edge: bool, cast_skill: int = 0, summon_skill: int = 0) -> bool:
    """Feeling that an item is magical by touch: any Graced, mage or summoner."""
    return bool(has_magical_edge or cast_skill or summon_skill)


def can_identify(*, minimum_magic_skill: int | None, cast_skill: int = 0, summon_skill: int = 0,
                 days_of_study: int = 0) -> bool:
    """6.4.1: the item's minimum skill, or a day's study for an item without one."""
    best = max(cast_skill, summon_skill)
    if minimum_magic_skill is not None:
        return best >= minimum_magic_skill
    # No minimum: Cast-0 or Summon-0 plus a day's study is enough.
    return best >= 0 and days_of_study >= 1


def can_link_unaided(*, cast_skill: int = 0, summon_skill: int = 0) -> bool:
    """6.4.2: an intellectual knowledge of the process is enough — Cast-0 or Summon-0 qualifies."""
    return max(cast_skill, summon_skill) > 0


@dataclass
class LinkedItem:
    """The bookkeeping the rules actually require while an item is worn."""
    name: str
    linked: bool = False
    strain_committed: int = 0
    effort_committed: int = 0
    effort_committed_until: str = ""        # morning after the link ends
    arcanist: bool = False

    def link(self, *, guided: bool = False, cast_skill: int = 0, summon_skill: int = 0) -> "LinkedItem":
        if self.linked:
            raise MagicItemError("already linked")
        if not (can_link_unaided(cast_skill=cast_skill, summon_skill=summon_skill) or guided):
            raise MagicItemError("linking needs Cast/Summon skill or a magical guide")
        self.linked = True
        self.strain_committed = 1
        if self.arcanist:
            self.effort_committed = 1
        return self

    def unlink(self) -> dict:
        """Strain returns now; a committed Effort point returns the following morning."""
        if not self.linked:
            raise MagicItemError("not linked")
        self.linked = False
        returned_effort = self.effort_committed
        self.strain_committed = 0
        self.effort_committed = 0
        self.effort_committed_until = "next_morning" if returned_effort else ""
        return {"effort_returns": returned_effort, "when": self.effort_committed_until}
