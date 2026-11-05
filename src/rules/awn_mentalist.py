"""AWN Deluxe Mentalist Edge at campaign start (printed pp.264-269).

No SWN discipline is conferred. Mentalist has its own arts and Effort accounting;
other CWN/SWN character machinery stays authoritative. Art effects use the book.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class MentalistError(ValueError):
    pass


ARTS_BY_LEVEL = {**{level: 1 for level in range(2, 10)}, 1: 2, 10: 2}


@dataclass(frozen=True)
class Art:
    name: str
    discipline: str
    greater: bool = False
    source_page: int = 266

    def __post_init__(self) -> None:
        if not self.name or not self.discipline or not 266 <= self.source_page <= 269:
            raise MentalistError("art must be sourced from AWN Deluxe pp.266-269")


@dataclass
class Mentalist:
    actor_id: str
    character_level: int = 1
    mentalism_skill: int = 0
    wisdom_modifier: int = 0
    charisma_modifier: int = 0
    arts: list[Art] = field(default_factory=list)
    effort_scene: int = 0
    effort_day: int = 0
    focused_discipline: str | None = None
    extra_effort: int = 0

    def __post_init__(self) -> None:
        if not self.actor_id or not 1 <= self.character_level <= 10:
            raise MentalistError("Mentalist needs an actor and level 1..10")
        if self.mentalism_skill < 0:
            raise MentalistError("Mentalism skill must be nonnegative")

    @property
    def effort_max(self) -> int:
        return max(0, 1 + self.mentalism_skill
                   + max(self.wisdom_modifier, self.charisma_modifier)
                   + self.extra_effort)

    @property
    def arts_limit(self) -> int:
        return sum(ARTS_BY_LEVEL[level] for level in range(1, self.character_level + 1))

    def learn(self, art: Art) -> None:
        if len(self.arts) >= self.arts_limit or any(a.name == art.name for a in self.arts):
            raise MentalistError("art slots exhausted or art already learned")
        if self.focused_discipline and art.discipline != self.focused_discipline:
            raise MentalistError("Focused Mind limits arts to a single discipline")
        if art.greater:
            lesser = sum(1 for a in self.arts if a.discipline == art.discipline and not a.greater)
            greater = sum(1 for a in self.arts if a.discipline == art.discipline and a.greater)
            if lesser < 2 * (greater + 1):
                raise MentalistError("each greater art requires two lesser arts of that discipline")
        self.arts.append(art)

    def commit(self, *, duration: str, amount: int = 1) -> None:
        if duration not in ("scene", "day") or amount <= 0:
            raise MentalistError("Effort requires scene/day duration and positive amount")
        if self.effort_scene + self.effort_day + amount > self.effort_max:
            raise MentalistError("insufficient Mentalist Effort")
        if duration == "scene":
            self.effort_scene += amount
        else:
            self.effort_day += amount

    def end_scene(self) -> None:
        self.effort_scene = 0

    def sleep(self, *, comfortable: bool) -> None:
        if comfortable:
            self.effort_day = 0

    def check_cyberware(self, *, nerve_type: bool) -> None:
        if nerve_type:
            raise MentalistError("AWN Mentalist may not implant CWN Nerve-type cyberware (p.265)")


def create_first_level_mentalist(actor_id: str, lesser_arts: tuple[Art, Art],
                                *, wisdom_modifier: int = 0,
                                charisma_modifier: int = 0) -> Mentalist:
    """AWN p.265: Mentalism-0 and two lesser arts, chosen at first level."""
    character = Mentalist(actor_id, wisdom_modifier=wisdom_modifier,
                          charisma_modifier=charisma_modifier)
    if len(lesser_arts) != 2 or any(a.greater for a in lesser_arts):
        raise MentalistError("first-level Mentalist selects two lesser arts")
    for art in lesser_arts:
        character.learn(art)
    return character
