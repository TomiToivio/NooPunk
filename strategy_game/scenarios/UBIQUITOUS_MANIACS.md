# Ubiquitous Maniacs: current-engine scenario

An original two-day UFAB clinic investigation adapted from the author's historical Ubiquitous Maniacs project. A test participant encounters inconsistent records, a psychotronic trial and a dream simulation. This is a compact playable narrative scenario seed, **not** a full port of the legacy campaign, character arcs, social graph or hacking minigame.

Run from repository root:

```sh
python -m strategy_game.scenarios.ubiquitous_maniacs
python -m unittest strategy_game.tests.test_ubiquitous_maniacs
```

The module uses the current `Character`, six individual RPG skills, `Action.OVERCOME` and `scene.check`. Choices are narrative transitions; optional seeded Fate checks are nonblocking and replay-verified when loading a save. A full session can be serialized through `to_dict()` / `from_dict()`.

## Copyright and source hygiene

This new adapter includes only newly written scenario prose and the author's original UFAB/Romppainen premise. **No original legacy tree is included.** In particular, the legacy `references/maniac_transcripts` directory contains television scripts and must never be copied to main or into release artifacts. No dialogue, character names, episode scenes, brand names, artwork, music or episode transcripts from *Maniac*, *Riget*, *Paprika* or other source works are used in this scenario. Mentioning external titles here is attribution of inspiration, not permission to redistribute them.

The earlier branch `import/ubiquitous-maniacs-legacy` remains separate and contains uncleared material. Do **not merge that branch**, even after deleting files, because ordinary merges preserve history. Any future salvage should use fresh, individually reviewed additions on branches based on `main`. A legal/human review is still required for a public release; this technical cleanup cannot prove absence of all infringement.
