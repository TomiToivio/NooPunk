# Development fixtures for the detective adventure

`romppainen_development_case.json` is a **synthetic, noncanonical** test case created to prove the investigation loop works. It is **not** an excerpt from Tomi's `NooPunk-Story/Story/` and must never be silently promoted to official story canon.

The scene graph and clue graph are currently represented by simple JSON choice edges and evidence IDs. There is no need for a second Graph engine. See [the runner documentation](../../Code/ADVENTURE.md). Original author writing remains read-only.
## Simulator graph fixtures (#1309)

| file | what it is |
|---|---|
| `social_graph_1309.json` | six actors with mutual and one-sided ties on the author's −4…+4 scale |
| `ideology_graph_1309.json` | coded actor–concept–position statements, each naming its statement id |
| `physical_graph_1309.json` | five Helsinki places, three routes, no coordinates |

They load together through `social_sim.graphs.load_world()`; the rules are in
[`../../Rulebook/GRAPHS_1309.md`](../../Rulebook/GRAPHS_1309.md) and the overview in [`../GRAPHS_OVERVIEW.md`](../GRAPHS_OVERVIEW.md).
All three are labelled synthetic: they are fixtures, not Helsinki data.
