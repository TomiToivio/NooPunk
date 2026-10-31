"""NoöPunk MUD — a second game in the same universe (#946).

This package is the **platform-neutral core** the Evennia server will host. It knows nothing about the Godot
project, nothing about engine asset paths, and nothing about Evennia's object model; it holds the authoritative
world state, the CWN contract, the LLM proposal boundary and the simulation bridge.

Boundary: see `docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md`.
"""

__all__ = ["rules_contract", "world_state", "llm_gateway", "sim_bridge"]
__version__ = "0.1.0"

# The MUD shares the CWN kernel in `<repo>/src/rules` rather than keeping a second copy of the
# arithmetic, and this is the one place that makes the sharing importable. Without it, a plain
# `python -m nopunk_mud.cli` from `mud/` (which is how the CLI smoke and the Evennia server are
# started) sees `nopunk_mud` but not `src`, and every rules import dies with
# `ModuleNotFoundError: No module named 'src'` — while the same code passes under pytest, whose
# conftest already puts the root on the path. One path insertion, not an environment variable.
import sys as _sys
from pathlib import Path as _Path

_ROOT = _Path(__file__).resolve().parents[2]
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))
