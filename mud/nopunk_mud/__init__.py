"""NoöPunk MUD — a second game in the same universe (#946).

This package is the **platform-neutral core** the Evennia server will host. It knows nothing about the Godot
project, nothing about engine asset paths, and nothing about Evennia's object model; it holds the authoritative
world state, the CWN contract, the LLM proposal boundary and the simulation bridge.

Boundary: see `docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md`.
"""

__all__ = ["rules_contract", "world_state", "llm_gateway", "sim_bridge"]
__version__ = "0.1.0"
