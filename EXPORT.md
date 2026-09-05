# Noöpunk public export — operating manual for Ai (愛) and Tomi

`noopunk/public/` is the ONLY folder in this subproject that ever gets
published to the public GitHub repo. Tomi publishes manually.

## Rules

1. Everything in `public/` is public the moment Tomi pushes it. No private
   notes, no agent scratch, no internal paths to the wider repo.
2. Rebuild `public/` ONLY when Tomi asks ("export for publication" / "päivitä
   public"). Never preemptively.
3. `BOOK.md` = the 2004 edition text from `books/noopunk.md` + the 2026
   edition material. `RULEBOOK.md` = the RPG rules (from the 2004 edition,
   aligned with the ubiquitous_maniacs RULEBOOK where they disagree the
   Mandela-edition frame applies: both are true, contradictions are
   features).
4. After every export: verify byte-identity of copied files (md5), update
   `EXPORT.md` ledger at the bottom, commit to the LaclauGPT branch of the
   PCM root repo with Tomi's git identity. Tomi pushes manually.
5. Public repo name reservation: `Noöpunk` / `Noopunk` / `noopunk` — Tomi
   decides the final repo name; keep folder name ASCII-safe (`noopunk`).

## Current export (2026-09-05)

| file | source | md5 |
|---|---|---|
| README.md | hand-written for public | 76f6107b482745bc024d2e26d42807fb |
| BOOK.md | books/noopunk.md verbatim + 2026 edition (Ubiquitous Maniacs précis) | daa1ed6cb3216577db5741f55cf47980 |
| RULEBOOK.md | 2026 edition rules — English translation of ubiquitous_maniacs/RULEBOOK.md v0.1 | e8f16c7300374fbb1e386e0f383f1c25 |
| LICENSE | PCM root LICENSE (CC0 1.0) | 473a7959b44c2f42c375d904305b6307 |

Ledger updates append below.