# Foundational lock (#897)

**Status:** locked. This document is the authority for *what NoöPunk is built on*, and it is deliberately
narrow: it decides the rules engine, the boundary between baseline and overlay, and how a future proposal
may change either.

Two things are locked here and nowhere else:

1. **Cities Without Number is the rules engine.** Not a starting point, not a reference — the engine.
2. **NoöPunk is a set of overlays on top of it.** Overlays may add, colour and reframe. They may not
   replace resolution.

Everything else in this directory is downstream of those two sentences.

## 1. The baseline, stated once

| Question | Answer |
| --- | --- |
| Rules engine | **Cities Without Number** (CWN), first edition material |
| Additions | SWN (psionics, space, factions) and WWN (a few procedures) **only** where CWN is silent and the addition is justified in writing |
| Attributes | STR / DEX / CON / INT / WIS / CHA |
| Skills | level 0–4; checks are 2d6 + attribute modifier + skill |
| Attacks and saves | d20 |
| Character growth | CWN advancement; foci and edges as published |
| Non-negotiable | no replacement of the resolution core, ever, by default |

A NoöPunk rulebook must be intelligible **without** any overlay. If an overlay were deleted, a table
running CWN would notice nothing missing.

## 2. What is implemented, adapted, or optional

The inventory lives in one place: **[`CORE_VS_MOD_MATRIX_897.md`](CORE_VS_MOD_MATRIX_897.md)**. It records,
per mechanic, whether it is implemented verbatim, adapted, a NoöPunk module, or dormant.

This document deliberately does not repeat that table. Two copies of a classification is how a
classification stops being true — the matrix is the authority, and adding a mechanic means adding a row
there before writing code.

## 3. Architectural boundary

```
godot/core/          CWN resolution: dice, checks, saves, combat, injury, hacking, cyberware, progression
godot/narrative/     location, dialogue, investigation, campaign state
mods/noopunk/        overlays: noösphere, ideology, obligations, investigation framing
data/rules/          rule data (contracts, catalogues) — read by core, never by mods directly
```

Rules that keep the boundary honest:

- `godot/core/` **must not** import from `mods/`. Enforced by `tests/test_foundational_lock_897.py`.
- A mod receives data and returns data; it never mutates a core result in place.
- A mod that needs a roll asks the core for it — it does not roll its own dice.
- If an overlay needs a new number, it stores it beside the core value rather than reinterpreting it.

## 4. The narrative pivot

The playable campaign is **location-based narrative** (Citizen Sleeper-shaped): a Helsinki location map,
action menus, investigation and conversation as the backbone, non-tactical combat resolution driven by
CWN mechanics, prominent graph hacking.

The tactical top-down encounter remains in the tree **dormant**. It is not deleted, not maintained, and
not on the default path. Migrating it back is a planned change, not an accident.

## 5. How this may change

A proposal to replace the core resolution **requires a separate, approved foundational decision** —
recorded here, with its own issue number. Brainstorming a mechanic is not authorisation. "It would fit
the fiction better" is not a reason to fork the engine; it is a reason to write an overlay.

Adding an overlay needs only: a rule reference, examples, tests, and a flag that turns it off.

## 6. Why this lock exists

This project has already replaced its rules engine more than once — a blank restart, a seven-attribute
design, a narrative substitute — and each replacement invalidated downstream work. The cost was not the
new design; it was everything that had been built on the old one.

The lock is the cheap version of that lesson: decide once, in writing, and make the change expensive and
explicit.
