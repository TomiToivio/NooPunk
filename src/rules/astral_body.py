"""The Astral Body MVP (#1261, author update of 2026-11-06).

The issue withdraws the old "no astral combat" line and replaces it with something narrower and more
testable: a **projected Astral Body** that has locatable presence, can be attacked and can attack,
while the physical body stays where it was. This module implements only the parts that are
*structural* — state, perception filters, action rights, target eligibility — and refuses the parts
that need an author-approved bridge (astral damage to CWN health) or a published ruling (which SWN
techniques may target astral bodies).

Three rules are load-bearing and are enforced here rather than described:

1. **One actor, one body.** Projection is a state of the actor, not a second character. `body_location`
   cannot change while projected, and returning restores the embodied state without a duplicate.
2. **Perception is filtered by mode, not by goodwill.** In Time/Space a projector cannot see physical
   objects at all; in Space/Time it can, but fallibly. The filter is a function, not a note.
3. **Entry is scripted.** Sleep, NDE, psychotronics or an authored event. There is no will-power
   projection and no selectable discipline; nothing here grants a power.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class AstralBodyError(ValueError):
    """A projection, perception or targeting call that the rules do not allow."""


class Embodiment(str, Enum):
    EMBODIED = "embodied"
    PROJECTED = "projected"
    RETURNED = "returned"


class PerceptionMode(str, Enum):
    """How the projector's interface renders Noöspace. Not a place — a mode of representation."""

    SPACE_TIME = "space_time"
    TIME_SPACE = "time_space"


class EntryTrigger(str, Enum):
    """The only ways a projection starts. Absence of "at will" is the point."""

    SLEEP = "sleep"            # spontaneous OOBE while sleeping or dreaming
    NDE = "nde"                # near-death experience
    PSYCHOTRONIC = "psychotronic"  # Monroe-style apparatus or authorised session
    AUTHORED = "authored"      # a plot event Tomi wrote


class TargetKind(str, Enum):
    PHYSICAL = "physical"
    ASTRAL_AGENT = "astral_agent"
    SYMBOL = "symbol"


@dataclass(frozen=True, slots=True)
class Perception:
    """Whether a projector perceives something, and how much to trust it."""

    allowed: bool
    reliable: bool
    reason: str = ""

    def __bool__(self) -> bool:
        return self.allowed


#: The perception contract, executable. The middle column is the one people forget: near-physical
#: astral sight is *fallible*, so "I saw it in the astral" is a lead, never a proof.
_PERCEPTION: dict[tuple[Embodiment, PerceptionMode | None, TargetKind], Perception] = {}


def _register(embodiment: Embodiment, mode: PerceptionMode | None, kind: TargetKind,
              allowed: bool, reliable: bool, reason: str) -> None:
    _PERCEPTION[(embodiment, mode, kind)] = Perception(allowed, reliable, reason)


# Embodied and returned: ordinary senses, and no free astral sight.
for _state in (Embodiment.EMBODIED, Embodiment.RETURNED):
    _register(_state, None, TargetKind.PHYSICAL, True, True, "ordinary senses")
    _register(_state, None, TargetKind.ASTRAL_AGENT, False, False,
              "no direct astral sight without a permitted effect")
    _register(_state, None, TargetKind.SYMBOL, False, False, "symbols need an interface")

# Projected, near-physical: the room, but not reliably.
_register(Embodiment.PROJECTED, PerceptionMode.SPACE_TIME, TargetKind.PHYSICAL, True, False,
          "near-physical representation is fallible and not line of sight")
_register(Embodiment.PROJECTED, PerceptionMode.SPACE_TIME, TargetKind.ASTRAL_AGENT, True, True,
          "astral agents are the native population here")
_register(Embodiment.PROJECTED, PerceptionMode.SPACE_TIME, TargetKind.SYMBOL, True, False,
          "symbols read through a familiar headset")

# Projected, inner: meaning, not matter.
_register(Embodiment.PROJECTED, PerceptionMode.TIME_SPACE, TargetKind.PHYSICAL, False, False,
          "Time/Space does not render physical objects as physical objects")
_register(Embodiment.PROJECTED, PerceptionMode.TIME_SPACE, TargetKind.ASTRAL_AGENT, True, True,
          "conscious agents are directly present")
_register(Embodiment.PROJECTED, PerceptionMode.TIME_SPACE, TargetKind.SYMBOL, True, True,
          "symbol and meaning are the medium")


def perceive(embodiment: Embodiment, mode: PerceptionMode | None, kind: TargetKind) -> Perception:
    try:
        return _PERCEPTION[(embodiment, mode, kind)]
    except KeyError:
        raise AstralBodyError(f"no perception contract for {embodiment}/{mode}/{kind}") from None


def can_perceive(embodiment: Embodiment, mode: PerceptionMode | None, kind: TargetKind) -> bool:
    return perceive(embodiment, mode, kind).allowed


@dataclass
class Projection:
    """One actor, projected. The physical body does not move and is not duplicated."""

    actor_id: str
    body_location: str
    trigger: EntryTrigger
    mode: PerceptionMode = PerceptionMode.SPACE_TIME
    astral_location: str = ""
    manifestation: str = "hidden"   # hidden | visible (never tangible without an authored effect)
    esp_visible: bool = False       # detected by ESP or an authorised sensor
    active: bool = True
    memories: list[str] = field(default_factory=list)
    interpretations: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.actor_id.strip():
            raise AstralBodyError("a projection belongs to an actor")
        if not self.body_location.strip():
            raise AstralBodyError("a projection needs the physical body's location")
        if self.mode is PerceptionMode.TIME_SPACE and self.astral_location == self.body_location:
            raise AstralBodyError(
                "Time/Space has no physical coordinates; an astral location is symbolic"
            )

    # -- state ------------------------------------------------------------------------------
    @property
    def embodiment(self) -> Embodiment:
        return Embodiment.PROJECTED if self.active else Embodiment.RETURNED

    @property
    def body_is_fixed(self) -> bool:
        """While projected, the body stays where it was. There is no second body to move."""
        return self.active

    def sees(self, kind: TargetKind) -> Perception:
        return perceive(self.embodiment, self.mode if self.active else None, kind)

    def may_take_physical_action(self) -> bool:
        """A projected Astral Body cannot punch a door, pick up a gun or fire one."""
        return not self.active

    def may_speak_to_material(self) -> bool:
        """Only an authored manifestation with the speech channel enabled would allow this."""
        return False

    # -- transitions ------------------------------------------------------------------------
    def shift_mode(self, mode: PerceptionMode, *, authored: bool = False) -> Projection:
        """Switching from near-physical to inner Noöspace is an authored transition, not a toggle."""
        if not authored:
            raise AstralBodyError(
                "shifting between Space/Time and Time/Space needs an authored transition"
            )
        self.mode = mode
        return self

    def manifest(self, *, channel: str = "sight") -> Projection:
        """Become perceptible to physical witnesses without becoming tangible."""
        if channel not in ("sight", "sound", "sight_and_sound"):
            raise AstralBodyError(f"unknown manifestation channel {channel!r}")
        self.manifestation = "visible"
        return self

    def return_to_body(self) -> Projection:
        """End the projection. The actor is embodied again, at the same location, once."""
        if not self.active:
            return self
        self.active = False
        return self

    def record(self, memory: str, interpretation: str = "") -> None:
        """What the player saw and what they made of it are different records."""
        if not self.active:
            raise AstralBodyError("a returned projector cannot add new astral memories")
        self.memories.append(memory)
        if interpretation:
            self.interpretations.append(interpretation)


def begin_projection(
    actor_id: str,
    body_location: str,
    trigger: EntryTrigger | str,
    *,
    mode: PerceptionMode | str = PerceptionMode.SPACE_TIME,
    astral_location: str = "",
) -> Projection:
    """Start a scripted projection. There is deliberately no 'at will' trigger."""
    try:
        entry = trigger if isinstance(trigger, EntryTrigger) else EntryTrigger(trigger)
    except ValueError:
        raise AstralBodyError(
            f"{trigger!r} is not an entry trigger; projection is scene-triggered, never a power"
        ) from None
    perception = mode if isinstance(mode, PerceptionMode) else PerceptionMode(mode)
    return Projection(actor_id=actor_id, body_location=body_location, trigger=entry,
                       mode=perception, astral_location=astral_location)


# --------------------------------------------------------------------------- #
# Targeting: who may hit whom, and with what
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class Combatant:
    """How an actor is present for the purpose of being hit."""

    actor_id: str
    physically_present: bool
    astrally_present: bool = False
    manifestation: str = "hidden"   # hidden | visible
    has_esp: bool = False


@dataclass(frozen=True, slots=True)
class Eligibility:
    allowed: bool
    reason: str

    def __bool__(self) -> bool:
        return self.allowed


def astral_can_target(attacker: Projection, target: Combatant) -> Eligibility:
    """Astral Body to Astral Body. The attacker must be projected; the target must be present."""
    if not attacker.active:
        raise AstralBodyError("an embodied actor cannot make an astral attack")
    if not target.astrally_present:
        return Eligibility(False, "the target is not astrally present")
    return Eligibility(True, "both combatants are astrally present")


def physical_can_target(attacker_embodied: bool, target: Combatant) -> Eligibility:
    """A gun does not shoot a projection.

    A merely visible apparition is not tangible, and a hidden one is not even seen. Only an
    explicitly authored tangible manifestation changes this, and that is not modelled here.
    """
    if not attacker_embodied:
        raise AstralBodyError("an embodied attack comes from an embodied actor")
    if target.physically_present:
        return Eligibility(True, "the target is physically present")
    if target.manifestation == "hidden" and not target.has_esp:
        return Eligibility(False, "the projection is not perceptible to ordinary senses")
    return Eligibility(False, "a manifested astral form is visible, not tangible")


def detect_by_esp(observer_has_esp: bool, target: Projection) -> bool:
    """ESP may reveal a projector; ordinary eyes may not."""
    return bool(observer_has_esp and target.active)


# --------------------------------------------------------------------------- #
# Deliberately unimplemented, and loudly so
# --------------------------------------------------------------------------- #

#: The astral-to-physical damage bridge needs an author-approved adapter. Until then nothing here
#: may reduce CWN health, and a caller that tries gets a sentence rather than a number.
ASTRAL_DAMAGE_BRIDGE_APPROVED = False


def apply_astral_damage(*_args: object, **_kwargs: object) -> None:
    raise AstralBodyError(
        "the astral-to-physical damage bridge is not approved (#1261 §B.5); "
        "resolve the encounter with CWN combat and record the consequence in the scene"
    )


#: A projection grants no discipline, technique or resource. This function exists so a caller can
#: assert the absence rather than remember it.
def unlocked_disciplines(_projection: Projection) -> tuple[str, ...]:
    return ()


def requires_authored_transition(from_mode: PerceptionMode, to_mode: PerceptionMode) -> bool:
    """Any mode change is authored. Within a mode, movement is scene business."""
    return from_mode is not to_mode


# --------------------------------------------------------------------------- #
# The superskill: ranks 0-4, and the MVP window of 0-1 (author update 2026-11-06)
# --------------------------------------------------------------------------- #
#: Astral Projection is an *Astral-domain* superskill, not a general-purpose power: it does almost
#: nothing in a Physical or Cyber scene and everything inside Noöspace. Each rank is a model of
#: reality, a perception and a capability at once, so a higher rank is not "more minutes outside".


class AstralRank(IntEnum):
    DISORIENTATION = 0        # unfamiliar; near Astral, may not tell dream from waking
    LUCID = 1                 # lucid flight, Lower Astral, dreams seen being built
    AGENT_NETWORK = 2         # conscious-agent network, ROTE, learn an Ident
    AUTHORIZED_AGENCY = 3     # Use Ident, permission-gated quantum-information editing
    COSMOLOGICAL = 4          # Devachanic/Etheric/Buddhic, Akashic research, timelines


#: The initial campaign allows 0 or 1. 2-4 are design-only until a later campaign needs them.
MVP_RANKS: tuple[AstralRank, ...] = (AstralRank.DISORIENTATION, AstralRank.LUCID)

#: **Provisional** caps, retained only as ceilings until the author settles them. Not a promise that
#: a long projection yields reliable knowledge.
PROVISIONAL_MINUTES: dict[AstralRank, int] = {
    AstralRank.DISORIENTATION: 10,
    AstralRank.LUCID: 60,
    AstralRank.AGENT_NETWORK: 600,
    AstralRank.AUTHORIZED_AGENCY: 2880,
    AstralRank.COSMOLOGICAL: 10080,
}

#: Planes, in the order the setting climbs them. The first three are reachable inside the MVP; the
#: upper three are Level 4 by the author's ordering correction, not Level 2.
PLANES: tuple[str, ...] = (
    "near_astral",
    "lower_astral",
    "astral",
    "devachanic",
    "etheric",
    "buddhic",
)

_PLANES_BY_RANK: dict[AstralRank, frozenset[str]] = {
    AstralRank.DISORIENTATION: frozenset({"near_astral"}),
    AstralRank.LUCID: frozenset({"near_astral", "lower_astral", "astral"}),
    AstralRank.AGENT_NETWORK: frozenset({"near_astral", "lower_astral", "astral"}),
    AstralRank.AUTHORIZED_AGENCY: frozenset({"near_astral", "lower_astral", "astral"}),
    AstralRank.COSMOLOGICAL: frozenset(PLANES),
}

#: The only ways an Ident may be learned. A name, an address, a photograph or a body is none of them.
IDENT_SOURCES: tuple[str, ...] = ("authored_encounter", "consensual_exchange", "recognition_technique")


@dataclass(frozen=True, slots=True)
class AstralSkill:
    """One character's Astral Projection rank, with the gates the rank actually opens."""

    rank: AstralRank = AstralRank.DISORIENTATION

    @classmethod
    def starting(cls, rank: AstralRank | int = 0) -> AstralSkill:
        """Character creation: 0 or 1. Rank 2-4 is earned later, never picked at session one."""
        value = rank if isinstance(rank, AstralRank) else AstralRank(int(rank))
        if value not in MVP_RANKS:
            raise AstralBodyError(
                f"Astral Projection {int(value)} is not available at character creation; the initial "
                f"campaign allows {tuple(int(r) for r in MVP_RANKS)}"
            )
        return cls(rank=value)

    # -- model of reality --------------------------------------------------------------------
    @property
    def understands_quantum_information(self) -> bool:
        return self.rank >= AstralRank.AGENT_NETWORK

    @property
    def understands_interface(self) -> bool:
        """Rank 3+: an appearance is a rendering of information, not the information."""
        return self.rank >= AstralRank.AUTHORIZED_AGENCY

    # -- capability --------------------------------------------------------------------------
    @property
    def can_fly(self) -> bool:
        return self.rank >= AstralRank.LUCID

    @property
    def can_enter_lower_astral(self) -> bool:
        return self.rank >= AstralRank.LUCID

    @property
    def can_send_rote(self) -> bool:
        return self.rank >= AstralRank.AGENT_NETWORK

    @property
    def can_learn_ident(self) -> bool:
        return self.rank >= AstralRank.AGENT_NETWORK

    @property
    def can_use_ident(self) -> bool:
        return self.rank >= AstralRank.AUTHORIZED_AGENCY

    @property
    def can_edit_quantum_information(self) -> bool:
        """Permission, not raw power: the caller must still own the pattern (see `may_edit`)."""
        return self.rank >= AstralRank.AUTHORIZED_AGENCY

    @property
    def can_research_cosmology(self) -> bool:
        return self.rank >= AstralRank.COSMOLOGICAL

    def planes(self) -> frozenset[str]:
        return _PLANES_BY_RANK[self.rank]

    def may_enter(self, plane: str) -> bool:
        return plane in self.planes()

    def duration_cap_minutes(self) -> int:
        return PROVISIONAL_MINUTES[self.rank]

    def may_edit(self, *, owner: str, editor: str) -> bool:
        """Level-3 editing is scoped: your own information, or a limbo you are authorised to shape."""
        if not self.can_edit_quantum_information:
            return False
        return owner in (editor, "limbo:unclaimed")


@dataclass(frozen=True, slots=True)
class Ident:
    """A Conscious Agent's persistent noetic address — not a name, a body or a consent token.

    Eternal only while **the same agent** exists: reincarnation, resleeving and uploading keep it,
    a copy or fork does not inherit it. Permanent is not reachable: wards and the projector's rank
    decide whether *this* jump arrives.
    """

    agent_id: str

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise AstralBodyError("an Ident names an agent, not a body")

    def survives(self, event: str) -> bool:
        """Continuity events keep the Ident; duplication is exactly the case that does not."""
        if event in ("death", "reincarnation", "resleeve", "upload"):
            return True
        if event in ("copy", "fork", "simulation"):
            return False
        raise AstralBodyError(f"unknown continuity event {event!r}")


def learn_ident(skill: AstralSkill, agent_id: str, *, via: str) -> Ident:
    """Learn an Ident at rank 2+. A name in a file is not a route: the *source* is required."""
    if not skill.can_learn_ident:
        raise AstralBodyError(
            f"learning an Ident is Astral Projection {int(AstralRank.AGENT_NETWORK)}; "
            f"this character is {int(skill.rank)}"
        )
    if via not in IDENT_SOURCES:
        raise AstralBodyError(
            f"{via!r} does not establish an Ident; expected one of {IDENT_SOURCES}"
        )
    return Ident(agent_id=agent_id)


def use_ident(
    projection: Projection,
    skill: AstralSkill,
    ident: Ident,
    *,
    ward: str = "",
    plane: str = "astral",
) -> Projection:
    """Relocate the *Astral Body* to a known agent's present astral locus — instantly, once.

    Never the physical body, never a second actor, and never a way around a ward: a blocked arrival
    says so without naming where the agent is.
    """
    if not skill.can_use_ident:
        raise AstralBodyError(
            f"Use Ident is Astral Projection {int(AstralRank.AUTHORIZED_AGENCY)}; "
            f"this character is {int(skill.rank)}"
        )
    if not projection.active:
        raise AstralBodyError("only a projected Astral Body can use an Ident")
    if not skill.may_enter(plane):
        raise AstralBodyError(
            f"Astral Projection {int(skill.rank)} does not reach the {plane} plane"
        )
    if ward:
        raise AstralBodyError(
            f"the arrival is refused by a ward ({ward}); the agent's location is not revealed"
        )
    projection.astral_location = f"presence:{ident.agent_id}"
    return projection
