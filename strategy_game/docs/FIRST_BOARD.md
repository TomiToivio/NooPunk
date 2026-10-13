# The first board with content on it (issue #347, work item 3)

Status: **structure record for issue [#347](https://github.com/TomiToivio/NooPunk/issues/347)**, the
implementation-track issue. It defines no rule, opens no reserved area, and per the code-only testing
policy (#271) nothing in this document is asserted by a test. The executable half of this step is
[`bridge.py`](../tabletop/bridge.py) (`board_from_local_slice`, `layout_from_slice_binding`,
`local_slice_board`, `load_board_binding`), tested by
[`tests/test_board_local_projection.py`](../tests/test_board_local_projection.py).

## 1. What was still missing

The primitives landed in #351 (`strategy_game/tabletop/`) and the interface spike in #368
(`strategy_game/render/`). Both draw *declared state*; neither put **authored content on the layered
board**. `board_from_world(state)` projects a `WorldState`, which on a fresh state is empty, and the
renderer draws the pinned `view.board_view` projection, not the `Board`.

`strategy_game/data/ukweli_local.json` (the Republic of Ukweli slice, #322/#324) is the one piece of
complete authored local content in the crossover: 8 locations, 7 routes, 3 parties, 12 leaders, 2
relationships, 5 shocks. The board the issue describes — a layered network society with places,
factions and people — can be projected from it **without inventing a single record**. That is this
step, and it is the ordering the issue's own plan comment proposes (S1).

## 2. What the projection does

```
python -c "from strategy_game.tabletop import local_slice_board as b; import json; \
b_, l_ = b(); print(b_.identifier, len(b_.nodes), 'nodes,', len(b_.edges), 'edges'); \
print(sorted(n.layer for n in b_.nodes.values())); print(l_.to_dict()['positions']['old_harbor'])"
```

| Source (declared) | Board | Notes |
| --- | --- | --- |
| `locations` (8) | `physical` **location** nodes | declared `tags` carried; `pressure` deliberately not |
| `parties` (3) | `social` **faction** nodes | label from the party's `name` |
| `leaders` (12) | `social` **person** nodes | label from the leader's `name` |
| `routes` (7) | **travel** edges on `physical` | id derived from both endpoints |
| `relationships` (2) | **social** edges | each keeps its *own* declared tags verbatim in `notes` |

Every identifier is preserved verbatim, `Board.validate()` runs before the board is returned, and an
edge whose endpoint was not projected is **skipped, not invented** — the same behaviour
`board_from_world` already documents.

The mapping is **data**. `data/board_local.json` declares which source collection becomes which kind
and layer, which edge kinds the two edge families get, the cosmetic layout, and a `reserved` list of
what the board is *not*. So a new place, faction, person or route enters the board by editing the
slice data alone — the test
`test_a_new_place_enters_the_board_by_editing_the_slice_data_only` proves it, and
`test_the_binding_can_be_pointed_at_another_slice_without_touching_code` proves that a second slice is
a second document rather than a second module.

## 3. The two exclusions, and why they are the point

1. **No number reaches the board.** The slice carries illustrative quantities — `pressure` per
   location, `trust` per relationship, `legitimacy_delta` per shock, a `skill` per leader, the `year`.
   A prototype's number promoted into the shared board would be an unapproved rule by the back door,
   which is the trap the slice audit is proud of avoiding. Three contracts hold the line: no
   `BoardNode`/`BoardEdge`/`BoardPiece` field can hold a quantity; the projected payload contains no
   number at all; and changing *every* quantity in the source leaves the board **byte-identical**.
2. **No piece is invented.** The slice declares no token and no position, so no piece is projected. In
   particular no leader is placed "on" the location the slice names — a leader standing somewhere is a
   semantic the source does not state, and it is exactly the kind of reading that would later look like
   a rule.

Layout is kept **outside** the board, as the model requires: the committed layout in
`data/board_local.json` covers every projected node, so the issue's "no force-directed graph jitter
during gameplay" is a caching decision rather than a hope, and
`test_recomputing_a_layout_cannot_change_the_graph` pins that. A layout entry for a node the board no
longer has is **refused** (`BoardBindingError`) rather than quietly ignored.

## 4. What this step does not do

The gates in [`RULE_SYSTEM_RESEARCH.md`](RULE_SYSTEM_RESEARCH.md) are untouched — Gate A (leader RPG
rules), Gate B (political-simulation methodology), Gate C (strategy rules) and Gate D (integration
contract) are all still open, and *"Until all relevant gates, no gameplay mechanics are implemented."*
So, deliberately absent:

- **no action, cost, movement, eligibility, turn or victory** — the board is a graph container, and
  `Board.move_piece` still checks nothing about legality;
- **no pieces** (above);
- **no join to `WorldState`** — the projection takes the slice **as an argument** and returns a
  projection, so no Gate D join is performed and the argument is left to remove;
- **no new canon**. No faction, place, person, creature or event is created: every label on this board
  comes from the authored slice;
- **no rule in a second language, no live service, no proprietary engine, no model provider.**
  Standard library only, offline, deterministic.

## 5. What remains, and whose decision it is

1. **Helsinki-first, or Ukweli-first?** Issue #347's geography section describes a Helsinki faction
   headquarters, Finnish government and local institutional nodes, one or two abstract faraway contact
   nodes. `strategy_game/` holds **no Helsinki content at all**, and the legacy Helsinki material
   (`data/rules/unsa_academy.json`, `data/world/organizations.yaml`) is legacy-RPG content that needs
   an explicit conversion decision before the crossover binds to it (`AGENTS.md` §0). This step
   therefore projects the slice the crossover actually has and **records the Helsinki board as an open
   author content decision** rather than inventing headquarters, ministries or contacts. **PENDING.**
2. **Pieces.** Whether a leader should be a marker on a location, and what may move one, is a rule
   (`AGENTS.md` §4 and Gate C). The model supports pieces; this projection uses none. **PENDING.**
3. **Relationship kinds.** A relationship declares no kind in the source, so the neutral
   `communication` default is used and the declared tags are kept verbatim. Typing them is a one-line
   data change (`kind_from_tags`, e.g. `{"rivals": "opposition"}`) — and the choice is the author's.
   **PENDING.**
4. **The remaining #347 checklist items.** The RPG scene and the faction strategic action both pass
   through Gate A or Gate C; the Cosmist International Helsinki opening needs item 1 above; the
   turn/event history is the append-only record the plan proposes as S4; the data-driven example-card
   set and the content-pack loader are S3. None of them is closed by this step, and none of them should
   be closed on the author's behalf.
5. **The playtest.** Whether the presentation stays fast, eventful and readable at scale is a tabletop
   question, and `AGENTS.md` says out loud that playtesting is a human process that must not be
   converted back into a CI gate.

## 6. Verification

```
strategy_game/tests   704 OK   (640 before; 37 in test_board_local_projection.py, 27 in the #359 file)
tests                 509 OK
python -m strategy_game        key set unchanged: {schema_version, locations, network_nodes,
                               network_edges, assets}
```

`strategy_game/render/`, `strategy_game/view.py`, `strategy_game/__init__.py`,
`strategy_game/core.py` and `strategy_game/local_slice.py` are **untouched**: the renderer's pinned
view model, the pinned package `__all__` and the pinned `python -m strategy_game` key set all still
pass. `local_slice.py`'s parallel dataclasses, its `network: int` and its provisional playtest rules
are neither extended nor inherited. Legacy RPG untouched (`AGENTS.md` §0, #306).
