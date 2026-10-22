"""Psychotronic / Cybernetic hacking simulation demo for Noöpunk.

Standalone graph-based hacking simulator. Not integrated with RPG.

Models hacking as manipulation of a network of informational, psychological,
cybernetic, and noetic nodes rather than conventional terminal minigame.

Public API:
    hack = HackingSimulation()
    hack.build_default_target()      # pre-built demo target
    hack.inspect(node_id)            # inspect a node
    hack.trace(node_a, node_b)        # trace connection
    hack.strengthen(node_a, node_b)   # strengthen edge
    hack.weaken(node_a, node_b)       # weaken edge
    hack.inject(node_id, pattern)     # inject pattern into node
    hack.resonate(node_a, node_b)     # resonate two nodes
    hack.entangle(node_a, node_b)     # entangle two nodes
    hack.isolate(node_id)            # isolate node
    hack.collapse(node_id)           # collapse unstable state
    hack.state()                      # inspectable graph state
    hack.history()                    # event log
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

import networkx as nx

# ── Node types ──────────────────────────────────────────────────

NODE_TYPES = {
    "memory":        {"stability": 50, "description": "Muistijälki tai muistikuvapatterni."},
    "belief":        {"stability": 60, "description": "Uskomus tai vakaumus."},
    "emotion":       {"stability": 40, "description": "Tunnetila tai emotionaalinen kaava."},
    "identity":      {"stability": 70, "description": "Identiteettisolmu, minuuden osa."},
    "archetype":     {"stability": 80, "description": "Jungilainen arkkityyppinen rakenne."},
    "device":        {"stability": 75, "description": "Kyberneettinen laite tai implantaatti."},
    "implant":       {"stability": 85, "description": "BCI tai neurologinen implantti."},
    "process":       {"stability": 55, "description": "Ohjelmistoprosessi tai ajatusrakenne."},
    "conscious":     {"stability": 65, "description": "Conscious Agent -solmu, tietoinen entiteetti."},
    "external":      {"stability": 90, "description": "Ulkoinen verkkosysteemi."},
}

# ── Edge types ──────────────────────────────────────────────────

EDGE_TYPES = {
    "association":   {"description": "Assosiaatio, muistiyhteys."},
    "causal":        {"description": "Kausaaliyhteys, syy-seuraussuhde."},
    "emotional":     {"description": "Emotionaalinen yhteys."},
    "semantic":      {"description": "Semanttinen/merkitysyhteys."},
    "noetic":        {"description": "Noeettinen/kvanttiresonanssiyhteys."},
    "entangled":     {"description": "Kvanttihihmassa oleva yhteys (entanglement)."},
}

# ── Stability states ─────────────────────────────────────────────

def stability_label(value: int) -> str:
    if value >= 80: return "stable"
    if value >= 50: return "wavering"
    if value >= 25: return "unstable"
    return "critical"


@dataclass
class HackEvent:
    tick: int
    action: str
    target: str
    success: bool
    description: str
    side_effects: list[str] = field(default_factory=list)


@dataclass
class HackingSimulation:
    graph: nx.Graph
    _tick: int = 0
    _events: list[HackEvent] = field(default_factory=list)

    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.graph.graph["domain"] = "hacking"
        self._tick = 0
        self._events = []

    # ── Target construction ──────────────────────────────────────

    def add_node(self, node_id: str, node_type: str, label: str = "", **extra: Any) -> None:
        if node_type not in NODE_TYPES:
            raise ValueError(f"Unknown node type: {node_type}")
        stability = extra.pop("stability", NODE_TYPES[node_type]["stability"])
        node_state = extra.pop("state", "coherent")
        self.graph.add_node(
            node_id,
            type=node_type,
            label=label or node_id,
            stability=stability,
            state=node_state,
            patterns=[],
            **extra,
        )

    def add_edge(self, source: str, target: str, edge_type: str, strength: int = 50) -> None:
        if edge_type not in EDGE_TYPES:
            raise ValueError(f"Unknown edge type: {edge_type}")
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            raise KeyError("Both nodes must exist")
        self.graph.add_edge(source, target, type=edge_type, strength=max(0, min(100, strength)))

    def build_default_target(self) -> None:
        """Build a demo target: a patient psyche with implants and external connections."""
        # Identity core
        self.add_node("self_image", "identity", "Self-Image", stability=65)
        self.add_node("cover_identity", "identity", "Cover Identity (Sven-Olof)", stability=55)
        self.add_node("true_self", "identity", "True Self (Romppainen)", stability=30, state="suppressed")

        # Memories
        self.add_node("memory_fall", "memory", "The Fall — Stockholm", stability=35, state="traumatic")
        self.add_node("memory_elsa", "memory", "Elsa's Death", stability=20, state="traumatic")
        self.add_node("memory_childhood", "memory", "Childhood", stability=60)
        self.add_node("memory_academy", "memory", "Police Academy", stability=45, state="suppressed")

        # Beliefs
        self.add_node("belief_ufab_good", "belief", "UFAB Is Good", stability=50)
        self.add_node("belief_firewall", "belief", "Firewall Mission", stability=15, state="suppressed")

        # Emotions
        self.add_node("emotion_ingrid", "emotion", "Attachment to Ingrid", stability=40)
        self.add_node("emotion_fear", "emotion", "Fear of Discovery", stability=55)
        self.add_node("emotion_ufab_craving", "emotion", "UFAB Craving", stability=35)

        # Archetypes
        self.add_node("archetype_warrior", "archetype", "Warrior", stability=70)
        self.add_node("archetype_healer", "archetype", "Healer", stability=60)
        self.add_node("archetype_trickster", "archetype", "Trickster", stability=75)

        # Devices / Implants
        self.add_node("implant_cortical", "implant", "Cortical Stack", stability=90)
        self.add_node("implant_mesh", "implant", "Mesh Inserts", stability=85)
        self.add_node("device_psychotronic", "device", "Psychotronic Interface", stability=70)

        # Conscious agent
        self.add_node("cg_jung", "conscious", "C.G. Jung (UFAB Ragnarök)", stability=80)

        # External
        self.add_node("ext_firewall_net", "external", "Firewall Network", stability=90)
        self.add_node("ext_ufab_net", "external", "UFAB Internal Network", stability=85)

        # Edges — associations and causal links
        self.add_edge("self_image", "cover_identity", "association", 60)
        self.add_edge("self_image", "true_self", "association", 15)
        self.add_edge("cover_identity", "true_self", "association", 10)
        self.add_edge("memory_fall", "memory_elsa", "emotional", 80)
        self.add_edge("memory_fall", "emotion_ingrid", "emotional", 65)
        self.add_edge("memory_elsa", "emotion_ingrid", "emotional", 70)
        self.add_edge("memory_academy", "true_self", "causal", 40)
        self.add_edge("belief_ufab_good", "emotion_ufab_craving", "causal", 55)
        self.add_edge("belief_firewall", "true_self", "causal", 50)
        self.add_edge("archetype_warrior", "true_self", "noetic", 35)
        self.add_edge("archetype_healer", "true_self", "noetic", 30)
        self.add_edge("archetype_trickster", "cover_identity", "noetic", 45)
        self.add_edge("implant_cortical", "memory_academy", "association", 50)
        self.add_edge("implant_mesh", "device_psychotronic", "causal", 60)
        self.add_edge("device_psychotronic", "cg_jung", "noetic", 40)
        self.add_edge("cg_jung", "ext_ufab_net", "semantic", 70)
        self.add_edge("ext_firewall_net", "true_self", "noetic", 25)
        self.add_edge("ext_firewall_net", "belief_firewall", "semantic", 35)
        self.add_edge("implant_cortical", "ext_ufab_net", "semantic", 30)

    # ── Actions ────────────────────────────────────────────────────

    def inspect(self, node_id: str) -> dict[str, Any]:
        """Inspect a node: return its state and connections."""
        if node_id not in self.graph:
            raise KeyError(f"Unknown node: {node_id}")
        data = self.graph.nodes[node_id]
        neighbors = [
            {"id": n, "type": d.get("type", ""), "strength": d.get("strength", 0)}
            for n, d in self.graph[node_id].items()
        ]
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="inspect", target=node_id,
            success=True, description=f"Inspected {node_id}: {stability_label(data['stability'])}",
        ))
        return {
            "id": node_id,
            "type": data.get("type"),
            "label": data.get("label"),
            "stability": data.get("stability"),
            "state": data.get("state"),
            "patterns": data.get("patterns", []),
            "neighbors": neighbors,
        }

    def trace(self, source: str, target: str) -> list[str]:
        """Trace the shortest path between two nodes."""
        if source not in self.graph or target not in self.graph:
            raise KeyError("Both nodes must exist")
        try:
            path = nx.shortest_path(self.graph, source, target)
        except nx.NetworkXNoPath:
            path = []
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="trace", target=f"{source}->{target}",
            success=bool(path), description=f"Trace: {' -> '.join(path) if path else 'no path'}",
        ))
        return path

    def strengthen(self, source: str, target: str, amount: int = 10) -> bool:
        """Strengthen an edge between two nodes."""
        if not self.graph.has_edge(source, target):
            raise KeyError("No edge between nodes")
        current = self.graph[source][target].get("strength", 0)
        self.graph[source][target]["strength"] = min(100, current + amount)
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="strengthen", target=f"{source}-{target}",
            success=True, description=f"Strengthened {source}-{target}: {current} -> {self.graph[source][target]['strength']}",
        ))
        return True

    def weaken(self, source: str, target: str, amount: int = 10) -> bool:
        """Weaken an edge between two nodes."""
        if not self.graph.has_edge(source, target):
            raise KeyError("No edge between nodes")
        current = self.graph[source][target].get("strength", 0)
        new_val = max(0, current - amount)
        self.graph[source][target]["strength"] = new_val
        # If edge becomes very weak, there's a chance it breaks
        broken = False
        if new_val <= 0:
            self.graph.remove_edge(source, target)
            broken = True
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="weaken", target=f"{source}-{target}",
            success=True, description=f"Weakened {source}-{target}: {current} -> {new_val}{' (broken)' if broken else ''}",
            side_effects=["edge_broken"] if broken else [],
        ))
        return True

    def inject(self, node_id: str, pattern: str) -> bool:
        """Inject a pattern into a node. Lowers stability, may change state."""
        if node_id not in self.graph:
            raise KeyError(f"Unknown node: {node_id}")
        data = self.graph.nodes[node_id]
        data["patterns"] = data.get("patterns", []) + [pattern]
        data["stability"] = max(0, data.get("stability", 50) - random.randint(5, 15))
        # If stability drops, state may shift
        if data["stability"] < 25 and data.get("state") == "coherent":
            data["state"] = "destabilized"
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="inject", target=node_id,
            success=True, description=f"Injected '{pattern}' into {node_id}. Stability now {data['stability']}.",
            side_effects=[f"state->{data.get('state')}"] if data.get("state") != "coherent" else [],
        ))
        return True

    def suppress(self, node_id: str) -> bool:
        """Suppress a node's patterns. Raises stability slightly."""
        if node_id not in self.graph:
            raise KeyError(f"Unknown node: {node_id}")
        data = self.graph.nodes[node_id]
        data["patterns"] = []
        data["stability"] = min(100, data.get("stability", 50) + random.randint(5, 10))
        if data.get("state") == "destabilized" and data["stability"] >= 50:
            data["state"] = "coherent"
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="suppress", target=node_id,
            success=True, description=f"Suppressed patterns in {node_id}. Stability now {data['stability']}.",
        ))
        return True

    def resonate(self, source: str, target: str) -> bool:
        """Resonate two nodes. Strengthens their edge and may destabilize both."""
        if not self.graph.has_edge(source, target):
            self.add_edge(source, target, "noetic", 20)
        self.strengthen(source, target, 15)
        # Resonance destabilizes both nodes slightly
        for nid in (source, target):
            data = self.graph.nodes[nid]
            data["stability"] = max(0, data.get("stability", 50) - random.randint(3, 8))
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="resonate", target=f"{source}-{target}",
            success=True, description=f"Resonated {source} and {target}. Edge strengthened, both destabilized slightly.",
        ))
        return True

    def entangle(self, source: str, target: str) -> bool:
        """Entangle two nodes. Creates a quantum-entangled edge."""
        if not self.graph.has_edge(source, target):
            self.add_edge(source, target, "entangled", 50)
        else:
            self.graph[source][target]["type"] = "entangled"
            self.graph[source][target]["strength"] = max(self.graph[source][target].get("strength", 0), 50)
        # Entanglement makes states mirror
        s_data = self.graph.nodes[source]
        t_data = self.graph.nodes[target]
        avg_stability = (s_data.get("stability", 50) + t_data.get("stability", 50)) // 2
        s_data["stability"] = avg_stability
        t_data["stability"] = avg_stability
        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="entangle", target=f"{source}-{target}",
            success=True, description=f"Entangled {source} and {target}. Stabilities synchronized to {avg_stability}.",
        ))
        return True

    def isolate(self, node_id: str) -> list[str]:
        """Remove all edges from a node. Returns removed edge descriptions."""
        if node_id not in self.graph:
            raise KeyError(f"Unknown node: {node_id}")
        removed = list(self.graph.edges(node_id))
        self.graph.remove_edges_from(removed)
        self._tick += 1
        removed_descs = [f"{s}-{t}" for s, t in removed]
        self._events.append(HackEvent(
            tick=self._tick, action="isolate", target=node_id,
            success=True, description=f"Isolated {node_id}. Removed {len(removed)} edges.",
            side_effects=removed_descs,
        ))
        return removed_descs

    def collapse(self, node_id: str) -> dict[str, Any]:
        """Collapse an unstable node state. May stabilize or destroy the node."""
        if node_id not in self.graph:
            raise KeyError(f"Unknown node: {node_id}")
        data = self.graph.nodes[node_id]
        stability = data.get("stability", 50)
        state = data.get("state", "coherent")

        result: dict[str, Any] = {"node": node_id, "before": {"stability": stability, "state": state}}

        if state == "suppressed":
            # Collapsing a suppressed state may reveal it
            if random.random() < 0.4:
                data["state"] = "coherent"
                data["stability"] = min(100, stability + random.randint(10, 25))
                result["outcome"] = "revealed"
                result["after"] = {"stability": data["stability"], "state": data["state"]}
            else:
                data["stability"] = max(0, stability - random.randint(5, 10))
                result["outcome"] = "failed_collapse"
                result["after"] = {"stability": data["stability"], "state": state}
        elif state == "destabilized":
            # Collapsing a destabilized state either stabilizes or collapses
            if random.random() < 0.5:
                data["state"] = "coherent"
                data["stability"] = min(100, stability + random.randint(10, 20))
                result["outcome"] = "stabilized"
            else:
                data["state"] = "collapsed"
                data["stability"] = 0
                result["outcome"] = "collapsed"
            result["after"] = {"stability": data["stability"], "state": data["state"]}
        else:
            # Already coherent — collapse does nothing useful
            result["outcome"] = "no_effect"
            result["after"] = {"stability": stability, "state": state}

        self._tick += 1
        self._events.append(HackEvent(
            tick=self._tick, action="collapse", target=node_id,
            success=result["outcome"] != "no_effect",
            description=f"Collapsed {node_id}: {result['outcome']}.",
        ))
        return result

    # ── State inspection ──────────────────────────────────────────

    def state(self) -> dict[str, Any]:
        """Return inspectable graph state."""
        return {
            "tick": self._tick,
            "nodes": [
                {
                    "id": nid,
                    "type": d.get("type"),
                    "label": d.get("label"),
                    "stability": d.get("stability"),
                    "state": d.get("state"),
                    "patterns": d.get("patterns", []),
                }
                for nid, d in sorted(self.graph.nodes(data=True))
            ],
            "edges": [
                {"source": s, "target": t, "type": d.get("type"), "strength": d.get("strength", 0)}
                for s, t, d in sorted(self.graph.edges(data=True))
            ],
            "node_types": list(NODE_TYPES.keys()),
            "edge_types": list(EDGE_TYPES.keys()),
        }

    def history(self) -> list[dict[str, Any]]:
        """Return event log."""
        return [
            {
                "tick": e.tick, "action": e.action, "target": e.target,
                "success": e.success, "description": e.description,
                "side_effects": e.side_effects,
            }
            for e in self._events
        ]