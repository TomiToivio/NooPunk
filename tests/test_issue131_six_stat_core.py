"""Regression guard for the six-stat core established by issue #131."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = [
    ("Fitness", "FIT"),
    ("Reflexes", "REF"),
    ("Intelligence", "INT"),
    ("Social", "SOC"),
    ("Cybernetics", "CYB"),
    ("Psyche", "PSY"),
]

RETIRED_CODES = {"RES", "REA", "EMP", "PRE", "WIL", "INU", "NOE", "CYI", "BND", "CTL"}


def test_core_json_locks_exactly_six_character_stats() -> None:
    data = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
    actual = [(item["name"], item["code"]) for item in data["stats"]["final_list"]]
    assert actual == EXPECTED


def test_cyber_hardware_stats_are_not_character_stats() -> None:
    data = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
    character_codes = {item["code"] for item in data["stats"]["final_list"]}
    assert data["cybernetic_system"]["character_stat"] == "CYB"
    assert data["cybernetic_system"]["hardware_stats"] == ["COMPUTE", "INTERFACE", "NETWORK"]
    assert character_codes.isdisjoint({"COMPUTE", "INTERFACE", "NETWORK"})


def test_attribute_chapter_uses_six_stat_core_not_retired_twelve_stat_block() -> None:
    text = (ROOT / "rulebook" / "2_ATTRIBUTES.md").read_text(encoding="utf-8")
    for name, code in EXPECTED:
        assert name in text
        assert code in text

    assert "six-STAT" in text
    assert "COMPUTE / INTERFACE / NETWORK are not character STATS" in text
    assert "The final 12-STAT list" not in text

    for code in RETIRED_CODES:
        assert f"({code})" not in text
