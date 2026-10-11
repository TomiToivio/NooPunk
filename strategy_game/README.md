# NoöPunk Strategy Game (separate experimental project)

Standalone **Python** framework for a proposed faction-leader narrative RPG, LaclauGPT-informed political simulator, and abstract faction-management strategy game. See [issue #282](https://github.com/TomiToivio/NooPunk/issues/282).

The three layers are represented as data only: `core.py` (leader, faction, asset, location, network, event), `political.py` (the Layer II vocabulary — Laclau/Mouffe demands, signifiers and their roles, articulations and frontiers, plus Castells' communicative modes), `provenance.py` (recorded origin, unknown by default) and `view.py` (the board view, plus `political_view(field)` which renders a `PoliticalField` passed in explicitly). Design records: [`docs/POLITICAL_SIMULATOR_SCOPE.md`](docs/POLITICAL_SIMULATOR_SCOPE.md), [`docs/POLITICAL_SIMULATION_DESIGN.md`](docs/POLITICAL_SIMULATION_DESIGN.md), [`docs/RULE_SYSTEM_RESEARCH.md`](docs/RULE_SYSTEM_RESEARCH.md).

**Important:** no game rules, turn engine, agent actions, resource economics, objectives, or canon are implemented. This directory does not change or replace the NoöPunk RPG. The strategy game maintains its own [RULEBOOK.md](RULEBOOK.md) and [research plan](docs/RULE_SYSTEM_RESEARCH.md).

[`political.py`](political.py) models Laclaudian articulations and Castellsian communication as containers only — no numeric scores, and no LaclauGPT import. It is deliberately **not** wired into `WorldState`: integrating the layers is a Gate D decision, so the rendering hook takes the field as an argument instead. See [the Gate B design proposal](docs/POLITICAL_SIMULATION_DESIGN.md).

## Run the empty-state demo
From repository root:

```bash
python -m strategy_game
python -m unittest discover -s strategy_game/tests -v
```

Only standard-library packages are required. The entrypoint displays the empty map/network view model as JSON. Later optional adapters may use NetworkX, Mesa, Ollama, Concordia and a map/UI framework after their designs are approved.
