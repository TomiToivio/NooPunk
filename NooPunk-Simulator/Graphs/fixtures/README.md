The scene graph and clue graph are currently represented by simple JSON choice edges and evidence IDs. There is no need for a second Graph engine. See [the runner documentation](../../Code/ADVENTURE.md) and [the story adapter](../../Code/STORY_ADAPTER.md). Original author writing remains read-only.

`story_source_development.md` is a synthetic Markdown source for exercising the story adapter. It is not Tomi's prose and is not a case canon; the adapter copies scene text verbatim into a derivative JSON case with `canon: false`.

## Simulator graph fixtures (#1309)

| file | what it is |
|---|---|
| `social_graph_1309.json` | six actors with mutual and one-sided ties on the author's −4…+4 scale |
| `ideology_graph_1309.json` | coded actor–concept–position statements, each naming its statement id |
| `physical_graph_1309.json` | five Helsinki places, three routes, no coordinates |

They load together through `social_sim.graphs.load_world()`; the rules are in
[`../../Rulebook/GRAPHS_1309.md`](../../Rulebook/GRAPHS_1309.md) and the overview in [`../GRAPHS_OVERVIEW.md`](../GRAPHS_OVERVIEW.md).
All three are labelled synthetic: they are fixtures, not Helsinki data.
