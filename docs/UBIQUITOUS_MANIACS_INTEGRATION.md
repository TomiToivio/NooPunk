# Ubiquitous Maniacs in the current NoöPunk RPG

The **canonical integrated case** is *The Listening Ward*, a self-contained, optional investigation that uses the current `strategy_game.casework.CaseSession`, Fate resolution, UNSA five-seat roster, clue assembly, mission outcome writer and save/resume. It does **not** load any old Ubiquitous Maniacs engine or external copyrighted dialogue.

Run from the repository root:

```sh
python -m strategy_game.rpg --scenario ubiquitous-maniacs-case --save ward.json --new
```

Resume by leaving off `--new`. Within the prompt, use `help`, `status`, `act SEAT ACTION`, `next`, `assemble`, `resolve closed_by_evidence` (or `closed_by_withdrawal`), `save`, `quit`. The live implementation is `strategy_game/casework/ubiquitous_maniacs.py`; direct invocation of `python -m strategy_game.casework.ubiquitous_maniacs_play` is equivalent.

The older two-day narrative prototype is retained separately for compatibility at `python -m strategy_game.rpg --scenario ubiquitous-maniacs`. It shares RPG Fate checks but **is not** the canonical five-seat investigation. Do not mistake its self-contained story state for a full campaign save or merge its rules into the current engine. Existing saves from the two adapters are not interchangeable.

## Rights and provenance boundaries

- Active scenario text and investigation scenes are original adaptations of the author's project premise. References to a film, a television series, a game system, or a researcher are **inspirations/analysis**, not permission to reproduce screenplay dialogue, art, rulebook text, or game settings.
- Third-party `maniac_transcripts` directories and the quote-heavy stylistic analyses identified in the earlier cleanup were removed from current tracked paths. The repository's **Git history and other branches may still contain those objects**. A normal Git commit cannot erase history; full distribution cleanup requires an explicitly planned history rewrite of every affected ref and review of forks/caches.
- The `archive/ubiquitous-maniacs-2026-10` and `legacy/ubiquitous_maniacs` directories are **research/legacy archives**, not gameplay dependencies and not blanket-cleared for redistribution. Their remaining quotations, adaptations, images and licence attributions still require a file-by-file rights review. Do not package them as release assets by default.
- Neither the imported repository's CC0 designation nor original authorship of surrounding prose licenses third-party text embedded inside it. See `docs/ATTRIBUTION_POLICY.md` and `legacy/ubiquitous_maniacs/references/README.md`.

## Validation

```sh
python -m unittest strategy_game.tests.test_ubiquitous_maniacs_case strategy_game.tests.test_unified_ubiquitous_maniacs strategy_game.tests.test_ubiquitous_entrypoint
```

These checks test wiring and case behavior, **not copyright clearance**. Review CI before release or merging new content.
