# NoöPunk: Global — source verification ledger (companion to NOOPUNK_GLOBAL.md)

**Status: noncanonical working note.** This is the raw evidence behind the seven-simulator comparison matrix and the two tabletop models in [`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §6 and §8. It exists so the reliability column can be *checked*, and so nothing is described from plausibility. It adopts no mechanic, and it changes no other document.

**Method.** For each product I retrieved its **own** page(s) and, where possible, third-party reviews. The status labels are:

- **VERIFIED** — mechanics described on the product's own page (or two independent descriptions) were read.
- **PARTIALLY VERIFIED** — some mechanics were read, but key detail sits behind a login/account or is undocumented.
- **NOT VERIFIED** — no mechanics reachable; only marketing copy; **nothing is inferred**.

Retrieval date: 2026-10-12.

---

## Seven political simulators

| # | Product | URL(s) reached | What was actually read | Status |
|---|---|---|---|---|
| 1 | **Fantasy Parliament / PM Career** | `fantasyparliament.co.uk/career-lander`, `/mp-mode/welcome`, `/parallel-parliament` | weekly decisions/crises; party factions can remove you; leadership contests (letters/hustings/ballots); cabinet & shadow-cabinet scores; monthly bill, whips, free vote, one-/three-line whips; party HQ (membership fee, donors, marginal research, activist teams); AI-scored speeches + front pages; an AI "policy tester" scoring policies across demographic groups | **PARTIALLY VERIFIED** — feature pages read; the product is account/login-based; internal numbers not verifiable. **Naming ambiguity:** a BBC article describes the same domain's *Fantasy Parliament* as an MP-drafting fantasy league; the PM-career is a distinct mode. |
| 2 | **Politics Simulator** | `politics-simulator.com` | only the marketing landing: "from activist to head of state", "lying/betraying/manipulating", "geopolitics", "resources", satire; site claims 47,832 "politicians" etc. | **NOT VERIFIED** — no mechanics reachable without an account; **not described from plausibility**. The name also collides with an unrelated itch.io card game ("Politics Simulator" by rigour/ambadoom). |
| 3 | **Fantasy President Career** | `fantasypresidentcareer.com` | Career Mode 1990–2025, month-by-month, any state; start as governor/state legislator/Congress/senator/president/outsider; legislative desk (bill calendar, votes, floor speeches, committees, your own bill); governor's desk; presidency takes over the same career; a monthly "character sheet"; Wikipedia page generation; "Fed Chair" mode described as an early, untested reskin of another mode; subscription £5.99/mo, £59.99/yr | **PARTIALLY VERIFIED** — own site read at moderate detail; deep numbers and the login-gated career state not verifiable. |
| 4 | **The Political Process** | `store.steampowered.com/app/1184770`; third-party review | turn-based; create a character; run for office up the hierarchy; write legislation; balance budgets; 600+ procedural politicians with ideologies; primary + general elections simulated for every politician; 100+ metrics responding to policies; **no win conditions**; **no tutorial**; Early Access; planned (not present): diplomacy, international relations | **VERIFIED (scope).** |
| 5 | **Geo-Political Simulator 2026 Edition** | `store.steampowered.com/app/4021780`; reviews (Virus.hr, GamingWithNoobs, Steam) | play as head of state **or opposition**; regime censures (motion against head of state, constructive no confidence, dissolution, confidence vote, Art. 49.3); party AI forms/dissolves coalitions, changes leaders, creates parties; parliaments reproduced; electoral-threshold legislation; G20 worldwide laws; 600+ data elements for 175 countries, real-time; AI/robotics employment impact; DLC God'n Spy + Modding Tool | **MIXED.** Feature/scope list **verified**; but the *simulation's trustworthiness* is **disputed** — Steam ~48% mixed, reports of crashes, opaque UI, "mechanics feel random", "reskin" criticism. Feature list recorded; model quality **not** endorsed. |
| 6 | **Global Election Simulator** | `globalelectionsimulator.com` | country-by-country election simulators; begins from the real latest result; each explains its own electoral law; move party/candidate support by slider; map + parliament update live; live election-night count by batch; historical + imaginary scenarios; educator/journalist focus | **VERIFIED (scope).** It is an **electoral explainer**, not a between-elections/party sim. |
| 7 | **Poliwave** | `poliwave.com`, `poliwave.com/game`, `poliwave.com/simulator`, `/contest` | seat projections from polls + swing model; Monte Carlo ranges (Pro); 195 jurisdictions, 18,990 simulatable elections; district drawer; map maker; scenario save/share; a campaign minigame "**Landslide** — take a party through a full campaign"; poll averages; built by one person | **VERIFIED (scope).** It is an **election-forecasting platform** with a campaign game, not a between-elections political sim. |

### Notes on the reliability column

- Only products **2** is **NOT VERIFIED**; nothing about its mechanics is asserted in the matrix.
- Products **1** and **3** are **PARTIALLY VERIFIED** (own pages, but account-gated depth).
- Products **4–7** are **VERIFIED for their stated scope**, with **5** carrying an explicit caveat that *scope is documented but model quality is disputed*.
- The issue's own guidance — *"verify mechanics before adopting"* and *"assuming inaccessible/unverified details"* — is honoured by recording these statuses rather than estimating.

---

## Two tabletop / card models

| Model | URL(s) reached | What was actually read | Status |
|---|---|---|---|
| **Dune: Imperium** | `store.steampowered.com/app/1689500`; rules guide (boardgamemate.com); BGG blog; GeekDad | hybrid **deck-building + worker placement**; each round a 5-card hand split between *Agent turns* (cards send agents to board spaces via icons) and a *Reveal turn* (remaining cards give Persuasion to buy cards and Swords for the round's Conflict); **4 faction Influence tracks** with alliance tokens that transfer on overtake; a **Conflict deck** of 10 rounds with graduated rewards by strength; first to 10 VP (round played out); resources spice/solari/water; solo "House Hagal" automa | **VERIFIED** — multiple independent descriptions agree on the mechanic shape. |
| **Cultist Simulator** | `store.steampowered.com/app/718670`; Indie Game Website review; Steam discussions | **cards are nouns** (people, cultists, emotions, tools, books) with "aspects"; **tiles are verbs** (study/explore/work); place a card in a verb slot to start a **real-time timer**; combinations yield unfolding narrative/recipes; permadeath; different characters; **no tutorial** | **VERIFIED.** Practical drawbacks corroborated by reviews: opaque/no tutorial, real-time timers vs thinking, micromanagement, "not knowing the objective". |

**Drawbacks captured for §6/§8 of the main document**

- *Dune: Imperium:* large component count and table footprint; upkeep of four influence tracks + conflict + intrigue in every round; 60–120 min; the conflict deck's randomness; turn order largely fixed by a rotating first-player marker; it is **not** a politics-between-elections sim (its analogue is *influence tracks*, not legislatures).
- *Cultist Simulator:* opaque onboarding; real-time timers interrupt thinking; repetitive card micromanagement; permadeath discards progress; scattered board with weak organisation. These are exactly the failure modes a NoöPunk card layer must avoid.

---

## What this ledger does **not** do

- It does not adopt any mechanic.
- It does not claim any unverified detail.
- It does not rank the products; it reports what was read.
- It is not guarded by any test (per [AGENTS.md](../../AGENTS.md) and [#271](https://github.com/TomiToivio/NooPunk/issues/271)).
