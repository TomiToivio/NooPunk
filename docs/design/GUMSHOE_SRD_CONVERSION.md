# GUMSHOE → CWN conversion, from the SRD (#932)

**Authority:** GUMSHOE SRD (OGL version), Pelgrane Press. **Engine:** CWN, per the #897 lock. This document
converts an *investigation procedure*, not a ruleset: attributes, saves, 2d6 checks, combat, hacking and
progression stay CWN's, untouched.

Implementation: `mods/noopunk/gumshoe_investigation.gd` and `data/rules/gumshoe_investigative.json`, tested by
`godot/tests/test_gumshoe_932.gd`. Design context: [`ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md`](ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md).

## What is borrowed, and only this

| SRD rule | Verbatim intent | What we do |
|---|---|---|
| *Gathering Clues* — "you will never fail to gain a piece of necessary information. It is never dependent on a die roll" | essential information is free to a competent investigator | `gather()` returns the clue; it has no failure branch and rolls nothing |
| *Core Clues* — "the clue you absolutely need to move to the next scene… costs nothing" | the spine of the case cannot be missed | `core: true` is recorded, and still costs **zero** pool |
| *Special Benefits* — "each benefit costs either 1 or 2 points" | spending buys colour, advantage, goodwill — never the solution | `buy_benefit()` accepts cost 1–2 only, and returns no clue |
| *Investigative Ratings* — "spent points do not return until the next investigation begins" | pools are a per-case resource | `refresh()` restores every pool to its rating and forgets benefits |
| *Tests* — "Tests apply to general skills only"; GUMSHOE rolls a d6 | general action can fail | **not imported.** `delegate_to_cwn()` takes the CWN result and adds no die |

The last row is the important one. Importing GUMSHOE's d6 general tests would create a second resolution
engine beside CWN's 2d6 — exactly what the foundational lock forbids. Where an outcome is in doubt, CWN
resolves it; the overlay only decides what a spent point can add.

## What a rating buys

A rating of **1** is professional competence. With it, the investigator gets the information the scene holds.
An **empty pool does not block this** — the pool is for benefits, not for access. This is the single
behaviour that makes investigative games feel different from dice gates, and it is asserted in the suite.

An investigator **without** the ability is not stuck either: every converted ability names the CWN skill that
covers the same ground, so a character built purely on CWN can still work the case at 2d6.

## Ability conversion

| GUMSHOE ability | Kind | CWN skill | Used for |
|---|---|---|---|
| Research | academic | Know | archives, records, names into files |
| Textual Analysis | academic | Administer | authorship, redaction, format tells |
| History | academic | Know | institutional memory, old names for old crimes |
| Law | academic | Administer | jurisdiction, warrants, which badge authorises this |
| Occultism | academic | Know | cults, noetic claims, belief vs evidence |
| Forensic Pathology | academic | Heal | cause and time, contradictions with the report |
| Biology | academic | Heal | non-human tissue, contamination |
| Cryptography | technical | Program | ciphers, signatures |
| Data Retrieval | technical | Program | finding the record that exists |
| Evidence Collection | technical | Notice | scene search |
| Ballistics | technical | Fix | weapons, damage reconstruction |
| Chemistry | technical | Fix | substances, residues |
| Interrogation | interpersonal | Talk | pressure; elicits statements, not truth |
| Reassurance | interpersonal | Talk | witness care; the frightened person speaks |
| Streetwise | interpersonal | Connect | who to ask, and what not to ask |
| Bureaucracy | interpersonal | Administer | which form unlocks the door |

**Sixteen abilities, not the SRD's full list.** A conversion that ships forty abilities nobody uses is a
second skill list with extra steps. Adding one means adding its CWN skill mapping in the same edit — the test
fails otherwise.

## Scene structure for a NoöPunk case

Adapted from the SRD's investigative scenario shape:

1. **Hook** — the case arrives through an institution, not a mystery box.
2. **Scenes** — each has one **core clue** that points onward, plus optional clues that colour it.
3. **Benefits** — at 1–2 points, buy advantage: an earlier interview, a favour, a name, a head start.
4. **Climax** — the confrontation CWN resolves (combat, chase, hacking, or a hard social check).
5. **Wrap-up** — consequences, including the institutional ones.

The evidence notebook from #897/#913 keeps the clue graph; this overlay adds the pool accounting and the
"core clue is free" guarantee to it.

## What this conversion deliberately does not do

- **No d6 general tests.** CWN resolves uncertainty.
- **No second ability list.** Investigative abilities are an overlay; general competence is CWN skills.
- **No Stability or Stress import.** NoöPunk has its own Psyche overlay (`mods/noopunk/psyche.gd`).
- **No copied Esoterrorists text, creatures or cases.** The SRD is the source; original cases are authored.
- **No automatic truth.** An occult clue is evidence, not a cosmology.

## Acceptance mapping (#932)

| Issue requirement | Status |
|---|---|
| preserve CWN sheet, skills, 2d6, saves, combat, hacking | untouched; overlay imports none of it |
| essential clues never gated by a roll | `gather()` has no failure path; asserted with an empty pool |
| clues vs interpretation separated | `gather()` returns information; spending returns benefits |
| translate cases scene-by-scene | scene structure above; per-scene core clue + optional benefits |
| no second resolution engine | `delegate_to_cwn()`; suite asserts `engine == "cwn"` |
| no GUMSHOE d6 tests | not implemented, deliberately |
| uncanny tone preserved | the overlay never decides whether a clue is *true* |
