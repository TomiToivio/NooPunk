# Issue #932 — acceptance record: the GUMSHOE SRD investigation mod

**Basis.** #932 is explicitly a **design deliverable**: *"Stop at written rules proposal. No
implementation PR, code or Godot changes until separately requested."* The proposal itself landed as
[`ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md`](ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md) (PR #933) and is not repeated
here. This record does the two things that proposal could not do for itself: it **checks the rules
digest against the GUMSHOE SRD**, and it **reconciles the proposal with the investigation layer that
is already implemented** (#704, #707) — so that nobody implements a second one. **No code, case,
scenario, Godot mechanic or rulebook text is added by this record.**

## 1. How the citations were checked

Citations name a **section of the [GUMSHOE SRD (OGL)](https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf)**,
never a page of a commercial book. No commercial GUMSHOE game supplies the rules basis: the SRD is the open
source, and the proprietary settings, adventures and creature material are out of scope by construction.

| SRD section | What it settles here |
| --- | --- |
| *Investigative Abilities* | ratings, pools, three families, the free-information principle |
| *General Abilities* | the separate list, including Stability |
| *Gathering Clues* | three conditions, never a die roll |
| *Core Clues* | the scene's essential clue costs nothing |
| *Special Benefits* | 1–2 point spends, advantages only |
| *Tests* / *Contests* | general action can fail; **not imported** |
| *Stability* | a full second mental system; **not imported** |

## 2. The digest, checked claim by claim

| Claim in §2 of the proposal | SRD section | Verdict |
| --- | --- | --- |
| Investigative and general abilities are different categories with different mechanics | *Investigative Abilities*, *General Abilities* | **confirmed** — the SRD states that a test applies to general skills only, which is why the overlay never rolls for a clue |
| Investigative abilities come in three families (Academic, Interpersonal, Technical) | *Investigative Abilities* | **confirmed** |
| The SRD publishes a full investigative ability list | *Investigative Abilities* | **confirmed** — and NoöPunk converts **sixteen** of them deliberately (see §3); a conversion that ships the whole list is a second skill list by installments |
| General abilities are a separate list; **Stability** is one of them | *General Abilities*, *Stability* | **confirmed** — and Stability is refused rather than merged (see §4.3) |
| A clue costs a die roll or a spend to find | *Gathering Clues* | **refuted, as the proposal says** — "It is never dependent on a die roll" |
| Spending points buys a **special benefit**, never the core clue | *Special Benefits*, *Core Clues* | **confirmed** — 1- and 2-point spends, benefits are advantages, and a core clue costs nothing |
| Zero-point clues, inconspicuous clues, simple searches | *Gathering Clues* | **confirmed** — and the SRD adds an allocation rule the proposal omits (see §4.2) |
| Clue taxonomy: floating, leveraged (with prerequisite clues), pipe, restricted, timed result | *Scenario Structure* | **confirmed** — the SRD's own vocabulary, adopted as-is |
| Stability is a full second psychological system | *Stability* | **confirmed** — which is exactly why it is refused rather than merged (see §4.3) |

## 3. The crosswalk is complete

The issue asked for a "full investigative + general crosswalk". The conversion in
`data/rules/gumshoe_investigative.json` ships **sixteen** abilities, each mapped to the CWN skill that covers
the same ground, and the suite fails if any of them loses that mapping. Sixteen is a design decision, not an
oversight: the goal is a procedure a table will actually use, not a second skill list arriving in instalments.

General abilities are **CWN's own skills**. The overlay does not convert them, because doing so would create
the second resolution engine the #897 lock forbids.

## 4. Three corrections the proposal needs

### 4.1 "A positive rating", and where NoöPunk deliberately differs

The digest says a clue arrives with "an appropriate investigative ability with a positive rating …
even if its pool is empty". The SRD is precise in *Investigative Abilities*: an ability must be *held*; a positive
rating with an empty pool still yields every core clue tied to it; a **zero rating** yields nothing.

The implemented NoöPunk layer deliberately differs: `Investigator.is_competent` counts **CWN rank 0 as
trained**, because that is what `data/rules/without_number.json` says (`skills.min: 0`,
`untrained_check: -1`). So NoöPunk is *more generous* than its source here. That is a defensible choice —
it stops character creation from gating the first scene — but it must be **stated**, not left to be
discovered. It is already recorded as **G1** in `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md` §7; this
record only pins that the divergence is real and intentional.

### 4.2 Passive clues have an allocation rule, not just a name

The proposal lists "inconspicuous clues may be noticed without consciously investigating" but omits the
mechanic the SRD gives in *Gathering Clues*: a clue in a transitional scene goes to whoever holds the
**highest current pool** in the ability, ties broken by highest rating. `inconspicuous_finder()` in
`src/rules/investigation.py` implements an allocation; whoever reviews that function should check which
rule it encodes before changing it.

### 4.3 Stability is refused because it is a system, not a flavour

*Stability* runs as a general ability with its own recovery, episode carry-over and
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
| 8 | Approve the UNSA agency, NHI adversary, containment and recurring-base conversions; keep rookie-PC agency and Romppainen as NPC | **author decision — D60** for the institution mapping; the PC/NPC guardrail is already executed in the proposal §6 |
| 9 | Review a generic multi-scene graph for loops, bottlenecks and alternative routes; author no Lakkahaltia scenario | **partly met** — the shipped `data/scenarios/lakkahaltia/case_graph.json` is a validated multi-scene graph and `CaseGraph.validate` rejects dead ends; a *generic, scenario-independent* graph is not authored, and authoring one is scenario work this issue forbids |
| 10 | Record licensing/attribution boundaries | **met** — §7 |
| 11 | Stop at the written proposal | **met** — no code in this PR |

## 7. Licensing boundary: the SRD, not a commercial game

The GUMSHOE SRD is open game content with a prescribed attribution sentence, and it grants the GUMSHOE mark
while withholding the marks of the commercial game lines. No commercial GUMSHOE game is a rules source for
NoöPunk, and none is required.

Consequences, binding on anything derived from this issue:

- the **only** rules reference is the GUMSHOE SRD (OGL); no commercial book is quoted, committed or
  paraphrased as authority;
- what §2–§5 take from the SRD are **mechanics and procedure** (which cannot be copyrighted) and section
  locators, not page numbers of a closed text;
- the SRD's **setting-neutral** vocabulary is used; NoöPunk's UNSA, its institutions and its adversaries are
  original, and no commercial game's named factions, entities or marks appear in shipped material;
- if NoöPunk ever claims GUMSHOE compatibility in a published build, the SRD's attribution sentence — and only
  that sentence — goes where our own notice sits (`docs/rules/GUMSHOE_INVESTIGATION_LAYER.md` §0 carries it
  verbatim, as the licence requires).

## 8. What this record does not do

It adds no rule, no case, no scenario, no Godot or Python change and no test — the issue forbids all of
them, and #271 forbids prose guards. It does not approve the crosswalk, the tags or the institution
mapping; those are rows **D59**, **D60** and the existing **G1–G5**. It does not author a Lakkahaltia
scenario, and it keeps Dr. Romppainen an NPC supervisor rather than the protagonist.
