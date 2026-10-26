# Godot detective slice (#631): what exists what is missing and the gate

**Status: groundwork only. The milestone is not runnable yet, and this issue must not be closed.**

## What the repository already has

| Artefact | State |
|---|---|
| `project.godot` | Godot 4 project, `main.tscn` as the entry point |
| `scenes/main.tscn` | a **Control**-based menu/placeholder, not a 2.5D level |
| `src/godot/core_rules.gd` | rules adapter over `data/rules/core.json` - **the superseded 1d10 kernel** |
| `src/godot/wn_rules.gd` | **new**: adapter over `data/rules/wn_core.json`, the Without Number baseline |

## The finding this issue depends on

`core_rules.gd` documents its resolution as `STAT + Skill + 1d10 vs DV`, reading `data/rules/core.json`.
That kernel was superseded on 2026-10-26 when the author directed the Without Number chassis for
everything (#615, implemented in #620). New Godot work must go through `wn_rules.gd`; the old adapter is
left in place only because existing scenarios still resolve on it.

The instruction in #631 - *do not substitute stock 2d6 for a currently approved 3d6 rule* - is answered by
the timeline: there is no approved 3d6 check anywhere in the tree, and the current approved baseline
**is** `2d6`. That is recorded here rather than assumed, because the issue asks for the full #564
timeline to be inspected first.

## What a playable vertical slice still needs

1. A 2.5D/isometric level scene (entrance, corridor, reception, consultation room) with a
   `CharacterBody3D` player, camera rig and collision.
2. Interaction system: raycast/area prompts, an interaction interface, and data-driven dialogue.
3. Branching interview content for doctor, nurse and patient, plus a persistent evidence journal.
4. A record/clue inspection flow calling `wn_rules.skill_check` with a **visible** roll and result.
5. Choice-dependent state, the Lakkahaltia encounter, and two ambiguous endings (mundane vs anomalous).
6. Save/load of case state, dialogue flags and evidence.
7. Fully offline; no LLM, no network.

## The gate stated plainly

None of the above can be verified on the machine this was written on: **there is no `godot` binary
installed**. The issue's own closing rule is *do not close until a clean checkout can run the
milestone*. That condition is not met, and the rules adapter alone does not meet it.

To proceed, either install Godot 4 on Laskin so the slice can actually be launched and tested, or run
the slice authoring on a workstation that has it. Until then this stays a groundwork PR: one adapter,
one honest status document, no claim of playability.
