# Design documents: scoped agent instructions (#989, #993)

This directory contains Tomi's authored game-design specifications. **Read [README.md](README.md) first.** It is the *single source of truth* for the design workflow and all document-type meanings; this file adds agent operating instructions, not another workflow.

1. Tomi authors a design document in `design/`.
2. Tomi creates a GitHub issue based on that document.
3. Agents implement the specified document under that issue.

Before implementing **authored game content**, identify the **specific design file, issue, and in-scope/out-of-scope work**. Read the entire document. Implement only the current described step; do not preempt future designs. Follow detailed text exactly, and use creativity only for gaps the document leaves open. Raise consequential undefined canon decisions for Tomi rather than guessing.

**Author boundary:** Do not rewrite, translate, correct, or expand Tomi-authored Finnish/Finglish design and player-facing text. Do not edit design documents unless Tomi explicitly requests that edit. Agent-written development documents and tabletop rules are plain English. Player-visible MUD writing uses **one canonical Finglish language without localized editions**; agents generally write English-led Finglish, with occasional contextual slang. Consult [../docs/FINNISH.md](../docs/FINNISH.md) (#996) and [../GLOSSARY.md](../GLOSSARY.md) for language.

**Implementation boundary:** Implement in the Python Evennia MUD (`mud/`) by default (#950), retain the CWN core and modular overlays (#897), and keep tabletop rules, scenarios, and lore in sync as appropriate. Respect spoiler/knowledge gates. Test deterministic code changes and report anything not verified. Future LLM GM/NPCs do not replace the playable solo campaign.

**Manual review:** Check the author document, issue and scope; compare implementation to the precise text; verify Tomi's material remains unchanged, canonical Finglish conventions are used only for player-visible text, and matching tests/tabletop updates exist where relevant.

For **Day vs Storyline**, missions, random events, locations and other categories, consult the *definitions in README.md* rather than maintaining a second copy here.
