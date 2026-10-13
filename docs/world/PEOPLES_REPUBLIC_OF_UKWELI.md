# The People's Republic of Ukweli — setting bible

**Deliverable 2 of [#325](https://github.com/TomiToivio/NooPunk/issues/325)** — *"Setting bible
(`docs/world/PEOPLES_REPUBLIC_OF_UKWELI.md` or consistent path): fictional alternate history and
chronology, culture, economy, politics, religion and paranormal ambiguity. Explicitly mark established
user decisions versus proposed additions."*

This document is **setting only**. It defines no rule, no number, no threshold and no engine
behaviour — `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**, and the simulation spine is
a separate artefact (the proposal comment on #325 maps it; this file does not restate it).

## How to read the marks

Every substantive claim carries one of four marks, because a recalled claim and a sourced one must not
sit unlabelled beside each other:

| Mark | Means |
| --- | --- |
| **CANON** | Stated by the author in the #325 brief. It is the author's text, transcribed here. |
| **PROPOSAL** | This document's suggestion. Nothing is ratified by writing it down. |
| **OPEN** | A conflict the #324 inventory flagged for the author. This file carries it forward and **does not settle it**. |
| **NOT RECOVERABLE** | #324's inventory established that no pre-existing Ukweli material survives anywhere (`git log --all -S`, filenames, and the warehouse under `books/`, `ubiquitous_maniacs/`, `docs/archive/` were all searched). Anything not in this week's material is therefore new, and is marked PROPOSAL rather than "recovered". |

Provenance precedence for this file: **the #325 brief**, then `docs/scenarios/UKWELI_LOCAL_SCENARIO.md`
(#324 B) and `strategy_game/data/ukweli_local.json` (the working map), then
`docs/design/ISSUE_324_UKWELI_CANON_REUSE.md` (the inventory). This file does not override the brief.

---

## 1. The state and its name register

**CANON.** The **People's Republic of Ukweli** is a multiparty liberal democracy that has been
continuously governed by the Communist Party of Ukweli since independence in 1964. It is a prosperous,
open, internationally networked island republic in the Indian Ocean, not an isolated command economy.
Its **indigenous Swahili-speaking majority** is roughly **60%** of the population in this fictional
setting, with Omani Arab, Portuguese, British/English, Indian and Chinese minorities and mixed
communities shaped by centuries of trade, migration and colonial rule.

**CANON — the name is load-bearing, not decorative.** "People's Republic" reflects the communist
independence tradition and the longevity of the governing party, **not** a present-day one-party
dictatorship. The setting's own joke depends on that gap: *"Not quite Cuba, comrade."* Some outsiders
read the words and imagine Cuba-style isolation while Ukweli is prosperous and globally connected.

**CANON — no utopia.** Nuanced tensions and legitimate criticisms stay in the setting. The brief is
explicit that political disagreements are plausible, that democracy is meaningful, and that neither
ethnic groups nor political actors are reduced to stereotypes.

**OPEN — the formal name of the state.** The #324 inventory records a conflict and offers a reading for
confirmation: *People's Republic of Ukweli* as the formal name with *Ukweli* / *New Ukweli* as the
everyday register — which is what the joke depends on. It also records why it is not a stylistic
variant: "People's Republic" carries a claim about the state's self-understanding. This document uses
the **#325 form**, as that inventory instructed, and does not decide the question.

## 2. Alternate fictional chronology, 1500s–2027

**CANON (sequence).** The brief gives the sequence and explicitly notes that it is *fiction*: "Build a
consistent alternate fictional chronology, **noting that real-world Mombasa's historical sequence was
not this exact linear order.**" The order is **Omani Arab domination/colonization → Portuguese colonial
rule → British colonial rule → independence in 1964**.

**PROPOSAL (dates).** The brief asks for a "concise timeline 1500s–2027" but supplies only the
sequence and 1964. Every specific year below is this document's suggestion, to be overwritten by the
author. They are proposed so the setting is internally consistent, not because they are sourced.

| Period | PROPOSAL | What it leaves behind |
| --- | --- | --- |
| ~1000–1500 | Swahili city-state phase: an entrepôt trading East Africa, Arabia, India and East Asia; Islam and local practice interweave | The cosmopolitan layer, the language, the merchant families |
| 1500s–1698 | Omani ascendancy over the islands and the coast | Arab-descended elites, landholding patterns, the old town's architecture |
| 1698–1750s | Portuguese colonial rule, contested by Omani and local forces | Legal residue, Catholic missions, the fort quarter |
| 1750s–1890 | Second Omani period, then British protectorate | Consular and customs institutions, the port as imperial infrastructure |
| 1890–1963 | British colonial rule: port, railway and administration built for export | English in law and higher education, the property regime, the class geography |
| **1964** | **CANON: independence.** The CPU forms the government, aligns with both the Soviet Union and China while carefully retaining functional relations with Britain and the United States | Non-alignment as a founding posture, and the patronage rivalry that comes with it |
| 1964–1980s | Post-independence development, state-led industrialisation, "Ukweli Socialism" | Mass organisations, social programmes, the CPU's record |
| 1990s | After the Soviet collapse: transition to genuine multiparty democracy, and the CPU keeps winning it | The Democracy Bargain, and an opposition that must find a real argument |
| 1990s–2010s | **CANON: Chinese-style market reforms**, export-oriented investment, industrialisation — state-led development alongside private enterprise and international trade | New Ukweli's skyline, the sweatshop-to-advanced-manufacturing arc, the inequality |
| 2020s–**2027** | **CANON: the starting point.** Ordinary politics dominates; the unexplained is present only at the margins | The board the scenario opens on |

**PROPOSAL — the chronology's playable residue.** Rather than dates, what the history leaves is
**inheritances with different legal statuses**, which is what decides who can re-open them. Three are
written down (the liberation settlement, the market opening, the democratic transition) and one is
**unwritten** — the exclusion island (§5) — which is precisely why it is the leak surface. The #325
proposal comment develops this as the simulation spine; this file records only the setting fact that
three inheritances are documented and one is not.

## 3. Society and culture

**CANON.** Five centuries of cosmopolitan Indian Ocean exchange: an entrepôt linking East Africa, India,
the Arabian Peninsula and East Asia, with diverse religious, mercantile and maritime traditions.

**CANON — the non-determination rule.** "Avoid suggesting that ethnic ancestry determines ideology,
religion, class or political loyalty." The same rule governs the parties (§6): no demographic segment
maps one-to-one to a party.

**CANON — the segments must overlap.** The brief asks for the Swahili majority and the minorities to be
modelled "through **overlapping** geographic, occupational, economic, linguistic, ethnic and belief
segments".

**PROPOSAL — the starting segments.** Defined by *exposure* rather than ancestry, each mapped to at
least two of the eight existing map locations, so the anti-bloc rule has something to attach to:

| # | Segment | Locations it lives across |
| --- | --- | --- |
| 1 | Port and logistics households | Old Harbor, Industrial Logistics Port |
| 2 | Ferry-dependent outer-island communities | Outer Island Communities, Coastal Hinterland |
| 3 | New Ukweli professionals and commuters | Civic and Commercial Centre, Mixed Neighborhoods |
| 4 | Informal-quarter renters and street traders | Mixed Neighborhoods, Old Harbor |
| 5 | Campus, clinic and research staff | University and Hospital, Civic |
| 6 | Fisherfolk cooperatives and maritime traditionalists | Old Harbor, Outer Island Communities |
| 7 | Diaspora-remittance households | Mixed Neighborhoods, Civic |

**PROPOSAL — the invariant that makes it not a bloc model.** No segment has a fixed party; each
segment's support is a distribution with at least two live options; and **any single crisis may split a
segment**, so a party that owns a segment this turn can lose half of it next turn without the segment
changing at all. Without that rule the non-determination instruction is a disclaimer rather than a
model.

**Languages (PROPOSAL, from CANON elements):** Swahili as the everyday and national language; English
retained in law, higher education and international commerce from the British period; Arabic and
Gujarati in specific mercantile and religious communities; Portuguese as a historical residue in
toponyms and the fort quarter.

## 4. Religion and the paranormal register

**CANON.** Ukweli's **local shamanic traditions, folk religions and island mythologies** contain stories
that the fiction interprets as related to NHI, PSI and anomalous experience. Two constraints bind any
expansion:

- **Create respectful and original traditions, with varied interpretations.** Do **not** make real
  ethnic or religious traditions synonymous with paranormal powers.
- **Catholic Christianity** is significant in parts of rural Ukweli (CANON, from the UIP section). The
  UIP's **appropriation** of both folk belief and Catholic identity is **contested by practitioners and
  believers**, and religious identity does not determine party affiliation.

**CANON — belief cuts across demographics.** Ukweli is a fictional UFO and paranormal hotspot, but most
**urban residents** treat UFOs and PSI as irrelevant, implausible, old-fashioned rural superstition, or
a modern New Age scam. Others believe, remain uncertain, or have direct experience. Believers and rural
people must **not** be portrayed as intrinsically uneducated; belief and scepticism cut across
demographics rather than along them.

**PROPOSAL — four registers, kept apart.** The brief distinguishes the public position, competing
internal assessments and the setting's deeper mysteries. Representing them as one thing is what makes
a disclosure plot collapse into a single reveal:

1. **Official denial register** — what the state *says* it knows.
2. **Internal assessment divergence** — agencies that do not agree with each other, sincerely.
3. **Conservation legitimacy** — the biodiversity rationale, which has its own credible truth (§5).
4. **Popular interpretation** — indifference, folk tradition, faith, scepticism, scam-detection and
   direct experience, spread across the segments in §3 rather than sitting in one of them.

Ideological tensions over **indigenous knowledge, tourism, conservation, disclosure, scientific method,
religious authority, sovereignty and foreign intelligence** are **CANON** as a list of the fault lines
the setting must support.

## 5. The exclusion island

**CANON.** The government **privately knows there are strange, recurrent events** on some islands. It
has designated **an entire island a prohibited/protected zone**, publicly **to safeguard Ukweli's
unusual biodiversity and ecological heritage**. Three things are explicit:

- the **biodiversity rationale has its own credible truth and conservation value**, "even if security is
  also involved";
- the government **officially acknowledges** unusual, unexplained UFO/PSI reports and the rich local
  mythology, but **consistently denies possessing definitive or special knowledge of their causes**;
- the distinction between the public position, competing internal assessments and the deeper mysteries
  is a setting requirement, not decoration.

**PROPOSAL — the NoöPunk reading worth keeping.** The ecology is genuine **and** the closure is a cover,
and neither fact cancels the other. A setting where the conservation is fake is a smaller setting than
one where a real, defensible conservation regime is also a gate.

**PROPOSAL — it is a gated location.** Opening it is a decision with a cost, which is why the MVP map
carries one node marked restricted. Per #324's inventory the **exact legal autonomy** of the enclave and
its relationship to the Freedom Colony are **OPEN** (§8).

**NOT RECOVERABLE.** No older material names the island or fixes what is on it. This file does not name
it: naming it is a canon decision, and #324 §4.3 already shows one name from a superseded source sitting
in tension with another.

## 6. The three established parties

**CANON — these are established setting canon, not placeholders.** "Represent their stated ideology,
documented actions in the fictional history, actual constituencies and opponents' accusations as
distinct simulation fields." The electoral strengths below are **setting assumptions**, not claims about
real countries or populations.

### Communist Party of Ukweli (CPU) — incumbent liberation party

Pan-African Marxist-Leninist roots; led the independence struggle and won independence in **1964**;
cultivated ties with the USSR and China while keeping pragmatic relations with Britain and the USA.
Guided the Chinese-style market opening, **preserving the broadly egalitarian ideals and social
programmes of "Ukweli Socialism"**, and managed a genuine transition to multiparty democracy **without
losing power**. **Continuously democratically elected and genuinely popular**, its legitimacy founded on
national liberation, rising living standards, social equality, successful reform and stability. It is
**not** secretly a one-party regime.

- *Strategic tension (CANON):* a revolutionary liberation party now governing a prosperous, commercially
  open, globally integrated society. Model disagreement between older Marxist cadres, pragmatic
  reformers, unions, young cosmopolitans and rural voters **without presuming a historical rupture**.
- *Advantage (CANON):* institutional relationships, durable trust, national organisation, broad
  legitimacy, established networks. *Vulnerability:* incumbency during sudden global economic, political
  or ontological shocks.

### Ukweli Identity Party (UIP) — ethnic-nationalist and rural populist challenger

Mixes **ethnic/"tribal" identity politics** with global-style right-wing populism; claims to represent
the indigenous Swahili majority and rural communities against urban elites and the communist-led
establishment. Draws selectively on shamanic/folk belief and Catholic Christianity, an appropriation
**contested by practitioners**. Uses anti-immigrant and anti-colonial rhetoric targeting people it
labels foreign, including white residents, Muslims and Asian-origin communities, with racist,
Islamophobic, nativist and conspiratorial claims, and depicts LGBTQ+ identities as "un-African".

**These are party positions and prejudices to model critically — the setting does not endorse them.**
Two CANON guard rails: **do not equate Swahili ethnicity with UIP support** (many Swahili residents
reject its politics), and distinguish historical colonial power from modern citizens and minorities.
Its attack on the CPU as **communist** is accurate to the party's identity; its attack as
**totalitarian** is **false within the established setting**. Its opportunity is conditional — a serious
contender if the government falters, especially under an ontological shock — and is **not a
predetermined election result**. Support, grievance frames, media channels and organisational capacity
must be modelled **without assuming a uniform rural or ethnic electorate**, and the consequences for
targeted populations must be visible.

### Libertarian Freedom Party of Ukweli (LFP) — libertarian enclave and tycoon-sponsored populism

Originally advocated turning Ukweli into a **libertarian/anarcho-capitalist experiment** with minimal
state interference, and operates its own **Freedom Colony**. A relatively small party whose localised
base includes a disproportionate share of **white residents and recent expatriates in the Freedom
Colony** — "do not reduce all white residents or expatriates to party supporters." Over time it moves
from doctrinaire libertarianism toward **Trump-style right-wing populism**, creating internal
contradictions over free markets, immigration, elite patronage and charismatic leadership. Nationwide
support is low; its reach depends disproportionately on **financing and sympathetic media** owned or
influenced by its benefactor, **Sir "Mars" Eldrich**.

**CANON — not a secret twist.** The distinction between a formally autonomous party and Eldrich's
**publicly known** financial and media influence is to be modelled explicitly; the relationship is not
a hidden reveal.

**CANON — Sir Mars Eldrich.** An eccentric British aristocrat, owner/controller of the setting's
world-largest shipping company, serial inventor, political meddler and publicly known financier of the
LFP. His obsessions are **colonising Mars** and supporting right-wing populist parties. He is to be
developed as a major NPC and organisational network — **not an omnipotent puppet master**. His dynasty,
company and media assets are **#326's** deliverable.

### Three-faction starting tension (CANON)

| Dimension | CPU | UIP | LFP |
| --- | --- | --- | --- |
| Public identity | Liberation, egalitarian socialism, reform and stability | Indigenous identity, cultural traditionalism, rural grievance | Libertarian freedom, enclave experimentation, populist opposition |
| Strength | Broad popularity, incumbency, institutions | Grievance mobilisation, crisis-driven growth | Financial backing, Freedom Colony, media access |
| Vulnerability | Accountability for shocks while in office | Credibility ceiling outside its base | Vote support far below its media reach |

**PROPOSAL — a reading of that table.** The three are not three positions on one axis; they hold three
different *kinds* of power (institutional trust, grievance mobilisation, media reach), which is why the
same shock can strengthen one and destroy another. Whether the three powers become comparable quantities
is a design question owned by the simulation spine, not by this file.

## 7. Economy and infrastructure

**CANON.** Growth evokes China's transformation at a much smaller geographic scale. **New Ukweli** is a
glossy, high-rise, high-connectivity modern port and CBD evoking selected features of Singapore, while
older quarters, fishing communities, outer islands and rural areas experience **uneven infrastructure,
wealth, public services and exposure to global markets** — "avoid implying Africa is uniformly poor or
premodern."

**CANON — economic pillars:** fishing; farming; tourism; shipping and logistics; a modern port and
international airport; export manufacturing (historically sweatshops, now also advanced and high-tech
products); services; finance and telecommunications; and local technology adoption.

**CANON — the shipping corporation.** A world-leading shipping corporation, within the fiction the
world's largest, is owned or controlled by an **eccentric British aristocrat** (Eldrich). Its business
model, local footprint, leadership, political ties, labour relations and tensions with the communist-led
government are to be designed — and **ownership of a global corporation must not be confused with
sovereignty over the port**.

**CANON — connectivity as infrastructure, not units.** The port, international airport, undersea
internet cables, an extensive fishing fleet of thousands of boats, Starlink/satellite internet,
satellite television and global mobile networks. "Model boats, cables and the port as
infrastructure/network nodes and vulnerabilities, **not individual units**."

**PROPOSAL — the grounded node list.** The working map already carries the economy as eight locations
and seven routes (`strategy_game/data/ukweli_local.json`): Old Harbor, Civic and Commercial Centre,
Mixed Neighborhoods, University and Hospital, Industrial Logistics Port, Outer Island Communities,
Airfield Island and Coastal Hinterland. Airfield Island is the connectivity node (its tag is
`communications`); read the port, the airfield and the cables as the state's three chokepoints.

## 8. The MVP scope, and what this document does not do

**CANON — keep the MVP radically small.** One city plus 3–4 islands represented by **6–8 location
nodes**, one marked restricted; **3 political factions × 4 leaders**; 5–7 overlapping population
segments; 4–6 key institution, media and corporate nodes; 3–5 contested signifiers; one tiny network
graph; a handful of social-system pressures; and a small event deck. All active moves belong to one
leader. A 10–12-turn deterministic prototype, with **scenario data separated from engine code**. Rich
detail can live in prose without every lore item being a simulation variable.

**CANON — the creative north star.** *A genuinely successful, democratic, communist-led Indian Ocean
republic with one dazzling modern city, centuries of cosmopolitan history, and something unexplained on
an island the government insists is closed purely to protect its biodiversity. The rest of the world is
about to get much stranger, comrade.*

### What this document deliberately does not do

- **It decides no OPEN conflict.** Carried forward untouched: the state's formal name (#324 §4.1), the
  third party's name — **LFP in the #325 brief and #326, `ulp` in `ukweli_local.json` and
  `global_factions.json`** (§4.2), and the restricted island's relationship to the Freedom Colony,
  including its legal autonomy (§4.3).
- **It names no party leaders.** #324's inventory defers the leader roster to **#326**, and this file
  does not pre-empt it. The twelve entries in `ukweli_local.json` are **generic role placeholders**
  (`CPU Chair`, `UIP Organiser`, …), not named canon.
- **It defines no mechanics.** No signifier, metric, score, action, turn loop, event deck or resolution
  procedure. The theory-to-mechanics table (deliverable 5), the event cards (6) and the playable
  scenario spec (7) belong to the simulation spine and to the design gates.
- **It does not restate the simulation spine proposal** already on #325's thread, nor #324's reuse
  inventory, the two existing scenario documents, or `strategy_game/docs/MVP_LOCAL_CITY_M0.md`. Those
  are cross-linked above; a second copy of any of them would fork the record.
- **It moves no existing file.** `docs/world/` is new; nothing was relocated to make room for it.

### Inventory coverage, and who owns what

The brief's acceptance criterion asks the modelling inventory to cover sixteen categories. This
document supplies each category's **setting input** — the entities, registers and constraints — and
names the owner of the mechanics:

| # | Category | Setting input (here) | Mechanics owner |
| --- | --- | --- | --- |
| 1 | Population segments | §3 | simulation spine |
| 2 | Corporations and economy | §7 | simulation spine |
| 3 | Government | §1, §2 | #322 / #323 |
| 4 | Communist Party of Ukweli | §6 | #323 |
| 5 | Opposition, parties, movements | §6 | #323 / #327 |
| 6 | Media and information ecosystem | §7 (media owned by Eldrich) | #327 |
| 7 | Laclau's discourse theory | §6 fault lines | simulation spine, gated |
| 8 | Castells's network power | §7 node list | simulation spine, gated |
| 9 | Luhmannian social systems | §4 registers | simulation spine, gated |
| 10 | Strategic map | §7 grounded nodes | #324 C |
| 11 | Factions | §6 | #325 / #323 |
| 12 | Organizations | §4, §6 | #325 (open) |
| 13 | People | §6 (Eldrich only) | **#326** |
| 14 | World events | §2 timeline, §5 | #327 |
| 15 | Science, technology, infrastructure | §7 | #347 / simulation spine |
| 16 | Time and historical change | §2 | this document |

**PROPOSAL — the smallest useful next step.** Categories 12 and 13 are the only ones with no landed
artefact and no obvious owner: the cast of non-leader NPCs (ministers, scientists, media figures,
clergy, environmental officers) and the non-playable organisations (unions, religious communities,
conservation NGOs, research groups, associations, diaspora networks) that the brief lists. **#326 owns
the leaders and the dynasty**; the surrounding cast is still unowned.
