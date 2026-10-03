# Concordia RPG / Simulation Architecture

This document describes the preserved **infrastructure-only** Concordia runtime for NoöPunk.

> **Development status:** Concordia is a later-stage port/simulation runtime. Substantive NoöPunk mechanics, world systems, scenarios, and agent behavior should not advance ahead of the canonical tabletop rules/worldbook. Existing Concordia infrastructure is preserved for later conversion work.

It consumes the author-defined core attributes and the core skill check from shared code. **The check is now the canonical 2d6 engine** (`2d6 + skill level + attribute modifier` against `6 / 8 / 10 / 12 / 14+`, RULEBOOK.md §4) — the 3d6 port debt recorded in RULEBOOK.md §17.1 has been retired for this runtime. It does not define additional characters, factions, world facts, skills, combat, or simulation theory.

## One RPG, three runtimes, tabletop first

NoöPunk is intended to use one conceptual rules and world model across:

1. tabletop RPG
2. Godot RPG
3. Concordia RPG / generative social simulation

`RULEBOOK.md` is the canonical human-readable rules source. Shared rules and canonical data belong outside runtime-specific code, and the tabletop definition is stabilized before Concordia receives the system.

Per [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) §2, the runtimes share the same rules, mechanics, character model, world model, and terminology, and may diverge only in scenarios, presentation, UI, pacing, and medium-specific implementation details. Concordia may not fork a rule to make simulation easier: if a shared rule is undefined, leave it undefined or use clearly non-canonical fixtures.

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

LLM and human participant specs currently still expose the older AttributeSet for compatibility. Issue #51's target model is the unified four-system tag representation; runtime migration must follow the canonical rulebook rather than treating the old six identifiers as final canon.

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

The Concordia runtime currently consumes legacy six-attribute compatibility data plus deterministic resolution from shared code. Issue #51 defines the future participant model as four-system typed tags; final attribute names/counts remain author-owned. **That resolution is now the canonical 2d6 skill check** (RULEBOOK.md §4): the shared `resolve_check` in `src/rules/core.py` rolls 2d6 and adds skill level and the attribute modifier against the `6 / 8 / 10 / 12 / 14+` ladder, and the §17.1 port debt is retired for this runtime. It still does not define:

- skill levels and the skill list (specified for tabletop in RULEBOOK.md §5.3; not yet ported)
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


## Porting gate

Concordia work follows the sequence **tabletop rule → digital specification → Godot implementation → Concordia implementation** unless an author-approved task explicitly changes the order.

Before adding a substantive Concordia system, verify that the corresponding tabletop mechanic/world concept is explicitly defined and coherent. If simulation work exposes ambiguity, repair the tabletop source first rather than resolving it only in prompts, components, or agent logic.

Concordia-specific simulation plumbing may remain as preserved infrastructure while tabletop design proceeds.


## Issue #51 agent ecology

NoöPunk should not run every simulated person as a persistent LLM.

Use a hierarchy:

1. **Aggregate/environmental processes** for crowds, traffic, public mood, markets and other non-individual state.
2. **Mesa / rule agents** for background individuals with structured state and limited action vocabularies.
3. **Lightweight interactive NPCs** that remain simulation-driven but may invoke an LLM temporarily when a meaningful conversation begins.
4. **Persistent Concordia / LLM agents** for major recurring characters with memory, beliefs, goals, relationships, motivations and unrestricted natural-language interaction.

All tiers should share the same underlying entity/tag representation so an NPC can be promoted when it becomes narratively salient without being recreated from scratch.

No promotion threshold, scheduler, Mesa dependency or population rule is canonical yet. Those require a focused implementation task.

## Human multiplayer direction

The architecture should support multiple humans sharing one authoritative simulation state.

~~~text
Human A ─┐
Human B ─┤
Human C ─┤
         ▼
 authoritative NoöPunk server
         │
 rules + world state + event log
         │
 ┌───────┼──────────┐
 ▼       ▼          ▼
Mesa   LLM NPCs  Concordia GM
agents
~~~

Human and AI-controlled participants should submit compatible intent/action envelopes into the same deterministic rules/simulation layer.

### Web UI sequence

A **Streamlit** interface is suitable for an early small-group prototype because the project is Python-first and needs character sheets, dialogue, logs, maps/network views and debug/admin controls more than a high-performance graphical client.

Streamlit should remain a client/presentation layer, not the owner of canonical game state.

If richer real-time multiplayer is later needed, prefer an authoritative Python server with **FastAPI + WebSockets**, while keeping Streamlit as a prototype/admin UI and optionally adding a JavaScript client later.

> **The UI is a client. The NoöPunk simulation is the game.**
