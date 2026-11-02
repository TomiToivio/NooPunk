# NoöPunk interfaces: one library, multiple presentations (#1053, #1054)

**Binding dependency direction:** UI/engine adapter → portable NoöPunk Python game library. **Evennia is one optional MUD adapter, never the foundation for other UIs.** CWN remains immutable; selected SWN/WWN/AWN rules and optional NoöPunk mods belong in shared Python implementations, not client code.

## Working reference interfaces

The portable example campaign is an **original rules-neutral prototype**, not a complete CWN conversion. It already supports a headless session, an optional library-record side quest, two clues, completion, and versioned save/load.

From repository root (Python 3.10+):

| Interface | Run | Dependencies |
|---|---|---|
| Plain console | `python -m portable_noopunk.console` | Python standard library |
| Local browser | `python -m portable_noopunk.interfaces.web` then visit `http://127.0.0.1:8765/` | Python standard library |
| Illustrated browser starter | `pip install ".[web]"` then `python -m portable_noopunk.interfaces.nicegui` | NiceGUI |
| Enhanced terminal starter | `pip install ".[textual]"` then `python -m portable_noopunk.interfaces.textual` | Textual |

The standard-library web UI intentionally binds to **127.0.0.1 only** and keeps a single process-local shared session. It has **no authentication or multi-user isolation** and must not be deployed publicly. The NiceGUI/Textual implementations are minimal exploratory views, not claims of polished artwork or feature-complete clients.

## Next adapters (not yet implemented here)

- **Evennia MUD:** move/bridge the active MUD code to calls into a single authoritative Python rules and campaign package; preserve existing command behavior and save migration. Do not claim completion until parity tests demonstrate it.
- **Arcade 2D** (or existing Pygame): presentation of scene/map/sprites and tactical interaction on top of shared action results, never another rules implementation.
- **Ursina 3D**: optional later prototype.
- **Concordia:** agent/GM action proposer/integration, *not* an authoritative engine or a player-facing UI.

## Contract and acceptance

`portable_noopunk.campaign.Game` handles validation and game-state changes. `portable_noopunk.adapters.LocalAdapter` accepts commands, returns library `Outcome`, exposes legal actions and detached snapshots. Frontends may render text, buttons, images and maps, but must never decide clues, combat, CWN rolls or faction effects.

Run the core/adapter regression tests:

```bash
python -m unittest discover -s tests -p 'test_portable_*.py'
```

**Limitations:** Existing `src/rules`, `mud/nopunk_mud`, and `portable_noopunk` still contain multiple historical models. The authoritative CWN migration, comprehensive tabletop parity, a fully fledged single-player UNSA campaign and Evennia conversion are *not* completed by these UI samples. See `docs/design/ISSUE_1053_ENGINE_INDEPENDENCE_AUDIT.md`.

**Rulebook sync:** This patch only adds presentation behavior, so it adds no tabletop mechanics. If shared rules/mods change later, update the tabletop rulebook, code, coverage matrix and golden tests together.
