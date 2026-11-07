# Story-to-case adapter (#1310, P3 infrastructure)

**Purpose:** convert an author-written Markdown case script into the small adventure case JSON consumed by
[`adventure.py`](adventure.py). It is a **thin, read-only adapter**: it never writes into
`NooPunk-Story/Story/`, never invents missing scenes, and never marks a case as canon.

The current author script does not yet contain an executable Romppainen case. This adapter and its fixture
are infrastructure for when one exists. The fixture is a **noncanonical development example**, not Tomi's
prose.

## Command

```sh
python3 NooPunk-Simulator/Code/story_adapter.py \
  --story path/to/case.md \
  --out /tmp/romppainen_case.json
python3 NooPunk-Simulator/Code/adventure.py --case /tmp/romppainen_case.json
```

## Author format

The format is deliberately small and readable. Scene text is copied verbatim; only the container syntax
is interpreted.

```markdown
# Case: <case title>

id: <stable-case-id>
start: <scene-id>
author: <author name>
author_reviewed: false

## Scene briefing | Briefing title

Narrative text. A blank line separates paragraphs.

- [Choice label](records) adds=clue.one,clue.two
- [Another choice](witness) adds=clue.one; requires=clue.two

## Scene records | Records desk

More narrative text.

- [Go back](briefing)

## Scene ending_private | Private ending | ending

The terminal scene text.

## Clues

- clue.one: What the clue establishes, with its source.
- clue.two: Another clue.

## Hypotheses

- A tentative explanation. | requires=clue.one,clue.two

## Contradictions

- clue.one + clue.two: What the two records cannot both be right about, and what that implies.
```

### Rules

- First line must be `# Case: <title>`.
- Metadata lines before the first `##` are `key: value`; `id` and `start` are required.
- `## Scene <id> | <title>` starts a scene. Add `| ending` for a terminal scene.
- Scene prose is every non-choice line until the next `##` section, preserved as written.
- Choices use `- [label](target)`. Optional attributes:
  - `adds=id,id` — clues recorded when the choice is taken;
  - `requires=id,id` — clues required for the choice to be visible.
  Attributes may be separated by `;`.
- `## Clues` maps `id: description`.
- `## Hypotheses` uses `- text | requires=id,id`; the requirement is optional.
- `## Contradictions` uses `- clue.a + clue.b: what conflicts`. Both clues must exist; a
  contradiction is a recorded conflict in the evidence, never a verdict, and never a substitute for
  one. The runner surfaces it in the notebook only once the detective holds both clues. The section is
  optional: a script without it parses exactly as before.
- Every choice target and clue id must exist. A malformed file is rejected, not repaired.

## Provenance

The generated case stores:

```json
"source": {
  "kind": "author_story",
  "author": "...",
  "story_manuscript": "...",
  "source_sha256": "...",
  "author_reviewed": false,
  "canon": false,
  "issue": 1310,
  "adapter_note": "..."
}
```

`canon` is always `false` from this adapter. Only the author can approve a case as canon. The source file
is read-only and is never rewritten.

## Boundary

- No RPG import, no CWN mechanics, no LLM.
- No scene or prose generation.
- No modification of `NooPunk-Story/Story/` or `NooPunk-Simulator/Paper/`.
- The fixture at `../Graphs/fixtures/story_source_development.md` is explicitly a development example.
