"""Optional local crisis and NHI contact trackers for NoöPunk (#594).

These are original, deterministic scenario-state models. They do not replace
the established network, PSI, combat, or faction-turn subsystems.
"""
from dataclasses import dataclass


@dataclass
class Crisis:
    """Localized supply, solidarity and exposure pressures, not a global Fall."""
    scarcity: int = 0
    trust: int = 3
    exposure: int = 0

    def event(self, *, supply_loss: int = 0, solidarity: int = 0,
              exposure_gain: int = 0) -> None:
        self.scarcity = max(0, self.scarcity + supply_loss)
        self.trust = max(0, min(6, self.trust + solidarity))
        self.exposure = max(0, self.exposure + exposure_gain)


@dataclass
class Contact:
    """Reciprocity and autonomy remain separate in NHI diplomacy."""
    reciprocity: int = 0
    autonomy: int = 3

    def negotiate(self, *, exchange: int, pressure: int) -> None:
        self.reciprocity = max(-6, min(6, self.reciprocity + exchange))
        self.autonomy = max(0, min(6, self.autonomy - pressure))
