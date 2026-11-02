# The agent adapter (#1084): a model may propose, only the rules may decide

Milestone B asks for a **Concordia** adapter: an LLM actor or GM that plays the same UNSA case through
the same session interface, without becoming a rules engine and without being required. This is the
first half of that — the gate every agent proposal has to pass — and it is deliberately model-agnostic.

`src/console/agent.py` + `tests/test_agent_adapter_1084.py` (15 cases).

## The contract

| the adapter may | the adapter may not |
| --- | --- |
| read an `observation()` and render it to a model | add a field the session does not hold |
| validate a proposed command against the console's verb list and arity | decide whether the command succeeds |
| call `run_command`, which calls the same `CaseSession` a human uses | compute a check, damage, a clue or a movement |
| report the **engine's** before/after diff | narrate a state change that did not happen |
| persist, schedule, stop the loop | hold a rule the plain package does not also expose |

The rule is the ADR's (#1054 §4), applied where it is most likely to break: in front of a language
model. A model's most natural failure is not a wrong roll, it is a confident sentence about a clue it
never found.

## What the tests actually pin

* **`test_a_fabricated_clue_cannot_be_taken`** — `take access_log` before the terminal is searched is
  refused, `changed` is empty, and the clue does not enter the session.
* **`test_a_claimed_result_is_not_a_result`** — "I rolled a 12 and found the badge" is not a verb; the
  discovery map is byte-identical before and after.
* **`test_the_adapter_reports_the_engines_diff_not_its_own`** — stating a theory changes exactly
  `events`, `theory` and `turns`, because that is what the session changed.
* **`test_the_dice_for_a_risk_come_from_the_engine_and_replay`** — two gates with seed 7 produce
  identical output and identical state; the adapter contributes no randomness.
* **`test_the_loop_is_bounded`** — `run()` stops at `max_turns`, so a model with no stopping condition
  cannot spin forever.
* **`test_the_observation_is_the_players_knowledge_only`** — no `solution`, `answer` or
  `correct_hypothesis` field exists, because there is no such field on the session to leak.

## Plugging Concordia in

Concordia supplies a callable; this module supplies everything else:

```python
from console.agent import load_gate

gate = load_gate("data/scenarios/lakkahaltia/case_graph.json", seed=7)

def proposer(observation: dict) -> str:
    # a Concordia agent / any LLM reads `observation` and returns one command line
    ...

for record in gate.run(proposer, max_turns=12):
    print(record["accepted"], record["proposal"], record["reason"] or record["changed"])
```

Two notes for whoever wires the real runtime:

1. **Concordia is an optional dependency.** `requirements.txt` pins it for the narrative runtime, but
   nothing in `src/` imports it, and `tools/check_engine_boundary.py` keeps it that way. The adapter
   takes text, not an agent object, so the library keeps working with no model installed.
2. **The GM role is the interesting one.** A model may propose a *player* action today; proposing
   *scene content* (a new NPC line, a complication) is authoring, and `docs/design/ISSUE_1037_*`
   records why that is the author's, not an agent's. The gate's `author` field exists so a later,
   authorised GM adapter can be distinguished in the transcript.

## Still open on #1084

- Pygame or Arcade front end over the identical session API (the browser, NiceGUI and Textual adapters
  already exist and call the same session).
- The Tarot mod: card data and a physical procedure first, code second.
- A cross-adapter parity test per new adapter, replaying one seeded case and comparing state documents
  — the pattern `mud/tests/test_session_adapter_1053.py` established.

None of these changes a rule; all of them are adapters.
