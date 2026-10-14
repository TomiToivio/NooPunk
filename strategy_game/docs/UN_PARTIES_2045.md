# The four UN parties of 2045 (issue #470)

**Status: the author's decision of 2026-10-15, implemented as data.** `strategy_game/data/un_parties_2045.json`
carries the four parties; `strategy_game/ideology_framework.py` loads and validates them;
`strategy_game/tests/test_ideology_framework.py` asserts the shape. **No mechanic, number or rule is fixed
here** — `strategy_game/RULEBOOK.md` still reads NO RULES APPROVED.

The four are **fictional 2045 successor coalitions**, not assertions about present-day parties, and the
UN/UNSA remain governing institutions whose control is politically contested rather than a fifth faction.

| Party | What it holds | Material base | Its problem |
| --- | --- | --- | --- |
| **Libertarian Accelerationist Party** | Opposes UN and member-state intervention and market regulation; demands Extraterrestrial Special Economic Zones and permission for accelerated ASI research | Substantial megacorporate funding | Corporate resources without popularity; suspicions of hostile-ASI control, Grey mind control and hybrid infiltration are **in-world allegations, never confirmed** |
| **True Humans Party** | Hostile to all NHI; advocates genocidal and exterminationist policies against them, **depicted as an extremist position and not endorsed** | A mobilised populist base, no comparable institutional or corporate base | Popular rage without a coherent positive future; four incompatible strands |
| **Unity, Security and Stability Party** | The **incumbent with majority popular support**: defence, public order, strong security, diplomatic options kept open | Functioning institutions and broad everyday legitimacy | Inertia and power concentration; critics see an inability to respond creatively to simultaneous paradigm changes |
| **The Noösphere** | Earth's Green and Left parties with the **reformed CCP** as the largest player; a Taoist-Maoist ideology of the cyborg multitude; seeks to **join the Confederacy** while keeping the Noösphere and Biosphere alive | Green and Left parties, and the party-state | Transformative ambition dependent on an unknowable patron — the faith in Confederacy *Service to Others* is the party's conviction, not verified truth |

## Stances, kept separate per shift

Each party carries a stance on **each** of the four axes — soft PSI, Confederacy, Orion, ASI — because one
generic pro/anti-alien scale cannot represent this politics. The values are a working hypothesis recorded
in the data (`stance_status: working_hypothesis_not_locked`), not locked doctrine.

## Reconciliation with what already existed

This is a **revision of canon, not new authoring**, and the file says so: it names
`data/world/un_parties.yaml` (the legacy four-bloc register) and queue row **D8** — *reconcile the legacy
UN party records with the established UN world government and eleven Parties*. The four occupy the
**UN-parliamentary register**, which stays distinct from the seven paradigm formations in
`global_factions.json` and from #328's Party table. Each party records its candidate ancestors in all
three registers, with the mapping left for the author to ratify.

## What is deliberately not here

No names of leaders, no numbers, no seats, no mechanics, no dates for the background. The three-umbrella
proposal is superseded for default UN politics and retained only as ancestry and constituent currents.
