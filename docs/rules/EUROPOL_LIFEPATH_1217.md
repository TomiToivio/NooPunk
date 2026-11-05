# Tony German's lifepath: the builder and its legality contract (#1217)

> **Status: builder core, author-facing.** `src/rules/europol_lifepath.py` validates a complete set of creation
> choices and returns a character, or refuses with every violation named. It is **not** yet the player-facing
> choose-your-lifepath flow: it offers no prompts, no prose, no memories and no default picks.

The tracker's opening line asks for a **choose-your-lifepath** flow and a deterministic builder for Tony German,
*"test legality and tabletop equivalence"*. This is the part of that which can be built without inventing canon.

## What is fixed, and where each line came from

| fact | value | source |
|---|---|---|
| name | Tony German | #1217 line 7 |
| origin | Helsinki | #1217 line 7 |
| academy | Europol Academy | #1217 line 7 |
| background | Law Enforcement | #1217 line 7; a published CWN background |
| employer | Europol | #1217 note — supersedes the older UNSA employer |
| posting | Europol Field Office, Ratakatu 12 | #1217 line 8 |
| supervisor | Dr Harri Romppainen | #1217 line 8 |

These live in `FIXED` as `(value, source)` pairs, and the builder will not accept a different Background — a
different one is an author decision, not a player option.

## The three recruitment routes

`PATHS` holds `grunt`, `geek` and `freak`. Each is a **label for the authored flow**, not a mechanic:

* `grunt` and `geek` require no Edge and grant nothing;
* `freak` requires the **Mutant** Edge, because #1178 makes that Edge the human-alien Hybrid and the route is named
  for it;
* **no route grants a bonus.** If the flow later needs one, that is an author decision and a rules change, not a
  quiet addition here.

## What the builder delegates, so that nothing can drift

| question | answered by |
|---|---|
| is this a legal attribute assignment? | `rules.cwn_character.assign_array` (the published array) or `roll_attributes` (3d6 results) |
| how many Edges, and may this one be taken? | `rules.cwn_edges_foci.pick_edge`, including the Underdog Rule's power-Edge exclusion |
| is the character an underdog? | `rules.cwn_edges_foci.underdog_eligible` |
| how many Focus picks? | `rules.cwn_edges_foci.focus_slots` (one, two with the Focused Edge) |
| which Focuses exist? | `rules.cwn_foci.FOCI` — the published twenty-six |
| which skills does the Background grant? | `rules.cwn_backgrounds` (free skill plus two Learning picks) |
| is this a real personality tag? | `rules.scene_tags.PersonalityTag` |

There is no second copy of any of that arithmetic. A rule change lands in the rules module and this builder follows,
which is the only way a builder and a rulebook can stay equal.

## The one deliberate refusal

**There is no verified CWN Edge catalogue in the repository.** Only the four author-approved PC Edges in
`rules/psi_access.py` are named with confidence; the rest were marked `[?]` in the #1174 draft rather than guessed.
So `build_lifepath` takes `edge_catalogue:` as an argument. Pass the real catalogue and a typo becomes a violation;
pass nothing and the builder trusts the objects it was given, which is what tests do with fixtures.

The missing catalogue is the reason the tracker's line 7 stays unticked: the *flow* needs to offer a list of legal
Edges, and nobody has yet transcribed the published Edge list into the repository. Foci are already there.

## Contract

```python
from rules.europol_lifepath import build_lifepath, LifepathError

path = build_lifepath(
    path="grunt",
    attributes={"Strength": 14, "Dexterity": 12, "Constitution": 11,
                "Intelligence": 10, "Wisdom": 9, "Charisma": 7},
    background=law_enforcement_background,
    edges=(edge_alert, edge_ghost),
    foci=("Alert",),
    learning_picks=("Connect", "Shoot"),
    edge_catalogue=verified_edges,
)
```

* legal → a `Lifepath` with attributes, background, edges, focus levels, skills, underdog flag, personality tags and a
  `provenance` tuple naming the source of each part;
* illegal → `LifepathError` whose `.violations` lists **every** problem as `(field, reason)`, not just the first;
* `to_dict()` is stable, so two equal lifepaths serialise identically and a saved character restores deterministically.

## Tests

`tests/test_europol_lifepath_1217.py` — 24 tests, all with **invented fixtures** (a two-skill Background, three Edge
objects, real Focus names). They cover the legal builds, determinism, provenance, the hybrid route with the Mutant
Edge, and thirteen refusals: third Edge without Underdog, wrong route, wrong Background, wrong attribute set, an
assignment that is not the array, wrong Learning count, an unlisted Learning pick, an Edge outside the catalogue, a
nonexistent Focus, two Focuses without Focused, an Underdog power Edge, and the requirement that every violation is
reported at once.

No test asserts a CWN Edge name beyond `Mutant` and `Focused`, because none has been verified here.

## What is still missing for the tracker line

1. **The verified Edge catalogue** — the blocker above. Until it exists the flow can only offer Foci.
2. **The offer lists** — which personality, goal and social tags the flow presents. Personality tags are descriptive
   and unconstrained by rules, which makes this purely an authoring decision.
3. **The memories** — #1123; Tomi writes them.
4. **The player-facing loop** — prompts, re-asking after a violation, and the CLI adapter. The builder is the piece
   such a loop calls.
