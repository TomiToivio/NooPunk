# #468 acceptance record — the 2045 global default scenario

**Date:** 2026-10-22. **Status:** acceptance record. **Step 1 is delivered; the default snapshot is
still the author's choice, and the global strategy layer is gated behind the RPG.**

## What the issue asks for, and where it lives

The issue's own step-1 deliverable asks for **2–3 short post-crisis openings with one explicitly
recommended**, plus the default five-character roster per playable faction. The author ruling of
2026-10-15 also fixes the frame: the default opening is **2045**, the background events are
**unordered `20XX`**, and the Fall is partial and geographically uneven.

| Criterion | Where it lives | Status |
| --- | --- | --- |
| **Step 1 — 2–3 post-crisis opening snapshots**, with one explicitly recommended | `docs/design/ISSUE_468_STEP1_OPENING_SNAPSHOTS.md` — Snapshot A *"The Quarantine Belt"*, Snapshot B *"The Empty Seat"* (**recommended**), Snapshot C *"The Recovery Boom"* | **met** — three snapshots, one recommendation, each answering the same three questions: what holds the peace, who is playing, what the first turn is |
| The 2045 / unordered-`20XX` frame, and the partial, uneven Fall | the same document, stated as the frame all three snapshots share | **met** |
| What the snapshots **deliberately leave open** | the same document's closing section | **met** — the empty seat is read as an *empty signifier* rather than settled by a quiet canon decision |
| The **five-character roster** per playable faction (leader + four agents) | `strategy_game/rpg/roster.py` — five seats, one action per character per turn; `strategy_game/data/un_political_discourse.json` — `default_playable_party_ids` (3) | **met as structure** — the capacity exists for the three playable factions |
| The three-faction decision applied to the scenario | `un_political_discourse.json` — `default_playable_party_ids` | **met** |
| A playable local scenario instance, and the city-scenario contract | `strategy_game/data/city_scenario_schema.json`; `strategy_game/data/board_local.json` | **met** — the schema and a reference instance exist; the *global* scenario is a different layer |
| The founding story as a proposal, approving nothing | `strategy_game/data/founding_story.json` — `status: PROPOSAL - approves nothing`, `pending_author_decisions` (2) | **met** |

## What is deliberately not settled

- **D24 — which 2045 opening snapshot is the default.** This is the issue's own step-1 question
  and it is the author's: the document *recommends* Snapshot B and says why, and a recommendation is
  not a decision. This record does not turn the recommendation into canon.
- **D17** (the four 2045 UN parties) and **D18** (complete roster at start, or the starting three)
  are shared with #470.
- **The global strategy layer is not built.** The global scenario is a *future* start, and the
  author's own work order keeps the Strategy level behind the RPG gate.

## Reproducible checks

```bash
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"   # 1535 tests, OK
python3 -m unittest discover -s tests -p "test_*.py"                 # 585 tests, OK
```

## What closure of #468 does and does not mean

It means **step 1 is delivered**: three 2045 opening snapshots with a reasoned recommendation, the
shared frame, the explicitly open questions, and a five-character roster structure for the three
playable factions.

It does **not** mean a default snapshot has been chosen, that the global scenario is implemented, or
that the strategy layer is unlocked. The recommendation in the document is exactly what it says it
is.
