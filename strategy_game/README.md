# NoöPunk Strategy Game (separate experimental project)

Standalone **Python** framework for a proposed faction-leader narrative RPG, LaclauGPT-informed political simulator, and abstract faction-management strategy game. See [issue #282](https://github.com/TomiToivio/NooPunk/issues/282).

The three layers are represented as data only: `core.py` (leader, faction, asset, location, network, event), `politics.py` (the Layer II political vocabulary — demands, signifiers, formations, frontiers, and relation layers on the same `NetworkEdge`), `provenance.py` (recorded origin, unknown by default) and `view.py` (the board view plus the Layer II panel). Design records: [`docs/POLITICAL_SIMULATOR_SCOPE.md`](docs/POLITICAL_SIMULATOR_SCOPE.md), [`docs/POLITICAL_SIMULATOR_MODEL.md`](docs/POLITICAL_SIMULATOR_MODEL.md), [`docs/RULE_SYSTEM_RESEARCH.md`](docs/RULE_SYSTEM_RESEARCH.md).

**Important:** no game rules, turn engine, agent actions, resource economics, objectives, or canon are implemented. This directory does not change or replace the NoöPunk RPG. The strategy game maintains its own [RULEBOOK.md](RULEBOOK.md) and [research plan](docs/RULE_SYSTEM_RESEARCH.md).

The additional standalone [`political.py`](political.py) vocabulary models Laclaudian articulations and Castellsian communication without numeric scores or importing LaclauGPT. It remains separate from the `WorldState`-integrated `politics.py` model pending explicit integration approval. See [the Gate B design proposal](docs/POLITICAL_SIMULATION_DESIGN.md).

**Global factions** — the seven authored paradigm factions (Accelerationists, Cyborgists, Critical, Butlerian Jihad, Confederacy Awakening, Orion/Grey networks, Normalcy Bloc) are recorded as author canon in [`docs/GLOBAL_FACTIONS.md`](docs/GLOBAL_FACTIONS.md) and [`data/global_factions.json`](data/global_factions.json), read by [`factions.py`](factions.py). Setting canon only: no simulation rules are implemented, and the roster defines no mechanics.

**Cyberspace and connectivity** — [`docs/CYBERSPACE_AND_CONNECTIVITY.md`](docs/CYBERSPACE_AND_CONNECTIVITY.md) records the three campaign periods (the internet still useful at game start, down during the NHI Crisis, and quarantined behind a Blackwall-like boundary afterwards), the connectivity classes and access paths, and the one check the acceptance criteria demand: whether an intrusion is *physically and logically possible*, before any skill roll. [`data/connectivity.json`](data/connectivity.json) holds the model, read by [`cyber.py`](cyber.py), with code contracts in [`tests/test_cyber_access.py`](tests/test_cyber_access.py). A Castellsian social edge is refused by name as an access path, a genuinely isolated system refuses every remote path in every era, and a mismanaged Safenet exposure stays distinct from the illegal old-Internet containment breach. No numeric rule.

**Faction creation** — [`docs/FACTION_CREATION.md`](docs/FACTION_CREATION.md) records the five ideological dimensions as *named qualitative positions* (an ordered scale only after playtesting), the typed shared tag vocabulary for faction and character cards, and NHI contact policy kept separate from per-polity diplomacy (issue [#346](https://github.com/TomiToivio/NooPunk/issues/346)). [`data/faction_creation.json`](data/faction_creation.json) holds the vocabulary and the Cosmist International template, read by [`faction_creation.py`](faction_creation.py), with contracts in [`tests/test_faction_creation.py`](tests/test_faction_creation.py). A doctrine is never read as a capability, a remote-viewing team is never a character's skill, and a pro-contact faction may hold a hostile relation toward a named polity without contradiction. It consumes the axes already declared in [`data/global_factions.json`](data/global_factions.json) rather than restating them, and computes no affinity or balance rule.

**NHI entities and first contact** — [`docs/NHI_CODEX_SCOPE.md`](docs/NHI_CODEX_SCOPE.md) records the scope of the NHI entity codex (issue [#348](https://github.com/TomiToivio/NooPunk/issues/348)): the four ontologies (Biologics, Noetics, Plasmoids, Constructs) as kinds of entity rather than factions, the knowledge registers kept apart, and the reveal progression. [`codex/`](codex/) holds the record types and the translation model, [`data/codex.json`](data/codex.json) the first entries, and [`docs/NHI_CODEX_RESEARCH_NOTES.md`](docs/NHI_CODEX_RESEARCH_NOTES.md) records which claims are verified against the L/L Research transcripts and which are NoöPunk invention. No entity is approved canon, and GM-only material is withheld by the code rather than by renderer discipline.

## Run the empty-state demo
From repository root:

```bash
python -m strategy_game
python -m unittest discover -s strategy_game/tests -v
```

Only standard-library packages are required. The entrypoint displays the empty map/network view model as JSON. Later optional adapters may use NetworkX, Mesa, Ollama, Concordia and a map/UI framework after their designs are approved.

## Long-term vision

The horizon this project is building toward — **one open-source indie Grand Strategy RPG with a God's-eye view**, one universe and two games, six zoom levels of one simulation, and the S0–S4 stage plan — is recorded in [`docs/design/VISION.md`](../docs/design/VISION.md) (issue [#309](https://github.com/TomiToivio/NooPunk/issues/309)). It is a **north star, not an instruction**: it authorizes no mechanics, canon or scope, and it does not change anything in this directory.

## NoöPunk: Global design alternative

The ultra-abstract worldwide Network Society / Luhmannian social systems / Laclaudian hegemony concept, political-simulator references, card/tabletop architecture options, illustrative crisis-turn walkthrough and preliminary bookkeeping analysis are documented in [`docs/NOOPUNK_GLOBAL_DESIGN.md`](docs/NOOPUNK_GLOBAL_DESIGN.md) ([issue #338](https://github.com/TomiToivio/NooPunk/issues/338)). This is a **design proposal only**, not approved gameplay rules, and does not replace the local-city scenario #322.

## Experimental NoöPunk: Global vertical slice (#338)

Run a **noncanonical** deterministic example from the repository root:

```bash
python -m strategy_game.global_slice
python -m unittest strategy_game.tests.test_global_slice -v
```

`global_slice.py` contains a deliberately small, **separate** demonstration of four text views (global city-hub map and typed network links, faction assets and agents, global political responses, mission/encounter choices), discoverable mission sites and agent-led resource activation. A crash investigation can discover an NHI installation; the archive infiltration can resolve nonviolently; abstract force-response is represented only as a possible mission choice. Randomness is seeded for reproduction and all skill/asset calculations are explicitly **illustrative**, not approved rules or balanced gameplay. The user cannot yet operate a general interactive campaign from this CLI: `demo()` runs a fixed illustrative sequence.

**Author approval still required:** final skill/TAG vocabulary, dice mechanism, difficulty scales, asset economy, political transitions, combat, encounter writing and comprehensive UI. The prototype does **not** change `WorldState`, canonical strategy `RULEBOOK.md`, the separate local-city slice, or the legacy RPG. See [issue #338](https://github.com/TomiToivio/NooPunk/issues/338).
