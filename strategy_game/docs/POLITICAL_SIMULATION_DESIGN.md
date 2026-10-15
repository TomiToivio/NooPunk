# NoöPunk Strategy Game — Layer II: political simulation design proposal

**Status: proposal for author review (Gate B). No rules are approved, and no transition is
implemented.** Issue: [#282](https://github.com/TomiToivio/NooPunk/issues/282).

Gate B in [RULE_SYSTEM_RESEARCH.md](RULE_SYSTEM_RESEARCH.md) asks for an author-approved
political-simulation *methodology and assumptions* before any mechanic is coded. This document is
that proposal. It replaces nothing: [../RULEBOOK.md](../RULEBOOK.md) still says **NO RULES
APPROVED**.

## Scope: the theory as vocabulary, not as an import

The brief for this layer is a **simple, abstract, gamified political simulator built on LaclauGPT's
theories — not an import of the entire LaclauGPT.**

So LaclauGPT is used here as a *theory source* only. Its Phase 1 taxonomy supplies the words this
layer speaks, and nothing else. The vocabulary is implemented in
[`../political.py`](../political.py):

| Theory concept | Container |
| --- | --- |
| Demands as the unit of political reason (Laclau, *On Populist Reason*, 2005) | `Demand` |
| Signifiers and their roles — nodal, floating, empty (Laclau & Mouffe, 1985/2001) | `Signifier`, `SignifierRole` |
| Articulation of demands into equivalential chains (Laclau & Mouffe) | `Articulation` |
| The antagonistic frontier dividing inside from outside | `Frontier` |
| Communicative power: programming and switching (Castells, *Communication Power*, 2009) | `CommunicativeTie`, `PowerMode` |
| The bloc an observer reads out of a chain | `PoliticalFormation` |

**What is deliberately not imported:** the LaclauGPT package, its classifier, its corpus pipeline and
its data. There is no model, no inference, no sentiment pass, no prediction. `political.py` imports
`json`, `dataclasses`, `enum`, `typing` and `strategy_game.provenance` — and a test asserts *in a
subprocess* that importing the layer pulls in neither `laclaugpt` nor Mesa/NetworkX/Ollama/Concordia.

This also keeps the rule [INTEGRATION_BOUNDARIES.md](INTEGRATION_BOUNDARIES.md) sets: the taxonomy
**describes** discourse, so no analytic label is compiled into a causal transition formula.

## Abstraction rules this layer commits to (enforced by tests, not prose)

1. **Demands are the unit.** Not voters, not parties, not populations, not polling.
2. **No quantities at all.** No score, strength, influence or threshold is stored. Two tests enforce
   it: one walks the serialized payload and rejects any `int`/`float`, the other rejects
   metric-shaped keys. From the research note: *"Political hegemony is not automatically a scalar
   score."*
3. **An absence stays visible.** A signifier whose role was never recorded keeps `role = None`; a
   record whose provenance was never recorded keeps `UNKNOWN`. Neither is silently promoted — to
   `nodal`, or to `EVIDENCE`.
4. **Evidence and simulation stay apart.** A demand extracted from a corpus (`EVIDENCE`) and an
   articulation produced by a simulation run (`SIMULATED`) share a shape and never share a claim.

## The proposed loop — gamified, and not implemented

The player is one faction leader and acts **through articulation**, the way the theory describes
hegemony being built. A round offers a small set of abstract moves over the field:

- **articulate** — attach a demand to a signifier, extending an equivalential chain;
- **re-role** — declare a signifier nodal, floating or empty;
- **draw a frontier** — decide which demands the chain stands *against*;
- **program or switch** — set the meaning a tie carries, or connect/disconnect two actors.

How many moves a round grants, and what any of them costs, is **deliberately unset** — that is a
rule, and rules are the author's.

**How a hegemonic shift stays legible without a score.** The player reads the *structure*: which
demands sit inside a frontier, which signifier carries them, and which formation currently claims
that signifier. A shift is not a meter moving; it is the same signifier carrying a different chain.

*Illustrative micro-example* (invented for this document; not canon, not a scenario):

> The floating signifier *s1* carries `d1 housing, d2 transport`, with a frontier that excludes
> `d3 order`. A rival re-roles *s1* to **empty** and articulates `d3` to it, redrawing the frontier
> so `d1` and `d2` fall outside. Nothing was measured and nothing increased: *s1* now means a
> different chain, and the player can read that straight off `demands_of("s1")` and the frontier.

## Assumptions this proposal asks the author to approve (Gate B)

1. Political standing is represented **relationally** (chain + frontier + who claims a signifier),
   never as a scalar.
2. Demands, not people, are the atomic unit; the layer makes **no claim about populations or
   electorates**.
3. The theory's labels are **descriptive**: nodal/floating/empty and programming/switching classify a
   record, and none of them implies a transition, a probability or an effect size.
4. Corpus-derived records (`EVIDENCE`), authored scenario material (`AUTHORED`), machine text
   (`GENERATED`) and modelled outcomes (`SIMULATED`) stay distinguishable in every snapshot.
5. The layer is **standalone**: it is not wired into `WorldState` yet, and it refers to leaders and
   factions by id. Integration is a Gate D decision.

## Deliberately not modelled

No electorates, polling, vote shares or seat counts. No parties as fixed entities (a
`PoliticalFormation` is an *inference*, and the scaffold neither derives nor scores it). No media
reach, no audience size, no propaganda potency. No sentiment or affect measurement. No causal claim
that any articulation *causes* an outcome.

## Open questions for the author

1. Is the four-move loop the right shape, and should a round exist as a named unit at all?
2. Should a formation be recorded by the player, or inferred by a future (author-approved) rule?
3. Should re-roling a signifier cost anything, and if so, in what currency — which Layer III decides?
4. What makes a signifier *empty* rather than merely under-described — is that a player declaration
   or an observation?
5. Should the field reference Layer III assets/ties directly, or stay id-coupled as it is now?

## Implementation status

The tabletop layer built on this vocabulary - faction sheets, PCM demand and event cards, an
adversarial crisis and a one-page turn procedure - is in
[../../docs/design/ISSUE_479_PCM_LACLAU_MECHANICS.md](../../docs/design/ISSUE_479_PCM_LACLAU_MECHANICS.md)
(issue #479). It consumes this layer's containers and adds no rules.

**Implemented and tested (containers only):** the vocabulary above, deterministic JSON round-trip,
per-instance collections, the read-only queries `demands_of` / `signifiers_of`, the provenance
separation, and the two boundaries (no LaclauGPT/adapter import, no numeric quantity).

**Not implemented, awaiting Gate B:** every move in the proposed loop, any resolver, any cost, any
round structure, any win condition. `strategy_game/political.py` contains no transition function.
