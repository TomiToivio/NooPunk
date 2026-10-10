# Issue #220 — social procedures: dialogue, faction relationships and consequences

**Status: PROPOSAL landed as a procedure, not a calibration.** `rulebook/4_SOCIAL.md` carries the
playable social procedure; `src/rules/social.py` executes it with `IS_CANONICAL = False`.

Cross-links: #200 (epic), #225 (the shared clock), #219 (the shared band arithmetic), #233 (the
aspect layer reused), #107/#122/#144 (the Affect graph preserved), #226 (investigation, untouched).

## The decision that governs the whole chapter

> **A social check changes what a character can *achieve*. It never changes what a target
> *believes*.**

Every other choice follows from taking that seriously. A social system fails at the moment a good
roll silently rewrites a person — the NPC stops being an agent and becomes a difficulty number with
a face. AC3 asks for exactly this, so the guard tests it as **capability absence**, not as prose:

- `rewrites_motivation(consequence)` returns **False for every band**, and the guard asserts there is
  **no `set_motivation` / `overwrite_motivation` / `write_belief` function in the module at all** — a
  capability that does not exist cannot be called by accident.
- `detects_lie(kinesics_succeeded=…, contradicting_evidence=…)` returns True **only** on independent
  evidence. A perfect Kinesics roll has no path to certainty about another mind, by signature.

## One arithmetic across realms, not two

The margin→band function is **imported** from `src/rules/physical_combat.py` rather than
re-implemented, and the guard asserts `social.band_for_margin is physical_combat.band_for_margin`.
Physical and social differ in what a band **means**, never in how it is computed. The consequence
vocabulary is social (`Heard / Leaning / Convinced / Committed`, with `Unmoved` below zero), and a
guard sabotages the import by replacing it with a stub — proving the reuse is load-bearing.

The sign check lives in the social module because the band function maps *every* negative margin to
"glancing"; that is documented in the docstring rather than left as a trap.

## Preserving the graph, adding only what was missing

Existing canon is **consumed, not forked**:

- Reputation stays an **Affect edge** on the **−10…+10** scale; US/FRONTIER and the seven SNA layers
  are untouched; `src/simulation/affect.py` remains the reference model.
- **Relationship statuses** (`Unknown / Acquainted / Trusted / Indebted / Estranged / Hostile`) are
  **derived from Affect edges** — `relationship_status()` takes edges and computes a status. Nothing
  is stored beside the graph, so a status field and the graph can never disagree. The chapter's
  original rule — *no edge means unknown, and unknown is not a stored zero* — is preserved, and the
  guard tests it directly (`relationship_status([]) == Unknown` **and** `!= Acquainted`).
- **Aspects come from #233** (`ISSUE_200_ASPECTS_PROTOTYPE.md`); this chapter does not add a second
  aspect layer. **Grievance** is defined as the canonical bounded consequence of coercion.

## Bounded modifiers and one-step movement

- **Group support is capped at +2**, the same ±2 situational cap the resolution pass recorded (#217),
  so a crowd cannot become an unbounded bonus. Sabotage raises the cap to 5 and the guard catches it.
- **A witnessed exchange may move a Reputation edge by exactly one step** — the same one-step
  vocabulary physical armor uses — and never more; a 3-step value is refused at construction.

## The Concordia seam (AC4)

The chapter states the seam explicitly: the **engine resolves deterministically** and writes the
result; the **LLM narrates and chooses but never rolls and never sets state** (`AGENTS.md` §12). The
LLM may **propose** an aspect; the engine **validates** it and **rejects** anything that would
rewrite a Motivation, invent a score, or exceed the aspect bounds — "rejected, not narrated into
existence". Narration is generated; numbers are not.

## AC mapping

| AC | Where |
| --- | --- |
| 1 — social contests, contacts, negotiation, deception, coercion, group interactions | §*Social contests*, §*Contacts and the social graph*, §*Group interactions*; `resolve_social`, `group_support` |
| 2 — preserve reputation/contacts/motivations/networks; bounded aspects, statuses, consequences | §*Relationship statuses*, §*Bounded narrative aspects*; `relationship_status`; `PreservationTests` |
| 3 — NPC agency, no mind-reading, no guaranteed lie detection | §*The hard limits*; `detects_lie`, `rewrites_motivation`; `HardLimitTests` |
| 4 — tabletop and Ollama/Concordia examples | §*Worked examples* (both) |
| 5 — cross-links, tests, comment | cross-links; `tests/test_issue220_social_procedures.py`; the PR |

## Deliberately not done

- **No persuasion formulas, Affect-score increments, or propagation algorithm** — reserved
  (`AGENTS.md` §4, #107). The chapter specifies the **shape**; the author owns the arithmetic.
- **No new Skills, STATs or derived statistics.**
- **No second graph and no second aspect layer.**
- **No investigation/evidence procedure** (#226).
- **No calibration** — every value is **PROVISIONAL** and the module is non-canonical.

## Verification

- Full suite green (see PR); `ruff` clean.
- `tests/test_issue220_social_procedures.py` — 45 tests, sabotage-proven 26/26 caught with 4/4
  controls clean and byte-identical restores.
- The sabotage round found one real hole in my own guard (no second-dice assertion on this chapter);
  closed before shipping.
