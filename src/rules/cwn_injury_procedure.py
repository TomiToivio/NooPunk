"""The zero-hit-point procedure: risk, save, and the Major Injury table.

Three modules each own a piece of this and none of them owned the *sequence*:

* ``cwn_trauma`` answers whether a Major Injury is risked at all
  (``major_injury_risk``: zero hit points **and** a Traumatic Hit in this fight);
* ``cwn_core`` owns the Physical save;
* ``cwn_major_injury`` owns the outcome once the save fails.

Between them sat one unstated rule that a runtime cannot guess: **the save is
gated by the trauma**. Being dropped to zero by ordinary damage is a knockout.
Being dropped to zero in a fight where a Traumatic Hit landed means a Physical
save - and failing it means a roll on the d12 table, not merely a longer rest.

This module is that sequence and nothing else. It calls the three owners rather
than restating any of their rules.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .cwn_core import Save, saving_throw
from .cwn_major_injury import MajorInjury, resolve_major_injury
from .cwn_trauma import major_injury_risk


class ProcedureError(ValueError):
    """Raised when the procedure is called without a value it needs."""


@dataclass(frozen=True)
class ZeroHitPointOutcome:
    """What happened when a character reached zero hit points.

    ``save`` is present only when the trauma gate asked for one. ``injury`` is
    present only when that save was failed and the table was consulted.
    """

    mortally_wounded: bool
    risked_major_injury: bool
    save: Save | None
    injury: MajorInjury | None


def resolve_zero_hit_points(
    *,
    hit_points_after: int,
    traumatic_in_fight: bool,
    level: int,
    attributes: Mapping[str, int],
    save_die: int | None = None,
    save_bonus: int = 0,
    injury_roll: int | None = None,
    injury_modifier: int = 0,
) -> ZeroHitPointOutcome:
    """Run the procedure for a character who has just taken damage.

    Dice enter as explicit values: ``save_die`` for the Physical save and
    ``injury_roll`` for the d12 table. Both are required only in the branches
    that actually use them, so a knockout costs the table nothing and a passed
    save never consults a table it did not reach.
    """
    if hit_points_after > 0:
        return ZeroHitPointOutcome(
            mortally_wounded=False, risked_major_injury=False, save=None, injury=None
        )

    risked = major_injury_risk(hit_points_after, traumatic_in_fight=traumatic_in_fight)
    if not risked:
        # Zero hit points without trauma is a knockout, not a wound.
        return ZeroHitPointOutcome(
            mortally_wounded=True, risked_major_injury=False, save=None, injury=None
        )

    if save_die is None:
        raise ProcedureError("a risked Major Injury needs its Physical save roll")

    save = saving_throw(
        "Physical", level=level, attributes=attributes, bonus=save_bonus, die=save_die
    )
    if save.success:
        # Passing does not undo the wound: the character is still Mortally
        # Wounded and still needs stabilising. It only keeps them off the table.
        return ZeroHitPointOutcome(
            mortally_wounded=True, risked_major_injury=True, save=save, injury=None
        )

    if injury_roll is None:
        raise ProcedureError("a failed save needs its d12 Major Injury roll")

    injury = resolve_major_injury(injury_roll, modifier=injury_modifier)
    return ZeroHitPointOutcome(
        mortally_wounded=True, risked_major_injury=True, save=save, injury=injury
    )


__all__ = ["ProcedureError", "ZeroHitPointOutcome", "resolve_zero_hit_points"]
