"""Phase-1 solo campaign arc: scenes, checks, consequences, endings (#950).

Deliberately engine-free. The scene chain does not know whether it is being driven by an Evennia command,
a CLI, or a test, and it never imports Evennia. Rules resolution is injected as a callable, so the same arc
can run on the CWN kernel today and on anything else later without the campaign code changing.

Two rules are load-bearing and are tested:

1. **No dead ends.** A failed check costs you a clue, never the case. GUMSHOE's core-clue principle applied to
   a scripted GM: the player may reach a weaker ending, but never a wall.
2. **Consequences are recorded, not implied.** Every failure writes an entry the ending reads, so the ending
   is a function of what happened rather than a caption chosen for mood.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Callable

# skill -> difficulty key the caller resolves; names are NoöPunk-side labels wired to CWN skills by the host.
STAGES = ("briefing", "kurvi", "records", "confrontation", "report", "complete")

Resolve = Callable[[str, str, tuple[int, ...]], bool]


@dataclass
class Arc:
    stage: str = "briefing"
    clues: list[str] = field(default_factory=list)
    consequences: list[str] = field(default_factory=list)
    ending: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Arc":
        return cls(stage=data.get("stage", "briefing"),
                   clues=list(data.get("clues", [])),
                   consequences=list(data.get("consequences", [])),
                   ending=data.get("ending"))


def _need(arc: Arc, action: str, stage: str, choices) -> bool:
    return arc.stage == stage and action in choices


def advance(arc: Arc, action: str, resolve: Resolve, *, dice: tuple[int, ...] = ()) -> tuple[Arc, str]:
    """Apply one action. Returns (new_state, text). Rejected actions never mutate the arc."""
    a = Arc.from_dict(arc.to_dict())
    action = action.strip().lower()

    if action == "status":
        return a, _status(a)

    if _need(a, action, "briefing", {"accept"}):
        a.stage = "kurvi"
        return a, "Assignment accepted. Kurvi first: a witness saw the researcher last."

    if _need(a, action, "kurvi", {"interview"}):
        if resolve("Notice", "routine", dice):
            if "witness" not in a.clues:
                a.clues.append("witness")
            return a, "The witness places a university badge beside an unmarked vehicle."
        a.consequences.append("witness_uncooperative")
        a.stage = "records"
        return a, ("The witness will not talk to a new graduate. Nothing is lost but the testimony - "
                   "university records remain.")

    if _need(a, action, "kurvi", {"leave"}):
        a.stage = "records"
        return a, "You leave Kurvi and take the tram to the university."

    if _need(a, action, "records", {"records"}):
        if resolve("Notice", "routine", dice):
            if "records" not in a.clues:
                a.clues.append("records")
            a.stage = "confrontation"
            return a, "Access logs place the researcher in the laboratory after closing."
        a.consequences.append("records_incomplete")
        a.stage = "confrontation"
        return a, "The logs are incomplete. You have enough to ask a question, not enough to prove one."

    if _need(a, action, "confrontation", {"press"}):
        if not a.clues:
            a.consequences.append("confronted_without_evidence")
            a.stage = "report"
            return a, ("You press with nothing but suspicion. It is refused, and the refusal is on record.")
        a.stage = "report"
        return a, "The badge number does not match the badge. Someone was issued a dead man's credentials."

    if _need(a, action, "report", {"submit"}):
        a.ending = _ending(a)
        a.stage = "complete"
        return a, f"Case closed: {a.ending}"

    return a, "That action is unavailable here or at this stage. Use 'status'."


def _ending(a: Arc) -> str:
    if len(a.clues) >= 2 and not a.consequences:
        return "corroborated"
    if len(a.clues) >= 2:
        return "corroborated_with_gaps"
    if a.clues:
        return "partial"
    return "unsolved"


def _status(a: Arc) -> str:
    if a.stage == "complete":
        return f"Case closed: {a.ending}."
    return (f"Stage: {a.stage}. Clues: {', '.join(a.clues) or 'none'}. "
            f"Consequences: {', '.join(a.consequences) or 'none'}.")
