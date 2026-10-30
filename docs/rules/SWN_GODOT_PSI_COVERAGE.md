# SWN Revised Deluxe psionics: Godot port status

Source: user-supplied *Stars Without Number Revised Deluxe* (2017), **Psionics**, printed pp. 29–43 (PDF pages 33–47). This module is a non-verbatim implementation of rules procedures, **not a redistribution of the book**.

## Implemented here

- `src/godot/swn_psionics.gd`: independently namespaced `SWNPsionics`, preserving existing NoöPunk provisional `NoopunkPsionics` as legacy.
- Full and Partial Psychic package validation, six disciplines and advancement authorization gates (source character creation summary pp. 4–5 and Psionics pp. 29–31).
- Maximum Effort, distinct active/scene/day commitments, duplicate-key checks, scene recovery and rest (p.31).
- Torching: limited to once per round, one extra point for the scene, source d6 attribute damage, terminal below-3 attribute check (p.31).
- Source-derived numeric core helpers: Psychic Succor recovery/System Strain calculation (p.32) and Personal Apportation distance thresholds (p.42). These are **not** a complete ability execution pipeline; targets, attack rolls, timing, terrain and side effects must be checked at the scene/combat boundary.
- Atomic versioned snapshot restoration and behavior tests (`tests/godot/test_swn_psionics.gd`).

## Missing to claim a complete SWN psionics system

| Area | Status |
|---|---|
| Psychic class/skill checks, training authorization | Implemented kernel; **not character-creation UI** |
| Full/partial package progression, discipline technique selection by level | Partial; level-up purchase accounting is external |
| Active/scene/day Effort and recovery | Kernel implemented |
| Torching and attribute consequences | Kernel implemented; scenario representation of feral psychic and death remains unimplemented |
| Biopsionics | Partial: numerical Psychic Succor only |
| Metapsionics | Technique-specific effects not implemented |
| Precognition | Technique-specific effects not implemented |
| Telekinesis | Technique-specific effects not implemented |
| Telepathy | Technique-specific effects not implemented |
| Teleportation | Range table only; no movement or destination legality |
| Core ability names, effects, learned technique catalogues | Not shipped as a fully verified playable catalogue |
| Rules-native combat integration | Not yet wired into Godot turn system |
| Case gameplay, UI, character sheet and save schema | Not yet wired into MVP campaign |
| Manual windowed playtest | Not verified |

**Important boundaries:** CWN remains the NoöPunk base chassis. SWN psychic access is optional and must be an authorized character choice. Detective Romppainen is not automatically a psychic. `data/rules/psionics_techniques.json` contains provisional **non-SWN** custom abilities and must not be treated as a vanilla SWN rules source. The official book's ability descriptions and illustrations are not copied to this public GitHub repository.

## Next port order

1. Build source-verified, legally distributable mechanical technique definitions **per discipline** without copyrighted descriptive prose.
2. Tie each ability to a concrete Godot action, target, legality, effects, System Strain and saves, with tests.
3. Connect authorized psychic character creation and skills to CWN campaign character data.
4. Display learned techniques and available Effort in the MVP UI; test save/load and combat-round interaction.
5. Test against the original book with documented example outcomes; perform a windowed playtest before considering release.

Run the project's standard Godot test suite, which discovers `tests/godot/test_*.gd`. These tests exercise executable rules, not prose.
