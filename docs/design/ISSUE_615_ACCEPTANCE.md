# Issue #615 — acceptance record

**Governing design decision, recorded. Checked against `origin/main` at `e16d025`.**

## Criterion check

| # | Criterion | Evidence | Met |
| --- | --- | --- | --- |
| 1 | Document the core hierarchy and four genre/location mappings in the canonical rules documentation | `docs/design/ISSUE_615_RULES_BASELINE.md` §1 — one core contract, four modules, with per-module "what it contributes" **and "what it must not contribute"** | yes |
| 2 | Cross-reference #564 and pre-existing approved character/check decisions; publish a conflict-and-resolution register | §3 — 10 rows, each with the conflict, the evidence and the direction taken: `1d10` vs 2d6 (#111 vs CWN), classes (#197/#566), `SOC` vs `CHA`, the non-existent 3d6, two kernels (#389/#482), PSI ontology (#482), hacking, AWN's apocalypse premise, WWN cosmology, long-term independence | yes |
| 3 | System-by-system provenance, licensing, adaptation and compatibility matrix | §4 — eight sources, status measured against `data/sources/game_system_rights.json` and the #569 audit: CWN CC0, WWN CC0 (SRD scope only), **SWN `blocked-unverified`**, **AWN `blocked-unverified`**, Fate per-option, Transhumanity's Fate and EP2 BY-NC-SA, AW/Veil inspiration only | yes |
| 4 | A concrete unified mixed-genre play example using one character sheet and one resolution grammar | §6 plus **executable**: `tests/test_issue615_mixed_genre_grammar.py`, 6 tests. One sheet, four environments, one kernel | yes |
| 5 | Lightweight optional narrative and simulation layers with clear triggers and costs | §5 — four layers (aspect, complication, clock, fail-forward) with trigger, cost and an explicit "what it cannot do"; **core-only play must remain possible** | yes |
| 6 | Preserve no-LLM tabletop scenarios and regression tests across all four environment types | The same test file: four environments resolve on `core.resolve_check`; seeded replay is exact; the kernel is asserted free of `openai`/`anthropic`/`requests`/`urllib`/`socket`/`http`; the sheet is asserted unmutated by every environment | yes |
| 7 | Vetted credits, licence notices and non-endorsement disclaimer in repo-facing documentation | `README.md` → "Rules influences", extended with the #615 baseline, a precise licensing paragraph and a non-affiliation sentence | yes, **with corrected wording** (see below) |
| 8 | Maintain a versioned, independently authored evolution roadmap, driven by playtesting | §8 — Stages A–D with exit criteria and versions `0.x → 1.0`, plus the rule that **independence is not cosmetic renaming** | yes |

## Corrections made to the issue's own text

Two claims in #615 needed adjusting before they could be shipped as documentation.

1. **"CWN is the primary mechanical reference"** cannot extend to the *check kernel*. CWN's core is
   `2d6`; NoöPunk's is `STAT + Skill + 1d10` (#111), and #566 ruled `1d10` stays. #615's own
   non-regression clause resolves this: the family is the primary **procedure** reference, the kernel
   stays. Reversing the kernel would touch 80 `1d10` sites across 41 files and 41 test files.
2. **The proposed credit sentence overstated the licensing.** *"primarily based on/adapted from the
   Without Number family"* is not supported for SWN or AWN, which have **no verified SRD** and are
   `blocked-unverified` (#569). The README therefore names the **CWN and WWN SRDs** as adapted
   sources and SWN/AWN as **design references only**. Credit is not a licence, and no single licence
   covers the family.

## What is shipped versus what is proposed

- **Shipped:** criteria 1–6, 8, and the corrected credits block in `README.md`.
- **Still the author's:** the final credit wording, and **D10** (NoöPunk's own licence pair). An agent
  may state facts about licences; choosing one is not an agent's call.
- **Not claimed:** Stages B–D. §8 is a roadmap with exit criteria, not a status report.

## Verification

- **715 root tests OK** (6 new in `test_issue615_mixed_genre_grammar.py`).
- `tools/release_packaging_guard.py --mode audit`: **PASS, 0 errors, 338 warnings**. The count moved
  from 337 to 338 because the README now documents another licence — that is the guard's inventory
  noticing a new documented mention, not a regression.
- No mechanic, die, number, class or threshold was changed by this issue.
