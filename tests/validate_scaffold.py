#!/usr/bin/env python3
"""Static validation for the intentionally minimal NoöPunk Godot scaffold."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "project.godot",
    "scenes/main.tscn",
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

project = (ROOT / "project.godot").read_text(encoding="utf-8")
if 'run/main_scene="res://scenes/main.tscn"' not in project:
    raise SystemExit("project.godot does not point to the bootstrap scene")

scene = (ROOT / "scenes/main.tscn").read_text(encoding="utf-8")
if "Core attributes/checks specified; other systems remain intentionally unresolved." not in scene:
    raise SystemExit("bootstrap scene lost its scoped rules-status notice")

print("NoöPunk Godot scaffold validation passed.")
