"""Astral projection and Noöspace travel — issue #224 (parent epic #200).

**Status: PROVISIONAL, NOT CANONICAL.** ``IS_CANONICAL = False``. Every number here is a
placeholder for author calibration; the author owns the final values. ``AGENTS.md`` §4 reserves
psionic mechanics and #224 asks for a *procedure*, not a recalibration.

The ontology is canon and lives in `RULEBOOK.md` §40.4 (#119): Noöspace **is** the Astral Plane
and the Conscious Agent Network, with near / collective-unconscious / biospheric / Noöspheric /
deep regions and navigation by resonance rather than distance. This module consumes that.

It consumes three existing specifications rather than restating them:

* the **state machine** — ``src.rules.cross_domain_state`` (#225) owns the four states, the
  body-control rule, the transition legality, and the AP economy;
* the **difficulty ladder** — ``src.rules.core`` (#131/#217), which reads
  ``data/rules/core.json``;
* the **wound vocabulary** — ``RULEBOOK.md`` §51, for what happens to an undefended body.

What this module adds is only the projection-specific procedure: access routes, depth, the
resonance model, temporal ambiguity, the uncertainty of dream-versus-shared information, and
return.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from . import core
from .cross_domain_state import (
    AP_COSTS,
    AP_PER_EXCHANGE,
    ASTRAL_PROJECTED,
    CYBER_IMMERSED,
    EMBODIED,
    INVOLUNTARY_DREAM_NDE,
    NOOSPACE,
    REALMS,
    assert_can_act_in,
    assert_transition,
    can_act_in,
    controls_body,
    legal_transition,
    realms_for,
)

IS_CANONICAL = False
PROVISIONAL = True

ASTRA = "astral"  # the vocabulary §40.4 uses for the plane
PLANE_ALIASES: tuple[str, ...] = ("Noöspace", "the Astral Plane")


class AccessRoute(str, Enum):
    """How a projection is entered (§40.4.5's access list, reduced to distinct mechanics)."""

    TRAINED = "trained"            # meditation, Focus-state technique, sensory deprivation
    LUCID_DREAM = "lucid-dream"    # sleep-state transition
    PSYCHEDELIC = "psychedelic"    # DMT and related
    PSYCHOTRONIC = "psychotronic"  # device, QIP interface, neural implant
    RITUAL = "ritual"              # ceremonial / CE-5 contact
    INVOLUNTARY = "involuntary"    # trauma, NDE, bled-through dream
    NHI_ASSISTED = "nhi-assisted"  # contact-mediated

    @property
    def voluntary(self) -> bool:
        return self is not AccessRoute.INVOLUNTARY


#: PROVISIONAL: which state an access route enters, and whether the body stays controlled.
#: Only the routes that leave the body in Noöspace are projections; a lucid dream that does not
#: separate is still ``involuntary-dream-nde`` in #225's vocabulary.
ROUTE_STATE: dict[AccessRoute, str] = {
    AccessRoute.TRAINED: ASTRAL_PROJECTED,
    AccessRoute.LUCID_DREAM: INVOLUNTARY_DREAM_NDE,
    AccessRoute.PSYCHEDELIC: ASTRAL_PROJECTED,
    AccessRoute.PSYCHOTRONIC: ASTRAL_PROJECTED,
    AccessRoute.RITUAL: ASTRAL_PROJECTED,
    AccessRoute.INVOLUNTARY: INVOLUNTARY_DREAM_NDE,
    AccessRoute.NHI_ASSISTED: ASTRAL_PROJECTED,
}


class Region(str, Enum):
    """The five Noetic regions of §40.4.3. Ordered from near to deep."""

    NEAR = "near"
    COLLECTIVE = "collective-unconscious"
    BIOSPHERIC = "biospheric"
    NOOSPHERIC = "noospheric"
    DEEP = "deep"


REGION_ORDER: tuple[Region, ...] = (
    Region.NEAR, Region.COLLECTIVE, Region.BIOSPHERIC, Region.NOOSPHERIC, Region.DEEP,
)

#: PROVISIONAL: how reliable human categories are in each region. §40.4.3's governing design
#: rule is "the deeper Noöspace becomes, the less reliable human categories become", so this
#: must be strictly decreasing with depth.
CATEGORY_RELIABILITY: dict[Region, float] = {
    Region.NEAR: 0.9,
    Region.COLLECTIVE: 0.7,
    Region.BIOSPHERIC: 0.55,
    Region.NOOSPHERIC: 0.45,
    Region.DEEP: 0.2,
}

#: PROVISIONAL: information you cannot tell apart from your own imagination.
UNCERTAINTY_BY_REGION: dict[Region, float] = {
    Region.NEAR: 0.1,
    Region.COLLECTIVE: 0.25,
    Region.BIOSPHERIC: 0.4,
    Region.NOOSPHERIC: 0.5,
    Region.DEEP: 0.75,
}


class Direction(str, Enum):
    DEEPER = "deeper"
    NEARER = "nearer"


def shift_region(current: Region, direction: Direction, steps: int = 1) -> Region:
    """Move along the near..deep axis, saturating at both ends."""
    if steps < 0:
        raise ValueError("steps must be non-negative; use Direction to choose the sign")
    index = REGION_ORDER.index(current)
    delta = steps if direction is Direction.DEEPER else -steps
    index = max(0, min(index + delta, len(REGION_ORDER) - 1))
    return REGION_ORDER[index]


def deeper(current: Region, steps: int = 1) -> Region:
    return shift_region(current, Direction.DEEPER, steps)


def nearer(current: Region, steps: int = 1) -> Region:
    return shift_region(current, Direction.NEARER, steps)


# ---------------------------------------------------------------------------
# Navigation: resonance, not distance
# ---------------------------------------------------------------------------

#: PROVISIONAL resonance inputs. §40.4.3: "'Near' and 'far' are practical human metaphors for
#: resonance, informational distance, entanglement, familiarity, symbolic association, and
#: cognitive accessibility" -- so navigation must not consume Euclidean distance at all.
RESONANCE_WEIGHTS: dict[str, float] = {
    "familiarity": 1.0,
    "symbolic_association": 0.8,
    "emotional_state": 0.6,
    "intention": 0.6,
    "memory": 0.5,
    "technological_assistance": 0.7,
    "learned_technique": 0.9,
    "agent_contact": 0.5,
}


def resonance_score(**factors: float) -> float:
    """Weighted resonance toward a target, 0.0 .. 1.0.

    Unknown factors are rejected: a navigation factor the chapter does not name must not be
    invented at the call site.
    """
    unknown = set(factors) - set(RESONANCE_WEIGHTS)
    if unknown:
        raise ValueError(f"unknown resonance factor(s) {sorted(unknown)}; "
                         f"§40.4.3 names {sorted(RESONANCE_WEIGHTS)}")
    total = sum(RESONANCE_WEIGHTS[k] * max(0.0, min(1.0, float(v))) for k, v in factors.items())
    ceiling = sum(RESONANCE_WEIGHTS.values())
    return total / ceiling


def navigation_dv(*, region: Region, resonance: float, base_dv: int = 13) -> int:
    """DV to reach a target, from resonance and depth.

    PROVISIONAL. Deeper regions and low resonance both make navigation harder; the result is a
    plain DV on the core ladder, so navigation is resolved by the normal check.
    """
    if not 0.0 <= resonance <= 1.0:
        raise ValueError("resonance must be in 0.0..1.0")
    depth = REGION_ORDER.index(region)
    dv = int(base_dv) + depth * 2 + int(round((1.0 - resonance) * 6))
    return dv


def navigation_difficulty(*, region: Region, resonance: float, base_dv: int = 13) -> str:
    """The named rung for a navigation DV, snapped onto the core ladder."""
    dv = navigation_dv(region=region, resonance=resonance, base_dv=base_dv)
    ladder = core.DIFFICULTY_LADDER
    rung = ladder[0]
    for value in ladder:
        if value <= dv:
            rung = value
        else:
            break
    return core.DIFFICULTIES[rung]


# ---------------------------------------------------------------------------
# The body: present, vulnerable, uncontrolled
# ---------------------------------------------------------------------------

#: PROVISIONAL: while projected, the body is defenceless against a deliberate attack.
BODY_DEFENCE_WHILE_PROJECTED = "passive-only"

#: PROVISIONAL: temporal ambiguity. Noöspace time does not map 1:1 onto spacetime.
TIME_RATIO_BY_REGION: dict[Region, float] = {
    Region.NEAR: 1.0,
    Region.COLLECTIVE: 1.5,
    Region.BIOSPHERIC: 2.0,
    Region.NOOSPHERIC: 3.0,
    Region.DEEP: 6.0,
}


def elapsed_in_spacetime(*, region: Region, subjective_minutes: float) -> float:
    """Spacetime minutes that pass for ``subjective_minutes`` inside a region.

    DEEP Noöspace includes "nonlinear causality", so this is a *rate*, never a reliable clock --
    the chapter says the information cannot be trusted, not that the arithmetic is exact.
    """
    if subjective_minutes < 0:
        raise ValueError("subjective time cannot be negative")
    return subjective_minutes * TIME_RATIO_BY_REGION[region]


def body_in_danger(*, state: str, deliberately_attacked: bool) -> bool:
    """A projected body cannot defend itself, so an attack on it is unopposed."""
    return state in (ASTRAL_PROJECTED, CYBER_IMMERSED, INVOLUNTARY_DREAM_NDE) \
        and deliberately_attacked


def can_act_through_body(state: str) -> bool:
    """The explicit rule: a projected consciousness cannot intentionally act via its body."""
    return controls_body(state)


def check_remote_action(*, state: str, realm: str) -> None:
    """Raise unless a projected consciousness may act in ``realm`` right now.

    This is the permission boundary the issue asks to test: a projection acts in Noöspace, not
    in Physical or Social space, and cannot reach through its own body.
    """
    assert_can_act_in(state, realm)


# ---------------------------------------------------------------------------
# Information: dream, private imagination, or shared Noöspace?
# ---------------------------------------------------------------------------

class InformationSource(str, Enum):
    """§40.4.1: the experiencer "is not necessarily inventing a private fantasy world"."""

    SHARED_NOOSPACE = "shared-noospace"
    PERSONAL_IMAGINATION = "personal-imagination"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class Perception:
    """A perceived fact with a confidence, never a verdict.

    This mirrors the anti-shortcut rule that governs sensors and identity verification: the
    setting's own rule is that appearance is evidence with a confidence.
    """

    content: str
    source: InformationSource
    confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in 0.0..1.0")


def perceived_information(*, region: Region, corroborated: bool,
                          same_region_witnesses: int = 0) -> InformationSource:
    """Classify perceived Noöspace information.

    PROVISIONAL. Deeper regions make it progressively harder to separate shared Noöspace from
    one's own imagination; corroboration by another witness inside the same region is the way
    out. Nothing here reaches certainty by inspection alone.
    """
    if same_region_witnesses < 0:
        raise ValueError("witness count cannot be negative")
    if not corroborated:
        return InformationSource.AMBIGUOUS
    if same_region_witnesses >= 1:
        return InformationSource.SHARED_NOOSPACE
    return InformationSource.AMBIGUOUS


def confidence_in(*, region: Region, source: InformationSource,
                  corroborated: bool) -> float:
    """Confidence for a perceived fact, bounded and region-dependent."""
    base = 1.0 - UNCERTAINTY_BY_REGION[region]
    if source is InformationSource.SHARED_NOOSPACE and corroborated:
        return min(1.0, base + 0.1)
    if source is InformationSource.PERSONAL_IMAGINATION:
        return max(0.0, base - 0.4)
    return base * 0.6


# ---------------------------------------------------------------------------
# Encounters
# ---------------------------------------------------------------------------

class EncounterKind(str, Enum):
    """§40.4.1's Conscious Agent classes, at the level a procedure needs."""

    INDIVIDUAL_MIND = "individual-mind"
    COLLECTIVE_FORMATION = "collective-formation"
    ARCHETYPAL_FIGURE = "archetypal-figure"
    DREAM_ENTITY = "dream-entity"
    MACHINE_ELF = "self-transforming-machine-elf"
    NOETIC_AI = "noetic-ai"
    NONHUMAN = "nonhuman-intelligence"


#: PROVISIONAL: an encounter is resolved as a normal check; these are the Skills that apply.
ENCOUNTER_SKILLS: dict[EncounterKind, str] = {
    EncounterKind.INDIVIDUAL_MIND: "Telepathy",
    EncounterKind.COLLECTIVE_FORMATION: "Telepathy",
    EncounterKind.ARCHETYPAL_FIGURE: "Perceive",
    EncounterKind.DREAM_ENTITY: "Perceive",
    EncounterKind.MACHINE_ELF: "Psychic Defence",
    EncounterKind.NOETIC_AI: "Psychic Defence",
    EncounterKind.NONHUMAN: "Psychic Defence",
}


def encounter_skill(kind: EncounterKind) -> str:
    return ENCOUNTER_SKILLS[kind]


def encounter_dv(*, kind: EncounterKind, region: Region, hostile: bool,
                 base_dv: int = 13) -> int:
    """PROVISIONAL encounter DV. Depth and hostility both raise it."""
    dv = int(base_dv) + REGION_ORDER.index(region) * 2 + (3 if hostile else 0)
    if kind is EncounterKind.NONHUMAN:
        dv += 3
    return dv


# ---------------------------------------------------------------------------
# Return
# ---------------------------------------------------------------------------

class ReturnKind(str, Enum):
    VOLUNTARY = "voluntary"
    SNAP_BACK = "snap-back"    # involuntary, e.g. shock to the body
    SEVERANCE = "severance"    # the link is cut; the worst case


#: PROVISIONAL: return cost in AP, and which returns leave a cost behind.
RETURN_AP: dict[ReturnKind, int] = {
    ReturnKind.VOLUNTARY: AP_COSTS["exit"],
    ReturnKind.SNAP_BACK: 0,
    ReturnKind.SEVERANCE: 0,
}

#: PROVISIONAL: what a return leaves behind, as §51 wound-ladder vocabulary.
RETURN_AFTERMATH: dict[ReturnKind, str | None] = {
    ReturnKind.VOLUNTARY: None,
    ReturnKind.SNAP_BACK: "Scratched",
    ReturnKind.SEVERANCE: "Wounded",
}


def return_cost(kind: ReturnKind) -> int:
    return RETURN_AP[kind]


def return_aftermath(kind: ReturnKind) -> str | None:
    """The wound state a return inflicts, or None. Never invents a new ladder state."""
    return RETURN_AFTERMATH[kind]


def can_return(state: str) -> bool:
    """Only a projected or dream state has anywhere to return *from*."""
    return state in (ASTRAL_PROJECTED, CYBER_IMMERSED, INVOLUNTARY_DREAM_NDE)


# ---------------------------------------------------------------------------
# The procedure, assembled
# ---------------------------------------------------------------------------

@dataclass
class Projection:
    """One character's projection: a projection is a state, not a Skill roll."""

    actor_id: str
    route: AccessRoute
    region: Region = Region.NEAR
    state: str = field(init=False)

    def __post_init__(self) -> None:
        self.state = ROUTE_STATE[self.route]

    @property
    def voluntary(self) -> bool:
        return self.route.voluntary

    def navigate(self, *, resonance: float, direction: Direction, steps: int = 1) -> Region:
        """Change region. Navigation is legal only while projected into Noöspace."""
        if not can_act_in(self.state, NOOSPACE):
            raise ValueError(f"{self.state} cannot navigate Noöspace")
        if resonance < 0.25:
            raise ValueError("navigation needs a minimum of resonance; low resonance is not travel")
        self.region = shift_region(self.region, direction, steps)
        return self.region

    def return_to_body(self, kind: ReturnKind) -> str:
        if not can_return(self.state):
            raise ValueError(f"{self.state} has nowhere to return from")
        assert_transition(self.state, EMBODIED)
        self.state = EMBODIED
        return self.state


def astral_realms() -> frozenset[str]:
    """Realms reachable from the astral state — #225's answer, not a second one."""
    return realms_for(ASTRAL_PROJECTED)


def ap_price(action: str) -> int:
    """AP for a projection action, from #225's table (never re-declared here)."""
    if action not in AP_COSTS:
        raise ValueError(f"unknown action {action!r}; #225 defines {sorted(AP_COSTS)}")
    return AP_COSTS[action]
