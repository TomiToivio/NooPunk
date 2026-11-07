# Development fixtures for the detective adventure

`romppainen_development_case.json` is a **synthetic, noncanonical** test case created to prove the investigation loop works. It is **not** an excerpt from Tomi's `NooPunk-Story/Story/` and must never be silently promoted to official story canon.

The scene graph and clue graph are currently represented by simple JSON choice edges and evidence IDs. There is no need for a second Graph engine. See [the runner documentation](../../Code/ADVENTURE.md) and [the story adapter](../../Code/STORY_ADAPTER.md). Original author writing remains read-only.

`story_source_development.md` is a synthetic Markdown source for exercising the story adapter. It is not Tomi's prose and is not a case canon; the adapter copies scene text verbatim into a derivative JSON case with `canon: false`.
