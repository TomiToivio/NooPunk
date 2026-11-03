# Engine independence: where the rules actually live (#1053, #1054)

> **Superseded:** [ISSUE_1053_ARCHITECTURE_SURVEY.md](/docs/architecture/ISSUE_1053_ARCHITECTURE_SURVEY.md) is the one document kept up to date for this
> subject. This file is kept as history — it is a second answer to a question that already had one,
> and the counts in it disagree with the audited ones. Do not update it; update the canonical file.


**Status: measured survey, not a migration plan.** Everything below was counted or executed in this
repository on 2026-11-02; nothing here moves a file.

The architecture decision says the gameplay rules must not depend on an engine, and that tabletop play must
work with pencils and dice. This document answers the question that has to come first: **which of those things
is already true, and where is the same rule implemented twice?**

## 1. What already runs without an engine

The console slice is real, not aspirational:

```
cd mud
python -m nopunk_mud.cli --campaign --script "go street,go university,examine terminal,go street,go kurvi,\
talk witness,ask witness badge,examine woman,go street,go safehouse,report"
→ Case filed: the researcher, the van, the second badge
  {"ending": "solved", "clues": ["access_log", "witness_badge"], "hp": 6, "turns": 11}
```

`tests/test_engine_independence_1053.py` runs exactly that in a subprocess whose environment contains only
`PATH` and `HOME`, and asserts three things: it reaches an ending, the same script produces byte-identical
output twice (no clock, no RNG drift), and importing the rules/campaign packages pulls **no** Evennia,
Django, Godot, Concordia, Pygame, Mongo or Redis module.

That gives #1053's Priority 0 a floor to build from rather than a blank page.

## 2. The inventory, counted

| What | Where | Size | Engine dependency |
|---|---|---|---|
| MUD CWN package | `mud/nopunk_mud/cwn/` (`__init__`, `combat`, `initiative`) | 3 modules | none |
| MUD CWN single-module core | `mud/nopunk_mud/cwn_core.py` | 17 functions | none |
| Python rules reference | `src/rules/` | 73 modules | none (pure Python) |
| Godot kernels | `godot/core/` | 52 scripts | Godot |
| Evennia-side rules slice | `mud/systems/cwn.py` | 1 module | Evennia tree |
| NoöPunk overlays (Godot) | `mods/noopunk/` | 4 scripts | Godot |
| NoöPunk overlays (MUD) | `nopunk_mud/{social,ideology,discourse_network,consciousness,case_consciousness}.py` | 5 modules | none |
| Deterministic campaign | `mud/nopunk_mud/campaign/` | engine + content | none |
| Tests | `tests/` 133 files, `mud/tests/` 25 files, `godot/tests/` | — | — |

## 3. The duplication this audit exists to expose

Counted, not guessed:

1. **CWN arithmetic exists in four places.** `mud/nopunk_mud/cwn/` (parity-tested against `src/rules/`),
   `mud/nopunk_mud/cwn_core.py` (a near-twin of the package: 17 functions each), `src/rules/` (the reference the
   parity test compares against), and `godot/core/` (52 scripts, maintenance-only). `mud/systems/cwn.py` is a
   *fifth*, partial slice used by the Evennia commands.
2. **Two discourse models landed within three minutes of each other**: `ideology.py` (#1046) and
   `discourse_network.py` (#1049). Different shapes — statements/positions/relationships with evidence kinds and
   visibility, versus profiles/communication/affiliation/alignment/snapshots — both persisted, both tested.
   `dossier` (#1052) builds on `ideology.py` because that is where the rule semantics live.
3. **Two campaign engines**: `campaign/` (the playable case, deterministic, tested) and `solo_campaign.py` (the
   earlier prologue behind the `case` command). Both run; they are not the same story.
4. **Overlays split across runtimes**: GUMSHOE and Noösphere exist as Godot overlays (`mods/noopunk/*.gd`) while
   the MUD has its own consciousness/ideology modules. The rules constitution's `full-noopunk` profile therefore
   cannot be assembled in one runtime today.

None of this is a bug report. It is the map #1053 asks for before anything moves.

## 4. What "tabletop-first" already satisfies, and what it does not

Satisfied: the rules that matter are arithmetic over explicit inputs and are exercised by tests; a human can
run the same procedures on paper; no rule requires an LLM, a database or a GUI.

Not satisfied, and not pretendable:

- **No printable artefacts.** There is no character sheet, no procedure sheet, no worked example block for the
  subsystems the slice uses. Tabletop parity is currently an argument, not a document.
- **No packaged distribution.** The MUD packages are importable only with `mud/` on `sys.path`; there is no
  `pyproject.toml` for a `noopunk-rules` distribution, so "importable, distributable Python packages" is not yet
  true.
- **No adapter layer.** Evennia commands call the model directly; there is no shared typed action/result/event
  vocabulary that a CLI, Evennia, Concordia and a hypothetical Pygame front end could all speak.

## 5. The smallest honest next steps

Ordered so each one is verifiable on its own:

1. **One CWN core, or a stated reason for two.** `cwn_core.py` and `cwn/` differ only in packaging; the parity
   test already proves their arithmetic agrees. Retire or re-export one.
2. **One discourse model.** A decision, not a merge: pick `ideology.py` or `discourse_network.py` and make the
   other a thin adapter, before more code learns both APIs.
3. **Printable procedure sheet** for exactly the subsystems the first case uses: attributes and modifiers, skill
   checks, saves, damage and strain, the GUMSHOE pool spend, and the Noösphere exposure step. One page each, with
   a worked example — the golden examples #1053 asks for.
4. **A typed action/result envelope** shared by the console and Evennia, with an adapter test that runs the same
   seeded scenario through both and compares outcomes.
5. **Package the rules** (`noopunk-rules`) once 1–4 have stopped moving.

Doing 4 before 1 and 2 would package the duplication.
