# NoöPunk Simulator

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
## What this track is for now (#1310, 2026-11-07)

**The playable detective adventure is the deliverable.** Romppainen investigates political extremists radicalised by the
three paradigm shifts; the player explores a few Helsinki locations, interviews people, reads documents, records clues
and reaches an outcome grounded in what they established.

The LaclauGPT-derived social simulation described above is **optional infrastructure**: a possible provider of synthetic
faction state for a case, never a runtime dependency of the story and never a prerequisite for playing. Do not build a
pipeline before a case is fun.

`Paper/` remains **Tomi's, agent read-only**. `Rulebook/` belongs to the paused RPG track and is not extended here.
See [`../docs/adventure/PIVOT_1310.md`](../docs/adventure/PIVOT_1310.md) for the inventory of what already exists.
