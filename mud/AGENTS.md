# AI contributor boundary: NoöPunk MUD — the main game (#950)

This directory is **NoöPunk MUD**, a Python Evennia application, and since #950 it is the
**default target** for new game work: the first deliverable is a complete single-player UNSA story with no LLM,
no Mesa and no other players. It is still NOT the Godot game. Do not change the Godot project, scenes, game kernels or images while working on MUD issues. Consult repository-root AGENTS.md for the priority order (#950) and the CWN foundation lock (#897).

Core rules: Cities Without Number, with Stars Without Number additions only where authorized. Keep Noösphere, ontological stress, and ideological factions as overlays, never alternative dice mechanics.

Evennia is authoritative for multiplayer and persistent world state. LLM GM and NPCs may describe or *propose* actions; validated CWN/Evennia handlers alone execute them. Mesa is for coarse social/resource simulation, not deterministic rules adjudication. Never control human PCs through an agent, and do not let an AI mint resources, override a roll, or rewrite canon.

Changes in this folder should be testable with pure Python unit tests where possible. No secrets or hard-coded external LLM endpoints. Label any untested Evennia integration accurately.
