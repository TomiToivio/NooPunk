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

---

## Addendum, same day: the issue grew after this record was written

This record audits the issue as it stood at **27,745 characters**, which is the revision the five commits above were produced against. **The body then grew to 39,599 characters**, adding four sections and seven further acceptance checks:

- ***A 1974 film that accurately predicts 2026*** — the governing maxim **"NoöPunk looks as if it was MADE in the seventies, not SET in the seventies"**, with the timeline-slip rule that divergences stay rare, identified, minor and non-cascading;
- ***Visual art direction for later game graphics and UI*** — the comics/graphic-art references added to the hierarchy (**Mœbius**; **Christin and Mézières' *Valérian et Laureline***) with *Zardoz*'s position as #1 unchanged, plus the visual vocabulary, six concrete graphics concepts (a punch-card LLM interface, discourse mapping, NHI contact, a PSI laboratory, the faction board and event cards, map fieldwork) and the production constraints;
- ***Writing style: precognitive science fiction written/filmed in the seventies*** — period futurology and prose, the framing convention contrasting a "Pilgrim, 1974 edition" excerpt with an "Editorial/Simulation note, 2026", and the sound direction;
- ***1970s state of the art: grounded reference shelf*** — six period sources (Toffler; Meadows et al.; Hynek; Vallée; Targ and Puthoff; Marks and Kammann) with their dates and their epistemic cautions, including the pre/post-1974 chronology that separates what Pilgrim could have read from later commentary.

**This record does not audit those four sections and does not claim their seven checks.** They are being delivered by **PR #457** (`pilgrim-spec-447-v3`), which re-applied on top of #451 and #452 and preserved this document's §3.4 verbatim rather than losing it in a rewrite.

**The close this record accompanied was reversed.** The issue was closed and then **reopened**, because a closure labelled *completed* over a revision nobody had audited is a false record — the failure mode this addendum exists to prevent. Extend the addendum against the merged #457 before closing the issue again, and state the revision in characters, since that is what changed.

---

## Addendum 2, 2026-10-15: the expanded criteria, audited against the tree

**Why this exists.** Addendum 1 ended by handing a condition to its successor — *"Extend the addendum against the merged #457 before closing the issue again, and state the revision in characters, since that is what changed"* — and named four added sections and their seven checks as **unaudited**. This is that audit. It is measured against the tree, not against the claims in the thread, and it is the criterion map the issue has never had.

**The revision, in characters: 39,599**, carrying **32** checkboxes. Re-measure before any close — the body moved five times in two days, and this number is the only statement of whether the audit still applies to what is on the page.

**The tree audited:** `main` at **`0ec5a99`** (*"design(#447): accessible 1974 retrofuture UI prototype and expanded-scope audit (#491)"*, 2026-10-15). Every figure below was measured there, and every command in the last section was re-run green after this branch was rebased onto `e91bcae` — whose only change is `ISSUE_482_ACCEPTANCE.md`, so no file this audit reads moved.

**One correction to Addendum 1.** It named **PR #457** (`pilgrim-spec-447-v3`) as the delivery of the four added sections. **#457 was closed unmerged**; the same content landed as **PR #459** (`eb517ae4`), which also carried the rulebook's 1974 reference shelf. #457 is not the provenance. #459 is.

### The four added sections, and where each one is

| Added section | On `main` |
| --- | --- |
| *A 1974 film that accurately predicts 2026* — the maxim, and the rare/short/non-cascading timeline-slip rule | spec **§1**, **§1.1**; the rulebook states the same rule at **§1.4** (*"presentation is not canon"*) |
| *Visual art direction for later game graphics and UI* — Mœbius and *Valérian et Laureline*, the visual vocabulary, six graphics concepts, the production constraints | spec **§2.1–§2.6**; `RULEBOOK.md` **§35.9** (new) with *Zardoz* held at **#1** in **§35.4** |
| *Writing style* — period voice, the *"Pilgrim, 1974 edition"* / *"Editorial / Simulation note, 2026"* convention, sound direction | spec **§3.1–§3.3**, **§3.5**, **§3.6**, **§3.7**; `RULEBOOK.md` **§1.4**, **§35.8** |
| *1970s state of the art* — six period sources with dates, and the pre/post-1974 chronology that separates what Pilgrim could have read from later commentary | spec **§7**; `RULEBOOK.md` **§35.10** (new) |

### The prototype criterion was the one with no artefact. It has two, and the spec contradicted them

The check *"Prototype an accessible indie-friendly illustrated UI/event card and one punch-card LLM scene, with accurate underlying simulation"* was the **only** criterion whose stated position was *"not built"*. It is met twice over. Both artefacts are offline, dependency-free, keyboard-operable files on `main`:

- `strategy_game/render/retro_1974.html` (55 lines, **PR #454**) with `strategy_game/docs/INDIE_RETRO_ART_DIRECTION.md`;
- `docs/design/ISSUE_447_RETRO_UI_PROTOTYPE.html` (39 lines, **PR #491**) with the art-bible and acceptance note `docs/design/ISSUE_447_PROTOTYPE_AND_AUDIT.md` (28 lines).

**Two documents described this one row and only one of them was right.** The specification's **§10** still read *"specified, **not built**; … no art bible exists yet"*, and its sound row cited **§3.5** — the *VALIS* naming-anachronism section — where sound is **§3.7**, stale since #459 inserted §3.4/§3.5 and renumbered the writing sections. Both rows are superseded in place in this round, under a dated note recording why. **The specification and the tree now agree**, which is the state this issue has repeatedly failed to reach.

### What remains — and it is not agent work

| Remainder | Why it stays open |
| --- | --- |
| Tommy Pilgrim's **prologue text** | the standing project rule: the narrative text is the author's to write and an agent's to read. The convention, its position (`RULEBOOK.md` §1.4) and the *VALIS* anachronism marking (spec §3.5) are specified; the prose is not written, and an agent must not write it |
| **Which rulebook owns** §1.4 and §2.2 | author decision — carried as queue row **D25** |
| Whether ***The Iron Dream*** joins the locked in-universe hierarchy | author decision — carried as queue row **D26** |
| **Event Card mechanics** — taxonomy, deck size, probabilities, draw cadence, triggers, effects | deferred by this issue's own instruction (*"we decide the details later"*), not by omission |
| The **reading-list checkboxes** | the *advance reading and source list for Tomi* is the author's reading, not an agent deliverable, and the brief keeps it out of Pilgrim's 1974 library on purpose |
| **Editorial acceptance** of the artefacts above | the author's |

### One contradiction in the body, named rather than resolved

Two sections of this issue give **opposite instructions about the same bibliography**. *Advance reading and source list for Tomi* declares itself out-of-universe and requires that it stay separate from Pilgrim's biography — the reading that has governed so far, and the spec's **§9** non-goals repeat it. *Additional sources and inspirations*, added later, is headed *"(out-of-universe; **add to rulebook sources list**)"*.

The works that became **influences** are in `RULEBOOK.md` §35 (**§35.3** fiction, **§35.4** film, **§35.9** graphic, **§35.10** period shelf), and the contemporary shelf the author named on 2026-10-15 is recorded **out-of-universe in the specification**. The **to-read / to-re-read** entries — Bester, Zelazny, Brunner, Miéville, Silverberg, Pohl and Kornbluth, *Bug Jack Barron* — are in neither, and **this round did not add them**: §35.3 admits fiction *"when it materially shapes NoöPunk's tone, society, technology, or cosmology"* and §35.7 admits a work when a decision *"begins relying on"* it — a to-read list is neither yet. Flagged, not resolved. It is a question for the author and it gates no criterion.

### What this addendum does not claim

- **No rule, mechanic, statistic, number, canon, chronology or scenario fact** — and **no `strategy_game/` code or data**. The artefacts behind it are documentation.
- **No automated test** ([#271](https://github.com/TomiToivio/NooPunk/issues/271)): documents in this repository are reviewed editorially and by playtesting, and no gate was added for any of this.
- **It does not close the issue.** Addendum 1's condition is now satisfied, but the remainder in the table above is the author's. A close labelled *completed* would have to call an unwritten prologue and two open decisions met — the exact failure that got the previous close reversed.
- **Superseded rows are counted, not hidden.** Two rows of the specification's §10 changed, both because they had become false. No prose was deleted, and no other file was rewritten.

### The verification behind it

Run on a fresh clone of `main` at `0ec5a99`, using the repository's own canonical commands:

```bash
python3 tools/split_rulebook_twelve.py --check          # rc 0 — 64 headings -> 12 parts; RULEBOOK.md untouched
python3 -m unittest discover -s tests -p "test_*.py"    # Ran 531 tests ... OK
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # Ran 1262 tests ... OK
python3 -m strategy_game | python3 -c "import json,sys; d=json.load(sys.stdin); assert set(d)=={'schema_version','locations','network_nodes','network_edges','assets'}"
python3 scripts/noopunk_text.py --help
printf 'quit\n' | python3 scripts/noopunk_text.py --scenario issue74
python3 scripts/concordia_smoke.py
python3 scripts/concordia_smoke.py --build-concordia-config
```

The strategy suite reads **1262**, up from the 1166 recorded in the first half of this record: the growth is sibling merges landing under this issue, and re-running green on that newer `main` is the evidence that the artefacts survived them.

**Two documents now describe this issue's position.** `ISSUE_447_PROTOTYPE_AND_AUDIT.md` (§491) is an editorial acceptance note; this addendum is the criterion map. They agree, and they will drift apart if either is edited without the other — the reason the map is here, in the record whose job it is.
