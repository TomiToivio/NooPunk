#!/usr/bin/env python3
"""Static validation for the intentionally minimal NoöPunk Godot scaffold."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "project.godot",
    "scenes/main.tscn",
    "AGENTS.md",
    "RULEBOOK.md",
    "src/godot/.gitkeep",
    "src/rules/.gitkeep",
    "src/world/.gitkeep",
    "src/simulation/.gitkeep",
    "data/rules/.gitkeep",
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
if "Rules and world systems are intentionally unspecified." not in scene:
    raise SystemExit("bootstrap scene lost its non-canon placeholder notice")

print("NoöPunk Godot scaffold validation passed.")
