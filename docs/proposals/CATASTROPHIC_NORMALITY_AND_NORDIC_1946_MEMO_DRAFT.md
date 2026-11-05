# DRAFT MEMO — Catastrophic normality, three narrative modes, and the Nordic 1946 secret

> **DESIGN MEMO — TOMI REVIEW REQUIRED — NOT CANON, NOT AN IMPLEMENTATION TICKET**
>
> Written for [#1168](https://github.com/TomiToivio/NooPunk/issues/1168) as a discussion synthesis. It changes no
> rule, no timeline entry, no rulebook chapter and no existing research document. Where it proposes something, the
> proposal is marked; where a claim is historical, its evidence tier is marked; where the discussion left a
> question open, the question stays open.
>
> Cross-referenced, not replaced: [`rulebook/7_TIMELINE.md`](../../rulebook/7_TIMELINE.md) §UFO/UAP disclosure,
> [`rulebook/parts/10_campaign_unsa_factions.md`](../../rulebook/parts/10_campaign_unsa_factions.md) §40 (the Nordic
> lineage), [`docs/world/ALTERNATE_HISTORY_1114.md`](../world/ALTERNATE_HISTORY_1114.md),
> [`docs/research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md`](../research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md) §7.2,
> and the PR #1162 drafts in this directory.

**Evidence labels:** **[H]** verifiable historical record · **[H?]** historically reported but not established ·
**[O]** open question · **[P]** design proposal · **[C]** fictional canon (author) · **[X]** contested external
claim, not evidence.

---

## 1. Thesis

**The NHI Crisis was a real catastrophe, and 2045 is post-post-apocalyptic.** Institutions function unevenly
rather than not at all. People have normalised overlapping nuclear, machine, psychic, extraterrestrial, economic
and religious shocks — the way people actually normalise: by going to work, watching sport, and refusing to think
about it before lunch.

Nobody can write a definitive global history of the Crisis, and that is a **design decision, not a gap**. The
events overlapped; archives were destroyed or curated; witnesses contradict one another; and time/space plus the
Soviet Mandela Effect make chronology itself unreliable. A game that demanded one authoritative timeline would be
telling a story the setting says cannot be told.

**What replaces the authoritative history:** *catastrophic normality*. One block runs avant-garde fourth-density
psychic research; the next runs a factory with ordinary staff; much of the population maintains the cultural
routines of 1974. Reptilian raids kill people. Abandoned machine ecologies keep working without purpose. Denial
gets more dangerous every year, and the comedy and the stakes are the same scene.

---

## 2. AWN is a mode switch, not a second game

CWN stays the immutable core. AWN is a **CWN-compatible overlay** for the places where society actually broke —
its existing implementation, not a new one.

**What exists and can be switched on today** (verified in code, not assumed):

| module | what it already does |
|---|---|
| `src/rules/awn_stress_tracker.py` | stress contract, thresholds, events and recovery, `new_tracker`, `is_enabled` — the off-switch exists at the API level |
| `src/rules/awn_region.py` | region states, severity, `transition_allowed`, a region ledger |
| `src/rules/awn_survival.py` | terrain, travel hours, exposure, encounter checks, scouting days |
| `src/rules/awn_world.py` | enclaves, sites, crises, world ledger |

**Proposed activation boundary** — an expedition mode with an explicit on/off, because a survival system that
never turns off turns every social scene into a scavenging game:

| place / situation | mode | what switches on |
|---|---|---|
| Ordinary Helsinki, Europol investigation | **CWN** | nothing from AWN |
| During the Crisis (flashback or late campaign) | **CWN + AWN** | stress tracker, region state, scarcity, breakdown/hardening |
| Hyvinkää Machine Exclusion Zone | **AWN expedition** | survival travel, encounters, stress, salvage, hazardous terrain |
| Loviisa radiation exclusion | **AWN containment** | exposure, supply, evacuation procedure — **no** operational sabotage detail |
| Collapsed border / external areas | **AWN travel** | enclaves, resource pressure, recovery |
| Embassy, astral hearing, corporate office | **CWN** (+ light PSI tags) | AWN only if survival pressure becomes real |

**Three rules that keep the switch honest:**

1. **The switch is declared, not inferred.** A scene header says `mode: cwn | cwn+awn | awn`, and the table knows
   before dice are rolled. Hidden mode changes are how a game becomes unfair.
2. **Stakes travel, systems do not.** Leaving the Zone ends the stress tracker at a stated recovery point; it does
   not silently carry AWN scarcity into Helsinki.
3. **One resolver.** AWN never rolls its own attack, save or skill check; it supplies *conditions* to CWN's.

Open questions for the author: does stress **persist** across mode boundaries (a week in the Zone marking the
character), or reset? Are breakdown and hardening per-scene or per-arc? (#1109 and #928 own the technical answers;
this memo only proposes the boundary.)

---

## 3. The 50/25/25 reaction heuristic is a tool, not a census

The existing heuristic, restated as **behaviour, not demography**:

* **~50% normalisers** — attempt to keep going. Some are competent and brave; some are absurd; a few are
  heroic precisely because the buses still run. Culturally 1974: work, television, sport, beer, relationships.
  **Not unintelligent.**
* **~25% accelerationists** — heterogeneous, enthusiastic about ASI, BCI, PSI, contact, resleeving, fusion and
  self-transformation. Some sign terrible contracts knowingly and some do not.
* **~25% doomers / bioconservatives** — heterogeneous, distrust NHI, hybridisation, dangerous AI and psychic
  intrusion. Sometimes right, sometimes coercive, paranoid, scapegoating.

**How to play it without turning it into a demographic table:**

1. **Roll a stance, not a person.** When an NPC's reaction matters, pick the stance that makes the scene
   interesting, then give the NPC a reason. Never infer competence or decency from the stance.
2. **Institutions are not people.** A ministry can be a normaliser while its best analyst is an
   accelerationist and its security chief a doomer. That mismatch *is* the political comedy.
3. **Comedy never erases a victim.** A Reptilian raid kills someone; the joke is about the response, never the
   death.
4. **No stance is the moral default.** The 25% who distrust hybridisation are not automatically villains, and the
   25% who embrace contact are not automatically wise.

*Idiocracy* is a tonal ingredient: the satire targets **institutions and behaviour**, not the intelligence of
ordinary people. A normie may be the most competent person in the room.

---

## 4. The three writing modes, as a style guide

The author's method, recorded here as an explicit norm rather than an occasional comedy add-on.

| mode | what it does | touchstones | failure to avoid |
|---|---|---|---|
| **1. Satire and comedy** | bureaucracy, political contradiction, religious adaptation, extraordinary normality, deadpan local dialogue | *Idiocracy*, Robert Anton Wilson | contempt for ordinary people; jokes that dissolve consequence |
| **2. Over-the-top genre pastiche** | cyberpunk, science fantasy, New Weird, occult detective, post-apocalypse, *Stalker* / *Solaris* incomprehension, 1970s psychedelic retrofuturism **not** 1980s neon | *Stalker*, *Solaris*, New Weird | pastiche that stops being frightening; aesthetics replacing stakes |
| **3. Academic / social-scientific modelling** | the fiction as a speculative-sociology instrument: legitimacy, sovereignty, identity, dependency, SMC, civil rights | Laclau, Castells, Wendt, Luhmann, LaclauGPT's method | a lecture; theory that resolves what the story should leave contested |

**Working label:** *Carnivalesque Social Science Fiction* — a description, not a compulsory genre.

**The governing rule: consistent consequences, flexible seriousness.** The modes may switch inside one scene — a
darkly comic public hearing, a genuine alien terror attack, and an investigation of how a corporation marketed
that attack can all be the same session. What may **not** vary is causality: if a raid kills, the death stays
dead; if an institution lied, the lie has a paper trail.

Two practical tests for the table: *(a)* after a comic beat, ask what it cost someone; *(b)* after a serious beat,
ask whether the institution that caused it is still faintly ridiculous — because it is.

---

## 5. The Nordic 1946 question

**The author's new direction [C]:** it makes little sense for a well-intentioned Confederacy to hand technology to
the USA and the Soviets and overlook Finland. The 1946 Ghost Rockets can be **Sirian physical craft or a
technology transfer facilitated by the Confederacy**, and the Finnish President's later disclosure of contact
since **1946** becomes a direct consequence.

### 5.1 What the historical record actually supports

| claim | tier | what the sources say | what they do **not** establish |
|---|---|---|---|
| Ghost Rocket wave, Feb–Dec 1946 | **[H]** | first reports **26 February 1946, from Finnish observers**; ~2,000 sightings May–December, peaks 9 and 11 August; ~200 radar returns; press and military-attaché reporting across Scandinavia | no recovered object; no origin |
| Swedish military investigation | **[H]** | a Swedish military inquiry; press directive not to publish exact location, direction or speed; dives on lakes (notably Kölmjärv, 19 July 1946) found craters and torn plants, no craft | no confirmation of any foreign programme |
| Explanations | **[H]** contested | many sightings fit meteors (Perseid peak); others report silent, no-exhaust, manoeuvring objects inconsistent with meteors; Peenemünde/Soviet-test theory was considered and **not** confirmed | no settled explanation, then or now |
| Hessdalen lights, Norway | **[H]** | sudden increase December 1981; up to ~20 sightings/week 1981–85; Project Hessdalen founded 1983; 1984 technical report records 53 observations with camera, radar, magnetometer; Blue Box automated station from 1998; ~20 reports/year now | no agreed mechanism; not linked to 1946 |
| Denmark, 1946 | **[H?]** / **[O]** | Scandinavian reporting exists; **no Danish recovery is established in this pass** | **do not assert crashed hardware or a Danish programme** |
| Ghost Flier wave, 1930s | **[H]** | already canon in the rulebook's Nordic lineage | — |
| Sirian craft at 1946 Finland | **[C]** | author's fictional addition | **nothing historical supports it**, and the memo should say so once, in the setting bible, then stop saying it |

**The discipline this implies:** NoöPunk uses the *record* (reports, investigations, dead ends, contradictory
files) and adds the *fiction* on top. It never presents the fiction as the record's conclusion.

### 5.2 Three contact models, to choose between

Each model is internally consistent, gives a different game, and leaves the others available as **rumour** — which
is what an unresolved archive sounds like.

| model | what happened in 1946 | who knew | what it produces in 2045 | cost |
|---|---|---|---|---|
| **A. The Gift** | the Confederacy **arranged** a Sirian transfer; a small Nordic circle received it | a few ministers, officers, scientists | a coherent secret, a moral debt, a state that has lied for a century | too tidy; risks the "Nordic MJ-12" the author warns against |
| **B. The Accident** | Sirian craft **failed** over Scandinavia; the recoveries were partial and mostly misunderstood | local units, one laboratory, one ministry official | the best game: fragments, misread metallurgy, a rumour that outlived the truth | weakens the "why Finland" moral question |
| **C. The Misunderstanding** | contact happened, but **nobody on either side agreed what it was**; some hardware changed hands; both sides kept it quiet for different reasons | compartments that never met | the strongest thematic fit: distributed, informal, contradictory | hardest to summarise in one paragraph |

**Recommended: B as the event, C as the structure, A as the rumour.** The 1946 recovery was an accident nobody
fully understood (B); the Nordic response was a distributed, compartmented, partially informal network rather
than a single programme (C); and by 2045 the *story* has hardened into a gift narrative that the surviving
documents do not support (A). That combination gives the author the moral question — why Finland, and who decided
— without requiring an omniscient conspiracy.

### 5.3 Distributed, not centralised

Do not build a Nordic MJ-12. Build the thing that actually happens in small states: overlapping compartments that
each believe they are the whole picture.

```
ministry official ── one file ── laboratory director ── two technicians
        │                              │
   defence staff ── nothing ──  university department ── a professor who left
        │                              │
   state firm ── a contract ──  a single foreign liaison who was never briefed
```

What this buys: **no single person can answer the player's question**, and every answer is partial and interested.
Formal Nordic cooperation may come later — the rulebook already says whether it ever became a single programme is
open (§40), and this memo keeps it open.

### 5.4 Minimal divergences (not a rewritten century)

Proposals, each small enough that the 2045 world still looks like ours with one seam:

1. **A classified materials and cryogenics programme** with early, narrow expertise and belated civilian
   spillover — no consumer fusion in 1970.
2. **A single unexplained industrial accident** whose paperwork never matched its outcome (a cover story the
   players can find, and disprove, or fail to).
3. **A neutrality problem**: sharing with one bloc and not the other, argued about in cabinet minutes that
   survive.
4. **Human agency preserved**: the engineers, ministries, unions and parliaments did the work; the alien material
   was a *component*, never the explanation for a whole economy.
5. **Finnish/Soviet archives that contradict the universal Mandela Effect** without explaining it — the effect
   stays unsolved, and this is one of its cracks.

### 5.5 Confederacy and Sirius are not the same polity

Verified in the Ra material this pass, and worth keeping straight because the game's politics depend on it:

* **8.6** — the Russians received technology "from one of the Confederation" about twenty-seven years earlier, in
  an attempt to share information and bring peace; Ra calls the givers "in error" and cites it as a reason for
  later caution.
* **38.7** — an entity from Sirius "has approached this planetary body twice".
* **38.13** — that craft was of third-density physical material, visible to third-density observers.
* **51.2** — Ra: those coming from distant points "for the most part … do not need craft as you know them",
  which is exactly why a **physical** Sirian arrival is a different event from a Confederation contact.

**What this does not establish:** none of these passages mentions Finland, 1946, or a transfer to any Nordic
state. The Finnish connection is **authorial fiction [C]**, and the memo's job is to keep that visible.

---

## 6. Mission progression (candidate, not canon)

Ten candidate beats, ordered so that each one teaches a different mode. Names are placeholders.

| # | beat | mode | what it tests |
|---|---|---|---|
| 1 | **Kruununhaka archive** — authenticate a 1946 Finnish Ghost Rocket case; a Swedish file describes the same object and disagrees about who owned it | CWN investigation + satire | the record is real, the interpretation is not |
| 2 | **Otaniemi provenance** — an instrument in a quantum/PSI lab carries a Nordic Cold War serial code | CWN investigation | ethics of research, and a component that should not exist |
| 3 | **Stockholm archives** — a photo negative is genuinely old; its inventory label is new | CWN social/investigation | the forgery is in the filing, not the image |
| 4 | **Hessdalen station** — a surviving sensor picks up a signature that resembles Hyvinkää | CWN + genre | a phenomenon that is not a vehicle and not a ghost |
| 5 | **Copenhagen dataset** — a research group holds a 1946 chain of custody nobody can explain | CWN social | *proposal*; asserts nothing about real Danish institutions |
| 6 | **Hyvinkää Zone** — a search-and-rescue becomes an AWN expedition | **AWN** | survival, stress, and an entity that may not be a machine |
| 7 | **Loviisa** — a worker's compensation case exposes partial sabotage records | CWN + AWN containment | bureaucracy as the horror, no sabotage instructions |
| 8 | **Parliament briefing** — classified Nordic history is exposed; oversight is demanded | CWN social / satire | the lie is older than everyone in the room |
| 9 | **Vallisaari embassy** — a Confederacy partner and a Sirian refugee disagree about what the 1946 gift meant | CWN social + PSI | no bloc is a monolith |
| 10 | **Sörnäinen PSI prison** — civil rights, crime and astral escape collide | CWN + PSI | how a society criminalises a faculty |

**Session-level tonal transitions** the memo recommends as a *craft* note: a filing error → deadpan political
satire → genuinely strange physical or noetic evidence → a real civilian threat → CWN/AWN procedure → institutional
comedy with consequences.

---

## 7. Four scene sketches (one per mode, plus one that switches)

**7.1 Satire — the hearing.**
A parliamentary committee asks why a 1946 file was classified for a century. A civil servant answers in perfect
procedural Finnish for four minutes without saying anything. The player may press (Talk), produce a document
(Administer), or let it go. Success changes nothing about the file; it changes who is now afraid of her.
*Cost of the joke:* the committee's chair is a doomer who will use the exposure to attack hybridisation.

**7.2 Genre pastiche — the Zone at night.**
Hyvinkää: a factory that still runs. Machines that do their old jobs without purpose. A `Stalker`-shaped
expedition with real AWN rules: travel hours, exposure, encounters, stress. The horror is a machine that
**politely** continues an obsolete process while people are inside it. No combat unless the players make it one.

**7.3 Social-scientific — the ownership question.**
A Sirian refugee and a Confederacy attaché give incompatible accounts of the 1946 event, each internally coherent,
each supported by a document. The scene is an investigation of *legitimacy*, not of fact: who has the right to
narrate the gift? The correct outcome is that the player must choose a reading to act on, and live with it.

**7.4 The switch — one session, three modes.**
A darkly comic briefing about a missing invoice → the invoice leads to a Zone maintenance contract → the team
enters Hyvinkää (mode switches to AWN, declared at the scene header) → a genuine casualty → back at the office, a
bureaucratic joke that lands badly because someone died. That is the thesis of this memo in one session.

---

## 8. Cross-check against existing canon

| document | what it already fixes | this memo |
|---|---|---|
| `rulebook/7_TIMELINE.md` | disclosure is plural; Nordic countries build on Ghost Flier/Rocket recoveries; First Contact beats are an **order, not a chronology** | does not add beats, adds *how they are narrated* |
| `rulebook/parts/10_campaign_unsa_factions.md` §40 | Nordic lineage spans Finland/Sweden/Norway/Denmark/Iceland; "whether this ever became a single formal multinational program remains open" | keeps it open, and builds the distributed network *inside* that openness |
| `docs/world/ALTERNATE_HISTORY_1114.md` | the 2045 political order (EU federation, UNSA limited, USSR collapse, Mandela Effect) | **authoritative over** `design/ZONES.md`'s older "UN as semi-functional world government" preamble |
| `design/ZONES.md` | the zones themselves: two Helsinki EEZs, two embassies, three Sirian protection zones, Hyvinkää and Loviisa exclusion zones | zone **content** is used; its **political preamble is superseded** and should not be quoted as canon |
| `docs/research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md` §7.2 | 1946 ghost rockets with sources and the naval-attaché Helsinki report | reuses its dating and refrains from re-researching it |
| PR #1162 drafts | disclosure background, scenario draft, mission gazetteer, Hyvinkää addendum | linked, not merged; this memo is a *narrative method + secret-history* layer, not a fifth gazetteer |

**One correction this memo asks for:** `design/ZONES.md` still frames the world as a UN/UNSA world government.
That is the superseded lore #1168 explicitly warns against. The zone list is usable; the framing is not.

---

## 9. Open questions for the author

1. **Contact model:** B-as-event / C-as-structure / A-as-rumour (recommended), or a cleaner single model?
2. **Who knew in 1946** — a minister, a colonel, a professor, a firm? The answer changes what can be found.
3. **Did the Confederacy intend the Finnish contact**, or merely fail to prevent it?
4. **Was secrecy a betrayal** the Confederacy later judged, or something it accepted?
5. **Parallel deliveries** to Sweden and Norway: same model, or deliberately different?
6. **Denmark** — nothing established. Does it get a dataset, a rumour, or silence?
7. **Stress persistence** across AWN mode boundaries.
8. **Does the 1946 recovery connect causally** to the later donated fusion ships, or is that a coincidence the
   public insists on?
9. **How much of the Nordic network survives to 2045**, and who owns the hardware now?
10. **What may the player actually prove?** The memo's working answer: enough to force a political reckoning,
    never enough to close the file.

---

## 10. What this memo does not do

* It does not edit `rulebook/`, `design/`, or any timeline.
* It does not implement AWN activation, stress, or any game system.
* It does not claim any historical source establishes alien contact.
* It does not merge PR #1162's drafts, or promote them to canon.
* It does not resolve the Mandela Effect, the 1946 origin, or the Danish question — by design.

## 11. Sources checked in this pass

| source | status |
|---|---|
| Wikipedia, *Ghost rockets* | read; dates, ~2,000 sightings, radar returns, Kölmjärv, meteor explanation, Swedish press directive |
| Project Hessdalen, "About" (Erling Strand, 2025) and *Project Hessdalen 1984 — Final Technical Report* | read; 1981 onset, 53 observations, 1983 founding, Blue Box 1998, ~20/year now |
| Law of One 8.6, 38.7, 38.13, 51.2 | read verbatim from lawofone.info in this pass; quoted above |
| `docs/research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md` §7.2 and the R-5-8-47 transcript | read; not re-researched |
| Danish 1946 material | **not verified**; the memo asserts nothing |
| Hessdalen–Hyvinkää link | **[P] fiction**, not a finding |
