# NoöPunk MUD — the main NoöPunk game

A persistent, text-first, Python **Evennia** game set in the NoöPunk universe and resolved on the
canonical **Cities Without Number** rules. It is *not* the Godot game and shares no runtime with it:
Godot (`project.godot`, `godot/`) is the preserved graphical implementation, maintained only for
specifically scoped work. See
[`docs/design/ISSUE_950_MUD_IS_THE_MAIN_GAME.md`](../docs/design/ISSUE_950_MUD_IS_THE_MAIN_GAME.md).

**Phase 1 (current):** one human, no LLM, no other players — a UNSA investigation campaign in Helsinki.
**Phase 2 (later):** multiplayer, LLM NPCs/GM, Mesa population simulation, other factions.

## Run it

```bash
python3 -m venv .venv
.venv/bin/pip install -r mud/requirements-mud.txt

cd mud
PATH="$PWD/../.venv/bin:$PATH" evennia migrate
PATH="$PWD/../.venv/bin:$PATH" evennia start          # telnet 4000, web 4001
PATH="$PWD/../.venv/bin:$PATH" evennia stop
```

First start needs an owner account; in a non-interactive shell, give the launcher one:

```bash
EVENNIA_SUPERUSER_USERNAME=admin EVENNIA_SUPERUSER_PASSWORD=<something long> \
EVENNIA_SUPERUSER_EMAIL=admin@example.invalid evennia start
```

Then `telnet localhost 4000`, and use the connection screen's own verbs: `create <user> <password>`,
`connect <user> <password>`. A character is created on first login and placed in the neighbourhood.

## Commands the MUD adds

| Command | What it does | Rules authority |
| --- | --- | --- |
| `sheet` | six attributes, modifiers, trained skills, carried supplies | `src/rules/cwn_character.py` |
| `scavenge [simple\|significant\|expert]` | one Survival check, one consequence: a supply, or a worse room | `src/rules/wn_core.py` |
| `faction` / `faction join <name>` / `faction give <stock> [n]` | UNSA membership, reputation and stocks | `mud/world/factions.py` |

## Test it

```bash
cd mud
PATH="$PWD/../.venv/bin:$PATH" evennia test --settings settings.py tests     # 22 tests
python3 tools/probe_two_sessions.py                                          # live, needs a running server
```

## Where things live

| Path | What it is |
| --- | --- |
| `world/cwn.py` | the **only** place the MUD reaches the rules: it imports `<repo>/src/rules` and owns no arithmetic |
| `world/helsinki.py` | the neighbourhood, authored as data; `build()` is idempotent |
| `world/factions.py` | UNSA state: membership, roles, reputation, four stocks |
| `typeclasses/` | character (carries a CWN sheet), room (has power or not), exit |
| `commands/noopunk.py` | the three commands above |
| `tests/` | CWN sharing, the boundary (the MUD never imports Godot), the world, two humans |

The rules are **shared, not copied**: `tests/test_mud_cwn.py` asserts
`world.cwn.skill_check is rules.wn_core.skill_check` — identity, not equality, because two copies of a
formula pass an equality check right up until somebody edits one of them.

## Deliberately not here yet

A browser client, LLM narration, other factions, Mesa, and the single-player quest campaign. The
campaign is the next deliverable; everything above it is scaffolding for it.

## Licence and attribution

Evennia is BSD-licensed; its generated game directory is boilerplate and is kept as generated so the
framework's documented extension points stay where the framework expects them. Cities Without Number
material is referenced, never reproduced: the rules live in `src/rules/`, which is NoöPunk's own
implementation, and the compliance matrix records what is and is not covered.
