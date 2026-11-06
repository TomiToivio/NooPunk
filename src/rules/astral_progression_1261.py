"""Issue #1261 Astral Projection rank 0–1 action gates.

This is an additive authorization layer over astral_body. It does not define
a psychic Effort pool, extend CWN combat, or supersede the mode perception filter.
Ranks 2–4 remain design-only. Access to projection itself must be granted by
character eligibility or an authored scene, outside this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .astral_body import PerceptionMode, Projection


class AstralRankAction(str, Enum):
    OBSERVE = "observe"
    WALK = "walk"
    ASTRAL_CONTACT = "astral_contact"
    RETURN = "return"
    FLY = "fly"
    ENTER_LOWER_ASTRAL = "enter_lower_astral"
    TRANSMIT_ROTE = "transmit_rote"
    LEARN_IDENT = "learn_ident"
    USE_IDENT = "use_ident"
    EDIT_QUANTUM_INFORMATION = "edit_quantum_information"
    ENTER_HIGHER_PLANES = "enter_higher_planes"


@dataclass(frozen=True, slots=True)
class RankPermission:
    allowed: bool
    reason: str
    requires_authored_gateway: bool = False


# Only ranks 0 and 1 are an implemented capability policy.
_MINIMUM_RANK = {
    AstralRankAction.OBSERVE: 0,
    AstralRankAction.WALK: 0,
    AstralRankAction.ASTRAL_CONTACT: 0,
    AstralRankAction.RETURN: 0,
    AstralRankAction.FLY: 1,
    AstralRankAction.ENTER_LOWER_ASTRAL: 1,
}
_FUTURE_RANK = {
    AstralRankAction.TRANSMIT_ROTE: 2,
    AstralRankAction.LEARN_IDENT: 2,
    AstralRankAction.USE_IDENT: 3,
    AstralRankAction.EDIT_QUANTUM_INFORMATION: 3,
    AstralRankAction.ENTER_HIGHER_PLANES: 4,
}


def starting_rank_allowed(rank: int) -> bool:
    """Starting campaign eligibility; separate from later advancement."""
    return type(rank) is int and rank in (0, 1)


def authorize_rank_action(
    projection: Projection,
    rank: int,
    action: AstralRankAction | str,
    *,
    authored_gateway: bool = False,
) -> RankPermission:
    """Authorize the skill gate, not the entire resolved scene action.

    CWN/SWN dice, Effort and resource costs stay with their native systems.
    Physical targeting and perception are still checked by astral_body.
    A Lower Astral dream gateway is scene-authored and never an evidence shortcut.
    """
    if not projection.active:
        return RankPermission(False, "the actor has returned to the physical body")
    if type(rank) is not int or not 0 <= rank <= 4:
        return RankPermission(False, "invalid Astral Projection rank")
    try:
        selected = AstralRankAction(action)
    except ValueError:
        return RankPermission(False, "unknown Astral Projection action")
    if selected in _FUTURE_RANK:
        return RankPermission(
            False, f"{selected.value} is rank {_FUTURE_RANK[selected]} design-only"
        )
    minimum = _MINIMUM_RANK[selected]
    if rank < minimum:
        return RankPermission(False, f"{selected.value} requires rank {minimum}")
    if selected in (AstralRankAction.WALK, AstralRankAction.FLY):
        if projection.mode is not PerceptionMode.SPACE_TIME:
            return RankPermission(False, "near-Astral navigation requires Space/Time")
    if selected is AstralRankAction.ENTER_LOWER_ASTRAL:
        if projection.mode is not PerceptionMode.SPACE_TIME:
            return RankPermission(False, "enter Lower Astral from an authored gateway")
        if not authored_gateway:
            return RankPermission(False, "Lower Astral entry needs an authored gateway", True)
    return RankPermission(True, "rank gate passed; apply scene, target and resource rules")


def describe_rank(rank: int) -> str:
    """Player-facing model of the Astral; no unearned GM-only ontology."""
    if rank == 0:
        return ("The room is familiar but distorted. You can observe and move "
                "uncertainly; you may be dreaming.")
    if rank == 1:
        return ("Physical distance no longer feels binding. You can fly through "
                "the near Astral and seek authored entrances into dream landscapes.")
    if rank in (2, 3, 4):
        return "Advanced Astral Projection is not implemented in the starting campaign."
    raise ValueError("Astral Projection rank must be 0–4")
