"""The SWN **Psychic Training** focus, implemented from the author's own quotation (#1217 line 11, #1178).

The repository has refused for weeks to implement this focus, and the refusal was correct at the time: `psi_edges`
gates it behind a `Citation` because the level benefits are printed rules and nobody would transcribe them from
memory. The author then quoted the focus in full in #1178 §1. That removes the reason for the gate — and does **not**
remove the licence rule: the prose is his, published, and is not reproduced here. What lives in code is the *mechanics*
the quotation states, with a locator that says where the rule comes from and who supplied it.

The printed focus says, in mechanics:

* **Prerequisite:** a Psychic, or an Adventurer who took the Partial Psychic option — and then only in the discipline
  they chose. Taken once only.
* **Level 1:** gain any psychic skill as a bonus; if that improves it to level-1 proficiency, choose a free level-1
  technique from that discipline; **maximum Effort +1**.
* **Level 2:** on advancing a level, the bonus skill automatically receives one point toward raising the skill or
  buying a technique from it; points may be banked; **awarded retroactively** if the focus level is taken later.

Three implementation decisions, all marked so a reader can argue with them:

* **The Effort increase is a property of the focus, not a mutation of the psychic.** `Psychic.capacity` is computed
  arithmetic in an immutable-ish SWN module; adding one to it by patching the class would fork a rulebook formula.
  :func:`effort_max` returns the sum instead, and is the only supported way to read it.
* **"Retroactively" is read as one point per character level gained before the focus level was taken** —
  :func:`retroactive_points`. The book says the points are awarded retroactively but does not state a formula, so this
  is the plain reading, and it is the one thing here that a table should confirm.
* **The technique grant is a permission, not a discount.** A free level-1 technique is added to the character's
  authorized set; using it still costs its Effort and still requires its check. Nothing here rolls dice.

No rules module is modified: `psi_access`, `psionics` and `swn_psionics` stay as they are, and this module composes them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .psionics import load_catalogue
from .psi_access import PC_DISCIPLINES, require_pc_discipline
from .swn_psionics import DISCIPLINES, Psychic

__all__ = [
    "FOCUS_NAME",
    "LOCATOR",
    "PsychicTraining",
    "PsychicTrainingError",
    "advance_to_level_two",
    "choose_technique",
    "effort_max",
    "retroactive_points",
    "spend_point",
    "take_focus",
]

FOCUS_NAME = "Psychic Training"

#: Where the rule lives, and who supplied it. Never a paraphrase of the printed benefit text.
LOCATOR = (
    "Stars Without Number Revised Deluxe, the Psychic Training focus; mechanics supplied by the author's "
    "quotation in NooPunk issue #1178 §1. The printed prose is not reproduced in this repository "
    "(docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md)."
)

#: A discipline's maximum rank under the SWN engine.
MAX_RANK = 4


class PsychicTrainingError(ValueError):
    """A focus operation the rules, the licence or the character's own limits refuse."""


@dataclass
class PsychicTraining:
    """A character's Psychic Training focus, once taken.

    ``discipline`` is the bonus psychic skill chosen at level 1; ``technique`` is the free level-1 technique that came
    with reaching proficiency; ``banked_points`` are level-2 points not yet spent.
    """

    discipline: str
    level: int = 1
    technique: str = ""
    banked_points: int = 0
    #: Effort granted by level 1. Read through :func:`effort_max`, never added by hand.
    effort_bonus: int = 1
    history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.discipline not in DISCIPLINES:
            raise PsychicTrainingError(f"unknown psychic discipline {self.discipline!r}")
        if self.discipline not in PC_DISCIPLINES:
            raise PsychicTrainingError(
                f"{self.discipline!r} is not selectable by a player character (#1178 §1); "
                f"the focus trains {PC_DISCIPLINES}"
            )
        if self.level not in (1, 2):
            raise PsychicTrainingError("the focus has two levels")
        if self.banked_points < 0:
            raise PsychicTrainingError("banked points cannot be negative")


def _catalogue() -> dict[str, dict]:
    return load_catalogue()


def take_focus(psychic: Psychic, discipline: str, *, partial: bool = False,
               already_taken: bool = False) -> PsychicTraining:
    """Take Psychic Training at level 1 and apply its grants to ``psychic``.

    Mutates ``psychic.disciplines`` (the bonus skill) and returns the focus. It does **not** mutate Effort capacity:
    see :func:`effort_max` for why.

    Refusals, in the order a table will hit them: the focus is once-only; the discipline must be one a player may
    choose; a Partial Psychic may only train the discipline they chose; a discipline already at maximum rank cannot be
    improved.
    """
    if already_taken:
        raise PsychicTrainingError("Psychic Training can be taken only once")
    require_pc_discipline(discipline)
    restricted = psychic.restricted_discipline
    if partial and not restricted:
        raise PsychicTrainingError("a Partial Psychic has exactly one discipline; set it on the Psychic first")
    if restricted and restricted != discipline:
        raise PsychicTrainingError(
            f"a Partial Psychic may only train {restricted!r}, not {discipline!r}"
        )
    current = psychic.disciplines.get(discipline, 0)
    if current >= MAX_RANK:
        raise PsychicTrainingError(f"{discipline} is already at rank {MAX_RANK}")
    psychic.disciplines[discipline] = current + 1
    return PsychicTraining(discipline=discipline)


def choose_technique(training: PsychicTraining, technique_id: str) -> str:
    """Grant the free level-1 technique, which must belong to the trained discipline and be a rank-1 technique.

    The grant is a *permission*: the technique still costs Effort and still requires its check when used.
    """
    catalogue = _catalogue()
    entry = catalogue.get(technique_id)
    if entry is None:
        raise PsychicTrainingError(f"no technique {technique_id!r} in the catalogue")
    if str(entry.get("discipline", "")) != training.discipline:
        raise PsychicTrainingError(
            f"{technique_id!r} belongs to {entry.get('discipline')!r}, not {training.discipline!r}"
        )
    if int(entry.get("min_skill", 0)) > 1:
        raise PsychicTrainingError(
            f"{technique_id!r} needs skill rank {entry.get('min_skill')}; level 1 grants a rank-1 technique"
        )
    training.technique = technique_id
    training.history.append(f"technique:{technique_id}")
    return technique_id


def effort_max(psychic: Psychic, training: PsychicTraining) -> int:
    """The character's maximum Effort, including the focus's +1.

    ``Psychic.capacity`` implements the SWN formula; the focus adds one to the *maximum*. Summing here keeps that
    formula in one place instead of re-deriving it with a bonus term.
    """
    return psychic.capacity + training.effort_bonus


def retroactive_points(character_level: int) -> int:
    """Points owed when level 2 is taken late: one per level already gained.

    The book states the award is retroactive without printing a formula. This is the plain reading — a character who
    takes the second level at character level 5 receives four points — and it is the one item here that needs a table's
    confirmation rather than a test's.
    """
    if character_level < 1:
        raise PsychicTrainingError("character level starts at 1")
    return character_level - 1


def advance_to_level_two(training: PsychicTraining, *, character_level: int) -> int:
    """Raise the focus to level 2 and bank the points owed; returns how many were banked."""
    if training.level == 2:
        raise PsychicTrainingError("the focus is already at level 2")
    granted = retroactive_points(character_level)
    training.level = 2
    training.banked_points += granted
    training.history.append(f"level2:+{granted}")
    return granted


def spend_point(training: PsychicTraining, *, target: str = "skill", technique_id: str = "") -> str:
    """Spend one banked point on the trained skill or on a technique of that discipline.

    ``target="skill"`` may be capped by the caller's own advancement rules; this function only tracks the focus's own
    bookkeeping and refuses to spend a point it does not have.
    """
    if training.banked_points <= 0:
        raise PsychicTrainingError("no banked points to spend")
    if target == "skill":
        training.banked_points -= 1
        training.history.append("point:skill")
        return "skill"
    if target == "technique":
        entry = _catalogue().get(technique_id)
        if entry is None:
            raise PsychicTrainingError(f"no technique {technique_id!r} in the catalogue")
        if str(entry.get("discipline", "")) != training.discipline:
            raise PsychicTrainingError("a point may only buy a technique of the trained discipline")
        training.banked_points -= 1
        training.history.append(f"point:technique:{technique_id}")
        return technique_id
    raise PsychicTrainingError("a point is spent on 'skill' or on a technique")
