"""A minimal faction-project clock for background campaign motion."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FactionProject:
    name: str
    goal: int = 4
    progress: int = 0

    @property
    def complete(self) -> bool:
        return self.progress >= self.goal


@dataclass
class Faction:
    id: str
    name: str
    goals: list[str]
    influence: int = 0
    resources: int = 0
    description: str = ""
    canon: str = "authoritative"
    assets: set[str] = field(default_factory=set)
    relationships: dict[str, int] = field(default_factory=dict)
    projects: list[FactionProject] = field(default_factory=list)

    def advance_project(self, project: str, amount: int = 1) -> FactionProject:
        selected = next((item for item in self.projects if item.name == project), None)
        if selected is None:
            raise KeyError(f"Unknown faction project: {project}")
        selected.progress = max(0, min(selected.goal, selected.progress + amount))
        return selected

    def discourse(self) -> str:
        """Render this faction into prose for the Laclau/Palonen populism lens.

        Produces a short manifesto-style text from the faction's goals,
        relationships, and active projects — the input ``analyze_faction`` feeds
        to ``analyze_discourse``. Pure-Python, no dependencies.
        """
        lines = [f"Faction: {self.name}", f"Influence: {self.influence}",
                 f"Resources: {self.resources}"]
        if self.goals:
            lines.append("Goals: " + "; ".join(self.goals))
        if self.relationships:
            rel = ", ".join(f"{target} ({'+' if delta >= 0 else ''}{delta})"
                             for target, delta in self.relationships.items())
            lines.append(f"Relationships: {rel}")
        if self.projects:
            proj = ", ".join(f"{p.name} ({p.progress}/{p.goal})" for p in self.projects)
            lines.append(f"Projects: {proj}")
        if self.assets:
            lines.append("Assets: " + ", ".join(sorted(self.assets)))
        return "\n".join(lines)


def analyze_faction(faction: "Faction", **kwargs):
    """Analyze a faction's discourse via the Laclau/Palonen populism lens.

    Lazily imports ``src.political.populism_analysis`` (which is import-gated)
    so the core ``src.rpg`` package stays dependency-free. Raises the lens's
    ``RuntimeError`` if ``ollama``/``pydantic`` are not installed.
    """
    from src.political.populism_analysis import analyze_discourse

    return analyze_discourse(faction.discourse(), **kwargs)


def analyze_faction_v3(faction: "Faction", **kwargs):
    """Analyze a faction's discourse via the LaclauGPT v3 Noetic Hegemony engine.

    A superset of :func:`analyze_faction`: where the populism lens returns a
    ``FormulaOfPopulism`` (Us vs Frontier), the v3 engine returns a full
    ``LaclauGPTResult`` — the 13-section analysis, the 10-card hegemonic Tarot
    spread, archetypal attractors, the six graph representations, and the
    Oracle sentence. Lazily imports ``src.political.laclaugpt_v3`` (import-gated)
    so ``src.rpg`` stays dependency-free. Raises the engine's ``RuntimeError``
    if ``ollama``/``pydantic`` are not installed. ``client=`` is accepted for
    fake-based tests (no live Ollama required).
    """
    from src.political.laclaugpt_v3 import LaclauGPT

    # ``client`` and ``model`` are kwargs for LaclauGPT.analyze, not __init__;
    # construct a default agent and forward all kwargs to analyze().
    agent = LaclauGPT()
    return agent.analyze(faction.discourse(), **kwargs)


def _faction_from_dict(data: dict[str, Any]) -> Faction:
    projects = [FactionProject(name=p["name"], goal=p.get("goal", 4),
                               progress=p.get("progress", 0))
               for p in data.get("projects", [])]
    return Faction(
        id=data["id"],
        name=data["name"],
        goals=list(data.get("goals", [])),
        influence=int(data.get("influence", 0)),
        resources=int(data.get("resources", 0)),
        description=str(data.get("description", "")),
        canon=str(data.get("canon", "authoritative")),
        assets=set(data.get("assets", [])),
        relationships={k: int(v) for k, v in data.get("relationships", {}).items()},
        projects=projects,
    )


def load_factions(path: str | Path) -> list[Faction]:
    """Load factions from a JSON file.

    Accepts either a top-level list of faction objects or an object with a
    ``factions`` list (the layout used by ``data/rpg/factions/*.json``).
    Duplicate faction ids are rejected, mirroring the scenario loader's
    uniqueness checks.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        entries = data.get("factions", [])
    elif isinstance(data, list):
        entries = data
    else:
        raise ValueError(f"Expected a JSON list or object with 'factions', got {type(data).__name__}")
    factions: list[Faction] = []
    seen: set[str] = set()
    for item in entries:
        faction = _faction_from_dict(item)
        if faction.id in seen:
            raise ValueError(f"Duplicate faction id: {faction.id}")
        seen.add(faction.id)
        factions.append(faction)
    return factions
