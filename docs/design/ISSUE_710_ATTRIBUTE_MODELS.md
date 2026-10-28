# Attribute models: A, B and C compared (#710)

**Status: comparison and a recorded decision. Nothing is implemented; no save format,
schema or canonical stat is changed by this document.**

The question is whether NoöPunk keeps CWN's `STR / DEX / CON / INT / WIS / CHA`, displays
something more contemporary, or redesigns the attribute set entirely.

---

## A — unchanged CWN (the baseline)

| | |
|---|---|
| **What it is** | `Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma`, 3–18, modifiers −2..+2 |
| **Cost** | none: it is what `src/rules/cwn_*.py` already implements |
| **Benefit** | every CWN procedure works unmodified — saves, HP, System Strain ceiling, load, Effort, NPC stat lines, Edges and Foci references, and any future CWN supplement |
| **Risk** | the vocabulary reads fantasy-coded in a near-contemporary setting; "Wisdom" in particular does work that NoöPunk splits between judgement and psychic capacity |

## B — six modern display aliases, CWN keys retained

| | |
|---|---|
| **What it is** | the sheet *prints* `Body / Reflexes / Endurance / Intellect / Perception / Presence` while the stored keys stay `str/dex/con/int/wis/cha` |
| **Cost** | one presentation layer; a mapping table; every place that renders a stat must use the display name |
| **Benefit** | tone changes completely at zero mechanical risk; saves, formulas, NPCs and saves are untouched; reversible by deleting the table |
| **Risk** | two vocabularies in the same repository — a reader of the code sees `wis`, a player sees `Perception`, and the mapping must be single-sourced or it drifts |

**This is the only option that is a *reskin* in the strict sense**, and it satisfies the
"mechanical complexity preserved" requirement by not touching mechanics at all.

## C — FIT / REF / INT / SOC / PSY / CYB redesign

| | |
|---|---|
| **What it is** | the #263 candidate, six new axes |
| **Benefit** | the sheet names what the game is about; PSY and CYB are setting-load-bearing |
| **Cost** | **a new mechanical design, not a rename.** Every derived quantity must be re-derived: HP, saves, System Strain ceiling, Effort, load, combat numbers, skill-to-attribute pairings, advancement, NPC stat lines, and all stored schemas |
| **Specific problems, named** | **FIT** merges Strength and Constitution, which collapses the distinction between *lifting* and *enduring* that the injury rules rely on · **PSY** conflates ordinary judgement (`WIS`) with psychic capacity, which is exactly the separation #572 and D46 insist on · **CYB** has **no CWN source axis** and, if made an attribute, penalises unaugmented characters by definition; it is better modelled as equipment/interface or a skill domain |

**Verdict: C is not a reskin.** It is a new game whose compatibility with CWN procedures has
to be re-established case by case, and the three named problems are not cosmetic.

## Recommendation and recorded decision

**A is retained.** The reasons are mechanical rather than aesthetic: it is the only option
under which the 1,429-test suite, the save formulas, the Strain ceiling and the Effort
economy keep meaning what they mean today.

**B remains available and is not authorised.** If the fantasy-coded vocabulary becomes the
thing that hurts most, B is the cheap fix — a presentation table, not an engine change — and
it can be adopted without revisiting this decision.

**C is rejected as a rename** and would need to return as its own design with the three
problems above solved, plus a migration plan that preserves existing characters rather than
rescaling them.

> This decision is **provisional and reversible in one sentence**, like the other design
> records in this repository. It is recorded here because the issue could not be closed
> without naming an outcome, and "we compared them" is not an outcome.
