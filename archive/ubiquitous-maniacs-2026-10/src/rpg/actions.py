"""Unified Overcome/Create Advantage/Attack/Defend action API."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .dice import fixed_4df
from .models import Character, CheckResult, GraphEffect, ResultTier, SkillCheck
from .rules import resolve_check


class ActionType(StrEnum):
    OVERCOME = "overcome"
    CREATE_ADVANTAGE = "create_advantage"
    ATTACK = "attack"
    DEFEND = "defend"


@dataclass(frozen=True)
class ActionResult:
    action: ActionType
    check: CheckResult
    target: str | None = None
    created_aspect: str | None = None
    graph_effects: tuple[GraphEffect, ...] = ()

    @property
    def succeeded(self) -> bool:
        """Whether the intent advances, including Noöpunk's success-at-a-cost tier."""
        return self.check.tier in {
            ResultTier.CRITICAL_SUCCESS,
            ResultTier.SUCCESS,
            ResultTier.COSTLY_SUCCESS,
        }

    @property
    def clean_success(self) -> bool:
        """Whether the intent succeeds without the mandatory cost of a negative margin."""
        return self.check.tier in {ResultTier.CRITICAL_SUCCESS, ResultTier.SUCCESS}

    @property
    def requires_cost(self) -> bool:
        """Whether applying the progress also requires a negotiated or scripted cost."""
        return self.check.tier == ResultTier.COSTLY_SUCCESS

    @property
    def shifts(self) -> int:
        return max(0, self.check.margin)

    @property
    def applicable_graph_effects(self) -> tuple[GraphEffect, ...]:
        """Effects are permissions earned by a successful action, not failure payloads."""
        return self.graph_effects if self.succeeded else ()

    @property
    def applicable_created_aspect(self) -> str | None:
        """Return the created aspect only when the action actually advances."""
        return self.created_aspect if self.succeeded else None


def resolve_action(
    actor: Character,
    *,
    attribute: str,
    skill: str | None,
    difficulty: int,
    action: ActionType = ActionType.OVERCOME,
    roll: int | None = None,
    situational_modifier: int = 0,
    target: str | None = None,
    created_aspect: str | None = None,
    graph_effects: tuple[GraphEffect, ...] = (),
    stunt: str | None = None,
) -> ActionResult:
    """Resolve an action; ``roll`` is the deterministic 4dF total when supplied."""
    fate_die = None
    if roll is not None:
        values = iter(fixed_4df(roll))
        fate_die = lambda: next(values)
    check = resolve_check(
        actor,
        SkillCheck(
            attribute=attribute,
            skill=skill,
            difficulty=difficulty,
            situational_modifier=situational_modifier + (2 if stunt in actor.stunts else 0),
        ),
        fate_die,
    )
    return ActionResult(action, check, target, created_aspect, graph_effects)
