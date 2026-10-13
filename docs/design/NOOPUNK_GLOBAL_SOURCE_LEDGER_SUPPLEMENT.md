# NoöPunk: Global — source ledger supplement (Sigma Theory, Shadow Government Simulator, upgraded retrievals)

**Status: noncanonical working note.** This supplements [`NOOPUNK_GLOBAL_SOURCE_LEDGER.md`](NOOPUNK_GLOBAL_SOURCE_LEDGER.md); it does not replace or edit it. It adopts no mechanic, changes no other document, and approves nothing. Not guarded by any test (per `AGENTS.md` and [#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Why it exists.** [#338](https://github.com/TomiToivio/NooPunk/issues/338) states its central claim as *"We can simulate the entire Earth with less complexity than a detailed city… Study the strategic abstraction of **Sigma Theory** and **The Shadow Government Simulator**"*. In the merged design work those two products carry a single table row each (`strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md` lines 75–76) and appear **zero** times in `NOOPUNK_GLOBAL.md` and in the source ledger — yet they are the existing commercial proof of the issue's own core insight. This note records their mechanics at the ledger's own depth, and upgrades two retrievals the ledger marks more pessimistically than the public pages warrant.

## Method and status labels

Same convention as the ledger: **VERIFIED** — mechanics described on the product's own page were read; **PARTIALLY VERIFIED** — some mechanics read, key detail behind a login/account; **NOT VERIFIED** — no mechanics reachable, nothing inferred; **BLOCKED** — retrieval refused by the server. Retrieval date: 2026-10-12. Pages fetched over HTTP with a normal browser User-Agent; a headless browser was used only where the response was a JS-only shell or a challenge page.

---

## 1. Sigma Theory: Global Cold War — `store.steampowered.com/app/716640`

**Status: VERIFIED (scope).** Store page (145 KB) read.

| Aspect | What was read |
|---|---|
| Framing | A paradigm-shifting discovery (*"the Sigma Theory"*) that only **a handful of scientists** can harness; the superpowers race for it. *"You are placed at the head of your country's Sigma division."* *"It's a cold war out there."* |
| Roster | *"recruit a team of **four special agents** from **50 unique unlockable characters**"*, each with *"story, motivations and traits"*; archetypes include *"investigator, soldier, hacker, seducer"*. |
| Missions | Assign agents *"missions around the world to gather scientists, discover compromising documents on local politicians"*; seduce, manipulate or bribe targets, or neutralise them; *"turn-based exfiltration phases through the world's greatest capitals"* with drone support. |
| Counter-espionage | Enemy nations run agents against you: *"Track, capture and interrogate them… then exchange them for ransom."* |
| Relations | *"Develop and manage your relations with **over 100 NPCs**: lobbies, armed groups, politicians"* via flattery, threats or blackmail; lobbies *"may turn on you"*. |
| Breakthroughs | Rally scientists to *"discover new technologies"* — mind control, economic destabilisation, robot soldiers, immortality — then *"keep these discoveries for yourself or share them with the world"*. |

- **Mechanical lesson.** Planetary-scale rivalry is expressible with a **tiny cast**: four agents, a world map of named capitals and roughly a hundred relationship dials — **no country simulated in detail**. This is the issue's core insight already demonstrated by a shipped game, and the strongest available argument that Global's scope can be reached by *higher abstraction* rather than by generating a planet.
- **Non-goals (do not copy).** Its per-mission tactical pursuit and exfiltration minigames. If abstraction is the goal, detailed per-mission slices are the first thing to cut.
- **Correction to ids in circulation.** `app/1002370` **redirects to the Steam homepage** and is not a Sigma Theory page. The correct id is **`716640`**, found via Steam store search and confirmed by page title.

## 2. The Shadow Government Simulator — `store.steampowered.com/app/1281190`

**Status: VERIFIED (scope).** Store page (155 KB) read.

| Aspect | What was read |
|---|---|
| Framing | Turn-based strategy as a shadow organisation pursuing global domination *"via bribery, intimidation, seduction, and any means necessary"*; explicitly *"inspired by old classics like **Plague Inc.** and modern gems like **The Shrouded Isle**"*. |
| Fog-of-war discovery | Entering a nation you are *"alone with just a headquarters… and minimal information"*; you *"send your tendrils throughout the region uncovering **who are the influential and how much power they truly wield**"* and *"discover their **traits and personalities**, earning an understanding of their weaknesses"*. |
| Edges are the prize | *"you'll discover **who they are connected to**, and thus person by person, you shall take over the whole elite."* |
| Growth vs visibility | *"Having a strong interconnected network is the key to success, but the bigger you get the more visible you are and this could lead to your demise. **Manage your network, cut and create connections**, to ensure you act from the shadows."* |
| Influence accrual | Converting discovered elites person by person; captured units can be re-traited (*"change their abilities, unlocking new traits"*); conquered nations become commandable. |
| Escalation | Growth raises visibility; *"The world's countries will unite against you and you will face off against **rival organizations**."* |
| World structure | Regions offer *"different bonuses, but also present different challenges"*; regional networks are *"**procedurally generated**"* with time-based modifiers; faction unlocks after world conquest. |

- **Mechanical lesson.** Make **the influence graph itself the discovery layer**: nodes (elites) and edges (who-is-connected-to-whom) start hidden, are uncovered by play, and are then cut or created — with **growth-versus-visibility as the core tension**. That is a directly reusable rule shape for a Castellsian network board, and it is the one mechanic in the reference set that makes *hidden information* structural rather than decorative.
- **Non-goals (do not copy).** Its procedurally generated networks and regional modifiers. They make the world disposable and unauthored, which is the wrong foundation for a fiction-first setting that needs a fixed, hand-authored power map.
- **Correction to ids in circulation.** `app/1401920` is **a different game** (*Chinatown Detective Agency: Day One*, confirmed from page title and description). The correct id is **`1281190`**, found via Steam store search and confirmed by page title.

## 3. Upgrade: Fantasy Parliament — the between-elections mechanics are public

The ledger records Fantasy Parliament as **PARTIALLY VERIFIED** because *"the product is account/login-based"*. That is true of three routes only. `/career-lander`, `/` , `/how-to-play` and **`/mp-mode/welcome` are HTTP 200 and public**, and the last two document the between-elections economy in detail.

**Upgraded status: the between-elections mechanics are VERIFIED (scope) from public pages; internal numbers behind the account gate remain unverified.**

| Aspect | What was read (public pages) |
|---|---|
| Month economy | *"Every month is four weeks of action points. Short jobs take a week or two and can each be done once; the set pieces take the month; Party HQ is free alongside everything."* |
| Legislature | *"Every month the House sits on a real bill."* As a backbencher the whips name your lobby and *"the book remembers rebels"*; as leader the whip is yours — Aye, No or a free vote, one-line or three-line, *"with a live estimate of how many of your bench will follow"*. *"Rebellions cost authority; a government beaten on a whipped vote is a crisis."* |
| Party machine | Party HQ: membership fees feed the membership roll; marginals reports; activist teams; a donor book *"with backlash when fees/algorithms overreach"*; party pillars attract joiners. |
| Media | The console offers *"Fifteen outlets, per-platform messaging, message tests"*, with goodwill tracked *"by voter archetype, mapped onto every seat's mix"*. Everything AI-scored: *"a newspaper writes tomorrow's front page about what you actually did"*, and *"old decisions come back months later as news"*. |
| Small parties | *"every seat score is docked until credibility is earned"* and *"the party stands only where it has a branch"*. |
| Elections | Selection three months out; a live count of all 650 seats *"with a bandwagon that turns a clear lead into a majority"*; hung parliaments (partner / govern alone / vote again); snap elections and referendums *"one per parliament"*; leadership contests via *"letters, hustings, ballots"*; floor-crossing; a full historical record. |
| Career Mode | Weekly decision scenarios with editable suggested responses; *"Face authentic reactions from voters, media, and your own party"*; an explicit fail-state — *"Lose the party, lose your job"*; a flagship national policy to reset the agenda where *"too early and you waste leverage — too late and you may not survive"*. |

Still **403 login-gated, nothing summarised:** `/party-tycoon/`, `/career`, `/mp-mode/`.

- **Mechanical lesson.** Between-elections play is a **time-budgeted action economy** plus free-text decisions scored against persona factions — and stakeholders that can **remove** the incumbent rather than merely disapprove. The removal mechanic is the part most worth studying: it makes internal party standing a real risk surface rather than a progress bar.
- **Non-goals (do not copy).** Britain as default physics — the 650-seat Westminster map, whip/lobby machinery, press-gallery scoring, and the real-MP fantasy-league meta layered on top.

## 4. Upgrade: Fantasy President Career — ~30 public wiki pages

The ledger records this as **PARTIALLY VERIFIED** with *"deep numbers and the login-gated career state not verifiable"*. Its own **public wiki** is extensive, and the between-elections model below was read from it directly.

**Upgraded status: the between-elections model is VERIFIED (scope) from public wiki pages; the login-gated career state and internal balance remain unverified.**

| Aspect | What was read (public wiki) |
|---|---|
| Modes | Presidency — a four-year term on **monthly turns** (weekly with "Weekly Pacing"); Career Mode — start 1990–2025 as private citizen, state legislator, Congress member, governor, senator or President. *"Losing an election sends the career back into that world rather than ending it."* |
| The month | An event → a typed policy response, auto-classified as legislation / executive order / diplomatic / military / statement / personnel. *"Every persona in the era's focus group reacts… and scores it from 1 to 100, **judging its direction rather than its size**."* Three press headlines from the left, centre and right papers. Consequence events are *"queued to land one to three months later"*. |
| Month close | Blends persona scores into approval, applies stakeholder passive effects and favour thresholds, *"derives government and party stability from the stakeholder scores"*, resolves waiting bills, advances the calendar. |
| Checks | Legislation → Congress → Supreme Court → cabinet, in mechanism-dependent order, with outcomes **Passed, Modified, Blocked or Defied**. Own-party members *"are more likely to break ranks on a bill that is extreme"*; opposing-party members cross over on bipartisan bills. Court challenge probability scales with extremism. Statements and personnel orders bypass checks entirely. |
| The career board | A monthly schedule of **90 activities** across Ground / Press / Party / Money, costing **1–3 action points**; ground activities run at 1–3 "pips". Your own words are carried by most activities, *"judged by every voter in the game's current cast"*, with **no instant feedback** — the verdict arrives in the monthly debrief *"as named reactions, worst first"*. The same words are judged differently per setting, and **re-judged afresh after October 2001**. |
| Party machine | *"not a single meter"* — named officials (state chair, county chairs, sitting legislators), each a stranger / someone aware of the player / someone who has met the player, each with an individual opinion *"from hostile to warm"* that moves with what the player says publicly and how meetings go. Arguments damage standing, worse across party wings. Periodic **party requests** naming subjects; ignoring them *"damages the player's standing with everyone in the party who knows them."* |
| Money | Two accounts. The personal account *"can't go below zero"*, and the first overdraft *"becomes a state-news story"*; later months that pay less than they cost **drain action points**. Overspending trims the month's most expensive activities. |
| Recognition & favourability | Two **0–100** numbers tracked **per persona per state**; all other readings are views on the same record. Favourability moves *only* from what you actually say, *"in proportion to how much of that month's exposure they actually received"*. |
| Races | Strength = recognition + favourability among the seat's party voters. *"There is no separate counter for campaign effort."* |
| Stakeholders | *"Each group has a score that reacts to every policy. The score is a **weighted average of the reactions of the individual voters who make up the group**."* Era-specific lists (the 1950s page lists 21, including AFL-CIO, US Chamber, Dixiecrat Bloc, Pentagon, FBI, NAACP, AMA). |

- **Mechanical lesson.** This is the most complete documented model of *politics between elections* found in this research, and it answers the issue's own requirement directly. Three transferable shapes: **(i)** a policy is judged by an audience **on direction rather than magnitude**, which is how a non-numeric politics stays legible; **(ii)** consequences are **queued one to three months out**, so feedback is delayed and news-mediated rather than instant; **(iii)** party elites are **named individuals with independent opinions** — *"not a single meter"* — whose dissatisfaction can end a career. Point (iii) is the direct remedy for the "increase influence button" failure the issue names.
- **Non-goals (do not copy).** US institutions as universal rules — the electoral college, the fixed midterm/re-election calendar, the cabinet/SCOTUS structure, era-specific personas and hard-coded historical dates (the 9/11 re-judgement). Career Mode is also self-labelled beta and its monetisation is heavy.

## 5. Access report and blockers (this retrieval)

| Product | This retrieval | Note |
|---|---|---|
| **Poliwave** | **BLOCKED** — HTTP 403 on both `www` and the apex with a browser User-Agent; a headless browser reached only a **Cloudflare challenge**; the Wayback availability API returned **zero snapshots**. | The sibling ledger records **WELL VERIFIED (scope)** from `poliwave.com` and `/game`. I could not reproduce that access and do not dispute the reading — it may be transient or User-Agent dependent. Recorded so the reliability column can rest on a page that is retrievable on demand; worth one re-check. |
| **Fantasy Parliament** `/party-tycoon/`, `/career`, `/mp-mode/` | **403 login-gated** (server-side, via HTTP *and* headless) | Nothing summarised from these routes. |
| **Politics Simulator** | **NOT VERIFIED** | A 5.7 KB JS-only SPA; a browser renders the landing page, but **no mechanics documentation exists publicly** and the blog is satirical fiction. Consistent with the sibling ledger; nothing inferred. |
| **Geo-Political Simulator 2026** | Feature scope read; **model quality not assessed by me** | The sibling ledger's caveat is the stronger and correct one: the feature list is documented but the simulation's trustworthiness is disputed (~48% mixed reviews), so it must **not** be endorsed as a model. |
| **eversim.com** | **Not read** | TLS certificate validation failed and an insecure-SSL retry was refused. The Steam page was complete for scope purposes. |
| **Cultist Simulator timers / micromanagement** | Not on the Steam page | The sibling ledger corroborates both from third-party reviews, which is the better sourcing; the Steam page alone does not state them. |

**Id corrections worth propagating:** Sigma Theory **`716640`** (not `1002370`, which redirects to the Steam homepage); The Shadow Government Simulator **`1281190`** (not `1401920`, which is *Chinatown Detective Agency: Day One*). Both confirmed by page title and independently identical to the ids cited in `strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md`.

## 6. What this note does **not** do

- It adopts no mechanic, sets no number, and approves nothing.
- It claims nothing that was not read: the four "upgraded" retrievals name exactly which pages were public.
- It ranks nothing and replaces nothing; the merged design documents remain the artefacts.
- It is not guarded by any test — documentation is reviewed editorially, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).
