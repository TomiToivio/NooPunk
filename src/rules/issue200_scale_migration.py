"""Author-directed #200 seven-step scale conversion, independent of dice engine.

The desired Fudge-style -3..+3 ratings are represented in versioned project
data. Legacy 1..10 values remain available to old runtimes during migration.
No external RPG prose, table or NC/OGL content is imported.
"""
from __future__ import annotations

import json
from pathlib import Path

FILE = Path(__file__).resolve().parents[2] / "data" / "rules" / "fudge_scale_migration.json"
CONFIG = json.loads(FILE.read_text(encoding="utf-8"))
RATING_MAP = {int(k): int(v) for k, v in CONFIG["attribute_skill_mapping"].items()}
DIFFICULTY_MAP = {int(k): int(v) for k, v in CONFIG["difficulty_mapping"].items()}
STEP_LABELS = {int(k): str(v) for k, v in CONFIG["difficulty_labels"].items()}
STATS = tuple(CONFIG["stat_codes"])
MIN_STEP, MAX_STEP = CONFIG["bounds"]["min"], CONFIG["bounds"]["max"]


def _convert(value: int, mapping: dict[int, int], name: str) -> int:
    if type(value) is not int or value not in mapping:
        raise ValueError(f"Unsupported legacy {name} value: {value!r}")
    return mapping[value]


def attribute_level(legacy_level: int) -> int:
    """Translate a legacy 1..10 Attribute to the new -3..+3 rating."""
    return _convert(legacy_level, RATING_MAP, "Attribute")


def skill_level(legacy_level: int) -> int:
    """Same seven-step scale, preserving the separate Skill dimension."""
    return _convert(legacy_level, RATING_MAP, "Skill")


def difficulty_level(legacy_dv: int) -> int:
    """Map one of the seven canonical named legacy difficulties."""
    return _convert(legacy_dv, DIFFICULTY_MAP, "difficulty")


def difficulty_name(step: int) -> str:
    """Current NoöPunk difficulty label on a new scale, not a Fate label."""
    if type(step) is not int or step not in STEP_LABELS:
        raise ValueError(f"Unsupported difficulty step: {step!r}")
    return STEP_LABELS[step]


def convert_character(attributes: dict[str, int], skills: dict[str, int]) -> dict[str, dict[str, int]]:
    """Convert two separate dictionaries, retaining names and rejecting unknown STATs.

    Skill names are checked against the current machine-readable vocabulary to
    ensure that the conversion does not invent or delete competencies.
    """
    if set(attributes) != set(STATS):
        raise ValueError("Character must supply exactly the six canonical Attributes")
    skills_source = FILE.parent / "skills.json"
    valid_skills = {entry["name"] for entry in json.loads(skills_source.read_text(encoding="utf-8"))["skills"]}
    if not set(skills).issubset(valid_skills):
        raise ValueError("Unknown canonical Skill")
    return {
        "attributes": {key: attribute_level(value) for key, value in attributes.items()},
        "skills": {key: skill_level(value) for key, value in skills.items()},
    }
