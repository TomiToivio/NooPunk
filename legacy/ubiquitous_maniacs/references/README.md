# references/ — deliberately not imported

The source tree (`Panpsychic-Cyborg-Multitude` @ `LaclauGPT` → `noopunk/ubiquitous_maniacs/`)
carried a `references/` directory. **It was not imported into this repository**, by the author's
ruling of 2026-10-22.

## Why

`references/maniac_transcripts/` held material derived from the Netflix miniseries *Maniac* (2018,
directed by Cary Joji Fukunaga) and the Swedish series *Riget*, together with a `README.md` that
records where the transcripts came from:

> Source: Springfield Springfield (springfieldspringfield.co.uk)

That is third-party copyrighted script and dialogue with **no licence grant of any kind**. Copying
it into a public repository would redistribute it, so it is excluded.

## What was excluded

All 13 files of `references/maniac_transcripts/`:

- `README.md` — the transcript set's own front matter, naming the source site
- `STYLISTIC_ANALYSIS.md` — the author's analysis of the series' style
- `riget_wikipedia_episodes.txt` — an episode guide for *Riget*
- `s01e01_the_chosen_one.txt` … `s01e10_option_c.txt` — the ten episode transcripts

### Why the analysis file went with them

`STYLISTIC_ANALYSIS.md` is the author's own writing *about* the series, and it would have been
reasonable to keep it as the one clearly-authored piece. On reading it, though, it turns out to
**quote the script extensively**: 74 spans of 25 characters or more of quoted dialogue, including
signature lines, with the characters discussed by name throughout.

The author's own analysis of a third party's work is the author's work. But a document that
interleaves that analysis with the third party's words is no longer cleanly separable from the
expression it quotes — and the point of the exclusion is that the expression does not travel.
Keeping the file would have meant making a judgement call about how much quoted dialogue is
acceptable, which is exactly the judgement the exclusion avoids.

So it is excluded with the rest. If the style analysis is wanted later, the honest route is to
write a new one that describes the techniques without quoting — which is a piece of original work,
not an import, and would belong in the RPG's own documentation rather than in a provenance tree.

## The record

The full import record, with the source repository, branch, path, CC0-1.0 licence basis and the
provenance of the import itself, is `docs/import/UBIQUITOUS_MANIACS_LEGACY_IMPORT.md`.
