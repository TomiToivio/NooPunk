# The console case slice (#1053, #1054)

A complete NoöPunk investigation is playable in a plain terminal, offline, with no GM and no LLM:

```bash
pip install -e .                       # optional: also gives you `noopunk-case`
python scripts/noopunk_case.py         # interactive
python scripts/noopunk_case.py --script docs/examples/lakkahaltia_walkthrough.txt --seed 7
python scripts/noopunk_case.py --load case-save.json
```

The case is the one already in the repository — `data/scenarios/lakkahaltia/case_graph.json`,
*Etsivä Romppainen ja Lakkahaltian Salaisuus* (#704): four scenes, twelve clues, four hypotheses, one
of them anomalous and one mundane, as `CaseGraph.validate()` requires.

## What this adapter is, and is not

| it is | it is not |
| --- | --- |
| the **reference adapter**: the smallest presentation that plays the case through `src/rules/investigation.py` | a rules implementation — it imports `discover`, `Clue`, `Hypothesis`, `Investigator`, `load_case_graph` |
| a **session** with versioned, engine-neutral state you can save and resume | a campaign engine with quests, NPC AI or multiplayer |
| a **deterministic** replay harness (`--seed` + a command file reproduces a run exactly) | a randomiser you cannot audit |

The rules decide what a competent investigator sees. The session records what the player did. The player
holds the theory — `conclude` records the answer and the evidence attached to it and prints
`the console does not decide the truth of the theory`. Nothing in `src/console/` compares a theory to a
solution, because there is no solution field to compare against.

## Commands

```
look                     look around; declare a search for anything that needs one
go <scene>               move through a discovered lead
clues                    what you have found so far
take <clue>              examine a clue you were not handed on entry
support|contradict|neutral <clue>   record how you read a clue against your theory
theory <hypothesis>      state which hypothesis you are working on
hypotheses               list the hypotheses this case allows
risk <difficulty> [skill]  a CWN 2d6 check under pressure (8, 10 or 12)
status                   scene, theory, evidence counts, turns, seed
conclude <hypothesis> [note]   record your answer; the case ends
save [path] | load <path>      portable JSON state
help | quit
```

## Playing the same thing at a table (parity by construction)

The console is not a separate game. To run this case with paper:

1. Print the case graph (`data/scenarios/lakkahaltia/case_graph.json`) or the case text
   (`data/scenarios/lakkahaltia/case.json`).
2. Read the scene's clues aloud to a player whose sheet lists that clue's **competency**. Rank 0 counts —
   in the Without Number baseline untrained is the *absence* of rank, so `Notice 0` reads the log.
   No roll: finding information is not a roll.
3. When a player wants to act under pressure (`risk`), roll 2d6 + the skill rank against the difficulty
   the referee names (8 routine, 10 hard, 12 brutal). The die decides danger, time and quality — never
   whether a clue exists.
4. Each player keeps a theory and marks clues as *supports / contradicts / neutral*. That is their reading,
   not the system's.
5. The case ends when the table states its answer. Write it down; the mystery is the table's.

`docs/examples/lakkahaltia_walkthrough.txt` is exactly that sequence in command form — the same file the
test suite replays, so the printed walkthrough and the tested behaviour cannot drift apart silently.

## Save format

One JSON object, `state_version: 1`:

```json
{
  "state_version": 1, "case_id": "lakkahaltia",
  "investigator": {"name": "…", "ratings": {"Notice": 1}},
  "scene": "patient_room", "seed": 7, "visited": ["entrance"],
  "discovered": {"sign-in-sheet": "entrance"},
  "evidence": {"deliberate_falsification": {"duty-roster": "supports"}},
  "theory": "deliberate_falsification", "turns": 17,
  "concluded": false, "conclusion": {}, "events": [],
  "rng_state": [3, [2147483648, …], null]
}
```

`rng_state` is `random.Random.getstate()`: it is what makes a resumed session roll the *same* dice as an
uninterrupted one (tested). An unknown `state_version`, a missing key, or a save belonging to another
`case_id` is refused with a message — never loaded as a half-valid game.

## Determinism

```bash
python scripts/noopunk_case.py --seed 7 --script docs/examples/lakkahaltia_walkthrough.txt --save a.json
python scripts/noopunk_case.py --seed 7 --script docs/examples/lakkahaltia_walkthrough.txt --save b.json
diff a.json b.json     # identical
```

`--seed 8` moves the dice but not the clues: discovery is not stochastic, and the tests assert exactly
that (`test_a_different_seed_moves_the_dice_but_not_the_clues`).

## What is not here yet

* an Evennia adapter over this session (the MUD still plays its own loop);
* `noopunk.*` import names (the package is installed as `rules`, `console`, `text_game`, …);
* NPC behaviour beyond what the case data states, and side quests — the graph is one case;
* the rulebook-side walkthrough table (§6 of #1054) generated from these examples.

See `docs/design/ARCHITECTURE_AUDIT_1053.md` for the survey these gaps come from and the order in which
they are worth closing.
