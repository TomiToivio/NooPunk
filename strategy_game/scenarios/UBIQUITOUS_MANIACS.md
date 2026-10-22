# Ubiquitous Maniacs in the shared NoöPunk RPG

The supported play entrypoint is now the **same RPG package** as other NoöPunk demonstrations:

```sh
python -m strategy_game.rpg --scenario ubiquitous-maniacs
python -m strategy_game.rpg --scenario ubiquitous-maniacs --new --save my_case.json
python -m unittest strategy_game.tests.test_unified_ubiquitous_maniacs
```

Choose a displayed option, or use `check romppainen SAV 1 42` to request a seeded, optional Fate check. The game saves after each valid action and on quit/EOF. Reopen the same command to resume. The current Fate resolver, character sheets and six-skill vocabulary are shared with the engine, not copied into the scenario.

The two-day scenario is a minimal integrated slice. The historical project included richer psychotronic, relationship and cyber subsystems which remain outside the active engine until separately adapted and tested; the old engine is **not** invoked.

## Copyright hygiene and remaining release decisions

The original works that inspired the setting are credited as inspirations only. The imported transcript collection is not shipped. Transcript-derived style analysis, which directly quotes protected dialogue and branded fiction, is removed from both duplicate historical trees. Original design commentary may be retained but must not be described as legally cleared without human review.

**Git history remains a separate cleanup issue.** Ordinary Git commits cannot erase past blobs, and deleting historic material from HEAD is not history sanitization. To purge published historical refs, coordinate a repository-wide history rewrite, review PR/branch refs and caches, force-push a rewritten root and inform collaborators to reclone. The GitHub connector here does not provide a complete safe GitHub history purge operation. No code licence or original-content licence is selected by this change.
