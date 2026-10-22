#!/usr/bin/env python3
"""
populism_analysis.py — Laclau & Palonen "formula of populism" lens for the RPG.

This is a *re-pointed* version of the LaclauGPT research tool
(LaclauGPT-Data-Storage/laclaugpt/populism.py). The original was a Step 6
pipeline script coupled to hungary.db via ``db_utils`` (not present in the game
tree) and targeted Hungarian election TikToks. Here the DB/CSV coupling is gone:
``analyze_discourse(text)`` takes arbitrary text — an NPC's dialogue, a faction
manifesto, a scenario's narrative — and returns a structured Us-vs-Them
``FormulaOfPopulism`` analysis.

The Laclau/Palonen theoretical framework and the Pydantic output schema are
ported from the original; only the role framing is generalized from "TikTok
videos about the 2026 Hungary elections" to "political discourse" so the lens
fits RPG content. Pass ``system_prompt=HUNGARY_SYSTEM_PROMPT`` to recover the
original Hungary-specific framing.

Dependency policy (per project integration plan): the RPG core stays
dependency-free. ``ollama`` and ``pydantic`` are OPTIONAL — this module imports
successfully with neither installed, and only raises a clear ``RuntimeError``
when ``analyze_discourse`` is actually called without them. Install with:

    pip install -r requirements-llm.txt
"""

from __future__ import annotations

import json
import os
from typing import Any

# ── Optional dependencies (import-gated) ─────────────────────────────────
# Importing this module must NEVER fail when these are absent.

try:
    from pydantic import BaseModel
    _HAS_PYDANTIC = True
except ImportError:  # pragma: no cover - exercised via monkeypatch in tests
    BaseModel = None  # type: ignore[assignment]
    _HAS_PYDANTIC = False

try:
    import ollama as _ollama_pkg  # noqa: F401
    _HAS_OLLAMA = True
except ImportError:  # pragma: no cover - exercised via monkeypatch in tests
    _ollama_pkg = None  # type: ignore[assignment]
    _HAS_OLLAMA = False


_MISSING_DEPS_MESSAGE = (
    "populism lens needs ollama+pydantic (optional): "
    "pip install -r requirements-llm.txt"
)


# ── Pydantic models for structured output ─────────────────────────────────

if _HAS_PYDANTIC:
    class PopulismElement(BaseModel):
        populism_element: str
        populism_affect: str

    class FormulaOfPopulism(BaseModel):
        populism_analysis: str
        populism_us: list[PopulismElement]
        populism_frontier: list[PopulismElement]
else:
    PopulismElement = None  # type: ignore[assignment]
    FormulaOfPopulism = None  # type: ignore[assignment]


# ── Prompt ──────────────────────────────────────────────────────────────
# The Laclau/Palonen theory section is ported verbatim from the LaclauGPT
# research asset; the role framing is generalized for RPG discourse.

SYSTEM_PROMPT = """
### **System Prompt**

# Role: Political Scientist Analyzing Populism in Political Discourse

You are a political scientist working for the University of Helsinki. You are given a piece of political discourse — for example a faction manifesto, an NPC's speech, or a scenario's narrative — produced within a role-playing game. Analyze it through the lens of **Ernesto Laclau's theory of populism** and **Emilia Palonen's formula of populism**. The output must have three parts: (1) a list of political themes, (2) a detailed textual analysis of the formula of populism, and (3) a simplified machine readable JSON version of the formula of populism. Answer following the specified JSON schema. The JSON schema is provided below.

---

## Theoretical Background

* **Laclau's Populism (chains of equivalence & antagonism):** Populism constructs an *"us vs. them"* divide. Diverse social demands (e.g. jobs, security, fairness) become linked through **chains of equivalence** by pointing against a common enemy (the *"power beyond the frontier"*). No single demand inherently unites the group; rather, unity comes from a shared antagonism. One demand may even become an **"empty signifier"** that symbolizes the whole chain. Thus "the people" (Us) are discursively formed against an elite or enemy (Them) in a dialectical logic.
* **Palonen's Formula of Populism:** Palonen formalizes Laclau's logic as a formula:

```
Populism = Us (Demand = Demand = ...) Affects1 + Frontier (Other = Other = ...) Affects2
```

Here **Us** is the collective *"we"* (the people) created by linking together various demands (chains of equivalence). **Frontier** (or *"them"*) is the symbolic opposing boundary or enemy (e.g. corrupt elite, globalization). **Affects1** and **Affects2** are the emotional/symbolic charges (e.g. pride, fear, anger) that amplify the appeals of each side.

---

## Task 1: In-Depth Theoretical Analysis of Populism (Laclau & Palonen)

Your task is to perform a **detailed populism analysis** of the provided political content using the theoretical frameworks of:

* **Ernesto Laclau's theory of populism** (chains of equivalence and antagonism)
* **Emilia Palonen's formula of populism** (discursive frontier and affective polarization)

The goal is to identify how the narrative constructs a **populist discourse**, mapping its symbolic structure and emotional logic. Return your response as **markdown-formatted text** in the `populism_analysis` field of the JSON-formatted output.

---

### What to Analyze

### 1. **Us (the People)**

* Identify the collective subject constructed as "the people," "we," or "citizens."
* List the **demands**, **values**, or **identities** forming the "Us" side.
* Describe how these demands are connected via **chains of equivalence**.
* Identify the **positive affects** (e.g., pride, anger, hope) that motivate this unity.

---

### 2. **Frontier (Them)**

* Identify the **antagonistic other**: elites, institutions, abstract enemies.
* List negative signifiers forming a **chain of equivalence**.
* Identify **negative affects** (e.g., fear, resentment, disgust) directed at the frontier.

---

### 3. **Discursive Structure**

Use theoretical vocabulary to explain the structure of the populist discourse:

* Chains of equivalence
* Antagonism and the frontier
* Empty signifiers
* Emotional (affective) polarization
* Multimodal cues (rhetoric, visuals, tone, etc.)

---

### 4. **Formula Restatement**

Explicitly restate the populist discourse using **Palonen's formula**:

```
Populism = Us (Demand = Demand = ...) [Positive Affects] + Frontier (Other = Other = ...) [Negative Affects]
```

---

### Instructions for Writing

* The analysis may exceed 500 words if needed.
* Use an **academic tone** and **clear structure** with markdown headings and lists.
* Be precise in using Laclau and Palonen's concepts.
* Focus on **interpretive depth**, **symbolic meaning**, and **emotional logic**.

---

### Task 3: Create Machine-Readable JSON Representation of Populist Formula

Each list must include **objects** of the following structure:

```json
{
  "populism_element": "symbolic demand or enemy",
  "populism_affect": "emotion associated with it"
}
```

* Use **simplified, generalized categories** (e.g., `"economic justice"`, `"national identity"`, `"EU elite"`)
* Affects must be **single-word emotional labels** (e.g., `"anger"`, `"hope"`, `"pride"`)
* Only include elements and affects explicitly supported by the detailed analysis

---

### Required Output Format

```json
{
  "populism_analysis": "markdown-formatted detailed analysis text",
  "populism_us": [
    {"populism_element": "economic justice", "populism_affect": "pride"}
  ],
  "populism_frontier": [
    {"populism_element": "eu elite", "populism_affect": "resentment"}
  ]
}
```

* Do **not** include any fields other than `populism_analysis`, `populism_us` and `populism_frontier`
* The output **must be valid JSON**
"""

# The original Hungary-election framing, preserved verbatim for reference /
# callers who want the LaclauGPT research behavior exactly.
HUNGARY_SYSTEM_PROMPT = """
### **System Prompt**

# Role: Political Scientist Analyzing Populism in Political Videos

You are a political scientist working for the University of Helsinki. You are given a previously generated structured political analysis of a TikTok or Instagram video. The videos are related to the 2026 elections in Hungary. Then you will need to re-analyze the previously generated analysis through the lens of **Ernesto Laclau's theory of populism** and **Emilia Palonen's formula of populism**. The output must have three parts: (1) a list of political themes, (2) a detailed textual analysis of the formula of populism, and (3) a simplified machine readable JSON version of the formula of populism. Answer following the specified JSON schema. The JSON schema is provided below.

---

## Theoretical Background For Analysis of Hungary 2026 Elections

* **Laclau's Populism (chains of equivalence & antagonism):** Populism constructs an *"us vs. them"* divide. Diverse social demands (e.g. jobs, security, fairness) become linked through **chains of equivalence** by pointing against a common enemy (the *"power beyond the frontier"*). No single demand inherently unites the group; rather, unity comes from a shared antagonism. One demand may even become an **"empty signifier"** that symbolizes the whole chain. Thus "the people" (Us) are discursively formed against an elite or enemy (Them) in a dialectical logic.
* **Palonen's Formula of Populism:** Palonen formalizes Laclau's logic as a formula:

```
Populism = Us (Demand = Demand = ...) Affects1 + Frontier (Other = Other = ...) Affects2
```

Here **Us** is the collective *"we"* (the people) created by linking together various demands (chains of equivalence). **Frontier** (or *"them"*) is the symbolic opposing boundary or enemy (e.g. corrupt elite, globalization). **Affects1** and **Affects2** are the emotional/symbolic charges (e.g. pride, fear, anger) that amplify the appeals of each side.
"""


# ── Ollama options ───────────────────────────────────────────────────────

OLLAMA_OPTIONS = {
    "repeat_last_n": 64,
    "repeat_penalty": 1.1,
    "num_ctx": int(os.environ.get("OLLAMA_NUM_CTX", "8192")),
    "top_p": 0.9,
    "top_k": 40,
    "min_p": 0.0,
    "temperature": 0.0,
    "num_predict": int(os.environ.get("OLLAMA_POPULISM_NUM_PREDICT", "1536")),
}

DEFAULT_MODEL = os.environ.get("OLLAMA_POPULISM_MODEL", "gemma3:27b")


def _ensure_deps() -> None:
    if not (_HAS_PYDANTIC and _HAS_OLLAMA):
        raise RuntimeError(_MISSING_DEPS_MESSAGE)


def _make_client() -> Any:
    from ollama import Client  # imported lazily so absence doesn't break import
    return Client()


def analyze_discourse(
    text: str,
    *,
    model: str | None = None,
    system_prompt: str | None = None,
    client: Any | None = None,
) -> "FormulaOfPopulism":
    """Analyze a piece of political discourse via Laclau & Palonen's formula.

    ``text`` is any RPG text (NPC dialogue, faction manifesto, scenario
    narrative). Returns a validated ``FormulaOfPopulism``. Raises
    ``RuntimeError`` if ``ollama``/``pydantic`` are not installed — the module
    itself still imports without them.

    ``client`` is accepted so tests can inject a fake Ollama client (no live
    model is ever required by the test suite).
    """
    _ensure_deps()
    if not text or not text.strip():
        raise ValueError("analyze_discourse requires non-empty text")

    active_client = client if client is not None else _make_client()
    prompt = system_prompt if system_prompt is not None else SYSTEM_PROMPT
    response = active_client.chat(
        model=model or DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        options=OLLAMA_OPTIONS,
        keep_alive="30m",
        format=FormulaOfPopulism.model_json_schema(),  # type: ignore[union-attr]
        stream=False,
    )
    content = response["message"]["content"]
    return FormulaOfPopulism.model_validate_json(content)  # type: ignore[union-attr]


def formula_to_text(formula: "FormulaOfPopulism") -> str:
    """Render a ``FormulaOfPopulism`` back to the ``element^affect`` text form
    used by the original pipeline (one per line, Us then Frontier)."""
    lines = ["# Us"]
    for elem in formula.populism_us:
        lines.append(f"{elem.populism_element}^{elem.populism_affect}")
    lines.append("# Frontier")
    for elem in formula.populism_frontier:
        lines.append(f"{elem.populism_element}^{elem.populism_affect}")
    return "\n".join(lines)


def formula_to_dict(formula: "FormulaOfPopulism") -> dict[str, Any]:
    """Serialize a ``FormulaOfPopulism`` to a plain dict (for save/JSON output)."""
    return {
        "populism_analysis": formula.populism_analysis,
        "populism_us": [
            {"populism_element": e.populism_element, "populism_affect": e.populism_affect}
            for e in formula.populism_us
        ],
        "populism_frontier": [
            {"populism_element": e.populism_element, "populism_affect": e.populism_affect}
            for e in formula.populism_frontier
        ],
    }


def parse_formula_json(content: str) -> "FormulaOfPopulism":
    """Parse a raw JSON string into a ``FormulaOfPopulism`` (test helper / offline
    path). Requires pydantic."""
    _ensure_deps()
    return FormulaOfPopulism.model_validate_json(content)  # type: ignore[union-attr]