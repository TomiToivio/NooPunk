"""RPG-yhteensopiva nelikerroksinen kyberneettis–psykotroninen hacking-moottori.

Kerrokset eivät ole erillisiä tasoja — ne läpitunkeutuvat toisiinsa:

  kyberneettinen  — tietokoneet, päätteet, implantit, sensorit, UKK-järjestelmät
  sosiaalinen     — identiteetit, valtasuhteet, luvat, suostumukset, byrokratia
  biologinen      — hermosto, aineenvaihdunta, UFAB 80MG, unisyklit, keho
  psyykkinen      — CAN-solmut, noetoottiset signaalit, arkkityypit, muistot,
                    unet, astraalitila, NHI-rajapinnat

Cross-layer-kaaret (edge_type) ovat moottorin ydin:
  psychotronic_feedback   psyykkinen → kyberneettinen (Ragnarökin signaali vuotaa tietokoneisiin)
  implant_brain_interface biologinen → kyberneettinen (UFAB 80MG vahvistaa implantin resonanssia)
  embodied_dream          biologinen → psyykkinen (unisykli porttina unimaailmaan)
  authority               sosiaalinen → kyberneettinen (Pilgrimin valta avaa järjestelmän)
  trusted_intermediary    sosiaalinen → sosiaalinen (Tanakan luottamus välittää suostumuksen)

Psykotroninen resonanssi (resolve_cross_layer) on erityinen toiminto:
pelaaja voi siirtyä kerroksesta toiseen vain, jos kaari tukee siirtymää.
Tämä tekee neljästä kerroksesta yhden ontologisesti epämääräisen tilan,
ei neljää erillistä minipeliä.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Any

import networkx as nx

from src.rpg import ActionResult, ActionType, Character, GraphEffect, RPGState, resolve_action


class OperationalLayer(StrEnum):
    CYBERNETIC = "cybernetic"
    PSYCHIC = "psychic"
    SOCIAL = "social"
    BIOLOGICAL = "biological"


class AccessLevel(IntEnum):
    OBSERVED = 0
    CONTACT = 1
    ACCESS = 2
    PRIVILEGED = 3
    CONTROL = 4


class HackingAction(StrEnum):
    OBSERVE = "observe"
    CREATE_ACCESS = "create_access"
    EXPLOIT = "exploit"
    CREATE_ADVANTAGE = "create_advantage"
    DEFEND = "defend"
    OVERCOME = "overcome"
    ATTACK = "attack"
    RETREAT = "retreat"
    RESONATE = "resonate"


# Cross-layer-kaaret, jotka yhdistävät eri operatiiviset kerrokset.
# Näitä pitkin pelaaja voi siirtyä kerroksesta toiseen (psykotroninen resonanssi).
# Muut kaaret ovat saman kerroksen sisäisiä tai eivät tue resonanssia.
CROSS_LAYER_EDGES: frozenset[str] = frozenset({
    "psychotronic_feedback",
    "implant_brain_interface",
    "embodied_dream",
    "unauthorized_resonance",
    "counter_resonance",
})


@dataclass(frozen=True)
class HackingCheck:
    attribute: str
    skill: str | None
    difficulty: int


@dataclass(frozen=True)
class HackingTool:
    id: str
    label: str
    layers: frozenset[OperationalLayer]
    actions: frozenset[HackingAction]
    bonus: int = 0
    permission: str | None = None


@dataclass(frozen=True)
class LayeredHackingResult:
    action: HackingAction
    success: bool
    summary: str
    source: str | None = None
    target: str | None = None
    check: ActionResult | None = None
    revealed_nodes: tuple[str, ...] = ()
    access_level: AccessLevel | None = None
    alert_delta: int = 0
    trace_delta: int = 0
    stress_delta: int = 0
    created_aspect: str | None = None
    objective_updates: tuple[str, ...] = ()

    @property
    def costly_success(self) -> bool:
        return self.check is not None and self.check.requires_cost


@dataclass
class HackingTransfer:
    """Serialisoitavat tehosteet jotka palautetaan RPG-tilaan omistamatta sitä."""

    information: set[str] = field(default_factory=set)
    conditions: set[str] = field(default_factory=set)
    consequences: list[str] = field(default_factory=list)
    relationships: dict[str, int] = field(default_factory=dict)
    flags: dict[str, Any] = field(default_factory=dict)
    graph_effects: list[GraphEffect] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "information": sorted(self.information),
            "conditions": sorted(self.conditions),
            "consequences": list(self.consequences),
            "relationships": dict(self.relationships),
            "flags": copy.deepcopy(self.flags),
            "graph_effects": [vars(effect) for effect in self.graph_effects],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HackingTransfer":
        if not isinstance(data, dict):
            raise TypeError("Hacking transfer must be an object")
        return cls(
            information={str(value) for value in data.get("information", [])},
            conditions={str(value) for value in data.get("conditions", [])},
            consequences=[str(value) for value in data.get("consequences", [])],
            relationships={str(key): int(value) for key, value in data.get("relationships", {}).items()},
            flags=copy.deepcopy(data.get("flags", {})),
            graph_effects=[GraphEffect(**raw) for raw in data.get("graph_effects", [])],
        )

    def apply(self, state: RPGState, character: Character) -> None:
        state.known_information.update(self.information)
        state.conditions.update(self.conditions)
        state.consequences.extend(item for item in self.consequences if item not in state.consequences)
        character.conditions.update(self.conditions)
        character.consequences.extend(item for item in self.consequences if item not in character.consequences)
        state.campaign_flags.update(self.flags)
        for target, delta in self.relationships.items():
            old = state.relationships.get(target, 0)
            new = max(-100, min(100, old + delta))
            state.relationships[target] = new
            state.graph_effects.append(
                GraphEffect("social", "adjust_edge", character.id, target, "relationship", new - old)
            )
        state.graph_effects.extend(self.graph_effects)


_DEFAULT_CHECKS: dict[OperationalLayer, dict[HackingAction, HackingCheck]] = {
    OperationalLayer.CYBERNETIC: {
        HackingAction.OBSERVE: HackingCheck("Awareness", "Investigate", 3),
        HackingAction.CREATE_ACCESS: HackingCheck("Cybernetics", "Infosec", 4),
        HackingAction.EXPLOIT: HackingCheck("Cybernetics", "Infosec", 5),
        HackingAction.CREATE_ADVANTAGE: HackingCheck("Intelligence", "Program", 4),
        HackingAction.DEFEND: HackingCheck("Cybernetics", "Infosec", 4),
        HackingAction.OVERCOME: HackingCheck("Cybernetics", "Hardware", 4),
        HackingAction.ATTACK: HackingCheck("Cybernetics", "Infosec", 5),
        HackingAction.RESONATE: HackingCheck("Cybernetics", "Infosec", 5),
    },
    OperationalLayer.PSYCHIC: {
        HackingAction.OBSERVE: HackingCheck("Awareness", "Investigate", 4),
        HackingAction.CREATE_ACCESS: HackingCheck("Charisma", "Rapport", 4),
        HackingAction.EXPLOIT: HackingCheck("Willpower", "Will", 6),
        HackingAction.CREATE_ADVANTAGE: HackingCheck("Charisma", "Rapport", 4),
        HackingAction.DEFEND: HackingCheck("Willpower", "Will", 4),
        HackingAction.OVERCOME: HackingCheck("Willpower", "Will", 5),
        HackingAction.ATTACK: HackingCheck("Willpower", "Will", 6),
        HackingAction.RESONATE: HackingCheck("Willpower", "Kinesics", 5),
    },
    OperationalLayer.SOCIAL: {
        HackingAction.OBSERVE: HackingCheck("Awareness", "Kinesics", 3),
        HackingAction.CREATE_ACCESS: HackingCheck("Charisma", "Rapport", 4),
        HackingAction.EXPLOIT: HackingCheck("Charisma", "Deceive", 5),
        HackingAction.CREATE_ADVANTAGE: HackingCheck("Charisma", "Rapport", 4),
        HackingAction.DEFEND: HackingCheck("Charisma", "Kinesics", 4),
        HackingAction.OVERCOME: HackingCheck("Intelligence", "Investigate", 4),
        HackingAction.ATTACK: HackingCheck("Charisma", "Provoke", 5),
        HackingAction.RESONATE: HackingCheck("Charisma", "Kinesics", 5),
    },
    OperationalLayer.BIOLOGICAL: {
        HackingAction.OBSERVE: HackingCheck("Awareness", "Medicine", 3),
        HackingAction.CREATE_ACCESS: HackingCheck("Intelligence", "Medicine", 4),
        HackingAction.EXPLOIT: HackingCheck("Intelligence", "Medicine", 5),
        HackingAction.CREATE_ADVANTAGE: HackingCheck("Intelligence", "Medicine", 4),
        HackingAction.DEFEND: HackingCheck("Body", "Somatics", 4),
        HackingAction.OVERCOME: HackingCheck("Intelligence", "Medicine", 4),
        HackingAction.ATTACK: HackingCheck("Intelligence", "Medicine", 6),
        HackingAction.RESONATE: HackingCheck("Intelligence", "Medicine", 5),
    },
}


_RPG_ACTIONS = {
    HackingAction.OBSERVE: ActionType.OVERCOME,
    HackingAction.CREATE_ACCESS: ActionType.OVERCOME,
    HackingAction.EXPLOIT: ActionType.OVERCOME,
    HackingAction.CREATE_ADVANTAGE: ActionType.CREATE_ADVANTAGE,
    HackingAction.DEFEND: ActionType.DEFEND,
    HackingAction.OVERCOME: ActionType.OVERCOME,
    HackingAction.ATTACK: ActionType.ATTACK,
    HackingAction.RESONATE: ActionType.OVERCOME,
}


class LayeredHackingSession:
    """Dataohjattu hacking-skeeni joka ratkaistaan RPG-action-moottorilla."""

    def __init__(self, actor: Character, graph: nx.Graph, metadata: dict[str, Any]):
        self.actor = actor
        self.graph = graph
        self.metadata = metadata
        self.objective = str(metadata.get("objective", "Tutki kohdetta"))
        self.known_nodes = {node for node, attrs in graph.nodes(data=True) if not attrs.get("hidden", False)}
        self.discovered_edges: set[tuple[str, str]] = set()
        self.access = {node: AccessLevel.OBSERVED for node in self.known_nodes}
        for node, attrs in graph.nodes(data=True):
            if attrs.get("entry", False):
                self.access[node] = AccessLevel.CONTACT
        self.current_node = str(metadata["entry_node"])
        self.alert = 0
        self.trace = 0
        self.feedback = 0
        self.instability = 0
        self.system_stress = 0
        self.aspects: set[str] = set()
        self.completed_objectives: set[str] = set()
        self.exploited_nodes: set[str] = set()
        self.status = "active"
        self.history: list[dict[str, Any]] = []
        self.transfer = HackingTransfer()
        self.tools = {
            str(raw["id"]): HackingTool(
                id=str(raw["id"]),
                label=str(raw.get("label", raw["id"])),
                layers=frozenset(OperationalLayer(value) for value in raw.get("layers", [])),
                actions=frozenset(HackingAction(value) for value in raw.get("actions", [])),
                bonus=max(0, min(2, int(raw.get("bonus", 0)))),
                permission=raw.get("permission"),
            )
            for raw in metadata.get("tools", [])
        }

    @classmethod
    def from_dict(cls, actor: Character, data: dict[str, Any]) -> "LayeredHackingSession":
        graph = nx.Graph(domain="cybernetic_psychotronic_hacking")
        seen: set[str] = set()
        for raw in data.get("nodes", []):
            record = copy.deepcopy(raw)
            node_id = str(record.pop("id"))
            if node_id in seen:
                raise ValueError(f"Duplicate hacking node: {node_id}")
            seen.add(node_id)
            try:
                record["layer"] = OperationalLayer(record["layer"]).value
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid layer for hacking node {node_id}") from exc
            record.setdefault("label", node_id)
            record.setdefault("description", "")
            record.setdefault("defense", 4)
            record.setdefault("hidden", False)
            record.setdefault("vulnerabilities", [])
            record.setdefault("checks", {})
            graph.add_node(node_id, **record)
        seen_edges: set[frozenset[str]] = set()
        for raw in data.get("edges", []):
            record = copy.deepcopy(raw)
            source, target = str(record.pop("source")), str(record.pop("target"))
            if source not in graph or target not in graph:
                raise ValueError(f"Unknown hacking edge endpoint: {source}, {target}")
            edge_id = frozenset((source, target))
            if edge_id in seen_edges:
                raise ValueError(f"Duplicate hacking edge: {source}, {target}")
            seen_edges.add(edge_id)
            record.setdefault("edge_type", "connection")
            record.setdefault("strength", 1)
            record.setdefault("hidden", False)
            record.setdefault("active", True)
            graph.add_edge(source, target, **record)
        metadata = {key: copy.deepcopy(value) for key, value in data.items() if key not in {"nodes", "edges"}}
        entry = metadata.get("entry_node")
        if entry not in graph:
            raise ValueError(f"Unknown hacking entry node: {entry}")
        if graph.nodes[entry].get("hidden", False):
            raise ValueError(f"Hacking entry node must be visible: {entry}")
        tool_ids: set[str] = set()
        for raw in metadata.get("tools", []):
            tool_id = str(raw.get("id", ""))
            if not tool_id:
                raise ValueError("Hacking tool requires a non-empty id")
            if tool_id in tool_ids:
                raise ValueError(f"Duplicate hacking tool: {tool_id}")
            tool_ids.add(tool_id)
        return cls(actor, graph, metadata)

    @classmethod
    def from_json(cls, actor: Character, path: str | Path) -> "LayeredHackingSession":
        with Path(path).open(encoding="utf-8") as handle:
            return cls.from_dict(actor, json.load(handle))

    def to_save_dict(self) -> dict[str, Any]:
        """Serialize both the scenario graph and its mutable investigation state."""
        scenario = copy.deepcopy(self.metadata)
        scenario["nodes"] = [
            {"id": node, **copy.deepcopy(attrs)} for node, attrs in self.graph.nodes(data=True)
        ]
        scenario["edges"] = [
            {"source": source, "target": target, **copy.deepcopy(attrs)}
            for source, target, attrs in self.graph.edges(data=True)
        ]
        return {
            "scenario": scenario,
            "known_nodes": sorted(self.known_nodes),
            "discovered_edges": [list(edge) for edge in sorted(self.discovered_edges)],
            "access": {node: int(level) for node, level in self.access.items()},
            "current_node": self.current_node,
            "alert": self.alert,
            "trace": self.trace,
            "feedback": self.feedback,
            "instability": self.instability,
            "system_stress": self.system_stress,
            "aspects": sorted(self.aspects),
            "completed_objectives": sorted(self.completed_objectives),
            "exploited_nodes": sorted(self.exploited_nodes),
            "status": self.status,
            "history": copy.deepcopy(self.history),
            "transfer": self.transfer.to_dict(),
        }

    @classmethod
    def from_save_dict(cls, actor: Character, data: dict[str, Any]) -> "LayeredHackingSession":
        """Restore a save created by :meth:`to_save_dict`."""
        if not isinstance(data, dict) or not isinstance(data.get("scenario"), dict):
            raise TypeError("Layered hacking save must contain a scenario object")
        session = cls.from_dict(actor, data["scenario"])
        nodes = set(session.graph.nodes)
        known_nodes = {str(node) for node in data.get("known_nodes", [])}
        if not known_nodes <= nodes:
            raise ValueError("Hacking save contains unknown known nodes")
        discovered_edges: set[tuple[str, str]] = set()
        for raw in data.get("discovered_edges", []):
            if not isinstance(raw, list) or len(raw) != 2:
                raise TypeError("Discovered hacking edge must contain two node ids")
            source, target = str(raw[0]), str(raw[1])
            if not session.graph.has_edge(source, target):
                raise ValueError(f"Unknown discovered hacking edge: {source}, {target}")
            discovered_edges.add((source, target))
        raw_access = data.get("access", {})
        if not isinstance(raw_access, dict) or not set(raw_access) <= nodes:
            raise ValueError("Hacking access map contains unknown scenario nodes")
        access = {str(node): AccessLevel(int(level)) for node, level in raw_access.items()}
        if not known_nodes <= set(access):
            raise ValueError("Every known hacking node must have an access level")
        current_node = str(data.get("current_node", ""))
        if current_node not in nodes or current_node not in known_nodes:
            raise ValueError("Hacking current node must be known")
        status = str(data.get("status", "active"))
        if status not in {"active", "completed", "detected", "feedback_failure", "retreated"}:
            raise ValueError(f"Invalid hacking status: {status}")

        session.known_nodes = known_nodes
        session.discovered_edges = discovered_edges
        session.access = access
        session.current_node = current_node
        for field_name in ("alert", "trace", "feedback", "instability", "system_stress"):
            value = int(data.get(field_name, 0))
            if value < 0:
                raise ValueError(f"Hacking {field_name} cannot be negative")
            setattr(session, field_name, value)
        session.aspects = {str(value) for value in data.get("aspects", [])}
        session.completed_objectives = {str(value) for value in data.get("completed_objectives", [])}
        session.exploited_nodes = {str(value) for value in data.get("exploited_nodes", [])}
        if not session.exploited_nodes <= nodes:
            raise ValueError("Hacking save contains unknown exploited nodes")
        session.status = status
        history = data.get("history", [])
        if not isinstance(history, list) or not all(isinstance(item, dict) for item in history):
            raise TypeError("Hacking history must be a list of objects")
        session.history = copy.deepcopy(history)
        session.transfer = HackingTransfer.from_dict(data.get("transfer", {}))
        return session

    def _require_known(self, node: str) -> None:
        if node not in self.graph:
            raise KeyError(f"Unknown hacking node: {node}")
        if node not in self.known_nodes:
            raise ValueError(f"Hacking node is hidden: {node}")

    def _ensure_active(self) -> None:
        if self.is_terminal:
            raise ValueError(f"Hacking session has ended: {self.status}")

    def _layer(self, node: str) -> OperationalLayer:
        return OperationalLayer(self.graph.nodes[node]["layer"])

    def _check_for(self, node: str, action: HackingAction) -> HackingCheck:
        override = self.graph.nodes[node].get("checks", {}).get(action.value)
        default = _DEFAULT_CHECKS[self._layer(node)][action]
        if not override:
            return HackingCheck(default.attribute, default.skill, int(self.graph.nodes[node].get("defense", default.difficulty)))
        return HackingCheck(
            str(override.get("attribute", default.attribute)),
            override.get("skill", default.skill),
            int(override.get("difficulty", self.graph.nodes[node].get("defense", default.difficulty))),
        )

    def _resolve(
        self,
        node: str,
        action: HackingAction,
        roll: int | None,
        aspect: str | None = None,
        tool_id: str | None = None,
        invoke_aspect: str | None = None,
    ) -> ActionResult:
        check = self._check_for(node, action)
        modifier = 0
        if tool_id is not None:
            if tool_id not in self.tools:
                raise ValueError(f"Unknown hacking tool: {tool_id}")
            tool = self.tools[tool_id]
            if self._layer(node) not in tool.layers or action not in tool.actions:
                raise ValueError(f"Tool {tool.label} does not permit this action")
            modifier += tool.bonus
        if invoke_aspect is not None:
            if invoke_aspect not in self.actor.aspects and invoke_aspect not in self.aspects:
                raise ValueError(f"Aspect is not available: {invoke_aspect}")
            if self.actor.resources.get("fate_points", 0) < 1:
                raise ValueError("Invoking an aspect requires one Fate point")
            modifier += 2
        result = resolve_action(
            self.actor,
            attribute=check.attribute,
            skill=check.skill,
            difficulty=check.difficulty,
            action=_RPG_ACTIONS[action],
            roll=roll,
            situational_modifier=modifier,
            target=node,
            created_aspect=aspect,
        )
        if invoke_aspect is not None:
            self.actor.resources["fate_points"] -= 1
        return result

    def _discover_around(self, node: str) -> tuple[str, ...]:
        revealed: list[str] = []
        for neighbor in self.graph.neighbors(node):
            edge = self.graph.edges[node, neighbor]
            if not edge.get("active", True):
                continue
            self.discovered_edges.add(tuple(sorted((node, neighbor))))
            if neighbor not in self.known_nodes:
                self.known_nodes.add(neighbor)
                self.access[neighbor] = AccessLevel.OBSERVED
                revealed.append(neighbor)
        return tuple(sorted(revealed))

    def _pressure(self, result: ActionResult, layer: OperationalLayer) -> tuple[int, int, int]:
        if result.clean_success:
            return (0, 0, 0)
        if result.requires_cost:
            return (1, 1, 1 if layer is OperationalLayer.PSYCHIC else 0)
        if result.check.margin >= -4:
            return (2, 1, 1 if layer is OperationalLayer.PSYCHIC else 0)
        return (3, 2, 2 if layer is OperationalLayer.PSYCHIC else 1)

    def _record(self, result: LayeredHackingResult) -> LayeredHackingResult:
        self.history.append({
            "action": result.action.value,
            "source": result.source,
            "target": result.target,
            "success": result.success,
            "summary": result.summary,
            "tier": result.check.check.tier.value if result.check else None,
            "alert": self.alert,
            "trace": self.trace,
            "feedback": self.feedback,
        })
        self._check_terminal_state()
        return result

    def _apply_pressure(self, action_result: ActionResult, layer: OperationalLayer) -> tuple[int, int, int]:
        alert, trace, feedback = self._pressure(action_result, layer)
        self.alert = min(8, self.alert + alert)
        self.trace = min(8, self.trace + trace)
        self.feedback = min(8, self.feedback + feedback)
        if layer is OperationalLayer.PSYCHIC:
            self.instability = min(8, self.instability + feedback)
        return alert, trace, feedback

    def observe(
        self, node: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(node)
        action_result = self._resolve(node, HackingAction.OBSERVE, roll, tool_id=tool_id, invoke_aspect=invoke_aspect)
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(node))
        revealed = self._discover_around(node) if action_result.succeeded else ()
        if action_result.succeeded:
            self.current_node = node
        summary = f"Tutkit noden {self.graph.nodes[node]['label']}."
        if revealed:
            summary += f" Paljastui: {', '.join(revealed)}."
        if not action_result.succeeded:
            summary += " Vastatoimi havaitsi yrityksen."
        return self._record(LayeredHackingResult(
            HackingAction.OBSERVE, action_result.succeeded, summary, target=node,
            check=action_result, revealed_nodes=revealed, alert_delta=alert,
            trace_delta=trace, stress_delta=feedback,
        ))

    def create_access(
        self, source: str, target: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(source)
        self._require_known(target)
        if source != target and (
            not self.graph.has_edge(source, target)
            or not self.graph.edges[source, target].get("active", True)
        ):
            raise ValueError("Access requires an active fictional connection")
        if self.access.get(source, AccessLevel.OBSERVED) < AccessLevel.CONTACT:
            raise ValueError("Source node requires Contact before lateral movement")
        action_result = self._resolve(
            target, HackingAction.CREATE_ACCESS, roll,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(target))
        new_level = self.access.get(target, AccessLevel.OBSERVED)
        if action_result.succeeded:
            step = 2 if action_result.check.tier.value == "critical_success" else 1
            new_level = AccessLevel(min(AccessLevel.CONTROL, int(new_level) + step))
            self.access[target] = new_level
            self.current_node = target
            if source != target:
                self.discovered_edges.add(tuple(sorted((source, target))))
        summary = (
            f"Pääsy nodeen {self.graph.nodes[target]['label']}: {new_level.name}."
            if action_result.succeeded else
            f"Pääsy nodeen {self.graph.nodes[target]['label']} torjuttiin."
        )
        return self._record(LayeredHackingResult(
            HackingAction.CREATE_ACCESS, action_result.succeeded, summary,
            source, target, action_result, access_level=new_level,
            alert_delta=alert, trace_delta=trace, stress_delta=feedback,
        ))

    def create_advantage(
        self, node: str, aspect: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(node)
        action_result = self._resolve(
            node, HackingAction.CREATE_ADVANTAGE, roll, aspect,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(node))
        applicable = action_result.applicable_created_aspect
        if applicable:
            self.aspects.add(applicable)
        return self._record(LayeredHackingResult(
            HackingAction.CREATE_ADVANTAGE, action_result.succeeded,
            f"Etu {aspect} {'luotiin' if applicable else 'ei syntynyt'}.",
            target=node, check=action_result, created_aspect=applicable,
            alert_delta=alert, trace_delta=trace, stress_delta=feedback,
        ))

    def exploit(
        self, node: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(node)
        if self.access.get(node, AccessLevel.OBSERVED) < AccessLevel.ACCESS:
            raise ValueError("Exploit requires Access or better")
        if node in self.exploited_nodes:
            raise ValueError(f"Hacking node has already been exploited: {node}")
        action_result = self._resolve(
            node, HackingAction.EXPLOIT, roll,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(node))
        updates: list[str] = []
        if action_result.succeeded:
            self.exploited_nodes.add(node)
            effects = self.graph.nodes[node].get("effects", {})
            for objective in effects.get("objectives", []):
                self.completed_objectives.add(str(objective))
                updates.append(str(objective))
            self.transfer.information.update(map(str, effects.get("information", [])))
            self.transfer.conditions.update(map(str, effects.get("conditions", [])))
            self.transfer.consequences.extend(map(str, effects.get("consequences", [])))
            for target, delta in effects.get("relationships", {}).items():
                key = str(target)
                self.transfer.relationships[key] = self.transfer.relationships.get(key, 0) + int(delta)
            self.transfer.flags.update(effects.get("flags", {}))
            for raw in effects.get("graph_effects", []):
                self.transfer.graph_effects.append(GraphEffect(**raw))
        summary = (
            f"Hyödynsit noden {self.graph.nodes[node]['label']}."
            if action_result.succeeded else f"Noden {self.graph.nodes[node]['label']} puolustus piti."
        )
        return self._record(LayeredHackingResult(
            HackingAction.EXPLOIT, action_result.succeeded, summary,
            target=node, check=action_result, objective_updates=tuple(updates),
            alert_delta=alert, trace_delta=trace, stress_delta=feedback,
        ))

    def defend(
        self, node: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(node)
        action_result = self._resolve(
            node, HackingAction.DEFEND, roll,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(node))
        if action_result.succeeded:
            reduction = 2 if action_result.clean_success else 1
            self.alert = max(0, self.alert - reduction)
            self.trace = max(0, self.trace - reduction)
            if self._layer(node) is OperationalLayer.PSYCHIC:
                self.feedback = max(0, self.feedback - reduction)
        return self._record(LayeredHackingResult(
            HackingAction.DEFEND, action_result.succeeded,
            "Murtumisen jäljet rajattiin." if action_result.succeeded else "Vastatoimi jäi auki.",
            target=node, check=action_result, alert_delta=alert,
            trace_delta=trace, stress_delta=feedback,
        ))

    def overcome(
        self, node: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(node)
        action_result = self._resolve(
            node, HackingAction.OVERCOME, roll,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(node))
        if action_result.succeeded:
            self.graph.nodes[node]["overcome"] = True
            self._discover_around(node)
        return self._record(LayeredHackingResult(
            HackingAction.OVERCOME, action_result.succeeded,
            f"Este {self.graph.nodes[node]['label']} {'ohitettiin' if action_result.succeeded else 'jäi voimaan'}.",
            target=node, check=action_result, alert_delta=alert,
            trace_delta=trace, stress_delta=feedback,
        ))

    def attack(
        self, node: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        self._ensure_active()
        self._require_known(node)
        if self.access.get(node, AccessLevel.OBSERVED) < AccessLevel.ACCESS:
            raise ValueError("Attack requires Access or better")
        action_result = self._resolve(
            node, HackingAction.ATTACK, roll,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, self._layer(node))
        # Kallin onnistuminen muuttaa silti fiktiota. Fate-tyylinen
        # tulos paljastaa nolla marginaalin tälle tasolle, joten Attack
        # tarvitsee vähimmäisosuman.
        shifts = max(1, action_result.shifts) if action_result.succeeded else 0
        self.system_stress += shifts
        return self._record(LayeredHackingResult(
            HackingAction.ATTACK, action_result.succeeded,
            f"Kohdejärjestelmään kohdistui {shifts} stressiä.", target=node,
            check=action_result, alert_delta=alert, trace_delta=trace,
            stress_delta=feedback,
        ))

    def retreat(self) -> LayeredHackingResult:
        self._ensure_active()
        self.status = "retreated"
        if self.trace >= 4:
            self.transfer.conditions.add("europol_trace_pending")
        return self._record(LayeredHackingResult(
            HackingAction.RETREAT, True, "Irrottauduit kohteesta; jo syntyneet seuraukset säilyvät."
        ))

    def _cross_layer_neighbors(self, node: str) -> list[tuple[str, str]]:
        """Palauta cross-layer-kaaret tästä solmusta.

        Kaaren edge_type on oltava CROSS_LAYER_EDGES-joukossa. Nämä
        kaaret yhdistävät eri operatiiviset kerrokset (esim. psykotroninen
        palaute psyykkisestä kyberneettiseen, embodied dream biologisesta
        psyykkiseen). Niitä pitkin pelaaja voi resonoida itsensä toiseen
        kerrokseen — siirtyä ontologisesti epämääräiseen tilaan.
        """
        result: list[tuple[str, str]] = []
        for neighbor in self.graph.neighbors(node):
            edge = self.graph.edges[node, neighbor]
            if not edge.get("active", True):
                continue
            edge_type = str(edge.get("edge_type", ""))
            if edge_type in CROSS_LAYER_EDGES:
                result.append((neighbor, edge_type))
        return sorted(result)

    def resonate(
        self, source: str, target: str, *, roll: int | None = None,
        tool_id: str | None = None, invoke_aspect: str | None = None,
    ) -> LayeredHackingResult:
        """Psykotroninen resonanssi — siirry kerroksesta toiseen cross-layer-kaarta pitkin.

        Tämä on Noöpunkin ydintek mekaniikka: hacking ei ole neljä erillistä
        minipeliä vaan yksi ontologisesti epämääräinen tila. Pelaaja voi
        siirtyä kyberneettisestä psyykkiseen (psychotronic_feedback),
        biologisesta psyykkiseen (embodied_dream), biologisesta kyberneettiseen
        (implant_brain_interface) jne.

        Vaatimukset:
          - lähde- ja kohdesolmu ovat tunnettuja
          - niiden välillä on aktiivinen cross-layer-kaari
          - lähteellä on vähintään Contact-taso
          - kohde on eri kerroksessa kuin lähde

        Onnistuessa: kohde paljastuu ja saa Contact-tason. Pelaaja siirtyy
        sinne (current_node). Epäonnistuessa: feedback kasvaa, koska
        psykotroninen resonanssi on vaarallista — se sotkee kerroksia
        myös pelaajan omassa psyykessä.
        """
        self._ensure_active()
        self._require_known(source)
        if source == target:
            raise ValueError("Resonanssi vaatii kaksi eri solmua")
        if self.access.get(source, AccessLevel.OBSERVED) < AccessLevel.CONTACT:
            raise ValueError("Resonanssi vaatii Contact-tason lähteellä")

        # Tarkista cross-layer-kaari (ennen hidden-tarkistusta — resonanssi
        # on juuri se mekaniikka jolla piilotetut cross-layer-solmut paljastuvat)
        if not self.graph.has_edge(source, target):
            raise ValueError("Solmujen välillä ei ole kaarta")
        edge = self.graph.edges[source, target]
        if not edge.get("active", True):
            raise ValueError("Kaari ei ole aktiivinen")
        edge_type = str(edge.get("edge_type", ""))
        if edge_type not in CROSS_LAYER_EDGES:
            raise ValueError(
                f"Kaari '{edge_type}' ei tue psykotronista resonanssia. "
                f"Cross-layer-kaaret: {', '.join(sorted(CROSS_LAYER_EDGES))}"
            )

        source_layer = self._layer(source)
        target_layer = self._layer(target)
        if source_layer == target_layer:
            raise ValueError(
                f"Resonanssi vaatii eri kerrokset: {source_layer.value} → {target_layer.value} "
                "ovat samassa kerroksessa"
            )

        action_result = self._resolve(
            target, HackingAction.RESONATE, roll,
            tool_id=tool_id, invoke_aspect=invoke_aspect,
        )
        alert, trace, feedback = self._apply_pressure(action_result, target_layer)

        # Resonanssi-epäonnistuminen on erityisen vaarallista: se sotkee
        # pelaajan omia kerroksia ja kasvattaa instabilityä riippumatta
        # siitä, onko kohde psyykkinen vai ei.
        if not action_result.succeeded:
            self.instability = min(8, self.instability + 1)

        revealed: tuple[str, ...] = ()
        if action_result.succeeded:
            self.discovered_edges.add(tuple(sorted((source, target))))
            if target not in self.known_nodes:
                self.known_nodes.add(target)
                revealed = (target,)
            self.access[target] = max(self.access.get(target, AccessLevel.OBSERVED), AccessLevel.CONTACT)
            self.current_node = target
            # Resonanssi paljastaa myös kohteen naapurit — kerrokset vuotavat
            revealed += self._discover_around(target)

        layer_desc = f"{source_layer.value} → {target_layer.value}"
        if action_result.succeeded:
            summary = (
                f"Psykotroninen resonanssi: {layer_desc}. "
                f"Siirryit noden {self.graph.nodes[target]['label']} kerrokseen."
            )
            if revealed:
                summary += f" Vuoto paljasti: {', '.join(revealed)}."
        else:
            summary = (
                f"Psykotroninen resonanssi epäonnistui: {layer_desc}. "
                f"Kerrokset sotkeutuvat — instability kasvaa."
            )
        return self._record(LayeredHackingResult(
            HackingAction.RESONATE, action_result.succeeded, summary,
            source, target, action_result, revealed_nodes=revealed,
            alert_delta=alert, trace_delta=trace, stress_delta=feedback,
        ))

    def _check_terminal_state(self) -> None:
        required = set(map(str, self.metadata.get("required_objectives", [])))
        if required and required <= self.completed_objectives:
            self.status = "completed"
            self.transfer.flags["sleeping_patient_resolved"] = True
        elif self.alert >= int(self.metadata.get("alert_limit", 8)):
            self.status = "detected"
            self.transfer.conditions.add("ufab_intrusion_detected")
        elif self.feedback >= int(self.metadata.get("feedback_limit", 8)):
            self.status = "feedback_failure"
            self.transfer.consequences.append("Psyykkinen kaikuhäiriö")

    @property
    def is_terminal(self) -> bool:
        return self.status != "active"

    def snapshot(self) -> dict[str, Any]:
        visible_nodes = []
        for node in sorted(self.known_nodes):
            attrs = copy.deepcopy(self.graph.nodes[node])
            attrs.pop("effects", None)
            attrs.pop("checks", None)
            visible_nodes.append({"id": node, **attrs, "access": self.access[node].name})
        visible_edges = []
        for source, target in sorted(self.discovered_edges):
            attrs = copy.deepcopy(self.graph.edges[source, target])
            visible_edges.append({"source": source, "target": target, **attrs})
        # Cross-layer-resonanssimahdollisuudet nykyisestä solmusta
        resonance_options = []
        if self.current_node in self.known_nodes:
            for neighbor, edge_type in self._cross_layer_neighbors(self.current_node):
                neighbor_layer = self.graph.nodes[neighbor].get("layer", "?")
                resonance_options.append({
                    "target": neighbor,
                    "edge_type": edge_type,
                    "target_layer": neighbor_layer,
                    "target_known": neighbor in self.known_nodes,
                })
        return {
            "scenario": self.metadata.get("id"),
            "objective": self.objective,
            "status": self.status,
            "current_node": self.current_node,
            "current_layer": self.graph.nodes[self.current_node].get("layer"),
            "known_nodes": visible_nodes,
            "discovered_edges": visible_edges,
            "resonance_options": resonance_options,
            "aspects": sorted(self.aspects),
            "tools": [
                {
                    "id": tool.id,
                    "label": tool.label,
                    "layers": sorted(layer.value for layer in tool.layers),
                    "actions": sorted(action.value for action in tool.actions),
                    "bonus": tool.bonus,
                    "permission": tool.permission,
                }
                for tool in self.tools.values()
            ],
            "completed_objectives": sorted(self.completed_objectives),
            "exploited_nodes": sorted(self.exploited_nodes),
            "alert": self.alert,
            "trace": self.trace,
            "feedback": self.feedback,
            "instability": self.instability,
            "system_stress": self.system_stress,
            "history": copy.deepcopy(self.history),
            "rpg_transfer": self.transfer.to_dict(),
        }
