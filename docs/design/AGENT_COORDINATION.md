# Before you build: how not to do another agent's work twice

This repository is worked by several agents at once, often on the same issue, sometimes within the same
hour. That is deliberate and it is not going to change. What has to change is the part where two agents
each build the same thing and nobody notices until the numbers disagree.

This is not hypothetical. In one evening of parallel work on #1068 the tree acquired:

* **three implementations of one SRD section** — "Lifestyles, Wages and Bribes" existed as an embedded
  table in `src/rules/cwn_lifestyles.py`, as two catalogues in `data/rules/cwn/`, and as a separate loader
  in `mud/nopunk_mud/cwn/economy.py`;
* **three implementations of the overcasting roll**, in `cwn_magic`, `cwn_spells` and `EffortPool`;
* **two implementations of Alienation**, whose chrome-syndrome tables had already drifted: Stressed was
  worth `+3` in one and `+5` in the other, and the SRD says `+5`;
* **two generated CWN coverage reports** from one tool, plus five older hand-maintained matrices, six of
  which gave a different answer to "how much of CWN is implemented?";
* **three architecture surveys** of the same tree, written the same day.

Everything below exists so that the next agent spends ten minutes checking instead of an hour rebuilding.

## 1. Search first — three commands, in this order

```bash
python3 tools/duplication_audit.py --all         # duplicated rules, duplicated tables, duplicated documents
grep -rn "def <the_procedure_you_are_about_to_write>" src/rules mud        # is it already written?
grep -rln "<the_concept>" docs/rules data/rules                           # is it already documented?
```

`tools/duplication_audit.py` groups rule definitions by name and compares bodies, and with `--all` it also
compares literal tables (dicts/sets of five or more keys, in code or in data) and document headings. It is
cheap and it is intentionally dumb: a hit is a question ("is this the same rule?"), never a verdict.

Then read `docs/DOCUMENT_REGISTER.md` — it names the canonical document for each topic so you do not
write a sixth coverage matrix.

## 2. Content lives in data, procedures live in code, adapters do neither

| what | where | rule |
| --- | --- | --- |
| rule **numbers** (tables, costs, catalogues) | `data/rules/**/*.json` | one row per rule; a module may not restate a table it can load |
| rule **procedure** | `src/rules/**.py` | one function per rule; a second module may call it, never copy it |
| **presentation** | `src/console`, `godot/`, `mud/`, `portable_noopunk/` | reads the canonical procedure; may reformat the answer, may not recompute it |
| **claim** about coverage | `docs/rules/CWN_COVERAGE_1068.md` | generated; never hand-edited |

The corollary is the one that kept being broken: **a module that reformats an answer must not also
re-derive it.** `mud/nopunk_mud/cwn/economy.py` used to read the wage table itself; it now calls
`rules.cwn_lifestyles.wage()`. `cwn_spells.overcast_roll()` used to re-add the same numbers; it now calls
`cwn_magic.overcast_total()`.

## 3. Claim a slice before you write code

1. **Comment on the issue** with the slice you are taking and the branch name, for example
   `Taking: special combat maneuvers -> branch feat/1068-maneuvers`. One line, before the first commit.
2. **Check for a claim or an open PR on that slice** (`gh pr list --search "1068" --state open`) and for a
   merged one (`gh pr list --state merged --search "1068"`). If someone else is already on it, either
   review theirs, or take a *different* slice and say so.
3. **Name the branch after the issue and the slice**: `feat/<issue>-<slice>`, not `feat/fix-stuff`.
4. **One PR per slice.** A second PR for the same slice is a merge, not a contribution — see §5.

The issue is the shared notebook. The commit message is not.

## 4. If you find a duplicate, you own the merge

A duplicate that is reported and left alone is a duplicate that will drift. The merge protocol:

* **Delegate, do not delete.** Keep the public API of the module that other code imports; make it call
  the canonical implementation. `cwn_alienation.SYNDROMES` still exists and still has `max_bonus`; it is
  now derived from `cwn_cyberware.SYNDROMES`, so the two cannot disagree again.
* **Pick the canonical side by evidence, not by age**: the one with SRD citations, tests and the wider
  call graph usually wins. When two implementations disagree on a *number*, the SRD decides — during this
  merge the SRD said Stressed is `+5`, so the module that said `+3` was wrong, not merely older.
* **Say which one is canonical in a docstring**, with the reason. The next agent reads the module.
* **Pin it with a test that asserts an equality between the two paths**, never a literal number:
  `assert cwn_spells.overcast_outcome(t)["strain"] == cwn_magic.overcast_result(t)["strain"]`.
  A literal can be copied; an equality cannot be satisfied by a second transcription.
* **Retire the document, do not rewrite it.** Add a `> **Superseded:**` banner pointing at the canonical
  file and register it in `docs/DOCUMENT_REGISTER.md`. Deleting the history is worse than keeping a stale
  copy that admits it is stale.

The merged copies from this audit are guarded by `tests/test_rule_duplication_merged.py`.

## 5. Two PRs for one slice

Do not open a third. Merge the second into the first — the older PR wins unless it is abandoned — and say
in the closed one which PR carries the work and why. If both landed already, consolidate in a follow-up
that keeps both test suites green, then delete the weaker implementation.

## 6. What CI enforces, and what it cannot

CI enforces: tests, the rules constitution, CWN baselines, matrix freshness, packaging, and — after this
audit — cross-module equalities and the absence of a second generated report.

CI **cannot** enforce Markdown consistency (#271 forbids asserting over prose). Documentation duplication
is therefore a human-review obligation. That is why `docs/DOCUMENT_REGISTER.md` exists as a
machine-readable-ish list and why the superseded banner is a one-line, greppable convention:

```bash
grep -rln "> \*\*Superseded:\*\*" docs | wc -l     # how much history is explicitly retired
```

## 7. When in doubt

Ask the issue. A comment that says "I am about to implement X in Y; is that already covered?" costs one
minute and has, on this repository, been cheaper than every reimplementation listed at the top of this
page.
