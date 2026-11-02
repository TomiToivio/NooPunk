"""An agent adapter for the case session (#1084): an LLM may propose, only the rules may decide.

The architecture rule this file exists to enforce is one sentence long: *an adapter may read input,
render, persist and schedule, and it may not compute a check, decide damage, resolve a clue, or hold a
rule the plain package does not also expose.* An LLM in the loop is the adapter most likely to break
it, because a language model will happily narrate a clue it never found and a hit it never rolled.

So the agent gets exactly two things:

* ``observation()`` — what the character could know right now (scene, exits, the clues *they* hold, the
  board). It does not include anything the session has not recorded, and it never includes an answer.
* ``act(text)`` — one command, validated against the console's own verb list and arity, executed by
  :func:`console.play.run_command`, and reported back with the **engine's** state diff attached.

A rejected proposal is not an error the model should be allowed to talk its way out of: it comes back
as ``accepted: False`` with the reason and an empty ``changed`` list, and nothing about the session
moves. Concordia (or any other runtime) plugs in by supplying a callable that produces text; this
module imports no model provider, no network stack and no engine, which is what keeps the boundary
check green.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from .play import run_command
from .session import CaseSession

#: The verbs an agent may use, with the minimum and maximum argument count. Taken from the console's
#: dispatch table on purpose: if the console grows a verb and this list does not, the test fails.
VERBS: dict[str, tuple[int, int]] = {
    "look": (0, 0),
    "go": (1, 1),
    "clues": (0, 0),
    "take": (1, 1),
    "support": (1, 1),
    "contradict": (1, 1),
    "neutral": (1, 1),
    "theory": (1, 1),
    "hypotheses": (0, 0),
    "risk": (1, 2),
    "status": (0, 0),
    "conclude": (1, 8),
    "save": (0, 1),
    "help": (0, 0),
}


class AgentError(ValueError):
    """The proposal cannot be turned into an action at all."""


@dataclass(frozen=True)
class Proposal:
    """One thing an agent wants to do, and where it came from."""

    text: str
    author: str = "agent"


class AgentGate:
    """Mediates between an agent and one :class:`CaseSession`. It owns no rule."""

    def __init__(self, session: CaseSession) -> None:
        self.session = session
        self.history: list[dict] = []

    # ---- what the agent may see -----------------------------------------
    def observation(self) -> dict:
        """The player's knowledge, rendered as data.

        Deliberately absent: any field the session does not already hold, and anything resembling an
        answer. A model that needs to know more must ask the world through ``act()``.
        """
        scene = self.session.scene()
        return {
            "scene": {"id": scene.id, "title": scene.title},
            "exits": list(self.session.exits()),
            "open_clues": [
                {"id": clue_id, "fact": self.session.clue(clue_id).fact}
                for clue_id in self.session.open_clues()
            ],
            "discovered": list(self.session.discovered),
            "theory": self.session.theory_id,
            "readings": dict(self.session.evidence.get(self.session.theory_id, {})),
            "hypotheses": [{"id": h.id, "statement": h.statement}
                           for h in self.session.graph.hypotheses],
            "turns": self.session.turns,
            "concluded": self.session.concluded,
            "verbs": sorted(VERBS),
        }

    # ---- what the agent may do ------------------------------------------
    def validate(self, proposal: Proposal | str) -> tuple[str, str]:
        """Return ``(verb, reason)``; ``reason`` is empty when the proposal is well formed."""
        text = proposal.text if isinstance(proposal, Proposal) else str(proposal)
        parts = text.strip().split()
        if not parts:
            return "", "empty proposal"
        verb, args = parts[0].lower(), parts[1:]
        if verb not in VERBS:
            return verb, f"unknown verb {verb!r}; the case understands {', '.join(sorted(VERBS))}"
        low, high = VERBS[verb]
        if not low <= len(args) <= high:
            return verb, f"{verb} takes {low}..{high} arguments, got {len(args)}"
        if verb == "risk":
            try:
                int(args[0])
            except ValueError:
                return verb, "risk needs a numeric difficulty (8, 10 or 12)"
        return verb, ""

    def act(self, proposal: Proposal | str) -> dict:
        """Validate, execute through the console, and report the engine's own state diff."""
        text = proposal.text if isinstance(proposal, Proposal) else str(proposal)
        author = proposal.author if isinstance(proposal, Proposal) else "agent"
        _, reason = self.validate(text)
        before = self.session.to_dict()
        if reason:
            return self._record(author, text, accepted=False, reason=reason, output="",
                                changed=[], concluded=self.session.concluded)
        try:
            keep_going, output = run_command(self.session, text)
        except Exception as exc:  # noqa: BLE001 - a refused action must not kill the agent loop
            return self._record(author, text, accepted=False, reason=f"{type(exc).__name__}: {exc}",
                                output="", changed=[], concluded=self.session.concluded)
        after = self.session.to_dict()
        return self._record(author, text, accepted=True, reason="", output=output,
                            changed=_diff(before, after), concluded=self.session.concluded,
                            keep_going=keep_going)

    def run(self, proposer: Callable[[dict], str], *, max_turns: int = 12) -> list[dict]:
        """Drive an agent loop: hand it the observation, take one proposal, repeat.

        The loop stops on ``conclude``/``quit``, when the proposer returns nothing, or at
        ``max_turns`` — a model with no stopping condition must not be able to spin forever.
        """
        results: list[dict] = []
        for _ in range(max_turns):
            proposal = proposer(self.observation())
            if not proposal or not str(proposal).strip():
                break
            result = self.act(str(proposal))
            results.append(result)
            if result.get("concluded") or str(proposal).strip().lower() in ("quit", "exit"):
                break
        return results

    # ---- internals -------------------------------------------------------
    def _record(self, author: str, text: str, *, accepted: bool, reason: str, output: str,
                changed: Iterable[str], concluded: bool, keep_going: bool = True) -> dict:
        record = {
            "author": author,
            "proposal": text,
            "accepted": accepted,
            "reason": reason,
            "output": output,
            "changed": sorted(changed),
            "turns": self.session.turns,
            "concluded": concluded,
            "keep_going": keep_going,
        }
        self.history.append(record)
        return record


def _diff(before: dict, after: dict) -> list[str]:
    """Top-level keys whose value the engine changed. This is the adapter's *whole* claim."""
    keys = set(before) | set(after)
    return [key for key in keys if before.get(key) != after.get(key)]


def load_gate(case_path: str | Path, *, seed: int = 7,
              ratings: dict[str, int] | None = None) -> AgentGate:
    """Convenience constructor for tests and harnesses: one case, one competent sheet."""
    from rules.investigation import Investigator, load_case_graph

    graph = load_case_graph(case_path)
    investigator = Investigator(name="Agent-run investigator",
                                ratings=ratings or {"Notice": 1, "Talk": 1, "Administer": 1})
    return AgentGate(CaseSession.start(graph, investigator, seed=seed))
