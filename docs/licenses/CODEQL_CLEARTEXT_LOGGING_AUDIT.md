# Code scanning alert #4 — `py/clear-text-logging-sensitive-data` in `strategy_game/__main__.py`

**Status:** resolved by dismissal on grounded grounds, with the grounds turned into executable
guards. **No rule, canon or mechanic was changed.**

## The finding

| field | value |
| --- | --- |
| alert | [#4](https://github.com/TomiToivio/NooPunk/security/code-scanning/4) |
| rule | `py/clear-text-logging-sensitive-data` (CWE-312 / CWE-359 / CWE-532), security severity `high` |
| sink | `strategy_game/__main__.py:12` — `print(json.dumps(board_view(WorldState()), …))` |
| classification reported | `private` |

## Why the rule fires: it matches a **field name**, not a value

CodeQL's shared `maybePrivate()` heuristic
([`SensitiveDataHeuristics.qll`](https://raw.githubusercontent.com/github/codeql/main/shared/concepts/codeql/concepts/internal/SensitiveDataHeuristics.qll))
lists, among its patterns for personal-location data:

```
"latitude|longitude|nationality|" + …
```

The crossover's board record carries those two names as fields:

```python
# strategy_game/core.py
@dataclass
class Location:
    identifier: str
    label: str
    latitude: float | None = None
    longitude: float | None = None
```

So **every** `print()` downstream of a `Location` is a taint sink for this rule, whatever the
coordinates hold. The rule fires on a *shape*; it does not know that the values are a fictional
board's geography rather than a person's location. The `private` bucket in the alert text is the
analyzer's generic label, not an assertion that personal data is present.

## The four facts that decide the alert, and how each is checked

The same rule raised three sibling alerts (#1, #2, #3). A sibling's dismissal does **not** bind
this one, so each fact below is re-derived and independently checked. The executable guards live in
[`strategy_game/tests/test_cli_output_safety.py`](../../strategy_game/tests/test_cli_output_safety.py).

### 1. There is no log-file surface — the package never writes the board to disk

`strategy_game` imports no logging framework and configures no file handler anywhere; the two
flagged modules contain no `open(…)` for writing and no `Path.write_text`. The only sinks are
`print()` to the caller's own stdout, which is what a view is for.

A board payload inside a **log file** would be a genuine CWE-312 finding. The same payload on the
terminal that asked for it is not. That distinction is the whole answer to the rule.

*Guards:* `test_no_module_imports_the_logging_framework`,
`test_the_two_flagged_modules_write_no_file`, `test_neither_cli_writes_a_file`.

The package *does* write files elsewhere — `save_campaign`, the casework and investigation
`save` methods, `save_table`, the playtest's `--json` output. All of them take an explicit path
**from the caller** and are the save features the tools are built around; a user asking the game to
save its state is not this finding. The guard is therefore scoped to the flagged modules, where
no caller-chosen path exists.

### 2. The scaffold CLI's output is a constant — 118 bytes, no coordinate value

`python -m strategy_game` takes **no argument**, reads **no environment variable** and opens **no
file**. Its output is therefore fixed, and it contains no coordinate at all:

```json
{
  "schema_version": "scaffold-1",
  "locations": [],
  "network_nodes": [],
  "network_edges": [],
  "assets": []
}
```

All four collections are empty. The board is the *empty scaffold*.

*Guards:* `test_the_payload_carries_no_coordinate_value`,
`test_the_output_is_a_constant_across_runs_and_working_directories`,
`test_the_cli_reads_no_argument_environment_or_file`,
`test_the_entrypoint_source_declares_no_input_path`.

The last of these is the strongest form: it asserts on the **source** of the entrypoint, so it
fails if the module ever grows an `argparse` import, an `os` import, an `environ`/`argv` read or a
file read. A behavioural probe can only show that the paths it tried did not work; this shows that
no such path exists.

### 3. Alert #4 is the same sink as the already-dismissed alert #1

Alert #1 was raised against the same `print` at line 7, when the module still printed at import
time. Commit `76fe468` ("make empty-state CLI import-safe") moved the statement into `main()`, so
the sink moved to line 12 and the analyzer re-raised it as a new alert. It is the same expression,
the same data, the same emptiness — a new finding number for an unchanged fact. That is why #1's
dismissal and this one agree.

*Evidence:* `git show 5341b5c:strategy_game/__main__.py` (line 7, module-level print) versus
`git show 76fe468:strategy_game/__main__.py` (line 12, inside `main()`).

### 4. The render CLI is a *different* case and is **not** dismissed on this reasoning

`strategy_game/render/__main__.py` (alerts #2 and #3) has a `--world <file>` flag that loads a
real JSON world and prints it. Its output is **not** constant, so the "provably constant"
premise does **not** hold there, and a copy of this dismissal would be a false record. What holds
for the render path is fact 1 alone: the board goes to the terminal that asked for a rendering, and
nowhere else. The render CLI exists to draw a board; the coordinates *are* the board.

*Guard:* `test_a_loaded_world_reaches_stdout_and_writes_no_file` — a loaded world with a
coordinate reaches stdout, and the run writes no file.

## Why the guards are not vacuous

A scanner that finds nothing is indistinguishable from a broken scanner, so every guard class was
proven capable of failing by mutating the code and re-running (the pre-fix file was backed up and
restored, not stashed):

| mutation | guard that fired |
| --- | --- |
| scaffold CLI reads a world file from `NOOPUNK_WORLD` | `test_the_cli_reads_no_argument_environment_or_file` **and** `test_the_entrypoint_source_declares_no_input_path` |
| render module imports `logging` and logs the world state | `test_no_module_imports_the_logging_framework` |
| render module writes the board to an absolute path | `test_the_two_flagged_modules_write_no_file` |

All three mutations were reverted; the suite is green on the restored tree.

## What is **not** claimed

- No rule, canon, mechanic, skill or balance number was changed.
- No file was rewritten to change the analyzer's view: the code is byte-identical to `main`.
- The `latitude`/`longitude` **field names are kept.** Renaming them would silence the analyzer
  while changing the board's public shape — and `strategy_game/tests/test_view_model_and_ports.py`
  pins that shape. A suppression comment would hide a *shape* rather than a fact, and under this
  repository's default CodeQL setup (no `.github/codeql/codeql-config.yml`) a path-scoped
  exclusion is not available, while a repo-wide `query-filters` exclusion would blind the
  repository to future genuine instances.
- The guard does not assert that coordinates are *absent* from the render CLI's output. They are
  present, on purpose. The guard is that they reach stdout and nowhere else.

## The dismissal record

Dismissed as a **false positive**, with the grounds above, on alert #4 and its two siblings. The
comment on each alert states the specific facts for *that* alert rather than one boilerplate
paragraph, and every dismissal is revertible with `state=open`.
