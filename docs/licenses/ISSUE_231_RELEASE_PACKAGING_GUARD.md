# Issue #231: the release packaging guard

**Status: guard implemented; the licence decision remains OPEN and belongs to the author.**
This document describes the executable packaging check. It does **not** select a licence, and
no `LICENSE` or `NOTICE` file is created — relicensing the repository is a one-way legal act
that issue #200 reserves to the author.

Companions: [`ISSUE_200_CC_RELEASE_GATE.md`](ISSUE_200_CC_RELEASE_GATE.md),
[`ISSUE_200_LICENSE_AND_NOTICE_PLAN.md`](ISSUE_200_LICENSE_AND_NOTICE_PLAN.md),
[`ECLIPSE_PHASE_HOMEBREW.md`](ECLIPSE_PHASE_HOMEBREW.md).

## Why this exists

Issue #231 asks for *"machine-readable component-level rights ledger, attribution and release
packaging guard"*, and the release gate's own checklist asked for the last missing piece:

> *"Add checks that flag unreviewed third-party material in packaging and prevent
> reintroduction of explicitly excluded licenses."*

The audit (`data/sources/game_system_rights.json`), the itemized licence/NOTICE plan and the
release gate already existed. Nothing guarded the **packaging step**, so an excluded licence or
the quarantined EP2 prototype could re-enter a release bundle without any test noticing.

## The pieces

| Artifact | Role |
| --- | --- |
| `data/licenses/release_packaging_policy.json` | machine-readable packaging rules: quarantine list, artifact classes, exclusion vocabulary |
| `tools/release_packaging_guard.py` | the check, runnable and importable |
| `data/sources/game_system_rights.json` | the single source of truth for *which licences are excluded* |

The policy defers its exclusion vocabulary to the rights ledger's `decision_vocabulary`, and the
guard **errors if the two drift apart**. That is deliberate: a packaging gate that maintained its
own second copy of "excluded licences" would eventually disagree with the audit it is supposed to
enforce.

## Two modes, and strictness follows the bundle

* **Full-tree scan** (`--mode audit`, no `--bundle`) — every release-bound path is checked.
  Findings about unreviewed paths and documented licence mentions are **warnings**, because a
  mid-development tree legitimately contains both. Internal inconsistency is still an error.
  This is what CI runs.
* **Explicit bundle** (`--bundle manifest.txt`) — the listed paths *are* the release set, so a
  quarantined or unreviewed path in it is an **error**. This is the actual packaging gate.

`--mode public` additionally **fails while the author's licence decision is open**, because a real
release may not be declared clean on an unmade choice.

```
python3 tools/release_packaging_guard.py --mode audit                   # CI, full tree
python3 tools/release_packaging_guard.py --bundle bundle.txt --mode public
```

## What the guard enforces

1. **Quarantine.** A path matching the quarantine list (the EP2 homebrew prototype and its
   Concordia/script adapters) may not appear in an explicit release bundle. In a full-tree audit
   the same finding is a warning: the prototype legitimately lives in the repository, and it is
   the *release step* that must exclude it.
2. **Coverage.** Every path in a release set must be covered by an artifact class from the
   licence plan. An uncovered path is unreviewed third-party material.
3. **No excluded licence by declaration.** No artifact class may be declared under a licence
   decision the ledger excludes — the class-level half of "prevent reintroduction".
4. **Consistency.** The policy's exclusion vocabulary must exist in the ledger.
5. **Fail closed.** A missing or unparseable policy/ledger raises; it never becomes a pass.

## What the guard deliberately does NOT enforce

**Documented licence mentions are warnings, always.** `README.md`, `RULEBOOK.md` and the audit
records *name* excluded licences — that is what a provenance record is for. By inspection, a
sentence stating "the game contains BY-NC-SA-derived material" is indistinguishable from text
copied out of a BY-NC-SA work, so no mechanical rule can promote this to a pass/fail verdict
without becoming a false-positive machine. It is an **inventory for human review**; the
enforceable checks are quarantine, coverage and class-declaration.

Legal clearance is likewise out of scope. The guard answers *"is this bundle internally
consistent with the recorded rights position?"*, not *"is this bundle lawful?"*. The release gate
still calls for a release-stage legal review before publication.

## Current state on `main`

* Full-tree audit: **PASS** (warnings only — the EP2 prototype and documented mentions).
* Public mode: **FAIL** by design, because every artifact class is still `author-decision`.

The guard is meant to keep failing in public mode until the author selects a licence. That is the
point: the failure is the record that the decision is still open.
