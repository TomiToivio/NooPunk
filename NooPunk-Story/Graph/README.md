# Graph — the agent-maintained adaptation

A derivative of `../Story/`, in the existing Story Graph model: **Series → Episodes → Scenes**, with
choices, prerequisites, consequences and references back to the manuscript.

## Rules

1. **Every graph record cites its source.** A scene without a `source` reference (file and heading, or
   line range) is not accepted.
2. **Ambiguity becomes a review note, not a decision.** If the manuscript does not say whether Tony
   takes the tram, the graph records the question in `reviews/` and leaves the branch open.
3. **The graph never edits the manuscript.** Conversion is one-way.
4. **The contract is shared.** Node and edge shapes come from
   [`docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md`](../../docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md);
   changing them needs a cross-project review.

## Status

P0 skeleton. The templates live in [`docs/graphs/templates/`](../../docs/graphs/templates/) until P2,
which adds the first converted scene and the validation procedure.
