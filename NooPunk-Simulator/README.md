# NoöPunk Simulator

> **This is the game now (#1310).** The deliverable is a small, complete **detective interactive-fiction
> adventure** about Etsivä Harri Romppainen investigating political extremists radicalized by the paradigm
> shifts — scenes, dialogue, clues, choices, consequences, save/load, an inspectable notebook. Any faction
> or hacking simulation is **optional and skippable**, never a runtime dependency of the story.
> **`Paper/` is Tomi-only and agent READ-ONLY.** See [../docs/architecture/PIVOT_1310_DETECTIVE_IF.md](../docs/architecture/PIVOT_1310_DETECTIVE_IF.md).

The social-science track: a **LaclauGPT-informed** simulation of actors, institutions, discourse and
social processes, using the project's shared Tag/Graph model.

> **Methodological attribution.** The Phase 1 paper
> ([`LaclauGPT/paper/PHASE_1_PAPER.md`](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md))
> is the reference. Its theoretical and methodological commitments are preserved; this simulator does
> not claim Phase 1 already supplies a complete simulation engine.

## Independence

- Runs and is tested **without** CWN character sheets and without the Story runtime.
- Shares the Tag/Graph contract, not the RPG's rules.
- Uses existing LaclauGPT code and ideas where appropriate; does not redesign that pipeline.

## Status

P0 skeleton of the directory; **the simulator itself is already on `main`** — it is just not here yet.
`src/social_sim/` carries `kernel.py` (WP1: actors, organizations, typed social/communication ties,
events, seeded rules, snapshots and replay) and `ai26.py` (WP2: the read-only canonical-record adapter),
with `docs/simulator/` and 66 tests. Nothing in it imports CWN, Evennia or the Story runtime, which is
what "independent" means here.

The next work is #1286's WP3–WP7 (behavioural assumptions, paired experiment, exports and metrics,
end-to-end demonstration, integration seam), done **in place**. Stage P3/P4 moves the package into this
directory behind a `social_sim` compatibility package so an existing `from social_sim.kernel import …`
keeps working.
