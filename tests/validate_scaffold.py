#!/usr/bin/env python3
"""Static validation for the intentionally minimal NoöPunk Godot scaffold."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "project.godot",
    "scenes/main.tscn",
    "AGENTS.md",
    "RULEBOOK.md",
    "docs/DESIGN_PRINCIPLES.md",
    "src/godot/.gitkeep",
    "src/godot/core_rules.gd",
    "src/rules/.gitkeep",
    "src/rules/__init__.py",
    "src/rules/core.py",
    "src/world/.gitkeep",
    "src/simulation/.gitkeep",
    "data/rules/.gitkeep",
    "data/rules/core.json",
    "data/world/.gitkeep",
    "data/simulation/.gitkeep",
]

missing = [path for path in REQUIRED if not (ROOT / path).exists()]
if missing:
    raise SystemExit("Missing scaffold files: " + ", ".join(missing))

# The three design balances have exactly one canonical explanation. It is part of
# the scaffold, not decoration: agents must be able to find it, and its removal
# should fail loudly rather than silently leaving the balances undocumented.
PRINCIPLES = (ROOT / "docs/DESIGN_PRINCIPLES.md").read_text(encoding="utf-8")
for required_section in (
    "Gamism / Narrativism / Simulationism",
    "CY_BORG",
    "Cyberpunk 2020",
    "The Sprawl",
    "Tabletop / Godot / Concordia",
    "Cyberpunk / Noösphere",
    "UFO / UAP Disclosure",
    "Psionics",
    "Panpsychism",
    "Shadowrun",
    "Eclipse Phase",
):
    if required_section not in PRINCIPLES:
        raise SystemExit(
            f"docs/DESIGN_PRINCIPLES.md no longer documents '{required_section}'"
        )

agent_rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
if "docs/DESIGN_PRINCIPLES.md" not in agent_rules:
    raise SystemExit("AGENTS.md no longer points agents at docs/DESIGN_PRINCIPLES.md")

project = (ROOT / "project.godot").read_text(encoding="utf-8")
if 'run/main_scene="res://scenes/main.tscn"' not in project:
    raise SystemExit("project.godot does not point to the bootstrap scene")

scene = (ROOT / "scenes/main.tscn").read_text(encoding="utf-8")
if "Core attributes/checks specified; other systems remain intentionally unresolved." not in scene:
    raise SystemExit("bootstrap scene lost its scoped rules-status notice")

print("NoöPunk Godot scaffold validation passed.")
