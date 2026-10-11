"""Capability checks for the reserved optional adapters — declared, never imported by the core.

Issue #282 requires Mesa, NetworkX and Ollama/Concordia to be **optional and injectable**, with
**no LLM required to load or view world state**. This module is how that requirement is expressed
in code: a side-effect-free availability check over the import system, plus a single explicit entry
point for a caller that has decided it wants an adapter.

Nothing here imports any of the declared adapters at import time, and nothing here decides what an
adapter would do. The purposes below are labels for the reserved seams, not designs.
"""
from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from typing import Any, Mapping

#: The optional adapters this project reserves a seam for. Import order/side effects: none.
OPTIONAL_ADAPTERS: tuple[str, ...] = ("mesa", "networkx", "ollama", "concordia")

#: Human-readable label for each reserved seam. These describe *intent to reserve a slot* only.
ADAPTER_PURPOSE: Mapping[str, str] = {
    "mesa": "optional aggregate-actor support for the political simulation layer",
    "networkx": "optional communication-network layer",
    "ollama": "optional local LLM narration for faction leaders",
    "concordia": "optional agent-runtime adapter",
}


def is_available(module_name: str) -> bool:
    """True if ``module_name`` can be imported in this environment. Imports nothing.

    Uses :func:`importlib.util.find_spec`, so it reports availability without executing module
    code. A missing *parent* package raises :class:`ModuleNotFoundError` from ``find_spec`` and is
    treated as unavailable rather than propagated.
    """
    try:
        return find_spec(module_name) is not None
    except (ImportError, ValueError):
        return False


def available_adapters() -> dict[str, bool]:
    """Availability of every declared optional adapter, as data."""
    return {name: is_available(name) for name in OPTIONAL_ADAPTERS}


def missing_adapters() -> tuple[str, ...]:
    """The declared adapters that are not importable here."""
    return tuple(name for name in OPTIONAL_ADAPTERS if not is_available(name))


def require(module_name: str) -> Any:
    """Import one declared optional adapter, on explicit request only.

    The core load/view path never calls this. Raising :class:`ValueError` for an undeclared name
    keeps the seam closed: an adapter must be declared in ``OPTIONAL_ADAPTERS`` before it can be
    pulled in through this entry point.
    """
    if module_name not in OPTIONAL_ADAPTERS:
        raise ValueError(f"{module_name!r} is not a declared optional adapter")
    return import_module(module_name)
