"""Mesa social simulation. Proposals ONLY; no direct Evennia mutations."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SupplyProposal:
    area: str
    delta: int
    reason: str

def validate_proposal(proposal: SupplyProposal, known_areas: set[str]) -> bool:
    return proposal.area in known_areas and -2 <= proposal.delta <= 2 and len(proposal.reason) <= 160

def build_model():
    import mesa
    class SurvivorAgent(mesa.Agent):
        def __init__(self, model, area: str):
            super().__init__(model)
            self.area = area
        def step(self):
            self.model.events.append(SupplyProposal(self.area, -1, "Background consumption"))
    class HelsinkiModel(mesa.Model):
        def __init__(self, seed=42):
            super().__init__(seed=seed)
            self.events = []
            self.population = [SurvivorAgent(self, "Kurvi")]
        def step(self):
            self.events.clear()
            for agent in self.population:
                agent.step()
            return tuple(self.events)
    return HelsinkiModel()
