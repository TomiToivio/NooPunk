# Attribution policy

**Status: PROPOSED — no licence is selected here.** Issue #421 item 4 names this as the missing artifact:
*"the project's own attribution policy is not yet written"*. This writes it. The two licence decisions
(software, content) and the commercial model remain the **author's** (VISION.md §7a, §9) and are tracked
in #421.

This document says how attribution is *done*, not which licence applies. It restates no exclusion list:
the excluded-licence set has exactly one home, `data/sources/game_system_rights.json`, and the packaging
rules have exactly one home, `data/licenses/release_packaging_policy.json`. Where this policy and those
files could disagree, **they win**.

---

## 1. What must always be attributed, whoever decides the licences

| Source | Obligation | Where it is already honoured |
| --- | --- | --- |
| **Fate Core** (Evil Hat / Fred Hicks, Rob Donoghue) | CC BY 3.0 — attribution required, and the official notice must appear verbatim | `strategy_game/rpg/ATTRIBUTION.md` (shipped under #389) |
| **NoöPunk's own text and rules** | The selected content licence's attribution terms, once chosen | **Open** — #421 item 1 |
| **This project's code** | The selected software licence's terms, once chosen | **Open** — #421 item 1 |
| **Research and theory** (Laclau, Castells, Luhmann, Faggin, Radin, Sheldrake, Powell and others) | Ideas are credited by name; no implication of endorsement or of proving a contested claim | `strategy_game/data/genre_paradigms.json`, `strategy_game/docs/GENRE_PARADIGMS.md`, `RULEBOOK.md` |
| **Eclipse Phase-derived material** | CC BY-NC-SA — **can never enter a distributable build** | `docs/licenses/ECLIPSE_PHASE_HOMEBREW.md`, quarantine in the packaging policy |

Two of these are settled and shipped. Two wait on the author. One is a prohibition rather than an
attribution.

## 2. The rules this policy adds

1. **Code and content are attributed separately**, because they are licensed separately. A file's
   licence is a property of its artefact class, not of the repository.
2. **Provenance is recorded where the material enters**, not reconstructed at release time. The rights
   ledger is the record of what came from where.
3. **A source named in-fiction is not an attribution requirement** — but a source *used* is. Fictional
   figures (per `AGENTS.md` §6.1) are not real people and must not be attributed as if they were.
4. **No endorsement may be implied.** Crediting an author for an idea does not suggest they endorse
   NoöPunk, and describing an in-world discovery does not claim a real one. The `51% QIP / 49%
   materialism` figure is in-world canon only (#345's own caution).
5. **A mention is not a derivation.** Naming an excluded licence in provenance prose is expected and is
   flagged as a warning, not an error, by the packaging guard; adapted expression from it is the thing
   that is forbidden.
6. **The attribution text is part of the build, not the repository.** Whatever the author selects must be
   reproduced in the distributed artifact, which is why the guard checks a release *set* rather than the
   working tree.

## 3. What happens once the author decides

When #421 items 1–2 are settled, this document gains one table row per license and the concrete
attribution strings; the guard's `licence-decision-open` error clears; and `LICENSE` / `NOTICE` files can
be created — which the guard's tests assert do **not** exist yet, so that a release cannot be declared
clean by accident.

## 4. Verification

`tests/test_release_packaging_guard.py` pins the parts that are executable: that no licence is selected
by the packaging policy, that no `LICENSE`/`NOTICE` file has been created ahead of the decision, that a
release set containing NC-SA-derived material fails, and that a public release is blocked until the
decision is made. The prose above is not tested — automated tests cover executable code only (#271).
