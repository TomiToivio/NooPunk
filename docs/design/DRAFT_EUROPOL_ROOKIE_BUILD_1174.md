# DRAFT — The Europol rookie PC: three legal builds, the Academy Edge, awakening and the issued kit

> **DRAFT DESIGN SPECIFICATION — TOMI REVIEW REQUIRED — NOT IMPLEMENTATION APPROVAL**
>
> Companion to the five #1137 drafts, not a replacement for any of them. This file proposes a **playable starting
> character** and the catalogue around it; it implements nothing and changes no CWN rule.
>
> Deliverables A–F from [#1174](https://github.com/TomiToivio/NooPunk/issues/1174) are sections 2–7 below.

**Evidence labels:** **[SRD]** verified in this pass against the Cities Without Number SRD or this repository's
data/code · **[?]** needs author or source decision · **[P]** proposal · **[C]** campaign canon.

---

## 1. What the rules actually allow — the constraint set

Verified before designing anything, because most balance mistakes here are arithmetic:

| constraint | source | consequence |
|---|---|---|
| **Two Edges at character creation**, a third at level 5 | [SRD] Edges: "A beginning PC chooses two, and may choose a third once they reach the fifth level of experience" | "Academy + one recruitment track" consumes **both** slots. Nothing else may be an Edge. |
| **Bonus Edge** if the final attribute modifier total is ≤ −1 | [SRD] Underdog Rule | a weak-rolled rookie may legally carry three starting benefits; the builds must plan for it rather than pretend it doesn't exist |
| **One Focus**, plus one more with the **Focused** Edge | [SRD] Foci | Focuses are the *only* free place for extra expertise, and taking Focused costs the second Edge slot |
| Background grants a **free skill** plus **two picks** from its Learning table (or three rolls across Growth/Learning); "Any Skill" may not be picked | [SRD] Backgrounds | the Background, not the Academy, is where the character's skill base comes from |
| Edges are stronger than Foci and should grant **options**, not generic competence | [SRD] Edges | an Edge that only adds skill ranks is a badly designed Edge by the SRD's own instruction |
| CWN core is immutable; SWN/WWN/AWN are additive | [repo] `CWN_IMMUTABLE_CORE_1068.md` | no parallel resolution, no second skill economy, no new dice |
| PSI may not grant clues or open exits | [repo] `PSI_INVESTIGATION_BOUNDARY_1105.md` | the Freak's starting ability cannot be a case-solver |

**Verified CWN names used below** — Edges: Educated, Face, **Focused**, Ghost. Foci: **Alert**, Henchkeeper,
Unique Gift, Unregistered. Skills (19): Administer, Connect, Drive, Exert, Fix, Heal, Know, Lead, Notice, Perform,
Program, Punch, Shoot, Sneak, Stab, Survive, Talk, Trade, Work. Any other CWN Edge or Focus name in this document is
marked **[?]** and must be checked against the SRD before it is printed in a rulebook.

### 1.1 The conflict with #1137, stated plainly

The merged [#1137 Europol draft](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md) recommends **one optional Background
wrapper, zero new Edges, zero new Foci**, on the reasoning that CWN already covers police careers. #1174 asks for an
Academy **Edge** and three recruitment-track **Edges**.

Both cannot be true. #1174 is the newer instruction and this spec follows it — **but the #1137 objection is kept as
a test**: every new Edge here must justify why an existing CWN Edge cannot do the job, and the answer is recorded in
§3.2. If the answer is weak for any of them, that Edge should be cut, not balanced.

---

## 2. Deliverable A — three legal builds of the same rookie

All three use the same rules: one Background, **two Edges**, one Focus, standard attribute generation, and the same
agency kit. They differ in *where the competence comes from*, not in how much of it there is.

### 2.1 Grunt — recruited from the Finnish police

```
Background:  Law Enforcement                     [SRD: one of the 20 CWN backgrounds]
  free skill: as the background defines it       [SRD]
  picks:      two from its Learning table        [SRD]
Edges (2):   Europol Academy Graduate
             Recruit: Grunt
Focus (1):   Alert                               [SRD: Notice, cannot be surprised, group initiative advantage]
Attribute:   standard CWN generation, swap once if the SRD method allows
Kit:         issued sidearm + service weapon, armour, BCI, defensive implant, bodycam, radio, cyberdeck
Restriction: no PSI at start beyond the implant's defence
```

**What Grunt is for:** the player who wants the procedural, physical, "kick the door with a warrant" experience.
**What it must not be:** better at shooting than a CWN character who spent their Edges on combat. Grunt's Edge is
**access to national-police procedure and people**, not a damage bonus.

### 2.2 Geek — recruited from a university or a lab

```
Background:  Technician or Coder                [SRD backgrounds; Coder covers software, Technician hardware]
  free skill + two Learning picks               [SRD]
Edges (2):   Europol Academy Graduate
             Recruit: Geek
Focus (1):   Unregistered  or a verified analysis Focus [?]
Kit:         the same issued kit; the cyberdeck is the character's main instrument
Restriction: no PSI at start; no extra hacking dice — CWN Hacking is unchanged
```

**What Geek is for:** the player who wants the case to be solved by *reading*. **What it must not be:** a free
second cyberdeck bonus or a permission to bypass CWN hacking prerequisites.

### 2.3 Freak — recruited for demonstrated PSI

```
Background:  Professional Psychic / Telepath     [P: a new background, or Law Enforcement with a PSI tag]
Edges (2):   Europol Academy Graduate
             Recruit: Freak
Focus (1):   Unique Gift                         [SRD: exactly the Focus for "an ability you would not otherwise have"]
Starting PSI: ONE bounded capability, drawn from Awakening Level 1 (§4), not a tree
Restriction: the starting capability is the *same* grant the Grunt and Geek receive at Level 1 — the Freak does
             not get a better version, only earlier access and the scrutiny that comes with being known
```

**What Freak is for:** the player who wants the gift to be the character's problem from session one.
**What it must not be:** a psychic class. There is no PSI skill, no power list, no third resource.

**Balance note [P]:** the Freak is the build most likely to be unbalanced in either direction. If playtest shows the
early capability trivialises Act I, the fix is **not** to weaken it but to make Act I's mandatory facts immune to it
(which the investigation module already enforces), and to charge it in **exposure** — a known psychic in a Europol
office is a political fact.

### 2.4 The comparison the issue asks for

| | **Grunt** | **Geek** | **Freak** |
|---|---|---|---|
| Background | Law Enforcement [SRD] | Technician/Coder [SRD] | Professional Psychic [P] |
| Edge 1 | Europol Academy Graduate | Europol Academy Graduate | Europol Academy Graduate |
| Edge 2 | Recruit: Grunt | Recruit: Geek | Recruit: Freak |
| Focus | Alert [SRD] | Unregistered / analysis [?] | Unique Gift [SRD] |
| Best at | procedure, presence, physical risk | documents, data, intrusion | perception, consent, the uncanny |
| Weak at | abstraction, patience with datasets | physical confrontation, street sense | being believed; institutional trust |
| Starting PSI | implant defence only | implant defence only | one Level 1 capability |
| Core-clue access | equal | equal | equal |

**The last line is the design's most important claim**, and §6 is the proof: no track sees a clue another track
cannot.

---

## 3. Deliverable B — the catalogue

One entry per line, each tagged **Background**, **Edge**, **Focus** or **institutional tag**, so the same fact is
never counted twice.

### 3.1 Backgrounds

| entry | type | grants | notes |
|---|---|---|---|
| **Law Enforcement** | Background [SRD] | police skill base per the SRD table | the Grunt's default; requires no invention |
| **Technician**, **Coder** | Background [SRD] | hardware / software skill base | the Geek's default |
| **Professional Psychic / Telepath** | Background [P] | a *past career*: readings, clients, fraud, burnout; grants social and Know/Notice skills, **not** PSI potency | potency is §4's business. This is the entry that stops "psychic" becoming a class |
| **Academic / Researcher** | Background [P] *only if* no CWN equivalent fits [?] | theory, publishing, institutional access | check the SRD list before adding |
| **Military / SWAT** | Background [P] or prior-service **tag** | tactical competence | a tag is cheaper and avoids a sixth police background |

### 3.2 Edges — and why each one exists

| entry | why an existing CWN Edge cannot do it | grants | explicitly not |
|---|---|---|---|
| **Europol Academy Graduate** | Educated grants a skill and skill points but **no institutional qualification**; Face grants a contact but **no authority to act**; no CWN Edge represents *being a sworn EU officer with a badge that opens doors and no power to arrest* | (1) **Qualification**: may act under Europol authority, request liaison, sign for evidence, use Europol systems; (2) **one** skill at level 0 from {Administer, Connect, Know, Notice, Program, Talk} **not already granted by the Background**; (3) the Rookie obligation: no command authority | no arrest or search power; no extra skill points; no gear discount; no combat bonus |
| **Recruit: Grunt** | no CWN Edge grants a *jurisdiction's* procedure and its people | access to national-police procedure and one Suomen Poliisi contact; may invoke local procedure where a Europol officer could not | no to-hit or damage bonus; no extra weapon proficiency |
| **Recruit: Geek** | Educated/Focused give breadth, not **institutional analysis access** | may route evidence to a Europol lab or controller with a stated turnaround; may treat academic sources as accessible | no hacking bonus; no bypass of CWN hacking prerequisites |
| **Recruit: Freak** | Unique Gift is a Focus and one Focus cannot express a *status* | one Level 1 PSI capability at start; and the status that comes with it (registered, scrutinised, valuable) | no power list, no PSI skill, no second resource |

**Anti-double-dip rule (binding on any later implementation):** the Academy Edge may not grant a skill the
Background already grants. The implementation must check the resolved skill set, not the intended one, and refuse —
which is exactly the bug that would otherwise ship silently.

**Stacking:** Academy is unique and mandatory for this campaign. Exactly one Recruit Edge. No third Edge at start
(the Underdog bonus, if earned, may be spent on a CWN Edge — **not** on a second Recruit Edge).

### 3.3 Foci

Foci stay CWN's: one at start, two with the Focused Edge, and the character may take any Focus they can justify
[SRD]. Recommended picks, none mandatory:

| build | first Focus | why |
|---|---|---|
| Grunt | **Alert** [SRD] | the physical/procedural build benefits from never being surprised |
| Geek | **Unregistered** [SRD] or a verified analysis Focus [?] | the first is a story engine, the second a competence |
| Freak | **Unique Gift** [SRD] | the SRD's own tool for "an ability you would not otherwise have" — and the right place for a bounded psychic edge |

**Do not** create an "Investigation" Focus. The investigation module (§6) already grants core clues for competence
plus declared access and inquiry; a Focus that adds clue-finding would be a second resolver wearing a hat.

### 3.4 Institutional tags (not Edges, not Foci)

`europol_credential`, `clearance:case_files`, `clearance:forensics`, `liaison:finnish_police`,
`housing:kurvi_agency`, `kit:issued`. These are **assets with owners** (§5), not character-building currency, and
losing them must never remove training.

---

## 4. Deliverable C — Psychic Awakening: four descriptive levels, three narrative stages

The ladder is **campaign-granted**, GM-gated, and costs no Edge and no Focus. It exists so that the same character
sheet can carry a story, not so a player can buy powers.

| level | narrative stage | what the character can do | what it costs | what it must not do |
|---|---|---|---|---|
| **0 — Latent** | Act I | dreams, unease, the implant's defensive twitch; nothing reliable | nothing mechanical | no active PSI, no "sense the anomaly" |
| **1 — First awakening** | Act II | **psychic defence** and **bounded empathic reading** (surface emotion, consent or defence) | a condition tag per use; exposure | no secrets, no lie detection, no clue |
| **2 — Controlled practice** | Act III | **telepathy (receive)** within a scene; **short projection** with an anchor and a return rule | the condition + the projection's link boxes | no remote scouting of unseen places, no memory reading |
| **3 — Integration** | Act IV | the **authored package**: Higher Self contact (scripted), a stronger defence, one named advanced capability | narrative cost, and the story's attention | no god-mode, no new resolution, no optional StS branch |

**Mapping rule:** the four levels are *descriptive*, the three stages are *canonical*. Level 1 belongs to the
awakening stage; Levels 2–3 sit inside the practice and integration stages. The mapping may never be inverted, and a
player-facing description must not spoil Act IV.

**What is not PSI:** the implant's defence (technology), the Freak's *reputation* (social), and dreams (scripted).
Mixing them is how a game ends up with three overlapping power systems.

**Investigation limit, restated:** no level grants a clue, opens an exit, or resolves an interrogation. The
`discover()` signature has no psi parameter and must not gain one.

---

## 5. Deliverable D — the issued kit

Every line is an **asset with an owner**, not a character feature. CWN item ids are the canonical ones from
`data/rules/cwn_equipment.json` and `data/rules/cwn_catalogue.json`; prices are deliberately omitted and come from
CWN [SRD].

### 5.1 Personal issue

| item | CWN equivalent | custody | failure mode |
|---|---|---|---|
| Service weapon (large-frame) | `heavy_pistol` [SRD id verified in repo data] | issued, signed for | lost weapon = report + review; use = incident |
| Duty sidearm | `light_pistol` | issued | as above |
| Body armour | `reinforced_clothing` / `armored_clothing` | issued | visible armour is a social fact |
| **Body camera** | none in CWN; a tag | agency, always on duty | outage is logged and questioned |
| **Clunky police radio** | none in CWN | agency | works when the network does not; static, range |
| **Cranial jack / BCI** | cyberware (`cybernetic_baseline` family) | implanted, agency-owned | CWN cyberware rules; removal is surgery |
| **Defensive psychotronic implant** | cyberware | implanted, agency-owned | calibrated to her; useless to a thief |
| Scanner (multimode) | none in CWN; a tool | agency, checked out | preliminary results only; lab confirmation required |
| Evidence kit | CWN gear | consumable | chain of custody is the mechanic |
| Trauma kit | CWN gear (`Heal`) | consumable | — |
| Credentials, tokens | none | agency, revocable | losing them removes *access*, never training |

### 5.2 Vehicle and drone

| item | what it does | what it may not do |
|---|---|---|
| **Police vehicle** | transport, secure storage, drone dock, camera feed to Dispatch | no autonomous driving decisions; remote driving **only** under a human-authorised emergency protocol |
| **Surveillance drone** | portable, live camera, dispatch-assisted piloting | no autonomous targeting, no weapons, battery and signal limits |

### 5.3 Office and restricted kit

Office: a desk, case files, lab access, interpreter access, meeting rooms — **callable resources**, not carried
items. Restricted (mission-justified only): SWAT equipment, forensic lab instruments, psychotronic shielding,
Faraday transport. Each requires an authorising human and leaves a record — which is also the story.

### 5.4 Dispatch: human authority is absolute

| Dispatch may | Dispatch may not |
|---|---|
| aggregate bodycam/radio/drone feeds, transcribe, translate, route, alert | decide tactics, authorise force, order an arrest or a search |
| run narrow forensic analysis and label it **preliminary** | declare identity, guilt, alien origin or lie detection |
| drive the vehicle or drone under a pre-authorised emergency protocol | drive them in ordinary operations, or choose a route that endangers anyone |
| tell the officer what it cannot see | pretend to certainty it does not have |

**Model the failure modes,** because they are the interesting part: comms delay, spoofed feed, compromised firmware,
a controller who is overloaded, a lab backlog, and an AI that is confidently wrong. Every one of them is a scene.

### 5.5 The Romppainen–Fujita device

A clunky, retro, MKULTRA-meets-Voight-Kampff console that shows **several emotional-response channels** while the
interviewer chooses questions. Mechanically: it turns the interview into a reading task (which channel moved, and
why), never a verdict.

| it shows | it does not show |
|---|---|
| arousal, stress, guardedness — as **noisy estimates** with a confidence | truth, lies, identity, species, guilt |
| contradictions between channels | the reason for a contradiction |
| a reason to ask the next question | an answer to it |

False positives are the design's engine: a traumatised innocent looks exactly like a guilty person on a bad
calibration, and the officer who says so out loud is the one the campaign is about.

---

## 6. Deliverable E — the vertical slice, and the equal-access proof

**Scene chain:** bodycam → scanner sample → evidence bag → cyberdeck OSINT → interview with the device → human
Dispatch interpretation → optional authorised hack → handoff to the Finnish police and the lab.

| step | Grunt's route | Geek's route | Freak's route | core clue |
|---|---|---|---|---|
| 1. bodycam review | **Notice** + declared review | **Program** + review | **Notice** + review | `clue:van_plate` |
| 2. sample at the depot | **Exert/Notice** to collect correctly | **Know** to choose the right test | **Notice** + the device's reading | `clue:residue_trace` |
| 3. bag and log it | **Administer** (custody) | **Administer** | **Administer** | `evidence:custody_log` |
| 4. OSINT on the shell company | **Connect** (ask the right office) | **Program/Know** (registry, metadata) | **Talk** (someone who knows) | `lead:director_identity` |
| 5. interview | **Talk** + procedure | **Talk** + the device's channels | **Talk** + empathic reading (Level 1+) | `clue:contradiction` |
| 6. Dispatch interpretation | same for all: a human reads the feed and says what she thinks | | | `lead:lab_handoff` |
| 7. authorised hack (optional) | **CWN Hacking** — identical for all | identical | identical | `evidence:inbox` |
| 8. handoff | **Work** (paperwork) | **Work** | **Work** | `flag:case_handed_off` |

**The proof, stated as a testable rule:** for every row, the clue is granted when the character has the named
competence **or** an authored alternative, plus the declared access and inquiry — and the investigation module
guarantees that a **failed** check changes time, cost, risk or extra detail, never the availability of a core clue.
The three tracks differ in *how* they get there, not in *whether* they can.

**The Freak's temptation, and its refusal:** at step 5 the player will want to read the suspect's mind. The answer is
the boundary: empathy reads *affect*, and the contradiction is found by asking the next question. The device and the
gift both produce **leads**, never conclusions.

---

## 7. Deliverable F — data model proposal (design only, no code)

```
RookieBuild {
  background: BackgroundId            # SRD id
  edges: [EdgeId, EdgeId]             # exactly two; Academy + one Recruit
  focus: FocusId
  underdog_edge: EdgeId | None        # if modifier total <= -1
  recruit_track: "grunt" | "geek" | "freak"
  skill_resolution: {granted_at_creation: [...], refused: [...], reasons: [...]}
}

EdgeGrant {
  edge_id: EdgeId
  grants: {qualification: bool, skill: SkillId | None, access: [AccessTag], contacts: [ContactId]}
  refuses_if: [Rule]                  # e.g. "skill already granted by background"
}

AwakeningState {
  level: 0..3
  narrative_stage: "act1" | "act2" | "act3" | "act4"
  capabilities: [PsiCapabilityId]
  costs_incurred: [ConditionTag]
  gm_gated: bool                      # always true
}

AssetCustody {
  asset_id: str
  owner: "agency" | "personal"
  revocable: bool
  loss_consequence: str               # access removed, training retained
}

DispatchAuthority {
  actor: "human_controller" | "narrow_ai"
  may: [CommandType]
  may_not: [CommandType]              # decisions, force, arrest, search, identity
  protocol: "pre_authorised_emergency" | None
}
```

**Tests that must exist in the implementation phase** (stated now so the model can be argued with):

1. **Edge arithmetic:** a build with three non-Underdog Edges is refused; a second Recruit Edge is refused.
2. **Double-dip refusal:** an Academy pick that duplicates a Background skill is refused with a reason.
3. **Awakening monotonicity:** a level may not exceed the narrative stage; a capability may not appear without its
   level.
4. **Asset revocation:** removing credentials removes access tags and **no** skill, feat or training.
5. **Dispatch refusal:** every command in `may_not` returns a refusal, including "drive to the suspect's address".
6. **Clue parity:** the same case, run through all three tracks, yields the same set of core clues.
7. **Psi boundary:** `discover()` still has no psi parameter, and the psi module still cannot import the
   investigation module.

---

## 8. Open decisions for Tomi

1. **Academy as Edge** (recommended), as a **career package** layered on a Background, or as a Focus? The Edge
   version costs the second slot, which is the only clean way to prevent double competence.
2. **Professional Psychic Background**: a full Background, or Law Enforcement with a `psi_past` tag?
3. **Freak's starting capability**: empathy only, defence only, or a choice of one of the two?
4. **Grunt's police access**: Suomen Poliisi contact and procedure, or a narrower "may request" permission?
5. **Which CWN Foci** are recommended for each track (I named only verified ones; the rest need the SRD list).
6. **Is `Recruit: Freak` public knowledge** at the office, or a secret the player must manage?
7. **Underdog bonus Edge**: allowed for these builds at all, or excluded because the Academy already grants access?
8. **The service weapon**: which CWN firearm is the canonical Europol issue — `heavy_pistol`, or something larger
   from the rifle table?
9. **Does the Romppainen–Fujita device ever produce a decisive result**, or always only a stronger lead?
10. **Kurvi flat**: agency housing (as in the graph draft's `@v2` profile) or the older Helsinginkatu flat?

---

## 9. What this document does not do

* No Python, no rulebook chapter, no CWN change, no campaign file.
* No new PSI mechanic: §4 maps to the existing proposals and the module that already exists.
* No new investigation mechanic: §6 relies on `src/rules/investigation.py` as it stands.
* No promotion of the #1137 drafts to approved mods.

## 10. Sources verified in this pass

| source | status |
|---|---|
| CWN SRD — Edges ("two … a third at fifth level", Underdog Rule, Educated, Face, Focused, Ghost) | read |
| CWN SRD — Foci ("one Focus, plus one more if you have the Focused Edge"; Alert, Henchkeeper, Unique Gift, Unregistered) | read |
| CWN SRD — Backgrounds (free skill + two Learning picks; the "Any Skill" exclusion) | read |
| `data/rules/cwn/srd_tables.json` — 20 backgrounds; weapon/armour/cyberdeck/drone/vehicle tables | read |
| `data/rules/cwn_equipment.json` — `heavy_pistol`, `light_pistol`, `rifle`, `armored_clothing`, `impact_jacket`, … | read |
| `data/rules/cwn_catalogue.json` — 17 cyberware entries incl. `cybernetic_baseline` | read |
| `src/rules/cwn_backgrounds.py`, `cwn_edges_foci.py` (`EDGES_AT_START = 2`, `FOCI_AT_START = 1`), `cwn_foci.py` | read |
| `src/rules/investigation.py` — `Clue(competency, access, inquiry, kind)`, `discover()` | read |
| `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`, `CWN_IMMUTABLE_CORE_1068.md` | read |
| `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` — acts, team, staged PSI | read |
| `docs/design/DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md` (#1137) | read; its "no new Edges" recommendation is reconciled in §1.1 |
| CWN Edge/Focus names beyond the six above | **not verified**; marked [?] and must be checked before print |
