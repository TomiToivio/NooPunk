# Ukweli — history, society, factions and simulation relevance (issue #325)

**Status: design record, proposal-marked throughout.** It decides no canon question, defines no
rule, number, threshold, cost or engine behaviour, and touches no engine code.
`strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**, and #325's own material sits behind
the S0-A design gate (`docs/design/VISION.md` §7). Lore and design documents are reviewed
editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**What this file is, and why it exists.** Issue #325 asked, across one brief, for the republic's
**history, society, factions and their simulation relevance** — the whole setting as one playable
unit. Its individual deliverables have since been answered by sibling artefacts, each owning one
piece and each landed on `main`. What was still missing is the **consolidation**: one record that
says what is settled canon, what is proposal, what each element *gives the simulation* rather than
just the reader, and which questions remain the author's. This file is that record. It **cites**
the siblings rather than copying them, so no second copy of any of them forks the record.

---

## 0. Where each of #325's deliverables already landed

Every row below is on `main` and is **cited, not restated**. This record adds no new setting entity,
person, place or date.

| # | Deliverable (#325) | Where it lives | Register |
| --- | --- | --- | --- |
| 1 | Canon/lore recovery, keep/adapt/replace with sources | [`ISSUE_324_UKWELI_CANON_REUSE.md`](ISSUE_324_UKWELI_CANON_REUSE.md) | **met** — the all-refs and warehouse audit; establishes that no older Ukweli material survives |
| 2 | Setting bible, established-vs-proposed marked | [`../world/PEOPLES_REPUBLIC_OF_UKWELI.md`](../world/PEOPLES_REPUBLIC_OF_UKWELI.md) | **met** |
| 3 | Modern map specification + data-driven location/network schema, 6–8 nodes | [`ISSUE_324_UKWELI_GAP_CLOSURE.md`](ISSUE_324_UKWELI_GAP_CLOSURE.md), [`../../strategy_game/data/ukweli_local.json`](../../strategy_game/data/ukweli_local.json), [`../../strategy_game/data/city_scenario_schema.json`](../../strategy_game/data/city_scenario_schema.json), [`ISSUE_324_ACCEPTANCE.md`](ISSUE_324_ACCEPTANCE.md) | **met as structure**; the island placement and its legal relation stay OPEN (§8.3–§8.4) |
| 4 | Political design: party profiles, institutions, population/media/corporations, NPC roster | §4 below; [`ISSUE_326_UKWELI_LEADERS_AND_NPCS.md`](ISSUE_326_UKWELI_LEADERS_AND_NPCS.md), [`../../strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md`](../../strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md), `ISSUE_328_*`, `ISSUE_329_*` | **met for parties and the people owned by #326**; the non-leader cast is still unowned (declared blank §4) |
| 5 | Theory-to-mechanics table (Laclau, Castells, Luhmann) | §7 below; consumed from `NOOPUNK_GLOBAL.md` §7, `POPULISM_PATRONAGE_AND_REALIGNMENT.md`, `POLITICAL_SIMULATOR_MODEL.md` | **proposed** (#325's own proposal comment); the gates still own it |
| 6 | Global events & NHI mysteries, local effects, government/public perspectives | §5 and §7; `ukweli_local.json` `shocks`; `strategy_game/data/paradigm_event_seeds.json` | **met small by design** |
| 7 | Playable scenario spec + 10–12-turn example | `strategy_game/local_slice.py`, [`../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md`](../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md), `ISSUE_322_MVP_LOCAL_CITY.md` | **met as a provisional deterministic slice, not an approved ruleset** |
| 8 | Docs integration (README, site, #324) | `strategy_game/README.md`, `docs/index.html` | **met** |

**What this record adds, precisely:** (a) the explicit **canon-versus-proposal split** for the history,
society and factions, statement by statement; (b) each element's **simulation relevance** — the
faction, stake, decision or relationship it gives play, not atmosphere alone; (c) the six quantities
kept distinct wherever society and politics are modelled (§7); and (d) the **four unresolved
conflicts** recorded as options for the author, factual separated from interpretation (§8). Nothing
here is promoted to canon by being written down.

---

## 1. How to read the marks

| Mark | Means |
| --- | --- |
| **CANON** | Stated by the author in the #325 brief, or already landed as authored content and cited. |
| **PROPOSAL** | This record's or the #325 proposal comment's suggestion. Nothing is ratified by writing it down. |
| **OPEN** | A conflict #324's inventory flagged for the author. Carried forward here, **not settled**. |
| **DECLARED BLANK** | A slot where a person, place or institution would be needed. Left empty on purpose (`AGENTS.md` §1). |
| **NOT RECOVERABLE** | #324's inventory established that no older Ukweli material survives anywhere, so anything outside the current material is new and marked PROPOSAL rather than "recovered". |

Provenance precedence used here: **the #325 brief**, then
[`../scenarios/UKWELI_LOCAL_SCENARIO.md`](../scenarios/UKWELI_LOCAL_SCENARIO.md) (#324 deliverable B),
then [`../world/PEOPLES_REPUBLIC_OF_UKWELI.md`](../world/PEOPLES_REPUBLIC_OF_UKWELI.md), then
[`../../strategy_game/data/ukweli_local.json`](../../strategy_game/data/ukweli_local.json), then
[`ISSUE_324_UKWELI_CANON_REUSE.md`](ISSUE_324_UKWELI_CANON_REUSE.md).

---

## 2. History — the chronology, and the liabilities it leaves playable

### 2.1 What is CANON

Each of these is verified against the cited source, not recalled:

- **The state.** The **People's Republic of Ukweli**, an Indian Ocean island republic: a prosperous,
  open, internationally networked **multiparty liberal democracy**, **not** a one-party state, with an
  indigenous Swahili-speaking majority and Omani Arab, Portuguese, British/English, Indian and Chinese
  minorities and mixed communities (`UKWELI_LOCAL_SCENARIO.md` §1; `PEOPLES_REPUBLIC_OF_UKWELI.md` §1).
- **The name is load-bearing.** "People's Republic" reflects the communist independence tradition and
  the governing party's longevity, **not** a present-day dictatorship; the setting's own joke —
  *"Not quite Cuba, comrade."* — depends on the gap (`PEOPLES_REPUBLIC_OF_UKWELI.md` §1).
- **The independence chronology.** A **fictional** alternate sequence: **Omani Arab domination →
  Portuguese colonial rule → British colonial rule → independence in 1964** — explicitly an alternate
  chronology, **not** real-world Mombasa's exact order (`UKWELI_LOCAL_SCENARIO.md` §1;
  `PEOPLES_REPUBLIC_OF_UKWELI.md` §2).
- **Nonalignment at independence (1964).** The **Communist Party of Ukweli (CPU)** forms the
  government and aligns with **both** the Soviet Union and China **while retaining functional relations
  with Britain and the United States** (`UKWELI_LOCAL_SCENARIO.md` §1; `PEOPLES_REPUBLIC_OF_UKWELI.md`
  §2). This is canon nonalignment — one founding posture, two patrons and two trading partners.
- **Five centuries of cosmopolitan exchange.** A major entrepôt linking East Africa, India, the Arabian
  Peninsula and East Asia (`UKWELI_LOCAL_SCENARIO.md` §1).
- **Chinese-style market reforms.** After the Cold War, industrialisation and export-oriented investment
  combine state-led development with private enterprise and international trade, including the
  sweatshop-to-advanced-manufacturing arc (`PEOPLES_REPUBLIC_OF_UKWELI.md` §2).
- **A genuine post-Soviet democracy — and the incumbent keeps winning.** After the Soviet collapse
  Ukweli becomes a **genuine multiparty liberal democracy** (competitive elections, civil liberties,
  independent media, courts, viable opposition rights) and the CPU **keeps winning democratically**, on
  durable popularity and a credible social-development record — **not** a sham (`PEOPLES_REPUBLIC_OF_UKWELI.md`
  §2, §6).
- **The ~2027 boundary.** The starting point is **~2027**, during the *acceleration toward* the NHI
  Crisis; the NHI Crisis is **not resolved and not dated** (`UKWELI_LOCAL_SCENARIO.md` §7).

No exact date other than **1964** and the **~2027** boundary is canon; every other year in the setting
bible is a marked **PROPOSAL** (`PEOPLES_REPUBLIC_OF_UKWELI.md` §2). This record invents no date.

### 2.2 What the history gives the simulation (PROPOSAL, from #325's own comment)

The proposal comment on #325 reads the chronology as **four inheritable bargains**, each with a
*different legal status* — because legal status is what decides who can re-open it. This record keeps
that reading and, importantly, keeps each bargain attached to a **stake a faction can spend**:

| Inheritance | CANON content it rests on | Legal status (PROPOSAL) | Simulation relevance — the stake |
| --- | --- | --- | --- |
| **The Liberation Bargain** | CPU led the independence struggle, 1964; nonalignment (above) | Written (constitution, party self-understanding) | The CPU can never *abandon* sovereignty talk, because it **is** the party's founding claim — so a rival can **capture the word instead**, which is the Laclauian move the scenario exists to teach |
| **The Commercial Bargain** | The CPU left British businesses operating; the Eldrich dynasty facilitated a negotiated, peaceful transition (`ISSUE_326_UKWELI_LEADERS_AND_NPCS.md` §2) | Written, contested, periodically leaked | The most productive fault line: the left flank can re-open it any turn, and the investment that underwrites New Ukweli can be threatened in reply |
| **The Democracy Bargain** | Genuine post-Soviet multiparty democracy; the CPU keeps winning *democratically* | Written, honestly functioning | The governing party's record must be a **variable, not a virtue** — its legitimacy is losable by governing badly, not winnable by one trick |
| **The Exclusion Bargain** | The government privately knows of recurrent strange events and has designated an island prohibited, publicly for biodiversity (§5) | **Unwritten** | The strongest single event source in the setting, precisely because **no document protects it** |

**Playable relevance, plainly:** each bargain hands a faction a *reason to act* and a *cost for
acting*, and the unwritten one leaks. None of it is atmosphere.

---

## 3. Society — a cosmopolitan majority, modelled by exposure, never by ancestry

### 3.1 What is CANON

- **Non-determination rule.** Ethnic ancestry must **never** be presented as determining ideology,
  religion, class or political loyalty; communities are **never** fixed blocs or default antagonists
  (`UKWELI_LOCAL_SCENARIO.md` §6; `PEOPLES_REPUBLIC_OF_UKWELI.md` §3).
- **The majority and the segments overlap.** The Swahili majority and the minorities are modelled
  through **overlapping** geographic, occupational, economic, linguistic, ethnic and belief segments —
  no demographic segment maps one-to-one to a party (`PEOPLES_REPUBLIC_OF_UKWELI.md` §3).
- **Colonial legacy is material, not moral.** It persists in law, architecture, language, capital,
  property and class; **uneven development** separates glossy New Ukweli from older quarters, fishing
  communities, outer islands and rural areas (`UKWELI_LOCAL_SCENARIO.md` §6).
- **Belief cuts across demographics.** Urban indifference, folk tradition, faith, scepticism,
  scam-detection and direct experience are spread across the segments, not located in one of them;
  believers and rural people are **not** portrayed as intrinsically uneducated
  (`PEOPLES_REPUBLIC_OF_UKWELI.md` §4).

### 3.2 What society gives the simulation (PROPOSAL)

The **5–7 exposure-first segments** of the #325 proposal comment, each mapped to at least two of the
eight landed locations, plus the **anti-bloc rule** as the segment model's one invariant: no segment
has a fixed party; each segment's support is a **distribution with at least two live options**; and
**any single crisis may split a segment**, so a party that owns a segment this turn can lose half of
it next turn without the segment changing at all.

| # | Segment (PROPOSAL) | Locations it lives across | Simulation relevance — the decision it opens |
| --- | --- | --- | --- |
| 1 | Port and logistics households | Old Harbor, Industrial Logistics Port | port labour versus logistics automation is a live fight over the same node |
| 2 | Ferry-dependent outer-island communities | Outer Island Communities, Coastal Hinterland | service and access decisions buy or cost a whole archipelago's support |
| 3 | New Ukweli professionals and commuters | Civic and Commercial Centre, Mixed Neighborhoods | housing and cost-of-living are the incumbency's own risk |
| 4 | Informal-quarter renters and street traders | Mixed Neighborhoods, Old Harbor | development versus displacement in the historic quarter |
| 5 | Campus, clinic and research staff | University and Hospital, Civic | research legitimacy is a resource a faction can raise or spend |
| 6 | Fisherfolk cooperatives and maritime traditionalists | Old Harbor, Outer Island Communities | conservation and maritime livelihoods pull apart on the exclusion island (§5) |
| 7 | Diaspora-remittance households | Mixed Neighborhoods, Civic | outside money and outside attention enter as an internal constituency |

**Canon versus proposal is explicit here:** the *rule* that segments must overlap and that ancestry
never determines politics is **CANON**; the specific seven segments and the anti-bloc invariant are
**PROPOSAL**, and the segments are chosen to give the CANON anti-bloc instruction something concrete
to attach to rather than restating a disclaimer.

---

## 4. Factions — three playable parties, three kinds of power

### 4.1 What is CANON

Exactly **three playable parties** at MVP — *"V1 is three political parties, not eleven global playable
factions."* A global faction may appear **only** through one character, a news event, an alliance, a
clandestine cell or scenario-specific pressure; the initial setup is not to be replaced or expanded
(`UKWELI_LOCAL_SCENARIO.md` §5; `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §5).

| Party | Canon role | Simulation relevance — the stake it holds, the decision it forces |
| --- | --- | --- |
| **CPU — Communist Party of Ukweli** | incumbent national-liberation government; governs by winning elections; not secretly a one-party regime | holds **institutional trust**; its decision is always whether to spend the Liberation Bargain's credit, and its vulnerability is **incumbency during shock** |
| **UIP — Ukweli Identity Party** | ethnic-nationalist and rural-populist challenger, contested appropriation of folk and Catholic identity | holds **grievance mobilisation**; its decision is whether to escalate uncertainty into antagonism, and its ceiling is credibility outside its base |
| **LFP — Libertarian Freedom Party of Ukweli** | libertarian enclave and tycoon-sponsored populism, financed and backed by sympathetic media of its benefactor Sir Mars Eldrich | holds **media reach**; its decision is whether to convert reach into votes (it usually cannot), and its vulnerability is vote support far below that reach |

**Four things a scenario must never merge** (CANON, from #325 and `ISSUE_324_UKWELI_CANON_REUSE.md`
§5): a party's **declared manifesto**, a leader's **hidden allegiance**, a **covert sponsor**, and the
**actual voter base**. And organisational membership is never forced: outside networks recruit
*individuals* inside mainstream parties, the civil service, the military, science and corporations
**without the party becoming them** (`UKWELI_LOCAL_SCENARIO.md` §5).

**Party ↔ global-current affinities are tendencies, not memberships** (CANON, starting tendencies
only): CPU's likely currents are establishment-pragmatic and public-interest, defending sovereign human
institutions; UIP's strongest potential affinity is Doomer / Human Sovereignty networks, especially
after disruptive NHI events — and Swahili identity and religious affiliation are **never** equated
with one uniform NHI stance; LFP's likely alliance is Accelerationist trade and technology
(`UKWELI_LOCAL_SCENARIO.md` §5; `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §7).

### 4.2 What the three parties give the simulation (PROPOSAL reading)

The three parties are **not three positions on one axis** — they hold three different *kinds* of power
(institutional trust, grievance mobilisation, media reach), which is why the same shock can strengthen
one and destroy another (`PEOPLES_REPUBLIC_OF_UKWELI.md` §6). Whether the three powers become
comparable quantities is a design question owned by the simulation spine, not by this record. The
canon test cases the issue names are kept as **model obligations**, not mechanics: the CPU stays popular
for substantive reasons; the UIP can gain traction under stress **without a guaranteed victory**; LFP
media influence can exceed its actual vote support.

### 4.3 DECLARED BLANK — the people

**No party leader is named here**, and none is invented. The twelve leader seats already exist in
`ukweli_local.json` (`cpu1`–`cpu4`, `uip1`–`uip4`, `ulp1`–`ulp4`) as **generic role placeholders**;
#326 owns the roster and deliberately left the twelve seats **empty with the institutional tie each
needs**, each marked `TODO: requires author specification` (`ISSUE_326_UKWELI_LEADERS_AND_NPCS.md` §4).
Sir Mars Eldrich is a canonical card, **not a council seat** (`ISSUE_326_UKWELI_LEADERS_AND_NPCS.md`
§2–§3). The surrounding non-leader cast (ministers, scientists, media figures, clergy, environmental
officers, contacts) is **still unowned** and is recorded as a declared blank, not filled with invented
people (`PEOPLES_REPUBLIC_OF_UKWELI.md` §7).

---

## 5. The exclusion island and the NHI/PSI register

### 5.1 What is CANON

- There is an **exclusion island**: the government **privately knows there are strange, recurrent
  events** and has designated **an entire island a prohibited/protected zone**, publicly **to safeguard
  Ukweli's unusual biodiversity and ecological heritage** (`UKWELI_LOCAL_SCENARIO.md` §2;
  `PEOPLES_REPUBLIC_OF_UKWELI.md` §5).
- The **biodiversity rationale has its own credible truth and conservation value**, "even if security is
  also involved" — **CANON**.
- The government **officially acknowledges** unusual, unexplained UFO/PSI reports and the rich local
  mythology, but **consistently denies possessing definitive or special knowledge of their causes**.
- Ukweli's **local shamanic traditions, folk religions and island mythologies** contain stories read
  in-fiction as related to NHI, PSI and anomalous experience; they are original and must be written with
  the same care as the rest of the setting, with **varied interpretations**, and must **not** make real
  ethnic or religious traditions synonymous with paranormal powers.

### 5.2 What the island gives the simulation (PROPOSAL)

Four registers, **kept apart** — representing them as one thing is what makes a disclosure plot collapse
into a single reveal: (1) **official denial register** (what the state says it knows), (2) **internal
assessment divergence** (agencies that sincerely disagree — the leak surface), (3) **conservation
legitimacy** (a real, separately winnable claim), and (4) **popular interpretation** (indifference, folk
tradition, faith, scepticism, scam-detection and direct experience, spread across the segments of §3).

**Playable relevance:** the island is a **gated location**. Opening it is a decision with **four
separable consequences** — conservation, disclosure, sovereignty and foreign attention — so a faction
can want one and not the others. That is how a serious internal disagreement inside the governing party
is produced **without making anyone a caricature**. The NoöPunk reading worth keeping: the ecology is
genuine **and** the closure is a cover, and neither fact cancels the other.

### 5.3 DECLARED BLANK — the island has no name

**No older material names the island or fixes what is on it** (`NOT RECOVERABLE`), and naming it is a
canon decision. This record does **not** name it.

---

## 6. Economy, infrastructure-as-nodes and the Eldrich Corporation

### 6.1 What is CANON

- **Economic pillars:** fishing; farming; tourism; shipping and logistics; a modern port and
  international airport; export manufacturing (historically sweatshops, now also advanced and high-tech
  products); services; finance and telecommunications; and local technology adoption
  (`PEOPLES_REPUBLIC_OF_UKWELI.md` §7).
- **New Ukweli** is the glossy, high-rise, high-connectivity modern port/CBD; **uneven development**
  is CANON (`UKWELI_LOCAL_SCENARIO.md` §2–§3).
- **Connectivity as infrastructure, not units:** the port, international airport, **undersea internet
  cables**, an extensive fishing fleet (thousands of boats), satellite internet, satellite television
  and global mobile networks are modelled as **network nodes and vulnerabilities**, **not individual
  units** (`UKWELI_LOCAL_SCENARIO.md` §3).
- **The Eldrich Corporation** — the world-leading shipping corporation, successor to the **Eldrich
  Colonial Shipping Corporation**, controlled by the eccentric British aristocrat **Sir Mars Eldrich**
  (`UKWELI_LOCAL_SCENARIO.md` §3; `ISSUE_326_UKWELI_LEADERS_AND_NPCS.md` §2).
- **Ownership is not sovereignty.** Ownership of a global corporation is **not** sovereignty over the
  port — carried as an explicit guard on the landed card (`UKWELI_LOCAL_SCENARIO.md` §3;
  `ISSUE_326_UKWELI_LEADERS_AND_NPCS.md` §3).

### 6.2 What the economy gives the simulation (PROPOSAL)

The landed map reads the economy as eight locations and seven routes; **Airfield Island** is the
connectivity node (tag `communications`), and the **port, the airfield and the cables are the state's
three chokepoints** — nodes whose disruption is a local event with global cause
(`PEOPLES_REPUBLIC_OF_UKWELI.md` §7; `ukweli_local.json`). The Eldrich Corporation gives the board its
cleanest illustration of a distinction the simulation must hold: a faction can hold the **loudest
network** and the **smallest vote** on the same board (§7).

---

## 7. Simulation relevance — the six quantities kept distinct

Wherever society or politics is modelled, **six different things stay in six different fields**
(`NOOPUNK_GLOBAL.md` §7 — *"The six quantities that must stay distinct"*). This is not decoration; it
is the acceptance criterion that stops "media reach" from silently becoming "votes." The Ukweli-relevant
reading:

| # | Quantity | What it is | What it is **not** | Where Ukweli shows it |
| --- | --- | --- | --- | --- |
| 1 | **Opinion / support** | how a constituency currently feels | not membership; not seats; not hegemony | a segment's distribution (§3) |
| 2 | **Organizational membership / resources** | members, volunteers, funds, capacity | does not buy extra actions; it *amplifies* a leader-led mission | the CPU's cadres and mass organisations; the enclave's money |
| 3 | **Legislative representation** | seats in a body | not opinion; not office | the council (§4) |
| 4 | **Office & government control** | who holds which executive office | not seats; not access | the incumbent CPU |
| 5 | **Institutional access** | a faction's ability to *reach and be heard by* a function-system interface | not ownership of the system; not seats; not hegemony | reaching a ministry, regulator or broadcaster |
| 6 | **Laclauian discursive hegemony** | which articulation is **nodal** / where the frontier runs | **not a scalar**; **not ownership, popularity or office or control** | the articulation graph — *not* a meter |

**The non-identities the model must preserve** (from `NOOPUNK_GLOBAL.md` §7): a faction can hold **#1
support** and lose **#3 seats**; win **#3 seats** and not hold **#4 office**; hold huge **#2 membership**
and no **#5 access**; and hold the **#6 nodal signifier** while losing everything else — **hegemony in
meaning is not power**. And **#5 access ≠ #6 hegemony**: reaching a broadcaster is not owning the media
system and not defining common sense. Stated for Ukweli directly: **discursive hegemony is explicitly
not the same as ownership, popularity or office.**

### 7.1 The theory-to-mechanics reading (PROPOSAL, from #325's comment)

Each row consumes something already landed rather than inventing a parallel scaffold. **No numbers,
thresholds or victory conditions are proposed** — those are S0-A.

| Theory | State variables (proposal) | Leader action | Observable outcome on the board |
| --- | --- | --- | --- |
| **Laclau / Mouffe** | which signifier is *nodal*; where the **frontier** runs; which demands chain to which. **No scalar.** | articulate a demand to a signifier; re-role a signifier; redraw the frontier | the political view *is* the graph — a player reads who is linked to what and where the line runs (consumes `politics.py`, `POLITICAL_SIMULATOR_MODEL.md`) |
| **Castells** | network **reach**, bridges/gatekeepers, funding edges, access tokens — **kept apart from opinion and seats** | cultivate a tie; bridge two networks; maintain or buy reach; reach an interface | a faction holds the loudest network and the smallest vote (the Eldrich case makes the distinction visible; consumes §7 above) |
| **Luhmann** | which system currently holds the issue; whether two holders conflict | route the issue: court / university / congregation / market / street / chamber | the same report is a clinic question, an admissibility question and a heresy question three turns apart |

The Luhmannian content is represented as **jurisdiction friction** — *the same event is several
different problems at once, and the playable move is to route it into the system whose code favours
you* — rather than importing any legacy layer rule (`AGENTS.md` §0; the fork is noted in
`NOOPUNK_GLOBAL.md` §6B.1). This keeps the six quantities distinct and keeps the theory inspiration,
never a validated predictive law.

### 7.2 The event deck's shape (PROPOSAL)

Five shocks are already landed (`ukweli_local.json` `shocks`: global frontier model released;
unverified anomalous signal at a coastal facility; maritime trade disruption; contested PSI research
report; international AI-safety agreement). The proposed **shape** — external premise + **local
transmission channel** (port, cable, airport, ferry, media, diaspora) + **party-specific
interpretations that are each defensible** + one non-party actor + effects written against the **six
distinct quantities above** — is what keeps "media reach" from becoming "votes." Content stays small by
design; the global developments arrive as **external influences**, per the issue's own scope rule.

---

## 8. The four carried conflicts — options for the author

These are **not resolved here**, deliberately. For each, what is **factual** is separated from what is
**interpretation**, and the options are named. Settling any of them is a canon decision belonging to the
author.

### 8.1 The state's name — *Republic of Ukweli* vs *People's Republic of Ukweli*

**Factual.** The #325 brief states **"Official name: People's Republic of Ukweli."** #324 (the sibling
issue title and body) says **"Republic of Ukweli"** throughout and predates #325's landing. #328/#331/#332
and `GLOBAL_FACTIONS.md` name only **New Ukweli** and no state (`ISSUE_324_UKWELI_CANON_REUSE.md` §4.1;
`ISSUE_324_UKWELI_GAP_CLOSURE.md` §1).

**Interpretation offered (not a ruling).** The gap-closure record reads the two as a **register
difference, not rival official names**: *People's Republic of Ukweli* as the **official** register;
*Ukweli* / *New Ukweli* as the **everyday** register; *Republic of Ukweli* as the **informal** register
in older prose. That reading is what the setting's own joke requires, since the joke only works because
the formal name misleads.

**Options.** (a) Ratify the register mapping as the closure; (b) reverse it by making the plainer
"Republic of Ukweli" the official form — one deliberate edit to #325's sentence; or (c) leave the
residual question (whether the informal short form persists in issue titles and prose) PENDING. The
record `strategy_game/data/ukweli_geography.json` → `state_names` already carries option (a)'s mapping
with a `residual_pending` container.

### 8.2 The third party's name — **LFP** vs **ULP**

**Factual.** The **data id is `ulp`** in both `ukweli_local.json` and the landed Sir Mars Eldrich card's
`faction_ids`; a fourth id would fork the data. The **display label** differs: **LFP — Libertarian
Freedom Party of Ukweli** in the #325 brief and #326; **ULP — Ukweli Libertarian Party** in #327's
table, `global_factions.json` and #328's roster record
(`ISSUE_324_UKWELI_CANON_REUSE.md` §4.2; `ISSUE_326_UKWELI_LEADERS_AND_NPCS.md` §6).

**Interpretation offered (not a ruling).** The reuse inventory **recommends LFP** on two grounds: both
the dedicated setting issue and the character issue agree on it, and #328's precedence ruling concerned
the *global-faction* register, not Ukweli's parties. It is a recommendation, not a change.

**Options.** (a) Adopt **LFP** as the label, changing `global_factions.json` and the documents together;
(b) keep **ULP**; or (c) hold the current state — the data id stays `ulp`, the label stays open with a
`TODO`, and a landed contract (`test_ukweli_leaders.py::test_naming_conflict_is_surfaced_and_not_resolved`)
asserts the conflict stays **surfaced rather than resolved**, so neither name quietly wins.

### 8.3 Eldrich Island vs the Freedom Colony — the legal relation is **undefined**

**Factual.** The relation is **explicitly undefined**: the two "may be the same enclave, adjacent
areas, or separate linked places" (`ISSUE_324_UKWELI_CANON_REUSE.md` §4.3; `ISSUE_324_UKWELI_GAP_CLOSURE.md`
§3). The Freedom Colony is the LFP's own enclave (`PEOPLES_REPUBLIC_OF_UKWELI.md` §6).

**Interpretation offered (not a ruling).** The gap-closure record transcribes what each option costs,
and **asserts none**:

| Option | What it buys, and what it spends |
| --- | --- |
| **Same place** | one node does the work of two: the island *is* the enclave; simplest map, but the family's private residence and a business enclave become one political object |
| **Adjacent** | one node with two faces: mansion and colony share infrastructure and fate; cheapest for the node budget, richest for internal conflict |
| **Separate, linked** | two nodes of the 6–8: a *domestic* base and a *public* enclave — politically opposite assets, at the cost of a node |

The two island nodes already on the board (`outer_island`, `airfield_island`) are **not** equated with
either place, and `local_geography.problems()` reports any relation that claims to be resolved without a
cited ruling (`ISSUE_324_UKWELI_GAP_CLOSURE.md` §3).

### 8.4 The island-count gap — one city + 3–4 islands (one restricted) vs the live board

**Factual.** #325 asks for **1 city + 3–4 islands** represented by **6–8 location nodes**, one marked
restricted; the setting bible states this as **CANON** (`PEOPLES_REPUBLIC_OF_UKWELI.md` §8). The live
board carries **two** island nodes (`outer_island`, `airfield_island`) and **no** restricted node, so it
shows one island fewer than the canon it instantiates — and an exclusion island is canon in its own
right (§5) (`ISSUE_324_UKWELI_GAP_CLOSURE.md` §4).

**Interpretation offered (not a ruling).** Adding the island needs a **ninth node**, which the eight-node
cap that #322, #325 and the merged schema all state rules out, **or** the removal of an existing node.
The board's node set is pinned not only by the cap but by a **merged board projection**
(`board_local.json` and `tests/test_board_local_projection.py`) that binds each node id to a layout
position. So the gap is recorded rather than hidden: the full island set is **declared** — three
islands, one of them the restricted exclusion island — with the restricted one marked
`on_playable_board: false` **with its reason**, and `island_count.pending` naming the three options.

**Options.** (a) Make the restricted island a **ninth** node, moving the cap; (b) have it **displace**
one of the eight (and if so, which); or (c) represent it **off-board** as a declared non-playable zone.
Whichever is taken, the island carries **no route**, so a prohibited zone stays unreachable under the
provisional travel rules. Because `island` and `access` are now optional **schema** fields, placing it
needs no code change at all — it is an edit to the scenario data and its board binding.

---

## 9. #325's acceptance criteria, walked

| # | Criterion (issue's own words, abridged) | Position | Where |
| --- | --- | --- | --- |
| 1 | Setting is explicitly the **People's Republic of Ukweli**, a multiparty liberal democracy continuously governed by the popular Communist Party since 1964 | **met as canon**; the *official-name* register is carried OPEN (§8.1) | §2.1; `PEOPLES_REPUBLIC_OF_UKWELI.md` §1 |
| 2 | Cosmopolitan Swahili-majority Indian Ocean society, Omani/Portuguese/British/Indian/Chinese waves, in a coherent **fictional** chronology | **met** | §2.1, §3.1 |
| 3 | Modern prosperity **uneven**; New Ukweli highly developed, with port, airport, global communications and diverse industry | **met** | §3.1, §6.1 |
| 4 | Shipping giant, ecological forbidden island, public/secret NHI/PSI tensions, distinct popular attitudes | **met** | §5, §6.1 |
| 5 | Modeling inventory covers population, firms, state, party, media, discourse, networks, social systems, map, factions, organizations, people, technology, world events | **met as setting input with named mechanics owners**; the non-leader cast and non-playable organizations have **no landed artefact and no obvious owner** | `PEOPLES_REPUBLIC_OF_UKWELI.md` §7 inventory table; §4.3 here |
| 6 | Political disagreements plausible, democracy meaningful, neither ethnic groups nor political actors reduced to stereotypes | **met** | §3.1, §4 |
| 7 | Scope stays within the city/islands MVP and works with the four-leader model; global developments arrive as external influences | **met** | §6.2, §7.2; `ukweli_local.json`; `LEADER_COUNCIL_SYSTEM.md` |

**The one criterion with a genuine remainder** is **#5**: the sixteen-category inventory is answered
category by category in the setting bible's coverage table, but **categories 12 (non-playable
organizations) and 13 (the non-leader cast)** have no landed artefact and no obvious owner. That is
recorded here as a **declared blank**, not claimed as done.

---

## 10. What this record deliberately does not do

- It defines **no** rule, statistic, number, threshold, cost, magnitude, turn loop, victory condition or
  engine behaviour, and changes **no** engine or data file. It is Markdown only.
- It invents **no** exact date beyond the canon **1964** and the **~2027** boundary, and **no** person,
  place or institution: the leaders (§4.3) and the island's name (§5.3) are **declared blanks**.
- It resolves **none** of the four carried conflicts (§8); each is recorded as **options with what is
  factual separated from what is interpretation**.
- It does **not** touch the four known open findings (the 4/7/11 global-roster discrepancy, the
  `politics.py` / `political.py` fork, the `Controller`/`MoveProposal` duplicate-type fork, or
  `local_slice.py`'s parallel dataclasses and its `network` scalar-stock), and it edits **no** file owned
  by the running sibling issues (#306, #322, #347, #389).
- It **restates no sibling artefact**: it cites `ISSUE_324_UKWELI_CANON_REUSE.md`,
  `ISSUE_324_UKWELI_GAP_CLOSURE.md`, `ISSUE_324_ACCEPTANCE.md`, `ISSUE_326_UKWELI_LEADERS_AND_NPCS.md`,
  `IDEOLOGICAL_FORMATIONS_2026.md` and `NOOPUNK_GLOBAL.md` §7 rather than copying them.
- It carries **no automated test**: per #271, lore, worldbuilding, scenario prose and design records are
  reviewed editorially and by playtesting, never by CI. A test over this document would be exactly what
  that policy forbids.

*A proposal record offered as design input. Anything selected here becomes canon by the author's
decision, not by this file.*
