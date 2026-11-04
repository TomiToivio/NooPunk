# DRAFT — NoöPunk Psionics: conscious-agent networks, active PSI and Astral Projection

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED**
>
> Phase A of [#1137](https://github.com/TomiToivio/NooPunk/issues/1137). This is an agent-written **proposal**.
> Nothing here is a rule. No Python, no rulebook chapter, no character option exists because of this document,
> and nothing in it changes CWN. Edit it, replace it, or reject it — the author owns the canon.
>
> Companion drafts: [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md) ·
> [Bionics](DRAFT_NOOPUNK_BIONICS.md) ·
> [Europol rookie](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md) ·
> [Tags](DRAFT_NOOPUNK_CHARACTER_TAGS.md). The cross-document map is in the issue, not in a sixth file.

**Evidence key used throughout** (required by the issue):

| tier | meaning |
|---|---|
| **[a]** | established, approved clinical or laboratory technique |
| **[b]** | experimental demonstrator with stated limitations |
| **[c]** | hypothesis or contested interpretation — *not* demonstrated |
| **[d]** | NoöPunk fiction: 2045 extrapolation, Law of One canon, or visual/aesthetic inspiration |

Everything in this draft is **[d]** unless it carries another tag. The purpose of the tags is that a reader can
tell, at a glance, where the fiction stops and the evidence ends.

---

## 1. What the author asked for

From [#1137](https://github.com/TomiToivio/NooPunk/issues/1137) §1 and the author's own
[`design/BIONICS.md`](../../design/BIONICS.md):

1. **Astral Projection is the centrepiece**, then **Telepathy**, then **Psychic Defence**. Everything else —
   clairvoyance, precognition, mind control, physical manifestation, probability manipulation, extreme
   telekinesis — is **restricted, scripted or rare NPC** unless separately approved.
2. **PSI and Magick are aspects of one metaphysical phenomenon** in-setting, with different *practices and
   traditions*, not two parallel advancement trees.
3. **Three sources of PSI**, all canonical in the author's note: latent human genetics, alien hybridisation,
   and psychotronic technology. **Source ≠ effect**: three routes to one effect, never three implementations.
4. **Physical / Cyber / Astral** are three interacting layers. Astral can be an AR-style overlay on the
   physical (dual perception) or an immersive disembodied traversal — in both cases a **real fictional realm**,
   not software VR.
5. A **three-stage progression**, authored not chosen: Europol defensive implant → natural awakening (bounded)
   → Higher Self / Wanderer package.
6. Psychic powers must **never solve an investigation** — the binding boundary is
   [`docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md).

---

## 2. Existing rules, exact sources, and what is already implemented

**CWN is immutable** ([`CWN_IMMUTABLE_CORE_1068.md`](../rules/CWN_IMMUTABLE_CORE_1068.md)): nothing in this
draft may shadow a CWN outcome. Every option below is additive or does not exist.

| system | edition / location | what it actually gives | what we may borrow | what we must not import |
|---|---|---|---|---|
| **CWN core** | SRD https://cwn.quadrifons.com/ ; repo `src/rules/cwn_*.py` | 2d6 skill checks, attribute modifiers, saves, combat, trauma, System Strain, investigation, advancement | the whole resolution spine | any change to it |
| **SWN Revised (Deluxe)** — Psionics | pp. 30–41; Telepathy pp. 40–41, Biopsionics 32–33, Metapsionics 34–35 | Psychic class, six disciplines with ranks 0–4, **Effort** pool, techniques bought per rank, torching | the *shape* of trained discipline + committed resource | SWN class text, power lists, Effort numbers |
| **AWN (Deluxe)** — Mentalist | The Mentalist p. 264; Mentalist Disciplines p. 266 | a lower-powered arts/effort caster aimed at non-combat scenes | its restraint: few powers, investigation-adjacent, no artillery | AWN arts text and its post-apocalyptic framing |
| **WWN** — Magic / Arts / Workings | Magic p. 62; Magical Workings p. 90; Arts of the Gyre p. 344 | Vancian-ish high magic, ritual workings, tradition arts | the *idea* of a Working as a slow, costly, prepared effect | spell lists; WWN's high-magic economy |
| **CWN Hacking** | SRD §Hacking; `src/rules/cwn_hacking.py` | access route → permission → contested check → alert clock → countermeasure | the **access/permission/detection** grammar | "the mind is a network you can port-scan" |
| **Repo prototypes** | `src/rules/noopunk_extensions.py` (opt-in, non-canonical), `strategy_game/rpg/psi.py` | capability-tag permission model; provisional Effort-like ledger | lessons: permissions before dice, commitments that serialize | any of its provisional numbers |

**Implementation status, verified in code rather than assumed:**

* `src/rules/swn_psionics.py` — SWN-shaped engine exists: disciplines, ranks, Effort capacity
  `1 + best(WIS, CON) mod + highest discipline rank`, reservations with `active / scene / day` durations,
  torching, Partial Psychic restriction. It is an SWN-compatibility surface, **not** a NoöPunk psi rule.
* `src/rules/psionics.py` — the shared Effort/technique vocabulary and catalogue.
* `src/rules/cwn_hacking.py` — access pool, security difficulty, alert clock, failure-per-alert accounting.
* **No astral projection module exists.** No NoöPunk psi module exists. Nothing in `src/rules` implements
  Telepathy, Psychic Defence or a projection loop, and this draft does not add any.

**The comparison, in one line each:**

* *SWN* answers "what can a trained psychic do, and what does it cost per day?" — a class economy.
* *AWN Mentalist* answers "what can a psychic do without turning the game into a wargame?" — restraint.
* *WWN* answers "what does magic cost when it is a craft and a tradition?" — preparation and ritual.
* *CWN Hacking* answers "what must be true before you may even try?" — access, permission, detection.
* **NoöPunk needs the last two more than the first two.** The rookie's PSI is a permission question and a
  privacy question before it is a power question.

**Do not combine.** No NoöPunk character may stack an SWN Psychic class, an AWN Mentalist and a CWN cyberdeck
resource. The drafts below assume **one effect, one cost, one owner**.

---

## 3. What the real world actually supports

| claim | tier | source (date) | the limit that matters for design |
|---|---|---|---|
| Continuous language can be reconstructed from **non-invasive fMRI** | **[b]** | Tang, Schmittmann, Bhattacharya et al., *Nature Neuroscience* 26:858–866 (2023), https://www.nature.com/articles/s41593-023-01304-9 | subject-specific decoder training, cooperative subject attending to a story, **semantic gist not verbatim**; a bulky scanner, not a helmet |
| **Inner speech** is decodable from motor cortex with an implanted array | **[b]** | Kunz, Shlizerman et al., *Cell* 188(17):4658–4673 (21 Aug 2025), https://www.cell.com/cell/fulltext/S0092-8674(25)00681-6 | the same paper reports that **simple strategies reliably prevent private inner speech from being decoded** — privacy is defensible by the subject, which is the design gift here |
| Precise **deep-brain** neuromodulation without surgery (256-element 555 kHz array, real-time fMRI guidance) | **[b]** | *Nature Communications* (5 Sep 2025), https://www.nature.com/articles/s41467-025-63020-1 | individualized planning, stereotactic positioning, laboratory equipment; effect on a *targeted circuit*, never a command |
| Non-invasive ultrasound shifts **reward sensitivity** | **[b]** | *Nature Communications* (2025), https://www.nature.com/articles/s41467-025-65080-9 | small n, one deep target, behavioural effect size d≈0.5–0.7 — a nudge, not a puppet |
| Quantum theories of consciousness, including Orch-OR, are **not empirically established** | **[c]** | Ma & Wang, *Frontiers in Psychology* 17 (28 Apr 2026), https://doi.org/10.3389/fpsyg.2026.1730965 | many such theories "lack testable mechanistic commitments"; warm, wet, decohering tissue is the standing objection |
| PSI (telepathy, precognition, remote viewing) as a laboratory effect | **[c]** — contested, and the burden is unmet | Bem (2011) vs Wagenmakers et al., *JPSP* 100(3):426–432 (2011), https://pubmed.ncbi.nlm.nih.gov/21280965/ ; Ritchie, Wiseman & French, *PLoS ONE* 7(3):e33423 (2012), https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0033423 | the flagship result failed three direct replications. **NoöPunk must not present PSI as demonstrated science**, and this draft does not |
| Perception as a user interface; consciousness as fundamental | **[c]** | Hoffman & Prakash, "Objects of consciousness", *Front. Psychol.* 5:577 (2014), https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00577/full | a formal model of perception, **not** evidence of psychic action at a distance |
| Universe as a quantum computer; information as physical | **[c]** | Lloyd, *Programming the Universe* (2006); "The Universe as Quantum Computer", arXiv:1312.4455 (2013) | a computational framing of physics; it does not imply minds can address each other |
| Quantum-information panpsychism (NoöPunk's fictional technological basis) | **[c]→[d]** | Faggin, "Hard Problem and Free Will: an information-theoretical approach", arXiv:2012.06580 (2020) | a first-party philosophical-physical proposal. In NoöPunk it is **engineering doctrine**, not proof — the setting believes it, the book does not assert it |
| DMT-style hyperspace architecture as astral aesthetics | **[d]** | Gallimore, *Alien Information Theory* (2019) | **visual and worldbuilding analogy only.** Not evidence that DMT transports anyone anywhere |

**How the fiction is allowed to use [c] and [d]:** NoöPunk's in-world scientists *believe* QIP explains PSI, and
their instruments are built on that belief. That is how real technology works — on models that may be wrong —
and it lets the game be plausible without claiming the science is settled. The book should say so once, plainly,
in a sidebar, and never again.

---

## 4. The design space: three ways to resolve PSI, and a recommendation

| option | spine | cost | risk | verdict |
|---|---|---|---|---|
| **A. Scene procedure + existing CWN check** | CWN skill check (Notice/Know/Talk/Exert — no new skill) or an attribute check, plus a condition the GM states before the roll | fatigue, exposure, a nosebleed, a worsened position | needs discipline to keep it from becoming free narration | **recommended for Acts II–III** |
| **B. Effort-style discipline pool** | small committed pool, techniques priced per use, refresh on rest | bookkeeping; invites an SWN clone | two pools (psi + System Strain) drift into double-charging | **only at Act IV, capped at 2 points** |
| **C. Full class/tree** | ranks, powers, advancement tree | turns a rookie procedural into a superhero game; breaks the investigation boundary | **rejected** | — |

**Why A first.** The campaign's PSI arrives *inside a police procedural*; the tension is that a rookie can do
something nobody can explain while her caseload gets no easier. A pool of points invites players to optimise
PSI; a declared cost invites them to *choose* it. The repo already has this instinct in
[`CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) §8.3: "my preference is the third
for Act III and the second for Act IV".

**Why not a new skill.** CWN's 19 skills are the immutable spine. Adding "Psychic" would either be a 20th skill
(altering the skill economy) or a second resolver. Use the existing skill the *action* resembles, and let the
psi condition do the work: reading a hostile's intent is **Notice**; holding a defence under pressure is
**Exert**; making contact with something that is not a person is **Know**.

---

## 5. Draft procedure — Active PSI (the recommended version)

### 5.1 One gate before every use

State, out loud, in this order:

1. **Which source** the power comes from — natural awakening, bionic eligibility, or a psychotronic device
   (§2 of [`design/BIONICS.md`](../../design/BIONICS.md)).
2. **What the target is** — a mind, a place, an object, an entity. If the answer is "the case", stop: that is
   the investigation boundary.
3. **The condition** — what it costs if it works, and what it costs if it fails. The GM states it *before* the
   roll, and it is always one of: a condition tag, exposure, or a worsened position on an existing track.

No condition, no attempt. This is the whole balance mechanism, stated once.

### 5.2 Telepathy — receive (Act II)

* **Effect:** surface intent and emotional weather from a visible, thinking being in the same scene. One
  sentence of impression per success, in the target's own idiom ("he is deciding whether to lie about the
  stairs").
* **Never:** memories, passwords, exact numbers, plans not currently being thought, anything from an absent
  person, or any **clue**. A clue is obtained by competence and declared procedure
  ([boundary](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md)).
* **Check:** Notice (or Know for a non-human mind) against the target's relevant defence; the GM may set it at
  10 + the target's rank/HD if the target is resisting.
* **Cost:** on success, a **strain tag** for the scene ("pale", "ears ringing"). On failure, the target feels
  watched — that is a **social fact**, not hit points, and it is the interesting consequence.
* **Consent/agency:** a *willing* contact is free of the check. An *unwilling* one is the whole conflict.
  A person's mind is never "unsecured"; it is a person.

### 5.3 Psychic Defence (Act II)

* **Effect:** resist an incoming psychic effect — intrusion, compulsion, contact — by holding a defence for a
  scene.
* **Check:** an opposed check against the intruding effect, using the skill the defender is actually doing
  (Exert to hold, Know to recognise and close).
* **Cost:** defence is **exclusive**: while held, the character cannot also use active PSI this scene. That one
  line prevents the "always shielded and always scanning" build.
* **Failure:** the effect lands, and the defender learns *that* they were touched and by what *kind* of thing —
  never who.

### 5.4 Astral Projection — the centrepiece

Five states, one resource (the link), one hazard (return), no combat engine.

```
embodied → projecting → astral → returning → embodied
```

| step | what happens at the table | mechanical content |
|---|---|---|
| **1. Anchor** | the character names a place, object or trusted person and describes settling | an anchor is *fiction*; without one, projection is possible but the return difficulty rises by 2 |
| **2. Project** | the room thins; the physical body stays visible to the player, dull to the character | one check (Know, or Exert if forced), condition stated first |
| **3. Travel** | arrival is in a Time/Space scene: symbolic, non-spatial, communicated by intent | movement is by declaration; a "distance" is a number of scene beats, never metres |
| **4. Perceive** | other presences are *impressions with intent*, not monsters with stat blocks | perception is dual: the player still sees the physical scene as an overlay if they choose |
| **5. Interfere** | something notices. The hazard is **losing the thread home** | a short **return track** (3 boxes). Each interference fills one box. Three boxes = lost, and "lost" is a scene, not a death |
| **6. Return** | waking is a scene: the body is cold, the nose bleeds, the memory is there but unattached | difficulty = anchor (0/2) + boxes filled; failure means *another* scene of finding the way back |

**Link integrity** is the resource: three boxes, filled by interference and by overstaying. It is not Effort,
not System Strain, and not hit points — it is the projection's own clock, and it resets when the character
sleeps.

**The body's vulnerability is the tension, not a combat sub-system.** While projected, the physical body can be
found, moved, hurt or killed by anyone in the physical scene. That is a *scene fact* the GM narrates; there are
no astral hit points and no astral combat round. If a fight happens on the astral, it is resolved with the same
CWN combat rules as anything else, with the caveat that "damage" there fills the return track.

**Ectoplasm / manifestation** (advanced, Act III+): a projected character with a bright green centre and a
settled link may become *perceptible* to physical witnesses — a shape, a voice, a cold spot — at the cost of two
link boxes and a condition tag. It is always legible, always brief, and never a way to act on the physical world.

**What projection may never do** (each is a testable boundary in Phase B):

1. grant a clue or open an exit (investigation boundary);
2. scout a location the character has never been to *and* return with usable detail — arrival is by intent, but
   detail is impression, not floor plans;
3. speak to the dead as a telephone (contact with a presence is not automatic truth);
4. replace a warrant, a search or a witness statement;
5. happen automatically at need: it requires a settled, declared scene.

---

## 6. Psychic Defence and the three sources: one effect, three routes

| route | eligibility | what it costs | what it may never do |
|---|---|---|---|
| **Natural awakening** | the character has the latent trait; it wakes in Act II | the condition tags of an untrained mind; social exposure | skip training: the first uses are involuntary |
| **Bionic eligibility** | a bionic modification that unlocks latent PSI (Act II+) | the bionic's own drawbacks; it is *eligibility*, not a power | create a second telepathy mechanic |
| **Psychotronic device** | issued implant or an external device with an operator | the device's charge, calibration, ownership, lawful use | grant an effect the wearer's own PSI could not reach — only *enable* it, and badly |

**Anti-stacking precedence**, in order:

1. If a CWN rule already resolves it, CWN wins.
2. If two psi sources could pay for the same effect, the player picks **one payer** for the scene; the others
   do not stack, and the fiction says why (a device that duplicates a natural gift is *noise*, not a bonus).
3. A psychotronic device never grants a power the character could not otherwise be eligible for; it only reduces
   the requirement by one step at a stated cost.
4. Scripted phenomena (dreams, NDEs, the Higher Self) are **not** player actions and never consume a resource.

---

## 7. Three tabletop examples

**Example A — the stairwell (Act I, implant only).**
The rookie's defensive implant is not PSI; it is CWN cyberware. A hostile psychic tries to push a compulsion on
her. The GM calls for an opposed check (Exert vs the effect), states the condition ("if this fails you take the
stair two at a time, and your partner sees it"), and rolls. She holds. The implant's fiction is that it was the
implant that twitched, not her — and she does not yet know why that matters.

**Example B — the informant (Act II, first telepathy).**
Interview scene. The informant is lying about a visitor. The player declares telepathy: *target = the informant;
source = awakening; condition = a strain tag, and he will remember feeling watched.* Notice vs 10. Success:
"he is deciding whether to protect someone." That is **not** the clue — the clue is the ledger in the clinic,
and the case still requires Administer and access to the ward. The telepathy told her *where to press*, which is
what a good interview does anyway.

**Example C — the projection that goes wrong (Act III).**
She projects from her Kurvi flat to a place she has seen once in a photograph. Anchor: the flat. Travel: by
intent, three beats. Something in the time/space scene notices her — box 1. She stays to listen — box 2. She
tries to return: difficulty 2 (anchor) + 2 (boxes) = 4, and she has Know 1. Failure is not death; it is a
scene of finding the thread, and when she wakes her flat has been entered and her case file is open on the
table.

---

## 8. Python model / interface proposal (design only — Phase B, not this issue)

Nothing in this section may be implemented before the author approves the rules above.

```
src/rules/noopunk_psi.py            # pure functions, no engine, no dice of its own
    @dataclass Condition(tag: str, duration: str, source: str)
    @dataclass Link(boxes: int = 3, filled: int = 0)          # projection clock
    @dataclass Projection(anchor: str | None, state: str, link: Link, scene: int)

    def projection_check(*, skill_total: int, difficulty: int, anchor: bool) -> Outcome
    def return_difficulty(*, anchor: bool, boxes_filled: int) -> int
    def telepathy_contact(*, target_defence: int, willing: bool) -> Outcome
    def defence_contest(*, defender_total: int, intruder_total: int) -> Outcome
    def may_stack(*, payers: Sequence[str]) -> str        # returns the single legal payer
```

Rules the module must obey, so that Phase B cannot quietly become a second engine:

* **No new die.** Every contested check takes a total that the CWN resolver produced; this module never rolls.
* **No import of the investigation module**, and it may not be imported by it — the same AST check that guards
  `swn_psionics` already exists in `tests/test_1105_psi_investigation_boundary.py` and must cover this module too.
* **States serialize.** `Projection` round-trips to JSON so a save/replay reproduces the same scene.
* **One payer.** `may_stack` refuses two sources for one effect, with a reason a table can read out loud.

---

## 9. Interaction with the other four drafts, and with the acts

| with | rule |
|---|---|
| **Psychotronics** | a device is an *enabler*: it can lower the requirement for an effect the character is eligible for, and it carries charge/calibration tags. It never adds a second implementation of Telepathy. |
| **Bionics** | bionic eligibility unlocks a *route*, not a power. A hybrid's PSI is natural PSI with a different origin story. |
| **Europol chargen** | the defensive implant is issued kit; the awakening is a GM secret with a staged unlock, not a character-creation choice. |
| **Tags** | psi conditions are **status tags** with a duration and a source; "watched" and "pale" are tags, not new statistics. Polarisation (StO/StS) is untouched by PSI use. |
| **Act I** | no active PSI. The implant defends, badly, and the dreams are scripted. |
| **Act II** | telepathy (receive) and psychic defence; projection only as an involuntary glimpse. |
| **Act III** | full projection loop, astral perception, narrow psychometry. |
| **Act IV** | the authored advanced package; astral interference; Higher Self contact stays scripted. |

---

## 10. Open decisions for Tomi

1. **Resolution spine:** scene procedure (A), small Effort pool (B), or A then B per act? Recommendation: A for
   II–III, B capped at 2 for IV.
2. **The return track:** three boxes, or a difficulty ladder with no boxes? Boxes are more legible; a ladder is
   less bookkeeping.
3. **Telepathy's range:** same scene only, or same building? Same scene keeps it a conversation, not a scanner.
4. **Is the defensive implant PSI at all**, or purely CWN cyberware that happens to work? The campaign doc says
   equipment; keeping it equipment protects CWN.
5. **Does a failed telepathy always reveal the psychic?** Recommendation: yes for unwilling targets — it is the
   most NoöPunk consequence available.
6. **Astral combat:** never (recommended), or a named exception at Act IV with the return track as its damage?
7. **Psychometry:** keep, cut, or script it? It is the power most likely to break a case.
8. **Who else has this?** Are there Europol colleagues with the same gift — and if so, is that a faction?

---

## 11. Bibliography (checked in this pass; verification status recorded)

| source | date | status |
|---|---|---|
| Tang et al., *Nat. Neurosci.* 26:858–866 | 2023 | metadata and abstract confirmed; full text paywalled |
| Kunz et al., *Cell* 188(17):4658–4673 | 21 Aug 2025 | open access; inner-speech decoding **and** its defensibility confirmed |
| *Nat. Commun.*, 256-element TUS system | 5 Sep 2025 | abstract confirmed |
| *Nat. Commun.*, TUS of nucleus accumbens | 2025 | abstract and results confirmed |
| Ma & Wang, *Front. Psychol.* 17, 10.3389/fpsyg.2026.1730965 | 28 Apr 2026 | abstract confirmed |
| Wagenmakers et al., *JPSP* 100(3):426–432 | 2011 | citation confirmed; text not read in full |
| Ritchie, Wiseman & French, *PLoS ONE* 7(3):e33423 | 2012 | confirmed |
| Hoffman & Prakash, *Front. Psychol.* 5:577 | 2014 | confirmed |
| Lloyd, *Programming the Universe* / arXiv:1312.4455 | 2006 / 2013 | cited from the issue; **not read in this pass** |
| Faggin, arXiv:2012.06580 | 2020 | located; **not read in this pass** |
| Gallimore, *Alien Information Theory* | 2019 | cited from the issue; **not read in this pass** |
| SWN Revised Deluxe pp. 30–41; AWN Deluxe pp. 264–266; WWN pp. 62, 90, 344; CWN SRD | — | section and page anchors taken from `data/rules/*_sections.json`, not from memory; no protected text reproduced |
