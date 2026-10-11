# NoöPunk Strategy Game (separate experimental project)

Standalone **Python** framework for a proposed faction-leader narrative RPG, LaclauGPT-informed political simulator, and abstract faction-management strategy game. See [issue #282](https://github.com/TomiToivio/NooPunk/issues/282).

The three layers are represented as data only: `core.py` (leader, faction, asset, location, network, event), `politics.py` (the Layer II political vocabulary — demands, signifiers, formations, frontiers, and relation layers on the same `NetworkEdge`), `provenance.py` (recorded origin, unknown by default) and `view.py` (the board view plus the Layer II panel). Design records: [`docs/POLITICAL_SIMULATOR_SCOPE.md`](docs/POLITICAL_SIMULATOR_SCOPE.md), [`docs/POLITICAL_SIMULATOR_MODEL.md`](docs/POLITICAL_SIMULATOR_MODEL.md), [`docs/RULE_SYSTEM_RESEARCH.md`](docs/RULE_SYSTEM_RESEARCH.md).

**Important:** no game rules, turn engine, agent actions, resource economics, objectives, or canon are implemented. This directory does not change or replace the NoöPunk RPG. The strategy game maintains its own [RULEBOOK.md](RULEBOOK.md) and [research plan](docs/RULE_SYSTEM_RESEARCH.md).

## Run the empty-state demo
From repository root:

```bash
python -m strategy_game
python -m unittest discover -s strategy_game/tests -v
```

Only standard-library packages are required. The entrypoint displays the empty map/network view model as JSON. Later optional adapters may use NetworkX, Mesa, Ollama, Concordia and a map/UI framework after their designs are approved.
