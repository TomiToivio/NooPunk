# Ubiquitous Maniacs in the shared NoöPunk RPG

The supported play entrypoint is now the **same RPG package** as other NoöPunk demonstrations:

```sh
python -m strategy_game.rpg --scenario ubiquitous-maniacs
python -m strategy_game.rpg --scenario ubiquitous-maniacs --new --save my_case.json
python -m unittest strategy_game.tests.test_unified_ubiquitous_maniacs
python -m unittest strategy_game.tests.test_ubiquitous_maniacs_canon_anchoring
```

Choose a displayed option, or use `check romppainen SAV 1 42` to request a seeded, optional Fate check. The game saves after each valid action and on quit/EOF. Reopen the same command to resume. The current Fate resolver, character sheets and six-skill vocabulary are shared with the engine, not copied into the scenario.

## What was unified, and what it is anchored to

The Ubiquitous Maniacs corpus — the author's earlier prototype, imported as reference material
under `legacy/ubiquitous_maniacs/` and `archive/ubiquitous-maniacs-2026-10/` — describes a
two-day scenario at a clinic that trades treatment for access to memory. That scenario now plays
**on the current RPG engine**: the current Fate resolver, the current six-skill vocabulary, the
current character model. The corpus's own engine is not invoked; it is a superseded prototype kept
as a reference implementation.

The corpus predates this repository's canon and contradicts it in twelve recorded places
(`archive/ubiquitous-maniacs-2026-10/MIGRATION_MAP.md`, rows C1–C12). The scenario is built so
it does not contradict canon:

| corpus | canon | what the scenario does |
| --- | --- | --- |
| **C5** — the setting is *UFAB*, a psychiatric research complex | UFAB appears in **none** of the 57 canon rulebook files; canon has the UNSA, the Academy, Eurodef, the Supo, Ö-Mappi | the scenario is anchored to the **UNSA Helsinki Field Office**, and the clinic is a **scenario-local** contracted site beneath it — labelled as such, claiming no canon status |
| **C3** — the protagonist is *Emil* Romppainen, a Jungian psychoanalyst | canon's is *Dr. Harri S. Romppainen* ("Dirty Harry"), a veteran of Ö-Mappi — **a different man** | the scenario uses the **canon** Romppainen |
| **C4** — *Lotta Kallio* is a person | canon's *Kallio* is a **district** | the scenario uses neither name |
| **C2** — the corpus rejects fixed years on purpose | canon writes `20XX` unless the author says otherwise (`AGENTS.md` §6) | the narration carries **no year**; the `20XX` frame is metadata |
| **C1** — the corpus is post-Fall | canon is pre-Fall | the scenario never narrates the Fall |

**What the corpus contributes that the current game did not**, and is kept: the
**memory-as-currency** premise (treatment traded for access to memory) and the
**persona-phase** structure — professional detachment and compulsive appetite as two faces of
one Jungian shadow — which appears as a playable trait on the canon Romppainen, stated as a trait
rather than as a rewrite of who he is.

`strategy_game/tests/test_ubiquitous_maniacs_canon_anchoring.py` pins these mechanically: the
cast must not contain *Emil* or *Ingrid*, must not turn *Kallio* into a person, must not present
UFAB, and the narration must carry no exact future year. The test is over executable data — the
scenario's cast and scene text — and asserts nothing about whether the prose is good.

## What is still minimal

The two-day scenario is an integrated slice. The historical project included richer
psychotronic, relationship and cyber subsystems which remain outside the active engine until
separately adapted and tested; the old engine is **not** invoked.

## Copyright hygiene and remaining release decisions

The original works that inspired the setting are credited as inspirations only. The imported
transcript collection is not shipped. Transcript-derived style analysis, which directly quotes
protected dialogue and branded fiction, is removed from both duplicate historical trees.

`tests/test_third_party_expression_absent.py` fails if distinctive verbatim lines from *Maniac*
(2018) or *Riget / The Kingdom* (1994) reappear in the working tree or in a commit. It was
verified by negative control: with two such lines re-added, the guard fails and names the file.

Original design commentary may be retained but must not be described as legally cleared without
human review.

**Git history remains a separate cleanup issue.** Ordinary Git commits cannot erase past blobs, and
deleting historic material from HEAD is not history sanitization. To purge published historical
refs, coordinate a repository-wide history rewrite, review PR/branch refs and caches, force-push a
rewritten root and inform collaborators to reclone. The GitHub connector here does not provide a
complete safe GitHub history purge operation. No code licence or original-content licence is
selected by this change.
