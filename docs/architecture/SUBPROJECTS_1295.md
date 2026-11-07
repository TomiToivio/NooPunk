# Three subprojects: the contract between them (#1295)

> **Status: structure and contracts only.** Nothing has been moved yet. This page says what each subproject
> owns, what crosses the boundary, and in which direction — so that the migration can happen in small PRs
> without a week of broken imports.

## The shape

```
NooPunk-Story/
  Story/     Tomi's manuscript          ← human only, read-only to agents
  Graph/     the adaptation             → agent-owned derivative
NooPunk-Simulator/   social-science simulation     (code today: src/social_sim)
NooPunk-RPG/         CWN + NoöPunk overlays        (code today: src/rules, src/world, rulebook)
```

Each directory has a `README.md` that says what it owns and what it refuses to own. The Story subproject also
carries `Story/POLICY.md`, because the manuscript rule is the one rule that cannot be softened.

## What crosses, and which way

| Direction | Payload | Rule |
| --- | --- | --- |
| Story → Graph | passages, scenes, choices | the graph cites `source_ref`; a node with no resolvable source must be `authored: true` |
| Graph → RPG | scenes, choices, prerequisites, consequences | the RPG consumes; it never writes back |
| Simulator → RPG | social-world state as a tag graph | via the shared contract, not a private format |
| RPG ↛ anything | — | the RPG is a consumer, not a source of truth |

The arrows are the whole design. An adaptation that feeds back into the manuscript destroys the only copy of
the author's voice; an RPG that authors scenes makes the graph decorative.

## The two schemas

Both live in [`data/schema/subproject_contracts_1295.json`](../../data/schema/subproject_contracts_1295.json).

**`noopunk.story_graph/1`** — `series → episode → scene`, with `choice` and `transition` edges. Required on
every node: `id`, `kind`, `label`, `source_ref`. A `choice` edge needs a label a player would recognise.
Scene types are the six the engine already knows: Investigation, Exploration, Action, Social, Cyber, Astral.

**`noopunk.tag_graph/1`** — actors, factions, institutions, places, devices, discourses and events, joined by
relation, membership, reference, influence and ownership edges. This is what the Simulator emits and the RPG
reads.

The contract is deliberately small. A consumer that needs more bumps the version rather than inventing a
private format; that is the only way three projects can be developed separately and still be integrable.

## Enforcement

| Check | What it proves |
| --- | --- |
| `tools/check_story_boundary.py --check` | subprojects exist with READMEs; `Story/` holds manuscript text and its policy, and no generated-artefact marker |
| `tools/check_story_boundary.py --changed` | fails when `Story/` changed without `NOOPUNK_STORY_HUMAN_AUTHOR=1` — the agent's default path is refusal |
| `tests/test_subprojects_1295.py` | the contract refuses an unsourced scene, a duplicate id, an unlabelled choice and an unknown scene type; the RPG adapter builds the RPG's own `StoryGraph` and refuses an invalid hierarchy |

The boundary check is a tripwire, not a proof of authorship: no repository check can tell who typed a
sentence. It makes the honest path the easy one and the dishonest path deliberate.

## Migration

See [`MIGRATION_MAP_1295.md`](MIGRATION_MAP_1295.md). Nothing moves in the PR that introduces this page: the
point of the structure is to make the move cheap later, not to perform it under pressure.

## Why not one folder per concern, immediately

Because the RPG and the simulator are both live. Moving `src/rules` or `src/social_sim` in a single commit
breaks imports, tests, CLI, Evennia and the CWN parity tools at once, and the fix would consume exactly the
creative attention this issue exists to free. The staged map is the compromise: directories and contracts now,
code later, compatibility wrappers during.
