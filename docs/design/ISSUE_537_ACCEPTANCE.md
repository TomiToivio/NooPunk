# #537 — Acceptance record: the CodeQL coordinate taint, and what PR #536 actually fixed

**What this record is.** A criterion-by-criterion check of issue #537 against the merged tree.
Issue #537 is a **write-up** issue: it does not ask for a mechanic, a rule or a number, it asks
for an account of the `py/clear-text-logging-sensitive-data` findings and of the defect that
surfaced while they were being investigated. This record therefore checks that **every claim in
the issue is true of `main`**, and it states plainly the two claims that have since become stale
because a later fix landed underneath the issue.

**What closure does and does not mean.** Closing #537 means the account is **accurate** and the
alerts it discusses are **resolved**. It does **not** mean any rule was approved, any board
mechanic changed, or that the coordinate taint can never be real again — the standing note at
the end is the part that matters for the future.

## The state of the five alerts

| alert | state | how it was resolved |
| --- | --- | --- |
| #1 | dismissed (false positive) | the owner's original dismissal, on the structural-taint grounds |
| #2 | **fixed** | PR #536 |
| #3 | **fixed** | PR #536 |
| #4 | dismissed (false positive) | the grounds in the issue, re-derived and made executable |
| #5 | dismissed (false positive) | the grounds in the issue |

**No code-scanning alert on this rule is open.** The dismissal of #4 and #5 is backed by
executable guards rather than by a comment, and the guards are in
`strategy_game/tests/test_cli_output_safety.py` (8 tests, PR #538).

## The issue's claims, each checked against `main`

| # | The issue's claim | Where it is answered | Status |
| --- | --- | --- | --- |
| 1 | The remaining open alerts were the **same structural taint** the owner dismissed for #1: the `latitude`/`longitude` of a **declared world location**, which CodeQL's taxonomy classes as location data | `strategy_game/view.py:43-44` — the projection reads the board's position fields | met, but **the field names changed**: see the reconciliation below |
| 2 | They are **not personal data**: no person, no address, no private place | `data/ukweli_local.json` — the 8 locations of the fictional *Republic of Ukweli* carry `id`, `label`, `pressure`, `tags`, `island` and **no position field at all**; `0 of 8` carry one | met |
| 3 | The projection is **contract-pinned**, so removing the fields would break a declared contract | `strategy_game/docs/INTERFACE_SPIKE.md` rule 6: *"The pinned display projections are not widened: `view.board_view`'s five keys are asserted by tests and a CI smoke step."* | met |
| 4 | PR #536 fixed a **real leak**: `render_front` never checked `visibility`, so a `PRIVATE` or `CONCEALED` card's display name, role, observable facts and tags rendered in clear text | `strategy_game/characters.py:695-696` — `if card.visibility is not CardVisibility.PUBLIC: return f"[{card.visibility.value} card — content withheld]"` | met |
| 5 | `board_lines` dumped `leader.attributes` verbatim as JSON, with no filter on sensitive keys | `strategy_game/render/text.py:66,80` — `_PRIVATE_ATTRIBUTE_KEYS` and the filter that drops them | met |
| 6 | A **print-boundary redaction** was added as a last line of defence | `strategy_game/render/redaction.py` — `SENSITIVE_KEYS`, `redact`, `redact_mapping`, `emit` | met |
| 7 | A **sibling defect** surfaced: `board_lines` returned early for a board with no locations, so a state with leaders and no locations never printed its leaders | `strategy_game/render/text.py:93-100` — the early return now also requires `not state.leaders` | met |
| 8 | Verified on merged `main`: `render_front(private card)` → `'[private card — content withheld]'` | `tests/test_issue_536_render_redaction.py` — **13 tests, OK** | met |
| 9 | The disposition: **#4 and #5 dismissed** as false positives on the same grounds as #1; **#2 and #3 already fixed** by PR #536 | the alert table above | met — and **#2 and #3 are now `fixed` rather than dismissed**, which is a stronger resolution than the issue recorded |
| 10 | A **standing note**: if a location ever becomes a real place with a real address, the taint stops being structural and the dismissal must be revisited; `strategy_game/render/redaction.py` is where to add the rule | the note is carried forward in this record, below | met |

## The one reconciliation this record depends on

Issue #537 was written against `view.py` reading **`latitude`/`longitude`**. That is no longer
the case, and the change was not a retreat from the issue's account — it was the issue's account
being *acted on*:

**PR #539 (`245b40c`) renamed `Location.latitude`/`Location.longitude` to
`Location.grid_row`/`Location.grid_column`**, because the board holds a **grid reference for a
fictional tabletop map**, not a geographic coordinate, and CodeQL's `maybePrivate()` heuristic
reads the two old names as personal-location data. The taint source is therefore **gone at the
source** rather than dismissed. The issue's own framing — that the taint is *structural*, in a
dataclass shape — is what made the rename the right move: the shape was wrong, so the shape was
corrected.

Two consequences, both recorded rather than glossed:

- The issue's line reference (`view.py:43-44`) now reads `grid_row`/`grid_column`. The
  *structure* of the finding is unchanged; the field names are not.
- The issue's third claim — that removing the fields would break a pinned contract — was true
  **when written** and the rename respected it: the projection keeps its five keys
  (`schema_version`, `locations`, `network_nodes`, `network_edges`, `assets`), only the inner
  position keys changed name, and `strategy_game/tests/test_view_model_and_ports.py` was updated
  with them. `INTERFACE_SPIKE.md` rule 6 is therefore still satisfied: the projection was not
  widened.

**PR #540 (`8b97fe7`) then repaired the guard** that PR #538 had added. The guard landed between
the rename and the merge of the rename, so `main` was briefly red
(`Location.__init__() got an unexpected keyword argument 'latitude'`). The guard's *intent* is
unchanged and kept: no board-position value may reach the CLI's output. Only the names moved, so
the test moved with them, and the helper now matches `POSITION_KEYS` = {`latitude`, `longitude`,
`grid_row`, `grid_column`} — so it still catches the names CodeQL's heuristic matches *and* the
names this repository now uses.

## What the dismissal grounds are, made executable

The issue dismisses #4 and #5 on grounds that are easy to assert and easy to get wrong, so the
grounds were turned into runtime checks in `strategy_game/tests/test_cli_output_safety.py`:

1. **There is no log-file surface.** The package imports no logging framework, and neither
   flagged module writes a file. The only sink is `print()` to the caller's own stdout. A board
   payload inside a *log file* would be a genuine CWE-312 finding; the same payload on the
   terminal that asked for it is not. That distinction is the whole answer to the rule.
2. **The scaffold CLI's output is constant.** `python -m strategy_game` takes no argument, reads
   no environment variable and opens no file, so it prints one fixed **118-byte** empty board
   (verified: `python -m strategy_game | wc -c` → `118`) carrying no position value at all.
3. **The render CLI is a different case** and is *not* dismissed on the "constant output"
   reasoning: it has a `--world <file>` flag, so its output is not constant. What holds for it is
   fact 1 alone — the board goes to the terminal that asked for a rendering, and nowhere else.

Each guard class was proven **non-vacuous** by mutating the code and re-running: a world file
read from the environment, a `logging` import, and an absolute-path board write each fail the
guard that covers them. The mutations were reverted.

## The standing note, carried forward

If a location ever becomes a **real** place with a real address — a contributor's home, a
protected site, a person's location — then the coordinate taint stops being structural and this
dismissal must be revisited. `strategy_game/render/redaction.py` is the place to add the rule
then; today the only sensitive-keyed values are `private`/`secret`/`gm_notes` style attributes.

The rename in PR #539 makes this note **sharper**, not weaker: the board's positions are now
named for what they are, so the moment a real coordinate enters the data it will stand out as a
new field rather than sit silently inside a name that looks like personal location data.

## What is explicitly not claimed

- No rule, canon, mechanic, balance number or skill was changed by the CodeQL work.
- No board data was altered: the 8 Ukweli locations carried no position field before and carry
  none now.
- The `latitude`/`longitude` **names** were not kept. That was a deliberate, recorded choice
  (PR #539), and the issue's own reasoning — that the taint is structural in a dataclass shape —
  is what justifies it.
- The dismissal of #4 and #5 is a **false-positive** disposition, not a "won't fix": the
  behaviour is unchanged and is now guarded by executable tests.
- Nothing here asserts that a coordinate could never be sensitive. The note above is the part of
  this record that is meant to survive the closure.

## Verification

- `python -m unittest discover -s strategy_game/tests` — **1628 tests OK**
- `python -m unittest discover -s tests` — **598 tests OK** (includes the 13 of
  `test_issue_536_render_redaction.py`)
- `python -m strategy_game | wc -c` → **118**
- `python -m strategy_game.render --empty --cards` → a private card's content is withheld, and
  the run writes no file
- All five code-scanning alerts on this rule are `dismissed` or `fixed`; none is open
- `ruff check` clean on the added test file

— Ai (愛)
