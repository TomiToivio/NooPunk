# CWN/SWN vanilla baseline — decision record (#848)

**Status:** authoritative. Supersedes the blank-rulebook / custom-attribute restart (#827, #835 and
follow-ups) and any NoöPunk-specific rule modification.
**Measured:** 2026-10-30 against `origin/main`.

## Handoff block (copy into every related PR and child issue)

**Baseline commit SHA:** `36092a5` (`origin/main` at the time of measurement — re-resolve before starting
work, and never treat a historical SHA as a licence to roll the whole repo back)
**Canonical rulebook:** `rulebook/` — entry point `rulebook/00_INDEX.md`, orientation `rulebook/00_START_HERE.md`
**Canonical Godot project:** `project.godot` (repository root)
**Canonical startup scene:** `res://scenes/main.tscn`
**Rules authority:** vanilla **CWN primary**, vanilla **SWN Revised** where CWN has no equivalent
(psionics), subsystem boundaries documented below
**Superseded instructions:** #827 (blank restart), #835 (UNSA seven-attribute sheet), #821 (typed tag
system), and any AGENTS/START_HERE guidance pointing at `noopunk/`
**Verified behaviors:** `godot --headless --path . --script res://godot/tests/run_tests.gd` →
**760 checks, 0 failed**; `godot --headless --path . --import` → rc 0

## What this means concretely

1. **Rules are vanilla.** STR/DEX/CON/INT/WIS/CHA; CWN character creation, classes, skills, 2d6 skill
   checks, d20 attacks and saves, combat, equipment, cyberware, hacking, progression; SWN Revised
   psionics including its class and discipline rules. No seven-attribute Fitness/Reflexes/Cognition/
   Cyber/Awareness/Agency/Empathy system, no alternate difficulty ladder, no reskin, no narrativist
   replacement.
2. **Subsystem boundaries** must be named whenever both books have an opinion. CWN governs unless the
   subsystem is psionics, where SWN Revised governs. Where CWN is silent and SWN covers it, say so
   explicitly in the implementing module docstring and in the coverage matrix.
3. **One game.** A 2D top-down Godot RPG with turn-based tactical play, source-faithful hacking and PSI.
   The root `project.godot` is that game. No parallel prototype, no action-RPG or first-person redesign,
   no invented minigame standing in for a CWN procedure.
4. **Nothing is deleted.** The restart work stays on disk as archived reference until Tomi reauthorizes
   it; deletion requires an audited migration, not a cleanup impulse.

## Audit of `main` (measured, not assumed)

| Path | What it is | Status |
|---|---|---|
| `project.godot` + `godot/` (134 files) | the top-down CWN RPG; 77 CWN rule/engine modules; `godot/tests/run_tests.gd` | **canonical** |
| `src/rules/cwn_*.py` (20+ modules) | engine-neutral CWN procedures shared by tabletop and game | **canonical** |
| `rulebook/` (00_INDEX.md, 10_SINGULARITY_CRISIS.md, 11_ONTOLOGY.md, …) | the tabletop book | **canonical** |
| `noopunk/` (game + rulebook) | the blank restart from #827; custom seven attributes from #835 | **archived — reference only** |
| `src/rules/noopunk_tags.py`, `data/rules/noopunk_tags.json`, `godot/core/noopunk_tags.gd` | the #821 tag model | **archived — reference only** |
| `src/rules/party.py`, `src/rules/field_agent.py` | party roster (#806) and agency generator (#809) | archived; the party *structure* may be reusable, the attribute content is not |
| `strategy_game/` | the NoöPunk × LaclauGPT crossover game (separate, per #306) | **unaffected by this decision** |

## Migration tasks, in order

1. **Freeze, don't delete.** `noopunk/README.md` and `noopunk/rulebook/RULEBOOK.md` now carry a
   superseded banner. No new work targets `noopunk/`.
2. **Resolve the conflicting guidance.** `AGENTS.md` carries the CURRENT DIRECTIVE at the top; any agent
   doc that still points at `noopunk/` or the seven attributes is contradicted there.
3. **Triage open work** produced under the custom direction: mark superseded, port compatible assets
   (tests, scenes, UI plumbing) only where they do not carry custom mechanics.
4. **Close the coverage gap honestly.** `docs/CWN_COVERAGE_MATRIX.md` records what is implemented; the
   known hole remains CWN Verbs/Subjects/programs/CPU slots/Access costs, and `rules_adapter.gd` has no
   hacking call.
5. **Verify chapter-by-chapter** against the SRD before claiming completion, and keep the licensing
   boundary: CWN's SRD permits verbatim transcription including tables with citation; the commercial
   book's setting material remains reserved.

## What must not be claimed

No agent may state that the rule system is complete on the strength of a passing suite alone. The suite
proves the implemented procedures behave as specified; coverage against the books is a separate,
documented measurement.
