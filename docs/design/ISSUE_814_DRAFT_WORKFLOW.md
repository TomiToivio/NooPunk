# Draft workflow for #814 (Tomi-led rules → tabletop + Godot)

Permanent process note for meta-issue **#814**. That issue stays open: it is an index and a
contract, not a checklist. Each Tomi draft becomes **one child issue**, and the child closes —
never the meta-issue.

## The pipeline

```
Tomi's draft (linked in a child issue)
   ├─ tabletop:  RULEBOOK.md → regenerate parts + manifest → review
   └─ Godot:     data/rules/*.json → core procedures → tests → UI/scenario
                            ↓
              parity evidence + open questions recorded → PR → link back to #814
```

### 1. Intake (child issue)

Use the **NoöPunk rule draft** issue form (`.github/ISSUE_TEMPLATE/noopunk-draft.yml`). It asks
for the one thing an implementer cannot invent: the draft itself, its scope, and the questions
it leaves open. One section or one scenario per child issue.

Rules of intake:

- Quote Tomi's draft; do not paraphrase decisions into place.
- Anything the draft does not settle is an **open question**, never a silent design choice.
- If the draft conflicts with the CWN/SWN baseline, record the conflict and ask; do not
  "correct" the author.
- Never widen the scope because a neighbouring section looks easy.

### 2. Tabletop form

`RULEBOOK.md` is canonical. The numbered chapters under `rulebook/parts/` are **generated** from
it, so edit `RULEBOOK.md` and then regenerate:

```sh
python tools/split_rulebook_twelve.py
```

That rewrites `rulebook/parts/` and the frozen manifest `data/rules/rulebook_split_manifest.json`.
Commit the canonical text, the regenerated parts and the manifest together; never hand-edit a
part.

Tabletop text must cite its CWN/SWN source section and mark NoöPunk departures explicitly. Do
not reproduce non-open rulebook prose; implement procedures and cite the open SRD.

### 3. Godot form

The computer game reads mechanics from data, not from prose or duplicated constants:

| Layer | Location |
|---|---|
| numeric rules and catalogues | `data/rules/*.json` (each file carries its `_source` URLs) |
| procedures | `godot/core/*.gd` (`rules_adapter`, `cwn_catalogue`, `combat`, `hacking`) |
| scenario content | `godot/scenarios/**`, `data/scenarios/**` |
| tests | `godot/tests/test_*.gd`, run by `godot/tests/run_tests.gd` |

An adaptation adds its numbers **once** in `data/rules/noopunk_adaptations.json` (or a sibling
data file) and the procedure reads them. The tabletop chapter quotes the same numbers. A number
that appears in two places is a parity bug.

### 4. Parity evidence

Parity is demonstrated by executable behaviour, not by comparing sentences:

- a Godot headless test that exercises the rule (see `AGENTS.md`: tests for executable code only);
- a tabletop example that walks the same case with the same numbers;
- both linked from the child issue.

Do **not** add tests that read Markdown, assert prose or freeze a rulebook section. Editorial
review and playtesting are the tabletop gate.

### 5. Deliberate differences

Platform differences are allowed and must be written down: real-time UI pacing, simplified
bookkeeping, content not yet built in 3D. Record them in the child issue under
"Tabletop ↔ Godot differences", with the reason.

### 6. Definition of done (child issue)

- [ ] Draft linked; scope restated in one sentence.
- [ ] `RULEBOOK.md` updated and parts + manifest regenerated in the same commit.
- [ ] Godot data/procedure/UI updated where the draft reaches the computer RPG.
- [ ] Executable parity test added or updated; suite green.
- [ ] Open questions and deliberate differences listed for Tomi.
- [ ] PR linked here; child issue closed only after merge.

## Current state (so the next draft starts from the truth)

- **No adaptations are approved yet.** `data/rules/noopunk_adaptations.json` exists with an empty
  `adaptations` list and `_status: none_approved`; the CWN baseline (`data/rules/wn_core.json`,
  `cwn_catalogue.json`) is the only ratified mechanics.
- The Godot slice implements the CWN core procedures; the coverage matrix is
  `docs/rules/CWN_GODOT_COVERAGE.md`.
- The strategy game is a separate game with **no approved rules**; do not route an RPG draft into
  `strategy_game/` and do not route a strategy draft into `RULEBOOK.md`.

## Readiness check — verified 2026-10-30

The pipeline was exercised before inviting drafts into it, because a workflow whose first step is
broken wastes the author's time.

| Check | Result |
| --- | --- |
| `python tools/split_rulebook_twelve.py --apply` | runs; **idempotent** (a second run changes nothing) |
| Generated parts vs `RULEBOOK.md` | **were drifted, now regenerated.** Three parts had been hand-edited; the canonical text is the rulebook and the parts are output |
| `data/rules/noopunk_adaptations.json` | present, `_status: none_approved`, `adaptations: []` |
| `docs/rules/CWN_GODOT_COVERAGE.md` | present — the Godot coverage matrix to extend with each draft |
| Issue templates | `noopunk-draft.yml` parses (8 fields); `tomi_draft_child.md` present |
| Godot suite | 530 checks, 0 failed |

### What the drift taught

`rulebook/parts/` is **generated**, and three parts had been edited directly — including a full
§33.6c Noösphere section that existed nowhere in `RULEBOOK.md`. Regenerating would have deleted it,
which is how "generated" directories lose work.

The section's substance was already in canonical files (`docs/world/NOOSPHERE.md` carries the
definition and its Jung/Teilhard sourcing; `rulebook/10_SINGULARITY_CRISIS.md` carries the
*claimant, not the definition* reconciliation), and `RULEBOOK.md` links to it. So the regeneration
lost nothing — but it would have lost everything if the only copy had been the part.

**Rule for every draft:** edit `RULEBOOK.md`, regenerate, commit both. A hand-edited part is a
future deletion.

### First-draft checklist

1. Child issue from the **NoöPunk rule draft** form.
2. Draft quoted verbatim; anything it leaves open becomes an open question.
3. Tabletop: `RULEBOOK.md` → `python tools/split_rulebook_twelve.py --apply` → tabletop example.
4. Godot: numbers in `data/rules/*.json`, procedure in `godot/core/*.gd`, test in `godot/tests/`.
5. Parity: one headless test and one tabletop example walking the same numbers.
6. PR linked back to #814; close the child, never the meta-issue.
