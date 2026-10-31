# NoöPunk MUD (issue #946)

**This is the separate Python/Evennia MUD, NOT the NoöPunk Godot game.** Same setting, scenarios, canonical CWN rules and optional overlays; different runtime, commands, persistence and tests. Do not edit `godot/`, `project.godot`, `scenes/` or canonical rules to implement MUD features.

## Quick start

Requires Python 3.12+ and a compatible Evennia release.

```sh
cd mud
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
evennia migrate
evennia start
```

Use Evennia's browser client at http://localhost:4001 or a telnet client at localhost:4000. Create two separate accounts to test concurrent presence. **Not validated on a running Evennia server in this PR.** Evennia owns durable character/room state; the game setup hook seeds three connected Helsinki rooms once.

Commands: `look`, `say`, `north` / `south` / exits, `sheet`, `check <skill>=<difficulty>`, `supplies`, `scavenge`, `unsa`, `faction`, `talk <npc>`. Standard Evennia multiplayer communication and connection commands remain available.

## Architecture contract

- `server/`, `commands/`, `typeclasses/`, `world/`: **Evennia only**; persists authoritative rooms, characters and faction inventory.
- `systems/cwn.py`: a **small verified CWN skill-check slice** (2d6 + skill + attribute modifier against difficulty), not a complete CWN implementation. CWN's remaining character creation, combat, hacking, equipment and progression are future work.
- `systems/agents.py`: bounded, provider-neutral Concordia-*style* narration and validated intents; no dependence on Concordia internals and no LLM controlling player characters.
- `systems/simulation.py`: optional Mesa resource agents, emitting proposals only. World mutations must be applied separately by validated Evennia code.
- `world/seed.py`: starter Helsinki, UNSA safehouse and NPC. The Noösphere / ideology system is deferred as an optional overlay.

**Authority:** Never treat LLM prose or Mesa events as CWN rolls or inventory mutations. Players choose actions. The MUD and Godot share **specification and canon**, not runtime classes. MUD agents must read `mud/AGENTS.md` before changing code.

## Current scope

This PR provides an isolated playable-text vertical-slice scaffold and unit-tested pure mechanics/contracts. Survival, GM, NPC and Mesa integration are intentionally minimal, not a claim of full #946 acceptance. The first faction is UNSA; rogue factions and player-founded organizations come later.
