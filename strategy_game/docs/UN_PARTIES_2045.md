# The four UN parties of 2045 (issue #470)

**The roster lives in `data/world/un_parties.yaml`** — the legacy UN-party register, reconciled in place
(it gains `id`, `legacy_name`, `position`, `governing`, `support`, `resources`, `themes`, `allegation` and
the `un_parliamentary_parties` register marker, with `scenario_start_year: 2045`). That file is the
**single** roster; the paradigm register in `strategy_game/data/global_factions.json` stays separate.

The discourse layer is `strategy_game/data/un_political_discourse.json`, read by
`strategy_game/un_political_discourse.py`. See `REALITY_TUNNELS.md` for the model and the 2026 baseline.

## The four, in the author's words

| Party | What it holds | Its position | Its problem |
| --- | --- | --- | --- |
| **Libertarian Accelerationist Party** | Opposes UN and member-state intervention and market regulation; demands Extraterrestrial Special Economic Zones and accelerated ASI research | right; electorally marginal; megacorporate funding | Corporate resources without popularity; hostile-ASI, Grey mind-control and hybrid-infiltration suspicions are **allegations, never confirmed** |
| **True Humans Party** | Hostile to all NHI; advocates their extermination — **a fictional extremist position, not endorsed** | far right | Popular rage without a coherent positive future; four incompatible strands |
| **Unity, Security and Stability Party** | Defence, public order, strong security, diplomatic options kept open | **the incumbent, majority support** | Inertia and power concentration; criticised for failing to adapt |
| **The Noösphere** | Green and Left parties with the **reformed CCP** as the largest player; a Taoist-Maoist cyborg multitude; seeks to join the Confederacy while keeping the Noösphere and Biosphere alive | green left | Transformative ambition dependent on an unknowable patron: its confidence in Confederacy *Service to Others* is **the party's belief**, not verified truth |

## What this is not

No leader names, no numbers, no seats, no dates for the background, no mechanics — the data file records
`simulation_rules_approved: false`. The three-umbrella proposal is superseded for default UN politics and
retained only as ancestry.
