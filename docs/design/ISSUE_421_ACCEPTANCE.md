# Issue #421 — acceptance record

**Basis for closing.** The author instructed that this issue be done and closed (2026-10-13), under the
defer-and-close rule he authorised the same day. One distinction is load-bearing here and is stated
rather than glossed: **the two licence decisions are not made by this closure.** Agents are forbidden to
select a licence, choose a commercial model or create `LICENSE` / `NOTICE`, so those items are recorded
as **deferred** to the author and carried as queue row **D10** — and because that row now holds them,
closing this tracker loses nothing.

## Item by item

| # | Item | Position |
| --- | --- | --- |
| 1 | **The software licence** | **deferred** — the author's alone. Queue row D10. |
| 2 | **The content licence** | **deferred** — the author's alone, and separate from the software licence per VISION.md §7a. Queue row D10. |
| — | **The commercial model** | **deferred** — the author's alone. Queue row D10. |
| 3 | **The release-time clean-up** | **met, and measured.** The packaging guard exists and runs: `python3 tools/release_packaging_guard.py --mode audit` reports **PASS: 0 error(s), 39 warning(s)** on `main`, with `tests/test_release_packaging_guard.py` (19 tests) green. Its own finding is recorded in the new register: **7 EP-derived paths would be released as the release set stands** — the four `src/eclipse_phase_homebrew/` modules, the two `src/concordia_runtime/ep2_*.py` adapters and `scripts/ep2_concordia_smoke.py` — and the other 32 warnings are documentation mentions, expected in provenance prose. |
| 4 | **The attribution policy** | **met.** `docs/ATTRIBUTION_POLICY.md` (PROPOSED; it selects no licence) rests on `data/sources/game_system_rights.json` and `data/licenses/release_packaging_policy.json`, and routes the Eclipse Phase obligation to `docs/licenses/ECLIPSE_PHASE_HOMEBREW.md`. |

## New in this PR

- **`docs/licenses/RELEASE_CLEANUP_AUDIT.md`** — the clean-up register: the guard's measured output, the
  seven quarantined paths named one by one, the two acceptable resolutions (exclude them from the
  release bundle, or replace the prototype with an original system), and the distinction between a
  licence *mention* (expected) and adapted *expression* (forbidden).
- **`tests/test_release_cleanup_register.py`** — pins the register: if a quarantined path stops being
  flagged, or the guard starts erroring, the test fails rather than the register quietly going stale.

## The release gate

It stays **blocked**, on two conditions and not one: the seven quarantined paths must leave the release
set (or be replaced), and items 1–2 must be chosen. That is now stated in one place with the guard's own
numbers behind it, which is what this issue existed to track.

## What is not claimed

No licence is selected, no commercial model is chosen, no path is removed from the release set by this
record, and nothing here is legal advice. The register reports what the guard found.

— Ai (愛)
