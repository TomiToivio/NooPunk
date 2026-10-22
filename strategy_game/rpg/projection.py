"""Psyche projection: an inspectable, deterministic model of a nonlocal experience.

Ported from the *Ubiquitous Maniacs* corpus (``archive/ubiquitous-maniacs-2026-10/src/rpg/
astral.py``) onto this repository's engine, so that the corpus's material and the live RPG are
**one** system rather than two parallel ones. The port is mechanical: the same state machine, the
same costs, the same thresholds. What changed is the language (English, per the repository's
convention), the module's home, and the vocabulary it borrows.

What it models
--------------

A character goes somewhere the body does not follow. The model tracks **what that costs** and
**what it leaves behind**, and it deliberately does **not** decide what the experience *was*.
Dream, psychedelic state, VR construction, and genuinely non-local noetic projection are four
competing hypotheses, held as weights, and the fiction may never settle which one is true —
which is exactly the corpus's point, and exactly the register ``rulebook/parts/09_characters_and
_beings.md`` asks for.

Why this is a scene model and not a new mechanic
------------------------------------------------

It introduces **no dice, no skill, no outcome rung and no resolution rule**. It is a state
machine over a scene: a GM or a session moves it, and the existing Fate resolver
(:mod:`strategy_game.rpg.fate`) still decides every uncertain action inside it. A projection
does not roll; it *charges*. Coherence and anchor are the two resources the experience spends,
and running either to zero ends it.

This also keeps the layer boundary: it sits in ``strategy_game/rpg/`` because the RPG layer is
the foundation and the strategy layer consumes it, never the reverse.

What it is not
--------------

Not a claim about ontology, not a power, not a disease, not a stack effect, and not a
replacement for the existing PSI seam (:mod:`strategy_game.psi_operations`). Where that seam
declares a *mission*, this models a *state of consciousness* inside a scene.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

__all__ = [
    "ProjectionLayer",
    "ProjectionResult",
    "ProjectionSession",
    "ProjectionStatus",
]


class ProjectionLayer(StrEnum):
    """The four competing accounts of what a projection experience is.

    The model never resolves them. A session may leave every one of them standing, and the
    fiction may treat the ambiguity as the point.
    """

    DREAM = "dream"
    PSYCHEDELIC = "psychedelic"
    VIRTUAL = "virtual"
    NOETIC = "noetic"


class ProjectionStatus(StrEnum):
    """Where the character is relative to the body."""

    EMBODIED = "embodied"
    PROJECTED = "projected"
    RETURNED = "returned"
    LOST = "lost"


@dataclass(frozen=True)
class ProjectionResult:
    """What one move of the projection did.

    Every field is a fact about the *state*, not a story: the costs are what the session pays,
    the information is what is now known, and the text is a neutral description the fiction can
    be written on top of.
    """

    text: str
    coherence_cost: int = 0
    anchor_cost: int = 0
    trace_gain: int = 0
    information: frozenset[str] = frozenset()


@dataclass
class ProjectionSession:
    """An inspectable, deterministic projection loop.

    Nothing here consults a random number: the same sequence of calls always produces the same
    state, so a projection can be replayed, asserted on, and saved.
    """

    status: ProjectionStatus = ProjectionStatus.EMBODIED
    coherence: int = 100
    anchor: int = 100
    trace: int = 0
    distance: int = 0
    elapsed_turns: int = 0
    known_information: set[str] = field(default_factory=set)
    hypotheses: dict[ProjectionLayer, int] = field(
        default_factory=lambda: {layer: 25 for layer in ProjectionLayer}
    )
    history: list[str] = field(default_factory=list)

    def enter(self, *, preparation: int = 0, anchor_support: int = 0) -> ProjectionResult:
        """Leave the body.

        ``preparation`` and ``anchor_support`` are the two ways a character can arrive better
        equipped than they were: one is what they did beforehand, the other is what someone or
        something else did for them. Neither is a skill and neither rolls.
        """
        if self.status is not ProjectionStatus.EMBODIED:
            raise ValueError("a projection can only begin from an embodied state")
        self.status = ProjectionStatus.PROJECTED
        self.coherence = min(100, 70 + preparation)
        self.anchor = min(100, 70 + anchor_support)
        return self._apply(
            "enter",
            ProjectionResult(
                "The psyche's viewpoint separates from the bodily anchor. The layer does not "
                "recognise itself.",
                information=frozenset({"projection_layer_unresolved"}),
            ),
        )

    def observe(
        self, clue: str, evidence: dict[ProjectionLayer, int] | None = None
    ) -> ProjectionResult:
        """Notice something, and optionally weight the hypotheses.

        Observing always costs coherence and leaves a trace. The hypothesis weights are the
        *only* place where the four accounts compete, and a session is under no obligation to
        move them at all.
        """
        self._require_projected()
        if evidence:
            for layer, change in evidence.items():
                self.hypotheses[layer] = max(0, self.hypotheses[layer] + change)
            self._normalize_hypotheses()
        return self._apply(
            "observe",
            ProjectionResult(
                "The observation is recorded, but its ontological source stays open.",
                coherence_cost=2,
                trace_gain=1,
                information=frozenset({clue}),
            ),
        )

    def traverse(self, steps: int = 1) -> ProjectionResult:
        """Go further out."""
        self._require_projected()
        if steps < 1:
            raise ValueError("steps must be positive")
        self.distance += steps
        return self._apply(
            "traverse",
            ProjectionResult(
                "The psyche moves without ordinary distance; the surroundings lose their physical "
                "detail.",
                coherence_cost=2 * steps,
                anchor_cost=steps,
                trace_gain=steps,
            ),
        )

    def resonate(self, target: str, intensity: int = 1) -> ProjectionResult:
        """Make contact with another psyche.

        Neither party can afterwards prove whether a memory was transferred or was made jointly.
        That ambiguity is the cost, and it is deliberate.
        """
        self._require_projected()
        if intensity not in range(1, 4):
            raise ValueError("intensity must be 1, 2 or 3")
        return self._apply(
            "resonate",
            ProjectionResult(
                "Two psyches share content. Neither can prove whether a memory was carried "
                "across or was made between them.",
                coherence_cost=4 * intensity,
                anchor_cost=2 * intensity,
                trace_gain=3 * intensity,
                information=frozenset({f"resonance:{target}"}),
            ),
        )

    def manifest(self, witness: str) -> ProjectionResult:
        """Be perceived from outside.

        The witness sees a presence. The recording equipment does not get an unambiguous
        record, and the difference between the two is the whole problem.
        """
        self._require_projected()
        return self._apply(
            "manifest",
            ProjectionResult(
                "A witness perceives a presence, but the recording system cannot turn it into "
                "unambiguous evidence.",
                coherence_cost=6,
                anchor_cost=3,
                trace_gain=5,
                information=frozenset({f"manifested_to:{witness}"}),
            ),
        )

    def return_to_body(self, *, assistance: int = 0) -> ProjectionResult:
        """Try to come back.

        The return threshold grows with the distance travelled and with how little anchor is
        left, so a long projection with a thin anchor can simply fail. A failure is not death:
        the session ends in :attr:`ProjectionStatus.LOST`, which is a state the fiction can
        continue from.
        """
        self._require_projected()
        threshold = self.distance * 3 + max(0, 30 - self.anchor)
        if self.coherence + assistance < threshold:
            self.status = ProjectionStatus.LOST
            return self._apply(
                "return_failed",
                ProjectionResult(
                    "The way back comes apart into rival body, pod and memory images.",
                    information=frozenset({"return_anchor_lost"}),
                ),
            )
        self.status = ProjectionStatus.RETURNED
        return self._apply(
            "return",
            ProjectionResult(
                "The psyche reattaches to the body. The experience survives; its provenance "
                "does not.",
                information=frozenset({"returned_with_ambiguous_provenance"}),
            ),
        )

    def inspect_state(self) -> dict[str, object]:
        """The whole state, as plain data. Used by a report, a save file or a test."""
        return {
            "status": self.status.value,
            "coherence": self.coherence,
            "anchor": self.anchor,
            "trace": self.trace,
            "distance": self.distance,
            "elapsed_turns": self.elapsed_turns,
            "hypotheses": {layer.value: value for layer, value in self.hypotheses.items()},
            "known_information": sorted(self.known_information),
            "history": list(self.history),
        }

    def _apply(self, action: str, result: ProjectionResult) -> ProjectionResult:
        self.coherence = max(0, self.coherence - result.coherence_cost)
        self.anchor = max(0, self.anchor - result.anchor_cost)
        self.trace += result.trace_gain
        self.known_information.update(result.information)
        self.history.append(action)
        if self.status is ProjectionStatus.PROJECTED:
            self.elapsed_turns += 1
            if self.coherence == 0 or self.anchor == 0:
                self.status = ProjectionStatus.LOST
                self.known_information.add("projection_integrity_lost")
        return result

    def _require_projected(self) -> None:
        if self.status is not ProjectionStatus.PROJECTED:
            raise ValueError("this action requires an active projection")

    def _normalize_hypotheses(self) -> None:
        """Keep the four weights summing to 100, largest remainder first."""
        total = sum(self.hypotheses.values())
        if total <= 0:
            self.hypotheses = {layer: 25 for layer in ProjectionLayer}
            return
        raw = {layer: value * 100 / total for layer, value in self.hypotheses.items()}
        normalized = {layer: int(value) for layer, value in raw.items()}
        remainder = 100 - sum(normalized.values())
        ranking = sorted(ProjectionLayer, key=lambda layer: raw[layer] - normalized[layer], reverse=True)
        for layer in ranking[:remainder]:
            normalized[layer] += 1
        self.hypotheses = normalized
