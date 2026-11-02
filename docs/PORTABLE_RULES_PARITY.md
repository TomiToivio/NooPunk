# Portable rulebook ↔ Python contract (#1053, #1054)

## Scope and current status

This is an **incremental extraction**, not a claim that the published
CWN/SWN/WWN/AWN rules are comprehensively implemented. CWN remains immutable;
SWN/WWN/AWN are optional source-specific modules. Do not alter or paraphrase
licensed source rules into a replacement open rulebook.

The existing pure-Python CWN implementation lives at
`mud/nopunk_mud/cwn_core.py` and its companion `mud/nopunk_mud/cwn/`.
`mud/nopunk_mud/solo_campaign.py` implements an original GM-less UNSA prologue.
The `portable.py` layer wraps **existing** transitions and checks rather than
copying or modifying CWN calculations. `portable_cli.py` is a plain-terminal
reference adapter. Evennia, Concordia and Pygame integrations remain future
tasks; no claim of tested cross-adapter parity yet.

## Traceability matrix (first slice)

| Tabletop reference / mechanic | Canonical Python owner | Test | Status |
|---|---|---|---|
| CWN skill check (published rule; see `rulebook/WITHOUT_NUMBER_BASELINE.md`) | `mud/nopunk_mud/cwn_core.py:skill_check` | `mud/tests/test_portable_1053_1054.py::test_published_check_delegation` | Existing implementation, delegation tested |
| Original NoöPunk UNSA investigation actions and location conditions | `mud/nopunk_mud/solo_campaign.py:advance` | `test_complete_and_save_resume`, `test_invalid_actions_do_not_mutate` | First playable prologue |
| Portable commands, state and results | `mud/nopunk_mud/portable.py` | `test_complete_and_save_resume` | Initial application contract |
| Offline text console | `mud/nopunk_mud/portable_cli.py` | Manual script command below | Initial adapter, not full campaign |
| SWN psionics, WWN, AWN, richer mods | Existing modules, audit pending | Coverage matrix pending | Not certified by this change |
| Evennia/Concordia/Pygame adapters | To be implemented | Future parity fixtures | Deferred |

## Paper-play equivalent of the current prologue

With a character sheet and the published CWN book, start at the UNSA
safehouse. Accept the assignment. At Kurvi, interview a witness and mark the
**witness** clue, or at the University of Helsinki consult records and mark the
**records** clue. Return to the UNSA safehouse with at least one clue and
report. Submit to complete **Missing Researcher**. These are original
adventure transitions, not new CWN dice rules. The current lightweight
prologue includes no compulsory skill roll or combat.

Run with no GM, LLM or network:

```sh
cd mud
python -m nopunk_mud.portable_cli --script "accept hq;interview kurvi;report hq;submit hq"
python -m unittest discover -s tests -p 'test_portable_1053_1054.py'
```

## Review and release gate

Every change to a playable rule or mod must include in **the same PR**:
(1) matching tabletop procedure/rulebook section, (2) Python implementation,
(3) automated golden example, (4) an updated matrix row including source
edition and implementation status. Do not modify published CWN mechanics.
All user-interface adapters call this same domain API. Check reproducibility,
versioned save migration and license limits before a release.

**Next:** audit existing Python modules, avoid duplicate mechanics, extract
packaging and data dependencies from repository-relative paths, extend the
case with side quests and actual gameplay tests, then implement the Evennia
adapter. Concordia/Pygame and SWN faction strategy follow only after an
offline solo campaign is fully playable.
