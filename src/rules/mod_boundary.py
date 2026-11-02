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
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping

__all__ = ["BaselineViolation", "Mod", "ModEffect", "ModContractViolation", "apply_mods",
           "validate_registry"]


class BaselineViolation(RuntimeError):
    """A mod tried to change a CWN outcome. This is a design error, never a runtime condition."""


class ModContractViolation(BaselineViolation):
    """A registered mod does not declare what ADR_1054 requires it to declare (#1091)."""


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


REQUIRED_CONTRACT_KEYS = ("hooks", "state", "dependencies", "off_switch", "tabletop_procedure", "status")
STATUSES = ("implemented", "documented")


def validate_registry(entries: Iterable[Mapping[str, Any]], *,
                      root: Path | None = None) -> tuple[str, ...]:
    """Check a mod registry (``data/mods/registry.json``) and return the accepted mod names.

    Two things are checked, because two rules are at stake.

    **The baseline (#897).** Every overlay is listed, none may claim the baseline, and no name repeats.

    **The activation contract (#1091, ADR_1054 §2).** Each mod declares what it hooks, what state it
    owns, what it depends on, how it is switched off and — as a path to a real document — its tabletop
    procedure. A mod that cannot be played with dice and paper is not a mod yet, so a missing procedure
    must be an explicit ``tabletop_gap`` rather than silence.

    A declaration is checked against the code, not taken on trust: every path in ``implementation`` must
    exist, every ``hooks`` entry must appear in one of those files, and an off-switch that names a flag
    must name one the code actually reads.
    """
    base = Path(root) if root is not None else Path(__file__).resolve().parents[2]
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

    for entry in entries:
        _validate_contract(entry, base=base, known=set(names))
    return tuple(names)


def _text_of(entry: Mapping[str, Any], base: Path) -> str:
    parts = []
    for rel in entry.get("implementation") or ():
        path = base / str(rel)
        if path.is_file():
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def _validate_contract(entry: Mapping[str, Any], *, base: Path, known: set[str]) -> None:
    name = str(entry.get("name"))
    missing = [key for key in REQUIRED_CONTRACT_KEYS if key not in entry]
    if missing:
        raise ModContractViolation(
            f"mod {name!r} does not declare {missing}: ADR_1054 §2 is the contract, not a suggestion")

    status = entry["status"]
    if status not in STATUSES:
        raise ModContractViolation(f"mod {name!r} has status {status!r}; expected one of {STATUSES}")

    implementation = list(entry.get("implementation") or ())
    for rel in implementation:
        if not (base / str(rel)).exists():
            raise ModContractViolation(f"mod {name!r} implementation path does not exist: {rel}")

    if status == "implemented" and not implementation:
        raise ModContractViolation(
            f"mod {name!r} claims to be implemented and names no code: that is how a mod stops being real")
    if status == "documented" and implementation:
        raise ModContractViolation(
            f"mod {name!r} is marked documented and names implementation paths; pick one")

    text = _text_of(entry, base)
    hooks = list(entry.get("hooks") or ())
    if status == "implemented" and not hooks:
        raise ModContractViolation(f"mod {name!r} declares no hooks; nothing calls it")
    for hook in hooks:
        if str(hook).split(".")[-1] not in text:
            raise ModContractViolation(
                f"mod {name!r} declares hook {hook!r}, which appears in none of its implementation files")

    state = list(entry.get("state") or ())
    if status == "implemented" and not state:
        raise ModContractViolation(f"mod {name!r} declares no state; ADR_1054 says the mod owns some")

    dependencies = entry.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise ModContractViolation(f"mod {name!r}: dependencies must be an object")
    for key in ("mods", "contracts", "core"):
        if key not in dependencies:
            raise ModContractViolation(f"mod {name!r}: dependencies is missing {key!r}")
    unknown = sorted(set(dependencies.get("mods") or ()) - known)
    if unknown:
        raise ModContractViolation(f"mod {name!r} depends on unknown mods: {unknown}")
    for rel in dependencies.get("contracts") or ():
        if not (base / str(rel)).exists():
            raise ModContractViolation(f"mod {name!r} dependency does not exist: {rel}")

    switch = entry.get("off_switch")
    if not isinstance(switch, Mapping) or "kind" not in switch:
        raise ModContractViolation(f"mod {name!r}: off_switch must be an object with a kind")
    if switch["kind"] == "none":
        if not str(switch.get("gap") or "").strip():
            raise ModContractViolation(
                f"mod {name!r} has no off-switch and says nothing about why: record the gap")
    else:
        switch_name = str(switch.get("name") or "").strip()
        if not switch_name:
            raise ModContractViolation(f"mod {name!r}: off_switch kind {switch['kind']!r} needs a name")
        if switch_name not in text:
            raise ModContractViolation(
                f"mod {name!r}: off-switch {switch_name!r} is not read by any implementation file")

    procedure = entry.get("tabletop_procedure")
    if procedure:
        if not (base / str(procedure)).exists():
            raise ModContractViolation(
                f"mod {name!r} names a tabletop procedure that does not exist: {procedure}")
    elif not str(entry.get("tabletop_gap") or "").strip():
        raise ModContractViolation(
            f"mod {name!r} has no tabletop procedure and no recorded gap; a mod that cannot be played "
            f"with dice and paper is not a mod yet (ADR_1054 §2)")
