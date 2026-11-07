> **Current gameplay direction (#1310, 2026-11-07):** `NooPunk-Story/` holds Tomi's interactive detective-fiction script starring Etsivä Romppainen, potentially later a novel. The playable adventure lives in `NooPunk-Simulator/`. **All agent access to `Story/` remains read-only**; agent derivatives belong in `Graph/`. No full RPG is required. Preserve the manuscript unchanged.

# NoöPunk Story

> **`Story/` is Tomi-authored and agent READ-ONLY (#1310).** Agents may build graphs, indexes and adapters
> **from actual author-written text**. Do not fabricate manuscript prose, dialogue or scene text in this
> directory. Where the script does not exist yet, use clearly labelled development fixtures — never
> pseudo-canon. See [../docs/architecture/PIVOT_1310_DETECTIVE_IF.md](../docs/architecture/PIVOT_1310_DETECTIVE_IF.md).

The creative track: **Tomi's manuscript**, and the Story Graph derived from it.

```
Story/   Tomi's original branching script, dialogue and novel chapters. AGENTS READ ONLY.
Graph/   Agent-maintained derivative: series, episodes, scenes, choices, branches, references.
```

**Direction of truth:** `Story/` → `Graph/`. The graph is an adaptation of the manuscript, never a
source that rewrites it. Where the graph needs something the manuscript does not say, that is a
**review note**, not an invention.

- Authorship policy: [`AGENTS.md`](../AGENTS.md) — hard rule, no exceptions.
- Migration map: [`docs/architecture/PIVOT_1295_MIGRATION_MAP.md`](../docs/architecture/PIVOT_1295_MIGRATION_MAP.md)
- Graph templates: [`docs/graphs/templates/`](../docs/graphs/templates/) (until P2 moves them here)
## What this track is for now (#1310, 2026-11-07)

`Story/` is the **interactive-fiction script the adventure plays** — scenes, dialogue, clues, choices, branches and case
arcs — and may later become a conventional novel. `Graph/` stays the agent-maintained derivative, and the direction of
truth is unchanged: **`Story/` → `Graph/`**, never the reverse.

Agents do not write manuscript prose into `Story/`, do not restructure it, and do not treat a missing scene as an
invitation to invent canon. If the script does not yet contain what a scene needs, that is a note for Tomi or a clearly
labelled development fixture.
