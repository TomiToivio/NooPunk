# Etsivä Romppainen: first adventure vertical slice (#1310)

**Current product direction:** cyberpunk detective interactive fiction, **not** a full RPG. This is a minimal self-contained text adventure. No CWN, levels, tactical combat, psionics implementation, LaclauGPT pipeline or full social simulation is required.

## Run

From repository root:

```sh
python3 NooPunk-Simulator/Code/adventure.py
python3 -m unittest discover -s tests -p 'test_detective_adventure_1310.py' -v
```

Select a numbered option; `notebook` shows collected evidence and provisional hypotheses; `save /path/to/save.json` and `load /path/to/save.json` persist the session; `quit` exits. A finished case ends the loop, and the state keeps every choice and resulting ending.

## Tiny case contract

The runner consumes a JSON object with `id`, `title`, `start`, `clues`, `scenes`, and a `source` marker. Every scene contains `title`, `text` and `choices`; each choice has `label` and `to` plus optional `requires`, `adds` and `flags`. Terminal scenes use `ending: true`. The notebook renders collected clue IDs and tentative hypotheses. No essential evidence depends on a chance roll.

## Source and authorship

`../Graphs/fixtures/romppainen_development_case.json` is a **noncanonical, agent-authored synthetic development fixture**, not Tomi's story. The current author-written `../../NooPunk-Story/Story/` contains notes but no imported executable case script. **Do not generate scenes or alter that protected directory.** When Tomi writes a case script, [`story_adapter.py`](story_adapter.py) converts the documented Markdown format into equivalent scene JSON, preserving the source path, hash and author attribution; see [`STORY_ADAPTER.md`](STORY_ADAPTER.md). Treat adapted scene JSON as derivative data, never as a replacement manuscript. The game never writes into `Paper/` or `Story/`.

This is one deterministic finite case with alternate investigation orders, important clues always obtainable, and three provisional outcomes. Political and hacking mini-simulations are deliberately not implemented; add them only as independent optional investigative modules after the primary case works.

## Architecture and boundaries

`Code/adventure.py` handles case navigation and saves. The existing social science implementation in `src/social_sim/` is unchanged and stays an optional provider of world state, not the adventure engine. Keep the future UI separate from case state, and never require `NooPunk-RPG/` or a CWN game loop. The source JSON's `source` metadata distinguishes the synthetic fixture from Tomi-authored story and empirical evidence.

## Test scope

`tests/test_detective_adventure_1310.py` checks three endings, alternate investigative order, gate accessibility, state round trip, incorrect saves, malformed scene references and independence from RPG imports. Further author-content conversion and integration are separate work.

## Case audit: the softlock check (#1310)

`python3 NooPunk-Simulator/Code/case_audit.py --check [--case PATH]`

A detective case fails quietly. Nobody dies and the game does not crash: the player simply reaches an ending
without the evidence that makes the ending honest, because one route skipped a clue.

The audit walks the case as a graph and reports:

| Error | Meaning |
| --- | --- |
| `ending-without-essential-evidence` | a route reaches an ending while never picking up a clue listed in `essential_clues` |
| `unobtainable-clue` | a clue is declared but no scene or choice ever adds it |
| `dangling-choice` | a choice points at a scene that does not exist |
| `unknown-requirement` / `unknown-clue` | a gate or an `adds` entry names a clue that is not declared |
| `no-ending` / `unreachable-ending` | the case cannot be finished, or an ending has no way in |
| `bad-contradiction` / `bad-deduction` | a notebook entry names a clue that does not exist |

Warnings do not fail a case unless `--check` sees an error: an unreachable optional scene, a single ending, or a
case with no `essential_clues` at all (which means the audit cannot tell what must survive — say so explicitly
rather than letting it pass silently).

The path question is answered **route by route**, not by the union of clues available in a scene: a union would
let a shortcut pass, which is the failure the audit exists to catch.

### Case fields added for the notebook

```jsonc
"essential_clues": ["missing", "witness"],
"deductions": [{"requires": ["missing", "roster"], "text": "What the evidence supports, stated as inference."}],
"contradictions": [{"between": ["witness", "message"], "text": "Two accounts that cannot both be complete."}]
```

The notebook prints deductions only when their clues are held, and shows contradictions as **disagreement**,
never as proof. The development fixture is still synthetic: these fields are the shape a case needs, not a
claim about the case.
