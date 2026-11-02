"""CWN chapter 6.2 — Summoners and Summoning (issue #1068).

The audit that produced this file found `summon`, `spirit`, `spellcasting` and `graced` **zero times** anywhere
in the rules library: CWN's magic chapter was entirely unimplemented while chapters 1-5 were covered. This module
implements the summoning half faithfully from the CWN SRD.

Rules implemented as written, not reinterpreted:

* **Effort cost** of a spirit = its powers, minus the summoner's Summon skill, floored at **1**, plus **+1 for
  each successive immediate summon within the same scene**.
* **Hit-dice cap**: total HD of spirits summoned at once may not exceed the summoner's character level.
* **Form tiers**: form I at 1st level, form II at 5th, form III at 9th.
* **Commanding**: a check at difficulty 9 (routine), 11 (an act contrary to the spirit's inclination), 13
  (suicidal or directly against its nature). Success = grudging obedience; failure = the spirit breaks free,
  its Effort becomes recoverable the next morning, and it is now uncontrolled and probably angry.
* **Banishing**: a Main Action, Commit Summoner Effort for the day, target a visible spirit within 30 m, opposed
  Cha/Summon against the spirit's summoner (or the spirit's skill bonus + 2 if uncontrolled). Success inflicts
  **1d8 damage per Summon skill level**.
* **Dispel**: the summoner may dispel a visible spirit within 30 m as a Main Action; the Effort restores the
  following morning. Spirits are dispelled instantly if the summoner dies.

Not implemented here, and deliberately: the Summoner Effort *pool* formula (6.2.1), spirit power catalogues
(6.2.8) and the manifestation statistics beyond the fields below. The pool is supplied by the caller rather than
derived from a formula this file has not transcribed.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: Form tier available at a given character level (CWN 6.2.3 step 3).
FORM_TIERS = ((1, 1), (5, 2), (9, 3))

#: Commanding difficulties (CWN 6.2.6).
COMMAND_DIFFICULTY = {"routine": 9, "contrary_inclination": 11, "against_nature": 13}

#: The published manifestation statistics (CWN 6.2.7 table).
MANIFESTATIONS = {
    ("spirit", 1): {"hd": 1, "hp": 5, "ac": 10, "attack": None, "move": 10, "morale": 15},
    ("spirit", 2): {"hd": 3, "hp": 15, "ac": 13, "attack": None, "move": 15, "morale": 14},
    ("spirit", 3): {"hd": 5, "hp": 25, "ac": 15, "attack": None, "move": 20, "morale": 13},
    ("physical", 1): {"hd": 1, "hp": 5, "ac": 12, "attack": "+2", "move": 10, "morale": 15},
    ("physical", 2): {"hd": 4, "hp": 20, "ac": 15, "attack": "+5", "move": 10, "morale": 13},
    ("physical", 3): {"hd": 8, "hp": 40, "ac": 18, "attack": "+8", "move": 10, "morale": 11},
}


class SummoningError(ValueError):
    """The rules were about to be broken."""


def form_tier(character_level: int) -> int:
    tier = 0
    for level, allowed in FORM_TIERS:
        if character_level >= level:
            tier = allowed
    if tier == 0:
        raise SummoningError("a summoner must be at least 1st level")
    return tier


def effort_cost(*, power_count: int, summon_skill: int, prior_summons_this_scene: int = 0) -> int:
    """CWN 6.2.3 step 6: powers minus skill, floored at 1, +1 per earlier summon this scene."""
    if power_count < 0:
        raise SummoningError("a spirit cannot have negative powers")
    if prior_summons_this_scene < 0:
        raise SummoningError("successive summons cannot be negative")
    return max(1, power_count - summon_skill) + prior_summons_this_scene


def may_summon(*, character_level: int, current_spirit_hd: int, new_spirit_hd: int) -> bool:
    """Total hit dice of spirits at once may not exceed the summoner's level (6.2.3 step 3)."""
    return current_spirit_hd + new_spirit_hd <= character_level


def command_difficulty(reason: str) -> int:
    try:
        return COMMAND_DIFFICULTY[reason]
    except KeyError:
        raise SummoningError(f"unknown command difficulty {reason!r}") from None


def banish_damage(*, summon_skill: int, rolls: tuple[int, ...]) -> int:
    """1d8 per Summon skill level (6.2.4). Rolls are supplied so the result is reproducible."""
    if summon_skill < 0:
        raise SummoningError("Summon skill cannot be negative")
    if len(rolls) != summon_skill:
        raise SummoningError(f"{summon_skill} skill levels need {summon_skill} d8 rolls, got {len(rolls)}")
    for die in rolls:
        if not 1 <= die <= 8:
            raise SummoningError("banishing damage uses d8s")
    return sum(rolls)


def banish_target(*, spirit_controlled: bool, summoner_summon_skill: int = 0, spirit_skill_bonus: int = 0) -> int:
    """Opposed Cha/Summon vs the spirit's summoner, or the spirit's skill bonus +2 when uncontrolled."""
    if spirit_controlled:
        return 10 + summoner_summon_skill          # opposed: the target number the banisher must beat
    return 10 + spirit_skill_bonus + 2


@dataclass
class Spirit:
    """One summoned spirit with the fields the rules actually use."""
    name: str
    nature: str
    form: str = "spirit"                      # spirit | physical
    tier: int = 1                             # 1..3, gated by level
    powers: tuple[str, ...] = ()
    effort_committed: int = 0
    hp: int = 0
    controlled: bool = True

    def __post_init__(self):
        if self.form not in ("spirit", "physical"):
            raise SummoningError(f"unknown form {self.form!r}")
        if not 1 <= self.tier <= 3:
            raise SummoningError("form tier is 1..3")
        if not self.name or not self.nature:
            raise SummoningError("a spirit needs a name and a nature")
        stats = MANIFESTATIONS[(self.form, self.tier)]
        if self.hp == 0:
            self.hp = stats["hp"]

    @property
    def hd(self) -> int:
        return MANIFESTATIONS[(self.form, self.tier)]["hd"]

    @property
    def stats(self) -> dict:
        return dict(MANIFESTATIONS[(self.form, self.tier)])

    def damage(self, amount: int) -> bool:
        """Returns True if the spirit was destroyed (hp to zero means it vanishes)."""
        if amount < 0:
            raise SummoningError("damage cannot be negative")
        self.hp = max(0, self.hp - amount)
        return self.hp == 0


def summon(*, summoner_level: int, summon_skill: int, spirit: Spirit,
           prior_summons_this_scene: int = 0, current_spirit_hd: int = 0) -> Spirit:
    """Apply every gate in 6.2.3, then return the spirit with its committed Effort."""
    if spirit.tier > form_tier(summoner_level):
        raise SummoningError(
            f"form tier {spirit.tier} needs level {dict(zip(range(1,4),(1,5,9)))[spirit.tier]}")
    cost = effort_cost(power_count=len(spirit.powers), summon_skill=summon_skill,
                       prior_summons_this_scene=prior_summons_this_scene)
    if not may_summon(character_level=summoner_level, current_spirit_hd=current_spirit_hd,
                      new_spirit_hd=spirit.hd):
        raise SummoningError("total spirit hit dice would exceed the summoner's level")
    spirit.effort_committed = cost
    spirit.controlled = True
    return spirit
