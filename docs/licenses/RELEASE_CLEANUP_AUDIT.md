# Release-time clean-up audit — the register (issue #421, item 3)

**What this is.** The measured output of the release packaging guard (`tools/release_packaging_guard.py`,
issue #231), run against `main`, recorded as the register of what must not ship. It selects no licence
and approves nothing; the two licence decisions and the commercial model remain the author's
(VISION.md §7a, §9).

Re-run it: `python3 tools/release_packaging_guard.py --mode audit`

## The run

```
PASS: 0 error(s), 44 warning(s)
```

**0 errors** means no release-set path is encumbered in a way the policy forbids outright. The warnings
are of two kinds, and only one kind is work.

## The work: quarantined material that would be released (9 paths)

These are the EP-derived artefacts. Each is recorded in `docs/licenses/ECLIPSE_PHASE_HOMEBREW.md` and
quarantined by `data/licenses/release_packaging_policy.json`; the guard's point is that they sit in the
release set as it currently stands, so a package built today would carry them.

| Path | Why |
| --- | --- |
| `src/eclipse_phase_homebrew/__init__.py` | EP2 homebrew prototype; CC BY-NC-SA-derived |
| `src/eclipse_phase_homebrew/core.py` | same |
| `src/eclipse_phase_homebrew/embodiment.py` | same |
| `src/eclipse_phase_homebrew/interactions.py` | same |
| `src/concordia_runtime/ep2_adapter.py` | Concordia adapters for the same prototype; same NC-derived boundary |
| `src/concordia_runtime/ep2_session.py` | same |
| `scripts/ep2_concordia_smoke.py` | EP2 smoke script for the same prototype; same NC-derived boundary |
| `tests/test_ep2_session.py` | the prototype's own tests; they import `eclipse_phase_homebrew` and `concordia_runtime.ep2_session` directly and encode its percentile/pool fixtures |
| `tests/test_issue60_ep2_interactions.py` | the same prototype's interaction tests; same direct imports |

**The last two rows are a correction to this register.** As first written it listed seven paths, because
the quarantine list covered the prototype, its Concordia adapters and its smoke scripts — but not the
modules that exercise it. Measured at `c45a7b8`, a `--mode public` bundle containing
`tests/test_ep2_session.py` and `tests/test_issue60_ep2_interactions.py` returned **no**
`quarantined-path-in-release-set` finding: the only error was the open licence decision. So a
distributable build carrying EP-derived test material would have passed the check whose whole purpose is
to stop that. Two globs were added to `quarantined_paths` with the reason recorded on each; the same
bundle now returns two quarantine errors, and `tests/test_release_packaging_guard.py` and
`tests/test_release_cleanup_register.py` both pin the widened set.

**Two acceptable resolutions, and they are the author's call because they are a scope decision, not a
licence one:** exclude these paths from the release bundle (the guard's `--bundle` mode makes this
checkable), or replace the prototype with an original system. Until either happens, the release gate
stays blocked — which is exactly what the packaging guard exists to say out loud. A source distribution
that omits the prototype's tests costs nothing: they cannot even import without the quarantined modules.

`tests/test_release_cleanup_register.py` pins this list: if one of these paths stops being flagged, or
an error appears, the test fails rather than the register quietly going stale.

## Not work: documented licence mentions (35 warnings)

The remaining warnings are `documented-licence-mention` — provenance prose naming an excluded licence
(CC BY-NC, BY-NC-SA, NonCommercial, OGL 1.0a, Product Identity). The count rises as licence records land:
this register and the #421 records are themselves mentions, which is the correct behaviour, not drift.
The policy distinguishes a **mention**,
which is expected in documentation and in the rights ledger, from **adapted expression**, which is the
thing forbidden. These are listed by the guard for a human to confirm, not to fix.

## Second finding, reported and deliberately **not** fixed

`tools/release_packaging_guard.py`'s `iter_tree_paths()` (~lines 158–167) walks the **working tree**
rather than the repository, and does not skip untracked or ignored paths — contradicting its own
docstring (*"every tracked file is checked"*) and its `SKIP_DIRS` comment about *"VCS metadata, caches,
editor droppings"*.

The consequence is a verdict that depends on which of the repository's own commands a developer has
run. `scripts/noopunk_text.py` writes `noopunk-save.json` into the repository root by default and CI runs
it as a smoke step; opening the Godot project writes `.godot/` editor caches, which `.gitignore` already
declares. On a machine that has done either, `python -m unittest discover -s tests` fails two of the
guard's own contracts — `test_the_audit_reports_no_unreviewed_material` and
`test_every_tracked_path_is_classified_or_quarantined` — on six paths that are not in the repository and
cannot be released. The same commit passes in CI, which checks out clean.

That is the noise-hides-signal failure the artifact classes were corrected for in PR #429, in a second
place — the scan rather than the classes. **It is recorded here and handed to the author, not repaired:**
what "release-bound" should mean (ignore-aware `git ls-files` versus an explicit skip list) is a decision
about the enforcement rule, and nothing about it blocks the release gate, which the open licence decision
blocks first. No line of `tools/release_packaging_guard.py` or `.gitignore` was changed by this work.

## What this does not decide

No licence is selected for the code or for the content. No commercial model is chosen. No path is
excluded from the release set by this document: it records what the guard found, and the exclusion itself
is the author's decision, carried as queue row D10.
