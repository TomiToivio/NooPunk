# Scope ruling: the 2026-10-07 lore and reference-list chapters

**Status: author-directed scope record.** This document records the scope boundary of the
chapter set the author requested on **2026-10-07**, so that a later session does not have to
re-derive it from prose.

## What the author asked for

> "These are mostly lore issues to be added to the rulebook. Also add relevant rules. Also
> create sections for character generation, equipment, cybernetic (and psychotronic)
> implants, PSI powers, types of beings (monster manual?), etc. These lists don't need to have
> full stats for everything yet, just make a list of stuff with light description."

The directive named ten issues (#171, #172, #173, #174, #175, #176, #177, #178, #179, #180)
with #173 and #174 explicitly restricted to **lore-only, rules as ideas**.

## What was delivered

| Chapter | Contents | Issues |
| --- | --- | --- |
| `rulebook/6_PSYCHIC.md` | Psionics/psychotronics/psyops continuum, BCI exploitation, ritual, sleep and dream nights, Atmanspacher, disconnected systems, Seity (idea only), the PSI power list | #171, #173, #174, #175, #176 |
| `rulebook/10_SINGULARITY_CRISIS.md` | The Crisis, Noösphere/Panopticon/Thanatos, cyborgist intelligence theory, the intelligence ecology, the two Singularities | #177, #178, #180 |
| `rulebook/11_ONTOLOGY.md` | Seven densities, vehicle-vs-entity, cryptoterrestrials, plasmoids/orbs, thought-forms, Higher Self, the Sphere Network | #179 |
| `rulebook/12_BEINGS.md` | Catalogue of kinds of being, hybrids, verification procedure, castes, the class conflict | #171, #172, #179, #180 |
| `rulebook/13_EQUIPMENT.md` | Equipment, cybernetic implants, psychotronic devices (A and B) | #180 + directive |
| `rulebook/14_CHARACTER_GENERATION.md` | The chargen section: origins, backgrounds, training paths | #144 + directive |

## The scope boundary — what the directive opens, and what it does not

`AGENTS.md` §4 reserved several of these areas (`psionic powers or psionic mechanics`;
`NHI taxonomy or capabilities`; `cyberware / augmentation rules beyond the capability-level
standard UNSA package`; `equipment statistics`; `character creation beyond the Lifepath
framework`). The author's directive is the **un-reservation for the descriptive half**, at
**list granularity and no further**. The un-reservation should be recorded in `AGENTS.md`
§4 by the author (that file is protected from agent writes); this document is the standing
record of the boundary until it is.

**Un-reserved by the directive (descriptive lists):**

- equipment — name/capability/role lists (`13_EQUIPMENT.md`);
- cyberware / augmentation — implant-type lists (same chapter);
- psionic powers — the power-and-technique vocabulary (`6_PSYCHIC.md` §6.7);
- NHI taxonomy and capabilities — the catalogue of kinds of being (`12_BEINGS.md`);
- character creation — a descriptive section over the #144 Lifepath
  (`14_CHARACTER_GENERATION.md`).

**Still reserved (no chapter may define it):**

- numeric equipment statistics — prices, damage, armor values;
- combat resolution, damage, health, wounds, armor, initiative;
- psionic mechanics — costs, durations, dice, tracks;
- the deep-hacking / cyberspace subsystem;
- derived statistics; advancement / XP; economy;
- character classes or archetypes (the training paths in `14_CHARACTER_GENERATION.md` are
  **careers, not classes**, and grant nothing mechanically);
- starting skill counts or levels beyond the canonical UNSA package;
- cortical-stack continuity and resleeving mechanics.

Each new chapter ends with an explicit "what this does NOT define" section restating its own
bound. Every chapter that quotes the directive's "light description" rule does so as a
**constraint**, not as a licence to fill the reserved half.

## Rules added, and the rule for adding them

The directive also said "add relevant rules". The rule applied throughout the new chapters:

> **A chapter may state a rule that already belongs to a canonical subsystem** — a check
> shape, a procedure, an order of operations, or a constraint on scenario and NPC design —
> **and may name the hooks a later mechanics pass will build on. It may not define a new
> numeric subsystem.**

Concretely, what was added as rules rather than lore:

- the **detection → suspicion → attribution → classification → authorisation** incident
  procedure (`6_PSYCHIC.md` §6.2.6), with attribution as the setting's named step;
- the **multi-signal verification procedure** for suspected hybrids and non-humans
  (`12_BEINGS.md` §11.9), including the audit requirement and the "the test must be beatable
  and fallible" constraint;
- the **coupling requirement** for every PSI power and the
  `PSY + Skill + 1d10` check shape (`6_PSYCHIC.md` §6.7.3);
- **altered states as situational modifiers, not new subsystems** (`6_PSYCHIC.md` §6.2.5);
- **zero-days as plot-grade assets, not equipment** (`6_PSYCHIC.md` §6.2.3);
- the **anti-trivialisation rule** for sensors, tests and PSI
  (`13_EQUIPMENT.md` §12.5, `12_BEINGS.md` §11.9.3);
- **no universal paradigm shift** as a standing constraint on scenario and NPC design
  (`6_PSYCHIC.md` §6.10.4);
- **augmentation is optional** and the non-implant path is fully playable
  (`13_EQUIPMENT.md` §12.1; `14_CHARACTER_GENERATION.md` §13.7).

## Issue-specific notes

- **#173 and #174 are lore-only.** Seity (`6_PSYCHIC.md` §6.6) and the disconnected-system
  failure states (§6.5) are recorded as **design parking places**, with the explicit note that
  they are **not implemented** and that nothing else may depend on them yet.
- **#172's EMP** is recorded as a possibility only; EMP is **not** restored as a STAT.
- **#177 and #178 are the same concept.** The chapter is a **single synthesis** of both
  drafts, not two competing accounts; where one had material the other lacked, it is included.
- **#171's cautions are binding.** `6_PSYCHIC.md` §6.11.8 lists what must **not** be imported
  uncritically (dual-aspect monism as established physics; every coincidence as synchronicity;
  generalized quantum theory as physical entanglement; Atmanspacher as having proved PSI).

## Sibling collision and the §44 repair

PR **#181** (`3dc7926`, "Integrate NoöPunk lore, field catalogs and light rules") landed the
**condensed** version of this same batch while the detailed chapters above were being written —
the standard mid-write collision. Per the standing rule (**upstream wins on parity; combine
the best parts**), the two were reconciled rather than one being dropped:

- **Their `rulebook/9_FIELD_CATALOGS.md` is kept** as the quick campaign-facing field list.
- **The detailed chapters were renumbered to 10–14** to clear the `9_` filename collision,
  and each of their summary chapters in `RULEBOOK.md` now cross-references the deep chapter.
- **Their `6_PSYCHIC.md` orientation header is kept** as the chapter lead; the detailed
  Psychic Systems material follows it.

**The merge also introduced a red `main`.** PR #181 added `RULEBOOK.md` ledger chapters
numbered **45–51** while never writing a **44**, so both ledger-contiguity guards failed
(`tests/test_issue78_four_layers.py::test_section_numbering_has_no_gaps`,
`tests/test_issue101_sources_dedup.py::test_top_level_numbering_is_contiguous`) — 817 tests,
2 failures on `3dc7926`. No §44 ever existed in the ledger (it was 1–43 contiguous before
#181), so the repair is to renumber the sibling's 45–51 down to **44–50**, restoring
contiguity. Verified: no external citation to §44–§51 exists outside the rulebook itself.
