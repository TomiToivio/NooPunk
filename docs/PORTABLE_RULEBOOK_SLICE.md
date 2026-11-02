# NoöPunk tabletop/console parity: first investigation slice

**Status:** original *rules-neutral narrative prototype*, not an implementation of any published CWN/SWN/WWN/AWN mechanical chapter. Use the published Cities Without Number rules for real character creation, skill tests, combat, and other underlying procedures. No original published mechanics are changed or reproduced here.

## Solo tabletop case: The Missing Ward (UNSA)

You need paper, a pencil and this sheet. Play as a UNSA rookie. Start at **UNSA HQ**. Your goals are to investigate an anomaly at the hospital and optionally complete the library sidequest. No GM or digital tools are required. No dice are needed for this preliminary narrative sequence (future mechanical encounters must follow the original CWN rules).

Track: **Current location** (HQ, hospital, library), **clues** (anomalous clock; witness statement), **library sidequest** (open/done) and **case** (open/closed).

- **HQ**: Ask for a briefing: Inspector Romppainen assigns the anomaly report. You can travel to the hospital or library.
- **Library**: Catalogue the record: mark the sidequest **done**; discover the missing ward's former name. Return to HQ.
- **Hospital**: Examine the room to record **anomalous clock**. Interview the witness to record **witness statement**. Each clue can be collected only once. Return to HQ as desired.
- **Conclude** (at hospital): If both clues are collected, close the case and submit an UNSA anomaly report. Otherwise continue investigating. Once closed, this slice ends.
- **Save/load by hand**: Copy the four tracking fields above to your character sheet; restore them to resume. Digital save serialization is versioned JSON, not a new tabletop mechanic.

## Rule-to-code traceability

| Tabletop rule/procedure | Python implementation | Test | Status |
| --- | --- | --- | --- |
| HQ/hospital/library travel | `portable_noopunk.campaign.Game.apply` | `test_case_and_sidequest_and_save_roundtrip` | Implemented |
| Two independent clues before concluding | `Game.apply` | `test_case_and_sidequest_and_save_roundtrip` | Implemented |
| Optional library record sidequest | `Game.apply` | `test_case_and_sidequest_and_save_roundtrip` | Implemented |
| Duplicate clues have no effect | `Game.apply` | `test_repeated_actions_do_not_duplicate_clues` | Implemented |
| Cross-interface action/result parity | `portable_noopunk.adapters.LocalAdapter` | `test_same_actions_same_results` | Implemented for two headless entry paths |
| Adapter save/load and read-only snapshots | `LocalAdapter.load/snapshot` | `test_save_round_trip_and_action_validation`, `test_snapshot_is_copy` | Implemented |
| Portable campaign state | `Game.to_json/from_json` | `test_case_and_sidequest_and_save_roundtrip` | Implemented |
| CWN full character creation/combat/skills | Existing published CWN rules; migration audit needed | Canonical examples needed | **NOT IMPLEMENTED BY THIS SLICE** |
| SWN/WWN/AWN additional systems, modifiers, Tarot | Separate future modules | Not yet | Deferred |

## Architecture and run instructions

The Python slice depends only on the standard library. `portable_noopunk.campaign` owns state/action resolution. `portable_noopunk.console` is a disposable thin frontend. Existing Evennia logic is untouched. `portable_noopunk.adapters.LocalAdapter` is the engine-neutral adapter facade: it dispatches validated actions, returns the legal action list, supports portable save/load, and exposes copied state snapshots. Both direct Python play and adapter play must produce identical outcomes for the same action sequence. Future Evennia/Concordia/Pygame adapters should translate framework input/output through this interface, never duplicate mechanics. LLMs cannot circumvent `available_actions`.

Run from repository root:

```bash
python -m portable_noopunk.console
python -m unittest discover -s tests -p 'test_portable_*.py'
# Optional package install: python -m pip install -e .
```

**Every new rule or mod must update both the tabletop rulebook and shared Python code in one PR**, with matching manual procedures, tests and a rule-to-code mapping. Avoid claiming complete book-rule parity until independently audited. See `docs/DESIGN_PRINCIPLES.md` and issues #1053 and #1054.
