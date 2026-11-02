"""CWN optional rule: magic in the city — mage Effort, preparation, casting, overcasting (#1068).

Source: *Cities Without Number, Deluxe Edition*, printed pp. 231–236 (Mages and Spellcasting; the spell
list's Effort/Duration table) and pp. 236–239 (summoners' Effort). Paraphrased mechanics; no rulebook
prose is reproduced. The spell *effects* are content, not engine — this module implements the economy
that every spell obeys.

The model in one paragraph: a mage's Cast skill plus the better of Intelligence or Wisdom sets their
Mage Effort; Effort is committed for the day, the scene, or the spell's duration; prepared spells are
ceil(level/2) + Cast; cybernetics cut the pool (at least a point each); and a desperate caster can
overcast an Effort-free spell at the risk of a roll on a table that runs from one point of System
Strain to outright death.

Nothing here touches the immutable CWN core: it is a self-contained optional module, like the psionic
packages, and a campaign without magic never constructs a :class:`Mage`.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum

#: Overcasting outcome bands, printed p. 232. (lower bound inclusive, upper bound inclusive, consequence)
OVERCAST_TABLE: tuple[tuple[int, int | None, str], ...] = (
    (1, 1, "death"),
    (2, 4, "mortal_wound"),
    (5, 8, "unconscious_minute_4_strain"),
    (9, 15, "stunned_2_strain"),
    (16, 19, "lost_main_action_1_strain"),
    (20, None, "1_strain"),
)

#: System Strain each overcast band adds, so a caller can apply it without re-reading prose.
OVERCAST_STRAIN = {"death": 0, "mortal_wound": 0, "unconscious_minute_4_strain": 4,
                   "stunned_2_strain": 2, "lost_main_action_1_strain": 1, "1_strain": 1}

TUTOR_COST = 5000
GRIMOIRE_COST = 10000


class MagicError(ValueError):
    pass


class Commitment(str, Enum):
    DAY = "day"        # returns next morning
    SCENE = "scene"    # returns at the end of the scene
    DURATION = "duration"  # reclaimable as an Instant action; the effect ends when it is


def cyber_effort_penalty(strain_costs: Sequence[float]) -> int:
    """Effort lost to implants: the System Strain of each, and at least one point per implant.

    The book's example (implants with stain costs 2, 0 and 0.5 costing four points of maximum Effort)
    only balances under the "at least one" reading, which is why it is a named rule rather than a comment.
    """
    penalty = 0
    for cost in strain_costs:
        if cost < 0:
            raise MagicError("System Strain costs cannot be negative")
        penalty += max(1, math.ceil(cost))
    return penalty


def mage_effort_max(int_mod: int, wis_mod: int, cast_skill: int,
                    *, cyber_strain_costs: Sequence[float] = ()) -> int:
    """Maximum Mage Effort (printed p. 231): max(Int, Wis) + Cast, minus every implant, minimum 1."""
    if cast_skill < 0:
        raise MagicError("skill levels are not negative")
    base = max(int_mod, wis_mod) + cast_skill
    return max(1, base - cyber_effort_penalty(cyber_strain_costs))


def summoner_effort_max(con_mod: int, cha_mod: int, summon_skill: int,
                        *, cyber_strain_costs: Sequence[float] = ()) -> int:
    """Summoner Effort: the better of Constitution or Charisma, plus Summon, minimum 1 (p. 236)."""
    if summon_skill < 0:
        raise MagicError("skill levels are not negative")
    base = max(con_mod, cha_mod) + summon_skill
    return max(1, base - cyber_effort_penalty(cyber_strain_costs))


def prepared_slots(level: int, cast_skill: int) -> int:
    """ceil(level / 2) + Cast (printed p. 231)."""
    if level < 1 or cast_skill < 0:
        raise MagicError("level is at least 1 and skill levels are not negative")
    return math.ceil(level / 2) + cast_skill


def overcast_result(total: int) -> dict:
    """Map 1d20 + Cast + Con (−2 for day-commitment) onto the overcasting table."""
    for low, high, consequence in OVERCAST_TABLE:
        if total >= low and (high is None or total <= high):
            return {"consequence": consequence, "strain": OVERCAST_STRAIN[consequence]}
    raise MagicError("an overcasting roll cannot be below 1")


@dataclass
class Mage:
    """A spellcaster's bookkeeping. Prepared spells are learned ones; Effort is committed, not spent."""

    level: int
    cast_skill: int
    int_mod: int
    wis_mod: int
    con_mod: int = 0
    known: list[str] = field(default_factory=list)
    prepared: list[str] = field(default_factory=list)
    #: Committed Effort, by commitment kind, so recovery knows what may come back.
    committed: dict[str, int] = field(default_factory=lambda: {k.value: 0 for k in Commitment})
    cyber_strain_costs: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.known:
            self.known = []
        if len(set(self.known)) != len(self.known):
            raise MagicError("a spell is learned once")
        if len(self.prepared) > self.slots:
            raise MagicError("prepared spells exceed the slots available")
        for spell in self.prepared:
            if spell not in self.known:
                raise MagicError(f"{spell!r} is prepared but not learned")

    # -- pools ----------------------------------------------------------------------
    @property
    def effort_max(self) -> int:
        return mage_effort_max(self.int_mod, self.wis_mod, self.cast_skill,
                               cyber_strain_costs=self.cyber_strain_costs)

    @property
    def committed_total(self) -> int:
        return sum(self.committed.values())

    @property
    def effort_free(self) -> int:
        return self.effort_max - self.committed_total

    @property
    def slots(self) -> int:
        return prepared_slots(self.level, self.cast_skill)

    # -- spells ---------------------------------------------------------------------
    def learn(self, spell: str) -> None:
        if spell in self.known:
            raise MagicError(f"{spell!r} is already known")
        self.known.append(spell)

    def prepare(self, spells: list[str]) -> None:
        """Fill the slots; the book allows changing them only when Effort refreshes."""
        if len(spells) > self.slots:
            raise MagicError(f"{self.slots} prepared slots at level {self.level} with Cast-{self.cast_skill}")
        unknown = [spell for spell in spells if spell not in self.known]
        if unknown:
            raise MagicError(f"cannot prepare unlearned spells: {', '.join(unknown)}")
        if len(set(spells)) != len(spells):
            raise MagicError("the same spell prepared twice still takes one slot")
        self.prepared = list(spells)

    # -- casting --------------------------------------------------------------------
    def can_cast(self, *, hands_free: bool = True, can_speak: bool = True,
                 disturbed: bool = False) -> bool:
        """One free hand, a voice, and no damage/grapple in the round (printed p. 232)."""
        return hands_free and can_speak and not disturbed

    def cast(self, spell: str, commitment: Commitment, *, overcast: bool = False,
             check: dict | None = None) -> dict:
        """Cast a prepared spell, committing Effort unless overcasting.

        `check` carries the caller's already-resolved casting conditions (hands_free, can_speak,
        disturbed) because those are scene state, not caster state.
        """
        if spell not in self.prepared:
            raise MagicError(f"{spell!r} is not prepared")
        conditions = check or {}
        if not self.can_cast(**conditions):
            raise MagicError("the caster lacks a free hand, a voice, or a steady round")
        if overcast:
            return {"spell": spell, "effort": 0, "overcast": True,
                    "commitment": Commitment.SCENE.value}
        cost = 1
        if self.effort_free < cost:
            raise MagicError("not enough free Mage Effort to commit")
        self.committed[commitment.value] += cost
        return {"spell": spell, "effort": cost, "overcast": False, "commitment": commitment.value}

    def overcast_roll(self, die: int, *, day_commitment: bool = False) -> dict:
        """The die is 1d20; Cast and Con are added, and a day-commitment spell subtracts 2."""
        if not 1 <= die <= 20:
            raise MagicError("overcasting is resolved on a d20")
        total = die + self.cast_skill + self.con_mod - (2 if day_commitment else 0)
        result = overcast_result(total)
        result.update({"die": die, "total": total})
        return result

    def struck_while_casting(self) -> dict:
        """A held action that lands mid-cast: the spell is lost and the Effort is wasted."""
        return {"spell_lost": True, "effort_wasted": True}

    # -- recovery -------------------------------------------------------------------
    def reclaim_duration(self) -> int:
        """Commitment for the duration can be reclaimed at will; the effect ends when it is."""
        amount = self.committed[Commitment.DURATION.value]
        self.committed[Commitment.DURATION.value] = 0
        return amount

    def end_scene(self) -> int:
        amount = self.committed[Commitment.SCENE.value]
        self.committed[Commitment.SCENE.value] = 0
        return amount

    def refresh(self, *, rested: bool = True) -> int:
        """Eight undisturbed hours in reasonable comfort; day Effort and everything else returns."""
        if not rested:
            raise MagicError("Mage Effort needs a full night's rest to refresh")
        self.committed = {k.value: 0 for k in Commitment}
        return self.effort_max


def summoner_spirit_binding(*, effort: int, controlled: bool = True) -> dict:
    """Summoner Effort bound in a spirit stays spent until the morning after it is dispelled (p. 236).

    The spirit *statistics* are content; what this pins is the accounting a caller must not get wrong.
    """
    if effort < 1:
        raise MagicError("binding a spirit costs at least one Summoner Effort")
    return {"effort_bound": effort, "dispellable": True,
            "recovers": "morning after the spirit is dispelled",
            "dismissed_but_bound_still_drains": True}
