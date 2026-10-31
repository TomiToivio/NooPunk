# Authoritative agent instructions: MUD is primary (#950)

This is the default game target for general NoöPunk coding. Preserve the Godot legacy but do not develop parallel Godot features without explicit instructions. First finish tested CWN rules migration from Godot and the reference book, then a complete solo UNSA campaign and optional side quests, all **without LLM, other players or live GM**. Multiplayer, LLM agents/GM, Mesa and non-UNSA factions are follow-on features only.

For mechanics: update `docs/design/ISSUE_950_CWN_DELUXE_AUDIT.md`, conformance tests, and the tabletop `rulebook/WITHOUT_NUMBER_BASELINE.md` with every behavior change. Keep CWN baseline separate from NoöPunk mods. Do not commit copyrighted CWN Deluxe PDF/text. Agent instructions from #946/#897 about equal priority are superseded.

---

# AI contributor boundary: NoöPunk MUD

This directory is **NoöPunk MUD**, a Python Evennia application. It is NOT the Godot game. Do not change the Godot project, scenes, game kernels or images while working on MUD issues. Consult repository-root AGENTS.md for the CWN foundation lock (#897).

Core rules: Cities Without Number, with Stars Without Number additions only where authorized. Keep Noösphere, ontological stress, and ideological factions as overlays, never alternative dice mechanics.

Evennia is authoritative for multiplayer and persistent world state. LLM GM and NPCs may describe or *propose* actions; validated CWN/Evennia handlers alone execute them. Mesa is for coarse social/resource simulation, not deterministic rules adjudication. Never control human PCs through an agent, and do not let an AI mint resources, override a roll, or rewrite canon.

Changes in this folder should be testable with pure Python unit tests where possible. No secrets or hard-coded external LLM endpoints. Label any untested Evennia integration accurately.
