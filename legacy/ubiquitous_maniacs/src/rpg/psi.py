"""GQ-CAN PSI actions built on the shared Noöpunk action resolver."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from enum import StrEnum
from pathlib import Path
from typing import Any

from .actions import ActionResult, ActionType, resolve_action
from .models import Character, GraphEffect, ResultTier


# ── QIP psi-escalation tables (loaded once from data/rpg/psi_tables.json) ──

_PSI_TABLES: dict[str, Any] | None = None


def load_psi_tables(path: str | Path | None = None) -> dict[str, Any]:
    """Load the QIP escalation thresholds. Falls back to baked defaults if absent."""
    global _PSI_TABLES
    if _PSI_TABLES is not None and path is None:
        return _PSI_TABLES
    defaults = {
        "psi_rating_max": 6,
        "psi_rating_modifier": {"per_rating": 2, "bonus_per_step": 1, "cap": 2},
        "reality_shift": {"min_rating": 5, "min_tier": "critical_success",
                          "target_layer": "physical", "source_layer": "astral",
                          "interface": "noosphere_layer3"},
        "ontological_shock": {"threshold": 3, "target_layer": "physical",
                              "source_layer": "noetic"},
        "consensus": {"believer_modifier": 1, "doubter_modifier": -1, "cap": 3},
        "belief_tag": {"tag_prefix": "belief:", "bonus": 1},
        "three_humanities": {
            "denier": {"tag": "humanity:denier", "psi_blocked": True, "doubt_modifier": -1},
            "future_shocked": {"tag": "humanity:future_shocked", "psi_unstable": True},
            "awakened": {"tag": "humanity:awakened", "psi_blocked": False},
        },
    }
    if path is None:
        path = Path(__file__).resolve().parent.parent.parent / "data" / "rpg" / "psi_tables.json"
    try:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
        _PSI_TABLES = {**defaults, **loaded}
    except (FileNotFoundError, json.JSONDecodeError):
        _PSI_TABLES = defaults
    return _PSI_TABLES


class PsiMode(StrEnum):
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
class PsiActionContext:
    """Scene facts that make a trajectory easier or harder to steer."""

    semantic_distance: int = 0
    corridor_strength: int = 0
    bifurcation_openness: int = 0
    affective_salience: int = 0
    composite_coherence: int = 0
    instrumentality: int = 0
    local_noise: int = 0
    psi_rating: int = 0
    believers: int = 0
    doubters: int = 0

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            if name == "psi_rating":
                continue
            if value < 0 or value > 4:
                raise ValueError(f"{name} must be between 0 and 4")
        tables = load_psi_tables()
        max_rating = int(tables["psi_rating_max"])
        if self.psi_rating < 0 or self.psi_rating > max_rating:
            raise ValueError(f"psi_rating must be between 0 and {max_rating}")

    @property
    def trajectory_modifier(self) -> int:
        support = (
            self.corridor_strength
            + self.bifurcation_openness
            + self.affective_salience
            + self.composite_coherence
        )
        resistance = self.semantic_distance + self.instrumentality + self.local_noise
        modifier = int((support - resistance) / 2)
        # QIP psi-rating contribution (Pylkkänen spectrum) + Consensus/Doubt.
        modifier += self._rating_modifier() + self._consensus_modifier()
        return max(-4, min(4, modifier))

    def _rating_modifier(self) -> int:
        cfg = load_psi_tables()["psi_rating_modifier"]
        steps = self.psi_rating // max(1, int(cfg["per_rating"]))
        return min(int(cfg["cap"]), steps * int(cfg["bonus_per_step"]))

    def _consensus_modifier(self) -> int:
        cfg = load_psi_tables()["consensus"]
        raw = (self.believers * int(cfg["believer_modifier"])
               + self.doubters * int(cfg["doubter_modifier"]))
        cap = int(cfg["cap"])
        return max(-cap, min(cap, raw))


@dataclass(frozen=True)
class PsiPressure:
    psyche_load: int = 0
    noetic_trace: int = 0
    instability: int = 0


@dataclass(frozen=True)
class CrossLayerEffect:
    source_layer: str
    target_layer: str
    interface: str
    trigger: str
    effect: GraphEffect
    provenance: tuple[str, ...] = ()
    consent_required: bool = False
    consent: bool | None = None
    reversible: bool = True

    @property
    def permitted(self) -> bool:
        return not self.consent_required or self.consent is True


@dataclass(frozen=True)
class PsiActionResult:
    action_result: ActionResult
    mode: PsiMode
    context: PsiActionContext
    pressure: PsiPressure
    cross_layer_effects: tuple[CrossLayerEffect, ...] = ()

    @property
    def applicable_cross_layer_effects(self) -> tuple[CrossLayerEffect, ...]:
        if not self.action_result.succeeded:
            return ()
        return tuple(effect for effect in self.cross_layer_effects if effect.permitted)


_MODE_PROFILE: dict[PsiMode, tuple[str, str, ActionType, str]] = {
    PsiMode.INTUITION: ("Awareness", "Notice", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.TELEPATHY: ("Charisma", "Rapport", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.REMOTE_PERCEPTION: ("Awareness", "Notice", ActionType.OVERCOME, "noetic"),
    PsiMode.PRECOGNITION: ("Awareness", "Notice", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.PSYCHOKINESIS: ("Willpower", "Will", ActionType.OVERCOME, "physical"),
    PsiMode.RESONANCE: ("Charisma", "Rapport", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.SYNCHRONICITY: ("Awareness", "Investigate", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.RITUAL: ("Charisma", "Rapport", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.SHARED_DREAM: ("Charisma", "Rapport", ActionType.CREATE_ADVANTAGE, "noetic"),
    PsiMode.PSYCHOSURGERY: ("Intelligence", "Medicine", ActionType.OVERCOME, "noetic"),
    PsiMode.PSYCHIC_HACKING: ("Willpower", "Will", ActionType.ATTACK, "noetic"),
    PsiMode.NOETIC_DEFENSE: ("Willpower", "Will", ActionType.DEFEND, "noetic"),
    PsiMode.NOETIC_RECONNAISSANCE: ("Awareness", "Investigate", ActionType.OVERCOME, "noetic"),
}


def _pressure_for(tier: ResultTier, context: PsiActionContext) -> PsiPressure:
    if tier == ResultTier.CRITICAL_SUCCESS:
        return PsiPressure(noetic_trace=max(0, context.instrumentality - 2))
    if tier == ResultTier.SUCCESS:
        return PsiPressure(psyche_load=1, noetic_trace=max(0, context.instrumentality - 1))
    if tier == ResultTier.COSTLY_SUCCESS:
        return PsiPressure(1, 1 + context.instrumentality // 2, 1)
    if tier == ResultTier.FAILURE:
        return PsiPressure(1, context.instrumentality // 2, 1)
    return PsiPressure(2, 1 + context.instrumentality // 2, 2)


def resolve_psi_action(
    actor: Character,
    target: str,
    mode: PsiMode,
    difficulty: int,
    *,
    context: PsiActionContext | None = None,
    roll: int | None = None,
    cross_layer_effects: tuple[CrossLayerEffect, ...] = (),
) -> PsiActionResult:
    """Resolve PSI as trajectory steering, not a separate spell system."""
    active_context = context or PsiActionContext()
    attribute, skill, action, domain = _MODE_PROFILE[mode]
    provisional_effect = GraphEffect(domain, "adjust_edge", actor.id, target, mode.value, 1)
    action_result = resolve_action(
        actor,
        attribute=attribute,
        skill=skill,
        difficulty=difficulty,
        action=action,
        roll=roll,
        situational_modifier=active_context.trajectory_modifier,
        target=target,
        created_aspect=f"{mode.value}:{target}",
        graph_effects=(provisional_effect,),
    )
    strength = 2 if action_result.check.tier == ResultTier.CRITICAL_SUCCESS else 1
    action_result = replace(
        action_result,
        graph_effects=(replace(provisional_effect, value=strength),),
    )
    return PsiActionResult(
        action_result=action_result,
        mode=mode,
        context=active_context,
        pressure=_pressure_for(action_result.check.tier, active_context),
        cross_layer_effects=cross_layer_effects,
    )


def use_psi(
    actor: Character,
    target: str,
    mode: PsiMode,
    difficulty: int,
    *,
    roll: int | None = None,
    context: PsiActionContext | None = None,
) -> ActionResult:
    """Compatibility API returning the shared action result only."""
    return resolve_psi_action(
        actor,
        target,
        mode,
        difficulty,
        roll=roll,
        context=context,
    ).action_result


# ── QIP escalation layer (4dF-tiered ports of QIP.md mechanics) ─────────
#
# These add the mechanical escalation layer A's QIP.md describes (psi-ratings,
# Reality Shifts, Ontological Shock, Consensus/Doubt, Belief-as-mechanic) onto
# B's existing 4dF/Fate psi model — as tiered effects, NOT A's CP-RED stats.

@dataclass(frozen=True)
class RealityShift:
    """A Noösphere Layer-3 spacetime penetration event (QIP.md §Reality Shifts).

    Fired only on a CRITICAL_SUCCESS psi result at psi_rating >= min_rating.
    Local physics temporarily reconfigures; the ``effect`` is a CrossLayerEffect
    the caller can apply to a layered hacking session.
    """

    rating: int
    effect: CrossLayerEffect

    @property
    def target_layer(self) -> str:
        return self.effect.target_layer


def consensus_modifier(believers: int, doubters: int) -> int:
    """Consensus/Doubt modifier (QIP.md §Belief as a Mechanical Factor).

    Awakened believers reinforce a Noöspheric effect (+1 each); Denier doubters
    suppress it (-1 each). Capped symmetrically. Used as a situational modifier
    on psi/Noöspheric checks.
    """
    cfg = load_psi_tables()["consensus"]
    raw = believers * int(cfg["believer_modifier"]) + doubters * int(cfg["doubter_modifier"])
    cap = int(cfg["cap"])
    return max(-cap, min(cap, raw))


def belief_bonus(character: Character, domain: str) -> int:
    """Belief-as-mechanic: a 'belief:<domain>' tag grants a psi bonus in domain.

    Consistent with B's tag_bonus pattern in SkillCheck (models.py). Returns the
    configured bonus (default +1) when the character carries the matching belief
    tag, else 0.
    """
    cfg = load_psi_tables()["belief_tag"]
    prefix = str(cfg["tag_prefix"])
    if f"{prefix}{domain}" in character.tags:
        return int(cfg["bonus"])
    return 0


def psi_rating_for(character: Character) -> int:
    """Read a character's psi_rating from ``character.psyche['psi_rating']``.

    Clamped to the configured 0..max range. Defaults to 0 (psi-null) when unset.
    """
    tables = load_psi_tables()
    max_rating = int(tables["psi_rating_max"])
    raw = int(character.psyche.get("psi_rating", 0))
    return max(0, min(max_rating, raw))


def humanity_for(character: Character) -> int:
    """Humanity (HUM) analog — stored in ``character.psyche['humanity']``.

    QIP ties psi-burn and ontological shock to HUM loss. B has no HUM stat, so
    this is an optional scalar on the psyche dict; defaults to a stable 10.
    """
    return int(character.psyche.get("humanity", 10))


def ontological_shock(
    pressure: PsiPressure,
    rating: int,
    *,
    actor: Character | None = None,
    trigger: str = "noosphere_distortion",
) -> CrossLayerEffect | None:
    """Detect ontological shock (QIP.md §Ontological Shock).

    Triggers when accumulated ``PsiPressure.instability`` + ``rating`` crosses
    the configured threshold. On shock, returns a ``CrossLayerEffect`` describing
    a Noösphere-layer-3 reality distortion the caller can apply to a layered
    hacking session; otherwise returns ``None``. Does not mutate state.
    """
    cfg = load_psi_tables()["ontological_shock"]
    threshold = int(cfg["threshold"])
    if pressure.instability + rating < threshold:
        return None
    source = str(cfg["source_layer"])
    target = str(cfg["target_layer"])
    magnitude = pressure.instability + rating - threshold + 1
    effect = GraphEffect("noetic", "adjust_edge", source, target, "reality_distortion", magnitude)
    return CrossLayerEffect(
        source_layer=source,
        target_layer=target,
        interface="noosphere_layer3",
        trigger=trigger,
        effect=effect,
        consent_required=False,
        reversible=False,
    )


def reality_shift(
    tier: ResultTier,
    rating: int,
    *,
    actor: Character | None = None,
    source: str = "astral",
) -> RealityShift | None:
    """Detect a Reality Shift (QIP.md §Layer 3 / Reality Shifts).

    Fires only on a CRITICAL_SUCCESS psi result at psi_rating >= min_rating
    (default 5 — psi-master and above). Returns a ``RealityShift`` whose
    ``effect`` is a CrossLayerEffect bridging astral → physical; else ``None``.
    """
    cfg = load_psi_tables()["reality_shift"]
    if tier != ResultTier(str(cfg["min_tier"])):
        return None
    if rating < int(cfg["min_rating"]):
        return None
    target = str(cfg["target_layer"])
    source_layer = str(cfg["source_layer"])
    interface = str(cfg["interface"])
    magnitude = rating - int(cfg["min_rating"]) + 1
    effect = GraphEffect("noetic", "adjust_edge", source_layer, target, "reality_shift", magnitude)
    cross = CrossLayerEffect(
        source_layer=source_layer,
        target_layer=target,
        interface=interface,
        trigger="critical_psi_success",
        effect=effect,
        consent_required=False,
        reversible=False,
    )
    return RealityShift(rating=rating, effect=cross)
