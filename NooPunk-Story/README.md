> **Current gameplay direction (#1310, 2026-11-07):** `NooPunk-Story/` holds Tomi's interactive detective-fiction script starring Etsivä Romppainen, potentially later a novel. The playable adventure lives in `NooPunk-Simulator/`. **All agent access to `Story/` remains read-only**; agent derivatives belong in `Graph/`. No full RPG is required. Preserve the manuscript unchanged.

# NoöPunk Story

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
