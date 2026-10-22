"""GQ-CAN PSI: trajectory steering on the one Fate resolver.

Ported from the *Ubiquitous Maniacs* corpus (``archive/ubiquitous-maniacs-2026-10/src/rpg/
psi.py``) onto this repository's engine, so that the corpus's material and the live RPG are
**one** system rather than two parallel ones.

What changed in the port, and why
---------------------------------

**The skill vocabulary.** The corpus resolved PSI against a seven-attribute skill system with
named skills of its own. This repository's engine has **six** individual skills
(:data:`strategy_game.rpg.skills.INDIVIDUAL_SKILL_NAMES`) and a vocabulary of *competence tags*
for capabilities. The port therefore resolves every PSI mode against the engine's six skills,
and gates modes that need a capability on the existing tag vocabulary — so a character without
the capability is refused **before any dice**, exactly as the rest of the engine behaves.

**The resolver.** The corpus carried its own Fate kernel. The port uses the live one
(:func:`strategy_game.rpg.fate.resolve`), so a PSI check is a check like any other: same dice,
same shifts, same outcomes, same stress.

What it models
--------------

PSI is treated as **trajectory steering**, not as a spell list. A mode is a way of acting; the
scene's own properties — how far the target is semantically from you, how open the situation is
to branching, how much the feeling is salient, how much noise is present — decide how hard the
action is, and the character's **psi rating** and the **consensus** around them decide how much
the attempt is helped or hindered. Four things follow from that:

* an **intuition** check creates an advantage; a **remote perception** check overcomes a
  problem; a **psychic hack** attacks; a **noetic defence** defends;
* the pressure a result puts on the psyche depends on how instrumental the target was — a
  machine is cheap to touch, a person is not;
* **consensus** and **doubt** are mechanical: believers reinforce, doubters suppress, and both
  are capped symmetrically;
* a **belief tag** is a bonus, and a belief is never a capability.

What it is not
--------------

Not a second resolution mechanic, not a new skill, and not a claim about ontology. It moves no
strategic state, and it decides no outcome on its own: the fiction still decides what a
successful remote perception *means*. It is the *scene layer's* PSI, and it composes with the
existing mission-level PSI seam (:mod:`strategy_game.psi_operations`) rather than replacing it.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from random import Random

from .fate import Action, Character, Outcome, resolve

__all__ = [
    "ConsensusTables",
    "CrossLayerEffect",
    "PsiActionContext",
    "PsiActionResult",
    "PsiMode",
    "PsiPressure",
    "belief_bonus",
    "consensus_modifier",
    "resolve_psi_action",
]


class PsiMode(StrEnum):
    """The ways a character can act psychically.

    Each mode names a *kind of act*, not a power. What it can achieve is decided by the scene
    and the fiction, not by this list.
    """

    INTUITION = "intuition"
    TELEPATHY = "telepathy"
    REMOTE_PERCEPTION = "remote_perception"
    PRECOGNITION = "precognition"
    PSYCHOKINESIS = "psychokinesis"
    RESONANCE = "resonance"
    SYNCHRONICITY = "synchronicity"
    RITUAL = "ritual"
    SHARED_DREAM = "shared_dream"
    PSYCHOSURGERY = "psychosurgery"
    PSYCHIC_HACKING = "psychic_hacking"
    NOETIC_DEFENSE = "noetic_defense"
    NOETIC_RECONNAISSANCE = "noetic_reconnaissance"


@dataclass(frozen=True)
class ConsensusTables:
    """The three tuned tables the model reads.

    The corpus loaded these from a JSON file that was never committed upstream; the values are
    therefore **baked in** here, which is also what makes the model deterministic and testable
    without a data directory.
    """

    #: The highest psi rating a character can carry.
    psi_rating_max: int = 6
    #: How many rating points make one step, how much a step is worth, and the ceiling.
    rating_per_step: int = 2
    rating_bonus_per_step: int = 1
    rating_cap: int = 2
    #: What one believer and one doubter are worth, and the ceiling on the total.
    believer_modifier: int = 1
    doubter_modifier: int = -1
    consensus_cap: int = 3
    #: What a matching belief tag is worth.
    belief_bonus: int = 1

    @classmethod
    def default(cls) -> ConsensusTables:
        return cls()


#: The tables the model reads. A caller may substitute their own.
TABLES = ConsensusTables.default()


@dataclass(frozen=True)
class PsiActionContext:
    """The scene facts that make a trajectory easier or harder to steer.

    Every field is a *situation* property, not a character property. The character contributes
    through their rating and through the belief and competence tags; this is the world.
    """

    #: How far the target is from the actor in meaning. Resistive.
    semantic_distance: int = 0
    #: How strongly the situation supports a directed change. Supportive.
    corridor_strength: int = 0
    #: How open the situation is to branching. Supportive.
    bifurcation_openness: int = 0
    #: How salient the feeling is. Supportive.
    affective_salience: int = 0
    #: How coherent the target's own field is. Supportive.
    composite_coherence: int = 0
    #: How instrumental the target is — how much of a machine or a system it is. Resistive, and
    #: it is also what makes an attempt *cheap* on the psyche.
    instrumentality: int = 0
    #: How much local noise there is. Resistive.
    local_noise: int = 0
    #: The actor's psi rating, 0 to :attr:`ConsensusTables.psi_rating_max`.
    psi_rating: int = 0
    #: How many around the actor already believe. Supportive.
    believers: int = 0
    #: How many around the actor doubt. Resistive.
    doubters: int = 0

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            if name == "psi_rating":
                continue
            if value < 0 or value > 4:
                raise ValueError(f"{name} must be between 0 and 4")
        if self.psi_rating < 0 or self.psi_rating > TABLES.psi_rating_max:
            raise ValueError(f"psi_rating must be between 0 and {TABLES.psi_rating_max}")

    @property
    def trajectory_modifier(self) -> int:
        """The situational modifier this scene contributes to the check.

        Support minus resistance, halved, then the rating and the consensus added, and the
        whole thing clamped to ±4 — so no scene can make an action trivially easy or impossible.
        """
        support = (
            self.corridor_strength
            + self.bifurcation_openness
            + self.affective_salience
            + self.composite_coherence
        )
        resistance = self.semantic_distance + self.instrumentality + self.local_noise
        modifier = int((support - resistance) / 2)
        modifier += self._rating_modifier() + self._consensus_modifier()
        return max(-4, min(4, modifier))

    def _rating_modifier(self) -> int:
        steps = self.psi_rating // max(1, TABLES.rating_per_step)
        return min(TABLES.rating_cap, steps * TABLES.rating_bonus_per_step)

    def _consensus_modifier(self) -> int:
        raw = self.believers * TABLES.believer_modifier + self.doubters * TABLES.doubter_modifier
        return max(-TABLES.consensus_cap, min(TABLES.consensus_cap, raw))


@dataclass(frozen=True)
class PsiPressure:
    """What an attempt costs the psyche, and what it leaves behind.

    ``psyche_load`` is the immediate strain, ``noetic_trace`` is how much of the actor is now
    visible in the target's field, and ``instability`` is how much the attempt destabilised
    the actor.
    """

    psyche_load: int = 0
    noetic_trace: int = 0
    instability: int = 0


@dataclass(frozen=True)
class CrossLayerEffect:
    """A change that crosses from one layer to another.

    ``consent_required`` is the same gate the psychosurgery module applies: an effect that
    changes someone needs their agreement, and the effect reports whether it is permitted
    rather than being applied silently.
    """

    source_layer: str
    target_layer: str
    interface: str
    trigger: str
    consent_required: bool = False
    consent: bool | None = None
    reversible: bool = True
    provenance: tuple[str, ...] = ()

    @property
    def permitted(self) -> bool:
        return not self.consent_required or self.consent is True


@dataclass(frozen=True)
class PsiActionResult:
    """The result of one psychical act: the check, the mode, the scene, and the pressure."""

    outcome: Outcome
    shifts: int
    mode: PsiMode
    context: PsiActionContext
    pressure: PsiPressure
    skill: str
    dice: tuple[int, int, int, int]
    total: int
    difficulty: int
    cross_layer_effects: tuple[CrossLayerEffect, ...] = ()

    @property
    def succeeded(self) -> bool:
        return self.outcome in (Outcome.SUCCESS, Outcome.SUCCESS_WITH_STYLE)

    @property
    def style(self) -> bool:
        return self.outcome is Outcome.SUCCESS_WITH_STYLE

    @property
    def applicable_cross_layer_effects(self) -> tuple[CrossLayerEffect, ...]:
        """Only the effects a *successful* act may carry, and only the permitted ones."""
        if not self.succeeded:
            return ()
        return tuple(effect for effect in self.cross_layer_effects if effect.permitted)


#: How each mode acts: the engine skill it rolls, the action it is, and the domain it touches.
#:
#: The skill is one of the engine's six. A mode whose fiction needs a capability is gated on the
#: existing tag vocabulary instead, so the gate is refused before any dice.
_MODE_PROFILE: dict[PsiMode, tuple[str, Action, str, str]] = {
    PsiMode.INTUITION: ("INT", Action.CREATE_ADVANTAGE, "noetic", ""),
    PsiMode.TELEPATHY: ("SAV", Action.CREATE_ADVANTAGE, "noetic", "TELEPATH"),
    PsiMode.REMOTE_PERCEPTION: ("INT", Action.OVERCOME, "noetic", "REMOTE_VIEWER"),
    PsiMode.PRECOGNITION: ("INT", Action.CREATE_ADVANTAGE, "noetic", ""),
    PsiMode.PSYCHOKINESIS: ("WIL", Action.OVERCOME, "physical", ""),
    PsiMode.RESONANCE: ("SAV", Action.CREATE_ADVANTAGE, "noetic", ""),
    PsiMode.SYNCHRONICITY: ("INT", Action.CREATE_ADVANTAGE, "noetic", ""),
    PsiMode.RITUAL: ("SAV", Action.CREATE_ADVANTAGE, "noetic", ""),
    PsiMode.SHARED_DREAM: ("SAV", Action.CREATE_ADVANTAGE, "noetic", ""),
    PsiMode.PSYCHOSURGERY: ("COG", Action.OVERCOME, "noetic", "PSYCHOSURGERY"),
    PsiMode.PSYCHIC_HACKING: ("WIL", Action.ATTACK, "noetic", ""),
    PsiMode.NOETIC_DEFENSE: ("WIL", Action.DEFEND, "noetic", ""),
    PsiMode.NOETIC_RECONNAISSANCE: ("INT", Action.OVERCOME, "noetic", "REMOTE_VIEWER"),
}


def consensus_modifier(believers: int, doubters: int) -> int:
    """What the room believes is worth, mechanically.

    Believers reinforce, doubters suppress, and the total is capped symmetrically, so a large
    crowd of believers cannot make an act certain.
    """
    raw = believers * TABLES.believer_modifier + doubters * TABLES.doubter_modifier
    return max(-TABLES.consensus_cap, min(TABLES.consensus_cap, raw))


def belief_bonus(character: Character, domain: str) -> int:
    """What a matching belief tag is worth.

    A belief is a **tag of kind ``belief``** whose value names the domain. It is a bonus, never
    a capability: a character cannot *do* a thing because they believe in it, they can only do
    it a little more surely once they are already able.
    """
    for tag in character.tags_of_kind("belief"):
        if tag.value == domain:
            return TABLES.belief_bonus
    return 0


def _pressure_for(outcome: Outcome, context: PsiActionContext) -> PsiPressure:
    """What the result costs.

    An instrumental target is cheap to touch and leaves little trace; a person is expensive.
    """
    if outcome is Outcome.SUCCESS_WITH_STYLE:
        return PsiPressure(noetic_trace=max(0, context.instrumentality - 2))
    if outcome is Outcome.SUCCESS:
        return PsiPressure(psyche_load=1, noetic_trace=max(0, context.instrumentality - 1))
    if outcome is Outcome.TIE:
        return PsiPressure(1, 1 + context.instrumentality // 2, 1)
    if outcome is Outcome.FAILURE:
        return PsiPressure(1, context.instrumentality // 2, 1)
    return PsiPressure(2, 1 + context.instrumentality // 2, 2)


def resolve_psi_action(
    actor: Character,
    target: str,
    mode: PsiMode,
    difficulty: int,
    *,
    context: PsiActionContext | None = None,
    rng: Random,
    roll: int | None = None,
    cross_layer_effects: tuple[CrossLayerEffect, ...] = (),
) -> PsiActionResult:
    """Resolve one psychical act as trajectory steering.

    ``roll`` supplies a fixed dice total for a pinned test; ``rng`` is the otherwise. The
    capability gate is checked **before** anything is rolled, so a character without the
    capability cannot attempt the act at a lower rating and be mistaken for a hard try.
    """
    from .skills import require_capability

    active_context = context or PsiActionContext()
    skill, action, _domain, capability = _MODE_PROFILE[mode]
    if capability:
        require_capability(actor, capability)

    rating = actor.skills.get(skill, 0)
    modifier = active_context.trajectory_modifier + belief_bonus(actor, mode.value)
    resolved = resolve(action, rating, difficulty, rng=rng, bonus=modifier)
    if roll is not None:
        # A pinned roll replaces the dice but not the arithmetic.
        total = roll + rating + modifier
        shifts = total - difficulty
        outcome = (
            Outcome.FAILURE if shifts < 0
            else Outcome.TIE if shifts == 0
            else Outcome.SUCCESS_WITH_STYLE if shifts >= 3
            else Outcome.SUCCESS
        )
        resolved = type(resolved)(
            resolved.action, resolved.dice, resolved.skill, resolved.difficulty,
            total, shifts, outcome,
        )

    return PsiActionResult(
        outcome=resolved.outcome,
        shifts=resolved.shifts,
        mode=mode,
        context=active_context,
        pressure=_pressure_for(resolved.outcome, active_context),
        skill=skill,
        dice=resolved.dice,
        total=resolved.total,
        difficulty=difficulty,
        cross_layer_effects=cross_layer_effects,
    )
