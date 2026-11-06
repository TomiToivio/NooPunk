"""Compatibility surface for the rank gates, delegating to :mod:`src.rules.astral_ranks` (#1261).

Three agents wrote the same ladder within an afternoon: ``astral_ranks`` (the full superskill, with
capabilities and Ident permissions), this module (a data-driven table and the gates that read it), and an
action-gate layer for ranks 0–1. The ladder now lives in **one** place — ``astral_ranks.RANKS`` — and this
module keeps the small API the body module and three test suites already import.

Nothing here restates a number. If this file grows a rank table again, the duplication has come back.
"""

from __future__ import annotations

from .astral_ranks import (
    CAMPAIGN_MAX_STARTING_RANK,
    RANKS,
    AstralRankError,
    duration_cap_minutes as _duration_cap_minutes,
    rank_spec,
    starting_rank,
)

AstralProgressionError = AstralRankError


class _RankView:
    """The rank as the older API described it: a name, a model of reality and a permission set."""

    __slots__ = ("rank", "name", "status", "understanding", "perception", "capability",
                 "flight", "lower_astral", "time_space", "rote", "ident_learn", "ident_use",
                 "planes", "akashic", "duration_cap_minutes")

    def __init__(self, rank: int) -> None:
        spec = rank_spec(rank)
        from .astral_ranks import Capability

        capabilities = spec.capabilities
        self.rank = rank
        self.name = spec.name
        self.status = "playable" if rank <= CAMPAIGN_MAX_STARTING_RANK else "design-only"
        self.understanding = spec.understanding
        self.perception = (spec.perception,)
        self.capability = (spec.actions,)
        self.flight = Capability.FLIGHT in capabilities
        self.lower_astral = Capability.LOWER_ASTRAL in capabilities
        # Deliberate switching between Space/Time and Time/Space is a later permission; no rank claims it yet.
        self.time_space = False
        self.rote = Capability.ROTE in capabilities
        self.ident_learn = Capability.LEARN_IDENT in capabilities
        self.ident_use = Capability.USE_IDENT in capabilities
        self.planes = tuple(
            name for name, present in (
                ("near_astral", Capability.PHYSICAL_OVERLAY in capabilities),
                ("lower_astral", Capability.LOWER_ASTRAL in capabilities),
                ("devachanic", Capability.HIGHER_PLANES in capabilities),
                ("etheric", Capability.HIGHER_PLANES in capabilities),
                ("buddhic", Capability.HIGHER_PLANES in capabilities),
            ) if present
        )
        self.akashic = Capability.AKASHIC in capabilities
        self.duration_cap_minutes = spec.provisional_max_minutes

    @property
    def playable(self) -> bool:
        return self.status == "playable"


def ranks() -> dict[int, _RankView]:
    return {rank: _RankView(rank) for rank in sorted(RANKS)}


def rank_of(value: int) -> _RankView:
    try:
        return _RankView(int(value))
    except (KeyError, TypeError, ValueError) as exc:
        raise AstralProgressionError(f"Astral Projection rank must be 0..4, got {value!r}") from exc


def mvp_max_rank() -> int:
    return CAMPAIGN_MAX_STARTING_RANK


def require_playable(value: int) -> _RankView:
    rank = rank_of(value)
    if rank.rank > mvp_max_rank():
        raise AstralProgressionError(
            f"rank {rank.rank} ({rank.name}) is design-only; the initial campaign allows 0..{mvp_max_rank()}"
        )
    return rank


def require_starting_rank(value: int) -> _RankView:
    if int(value) > mvp_max_rank():
        raise AstralProgressionError(
            f"a character may not start above Astral Projection {mvp_max_rank()}"
        )
    starting_rank(int(value))  # the canonical module's own check
    return require_playable(value)


#: Techniques the author has named, mapped to the capability that permits each one. The minimum rank is
#: computed from the canonical table rather than restated here.
_TECHNIQUE_CAPABILITY = {
    "rote": "ROTE",
    "learn_ident": "LEARN_IDENT",
    "use_ident": "USE_IDENT",
}


def _minimum_rank_for(capability_name: str) -> int:
    from .astral_ranks import Capability

    capability = Capability(capability_name.lower())
    return min(rank for rank, spec in RANKS.items() if capability in spec.capabilities)


def require_technique(value: int, technique: str) -> None:
    key = technique.strip().lower()
    if key not in _TECHNIQUE_CAPABILITY:
        raise AstralProgressionError(f"unknown Astral Projection technique {technique!r}")
    rank = rank_of(value)
    needed = _minimum_rank_for(_TECHNIQUE_CAPABILITY[key])
    if rank.rank < needed:
        raise AstralProgressionError(
            f"{technique} needs Astral Projection {needed}; the character has {rank.rank}"
        )


def require_plane(value: int, plane: str) -> None:
    key = plane.strip().lower()
    rank = rank_of(value)
    if key not in {name.lower() for name in rank.planes}:
        raise AstralProgressionError(
            f"{plane} is not available at Astral Projection {rank.rank}"
            + (" (it needs rank 4)" if key in {"devachanic", "etheric", "buddhic"} else "")
        )


def assert_astral_domain_only() -> None:
    for rank in ranks().values():
        joined = " ".join(rank.capability).lower()
        for forbidden in ("program check", "hack", "root access", "teleport the body", "resurrect"):
            if forbidden in joined:
                raise AstralProgressionError(
                    f"rank {rank.rank} claims a non-astral power ({forbidden!r}); the superskill is "
                    "astral-domain only"
                )


def duration_cap_minutes(value: int) -> int:
    return _duration_cap_minutes(int(value))
