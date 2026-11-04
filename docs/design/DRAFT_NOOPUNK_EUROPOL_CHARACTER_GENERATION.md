# DRAFT — NoöPunk Europol rookie: a pre-generated character, not a new character-creation system

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED**
>
> Phase A of [#1137](https://github.com/TomiToivio/NooPunk/issues/1137). Proposal only: no Python, no rulebook
> chapter, no equipment entry, no CWN change. The author owns the canon.
>
> Companion drafts: [Psionics](DRAFT_NOOPUNK_PSIONICS.md) · [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md) ·
> [Bionics](DRAFT_NOOPUNK_BIONICS.md) · [Tags](DRAFT_NOOPUNK_CHARACTER_TAGS.md).

**Evidence key:** **[a]** published CWN procedure · **[d]** NoöPunk fiction · **[?]** open question for the
author. This document is almost entirely **[a]** plus **[d]**, which is the point: the rookie should be built
out of what the game already has.

---

## 1. What the author asked for

From [#1137](https://github.com/TomiToivio/NooPunk/issues/1137) §4 and
[`CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md):

* A **pre-generated young Europol Helsinki rookie** is the first-campaign default — **an editable authored
  template**, not unrestricted character creation.
* Add **only** the backgrounds, edges/foci and equipment the campaign actually needs; **reuse CWN** where it
  fits; propose additions only for **demonstrable gaps**.
* **Standard equipment package**: BCI, defensive QIP psychotronic implant, lawful officer gear,
  communications/credentials, and **a company apartment in Kurvi** as a narrative benefit.
* Distinguish **issued gear / licensed access / personal property / agency-owned housing**.
* **Legal limits:** Europol coordinates cross-border investigation; **Finnish authorities retain arrest and
  search powers**. No magical Europol power to bypass warrants.
* **Preassigned dormant PSI / hidden biography flags** as **GM secrets**, with staged unlocks — no free PSI,
  no unsolicited Wanderer disclosure.
* Tabletop review: equipment references **canonical CWN items**; **no invented prices or stat blocks** until
  approved and verified.

---

## 2. What CWN already gives us (audited, not assumed)

| CWN piece | where it lives | what a Europol rookie actually uses |
|---|---|---|
| **20 backgrounds** | `data/rules/cwn/srd_tables.json` → `backgrounds`: Bum, Bureaucrat, Clergy, Coder, Corp Security, Corper, Criminal, Doctor, Drone Jockey, Ganger, Laborer, **Law Enforcement**, Manager, Outlander, Performer, Soldier, **Spy**, Trader, Streetwalker, Technician | **Law Enforcement** is the obvious fit; **Bureaucrat** and **Spy** cover the liaison/analyst variants; **Coder** and **Doctor** cover cyberforensics and forensic pathology |
| **Background mechanics** | `src/rules/cwn_backgrounds.py` — `Background`, `SkillPick`, `AnyCombat`, `AnySkill`, `AttributeBonus`, `growth_rolls`, `resolve_table_entry` | free skill, specific picks, growth rolls, attribute bonus — **unchanged** |
| **Edges and foci** | `src/rules/cwn_edges_foci.py` — `EDGES_AT_START = 2`, `FOCI_AT_START = 1`, `FOCUS_LEVEL_MAX = 2`, `UNDERDOG_THRESHOLD`; `src/rules/cwn_foci.py` — `new_character_picks`, `take_level`, `max_level` | two edges, one focus at level 1 — **unchanged** |
| **Skills** | `data/rules/cwn/skills.json` — 19 skills, Administer … Work | no new skill. PSI uses existing skills (see the psionics draft) |
| **Equipment** | `data/rules/cwn_equipment.json` (weapons `light_pistol`, `heavy_pistol`, `rifle`, `submachine_gun`…; armour `ordinary_clothing`, `reinforced_clothing`, `street_leathers`, `impact_jacket`…), `data/rules/cwn_catalogue.json` (17 cyberware entries incl. `cybernetic_baseline`) | issue from the **canonical catalogue**; no new stat blocks |
| **Cyberware** | `src/rules/cwn_cyberware.py`, `cwn_strain.py` | BCI and defensive implant are **cyberware**, with surgery, strain and complications |
| **Field agent generator** | `src/rules/field_agent.py` — `FieldAgent`, `generate_field_agent`, `swap_attributes` | an existing random-but-swappable generator: **the template can be produced by code later**, not hand-written |
| **Investigation** | `src/rules/investigation.py` | the campaign's engine; psi may never grant its clues |

**Gap analysis — what is genuinely missing, and what is not:**

| proposed addition | gap? | verdict |
|---|---|---|
| **Europol academy investigator** background | **partly** — *Law Enforcement* covers patrol/investigator skills, but not the academy's cross-border, multilingual, case-file emphasis | **propose one background**, reusing CWN's background structure (free skill + picks + growth + attribute bonus) |
| **Transnational police analyst** | **yes** — *Bureaucrat* is administration, not analysis | **propose one background**, or fold into the academy one as a pick |
| **Cyberforensics specialist** | **no** — *Coder* + *Technician* already do this | **do not add**; use existing backgrounds |
| **Liaison officer** | **no** — *Bureaucrat*/*Spy* cover it | **do not add** |
| **Field investigator** | **no** — *Law Enforcement* | **do not add** |
| **New edges for police authority** | **no** — CWN edges already cover contacts, authority-adjacent advantages | **do not add** unless the author names one |
| **Agency housing (Kurvi flat)** | **yes**, but it is not a character-creation item | **propose as a narrative benefit** with an ownership note, not a mechanical bonus |

So: **at most two backgrounds, zero new edges, zero new foci, zero new skills.** That is the whole chargen
proposal, and it is deliberately small.

---

## 3. The pre-generated rookie — a template, not a character

The template is a **filled-in CWN character** plus a small number of NoöPunk flags. It is *editable*: the player
may change name, pronouns, appearance, a skill pick and one edge. It is *not* a full build system.

```
NOÖPUNK PREGEN — "The Rookie" (Campaign 01, Act I)

CWN layer (all figures from the CWN rules; none invented here)
  background:      Europol Academy Investigator (proposed; else Law Enforcement)
  attributes:      rolled by the CWN method, swappable once (field_agent.swap_attributes)
  skills:          from the background + picks
  edges (2):       two CWN edges; recommend one social, one investigative
  focus (1):       one CWN focus at level 1
  cyberware:       BCI (cybernetic baseline) + defensive psychotronic implant
  gear:            canonical CWN items only — sidearm, armour, comms, credentials
  strain:          as CWN computes it for the installed cyberware

NoöPunk layer (tags, not statistics)
  reputation:      Europol +0, Finnish police +0, UNSA 0        (see the tags draft)
  personality:     two tags from play, none at creation          (see the tags draft)
  goals:           one short-term from the first case            (GOAL_TAG_1119)
  dormant:         latent_gene (GM secret), memory:2038 (GM secret)
  housing:         Kurvi apartment — agency-owned, not personal property
```

**Why dormant flags are not character options.** They are written on the **GM's** copy, not the player's. The
player's sheet shows nothing. At the awakening, the GM reveals the flag; at the Higher Self scene, the memory
reveals itself. If a player could pick "latent PSI" at creation, the campaign's first two acts would be spoiled
by the character sheet.

---

## 4. The issued kit, with ownership made explicit

| item | category | who owns it | what happens if lost/abused |
|---|---|---|---|
| **BCI** (CWN cyberware) | issued, implanted | Europol; the body carries it | removal is a CWN procedure with complications; the agency notices |
| **Defensive psychotronic implant** | issued, implanted | Europol | same; and it is *calibrated to her*, so it is useless to a thief |
| **Sidearm + armour** | issued equipment | Europol | CWN equipment rules; an lost weapon is a report, not a fine |
| **Comms / credentials / warrant card** | licensed access | Europol | credentials open doors that are *Europol's* doors — not Finnish ones |
| **Forensic kit / cyberdeck** | issued, on request | Europol | request is a scene; the kit is not personal gear |
| **Kurvi apartment** | agency-owned housing | Europol | not sellable, not collateral, and inspectable by the employer |
| **Personal possessions** | personal | the character | ordinary CWN gear, bought with ordinary money |

The distinction matters because it is the campaign's first lesson in institutional power: **she owns almost
nothing she uses.**

---

## 5. Legal limits as a table procedure

Europol's powers, as already established in [`EUROPOL_HELSINKI_1114.md`](../world/EUROPOL_HELSINKI_1114.md):

1. **Europol coordinates; it does not arrest.** An arrest is a Finnish officer's act. A Europol officer who
   arrests someone has made a diplomatic incident, not an arrest.
2. **Searches need Finnish authority** — a warrant, a consent, or an emergency the law recognises.
3. **Credentials are a permission, not a key.** They grant access to Europol facilities, Europol systems and
   invited liaison; they grant nothing over a Finnish crime scene.
4. **Cross-border evidence has a chain.** A psychotronic recording, a decoded file or a psychic impression
   follows the same admissibility questions as any other evidence (see the psychotronics draft).

**At the table:** when the player wants something only an institution can give, the GM asks *which*
institution, and makes the request a scene. This is not a punishment mechanic; it is the campaign's texture.

---

## 6. Tabletop example — session one in ten minutes

> The player sits down. The GM hands over the pregen. "You are twenty-four, three months out of the academy,
> seconded to the Helsinki liaison office. You have a flat you do not own in Kurvi, a badge that opens Europol's
> doors and a pistol you have never drawn."
>
> First case: a complaint about a missing courier. The player uses **Administer** to read the file, **Notice** at
> the tram depot, **Talk** with a witness. No PSI, no implants firing, no cosmic anything. The only strange thing
> is a dream the GM describes at the end of the session, in the past tense, and does not explain.

That is Act I working: the character is ordinary, the system is CWN, and the strangeness is a *scene*, not a
statistic.

---

## 7. Python model / interface proposal (design only — Phase B)

```
src/rules/noopunk_pregen.py
    @dataclass RookieTemplate:
        cwn: dict                 # a normal CWN character record
        flags: dict               # dormant: latent_gene / memory_2038 — GM-only
        housing: str              # "europol_kurvi"
        kit: list[str]            # canonical CWN item ids only

    def build_rookie(*, seed: int, background: str = "europol_academy") -> RookieTemplate
    def player_view(template) -> dict     # strips flags; what the player may see
    def reveal(template, flag: str) -> dict
```

Rules:

* **Reuse `field_agent`** rather than re-rolling attributes: `generate_field_agent` already implements CWN
  generation with attribute swapping.
* **`player_view` must strip every GM secret**, and a test must assert that the serialized player view contains
  no `latent_gene` key. This is the one place where a leak breaks the campaign.
* **Kit ids are validated against the canonical catalogue** (`data/rules/cwn_equipment.json`,
  `cwn_catalogue.json`), so no invented item can enter a pregen.

---

## 8. Interaction and precedence

| with | rule |
|---|---|
| **CWN chargen** | unchanged. The pregen is a filled-in CWN character; the two proposed backgrounds use CWN's own structure. |
| **Bionics / psionics** | dormant flags are the *only* route into those systems at Act I, and they unlock nothing mechanically until the act says so. |
| **Tags** | reputation/personality/goals start empty or at zero; the pregen does not pre-load a personality. |
| **Psychotronics** | the issued implant is kit, calibrated to her, and its loss is a report. |
| **Investigation** | the pregen's skills are what solve cases; PSI never adds a clue. |
| **Acts** | Act I uses this template verbatim. Act II adds tags and the first psi. Acts III–IV add the advanced material from the other drafts. |

---

## 9. Open decisions for Tomi

1. **One background or two?** Recommendation: one (`Europol Academy Investigator`), with analysis folded in as a
   pick.
2. **Which two CWN edges and one focus** does the canonical rookie start with? (This is author canon, not a
   balance question.)
3. **Is the BCI mandatory** for the pregen, or can a player refuse it and play a "clean" officer?
4. **Is the Kurvi apartment a benefit or a liability?** It is currently written as a benefit; an inspectable
   agency flat is also a plot device.
5. **Does the player ever see the dormant flags** before the reveal — e.g. as a cryptic tag — or is the sheet
   clean until the scene?
6. **Is the rookie's nationality Finnish?** It changes which institutions can order her around.
7. **How much of the sheet is editable** — a skill pick, one edge, or the whole build?

---

## 10. Sources

| source | status in this pass |
|---|---|
| CWN SRD §Character Creation, §Backgrounds, §Edges and Foci, §Equipment, §Cyberware | section anchors and repo symbols verified (`cwn_backgrounds.py`, `cwn_edges_foci.py`, `cwn_foci.py`, `cwn_equipment.json`, `cwn_catalogue.json`) |
| `data/rules/cwn/srd_tables.json` — 20 backgrounds | read; names listed verbatim |
| [`CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) | read; §8 rules-by-act, §2 dossier |
| [`EUROPOL_HELSINKI_1114.md`](../world/EUROPOL_HELSINKI_1114.md) | powers and limits taken from it, not restated from memory |
| [`GOAL_TAG_1119.md`](../rules/GOAL_TAG_1119.md) | read; goals are already implemented, not re-invented here |
| `design/BIONICS.md` | read; PSI sources and the defensive implant |
