"""Optional scene mechanics built on the original Fate Core-based resolution.

Fate Core System © Evil Hat Productions, licensed CC BY 3.0.
No Eclipse Phase setting text or noncommercial content is reproduced.
The GM still establishes fictional permission, costs, and narrative stakes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from random import Random

from .fate import Action, Character, Outcome, Resolution, ResourceError, resolve, roll_fate


@dataclass
class SceneAspect:
    name: str
    free_invocations: int = 0

    def __post_init__(self) -> None:
        if not self.name or self.free_invocations < 0:
            raise ResourceError("invalid scene aspect")


@dataclass
class Scene:
    aspects: dict[str, SceneAspect] = field(default_factory=dict)

    def create_aspect(self, name: str, *, free_invocations: int = 1) -> SceneAspect:
        if not name or name in self.aspects or free_invocations < 0:
            raise ResourceError("invalid or duplicate scene aspect")
        aspect = SceneAspect(name, free_invocations)
        self.aspects[name] = aspect
        return aspect

    def invoke(self, name: str, actor: Character, *, free: bool = False) -> int:
        aspect = self.aspects.get(name)
        if aspect is None:
            raise ResourceError("scene aspect does not exist")
        if free:
            if aspect.free_invocations < 1:
                raise ResourceError("no free invocations remain")
            aspect.free_invocations -= 1
        else:
            actor.spend_fate_point()
        return 2


@dataclass(frozen=True)
class Check:
    """All modifiers are recorded; dice are rolled only after permissions check."""
    resolution: Resolution
    invocation: str | None = None
    free: bool = False
    rerolled: bool = False


def check(
    actor: Character, action: Action, skill: str, difficulty: int, *,
    rng: Random, scene: Scene | None = None,
    invocation: str | None = None, free: bool = False,
    reroll: bool = False, permitted: bool = True,
) -> Check:
    if not permitted:
        raise ResourceError("fictional permission or target access was denied")
    if free and scene is None:
        raise ResourceError("free invocations require a tracked scene aspect")
    if invocation is None and (free or reroll):
        raise ResourceError("an invocation is required")
    bonus = 0
    if invocation:
        if scene is not None and invocation in scene.aspects:
            bonus = scene.invoke(invocation, actor, free=free)
        else:
            if free:
                raise ResourceError("only scene aspects have tracked free invokes")
            bonus = actor.invoke(invocation)
    first = resolve(action, actor.skills.get(skill, 0), difficulty, rng=rng)
    if reroll:
        dice = roll_fate(rng)
        total = sum(dice) + first.skill
        shifts = total - difficulty
        outcome = (
            Outcome.FAILURE if shifts < 0 else Outcome.TIE if shifts == 0
            else Outcome.SUCCESS_WITH_STYLE if shifts >= 3 else Outcome.SUCCESS
        )
        result = Resolution(action, dice, first.skill, difficulty, total, shifts, outcome)
    elif bonus:
        shifts = first.shifts + bonus
        outcome = (
            Outcome.FAILURE if shifts < 0 else Outcome.TIE if shifts == 0
            else Outcome.SUCCESS_WITH_STYLE if shifts >= 3 else Outcome.SUCCESS
        )
        result = Resolution(action, first.dice, first.skill, difficulty,
                            first.total + bonus, shifts, outcome)
    else:
        result = first
    return Check(result, invocation, free, reroll)


class ActionEffect(str, Enum):
    FAIL = "fail"
    TIE = "tie"
    SUCCEED = "succeed"
    SUCCEED_WITH_STYLE = "succeed_with_style"


#: Outcome -> ActionEffect. The two enums name the same four results differently
#: ("success" vs "succeed"), so the mapping is explicit rather than an accidental ``outcome.value``.
_EFFECT_BY_OUTCOME: dict[Outcome, ActionEffect] = {
    Outcome.FAILURE: ActionEffect.FAIL,
    Outcome.TIE: ActionEffect.TIE,
    Outcome.SUCCESS: ActionEffect.SUCCEED,
    Outcome.SUCCESS_WITH_STYLE: ActionEffect.SUCCEED_WITH_STYLE,
}


@dataclass(frozen=True)
class Interpretation:
    """Rules-facing signal; the GM chooses narrative consequences."""
    effect: ActionEffect
    shifts: int
    boost: bool
    free_invocations: int
    success_at_cost_option: bool
    stress_shifts: int


def interpret(result: Resolution) -> Interpretation:
    """Fate Core action-specific mechanical outputs without inventing narrative effects."""
    action, outcome, shifts = result.action, result.outcome, result.shifts
    style = outcome is Outcome.SUCCESS_WITH_STYLE
    success = outcome in (Outcome.SUCCESS, Outcome.SUCCESS_WITH_STYLE)
    return Interpretation(
        effect=_EFFECT_BY_OUTCOME[outcome],
        shifts=shifts,
        boost=(action in (Action.CREATE_ADVANTAGE, Action.DEFEND) and outcome is Outcome.TIE)
              or (action is Action.ATTACK and style),
        free_invocations=(2 if style else 1) if action is Action.CREATE_ADVANTAGE and success else 0,
        success_at_cost_option=action is Action.OVERCOME and outcome is Outcome.FAILURE,
        stress_shifts=max(0, shifts) if action is Action.ATTACK else 0,
    )


@dataclass(frozen=True)
class Hit:
    stress_box: int | None
    consequence: int | None
    taken_out: bool
    remaining: int


def apply_hit(
    target: Character, shifts: int, *, mental: bool = False,
    consequence: tuple[str, int] | None = None,
) -> Hit:
    """Allocate a hit to one stress box and at most one consequence.

    A consequence reduces shifts before selecting a stress box. If the
    remaining hit cannot be absorbed, the target is taken out. This
    routine never assumes a cortical-stack recovery or automatic death.
    """
    if shifts <= 0:
        raise ResourceError("hit must contain positive shifts")
    reduction = 0
    if consequence is not None:
        name, severity = consequence
        if severity not in (2, 4, 6) or not name:
            raise ResourceError("invalid consequence")
        if any(c.severity == severity and not c.recovered for c in target.consequences):
            raise ResourceError("consequence slot occupied")
        reduction = severity
    residual = max(0, shifts - reduction)
    track = target.mental_stress if mental else target.physical_stress
    box = next((i for i, used in enumerate(track, 1) if not used and i >= residual), None) if residual else None
    taken_out = bool(residual and box is None)
    # Commit only after validation; unabsorbed hits still record chosen consequences.
    if consequence:
        target.take_consequence(*consequence)
    if box is not None:
        track[box - 1] = True
    return Hit(box, reduction or None, taken_out, residual if taken_out else 0)


def compel(actor: Character, *, accepted: bool) -> bool:
    """An accepted compel awards one Fate point; refusal costs one."""
    if accepted:
        actor.fate_points += 1
    else:
        actor.spend_fate_point()
    return accepted


def refresh(actor: Character, rating: int = 3) -> None:
    """Start-session Fate-point floor. Existing higher balance is retained."""
    if rating < 0:
        raise ResourceError("refresh cannot be negative")
    actor.fate_points = max(actor.fate_points, rating)


def strategy_event_payload(actor: Character, result: Resolution) -> dict[str, object]:
    """Read-only handoff. NO faction turn, social propagation, or political rules."""
    return {"agent_id": actor.id, "action": result.action.value,
            "outcome": result.outcome.value, "shifts": result.shifts}
