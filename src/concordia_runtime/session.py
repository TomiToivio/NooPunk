"""Concordia session configuration without NoöPunk gameplay rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .participants import LLMAgentSpec


@dataclass(frozen=True, slots=True)
class SessionSpec:
    """Minimal, deliberately non-canonical session description."""

    gm_name: str = "placeholder_gm"
    llm_agents: tuple[LLMAgentSpec, ...] = field(default_factory=tuple)
    premise: str = (
        "placeholder_premise: no canonical world state has been specified."
    )
    max_steps: int = 1

    def __post_init__(self) -> None:
        if not self.gm_name.strip():
            raise ValueError("GM name must not be empty.")
        if self.max_steps < 1:
            raise ValueError("max_steps must be at least 1.")


def build_concordia_config(spec: SessionSpec) -> Any:
    """Translate the neutral NoöPunk session spec into current Concordia prefabs.

    This builds configuration only. It does not run an LLM, define RPG rules,
    create character statistics, or generate canonical world content.
    """
    try:
        from concordia.prefabs import entity as entity_prefabs
        from concordia.prefabs import game_master as gm_prefabs
        from concordia.typing import prefab as prefab_lib
    except ImportError as exc:
        raise RuntimeError(
            "Concordia is not installed. "
            "Install dependencies from requirements-concordia.txt."
        ) from exc

    prefabs = {
        "minimal__Entity": entity_prefabs.minimal.Entity,
        "generic__GameMaster": gm_prefabs.generic.GameMaster,
    }

    instances = [
        prefab_lib.InstanceConfig(
            prefab="minimal__Entity",
            role=prefab_lib.Role.ENTITY,
            params={"name": agent.name},
        )
        for agent in spec.llm_agents
    ]
    instances.append(
        prefab_lib.InstanceConfig(
            prefab="generic__GameMaster",
            role=prefab_lib.Role.GAME_MASTER,
            params={"name": spec.gm_name},
        )
    )

    return prefab_lib.Config(
        default_premise=spec.premise,
        default_max_steps=spec.max_steps,
        prefabs=prefabs,
        instances=instances,
    )


def build_simulation(
    *,
    spec: SessionSpec,
    model: Any,
    embedder: Any,
) -> Any:
    """Build Concordia's generic Simulation using injected runtime services.

    The embedder is intentionally injected rather than silently choosing a
    semantic model for the project.
    """
    if embedder is None:
        raise ValueError("A text embedder must be supplied explicitly.")

    try:
        from concordia.prefabs.simulation import generic as simulation
    except ImportError as exc:
        raise RuntimeError(
            "Concordia is not installed. "
            "Install dependencies from requirements-concordia.txt."
        ) from exc

    return simulation.Simulation(
        config=build_concordia_config(spec),
        model=model,
        embedder=embedder,
    )
