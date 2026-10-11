"""Optional-dependency capability checks for the strategy game scaffold.

Issue #282 requires Mesa, NetworkX and Ollama/Concordia to stay **optional and
injectable**, and requires that **no LLM is needed** to load or view world state. This
module is how the scaffold states that as code rather than as a promise in a README.

Two rules it exists to keep:

* Nothing here imports an optional package. ``importlib.util.find_spec`` reports whether
  a distribution is importable without paying for the import, so a machine with none of
  them still loads the scaffold, serializes a world and renders the view model.
* A caller that genuinely wants an adapter asks for it by name and gets an actionable
  error when it is absent, instead of an ``ImportError`` from somewhere unrelated.

No rule, threshold, cadence or decision procedure lives here — this is a capability
report, nothing more.
"""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass

#: (capability name, importable module, what an adapter would use it for)
_CANDIDATES: tuple[tuple[str, str, str], ...] = (
    ("networkx", "networkx", "multiplex network queries over the graph view"),
    ("mesa", "mesa", "aggregate and meso population agents"),
    ("ollama", "ollama", "optional LLM faction-leader deliberation"),
    ("concordia", "concordia", "optional Concordia agent runner"),
)


@dataclass(frozen=True)
class Capability:
    """Whether one optional adapter is importable, and what it would be for."""

    name: str
    module: str
    purpose: str
    available: bool


def _is_importable(module: str) -> bool:
    """Report importability without importing. Never raises."""
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def capabilities() -> tuple[Capability, ...]:
    """Every optional adapter this scaffold knows about, with its availability."""
    return tuple(
        Capability(name=name, module=module, purpose=purpose, available=_is_importable(module))
        for name, module, purpose in _CANDIDATES
    )


def available_names() -> tuple[str, ...]:
    """Names of the optional adapters present in this environment."""
    return tuple(cap.name for cap in capabilities() if cap.available)


def require(name: str) -> Capability:
    """Return one capability, or raise an actionable error when it is absent.

    The scaffold never calls this on the load/serialize/view path, so a missing adapter
    can never stop a world state from being read.
    """
    for cap in capabilities():
        if cap.name == name:
            if not cap.available:
                raise RuntimeError(
                    f"optional adapter {name!r} (module {cap.module!r}) is not installed. "
                    f"It is used for {cap.purpose}. The scaffold does not require it: "
                    "world state still loads, serializes and renders without it."
                )
            return cap
    raise KeyError(f"unknown optional adapter {name!r}")
