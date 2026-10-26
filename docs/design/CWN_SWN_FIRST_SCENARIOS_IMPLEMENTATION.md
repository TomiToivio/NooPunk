# CWN-first scenario rules implementation ledger

**Authority:** CWN governs all general mechanics. SWN Revised supplies psionics, WWN supplies otherworld exploration, AWN supplies crisis-zone survival. See [Without Number baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md).

**Rights and attribution:** The PDFs furnished for design reference are commercial publications; they are not permission to republish their prose, art, tables, or catalogues. This repository records original explanatory text and interoperable numerical mechanics only. Consult a legitimately obtained copy for complete source-specific ability descriptions, character packages, price/equipment tables and exceptions. Do not ingest the source PDFs into public game assets.

## Status by subsystem

| Rules surface | Authority | Implementation status and next gate |
| --- | --- | --- |
| Attributes, modifiers, skill checks, saves | CWN pp. 4–31 | Python `src/rules/wn_core.py`; Godot `rules_adapter.gd`; verify all edge cases |
| Character backgrounds, contacts, Edges, Foci | CWN pp. 4–26 | Tabletop baseline only; requires data contract and Godot character builder |
| Initiative, actions, movement, attack, grappling | CWN pp. 32–39 | Not a complete Godot combat implementation |
| HP, trauma, injuries, healing and strain | CWN pp. 32–43 | Not a complete Godot injury implementation |
| Cyberware, drugs, drones and vehicles | CWN pp. 48–89 | Equipment and effects not fully ported |
| Hacking programs, defenses, actions | CWN pp. 90–105 | Not a complete Godot hacking implementation; NoöPunk ubiquitous-network lore is fictional context |
| Mission rewards, Heat, reactions and NPCs | CWN pp. 132–195 | Requires encounter and mission integration |
| Six psychic disciplines and Effort lifecycle | SWN Revised pp. 29–43 | `src/rules/psionics.py` + `godot/core/psionics.gd` (supersedes #648's module, see [PSIONICS_SUPERSESSION_648](../rules/PSIONICS_SUPERSESSION_648.md)): **pool, lifecycle, snapshot/restore, training gate and torching implemented** |
| Psychic technique prerequisites, effects, overexertion | SWN Revised pp. 29–43 | SWN's own technique list is **not reproduced** (no verified SRD licence). A provisional NoöPunk catalogue lives in `data/rules/psionics_techniques.json`; a table with the book should use its effect text |
| Otherworld exploration | WWN pp. 38 onward | Activate in special sites with explicit WWN procedure |
| Crisis zones, hazards, supplies, enclaves | AWN pp. 36 onward | Activate for hazardous districts; no second HP/XP system |

## Playable scenario integration plan

1. **CWN character sheet first.** Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma, ordinary CWN skills, level, Edges/Foci, two Armor Classes, HP, attacks, saves, System Strain, gear, cyberware and XP. No replacement PSY or CYB attributes.
2. **Psychic character package.** Only a properly acquired SWN Psychic/Partial Psychic package can grant discipline ranks or techniques. No automatic free psychic powers for all investigators. Natural ability is the setting explanation; package access is a game-rule gate.
3. **PSI interfaces.** SWN technique IDs, minimum ranks, authorized package, target rules, duration and Effort commitment types are implemented in `src/rules/psionics.py` and `godot/core/psionics.gd`; the first-scenario techniques are audited in `data/rules/psionics_techniques.json`. The gate runs before the dice, and a refused technique spends nothing.
4. **First cases.** Telepathy: consent-based mental contact; Precognition: uncertain forewarning; Biopsionics: medically accountable aid; Metapsionics: detection/defence. Telekinesis and Teleportation remain available to characters with legal prerequisites, not automatic opening powers. Specific mechanical effects must come from the relevant source entries.
5. **Regression tests.** Verify deterministic dice, no double spend, scene/day recovery, save/reload, skill prerequisites, class-package authorization, Godot headless import and a scenario playthrough with evidence and psychic consequences.
6. **Complete CWN backlog.** Implement and test the **entire** CWN subsystems listed above, including advancement, Edges, Foci, combat, Trauma, cyberware, hacking, drones, vehicles, NPCs and mission procedures. Mark each as complete **only after** end-to-end playthrough coverage, not merely a rulebook reference.

## System boundaries

SWN Effort is a dedicated finite resource, not an additional hit-point track. Use the higher Wisdom/Constitution modifier, highest trained psychic discipline and the baseline 1-point allotment for capacity. A point committed for a scene remains unavailable until that scene ends; a daily commitment remains unavailable until rest. Continuous abilities must be actively released. The author is free to revise these rules later, but the first scenarios use the source-defined procedures. The generic `natural_psi.py` implementation still reflects an earlier, incompatible 1d10 prototype and **must not** be silently used as the source of the new character's dice or Effort.

**Source edition anchors:** Cities Without Number (2023), Stars Without Number Revised (2017), Worlds Without Number (2021), Ashes Without Number (free edition 2025). Page references above are printed page numbers, not PDF viewer indices.
