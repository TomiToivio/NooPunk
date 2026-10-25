# Ubiquitous Maniacs in the current NoöPunk RPG

The **canonical integrated case** is *The Listening Ward*, a self-contained, optional investigation that uses the current `strategy_game.casework.CaseSession`, Fate resolution, UNSA five-seat roster, clue assembly, mission outcome writer and save/resume. It does **not** load any old Ubiquitous Maniacs engine or external copyrighted dialogue.

Run from the repository root:

```sh
python -m strategy_game.rpg --scenario ubiquitous-maniacs --save ward.json --new
```

Resume by leaving off `--new`. Within the prompt, use `help`, `status`, `act SEAT ACTION`, `next`, `assemble`, `resolve closed_by_evidence` (or `closed_by_withdrawal`), `save`, `quit`. The live implementation is `strategy_game/casework/ubiquitous_maniacs.py`; direct invocation of `python -m strategy_game.casework.ubiquitous_maniacs_play` is equivalent.

The older two-day narrative prototype is retained separately for compatibility at `python -m strategy_game.rpg --scenario ubiquitous-maniacs-legacy`. The `ubiquitous-maniacs-case` selector remains an alias for the canonical case. It shares RPG Fate checks but **is not** the canonical five-seat investigation. Do not mistake its self-contained story state for a full campaign save or merge its rules into the current engine. Existing saves from the two adapters are not interchangeable — the canonical loader refuses a legacy save by schema, rather than half-loading it.

## Scope: what this case is, and what it is not

**It is one case, not a campaign, and not the legacy story.** *The Listening Ward* is a two-scene
investigation: an arrival, a records room, three clues, one assembles-able finding, and two
endings. A single sitting finishes it.

**It is not a retelling of the historical two-day prototype.** The legacy material in
`archive/ubiquitous-maniacs-2026-10/` and `legacy/ubiquitous_maniacs/` contains a two-day
narrative with a therapy sequence, a persona-phase protagonist, a dream layer and a second day
that the canonical case does **not** cover. That story remains reachable only through the
separate `ubiquitous-maniacs-legacy` selector and the archived corpus. Nothing in this case
promises to cover it.

Whether the legacy beats should become *stages* of the canonical scenario is an open design
question, not a completed one. What was taken from the corpus is its **premise** — treatment
traded for access to memory — and its mechanics (below). What was not taken is its plot.

The case is **non-canonical**: an optional side case, labelled as such in its own `detail` record
(`"OPTIONAL SCENARIO, NOT CANON"`). It uses the canonical frame — the 2045 campaign present, the
UNSA Helsinki Field Office, the post-Crisis network — and adds no institution, no character and
no world fact to canon.

## Requirements

**Python 3.12** is the tested version (CI), and **3.11 is the minimum**: the rules layer uses
`enum.StrEnum` and `datetime.UTC`, both added in 3.11.

**No third-party package is needed to play.** The scenario imports only the Python standard
library. Verified by running it with site-packages disabled:

```sh
python3.11 -S -m strategy_game.rpg --scenario ubiquitous-maniacs --save ward.json --new
```

`requirements.txt` installs `gdm-concordia` from a pinned git revision, which is the **optional**
Concordia and Ollama runtime. It is not required by this case; `requirements-concordia.txt`
carries the same pin for the optional path.

## Troubleshooting

| symptom | cause | remedy |
| --- | --- | --- |
| `Ubiquitous Maniacs / NoöPunk RPG needs Python 3.11 or newer` (exit 2) | an older interpreter | install 3.11+ and run with it; the message names the commands. Before the gate existed this was a bare `ImportError: cannot import name 'StrEnum'` from inside the rules layer, which named neither the interpreter nor a remedy. |
| `cannot resume saved case: … is not valid JSON` (exit 2) | a corrupt or truncated save | start a new case with `--new`, or delete the save file |
| `cannot resume saved case: unsupported session schema_version …` (exit 2) | a save from the legacy adapter, or a schema this build does not know | the two adapters are not interchangeable; play with the adapter that wrote the save, or start fresh |
| `Cannot do that: … has already acted this scene` | Fate's one-action-per-character-per-scene rule | use another seat, or `next` to open a new scene |
| `Cannot do that: this is the last scene; close the case with resolve(...)` | `next` at the end of the case | close it with `resolve closed_by_evidence` or `resolve closed_by_withdrawal` |

Errors are printed as one line beginning `Cannot do that:` and the prompt continues; the process
does not raise. A save or load failure exits **2** and prints to stderr.

## Validation

```sh
python -m unittest strategy_game.tests.test_ubiquitous_maniacs_case strategy_game.tests.test_unified_ubiquitous_maniacs strategy_game.tests.test_ubiquitous_entrypoint
python -m unittest strategy_game.tests.test_ubiquitous_maniacs_mechanics strategy_game.tests.test_rpg_corpus_ports
```

**End-to-end CLI smoke tests** drive the real command in a subprocess, exactly as a player does:

```sh
python -m unittest strategy_game.tests.test_ubiquitous_maniacs_e2e -v
```

They cover a full playthrough to each of the two endings, determinism across two runs of the same
route and seed (and that a different seed changes the dice), save/resume at the beginning,
mid-case and after resolution, a corrupt save, a save from the other adapter, and every invalid
input a player is likely to type. The suite prints the interpreter it verified against.

Observed, on Python 3.11.14 / Linux:

```
Ran 18 tests ... OK
  e2e verified on Python 3.11.14 (linux)
```

The full strategy suite ran **1772 tests OK** and the repository root suite **600 tests OK** on the
same interpreter, with `python tools/audit_corpus_expression.py --check` reporting
`clean: no third-party expression in 284 archived file(s)`.

These checks test wiring and case behaviour, **not copyright clearance**. Review CI before
release or merging new content.

## Rights and provenance boundaries

- Active scenario text and investigation scenes are original adaptations of the author's project premise. References to a film, a television series, a game system, or a researcher are **inspirations/analysis**, not permission to reproduce screenplay dialogue, art, rulebook text, or game settings.
- Third-party `maniac_transcripts` directories and the quote-heavy stylistic analyses identified in the earlier cleanup were removed from current tracked paths. The repository's **Git history and other branches may still contain those objects**. A normal Git commit cannot erase history; full distribution cleanup requires an explicitly planned history rewrite of every affected ref and review of forks/caches.
- The `archive/ubiquitous-maniacs-2026-10` and `legacy/ubiquitous_maniacs` directories are **research/legacy archives**, not gameplay dependencies and not blanket-cleared for redistribution. Their remaining quotations, adaptations, images and licence attributions still require a file-by-file rights review. Do not package them as release assets by default.
- Neither the imported repository's CC0 designation nor original authorship of surrounding prose licenses third-party text embedded inside it. See `docs/ATTRIBUTION_POLICY.md` and `legacy/ubiquitous_maniacs/references/README.md`.

## The corpus's mechanics, ported into the live engine

The corpus carried a body of **authorial mechanics** written against its own Fate kernel: PSI
as trajectory steering, psyche projection and what it costs, and consent-gated psychosurgery.
Leaving them in the legacy tree would have left two RPGs in one repository, so three modules
were ported onto this repository's engine:

| legacy module | live module | what the port changed |
| --- | --- | --- |
| `src/rpg/astral.py` | `strategy_game/rpg/projection.py` | English, the module's home, and the vocabulary it borrows. The state machine, the costs and the thresholds are unchanged. |
| `src/rpg/psychosurgery.py` | `strategy_game/rpg/psychosurgery.py` | English, and the live `Character` sheet instead of the corpus's own model. The **consent gate** is unchanged and still refuses every write while permitting every read. |
| `src/rpg/psi.py` | `strategy_game/rpg/psi.py` | English, the engine's **six** individual skills instead of the corpus's seven attributes, the engine's one Fate resolver instead of a second kernel, capability gates on the engine's existing tag vocabulary, and the escalation tables baked in because the corpus's JSON was never committed upstream. |

`strategy_game/casework/ward_mechanics.py` binds them to the *Listening Ward*: the patient's
session with the consent gate closed, the two witnesses who each saw a different person in the
chair, and the ward's PSI context.

**The corpus's seven-attribute skill system and its *Transhumanity's Fate* skill names were not
ported.** This repository's rulebook records that work's skill list as **names only**, for
cross-reference, and `strategy_game/docs/SKILL_LAYERS_AND_DECISIONS.md` is explicit that the
list is not imported as prose or as an operative system. A port that carried the corpus's list
into the live tree would have reintroduced exactly what the repository has already decided
against — in *code* rather than in a note, which is much harder to notice and to undo.

## Copyright audit

The archive's wording is checked by a **tool**, not by a test:

```sh
python3 tools/audit_corpus_expression.py --check
```

It scans the legacy and archive trees for reproduced dialogue, for the source's own devices
used as the corpus's own, for real performers named as character blueprints, and for the
source's episode titles. It exits non-zero when it finds anything.

It is deliberately **not** wired into CI, and it deliberately does not live under `tests/`.
`AGENTS.md`'s "Automated tests policy: executable code only" excludes automated assertions for
*scenario prose, wording and lore* from the test suite, because the author reviews that
material editorially and through tabletop playtesting rather than as a code contract. Checking
the wording of archived prose is exactly that category. The *licensing* assertions are a
separate matter and stay where the repository already keeps them, in
`strategy_game/tests/test_rpg_boundary.py`, which asserts on an attribution record rather than
on creative prose. The corpus's **code** is tested normally, against executable objects.

The audit's exemptions are deliberate and narrow. The provenance records (`MANIFEST.md`,
`manifest.json`, `MIGRATION_MAP.md`) may name the files that were removed, because a removal
that cannot be audited is not a removal. The influence-analysis documents may name the source's
devices, because naming an influence is not reproducing one. What may not survive is the
source's **words**, and a real performer's name as a **blueprint**.

## Distribution boundary

The archive and legacy trees remain in repository history and the source checkout for research, but are quarantined from public release bundles by `data/licenses/release_packaging_policy.json`. They are not dependencies of the canonical case. This is **not** certification of the entire repository as copyright-cleared; exclude unreviewed historical sources and check the selected release bundle. Removing a file in a new commit does not erase prior Git objects.
