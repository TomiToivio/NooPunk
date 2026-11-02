# LaclauGPT as a NoöPunk mod: DA, DNA, SNA (#1042)

**Status: character-level layer implemented and tested; SWN faction level deferred, as the issue instructs.**
`mud/nopunk_mud/ideology.py` · `mud/tests/test_ideology_1042.py` · 10 tests, full MUD suite green.

## The separation is the design

Three questions get asked about politics in a game and they are not the same question:

| Layer | Question | Object |
|---|---|---|
| **DA** | What did they *say*? | `Statement` — stance, demand, source, evidence kind |
| **DNA** | Where do they *stand*? | `positions()`, `contested_concepts()` |
| **SNA** | Who do they *know*? | `Relationship` — trust, debt |

The rule that makes the mod safe to build on: **none of these collapses into one friend/enemy score.** They are enforced structurally, not by convention —

- `Relationship` has no `stance`, no `concept`, no ideology field.
- `Statement` has no `trust`, no `debt`.
- `antagonists_are_not_enemies(a, b)` returns **overlap and trust side by side**, and the test asserts the pair `{overlap: 2, trust: -4}`: two shared signifiers, mutual contempt. A model that cannot represent that will turn every faction into a team.

## Evidence is not truth

Every statement carries an `evidence` kind: `document`, `testimony`, `observation`, `rumour`, `assertion`. Only the first three count as evidence-backed, `positions(evidence_only=True)` filters the rest out, and a rumour is never silently promoted by being repeated.

## Visibility has three levels, and the last two differ

- `public` — everyone.
- `private` — the speaker's own network knows it was said; outsiders do not.
- `secret` — need-to-know: **even the speaker's own network does not see it** without `shares_secret`, which means "someone told you".

I got this wrong first: my initial test treated `secret` as merely `private`, which is a distinction without a difference. The test now pins the sharper semantics, and the docstring states them.

## Determinism

Authored statements in, graph arithmetic out. No model call, no sampling, no hidden state. `positions()` returns sorted keys so two runs over the same fixtures are byte-identical — which is what lets a faction's politics be *argued with* instead of oracled.

An LLM may later suggest an interpretation. It may not become the thing the game reads.

## What is deliberately not here

- **No SWN faction integration.** The issue says defer it, and the strategic layer belongs behind #1008 Phase 3's unmodified SWN engine.
- **No automatic effect on reputation or reactions.** Ideology changes dialogue, access and what a faction asks of you; any movement of a reputation value is an explicit, logged event per Phase 1 rules.
- **No Palonen index.** The formula is named in the plan; its coefficients come from the paper, not from taste.

## Next

1. Authoring fixtures for the Helsinki starting cast — as data, reviewed, not generated.
2. A read-only view for the MUD (`ideology` command) that shows the PC only what they could know.
3. Then, and only then, the faction-level projections against real SWN faction state.
