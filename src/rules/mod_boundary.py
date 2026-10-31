"""The adapter boundary between the CWN baseline and NoöPunk mods (#897).

`docs/rules/RULES_BASIS_LOCK.md` states the rule: a mod **reads** the resolved CWN state and adds
narrative state; it may not change a CWN number. A document cannot enforce that, so this module does:

* a mod is an object with a name, a ``resolve()`` that returns *narrative* state only, and an explicit
  ``changes_core_mechanics`` declaration — a mod that declares it touches the baseline is refused;
* the resolved outcome is handed to a mod behind a read-only view, so mutating it raises instead of
  silently rewriting the resolution;
* a narrative effect may not shadow a key of the outcome (``total``, ``dv``, ``success`` …), which is how
  a "narrative" mod would otherwise overwrite a mechanical result;
* the outcome is compared before and after every mod, so the baseline is *provably* unchanged.

Baseline resolution itself is untouched: mods never sit inside the resolver. This module is the seam,
and ``tests/test_issue897_core_mod_boundary.py`` is the parity guard the lock promises.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping

__all__ = ["BaselineViolation", "Mod", "ModEffect", "apply_mods", "validate_registry"]


class BaselineViolation(RuntimeError):
    """A mod tried to change a CWN outcome. This is a design error, never a runtime condition."""


@dataclass(frozen=True)
class ModEffect:
    """What a mod is allowed to contribute: narrative state, namespaced by the mod's own name."""

    state: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", dict(self.state))


@dataclass(frozen=True)
class Mod:
    """A NoöPunk overlay. ``resolve`` receives the read-only outcome and the current narrative state."""

    name: str
    resolve: Callable[[Mapping[str, Any], Mapping[str, Any]], ModEffect | Mapping[str, Any] | None]
    changes_core_mechanics: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("a mod needs a name; an anonymous overlay cannot be audited")


def _effect_state(mod: Mod, effect: ModEffect | Mapping[str, Any] | None,
                  core_keys: frozenset[str]) -> dict[str, Any]:
    if effect is None:
        return {}
    state = dict(effect.state if isinstance(effect, ModEffect) else effect)
    shadowed = sorted(set(state) & core_keys)
    if shadowed:
        raise BaselineViolation(
            f"mod {mod.name!r} returned baseline keys {shadowed}: narrative state may not shadow a "
            f"CWN outcome — that is a rules change, not an overlay (#897)")
    return state


def apply_mods(
    outcome: Mapping[str, Any],
    mods: Iterable[Mod],
    *,
    state: Mapping[str, Any] | None = None,
    core_keys: Iterable[str] | None = None,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Run mods over a resolved CWN outcome; return ``(unchanged outcome, narrative state)``.

    ``core_keys`` defaults to the outcome's own keys, so a mod that tries to return ``total`` or ``dv``
    is refused even if nobody remembered to register them. Raising is the point: a mod that changes a
    CWN number must fail loudly here rather than quietly in a session.
    """
    protected = frozenset(outcome if core_keys is None else core_keys)
    resolved = dict(outcome)
    snapshot = copy.deepcopy(resolved)
    narrative: dict[str, dict[str, Any]] = dict(state or {})
    view = MappingProxyType(resolved)  # a mod may read this mapping, never write it
    for mod in mods:
        if mod.changes_core_mechanics:
            raise BaselineViolation(
                f"mod {mod.name!r} declares changes_core_mechanics: the baseline is CWN as written "
                f"(#897), so that proposal needs an approved foundational decision")
        narrative[mod.name] = _effect_state(
            mod, mod.resolve(view, MappingProxyType(narrative)), protected)
        if resolved != snapshot:
            raise BaselineViolation(f"mod {mod.name!r} changed the resolved outcome")
    return resolved, narrative


def validate_registry(entries: Iterable[Mapping[str, Any]]) -> tuple[str, ...]:
    """Check a mod registry (``data/mods/registry.json``) and return the accepted mod names.

    The registry is the machine-readable half of the core-versus-mod matrix: every overlay is listed,
    and none may claim the baseline.
    """
    names: list[str] = []
    for entry in entries:
        name = str(entry.get("name") or "").strip()
        if not name:
            raise BaselineViolation("registry entry without a name")
        if entry.get("changes_core_mechanics"):
            raise BaselineViolation(
                f"registry entry {name!r} declares changes_core_mechanics: it is a rules change, "
                f"not a mod")
        names.append(name)
    duplicates = {name for name in names if names.count(name) > 1}
    if duplicates:
        raise BaselineViolation(f"duplicate mod names in registry: {sorted(duplicates)}")
    return tuple(names)
