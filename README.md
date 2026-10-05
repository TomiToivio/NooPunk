# NoöPunk

**NoöPunk = Noösphere + Cyberpunk.**

NoöPunk is an experimental **computer RPG and social simulation** set in **20XX**, using an **independent NoöPunk rules system**, a deterministic Python RPG kernel, and **Google DeepMind Concordia** for optional LLM-driven agents and narration. Earth still exists. Transhuman technology is already here. AGI, cyborgification, NHI contact, psionics, panpsychism, and the emerging Noösphere are destabilizing the old world at the same time.

The project is currently a **playable text-based prototype**. You can run the normal game entirely without Ollama or an LLM.

## Quick start

Requires **Python 3.12** (the version tested in CI).

```bash
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/noopunk_text.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

The normal start command launches the default **pre-Fall 20XX** NoöPunk scenario:

```bash
python scripts/noopunk_text.py
```

Ollama is optional for basic play.

## First-player cheat sheet

At the prompt, try:

```text
look
n / s / e / w
go <direction>
inventory
take <item>
drop <item>
talk <character> <message>
say <message>
stats
sheet
save
quit
```

Useful rules/debugging commands also include:

```text
test skill ...
test social ...
test mesh ...
test combat ...
```

See [`RULEBOOK.md`](RULEBOOK.md) for the actual rules instead of treating the README as a second rulebook.

## Installation

### Linux / macOS

```bash
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
git clone https://github.com/TomiToivio/NooPunk.git
cd NooPunk
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The deterministic text game itself uses only the Python standard library. The top-level `requirements.txt` also installs the pinned Concordia dependency needed by the current Concordia integration and optional Ollama-backed runtime.

## Start the game

### Default NoöPunk scenario

```bash
python scripts/noopunk_text.py
```

This starts the canonical **20XX, Earth-intact** NoöPunk scenario.

### Small Concordia / EP2 proof of concept

```bash
python scripts/noopunk_text.py --scenario issue74
```

Issue #74 is a deliberately tiny vertical slice for testing the current architecture. It remains fully playable **without an LLM**, using deterministic mechanics and scripted NPC behaviour.

Scenario notes: [`docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md`](docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md).

### CLI help

```bash
python scripts/noopunk_text.py --help
```

## Optional Ollama / LLM mode

Ollama is an **external runtime/service**, not a Python dependency. Install and start Ollama separately, then make sure the model you want to use is available in Ollama.

The current NoöPunk adapter reads these environment variables:

- `NOOPUNK_OLLAMA_MODEL` — **required** model identifier.
- `NOOPUNK_OLLAMA_BASE_URL` — optional; defaults to `http://127.0.0.1:11434`.
- `NOOPUNK_OLLAMA_TEMPERATURE` — optional; defaults to `0.5`.
- `NOOPUNK_OLLAMA_TOP_P` — optional; defaults to `1.0`.
- `NOOPUNK_OLLAMA_TOP_K` — optional; defaults to `40`.

For example:

```bash
export NOOPUNK_OLLAMA_MODEL="your-installed-model"
python scripts/noopunk_text.py --ollama
```

To run the small issue #74 scenario with an LLM-controlled contact and optional GM narration:

```bash
export NOOPUNK_OLLAMA_MODEL="your-installed-model"
python scripts/noopunk_text.py --scenario issue74 --ollama --llm-gm
```

The division of labour is intentional:

- **LLM / Concordia:** dialogue, agent choice, natural-language intent translation, interpretation, and optional GM narration.
- **Python:** legal actions, game state, dice and rules resolution, character statistics, inventory, harm/stress, world-state changes, and consequences.

LLMs may decide what an agent attempts. They do not get to invent dice rolls or silently rewrite the rules.

## Current status

NoöPunk is an experimental text-based RPG/social-simulation prototype under active development.

The current direction is:

```text
Independent NoöPunk RPG
        ↓
1–10 STAT + 1–10 Skill + 1d10 core
        ↓
subsystems selectively inspired by many games
        ↓
shared deterministic rules for text / Concordia / future Godot use
```

NoöPunk is **not an Eclipse Phase conversion and not a hack of any single parent system**. Cyberpunk 2020/RED is an important reference for readable STAT + Skill + d10 resolution; Eclipse Phase remains important for transhuman concepts; Fate, PbtA, CY_BORG, Cities Without Number/OSR, Citizen Sleeper, The Expanse and other games inform different design problems.

The current core work is [issue #111](https://github.com/TomiToivio/NooPunk/issues/111).

## What NoöPunk is about

The **Cyberpunk** side explores the AI revolution, automation, surveillance, corporate and state power, hacking, biotechnology, BCI, cybernetics, morphs, cyborgification, transhumanism, and post-scarcity technologies.

The **Noösphere** side explores NHI/UAP contact, psionics, panpsychism, consciousness-related phenomena, and the possibility that humans, machines, cultures, and networks form larger cognitive assemblages.

The setting treats these as simultaneous paradigm shifts. Humans are deeply divided about them: enthusiasts, accelerationists, doomers, skeptics, regulators, opportunists, believers, critics, and people who simply do not care or understand what is happening all inhabit the same world.

NoöPunk therefore focuses not only on future technology, but on what societies do when several incompatible futures arrive at once.

## How the game works

NoöPunk is being developed as **one computer RPG and social simulation**, not as separate tabletop and computer games.

The rules are tabletop-like because they need to be:

- readable by humans;
- inspectable and testable;
- executable deterministically in Python;
- usable by Concordia/LLM agents without giving the model authority to invent outcomes.

The preferred loop is:

```python
intent = agent.choose_action(...)
result = rules.resolve(intent, actor, target, world)
world.apply(result)
agent.observe(result)
```

Important characters, factions, and institutions may use LLM cognition. Simpler background NPCs can use deterministic or lightweight scripted behaviour where rich language interaction is unnecessary.

## Rules influences

NoöPunk is an independent RPG. External games are **influences rather than compatibility targets**.

Current important influences include:

- **Cyberpunk 2020 / RED** for the clarity and feel of STAT + Skill + d10 resolution;
- **Eclipse Phase** for transhuman technology, morphs/embodiment, mesh, reputation, space and existential-risk ideas;
- **Fate** for aspects/stunts and fiction-facing flexibility;
- **PbtA / The Sprawl / The Veil** for moves, consequences and narrative pressure;
- **CY_BORG** and **Cities Without Number / OSR** for fast, compact play;
- **Citizen Sleeper 1/2** for text-RPG structure, clocks and pressures;
- **The Expanse** and other science-fiction RPGs where specific subsystem ideas fit.

Directly adapted material keeps its source and licensing provenance. No external ruleset supplies default mechanics automatically.

## Rules and world documentation

Active canonical documents:

- **Rules:** [`RULEBOOK.md`](RULEBOOK.md)
- **Continuity boundary:** [`docs/PRE_FALL_ALTERNATE_TIMELINE.md`](docs/PRE_FALL_ALTERNATE_TIMELINE.md)
- **Umbrella implementation work:** [issue #60](https://github.com/TomiToivio/NooPunk/issues/60)
- **Small Concordia/EP2 scenario:** [`docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md`](docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md)

Documents under [`docs/archive/`](docs/archive/) are historical design records. They are useful provenance, but they are **not automatically active canon** and do not override the current rulebook or explicit current author direction.

### Design references

These archived documents remain important design and architecture references even when they are not active canon:

- [`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md) — project-level design balances and invariants.
- [`docs/archive/SIMULATION_ARCHITECTURE_SPEC.md`](docs/archive/SIMULATION_ARCHITECTURE_SPEC.md) — simulation state, event-log and resolver architecture.
- [`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md) — the single-game / single-rule-model direction.

## Development and architecture

The runtime is split deliberately:

### Deterministic rules kernel

Python owns state and mechanical truth wherever practical:

- action legality;
- skill and opposed tests;
- dice;
- modifiers;
- damage and stress;
- inventories;
- resources;
- persistence;
- scenario objectives;
- explicit world-state mutations.

### Concordia / LLM layer

Google DeepMind Concordia is the agent/narrative layer. LLM agents can:

- choose goals and actions;
- converse;
- negotiate;
- interpret situations;
- translate natural-language player intent;
- narrate already-resolved outcomes.

The current Concordia dependency is pinned to a specific upstream Git revision because NoöPunk uses prefab/contrib APIs that were verified against that revision.

### Smoke checks

These commands should remain valid:

```bash
python scripts/noopunk_text.py --help
printf 'quit\n' | python scripts/noopunk_text.py --scenario issue74
python scripts/concordia_smoke.py
```

With the dependencies from `requirements.txt` installed, also check the real Concordia import/config bridge:

```bash
python scripts/concordia_smoke.py --build-concordia-config
```

## Eclipse Phase sources and license

Eclipse Phase is created by **Posthuman Studios**. Eclipse Phase-derived material in this repository must follow the applicable Eclipse Phase Creative Commons terms and attribution requirements.

License information and source references:

- [Eclipse Phase Creative Commons license](https://eclipsephase.com/cclicense/)
- [Eclipse Phase 2E online rules](https://eclipsephase.github.io/en/01/00-infamy.html)
- [Eclipse Phase 2E Quick-Start Rules](https://eclipsephase.com/wp-content/uploads/2024/02/PS10001_EclipsePhaseSecondEdition_QuickStartRulesAcrimony_Nov2023.pdf)

The Eclipse Phase material used for this homebrew is generally published under a **Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)** license. EP-derived material must remain appropriately attributed, noncommercial where required, and shared under compatible ShareAlike terms.

NoöPunk-original setting material and code should be kept clearly distinguishable from directly copied or adapted Eclipse Phase material. Imported rules text, game data, or code should record its source, license, and modifications.

The aim is to implement and transform the rules, not to mirror the Eclipse Phase books. Prefer code, structured data, compact rule summaries, conversion notes, and provenance records over copying large amounts of rulebook prose.

**NoöPunk is an unofficial fan/homebrew project and is not affiliated with or endorsed by Posthuman Studios.**
