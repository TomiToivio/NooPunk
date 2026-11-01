# Mandatory MUD language rule (#980 and #981)

**Finnish (Finglish) is the official primary language of the MUD, but all agents MUST author ONLY English. Never create, translate, correct, or improvise Finnish UI, story, dialogue or examples. Tomi alone writes Finnish story/dialogue. Do not overwrite Tomi-authored Finnish.** The first playable build may intentionally contain 50% Tomi Finnish and 50% agent English (or any mix), without a localization-completeness gate. Show English draft text as fallback where Finnish is not yet available. A separately edited English localization comes later. Rulebooks and docs remain English. Read `docs/FINNISH.md` before working on player-facing content. Treat #980 and #981 as one workstream.

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
