# DESIGN MEMO — Crisis, narrative method, and Nordic secret contact history (#1168)

> **Status: reviewable design memo, not canon and not an implementation ticket.** It records a discussion synthesis
> for the author to edit, approve or reject. No rulebook, timeline, world document or code is changed by this
> memo. Nothing here is implemented.
>
> **What is settled, and what is not:** everything marked **[AUTHOR]** restates a direction the author has already
> given. **[PROPOSAL]** is mine to be edited. **[FICTION]** distinguishes NoöPunk's in-universe history from
> real-world history. **[UNVERIFIED]** marks a claim I could not check, so nobody inherits it as fact.

---

## 0. What this memo is for

The discussion produced four things that need to survive as one readable document: a **thesis** about what 2045
feels like, a **narrative method** for writing it, **rules boundaries** for when AWN applies, and a **secret
history** that explains why Finland was not left out. This memo states all four, and marks every place where it
touches existing canon.

## 1. Thesis: the Crisis happened, and 2045 is post-post-apocalyptic

**[AUTHOR]** The NHI Crisis was a genuine catastrophe. 2045 is not the aftermath of a single event but the
settled-in normality of overlapping ones: nuclear, machine, psychic, extraterrestrial, economic and religious
paradigm shifts that arrived faster than any institution could sequence them.

**Nobody can write a definitive global history of the Crisis.** Not as a stylistic choice — as a consequence:

| Reason | Consequence for play |
|---|---|
| Events overlapped across years and regions | Any "then X happened" is local and partial |
| Archives destroyed, classified or manipulated | Institutional records are evidence, not truth |
| Witness memories contradict one another | Testimony is a lead, never a fact |
| **Time/space and the Soviet Mandela Effect** may make chronology unreliable | The game may present mutually incompatible pasts without adjudicating |

**[AUTHOR]** The result is **catastrophic normality**: one block runs avant-garde fourth-density psychic
research; another operates a factory with ordinary staff; much of the population attempts to maintain the cultural
routines of 1974. Reptilian terror raids and encounters with abandoned machine ecologies make denial progressively
more dangerous.

The fiction moves between comic absurdity and real stakes, and the memo's core claim is that this is **one world**,
not two tonal registers bolted together.

## 2. Narrative method: three modes, one world

**[AUTHOR]** The three modes below are not an occasional comedy layer. Movement between them is intrinsic to how
the setting is written.

| Mode | What it does | Touchstones (as tone, not imitation) |
|---|---|---|
| **1. Satire and comedy** | Bureaucracy, political contradiction, religious adaptation, extraordinary normality, deadpan local dialogue, social reaction to ontological shock | *Idiocracy*, Robert Anton Wilson — **without** assuming people are fools |
| **2. Over-the-top genre pastiche** | Cyberpunk, science fantasy, New Weird, occult detective, post-apocalypse, surreal conspiracy, *Stalker*/*Solaris* incomprehension, 1970s psychedelic retrofuturism (not 1980s neon) | Exaggeration that can fall away into real horror and wonder |
| **3. Academic / social-scientific modelling** | The fiction as speculative sociology: legitimacy, sovereignty, collective identity, techno-economic dependency, social-memory complexes, civil rights | Laclau, Castells, Wendt, systems theory, the LaclauGPT method — informing conflict, never lecturing |

**Working label [PROPOSAL]:** *Carnivalesque Social Science Fiction*. Proposed description, not a compulsory genre
designation.

### The rule that makes the three modes safe together

**Consistent consequences, flexible seriousness.**

- Consequence is never waived for a joke. A raid that kills people stays lethal in the next scene.
- Seriousness may change inside a scene: a darkly comic public hearing, a genuine alien terror attack, and an
  investigation of that attack's role in Grey corporate marketing can coexist.
- The narrator need not adjudicate every reality tunnel. Multiplicity of interpretation is a feature.
- **Two prohibitions:** no compulsory grimdark, and no turning affected people into disposable punchlines.

## 3. Rules boundary: CWN core, AWN where society actually broke

**[AUTHOR]** CWN is unchanged as the foundation. **AWN is a CWN-compatible overlay for disaster history,
hazardous locations and survival missions — never a replacement combat or skill engine.**

### 3.1 What already exists (do not duplicate)

| Component | Module | State |
|---|---|---|
| AWN Stress tracker (#1083) | `src/rules/awn_stress_tracker.py` — `event`, `recovery`, `new_tracker`, `is_enabled` | implemented |
| Survival layer | `src/rules/awn_survival.py` — terrain, `travel_hours`, `hexes_per_day`, `is_exposed` | implemented |
| Region model (#1045) | `src/rules/awn_region.py` — `RegionState`, `RegionLedger`, `transition_allowed` | implemented |
| Settlements, sites, crises | `src/rules/awn_world.py` — `Enclave`, `Site`, `Crisis`, `WorldLedger` | implemented |
| Trackers of record | #1109 (AWN), #928 (stress), #1083 (backlog) | **link, do not restate** |

The memo therefore does **not** propose a new stress mechanic, a new survival procedure, or a second crisis model.
It proposes **activation boundaries**.

### 3.2 When AWN turns on

| Dramatic environment | Primary mode | AWN overlay |
|---|---|---|
| Ordinary Helsinki / Europol investigation | CWN investigative | **Off** |
| During the Crisis (flashback or present) | Disaster / fractured institutions | On: supplies, scarcity, hazards, salvage, stress, hardening, enclaves |
| **Hyvinkää** machine-civilisation outbreak zone | *Stalker*-like exploration | On: encounters, environmental threat, logistics, field stress, anomalous salvage |
| **Loviisa** radiological aftermath | Containment and humanitarian crisis | On: exposure, supply, evacuation, recovery — **no operational sabotage detail** |
| Border / collapsed external areas | Post-apocalyptic travel and enclave politics | On: limited support, faction and resource pressure |
| Alien embassy, astral hearing, corporate office | CWN + light investigative/PSI tags | **Off** unless survival pressure is actually present |

**The test for "on":** is there scarcity, exposure or a hazard that can hurt someone this scene? If not, AWN stays
off. A Helsinki social scene must never become a scavenging game.

### 3.3 Open rules questions (for the AWN owners, not answered here)

1. How do AWN stress and breakdown procedures attach to CWN attributes without inventing a second attribute scale?
2. Does a stress tracker persist across mode switches, or reset per expedition?
3. Do the same modules run identically in tabletop and Evennia, or is one the reference?
4. What is the **exit condition** that turns AWN off again, stated per scene?

## 4. The 50/25/25 reaction heuristic

**[AUTHOR]** A structural heuristic about reactions to ontological shock — **not a demographic survey**.

| Share [PROPOSAL] | Reaction | Not |
|---|---|---|
| **~50% "normies"** | Normalise, ignore, compartmentalise, refuse. May live culturally as if it were 1974: work, television, sports, beer, relationships, consumer ritual | **Not uniformly unintelligent.** Keeping civic systems running can be practical and heroic; denial can also be absurd or fatal |
| **~25% accelerationists** (heterogeneous) | Welcome ASI, BCI, PSI, Pleiadian contact, Grey resleeving, Sirian fusion/biotech, self-transformation. Some sign terrible consciousness-ownership contracts with enthusiasm | Not one organisation |
| **~25% doomers / bioconservatives** (heterogeneous) | Distrust NHIs, hybridisation, dangerous AI, psychic intrusion. Concerns sometimes justified | Fear can become coercive politics, paranoia and scapegoating |

**Satirical reference:** *Idiocracy* is a **tonal ingredient**, not a mandate to depict people as stupid. A normie
can be brave and competent; an educated elite can be spectacularly credulous.

**Playable form [PROPOSAL]:** treat the three shares as an **NPC stance field** on any crowd or institution, not as
a character attribute — `normie / accelerationist / doomer`, with the understanding that individuals cross over
under pressure. A scene can then show the same crowd reacting three ways without rolling.

## 5. Nordic secret history: why Finland was not left out

**[AUTHOR]** It makes little sense for a well-intentioned Confederacy to give advanced technology to the USA and
the Soviets while overlooking Finland. **The 1946 Ghost Rockets can be Sirian physical craft or technology
transfer facilitated by the Confederacy**, connecting to a Finnish secret history of contact and
reverse-engineering. The President's later disclosure of contact *since 1946* becomes a direct consequence.

**What is already in canon:** `rulebook/7_TIMELINE.md` states that "the Nordic countries build on Ghost Flier and
Ghost Rocket recoveries" as one of several national reverse-engineering traditions. This memo therefore **extends**
an existing line rather than introducing one.

**Evidence discipline.** Real-world history and fiction are kept apart:

| Claim | Status |
|---|---|
| 1946 "Ghost Rocket" reports over Sweden, Finland and Norway; military investigation | **Real world** — widely documented reporting |
| Hessdalen lights and the instrumented research programme | **Real world** — a real, ongoing scientific interest |
| Those phenomena were alien craft | **[FICTION]** NoöPunk's in-universe answer. Real evidence does not establish alien origins |
| A 1946 recovery/transfer in Finland | **[FICTION]** authorial addition. **[UNVERIFIED]** as any kind of historical claim |

**[UNVERIFIED] and stated as such:** I did **not** read original 1946 military files, Finnish or Swedish press
archives, or Hessdalen's primary publications in preparing this memo. Specific dates, sites, officials, budgets and
unit names must be checked against originals before any of them enter canon. The issue's citation of
[Law of One 8.6](https://www.lawofone.info/s/8#6), [38.7–13](https://www.lawofone.info/s/38#7) and
[51.2](https://www.lawofone.info/s/51#2) describes Confederation assistance to Russians and Sirian physical travel
— **none of them establishes a Finnish transfer**, and the memo says so rather than implying a citation it does
not have.

### 5.1 Three contact models [PROPOSAL — pick one, or keep the ambiguity]

| Model | The 1946 event | Who knew | Story consequence |
|---|---|---|---|
| **A. The gift** | Confederacy sanctions a Sirian delivery of working hardware to a Nordic government that had shown restraint | A narrow ministry–military–laboratory circuit | The secrecy is a **moral debt**: fusion was withheld through energy crises |
| **B. The accident** | A Sirian craft is lost or abandoned; recovery is opportunistic and partial | Whoever reached it first, then compartmentalised | No one was chosen; the "gift" is a story told afterwards to justify the secrecy |
| **C. The misunderstanding** | Sirians make contact with scientists who read it as a technological offer, not a relationship | Scientists first, government later, each with a different account | The two sides still disagree about what was agreed in 1946 |

**Recommended:** keep **A and B simultaneously available as competing institutional accounts**. That is more useful
than one truth: different archives can support different models, and the player can never fully settle it.

### 5.2 Structure: distributed, not a Nordic MJ-12

**[AUTHOR]** Avoid a tidy centralised organisation. Prefer a **distributed, partially informal network** of
ministries, military units, laboratories, universities, state firms, scientists and intelligence services.

- Different people know different compartments.
- Formal cooperation may come later; **bilateral and individual connections did most of the work**.
- This is **one plausible design**, not a settled naming or org chart.

**Game value:** provenance conflict. Two archives disagree; a component has a serial number from a programme nobody
admits existed; a widow has a pension from a unit that is not in the order of battle. None of it needs a secret
council.

### 5.3 Candidate national specialisations [PROPOSAL]

| Country | Real anchor | In-world specialisation hypothesis |
|---|---|---|
| **Finland** | 1946 Ghost Rockets; early Nordic reports | Sirian hardware and biologics, fusion and cryogenics, psychotronics/PSI, pragmatic engineering, emergency governance |
| **Sweden** | 1946 wave and military investigation | Physical craft and materials, aerospace recovery, propulsion, sensors, industrial engineering |
| **Norway** | Ghost Flier reports; Hessdalen | Plasma phenomena, living light, environmental UAP, transmedium sensor studies |
| **Denmark** | Scandinavian 1946-era reporting; research history **[UNVERIFIED]** | Quantum/biological/medical science, consciousness interpretation |

**Denmark carries no hardware claim.** The issue's discipline is right: do not assert a Danish recovery without a
separately approved fictional event.

### 5.4 Minimum divergences, not alien determinism

**[AUTHOR]** Propose the *smallest* historical changes, not decades rewritten as alien technological determinism.

1. Classified programmes produce unusually early expertise in materials, sensors, power, cryogenics or biology,
   with **belated civilian spillover**.
2. A small number of achievements come from unacknowledged projects, while **normal economic and political history
   stays recognisable**.
3. Cold War neutrality, intelligence sharing and secrecy become subjects of real ethical conflict: who authorised
   spending, who benefited, why energy technology was withheld.
4. 2045 revelations make Nordic achievements **more controversial, not automatically alien**.
5. Human scientists, workers, democracies, labour movements and public institutions **keep their agency**.
6. Finnish/Soviet contact archives can **contradict** the universal USSR Mandela Effect without solving its cause.

**Political comedy [FICTION, explicitly a comic beat]:** the 2045 Finnish president admits contact since 1946; a
journalist asks why cheap fusion was withheld through the energy crises; an engineer complains his team could never
get spare parts for the alien hardware.

### 5.5 Confederacy and Sirius are not the same polity

**Working hypothesis [PROPOSAL]:** the Confederacy permitted or encouraged contact; **physical third-density Sirian
visitors** supplied more accessible spacecraft, hardware and biological knowledge. Collapsing the two into one
polity would destroy the most interesting diplomatic question in the setting.

**Keep unanswered [AUTHOR]:** Why Finland? Did the Sirians know they were engaging a secret programme? Did the
Confederacy regard later secrecy as betrayal? Were there parallel Swedish or Norwegian deliveries? What, if
anything, arrived in Denmark? Who holds the surviving hardware? Is 1946 causally related to the later donated fusion
ships and protection zones? How did the 1950s Soviet ПРОГРАММА interact with Nordic research, and which documents
are Mandela-effect anomalies rather than proof?

## 6. The intersecting Crisis: history, not a clean chronology

**[AUTHOR]** Already-specified author directions, with dating and causal detail deliberately unapproved:

- The EU–Russia war ends when **most** Russian nuclear launches are intercepted by UAPs; Russia collapses.
- The Machine Civilization sabotages **Loviisa** and causes a serious outbreak at **Hyvinkää** — a hazardous,
  sometimes *Stalker/Solaris*-like machine ecology.
- Human nuclear weapons and AGIs are disabled; the Confederacy opens contact through beings of light and makes
  serious demands. Pleiadian biologics rapidly increase Confederacy popularity; the Law of One becomes a mass
  religion.
- The end of quarantine enables far more visible **fourth-density awakening**, stronger PSI, and public
  Astral/Noösphere culture.
- The President reveals Finnish contact from **1946**; Confederacy and Sirian embassies in Helsinki; **three Sirian
  refugee protection zones**; Sirians donate fusion vessels.
- Greys offer EEZs and technological immortality; revelations about abductions and hybridisation produce paranoia
  and civil-rights conflict.
- Mediumship, Hermetic magick, shamanism, CE-5 orbs and commercial PSI expand. **Pope Teilhard II** reveals Vatican
  UFO archives and integrates Law of One / Noösphere / Omega Point into Catholic teaching while aligning with the
  Confederacy. High-profile psychic crimes produce registration and the Sörnäinen PSI prison.
- **Jellyfish UAPs** may be independent noetic/physical organisms rather than vehicles of any known bloc — an open
  proposal, not approved taxonomy.

**Historiographic method [PROPOSAL]:** present the Crisis through **separate witness accounts, conflicting agency
ledgers, municipal service records, oral histories and playable flashbacks**. Preserve the independent human PSI
breakthrough and the ordered First Contact beats in the rulebook. Preserve the collapsed USSR with the universal
Mandela Effect, the never-solved MJ-12/ПРОГРАММА, a limited UNSA, and Europol as the player's employer — and do not
accidentally revive superseded lore of a world-government UNSA or an institutionally surviving USSR.

## 7. Cross-check against existing canon

| Document | What it already says | This memo |
|---|---|---|
| `rulebook/7_TIMELINE.md` | Setting year **2045**; paradigm shifts deliberately unordered; **"the Nordic countries build on Ghost Flier and Ghost Rocket recoveries"** | Extends the Nordic line; adds no dates to the unordered shifts |
| `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` | Ordered First Contact story; independent human PSI awakening | Preserved unchanged; the memo does not re-sequence it |
| `docs/world/ALTERNATE_HISTORY_1114.md` | Collapsed USSR; **universal Mandela Effect as diegetic contradiction, never confirmed**; MJ-12/ПРОГРАММА unsolved | Keeps the Mandela Effect unresolved; the Nordic material is a separate lineage |
| `docs/world/EUROPOL_HELSINKI_1114.md` | Europol opens doors; national officers walk through them | Unchanged; the Parliament briefing scene uses that limit |
| `design/ZONES.md` | Extraterrestrial Special Economic Zones | Referenced, not extended (it is currently a single-page document) |
| `src/rules/awn_*` (#1109, #928, #1083) | Stress, survival, region, world/enclave models implemented | Linked, not duplicated; the memo proposes only activation boundaries |

**No canonical timeline, rule or world document is changed by this memo.**

## 8. Five scenes that switch modes on purpose

Each is written to show the transitions the memo argues for, with consistent consequences.

1. **Kruununhaka archival intimidation** *(satire → procedure)*. A civil servant refuses a 1946 file because the
   form was superseded in 1987; deadpan bureaucratic comedy. The file, once produced, is genuinely disturbing:
   Swedish records describe the same craft but disagree about who owned it. Same scene, both registers.
2. **Otaniemi provenance and research ethics** *(social science → genre)*. An instrument used for quantum/PSI
   experiments contains a component with a Nordic Cold War serial code. The scene is a research-ethics argument
   about who was told what — then the instrument does something it should not.
3. **Hessdalen sensor station** *(genre excess → measured uncertainty)*. A surviving sensor detects a
   jellyfish/plasma/noetic signature apparently related to Hyvinkää. **It is not explained.** The scene ends with a
   data set and three incompatible readings.
4. **Hyvinkää Zone** *(procedure → survival horror → procedure)*. A search-and-rescue task becomes an **AWN-enabled
   expedition**: supplies, exposure, stress. The rescue succeeds; the paperwork afterwards is the comedy, and the
   rescuer's hand is still shaking.
5. **Europol–Parliament briefing** *(politics → personal consequence)*. Classified Nordic history is exposed and
   Parliament demands to know why public oversight was avoided for decades. A named official's career ends. The
   joke is about institutions; the cost is a person's.

**Session-level tonal arc [PROPOSAL]:** a bureaucratic filing error → deadpan political satire → extraordinarily
strange physical or noetic evidence → a genuine civilian threat → CWN/AWN procedure → renewed institutional comedy,
with the consequences intact.

## 9. Candidate mission progression (Helsinki/Nordic)

1. **Kruununhaka** — authenticate a 1946 Finnish Ghost Rocket case; Swedish records disagree on ownership.
2. **Otaniemi** — provenance and research ethics; a Cold War serial code on a quantum/PSI instrument.
3. **Stockholm archives** — parallel Swedish records; a photo negative genuinely old, its inventory label much newer.
4. **Hessdalen** — a surviving sensor station sees a signature related to Hyvinkää; nature unknown.
5. **Copenhagen** — a dataset with an inexplicable 1946 chain of custody. *Proposal; no claim about real Danish
   institutions.*
6. **Hyvinkää Zone** — search and rescue becomes an AWN survival expedition; an entity that might not be a machine.
7. **Loviisa** — a worker's compensation case exposes partial sabotage records, not a reactor-infiltration scenario.
8. **Europol–Parliament briefing** — classified history exposed; oversight demanded.
9. **Vallisaari / Sirian embassy** — a benevolent Confederation partner and a Sirian refugee disagree about what
   the 1946 "gift" meant.
10. **Sörnäinen PSI prison** — civil rights, crime and astral-escape themes collide, with no real-world facility
    security detail.

## 10. Open decisions for Tomi

1. **Which contact model** — gift (A), accident (B), misunderstanding (C), or keep two in tension (recommended)?
2. **Is the Nordic network** best served by no name at all, by a mundane cover name, or by a later formal body?
3. **Does Finland's 1946 contact precede or follow Sweden's?** Whichever is chosen constrains every archive scene.
4. **Does the Confederacy know about the secrecy in 2045**, and does it care?
5. **What did Denmark get, if anything?** Leaving it blank is a legitimate answer and good game material.
6. **How far do the minimum divergences go?** Is one early fusion prototype acceptable, or is even that too much?
7. **Is *Carnivalesque Social Science Fiction* the label you want**, or is it a working description only?
8. **Do the 50/25/25 shares belong anywhere in the rules**, or only in GM guidance?

## 11. What this memo does not do

- It does not change the timeline, the rulebook, world documents or code.
- It does not assert any historical claim it could not verify; §5 marks those explicitly.
- It does not implement AWN, PSI or investigation; it links to the modules and trackers that own them.
- It does not close #1168. Approval and any canonical change are the author's.

## 12. Bibliography

**Repository (read for this memo):** `rulebook/7_TIMELINE.md`, `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md`,
`docs/world/ALTERNATE_HISTORY_1114.md`, `docs/world/EUROPOL_HELSINKI_1114.md`, `design/ZONES.md`,
`src/rules/awn_stress_tracker.py`, `awn_survival.py`, `awn_region.py`, `awn_world.py`.

**Real-world anchors [not re-verified in original archives by the author of this memo]:** the 1946 Ghost Rocket
reporting wave (Sweden/Finland/Norway); the Hessdalen lights and the instrumented research programme.

**Law of One (in-universe source, not evidence):** 8.6 (Confederation assistance to Russians), 38.7–13 and 51.2
(Sirians with physical/slow travel) — cited by the issue as context; **none establishes a Finnish transfer**.

**Related:** #1156 and PR #1162 (disclosure research drafts), #1109 (AWN tracker), #928 (stress), #1083 (AWN
backlog), #105 (reverse-engineering/contact lore), #1121 (Nordic zones), #1123 (Crisis flashback memories), #1120
(narrative entry), #106 (Wendt disclosure).
