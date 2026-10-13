# Issue #327 — acceptance record

**What this file is.** The criterion-by-criterion verification that issue #327's deliverables are
met, at the point of closing it. It adds no design content and changes no decision: it records where
each requested deliverable lives, how it was verified, and what stays **OPEN** so closure does not
bury it.

**What closure does not mean.** Closing #327 means *the requested documents exist and were
verified*. It does **not** approve an ideological rule, change canon, or expand the three initial
parties — the issue's own review checkpoint is **unspent**, which the deliverable itself states in
its §10.

## The deliverable

`strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md`, merged as PR #364 (387 lines).

## Verification, criterion by criterion

| # | Requested | Where it is met | Verified |
| --- | --- | --- | --- |
| 1 | Short, source-aware research/design proposal at `strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md` | the file itself | present on `main`; sources named and fetched (Pew Research Center, 11 Dec 2024; Pew, *How the U.S. Public and AI Experts View AI*) |
| 2 | 2D baseline compass + optional tags, three independent crisis dimensions, no misleading 3D compass | §1 *The baseline compass: two axes, and tags that are not axes*; §2 *Why there are three crisis dimensions and not a third axis* | both sections assert the separation explicitly |
| 3 | Cross-tab of the three canonical parties × crisis interpretations, policy demands, internal disputes, coalitions, communication/institutional resources | §5 *Cross-tab: the three canonical parties × the three complexes*, with per-complex subsections A/B/C; §6 for signifiers and Castellsian networks | §5 opens from the issue's own CANON power asymmetry and carries per-party readings; §6 keeps network power explicitly apart from public consent |
| 4 | A small optional list of emergent organisations, not a dozen playable factions | §7 *Emergent organisations — a shortlist, not a roster* | labelled a shortlist; none is promoted to a playable party |
| 5 | Three event vignettes **plus** a minimal proposed data schema, no engine rewrite | §8 *Three event vignettes* (verified NHI biologics/technology; AGI + BCI/cyborg adoption; PSI commercial scandal under an information blackout); §9 *A minimal proposed data schema (a document, not an implementation)* | §9 states "PROPOSAL ONLY … No file is added and no engine code is touched" |
| 6 | Mark canon vs research findings vs author proposals vs fictional assumptions distinctly, and link relevant issues | *How to read the marks*: CANON / SOURCE / PROPOSAL / FICTIONAL ASSUMPTION / OPEN | the five marks are defined up front and used throughout; #324, #325, #326, #282, #297, #305, #309, #322 are cited in text |
| 7 | Explicit review checkpoint before coding rules, changing canon or expanding the three parties | §10 *What this document deliberately does not do*, closing clause: "The review checkpoint is unspent" | consistent with the repository state: no ideological rule, module, data file or test was added by this work |

Also asked for in the body and present: the PSI institutions/rights/law treatment (§4), the
three-party baseline with its power asymmetry (§5 opening), the Laclaudian empty/floating signifiers
and antagonistic frontiers (§6), the Castellsian media/funding/infrastructure networks tracked
separately from consent (§6), and the EP24 far-right / centre-right / red–green groupings used as a
comparative starting point rather than transferable polling (source-aware, marked SOURCE).

## Carried forward — OPEN, not settled here

These were flagged by the deliverable and remain for the author. Listing them here is the point of
this record: closing #327 must not lose them.

- **The state's formal name** — #324 §4.1; still OPEN.
- **The third party's name** — the issue's table says **ULP (Ukweli Libertarian Party)**; the #325
  brief and #326 say **LFP (Libertarian Freedom Party of Ukweli)**; `data/ukweli_local.json` and
  `data/global_factions.json` use `ulp`. Recorded in §5, deliberately not resolved.
- **The restricted island's legal autonomy** — #324 §4.3; still OPEN.

## Verification method

Read of the merged file on `main` plus the issue body's own criteria list (fetched from the issue),
checked criterion by criterion rather than by summary. No content of the deliverable was modified to
make it pass: a deliverable that needed editing to satisfy its own criteria would have been reported
as a gap instead of closed.
