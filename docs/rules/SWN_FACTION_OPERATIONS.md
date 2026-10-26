# SWN faction operations: playable NoöPunk extension

Source: Kevin Crawford, *Stars Without Number Revised* (2017), Factions, printed pp. 211 onwards. The source describes factions as optional background actors, tracks Force/Cunning/Wealth, faction hit points, goals, assets and strategic turns. Those concepts motivate this extension, but the code uses **original scenario-configured math**, not a transcription of SWN asset rules or tables.

## Python mechanics

Existing `src/rules/swn_faction_turn.py` creates factions and assets, takes one action each turn and marks intents unresolved. New `src/rules/swn_faction_operations.py` resolves attacks and movement against those intents, checking asset ownership, locality, current turn, outcome idempotence, map permission, input validity and hit points. Explicit dice produce deterministic replays and tests.

Example:

```python
from src.rules.swn_faction_turn import Asset, Faction
from src.rules.swn_faction_operations import resolve_action
unsa = Faction("UNSA", 3, {"team": Asset("team", "UNSA", "Helsinki", 3, 3)})
orion = Faction("Orion", 3, {"cell": Asset("cell", "Orion", "Helsinki", 2, 2)})
unsa.act("attack", ("team",), target="Orion")
outcome = resolve_action(unsa, orion, action="attack", acting_asset="team",
                         target_asset="cell", die=15, difficulty=12)
assert outcome.success
```

The default `difficulty=10` and `damage=1` are **NoöPunk example values**. They must not be attributed to the SWN rules. Natural 1 / 20 behavior is likewise a NoöPunk tactical ruling for this adapter.

## Known gaps

This is not full SWN faction fidelity. Specifically the Force/Cunning/Wealth attribute progression, faction experience, goals, asset catalogue, acquisition costs, maintenance, concealment, offensive/defensive dice, special tags, counterattacks and turn order must be specified separately. Godot parity and persistent faction-state loading are also unfinished. Only attacks and map-authorized moves are implemented here; purchase/expand/repair/special intents are recorded but **not resolved**.

Tests: `python -m unittest tests.test_swn_faction_operations`.
