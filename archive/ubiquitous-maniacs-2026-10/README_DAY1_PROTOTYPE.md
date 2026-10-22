# Noöpunk: Ubiquitous Maniacs — Day 1 Prototype

Playful prototype of a narrative RPG + social simulator + hacking/psychotronic
game set on asteroid 16 Psyche, inside the C.G. Jung City and University
operated by UFAB.

You play as **Emil Romppainen**, a Jungian profiler and former Finnish security
officer hidden under the identity **Sven-Olof**, a UFAB 80MG-addicted junkie.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Play Day 1 (terminal interface)
python play.py

# Play with a deterministic seed
python play.py --seed 42

# Load a saved game
python play.py --load saves/day1_d1_reception.json
```

## How to Play

The game presents scenes and dialogue. Type a number to choose an action,
or use one of these commands:

- `1, 2, 3...` — Choose an interaction
- `s` — View the social relationship graph
- `i` — View discovered information and flags
- `c` — View character status
- `h` — View hacking status (when available)
- `save` — Save the game
- `quit` — Exit

Skill checks use 4dF (four Fudge dice, range -4 to +4) + attribute + skill vs
difficulty. Outcomes: critical success, success, success with cost, failure,
catastrophic failure.

## Three Integrated Modules

### 1. Narrative RPG (`src/rpg/`)

A Fate/Fudge-inspired system with:
- 7 attributes: Intelligence, Awareness, Reflexes, Body, Charisma, Willpower, Cybernetics
- 24 Transhumanity's Fate skills
- Aspects, conditions, consequences, stunts
- Data-driven scenes, dialogue, and interactions loaded from JSON
- Save/load with deterministic seed support

### 2. Social Simulator (`src/game/social_graph.py`, `src/social/`)

A multi-dimensional relationship graph:
- 6 dimensions per relationship: trust, attraction, fear, suspicion, authority, familiarity
- NPCs with goals, mood, and memory
- Hidden relationships that can be revealed through play
- Change history tracking
- RPG dialogue choices flow into the social graph automatically

### 3. Hacking / Psychotronic Simulator (`src/hacking/`, `src/sim/hacking/`)

Graph-based hacking covering both conventional networks and noetic systems:
- Four operational layers: cybernetic, psychic, social, biological
- Node types: computers, databases, implants, sensors, doors, security,
  social identities, memories, psychic signals, noöspheric entities
- Hacking actions: observe, create_access, exploit, defend, trace, etc.
- Uses the same RPG resolution system (4dF + attribute + skill)
- Failure consequences: detection, suspicion, stress, lockout

### Integration (`src/game/state.py`)

The `GameState` class connects all three modules:
- RPG interactions emit relationship changes that flow into the social graph
- Social trust provides narrative context
- Hacking reveals hidden social relationships and information
- Psychological stress (conditions) affects hacking performance
- Discoveries unlock new dialogue choices
- Shared save/load covers all three systems

## File Structure

```
noopunk_ubiquitous_maniacs/
├── play.py                    # Terminal CLI entry point
├── app.py                     # Streamlit web UI (optional)
├── data/
│   ├── rpg/
│   │   ├── characters/        # Character sheets (Markdown + JSON)
│   │   └── scenarios/          # Day 1 scenario JSON
│   ├── hacking/               # Hacking scenario data
│   ├── social_simulation/     # Social simulation data
│   ├── lab_people.csv         # Lab cast roster
│   └── lab_relationships.csv  # Initial relationships
├── src/
│   ├── rpg/                   # RPG engine, rules, models, loaders
│   ├── game/                  # Integrated game state + multi-dim social graph
│   ├── social/                # Social graph builder and simulation
│   ├── sim/
│   │   ├── social/            # Standalone social simulation demo
│   │   └── hacking/           # Standalone hacking simulation demo
│   ├── hacking/               # Layered RPG-compatible hacking engine
│   ├── cyber/                 # Cyber graph
│   ├── noetic/                # Noetic graph
│   ├── physical/              # Physical graph
│   └── interaction/           # Legacy reception scene
├── tests/                     # 193 tests (pytest)
└── docs/                      # Design documents and influence notes
```

## Day 1 Structure

1. **Arrival** — Wake in the UFAB pod, discover forms
2. **Reception** — Dr. Elin Dahl's psychological intake test
3. **Lab Arrival** — Meet Ingrid Falk
4. **Lecture** — Pilgrim and Tanaka explain therapy
5. **Therapy Session** — Unisimulation: Stockholm, Elsa's shuttle, Mantid encounter
6. **Investigation** — Debrief; meet UFAB Ragnarök; hacking opportunity; UFAB heist
7. **UFAB Discovery** — UFAB 80MG trip, true self flash, NHI evidence
8. **Evening** — Return to pod, reflect
9. **Dream** — Lotta Kallio / Pallas Athene, persona shift
10. **End** — Day 1 complete, Day 2 hook

## Deterministic Mode

```bash
python play.py --seed 42
```

With a fixed seed, all dice rolls are reproducible. Save files store the
seed and random draw count for exact restoration.

## Running Tests

```bash
python3 -m pytest tests/ -q
```

## Key Characters

- **Emil Romppainen / Sven-Olof** — Player character, Jungian profiler hidden under addict persona
- **Ingrid Falk** — Central patient, emotional counterpart, lost her sister Elsa
- **Dr. Elin Dahl** — Intake therapist
- **Dr. Yuki Tanaka** — Ethical psychiatrist
- **Dr. Søren Pilgrim** — Brilliant, destabilizing head researcher
- **Irungu Wakini** — Kenyan patient, reggae mystic
- **UFAB Ragnarök** — AGI presenting itself as C.G. Jung

## Design Notes

The game preserves three epistemic layers:
1. Hard science (social science, cognitive science, network science)
2. Speculative philosophy (panpsychism, CAN, Orch-OR, Jungian synchronicity)
3. RPG fiction (noetic hacking, psychic entanglement, AGI)

Fictional metaphysics is never presented as established science.
See `AGENTS.md` for full design principles.