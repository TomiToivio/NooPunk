# Agent rules for NoöPunk Story

The root [`AGENTS.md`](../AGENTS.md) applies, including the #1295 hard rule. This file is the local
contract for story work, and it is narrower than the root one, not looser.

## `Story/` is read-only for agents

Do **not** create, write, rewrite, edit, reflow, reformat, rename, move, delete, translate, summarise into
place, or otherwise modify any file under `NooPunk-Story/Story/` — including as a side effect of a
refactor, a graph conversion, a bulk transformation, an editor's cleanup or a "helpful" correction. Do not
regenerate it from a graph, and do not write into it while testing.

Four things hold the line: the rule in `AGENTS.md`, `CODEOWNERS` on `/NooPunk-Story/Story/**`, the
structure test `tests/test_issue_1295_structure.py`, and the diff-level check
`tools/story_boundary.py` (`.github/workflows/story-boundary.yml`), which fails a pull request that
changes any path there. Do not add exceptions to the tool and do not rename the directory to escape it.

## What agents may do

* **Read** `Story/` freely: it is the input to the graph adaptation.
* **Write** `NooPunk-Story/Graph/`: Story Graph records derived from `Story/`, each citing the file and
  anchor it came from — see [`Graph/README.md`](Graph/README.md).
* **Write** `NooPunk-Story/templates/`: author-facing skeletons, kept blank on purpose.
* **Report** gaps, contradictions and ambiguity as review notes, never by inventing canon in prose or in
  a graph record.

## Proposing a change to the prose

Write a note — in the graph's review notes, or as a comment on the issue that asked for the work —
addressed to Tomi. He changes it, or he does not. A diff against `Story/` is never the proposal.

## Templates

`templates/SCENE_SCRIPT.md` and `templates/NOVEL_CHAPTER.md` are for Tomi to copy into `Story/` and write
in. Do not fill them in, do not "improve" them with example prose, and do not treat their prompts as
canon.
