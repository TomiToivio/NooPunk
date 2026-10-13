# Release-time clean-up audit — the register (issue #421, item 3)

**What this is.** The measured output of the release packaging guard (`tools/release_packaging_guard.py`,
issue #231), run against `main`, recorded as the register of what must not ship. It selects no licence
and approves nothing; the two licence decisions and the commercial model remain the author's
(VISION.md §7a, §9).

Re-run it: `python3 tools/release_packaging_guard.py --mode audit`

## The run

```
PASS: 0 error(s), 39 warning(s)
```

**0 errors** means no release-set path is encumbered in a way the policy forbids outright. The warnings
are of two kinds, and only one kind is work.

## The work: quarantined material that would be released (7 paths)

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

**Two acceptable resolutions, and they are the author's call because they are a scope decision, not a
licence one:** exclude these paths from the release bundle (the guard's `--bundle` mode makes this
checkable), or replace the prototype with an original system. Until either happens, the release gate
stays blocked — which is exactly what the packaging guard exists to say out loud.

`tests/test_release_cleanup_register.py` pins this list: if one of these paths stops being flagged, or
an error appears, the test fails rather than the register quietly going stale.

## Not work: documented licence mentions (32 warnings)

The remaining warnings are `documented-licence-mention` — provenance prose naming an excluded licence
(CC BY-NC, BY-NC-SA, NonCommercial, OGL 1.0a, Product Identity). The policy distinguishes a **mention**,
which is expected in documentation and in the rights ledger, from **adapted expression**, which is the
thing forbidden. These are listed by the guard for a human to confirm, not to fix.

## What this does not decide

No licence is selected for the code or for the content. No commercial model is chosen. No path is
excluded from the release set by this document: it records what the guard found, and the exclusion itself
is the author's decision, carried as queue row D10.
