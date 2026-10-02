"""The mandatory resolver seam between Concordia/LLM output and the event log.

Issue #40 Phase C. The binding rule this module exists to enforce is
``docs/SIMULATION_ARCHITECTURE_SPEC.md`` §7.4:

> No LLM output may enter the event log except through the deterministic resolver.
> Where a canonical rule exists, the resolver must reach the rule through the shared
> rules layer — not through a re-implementation inside Concordia. Where no rule
> exists, the resolver must return an *explicit unresolved outcome*, not an
> improvised one.

Before this module the pieces existed separately: ``mechanics.py`` could resolve a
*check*, and ``simulation.engine`` could append an *event*, but nothing connected
them. An agent's proposed action could therefore be resolved to numbers and then
either vanish or reach the log by an ungoverned path.

Design:

* A proposal arrives as :class:`ProposedAction` — natural-language intent plus the
  structured fields the shared rules need. The LLM supplies *intent and words*; it
  never supplies dice, totals, or success.
* :func:`resolve_proposal` routes the action through the shared ``rules`` layer and
  returns a :class:`Resolution`. That is either ``RESOLVED`` (with the canonical
  numbers) or ``UNRESOLVED`` (with a reason), and it is the **only** input
  :meth:`ResolverSeam.commit` accepts.
* :meth:`ResolverSeam.commit` is the only function that appends to a
  ``simulation.Simulation``. It refuses a raw proposal, a raw string, and a
  hand-built event, so the seam cannot be bypassed by a caller that forgets it.

What this module deliberately does **not** do: it defines no skills, no targets, no
difficulty assignments, no factions, no social mechanics. Which skill or attribute
applies to an action, and which difficulty it faces, are tabletop decisions the
author has not made yet; those arrive as explicit inputs or the action is
UNRESOLVED. ``AGENTS.md`` §1/§2/§4/§14: an undefined rule becomes a visible gap, not
an invention.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

from rules import AttributeSet, CheckResult, SkillAccess, resolve_check

#: Why a proposal could not be resolved. Closed on purpose: a new reason is a
#: deliberate statement about a missing rule, not an ad-hoc string.
UNRESOLVED_NO_RULE = "no_canonical_rule_for_action"
UNRESOLVED_NO_TARGET = "no_difficulty_specified"
UNRESOLVED_NO_ATTRIBUTE = "no_attribute_specified"
UNRESOLVED_NO_CAPABILITY = "no_capability_specified"
UNRESOLVED_BLOCKED = "trained_only_without_skill"
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
    """What a character brings to a check.

    ``attribute_id`` names which of the six attributes the *tabletop* GM selected
    for this action. It is not chosen here: RULEBOOK §4 says the GM selects the
    attribute that fits the action, and skills are not permanently bound to one.
    """

    attribute_id: str
    skill_level: int = 0
    has_skill: bool = True
    skill_access: SkillAccess = SkillAccess.UNSKILLED_ALLOWED


@dataclass(frozen=True, slots=True)
class ProposedAction:
    """An action as proposed by an agent — LLM, human, or scripted.

    ``intent`` is natural language and is the only field an LLM may fill freely.
    ``check`` is the *structured* request: the caller (an orchestrator, or a GM
    adapter holding the tabletop decision) states which rule to apply. When
    ``check`` is missing, the action is not resolvable against a canonical rule and
    is reported as such rather than guessed.
    """

    actor: str
    intent: str
    action_type: str = ""
    target: str = ""
    location: str = ""
    visibility: str = "public"
    check: Mapping[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class Resolution:
    """The only thing the seam will commit to the event log."""

    decision: Decision
    proposal: ProposedAction
    #: Present only when RESOLVED.
    outcome: CheckResult | None = None
    #: Present only when UNRESOLVED.
    reason: str = ""
    #: The rule that decided it, for provenance. Empty when there was none.
    rule: str = ""
    note: str = ""

    @property
    def resolved(self) -> bool:
        return self.decision is Decision.RESOLVED

    def event_content(self) -> str:
        """The text recorded for this action.

        On a resolved check the canonical numbers are included so the log is
        self-describing; on an unresolved one the gap is recorded explicitly, which
        is the whole point of the seam (§7.4: a missing rule must be visible).
        """
        if self.resolved and self.outcome is not None:
            outcome = self.outcome
            verdict = "success" if outcome.success else "failure"
            return (
                f"{self.proposal.intent} "
                f"[check: 2d6={outcome.dice_total} + skill={outcome.skill_level} "
                f"+ attr={outcome.attribute_modifier} = {outcome.total} "
                f"vs difficulty {outcome.target} -> {verdict}]"
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
            payload["outcome"] = {
                "attempted": self.outcome.attempted,
                "dice_total": self.outcome.dice_total,
                "skill_level": self.outcome.skill_level,
                "attribute_modifier": self.outcome.attribute_modifier,
                "extra_modifiers": list(self.outcome.extra_modifiers),
                "unskilled_modifier": self.outcome.unskilled_modifier,
                "total": self.outcome.total,
                "target": self.outcome.target,
                "success": self.outcome.success,
            }
        return payload


def resolve_proposal(
    proposal: ProposedAction,
    *,
    attributes: AttributeSet | None = None,
    capability: Capability | None = None,
    rules: Mapping[str, Any] | None = None,
    dice_total: int | None = None,
    aid_bonus: int = 0,
) -> Resolution:
    """Route one proposed action through the shared rules layer.

    Returns ``RESOLVED`` with canonical numbers when a rule exists and its inputs
    are present, otherwise ``UNRESOLVED`` with an explicit reason. It never invents
    a difficulty, a skill, an attribute binding, or an outcome.

    ``rules`` is the registry of *canonical* actions this simulation knows about. It
    is supplied by the caller because defining which actions exist is a tabletop
    decision (``AGENTS.md`` §4); an action absent from it is UNRESOLVED, not
    improvised. ``dice_total`` is injectable for deterministic replay and tests only.
    """
    if not str(proposal.intent or "").strip():
        return Resolution(Decision.UNRESOLVED, proposal, reason=UNRESOLVED_EMPTY_ACTION,
                          note="an empty intent carries nothing to resolve")

    action_key = str(proposal.action_type or "").strip()
    rule = (rules or {}).get(action_key) if action_key else None
    if rule is None:
        return Resolution(
            Decision.UNRESOLVED, proposal, reason=UNRESOLVED_NO_RULE,
            note=(
                "no canonical rule is registered for this action type; "
                "RULEBOOK.md does not define it yet"
                if action_key
                else "no action type was stated, so no rule could be selected"
            ),
        )

    if attributes is None or capability is None:
        return Resolution(
            Decision.UNRESOLVED, proposal, reason=UNRESOLVED_NO_CAPABILITY,
            rule=action_key,
            note="resolving needs the acting character's attributes and capability",
        )

    try:
        attribute_modifier = attributes[capability.attribute_id]
    except KeyError:
        return Resolution(
            Decision.UNRESOLVED, proposal, reason=UNRESOLVED_NO_ATTRIBUTE,
            rule=action_key,
            note=f"unknown attribute {capability.attribute_id!r}; expected one of the six canonical ids",
        )

    target = rule.get("difficulty")
    if target is None and proposal.check:
        target = proposal.check.get("difficulty")
    if target is None:
        return Resolution(
            Decision.UNRESOLVED, proposal, reason=UNRESOLVED_NO_TARGET,
            rule=action_key,
            note="no difficulty is specified for this action; inventing one is not this layer's call",
        )
    target = int(target)

    extra: Iterable[int] = ()
    if proposal.check and proposal.check.get("extra_modifiers") is not None:
        extra = tuple(int(value) for value in proposal.check["extra_modifiers"])
    elif rule.get("extra_modifiers") is not None:
        extra = tuple(int(value) for value in rule["extra_modifiers"])

    outcome = resolve_check(
        attribute_modifier=attribute_modifier,
        target=target,
        skill_level=capability.skill_level,
        has_skill=capability.has_skill,
        extra_modifiers=extra,
        skill_access=capability.skill_access,
        dice_total=dice_total,
        aid_bonus=aid_bonus,
    )

    if not outcome.attempted:
        # A blocked trained-only attempt is a rule outcome, not a gap — but it is
        # still not a resolved check, and it must say so rather than read as failure.
        return Resolution(
            Decision.UNRESOLVED, proposal, outcome=outcome,
            reason=UNRESOLVED_BLOCKED, rule=action_key,
            note="trained-only action attempted without the skill; no dice were rolled",
        )

    return Resolution(Decision.RESOLVED, proposal, outcome=outcome, rule=action_key)


class ResolverSeam:
    """The only path from agent output into a simulation's event log.

    Construct it around a ``simulation.Simulation``. ``commit`` accepts only a
    :class:`Resolution`, so a caller cannot append a raw proposal, a model string,
    or a hand-made event. That refusal is the enforcement: the rule in §7.4 is a
    property of the code path, not a convention callers are asked to honour.
    """

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
        """Append the resolved action to the log and return the event.

        Raises ``TypeError`` for anything that is not a ``Resolution`` — including a
        ``ProposedAction`` or a plain string — because accepting those would be the
        bypass this seam exists to prevent.
        """
        if not isinstance(resolution, Resolution):
            raise TypeError(
                "ResolverSeam.commit accepts only a Resolution. A raw proposal or a "
                "model string must go through resolve_proposal first (spec §7.4)."
            )

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
        """Convenience: resolve, then commit. Returns ``(resolution, event)``."""
        resolution = resolve_proposal(proposal, **kwargs)
        return resolution, self.commit(resolution)

    def unresolved(self) -> tuple[Resolution, ...]:
        """The review queue: every action the canonical rules could not decide."""
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
