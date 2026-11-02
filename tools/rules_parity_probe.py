#!/usr/bin/env python3
"""Behavioural parity probe across the rules layers (#1053, #1054).

The duplication audit answers "how many copies are there". This answers the question that actually decides
whether a copy is a *bug*: **do the copies give the same answer for the same character?**

Two implementations can differ in text and agree in behaviour (debt: they will drift). They can also differ in
*contract* — different parameter names, different capitalisation of categories, different attribute keys — and
that is a defect today, because the same character is resolved differently depending on which layer asked.

The probe loads every implementation it finds, feeds each one a fixed corpus, and reports agreement. It never
modifies a rules module: this is a read-only diagnostic.

Usage:
    python3 tools/rules_parity_probe.py                 # print the matrix
    python3 tools/rules_parity_probe.py --render docs/RULES_PARITY_1053.md
    python3 tools/rules_parity_probe.py --check         # exit 1 if any contract diverges
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Where the same CWN rules are currently implemented. Kept as data so the report states its own scope.
IMPLEMENTATIONS = {
    "src/rules/wn_core.py": "src_rules_wn_core",
    "mud/nopunk_mud/cwn_core.py": "mud_cwn_core",
    "mud/nopunk_mud/cwn/__init__.py": "mud_cwn",
    "mud/systems/cwn.py": "mud_systems_cwn",
}

#: A character every layer must be able to describe, in each naming convention the layers use.
ATTRIBUTES_LONG = {"Strength": 10, "Dexterity": 14, "Constitution": 12,
                   "Intelligence": 9, "Wisdom": 13, "Charisma": 11}
ATTRIBUTES_SHORT = {"STR": 10, "DEX": 14, "CON": 12, "INT": 9, "WIS": 13, "CHA": 11}
ATTRIBUTES_LOWER = {k.lower(): v for k, v in ATTRIBUTES_LONG.items()}

SAVE_CATEGORIES = ("Physical", "Evasion", "Mental", "Luck")


def load_all() -> dict[str, object]:
    modules = {}
    for relative, name in IMPLEMENTATIONS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        spec = importlib.util.spec_from_file_location(f"_probe_{name}", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module  # dataclasses look their module up while building
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # noqa: BLE001 - a layer that cannot import is itself a finding
            modules[relative] = exc
            continue
        modules[relative] = module
    return modules


def call_attribute_modifier(module, score: int):
    fn = getattr(module, "attribute_modifier", None)
    if fn is None:
        return None
    try:
        return fn(score)
    except Exception as exc:  # noqa: BLE001
        return f"{type(exc).__name__}"


def call_save_target(module, relative: str, category: str, level: int, attributes: dict[str, int]):
    """Call `save_target` however this layer spells it — the spelling itself is what we are measuring."""
    fn = getattr(module, "save_target", None)
    if fn is None:
        return None
    attempts = [
        lambda: fn(category, level=level, attributes=attributes),          # mud/cwn
        lambda: fn(category, level=level, modifiers=attributes),           # src/rules
        lambda: fn(level, attributes, category),                           # mud/cwn_core
        lambda: fn(level, category, attributes),                           # mud/systems
    ]
    for attempt in attempts:
        try:
            return attempt()
        except TypeError:
            continue
        except Exception as exc:  # noqa: BLE001
            return f"{type(exc).__name__}"
    return "signature not matched"


def probe_attribute_modifiers(modules: dict) -> dict:
    scores = list(range(3, 19))
    table = {}
    for relative, module in modules.items():
        if isinstance(module, Exception):
            table[relative] = {"_import": type(module).__name__}
            continue
        table[relative] = {str(s): call_attribute_modifier(module, s) for s in scores}
    return {"scores": scores, "table": table}


def probe_saves(modules: dict) -> dict:
    table = {}
    for relative, module in modules.items():
        if isinstance(module, Exception):
            continue
        rows = {}
        for category in SAVE_CATEGORIES:
            for spelling, attributes in (("long", ATTRIBUTES_LONG), ("short", ATTRIBUTES_SHORT),
                                         ("lower", ATTRIBUTES_LOWER)):
                rows[f"{category}/{spelling}"] = call_save_target(module, relative, category, 1, attributes)
        table[relative] = rows
    return table


def compare(attribute_probe: dict, save_probe: dict) -> dict:
    reference = "src/rules/wn_core.py"
    findings = {"attribute_modifier": {}, "save_target": {}}
    if reference in attribute_probe["table"]:
        base = attribute_probe["table"][reference]
        for relative, row in attribute_probe["table"].items():
            if relative == reference or "_import" in row:
                continue
            differing = [s for s in row if row[s] != base.get(s)]
            findings["attribute_modifier"][relative] = differing
    if reference in save_probe:
        base = save_probe[reference]
        for relative, row in save_probe.items():
            if relative == reference:
                continue
            differing = [k for k in row if row[k] != base.get(k)]
            findings["save_target"][relative] = differing
    return findings


def render(attribute_probe: dict, save_probe: dict, findings: dict) -> str:
    lines = [
        "# Rules parity probe (#1053, #1054)",
        "",
        "**Generated by `tools/rules_parity_probe.py`; do not edit by hand.**",
        "",
        ("Duplication is measured statically by `tools/duplication_audit.py`. This document answers the question "
        "that decides whether a duplicate is *debt* or a *bug*: does each copy give the same answer for the same "
        "character?"),
        "",
        ("The probe feeds every layer an identical character and compares output. A layer that cannot be called "
        "with a given spelling is itself the finding — an adapter that resolves the same save differently "
        "depending on which module asked is a defect regardless of the arithmetic."),
        "",
        "## `attribute_modifier` — the arithmetic",
        "",
        "Scores 3–18, compared against `src/rules/wn_core.py`:",
        "",
        "| Layer | Agreement |",
        "|---|---|",
    ]
    for relative, differing in findings["attribute_modifier"].items():
        lines.append(f"| `{relative}` | {'**disagrees at ' + str(differing) + '**' if differing else 'agrees everywhere'} |")
    if not findings["attribute_modifier"]:
        lines.append("| — | only one implementation resolvable |")

    lines += [
        "",
        "## `save_target` — the contract",
        "",
        ("Level 1, every CWN save category, each of the three naming conventions the layers use "
        "(`Physical/Dexterity` · `Physical/STR` · `physical/dexterity`):"),
        "",
        "| Layer | Contract disagreements |",
        "|---|---|",
    ]
    for relative, differing in findings["save_target"].items():
        if differing:
            shown = ", ".join(f"`{d}`" for d in differing[:4]) + ("…" if len(differing) > 4 else "")
            lines.append(f"| `{relative}` | **{len(differing)} of {len(SAVE_CATEGORIES) * 3}** — {shown} |")
        else:
            lines.append(f"| `{relative}` | none |")

    lines += ["", "### Every layer's answer, verbatim", "",
              ("`TypeError`/`KeyError`/`ValueError` are results here, not bugs in the probe: they are how that layer "
              "rejects a character the other layers accept."), "",
              "| Call | " + " | ".join(f"`{r}`" for r in save_probe) + " |",
              "|---|" + "---|" * len(save_probe)]
    keys = sorted({k for row in save_probe.values() for k in row})
    for key in keys:
        cells = [str(save_probe[r].get(key, "—")) for r in save_probe]
        lines.append(f"| `{key}` | " + " | ".join(cells) + " |")

    lines += [
        "",
        "## What this means for #1054",
        "",
        ("The architecture decision says **no engine owns a rule**. These results show the stronger problem: the "
        "rule is owned by four places at once, and they do not agree on how to be called. Consolidating them is "
        "not a refactor for tidiness — until it happens, \"the CWN save rule\" is not a single fact in this "
        "codebase."),
        "",
        ("The arithmetic agreeing (where it can be compared at all) is why this has survived: no test fails, "
        "because no test asks two layers the same question. That is what this probe adds."),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--render", metavar="PATH")
    parser.add_argument("--check", action="store_true", help="exit 1 if any layer's contract diverges")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    modules = load_all()
    attribute_probe = probe_attribute_modifiers(modules)
    save_probe = probe_saves(modules)
    findings = compare(attribute_probe, save_probe)

    diverging = sum(1 for row in findings["attribute_modifier"].values() if row) \
        + sum(1 for row in findings["save_target"].values() if row)
    print(f"attribute_modifier: {len(findings['attribute_modifier'])} layers compared, "
          f"{sum(1 for r in findings['attribute_modifier'].values() if r)} disagree")
    print(f"save_target:        {len(findings['save_target'])} layers compared, "
          f"{sum(1 for r in findings['save_target'].values() if r)} disagree")
    if args.verbose:
        for relative, differing in findings["save_target"].items():
            print(f"  {relative}: {len(differing)} disagreements")

    if args.render:
        target = Path(args.render)
        text = render(attribute_probe, save_probe, findings)
        target.write_text(text, encoding="utf-8")
        print(f"{target}: written")

    if args.check and diverging:
        print(f"{diverging} contract divergence(s) between layers: see docs/RULES_PARITY_1053.md",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
