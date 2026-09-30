# Cities Without Number SRD as NoöPunk's open mechanical chassis

> **Status:** author-specified design policy (issue #19).
>
> This file is the **single canonical explanation** of how NoöPunk relates to the
> Cities Without Number SRD. Other documents should *reference* it rather than
> restate it. See [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) for the three
> project-level design balances, which remain the higher authority on design intent.

## The decision

NoöPunk starts from the **Cities Without Number SRD** (`CWN SRD`) as its main
**open mechanical chassis**, then deliberately modifies that system subsystem by
subsystem.

> **Cities Without Number as the open chassis, then progressively NoöPunkify
> everything.**

NoöPunk is **not** a Cities Without Number clone, conversion, or retroclone. CWN is
a starting point and a comparison source, not a target to converge on. The final
game is expected to diverge substantially from CWN.

Primary SRD reference: <https://cwn.quadrifons.com/>

## What the SRD is, and why it is the chassis

The CWN SRD is a free, open, public-domain system reference document that describes
the rules and mechanics of Kevin Crawford's cyberpunk tabletop RPG *Cities Without
Number*. It is intended for reuse and modification.

Using it gives NoöPunk a coherent, reasonably lightweight cyberpunk baseline so the
project does not have to reinvent every generic RPG subsystem from zero. That is the
whole value proposition: a playable skeleton, not a finished game.

The SRD is a **rules** source. It is not a setting source, and the full commercial
*Cities Without Number* book is not a source at all.

## Legal / source boundary

**Direct reuse is limited to material that is actually present in the CWN SRD.**

Do not copy or adapt:

- setting-specific material from the full *Cities Without Number* book that is not
  present in the SRD;
- protected megacorps, NPCs, places, events, or other setting content from that book;
- protected text, setting material, terminology, factions, characters, or
  proprietary creative content from any other RPG.

Cyberpunk 2020, Eclipse Phase, Shadowrun, The Sprawl, and CY_BORG are **design
references only**. They are influences and comparisons, never sources to copy from.

When in doubt about whether a piece of text is in the SRD, treat it as **not** in
the SRD and write NoöPunk's own wording.

## Working method: subsystem by subsystem

For every major subsystem, make one explicit decision:

| Decision | Meaning |
|---|---|
| **KEEP** | usable largely as-is from the CWN SRD |
| **MODIFY** | keep the structure, alter it for NoöPunk |
| **REPLACE** | use a different NoöPunk-specific rule |
| **OMIT** | do not use this CWN subsystem |
| **DEFER** | leave unresolved until the author decides later |

**Do not assume any subsystem survives unchanged.** No subsystem is sacred; every
part can be changed if NoöPunk needs something different.

This is an incremental design process, not a one-shot conversion. Each subsystem is
reviewed, decided, and stabilised in the tabletop rules on its own.

### Review scaffold

The following order is a scaffold for that review. It is **not** an implementation
plan, and it is **not** a claim that any of these subsystems are ready.

1. Attributes
2. Attribute generation / modifier scale
3. Skills
4. Character creation
5. Core checks
6. Saving throws / resistance mechanics
7. Combat
8. Damage / wounds / trauma / healing
9. Initiative / actions
10. Armor and weapons
11. Cyberware
12. Hacking / cyberspace
13. Drones
14. Vehicles
15. Equipment / encumbrance
16. Advancement
17. Contacts / backgrounds / edges / foci or their replacements
18. Mission structure
19. GM procedures
20. NoöPunk-specific systems: CYB, PSY, BCI, compute, cyberspace-native entities,
    uploaded humans, AI, psionics, Noösphere, NHI

### Review status

Nothing above is reviewed yet except where NoöPunk **already** has an author
decision. The only such case is the attribute layer, which NoöPunk replaced before
adopting CWN as a chassis:

| Subsystem | Decision | Note |
|---|---|---|
| Attributes | **REPLACE** | NoöPunk's own six attributes, already author-specified |
| Attribute generation / modifier scale | **DEFER** | NoöPunk's own 3d6 generation and −3..+3 range are canonical; the comparison with CWN is unreviewed |
| Skills | **DEFER** | NoöPunk's four levels are canonical; the catalog and the comparison with CWN are unreviewed |
| All other subsystems | **DEFER** | not yet reviewed; remain undefined (see `RULEBOOK.md` §19) |

Every row not marked otherwise stays **DEFER** until the author decides it. A DEFER
is not a decision to keep CWN: it means the question is still open.

## NoöPunk decisions take precedence

**Existing author-specified NoöPunk rules remain canonical unless a later author
task explicitly changes them.** CWN is a starting chassis and a comparison source,
not a higher authority that overrides already-specified NoöPunk rules.

That includes, but is not limited to:

- the six attributes: **FIT**, **REF**, **INT**, **CHA**, **CYB**, **PSY**
- 3d6 ordinary-human attribute generation
- the −3..+3 ordinary-human modifier range
- 3d6 core resolution
- the difficulty ladder
- skill levels 0–3
- the tabletop-first development order
- the current cyberspace modifier work

### The first known divergence: attributes

The attribute system is already intentionally different from CWN, and must **not**
be redesigned back toward it.

| NoöPunk | Conceptually |
|---|---|
| **FIT — Fitness** | CWN Strength + Constitution collapsed together |
| **REF — Reflexes** | maps broadly to CWN Dexterity |
| **INT — Intelligence** | maps broadly to CWN Intelligence |
| **CHA — Charisma** | maps broadly to CWN Charisma |
| **PSY — Psyche** | CWN Wisdom, reworked |
| **CYB — Cybernetics** | **new**; cyborg / cyberspace-native / technical integration |

NoöPunk also uses an ordinary-human modifier range of **−3 to +3**, which is wider
than CWN's narrower ordinary modifier scale. This difference is deliberate.

A wider ordinary modifier range is not a balance problem to be corrected by
importing CWN's scale: it is part of how NoöPunk's checks work.

## Tabletop first

CWN adoption changes nothing about the development order:

> **Tabletop first. Godot and Concordia later.**

For every subsystem:

1. review the CWN SRD version;
2. compare it with NoöPunk's goals;
3. define or modify the **tabletop** rule;
4. stabilize it;
5. only then create digital specifications and ports.

Do not bulk-port CWN mechanics into Godot or Concordia. Digital runtimes remain
deferred until individual tabletop subsystems are stabilised.

## Scope of this policy

Adopting the chassis establishes **policy and roadmap only**. It does not convert,
port, or implement any subsystem.

The specific deliverables of this policy are: the chassis relationship, the legal
boundary, the decision model, the review scaffold, and the precedence rule. Any
actual KEEP / MODIFY / REPLACE / OMIT decision is a separate, author-driven task.
