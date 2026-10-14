# Issue #447 — acceptance record

**Basis for closing.** The author authorised defer-and-close on 2026-10-13, provided the record states
a deferred item as deferred rather than met. This record does that. It credits the work it audits
rather than duplicating it: the specification is
[`ISSUE_447_PILGRIM_PRESENTATION_SPEC.md`](ISSUE_447_PILGRIM_PRESENTATION_SPEC.md) (PR #450, extended by
PR #452), the rulebook half is `RULEBOOK.md` §1.4 / §2.2 / §35.3 / §35.8 (PRs #448, #449), and the ledger
provenance is PR #451.

## The issue's acceptance criteria

| # | Criterion | Position |
| --- | --- | --- |
| 1 | **A concise art-direction and narrative-framing specification** for the 1974-origin aesthetic | **met** — `docs/design/ISSUE_447_PILGRIM_PRESENTATION_SPEC.md`, 206 lines, nine sections: the one rule, art direction, narrative framing, the boundary, the discrepancy register, worked templates, licensing, non-goals, cross-references |
| 2 | **`Zardoz` visual #1, PKD author #1, *Space Ritual* soundtrack #1**; only the named reference set | **met** — the spec's §2.1/§2.2/§2.3 tables carry the three at **#1** with their reasons; §2.1 states the no-substitution rule as binding on the document itself, and §8 repeats it as a non-goal. The rulebook carries the same locked set at §35.8 (sound) and §35.3 (books) |
| 3 | Describe the living Helsinki author, the VALIS download, the novel, fandom, adaptations, scholarly attention, university parapsychology | **met** — the narrative text is `RULEBOOK.md` §1.4; the framing is the spec's §3.1–§3.3. The **story prose remains the author's** (standing project rule), which is what the criterion asks for and not a shortfall of it |
| 4 | An explicit **presentation vs canonical-reality boundary**, with examples of non-disruptive discrepancies | **met** — the spec §1 (the one rule: presentation is not canon, and the canonical fact wins), §4 (a two-layer table stating what each side may and may not decide), §5 (a four-kind discrepancy register, each with a display convention), §6.4 (a worked notice) |
| 5 | **Examples/templates** for novel excerpts, marginalia, UI styling and alt-history inconsistencies | **met** — the spec §6.1 (a novel excerpt in period voice carrying a *correct* account with the error confined to a recording medium), §6.2 (the marginalia convention: `[TP]`, `[ED. n]`, `[ARCHIVE]`), §6.3 (an interface-styling note), §6.4 (an alt-history discrepancy notice) |
| 6 | Document the **Creative Commons licences, attributions and incompatibilities** without claiming false permissions | **met** — the spec §7 states the three licences, the binding guardrails (CC BY does not override NC/SA; no whole-project CC BY claim; no single-licence claim; ideas separated from expression), and now names **where the licence authority lives**, with the precedence rule that the ledger wins a disagreement. The ledger itself: `docs/sources/EXTERNAL_SOURCE_LICENSES.md` (#60), `docs/sources/GAME_SYSTEM_RIGHTS.md` + `data/sources/game_system_rights.json`, `docs/sources/ATTRIBUTION.md`. PR #451 closed the one provenance gap, sourcing the *Transhumanity's Fate* claim — and, correctly, recording that the publisher's announcement gives **no version number**, so the ledger's "3.0" stays unconfirmed |
| 7 | Keep story, scenario, mechanics, world model and timelines **unchanged**; do not rewrite content | **met — and measured.** The five commits this ticket produced touch **six files**: `RULEBOOK.md`, the two generated parts under `rulebook/parts/`, the derived `data/rules/rulebook_split_manifest.json`, the specification, and one ledger record (`data/sources/game_system_rights.json`). **No `src/` file, no `.py`, no `core.json`, and no mechanics, statistics, chronology or scenario artefact was altered.** The single `data/rules/` entry is the split manifest, which is *derived* and whose guard requires regeneration whenever the canonical prose moves |

## The three rulebook deliverables the author added on 2026-10-14

| Request | Position |
| --- | --- |
| The Tommy Pilgrim background story as the rulebook's **introduction, before the scenario** | **met** — `RULEBOOK.md` §1.4 *"How this book came to exist: Tommy Pilgrim, 1974"*, placed at the end of the introduction so it frames §2 and displaces nothing. It carries the download, the book, the genre, the fandom and the living Helsinki author, and states the rule that keeps the frame safe: *the book is an imperfect 1974 decoder; canon wins where they disagree* |
| The **Event Card idea** in the rulebook's Event Cards section, **default timeline first, variability later**, details to be decided later | **met as structure; the details are deferred, as directed.** §2.2 *"Event cards: how this history reaches the table"* records the idea with the phasing, consumes the eleven authored seeds rather than forking a second deck, and leaves card taxonomy, deck size, probabilities, draw cadence, triggers and effects **TBD** — which is the issue's own instruction, not an omission |
| The author's **inspirations in the sources list** | **met** — the §35 source map carries the *Iron Dream* entry with the details verified against the article the issue links (Spinrad's real authorship, the nested *Lord of the Swastika*, the alternate-history Hitler, Homer Whipple's faux-scholarly afterword, and the guard against borrowing the nested book's politics), plus the reading list. The framing spec's §3.4 records the model itself, because a *narrative-framing* specification that omits the issue's designated model leaves its own device unexplained |

## What this record does not claim

- **No mechanic, rule, statistic or scenario fact** is claimed as landed, and none was authored.
- **The Event Cards rules are not met and are not claimed.** Only the section's existence, its phasing and its reuse obligation are.
- **No test exists or should exist** for any of this ([#271](https://github.com/TomiToivio/NooPunk/issues/271)): the specification and the rulebook prose are reviewed editorially and by playtesting.

## Deferred — the two questions still the author's, to be carried as queue rows

1. **Which rulebook owns §1.4 and §2.2.** They currently sit in the legacy canonical `RULEBOOK.md` — the file whose scenario the introduction precedes and whose source map was extended. Moving them to the **crossover** rulebook (where `strategy_game/data/**` holds the seeds and Layer II reserves systemic events, now that #389 gives the crossover an approved Layer I) is a move plus a parts regeneration. *Smallest useful answer:* name the rulebook.
2. **Whether *The Iron Dream* also joins the locked in-universe hierarchy** in the spec's §2.2 (a fourth slot beside PKD, Wilson and Le Guin). Its 1972 date permits it; that section's rule is to include only the named set, so no document has added it. *Smallest useful answer:* accept / decline.

Neither question gates a criterion above, which is why they are deferrals rather than blockers.
