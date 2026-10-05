"""Deterministic resolver seam between Concordia/LLM output and the event log.

Issue #111 core: STAT + Skill + 1d10 vs Difficulty Value. The LLM may propose
intent, but code owns the roll and arithmetic. Undefined rules remain unresolved.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Mapping

from rules import AttributeSet, CheckResult, resolve_check

UNRESOLVED_NO_RULE = "no_canonical_rule_for_action"
UNRESOLVED_NO_TARGET = "no_difficulty_specified"
UNRESOLVED_NO_ATTRIBUTE = "no_stat_specified"
UNRESOLVED_NO_CAPABILITY = "no_capability_specified"
UNRESOLVED_BLOCKED = "skill_not_available"
UNRESOLVED_EMPTY_ACTION = "empty_action"

UNRESOLVED_REASONS = (
    UNRESOLVED_NO_RULE,
    UNRESOLVED_NO_TARGET,
    UNRESOLVED_NO_ATTRIBUTE,
    UNRESOLVED_NO_CAPABILITY,
    UNRESOLVED_BLOCKED,
    UNRESOLVED_EMPTY_ACTION,
)


class Decision(str, Enum):
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True, slots=True)
class Capability:
    """The explicit STAT and Skill inputs selected for this action.

    attribute_id is retained as an adapter field name; semantically it names a STAT.
    Final STAT and Skill lists are intentionally not locked by issue #111.
    """

    attribute_id: str
    skill_level: int = 1
    has_skill: bool = True


@dataclass(frozen=True, slots=True)
class ProposedAction:
    actor: str
    intent: str
    action_type: str = ""
    target: str = ""
    location: str = ""
    visibility: str = "public"
    check: Mapping[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class Resolution:
    decision: Decision
    proposal: ProposedAction
    outcome: CheckResult | None = None
    reason: str = ""
    rule: str = ""
    note: str = ""

    @property
    def resolved(self) -> bool:
        return self.decision is Decision.RESOLVED

    def event_content(self) -> str:
        if self.resolved and self.outcome is not None:
            verdict = "success" if self.outcome.success else "failure"
            return (
                f"{self.proposal.intent} "
                f"[check: STAT {self.outcome.stat} + Skill {self.outcome.skill} "
                f"+ 1d10 {self.outcome.die} = {self.outcome.total} "
                f"vs DV {self.outcome.target} -> {verdict}]"
            ).strip()
        return f"{self.proposal.intent} [unresolved: {self.reason}]".strip()

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "decision": self.decision.value,
            "actor": self.proposal.actor,
            "intent": self.proposal.intent,
            "reason": self.reason,
            "rule": self.rule,
            "note": self.note,
        }
        if self.outcome is not None:
            payload["outcome"] = asdict(self.outcome)
        return payload


def resolve_proposal(
    proposal: ProposedAction,
    *,
    attributes: AttributeSet | None = None,
    capability: Capability | None = None,
    rules: Mapping[str, Any] | None = None,
    dice_total: int | None = None,
    **_compat: Any,
) -> Resolution:
    """Resolve one action through the shared issue #111 core."""
    if not str(proposal.intent or "").strip():
        return Resolution(Decision.UNRESOLVED, proposal, reason=UNRESOLVED_EMPTY_ACTION)

    action_key = str(proposal.action_type or "").strip()
    rule = (rules or {}).get(action_key) if action_key else None
    if rule is None:
        return Resolution(
            Decision.UNRESOLVED,
            proposal,
            reason=UNRESOLVED_NO_RULE,
            note="No canonical rule is registered for this action type.",
        )

    if attributes is None or capability is None:
        return Resolution(
            Decision.UNRESOLVED,
            proposal,
            reason=UNRESOLVED_NO_CAPABILITY,
            rule=action_key,
        )
    if not capability.has_skill:
        return Resolution(
            Decision.UNRESOLVED,
            proposal,
            reason=UNRESOLVED_BLOCKED,
            rule=action_key,
            note="Issue #111 does not yet define an unskilled procedure.",
        )

    try:
        stat = attributes[capability.attribute_id]
    except KeyError:
        return Resolution(
            Decision.UNRESOLVED,
            proposal,
            reason=UNRESOLVED_NO_ATTRIBUTE,
            rule=action_key,
        )

    target = rule.get("difficulty")
    if target is None and proposal.check:
        target = proposal.check.get("difficulty")
    if target is None:
        return Resolution(
            Decision.UNRESOLVED,
            proposal,
            reason=UNRESOLVED_NO_TARGET,
            rule=action_key,
        )

    outcome = resolve_check(
        stat=stat,
        skill=capability.skill_level,
        target=int(target),
        die=dice_total,
    )
    return Resolution(Decision.RESOLVED, proposal, outcome=outcome, rule=action_key)


class ResolverSeam:
    def __init__(self, simulation: Any) -> None:
        if simulation is None:
            raise ValueError("ResolverSeam needs a simulation to guard")
        self._simulation = simulation
        self._committed: list[Resolution] = []

    @property
    def simulation(self) -> Any:
        return self._simulation

    @property
    def resolutions(self) -> tuple[Resolution, ...]:
        return tuple(self._committed)

    def commit(self, resolution: Resolution, *, turn: int | None = None) -> Any:
        if not isinstance(resolution, Resolution):
            raise TypeError("ResolverSeam.commit accepts only a Resolution.")
        proposal = resolution.proposal
        event = self._simulation.emit(
            actor=proposal.actor,
            action_type=proposal.action_type or resolution.rule or "action",
            target=proposal.target,
            content=resolution.event_content(),
            location=proposal.location,
            visibility=proposal.visibility,
            source="concordia",
            turn=turn,
        )
        self._committed.append(resolution)
        return event

    def resolve_and_commit(self, proposal: ProposedAction, **kwargs: Any) -> tuple[Resolution, Any]:
        resolution = resolve_proposal(proposal, **kwargs)
        return resolution, self.commit(resolution)

    def unresolved(self) -> tuple[Resolution, ...]:
        return tuple(r for r in self._committed if not r.resolved)

    def summary(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for resolution in self._committed:
            counts[resolution.decision.value] = counts.get(resolution.decision.value, 0) + 1
        reasons: dict[str, int] = {}
        for resolution in self.unresolved():
            reasons[resolution.reason] = reasons.get(resolution.reason, 0) + 1
        return {
            "committed": len(self._committed),
            "decisions": counts,
            "unresolved_reasons": reasons,
        }
