# NoöPunk Strategy Game (separate experimental project)

Standalone **Python** framework for a proposed faction-leader narrative RPG, LaclauGPT-informed political simulator, and abstract faction-management strategy game. See [issue #282](https://github.com/TomiToivio/NooPunk/issues/282).

**Important:** no game rules, turn engine, agent actions, resource economics, objectives, or canon are implemented. This directory does not change or replace the NoöPunk RPG. The strategy game maintains its own [RULEBOOK.md](RULEBOOK.md) and [research plan](docs/RULE_SYSTEM_RESEARCH.md).

**Layer II (political simulation)** has an abstract vocabulary in [`political.py`](political.py) — demands, signifiers and their roles, equivalential articulations, antagonistic frontiers and communicative ties, taken from Laclau/Mouffe and Castells as *theory*. It imports **no LaclauGPT** and stores **no numeric quantity**, both asserted by tests. The proposed but unapproved play loop is in [docs/POLITICAL_SIMULATION_DESIGN.md](docs/POLITICAL_SIMULATION_DESIGN.md).

## Run the empty-state demo
From repository root:

```bash
python -m strategy_game
python -m unittest discover -s strategy_game/tests -v
```

Only standard-library packages are required. The entrypoint displays the empty map/network view model as JSON. Later optional adapters may use NetworkX, Mesa, Ollama, Concordia and a map/UI framework after their designs are approved.
