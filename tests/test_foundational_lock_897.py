"""Foundational boundary guards (#897).

The lock is only real if something fails when it is broken. These tests enforce the parts a machine can
check: the core does not reach into overlays, the overlays exist and are documented, the instruction
surface carries the decision, and the art tokens are machine-readable rather than copied into code.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "godot" / "core"
MODS = ROOT / "mods" / "noopunk"


def test_core_never_imports_mods() -> None:
    offenders = []
    for path in CORE.glob("*.gd"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"\bmods/|mods\\|NoopunkPsyche|noopunk/psyche", text):
            offenders.append(path.name)
    assert offenders == [], f"core modules reference overlays: {offenders}"


def test_overlays_do_not_compute_core_resolution() -> None:
    """A mod may not roll dice or compute CWN arithmetic itself."""
    # Check for real coupling — an import or a call — not for the words in a comment that explains the
    # boundary. A guard that fails on prose teaches people to delete the explanation.
    forbidden = ('preload("res://godot/core/', "load(\"res://godot/core/", "RulesAdapter.new",
                 "RulesAdapter.", "attack_roll(", "skill_check(", "save_target(")
    offenders = []
    for path in MODS.glob("*.gd"):
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                offenders.append(f"{path.name}:{token}")
    assert offenders == [], f"overlay computes core resolution: {offenders}"


def test_overlay_folder_is_documented() -> None:
    assert (MODS / "README.md").exists()
    readme = (MODS / "README.md").read_text(encoding="utf-8")
    assert "overlay" in readme.lower()
  # the three rules must be stated, not implied
    assert "godot/core" in readme
    assert "optional" in readme.lower()


def test_lock_document_exists_and_states_the_engine() -> None:
    lock = (ROOT / "docs" / "design" / "FOUNDATIONAL_LOCK_897.md").read_text(encoding="utf-8")
    assert "Cities Without Number" in lock
    assert "locked" in lock.lower()
    assert "approved" in lock and "foundational decision" in lock


def test_matrix_is_the_single_inventory() -> None:
    matrix = ROOT / "docs" / "design" / "CORE_VS_MOD_MATRIX_897.md"
    assert matrix.exists(), "the core/mod matrix must exist; the lock defers to it"
    text = matrix.read_text(encoding="utf-8")
    assert "Verbatim" in text and "Mod" in text


def test_agents_carries_the_current_directive() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    head = agents[:4000]
    assert "#897" in head, "the #897 lock must be in the top of AGENTS.md, where agents read"
    assert "Never replace the rules engine" in head
    assert "mods/noopunk" in head


def test_art_tokens_are_machine_readable_and_valid() -> None:
    tokens_path = ROOT / "docs" / "art" / "design_tokens.json"
    assert tokens_path.exists(), "art tokens must be a file, not a paragraph"
    tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
    assert tokens.get("issue") == "#897"
    palette = tokens.get("palette")
    assert isinstance(palette, dict) and palette, "palette must be a non-empty mapping"

    def walk(node):
        if isinstance(node, dict):
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, str):
            yield node

    hexes = [value for value in walk(palette) if isinstance(value, str) and value.startswith("#")]
    assert len(hexes) >= 6, f"expected a real palette, found {hexes}"
    for value in hexes:
        assert re.fullmatch(r"#[0-9A-Fa-f]{6}", value), f"not a 6-digit hex colour: {value}"


def test_art_tokens_name_what_to_avoid() -> None:
    tokens = json.loads((ROOT / "docs" / "art" / "design_tokens.json").read_text(encoding="utf-8"))
    avoid = json.dumps(tokens).lower()
    assert "neon" in avoid or "1980" in avoid, "the 1974-not-1984 rule must be stated in the tokens"
