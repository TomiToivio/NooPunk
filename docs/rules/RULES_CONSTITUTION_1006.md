# Rules constitution — the Without Number foundation is locked (#1006)

**Status: binding.** This document is the human-readable half of
[`data/rules/rules_constitution.json`](../../data/rules/rules_constitution.json), which
`tests/test_rules_constitution_1006.py` checks. If the two disagree, the test fails.

## The author's decision

> We will use all CWN rules, many SWN rules and potentially some WWN/AWN rules. The NoöPunk Mods are built on
> top of plain vanilla CWN/SWN/WWN/AWN rules.

NoöPunk is not a new ruleset. It is **Cities Without Number**, plus a substantial part of **Stars Without
Number**, plus **Worlds Without Number** and **Ashes Without Number** material where a case needs it — with every
original NoöPunk idea built **on top**.

This ends a cycle. Core mechanics have been revisited repeatedly; they are not reopened again. CWN/SWN sit at
the intended complexity: enough for an experienced old-school player, not needlessly intricate.

**Precedence when sources disagree: CWN → SWN → WWN → AWN → NoöPunk overlays.**

## What is locked

1. **CWN in behaviour.** Six attributes, the original skill list and definitions, skill levels and advancement,
   character creation, combat, saves, equipment procedures, and the fundamental resolution rules. Behaviour is
   the standard: a refactor that produces identical rolls is fine, a rewrite that produces *better-feeling*
   rolls is forbidden.
2. **All of CWN, not a subset.** "We don't implement that section" is not a design decision; it is an
   unfinished matrix row. `tools/check_cwn_compliance.py` and
   [`docs/rules/CWN_COMPLIANCE_MATRIX_950.md`](CWN_COMPLIANCE_MATRIX_950.md) record what is real.
3. **SWN psionics as a module.** The PSI premise needs it, so it is essential — and essential does **not** mean
   editable. It arrives as an identified module with its own tests and its own documented bridging, never as a
   patch to CWN.
4. **Many SWN rules.** Space travel, ships, factions and equipment are needed by this setting and come from SWN
   rather than from invention. Each import is a module with a boundary.
5. **WWN/AWN are optional.** Imported when a case requires it. The AWN stress/survival data and overlay already
   exist; nothing from either source replaces a CWN procedure.
6. **Vanilla stays playable.** Turning off every overlay must leave a faithful CWN game. That profile is
   defined in the JSON and contains no overlay path.
7. **One contract everywhere.** Tabletop, the Evennia MUD and the Godot maintenance build use the same rules;
   `tests/test_mud_cwn_parity_950.py` is what keeps the MUD honest. Godot is maintenance-only and is not a
   second mechanical baseline.

## The three layers, and the line between them

| Layer | What it is | Where it lives | May it change CWN? |
|---|---|---|---|
| **Core** | CWN procedures | `mud/nopunk_mud/cwn/`, `mud/nopunk_mud/cwn_core.py`, `src/rules/`, `godot/core/` | It *is* CWN |
| **Module** | SWN/WWN/AWN material, imported whole | `mods/` and MUD modules, one per import | No — narrow, documented overrides only |
| **Overlay** | Original NoöPunk features | `mods/noopunk/`, `mud/nopunk_mud/` overlays | **No.** Adds behaviour around the core |

**The rule of the line:** an overlay may *ask* the core for a roll and read the result. It may not roll for it.
If an overlay contains its own difficulty table, its own attribute list, or its own damage arithmetic for a CWN
procedure, it has stopped being an overlay.

### Profiles

- **`vanilla-cwn`** — faithful CWN, no NoöPunk features. Must stay playable. This is the regression baseline.
- **`minimum-playable`** — CWN + SWN psionics. The smallest build that supports the PSI premise.
  **Psionics is not implemented yet**; the constitution says so rather than pretending.
- **`full-noopunk`** — core + psionics + SWN space/factions + GUMSHOE investigation + Noösphere/PbtA +
  ideology/factions. The intended experience.

## Mandatory overlays

Two overlays are **required features of the intended design**, not hypothetical inspirations. They are still
overlays: modular, independently testable, and outside the immutable core.

1. **GUMSHOE-inspired investigation** — investigative abilities and procedures, reliable core-clue discovery,
   optional spends, mystery structure. CWN keeps attributes, skills and combat; mapping is an adapter.
   Implemented: `mods/noopunk/gumshoe_investigation.gd`, `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`.
2. **PbtA-inspired Noösphere** — Noösphere, collective consciousness, ontological shock, moves/clocks/fronts,
   consciousness-related progression. StO/StS framing and density awakening live here. Implemented:
   `mods/noopunk/noosphere.gd`, `mud/nopunk_mud/consciousness.py`.

Distinguish **mandatory for the full experience** from **necessary for the minimum profile**. Psionics is
necessary; these two are mandatory for NoöPunk to be NoöPunk.

## What agents may not do

- **Do not redesign the core.** Not to simplify it, not to balance it, not to make it "feel more NoöPunk".
- **Do not invent a rule before inspecting the sources.** Read CWN, then SWN, then WWN/AWN. Prefer a source
  mechanic, a reskin, or an additive adapter over a new subsystem.
- **Do not add Empathy/Awareness or any other attribute.** If a NoöPunk skill is added, it is a **mod skill**;
  CWN's Notice, Know, Work and the six attributes keep their meaning and their behaviour.
- **Do not treat a vague instruction as authorisation.** "Improve the rules", "make PSI deeper", "implement this
  subsystem" are not permission to touch the core. Refuse the refactor and propose a mod.
- **Do not silently diverge.** Any deliberate difference from a source procedure goes in the module's
  documented deviation list and in the compliance matrix.
- **Do not present a planned module as implemented.** The JSON has a `planned` status precisely so that
  honesty is cheaper than optimism.

**Amending the constitution** requires an explicit author decision that names this document. Nothing else
qualifies — not a design document, not an issue comment from another agent, not a majority of agents agreeing.

## Licensing

Before copying wording or implementing additional mechanics, check the source and the licence ledger
([`data/sources/game_system_rights.json`](../../data/sources/game_system_rights.json)). The Without Number games
are not open-licensed; their *procedures* are implemented, their *prose* is not copied. GUMSHOE material comes
from the OGL SRD edition; the licence question there was settled in #966.

## Related, and not to be reversed

- #897 foundational lock (CWN core, overlay boundary, enforced by tests)
- #950 pivot to the Evennia MUD
- #932 GUMSHOE investigation mod
- #943 Noösphere mod
- #966 Evennia command layer
- #1006 this document · #1007 design canon · #1005 lore consolidation

Guiding principle, in the author's words:

> We are done choosing the basic RPG system. CWN/SWN are the right level of complexity for NoöPunk. We will keep
> adding mods on top of CWN, but we will never change CWN itself.
