"""Standalone Psyche projection mechanics for the narrative RPG layer.

The model tracks consequences without deciding whether an experience was a dream,
drug state, VR construction, or genuinely non-local noetic projection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ProjectionLayer(StrEnum):
    DREAM = "dream"
    PSYCHEDELIC = "psychedelic"
    VIRTUAL = "virtual"
    NOETIC = "noetic"


class ProjectionStatus(StrEnum):
    EMBODIED = "embodied"
    PROJECTED = "projected"
    RETURNED = "returned"
    LOST = "lost"


@dataclass(frozen=True)
class ProjectionResult:
    text: str
    coherence_cost: int = 0
    anchor_cost: int = 0
    trace_gain: int = 0
    information: frozenset[str] = frozenset()


@dataclass
class ProjectionSession:
    """An inspectable, deterministic first-pass astral projection loop."""

    status: ProjectionStatus = ProjectionStatus.EMBODIED
    coherence: int = 100
    anchor: int = 100
    trace: int = 0
    distance: int = 0
    elapsed_turns: int = 0
    known_information: set[str] = field(default_factory=set)
    hypotheses: dict[ProjectionLayer, int] = field(default_factory=lambda: {
        layer: 25 for layer in ProjectionLayer
    })
    history: list[str] = field(default_factory=list)

    def enter(self, *, preparation: int = 0, anchor_support: int = 0) -> ProjectionResult:
        if self.status is not ProjectionStatus.EMBODIED:
            raise ValueError("Projection can only begin from an embodied state")
        self.status = ProjectionStatus.PROJECTED
        self.coherence = min(100, 70 + preparation)
        self.anchor = min(100, 70 + anchor_support)
        result = ProjectionResult(
            "Psychen näkökulma irtoaa ruumiillisesta ankkurista. Kerros ei tunnista itseään.",
            information=frozenset({"projection_layer_unresolved"}),
        )
        return self._apply("enter", result)

    def observe(self, clue: str, evidence: dict[ProjectionLayer, int] | None = None) -> ProjectionResult:
        self._require_projected()
        if evidence:
            for layer, change in evidence.items():
                self.hypotheses[layer] = max(0, self.hypotheses[layer] + change)
            self._normalize_hypotheses()
        return self._apply("observe", ProjectionResult(
            "Havainto tallentuu, mutta sen ontologinen lähde jää avoimeksi.",
            coherence_cost=2,
            trace_gain=1,
            information=frozenset({clue}),
        ))

    def traverse(self, steps: int = 1) -> ProjectionResult:
        self._require_projected()
        if steps < 1:
            raise ValueError("steps must be positive")
        self.distance += steps
        return self._apply("traverse", ProjectionResult(
            "Psyche siirtyy ilman tavallista etäisyyttä; ympäristö menettää fyysiset yksityiskohdat.",
            coherence_cost=2 * steps,
            anchor_cost=steps,
            trace_gain=steps,
        ))

    def resonate(self, target: str, intensity: int = 1) -> ProjectionResult:
        self._require_projected()
        if intensity not in range(1, 4):
            raise ValueError("intensity must be 1, 2, or 3")
        return self._apply("resonate", ProjectionResult(
            "Kaksi Psycheä jakaa sisältöä. Kumpikaan ei voi todistaa, siirtyikö muisto vai syntyikö se yhdessä.",
            coherence_cost=4 * intensity,
            anchor_cost=2 * intensity,
            trace_gain=3 * intensity,
            information=frozenset({f"resonance:{target}"}),
        ))

    def manifest(self, witness: str) -> ProjectionResult:
        self._require_projected()
        return self._apply("manifest", ProjectionResult(
            "Todistaja havaitsee läsnäolon, mutta tallennusjärjestelmä ei saa siitä yksiselitteistä todistetta.",
            coherence_cost=6,
            anchor_cost=3,
            trace_gain=5,
            information=frozenset({f"manifested_to:{witness}"}),
        ))

    def return_to_body(self, *, assistance: int = 0) -> ProjectionResult:
        self._require_projected()
        threshold = self.distance * 3 + max(0, 30 - self.anchor)
        if self.coherence + assistance < threshold:
            self.status = ProjectionStatus.LOST
            return self._apply("return_failed", ProjectionResult(
                "Paluureitti hajoaa kilpaileviksi ruumis-, podi- ja muistokuviksi.",
                information=frozenset({"return_anchor_lost"}),
            ))
        self.status = ProjectionStatus.RETURNED
        return self._apply("return", ProjectionResult(
            "Psyche kiinnittyy ruumiiseen. Kokemus säilyy, mutta kerrosten provenienssi ei.",
            information=frozenset({"returned_with_ambiguous_provenance"}),
        ))

    def inspect_state(self) -> dict[str, object]:
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
            raise ValueError("Action requires an active projection")

    def _normalize_hypotheses(self) -> None:
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
