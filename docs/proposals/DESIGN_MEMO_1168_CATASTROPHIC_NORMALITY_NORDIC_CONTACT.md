# Design memo: catastrophic normality, three writing modes and Nordic secret contact

> **DRAFT — AUTHOR REVIEW REQUIRED. NOT APPROVED CANON.** Companion to [issue #1168](https://github.com/TomiToivio/NooPunk/issues/1168), created 2026-11-05.
>
> **Evidence key:** **[CANON]** existing approved NoöPunk authority; **[AUTHOR PROPOSAL]** idea requested in #1168 but not yet canon; **[HISTORY]** documented *reports or investigations*, not proof of alien origins; **[HYPOTHESIS]** alternative fictional model; **[OPEN]** author decision; **[SCENE]** illustrative fictional material. No published rules, chronology, author-owned design documents, or Python source are modified by this memo.
>
> **Relationship to existing work:** [Disclosure research](../research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md), [Disclosure crisis proposal](UFO_DISCLOSURE_NHI_CRISIS_SCENARIO_DRAFT.md), [Helsinki gazetteer](HELSINKI_UAP_MISSION_GAZETTEER_DRAFT.md). This memo synthesizes **AWN activation + narrative style + Nordic contact provenance**, not a second encyclopedic First Contact chronology or district gazetteer.

## Executive thesis

**[AUTHOR PROPOSAL] NoöPunk takes place in the condition of _catastrophic normality_.** The NHI Crisis was devastating. Some places underwent actual post-apocalyptic collapse, others preserve functioning institutions, and mundane routines persist amidst irreconcilable accounts of recent history. Helsinki is a **post-post-apocalyptic** place: Europol officers perform procurement audits, someone queues for beer, a research institute attempts to contact 4th-density entities, and a civil-defence siren is treated as either a known procedure or an existential threat depending on the district and speaker.

The crucial artistic engine is **not** a permanent tone of solemnity: NoöPunk moves organically between **(1) satire and comedy, (2) maximal genre pastiche/New Weird wonder and terror, and (3) academic/social-scientific scenario modeling**. Each makes the other meaningful. A joke has ordinary consequences; a truly horrific raid is not rendered harmless by satire; a social-science observation is enacted by character decisions and institutions, not delivered as a lecture.

The *1946 Nordic contact history* should be an unresolved but researchable set of partially overlapping files. **[HISTORY]** Ghost Rocket reports occurred around Scandinavia in 1946. **[HYPOTHESIS]** in the fictional setting some Finnish and Swedish sightings are related to **Sirian physical craft/biotech or a Confederacy-facilitated technology transfer**. Several distributed programs may have developed around these claims. The campaign should not decide that every 1946 observation was extraterrestrial, that every Nordic state received a crashed craft, or that one secretly omnipotent committee controlled history.

## 1. Continuity firewall: what not to rewrite

| Authority | Binding distinction for this memo |
|---|---|
| [Timeline, `rulebook/7_TIMELINE.md`](../../rulebook/7_TIMELINE.md) | **2045 fixed**, major paradigm shifts deliberately **unordered** as dates. Do not impose a single dated sequence. |
| [First Contact and PSI, `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md`](../../rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md) | Natural human PSI precedes/exists independently of NHI disclosure; the Confederacy messenger contact and Orion negotiation/infiltration have a particular **relative order**. Do not invert it or make PSI an alien gift. |
| [Playable history, `docs/world/ALTERNATE_HISTORY_1114.md`](../world/ALTERNATE_HISTORY_1114.md) | **Post-Soviet Russia**, Russian collapse after EU–Russia war, with a **universal USSR-survival Mandela Effect**. The Soviet-punk Troika/Cosmist surviving USSR is *contradictory in-world material*, not a second live canonical polity. **ПРОГРАММА / MJ-12** remain unsolved. |
| [Europol Helsinki, `docs/world/EUROPOL_HELSINKI_1114.md`](../world/EUROPOL_HELSINKI_1114.md) | Rookie employer is **Europol**, cooperating with Finnish agencies; limited UNSA X-Risk role. Do not create a universal UNSA police empire or unlimited Europol search power. |
| [Greater Helsinki zones, `design/ZONES.md`](../../design/ZONES.md) | Author proposed a Helsinki–Espoo–Vantaa metropolitan merger, extraterrestrial zones and diplomatic sites. Respect its *author draft* status and reconcile only through author edits. |
| [Existing #1156 dossiers](../research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md) | Their real-source excerpts and broader Crisis mission list remain references. Do not duplicate their 2040s event timeline or silently elevate their proposals to canon. |

**[OPEN]** Some current proposal documents present the Loviisa/Hyvinkää sequence and 1946 government knowledge with more definite wording than canonical rulebook chapters. This memo treats them as **scenario hypotheses** pending author approval, not a change to `7_TIMELINE.md`. Distinguish *what a file claims*, *what an agency accepts*, and *what actually happened*.

## 2. AWN overlay: use it where the environment is broken, not everywhere

**[CANON]** *Cities Without Number* is the unchanged rules engine. **[AUTHOR PROPOSAL]** *Ashes Without Number* adds specialist survival procedures only when a specific place/mission requires them. Refer to [AWN tracking #1109](https://github.com/TomiToivio/NooPunk/issues/1109), [stress #928](https://github.com/TomiToivio/NooPunk/issues/928), [AWN compatibility](../rules/AWN_CWN_COMPATIBILITY.md) and [baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md).

| Scene/location | Default chassis | AWN addition only if relevant | Turn-off condition |
|---|---|---|---|
| Kurvi apartment, Europol paperwork, city interviews | CWN | None: scarcity bookkeeping would be noise | Not enabled |
| NHI Crisis flashback with collapsed services | CWN | Supplies, shelter, hazard, stress and enclave support when explicitly depicted | Safe zone restored or flashback ends |
| Hyvinkää machine ecology **[PROPOSED]** | CWN | Expedition supplies, environmental hazard, salvage, fatigue/stress and site evacuation | Return to secure support/base |
| Loviisa incident response **[PROPOSED]** | CWN | Exposure, triage, evacuation and recovery; **no operational sabotage procedures** | Threat contained / scene transitions to civic investigation |
| External failed-state border expedition | CWN | Enclave and scarcity context if support collapses | Normal logistics resume |
| Astral meeting, alien diplomatic zone, social party | CWN + scene-specific PSI/investigation | Usually **no AWN** | Not enabled |

**Activation contract, still to design rather than implement:**
1. GM marks a **scene or region hazard profile**, e.g. `crisis_zone: true`, `supply_tracking: active`, `stress_overlay: active`, `enclave_turn: not_required`.
2. Only **published AWN specialty procedures** with source-verified edition/page and a concrete narrative trigger are used. No separate attack dice, character attributes, wounds or automatic gear economy.
3. On scene transition to safe support, record persistent consequences (harm/stress, depleted supplies, recovered objects, institutional fallout), then suspend **local** scarcity/hazard clocks; do **not** magically erase damage or trauma.
4. **[OPEN]** Audit the actual AWN implementation and stress/hardening overlap first. `docs/rules/AWN_SECTION_COVERAGE_1109.md` is generated and must not be manually edited. Any implemented overlay later needs matching tabletop/Python examples and tests.
5. Treat breakdown/hardening with care: neither a clinical diagnosis nor inevitable consequence of encountering NHI. Playable stress must respect human agency and character continuity.

**Hand-resolvable sample [SCENE].** A Europol team enters a quarantined Hyvinkää service area with issued safety equipment and two days' supplies. CWN resolves an obstacle and a confrontation. If supplies or environmental exposure are at stake, the approved AWN procedure resolves **that** pressure, then the team returns to Helsinki with a genuine injury and recovered industrial records. No AWN resource roll is performed at dinner in Kurvi.

## 3. The 50/25/25 heuristic: not a poll, not fixed alignments

**[AUTHOR PROPOSAL]** These percentages are **rough fictional ideal types**, not verified demographics or hard faction membership:

| Rough share | Type | Strength / plausible heroism | Failure / comedy |
|---|---|---|---|
| ~50% **Normies** | Compartmentalize the ontological changes and preserve familiar life; some culturally emulate **1974** | Civilians keep schools, hospitals, transit, unions, sports and care networks running | A bureaucracy preserves a 1974 approval form for a 2045 noetic emergency |
| ~25% **Accelerationists** | Embrace ASI/BCI/PSI, alien economies, hybridization and enhancement | Brave scientific work, emergency adaptation and liberation from old limitations | A self-improvement startup signs away its founders' cognition rights to a Grey service contract |
| ~25% **Doomers/bioconservatives** | Fear loss of humanity, unchecked AI, involuntary PSI and hidden NHI influence | Correctly identify coercive surveillance, real dangers and corporate abuses | Demands psychological screening of an entire district using an unreliable psychic helmet |

**Use as scene prompts, not mechanics.** A normie may be the most competent rescue worker; an accelerator may oppose authoritarian AGI; a doomer may defend an alien child's rights. A violent raid is real; subsequent comedy concerns the state's inept response, not the victims. Avoid assigning characters a permanent class or StO/StS score from these groupings.

**[OPEN]** In the first campaign, do these ideal types appear through NPC descriptive tags, political movement agendas or optional survey-style social simulation? Recommend **qualitative NPC/movement tags first**, not an artificial population census.

## 4. The three writing modes as the style engine

### Mode A: satire, comedy, mundane pain
Contemporary institutional comedy, deadpan dialogue, corporate billing, absurd licensing, conflicting laws, moral inconvenience, romance and neighborly life. *Maniac* and Robert Anton Wilson are useful tonal coordinates. The protagonist's honest struggle to complete a report is allowed to matter alongside cosmic events.

### Mode B: maximal New Weird / pastiche / science fantasy
Over-the-top genre sequences: strange noetic life, retro-psychedelic and Mœbius-like spatial aesthetics, corporate occult noir, *Stalker/Solaris*-like ambiguity, AWN survival horror, Reptilian violence, eerie benevolent Sirians and the possibility that an alien gift has the wrong meaning. Avoid reducing all phenomena to hardware, a single alien species or one conspiracy.

### Mode C: social-scientific simulation
Institutions, class, discourse, legitimacy, ideology, networks and sovereignty become explicit causes of scenes. Laclau-style political articulation (how competing groups give a Crisis its meaning), Castells-style communication networks and brokerage, Luhmann-style institutional differentiation and Wendt-style sovereignty/identity transformations can motivate NPC factions. This is *exploration through consequences*, not an academic infodump.

**Scene-writing template:** `who is harmed or helped? → what institution and incentive system does what? → where does the grotesque/funny contradiction surface? → which stranger-than-real genre image disrupts it? → what does a competent investigator actually discover? → which consequences carry to next scene?`

**Example scene switches [SCENE]:**
1. **City hall hearing.** A city councillor asks whether a fourth-density apparition requires a fire inspection (A). A witness materializes as a shifting geometry of faces (B). The actual issue is whether the human tenants retain the right to refuse an astral service contract (C). Decision creates an ongoing legal dispute.
2. **Hyvinkää rescue.** The team encounters a workplace safety placard solemnly certifying a rogue-machine hazard (A), then reaches an unnerving machine ecology that does not recognize the distinction between equipment and host bodies (B). They must choose whom to evacuate first and how to ration protective resources (C + AWN).
3. **Ghost Rocket audit.** An old procurement code is the only clue linking Finnish and Swedish 1946 files (C). A pension office denies the existence of a project while mailing its veterans anniversary cards (A). A supposed Sirian tool produces a physically impossible memory effect (B). Source authenticity remains separate from alien provenance.
4. **Embassy interview.** A Sirian representative is a genuinely disconcerting biological presence (B). The translation device asks if the meeting should be invoiced as forestry or diplomacy (A). A live conflict emerges between autonomy, technology access and secrecy (C).
5. **Post-raid insurance.** A Reptilian terror attack kills civilians (B, played gravely). Later an insurer has classified property damage as an astronomical-risk exclusion (A). Europol investigators follow who sold these contracts and which victims are left without aid (C). **The deaths are never a punchline.**

The same episode can move from comedy to real horror and back to ordinary police life, while **causal and human consequences remain constant**.

## 5. Historical Nordic source notes: records ≠ extraterrestrial origin

**[HISTORY] Sweden:** The **Swedish National Archives** describes the summer **1946** spökraketer reports across Nordic countries and a Swedish Defence Staff inquiry that never established what caused them. It is a primary institutional historical source, not a UFO-recovery confirmation.  
Source: Riksarkivet, *Arkivpodden: Spökraketer*, 2024-11-15 (podcast transcript), https://riksarkivet.se/resurser/spokraketer .

**[HISTORY] Finland:** A **U.S. Naval Attaché report dated 10 February 1947** quotes Finnish press reports: Finnish newspapers reported numerous 1946 rocket-like sightings, plus a January 1947 Helsinki observation, but the attaché noted a lack of corroborating information. The surviving transcription is a record of reports and uncertainty, not a verified object.  
Source/transcription and scan: https://ufologie.patrickgross.org/htm/foia01.htm ; related analysis already in [Disclosure research](../research/UFO_DISCLOSURE_BACKGROUND_RESEARCH.md).

**[HISTORY] Norway:** **Project Hessdalen** was founded in **1983**; documented field observations occurred **21 January–26 February 1984**, including 53 sighting reports during the field study. This is evidence of organized measurement and unresolved observations, **not evidence of extradimensional plasma intelligence**.  
Sources: Erling Strand, original 1984 technical report https://old.hessdalen.org/rapporter/hprapport84.shtml ; project background https://www.hessdalen.org/about .

**[HISTORY] Denmark:** Danish reports were included in the **1946** Scandinavian press wave; a contemporaneous Aftenposten account from **17 August 1946** reports sightings over Zealand and Copenhagen, while newspaper accounts in September mention Danish investigation cooperation. These are historical **claims/press reports**, not recovered hardware. Danish SUFOI reporting archive is much later, **dating from 1958**, so it should not be cited as direct archival proof of a 1946 recovery.  
Sources: 1946 press translations https://www.project1947.com/fig/1946a.htm ; contemporary reprint https://paperspast.natlib.govt.nz/newspapers/NA19460904.2.53 ; AFU archive holdings https://www.afu.se/collections/report-files/ .

**Contemporary alternative explanations:** late-war missile development, Soviet missile tests, misidentified meteors/aircraft and press amplification featured in historical investigations. A **1947 U.S. intelligence review** discusses uncertain evidence, civilian and military reports and conventional missile hypotheses. There is **no sourced public verification in this memo** of alien technology transfer, intact Nordic alien craft, recovered biologics or a single secret Nordic government organization.  
Source: declassified intelligence document transcript https://uapledger.com/documents/release-5-dow-uap-d099 ; other WWII-era military review https://ignaciodarnaude.es/wp-content/uploads/2025/08/Casos-OVNI-1946Ghost-Rockets-8.pdf .

## 6. Nordic contact: three competing fictional models

Treat **1946** as the shared documentary hinge while retaining multiple plausible interpretations. **Confederacy** and **Sirians** remain distinct: the former might authorize/encourage contact and the latter might supply a *physical third-density* visiting craft or biological insight. The **Law of One** sessions on Soviet aid **8.6**, Sirians **38.7–13** and **51.2** do **not** document an actual Finnish technology handoff; a Finnish transfer is **original NoöPunk fiction**. Primary source https://www.lawofone.info/s/8#6 ; https://www.lawofone.info/s/38#7 ; https://www.lawofone.info/s/51#2 .

| Model | How the secret starts **[HYPOTHESIS]** | Benefits for play | Unresolved ethical problem |
|---|---|---|---|
| **A. Intentional Sirian gift** | A Sirian liaison acting with Confederacy knowledge deliberately places limited equipment within reach of Finnish/Swedish researchers; comparts it through military-scientific channels | Human institutions must interpret strange but real material. Some old technical success is a *human* achievement built on donated components | Why was useful energy/medical knowledge withheld for generations? Did donor intend secrecy? |
| **B. Accident and salvage** | Genuine 1946 craft/activity was observed; a small number of components were found or traded without clear donor consent; contacts continue informally | Competing provenance, contradictory classified inventories and credible local detective cases | Theft, ownership and the right to share dangerous technologies |
| **C. Misinterpreted contact + later gift** | 1946 ghost rockets mix meteor/missile sightings with actual contact; authorities infer a secret program from ambiguous clues, and a **later** Sirian gift is backdated or attached to old files | Multiple honest witnesses, false leads, Mandela-effect documents and political humor | How do officials admit they built a vast bureaucracy on an uncertain premise? |

**Recommendation for Tomi:** combine A and C only if the author wants a *real* Finnish transfer while preserving genuine mystery: a **small, genuine Sirian/Confederacy-associated artifact or biological exchange**, surrounded by many mundane or mistaken ghost-rocket reports, later buried under retrospective myths and declassification. The source/cause of specific encounters can remain disputed. Do **not** decree this combination canonical in the draft.

### Four different national histories, not a single Nordic department

| Country | 1946/modern historical anchor | **[HYPOTHESIS]** specialization, deliberately unconfirmed |
|---|---|---|
| **Finland** | 1946/1947 reporting and later Finnish disclosure plot | Practical component reverse-engineering; cryogenics, fusion/safety, hybrid biologics, psychotronics and emergency governance |
| **Sweden** | Large 1946 inquiry, material/aircraft investigations | Aerospace, sensors, alloys, propulsion and industrial production |
| **Norway** | Hessdalen instrumented observations from 1984; older Ghost Flier reports | Plasma-like light, environmental monitoring, transmedium/noetic sensing |
| **Denmark** | 1946 reported lights, much later SUFOI archives | Biological/medical or quantum interpretation; possibly **data/liaison only**, not a crashed craft |

**The organization:** bilateral personnel, fragile university–military–industry links, Nordic committees in isolated eras, and personal contacts or archive handoffs. An investigator should find **incomplete overlapping chains of custody**, not a comprehensive top-secret directory named "Nordic MJ-12". Cross-border cooperation can rise and fall with politics. The **1950s Soviet ПРОГРАММА** and American MJ-12 remain separate mysteries with potential contacts/overlap, not explanatory keys that resolve everything.

**Minimal divergence rule:** a fictional program might marginally accelerate specialist materials, computing, industrial safety, bioengineering or sensors, but nothing about actual postwar Finland, Sweden, Norway or Denmark should be retrospectively credited wholesale to aliens. Civilian scientists, labor, universities, welfare institutions and political conflict retain their historical agency.

### A sample provenance ledger for Tomi [SCENE]

| Claim | Claimed period | Public record that actually exists | Possible secret source | Verification status |
|---|---|---|---|---|
| Finnish astronomer witnessed rocket-like object | 1946/1947 | Contemporary U.S. attaché reporting on Finnish press | None necessarily | Report established; phenomenon unknown |
| Swedish military investigated spökraketer | 1946 | Swedish National Archives historical account | A fictional separately classified workstream | Investigation established; recovered alien item **unverified** |
| Nordic scientists had a strange component | [OPEN] | No real historical verification offered | Proposed Sirian object, possible misidentification | Entire component **fictional** |
| Norwegian Hessdalen sensor recorded unusual light | 1984 | Project Hessdalen field report | Could be entirely unrelated to 1946; later noetic extrapolation | Investigation documented; NHI link unverified |
| Danish researcher possesses 1946 hybrid-related dataset | [OPEN] | No real 1946 material recovery verification supplied | Fictional transfer or later database reclassification | **Proposal only** |

A compelling dossier may contain a real press clipping, an authentic 1950s cabinet minute, a forged later appendix and a witness's incompatible memories. **Source authentication ≠ factual truth of extraterrestrial interpretation.** The first campaign can reveal who copied an archive without revealing who sent the object.

## 7. Crisis historiography: why there cannot be a single clean timeline

**[AUTHOR PROPOSAL]** War, nuclear interceptions, rogue AI, machine-ecology collapse, contact, quarantines, psychic awakening and mass religious/political transformation overlap in records and memories. Some episodes are genuinely simultaneous; others *appear* so because information systems, archives or cognition were compromised.

**Use evidence strata:** (1) canonical public baseline, (2) independently corroborated in-world documents, (3) institutional allegation/secret account, (4) testimony, dream, hallucination or astral perception, (5) Mandela-effect contradictions. The narrator may reveal which *file* is genuine without resolving what *world-state* caused it.

**Candidate incidents, awaiting approval** from #1156 dossier: EU–Russia war and intercepted nuclear launch; machine-ecology damage at **Hyvinkää**, severe **Loviisa** incident; Confederacy contact and Sirian protection/technology; Grey EEZ ambitions and hybrid controversies; Reptilian raids; expanded psi/mediumship/prison regulation; fictional Catholic Noösphere turn with Pope Teilhard II; unidentified jellyfish UAPs. Their **relative causal dependencies** must be checked against the First Contact chapter, and unapproved absolute years must not enter the canonical timeline.

**Never decide:** what truly happened in the Soviet Mandela Effect; whether MJ-12 or ПРОГРАММА now exist, how powerful they are, why some memories contradict records; whether *every* jellyfish UAP is an organism; or precisely which 1946 Nordic dossier is an intentional gift versus accident. The campaign can solve a case *within* an unsolved cosmology.

## 8. Helsinki-to-Nordic mission spine (examples, not assignments)

| Episode proposal | Place | Immediate human stake | Lore/mod hooks |
|---|---|---|---|
| Ghost Rocket authentication | Kruununhaka archive | A living claimant's pension and secrecy allegation | CWN forensic/records competence; two contradictory 1946 files |
| Provenance and ethics | Otaniemi | Lab worker implicated in concealed medical trials | Cyber/evidence tags, research rights |
| Divergent Swedish file | Stockholm | Witness protection for a records custodian | Europol joint investigation, Swedish military archives |
| Hessdalen observation | Norway | Protect a scientist and nearby residents amid unusual lights | Instrument uncertainty; AWN *only if* genuine field hazard |
| Copenhagen's contradictory dataset | Denmark | Who legally owns a potentially sensitive patient record? | Legitimate 1946 press reports ≠ confirmed lab from 1946 |
| Machine-zone rescue | Hyvinkää | Missing worker and family | CWN + **AWN scarcity/hazard/stress**, possibly strange living machines |
| Loviisa compensation inquiry | Loviisa | Reactor-area workers deserve truthful exposure records | CWN investigation + specialist crisis overlay; **no sabotage how-to** |
| Parliamentary disclosure | Helsinki | Accountability for decades of secret spending | Political/social factions, institutional comedy |
| Sirian–Confederacy consultation | Proposed diplomatic zone | Did an ally's "gift" violate recipients' autonomy? | NHI difference and high-stakes interpretation |
| PSI prison civil rights | Sörnäinen | A psychic detainee may be denied due process | Investigation/PSI tags, rights; no real facility access specifics |

**Tone ramp compatibility:** Act I Europol rookie missions remain **mundane**. The old 1946 file might first appear as a newspaper clipping or misfiled archive metadata, not an overt alien relic. AWN hazardous zone work belongs later. Greater Helsinki neighborhoods retain ordinary work, dating, pubs and transit between dramatic excursions.

## 9. Five small author-facing scene cards

Each follows the same **CWN case first, optional specialist module later** discipline:

**A. "The form that survived three paradigms"**  
- Start [A]: office has a 1970s-era procedure for incident classification.  
- Shift [C]: review who benefits from its preservation.  
- Shift [B]: a noetic visitor appears as a composite impossible geometry.  
- Consequence: a civil-rights test case, not a new combat stat.

**B. "Two countries, one rocket"**  
- Start [C]: compare Finnish press and Swedish military archives.  
- Shift [A]: both governments billed the same nonexistent telemetry contractor.  
- Shift [B]: a nonhuman-looking artifact is **claimed** by a witness, but could be manipulated.  
- Consequence: lead to lawful lab work, not automatic Confederacy proof.

**C. "Please return the machine ecology unharmed"**  
- Start [A]: government standard form lists contamination categories that cannot describe Hyvinkää.  
- Shift [B]: an autonomous machine forest consumes a derelict workshop.  
- Shift [C]: rescue and resource allocation involve different vulnerable populations.  
- Consequence: activate AWN hazard/scarcity only for this field mission.

**D. "The Helsinki right to refuse paradise"**  
- Start [C]: debate whether citizens may decline collectivizing PSI therapy.  
- Shift [A]: the vendor offers a bundled family discount on consciousness subscriptions.  
- Shift [B]: a benevolent alien representative cannot understand the concept of *individual billing*.  
- Consequence: negotiated privacy/consent and local political faction positions.

**E. "Claims adjuster, extraterrestrial"**  
- Start [B]: serious Reptilian assault, nontrivial casualties.  
- Shift [A]: insurer disputes coverage under an existential-threat exception.  
- Shift [C]: workers and victims organize a class-action/municipal accountability case.  
- Consequence: sustained grief, real costs, and a procedural investigation; humor never targets fatalities.

**Writing rule:** the **mode sequence is optional**, the **cause-and-effect ledger is not**.

## 10. Author decision queue

1. **1946 transfer:** which model A/B/C, if any, becomes **actual setting history**? How much remains unsettled to the player?
2. Should the **Confederacy** openly authorize Sirian aid, tacitly allow it or later disavow how it was handled?
3. Are *some* Swedish, Norwegian and Danish contacts true transfers, or mostly observations and intelligence exchanges?
4. Which classified organization owned the first Finnish artifact? Preserve compartmentation until decided.
5. What *small* visible technological divergences occurred before 2045, and which are falsely attributed to NHI?
6. Does the Finnish president's **contact since 1946** statement assert knowledge of a physical transfer, intermittent contact, or a politically simplified public account?
7. Which Hyvinkää and Loviisa incidents are author-approved, and what does AWN physically model at each?
8. Which AWN stress/hardening procedures are already fully tabletop/Python compatible? Audit before any future switch.
9. Does the 50/25/25 model remain a background qualitative heuristic or become an NPC distribution for social-science simulation? Avoid presenting it as empirical demography.
10. What does **"Carnivalesque Social Science Fiction"** mean as an optional *editorial label*, and how explicitly should it appear in author-facing style notes?
11. Which evidence in the 1946 investigation is intentionally **fabricated within the fiction**, and which is sincere but mistaken?
12. How can a player distinguish an authentic document from a true interpretation **without** ever receiving definitive answers to every Mandela-effect anomaly?

## 11. Implementation boundary, references and next steps

**What this memo does:** records the three writing modes, AWN gating philosophy, catastrophic-normality setting, differentiated Nordic historical anchors, three rival contact models and sample mission/scene cards. It **does not** update the playable timeline, the Crisis plot, approved faction structures, source documents or rulebook mechanics. This is suitable for Tomi to edit or adopt in parts.

**If approved later:** integrate author-accepted history into the appropriate existing `docs/world/` source and source-of-truth timeline *without changing the unordered-milestones rule*; use already approved CWN/AWN compatibility modules, tabletop and Python in one authorized change; link any localized episodes to the campaign/graph authoring work; preserve separate research provenance for historical claims. No automatic implementation occurs after author review.

**Repository crosslinks:** [#1168](https://github.com/TomiToivio/NooPunk/issues/1168), [#1156](https://github.com/TomiToivio/NooPunk/issues/1156), [#1109](https://github.com/TomiToivio/NooPunk/issues/1109), [#928](https://github.com/TomiToivio/NooPunk/issues/928), [#1083](https://github.com/TomiToivio/NooPunk/issues/1083), [#105](https://github.com/TomiToivio/NooPunk/issues/105), [#106](https://github.com/TomiToivio/NooPunk/issues/106), [#1121](https://github.com/TomiToivio/NooPunk/issues/1121), [#1123](https://github.com/TomiToivio/NooPunk/issues/1123), [#1120](https://github.com/TomiToivio/NooPunk/issues/1120).

**Nonnegotiable:** After Tomi edits, obtain **explicit author approval** before changing canonical lore, tabletop RPG rulebook, Python engine or campaign. A useful mystery is not a continuity bug: **archives can be authenticated, yet the world can remain unreliable**.
