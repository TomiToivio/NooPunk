"""Formal validator for city-and-environs scenario data (issue #324 deliverable C).

The repo already says this was missing: ``docs/LOCAL_SLICE_RULES_PROVISIONAL.md`` lists the
**"formal scenario schema validator"** among the known omissions, and
``docs/scenarios/REPUBLIC_OF_UKWELI.md`` states that "the model and mechanics accept any scenario
conforming to the JSON schema" without a schema existing. This module and
``data/city_scenario_schema.json`` close that.

What it does: reads the declarative schema and checks a scenario against it — required and optional
fields, types, item counts, unique ids, and cross-references (a leader's location, faction and
portfolio; a party's leader_ids; a route's endpoints; a relationship's endpoints). It **derives
nothing**: no value, cost, outcome or threshold is computed, and no rule is read or applied. A
scenario that validates is *shaped* correctly, not balanced or approved.

What it is for: any city, not just Ukweli. Nothing here names a country, a party, a district or an
institution, and the portfolios are consumed from the engine rather than restated.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .local_slice import PORTFOLIOS

#: The declarative schema's own contract.
SCHEMA_FORMAT = "noopunk.strategy_game.city_scenario_schema"
SCHEMA_VERSION = 1

SCHEMA_PATH = Path(__file__).with_name("data") / "city_scenario_schema.json"

_TYPE_CHECKS: dict[str, Any] = {
    "str": lambda v: isinstance(v, str),
    "int": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "float": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "bool": lambda v: isinstance(v, bool),
    "list": lambda v: isinstance(v, list),
    "dict": lambda v: isinstance(v, Mapping),
}


class ScenarioSchemaError(ValueError):
    """Raised when the schema itself cannot be read or is malformed."""


def _type_ok(value: Any, declared: str) -> bool:
    if declared.endswith("]"):
        base, _, inner = declared.partition("[")
        inner = inner.rstrip("]")
        if base != "list" or not isinstance(value, list):
            return False
        check = _TYPE_CHECKS.get(inner)
        return check is None or all(check(item) for item in value)
    check = _TYPE_CHECKS.get(declared)
    return True if check is None else check(value)


def load_schema(path: Path | str | None = None) -> dict[str, Any]:
    """Read the declarative schema and check its own format and version."""
    source = Path(path) if path is not None else SCHEMA_PATH
    try:
        schema = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScenarioSchemaError(f"scenario schema not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise ScenarioSchemaError(f"{source} is not valid JSON: {exc}") from exc
    if schema.get("format") != SCHEMA_FORMAT or schema.get("version") != SCHEMA_VERSION:
        raise ScenarioSchemaError(
            f"unexpected schema contract: format={schema.get('format')!r} version={schema.get('version')!r}"
        )
    return schema


def validate_scenario(
    data: Mapping[str, Any], schema: Mapping[str, Any] | None = None
) -> tuple[str, ...]:
    """Validate a scenario mapping. Returns the problems found; empty means it conforms."""
    schema = dict(schema or load_schema())
    problems: list[str] = []
    fields: Mapping[str, Any] = schema["fields"]
    records: Mapping[str, Any] = schema["records"]
    constraints: Mapping[str, Any] = schema["constraints"]

    if not isinstance(data, Mapping):
        return (f"scenario must be a mapping, got {type(data).__name__}",)

    # --- top-level fields ---------------------------------------------------
    for name, spec in fields.items():
        value = data.get(name)
        if value is None:
            if spec.get("required"):
                problems.append(f"{name}: required field missing")
            continue
        if not _type_ok(value, str(spec.get("type", "str"))):
            problems.append(f"{name}: expected {spec.get('type')}, got {type(value).__name__}")
            continue
        if isinstance(value, list):
            if "min_items" in spec and len(value) < int(spec["min_items"]):
                problems.append(f"{name}: needs at least {spec['min_items']} items, has {len(value)}")
            if "max_items" in spec and len(value) > int(spec["max_items"]):
                problems.append(f"{name}: allows at most {spec['max_items']} items, has {len(value)}")

    def record_problems(kind: str, index: int, item: Any) -> None:
        label = f"{kind}[{index}]"
        spec = records.get(kind)
        if spec is None:
            return
        if not isinstance(item, Mapping):
            problems.append(f"{label}: must be a mapping")
            return
        for field in spec.get("required", []):
            if field not in item:
                problems.append(f"{label}: required field {field!r} missing")
        allowed = set(spec.get("required", [])) | set(spec.get("optional", []))
        for field in item:
            if field not in allowed and constraints.get("unknown_record_fields_are_reported"):
                problems.append(f"{label}: unknown field {field!r} (schema allows {sorted(allowed)})")
        for field, declared in (spec.get("types") or {}).items():
            if field in item and not _type_ok(item[field], declared):
                problems.append(f"{label}: {field!r} expected {declared}, got {type(item[field]).__name__}")

    for kind in ("location", "party", "leader", "relationship", "shock"):
        for index, item in enumerate(data.get(kind + "s", []) or []):
            record_problems(kind, index, item)

    # --- unique ids ---------------------------------------------------------
    for collection in constraints.get("unique_ids", []):
        seen: dict[str, int] = {}
        for index, item in enumerate(data.get(collection, []) or []):
            if not isinstance(item, Mapping):
                continue
            identifier = str(item.get("id", ""))
            if identifier in seen:
                problems.append(f"{collection}[{index}]: duplicate id {identifier!r}")
            seen[identifier] = index

    # --- routes -------------------------------------------------------------
    location_ids = {str(x.get("id")) for x in (data.get("locations") or []) if isinstance(x, Mapping)}
    route_spec = constraints.get("routes", {})
    for index, route in enumerate(data.get("routes", []) or []):
        if not isinstance(route, list) or len(route) != 2:
            problems.append(f"routes[{index}]: must be a two-element list of location ids")
            continue
        if any(not isinstance(end, str) for end in route):
            problems.append(f"routes[{index}]: endpoints must be strings")
            continue
        if route_spec.get("pair_must_differ") and route[0] == route[1]:
            problems.append(f"routes[{index}]: a route needs two different endpoints")
        if route_spec.get("endpoints_must_exist"):
            for end in route:
                if end not in location_ids:
                    problems.append(f"routes[{index}]: endpoint {end!r} is not a location id")

    # --- leaders and parties ------------------------------------------------
    party_ids = {str(x.get("id")) for x in (data.get("parties") or []) if isinstance(x, Mapping)}
    leader_ids: set[str] = set()
    leader_spec = constraints.get("leaders", {})
    for index, leader in enumerate(data.get("leaders", []) or []):
        if not isinstance(leader, Mapping):
            continue
        identifier = str(leader.get("id", ""))
        leader_ids.add(identifier)
        if leader_spec.get("location_must_exist") and str(leader.get("location")) not in location_ids:
            problems.append(f"leaders[{index}]: location {leader.get('location')!r} is not a location id")
        if leader_spec.get("faction_must_be_a_party") and str(leader.get("faction")) not in party_ids:
            problems.append(f"leaders[{index}]: faction {leader.get('faction')!r} is not a party id")
        if leader_spec.get("portfolio_must_be_declared") and str(leader.get("portfolio")) not in PORTFOLIOS:
            problems.append(
                f"leaders[{index}]: portfolio {leader.get('portfolio')!r} is not one of {PORTFOLIOS}"
            )
    expected = int(constraints.get("leaders_per_party", 0) or 0)
    for index, party in enumerate(data.get("parties", []) or []):
        if not isinstance(party, Mapping):
            continue
        ids = [str(x) for x in (party.get("leader_ids") or [])]
        if expected and len(ids) != expected:
            problems.append(f"parties[{index}]: needs exactly {expected} leader_ids, has {len(ids)}")
        if len(set(ids)) != len(ids):
            problems.append(f"parties[{index}]: leader_ids must be unique")
        for leader_id in ids:
            if leader_id not in leader_ids:
                problems.append(f"parties[{index}]: leader_id {leader_id!r} is not a leader")
        faction_leaders = {
            str(x.get("id")) for x in (data.get("leaders") or [])
            if isinstance(x, Mapping) and str(x.get("faction")) == str(party.get("id"))
        }
        if set(ids) != faction_leaders:
            problems.append(
                f"parties[{index}]: leader_ids do not match the leaders whose faction is {party.get('id')!r}"
            )

    # --- relationships ------------------------------------------------------
    for index, relation in enumerate(data.get("relationships", []) or []):
        if not isinstance(relation, Mapping):
            continue
        a, b = str(relation.get("a", "")), str(relation.get("b", ""))
        if a == b:
            problems.append(f"relationships[{index}]: needs two different endpoints")
        for end in (a, b):
            if end not in leader_ids:
                problems.append(f"relationships[{index}]: endpoint {end!r} is not a leader id")

    return tuple(problems)


def load_scenario(
    path: Path | str, schema: Mapping[str, Any] | None = None
) -> tuple[dict[str, Any], tuple[str, ...]]:
    """Read a scenario and validate it. Returns ``(data, problems)``; problems may be empty."""
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScenarioSchemaError(f"scenario not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise ScenarioSchemaError(f"{source} is not valid JSON: {exc}") from exc
    if not isinstance(data, Mapping):
        raise ScenarioSchemaError("a scenario file must contain a JSON object")
    return dict(data), validate_scenario(data, schema)


def build_local_game(path: Path | str | None = None):
    """A validated scenario as a :class:`strategy_game.local_slice.Game`.

    The engine's own invariants are still asserted by ``Game.validate()``: this bridge checks the
    schema *first* so a shape error is reported as a readable list rather than an assertion, then
    hands the same file to the engine. No rule is added or changed by doing so.
    """
    if path is None:
        from .local_slice import DATA

        path = DATA
    data, problems = load_scenario(path)
    if problems:
        raise ScenarioSchemaError("; ".join(problems))
    from .local_slice import Game

    return Game.from_scenario(Path(path))
