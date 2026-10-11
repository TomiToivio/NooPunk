# Layer II: the political simulator model (design record, not rules)

**Status: design record for issue [#282](https://github.com/TomiToivio/NooPunk/issues/282). No
rules are approved and none are proposed here.** This document explains the *shape* of the
political layer's data and why it is that shape. It does not define statistics, thresholds, turn
cadence, costs, strengths, scores, transitions, victory conditions or agent decision
algorithms — those wait on the author, and on Gate B in
[`RULE_SYSTEM_RESEARCH.md`](RULE_SYSTEM_RESEARCH.md).

**Scope authority is [`POLITICAL_SIMULATOR_SCOPE.md`](POLITICAL_SIMULATOR_SCOPE.md)**, which
states the prime directive — build a game *inspired by* LaclauGPT's theories, do not import or
recreate LaclauGPT — and maps each research inspiration onto a candidate player-facing
abstraction. This document is the *code-side companion* to it: what the scope decision implies
for the data containers the scaffold actually has. Where the two disagree, the scope document
wins and this one is stale.

Code: `strategy_game/politics.py` (vocabulary), the Layer II collections on `WorldState`,
`board_view` and `political_view` in `strategy_game/view.py`.

## The design, in one sentence

**The political field is one labelled multiplex graph.** The theory's concepts are *node kinds*;
its relations are *edge layers* on the existing `NetworkEdge`.

```
nodes:    Demand · Signifier · Formation · Frontier      (politics.PoliticalNodeKind)
edges:    NetworkEdge(source, target, layer=…)           (reused, not re-declared)
layers:   articulation · equivalence · antagonism · communication   (politics.RelationLayer)
```

## Why this shape, rather than one subsystem per concept

**Abstract.** Articulation chains, equivalential links, antagonistic frontiers and communicative
ties are all relations. Giving each its own class would create four structures that behave
identically and must be rendered four times. One edge container with a label keeps the whole
political field as a single object a viewer or a player can look at.

**Simple.** There is no corpus, no NLP, no model, no extraction pipeline and no numbers anywhere
in the layer. `Signifier` carries a `kind` label and a provenance record; `Demand` carries a
claimant reference; `Formation` and `Frontier` carry a label. That is the entire vocabulary.

**Gamified.** The player-facing question this layer exists to answer is *"who is linked to what,
and where does the frontier run?"* — and in this design that question is answered by literally
reading the graph. A player can see a demand attached to a signifier, two demands drawn into the
same chain, and a boundary drawn between formations, without any of it being reduced to a score.
That is what makes it playable and legible rather than a research instrument.

**One graph, not two.** Political relations reuse `NetworkEdge`. A second edge type would mean
two ways to express "these two things are connected", which is the duplication the noösphere
side of this repository has had to undo before.

**`Frontier` is a node, not an edge.** A frontier is a relation in the theory, but it is the
*subject of play* — a player acts on the boundary itself. Making it a node means the boundary is
a single thing to look at and to name, while which formations sit on which side stays in ordinary
edges. No field on `Frontier` says who is on which side, because that would be a mechanic.

**`SignifierKind` defaults to `unspecified`, never `nodal`.** Whether a signifier is nodal,
floating or empty is an *interpretation*. The repository already made exactly this choice once:
`ProvenanceKind.UNKNOWN` is the default so a missing origin stays visibly unknown instead of
reading as fact. An unclassified signifier must stay visibly unclassified for the same reason.

## What is **not** imported from LaclauGPT — the load-bearing paragraph

The issue is explicit that the phase-1 paper *"informs interpretive categories, not a proven
generative political law"*, and that its extraction/interpretation must be distinguished from
hypothetical simulation transitions. [`POLITICAL_SIMULATOR_SCOPE.md`](POLITICAL_SIMULATOR_SCOPE.md)
lists the excluded runtime (collectors, classifiers, embeddings, databases, notebooks,
dashboards, DNA/SNA pipelines) and states plainly that there is **no coupling to LaclauGPT
repositories, services, schemas or infrastructure**. What follows is the same decision expressed
as *code*: the layer imports **vocabulary only**.

| Imported | Not imported |
| --- | --- |
| The names of the concepts: demand, articulation, equivalential chain, antagonistic frontier, nodal / floating / empty signifier, hegemonic formation | The corpus, any real political data, any sampling, scraping or feed |
| The idea that political identities are *constructed* rather than fixed demographic blocs | The extraction and interpretation pipeline, its NLP models, prompts or classifier output |
| The idea that communication is structured as networks (Castells) and that network-making, programming and switching are political operations | Any confidence value, score, threshold or probability produced by that pipeline |
| Provenance discipline: descriptive labels stay separate from generative claims | Any claim that these categories are a validated causal law, or that a classifier is a simulator |

Two consequences already encoded in the scaffold:

- **Absence of provenance stays unknown.** A political record defaults to `UNKNOWN` origin, never
  to `EVIDENCE`. A stored demand is not evidence until someone classifies it as such.
- **A description never becomes a transition.** Nothing in this layer maps a label to a state
  change. A future rule that does so must state its assumptions and receive its own approval,
  per [`INTEGRATION_BOUNDARIES.md`](INTEGRATION_BOUNDARIES.md).

## How a player would actually look at it

`board_view` already answers the map/network question: political records appear as typed nodes
alongside factions, and political relations appear as labelled edges in the same graph the whole
game uses, so a single board carries physical locations, faction networks and the political
field.

`political_view` is the Layer II panel: the four collections, the signifier kinds, each demand's
claimant, and the declared political relations. Both are display-only. Neither decides what a
record means, what a player may do with it, or what a link costs.

## Open questions this design deliberately leaves to the author (Gate B)

1. Is a `Frontier` best played as a node, or should the boundary itself be an edge between two
   formations? The node shape was chosen for legibility, not because the theory requires it.
2. Which relations should be *directed*? `NetworkEdge` is currently undirected in practice; the
   theory's articulation is asymmetric between signifier and demand.
3. Does a formation need a link to the leader and faction records in Layer I and Layer III, and
   if so, is that a stored reference or a view-time join?
4. Should the political field be recorded per-snapshot (as now) or accumulated as an append-only
   log, so that a frontier's *history* is visible? Provenance is already per-record, so either is
   reachable.
5. What makes a hegemonic shift legible to a player **without** pretending political change is a
   measured score? This is `RULE_SYSTEM_RESEARCH.md`'s question 3, and it is the one this layer
   most needs an answer to before any rule is written.

## Related

- [`POLITICAL_SIMULATOR_SCOPE.md`](POLITICAL_SIMULATOR_SCOPE.md) — the scope decision and the
  research-inspiration → player-abstraction table. **Authority for what this layer is.**
- [`RULE_SYSTEM_RESEARCH.md`](RULE_SYSTEM_RESEARCH.md) — Layer II options, comparative references
  and the four author-review gates.
- [`INTEGRATION_BOUNDARIES.md`](INTEGRATION_BOUNDARIES.md) — state/authority rules, the
  provenance discipline and the read-only view boundary.
- `../RULEBOOK.md` — the placeholder strategy rulebook; Layer II remains *no rules approved*.
- Issue [#152](https://github.com/TomiToivio/NooPunk/issues/152) — background RPG simulation, a
  distinct proposal, not this layer's runtime.
