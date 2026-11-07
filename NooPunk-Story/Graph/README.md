# Graph — the Story Graph adaptation

Agent-owned, human-audited. The graph is a **derivative** of [`../Story/`](../Story/): every node and edge cites
the manuscript passage it came from, and anything the manuscript does not say becomes a review note rather than
invented canon.

## Contents

| Path | What it is |
| --- | --- |
| `templates/BRANCHING_SCENE.md` | An empty scene template Tomi can copy into `Story/`. Prompts only, no prose. |
| `templates/NOVEL_CHAPTER.md` | The same for a conventional chapter. |
| `examples/` | Synthetic demonstrations of the conversion contract. **Never** manuscript content. |
| `REVIEW_NOTES.md` | Gaps, ambiguities and contradictions found while adapting, each with a source reference. |

## The contract

The machine-readable form is
[`data/schema/subproject_contracts_1295.json`](../../data/schema/subproject_contracts_1295.json), and the validator
is [`src/contracts/story_graph_contract.py`](../../src/contracts/story_graph_contract.py). A graph document must:

1. declare `schema: noopunk.story_graph/1`;
2. give every node a stable `id`, a `kind` from `series | episode | scene`, and a `source_ref` pointing into
   `Story/`;
3. declare `choices` as edges between scenes, with a `label` the player would recognise;
4. never contain a node whose `source_ref` does not resolve to an existing manuscript path — unless the node is
   explicitly marked `authored: true`, meaning Tomi approved it outside the current draft.

The last rule is the important one: an adaptation cannot quietly acquire a scene the author never wrote.

## What the RPG consumes

`NooPunk-RPG` reads the validated graph: scenes, choices, prerequisites and consequences. It does not read
`Story/` directly, and it never writes back.
