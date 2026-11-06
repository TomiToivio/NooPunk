"""Astral Projection as an Astral-domain superskill, ranks 0–4 (#1261, author revision 2026-11-06).

The author's governing direction is that Astral Projection is a **superskill inside the Astral**: each rank is three
things at once — a model of reality, a range of perception, and a set of things the projector can actually do. Higher
rank is not "more minutes outside the body", and the skill is deliberately *narrow* outside Noöspace: it does not
substitute for CWN skills, CWN hacking, SWN Telepathy or SWN Teleportation.

Scope, exactly as the issue fixes it:

* the **initial campaign allows rank 0 or 1 only**; a character cannot be created at 2–4;
* ranks 2–4 are **design-only** until an authorised later campaign needs them;
* durations are **provisional caps** (10 min / 60 min / 10 h / 48 h / 7 days) retained from earlier comments; the author
  has said understanding and perception are the governing axis, so these numbers must not be treated as balance;
* ROTE is an **Astral technique at rank 2**, Ident is *learned* at 2 and *used* at 3, higher planes and Akashic research
  are rank 4;
* editing quantum information is **permission-gated**, never a raw power: rank 3 edits its own information, and another
  agent's only under an authored mandate, and only if the pattern is mutable at all.

This module is the **capability table and its gates**. It does not create a second body, a second HP pool or a second
combat skill: `astral_body.Projection` remains the single model of one actor projected, and astral damage stays gated
behind `astral_body.ASTRAL_DAMAGE_BRIDGE_APPROVED`.

NoöPunk's QIP cosmology is fictional setting metaphysics, not established physics, and this module encodes no claim
about real consciousness or real quantum mechanics.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

__all__ = [
    "CAMPAIGN_MAX_STARTING_RANK",
    "Capability",
    "InformationPattern",
    "Projector",
    "RankSpec",
    "RANKS",
    "AstralRankError",
    "capabilities_for",
    "duration_cap_minutes",
    "may_edit",
    "require_edit",
    "starting_rank",
    "rank_spec",
]


class AstralRankError(ValueError):
    """A rank, a capability or an edit that the current rules do not allow."""


class Capability(str, Enum):
    """What a projector can do. Every rank's set is cumulative over the ranks below it."""

    SEPARATE = "separate"                 # leave the body; it stays put and stays vulnerable
    RETURN = "return"                     # reliable return
    WALK = "walk"                         # ordinary-looking movement and interaction attempts
    PHYSICAL_OVERLAY = "physical_overlay"  # the physical world remains visible, distorted
    LUCID = "lucid"                       # knows the astral does not obey physical geometry
    FLIGHT = "flight"                     # deliberate rapid movement without locomotion
    LOWER_ASTRAL = "lower_astral"         # constructed dreams and collective unconscious places
    DREAM_ENTRY = "dream_entry"            # enter a sleeping agent's dream environment
    ROTE = "rote"                         # transmit/receive organised thought packages
    LEARN_IDENT = "learn_ident"            # recognise and remember an agent's persistent Ident
    USE_IDENT = "use_ident"               # relocate to a known Ident's astral presence
    EDIT_OWN_INFORMATION = "edit_own_information"
    EDIT_MANDATED_INFORMATION = "edit_mandated_information"
    HIGHER_PLANES = "higher_planes"       # Devachanic, Etheric, Buddhic
    AKASHIC = "akashic"                   # read Akashic patterns


@dataclass(frozen=True, slots=True)
class RankSpec:
    """One rank of the superskill: what it understands, perceives and can do."""

    rank: int
    name: str
    understanding: str
    perception: str
    actions: str
    capabilities: frozenset[Capability]
    provisional_max_minutes: int


#: Initial campaign: the authored opening allows rank 0 or 1. Raising this is an author decision, not a tuning knob.
CAMPAIGN_MAX_STARTING_RANK = 1

_BASE = frozenset({
    Capability.SEPARATE, Capability.RETURN, Capability.WALK, Capability.PHYSICAL_OVERLAY,
})

RANKS: dict[int, RankSpec] = {
    0: RankSpec(
        rank=0,
        name="Disorientation",
        understanding="No QIP or Law of One model; assumes physical laws still apply and may not tell dream from projection.",
        perception="Near Astral only; the physical world remains visible, warped and symbolic.",
        actions="Separation, walking, basic encounters, return. No flight, no Lower Astral.",
        capabilities=_BASE,
        provisional_max_minutes=10,
    ),
    1: RankSpec(
        rank=1,
        name="Lucidity and dream navigation",
        understanding="Knows the astral is not governed by ordinary geometry; begins to grasp QIP in practice.",
        perception="Sees that dreams are constructed from quantum information; still imperfect and partly unreliable.",
        actions="Fast flight, Lower Astral, entry into constructed dream worlds. No ROTE, no Ident.",
        capabilities=_BASE | frozenset({Capability.LUCID, Capability.FLIGHT, Capability.LOWER_ASTRAL,
                                        Capability.DREAM_ENTRY}),
        provisional_max_minutes=60,
    ),
    2: RankSpec(
        rank=2,
        name="Conscious Agent Network",
        understanding="Reads astral objects as quantum information exchanged between conscious agents.",
        perception="Perceives agents as information-bearing structures rather than fixed shapes.",
        actions="Transmit Information (ROTE); learn and recognise an Ident. Cannot relocate by it yet.",
        capabilities=_BASE | frozenset({Capability.LUCID, Capability.FLIGHT, Capability.LOWER_ASTRAL,
                                        Capability.DREAM_ENTRY, Capability.ROTE, Capability.LEARN_IDENT}),
        provisional_max_minutes=10 * 60,
    ),
    3: RankSpec(
        rank=3,
        name="Authorised informational agency",
        understanding="Distinguishes a rendered appearance from the information underneath it.",
        perception="Perceives wave functions and collapse as NoöPunk's QIP ontology depicts them.",
        actions="Edit quantum information within an authorised scope; Use Ident to a known agent's presence.",
        capabilities=_BASE | frozenset({Capability.LUCID, Capability.FLIGHT, Capability.LOWER_ASTRAL,
                                        Capability.DREAM_ENTRY, Capability.ROTE, Capability.LEARN_IDENT,
                                        Capability.USE_IDENT, Capability.EDIT_OWN_INFORMATION,
                                        Capability.EDIT_MANDATED_INFORMATION}),
        provisional_max_minutes=48 * 60,
    ),
    4: RankSpec(
        rank=4,
        name="Cosmological research",
        understanding="Holds Noöspace as a fictionally interpreted infinite-dimensional Hilbert space; dimly perceives timelines.",
        perception="Higher-plane interpretations, alternative timelines and dimensions, uncertain and incomplete.",
        actions="Enter Devachanic, Etheric and Buddhic planes; research Akashic Records.",
        capabilities=_BASE | frozenset({Capability.LUCID, Capability.FLIGHT, Capability.LOWER_ASTRAL,
                                        Capability.DREAM_ENTRY, Capability.ROTE, Capability.LEARN_IDENT,
                                        Capability.USE_IDENT, Capability.EDIT_OWN_INFORMATION,
                                        Capability.EDIT_MANDATED_INFORMATION, Capability.HIGHER_PLANES,
                                        Capability.AKASHIC}),
        provisional_max_minutes=7 * 24 * 60,
    ),
}

#: Durations are provisional caps inherited from earlier comments, not balance. Named so nobody forgets.
DURATIONS_ARE_PROVISIONAL = True


def rank_spec(rank: int) -> RankSpec:
    """The rank's spec, refusing anything outside 0–4."""
    if not isinstance(rank, int) or isinstance(rank, bool):
        raise AstralRankError(f"a rank is an integer 0–4, got {rank!r}")
    spec = RANKS.get(rank)
    if spec is None:
        raise AstralRankError(f"rank {rank} is outside 0–4")
    return spec


def starting_rank(rank: int) -> int:
    """The rank a player character may start at. Anything above the campaign ceiling is refused, not clamped."""
    spec = rank_spec(rank)
    if spec.rank > CAMPAIGN_MAX_STARTING_RANK:
        raise AstralRankError(
            f"the opening allows Astral Projection {CAMPAIGN_MAX_STARTING_RANK} or lower at creation; "
            f"rank {spec.rank} is design-only until an authorised campaign needs it"
        )
    return spec.rank


def capabilities_for(rank: int) -> frozenset[Capability]:
    return rank_spec(rank).capabilities


def has(rank: int, capability: Capability) -> bool:
    """Whether this rank grants the capability. The only way a caller should ask."""
    return capability in capabilities_for(rank)


def duration_cap_minutes(rank: int) -> int:
    """The provisional ceiling on a projection, in minutes. Provisional — see :data:`DURATIONS_ARE_PROVISIONAL`."""
    return rank_spec(rank).provisional_max_minutes


@dataclass(frozen=True, slots=True)
class InformationPattern:
    """A quantum-information pattern in the astral interface, and who may change it.

    ``mutable`` is the scene's own statement that this pattern can be edited at all. A scene's editable symbolic
    scenery does not imply that atoms, records or identities are editable.
    """

    pattern_id: str
    owner_id: str
    mutable: bool = False

    def __post_init__(self) -> None:
        if not self.pattern_id.strip() or not self.owner_id.strip():
            raise AstralRankError("a pattern needs an id and an owner")


def may_edit(rank: int, actor_id: str, pattern: InformationPattern, *, mandate: bool = False) -> bool:
    """Whether this rank may edit this pattern.

    Rank 3 edits its **own** information. Another agent's pattern needs both a mutable pattern and an authored
    mandate; rank alone never grants it. Rank 4's plane access does not change this rule.
    """
    if not pattern.mutable:
        return False
    if pattern.owner_id == actor_id:
        return has(rank, Capability.EDIT_OWN_INFORMATION)
    return has(rank, Capability.EDIT_MANDATED_INFORMATION) and mandate


def require_edit(rank: int, actor_id: str, pattern: InformationPattern, *, mandate: bool = False) -> None:
    """Refuse an edit with a reason, rather than silently doing nothing."""
    if not may_edit(rank, actor_id, pattern, mandate=mandate):
        if not pattern.mutable:
            raise AstralRankError(f"{pattern.pattern_id} is not editable in this scene")
        if pattern.owner_id != actor_id:
            raise AstralRankError(
                f"{pattern.pattern_id} belongs to another agent; rank alone does not grant it "
                "(a mutable pattern plus an authored mandate is required)"
            )
        raise AstralRankError(f"rank {rank} cannot edit information")
    return None


@dataclass(frozen=True, slots=True)
class Projector:
    """An actor's astral skill rank, checked against the campaign's own ceiling.

    Deliberately not a second character sheet: it holds the rank and the actor id, and asks
    :func:`has` for everything else. The projection itself stays `astral_body.Projection`.
    """

    actor_id: str
    rank: int

    def __post_init__(self) -> None:
        if not self.actor_id.strip():
            raise AstralRankError("a projector is an actor")
        rank_spec(self.rank)

    def can(self, capability: Capability) -> bool:
        return has(self.rank, capability)

    def may_start_campaign(self) -> bool:
        return self.rank <= CAMPAIGN_MAX_STARTING_RANK
