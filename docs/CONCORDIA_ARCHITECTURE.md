# Concordia RPG / Simulation Architecture

This document describes the **infrastructure-only** Concordia runtime for NoöPunk.

It consumes the author-defined core attributes and 3d6 mechanics, but does not define additional characters, factions, world facts, skills, combat, or simulation theory.

## One RPG, three runtimes

NoöPunk is intended to use one conceptual rules and world model across:

1. tabletop RPG
2. Godot RPG
3. Concordia RPG / generative social simulation

`RULEBOOK.md` is the human-readable rules counterpart. Shared rules and canonical data belong outside runtime-specific code.

## Why Concordia

Google DeepMind Concordia is built around entities, Game Masters, components, and a simulation engine. This fits the intended NoöPunk simulation role, where a GM can mediate a world populated by LLM-driven agents and, later, human-controlled participants.

The current Concordia integration deliberately uses only its generic infrastructure. No NoöPunk social model has been implemented yet.

## Package layout

### `src/concordia_runtime/config.py`

Runtime-only configuration for local Ollama use.

The Ollama model is required through configuration. No model is canonical.

Environment variables:

- `NOOPUNK_OLLAMA_MODEL` — required model identifier
- `NOOPUNK_OLLAMA_BASE_URL` — default `http://127.0.0.1:11434`
- `NOOPUNK_OLLAMA_TEMPERATURE` — runtime generation setting
- `NOOPUNK_OLLAMA_TOP_P` — runtime generation setting
- `NOOPUNK_OLLAMA_TOP_K` — runtime generation setting

These are runtime controls, not game rules.

### `src/concordia_runtime/providers.py`

Defines a replaceable `LanguageModelProvider` boundary.

`OllamaProvider` currently delegates to Concordia's own Ollama language-model adapter instead of duplicating an Ollama HTTP client.

No cloud fallback exists.

### `src/concordia_runtime/participants.py`

Contains neutral runtime interfaces:

- `GameMasterSpec`
- `LLMAgentSpec`
- `HumanPlayer`

LLM and human participant specs may now carry an optional structured AttributeSet with the six canonical modifiers. They still contain no skills, personality model, equipment, faction, ideology, goals, psionics, or other unrequested RPG content.

`HumanPlayer` is currently only an input adapter. It is not silently converted into an LLM-controlled Concordia entity.

### `src/concordia_runtime/session.py`

`SessionSpec` represents a neutral session.

`build_concordia_config()` translates the neutral spec into Concordia's current prefab configuration using:

- `minimal__Entity` for placeholder LLM participants
- `generic__GameMaster` for the placeholder GM

`build_simulation()` constructs Concordia's generic simulation runner from explicitly injected:

- language model
- text embedder

The embedder is not chosen automatically because semantic memory is a technical/research choice that should remain explicit.

## Concordia dependency contract

The runtime currently targets Concordia APIs that are available on upstream GitHub `main`, including `concordia.prefabs`, `concordia.typing.prefab`, and `concordia.contrib.language_models.ollama`.

The PyPI release that originally satisfied `gdm-concordia[ollama]` did not contain those modules. Therefore `requirements-concordia.txt` intentionally installs Concordia from a **pinned upstream commit**, not from an unpinned PyPI release or moving Git branch.

Verified upstream revision:

```
405584db8e09e001da6deb147a6389f7a7f44e28
```

When updating Concordia, inspect the upstream API first, update the pin deliberately, and run the Concordia smoke check. Do not replace the pinned Git dependency with `gdm-concordia[ollama]` unless a released package has been verified to provide the exact APIs the runtime imports.

## Ollama

Install optional dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-concordia.txt
```

Choose a local model explicitly:

```bash
export NOOPUNK_OLLAMA_MODEL=your_local_model
```

The scaffold does not select a preferred model.

## Smoke tests

The neutral scaffold can be checked without installing Concordia or contacting Ollama:

```bash
python scripts/concordia_smoke.py
```

After installing the pinned Concordia dependency, its prefab translation can also be checked:

```bash
python scripts/concordia_smoke.py --build-concordia-config
```

The flag is important: the default smoke command validates only NoöPunk's neutral scaffold, while `--build-concordia-config` proves that the installed Concordia API matches the adapter imports.

Neither command generates NoöPunk lore.

A real Concordia run additionally requires an explicit text embedder and a local Ollama model.

## Human player seam

The optional human player is represented by an input adapter rather than an invented game UI or alternate rules system.

A later author-approved task can connect human actions into Concordia's engine after the desired interaction model is specified.

The human and LLM-controlled participants must ultimately use the same author-defined RPG semantics.

## Prompts are runtime instructions, not canon

The Ollama adapter contains only a minimal safety instruction telling the model not to invent rules or world facts and to use supplied simulation context.

Canonical mechanics and lore must not be smuggled into prompts.

## Intentionally undefined

The Concordia runtime now consumes the canonical six attributes and deterministic core 3d6 resolution from shared code. It still does not define:

- skills or a skill list
- character creation
- combat
- health, damage, armor, wounds, or initiative
- advancement
- psionics
- NHI taxonomy or mechanics
- cyberware mechanics
- hacking
- social mechanics
- equipment
- economy
- factions
- professions
- quests or plot
- detailed geography
- NPC personalities or goals
- simulation equations
- causal social model
- Noösphere mechanics
- exact future dates

Those remain separate author-driven design tasks.

## Current technical constraints

- Python runtime for Concordia integration.
- Current Concordia prefab API is isolated behind NoöPunk adapter functions.
- Concordia is pinned to a verified upstream Git commit because the required prefab/contrib API is not assumed to exist in PyPI releases.
- Local Ollama is the configured LLM backend for this runtime.
- A text embedder must be supplied explicitly before creating a real simulation.
- No third-party NoöPunk-specific agent framework has been added.
- No cloud LLM fallback has been added.

The adapter boundary is intended to absorb future Concordia API changes without altering canonical NoöPunk rules.
