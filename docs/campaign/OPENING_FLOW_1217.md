# The opening flow (#1217)

> **Status: the join is implemented, tested and blocked on two transcriptions.** `src/console/opening.py`,
> tested by `tests/test_opening_flow_1217.py` (14 cases). What is missing is not design — it is two
> catalogue entries the repository refuses to invent.

## The gap this closes

Two halves existed and never met:

- `rules.europol_lifepath.build_lifepath()` validated a complete set of character choices
- `console.first_day` played the authored first morning

Nothing called the builder. The officer who woke in Sörnäinen was **not** the officer anybody had
built: the sheet was a string (`sheet.tony.german`) and the issued kit was a list of flags.

`Opening` now binds the three things that must not separate:

```
answers → Lifepath → the canonical first-day session + a real Kit
```

and `save()` / `load()` round-trip all of it, so a half-played morning resumes.

## What the flow enforces

| Rule | Where it lives |
| --- | --- |
| every legality check on the character | `build_lifepath` (nothing is re-implemented here) |
| an Edge id must exist in the caller's catalogue | `build_opening` — a typo is refused, not sheeted |
| one session, one sheet | `Opening.__post_init__` refuses a second session |
| a kit belongs to one actor | `world.items.Kit` |
| a radio you have looked at is not a radio you can hear | `actions()` withholds `dispatch` until `dispatch.call` is covered |
| no roll to get to work | the whole `script()` path contains no dice |

The Dispatch rule is the reason the equipment sequence is a puzzle rather than a checklist: the flow
inspects the radio and the phone but does not link them, while `world.items.coverage()` counts only
**active** devices. Dispatch therefore stays unavailable until one of the two is switched on — the
player has to notice that the thing they checked is not yet working.

## Blocked on two transcriptions

The flow cannot ship a default character, and must not invent one. It needs:

1. **A verified CWN Edge catalogue.** The repository carries the four author-approved PC Edges
   (`psi_access.PC_DISCIPLINES` / `EDGE_SOURCES`) but no published Edge list, so `build_opening`
   takes `edge_catalogue` as an argument. A shipped CLI needs that catalogue filled from the book.
2. **The published *Law Enforcement* Background entry.** `rulebook/14_CHARACTER_GENERATION.md`
   contains no such entry today, so the flow cannot construct `Background(id="Law Enforcement", …)`
   from the repository's own text.

Both are transcription tasks with a citation, not design tasks. Until they exist, `build_opening` is
callable only with a caller-supplied catalogue — which is what the tests do, with fixtures that say
so in their docstring.

## Portable presentation and console resume (increment #1217)

The existing `Opening.view()` returns a JSON-safe read-only screen contract for the **current** actor: canonical actor and sheet IDs, current scene, current physical location, available first-day verbs, equipment coverage, and completion status. It deliberately does not expose the complete physical, social, cyber, or story graphs, because they may contain undiscovered nodes. The presentation can feed a text client, an Evennia command or a later Pygame-ce view without creating another resolver or session.

The reference console can now resume an already validated character's opening:

```bash
PYTHONPATH=src python -m console --opening --load opening.json
PYTHONPATH=src python -m console --opening --load opening.json --script actions.txt --save updated.json
```

Commands are `actions`/`help`, `status`/`look`, any verb in `Opening.actions()`, `save [path]`, and `quit`. The console delegates each mutation to `Opening.act()`. It does not create a default character, since verified CWN catalogues are still missing. This is **not** an Evennia command registration or a Pygame-ce display implementation; those remain open.

A third, smaller gap: the Foci catalogue exists (`cwn_foci`, 26 published Foci) but the flow passes
Focus picks through unchanged; choosing Foci is not yet a tested path for Tony.

## Evennia adapter

`mud/commands/default_cmdsets.py` now registers `CmdFirstDay`, a renderer over
`mud/nopunk_mud/first_day_adapter.py`. It stores the canonical
`WorldSession.to_snapshot()` on `caller.db.first_day_state`; it has no second map, sheet or
resolver. Typed commands:

```
firstday                  status / what is available now
firstday look             current place, scene and graph exits
firstday kit              issued kit and its active/fault state
firstday wake | uniform
firstday inspect <item>
firstday connect <item>
firstday repair <item>
firstday dispatch | ride | arrive | report
firstday reset            new morning; no other character state touched
```

Connection failure is a message and a preserved save, not a reset. The GUI remains open; the
interface-agnostic `Opening` object is what a GUI adapter should render.

## What this does not do

- It does not write Tony's nightmare, his lifepath prose or his memories. Those are Tomi's.
- It does not choose his Edges. An opening that picks its own character is a character nobody wrote.
- It does not add a minimal Python GUI. The Evennia adapter renders the same session; the GUI is
  still a separate change.

## Running it (once the catalogues are transcribed)

```python
from console.opening import OpeningAnswers, build_opening

opening = build_opening(
    OpeningAnswers(path="grunt", attributes=..., edges=("Alert", "Ghost"),
                   foci=(), learning=("Connect", "Shoot")),
    background=law_enforcement,          # the published entry
    edge_catalogue=verified_edges,       # the published list
)
for line in opening.script():            # no dice, no optional stop
    print(line)
```

## Cross-references

- [`docs/rules/PSI_ACCESS_1178.md`](../rules/PSI_ACCESS_1178.md) — which Edges a player character may take
- [`docs/rules/PSI_CARRYOVER_1196.md`](../rules/PSI_CARRYOVER_1196.md) — device grants and the Mutant Edge policy
- [`docs/tabletop/WORLD_GRAPHS_1178.md`](../tabletop/WORLD_GRAPHS_1178.md) — the graph procedure this session follows
