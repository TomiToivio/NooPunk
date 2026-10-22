"""Consent-aware, ontology-neutral psychosurgery state changes."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Character, GraphEffect


@dataclass
class PsychosurgerySession:
    patient: Character
    operator: str
    consent: bool
    revealed_aspects: set[str] = field(default_factory=set)
    log: list[str] = field(default_factory=list)

    def reveal_aspect(self, aspect: str) -> None:
        self.revealed_aspects.add(aspect)
        self.log.append(f"revealed:{aspect}")

    def integrate_aspect(self, aspect: str) -> None:
        if not self.consent:
            raise PermissionError("Aspect changes require patient consent")
        self.patient.aspects.add(aspect)
        self.log.append(f"integrated:{aspect}")

    def add_condition(self, condition: str) -> None:
        self.patient.conditions.add(condition)
        self.log.append(f"condition:{condition}")

    def heal_consequence(self, consequence: str) -> bool:
        if not self.consent:
            raise PermissionError("Consequence treatment requires patient consent")
        if consequence not in self.patient.consequences:
            return False
        self.patient.consequences.remove(consequence)
        self.log.append(f"healed:{consequence}")
        return True

    def resonate(self, other: str, strength: int = 1) -> GraphEffect:
        self.log.append(f"resonance:{other}:{strength}")
        return GraphEffect("noetic", "adjust_edge", self.patient.id, other, "resonance", strength)
