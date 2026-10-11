# NoöPunk Strategy Game (separate experimental project)

Standalone **Python** framework for a proposed faction-leader narrative RPG, LaclauGPT-informed political simulator, and abstract faction-management strategy game. See [issue #282](https://github.com/TomiToivio/NooPunk/issues/282).

**Important:** no game rules, turn engine, agent actions, resource economics, objectives, or canon are implemented. This directory does not change or replace the NoöPunk RPG. The strategy game maintains its own [RULEBOOK.md](RULEBOOK.md) and [research plan](docs/RULE_SYSTEM_RESEARCH.md).

## Run the empty-state demo
From repository root:

```bash
python -m strategy_game
python -m unittest discover -s strategy_game/tests -v
```

Only standard-library packages are required. The entrypoint displays the empty map/network view model as JSON. Later optional adapters may use NetworkX, Mesa, Ollama, Concordia and a map/UI framework after their designs are approved.
