# Issue #932 — acceptance record: the GUMSHOE SRD investigation mod

**Basis.** #932 is a **design deliverable**: *"Stop at written rules proposal. No implementation PR, code
or Godot changes until separately requested."* The proposal is
[`ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md`](ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md). This record checks that proposal
against the **GUMSHOE SRD (OGL version)** and reconciles it with the investigation layer already
implemented in #704/#707, so nobody builds a second one. **No code, case, scenario, Godot mechanic or
rulebook text is added here.**

## 0. Re-based on the OGL SRD, not on a commercial game

The first version of the proposal summarised a commercial GUMSHOE game the author owns as *inspiration*.
That was wrong for the record, though not for the table: the book is not open, and its game-line name is
declared **Product Identity** in the SRD's own copyright notice — a mark the licence grants to nobody.
The proposal is therefore re-based on the **GUMSHOE SRD, OGL version** (68 pp., © 2013 Pelgrane Press,
**Open Game License v1.0**), whose whole text is open content except the declared marks.

Three consequences, all executed in the rewrite:

| Was | Now | Why |
| --- | --- | --- |
| Digest page cites from the commercial book | **SRD page cites** (pp. 2, 5, 19–26, 32–33, 56–60) | verifiable by anyone with the open file |
| "40 investigative abilities" | **52 investigative** (19 Academic · 16 Interpersonal · 17 Technical) + **24 general** | counted from the SRD's own ability descriptions, pp. 6–26 |
| Setting vocabulary from the commercial line (its agency, its entities, its reality-boundary idea, its cover-story term, its station framing) | **NoöPunk's own institutions** in §6 of the proposal | none of those words is open content, and none is needed |

One digest term was **dropped as not in the SRD**: "zero-point clue". The SRD's open-content equivalents
are *passive clues* (p. 32), *inconspicuous clues* and *simple searches* (p. 33), and those are what the
proposal now uses.

## 1. The digest, checked claim by claim against the SRD

| Claim | SRD page | Verdict |
| --- | --- | --- |
| Open content: the whole document except the declared product identity; no mark granted | 1 | **confirmed** |
| Investigative and general abilities are two mechanics by design | 2, 5, 19 | **confirmed** — the reason is stated: failure is what a general test adds, and that is what an information roll must not do |
| Rating is static competence, pool is spent | 2 | **confirmed** — the SRD calls the distinction crucial |
| A rating of at least 1 is needed for useful information | 5 | **confirmed** — and it is the one place NoöPunk deliberately diverges (§3.1) |
| 52 investigative abilities in three families | 6–26 | **confirmed by counting**; the crosswalk covers all 52 |
| 24 general abilities, Stability among them | 19–26 | **confirmed** |
| Core clue: the GM avoids obscure gating, and the listed ability is "just one possibility, not a straight jacket" | 32 | **confirmed** |
| Passive clues arrive unprompted | 32 | **confirmed** |
| Inconspicuous clues go to the highest current pool, ties by rating | 33 | **confirmed** — and it is an allocation rule, not a flavour note |
| Simple searches need no ability and no roll | 33 | **confirmed** |
| Special benefits are bought with pool points and are advantages, not the clue | 32 | **confirmed** |
| Clue types: floating (56), leveraged (56), pipe (57), restricted (57), timed (57–58) | 56–58 | **confirmed** |
| Scene types: introductory, core, alternate, antagonist reaction, hazard, conclusion, hybrid | 58–60 (diagrams 61) | **confirmed** — *subplot* is **not** an SRD scene type and was dropped from the digest |
| Stability is a general ability with its own system | 25 + surrounding rules | **confirmed** — which is why refusing it is structural |

The SRD carries no setting, no institutions and no antagonist cosmology, so §6 of the proposal needed no
licence at all: it is NoöPunk's own design.

## 2. The crosswalk is complete for the SRD

Checked mechanically against the SRD's ability descriptions: **52 of 52** investigative abilities appear
in §5.1, and **24 general abilities** appear as a labelled block in §5.2 that explicitly says they are
*not* converted into CWN skills. Nineteen CWN skills against 52 SRD abilities means many-to-one by
construction — that is the point of a GM reference: `Know` absorbs a dozen scholarly fields, `Talk`
absorbs the interpersonal ones.

## 3. Three points a reviewer should decide on purpose

### 3.1 Rank 0 counts as trained — more generous than the SRD
The SRD needs a rating of at least 1 (p. 5). CWN says rank 0 is trained (`untrained_check: -1`,
`skills.min: 0`), and the implemented layer treats competence as **presence**
(`Investigator.is_competent`). NoöPunk will therefore hand over a core clue to a character the SRD would
refuse. Deliberate — it stops character creation gating the first scene — and recorded as **G1** in
`docs/rules/GUMSHOE_INVESTIGATION_LAYER.md` §7.

### 3.2 Passive clues are allocated, not merely named
Highest current pool, ties by highest rating (p. 33). `inconspicuous_finder()` implements an allocation;
check which rule it encodes before changing it.

### 3.3 Stability is refused because it is a system
A general ability with recovery, episode carry-over and its own consequences. Two mental-cost tracks
would contradict each other the first time a table used both, so the AWN-derived Stress module (#928)
stays the only one.

## 4. Reconciliation: what the proposal asks for and what already exists

I1–I10 are the proposal's rules. "Code" means it is on `main` with tests — not that it is approved for
play; approval is the author's (§5).

| Rule | Status today | Where |
| --- | --- | --- |
| **I1** core clue never behind a roll or a spend | **implemented** | `discover()` has no roll parameter; `test_discovery_takes_no_randomness` asserts no `roll/die/dice/rng/random` in the signature |
| **I2** risky actions roll normally; a failed action does not erase the lead | **implemented as the split**, the failure branch is author policy | `src/rules/investigation.py`; **G3** |
| **I3** expertise tags as descriptors, never locks | **proposal only** | queued as **D59** |
| **I4** extra discoveries; no investigative pool | **implemented as the refusal** — no `spend()`/`pool()`, asserted by `NoPoolEconomyTest` | `Investigator`; a resource variant stays **G2** |
| **I5** evidence vs interpretation recorded separately | **implemented** | `Clue.fact` vs `Hypothesis`/`Stance`; `CaseGraph.validate` requires a mundane **and** an anomalous hypothesis, and rejects conclusion-words in a fact |
| **I6** passive, inconspicuous, core, optional, floating, leveraged, pipe, restricted, timed | **partly implemented** — `ClueKind` has only core/optional, plus `terminal:` scenes and `inconspicuous_finder()`; the five SRD clue types have no representation | `src/rules/investigation.py` |
| **I7** CWN skills govern expertise; no SRD ratings | **implemented** | `Investigator.from_sheet` |
| **I8** Stress instead of Stability | **implemented** elsewhere | `mods/noopunk/stress.gd` + `data/rules/awn_stress.json` (#928) |
| **I9** accept a plausible method not in the scenario | **implemented** | `discover(..., alternative_method=True)`, `test_an_alternative_method_is_granted_not_rolled` |
| **I10** semantic conversion of a GUMSHOE case | **policy only** — a GM procedure, so it belongs in a scenario document | §5 of the proposal |

**For the next agent:** I1, I2, I4, I5, I7, I8 and I9 are done; do not re-implement them. The open
implementation surface is **I6's five clue types** and **I3's tags** — additive to the case-graph schema,
touching no CWN rule, and not authorised by this issue.

## 5. The issue's acceptance criteria

| # | Criterion | Position |
| --- | --- | --- |
| 1 | CWN unchanged and always primary | **met** — precedence order in the proposal, enforced by the #897 lock |
| 2 | Review the digest against the SRD (pp. 2, 5, 19–26, 32–33, 56–60) | **met by this record** (§1): every load-bearing claim checked, one term dropped, one count corrected |
| 3 | Approve or tweak the full 52 + 24 crosswalk | **author decision — D59**; completeness *verified* (§2) |
| 4 | Expertise tags as optional descriptors | **author decision — D59** |
| 5 | Core clues never hinge on a failed roll or a spend, while risky actions still use CWN | **met** — implemented and tested (I1, I2) |
| 6 | Extra discoveries free, or a resource rule | **author decision — G2**, recommendation on record: free |
| 7 | Stress instead of Stability | **met** — implemented (#928), refusal justified (§3.3) |
| 8 | Approve the NoöPunk institution mapping; keep rookie-PC agency and Romppainen as NPC | **author decision — D60** for the mapping; the PC/NPC guardrail is already written into §6–§7 |
| 9 | Review a generic multi-scene graph; author no Lakkahaltia scenario | **partly met** — the shipped `case_graph.json` is a validated multi-scene graph and `CaseGraph.validate` rejects dead ends; a *generic, scenario-independent* graph is scenario work this issue forbids |
| 10 | Record licensing/attribution boundaries | **met** — §0 and §6 |
| 11 | Stop at the written proposal | **met** — no code in the PRs behind this issue |

## 6. Licensing boundary

- **Used:** GUMSHOE SRD, OGL version, 68 pp., © 2013 Pelgrane Press, **Open Game License v1.0**. Open
  content is everything except the declared Product Identity — trademarked game-line names — and the
  licence grants neither those marks nor the GUMSHOE logo.
- **Obligations when anything ships:** include the OGL text and its Section 15 copyright notice, declare
  which parts are open content and which are product identity, and invent NoöPunk's own words for
  everything a withheld mark would name.
- **Not used and not adapted:** any commercial GUMSHOE game line — setting, institutions, entities,
  creatures, adventures. The author's commercial copy informed tone only; its text, tables and page images
  stay out of this repository.
- **No SRD text is reproduced here either.** What this record takes is procedure (not copyrightable) and
  page locators, which is the whole point of an open licence.
- The SRD's italic bracketed notes are guidance to implementers; they are not carried into NoöPunk.

## 7. What this record does not do

It adds no rule, case, scenario, Python or Godot change and no test — the issue forbids them, and #271
forbids prose guards. It does not approve the crosswalk, the tags or the institution mapping; those are
**D59**, **D60** and the existing **G1–G5**. It does not author a Lakkahaltia scenario, and it keeps Dr.
Romppainen an NPC supervisor rather than the protagonist.
