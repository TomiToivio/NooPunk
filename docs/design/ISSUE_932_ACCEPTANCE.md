# Issue #932 — acceptance record: the GUMSHOE / Esoterrorists investigation mod

**Basis.** #932 is explicitly a **design deliverable**: *"Stop at written rules proposal. No
implementation PR, code or Godot changes until separately requested."* The proposal itself landed as
[`ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md`](ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md) (PR #933) and is not repeated
here. This record does the two things that proposal could not do for itself: it **checks the rules
digest against the supplied book**, and it **reconciles the proposal with the investigation layer that
is already implemented** (#704, #707) — so that nobody implements a second one. **No code, case,
scenario, Godot mechanic or rulebook text is added by this record.**

## 1. How the citations were checked

The supplied file is the 2nd-edition PDF, 162 pages. Its printed page numbers sit **one page after the
PDF viewer index** (`printed = index + 1`), which is why a citation has to say which one it means. Every
page number below is a **printed page**, the same convention as the issue:

| Chapter | Printed pages (verified openers / running heads) |
| --- | --- |
| Your Character | 8–18 (ability descriptions 11–17; the ability list by family on 18) |
| The GUMSHOE Rules System | 19–34 (chapter head first appears on 20) |
| Ordo Veritatis | 35–43 |
| The Enemy | 44–65 |
| Scenarios | 66–78 |
| Station Duty | 79–95 |

## 2. The digest, checked claim by claim

| Claim in §2 of the proposal | Where | Verdict |
| --- | --- | --- |
| Investigative and general abilities are different categories with different mechanics | 9–10, 11 | **confirmed** — and the book gives the reason the mod rests on: general-ability failure "can stop a mystery story dead if applied to the collection of information" |
| Investigative abilities come in three families (Academic, Interpersonal, Technical) | 11 | **confirmed** |
| The book has **40 investigative abilities** | 13–18 | **confirmed** — mechanically counted from the book's own table of contents, and the crosswalk in §4 covers **all 40** (see §3) |
| General abilities are a separate list; **Stability** is one of them | 16–18 | **confirmed** — 13 general abilities plus Stability, all present as rows in the crosswalk |
| A clue costs a die roll or a spend to find | 22 | **refuted, as the proposal says** — the book's rule is that access to necessary information is never dependent on a roll |
| Spending points buys a **special benefit**, never the core clue | 23 | **confirmed** — 1-point and 2-point spends, benefits are advantages, and some minor non-core information is free |
| Zero-point clues, inconspicuous clues, simple searches | 24 | **confirmed** — and the book adds an allocation rule the proposal omits (see §4.2) |
| Clue taxonomy: floating, leveraged (with prerequisite clues), pipe, restricted, timed result | 69 | **confirmed** — this is the book's own vocabulary, in a chapter the proposal cites |
| Stability is a full second psychological system | 32–34 | **confirmed** — which is exactly why it is refused rather than merged (see §4.3) |

## 3. The crosswalk is complete

The issue asked for a "full investigative + general crosswalk". Checked mechanically against the book's
own ability list: **40 of 40** investigative abilities appear in §4's table, none missing, and the 13
general abilities appear as a labelled `GUMSHOE general` block rather than being smuggled in as
investigative ones. One extra row, `Local Knowledge (Station Duty)`, is the book's campaign-framing
ability rather than a character ability — it is correctly marked as such.

## 4. Three corrections the proposal needs

### 4.1 "A positive rating", and where NoöPunk deliberately differs

The digest says a clue arrives with "an appropriate investigative ability with a positive rating …
even if its pool is empty". The book is precise at printed p. 9: an ability must be *held*; a positive
rating with an empty pool still yields every core clue tied to it; a **zero rating** yields nothing.

The implemented NoöPunk layer deliberately differs: `Investigator.is_competent` counts **CWN rank 0 as
trained**, because that is what `data/rules/without_number.json` says (`skills.min: 0`,
`untrained_check: -1`). So NoöPunk is *more generous* than its source here. That is a defensible choice —
it stops character creation from gating the first scene — but it must be **stated**, not left to be
discovered. It is already recorded as **G1** in `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md` §7; this
record only pins that the divergence is real and intentional.

### 4.2 Passive clues have an allocation rule, not just a name

The proposal lists "inconspicuous clues may be noticed without consciously investigating" but omits the
mechanic the book gives at printed p. 24: a clue in a transitional scene goes to whoever holds the
**highest current pool** in the ability, ties broken by highest rating. `inconspicuous_finder()` in
`src/rules/investigation.py` implements an allocation; whoever reviews that function should check which
rule it encodes before changing it.

### 4.3 Stability is refused because it is a system, not a flavour

Printed pp. 32–34 run Stability as a general ability with its own recovery, episode carry-over and
network-of-loved-ones bookkeeping. The proposal's refusal to import it is therefore correct, and the
existing AWN-derived Stress module is the single mental-cost track. Two parallel meters would contradict
each other the first time a table used both.

## 5. Reconciliation: what the proposal asks for and what already exists

I1–I10 are the proposal's rules. "Code" means it is on `main` with tests, not that it is approved for
play — approval is the author's (§6).

| Rule | Status today | Where |
| --- | --- | --- |
| **I1** core clue never behind a roll or a spend | **implemented** | `discover()` has no roll parameter; `tests/test_investigation_layer.py` asserts no die/RNG in the path |
| **I2** risky *actions* roll normally, and a failed action does not erase the lead | **implemented as the split**, the failure branch is author policy | `src/rules/investigation.py` (discovery vs action), G3 in the layer doc |
| **I3** expertise tags as descriptors, never locks | **proposal only** | nothing in code; queued as **D59** |
| **I4** extra discoveries, no investigative pool | **implemented as the refusal** — no `spend()`/`pool()` exists and a test asserts their absence | `Investigator`; the resource variant stays **G2** |
| **I5** evidence vs interpretation recorded separately | **implemented** | `Clue.fact` vs `Hypothesis`/`Stance`; `CaseGraph.validate` requires a mundane *and* an anomalous hypothesis |
| **I6** clue types: passive, zero-point, core, floating, leveraged, pipe, restricted, timed | **partly implemented** — core/passive/terminal exist; floating, leveraged, pipe, restricted and timed are book vocabulary with no representation yet | `ClueKind`, `Scene.passive_clues`, `terminal:` scenes |
| **I7** CWN skills govern expertise; no GUMSHOE ratings | **implemented** | `Investigator.from_sheet` over the CWN skill list |
| **I8** Stress instead of Stability; no clinical claims | **implemented** elsewhere | `mods/noopunk/stress.gd` + `data/rules/awn_stress.json` (#928) |
| **I9** accept a plausible method not written in the scenario | **implemented** | `discover(..., alternative_method=True)` |
| **I10** semantic conversion of a GUMSHOE case, not a numeric one | **policy only** — and it is a *GM* procedure, so it belongs in a scenario document, not in code | §4 table above |

**The consequence for the next agent:** I1, I2, I4, I5, I7, I8 and I9 are done; do not re-implement them.
The open implementation work, if it is ever authorised, is **I6's five clue types** (floating, leveraged,
pipe, restricted, timed) and **I3's tags** — both additive to the case-graph schema, neither touching a
CWN rule.

## 6. The issue's acceptance criteria

| # | Criterion | Position |
| --- | --- | --- |
| 1 | Agree CWN is unchanged and always primary | **met** — restated in the proposal's precedence order and enforced by the #897 lock |
| 2 | Review the GUMSHOE summary against book pp. 8–34, 35–65, 66–77, 79–95 | **met by this record** (§1–§2): every load-bearing claim checked, three corrections recorded |
| 3 | Approve or tweak the full crosswalk | **author decision** — completeness *verified* (§3); approval is queued as part of **D59** |
| 4 | Agree expertise tags as optional descriptors | **author decision — D59** |
| 5 | Agree core clues never hinge on a failed roll or a spend, while risky actions still use CWN | **met** — implemented and tested (I1, I2) |
| 6 | Decide whether extra discoveries are free or need a resource rule | **author decision — already rowed as G2** in the layer doc; recommendation on record: free |
| 7 | Align psychological horror with Stress, no Stability | **met** — implemented (#928), refusal justified at §4.3 |
| 8 | Approve the UNSA/Ordo, NHI/Esoterrorist, containment/veil-out and Station Duty conversions; keep rookie-PC agency and Romppainen as NPC | **author decision — D60** for the institution mapping; the PC/NPC guardrail is already executed in the proposal §6 |
| 9 | Review a generic multi-scene graph for loops, bottlenecks and alternative routes; author no Lakkahaltia scenario | **partly met** — the shipped `data/scenarios/lakkahaltia/case_graph.json` is a validated multi-scene graph and `CaseGraph.validate` rejects dead ends; a *generic, scenario-independent* graph is not authored, and authoring one is scenario work this issue forbids |
| 10 | Record licensing/attribution boundaries | **met** — §7 |
| 11 | Stop at the written proposal | **met** — no code in this PR |

## 7. Licensing boundary for *The Esoterrorists* specifically

The GUMSHOE SRD is CC BY 3.0 and carries a prescribed attribution sentence, and it grants the GUMSHOE
mark while withholding the game-line marks. **This book is not the SRD.** *The Esoterrorists* is a
commercial game line whose mark the SRD licence explicitly does not grant, and it has no open licence.

Consequences, binding on anything derived from this issue:

- the book is a **reference the author owns**, never committed: no text, table, page image, adventure,
  Ordo Veritatis setting material, creature or example character is reproduced in this repository;
- what §2–§5 above take from it are **mechanics and procedure** (which cannot be copyrighted) and the
  **page locators** needed to re-check them;
- the *names* stay out of NoöPunk's own vocabulary: the UNSA mapping in §5 of the proposal exists
  precisely so that none of the book's institutions, entities or marks appear in shipped material;
- if NoöPunk ever claims GUMSHOE compatibility in a published build, the SRD's attribution sentence —
  and only that sentence — goes where our own notice sits (`docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`
  §0 carries it verbatim, as the licence requires).

## 8. What this record does not do

It adds no rule, no case, no scenario, no Godot or Python change and no test — the issue forbids all of
them, and #271 forbids prose guards. It does not approve the crosswalk, the tags or the institution
mapping; those are rows **D59**, **D60** and the existing **G1–G5**. It does not author a Lakkahaltia
scenario, and it keeps Dr. Romppainen an NPC supervisor rather than the protagonist.
