from __future__ import annotations

import copy
import json
import random
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


def _clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(value)))


@dataclass(frozen=True)
class HackingResult:
    action: str
    success: bool
    summary: str
    cost: int = 0
    alert_delta: int = 0
    data: object | None = None


class HackingSimulation:
    """Graph-manipulation sandbox; mechanics are fictional, not neuroscience."""

    COSTS = {
        "inspect_node": 0, "trace_connection": 0, "strengthen_edge": 1,
        "weaken_edge": 1, "inject_pattern": 2, "suppress_pattern": 1,
        "resonate_nodes": 2, "entangle_nodes": 2, "isolate_node": 2,
        "collapse_state": 2, "create_association": 1, "break_association": 1,
    }

    def __init__(self, graph: nx.Graph, focus: int = 12, seed: int = 1):
        self.graph = graph
        self.focus = focus
        self.alert = 0
        self.turn = 0
        self.history: list[dict[str, object]] = []
        self._rng = random.Random(seed)

    @classmethod
    def from_dict(cls, data: dict[str, object], seed: int = 1) -> "HackingSimulation":
        graph = nx.Graph(domain="psychotronic_cybernetic_hacking")
        for node in data.get("nodes", []):
            record = dict(node)
            node_id = str(record.pop("id"))
            record.setdefault("state", "stable")
            record["stability"] = _clamp(record.get("stability", 50))
            record["activation"] = max(-100, min(100, int(record.get("activation", 0))))
            record.setdefault("patterns", [])
            graph.add_node(node_id, **record)
        for edge in data.get("edges", []):
            record = dict(edge)
            source, target = str(record.pop("source")), str(record.pop("target"))
            if source not in graph or target not in graph:
                raise ValueError(f"Unknown hacking edge endpoint: {source}, {target}")
            record["strength"] = _clamp(record.get("strength", 50))
            record.setdefault("relation", "association")
            record.setdefault("active", True)
            graph.add_edge(source, target, **record)
        return cls(graph, focus=int(data.get("focus", 12)), seed=seed)

    @classmethod
    def from_json(cls, path: str | Path, seed: int = 1) -> "HackingSimulation":
        with Path(path).open(encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle), seed=seed)

    def _require_nodes(self, *nodes: str) -> None:
        missing = [node for node in nodes if node not in self.graph]
        if missing:
            raise KeyError(f"Unknown node(s): {', '.join(missing)}")

    def _afford(self, action: str) -> HackingResult | None:
        if self.COSTS[action] > self.focus:
            return HackingResult(action, False, "Insufficient focus.")
        return None

    def _commit(self, result: HackingResult) -> HackingResult:
        if result.cost > self.focus:
            return HackingResult(result.action, False, "Insufficient focus.")
        if result.success:
            self.focus -= result.cost
            self.alert = _clamp(self.alert + result.alert_delta)
            self.turn += 1
            self.history.append({"turn": self.turn, "focus": self.focus, "alert": self.alert,
                                 "action": result.action, "summary": result.summary})
        return result

    def inspect_node(self, node: str) -> HackingResult:
        self._require_nodes(node)
        data = {"id": node, **copy.deepcopy(self.graph.nodes[node]),
                "neighbors": sorted(self.graph.neighbors(node))}
        return self._commit(HackingResult("inspect_node", True, f"Inspected {node}.", data=data))

    def trace_connection(self, source: str, target: str) -> HackingResult:
        self._require_nodes(source, target)
        active = nx.Graph((u, v) for u, v, a in self.graph.edges(data=True) if a.get("active", True))
        active.add_nodes_from(self.graph.nodes)
        try:
            path = nx.shortest_path(active, source, target)
        except nx.NetworkXNoPath:
            return HackingResult("trace_connection", False, "No active route.")
        return self._commit(HackingResult("trace_connection", True, "Connection traced.", data=path))

    def adjust_edge(self, source: str, target: str, amount: int) -> HackingResult:
        self._require_nodes(source, target)
        action = "strengthen_edge" if amount >= 0 else "weaken_edge"
        if blocked := self._afford(action):
            return blocked
        if not self.graph.has_edge(source, target):
            return HackingResult(action, False, "No association exists.")
        edge = self.graph.edges[source, target]
        edge["strength"] = _clamp(int(edge.get("strength", 0)) + amount)
        return self._commit(HackingResult(action, True, f"Association strength is {edge['strength']}.", 1, 2))

    def inject_pattern(self, node: str, pattern: str) -> HackingResult:
        self._require_nodes(node)
        if blocked := self._afford("inject_pattern"):
            return blocked
        attrs = self.graph.nodes[node]
        if pattern not in attrs["patterns"]:
            attrs["patterns"].append(pattern)
        attrs["activation"] = min(100, int(attrs["activation"]) + 20)
        attrs["stability"] = _clamp(int(attrs["stability"]) - 10)
        attrs["state"] = "unstable"
        return self._commit(HackingResult("inject_pattern", True, f"Injected {pattern} into {node}.", 2, 8))

    def suppress_pattern(self, node: str, pattern: str) -> HackingResult:
        self._require_nodes(node)
        if blocked := self._afford("suppress_pattern"):
            return blocked
        attrs = self.graph.nodes[node]
        if pattern not in attrs["patterns"]:
            return HackingResult("suppress_pattern", False, "Pattern is not present.")
        attrs["patterns"].remove(pattern)
        attrs["activation"] = max(-100, int(attrs["activation"]) - 15)
        return self._commit(HackingResult("suppress_pattern", True, f"Suppressed {pattern}.", 1, 3))

    def resonate_nodes(self, source: str, target: str) -> HackingResult:
        self._require_nodes(source, target)
        if blocked := self._afford("resonate_nodes"):
            return blocked
        if not self.graph.has_edge(source, target):
            return HackingResult("resonate_nodes", False, "Resonance requires an association.")
        for node in (source, target):
            self.graph.nodes[node]["activation"] = min(100, int(self.graph.nodes[node]["activation"]) + 10)
        self.graph.edges[source, target]["strength"] = _clamp(self.graph.edges[source, target]["strength"] + 10)
        return self._commit(HackingResult("resonate_nodes", True, "Nodes entered a shared resonance.", 2, 6))

    def entangle_nodes(self, source: str, target: str) -> HackingResult:
        self._require_nodes(source, target)
        if blocked := self._afford("entangle_nodes"):
            return blocked
        self.graph.add_edge(source, target, relation="entanglement", strength=50, active=True)
        self.graph.nodes[source]["state"] = self.graph.nodes[target]["state"] = "superposed"
        return self._commit(HackingResult("entangle_nodes", True, "Nodes are provisionally entangled.", 2, 10))

    def isolate_node(self, node: str) -> HackingResult:
        self._require_nodes(node)
        if blocked := self._afford("isolate_node"):
            return blocked
        self.graph.nodes[node]["state"] = "isolated"
        for neighbor in self.graph.neighbors(node):
            self.graph.edges[node, neighbor]["active"] = False
        return self._commit(HackingResult("isolate_node", True, f"Isolated {node}.", 2, 5))

    def collapse_state(self, node: str) -> HackingResult:
        self._require_nodes(node)
        if blocked := self._afford("collapse_state"):
            return blocked
        attrs = self.graph.nodes[node]
        chance = _clamp(attrs["stability"]) / 100
        success = self._rng.random() <= chance
        attrs["state"] = "collapsed" if success else "unstable"
        attrs["stability"] = _clamp(attrs["stability"] + (15 if success else -10))
        return self._commit(HackingResult("collapse_state", True,
            f"Collapse {'stabilized' if success else 'destabilized'} {node}.", 2, 7, {"stabilized": success}))

    def create_association(self, source: str, target: str) -> HackingResult:
        self._require_nodes(source, target)
        if blocked := self._afford("create_association"):
            return blocked
        if self.graph.has_edge(source, target):
            return HackingResult("create_association", False, "Association already exists.")
        self.graph.add_edge(source, target, relation="association", strength=25, active=True)
        return self._commit(HackingResult("create_association", True, "Association created.", 1, 4))

    def break_association(self, source: str, target: str) -> HackingResult:
        self._require_nodes(source, target)
        if blocked := self._afford("break_association"):
            return blocked
        if not self.graph.has_edge(source, target):
            return HackingResult("break_association", False, "Association does not exist.")
        self.graph.remove_edge(source, target)
        return self._commit(HackingResult("break_association", True, "Association broken.", 1, 5))

    def snapshot(self) -> dict[str, object]:
        return {"turn": self.turn, "focus": self.focus, "alert": self.alert,
                "nodes": [{"id": n, **copy.deepcopy(a)} for n, a in sorted(self.graph.nodes(data=True))],
                "edges": [{"source": u, "target": v, **copy.deepcopy(a)} for u, v, a in sorted(self.graph.edges(data=True))],
                "history": copy.deepcopy(self.history)}
