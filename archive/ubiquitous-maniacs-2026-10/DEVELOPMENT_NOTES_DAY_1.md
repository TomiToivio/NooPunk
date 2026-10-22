# Day 1 prototype — development notes

## Completed

- Complete playable route from screening to the Day 2 hook, with fail-forward outcomes.
- Fate/Fudge-inspired 4dF checks, aspects, conditions, consequences, skills and relationships.
- Live Day 1 social graph synchronization through portable `GraphEffect` records.
- Optional cybernetic–psychic–social–biological hacking investigation at the UFAB heist.
- Hacking consequences transfer back to the shared RPG state.
- JSON save/load with scenario validation and deterministic seed continuation.
- Streamlit panels for narrative actions, status, social graph, discoveries and hacking pressure.
- Automated route, rules, hacking, persistence and content validation tests.
- **Integrated `GameState` backbone** (`src/game/`) bridging RPG, social graph and hacking
  through one shared state object, driven by the terminal play mode `play.py`.
- **Multi-dimensional social edges**: the integrated graph (`MultiDimensionalSocialGraph`)
  tracks trust, attraction, fear, suspicion, authority and familiarity as separate directed
  dimensions per edge, with clamping (-100..100) and a change history.
- **Hidden / partially revealed relationships**: edges can be marked hidden and are filtered
  out of the player's view until revealed; the UI surfaces the hidden-edge count.
- **NPC goals, moods and memory** stored on each social node and exposed through
  `GameState.get_npc_state()` and the social panel.
- **Hacking state embedded in the save document**: `HackingState` (availability, attempts,
  successes, failures, alert level, discovered/hacked nodes) is serialized in `GameSave`
  and restored on load.
- **Terminal interface** (`play.py`) with deterministic `--seed`, `--load`, scene/status
  rendering, 4dF result reporting, and panels for social network, discovered info,
  character state and psychotronic status.

## Placeholders

- Some scene prose is explicitly marked replaceable in scenario `content_status` fields.
- The sleeping-patient hacking case is a reusable vertical-slice scenario, not final Day 1 canon.
- Portraits, sound, map art and bespoke graph visualization are intentionally absent.
- The standalone social simulator (`src/sim/social`) still uses a single aggregate
  relationship score; the integrated `GameState` path uses the multi-dimensional graph.
- The psychotronic status panel in `play.py` reports `HackingState` metadata; the full
  interactive four-layer `LayeredHackingSession` is currently exercised through the
  Streamlit investigation panel rather than the terminal loop.

## Known limitations

- NPC goals, moods and memory are stored and displayed but do not yet drive autonomous
  NPC turns or reactions within Day 1 (the spec notes full autonomy is not required yet).
- The interactive `LayeredHackingSession` snapshot is not yet persisted mid-investigation;
  `HackingState` metadata is saved, but an in-progress layered operation restarts after load.
- Inventory is currently represented by resources, flags and information rather than item instances.
- Streamlit is a prototype interface and has no accessibility or localization pass.
- The legacy single-value social graph (`src/social`, `src/sim/social`) coexists with the
  multi-dimensional graph; the two are not yet unified.

## Recommended Day 2 extensions

- Unify the legacy single-value social graph with `MultiDimensionalSocialGraph` and migrate
  the Streamlit `render_day_1` path onto the integrated `GameState`.
- Persist the complete layered-hacking snapshot and resume investigations mid-operation.
- Introduce Komisario Kallio and the Kiimainen Poliisi persona as state-dependent Day 2 nodes.
- Add NPC memory reactions to Day 1 choices and hacking detection (basic autonomous turns).
- Replace the reusable sleeping-patient case with a canon-specific Ingrid/Romppainen signal trace.
- Add inventory item models for UFAB 80MG, credentials and diagnostic tools.
- Surface the interactive four-layer hack in the terminal loop, not only the Streamlit panel.
