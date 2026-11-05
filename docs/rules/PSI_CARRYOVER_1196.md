# Carry-over psionics and graph runtime wiring (#1196)

> **Status: §2–§6 implemented as far as the books allow.** `src/rules/psi_edges.py`,
> `src/console/world_session.py`; tested by `tests/test_issue_1196_carryover.py` (26 cases).
> §1 (Astral) remains deliberately unbuilt.

The issue deferred six items. Four of them are **structural constraints**, and those can be built
without transcribing a rulebook. The other two are either printed numbers or a graph nobody needs yet,
and they stay unbuilt rather than guessed.

| § | Item | State |
| --- | --- | --- |
| 1 | Astral graph | **not built** — no authored scene needs navigation |
| 2 | Mutant Edge | structure built, tables **not transcribed** |
| 3 | Mentalist / Spellcaster / Summoner | built — prerequisites and progress-track rules |
| 4 | Device-granted effects | built — grants live and die with the device |
| 5 | Psychic Training Focus | structure built, **effects not transcribed** |
| 6 | Runtime wiring | built — console adapter over the four graphs |

---

## §2 Mutant — playable Europol-approved PC or NPC, three independent facts

`MutantTemplate` refuses to exist without a quoted mutation. The new `awn_mutant.MutantBuild` supports approved rookies, Stigmas, points and purchasing using printed AWN Deluxe p.16. A `MutationCatalogue` starts **empty**
and every entry demands a `Citation` (source, page, quote). A template drawing on an empty catalogue
raises rather than inventing a mutation — which is the honest state until somebody transcribes the
published tables.

Three facts stay apart, which is the point of the section:

- **mutation** — what the body does
- **ancestry** — where it came from, if anyone knows (`ancestry_known`)
- **PSI** — whether the character is psychic (`psi_discipline`, independent)

A Mutant is not automatically psychic. A Hybrid is a **possible origin**, not a diagnosis. The earlier
mandatory Hybrid-only mutation packages are not reintroduced anywhere in this module.

## §3 Mentalist, Spellcaster, Summoner

`EdgeGrants` names what an Edge actually gives, and `validate_edge()` returns every structural
problem at once:

- an Edge may not grant a discipline outside `psi_access.PC_DISCIPLINES`
- a Partial Psychic's `restricted_discipline` is respected — the Edge cannot widen it
- two Edges may not both advance the same discipline
- two Edges may not both own psionic technique progress (the *second progress track* the issue names)
- `Mutant` is allowed for Europol-approved PCs during character creation, without making them Hybrids or psychics

`EDGE_SOURCES` records where each Edge comes from, so an unknown name is refused rather than assumed.

## §4 Device-granted effects

`active_grants(carried, grants)` is the whole rule: a grant is in force **while its device is
carried**. Take the implant off and the ability ends — no second psychotronic subsystem, no permanent
character option. `Grant.selectable` is still always `False` (from `psi_access`), so a device can do
something remarkable without ever widening advancement.

## §5 Psychic Training Focus

`PsychicTrainingFocus` is a *structure*: ordered levels, each one carrying its printed benefit and a
`Citation`. It has no defaults and no formulas. Two consequences follow:

- it cannot be built without quoting the book, because every level demands a quote
- it can only be built for **Telepathy or Telekinesis**, so the Focus cannot become the back door that
  `psi_access` already closed

`PSYCHIC_TRAINING_FOCUS_AVAILABLE` stays `False` in both modules. When the authorised text is quoted
in, the flag flips and the levels get filled — and the test that currently asserts the refusal becomes
the test that asserts the numbers.

## §6 Runtime wiring

`WorldSession` is the smallest adapter that makes the graphs playable:

```python
session = WorldSession.from_dict(payload)      # format: noopunk.world.graphs
session.register("pc.rookie", "sheet.rookie")  # explicit, once
session.move("pc.rookie", "loc.stair")         # refused if no passable route
session.look("pc.rookie")                      # occupants, devices, exits
session.enter_scene("scene.briefing")
session.scenes_available()                     # story graph, filtered by flags and goals
```

Three constraints from the issue are enforced rather than described:

1. **one canonical actor record** — a sheet belongs to one actor; a second actor claiming it raises
2. **explicit actor-ID mapping** — an unregistered actor raises, nothing is inferred from a name
3. **CWN remains the action authority** — this adapter moves actors and lists scenes; it never rolls
   dice, spends Effort or writes to a sheet

`identity(actor)` is the paper procedure's seventh check, executable: the same actor ID through the
physical graph, the cyber graph and the social graph, with one sheet. Not being jacked in returns
`None` rather than raising — a character without an avatar is normal.

### When a handle differs from the canonical id

`WorldSession.identity()` assumes the actor ID is the same string in every view, which is the normal
case. When it is not — `act.rookie` on the sheet, `av.rookie` jacked into a camera, `rookie` in a
contact list — the mapping must be *declared*, not inferred:

```python
from world.actor_registry import ActorRegistry, CanonicalActor, Handle

book = ActorRegistry()
book.register(CanonicalActor("act.rookie", "Rookie", (
    Handle("physical", "act.rookie"),
    Handle("cyber", "av.rookie"),     # the avatar is a session, not a person
    Handle("social", "rookie"),
)))
book.canonical("cyber", "av.rookie")        # -> "act.rookie"
book.check_graphs(graphs)                   # every occupant and avatar resolves
book.one_sheet(sheets={"act.rookie": "sheet.rookie"})
```

Two rules are enforced there that a session cannot express: a handle belongs to exactly one actor, and
**an avatar id that is also a registered actor is refused** — an avatar is a session, not a person
(#1178 node semantics). `WorldSession` and `ActorRegistry` agree on the seventh check; neither rolls.

## What this does not do

- It does not implement the Astral graph. Nothing needs one yet.
- It does not transcribe AWN mutation tables or SWN Focus benefits. Both need the authorised text.
- It does not make the console play a case through the graphs. `WorldSession` is a navigator; wiring
  `CaseSession` to it is a separate change with its own review.

## Cross-references

- [`PSI_ACCESS_1178.md`](PSI_ACCESS_1178.md) — the access policy these items extend
- [`WORLD_GRAPHS_1178.md`](WORLD_GRAPHS_1178.md) — the four families and the paper procedure
- [`SCENE_TYPES_1184.md`](SCENE_TYPES_1184.md) — the scene procedures that run inside these graphs
