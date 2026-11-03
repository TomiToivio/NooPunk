"""CWN 6.1–6.2 — magic in the city: Mage/Summoner Effort, preparation, casting, overcasting (#1068).

Implemented from *Cities Without Number, Deluxe Edition*, printed pp. 231–236, in original wording: the
arithmetic and the tables, never the rulebook's prose.

**Mage Effort** (6.1.1) = the higher of the Intelligence or Wisdom modifier plus the Cast skill level,
minimum 1, refreshed after eight uninterrupted hours of comfortable sleep — and a caster who is starved,
freezing, thirsting or sick does not refresh.

**Cyberware eats the pool** (6.2.2). Each implant costs its System Strain *and at least one point*: the
book's worked example (implants at 2, 0 and 0.5 costing four points) only balances under that reading, so
the example is treated as evidence about the rule rather than as an error to be flagged. A mage who wants
their pool back removes the chrome.

Three commitment durations exist and are not interchangeable: ``day`` returns the next morning, ``scene``
at the end of the scene, ``duration`` whenever the caster spends an Instant action to reclaim it — and the
effect it fuelled ends the moment they do.

Optional overlay, like the psionic packages: a campaign without magic never constructs a pool, and nothing
here is imported by the immutable core.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

from .cwn_character import attribute_modifier

#: The three commitment durations, in the order the book presents them.
COMMITMENTS = ("day", "scene", "duration")

#: Overcasting bands (p. 232): inclusive lower bound, inclusive upper bound (None = open), consequence.
OVERCAST_TABLE: tuple[tuple[int, int | None, str], ...] = (
    (1, 1, "death"),
    (2, 4, "mortal_wound"),
    (5, 8, "unconscious_minute_4_strain"),
    (9, 15, "stunned_2_strain"),
    (16, 19, "lost_main_action_1_strain"),
    (20, None, "1_strain"),
)

#: System Strain each overcasting band inflicts.
OVERCAST_STRAIN = {"death": 0, "mortal_wound": 0, "unconscious_minute_4_strain": 4,
                   "stunned_2_strain": 2, "lost_main_action_1_strain": 1, "1_strain": 1}

#: Learning prices the book names (p. 231): a tutor, or a grimoire.
TUTOR_COST = 5000
GRIMOIRE_COST = 10000


class MagicError(ValueError):
    pass


def cyberware_penalty(strain_costs: Sequence[float]) -> int:
    """Effort lost to implants: each costs its System Strain, and at least one point each.

    The book's example (2, 0 and 0.5 → "lose four points") is the reason for the per-implant floor: a
    sum-then-round reading gives three, and would make the book contradict itself.
    """
    penalty = 0
    for cost in strain_costs:
        if cost < 0:
            raise MagicError("System Strain cannot be negative")
        penalty += max(1, math.ceil(cost))
    return penalty


def mage_effort(*, intelligence: int, wisdom: int, cast_skill: int,
                strain_costs: Sequence[float] = ()) -> int:
    """Max Mage Effort = max(INT, WIS modifier) + Cast, minimum 1, less every implant (6.1.1, 6.2.2)."""
    if cast_skill < 0:
        raise MagicError("Cast skill cannot be negative")
    if intelligence <= 0 or wisdom <= 0:
        raise MagicError("attributes must be positive")
    base = max(attribute_modifier(intelligence), attribute_modifier(wisdom)) + cast_skill
    return max(1, base - cyberware_penalty(strain_costs))


def summoner_effort(*, constitution: int, charisma: int, summon_skill: int,
                    strain_costs: Sequence[float] = ()) -> int:
    """Summoner Effort = max(CON, CHA modifier) + Summon, minimum 1, less every implant (6.2.1)."""
    if summon_skill < 0:
        raise MagicError("Summon skill cannot be negative")
    if constitution <= 0 or charisma <= 0:
        raise MagicError("attributes must be positive")
    base = max(attribute_modifier(constitution), attribute_modifier(charisma)) + summon_skill
    return max(1, base - cyberware_penalty(strain_costs))


def prepared_slots(level: int, cast_skill: int) -> int:
    """ceil(level / 2) + Cast (p. 231): the book's level-1 and level-10 examples are tests."""
    if level < 1 or cast_skill < 0:
        raise MagicError("level is at least 1 and skill levels are not negative")
    return math.ceil(level / 2) + cast_skill


def can_cast(*, free_hand: bool, can_speak: bool, disturbed: bool = False) -> bool:
    """One hand free, a voice, and no hit-point damage or grappling in the round (6.1.3.1)."""
    return bool(free_hand and can_speak and not disturbed)


def overcast_total(*, die: int, cast_skill: int = 0, constitution_mod: int = 0,
                   day_commitment: bool = False) -> int:
    """The overcasting total: 1d20 + Cast skill + Con modifier, -2 for a day-long commitment (6.1.4).

    The single implementation of that arithmetic. ``EffortPool.overcast_roll`` and the spell corpus in
    ``cwn_spells`` both call it, so the two cannot drift into two answers for one roll.
    """
    if not 1 <= die <= 20:
        raise MagicError("overcasting is resolved on a d20")
    return die + cast_skill + constitution_mod - (2 if day_commitment else 0)


def overcast_result(total: int) -> dict:
    """Map 1d20 + Cast + Con (−2 for a day-commitment spell) onto the overcasting table."""
    for low, high, consequence in OVERCAST_TABLE:
        if total >= low and (high is None or total <= high):
            return {"consequence": consequence, "strain": OVERCAST_STRAIN[consequence]}
    raise MagicError("an overcasting roll cannot be below 1")


@dataclass
class EffortPool:
    """One caster's pool, kept separate per class: a mage cannot borrow a summoner's Effort."""

    maximum: int
    label: str = "mage"
    _committed: dict[str, int] = field(default_factory=lambda: {k: 0 for k in COMMITMENTS})

    def __post_init__(self) -> None:
        if self.maximum < 1:
            raise MagicError("an Effort pool is at least 1")

    @property
    def available(self) -> int:
        return self.maximum - sum(self._committed.values())

    @property
    def committed(self) -> dict[str, int]:
        return dict(self._committed)

    @property
    def total_committed(self) -> int:
        return sum(self._committed.values())

    def commit(self, amount: int, *, duration: str) -> None:
        if duration not in COMMITMENTS:
            raise MagicError(f"unknown commitment {duration!r}")
        if amount < 0:
            raise MagicError("cannot commit negative Effort")
        if amount > self.available:
            raise MagicError(f"only {self.available} Effort available, {amount} requested")
        self._committed[duration] += amount

    def end_scene(self) -> int:
        released, self._committed["scene"] = self._committed["scene"], 0
        return released

    def reclaim_duration(self) -> int:
        """Instant action; whatever the Effort fuelled ends immediately."""
        released, self._committed["duration"] = self._committed["duration"], 0
        return released

    def refresh_morning(self, *, slept_eight_hours: bool = True, comfortable: bool = True) -> bool:
        """Day commitments and everything else return — but only after an undisturbed night."""
        if not slept_eight_hours or not comfortable:
            return False
        self._committed = {k: 0 for k in COMMITMENTS}
        return True

    def overcast_roll(self, die: int, *, cast_skill: int = 0, constitution_mod: int = 0,
                      day_commitment: bool = False) -> dict:
        """1d20 + Cast + Con mod, −2 for a day-commitment spell (6.1.4)."""
        total = overcast_total(die=die, cast_skill=cast_skill, constitution_mod=constitution_mod,
                              day_commitment=day_commitment)
        result = overcast_result(total)
        result.update({"die": die, "total": total})
        return result


@dataclass
class Spellbook:
    """What a caster has learned and prepared. Prepared spells are drawn from learned ones."""

    level: int
    cast_skill: int
    known: list[str] = field(default_factory=list)
    prepared: list[str] = field(default_factory=list)

    @property
    def slots(self) -> int:
        return prepared_slots(self.level, self.cast_skill)

    def learn(self, spell: str) -> None:
        """One week of practice with a tutor or grimoire; the price is the caller's business."""
        if spell in self.known:
            raise MagicError(f"{spell!r} is already known")
        self.known.append(spell)

    def prepare(self, spells: Sequence[str]) -> None:
        if len(spells) > self.slots:
            raise MagicError(f"{self.slots} slots at level {self.level} with Cast-{self.cast_skill}")
        unknown = [spell for spell in spells if spell not in self.known]
        if unknown:
            raise MagicError(f"cannot prepare unlearned spells: {', '.join(unknown)}")
        if len(set(spells)) != len(spells):
            raise MagicError("the same spell prepared twice still takes one slot")
        self.prepared = list(spells)

    def cast(self, spell: str, pool: EffortPool, *, duration: str = "scene", overcast: bool = False,
             free_hand: bool = True, can_speak: bool = True, disturbed: bool = False) -> dict:
        """Cast a prepared spell: one Effort committed unless this is an overcast."""
        if spell not in self.prepared:
            raise MagicError(f"{spell!r} is not prepared")
        if not can_cast(free_hand=free_hand, can_speak=can_speak, disturbed=disturbed):
            raise MagicError("the caster needs a free hand, a voice and a steady round")
        if overcast:
            return {"spell": spell, "effort": 0, "overcast": True, "commitment": "scene",
                    "note": "a duration-committed spell overcast lasts one scene"}
        pool.commit(1, duration=duration)
        return {"spell": spell, "effort": 1, "overcast": False, "commitment": duration}
