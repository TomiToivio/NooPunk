# RPG-first execution checkpoint for #516, #515, #506, #482, #470, #469, #468, #461

**Date:** 2026-10-19. **Status:** implementation checkpoint, not final author approval or an eight-issue closure claim.

## Authority and sequencing

The latest explicit approved decision takes precedence; this is not a blanket rule that an issue's numerical ID changes canon. The RPG priority is #516; #482 supplies the currently approved six-skill Fate *prototype*; #506 retains exactly one proposed strategic **science** rating, not a family of knowledge skills; #515 is optional and may not block the RPG. Older strategy-first procedures in #461/#468/#469/#470 are deferred. The latest three-playable-human-faction roster decision overrides older four-party proposals.

1. **RPG now:** one faction-leader PC, four agents in the roster, individual Fate checks with COG/INT/REF/SAV/SOM/WIL, GM-led clues, dialogue, PSI/cyber as permission-gated actions, meaningful player choices and save/reload. No global simulation or mandatory graphical map.
2. **Optional tactical later:** use the existing headless four-agent tile prototype; a chosen renderer may project the same state. No second combat/rules engine.
3. **Organization strategy later:** bring in turn orders, research capacity and a *single* science project clock; an NPC or facility can provide narrative context in RPG scenes before this system exists.
4. **Global strategy last:** use 2045 as the separate default strategic start, unordered 20XX backstory, three playable political factions, Reality Tunnels and NHI actors when the earlier playable layers are stable.

## Existing executable pieces to reuse

- `strategy_game/rpg/fate.py`, `scene.py`, `skills.py`: Fate 4dF kernel and broad individual skills (#482/#516).
- `strategy_game/rpg/investigation.py` and `investigation_cli.py`: a noncanonical playable choice-based case, optional seeded skill checks, save/reload (#516/#502).
- `strategy_game/tactical/`: a *headless* grid, interaction and outcome adapter; not a graphical battle game (#515).
- `strategy_game/campaign/missions.py`: mission report transfer by named inventories, without political arithmetic.
- `strategy_game/research_projects.py` or corresponding research package where present: strategic projects stay separate from the first RPG case (#506).

## Reproducible checks

From repository root:

```bash
python -m unittest strategy_game.tests.test_rpg_first_vertical_slice -v
python -m unittest discover -s strategy_game/tests -v
python -m strategy_game.rpg --text
python -m strategy_game.tactical --json
python -m strategy_game.rpg.investigation_cli --save /tmp/noopunk-example-case.json
```

The investigation CLI is interactive. Example commands: `party leader agent_1 agent_2 agent_3 agent_4`, `interview`, `protect`, `report`. The executable check above asserts persistence and a completed case but **does not** certify author-approved narrative quality or combat balance.

## Remaining gates by issue

| Issue | Next meaningful gate | Current interpretation |
| --- | --- | --- |
| #516 | Tomi decides final compact rules, action costs, mixed-success and combat lethality after a playtest | **Open**: never auto-canonize proposed rules |
| #515 | Author chooses renderer and evaluates movement/dialogue/optional conflict frontend | **Open**: spike only; defer until RPG works |
| #506 | Integrate one-science-rating strategic research clock with institutional capacity | **Open**, after RPG |
| #482 | Human approval of strategic skill list and remaining character allocation decisions | **Open**; Fate prototype implemented |
| #470 | Resolve outstanding faction lore and eventual global strategy mechanics | **Open**, later |
| #469 | Work Reality Tunnels into narrative scenes before modeling numeric hegemony | **Open**, later simulation |
| #468 | Review 2045 global starting scenario and five-character faction rosters | **Open**, later |
| #461 | Approve strategic mission vocabulary and five orders per strategy turn | **Open**, not a requirement for RPG scene turns |

## Acceptance honesty

The new regression test exercises one complete noncombat case, deterministic GM-triggered Fate checks, persistence and illegal-action refusal. It intentionally does **not** claim a full #516 tabletop playtest, battle calibration, Pygame tactical map, science tech tree, three-faction global simulator or completed/closed issues. Those are gated design and engineering deliverables, not reasonable consequences of merging this checkpoint.
