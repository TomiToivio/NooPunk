# NoöPunk Europol Rookie: CWN Character Options and Issued Kit

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** Issue [#1137](https://github.com/TomiToivio/NooPunk/issues/1137); researched 2026-11-04. Planning only; do not implement, modify the CWN core, or copy a published ruleset. **Evidence labels:** [E] empirical/approved; [X] experimental; [H] contested theory or parapsychology; [F] fictional 2045 premise; [P] draft mechanics. Tomi edits this proposal first, then separately authorizes matching tabletop and Python implementation.

## Preflight: what already exists for this subsystem

Most of this subsystem is already canon. This document must be a **gap analysis**, not a new creation system.

- **Already written:** `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` §2.1–2.3 — fixed dossier, player-built
  identity, and a starting sheet that is explicitly a **proposal** with the attribute array left open.
- **Powers and limits:** `docs/world/EUROPOL_HELSINKI_1114.md` §3 — "Europol opens doors; national officers walk
  through them".
- **Gap-check target:** `src/rules/cwn_backgrounds.py` — the published CWN background table that any proposed
  background must be compared against **before** it is added.
- **Issued kit source:** `design/BIONICS.md` — the BCI and the defensive psychotronic implant.

## Design goal
Use **CWN character generation unchanged** and a **pre-generated first-campaign protagonist**, adding **only demonstrated Europol gaps** in background, Edges/Foci and issued gear. The rookie's cybernetic kit is an ordinary part of Europol 2045 life, **not** an early revelation of special natural PSI. Canon [Europol Helsinki Field Office](../world/EUROPOL_HELSINKI_1114.md); [campaign](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md).

## Rule audit: default to existing options
| Needed competency | First look for | Only if genuinely absent |
|---|---|---|
| Police investigations | CWN investigator / law-enforcement background, Know/Notice/Talk/Connect/Administer | `Europol Academy Graduate` background wrapper, **same** skill grants, not a second skill system |
| Cyberforensics | CWN Program/Fix and appropriate cyber-specialist Foci | **No new hacking bonuses** unless a gap is evidenced |
| Jurisdictional cooperation | CWN Administer, Connect, Talk, Lead | `EU Cross-Border Liaison` narrative access tag, not unilateral arrest powers |
| Defensive cyberware | CWN core cyberware and System Strain | QIP shield documented separately in Psychotronics draft |
| Ordinary field readiness | CWN Shoot, Sneak, Exert, Know, Notice, Heal | New Edge/Focus only after source-specific ability and balance comparison |
| PSI | Later SWN-compatible scripted campaign unlock | **No psychic class at character creation** merely to justify the issued defensive implant |

**Verification task before author approval:** compare exact CWN Deluxe backgrounds/Edges/Foci and the existing academy package in repository; list their published or verified canonical reference IDs, avoid duplicate options. No source-derived values, gear prices or slot costs are guessed here.

## Proposed pre-generated dossier fields (not numerical stat block)
`name` [OPEN], `age` [author campaign draft suggests 24; verify and approve], `background=Europol rookie`, `employer=Europol Helsinki Field Office`, `CWN attributes/skills/Edge/Foci` [pending reuse audit], `rank` [OPEN], `national-police liaison` [OPEN], `housing=Kurvi`, `issued_assets`, `reputation`, `relationships`, `memory_fragments`, `psi_stages` [GM-only].

**Player agency:** character creation is not the main story. Pre-design biography, first assignment, and secret Wanderer past; in play the character accumulates personality, habits, allegiances, friendships, romance, integrity/corruption and political interests. **First-campaign StO is fixed**; no StS faction option. Exact pre-incarnate StO service revealed **only in the campaign finale**.

## [P] Two deliberately small Europol options (do not adopt until verified)
1. **Background wrapper: Europol Academy Graduate**. Provides narrative professional familiarity with evidence chain, EU reporting, police cooperation, GDPR-style/data-rights procedures, basic weapons safety and tactical response. Skill picks must **reference existing CWN skill/background allocation** rather than free extra points. If an existing CWN law-enforcement background suffices, **drop this wrapper**.
2. **Field Liaison tag (not an Edge by default):** recognized interagency credential enabling authorized introductions and requests across national borders; cannot search, detain, issue warrants, obtain classified records or arrest unilaterally. Implement as equipment/role permission, no +1 to everything. If CWN Foci already model connections, don't duplicate them.

**No new Focus or Edge proposed yet:** the first draft finds no need to mint a free combat bonus or additional cyberware slot without auditing the canonical lists. Candidates for later review: cross-border coordination, protective interviewing, controlled psychotronics. Any proposed special action must cite a concrete scenario gap and demonstrate parity with an existing Focus.

## Basic issued Europol kit: proposal for author equipment selection
| Asset | Status | Reference/limits |
|---|---|---|
| Official credentials and EU secure access token | Issued | Credential/access permission; lawful authority defined by Finnish/EU setting |
| **BCI** | Issued implant | CWN cyberware entry or appropriate adapted item, price/System Strain **[OPEN]**, firmware policies |
| **Defensive QIP psychotronic implant** | Issued implant | One narrow defensive PSI permission, conscious operator required, effect in Psychotronics/PSI, not duplicated |
| Secure communications device | Issued | CWN ordinary comms, BCI link, not unlimited data access |
| Approved personal protective gear | Issued | Pick existing CWN armor when rank/mission policy chosen |
| Sidearm/authorized less-lethal option | **[OPEN] mission/rank-dependent** | Do not assume Europol alone has law-enforcement powers or universal carry rights |
| Evidence seals / field collection pack | Issued or checked out | Chain-of-custody process; CWN gear or descriptive kit |
| ID/medical registration for implants | Issued records | Regulated user and privacy notes |
| **Company housing, Kurvi** | Employment benefit | Access/location/lease and social scene; *not cyberware*, cannot be sold as adventuring gear |

**Jurisdiction [REPOSITORY CANON]:** Europol coordinates cross-border investigations and supports Finnish police; Finnish authorities conduct arrest/search under national law. This yields playable dilemmas, not a new Supercop Edge.

## First playable scene example
The rookie leaves the Kurvi apartment, checks BCI credentials, reports to Europol and examines contradictory maintenance invoices. CWN Administer/Notice/Connect and ordinary police procedure solve the case. The implant's first use is a controlled safety drill; no spontaneous Telepathy/astral event. In an interview, official credentials obtain a *request*, not forced cooperation. Later, a relationship or political choice may add a tag without changing class or StO.

## Suggested future Python interface (not implementation)
`EuropolRookiePackage{background_ref,existing_edge_refs,existing_focus_refs,issued_item_refs,credential_scope,housing_ref,hidden_psi_unlocks}`; `issue_equipment` logs ownership; `grant_role_access` checks jurisdiction; `record_character_choice` delegates to tag design. Never extend `cwn_core` attribute/skill formula.

## Author questions
1. Final rookie identity, pronouns, age, starting sheets and whether this is one protagonist or alternate pre-gens.
2. Is the legally relevant role a Europol employee, seconded Finnish officer, or joint-team member? Determine arrest and firearm rules accordingly.
3. Which exact published CWN cyberware items represent BCI and protective QIP; what is their System Strain and procurement legality?
4. Which starting Edges/Foci are actually missing after audit? Defaults should reuse existing rules.
5. Which colleagues/mentor names and roles must appear in onboarding? Follow current campaign, not older UNSA rookie outline.
6. How equipment ownership and Kurvi housing change on job suspension or resignation.

**Next gate:** Tomi edits; then implement approved rulebook and Python together, not here.

---

## Merged review pass — what this section adds

A second draft of this same subsystem was written in parallel on the same day; this file and that one were
reconciled rather than shipped twice. The earlier text above stands as the base. The sections below are the
material it did not contain: quantified procedures, the audit results, and the decisions that need a number
rather than a principle.

### The reuse audit, actually completed

The draft above says "compare exact CWN backgrounds/Edges/Foci … before approval". That comparison is done, and
it narrows the proposal further than the draft assumed:

| CWN piece | verified inventory | consequence for the rookie |
|---|---|---|
| backgrounds | **20**, in `data/rules/cwn/srd_tables.json`: Bum, Bureaucrat, Clergy, Coder, Corp Security, Corper, Criminal, Doctor, Drone Jockey, Ganger, Laborer, **Law Enforcement**, Manager, Outlander, Performer, Soldier, **Spy**, Trader, Streetwalker, Technician | *Law Enforcement* covers the field investigator; *Spy* and *Bureaucrat* cover liaison and analysis; *Coder* and *Doctor* cover cyberforensics and pathology. **At most one wrapper background is justified**, and only for the academy's cross-border case-file emphasis |
| edges / foci | `src/rules/cwn_edges_foci.py`: `EDGES_AT_START = 2`, `FOCI_AT_START = 1`, `FOCUS_LEVEL_MAX = 2`; `cwn_foci.py`: `new_character_picks`, `take_level` | **zero new edges, zero new foci.** The pregen picks two edges and one focus from the canonical lists |
| skills | **19**, `data/rules/cwn/skills.json` (Administer … Work) | **no new skill.** PSI uses the existing skill the action resembles |
| gear | `data/rules/cwn_equipment.json`: weapons `light_pistol`, `heavy_pistol`, `rifle`, `submachine_gun`, …; armour `ordinary_clothing`, `reinforced_clothing`, `street_leathers`, `impact_jacket`, … | the kit draws **only** from these ids; no invented items, no invented prices |
| cyberware | 17 entries in `data/rules/cwn_catalogue.json` (incl. `cybernetic_baseline`) | BCI and the defensive implant are cyberware with CWN's surgery, strain and complication rules |
| generation | `src/rules/field_agent.py` — `generate_field_agent`, `swap_attributes` | the pregen can be **produced by code later**, not hand-written |

So the character-generation addition is: **one optional background wrapper, a filled-in CWN sheet, two GM-only
flags, and a kit of canonical ids.** Anything larger is a second character-creation system.

### Ownership, made explicit

| asset | category | owner | if it is lost or abused |
|---|---|---|---|
| BCI | issued, implanted | Europol; the body carries it | removal is a CWN procedure with complications; the agency notices |
| defensive psychotronic implant | issued, implanted | Europol | calibrated to her, so useless to a thief; loss is a report |
| sidearm, armour | issued equipment | Europol | CWN equipment rules; a lost weapon is a report, not a fine |
| credentials, comms | **licensed access** | Europol | opens Europol's doors, not Finland's |
| Kurvi apartment | **agency-owned housing** | Europol | not sellable, not collateral, inspectable by the employer |
| personal kit | personal property | the character | ordinary CWN gear bought with ordinary money |

The first lesson of the campaign is in this table: **she owns almost nothing she uses.**
