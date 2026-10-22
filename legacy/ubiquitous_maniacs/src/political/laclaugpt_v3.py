"""LaclauGPT v3 — The Noetic Hegemony and Archetypal Discourse Engine.

A multimodal discourse analysis engine that combines Laclau/Mouffe, Castells,
LLM Structuralism, the Platonic Representation Hypothesis, Jungian archetypes,
Tarot as a symbolic interface, and the Faggin/Hoffman Conscious Agent Network,
with selected elements from Luhmann, Deleuze & Guattari, and Latour.

The full theoretical stack, the 11-phase workflow, the 13-section output format,
the 10-card hegemonic Tarot spread, the 6 graph representations, the 3 epistemic
modes and the 20 behavioural rules live in ``laclaugpt_v3_prompts.py`` (the
``SYSTEM_PROMPT``); this module is the engine that drives it.

Multimodality is OPTIONAL. By default the engine analyses text only. Pass
``images`` (file paths / raw bytes / base64 strings) and/or ``video`` (a file
path, cv2-gated) to ``analyze()`` to include visual data; when real images are
present the engine switches to a vision model. ``frame_descriptions`` adds text
descriptions of frames without invoking a vision model.

Dependencies (all import-gated — the module imports successfully with none
installed and only raises a clear ``RuntimeError`` when ``analyze()`` is called
without them):

    - ollama:  required for LLM analysis (``analyze()``)
    - pydantic: required for structured output models
    - opencv-python (cv2): OPTIONAL, required only for ``video=`` frame
      extraction. The text and still-image paths do not need it.

Install with::

    pip install -r requirements-llm.txt
    pip install opencv-python   # only if you analyse video

Usage::

    from src.political.laclaugpt_v3 import LaclauGPT

    agent = LaclauGPT()                       # text-only by default
    result = agent.analyze(text="Your discourse text here")
    print(result.analysis)                    # full 13-section markdown
    print(result.oracle_sentence)
    for card in result.tarot_cards:           # the 10-card hegemonic spread
        print(card.card_number, card.card_name)

    # Multimodal (images -> vision model; text-only otherwise):
    result = agent.analyze(text="Transcript", images=["/path/to/frame.jpg"])
"""

from __future__ import annotations

import base64
import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from src.political.laclaugpt_v3_prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

# ── Optional dependencies (import-gated) ──────────────────────────────
# Importing this module must NEVER fail when these are absent.

try:
    from pydantic import BaseModel, Field, ValidationError
    _HAS_PYDANTIC = True
except ImportError:  # pragma: no cover - exercised via monkeypatch in tests
    BaseModel = None  # type: ignore[assignment]
    Field = None  # type: ignore[assignment]
    ValidationError = None  # type: ignore[assignment]
    _HAS_PYDANTIC = False

try:
    import ollama as _ollama_pkg  # noqa: F401
    _HAS_OLLAMA = True
except ImportError:  # pragma: no cover - exercised via monkeypatch in tests
    _ollama_pkg = None  # type: ignore[assignment]
    _HAS_OLLAMA = False

try:
    import cv2  # noqa: F401
    _HAS_CV2 = True
except ImportError:  # pragma: no cover - exercised via monkeypatch in tests
    cv2 = None  # type: ignore[assignment]
    _HAS_CV2 = False


_MISSING_DEPS_MESSAGE = (
    "LaclauGPT v3 needs ollama+pydantic (optional): "
    "pip install -r requirements-llm.txt"
)

_MISSING_CV2_MESSAGE = (
    "LaclauGPT v3 video frame extraction needs opencv-python (optional): "
    "pip install opencv-python"
)


# ── Pydantic output models (defined if pydantic available) ─────────────

if _HAS_PYDANTIC:

    class TarotCard(BaseModel):
        """A single Tarot card from the analysis (Layer 7 / Phase 7-8).

        Carries all fourteen fields the spec requires: number, name, visual
        scene, central symbols, archetypal structure, associated signifiers,
        upright/reversed interpretation, affective charge, subject position,
        political function, network function, shadow card, confidence score,
        and representation-stability estimate.
        """
        card_number: int = 0
        card_name: str = ""
        visual_scene: str = ""
        central_symbols: list[str] = Field(default_factory=list)
        archetypal_structure: str = ""
        associated_signifiers: list[str] = Field(default_factory=list)
        upright_interpretation: str = ""
        reversed_interpretation: str = ""
        affective_charge: str = ""
        subject_position: str = ""
        political_function: str = ""
        network_function: str = ""
        shadow_card: str = ""
        confidence_score: float = 0.5
        representation_stability: str = "unstable"

    class ArchetypalAttractor(BaseModel):
        """An archetypal pattern detected in the discourse (Phase 5)."""
        name: str = ""
        evidence: str = ""
        relational_form: str = ""
        desire: str = ""
        lack: str = ""
        fear: str = ""
        transformation: str = ""
        shadow: str = ""
        political_articulation: str = ""
        confidence: float = 0.5

    class GraphNode(BaseModel):
        id: str = ""
        label: str = ""
        kind: str = ""

    class GraphEdge(BaseModel):
        source: str = ""
        target: str = ""
        relation: str = ""
        label: str = ""

    class GraphRepresentation(BaseModel):
        """One of the six analytical graphs (Section V of the spec).

        ``kind`` is one of: agent, systems, actor_network, signifier,
        hegemony, communication.
        """
        kind: str = ""
        nodes: list[GraphNode] = Field(default_factory=list)
        edges: list[GraphEdge] = Field(default_factory=list)
        notes: str = ""

    class LaclauGPTResult(BaseModel):
        """Structured result of a LaclauGPT v3 analysis.

        ``analysis`` holds the full 13-section markdown document the model
        produces; the remaining fields are the machine-readable extractions
        (Tarot spread, archetypes, the six graphs, Laclaudian signifiers,
        counter-hegemonic reading, epistemic modes, Oracle sentence). All
        fields except ``analysis`` are optional so the JSON schema stays
        permissive — the model is unlikely to fail validation, and a
        ``ValidationError`` triggers a graceful free-text fallback.
        """
        analysis: str
        oracle_sentence: str = ""
        tarot_cards: list[TarotCard] = Field(default_factory=list)
        archetypes: list[ArchetypalAttractor] = Field(default_factory=list)
        graphs: list[GraphRepresentation] = Field(default_factory=list)
        nodal_points: list[str] = Field(default_factory=list)
        empty_signifiers: list[str] = Field(default_factory=list)
        floating_signifiers: list[str] = Field(default_factory=list)
        chains_of_equivalence: list[str] = Field(default_factory=list)
        antagonisms: list[str] = Field(default_factory=list)
        subject_positions: list[str] = Field(default_factory=list)
        counter_hegemonic_articulation: str = ""
        epistemic_modes: list[str] = Field(default_factory=list)
        model: str = ""
        multimodal: bool = False
        raw_response: str = ""

else:
    TarotCard = None  # type: ignore[assignment]
    ArchetypalAttractor = None  # type: ignore[assignment]
    GraphNode = None  # type: ignore[assignment]
    GraphEdge = None  # type: ignore[assignment]
    GraphRepresentation = None  # type: ignore[assignment]
    LaclauGPTResult = None  # type: ignore[assignment]


# ── Ollama options (aligned with populism_analysis.py / puhti) ─────────

OLLAMA_OPTIONS = {
    "repeat_last_n": 64,
    "repeat_penalty": 1.1,
    "num_ctx": int(os.environ.get("OLLAMA_LACLAUGPT_NUM_CTX", "25000")),
    "top_p": 0.9,
    "top_k": 40,
    "min_p": 0.0,
    "temperature": float(os.environ.get("OLLAMA_LACLAUGPT_TEMPERATURE", "0.6")),
    "num_predict": int(os.environ.get("OLLAMA_LACLAUGPT_NUM_PREDICT", "4096")),
}

DEFAULT_MODEL = os.environ.get("OLLAMA_LACLAUGPT_MODEL", "gemma3:27b")
DEFAULT_VISION_MODEL = os.environ.get("OLLAMA_LACLAUGPT_VISION_MODEL", "llama3.2-vision:11b")
DEFAULT_HOST = os.environ.get("OLLAMA_LACLAUGPT_HOST", "http://localhost:11434")

# The six analytical graph kinds the engine/models recognise.
GRAPH_KINDS = ("agent", "systems", "actor_network", "signifier", "hegemony", "communication")


def _ensure_deps() -> None:
    if not (_HAS_PYDANTIC and _HAS_OLLAMA):
        raise RuntimeError(_MISSING_DEPS_MESSAGE)


def _make_client(host: str | None = None) -> Any:
    from ollama import Client  # imported lazily so absence doesn't break import
    return Client(host=host or DEFAULT_HOST)


# ── Multimodal helpers ─────────────────────────────────────────────────

def _normalize_image(item: Any) -> bytes:
    """Normalize a single image input to base64-encoded bytes for Ollama.

    Accepts:
      * ``str`` / ``pathlib.Path`` file path  -> read raw bytes, base64-encode
      * ``bytes`` / ``bytearray`` raw image   -> base64-encode
      * ``str`` already-base64 string         -> encode to ASCII bytes

    Returns base64-encoded bytes (the form ``ollama.chat(images=...)`` expects,
    matching ``puhti_frame.py``). No PIL dependency.
    """
    if isinstance(item, (bytes, bytearray)):
        return base64.b64encode(bytes(item))
    if isinstance(item, Path):
        return base64.b64encode(item.read_bytes())
    if isinstance(item, str):
        if os.path.exists(item):
            return base64.b64encode(Path(item).read_bytes())
        # Assume already base64-encoded.
        return item.encode("ascii")
    raise TypeError(
        f"Unsupported image input type {type(item).__name__}; "
        "expected a file path (str/Path), raw bytes, or a base64 string."
    )


def _extract_keyframes(
    video_path: str | Path,
    *,
    interval_s: int = 30,
    max_frames: int = 6,
    cap_duration_s: int = 180,
) -> list[bytes]:
    """Extract up to ``max_frames`` keyframes from a video as base64 bytes.

    Mirrors ``LaclauGPT-Multimodal-Analysis/puhti_preprocess.py``: one frame
    every ``interval_s`` seconds, capped at ``cap_duration_s`` seconds total,
    JPEG-encoded and base64-encoded. Requires ``cv2`` (opencv-python).
    """
    if not _HAS_CV2:
        raise RuntimeError(_MISSING_CV2_MESSAGE)
    video = cv2.VideoCapture(str(video_path))  # type: ignore[union-attr]
    if not video.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    try:
        fps = video.get(cv2.CAP_PROP_FPS) or 25.0  # type: ignore[union-attr]
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)  # type: ignore[union-attr]
        duration = int((frame_count / fps) if frame_count > 0 else 0)
        if duration <= 0:
            duration = cap_duration_s
        duration = min(duration, cap_duration_s)

        frames: list[bytes] = []
        for frame_time in range(0, duration, max(interval_s, 1)):
            if len(frames) >= max_frames:
                break
            video.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)  # type: ignore[union-attr]
            ok, frame = video.read()
            if not ok or frame is None:
                continue
            ok, buf = cv2.imencode(".jpg", frame)  # type: ignore[union-attr]
            if not ok:
                continue
            frames.append(base64.b64encode(buf.tobytes()))
        return frames
    finally:
        video.release()


# ── Engine ──────────────────────────────────────────────────────────────

class LaclauGPT:
    """LaclauGPT v3 discourse analysis engine.

    Args:
        model: text Ollama model (default: ``OLLAMA_LACLAUGPT_MODEL`` env or
            ``gemma3:27b``). Used for text-only and frame-description runs.
        vision_model: vision Ollama model (default: ``OLLAMA_LACLAUGPT_VISION_MODEL``
            env or ``llama3.2-vision:11b``). Used only when real ``images`` are
            supplied to ``analyze()``.
        host: Ollama host URL (default: ``OLLAMA_LACLAUGPT_HOST`` env or
            ``http://localhost:11434``).
        num_ctx: context window (default: ``OLLAMA_LACLAUGPT_NUM_CTX`` or 25000).
        num_predict: max tokens (default: ``OLLAMA_LACLAUGPT_NUM_PREDICT`` or 4096).
        temperature: sampling temperature (default: ``OLLAMA_LACLAUGPT_TEMPERATURE``
            or 0.6 — warmer than the populism lens's 0.0 because this is an
            interpretive/oracular engine, but still disciplined).

    Raises:
        RuntimeError: if ``ollama``/``pydantic`` are not installed and
            ``analyze()`` is called. The module imports fine without them.
    """

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
        num_ctx: int | None = None,
        num_predict: int | None = None,
        vision_model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        self.model = model if model is not None else os.environ.get(
            "OLLAMA_LACLAUGPT_MODEL", "gemma3:27b")
        self.vision_model = vision_model if vision_model is not None else os.environ.get(
            "OLLAMA_LACLAUGPT_VISION_MODEL", "llama3.2-vision:11b")
        self.host = host or os.environ.get(
            "OLLAMA_LACLAUGPT_HOST", "http://localhost:11434")
        self.num_ctx = num_ctx if num_ctx is not None else int(
            os.environ.get("OLLAMA_LACLAUGPT_NUM_CTX", "25000"))
        self.num_predict = num_predict if num_predict is not None else int(
            os.environ.get("OLLAMA_LACLAUGPT_NUM_PREDICT", "4096"))
        self.temperature = temperature if temperature is not None else float(
            os.environ.get("OLLAMA_LACLAUGPT_TEMPERATURE", "0.6"))
        self._client: Any = None

    def _get_client(self) -> Any:
        """Lazy-init an Ollama client (injectable via ``analyze(client=…)``)."""
        if self._client is not None:
            return self._client
        _ensure_deps()
        self._client = _make_client(self.host)
        logger.info("Ollama client initialized: %s", self.host)
        return self._client

    def analyze(
        self,
        text: str,
        *,
        frame_descriptions: str | None = None,
        images: list[Any] | None = None,
        video: str | Path | None = None,
        model: str | None = None,
        client: Any | None = None,
        **kwargs: Any,
    ) -> "LaclauGPTResult":
        """Analyse discourse using the full LaclauGPT v3 workflow.

        Args:
            text: the text to analyse (transcript, dialogue, manifesto, ...).
            frame_descriptions: optional text descriptions of video frames or
                images. Adds a multimodal section to the prompt without
                invoking a vision model.
            images: optional list of image inputs (file paths / raw bytes /
                base64 strings / ``Path``). When non-empty, the engine
                base64-encodes them, attaches them to the user message, and
                switches to ``vision_model``.
            video: optional video file path. When supplied (and ``images`` is
                not), up to six keyframes are extracted via cv2 and treated as
                ``images``. Requires opencv-python.
            model: override the text model for this call.
            client: inject an Ollama client (for tests; never required live).

        Returns:
            A validated ``LaclauGPTResult`` (full 13-section ``analysis`` plus
            structured tarot cards / archetypes / graphs / signifiers / oracle).
            On a ``ValidationError`` (model produced imperfect JSON on a GPU
            run), degrades gracefully to a free-text fallback so the call never
            hard-fails.

        Raises:
            RuntimeError: if ``ollama``/``pydantic`` are not installed (or cv2
                is absent when ``video=`` is given).
            ValueError: if ``text`` is empty/whitespace.
        """
        _ensure_deps()
        if not text or not text.strip():
            raise ValueError("analyze requires non-empty text")

        # Resolve visual inputs.
        if video is not None and not images:
            images = _extract_keyframes(video, **{
                k: v for k, v in kwargs.items()
                if k in {"interval_s", "max_frames", "cap_duration_s"}
            })
        images_b64 = [_normalize_image(x) for x in (images or [])]

        multimodal = bool(images_b64 or frame_descriptions)
        # Vision model only when real images are present; text-only and
        # frame-description runs stay on the (cheaper) text model.
        active_model = self.vision_model if images_b64 else (model or self.model)

        user_prompt = build_user_prompt(text, multimodal_description=frame_descriptions)

        logger.info(
            "LaclauGPT v3 analyzing %d chars (multimodal=%s, model=%s)",
            len(text), multimodal, active_model,
        )

        options = dict(OLLAMA_OPTIONS)
        options["num_ctx"] = kwargs.get("num_ctx", self.num_ctx)
        options["num_predict"] = kwargs.get("num_predict", self.num_predict)
        options["temperature"] = kwargs.get("temperature", self.temperature)

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        if images_b64:
            messages[1]["images"] = images_b64

        active_client = client if client is not None else self._get_client()
        response = active_client.chat(
            model=active_model,
            messages=messages,
            options=options,
            keep_alive="30m",
            format=LaclauGPTResult.model_json_schema(),  # type: ignore[union-attr]
            stream=False,
        )
        content = response["message"]["content"]

        result = _parse_result(content)
        # Stamp provenance fields.
        result.model = active_model
        result.multimodal = multimodal
        result.raw_response = content
        return result

    def analyze_text(self, text: str, **kwargs: Any) -> str:
        """Simplified text-only analysis. Returns the full markdown ``analysis``."""
        return self.analyze(text, **kwargs).analysis


# ── Result parsing ──────────────────────────────────────────────────────

def _parse_result(content: str) -> "LaclauGPTResult":
    """Parse model output into a ``LaclauGPTResult`` with a graceful fallback.

    Primary path: ``model_validate_json`` against the structured schema. If the
    model produced imperfect JSON (common on long creative GPU runs), fall back
    to a result built from the raw text via the regex extractors — the call
    never hard-fails and the ``analysis`` markdown is always preserved.
    """
    _ensure_deps()
    try:
        return LaclauGPTResult.model_validate_json(content)  # type: ignore[union-attr]
    except (ValidationError, ValueError, TypeError):
        logger.warning("LaclauGPT v3: structured parse failed; using free-text fallback")
        return LaclauGPTResult(  # type: ignore[call-arg]
            analysis=content,
            oracle_sentence=_extract_oracle_sentence(content),
            tarot_cards=[_dict_to_tarotcard(c) for c in _extract_tarot_cards(content)],
            archetypes=[_dict_to_attractor(a) for a in _extract_archetypes(content)],
        )


def _dict_to_tarotcard(card: dict[str, Any]) -> "TarotCard":
    """Coerce a fallback-extracted card dict into a ``TarotCard``."""
    return TarotCard(  # type: ignore[call-arg]
        card_number=int(card.get("card_number", 0) or 0),
        card_name=str(card.get("card_name", ""))[:100],
    )


def _dict_to_attractor(arch: dict[str, Any]) -> "ArchetypalAttractor":
    """Coerce a fallback-extracted archetype dict into an ``ArchetypalAttractor``."""
    return ArchetypalAttractor(name=str(arch.get("name", ""))[:100])  # type: ignore[call-arg]


def result_to_text(result: "LaclauGPTResult") -> str:
    """Render a ``LaclauGPTResult`` to a compact human-readable text form."""
    lines: list[str] = [result.analysis, ""]
    if result.oracle_sentence:
        lines += ["— Oracle —", result.oracle_sentence, ""]
    if result.tarot_cards:
        lines.append("— Tarot spread —")
        for c in result.tarot_cards:
            lines.append(f"{c.card_number}. {c.card_name}  [{c.affective_charge}]")
        lines.append("")
    if result.archetypes:
        lines.append("— Archetypal attractors —")
        for a in result.archetypes:
            lines.append(f"* {a.name}  (confidence {a.confidence})")
        lines.append("")
    if result.counter_hegemonic_articulation:
        lines += ["— Counter-hegemonic articulation —", result.counter_hegemonic_articulation]
    return "\n".join(lines).strip()


def result_to_dict(result: "LaclauGPTResult") -> dict[str, Any]:
    """Serialize a ``LaclauGPTResult`` to a plain dict (for save/JSON output)."""
    return {
        "analysis": result.analysis,
        "oracle_sentence": result.oracle_sentence,
        "tarot_cards": [c.model_dump() for c in result.tarot_cards],
        "archetypes": [a.model_dump() for a in result.archetypes],
        "graphs": [g.model_dump() for g in result.graphs],
        "nodal_points": list(result.nodal_points),
        "empty_signifiers": list(result.empty_signifiers),
        "floating_signifiers": list(result.floating_signifiers),
        "chains_of_equivalence": list(result.chains_of_equivalence),
        "antagonisms": list(result.antagonisms),
        "subject_positions": list(result.subject_positions),
        "counter_hegemonic_articulation": result.counter_hegemonic_articulation,
        "epistemic_modes": list(result.epistemic_modes),
        "model": result.model,
        "multimodal": result.multimodal,
    }


def parse_result_json(content: str) -> "LaclauGPTResult":
    """Parse a raw JSON string into a ``LaclauGPTResult`` (test/offline helper).

    Requires pydantic. Does NOT invoke the free-text fallback — raises on
    invalid JSON so tests can assert schema behaviour directly.
    """
    _ensure_deps()
    return LaclauGPTResult.model_validate_json(content)  # type: ignore[union-attr]


# ── Free-text fallback extractors (used only on ValidationError) ───────

def _extract_oracle_sentence(text: str) -> str:
    """Extract the Oracle sentence from the analysis output."""
    markers = ["## 13. Oracle sentence", "## 13.", "Oracle sentence:", "Oracle:"]
    for marker in markers:
        idx = text.lower().find(marker.lower())
        if idx >= 0:
            after = text[idx + len(marker):].strip()
            for line in after.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    return ""


def _extract_tarot_cards(text: str) -> list[dict[str, Any]]:
    """Attempt to extract Tarot card entries from the analysis text."""
    cards: list[dict[str, Any]] = []
    pattern = r'(?:Card|Kortti)\s*\d+[:\—\-]\s*(.+)'
    for i, m in enumerate(re.finditer(pattern, text, re.IGNORECASE), 1):
        start = m.start()
        chunk = text[start:start + 500]
        cards.append({
            "card_number": i,
            "card_name": m.group(1).strip()[:100],
            "raw_chunk": chunk[:200],
        })
    return cards


def _extract_archetypes(text: str) -> list[dict[str, Any]]:
    """Attempt to extract archetypal attractor entries from the analysis text."""
    archetypes: list[dict[str, Any]] = []
    pattern = r'(?:Archetype|Arkkityyppi)[:\—\-]\s*(.+)'
    for m in re.finditer(pattern, text, re.IGNORECASE):
        archetypes.append({"name": m.group(1).strip()[:100]})
    return archetypes