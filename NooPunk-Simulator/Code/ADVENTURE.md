# Etsivä Romppainen: first adventure vertical slice (#1310)

**Current product direction:** cyberpunk detective interactive fiction, **not** a full RPG. This is a minimal self-contained text adventure. No CWN, levels, tactical combat, psionics implementation, LaclauGPT pipeline or full social simulation is required.

## Run

From repository root:

```sh
python3 NooPunk-Simulator/Code/adventure.py
python3 -m unittest discover -s tests -p 'test_detective_adventure_1310.py' -v
```

Select a numbered option; `notebook` shows collected evidence, conflicting records, open leads and the
hypotheses you could hold; `consider ID` / `dismiss ID` record or set aside one of them; `save
/path/to/save.json` and `load /path/to/save.json` persist the session; `quit` exits. A finished case ends
the loop, and the state keeps every choice, every hypothesis you held and the resulting ending.

Check that a case cannot strand the player before shipping it:

```sh
python3 NooPunk-Simulator/Code/case_audit.py                     # the shipped development case
python3 NooPunk-Simulator/Code/case_audit.py --case my_case.json  # 0 sound, 1 findings, 2 unreadable
```

## Tiny case contract

The runner consumes a JSON object with `id`, `title`, `start`, `clues`, `scenes`, and a `source` marker. Every scene contains `title`, `text` and `choices`; each choice has `label` and `to` plus optional `requires`, `adds` and `flags`. Terminal scenes use `ending: true`. The notebook renders collected clues, contradictions whose two clues are both held, open leads (scenes you know about and have not visited), the hypotheses the evidence now makes available, the ones you recorded or set aside, and the disposition the ending chose. Hypotheses are the detective's reasoning, never a fact of the case, and the save stores them as such. No essential evidence depends on a chance roll.

## Source and authorship

`../Graphs/fixtures/romppainen_development_case.json` is a **noncanonical, agent-authored synthetic development fixture**, not Tomi's story. The current author-written `../../NooPunk-Story/Story/` contains notes but no imported executable case script. **Do not generate scenes or alter that protected directory.** When Tomi writes a case script, [`story_adapter.py`](story_adapter.py) converts the documented Markdown format into equivalent scene JSON, preserving the source path, hash and author attribution; see [`STORY_ADAPTER.md`](STORY_ADAPTER.md). Treat adapted scene JSON as derivative data, never as a replacement manuscript. The game never writes into `Paper/` or `Story/`.

This is one deterministic finite case with alternate investigation orders, important clues always obtainable, and three provisional outcomes. Political and hacking mini-simulations are deliberately not implemented; add them only as independent optional investigative modules after the primary case works.

## Architecture and boundaries

`Code/adventure.py` handles case navigation and saves. The existing social science implementation in `src/social_sim/` is unchanged and stays an optional provider of world state, not the adventure engine. Keep the future UI separate from case state, and never require `NooPunk-RPG/` or a CWN game loop. The source JSON's `source` metadata distinguishes the synthetic fixture from Tomi-authored story and empirical evidence.

## Test scope

`tests/test_detective_adventure_1310.py` checks three endings, alternate investigative order, gate accessibility, state round trip, incorrect saves, malformed scene references, the reasoning layer (evidence-gated hypotheses, contradictions, leads, save compatibility) and independence from RPG imports. `tests/test_case_audit_1310.py` proves the audit passes on the shipped case and names each defect on a case broken one way at a time: an unsatisfiable gate, an unreachable ending, an unobtainable clue, a dead-end scene, a missing ending, a hypothesis or contradiction resting on impossible evidence. Further author-content conversion and integration are separate work.

## Essential evidence: the one softlock a union check cannot see (#1310)

The audit's fixed point answers *"can this be reached at all"*. It does not answer *"can this be skipped"* — and
those are different questions:

* a case where **some** route collects the evidence and **another** route reaches the ending without it looks
  sound to a union check, and strands the player in a story they cannot honestly close.

So a case may declare what its endings depend on:

```jsonc
"essential_clues": ["missing", "witness"]
```

`case_audit.py` then walks every route to every ending and reports
`ending 'X' can be reached without essential clue 'Y'` when a shortcut exists. The listing is **optional**: a case
that declares nothing is not accused of anything, because the audit must not invent promises the author did not
make.

The check is per route, not per scene, and the test suite carries the smallest case that proves the difference: two
choices to one ending, the second skipping the evidence. Ungated, it must fail. Gated behind `requires: ["evidence"]`,
it must pass.
