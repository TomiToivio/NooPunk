"""The CWN rules registry must stay exhaustive and current (see tools/cwn_coverage_manifest.py).

This tests executable behaviour: that every public rule procedure under src/rules is present in
the committed registry, and that the registry is not stale. It does not test prose.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _tool():
    spec = importlib.util.spec_from_file_location(
        "cwn_coverage_manifest", ROOT / "tools" / "cwn_coverage_manifest.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_registry_lists_every_public_rule_procedure():
    data = _tool().build()
    assert data["totals"]["modules"] > 0
    assert data["totals"]["procedures"] > 0
    listed = {}
    for module in data["modules"]:
        names = set()
        for entry in module["procedures"]:
            names.add(entry["name"])
            for method in entry.get("methods", []):
                names.add(method["name"].split(".")[-1])
        listed[module["module"]] = names
    # A representative procedure from each implemented subsystem must be present.
    for module, name in (
        ("cwn_core.py", "resolve_attack"),
        ("cwn_core.py", "trauma_damage"),
        ("cwn_character.py", "roll_attributes"),
        ("cwn_combat.py", "attack_roll"),
        ("cwn_attack_modifiers.py", "attack_modifier"),
    ):
        assert name in listed.get(module, set()), f"{name} missing from {module}"


def test_the_committed_registry_is_not_stale():
    tool = _tool()
    committed = json.loads((ROOT / "data" / "rules" / "cwn_coverage.json").read_text(encoding="utf-8"))
    assert committed == tool.build(), "run python3 tools/cwn_coverage_manifest.py"


def test_check_mode_reports_current():
    assert _tool().main(["--check"]) == 0
