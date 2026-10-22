"""Tests for LaclauGPT v3 — the Noetic Hegemony and Archetypal Discourse Engine.

Mirrors the fake-client + monkeypatch-flags + ``pytest.importorskip("pydantic")``
pattern of ``tests/test_populism_lens.py``. No live Ollama is ever required:
``_FakeClient.chat(**kwargs)`` returns a canned JSON payload.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from src.political.laclaugpt_v3_prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from src.political import laclaugpt_v3 as v3
from src.political.laclaugpt_v3 import (
    LaclauGPT,
    _extract_keyframes,
    _extract_oracle_sentence,
    _extract_tarot_cards,
    _normalize_image,
)


# ── Prompt tests ────────────────────────────────────────────────────────


def test_system_prompt_exists():
    assert len(SYSTEM_PROMPT) > 5000
    assert "LACLAUGPT v3" in SYSTEM_PROMPT
    assert "Laclau" in SYSTEM_PROMPT
    assert "Castells" in SYSTEM_PROMPT
    assert "Jung" in SYSTEM_PROMPT
    assert "Tarot" in SYSTEM_PROMPT
    assert "Hoffman" in SYSTEM_PROMPT
    assert "Faggin" in SYSTEM_PROMPT


def test_system_prompt_has_9_layers():
    for i in range(1, 10):
        assert f"Layer {i}" in SYSTEM_PROMPT


def test_system_prompt_has_11_phases():
    for i in range(1, 12):
        assert f"Phase {i}" in SYSTEM_PROMPT


def test_system_prompt_has_tarot_spread():
    assert "Card 1" in SYSTEM_PROMPT
    assert "Card 10" in SYSTEM_PROMPT
    assert "The Field" in SYSTEM_PROMPT
    assert "The World" in SYSTEM_PROMPT


def test_system_prompt_has_6_graphs_and_3_modes_and_20_rules():
    for name in ("Agent graph", "Systems graph", "Actor-network graph",
                 "Signifier graph", "Hegemony graph", "Communication network graph"):
        assert name in SYSTEM_PROMPT
    for mode in ("Empirical mode", "Interpretive mode", "Speculative or oracular mode"):
        assert mode in SYSTEM_PROMPT
    # Twenty behavioural rules, numbered 1..20.
    for i in range(1, 21):
        assert f"\n{i}. " in SYSTEM_PROMPT or f"\n{i}." in SYSTEM_PROMPT


def test_build_user_prompt_text_only():
    prompt = build_user_prompt("Test discourse text")
    assert "Test discourse text" in prompt
    assert "Multimodal data" not in prompt


def test_build_user_prompt_with_multimodal():
    prompt = build_user_prompt("Test text", multimodal_description="Frame 1: podium")
    assert "Test text" in prompt
    assert "Frame 1: podium" in prompt
    assert "Multimodal data" in prompt


# ── Engine initialization tests ─────────────────────────────────────────


def test_engine_defaults():
    agent = LaclauGPT()
    assert agent.model == "gemma3:27b"
    assert agent.vision_model == "llama3.2-vision:11b"
    assert agent.num_ctx == 25000
    assert agent.num_predict == 4096
    assert agent.temperature == 0.6


def test_engine_env_overrides():
    with patch.dict(os.environ, {
        "OLLAMA_LACLAUGPT_MODEL": "test-model",
        "OLLAMA_LACLAUGPT_VISION_MODEL": "test-vision",
        "OLLAMA_LACLAUGPT_NUM_CTX": "8000",
        "OLLAMA_LACLAUGPT_TEMPERATURE": "0.2",
    }):
        agent = LaclauGPT()
        assert agent.model == "test-model"
        assert agent.vision_model == "test-vision"
        assert agent.num_ctx == 8000
        assert agent.temperature == 0.2


def test_engine_custom_params():
    agent = LaclauGPT(model="custom:13b", num_ctx=12000, num_predict=2048,
                      vision_model="custom-vision:7b", temperature=0.3)
    assert agent.model == "custom:13b"
    assert agent.vision_model == "custom-vision:7b"
    assert agent.num_ctx == 12000
    assert agent.num_predict == 2048
    assert agent.temperature == 0.3


# ── Response parsing (free-text fallback helpers) ───────────────────────


def test_extract_oracle_sentence():
    text = ("## 12. Integrated synthesis\n...\n"
            "## 13. Oracle sentence\nThe shadow knows what the light forgets.")
    result = _extract_oracle_sentence(text)
    assert "shadow" in result.lower()


def test_extract_oracle_sentence_missing():
    text = "No oracle sentence here."
    assert _extract_oracle_sentence(text) == ""


def test_extract_tarot_cards():
    text = "Card 1: The Field — the general order\nCard 2: The Nodal Point — freedom"
    cards = _extract_tarot_cards(text)
    assert len(cards) >= 2
    assert "Field" in cards[0]["card_name"]


def test_extract_tarot_cards_empty():
    assert _extract_tarot_cards("No cards here") == []


# ── Image normalization ─────────────────────────────────────────────────


def test_normalize_image_from_bytes():
    out = _normalize_image(b"\xff\xd8\xff\xe0fakejpg")
    # base64 of the raw bytes
    import base64
    assert out == base64.b64encode(b"\xff\xd8\xff\xe0fakejpg")


def test_normalize_image_from_base64_string():
    out = _normalize_image("YWJjZA==")  # base64 of 'abcd'
    assert out == b"YWJjZA=="


def test_normalize_image_rejects_bad_type():
    with pytest.raises(TypeError):
        _normalize_image(12345)


# ── Fake-client analyze tests ───────────────────────────────────────────


class _FakeClient:
    """Fake Ollama client mirroring the .chat(**kwargs) contract."""

    def __init__(self, payload):
        self._payload = payload
        self.calls = []

    def chat(self, **kwargs):
        self.calls.append(kwargs)
        return {"message": {"content": json.dumps(self._payload)}}


@pytest.fixture
def fake_result_payload():
    return {
        "analysis": "## 1. Analytical orientation\nThe discourse constructs a people...",
        "oracle_sentence": "The shadow knows what the light forgets.",
        "tarot_cards": [
            {"card_number": 1, "card_name": "The Field", "affective_charge": "fear"},
            {"card_number": 2, "card_name": "The Nodal Point", "affective_charge": "hope"},
        ],
        "archetypes": [{"name": "The Network Sovereign", "confidence": 0.8}],
        "graphs": [{"kind": "hegemony", "nodes": [{"id": "n1", "label": "freedom"}],
                    "edges": [{"source": "n1", "target": "n2", "relation": "antagonism"}]}],
        "nodal_points": ["freedom"],
        "empty_signifiers": ["the people"],
        "floating_signifiers": ["security"],
        "chains_of_equivalence": ["freedom = sovereignty"],
        "antagonisms": ["the elite"],
        "subject_positions": ["the people"],
        "counter_hegemonic_articulation": "Detach 'security' from the frontier...",
        "epistemic_modes": ["empirical", "interpretive", "speculative"],
    }


def test_module_imports_without_dependencies():
    """The module must import even if ollama/pydantic/cv2 are absent.

    Setting a ``sys.modules`` entry to ``None`` makes ``import`` of that name
    raise ``ImportError`` (CPython guarantee), so this reliably simulates
    absence even when the packages are installed in the test env.
    """
    with patch.dict(sys.modules, {"ollama": None, "pydantic": None, "cv2": None}):
        sys.modules.pop("src.political.laclaugpt_v3", None)
        spec = importlib.util.find_spec("src.political.laclaugpt_v3")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, "LaclauGPT")
        assert hasattr(module.LaclauGPT, "analyze")
        assert hasattr(module, "result_to_dict")
        assert module._HAS_OLLAMA is False
        assert module._HAS_PYDANTIC is False
        assert module._HAS_CV2 is False
        assert module.LaclauGPTResult is None
        assert module.TarotCard is None


def test_analyze_raises_without_deps(monkeypatch):
    monkeypatch.setattr(v3, "_HAS_OLLAMA", False)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", False)
    with pytest.raises(RuntimeError, match="requirements-llm.txt"):
        LaclauGPT().analyze("some text")


def test_analyze_raises_without_cv2_for_video(monkeypatch):
    monkeypatch.setattr(v3, "_HAS_CV2", False)
    with pytest.raises(RuntimeError, match="opencv-python"):
        LaclauGPT().analyze("some text", video="x.mp4")


def test_analyze_rejects_empty_text(monkeypatch):
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    with pytest.raises(ValueError):
        LaclauGPT().analyze("   ", client=_FakeClient({}))


def test_analyze_text_only_returns_result(monkeypatch, fake_result_payload):
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    fake = _FakeClient(fake_result_payload)

    result = LaclauGPT(model="text:model").analyze("Test discourse", client=fake)

    assert result.oracle_sentence == "The shadow knows what the light forgets."
    assert result.tarot_cards[0].card_name == "The Field"
    assert result.tarot_cards[0].affective_charge == "fear"
    assert len(result.tarot_cards) == 2
    assert result.archetypes[0].name == "The Network Sovereign"
    assert result.graphs[0].kind == "hegemony"
    assert result.counter_hegemonic_articulation.startswith("Detach")
    assert "speculative" in result.epistemic_modes
    assert result.multimodal is False
    assert result.model == "text:model"
    # Text-only: no images on the user message, structured format requested.
    assert "images" not in fake.calls[0]["messages"][1]
    assert "format" in fake.calls[0]
    assert fake.calls[0]["model"] == "text:model"
    assert fake.calls[0]["keep_alive"] == "30m"
    assert fake.calls[0]["stream"] is False


def test_analyze_with_images_passes_images_and_uses_vision_model(monkeypatch, fake_result_payload):
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    fake = _FakeClient(fake_result_payload)

    result = LaclauGPT(model="text:model", vision_model="vision:model").analyze(
        "Transcript text", images=[b"\xff\xd8fakejpg"], client=fake,
    )

    assert result.multimodal is True
    assert result.model == "vision:model"
    user_msg = fake.calls[0]["messages"][1]
    assert "images" in user_msg
    assert len(user_msg["images"]) == 1
    assert fake.calls[0]["model"] == "vision:model"


def test_analyze_with_frame_descriptions_only(monkeypatch, fake_result_payload):
    """frame_descriptions alone -> multimodal flag True, but text model (no images)."""
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    fake = _FakeClient(fake_result_payload)

    result = LaclauGPT(model="text:model").analyze(
        "Transcript", frame_descriptions="Frame 1: Politician at podium", client=fake,
    )

    assert result.multimodal is True
    assert result.model == "text:model"
    assert "images" not in fake.calls[0]["messages"][1]
    assert "Frame 1" in fake.calls[0]["messages"][1]["content"]


def test_analyze_video_extracts_frames(monkeypatch, fake_result_payload):
    """video= path flows through _extract_keyframes into the images field."""
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    fake_frames = [b"\xff\xd8frameA", b"\xff\xd8frameB"]
    monkeypatch.setattr(v3, "_extract_keyframes", lambda *a, **k: fake_frames)
    fake = _FakeClient(fake_result_payload)

    result = LaclauGPT(vision_model="vision:model").analyze(
        "Transcript", video="/tmp/x.mp4", client=fake,
    )

    assert result.multimodal is True
    assert result.model == "vision:model"
    user_msg = fake.calls[0]["messages"][1]
    assert len(user_msg["images"]) == 2


def test_analyze_fallback_on_invalid_json(monkeypatch):
    """When the model returns non-JSON, the engine degrades to free-text fallback."""
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)

    class _RawClient:
        def __init__(self):
            self.calls = []

        def chat(self, **kwargs):
            self.calls.append(kwargs)
            return {"message": {"content": (
                "## 1. Analytical orientation\nA long markdown analysis...\n"
                "Card 1: The Field — the general order\n"
                "## 13. Oracle sentence\nThe shadow knows what the light forgets."
            )}}

    raw = _RawClient()
    result = LaclauGPT(model="text:model").analyze("Some discourse", client=raw)

    assert result.analysis.startswith("## 1. Analytical orientation")
    assert result.oracle_sentence == "The shadow knows what the light forgets."
    assert len(result.tarot_cards) >= 1
    assert "The Field" in result.tarot_cards[0].card_name
    assert result.multimodal is False
    # Structured format was still requested even though the model ignored it.
    assert "format" in raw.calls[0]


def test_analyze_text_method(monkeypatch, fake_result_payload):
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    fake = _FakeClient(fake_result_payload)
    text = LaclauGPT().analyze_text("Some text", client=fake)
    assert "Analytical orientation" in text


# ── Schema richness ─────────────────────────────────────────────────────


def test_schema_is_rich():
    pytest.importorskip("pydantic")
    from src.political.laclaugpt_v3 import LaclauGPTResult
    schema = LaclauGPTResult.model_json_schema()
    props = set(schema.get("properties", {}).keys())
    for field in ("analysis", "oracle_sentence", "tarot_cards", "archetypes",
                  "graphs", "nodal_points", "empty_signifiers", "floating_signifiers",
                  "chains_of_equivalence", "antagonisms", "subject_positions",
                  "counter_hegemonic_articulation", "epistemic_modes"):
        assert field in props, f"schema missing {field}"
    # Only `analysis` is required.
    assert schema.get("required") == ["analysis"]


# ── Serialization helpers ───────────────────────────────────────────────


def test_result_to_dict_and_text(monkeypatch, fake_result_payload):
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    fake = _FakeClient(fake_result_payload)
    result = LaclauGPT(model="text:model").analyze("Discourse", client=fake)

    from src.political.laclaugpt_v3 import result_to_dict, result_to_text
    d = result_to_dict(result)
    assert d["oracle_sentence"].startswith("The shadow")
    assert d["tarot_cards"][0]["card_name"] == "The Field"
    assert d["model"] == "text:model"
    assert d["multimodal"] is False

    t = result_to_text(result)
    assert "Oracle" in t
    assert "Tarot spread" in t
    assert "The Field" in t


# ── Faction bridge ──────────────────────────────────────────────────────


def test_analyze_faction_v3_uses_engine(monkeypatch, fake_result_payload):
    pytest.importorskip("pydantic")
    monkeypatch.setattr(v3, "_HAS_OLLAMA", True)
    monkeypatch.setattr(v3, "_HAS_PYDANTIC", True)
    monkeypatch.setattr(v3, "_HAS_CV2", True)
    from src.rpg.factions import Faction, analyze_faction_v3

    faction = Faction(
        id="the_watchers", name="The Watchers",
        goals=["Observe without intervening", "Allow gradual contact"],
        influence=3, resources=2,
        assets={"interdimensional_presence"},
        relationships={"the_architects": -2},
    )
    fake = _FakeClient(fake_result_payload)
    result = analyze_faction_v3(faction, client=fake, model="text:model")

    # The faction's discourse() text is sent as the user message.
    assert "Faction: The Watchers" in fake.calls[0]["messages"][1]["content"]
    assert result.tarot_cards[0].card_name == "The Field"
    assert result.model == "text:model"