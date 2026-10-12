# Ukweli — local scenario (issue #324, deliverable B)

**Status:** scenario document. Every statement below is marked **CANON** (recovered from project sources — see [`../design/ISSUE_324_UKWELI_CANON_REUSE.md`](../design/ISSUE_324_UKWELI_CANON_REUSE.md)) or **PROPOSAL** (new, awaiting author approval). Nothing here is a mechanic; no rule, number or engine behaviour is defined. Documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Scope:** the *local* scenario for the strategy MVP — one city, its districts, the surrounding islands and limited coastal environs. **The world is global; the game board is local.** Ukweli is a republic with a wider world beyond the map, and that world enters as institutions, background conditions and event effects, never as a playable globe.

---

## 1. The republic

**CANON — the state.** The **People's Republic of Ukweli**: an Indian Ocean island republic, formally named for its communist independence tradition and the longevity of its governing party, **not** a present-day one-party state. Five centuries of cosmopolitan Indian Ocean exchange — a major entrepôt linking East Africa, India, the Arabian Peninsula and East Asia. Indigenous Swahili-speaking majority, with Omani Arab, Portuguese, British, Indian and Chinese minorities and mixed communities produced by trade, migration and colonial rule.

**CANON — history.** A fictional chronology: **Omani Arab domination → Portuguese colonial rule → British colonial rule → independence in 1964.** The sequence is an alternate fictional chronology, and does not reproduce Mombasa's actual historical order. At independence the **CPU** forms the government and aligns with both the Soviet Union and China while retaining functional relations with Britain and the United States. Later Chinese-style market reforms, industrialisation and export-oriented investment mix state-led development with private enterprise. After the Soviet collapse Ukweli becomes a **genuine multiparty liberal democracy** — competitive elections, civil liberties, independent media, courts, viable opposition rights — and the CPU **keeps winning democratically**, on durable popularity and a credible social-development record.

**CANON — the setting's own joke.** Outsiders hear "People's Republic" and picture Cuba-style isolation; Ukweli is a prosperous, open, internationally networked multiparty democracy. *"Not quite Cuba, comrade."* The joke is load-bearing: it is how the scenario tells the player not to trust the formal name.

**PROPOSAL — not a utopia.** The scenario should carry legitimate criticisms and live tensions, or the setting is propaganda. Candidates: enclave inequality around New Ukweli, the governing party's incumbency advantage as an unresolved question rather than a settled virtue, and the labour relations of the foreign-owned shipping sector.

---

## 2. The city and the islands

**CANON.** The arena is **one modern coastal/port capital with several surrounding islands**; national and global forces arrive as institutions, background conditions and event effects. **New Ukweli** is the glossy, high-rise, high-connectivity modern port/CBD. Older quarters, fishing communities, outer islands and rural areas experience **uneven** infrastructure, wealth, public services and exposure to global markets.

**CANON — inspirations, as dynamics.** *Mombasa* — a working port, Indian Ocean trade routes, Swahili coastal heritage, mainland–island connections. *Zanzibar* — archipelago geography, dense historic quarters, maritime cultures, tourism and religion. *Mumbai* — scale contrast, migration, finance/media/technology beside informal economies and sharply differing neighbourhoods, **borrowing the dynamics and not the megacity scale**. *Singapore* — shipping and logistics hubs, modern infrastructure, finance, international connectivity and tensions around technocratic governance, **without importing its exact political model**. The inspirations span different societies, histories and political systems; the city is culturally and politically specific on its own terms, and must not paste recognisable districts or caricatures onto it.

**CANON — an exclusion island.** Ukweli's local shamanic traditions, folk religions and island mythologies contain stories read within the fiction as related to NHI, PSI and anomalous experience. There is an **exclusion island** in the setting. The traditions are original and are to be written with the same care as the rest of the setting; their *mechanics* are unapproved.

**PROPOSAL — board size.** **6–8 abstract playable locations**, e.g. old harbour/historic quarter; CBD and government district; mixed-income residential neighbourhoods; university/hospital/technology cluster; industrial port and logistics zone; outer island with villages and tourism; strategic island with airfield and communications facilities; nearby coastal or rural hinterland. These are **illustrative placeholders, not established place names** — the named list, routes and access costs are deliverable **C**, and C is blocked on the Eldrich Island / Freedom Colony question ([reuse inventory](../design/ISSUE_324_UKWELI_CANON_REUSE.md) §4.3).

**PROPOSAL — connection model.** Islands link by **simple ferry, bridge or boat links with access costs**, not pathfinding or a maritime simulator. A "district" may be a mainland neighbourhood or an entire island; both use the same small location model.

---

## 3. Economy and the wider world

**CANON — pillars.** Fishing, farming, tourism, shipping and logistics, a modern port and international airport, export manufacturing (historically sweatshops, now also advanced and high-tech products), services, finance and telecommunications, and local technology adoption.

**CANON — connectivity as infrastructure.** Port, international airport, **undersea internet cables**, an extensive fishing fleet (thousands of boats), satellite internet and television, and global mobile networks. These are **infrastructure and network nodes with vulnerabilities**, not individual units to be modelled one by one.

**CANON — the shipping corporation.** A **world-leading shipping corporation** — within the fiction the world's largest — controlled by an **eccentric British aristocrat**: the **Eldrich Corporation**, successor to the Eldrich Colonial Shipping Corporation, headed today by **Sir Mars Eldrich**, Ukweli's richest citizen and among the world's wealthiest. He publicly meddles in politics, funds the libertarian party and sympathetic media, and is obsessed with colonising Mars. **Ownership of a global corporation is not sovereignty over the port.**

**CANON — world connections.** Ukweli's significance is as a globally networked Indian Ocean crossroads: trade routes, cables, migration and the attention of outside powers. The wider world beyond the map is **not simulated**.

---

## 4. Institutions

**CANON.** Institutions enter abstractly: council, administration, police, civic associations, courts, independent media, universities and religious bodies. The republic is a functioning liberal democracy, so these are live contested institutions rather than a facade.

**PROPOSAL — institutional play.** Each major institution should be reachable by faction influence through ordinary politics — appointments, budgets, media, association — with its **independence contested rather than assumed**. Luhmann-inspired institutions, Castells-inspired communication networks and Laclau-inspired ideological claims enter as **simple district-level mechanics**, to be designed separately and approved before implementation (S0-A).

---

## 5. The three parties

**CANON — exactly three playable parties at MVP.** *"V1 is three political parties, not eleven global playable factions."* A global faction may appear **only** through one character, a news event, an alliance, a clandestine cell or scenario-specific pressure. The initial setup is not to be replaced or expanded.

| Party | Role | Source |
| --- | --- | --- |
| **CPU — Communist Party of Ukweli** | incumbent national-liberation government; governs by winning elections | #325, #328 §7 |
| **UIP — Ukweli Identity Party** | ethnic-nationalist and rural-populist challenger | #325, #328 §7 |
| **LFP — Libertarian Freedom Party of Ukweli** | libertarian enclave, tycoon-sponsored; funded by Sir Mars Eldrich | #325, #326 |

**Name note (§4.2 of the inventory, awaiting your word):** `GLOBAL_FACTIONS.md` §5 and `global_factions.json` call this party the **ULP — Ukweli Libertarian Party**. This document uses **LFP**, because both the dedicated setting issue and the character issue use it, and #328's precedence ruling concerned the global-faction register. If ULP is preferred, this table and the inventory change together.

**CANON — affinities are tendencies, not memberships.** CPU's likely currents are establishment-pragmatic **Critical** and public-interest **Cyborgist**, defending sovereign human institutions — **not** automatically Majestic or Confederacy. UIP's strongest potential affinity is **Doomer / Human Sovereignty** networks, especially after disruptive NHI events — and UIP, Swahili identity and religious affiliation can never be equated with one uniform NHI stance. LFP's likely alliance is **Accelerationist** trade and technology, with Eldrich-linked private-sector networks. **Every party begins as a recognizable party or civic movement**, and organisational tendencies may evolve into religious, populist, militant, survivalist or illicit forms through play — *without new engines*.

**CANON — four things that must stay distinguishable.** A party's declared manifesto, a leader's hidden allegiance, a covert sponsor, and the actual voter base are four different things. Organisational membership is never forced: outside networks recruit *individuals* inside mainstream parties, civil services, military, science and corporations, without the party itself becoming them.

**DEFERRED — the leaders.** Four leaders per faction, Terra Invicta-style assigned missions and CK3-style portfolios and relationships, are [#323](https://github.com/TomiToivio/NooPunk/issues/323)'s and [#326](https://github.com/TomiToivio/NooPunk/issues/326)'s deliverable. **This issue names no leader.**

---

## 6. Social cleavages

**CANON — how to write communities.** Ukweli's ethnic and religious composition is **multidimensional**. Ancestry must never be presented as determining ideology, religion, class or political loyalty, and communities are **never fixed blocs or default antagonists**. This is the specific failure the setting's own history warns against.

**CANON.** Colonial legacies persist in law, architecture, language, capital, property and class. Uneven development separates glossy New Ukweli from older quarters, fishing communities, outer islands and rural areas.

**PROPOSAL — starting tensions.** Plausible, ordinary and non-exotic: port labour versus logistics automation; land and heritage in the historic quarter versus development; the cost of living and housing in New Ukweli; education and health access between the capital and the outer islands; the political meaning of foreign-owned infrastructure; and the slow, contested normalisation of PSI talk, from folklore to clinic to law.

---

## 7. The 2027 starting conditions

**CANON.** The crossover starts **around 2027**, during the **acceleration toward** the NHI Crisis — everyday institutions and electoral politics first, growing stranger as the AGI, NHI-disclosure and PSI shocks accelerate. The NHI Crisis is **not resolved** and is **not dated**. Global AI, NHI, PSI, market and geopolitical developments arrive as **external event cards and modifiers**.

**CANON — three complexes, three lenses.** The scenario reads paradigm-shift pressure through three overlapping complexes (soft/Archaic Revival, hard NHI/UAP, hard AI and human transformation) and through the Luhmann / Castells / Laclau lenses — used as **inspiration and legibility, never as a validated predictive law**.

**CANON — no post-crisis imports.** A developed UN parliament, UNSA, the UNSA Helsinki agent RPG, the Breakaway Civilization as an established actor and any post-crisis political order **do not exist at the start**. Where they appear, they are continuity hypotheses, not givens.

**PROPOSAL — local research.** "Research" in the scenario means **acquiring, adapting and deploying** global science and technology locally, and contesting its political meaning — not launching civilisation-changing global R&D.

---

## 8. What this document deliberately does not do

- It defines **no** named location, route, cost, starting value, event card, leader, NPC or polarizing-issue list. Those are deliverables **C–E**, and the inventory records them as genuinely new (§3.4).
- It adds **no** rule, statistic, number or mechanic, and changes **no** engine or data file. It touches no file owned by [#325](https://github.com/TomiToivio/NooPunk/issues/325), [#326](https://github.com/TomiToivio/NooPunk/issues/326), [#327](https://github.com/TomiToivio/NooPunk/issues/327), [#328](https://github.com/TomiToivio/NooPunk/issues/328) or [#329](https://github.com/TomiToivio/NooPunk/issues/329).
- It resolves **none** of the inventory's flagged conflicts. Those are your rulings.
- It carries **no** automated test: lore and design documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Acceptance position.** This document satisfies #324's deliverable B and the acceptance criteria *one modern city, multiple islands, 6–8 simple locations* / *Indian Ocean influences recognisable without one-to-one copying* / *geography, culture and politics remain scenario data, not engine assumptions* — **as design**. The criteria that need a running artefact (the deterministic prototype, the playable vertical slice, the integration into README/site/launcher) belong to deliverables **F** and **G** and are not claimed here.
