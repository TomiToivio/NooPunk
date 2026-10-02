# Concordia RPG / Simulation Architecture

This document describes the preserved **infrastructure-only** Concordia runtime for NoöPunk.

> **Development status:** Concordia is a later-stage port/simulation runtime. Substantive NoöPunk mechanics, world systems, scenarios, and agent behavior should not advance ahead of the canonical tabletop rules/worldbook. Existing Concordia infrastructure is preserved for later conversion work.

It currently still consumes the **legacy six-attribute digital model** plus the canonical 2d6 skill check from shared code. Issue #51 revises the tabletop character model to typed tags distributed across the four Physical / Social / Psychic / Cybernetic systems, so the six-attribute adapter is now explicit porting debt rather than final canon. The runtime must not invent the final attribute list while that author decision remains open.

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

LLM and human participant specs may currently carry the legacy structured AttributeSet only for backward compatibility. Future migration should use the engine-independent typed-tag state from `src/rules/tags.py`, including explicit system presence/absence. Participant specs still contain no invented skills, personality model, equipment, faction, ideology, goals, psionics, or other unrequested RPG content.

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

The Concordia runtime consumes the canonical six attributes and deterministic resolution from shared code. **That resolution is now the canonical 2d6 skill check** (RULEBOOK.md §4): the shared `resolve_check` in `src/rules/core.py` rolls 2d6 and adds skill level and the attribute modifier against the `6 / 8 / 10 / 12 / 14+` ladder, and the §17.1 port debt is retired for this runtime. It still does not define:

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

NoöPunk should not spend LLM inference on every simulated person. The intended architecture is hierarchical:

1. **Aggregate/environmental state** — crowds, traffic, public mood, markets, diffusion and other non-individual processes.
2. **Mesa / rule agents** — cheap background agents with structured tags, location, faction/network position, resources and limited actions.
3. **Lightweight interactive NPCs** — simulation-driven NPCs that can invoke an LLM temporarily when a human starts a meaningful conversation.
4. **Persistent Concordia / LLM agents** — major recurring characters with memory, beliefs, goals, relationships, motivations and open-ended natural-language interaction.

The same base entity/tag representation should be usable across tiers so an NPC can be promoted when it becomes narratively salient. Promotion changes the controller, not the character's identity or history.

No automatic promotion threshold is canonical yet. Do not invent one in runtime code without an author-approved rule.

### Mesa role

Mesa is appropriate for large populations of limited agents whose interaction vocabulary can remain structured, for example movement, avoidance, trade, reporting, joining/leaving groups, information sharing or other explicitly authored actions. Mesa agents can still participate in Social-system networks without pretending to have unrestricted dialogue.

The current repository does **not** yet add Mesa as a dependency. This section records the architecture approved by issue #51; implementation waits for a focused task so dependency choice, scheduler semantics and population rules are not silently invented.

## Human multiplayer direction

NoöPunk should be architected so multiple human players can participate in one authoritative simulation state.

Conceptually:

```text
Human A ─┐
Human B ─┤
Human C ─┤
         ▼
 authoritative NoöPunk server
         │
 rules + world state + event log
         │
 ┌───────┼────────┐
 ▼       ▼        ▼
Mesa   LLM NPCs  Concordia GM
agents
```

Human and AI-controlled participants should submit compatible **intent/action envelopes** into the same rules/simulation layer wherever practical. Deterministic mechanics remain authoritative regardless of who supplied the intent.

### UI/server sequence

The first multiplayer UI may be **Streamlit** because the project is Python-first and Streamlit is sufficient for a small prototype with character sheets, chat, logs, maps, network views and admin/debug controls.

Streamlit must remain a client/presentation layer rather than owning canonical simulation state.

For richer real-time multiplayer, the likely later architecture is:

```text
FastAPI + WebSockets
        │
authoritative Python simulation
        │
Mesa + Concordia + persistence
        │
Streamlit prototype UI
        │
optional later JavaScript client
```

This is an architecture direction, not a requirement to add FastAPI, WebSockets or Streamlit now.

> **The UI is a client. The NoöPunk simulation is the game.**
