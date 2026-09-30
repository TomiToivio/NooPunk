# NoöPunk

**NoöPunk = Noösphere + Cyberpunk.**

NoöPunk is an original speculative science-fiction genre, RPG setting, and simulation project. It asks what a cyberpunk future becomes when the familiar technological transformation of AI, networks, corporations, surveillance, cybernetics, and human augmentation is joined by more radical paradigm shifts concerning consciousness and non-human intelligence.

The project is grounded aesthetically and socially in **cyberpunk**, but its "other world" is not urban fantasy. Instead, NoöPunk explores a future shaped by the **Noösphere**, consciousness, psionics, non-human intelligences, and consciousness-fundamental metaphysics.

## The core idea

NoöPunk combines several layers:

- **Cyberpunk:** AI, automation, corporate and state power, surveillance, networks, cybercrime, inequality, biotechnology, brain-computer interfaces, and cyborgification.
- **Noösphere:** the emergence of a planetary layer of connected intelligence inspired by **Pierre Teilhard de Chardin**, expanded into a world of humans, AIs, networks, BCIs, culture, and potentially non-local forms of consciousness.
- **Quantum panpsychism / consciousness:** inspired in part by **Alexander Wendt's _Quantum Mind and Social Science_**, **Federico Faggin's quantum-information-oriented panpsychism**, and **Donald Hoffman's Conscious Realism**.
- **NHI / UFOs:** inspired in part by **Alexander Wendt's work on UFOs and state sovereignty** and **Jacques Vallée's Interdimensional Hypothesis**. In the NoöPunk scenario, NHI cannot be reduced to extraterrestrial biology and technology alone; the phenomenon may be stranger and consciousness-related.
- **Psionics:** inspired by the experimental research tradition associated with **Dean Radin**, treated inside the fictional scenario as a future scientific and technological domain.

These inspirations are not presented here as proof that the speculative claims are established science. They are inputs to the setting and simulation.

## Genre and influences

NoöPunk keeps the technological, political, urban, and economic core of old-school cyberpunk.

Major RPG influences include:

- **Cyberpunk 2013 / 2020 / RED**
- **Shadowrun**
- **Eclipse Phase**

A rough analogy is **Shadowrun with the cyberpunk left as cyberpunk, while the urban-fantasy layer is replaced by the Noösphere, NHI, psionics, and consciousness-fundamental metaphysics**.

Other important tonal influences include **Philip K. Dick** and 1970s space psychedelia, including **Hawkwind**. The intended result is simultaneously near-future and retrocyberpunk: recognizably descended from the world of 2026, but filtered through older visions of technological futures.

## Time and scenario

The setting uses dates written as **20XX**.

It is approximately the author's imagined **2045-like future**, extrapolated from the situation in 2026, without fixing the fiction to a single canonical calendar year.

See [TIMELINE.md](TIMELINE.md) for the current speculative scenario.

## RPG + simulation

NoöPunk has two connected purposes:

1. **RPG:** one shared ruleset usable in three runtimes:
   - **Tabletop RPG**
   - **Godot RPG**
   - **Concordia RPG / cyberpunk simulation**, using local **Ollama** LLMs for a GM and NPC agents, with support for adding a human-controlled player.
2. **Simulation:** an experimental model for exploring the social consequences of several interacting paradigm shifts:
   - AI and cyberpunk technological transformation
   - cyborgification and human-machine integration
   - consciousness as a scientific and metaphysical problem
   - scientifically validated psionics within the scenario
   - NHI becoming part of social and political reality
   - emergence of the Noösphere

The tabletop, Godot, and Concordia versions should share the same conceptual rules and world model wherever practical. Godot is the conventional computer-RPG runtime; Concordia is the agent-based simulation/RPG runtime. Neither runtime should redefine the canonical rules.

## Development principle: build slowly

The project must **not** fill gaps by inventing mechanics or lore.

The initial Godot work should create only a clean, minimal RPG foundation. Major design areas such as attributes, skills, combat, psionics, NHI, factions, character creation, equipment, economy, progression, world geography, quests, and detailed simulation rules are reserved for later specification by the author.

See [RULEBOOK.md](RULEBOOK.md) for the intentionally incomplete rules framework and [AGENTS.md](AGENTS.md) for mandatory agent constraints.

The rule is simple: **scaffold first, canon later**.


## Three design balances

NoöPunk holds three deliberate balances, documented once in [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md):

1. **Gamism / Narrativism / Simulationism** — the creative agendas, anchored on **CY_BORG** (challenge), **Cyberpunk 2020** (reality) and **The Sprawl** (story).
2. **Tabletop / Godot / Concordia** — same world, same rules, same mechanics wherever possible; scenarios and presentation may diverge.
3. **Cyberpunk / Noösphere** — neither half swallows the other; the Noösphere rests on UFO/UAP Disclosure, Psionics and Panpsychism.

**Shadowrun** and **Eclipse Phase** are important comparative influences, not templates. NoöPunk is not an Eclipse Phase homebrew or expansion.


## Godot scaffold

A minimal **Godot 4** project now lives in this repository.

To open it:

1. install Godot 4;
2. import or open this repository's `project.godot`;
3. run the project.

The current scene is deliberately only a neutral bootstrap screen. It contains no game mechanics or canonical world content.

Architecture notes: [docs/GODOT_ARCHITECTURE.md](docs/GODOT_ARCHITECTURE.md)

A lightweight static scaffold check is available with:

```bash
python tests/validate_scaffold.py
```

Future mechanics and worldbuilding must continue to follow [AGENTS.md](AGENTS.md) and be specified incrementally in [RULEBOOK.md](RULEBOOK.md).


## Concordia scaffold

The repository also contains a minimal **Google DeepMind Concordia** runtime for the simulation/RPG form of NoöPunk.

It is deliberately infrastructure-only:

- Concordia GM boundary
- generic LLM-controlled agent boundary
- optional human-player input boundary
- local Ollama provider
- no cloud fallback
- no invented rules, NPCs, factions, or simulation model

Install the optional runtime dependencies with:

```bash
pip install -r requirements-concordia.txt
```

Choose an Ollama model explicitly:

```bash
export NOOPUNK_OLLAMA_MODEL=your_local_model
```

Run the dependency-free neutral smoke check:

```bash
python scripts/concordia_smoke.py
```

See [docs/CONCORDIA_ARCHITECTURE.md](docs/CONCORDIA_ARCHITECTURE.md) for the runtime contract.
