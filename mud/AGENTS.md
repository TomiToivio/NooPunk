# Canonical Finglish, no localizations (#996)

The NoöPunk MUD has **one canonical player-facing language: Finglish**. No separate Finnish, English or other localized editions. In player-visible UI, quests, narration, dialogue and future Concordia NPC/GM responses, agents write mostly English with occasional basic Finnish, appropriate contemporary Stadin slangi and context-specific Swedish/Russian/Chinese/other loanwords. Check the glossary and Tomi's authored text for register. Never translate, correct, replace or overwrite Tomi-authored Finnish/Finglish. Non-player-facing docs, internal prompts, code and rulebooks stay plain English. See `docs/FINNISH.md`. Use optional spoiler-safe dictionary help rather than language editions; don't change save IDs or require LLMs for the solo campaign.

# Authoritative agent instructions: MUD is primary (#950)

This is the default game target for general NoöPunk coding. Preserve the Godot legacy but do not develop parallel Godot features without explicit instructions. First finish tested CWN rules migration from Godot and the reference book, then a complete solo UNSA campaign and optional side quests, all **without LLM, other players or live GM**. Multiplayer, LLM agents/GM, Mesa and non-UNSA factions are follow-on features only.

For mechanics: update `docs/design/ISSUE_950_CWN_DELUXE_AUDIT.md`, conformance tests, and the tabletop `rulebook/WITHOUT_NUMBER_BASELINE.md` with every behavior change. Keep CWN baseline separate from NoöPunk mods. Do not commit copyrighted CWN Deluxe PDF/text. Agent instructions from #946/#897 about equal priority are superseded.

---

# AI contributor boundary: NoöPunk MUD

---

## Boundary, restated for this directory

This directory is the **default target** for new game work (#950) and it is **not** the Godot game. Nothing here
imports the Godot project, and the Godot project does not import this package; `tests/test_mud_godot_boundary.py`
enforces both directions. Canon data under `data/` is read-only input.

The MUD's CWN core is `nopunk_mud/cwn/`, which imports nothing from `src/rules` — the parity comparison lives at
the repository root (`tests/test_mud_cwn_parity_950.py`) so that the package stays installable on its own.

This directory is **NoöPunk MUD**, a Python Evennia application, and since #950 it is the
**default target** for new game work: the first deliverable is a complete single-player UNSA story with no LLM,
no Mesa and no other players. It is still NOT the Godot game. Do not change the Godot project, scenes, game kernels or images while working on MUD issues. Consult repository-root AGENTS.md for the priority order (#950) and the CWN foundation lock (#897).

Core rules: Cities Without Number, with Stars Without Number additions only where authorized. Keep Noösphere, ontological stress, and ideological factions as overlays, never alternative dice mechanics.

Evennia is authoritative for multiplayer and persistent world state. LLM GM and NPCs may describe or *propose* actions; validated CWN/Evennia handlers alone execute them. Mesa is for coarse social/resource simulation, not deterministic rules adjudication. Never control human PCs through an agent, and do not let an AI mint resources, override a roll, or rewrite canon.

Changes in this folder should be testable with pure Python unit tests where possible. No secrets or hard-coded external LLM endpoints. Label any untested Evennia integration accurately.

## Design workflow (#989)

Authored game content — days, characters, missions, interactions, storylines, locations, rules, encounters and events — is specified by Tomi in [`design/`](../design/) and implemented through the issue raised from each document. Read [`design/README.md`](../design/README.md) and the root [`AGENTS.md`](../AGENTS.md) section *DESIGN WORKFLOW* before implementing any of it: implement only what the document describes, one step at a time, and preserve Tomi's Finnish/Finglish verbatim.

## Vocabulary authority (#1000)

Read the repository-root [`GLOSSARY.md`](../GLOSSARY.md) before writing player-facing dialogue or
narration. It is the canonical list of Stadin slangi and NoöPunk terms: reuse what is there, propose
rather than coin, and do not invent attestations. Tomi's entries are immutable.
