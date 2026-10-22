# Import record: the Ubiquitous Maniacs legacy tree

**What this is.** The `legacy/ubiquitous_maniacs/` tree in this repository was imported from
Tomi's own working material, held in the
[Panpsychic Cyborg Multitude](https://github.com/TomiToivio/Panpsychic-Cyborg-Multitude) repository
on the `LaclauGPT` branch, at `noopunk/ubiquitous_maniacs/`.

**Provenance.**

| | |
| --- | --- |
| Source repository | `github.com/TomiToivio/Panpsychic-Cyborg-Multitude` |
| Source branch | `LaclauGPT` |
| Source path | `noopunk/ubiquitous_maniacs/` |
| Import branch | `import/ubiquitous-maniacs-legacy` |
| Imported by | the agent, on the author's order of 2026-10-22 |
| Source licence | **CC0-1.0** (the source repository's `LICENSE`, read directly; the GitHub licence API also reports `CC0-1.0`) |
| Files imported | 280 |

**Licence basis.** The source is the author's own work, published under CC0-1.0 — a public-domain
dedication with no attribution obligation and no ShareAlike, so the import imposes no obligation
on this repository or on anything derived from it. The imported tree therefore does **not** alter
the licence position of NoöPunk, and it does not change the open author decision on the
project's own licence (row **D10** in `docs/design/AUTHOR_DECISION_QUEUE.md`).

## What was excluded, and why

**`references/maniac_transcripts/` — 13 files, not imported.**

This directory held full dialogue transcripts of the Netflix miniseries *Maniac* (2018, directed by
Cary Joji Fukunaga), an episode guide for the Swedish series *Riget*, and an analysis of the
series' style, taken from the fan transcript site `springfieldspringfield.co.uk` as the source's
own `README.md` records.

That material is **not the author's**: it is a third party's copyrighted script and dialogue, with
no licence grant of any kind. Importing it into a public repository would redistribute it. The
author ruled on 2026-10-22 that it is excluded.

`STYLISTIC_ANALYSIS.md` went with the transcripts rather than being kept as the one clearly
authored piece: on reading it, it **quotes the script extensively** — 74 spans of 25 characters or
more of quoted dialogue, signature lines included, with the characters discussed by name
throughout — so it is not cleanly separable from the expression it quotes.

`legacy/ubiquitous_maniacs/references/README.md` records this exclusion and its reason in place,
so a reader finds the explanation rather than a missing directory.

## What the imported tree is, in the repository's own terms

The tree is **legacy material**, and it is placed under `legacy/` for that reason. It is not the
current rules of this repository and it does not override them:

- the current legacy RPG rules live in `RULEBOOK.md` and `rulebook/`;
- the active crossover game lives in `strategy_game/`, whose own `strategy_game/RULEBOOK.md` still
  reads **NO RULES APPROVED**;
- the imported tree's own `RULEBOOK.md` is the **4dF "Ubiquitous Maniacs" rulebook v0.1** (in
  Finnish), which the project's own canon record calls a *Mandela edition*: it is one of the
  contradictory versions, and both it and the newer text are load-bearing rather than one of them
  being false.

The imported `RULEBOOK.md` is **byte-identical** to the `SÄÄNNÖT.md` that this repository carried
before the September 2026 reset (commit `615805e`, "Wikikirja", md5 `09e4b7dd9a44270c1f18035fe4b02069`).
It is therefore a restoration of material this project already published once, not a new import.

**The rules do not carry over.** Per `AGENTS.md` and the crossover's own boundaries, legacy
attributes, skill procedures, character sheets and gameplay are not canonical for the active
game, and importing a mechanic needs an explicitly approved conversion decision. The 4dF
material is here as *material*, not as a rule set that overrides the current one.

## The imported tree is incomplete, and that is a property of the source

**This matters for anyone who tries to run it.** The source tree's code reads a `data/` directory
that was **never committed to the source repository**:

```
data/rpg/characters/romppainen_day_1.md
data/rpg/characters/romppainen_narkkari.md
data/rpg/scenarios/day_1_arrival_and_entanglement.json
data/rpg/scenarios/day_2_kiimaiset_poliisit.json
data/rpg/scenarios/day_1.json
data/rpg/characters/demo_operator.md
data/rpg/tarot_deck.json
data/rpg/psi_tables.json
data/rpg/factions/nhi_factions.json
data/hacking/demo_target.json
data/social_simulation/demo.json
data/rpg/campaigns/helsinki/characters/…
```

Every one of these was checked against **all fifteen branches** of the source repository and
against **the full history of this repository**: none of them was ever committed anywhere. The
gap is in the source, not in the import.

Measured, running the imported suite in an isolated environment (Python 3.11, the tree's own
`requirements.txt` plus `pydantic`, which the tree's `requirements.txt` also omits):

```
191 passed, 254 failed
```

**248 of the 254 failures are a missing data file**, and the remaining 6 are the same cause seen
downstream: assertions over empty sets that would be populated by the absent data. There is no
second cause in the failures.

The tree is therefore imported **as it is** — a code-and-prose archive that is missing its data
directory. It is not a working game in this repository, and it is not presented as one.

### Running it

The imported tests are pytest-style and import `from src.rpg import ...`, so they resolve the
imported packages only when pytest is invoked **from inside** `legacy/ubiquitous_maniacs/`, and
they need Python 3.11+ (the source uses `enum.StrEnum`) and the tree's own dependencies. They
were left as they were rather than converted: this is legacy material, not a second test suite
for the current game.

**They are outside this repository's CI.** The workflow runs `unittest discover -s tests` and
`unittest discover -s strategy_game/tests`; neither recurses into `legacy/`, so these files do
not enter the CI run and cannot redden it. Verified with the imported tree in place: root discovery
still finds **598** tests.

## Provenance of the import itself

The import was carried out in batches, each batch a separate commit, so the history of the import
is legible file-range by file-range. The first 221 files were imported in an earlier session; the
remaining 59, the exclusion and this record were added in this one.

**One correction made during the import.** The first pass of the import copied the
`references/maniac_transcripts/` directory along with everything else. The author ruled that this
material must not be imported, and the transcripts were removed in their own commit with the
exclusion recorded in this file. The removal is a `git rm` in the branch's history, so the fact
that the files were briefly present is itself visible — deliberately, because a silent rewrite of
history would hide it.

## Related

- `docs/ATTRIBUTION_POLICY.md` — how attribution is done in this project, and the open licence
  decisions (D10) it depends on.
- `data/sources/game_system_rights.json` — the rights ledger, the one home for the excluded-licence
  set.
- `data/licenses/release_packaging_policy.json` — the release packaging rules, and the quarantine
  that keeps NC-derived material out of a distributable build.
