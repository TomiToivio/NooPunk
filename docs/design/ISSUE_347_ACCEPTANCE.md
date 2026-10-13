# Issue #347 — acceptance record

**Basis for closing.** The author authorised defer-and-close on 2026-10-13, provided a deferred item is
stated as deferred. This issue is the case that most needs that discipline: it was closed **by accident**
(the merge of PR #397 read a closing keyword out of that PR's own sentence *"This does **not** close
#347"* — the negation is not parsed), and reopened deliberately.

## Met (measured on `main`)

| # | Criterion | Evidence |
| --- | --- | --- |
| 1 | Audit reusable modules and open mechanics; document them | `docs/INTERFACE_SPIKE.md`, `TABLETOP_SLICE_AUDIT.md`, `FIRST_BOARD.md`, `INTEGRATION_BOUNDARIES.md` |
| 2 | Pure-Python dice, cards, decks and tarot placeholder, deterministic with seeds/serialization | `strategy_game/tabletop/{dice,cards,decks,tarot,serialization}.py`; `test_tabletop_primitives` — 84 tests OK |
| 3 | Layer-aware network board with persistent ids, Helsinki HQ, Finnish institutions, abstract nodes | `tabletop/board.py` + `data/board_local.json` + `docs/FIRST_BOARD.md`; `test_board_local_projection` — 37 tests OK |
| 4 | RPG choice/check and faction strategic action reach one authoritative state, with dice provenance | `turn.py` + `tests/test_turn_connection.py` (PR #424); 17 tests OK |
| 7 | **Data-driven example cards for all ten kinds** | New: `content_schema.py` + `data/tarot_placeholder.json` + `tests/test_content_authoring.py` — 7 tests OK. Measured examples: character 17, faction 7, organization 1, place 8, research 1, event 11, mission 4, relationship 2, ideology/signifier 16, tarot placeholder 3. **`missing_kinds()` is empty** |
| 9 | **Modding/authoring schema documented, and a new foreign node and card added from data alone** | New: `docs/CONTENT_AUTHORING.md` + `content_schema.py`; the test performs both additions in a temporary copy, loads them through `characters.load_character_cards()` and `local_geography.load_local_geography()`, and proves the shipped data's digests are unchanged |

## Deferred (recorded as deferred, not met)

| # | Criterion | Why it is deferred, and to what |
| --- | --- | --- |
| 5 | Interface spike in **two** candidate renderers, with Godot↔Python communication, SVG/Canvas/Qt graph rendering, packaging and accessibility evaluated | **partly met, partly deferred** — one renderer exists (`render/text.py`, the pinned view models, the offline import guard) and `docs/INTERFACE_SPIKE.md` records the evaluation and a recommendation. Choosing and evaluating the *second* renderer is the author's pick: queue row **D13** |
| 6 | Deliverable playable UI: Board, RPG Scene, Faction Management, Global Ideology, Character Sheet, cards/deck inspector, dice log | **deferred to D13** — the data and view models it would draw are landed (pinned keys, `council_view.py`, the text renderer), but building the UI before the renderer is chosen would be guessing |
| 8 | Cosmist International Helsinki opening: inspect HQ, talk to an NPC, one choice/check, one strategy move, one event/tarot prompt, advance | **deferred** — needs criteria 5/6 and the rules gate (`RULEBOOK.md`: NO RULES APPROVED); queue rows D11 and D13 |
| 10 | Playtest that presentation stays fast, eventful and readable with many dormant nodes and cards | **deferred** — it is a measurement of the UI that criterion 6 defers |

## Not claimed

No rule is approved, no renderer is chosen, no UI is claimed to exist, and nothing here makes any
content canon. The text renderer is the reference implementation, not the deliverable.

— Ai (愛)
