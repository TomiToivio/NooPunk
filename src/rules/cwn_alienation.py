"""CWN optional rule: cybernetic Alienation, chrome syndromes and cyber-induced psychosis (#1068).

Source: *Cities Without Number, Deluxe Edition*, printed pp. 226–231. This is an **opt-in module**: the
default CWN rules say chrome does not change a user's thinking, and nothing here attaches itself to the
cyberware procedures unless a campaign turns it on. Paraphrased mechanics, no rulebook text copied.

The **table** and the two arithmetic rules are not restated here: `cwn_cyberware` already implements
Alienation under the base rules (SRD "Cyberware Alienation"), and after #1068 there were two copies whose
syndrome bonuses had already diverged — this module said Stressed was worth +3, the SRD and
`cwn_cyberware` both say +5. The table now comes from `cwn_cyberware` and this module keeps only what the
optional rule adds: the accumulating score with its floor, the check/save cycle as one object, and the
rescue procedure the base module leaves to the GM.

The shape of the rule, in one paragraph: Alienation is spent like System Strain but accumulates. Adding
a system costs its System Strain rounded up (+2 for Nerveware); a chrome syndrome raises the ceiling by
its listed amount; the ceiling is Wisdom plus those bonuses. Fighting a syndrome forces a 1d20 check —
roll at or under your Alienation and it rises by one, and a rise past the ceiling forces a Mental save
(new syndrome on success, psychosis on failure). Therapy costs a week and $2,000 to drop one point, and
never below what the installed chrome already costs.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from src.rules.cwn_cyberware import (
    SYNDROMES as _SRD_SYNDROMES,
    THERAPY_COST_PER_WEEK,
    alienation_for_system,
    therapy_week as _therapy_week,
)

#: How much each syndrome raises the Alienation ceiling, and the behaviour it imposes.
#: Read out of `cwn_cyberware.SYNDROMES` — one table, so the two modules cannot disagree again.
SYNDROMES: dict[str, dict] = {
    name: {"max_bonus": int(row["bonus"]), "effect": str(row["effect"])}
    for name, row in _SRD_SYNDROMES.items()
}

#: Cost of a week of cyberpsychological therapy, in the book's currency (SRD "Cyberware Alienation").
THERAPY_COST = THERAPY_COST_PER_WEEK


class AlienationError(ValueError):
    pass


def system_cost(strain_cost: float, *, nerve: bool = False,
                discounted_sense: bool = False) -> int:
    """Alienation gained by installing one system (printed p. 226).

    System Strain rounded **up**, +2 for Nerveware. Eye and ear mods discounted by cybereyes or
    cyberears still cost 1 each, which is what `discounted_sense` pins.
    """
    if strain_cost < 0:
        raise AlienationError("System Strain cost cannot be negative")
    cost = alienation_for_system(strain_cost, nerve=nerve)
    if discounted_sense:
        cost = max(1, cost)
    return cost


@dataclass
class Alienation:
    """One character's chrome burden. Permanent only in the sense that chrome sets a floor."""

    wisdom: int
    score: int = 0
    syndromes: list[str] = field(default_factory=list)
    #: Alienation the currently installed chrome already accounts for; therapy cannot go below it.
    floor: int = 0

    def __post_init__(self) -> None:
        if type(self.wisdom) is not int or self.wisdom < 0:
            raise AlienationError("Wisdom must be a non-negative integer")
        if self.score < 0 or self.floor < 0:
            raise AlienationError("Alienation cannot be negative")
        if len(set(self.syndromes)) != len(self.syndromes):
            raise AlienationError("the same syndrome cannot be taken twice")
        for name in self.syndromes:
            if name not in SYNDROMES:
                raise AlienationError(f"unknown chrome syndrome: {name}")

    @property
    def maximum(self) -> int:
        """Wisdom plus the ceiling bonus of every syndrome taken (printed pp. 227, 231)."""
        return self.wisdom + sum(SYNDROMES[name]["max_bonus"] for name in self.syndromes)

    @property
    def broken(self) -> bool:
        return self.score > self.maximum

    # -- chrome ---------------------------------------------------------------------
    def install(self, strain_cost: float, *, nerve: bool = False,
                discounted_sense: bool = False) -> int:
        """Adding chrome raises both the score and the floor it can be treated down to."""
        gain = system_cost(strain_cost, nerve=nerve, discounted_sense=discounted_sense)
        self.score += gain
        self.floor += gain
        return gain

    def uninstall(self, strain_cost: float, *, nerve: bool = False,
                  discounted_sense: bool = False) -> int:
        """Removing chrome lowers the floor (printed p. 226: 'removing cyberware will lower this minimum')."""
        relief = system_cost(strain_cost, nerve=nerve, discounted_sense=discounted_sense)
        self.floor = max(0, self.floor - relief)
        self.score = max(self.floor, self.score - relief)
        return relief

    # -- syndromes ------------------------------------------------------------------
    def take_syndrome(self, name: str) -> None:
        if name not in SYNDROMES:
            raise AlienationError(f"unknown chrome syndrome: {name}")
        if name in self.syndromes:
            raise AlienationError("the same syndrome cannot be taken twice")
        self.syndromes.append(name)

    def drop_syndrome(self, name: str) -> None:
        """Only by uninstalling the chrome that induced it and treating the Alienation it caused."""
        if name not in self.syndromes:
            raise AlienationError(f"no such syndrome: {name}")
        self.syndromes.remove(name)

    # -- checks ---------------------------------------------------------------------
    def check(self, die: int) -> dict:
        """A 1d20 Alienation check: at or under the current score, it rises by one.

        Returns what happened rather than mutating silently, because the caller has to decide about the
        Mental save when the rise pushes past the ceiling.
        """
        if not 1 <= die <= 20:
            raise AlienationError("an Alienation check is a d20 roll")
        if die > self.score:
            return {"gained": 0, "over_maximum": self.broken, "mental_save": False}
        self.score += 1
        return {"gained": 1, "over_maximum": self.broken, "mental_save": self.broken}

    def mental_save(self, *, success: bool) -> str:
        """Resolve a rise past the ceiling: a new syndrome, or cyber-induced psychosis."""
        if not self.broken:
            raise AlienationError("a Mental save is only called for past the ceiling")
        return "syndrome" if success else "psychosis"

    # -- therapy --------------------------------------------------------------------
    def therapy_week(self) -> dict:
        """One week of therapy drops one point, never below the chrome's own cost."""
        if self.score <= self.floor:
            return {"dropped": 0, "score": self.score, "cost": 0}
        self.score = _therapy_week(self.score, self.floor)
        return {"dropped": 1, "score": self.score, "cost": THERAPY_COST}


def rescue_from_psychosis(*, wisdom: int, score: int, chrome_removed: bool,
                          therapist_skill: int, die: int) -> dict:
    """A psychosis victim's one way back (printed p. 226).

    Requires all chrome removed except medically necessary prostheses, Alienation brought below Wisdom,
    and a Mental save with a bonus equal to the therapist's best Heal or Talk level.
    """
    if therapist_skill < 0:
        raise AlienationError("skill levels are not negative")
    if not chrome_removed:
        return {"rescued": False, "reason": "chrome must be removed first"}
    if score >= wisdom:
        return {"rescued": False, "reason": "Alienation must be below Wisdom first"}
    target = 15  # CWN Mental save
    total = die + therapist_skill
    return {"rescued": total >= target, "total": total, "target": target,
            "reason": "" if total >= target else "the damage is permanent"}
