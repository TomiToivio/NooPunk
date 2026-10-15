# The crossover's two skill layers: decisions, differences and deferrals (#482)

**What this document is.** The design record behind [../RULEBOOK.md](../RULEBOOK.md) §2–§4 and the
modules `rpg/skills.py`, `rpg/roster.py` and `strategic_skills.py`. It records **what #482 decides**,
**what it deliberately leaves open**, **how this differs from each reference system**, and **what was
verified versus what could not be** — so the next session does not have to re-derive any of it, and
does not mistake a proposal for a ruling.

**Status.** Issue #482 approves the RPG foundation (`#389`'s Fate kernel) and the **six individual
skills**. It does **not** approve a strategic agent skill roster, a mission list, a probability, an
action economy or any political-simulation number. `council.json`'s ten author decisions and the
queue rows D3/D11 remain untouched: nothing here resolves a row.

## 1. What the issue decides, and what it only proposes

| #482 clause | What this edition does | Status |
| --- | --- | --- |
| "adopt the Fate/Transhumanity's Fate RPG baseline" | the approved kernel already implements it; §5 and §6 restate it for the table | **approved** (as #389) |
| "add all six Eclipse Phase aptitudes as Fate-style individual skills" | `rpg/skills.py::INDIVIDUAL_SKILLS` — exactly six, with the issue's own scope text | **approved** |
| "not percentile attributes and not an additional stat layer" | the six are keys on the one Fate ladder; the check reads `Character.skills`, and there is no second scale | **approved** |
| "Do not accidentally retain Transhumanity's Fate's existing Somatics / Will as duplicate attributes" | §3.1 removes the parallel *Physique*/*Will* pair: SOM and WIL are the six-name list's own entries | **approved** |
| "document a clean migration/crosswalk" | §3.1's crosswalk (18 → 6) and `data/strategic_skills.json::mapping` (18 → 7) | done |
| "how specialist stunts/TAGs … supplement a broad individual skill" | §3.2: a narrow speciality is a stunt (priced in refresh) or a typed `competence` TAG; a capability is a competence, never a skill | **approved** as a reading; the stunt catalogue is open |
| "review, merge and adapt the remaining TF skills into a small, TI-like councilor list" | `data/strategic_skills.json` — seven proposed skills, 18-row mapping, overlap notes | **PROPOSAL** |
| "prepare a mapping table from TF skills to proposed strategic agent skills" | the `mapping` array, with the caveat that TF's own list is not verifiable here (§4) | **PROPOSAL** |
| "one faction leader + four agents, one action per character per turn" | `rpg/roster.py` — five seats, per-character ledger | **approved as structure** |
| "do not automatically import TI's numeric scale, probabilities or action economy" | `data/strategic_skills.json::not_imported_from_terra_invicta` | **refused** |

## 2. The design decisions this edition makes, and why

1. **The layer is chosen by context, not by the skill's name.** A name that belongs to one list is
   refused for the other, at declaration, before any dice. The alternative — reading an unknown name
   at +0 — makes "wrong list" and "untrained" indistinguishable at the table, which is exactly the
   failure #482's "do not silently substitute one list for the other" names.
2. **The six are broad, and the speciality rides on them.** Fate Core's 18-skill list separated
   competences that a transhuman technothriller does not need separated; the six are the individual
   half of a two-scale sheet, and a specialist is a stunt plus a tag. This is the *simplification* the
   issue asks for, applied at the layer where it costs least.
3. **The strategic roster is data, not code, and it is injected.** The RPG package imports no strategy
   module and reads no roster file (`tests/test_rpg_boundary.py` pins the import boundary), so the
   roster arrives as a parameter. With none, a faction-agent check is refused as *pending author
   approval*. This is what "initially configurable/pending" has to mean in code if it is to mean
   anything.
4. **The one-action limit is per character, not per seat.** #482 words it "per character"; a character
   who somehow held two seats would still act once, and the ledger enforces the character-level rule.
5. **A refused declaration is not counted as an action** by the ledger, because whether a refused order
   costs the turn is the strategy layer's open question (`refusal_effect`), and inventing an answer
   here would be inventing a rule. The ledger records only what it can decide.
6. **The capability gate is a parameter of the check, not advice in the rules text.** A gated move
   passes `required_capability=`, the engine refuses it before any dice, and the capability is read
   from the sheet's `competence` tags -- so the gate cannot be forgotten at the table and a gated
   action cannot be rolled at a lower rating and read as a hard attempt. (Adopted after a sibling
   implementation on the same issue proposed it as a first-class parameter; the *vocabulary* is this
   repository's existing one rather than a second capability set.)
7. **Both scales share the scene resolver, not just the dice.** A context-checked action goes through
   `rpg/scene.py::check`, so tracked scene aspects with free invocations, rerolls, aspect invokes and
   the fictional-permission flag all apply identically in a scene and in a mission. The rating to use
   is handed in (`rating=`), because the strategic ladder lives beside the individual one -- but the
   *actor* is always the character themselves, never a copy of the sheet, so Fate points spent and
   invocations consumed are real.
8. **Two metacurrencies are refused.** Fate points stay the only one; Eclipse Phase's pools become a
   design reference for what an invoke may be spent on, not a second economy. This matches the
   consolidated `#461` position and keeps the arithmetic of both scales the same.

## 3. Differences from each reference system

**From Fate Core (CC BY 3.0, the chassis).** Kept: 4dF + skill = shifts, the four actions, the four
outcomes, aspects, invokes, compels, refresh, the pyramid, stunts, two stress tracks, three
consequence slots. Changed: the skill list (18 → **six** for the individual layer, → **seven** for the
strategic layer); the list is **not** flat-and-universal but *selected by context*, which Fate itself
licenses ("there are only a handful of basic game actions, but the number of potential contexts is
infinite"); a skill name from the other layer is refused rather than rated at 0. Not adopted: Fate's
own skill-cap arithmetic and its Extras — nothing here needs them.

**From Transhumanity's Fate (CC BY-NC-SA, design study only, no expression imported).** Adopted as
*method*: build on existing Fate Core concepts; gear and augmentation as stunts or sub-aspects rather
than a second sheet; a capability as a permission rather than a bonus; a chassis that costs refresh.
**Refused:** its setting, its prose, its skill list as such (unverifiable here — §4), and its
Somatics/Will duplication, which this edition removes by name.

**From Eclipse Phase 2e (CC BY-NC-SA, design reference only).** The **six aptitudes** and their scopes
are used, as *Fate-rated skills*. Refused: the percentile d100 kernel, the four pools (kept as one
metacurrency), the morph/ego stat split as a second sheet, reputations as a subsystem, and every
number. The morph/ego split survives only as the observation §7 already makes — physical stress
belongs to the body, mental stress to the mind.

**From Terra Invicta (proprietary; concept only).** The *shape* is taken: a small consolidated list of
councilor competences, each mapping to kinds of mission, on a handful of characters who act once per
turn. Refused, explicitly and in the data file: the numeric attribute scale, mission success
probabilities and weights, the council-size/XP/cost/turn-cadence economy, professions, traits, orgs,
detection and intel. TI's eighth attribute, **loyalty**, is deliberately **not** a skill: it describes
a character's relation to their faction, and this repository already models relations as edges — a
skill would turn betrayal into something the character rolls.

## 4. What was verified, and what could not be

- **Verified this session.** Fate Core's default list is 18 skills and its Great pyramid rates ten of
  them ([fate-srd.com/fate-core/skills](https://fate-srd.com/fate-core/skills)); each of the eighteen
  per-skill SRD pages resolves (`https://fate-srd.com/fate-core/<skill>`), which is how the mapping's
  source column was checked rather than remembered; Fate Core is CC BY 3.0 on the SRD's own licensing
  line. Terra Invicta's councilor page states **eight** attributes and their one-line meanings, that
  a faction starts with four councilors and may expand, and that missions are assigned in an
  assignment phase. Its mission model was read too: there is **no separate "skill" tier** — a
  contested mission compares an attack stat against a defence stat, both drawn from the same eight
  attributes — a councilor's usable mission set also comes from a profession and from equipped
  organisations, and each attribute carries a mission family (recorded per proposed skill in
  `data/strategic_skills.json::strategic_skills[].terra_invicta_missions`). Loyalty is used as the
  defence stat of two missions and describes how likely a councilor is to defect, which is the
  corroboration for keeping it out of the roster
  ([wiki.hoodedhorse.com/Terra_Invicta/Councilors](https://wiki.hoodedhorse.com/Terra_Invicta/Councilors),
  [/Missions](https://wiki.hoodedhorse.com/Terra_Invicta/Missions)). Both pages are Cloudflare-guarded,
  so they were read through the wiki's own raw and mirrored pages; names and structure only, and no
  value, weight, cost or duration was copied.
- **Could not be verified here, and therefore not asserted.** *Transhumanity's Fate's own skill list
  and its additions to Fate Core.* The source rulebook is not in this repository, it is not reachable
  on the web in a usable form, and its CC BY-NC-SA terms forbid reproducing its text even if it were.
  The mapping is therefore expressed against the **Fate Core list TF builds on** — which the repo's own
  landed `ISSUE_461_RESKIN_SPEC.md` §3.1 quotes the TF developer notes as doing deliberately
  ("avoided creating new concepts and wherever possible built off existing Fate Core concepts") — and
  the gap is recorded as an open item rather than filled with plausible names. **No TF skill name
  appears anywhere in this edition that was not first verified as a Fate Core skill name.** The
  reference's own **action economy** is unverified in the same way: that a councilor attempts exactly
  one mission per assignment phase is implied by the wiki's intel wording but not stated there, and
  nothing in the crossover depends on it — the one-action turn is #461/#482's.
- **Not touched, and not claimed.** `council.json`'s roster size and founder authority (open decisions
  `roster_size` / `founder_authority`), its ten author decisions, `local_slice.MISSIONS` (consumed by
  reference; four of its names are reused and the rest of the proposal is marked proposed), and
  `RULE_SYSTEM_RESEARCH.md`'s Gates A–D. Gate A's RPG half is what #482 opens; **Gate B (political
  simulation) and Gate C (strategy rules) are untouched**, and no strategic number was written.

## 5. The deferred-decisions register

Carried forward deliberately; none of these is answered by this edition.

| # | Open question | Where it lives |
| --- | --- | --- |
| 1 | The final **strategic skill roster**: accept, amend or replace the seven | `data/strategic_skills.json`; this document §2 |
| 2 | The **mission kinds** the strategic skills check, and which of the four new names are kept | `data/strategic_skills.json::proposed_mission_kinds` |
| 3 | **Transhumanity's Fate's own skill list** — confirm the mapping against the book | §4 above |
| 4 | Whether the **strategic map crosses the `LeaderRPG` boundary payload** | `rpg/boundary.py::SHEET_KEYS` is a pinned contract; left unchanged |
| 5 | Whether the **kernel's demonstrations** are restated in the six (they use plain skill names because the kernel is setting-independent) | `rpg/fate.py` demos; `rpg/RULEBOOK.md` §6 |
| 6 | **Advancement**, the full **stunt catalogue**, and equipment statistics | §9 of the rulebook |
| 7 | Whether a **consequence maps onto the council status vocabulary** (`injured`, `unavailable`, …) | `#461` decision list, item 4 |
| 8 | Every **numeric** strategy question: mission difficulty, cost, duration, cadence, effect, win conditions | queue rows D3, D11; `council.json` |
| 9 | Whether **EP2e's simulationist material** is ported, and the band→ladder question for legacy percentile content | `ISSUE_461_RESKIN_SPEC.md` rows R1–R5 |

## 6. Provenance and licensing of this edition

Rules only, and NoöPunk's own vocabulary: no Eclipse Phase or Transhumanity's Fate setting material,
prose, artwork or numbers, and no licensed PDF is bundled. Fate Core's attribution and unofficial
notice ship in [`../rpg/ATTRIBUTION.md`](../rpg/ATTRIBUTION.md) and
[`../rpg/attribution.py`](../rpg/attribution.py); the licence NoöPunk distributes under is still the
author's decision (#200 / queue row D10) and is not chosen here. Terra Invicta material is cited as a
**design reference** and paraphrased; no wiki text is reproduced.

Tests cover **executable code only** (#271). This document is reviewed editorially and by playtesting,
which is why nothing here is asserted by a test.

— Ai (愛)
