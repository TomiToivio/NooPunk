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

Three of these are the setting's **defining Noösphere paradigm shifts**: UFO / UAP Disclosure, Psionics, and Panpsychism. They are what replaces the urban-fantasy layer of a Shadowrun-like setting, and they must stay science-fictional rather than becoming generic fantasy magic.

## Design principles

NoöPunk is built on **three design balances** that are project-level invariants, not loose inspirations:

1. **Gamism / Narrativism / Simulationism** — anchored on **CY_BORG** (challenge), **Cyberpunk 2020** (reality), and **The Sprawl** (story). No pole may overwhelm the others.
2. **Tabletop / Godot / Concordia** — one RPG developed in sequence: **tabletop first**, then Godot and Concordia as later ports. The tabletop rulebook/worldbook is the canonical design source; digital runtimes inherit the same world, rules, and mechanics wherever possible. Scenarios and presentation may diverge.
3. **Cyberpunk / Noösphere** — neither half swallows the other. The cyberpunk side grows from plausible near-future technology; the Noösphere rests on UFO / UAP Disclosure, Psionics, and Panpsychism.

> **CY_BORG for challenge. Cyberpunk 2020 for reality. The Sprawl for story.**

The canonical explanation is [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md); the binding agent rules are [AGENTS.md](AGENTS.md) §13. Nothing here should restate that document in detail.

## Genre and influences

NoöPunk keeps the technological, political, urban, and economic core of old-school cyberpunk.

NoöPunk's **open mechanical chassis** is the **[Cities Without Number SRD](https://cwn.quadrifons.com/)** (public domain). NoöPunk starts from that SRD, then goes through the system **subsystem by subsystem** and deliberately decides what to KEEP, MODIFY, REPLACE, OMIT, or DEFER. NoöPunk is **not** a CWN clone and is expected to diverge substantially from it. Existing NoöPunk author decisions take precedence over CWN defaults. See [docs/CWN_CHASSIS.md](docs/CWN_CHASSIS.md).

Major RPG influences include:

- **Cities Without Number SRD** — the open mechanical chassis and main starting point
- **Cyberpunk 2013 / 2020 / RED** — the Simulationism reference (`Cyberpunk 2020`)
- **CY_BORG** — the Gamism reference
- **The Sprawl** — the Narrativism reference
- **Shadowrun** and **Eclipse Phase** — comparative influences, not templates

Only material actually present in the Cities Without Number **SRD** may be directly reused. Protected material from the full CWN book, and protected text or setting material from Cyberpunk 2020, Eclipse Phase, Shadowrun, The Sprawl, or CY_BORG, must not be copied. Those games are design references only.

A rough analogy is **Shadowrun with the cyberpunk left as cyberpunk, while the urban-fantasy layer is replaced by the Noösphere, NHI, psionics, and consciousness-fundamental metaphysics**. Unlike Shadowrun, the anomalous layer comes from UFO / UAP Disclosure, psionics, and panpsychism rather than fantasy races and magic. Eclipse Phase is the closest comparison where cyberpunk and anomalous / posthuman themes meet.

Other important tonal influences include **Philip K. Dick** and 1970s space psychedelia, including **Hawkwind**. The intended result is simultaneously near-future and retrocyberpunk: recognizably descended from the world of 2026, but filtered through older visions of technological futures.

## Time and scenario

The setting uses dates written as **20XX**.

It is approximately the author's imagined **2045-like future**, extrapolated from the situation in 2026, without fixing the fiction to a single canonical calendar year.

See [TIMELINE.md](TIMELINE.md) for the current speculative scenario.

## The world: ideology and paradigm shifts

Every paradigm shift in the setting — AI, NHI contact, psionics, panpsychism,
BCI/cyborgization, and the Noösphere — generates **its own** accelerationists,
doomers, critical/regulatory camps, believers, skeptics and hybrids. Positions on
different shifts are **separable**, so the world is a cross-product of intersecting
struggles rather than a single pro-technology versus anti-technology axis.

The **Panpsychic Cyborg Multitude** (PCM, "the Multitude") is a major Noöspheric
faction in that world: an assemblage rather than an organisation, and internally
contested rather than ideologically unified.

- Canonical positions and the reusable multi-axis model: [data/world/ideology.json](data/world/ideology.json)
- How it plays: [docs/WORLD_IDEOLOGY.md](docs/WORLD_IDEOLOGY.md)

The ideological model is setting material only; no numeric ideology mechanics are
defined.

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

Development is now explicitly **tabletop-first**. The tabletop RPG rules/worldbook are the canonical design source. Current Godot and Concordia scaffolds are preserved, but substantive digital implementation follows only after the relevant tabletop rules and world material are coherent and stable enough to port. Godot is the conventional computer-RPG runtime; Concordia is the agent-based simulation/RPG runtime. Neither runtime should redefine the canonical rules.

## Development principle: build slowly

The project must **not** fill gaps by inventing mechanics or lore.

The initial Godot work should create only a clean, minimal RPG foundation. Major design areas such as combat, psionics, NHI, factions, character creation, equipment, economy, progression, world geography, quests, and detailed simulation rules are reserved for later specification by the author. Attributes, core 3d6 checks, and the four tabletop skill levels are specified in [RULEBOOK.md](RULEBOOK.md); skill levels are tabletop-first and not yet ported to Godot or Concordia.

See [RULEBOOK.md](RULEBOOK.md) for the intentionally incomplete rules framework and [AGENTS.md](AGENTS.md) for mandatory agent constraints.

The rule is simple: **design the tabletop game first; implement the software second**.

### Development order

1. **Tabletop design:** define and playtest the RPG rules, worldbook, terminology, procedures, and scenario structure in human-readable form.
2. **Tabletop stabilization:** resolve ambiguities and edge cases in the tabletop source before software encodes them.
3. **Digital conversion:** port stable systems incrementally: tabletop rule → digital specification → Godot implementation → Concordia implementation.

Existing Godot and Concordia code is not discarded. It remains preserved infrastructure and later-stage implementation material.


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
