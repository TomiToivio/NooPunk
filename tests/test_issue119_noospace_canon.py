"""Regression guard for issue #119: canonical Noöspace ontology."""

from pathlib import Path

RULEBOOK = Path(__file__).resolve().parents[1] / "RULEBOOK.md"


def test_issue119_noospace_canon_survives():
    text = RULEBOOK.read_text(encoding="utf-8")

    required = [
        "Noöspace is real.",
        "infinite-dimensional",
        "quantum-information Hilbert space",
        "Astral Plane",
        "Conscious Agent Network",
        "Noöspace is the domain; the Noösphere is an emergent",
        "Time/Space",
        "Self-Transforming Machine Elves",
        "The deeper Noöspace becomes, the less reliable human categories become.",
        "interdimensional Zones",
        "mode of manifestation, not ultimate species identity",
    ]
    for phrase in required:
        assert phrase in text, f"Missing issue #119 canon phrase: {phrase}"


def test_issue119_retires_old_astral_partial_mapping():
    text = RULEBOOK.read_text(encoding="utf-8")
    assert "The astral is **not identical with all of time/space**" not in text
