# Republic of Ukweli: local strategy scenario (2027)

**Status:** Provisional city-map adaptation for #324. This does not retcon the separate post-crisis UNSA Helsinki RPG.

> **Two names below are contested on `main` and are NOT settled by this document.** Recorded here because this is the path #324 names, so a reader arrives here first.
>
> - **The state's name.** This file says *Republic of Ukweli*; [#325](https://github.com/TomiToivio/NooPunk/issues/325) states *"**Official name: People's Republic of Ukweli**"* and makes the name load-bearing for the setting's own joke (*"Not quite Cuba, comrade"*), which only works because the formal name misleads. These are not stylistic variants — *People's Republic* carries a claim about the state's self-understanding. **Awaiting the author.**
> - **The libertarian party.** This file and `ukweli_local.json` say **ULP (Ukweli Libertarian Party)**; [#325](https://github.com/TomiToivio/NooPunk/issues/325) and [#326](https://github.com/TomiToivio/NooPunk/issues/326) say **LFP (Libertarian Freedom Party of Ukweli)**. **Awaiting the author.**
>
> Both conflicts are now carried as **structure with the decision still PENDING** in [`../design/ISSUE_324_UKWELI_GAP_CLOSURE.md`](../design/ISSUE_324_UKWELI_GAP_CLOSURE.md): the state's **official name is #325's own declaration** (People's Republic of Ukweli) recorded as a register mapping rather than a choice, and the party keeps the data id `ulp` with its display label open. That record also closes the island-count gap this file's list could not — the map now carries three island nodes, one of them the restricted exclusion island.
>
> The completed all-refs and warehouse audit this file asks for in its closing paragraph — and the retain/adapt/retire inventory that goes with it — is [`docs/design/ISSUE_324_UKWELI_CANON_REUSE.md`](../../docs/design/ISSUE_324_UKWELI_CANON_REUSE.md) (#324 deliverable A). The longer scenario document at [`UKWELI_LOCAL_SCENARIO.md`](UKWELI_LOCAL_SCENARIO.md) is #324 deliverable B, marked CANON/PROPOSAL statement by statement.

## Provenance and reuse inventory

- **Retain:** The three-party local MVP (CPU, UIP, ULP), originally recorded in [#324](https://github.com/TomiToivio/NooPunk/issues/324), [#329](https://github.com/TomiToivio/NooPunk/issues/329) and [the global faction roster](../../strategy_game/docs/GLOBAL_FACTIONS.md). Earlier project declarations distinguish a national-liberation governing communist party, identity-focused populist opposition, and libertarian accelerationist opposition. The running data uses these party identities.
- **Retain/adapt:** The Indian Ocean archipelago and modern port metropolis specified in #324, influenced by Mombasa, Zanzibar, Mumbai and Singapore but not copying their actual districts.
- **Retire from this timeline:** Later UNSA institutions and post-NHI-Crisis certainties. These remain canon for the separate later-era RPG, not facts of the 2027 political slice.
- **Newly proposed:** The eight abstract playable location labels, their travel links, generic leader placeholders, starting resources and five event cards in [ukweli_local.json](../../strategy_game/data/ukweli_local.json). **None are claimed as recovered canon**.

This is a bounded repository/default-branch search, **not a complete audit of historical branches or archived sources**. Historical names and NPCs should be reconciled against archived lore before final canon approval.

## City and islands

One modern Indian Ocean port city, three island locations — one of them a restricted exclusion island — a mixed urban fabric and a short coastal hinterland. Playable places: Old Harbor and Civic Centre, Mixed Neighborhoods, University and Hospital, Industrial Logistics Port, Coastal Hinterland, Outer Island Communities, Airfield Island, Restricted Island (biodiversity exclusion zone). The historic quarter is folded into the waterfront civic node so the eight-node envelope holds three islands, one restricted; the closure and its still-open trade-off are recorded in [`../design/ISSUE_324_UKWELI_GAP_CLOSURE.md`](../design/ISSUE_324_UKWELI_GAP_CLOSURE.md). Connections are ferry/road/bridge *abstract adjacencies*, not a tactical map; the restricted island carries no route, so no leader reaches it under the provisional travel rules. The model and mechanics accept any scenario conforming to the JSON schema. Real-world inspirations are urban and institutional dynamics, not replicas or demographic stereotypes.

## Opening political situation

Three rivals: the Communist Party of Ukweli (incumbent national-liberation and reform legacy), Ukweli Identity Party (rural/identity populist opposition), and Ukweli Libertarian Party (libertarian accelerationist opposition). Four provisional functional leader placeholders per party are **not established named NPC canon**; replace them with sourced character records after canon audit. Core disputed demands include public security, automation, cultural identity, licensing and the costs of strategic technology. Religion and ethnic heritage are heterogeneous, not deterministic political loyalties.

## Global shocks, local outcomes

Externally supplied cards introduce AI breakthroughs, trade disruption, a reported anomalous signal, PSI research controversy and international governance. The player may adopt global technology locally, but never rewrites global science. Competing interpretations of the same incident remain possible. In the experimental slice these are small numerical modifiers, not claims about real societies or theories.

## Run

From repository root:

```sh
python -m strategy_game.local_slice --turns 12 --seed 2027
python -m unittest strategy_game.tests.test_local_slice -v
```

This runs **an explicitly provisional, deterministic Python experiment**, not an approved ruleset or a full character-driven campaign. The strategy_game scaffold and its separate placeholder RULEBOOK retain their existing contract.
