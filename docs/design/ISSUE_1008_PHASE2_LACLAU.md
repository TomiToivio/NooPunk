# Phase 2 plan: the LaclauGPT ideology overlay (#1008)

**Status: plan. Not implemented.** Phase 1 is the launch blocker; this is the layer that makes a faction game
argue rather than merely fight.

## What the mod is, in one sentence

A faction's position is not a stat but a **structured claim about what words mean**, and power is the ability to
make one reading of a floating signifier stick.

## Mapping the paper onto play

The reference is `LaclauGPT/paper/PHASE_1_PAPER.md` (42,788 chars, Sections 1–5): Laclau and Mouffe's discourse
theory, Palonen's Formula of Populism, sociotechnical imaginaries, Discourse Network Analysis, an
evidence-linked workflow, and an "LLM structuralism" methodological bridge.

| Paper element | In-game object |
|---|---|
| Actor | faction, bloc, outlet, NPC speaker |
| Concept / signifier | *Humanity*, *Security*, *Freedom*, *Consciousness*, *Acceleration*, *Stability* |
| Statement (support/oppose) | one articulation with a stance, a demand, a source and a timestamp |
| Chain of equivalence | weighted actor→signifier edges forming a bloc |
| Antagonism / frontier | explicit negative link between signifiers or blocs |
| Competing hegemonic projects | clusters of chains, scored by coverage and coherence |
| Sociotechnical imaginary | the future a bloc claims its project will produce |
| Evidence-linked workflow | every statement carries provenance, confidence and a visibility class |

## The four separations that keep it honest

1. **Speech ≠ belief.** A statement is something an actor *said*, not what it thinks.
2. **Belief ≠ truth.** A rumour and a verified document are both statements; only provenance distinguishes them.
3. **Ideological agreement ≠ reputation, alliance, loyalty or affection.** Sharing a chain of equivalence makes
   two actors *legible* to one another, not friendly.
4. **Player knowledge ≠ world state.** What the PC may see is a projection with spoiler gating, never the model.

## Deterministic by default

The gameplay layer must run with **no LLM at all**: statements are authored data, projections are graph
arithmetic, and every derived number is reproducible from the same fixtures. An LLM may *suggest*
interpretations (as the paper's workflow does for corpus analysis) but a human-authored rule validates any
change, and the deterministic path is the one that ships.

Suggested data layout, mirroring what the paper's pipeline already produces:

```
data/ideology/concepts.json          # signifiers, each with a short in-world gloss
data/ideology/actors.json           # factions and speakers, with network scope
data/ideology/statements.jsonl      # one articulation per line: actor, concept, stance, demand, source, date
```

## Projections worth building first

- **Bloc view**: which actors cluster on which signifiers; who is isolated.
- **Contested signifier view**: a word whose meaning is claimed by two blocs at once — the most interesting
  object in the whole system, and the natural generator of plot.
- **Drift**: how a faction's articulations move over a campaign, which is what makes an alliance collapse
  legible in retrospect instead of arbitrary.

## Palonen's Formula of Populism

Recorded here as a **named function with no coefficients yet**. The paper defines it; this project will not
invent weights to look finished. Implementation is `populism_index(actor, window) -> float` once the formula is
transcribed from the paper with its own definitions, and a test that pins it to worked examples.

## Effects must be bounded

Ideology may change: available dialogue, who will meet you, which faction goal becomes legible, what a faction
asks of you, and how a news item reads. Ideology may **not** silently move a reputation value or a reaction
roll; any such effect is an explicit, logged, bounded event with a reason, per Phase 1's rules.

## Tests this layer will need

- determinism: same fixtures → same projection, byte-identical
- no-LLM path: the whole layer runs with the LLM gateway absent
- provenance: every statement resolves to a source object
- spoiler gating: a secret statement cannot appear in a public projection
- separation: an actor with +ideological overlap and −reputation is representable and stable
