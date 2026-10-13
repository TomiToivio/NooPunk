# Digital tabletop slice: audit, scope record and what landed

Status: **audit and scope record for issue [#347](https://github.com/TomiToivio/NooPunk/issues/347).**
It is not a rules document, it opens no reserved area, and per the code-only testing policy (#271)
nothing in it is asserted by a test. The executable half of this issue is
`strategy_game/tabletop/`, tested by `strategy_game/tests/test_tabletop_primitives.py`.

This is work item 1 of #347 as the issue itself lists it: *"Audit current `strategy_game/`,
`project.godot`, rulebook, issues #304/#309/#346 and document reusable modules and open mechanics."*

## 1. What already exists, and what it is for

`strategy_game/` is a standalone package (issue #282) whose docstring says it "contains **no rules**".
That is accurate today, and it is the reason this issue starts with an audit rather than a design.

| Module | What it is | Reused by this unit? |
| --- | --- | --- |
| `core.py` | `WorldState` plus `Leader`, `Faction`, `Asset`, `Location`, `NetworkEdge`, `Event` — frozen typed containers, no causal transitions | Read-only, via `bridge.py`; **not modified** |
| `provenance.py` | `Provenance` / `ProvenanceKind`, default `UNKNOWN`, plus `PROVENANCE_KINDS` and `NON_EVIDENCE_KINDS` | Reused directly by `tabletop/cards.py` |
| `politics.py` | Layer II vocabulary: demands, signifiers, formations, frontiers, relation layers | Not touched (Gate B) |
| `political.py` | `PoliticalField`, `PowerMode`, `Articulation`, `CommunicativeTie` | Not touched (Gate B) |
| `capabilities.py` | Side-effect-free availability check for the reserved optional adapters (mesa, networkx, ollama, concordia) | Untouched; the tabletop package imports none of them |
| `ports.py` | Reserved protocols (`LeaderRPG`, `PoliticalSimulation`, `FactionStrategy`, `AgentProvider`, `MapProvider`, `AgentRunner`) | Untouched; `MapProvider` is the seam a board renderer would eventually sit behind |
| `view.py` | `board_view` (key set pinned by a CI smoke step) and `political_view` | Untouched; the pinned key set is why the table got its own package |
| `local_slice.py` / `global_slice.py`, `data/ukweli_local.json`, `data/global_factions.json` | The existing local (Helsinki) and global slices, and the faction roster data | Untouched |
| `docs/` | `RULE_SYSTEM_RESEARCH.md` (the gates), `INTEGRATION_BOUNDARIES.md`, `POLITICAL_SIMULATION_DESIGN.md`, `MVP_LOCAL_CITY_M0.md`, `NOOPUNK_GLOBAL_DESIGN.md`, `LEADER_COUNCIL_SYSTEM.md`, `GLOBAL_FACTIONS.md` | Read; the gates below come from the first two |

Two structural facts constrain anything built on top:

* **The public API is pinned in two places.** `strategy_game/__init__.py`'s `__all__` is asserted by
  tests, and `python -m strategy_game`'s key set is asserted by a CI smoke step. Anything new either
  goes inside that shape or gets its own package. The tabletop primitives therefore have their own
  `__init__` and their own `__main__`, and neither pin was widened.
* **`WorldState` is the *declared-data* record, not a simulation engine.** `INTEGRATION_BOUNDARIES.md`
  is explicit that presentation must be read-only, so the board is projected from a state rather than
  stored on it.

## 2. The gate reading that fixed this unit's scope

`RULE_SYSTEM_RESEARCH.md` keeps four gates open —

> Gate A: author-approved leader RPG rules. Gate B: author-approved political-simulation methodology
> and simulation assumptions. Gate C: author-approved strategy rules. Gate D: explicit integration
> contract and prototype playtest.

— and adds: ***"Until all relevant gates, no gameplay mechanics are implemented."***

Read against #347's checklist, that splits the issue cleanly:

**Inside the gates' boundary (built here):** dice notation, an injectable seeded RNG, a per-die
breakdown and a replayable log; card records; decks, zones and a reproducible draw log; a layered
graph with typed edges and pieces; cosmetic layout kept apart from topology; tarot **placeholders**;
versioned snapshot; a read-only projection from `WorldState`.

**Outside it (not built, and deliberately):** the check procedure and everything a roll is compared
against (Gate A); any political-simulation transition (Gate B); strategic actions, an economy, turn
cadence, victory (Gate C); joining the table to `WorldState` (Gate D); tarot composition, meanings and
modifiers (the issue routes these to #304).

The second row is not a caveat bolted on afterwards. It is the reason the first row is small enough to
be safe: what landed is the substrate an approved rule layer would manipulate, with no opinion about
what it manipulates it *for*.

## 3. What landed

`strategy_game/tabletop/`, eight modules, 84 runtime tests:

| Module | Contents |
| --- | --- |
| `dice.py` | `parse_notation` (`d6`, `2d6`, `3d8+1`, `1d20-2`), `DicePool`, `roll` with injectable/seeded RNG, `RollResult` with per-die breakdown, `RollLog` |
| `cards.py` | `Card`, `CardType` (the eleven families the issue names), `CardRole` (persistent record vs playable move), `CardVisibility`; prerequisites and effects as opaque structured data |
| `decks.py` | `Deck`, `Zone`, `DuplicatePolicy`, `DrawLogEntry`; seeded shuffle, logged draw, deliberate `place`, `discard`, `recycle` |
| `board.py` | `Board`, `BoardNode`, `BoardEdge` (six named kinds), `BoardPiece`, `Layout`; invariant checks that raise rather than repair |
| `tarot.py` | `TarotCard` placeholder, `TarotUse` (the five interpreter contexts), `TarotDraw` attribution, one shared deck type |
| `bridge.py` | `board_from_world(state)` — a projection taking the world state as an argument |
| `serialization.py` | `TableState`, `TABLE_SCHEMA_VERSION`, `save_table` / `load_table` |
| `__main__.py` | `python -m strategy_game.tabletop` — a rule-free demonstration |

Three design decisions worth stating explicitly, because each one is a place where the code could
have quietly invented something:

1. **The dice module has no resolution.** There is no difficulty, no target number, no success check,
   no advantage, no opposed roll and no modifier cap. `RollResult.total` is an integer.
   `parse_notation` **refuses** `4d6kh3`-style syntax rather than reading it as `4d6`, so an
   unapproved rule cannot enter through a notation string nobody looked at twice.
2. **Replay does not depend on the RNG.** `RollLog` stores the individual faces, so `replay()`
   reconstructs every result without consulting a random implementation. Determinism *and* auditability
   survive even an unseeded live roll.
3. **The projection performs no integration.** `board_from_world` takes a `WorldState` as an argument
   and returns a new `Board`; it mutates nothing and `WorldState` gains no field. A test asserts the
   world state's JSON is byte-identical before and after, and another asserts `WorldState` has no
   `board`/`decks` field — so the Gate D join cannot drift in unnoticed during a later refactor.

Two smaller ones: `Layout` is a separate object from `Board`, so recomputing a force-directed layout
can never alter the graph (the issue's "no force-directed graph jitter during gameplay" becomes a
caching decision); and an edge whose endpoint was not projected is **skipped, not invented** — a
dangling edge would be a false statement about the map.

## 4. Scope record: what this unit does NOT open

Recorded so a later session does not read the presence of primitives as permission.

- **No mechanic, number, threshold or cost is defined anywhere in this unit.** Not in code, not in
  data, not in prose.
- **No canon.** No faction, character, place, creature, institution or event is created. Node labels
  in the demo are marked illustrative.
- **`RULEBOOK.md`, `rulebook/*`, `AGENTS.md` and the legacy RPG are untouched.** No rule text was
  written.
- **No un-reservation is requested.** Unlike a design issue that asks for a reserved subsystem, this
  unit needs none of the `AGENTS.md` §4 areas: a dice *parser* is not a combat system, and a card
  *container* is not a card game.
- **The tarot boundary from #304 is preserved, not assumed.** The placeholder has no meaning,
  numeral semantics, reversal rule or modifier, and `TarotCard.assert_placeholder()` exists so the
  field can be shown to still be unclaimed.

## 5. Open mechanics, and the author's call

These are the decisions this unit deliberately leaves open. Each is a gate, not a gap.

1. **The resolution core.** Which die, what a check is compared against, and whether advantage or
   opposed checks exist at all. The machinery supports any of them; none is selected.
2. **Whether the table joins `WorldState` (Gate D).** Today the board is a projection with an
   explicit argument. If the author approves the join, the change is to read the board off the state
   and delete the argument — no redesign.
3. **Tarot composition, meanings and modifiers (#304).** The five interpreter contexts are modelled;
   what a card *says* is not.
4. **The renderer.** #347 asks for an interface spike comparing the existing Godot project against
   Qt/PySide6 and a Python-service-with-web-canvas approach, and for a committed decision record.
   That comparison is not in this unit, and `ports.py`'s reserved `MapProvider` seam is where a
   chosen renderer would attach.
5. **Whether the local and global slices become board data** rather than their present JSON, and
   whether `ukweli_local.json`'s Helsinki material is the starting board the issue describes.

## 6. Next unit, if the direction holds

The smallest useful continuation is the **interface spike** (item 4 above): a throwaway multi-screen
prototype against at least two candidate renderers, measured on packaging, iteration speed,
graph rendering and accessibility, with the decision recorded. It needs no gate, because it decides
*tooling*, not rules — and #347 asks for the decision to be committed rather than implied.

After that, the vertical slice's remaining pieces (RPG scene, faction action, turn history) all pass
through Gate A or Gate C, so they need the author's rule decisions first.
