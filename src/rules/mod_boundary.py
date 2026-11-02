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


def validate_registry(entries: Iterable[Mapping[str, Any]], *, root: str | None = None) -> tuple[str, ...]:
    """Validate the complete ADR_1054 mod contract (#1091), never just the baseline flag.

    Unknown/unimplemented mods may have empty hooks and state, but may not claim a
    tabletop procedure or silently omit an explicit tabletop gap. This validates
    declarations, not runtime integration or whether an authored procedure is correct.
    """
    from pathlib import Path

    base = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    records = list(entries)
    names = [str(entry.get("name") or "").strip() for entry in records]
    if any(not name for name in names):
        raise BaselineViolation("registry entry without a name")
    if len(set(names)) != len(names):
        raise BaselineViolation(f"duplicate mod names in registry: {sorted(n for n in set(names) if names.count(n) > 1)}")

    def file_at(path: str, label: str) -> Path:
        if not isinstance(path, str) or not path or Path(path).is_absolute() or ".." in Path(path).parts:
            raise BaselineViolation(f"{label}: invalid repository-relative path {path!r}")
        target = (base / path).resolve()
        if not target.is_relative_to(base.resolve()) or not target.is_file():
            raise BaselineViolation(f"{label}: path does not exist: {path}")
        return target

    for entry, name in zip(records, names):
        if entry.get("changes_core_mechanics") is not False:
            raise BaselineViolation(f"registry entry {name!r} must declare changes_core_mechanics=false")
        implementations = entry.get("implementation")
        if not isinstance(implementations, list) or any(not isinstance(p, str) for p in implementations):
            raise BaselineViolation(f"{name}: implementation must be a list of paths")
        for path in implementations:
            file_at(path, name + " implementation")
        hooks = entry.get("hooks")
        state = entry.get("state")
        deps = entry.get("dependencies")
        off = entry.get("off_switch")
        if not isinstance(hooks, list) or not isinstance(state, list) or not isinstance(deps, list):
            raise BaselineViolation(f"{name}: hooks, state and dependencies must be arrays")
        if any(not isinstance(s, str) or not s.strip() for s in state + deps) or len(set(deps)) != len(deps):
            raise BaselineViolation(f"{name}: invalid state/dependency declarations")
        if any(d != "cwn-core" and d not in names for d in deps) or name in deps:
            raise BaselineViolation(f"{name}: unknown/self dependency")
        if not isinstance(off, Mapping) or type(off.get("default_enabled")) is not bool or not isinstance(off.get("behavior"), str) or not off["behavior"].strip():
            raise BaselineViolation(f"{name}: explicit off_switch default_enabled and behavior required")
        if not implementations and (hooks or state or off["default_enabled"]):
            raise BaselineViolation(f"{name}: unimplemented mod must have no hooks/state and must default off")
        for hook in hooks:
            if not isinstance(hook, Mapping) or not isinstance(hook.get("path"), str) or not isinstance(hook.get("symbol"), str):
                raise BaselineViolation(f"{name}: hook needs path and symbol")
            if hook["path"] not in implementations:
                raise BaselineViolation(f"{name}: hook path is not a registered implementation: {hook['path']}")
            if not hook["symbol"].isidentifier():
                raise BaselineViolation(f"{name}: invalid hook symbol")
            source = file_at(hook["path"], name + " hook").read_text(encoding="utf-8")
            import re
            escaped = re.escape(hook["symbol"])
            if not re.search(r"(?m)^\s*(?:static\s+)?(?:func|def)\s+" + escaped + r"\s*\(", source):
                raise BaselineViolation(f"{name}: hook symbol not found: {hook['path']}:{hook['symbol']}")
        procedure, gap = entry.get("tabletop_procedure"), entry.get("tabletop_gap")
        if procedure is not None:
            if not isinstance(procedure, str):
                raise BaselineViolation(f"{name}: tabletop_procedure must be a path or null")
            file_at(procedure, name + " tabletop_procedure")
        elif not isinstance(gap, str) or not gap.strip():
            raise BaselineViolation(f"{name}: missing tabletop procedure must declare tabletop_gap")
    return tuple(names)
