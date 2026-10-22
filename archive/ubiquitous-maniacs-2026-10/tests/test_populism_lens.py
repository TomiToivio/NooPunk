from __future__ import annotations

import json
import sys
import types

import pytest

from src.rpg.factions import Faction, FactionProject, analyze_faction


# ── Module imports cleanly without ollama/pydantic (import-gate) ─────────


def test_module_imports_without_dependencies() -> None:
    """src.political.populism_analysis must import even if ollama is absent."""
    # Force a clean import with ollama missing from sys.modules.
    sys.modules.pop("ollama", None)
    mod = types.ModuleType("_probe")
    import importlib

    spec = importlib.util.find_spec("src.political.populism_analysis")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # The module object exists and exposes the prompt + gating flags.
    assert hasattr(module, "SYSTEM_PROMPT")
    assert hasattr(module, "HUNGARY_SYSTEM_PROMPT")
    assert hasattr(module, "analyze_discourse")


# ── analyze_discourse raises a clear RuntimeError when deps are missing ──


def test_analyze_discourse_raises_without_deps(monkeypatch) -> None:
    from src.political import populism_analysis as pa

    monkeypatch.setattr(pa, "_HAS_OLLAMA", False)
    monkeypatch.setattr(pa, "_HAS_PYDANTIC", False)
    with pytest.raises(RuntimeError, match="requirements-llm.txt"):
        pa.analyze_discourse("some discourse text")


def test_analyze_discourse_raises_with_only_ollama(monkeypatch) -> None:
    from src.political import populism_analysis as pa

    monkeypatch.setattr(pa, "_HAS_OLLAMA", True)
    monkeypatch.setattr(pa, "_HAS_PYDANTIC", False)
    with pytest.raises(RuntimeError, match="requirements-llm.txt"):
        pa.analyze_discourse("some discourse text")


def test_analyze_discourse_rejects_empty_text(monkeypatch) -> None:
    from src.political import populism_analysis as pa

    monkeypatch.setattr(pa, "_HAS_OLLAMA", True)
    monkeypatch.setattr(pa, "_HAS_PYDANTIC", True)
    # Even with deps "present", empty text is a client-side error before any call.
    with pytest.raises(ValueError):
        pa.analyze_discourse("   ")


# ── analyze_discourse parses a fake Ollama response into the Pydantic model ─
# This path needs pydantic installed; we skip gracefully if it is not, since the
# import-gate is the contract and this CI machine may not have pydantic.


@pytest.fixture
def fake_formula_payload() -> dict:
    return {
        "populism_analysis": "## Us vs Them\nThe faction constructs a people...",
        "populism_us": [
            {"populism_element": "economic justice", "populism_affect": "pride"},
            {"populism_element": "national identity", "populism_affect": "hope"},
        ],
        "populism_frontier": [
            {"populism_element": "eu elite", "populism_affect": "resentment"},
        ],
    }


class _FakeClient:
    def __init__(self, payload: dict):
        self._payload = payload
        self.calls = []

    def chat(self, **kwargs):
        self.calls.append(kwargs)
        return {"message": {"content": json.dumps(self._payload)}}


def test_analyze_discourse_parses_fake_response(monkeypatch, fake_formula_payload) -> None:
    pytest.importorskip("pydantic")
    from src.political import populism_analysis as pa

    monkeypatch.setattr(pa, "_HAS_OLLAMA", True)
    monkeypatch.setattr(pa, "_HAS_PYDANTIC", True)
    fake = _FakeClient(fake_formula_payload)
    formula = pa.analyze_discourse("We are the people; the elite have failed us.",
                                    client=fake, model="test-model")
    assert "Us vs Them" in formula.populism_analysis
    assert len(formula.populism_us) == 2
    assert formula.populism_us[0].populism_element == "economic justice"
    assert formula.populism_frontier[0].populism_affect == "resentment"
    # The fake client was called with the structured format schema.
    assert fake.calls and fake.calls[0]["model"] == "test-model"
    assert "format" in fake.calls[0]


def test_formula_to_text_and_dict_roundtrip(monkeypatch, fake_formula_payload) -> None:
    pytest.importorskip("pydantic")
    from src.political import populism_analysis as pa

    monkeypatch.setattr(pa, "_HAS_OLLAMA", True)
    monkeypatch.setattr(pa, "_HAS_PYDANTIC", True)
    fake = _FakeClient(fake_formula_payload)
    formula = pa.analyze_discourse("discourse", client=fake)
    text = pa.formula_to_text(formula)
    assert "economic justice^pride" in text
    assert "# Frontier" in text
    assert "eu elite^resentment" in text
    as_dict = pa.formula_to_dict(formula)
    assert as_dict["populism_us"][0]["populism_element"] == "economic justice"
    assert len(as_dict["populism_frontier"]) == 1


# ── Faction bridge ───────────────────────────────────────────────────────


def test_faction_discourse_renders_goals_relationships_projects() -> None:
    faction = Faction(
        id="watchers", name="The Watchers", goals=["observe humanity", "prevent escalation"],
        influence=4, resources=3, assets={"sigil", "mirror"},
        relationships={"architects": -2, "europol": 1},
        projects=[FactionProject(name="signal", goal=4, progress=2)],
    )
    text = faction.discourse()
    assert "Faction: The Watchers" in text
    assert "observe humanity" in text
    assert "architects (-2)" in text
    assert "europol (+1)" in text
    assert "signal (2/4)" in text
    assert "Assets: mirror, sigil" in text


def test_faction_discourse_handles_empty_faction() -> None:
    faction = Faction(id="x", name="X", goals=[])
    text = faction.discourse()
    assert "Faction: X" in text
    assert "Goals" not in text


def test_analyze_faction_uses_lens(monkeypatch, fake_formula_payload) -> None:
    pytest.importorskip("pydantic")
    from src.political import populism_analysis as pa

    monkeypatch.setattr(pa, "_HAS_OLLAMA", True)
    monkeypatch.setattr(pa, "_HAS_PYDANTIC", True)
    fake = _FakeClient(fake_formula_payload)
    faction = Faction(id="f", name="F", goals=["g1"], influence=1, resources=1)
    formula = analyze_faction(faction, client=fake, model="m")
    assert formula.populism_us[0].populism_element == "economic justice"
    # The user prompt sent to the fake client is the faction's discourse text.
    assert "Faction: F" in fake.calls[0]["messages"][1]["content"]


def test_analyze_faction_is_exposed() -> None:
    # analyze_faction is a free function on src.rpg.factions (and re-exported).
    from src.rpg.factions import analyze_faction as _af
    assert callable(_af)