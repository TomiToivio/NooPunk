# Development Notes — Noöpunk: Ubiquitous Maniacs, playable campaign

Päivitetty: 12. elokuuta 2026

## Completed Features

### RPG Engine (`src/rpg/`)
- 4dF resolution system with 5 outcome tiers (critical success → catastrophic failure)
- 7 canonical attributes: Intelligence, Awareness, Reflexes, Body, Charisma, Willpower, Cybernetics
- 24 Transhumanity's Fate skills with validation
- Data-driven scenes, dialogue, and interactions loaded from JSON
- Aspects, conditions, consequences, stunts
- Unified action API: Overcome, Create Advantage, Attack, Defend
- Save/load with deterministic seed restoration
- NPC creation helper
- Conflict resolution system
- Astral projection mechanics
- PSI/psychic action system
- Psychosurgery session model
- Faction and project tracking
- Graph effect system for cross-module communication

### Social Simulator
- **Multi-dimensional graph** (`src/game/social_graph.py`): 6 dimensions (trust, attraction, fear, suspicion, authority, familiarity)
- 7 Day 1 characters with goals, mood, and memory
- Hidden relationships that can be revealed through play
- Change history with turn tracking
- Full serialization/deserialization
- Deterministic NPC autonomy turns: mood + goals + directed relationships produce auditable relationship changes and persistent NPC memories
- **Legacy single-value graph** (`src/social/`): CSV-driven, GEXF export, DOT output
- **Standalone simulation demo** (`src/sim/social/`): ambient dynamics, gossip spread, player interactions

### Hacking / Psychotronic Simulator
- **Layered RPG-compatible engine** (`src/hacking/layered.py`): 4 operational layers (cybernetic, psychic, social, biological)
- Hacking actions: observe, create_access, exploit, defend, create_advantage, overcome, attack, retreat
- Access levels: observed → contact → access → privileged → control
- Hacking tools with layer/action permissions
- Transfer system for flowing hacking results back into RPG state
- **Sleeping Patient scenario** (`data/hacking/sleeping_patient.json`): 15 nodes, 16 edges, 3 objectives
- **Standalone hacking demo** (`src/sim/hacking/`): graph manipulation sandbox
- **Day 1 hack_terminal interaction**: hack Ragnarök's terminal during investigation scene

### Integration (`src/game/state.py`)
- `GameState` class bridges RPG session + social graph + hacking state
- RPG relationship changes automatically flow into multi-dimensional social graph
- Relationship-changing choices create structured, deduplicated NPC memories
- NPC memories persist through save/load and appear in the terminal social view
- Hacking module unlocks based on RPG information discovery
- Character ID mapping between RPG and social graph
- Full integrated save/load (RPG + social + hacking in one file)
- 18 integration tests

### Terminal CLI (`play.py`)
- Interactive text-based play
- Commands: number (choose), s (social), i (info), c (character), h (hacking), save, quit
- Scene rendering with dialogue and NPC speech
- Skill check display (dice, attribute, skill, total, difficulty, margin, tier)
- Save/load support
- Deterministic seed support

### Streamlit UI (`app.py`)
- Web-based visualization
- Social graph, cyber graph, noetic graph, physical graph tabs
- RPG session renderer
- Versioned integrated Day 1 save/load preserves RPG, live social, and layered hacking state
- Backward-compatible loading for legacy RPG-only Day 1 saves
- GEXF export for Gephi

### Day 1 Scenario (`data/rpg/scenarios/day_1.json`)
- 11 scenes covering full Day 1 arc
- 63 interactions total (including new hack_terminal)
- 23 dialogue nodes
- Meaningful choices affecting relationships, knowledge, suspicion, stress
- Branching but convergent structure (choices alter state, not storylines)
- Terminal scene with Day 2 placeholder
- Content status: playable draft with replaceable placeholder prose

### Character Data
- `romppainen_narkkari.md` — Day 1-2 Narkkari persona (25 skill points, 7 attributes)
- `romppainen_day_1.md` — Day 1 alternate character with suppressed identity
- `demo_operator.md` — Demo character for testing

### Testing
- 445 tests, all passing
- 20 hacking console tests (test_hacking_console.py)
- Happy path and alternate path through Day 1
- End-to-end Day 1 → Day 2 campaign, completion and reload coverage
- State persistence (save/load round-trip)
- Rejected saves are transactional and cannot mutate the supplied character
- Integrated save-version validation and automatic Day 2 scenario resolution
- Social graph serialization is idempotent, including canonical NPC-memory tags
- Seeded reproducibility
- Scenario structural integrity
- Module integration tests
- All 9 hacking actions reachable through terminal console

## Release scope and optional enhancements

- **Campaign**: Day 1 and Day 2 are playable as one persistent terminal campaign
- **Hacking UI**: Terminal CLI and Streamlit expose the layered hacking engine; visual graph navigation remains text- and table-based
- **Prose**: Scenario prose is a playable draft; human-authored `KIRJA.md` remains separate and untouched
- **Portraits**: No visual assets; text-only presentation
- **Irungu Wakini**: Character exists in the social graph; additional scenes are post-release content
- **Lotta Kallio**: Persistent social-graph node with directed relationships and memories
- **Sound/Music**: None
- **Animations**: None

## Known Limitations

1. **OneDrive sync**: Files may drift between writes and reads in WSL. Re-read files before patching if results seem inconsistent.

2. **Hacking integration depth**: The Day 1 RPG interaction and the optional Sleeping Patient investigation are still separate encounters. The terminal CLI exposes all 9 layered actions, tools, aspect invocation, and a text network map; Streamlit currently exposes the focused five-action investigation path (observe, create access, exploit, resonate, retreat).

3. **Social simulation autonomy**: Deterministic NPC turns are available through terminal command `n`; they remain player-triggered rather than real-time background agents.

4. **Two Day 1 scenario files**: `day_1_arrival_and_entanglement.json` is the release campaign path. `day_1.json` remains a tested legacy/extended scenario and is not selected by default.

5. **Two integration models**: Streamlit preserves its CSV-backed live social graph with a dedicated integrated save format, while the terminal uses `GameState` and its multidimensional social graph. Their persistence is complete, but the runtime models are not yet consolidated.

6. **Legacy files**: The 42 `-lh6-725-37563` agent backup copies were compared against their canonical counterparts and removed after confirming that useful changes were already merged or superseded.

## Recommended Day 2 Extensions

### High Priority
1. **Interactive hacking in terminal CLI**: ✅ DONE — Launch the layered hacking engine from `hack_terminal` interaction, with terminal-based node inspection and action selection
2. **Day 2 scenario**: ✅ DONE — Kiimaiset Poliisit: 5 scenes (Helsinki arrival → precinct → case → trauma → complete). Dramatic arc: poliisiparodia → ihmissuhderiski → trauma → psyykkinen valinta. 12 interactions, 25 tests.
3. **NPC autonomy**: ✅ DONE — deterministic social turns use goals, mood, and existing relationships; terminal command `n` shows the actions
4. **Persistent Day 1 → Day 2 campaign**: ✅ DONE — state, RNG position, social graph, hacking status and saves continue across the scenario boundary

### Medium Priority
5. **NPC memory system**: ✅ DONE — NPCs remember player choices and reference them in later scenes. `m` command in terminal CLI shows all NPC memories. Memory count visible in social network view.
6. **Psychosurgery scene**: Full psychosurgery session using `src/rpg/psychosurgery.py`
7. **Astral projection**: Use `src/rpg/astral.py` for dream/altered states sequences
8. **Conflict system**: Use `src/rpg/conflict.py` for the optional conflict requirement
9. **Irungu Wakini scenes**: Add reggae mystic to Day 2+ content
10. **Lotta Kallio social node**: ✅ DONE — persistent node, directed relationships and explicit memories

### Low Priority
11. **Web UI update**: Update `app.py` to use `GameState` integration
12. **Visual graph rendering**: Real-time graph visualization during play
13. **Music/Sound**: Ambient soundtrack for scenes
14. **Portrait art**: Character portraits
15. **Cleanup completed**: Agent-suffixed backup files were consolidated into canonical files and removed on 2026-08-02.

## Architecture Notes

The three epistemic layers are preserved:
1. **Hard science**: Network science, social graph theory, Fate RPG mechanics
2. **Speculative philosophy**: Panpsychism, CAN, Jungian archetypes, noosphere
3. **RPG fiction**: Noetic hacking, psychic entanglement, AGI as C.G. Jung

Fictional metaphysics (noetic hacking, psychic signals, NHI) is never presented
as established science. The game engine treats them as game mechanics, not
claims about reality.
