# Ubiquitous Maniacs: playable adaptation and copyright review

This is an **optional 2045 Helsinki side scenario**, not a replacement for the
NoöPunk crossover's pre-Crisis starting campaign and not a canon-setting decision.

## Play the unified scenario

From the repository root:

```sh
python -m strategy_game.casework.ubiquitous_maniacs_play --new
python -m strategy_game.casework.ubiquitous_maniacs_play  # resumes a save
python -m unittest strategy_game.tests.test_ubiquitous_maniacs_case
```

The playable scenario is `strategy_game/casework/ubiquitous_maniacs.py`. It
reuses `CaseFile`, `CaseSession`, current Fate checks, the five-seat UNSA party,
clue-chain assembly, the campaign outcome writer and serialization. It does **not**
load or import the older `archive/` or `legacy/` Python packages and does not
invent a second RPG rules implementation.

The story retains broad **author-owned ideas** from the earlier corpus: an
institutional therapy/research setting, sixteen contradictory records, contested
patient identity, uncertain psychotronic/PSI phenomena, and the possibility of
organizational misconduct. The concrete incident, original narrative text,
dialogue and resolution are newly written for NoöPunk. Historical names such as
UFAB are *legacy inspiration*, not automatically promoted to 2045 canon.

## Rights and provenance

Inspected the current `main` Git tree on 2026-10-22. The formerly identified
`references/maniac_transcripts` screenplay-transcript files are **not present**
in either imported tree under `legacy/ubiquitous_maniacs/` or
`archive/ubiquitous-maniacs-2026-10/`. The original source repository
contains third-party `Maniac` television dialogue transcripts and other
reference material; **do not copy these into the playable scenario**.

Previous import documents are inconsistent: the `docs/import/` record says
all 13 transcript/reference files were excluded, while the historical archive's
`MIGRATION_MAP.md` describes eight retained summaries. Those statements are
historical provenance claims, not proof that the current repository contains the
files; the current tracked-tree inventory above is the release-time check.

This adaptation contains no television script, episode dialogue, copyrighted
game-system prose or assets transplanted from those works. Mentioning a work
as an influence is not the same as copying its expression. Names, ideas and
genre tropes require a case-by-case review where trademark, contractual or
substantial-similarity questions arise.

**Limits:** This is a targeted provenance and scenario-content cleanup, not
a legal certification that every sentence in the entire repository, including
all archival research notes, is cleared. An exhaustive quotation audit of the
large archive remains an editorial review task. Deleting a file in a new commit
would not erase it from Git history or forks; requests for historic purging
require separate coordination and verification.

## Implementation boundaries

- Current runtime: `strategy_game/casework/` only.
- Current default case `kallio.py`: unchanged.
- Legacy `archive/` and `legacy/`: preserved as reference, not runtime.
- Current campaign party, Fate kernel, evidence and outcomes: reused.
- No promotion of legacy UFAB/Ragnarök AI, competing chronology or old 4dF
  procedures into active canon.
- Runtime tests: `strategy_game/tests/test_ubiquitous_maniacs_case.py`.
