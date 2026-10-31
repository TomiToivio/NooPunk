# NoöPunk rules basis: the foundational lock (#897)

**Status: permanent project decision, 2026-10-31.** This file is the record of what the game's rules
*are*, so no future agent or contributor re-opens the ruleset. It implements checklist items 1, 2 and 4
of issue #897. It does not by itself implement any mechanic.

## 1. Authority order

1. **CWN governs.** Every procedure that exists in *Cities Without Number* is implemented **as written**:
   attributes, classes, backgrounds, edges, foci, skills, 2d6 checks, d20 saves and attacks, combat,
   system strain, trauma, cyberware, hacking and progression. These are the baseline, not a starting
   suggestion.
2. **SWN / WWN fill gaps CWN does not cover, whole-procedure, one line each.** Psionics is the clear
   case: SWN Revised supplies the Psychic class, disciplines, Effort and techniques as a complete
   subsystem. It is **not** blended into CWN skills or combat. Any further WWN borrowing needs its own
   row below, naming the gap it fills.
3. **NoöPunk material is a mod, never an edit.** Noösphere/ontological shock, ideology and factions,
   relationships/reputation, investigative clocks, vices and temptations are **overlays that read CWN
   state and add narrative state**. A mod may not change a CWN target number, die, band or progression
   cost. If a mod appears to need that, it is a mod-design issue requiring Tomi's approval — not a
   rules change.
4. **Reskin is free; mechanics are not.** Names, aesthetics, gear flavour, city texture and framing may
   be reskinned freely. Any new *mechanical effect* is a documented mod with its own hook and test.

## 2. Core-versus-mod matrix

| Layer | What it covers | Status | May it change a CWN number? |
| --- | --- | --- | --- |
| **CWN core** | attributes, skills, backgrounds, edges, foci, 2d6 checks, d20 saves/attacks, combat, strain, trauma, cyberware, hacking, progression | **verbatim** | — it *is* the numbers |
| **SWN gap-fill** | Psychic class, disciplines, Effort, techniques | **whole procedure** | no |
| **WWN gap-fill** | *(none registered yet; each addition needs its own row and a named gap)* | — | no |
| **NoöPunk mods** | Noösphere / ontological shock / Psyche exposure; ideology, factions and polarization; relationships, reputation and contacts; investigative mode; vices and temptations | **overlay, read-only on CWN state** | **no** |
| **Reskin** | names, art, gear flavour, city texture, framing | free | no |

Anything not in this table does not exist yet. Adding a row is an authorised act; silently inventing a
layer is not.

## 3. Architectural boundary

- **`godot/core/` is the canonical owner of CWN/SWN rule implementations** (#791); `src/godot/` is a
  compatibility tree. Shared rule values come from `data/rules/` contracts.
- Baseline resolution lives behind an **adapter boundary**. NoöPunk mods read the resolved state and add
  narrative state; they do not sit inside the resolution function.
- **Parity tests** guard the baseline: a mod that changes a CWN outcome must fail the suite.
- Where a `mods/noopunk/` tree exists or is introduced, it may depend on `core/`, never the reverse.

## 4. What this lock settles, and what it does not

**Settled:**
- No further core-rule replacement. Brainstorming a new mechanic does not authorise replacing CWN.
- A proposal to replace the baseline requires a **separately approved foundational decision**.
- **The seven-attribute UNSA sheet (#835) is not the CWN baseline.** CWN's attributes are
  STR/DEX/CON/INT/WIS/CHA on 3–18. Where the seven-attribute sheet survives, it is a **NoöPunk mod**
  recorded in the matrix above; it may not override the baseline, and it must not be described as
  "the rules".

**Not settled here (open, per #897):**
- PC PSI scope (tentative: passive/minor for the PC, active for NPCs) — a playtest question.
- The exact narrativist mod list.
- The art-direction bible (item 12) and the Helsinki map, modes, and vertical slice (items 18–26).

## 5. Licensing

Mechanics are implemented from legitimately available sources; where exact licensed text cannot be
reproduced, the implementation stays procedural and attribution is recorded in the repository's
licence audit (`docs/licenses/ISSUE_569_CWN_SWN_LICENCE_AUDIT.md`). Reskinning does not create a
licence to redistribute protected text, tables or artwork.
