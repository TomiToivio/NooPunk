"""Natural, learnable PSI — NoöPunk's own psychic subsystem (issue #572).

**Status: PROVISIONAL, not canonical.** Every number is a `TUNING_` constant and belongs to the
author. `AGENTS.md` §4 reserves *psionic powers or psionic mechanics*; the author has now asked for a
natural, learnable PSI subsystem by name, so this module is the executable proposal — not a ruling.

The three canon sentences this obeys:

1. **PSI is natural, not viral** (`rulebook/6_PSYCHIC.md` §6.1). Human consciousness has a latent
   capacity; most people are weak and noisy; it is not an infection, a class feature, or a
   technology. Nothing here is granted by an implant, and the psychotronic channel stays separate.
2. **Training changes the probability** (§6.1, *"psychic training alters the probability and
   stability of normally latent phenomena"*). That is the learnability the author asked for: a
   discipline is **trained into reliability**, so an untrained character is not "blocked by birth"
   and a trained one is not a wizard. Learning is a *practice record*, not a level.
3. **The six PSY skills are the disciplines** (`data/rules/skills.json`, #159): `ESP`, `Telepathy`,
   `Psychokinesis`, `Precognition`, `Psychic Defence`, `Noöspace`. There is no seventh "Psionics"
   skill and this module does not invent one.

**What is borrowed and what is not.** The Without Number family's psionics are the wrong ontology
(virus, class, discrete powers), and SWN's text is licence-blocked anyway. What *is* usable is
**WWN's Effort pattern** — a small pool where a *lasting* effect keeps capacity committed until it is
released, so an ongoing burden is represented without a second hit-point track — and WWN's SRD is
CC0. So the cost model is Effort-shaped and independently implemented; the disciplines, the origin,
the pressure and the consensus are NoöPunk's own.

**Resolution stays on the one kernel:** `PSY + discipline + 1d10 ≥ DV` (`src/rules/core.py`). PSI gets
no second arithmetic.

Usage::

    practitioner = Practitioner(psy=6, practice={Discipline.TELEPATHY: 40})
    attempt = practitioner.attempt(Discipline.TELEPATHY, dv=15, rng=Random(3))
    practitioner.commit("a watching thread", cost=1)   # Effort committed until released
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Any

from . import core

#: PROVISIONAL. The author owns every number below; they exist so the procedure is executable.
IS_CANONICAL = False

# --------------------------------------------------------------------------- #
# TUNING — the author's numbers, marked as such
# --------------------------------------------------------------------------- #

TUNING_BASE_EFFORT = 1               # every latent human has this much capacity
TUNING_PSY_PER_EFFORT = 2            # PSY 2 buys a second point, 4 a third, 6 a fourth, 8 a fifth
TUNING_MAX_EFFORT = 5
TUNING_MIN_PRACTICE = 20             # hours of supervised practice before a discipline is usable
TUNING_MASTERY_PRACTICE = 120        # hours that make it reliable under pressure
TUNING_PRESSURE_PER_FAILURE = 1      # psyche load added by a failed attempt
TUNING_PRESSURE_PER_TIE = 1          # a tie costs something: no free failures
TUNING_PRESSURE_RECOVERY_PER_SCENE = 1
TUNING_BELIEVER_BONUS = 1            # each convinced witness standing with you
TUNING_DOUBTER_PENALTY = 1           # each hostile witness
TUNING_CONSENSUS_CAP = 2


class PsiError(ValueError):
    """A canon invariant was about to be violated."""


class Discipline(str, Enum):
    """The six PSY skills, as disciplines. Learnable; never innate-only, never a class."""

    ESP = "ESP"
    TELEPATHY = "Telepathy"
    PSYCHOKINESIS = "Psychokinesis"
    PRECOGNITION = "Precognition"
    PSYCHIC_DEFENCE = "Psychic Defence"
    NOOSPACE = "Noöspace"


class Training(str, Enum):
    """How far practice has taken a discipline. Not a level: it does not raise the skill rating."""

    UNTRAINED = "untrained"        # latent and unusable under pressure: refused before any die
    PRACTISED = "practised"        # usable, at the rating the character actually has
    MASTERED = "mastered"          # usable, and pressure costs one less


class Outcome(str, Enum):
    FAILURE = "failure"
    TIE = "tie"
    SUCCESS = "success"
    SUCCESS_WITH_STYLE = "success with style"


@dataclass(frozen=True)
class Pressure:
    """What an attempt costs the psyche. Not damage, not a stress track: a named load."""

    psyche_load: int = 0
    noetic_trace: int = 0

    def __add__(self, other: "Pressure") -> "Pressure":
        return Pressure(self.psyche_load + other.psyche_load,
                        self.noetic_trace + other.noetic_trace)


@dataclass(frozen=True)
class Attempt:
    discipline: Discipline
    training: Training
    outcome: Outcome
    total: int
    dv: int
    pressure: Pressure
    effort_spent: int
    modifier: int

    @property
    def succeeded(self) -> bool:
        return self.outcome in (Outcome.SUCCESS, Outcome.SUCCESS_WITH_STYLE)


def training_for(practice_hours: int) -> Training:
    """Practice, not birth, decides usability — §6.1's trainability, made arithmetic."""
    if practice_hours < TUNING_MIN_PRACTICE:
        return Training.UNTRAINED
    if practice_hours < TUNING_MASTERY_PRACTICE:
        return Training.PRACTISED
    return Training.MASTERED


def effort_capacity(psy: int) -> int:
    """A small pool that grows slowly with PSY and stops growing. `PSY 6` → 3."""
    if not 1 <= psy <= core.STAT_MAX:
        raise PsiError(f"PSY must be 1..{core.STAT_MAX}, got {psy}")
    return min(TUNING_MAX_EFFORT, TUNING_BASE_EFFORT + psy // TUNING_PSY_PER_EFFORT)


def consensus_modifier(believers: int = 0, doubters: int = 0) -> int:
    """The room matters: a witnessed act is easier with believers, harder with doubters."""
    raw = believers * TUNING_BELIEVER_BONUS - doubters * TUNING_DOUBTER_PENALTY
    return max(-TUNING_CONSENSUS_CAP, min(TUNING_CONSENSUS_CAP, raw))


# --------------------------------------------------------------------------- #
# The practitioner
# --------------------------------------------------------------------------- #

@dataclass
class Practitioner:
    """One person's trained capacity. No class, no level, no second dice convention."""

    psy: int
    practice: dict[Discipline, int] = field(default_factory=dict)
    skills: dict[str, int] = field(default_factory=dict)
    committed: dict[str, int] = field(default_factory=dict)
    psyche_load: int = 0
    rng: Any = field(default_factory=random.Random)

    # -- capacity ------------------------------------------------------------------------

    def __post_init__(self) -> None:
        self.capacity = effort_capacity(self.psy)

    @property
    def effort_free(self) -> int:
        return self.capacity - sum(self.committed.values())

    def training(self, discipline: Discipline) -> Training:
        return training_for(self.practice.get(discipline, 0))

    def rating(self, discipline: Discipline) -> int:
        """The discipline's rating: the character's own skill, never a bonus for training."""
        return int(self.skills.get(discipline.value, 0))

    # -- Effort: committed capacity, released on purpose ---------------------------------

    def commit(self, label: str, *, cost: int = 1) -> None:
        """Hold Effort on a lasting effect. Refuses rather than overcommitting."""
        if cost < 1:
            raise PsiError("a commitment costs at least 1 Effort")
        if cost > self.effort_free:
            raise PsiError(
                f"not enough free Effort: {self.effort_free} free, {cost} needed; release something"
            )
        self.committed[label] = self.committed.get(label, 0) + cost

    def release(self, label: str) -> int:
        """Release a commitment by name. Unknown labels release nothing rather than guessing."""
        return self.committed.pop(label, 0)

    def recover(self, *, scenes: int = 1) -> None:
        """Psyche load bleeds off between scenes; commitments do **not** expire on their own."""
        if scenes < 0:
            raise PsiError("recovery scenes cannot be negative")
        self.psyche_load = max(0, self.psyche_load - TUNING_PRESSURE_RECOVERY_PER_SCENE * scenes)

    # -- the attempt ---------------------------------------------------------------------

    def attempt(
        self,
        discipline: Discipline,
        *,
        dv: int,
        believers: int = 0,
        doubters: int = 0,
        effort: int = 0,
        rng: Any | None = None,
        die: int | None = None,
    ) -> Attempt:
        """Resolve one psychic act on the core kernel — or refuse it before any die is rolled.

        An untrained discipline is **refused**, not attempted at a penalty: that is what makes the
        canon's "latent but unreliable" different from "impossible", and it keeps training the thing
        that changes, exactly as §6.1 says.
        """
        learnt = self.training(discipline)
        if learnt is Training.UNTRAINED:
            raise PsiError(
                f"{discipline.value} is latent but untrained "
                f"({self.practice.get(discipline, 0)} h < {TUNING_MIN_PRACTICE} h): it cannot be "
                f"attempted under pressure; it can be practised"
            )
        rating = self.rating(discipline)
        if rating < core.SKILL_LEVEL_MIN:
            raise PsiError(
                f"{discipline.value} has no rating ({rating}); the canonical kernel takes a 1.."
                f"{core.SKILL_LEVEL_MAX} Skill, so give the character at least the minimum before "
                f"attempting it"
            )
        if effort:
            # Committed, not borrowed: this capacity stays locked until the caller
            # releases the label. Effort is a pool of *held* capacity, so refunding it
            # at the end of the attempt made spending it free and therefore pointless.
            self.commit(f"attempt:{discipline.value}", cost=effort)

        modifier = consensus_modifier(believers, doubters)
        # The kernel resolves STAT + Skill + 1d10 >= DV and takes no modifier argument,
        # so a situational modifier is applied as the same arithmetic on the other side:
        # +m on the roll is identical to -m on the target. Without this the consensus
        # value was computed, reported, and silently ignored.
        target = dv - modifier
        result = core.resolve_check(stat=self.psy, skill=rating, target=target,
                                    rng=rng if rng is not None else self.rng, die=die)
        total = result.total + modifier
        outcome = _outcome(total - dv)
        pressure = _pressure(outcome, learnt)
        self.psyche_load += pressure.psyche_load
        return Attempt(discipline, learnt, outcome, total, dv, pressure, effort, modifier)


def _outcome(margin: int) -> Outcome:
    if margin < 0:
        return Outcome.FAILURE
    if margin == 0:
        return Outcome.TIE
    if margin >= 3:
        return Outcome.SUCCESS_WITH_STYLE
    return Outcome.SUCCESS


def _pressure(outcome: Outcome, training: Training) -> Pressure:
    """A failure and a tie both cost; mastery does not remove the cost, it softens it once."""
    if outcome is Outcome.FAILURE:
        load = TUNING_PRESSURE_PER_FAILURE
    elif outcome is Outcome.TIE:
        load = TUNING_PRESSURE_PER_TIE
    else:
        load = 0
    if training is Training.MASTERED:
        load = max(0, load - 1)
    trace = 1 if outcome in (Outcome.SUCCESS_WITH_STYLE, Outcome.TIE) else 0
    return Pressure(psyche_load=load, noetic_trace=trace)


# --------------------------------------------------------------------------- #
# Learnability, stated as a procedure rather than a promise
# --------------------------------------------------------------------------- #

def practice(discipline: Discipline, *, hours: int, supervised: bool = True,
             prior_hours: int = 0) -> dict[str, Any]:
    """What a training block does. Unsupervised hours count half — a teacher is not decoration.

    `prior_hours` is what the character had already accumulated in this discipline. It is
    required for a correct tier report: the tier is a property of the *total*, so 100 hours
    plus a 30-hour block is mastery, even though neither number reaches the threshold alone.

    This is the whole of "learnable": no class, no feat, no level, and no cap other than the
    discipline's own rating scale. A table can track it on the character sheet as hours.
    """
    if hours < 0:
        raise PsiError("practice hours cannot be negative")
    if prior_hours < 0:
        raise PsiError("prior practice hours cannot be negative")
    effective = hours if supervised else hours // 2
    total = prior_hours + effective
    return {
        "discipline": discipline.value,
        "hours": effective,
        "total_hours": total,
        "training_after": training_for(total).value,
        "note": "supervised" if supervised else "unsupervised: half credit",
    }
