# Scene types (#1184)

> **Status: implemented.** `src/world/scenes.py`, tested by `tests/test_scene_procedures_1184.py`.
> Five scene types are live: **Social, Investigation, Exploration, Cyber, Action**. **Astral is
> postponed** and raises `PostponedScene` rather than returning an empty result.

A scene is an **interface shape, not a second rules engine**. Every procedure here answers the same
three questions, then hands the uncertainty to a module that already owns it:

1. what may the player do in this scene?
2. what must be true for the scene to end?
3. which existing module resolves the check?

| Scene | Resolves via | Produces |
| --- | --- | --- |
| Social | `rules.social.resolve_social` | a social tag — a fact, never a number |
| Investigation | `rules.investigation.discover` | clue tags, one per clue actually found |
| Exploration | `world.graphs.PhysicalGraph` | visited places and what was found there |
| Cyber | `rules.cwn_hacking.hacking_check` + `AlertClock` | a device outcome and the alert state |
| Action | `PhysicalGraph` + `rules.physical_combat` | a phase, an arrest, or a recorded use of force |

---

## Social

A conversation trying to change someone's mind.

**The procedure adds one rule:** without a lever there is no check. A social scene with no social tag
and no clue *about that person* is not a hard conversation — it does not move, so no dice are rolled.
The check itself is CWN's. Coercion always leaves a Grievance, recorded as an unfavourable tag rather
than invented as a penalty.

## Investigation

The point is to find something out.

Competency buys the clue; there is no roll to fail. `rules.investigation` already guarantees that a
core clue is reachable by an ordinary competency and that an exit is never gated behind luck. This
procedure adds the **record**: a clue tag per clue found, with its route and its rung on the evidence
ladder, so *"how do you know that?"* has an answer three scenes later.

## Exploration

Going somewhere and seeing what is there.

Movement is the graph's, not a new subsystem: every move goes through `can_move` / `move`, so a locked
door or a missing route fails here exactly as it fails everywhere else. Discoveries are attached to
places, not to dice.

## Cyber

A hacking scene.

CWN's hacking check resolves the action and the network's alert clock keeps the cost of failure. This
procedure adds nothing numeric. Note what it does **not** do: a successful run program does not hand
over the files — collecting the data is the next scene, and that is a separate problem.

## Action

An arrest, a pursuit, a door, a standoff — the scene the old vocabulary called **Combat**.

The rename is not cosmetic. The old word imports a genre the setting does not have: Finland is not the
United States, a Finnish police action scene is an arrest, a pursuit, a forced entry, a standoff or a
containment, and the people in it are usually not shooting at each other.

`ActionScene` is a **phase machine**, because most of an action scene is talking, waiting and walking,
and force is the short exception:

| Phase | Verbs |
| --- | --- |
| **approach** | close, observe, call_backup, make_contact, withdraw |
| **contact** | order, negotiate, contain, pursue, escalate, arrest, withdraw |
| **force** | restrain, brawl, draw_firearm, fire, arrest, break_off |
| **aftermath** | arrest, first_aid, report, release |

Three rules are enforced in code because prose does not enforce them:

- **Force needs a recorded reason.** `escalate` refuses without one.
- **A firearm needs recorded grounds.** `draw_firearm` refuses without them, and `fire` does not exist
  until the weapon is drawn. This is the Europol burden-of-proof rule from
  [`PSI_ACCESS_1178.md`](PSI_ACCESS_1178.md) §5 applied to the ordinary case: suspicion of hybrid
  ancestry is grounds for investigation and detention, never for summary force.
- **An arrest needs a lawful basis and the subject in reach.** `arrest` refuses otherwise; reaching
  them is what `contain` and `pursue` are for.

**A pursuit is a path problem, not a chase mini-game.** `pursue` takes one breadth-first step toward
the subject along the physical graph; if there is no passable route, the scene says so instead of
falling back on a chase table.

The violence itself is CWN's: `rules.physical_combat` owns margins, wounds and armour. This class
never rolls for them, and `brawl` / `fire` record the fact and hand it over.

---

## Astral — postponed, loudly

`SceneFrame(scene_type="Astral")` raises `PostponedScene`. The type exists in the design and is not
implemented. It is an error rather than an empty result **on purpose**: an unimplemented scene type
that returns `passed=False` quietly will eventually ship a scene that resolves to nothing, and nobody
will notice which scene it was.

It comes back when a scripted Astral Projection scene needs its own navigable graph — not before.

## Cross-references

- [`NARRATIVE_TAGS_1184.md`](NARRATIVE_TAGS_1184.md) — the tags these procedures read
- [`SCENE_PROPOSALS_1184.md`](SCENE_PROPOSALS_1184.md) — interrogation, data collection and data analysis: proposed, not implemented
- [`WORLD_GRAPHS_1178.md`](WORLD_GRAPHS_1178.md) — the graph families scenes live in
