# Issue #566 — acceptance record

**Decision issue. Answered by the author 2026-10-25. Checked against `main` at `f8d3036`.**

## Criterion

#566's own "done when": *each of the four questions is answered in a comment on this issue, and the
answers are transcribed into `docs/CWN_CHASSIS.md`.*

| Requirement | Evidence | Met |
| --- | --- | --- |
| Four questions answered in a comment | `#566` comment 6401398806 carries the costed framing; the four answers are recorded there and below | yes |
| Answers transcribed into `docs/CWN_CHASSIS.md` | the file carries an explicit **"CONFIRMED by the author"** ruling section, plus the three further rulings | yes |
| No mechanic silently approved | every gate A–D status left unchanged; no number filled | yes |

## The four answers

| # | Question | Ruling |
| --- | --- | --- |
| 1 | Scope | **Layer A only.** Legacy tabletop (`RULEBOOK.md`, `rulebook/`, `src/rules/`). Layer B keeps its approved Fate `4dF`. |
| 2 | Core check | **`1d10` stays** (`STAT + Skill + 1d10 ≥ DV`, #111). No die replaced. |
| 3 | Attributes | **`FIT/REF/INT/SOC/CYB/PSY` survive.** The epic's `CHA` is CWN's name and is not adopted. |
| 4 | Classes / levels | **Declined.** **Edges admitted** as classless differentiation; no levels, no XP thresholds. |

## Why scope A, in the record's own words

Measured on `origin/main` at `f8d3036`, moving layer A off `1d10` would have touched **80 `1d10`
occurrences across 41 files**, the `DIFFICULTIES`/`DIFFICULTY_LADDER`/`difficulty_for()` machinery in
`src/rules/core.py:41`–`173`, and **41 test files** touching `1d10` or `DV`.

A-only costs one cross-reference. Both-plus-one-die costs that table and retires an approved kernel.
"One unambiguous rulebook" is satisfied by **labelling**: `RULEBOOK.md` *is* the NoöPunk RPG;
`strategy_game/RULEBOOK.md` is Layer I of the crossover, which its opening already says.

## Three rulings carried with the answers

1. **Hacking runs on a ubiquitous network.** Access is not the scarce thing; CWN supplies the
   resolution procedure only, never the access model.
2. **PSI = SWN's rules, for a learnable natural human ability.** Effort adopted; ontology preserved
   (natural, learnable, open to anyone).
3. **New NoöPunk subsystems where the family has no equivalent** — Noösphere/cross-domain state,
   psychotronics, NHI contact, AGI/ASI, crisis-era topology.

## What stays open

D36 (Effort pool size; implant capacity), D23 (Edge count/frequency/admission), #572's subsystem
specs and access tiers. **Gates A–D remain open; no number is approved.**

## Honesty note

A prior provisional ruling section already existed in `docs/CWN_CHASSIS.md`, written by another
session, and it had reached the same scope answer. It is now marked **confirmed** rather than
duplicated. An earlier agent recommendation in the same file had classes "not admitted", with
differentiation deferred to an unnamed mechanism; the author's ruling names it — **Edges**.
