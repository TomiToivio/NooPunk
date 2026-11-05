# Issue #1174: Europol Academy rookie, recruitment tracks, awakening and field kit

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** Design only, no playable new mechanics, no changes to CWN source or NoöPunk rules code. Companion to [#1174](https://github.com/TomiToivio/NooPunk/issues/1174) and the five subsystem drafts of [#1137](https://github.com/TomiToivio/NooPunk/issues/1137). Author must approve before simultaneous tabletop/Python implementation.

## 0. Preflight, authoritative rules and genuine conflict

- [CWN baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md): 6 attributes, 19 standard CWN skills, background/contacts, **two starting Edges, one starting Focus** (two Foci only with Focused), conventional CWN advancement. The [Edge/Foci selection contract](../../src/rules/cwn_edges_foci.py) also handles the conditional Underdog exception; never silently claim *exactly* two under every special rule.
- The [SRD background inventory](../../data/rules/cwn/srd_tables.json) has 20 existing entries including **Law Enforcement**, **Bureaucrat**, **Coder**, **Soldier**, **Spy**, **Technician** and **Doctor**. The free skill for Law Enforcement is **Notice-0**; Coder is **Program-0**; Bureaucrat is **Administer-0**; Soldier grants **Any Combat-0**; Spy is **Sneak-0**. Preserve all background Growth/Learning picks and contacts; see [background contract](../../src/rules/cwn_backgrounds.py).
- [CWN Foci catalogue](../../src/rules/cwn_foci.py) has **26 Foci**, among them **Deadeye**, **Alert**, **Specialist**, **Expert Programmer**, **Drone Pilot**, **Diplomat**, **Authority**, **Unique Gift**, **Ace Driver**. This file confirms names and legal levels, **not** that a proposed Focus's detailed benefits are approved.
- **Conflict to decide:** [#1137 Academy draft](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md) concludes **no new Edges/Foci needed**, whereas #1174 specifically asks for **Academy Edge + one Grunt/Geek/Freak Edge**. Both cannot be canon automatically. This document gives **Route A (immediately CWN-legal)** and **Route B (author-proposed two custom Edges)**. The former is a runnable starting *selection structure* with source-legal options; the latter is homebrew awaiting mechanical approval.
- The [first campaign](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) fixes Europol service, StO protagonist and delayed Wanderer revelation. [Europol Helsinki](../world/EUROPOL_HELSINKI_1114.md) limits cross-border police powers; Finnish police retain arrests/searches. The [PSI investigation boundary](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md) prohibits automatic investigative solutions from psychic powers.
- **Known existing implementation hazard:** [field_agent.py](../../src/rules/field_agent.py) still names a legacy `Investigate` agency skill even though `Investigate` is **not** among CWN's 19 skills. Do **not** reuse its agency-grant as an extra free starting skill or treat that standalone generator as proof of full legal CWN character creation. This draft does not modify it.
- Use [author BIONICS.md](../../design/BIONICS.md) and the [Bionics](DRAFT_NOOPUNK_BIONICS.md), [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md) and [Psionics](DRAFT_NOOPUNK_PSIONICS.md) drafts for discipline boundaries. AWN mutation resemblance is a balance source, **not** a second rules engine.

## 1. The usable character-creation decision

**Recommended public-facing structure:** one earlier **Background**, an **Academy qualification**, one **Grunt/Geek/Freak recruitment track**, normal **Edge 1 / Edge 2 / Focus 1**, mandatory **agency issue** and separately tracked **Awakening** state. Institutional access is conditional on employment, legal authorization and the scene. Background is not retroactively changed by graduation; career training survives suspension; the agency owns its gear.

**Route A, compatible now:** `Academy Graduate` = narrative credential/training record; `Grunt|Geek|Freak` = descriptive recruitment tag; **two actual published CWN Edges** and **one published CWN Focus** using the source text. No bonus attributes/skills from tags. The existing [#1137](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md) audit prefers this route. In a Freak route, no *free* natural PSI power at level 1: either select the complete published SWN Psychic/Partial Psychic package under the baseline's alternative character creation rules (which **replaces**, not stacks with, parts of the CWN operator package), or wait for author approval of a bounded NoöPunk power Edge.

**Route B, author proposal:** `Edge 1 = Europol Academy Graduate`; `Edge 2 = Grunt` **or** `Geek` **or** `Freak`; **one normal CWN Focus**. These consume both ordinary Edge slots, not two plus other Edges. Each custom Edge needs comparable value to an existing published Edge, formal prerequisites, in-game action text, anti-stacking, and golden tests before adoption. Equipment and job access are **not** supernatural Edge features or permanent player wealth. The #1174 request prefers Route B as its character fantasy. **Never label a Route B sheet as currently CWN-legal.**

### Route B candidate specifications [P, not yet enacted]

| Proposed Edge | Permanent intrinsic effect proposed for balance review | Exclusions and non-mechanical flags |
|---|---|---|
| **Europol Academy Graduate** | One constrained **choice** from the Academy's training list (e.g. Notice, Talk, Administer, Connect or Know) *subject to the legal initial-skill cap and duplicate-pick procedure*. Stronger possible alternative: **one narrow counterintelligence situational permission**, not blanket +1 to investigations. Compare with an existing skill-oriented Edge and reduce if stronger. | `europol_graduate` qualification persists; `europol_active` job, credentials, badge, weapon, housing, AI access **do not** persist after dismissal. Do not give all five skills. |
| **Grunt** | Narrow operational specialism, e.g. one existing combat-related Edge effect or one bounded field competency. Prefer using an actual published CWN Edge and attaching `recruitment=grunt`. | Police experience ≠ legal authority to conduct EU-wide searches; SWAT experience does not confer a perpetual squad. |
| **Geek** | Narrow analysis/programming specialism, ideally analogous to a published skill-oriented Edge; one small benefit, **not** unbounded `Know + Program` rank increases. | Data analysis ≠ instant all-record access; hacking still needs CWN programs, deck, privileges and checks. |
| **Freak** | Exactly one narrow *non-omniscient* defensive or consensual contact capability if the PSI draft provides a complete source-legal acquisition/cost path. Treat as a **power Edge** for Underdog exclusion; no simultaneous SWN Psychic package benefits. | Professional telepathy job history and StO destiny are **not** themselves new power points. |

All four need author-approved exact power level, activation/action timing, checks or resources and counterpart CWN Edge comparison. `Psychic Awakening` is **not** a third Edge or a free Focus disguised as one.

## 2. Three starting sheet *blueprints* and one common chassis

**Sheet construction protocol (all):** choose one legal CWN attribute method (3d6 in order with its permitted adjustment **or** 14/12/11/10/9/7 standard array); apply one Background's free skill and Growth/Learning choices; pick contacts; use exactly two normal Edge selections and one Focus selection (unless using source exceptions); apply remaining normal free skill pick, languages, money, HP/AC/saves/System Strain; then add agency records *without skill or Edge grants*. All skills start capped at **level 1**. The proposed array below uses the legal fixed scores but is a **design suggestion**, not an automatically complete character sheet. Compute finished HP/saves/AC through CWN, not guessed fixed values.

| Field | **GRUNT** | **GEEK** | **FREAK** |
|---|---|---|---|
| Recruitment | Former Suomen Poliisi tactical investigator | Exceptional research / OSINT / cyber analyst | Natural psychic sensitiveness, recruited to study PSI |
| Proposed earlier Background | **Law Enforcement** (Notice-0) | **Coder** (Program-0), or Bureaucrat (Administer-0) if non-programming researcher | **Law Enforcement** (Notice-0) for a previously employed officer, or **Spy** (Sneak-0) for professional psychic liaison; a bespoke Psychic background awaits approval |
| Fixed attribute array emphasis | STR 11 / DEX 14 / CON 12 / INT 10 / WIS 9 / CHA 7 | STR 7 / DEX 10 / CON 9 / INT 14 / WIS 12 / CHA 11 | STR 9 / DEX 10 / CON 11 / INT 12 / WIS 14 / CHA 7 |
| Source-legal Focus *example* | **Deadeye** or **Alert** | **Expert Programmer** or **Specialist** | **Alert** or **Specialist** (no inherent PSI power) |
| Route A Edges | Choose **two published CWN Edges** per actual source rules; track Academy + Grunt as narrative tags | Same two Edge budget; Academy + Geek narrative tags | Two published CWN Edges *only if mundane*. For active PSI use SWN **complete alternative psychic package**, not a free third benefit |
| Route B Edges **[P]** | Academy Graduate + Grunt | Academy Graduate + Geek | Academy Graduate + Freak |
| Illustrative legal skill interests, not free grants | Notice, Shoot, Talk, Drive, Exert | Program, Know, Notice, Administer, Connect | Notice, Talk, Connect, Know, psychic abilities **only if separately authorized** |
| First-scene contribution | Catches tampering at the physical scene; handles danger under Finnish lead | Finds the disputed document trail, provenance, OSINT contradictions | Notices tension and anomalous signals **without becoming a lie detector** |
| Basic shared institution kit | **Identical** for all three tracks | **Identical** | **Identical** |

**Why no fabricated final skill totals:** the background-specific Learning table, selected Edges and Focus benefits are required to produce a valid finished sheet. Since Route B Edges are not yet source-backed and the exact Edge catalogue effects have not been approved, a numerical Route B level-1 sheet would pretend an incomplete homebrew proposal is legal. Phase B must generate three **fully audited legal** CWN sheets with source IDs and golden tests; for Route A, use exact published Edge texts. Do not claim a Freak psychic is a legal ordinary CWN operator with free SWN powers.

## 3. Compact extensible option catalogue

| Concept | Normal location in character model | Rules consequence |
|---|---|---|
| National Police / Law Enforcement | Existing **Law Enforcement Background** | CWN background skill and picks; national-service history in a tag |
| Soldier / military | Existing **Soldier Background** | CWN background skill and picks; SWAT is training/Focus depending on role |
| Academic / researcher | Existing **Bureaucrat**, **Coder** or **Doctor**, depending on professional history | `academic` career tag; **new Academic Background only if a genuine table gap is demonstrated** |
| Programmer / cyberforensics | Existing **Coder Background** or **Expert Programmer Focus** | Same CWN Program and hacking rules |
| Professional telepath | **New psychic-profession Background candidate** with ordinary paid job/contacts | PSI access is **separate** and must be purchased/authorized via one approved psychic rules package; a job title alone grants none |
| Field Agent | **Existing Law Enforcement or Spy Background** for career officers, or career/Academy qualification for later recruits | No second background free skill |
| Europol Academy Graduate | Shared **proposed Edge (Route B)** or qualification tag (Route A) | Elite training, but no automatic police jurisdiction or unlimited kit |
| Grunt / Geek / Freak | **Proposed second Edge (Route B)** or recruitment track (Route A) | Exactly one per starting campaign PC, not classes |
| Psychic Awakening | **Campaign progression flag** | Four descriptive levels linked to three acts/stages; cannot stack with Edge/Focus advancement |

All entries need source citations, normal acquisition requirements, and legal tabletop presentation before migrating into the rulebook.

## 4. Awakening ladder mapped to narrative staging (GM-only spoilers)

| State | GM story stage | Observable behavior | Player access, safeguards |
|---|---|---|---|
| **0 Latent** | Stage 1, grounded rookie / Act I | unusual dreams, passive empathy, defensive implant warnings | No innate active PSI for Grunt/Geek; Freak's existing formally purchased power remains narrow. No secret biography exposed |
| **1 First Contact** | Stage 2 / Act II | scripted catalyst, limited empathic attunement and defensive response | Source-approved one technique at a time, conditional targets; consent and Mental save/defence where relevant |
| **2 Control** | Stage 2 to early Stage 3 / Acts II–III | bounded telepathic exchange, possible supervised astral travel | No private-mind scraping; limited reach, detection, anchor/return; pay one approved resource system, not SWN Effort + AWN pool + strain for same effect |
| **3 Integration** | Stage 3 / Act IV, author's final reveal | Higher Self/Wanderer biography and preselected more sophisticated powers | Spoiler-only gate; not a public choice in the character creator, no indefinite free projection or automatic case solutions |

**Three story stages, four descriptive milestones** is intentional: level 1 and 2 are intermediate steps of Stage 2. A Freak has **earlier practical awareness**, not an alternate destiny. No alignment slider: the canonical protagonist is StO throughout; normal moral/political/personal choices shape relationships and reputation, not a path to StS. In-world characters may call this `awakening`, `noetic transition`, `integrated awareness`, not necessarily Law of One density terminology.

## 5. Equipment manifest, custody and rule routing

**Principle:** The issue intentionally gives a *lavish agency kit*. This is not a free CWN character wealth windfall, purchasable from starter credits or transferable on dismissal. All items have `owner`, `custodian`, `authorized_mission`, `condition`, `power_or_ammo`, `evidence_log` where relevant. Exact item price and damage use a **verified CWN catalogue reference** (e.g. `heavy_pistol`) or are **TBD** with no fabricated stats.

| Item | Custody | Tabletop procedure and limitations | Failure/availability |
|---|---|---|---|
| **Large-framed service gun** (big and nasty) | Individually signed out / issued, Europol property | Prefer CWN **heavy pistol** catalogue profile; any more powerful gun is mission-issued and subject to Finnish jurisdiction, holster, ammunition and CWN attack/encumbrance | Ammo, confiscation, suspension, safe storage and use-of-force review |
| Body armour, less-lethal option, cuffs, trauma kit | Personal issue/vehicle, as authorized | CWN armour, healing and equipment rules; training cannot waive constraints | Protection/charges/consumables; nonlethal tools are not automatically harmless |
| **Cranial jack BCI** | Europol-issued implant | Linked to **CWN cyberware** surgery/System Strain, identity authentication and network access | Disconnect, jamming, compromised updates, maintenance |
| **Passive/defensive QIP implant** | Europol-issued implant | Conscious operator, explicit approved defence trigger, **non-stacking** with natural psychic defence; never grants broad telepathy | Calibration failure, strain/maintenance TBD by psychotronics draft |
| **Standard biotech/bionics course** | Clinical treatment in PC's body; institutional medical record | Deliberate AWN-mutation-inspired *benefit/drawback* selected after author approval, not random mutation and not cyberware | Aftercare, detectability, medical eligibility, no science-fiction universal super-serum |
| Bodycam, ID, badge, encrypted police **radio** | Mandatory duty kit | Bodycam continuously sends to **human-led Dispatch** when on duty; radio remains deliberately clunky parallel channel; logged lawful use | Signal loss, tampering alert, protected off-duty privacy exceptions |
| **Brick cyberdeck** with cable to BCI | Issued hardware, not fused to head | **Evidence/OSINT**: files, provenance, contradictory statements, SafeNet searches and court-ready records. **Cyber**: entirely existing CWN hacking/Program/deck rules and graph view, as in *DROP* / *Midnight Protocol* | Network disconnect, account permissions, intrusion detection, device bulk, battery |
| Multimode scanner | Checkout or assigned field case | Modes: optical/spectral, limited chemical, residue, biometrics and fictional anomaly sensitivity where authorized. Record **provisional findings**, send structured readings to Dispatch narrow forensic model | Blind spots, calibration, contamination; **bag and send samples to physical lab** |
| Romppainen–Fujita psychotronic interrogator | **Restricted** agency instrument, usually deployed in interview room or vehicle case | *Silicon Dreams* / Voight-Kampff-inspired **questions + emotion response channels**. Display confidence/uncertainty, baseline calibration and possible NHI markers. Investigator interprets; **never a reliable lie/hybrid detector** | Consent, privacy, countermeasures, false positives/negatives, judicial oversight, specialist availability |
| Police vehicle with cameras and drone dock | Vehicle pool, assigned per mission | CWN vehicle/Drive and vehicle fittings; secure evidence transport, feeds, route/map support | Damage, fuel/power, network loss, crash, tracking; remote control **only under preauthorized human emergency instruction** |
| Portable surveillance drone | Vehicle mount, mission checkout | CWN drone operation, battery/range/signal and privacy rules; stream to human Dispatch | Jamming, concealment, battery loss; AI may **assist piloting** but never decide deployment/attack |
| Dispatch human + narrow AI | Shared service, not owned by PC | Mission controller authorizes orders; AI does transcription, search, alerting, bounded lab/forensic assistance and data collation | Human operator busy, system unavailable, wrong model inference, spoofed feed; **AI never independently decides** |
| Laura Wendt / Harri S. Romppainen / specialists | Independent NPC/team assets | Wendt accompanies most missions; Romppainen some; others on tasking, not property or automatic action economy | Other assignments, injuries, disagreement, reputation and liaison limits |
| **Kurvi apartment** / Europol office | Agency-owned housing/access | Starting social scene and workplace; player is occupant/employee, not titleholder | Reassignment or dismissal, legal tenancy/privacy protections to specify |

**Extra kit worth shipping as fiction:** tamper-evident seals, forensic labels and gloves; swabs and evidence bags; PPE/respirators, NHI containment and radiation/chemical alarms only as specialists authorize; portable lighting; offline paper maps and notebook; chargers, spare batteries, data adapters, Faraday bags/secure cases, multilingual interpreter access, encrypted evidence backups, authorized surveillance/counter-surveillance tools, radio repeaters, tactical team and paramedic callouts. Distinguish **always carried**, **vehicle locker**, **office checkout**, **restricted specialist support**. Never silently put every kit item in personal encumbrance.

### Dispatch authority contract

1. `human_dispatch_controller` is responsible for orders, escalation, interrogation approvals and exceptions. Multiple agents may share a controller; an AI alert is never itself an order.
2. `dispatch_ai` provides **narrow subsystem outputs** only: transcription, classification, suggested routes, forensic hypothesis and field-feed monitoring. Every AI output carries provenance, model confidence and human review state.
3. `drive_remote` and `drone_remote` only execute authenticated human orders, with **previously authorized emergency conditions** for vehicle override. If authorization is lost, fail safe; do not turn an AI route suggestion into autonomous policing.
4. Search, seizure, arrest, invasive interrogation and classified access require corresponding human/legal authority; a Europol Academy credential does not grant these automatically.
5. Capture/retention of bodycam/drone/suspect emotions needs chain of custody, role-based access, privacy exceptions, logged disclosures and evidence integrity checks.

### Cyberdeck: two interfaces, one rules engine

- **Evidence/OSINT** (reference: [*Orwell*](https://store.steampowered.com/app/491950/Orwell_Keeping_an_Eye_On_You/)): select claims, open legal records, compare contradictory identities, annotate provenance, preserve originals, submit a reasoned dossier. Use existing CWN Notice/Know/Administer/Connect/Program checks where justified; core clues are available by proper investigation, not hidden behind one mandatory roll.
- **Intrusion/Cyberspace** (reference: [*DROP*](https://store.steampowered.com/app/1902300/DROP_System_Breach/) and [*Midnight Protocol*](https://store.steampowered.com/app/1162700/Midnight_Protocol/)): show **graph nodes, access paths, programs and countermeasures** using **unchanged CWN hacking** timing, permissions and checks. The visual graph is not a replacement skill minigame and hacking is never justified by mere possession of the cyberdeck.
- **Evidence custody is shared**: any copied file must include time, source, authority, actor and a provenance trail. Investigations can survive an unavailable deck by official records or a lab request.

## 6. Tabletop vertical slice: “The Missing Container”, Helsinki

**Playable without any approved custom Edge or PSI.** Opening scene at Kurvi apartment; briefing at Europol Helsinki. Finnish Police request help with a cargo container transferred through different companies. The container has physically arrived but its digital import record says it never existed. All three tracks can discover the **core clue**: the manifest's custody signature belongs to a defunct subcontractor.

| Beat | Information / fair resolution | Grunt / Geek / Freak spotlight |
|---|---|---|
| 1. Dispatch briefing, bodycam check | Human controller assigns scope; AI displays **suggestion**, not conclusion. No roll for basics. | Grunt asks for scene-security contact; Geek requests logs; Freak notices another officer's stress, not secret motives |
| 2. Physical site, scanner | Scan of seal shows ambiguous synthetic residue; **core original serial number is visible** and baggable. CWN Notice/Know may add optional context; Finnish officer handles seizure. | Grunt sees replacement rivets; Geek recognizes production batch; Freak notices unease but **cannot name an NHI** |
| 3. Evidence/OSINT cyberdeck | The real signature appears in a lawful shipping archive after a basic authorized query. CWN Administer/Know/Program for *extra* metadata; provenance recorded. | Grunt interviews dockworkers; Geek links timestamps; Freak gets a willing witness to talk |
| 4. Interview with Romppainen–Fujita device | Subject consents under appropriate procedure; emotional graph spikes at a company name. This is **not proof of lying or hybrid identity**. Talk/Notice for interpretation, follow-up records for corroboration. | Grunt probes procedural detail; Geek cross-checks graph and ledger; Freak may sense confusion, **not read secrets** |
| 5. Optional authorized CWN cyber intrusion | If national/international legal approval exists, run original CWN hacking from nodes/programs. **Optional** route yields extra data; cannot lock core clue behind hacking or PSI. | Geek leads; Grunt protects access point; Freak monitors person-to-person contact |
| 6. Human review and Finnish handoff | Dispatch analyst compares the source record with physical seal. Finnish Police make any arrests or execute compulsory searches. | All three can assemble the same actionable report |

**Failure branches:** no drone feed → physical observations and interviews; broken scanner → bag/send sample; false-positive emotional signal → verify with ledger; inaccessible SafeNet → seek official request; unavailable Romppainen → traditional interview; denied hacking authorization → case still progresses. No single supernatural or cyber skill is a mandatory key.

## 7. Engine-neutral data contract [design only]

```text
RookieDraft {
  character_id, level=1, cwn_background_id, cwn_attribute_generation,
  cwn_attribute_scores, cwn_background_skill_choices, cwn_contacts,
  cwn_edge_ids[2], cwn_focus_levels, cwn_skills, recruitment_track,
  academy_qualification, europol_active, authorized_role_permissions,
  employment_housing_ref, issued_asset_ids, current_case_id,
  gm_only: { awakening_milestone, awakening_stage, wanderer_secret, psi_sources }
}
IssuedAsset {
  id, canonical_cwn_item_id|null, owner="Europol", custodian,
  category, clearance, issue_record, encumbrance_rule_ref|null,
  ammunition_or_charge, equipment_status, approved_uses
}
EvidenceArtifact {
  id, original_source, provenance, custodian, collected_at,
  collection_authority, chain_of_custody, lab_status, ai_findings_with_confidence
}
DispatchCommand {
  request_id, human_approver, scope, authenticated_actor, authorized_action,
  machine_assistance, audit_log, revocation_reason
}
```

The structures are **proposals**, not executable code. Source-legal selections must delegate to `cwn_backgrounds`, `cwn_edges_foci`, `cwn_foci`, `cwn_hacking`, `cwn_drones`, `cwn_vehicles`, `cwn_cyberware`, `cwn_encumbrance` and the existing skill resolver. The same state must serialize to paper sheet, CLI and Evennia; **no separate minigame rules**.

**Phase B parity tests (only after author acceptance):** validate each background skill pick and cap; reject a third normal Edge; reject unapproved custom Edge IDs; ensure Grunt/Geek/Freak are mutually exclusive; verify Academy qualification alone never changes employment powers; verify equipment losses revoke access without removing skills; prohibit double-PSI charges and unrestricted target-reading; ensure Dispatch commands cannot originate from AI; replay the same evidence sequence with all three tracks and verify identical required clues; ensure no additional law-enforcement jurisdiction arises from credentials.

## 8. Author decision queue (explicit)

1. **Route B** custom Academy + specialization Edges, or **Route A** published Edges plus Academy/recruitment qualifications? #1174 requests B; #1137 audit recommends A. **Do not decide silently.**
2. If B, should Academy grant **one controlled skill pick** or a unique limited counterintelligence action? Confirm exact comparison Edge and printed effect before source-backed numbers.
3. A Freak **with real active starting PSI** must use either a complete SWN alternative package or an approved narrow new power Edge. Which? No cherry-picked full Psychic benefits on a standard 2-Edge CWN operator.
4. Is the canonical pregen always Law Enforcement before Academy, or does each recruitment track choose a different old career? Recommend one common protagonist with three alternate pre-careers for replay.
5. Which bionic trait and implant defence are standard and what are exact **AWN/CWN** costs and limits? Resolve in #1137 proposals, not here.
6. Is big service gun a **heavy pistol** in every mission, or a more restricted specialist long gun? Who issues firearm authority in Finland?
7. Does the field agent have a *car permanently assigned* or only per-mission pool access, and when can Dispatch exercise preapproved remote control?
8. Which procedural rights govern the Romppainen–Fujita interview and suspect privacy? It must never become a magical lie detector.
9. Align character creator spoiler masking with staged awakening and the finale; **never expose the true Wanderer mission as a starting choice**.
10. Keep issue **open** through author review; only after approval create rulebook + Python + tests in the same change.

## Sources and traced repositories

- CWN SRD and Python parity: [CWN baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md), [background catalogue](../../data/rules/cwn/srd_tables.json), [background mechanics](../../src/rules/cwn_backgrounds.py), [Edge/Foci structure](../../src/rules/cwn_edges_foci.py), [Focus catalogue](../../src/rules/cwn_foci.py).
- Campaign and institutions: [Campaign 01](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md), [Europol Helsinki](../world/EUROPOL_HELSINKI_1114.md), [PSI investigation boundary](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md).
- Connected design drafts: [#1137 character](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md), [PSI](DRAFT_NOOPUNK_PSIONICS.md), [psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md), [bionics](DRAFT_NOOPUNK_BIONICS.md), [author specification](../../design/BIONICS.md).
- Inspirational interfaces, **not imported mechanics**: [Silicon Dreams](https://store.steampowered.com/app/1272070/Silicon_Dreams_cyberpunk_interrogation/), [Orwell](https://store.steampowered.com/app/491950/Orwell_Keeping_an_Eye_On_You/), [DROP](https://store.steampowered.com/app/1902300/DROP_System_Breach/), [Midnight Protocol](https://store.steampowered.com/app/1162700/Midnight_Protocol/).

**Verification status:** This is a source-aware design proposal. Numerical homebrew Edge benefits, full level-1 legal sheets, exact expensive kit budgets, psychic access and subsystem costs are **not** asserted as verified; approving and researching those values is a separate required gate. No new code or rulebook procedure was changed.
