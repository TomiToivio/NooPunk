# DRAFT — the first NoöPunk single-player campaign: *Europol Rookie → Fourth-Density Awakening → Wanderer*

> **STATUS: DRAFT / open to revision.** Source issue: [#1132](https://github.com/TomiToivio/NooPunk/issues/1132).
> This is the campaign **outline**, not rules, not prose, not an implementation. Nothing here is locked.
> The one thing it does not touch is the rules chassis: **Cities Without Number remains the immutable
> core** (`rulebook/WITHOUT_NUMBER_BASELINE.md`, `docs/architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md`).

**How to read this document.** Every claim carries one of four marks:

| mark | meaning |
| --- | --- |
| **CANON** | established in the repository; cited. Change it only through the document cited. |
| **AUTHOR** | an author decision, named. Agents must not fill these in. |
| **PROPOSAL** | a concrete shape offered for approval; not canon until accepted. |
| **OPEN** | a question this document deliberately leaves unanswered. |

Where this outline and an older document disagree, the newer authority wins: the Europol frame
(`docs/world/ALTERNATE_HISTORY_1114.md`, #1114) supersedes every earlier "the player is a UNSA rookie"
premise, and CWN supersedes every 1d10/1–10 prototype in `RULEBOOK.md`'s historical chapters.

---

## 1. Logline, premise, themes, tone ramp

**Logline.** A newly graduated Europol officer takes a routine posting in Helsinki, discovers that the
unit they were assigned to exists because the impossible keeps filling out forms, and eventually learns
that the impossible has been filling out *their* file since before they were born.

**Premise (CANON).** The year is 2045. The NHI Crisis has happened: contact is public, the Quarantine has
ended, UNSA exists but the project to turn the UN into a world government failed, the EU and
nation-states still decide what can actually be done, and psionics is a social and scientific revolution
rather than a secret (`README.md`; `rulebook/10_SINGULARITY_CRISIS.md` §9.3; `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` §4).
Europol's Helsinki Field Office — the former Suojelupoliisi anomalous-cases archive known informally as
**Ö-Mappi** — is the default playable frame (`docs/world/ALTERNATE_HISTORY_1114.md`;
`docs/design/ISSUE_626_ROMPPAINEN_EUROPOL_UNIT.md`).

**The four-act ramp.** Each act changes *genre*, not merely stakes:

| act | genre | what the player thinks the game is |
| --- | --- | --- |
| I | grounded cyberpunk police procedural | a job sim in a strange city |
| II | conspiracy thriller with New Weird intrusions | a cover-up story |
| III | threshold / transformation (PROPOSAL) | a story about what you are becoming |
| IV | cosmic science fantasy | a story about what humanity is for |

**Themes.** Service versus domination. The paperwork of the impossible. Institutions as people who
mostly mean well and are structurally wrong. Consent, evidence and jurisdiction as ethical objects.
Memory as an unreliable witness that is sometimes the only witness.

**Comedy guidance (AUTHOR tone, PROPOSAL texture).** The register is *Maniac*'s institutional absurdity:
the joke is that a classified unit has three incompatible coffee systems and a procurement process for
ontological anomalies. Comedy comes from character and bureaucracy, never from punching down, never from
mental illness as a punchline, and never at the expense of a witness. A scene may be funny or serious;
it may not be funny *about* the serious thing. Romppainen is the calibration: dry, precise, occasionally
devastating, never a quip machine.

---

## 2. The protagonist: fixed dossier versus player-built identity

The issue's principle: *the past is authored; the future remains open.*

### 2.1 Fixed (CANON-level design commitments)

| element | value | note |
| --- | --- | --- |
| Age / status | young; newly graduated Europol officer, first posting | CANON by #1132 |
| Employer | **Europol**, Helsinki Field Office / Ö-Mappi | #1114 supersedes the UNSA rookie premise |
| Housing | company flat in **Kurvi** | PROPOSAL detail: Kurvi is the bohemian tram-and-nightlife crossroads in `data/world/helsinki_locations.json`; a rookie flat above a bar is a better story than a barracks |
| Issued cyberware | basic Europol set: **BCI** and a **defensive psychotronic implant** | CANON by #1132; fiction in §8.4. No stat blocks or prices invented here |
| Gear | standard Europol officer equipment | CWN equipment procedures; the specific load-out is an AUTHOR pick |
| Latent PSI | present but unregistered/undeclared at start | CANON by #1132 ("latent PSI/psychotronic setup"); the *degree* is AUTHOR |
| Hidden past | authored, revealed through play | AUTHOR slot: `design/characters/ROOKIE_MEMORIES.md` (#1123) is the author's page and is deliberately empty; agents must not fill it |
| Identity revelations | scheduled, not exposited | §5 |

### 2.2 Open (player-built)

Personality, loyalties, political and civic alignment, professional ethics, relationships and romance,
whether they become a principled or a dirty cop, how they handle the institution's coercive edge, and
what they do with the truth at the end. None of this is pre-decided. There is no alignment score that
plays the character for them (§6).

### 2.3 Starting sheet — PROPOSAL, CWN-legal, no new rules

Level 1, CWN character creation as written (`src/rules/cwn_character.py`, `cwn_advancement.py`):

* Attributes: the standard array **14, 12, 11, 10, 9, 7** assigned to taste (CWN alternative to rolling;
  proposed so the tutorial character is legible). AUTHOR may prefer 3d6-in-order for tone.
* Skills: **Notice 0, Talk 0, Administer 0, Know 0** plus two picks shaped by the chosen specialist
  track (see §4.2). Ranks obey CWN's starting cap (level-1 maximum).
* Derived: HP by CWN hit dice (1d6, or 1d6+2 with Hard to Kill), saves 15+, attack bonus +0, System
  Strain maximum = Constitution (`tests/test_cwn_ch1_5_fidelity_1080.py` pins these).
* The BCI and the defensive psychotronic implant are **cyberware with a System Strain cost**; they occupy
  the character's Strain budget from the first scene, which is the honest way to make "issued kit" feel
  like a constraint rather than a gift.

---

## 3. The four acts

### ACT I — *The Rookie* (CANON: grounded police procedural, no metaphysics)

**Dramatic question:** can you be a decent cop inside an institution that is already lying to you about
something small?

**Purpose.** Teach CWN, the city, the unit and the tone. Establish that this is a world where the
impossible is *administratively* real and *personally* irrelevant — yet.

**Episodes (PROPOSAL, five shifts + downtime, §4):**

| # | episode | spine |
| --- | --- | --- |
| I.1 | *First Day in Ö-Mappi* | onboarding; a sealed evidence case arrives under an impossible tracking identity | 
| I.2 | *The Empty Case* | chain-of-custody investigation with three mundane explanations and one that is not |
| I.3 | *Paperwork* | interagency jurisdiction fight over a witness; procedural comedy with a real cost |
| I.4 | *Night Shift* | street-level case, ordinary crime, one detail that does not fit |
| I.5 | *The Review* | the rookie's first report is graded by people who want a different conclusion |

**Locations.** Ö-Mappi's basement, the Europol office at Ratakatu, Kurvi, Helsinginkatu, the university,
Olutravintola Putki, a logistics depot, a magistrate's waiting room (`data/world/helsinki_locations.json`).

**Cast.** Dr. Harri Romppainen (CANON-ish: hypothesis-driven director, `design/characters/HARRI_ROMPPAINEN.md`);
**Lotta Kallio** (CANON: established SuPo–Europol field partner); draft NPCs from
`docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md` — **Aino Laakso** (tactical), **Mika "Mikke" Rautio** (infosec),
**Leena Saarinen** (empath, PSI as leads not proof) — all marked draft names there and here.

**Transition to Act II (criteria, PROPOSAL):** the player has (a) closed or buried one case on their own
judgement, (b) formed at least two relationships with a stated position, and (c) been handed one document
that contradicts the official account. No timer; the act ends when those three are true.

**Revelations in Act I:** exactly one, ambiguous — a name or a date that recurs where it should not
(§5, fragment F2). No UFO set piece, no prophecy, no proof.

---

### ACT II — *The Conspiracy / First Awakening* (CANON: ethical rupture, escalation, bounded PSI)

**Dramatic question:** when the institution's interest and a person's freedom diverge, which one are you?

**Purpose.** Turn the procedural into a conspiracy with a *moral* centre, and open the protagonist's PSI
in a way the rules can actually pay for.

**Inciting incident (PROPOSAL).** A case that should be ordinary — a missing psychiatric patient, or a
whistle-blower in a biotech contractor — turns out to be *two* cases: a real crime that a ministry wants
closed, and an anomaly that the same ministry wants filed as the crime. The player discovers that Ö-Mappi
is being used as a laundering mechanism for inconvenient people: the "anomalous" label is doing the work
of a prison.

**The moral turning point (CANON: must hinge on service versus domination and free will, not on law,
loyalty, politics, drugs or romance).** PROPOSAL shape: the protagonist can (1) protect the witness and
lose the case, (2) use the witness to break the ministry and expose the mechanism, (3) hand the witness to
the institution that can *help* them but will also own them, or (4) walk away with the file and let the
system settle. Each is defensible; each costs something specific. The polarity question is not "did you
obey?" but "did you treat a person as an end or as an instrument?"

**The awakening (CANON: dramatic fourth-density psychic awakening, story-driven; PROPOSAL trigger).** In
the middle of the moral crisis, when the protagonist chooses to *reach* for someone — to hold a mind that
is slipping, to shield a witness from a psychic interrogation, to follow a thread that is not physical —
the first technique fires without training and without consent of the body. The trigger is the choice,
not a cutscene: alternate compatible routes are listed in §8.5 so a player who solved the act without
violence still awakens.

**Episodes (PROPOSAL):** three linked cases, one of them outside Helsinki (Tampere or Tallinn), each
adding one capability and one institutional enemy; a mid-act audit of the protagonist's own file; and a
finale where the choice is made under time pressure with incomplete information.

**Locations.** A ministry records office, a private clinic, a freight terminal, a Europol liaison office
abroad, and one place that does not appear on the map (§5).

**Transition to Act III:** the protagonist is awakened, has chosen a side *provisionally*, and has been
told — credibly — that the anomaly is not random. Act III opens because the protagonist starts asking
what the pattern is, not because the plot pulls them.

---

### ACT III — *Transformation / The Threshold* — **PROPOSAL, pending the author's decision**

> **This act is not confirmed canon.** #1132 defines Acts I, II and IV and leaves III unspecified. The
> shape below is offered for approval or replacement; nothing in the repository should treat it as
> settled.

**Dramatic question:** what are you willing to become, and who gets to decide?

**Purpose.** Bridge the grounded conspiracy and the cosmic revelation, and let the *player's* accumulated
choices determine what the protagonist's power costs them.

**Proposed content.**

* The investigation deepens into conflicting explanations: the protagonist's childhood, the Quarantine's
  end, the Harvest, and fourth-density reality start to look like the same subject from different sides.
* **Astral experiences** enter play here first — bounded, disorienting, and *not yet* a travel engine
  (§8.3). The distinction between physical and astral phenomena becomes a procedural problem: evidence
  from one layer does not convict anyone in the other.
* Life and career consequences: allies and antagonists inside Europol, a crisis of trust in the
  institution, relationships damaged by revelation, and the question of **PSI registration** — the
  protagonist is now someone the state would like to know about.
* Selected missions beyond Helsinki; the Wanderer identity stays concealed until Act IV.
* **Rules unlocked only as scenes need them:** bounded astral/Time-Space procedure, Chakra/awakening
  tags, and the first Catalyst reflection procedure (§8).

**Alternative shapes the author may prefer (OPEN):** (a) fold Act III into Act II as a long coda;
(b) make Act III the *institutional* act — a promotion/command phase where the protagonist is inside the
machine; (c) make Act III the *personal* act — a full campaign season of Helsinki life and relationships
before the cosmic turn. Each is a different game; the choice is D78 (§11).

---

### ACT IV — *The Wanderer* (CANON: astral Higher Self, expanded PSI, science fantasy, player-determined ending)

**Dramatic question:** now that you know what you are, what are you for?

**Purpose.** Pay off the memory ladder, expand the scale, and hand the ending to the player without
collapsing into a morality menu.

**The astral sequence (CANON).** In a major astral scene the protagonist meets their **Higher Self** and
learns they are a **Wanderer**. Earlier fragments are recontextualised: the reader/player now sees what
they meant, but *what it means for this person* — and what they do about it — stays open. The Higher Self
offers revelation, not obedience; a refusal or an argument is a legitimate response.

**Expanded play.** The protagonist is now an experienced character: CWN advancement (levels, skills,
Edges/Foci), cybernetics, potent PSI, possibly Bionics (§8). Scale expands to Confederacy civilization,
astral and orbital locations, and missions whose failure modes are political rather than personal.
Space operations, if reached, use SWN when actually needed — not as a new core.

**The final conflict (CANON: three trajectories plus reconciliation).**

1. **Wanderer in the Confederacy** — positive/StO service at cosmic scale; the cost is distance from
   everything human.
2. **Europol officer, committed to humanity** — also potentially StO, but with different loyalties and a
   different account of what service means; the cost is that the Confederacy may be right about some
   things the protagonist now has to refuse.
3. **StS — domination or personal power** — betraying or exploiting both. The cost is the people who
   believed in them; the ending must be written as a real choice, not a punishment cutscene.
4. **Reconciliation (attempt)** — available if the player earned it: human and Confederacy obligations
   held together for a while, at a price. Not a golden ending; a harder third thing.

**Zero-polarization interaction (CANON constraint).** The positive-path Law of One mod's proposal sends a
zero-polarization PC out of player control (`docs/law_of_one/WITHOUT_NUMBER_COMPATIBILITY_PHASE1.md`,
"Polarization (StO): 0–10 proposal, at 0 positive-path PC → NPC"). The campaign must not silently
contradict that. PROPOSAL: the StS route is presented as an **NPC handoff with an authored epilogue** —
the player makes the final choice, the epilogue narrates the character's trajectory as someone else now
watches them, and the rules' zero-polarization rule is honoured rather than patched (D80, §11).

---

## 4. Act I as a playable slice

The first mission must be **independently playable** and complete. The design borrows the structure of
`docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md` (an existing Europol-graduate scenario) without copying its
text, and uses the city data already in `data/world/helsinki_locations.json`.

### 4.1 The first week (PROPOSAL)

| shift | scene | CWN at the table | what it teaches |
| --- | --- | --- | --- |
| Mon | arrival, three doors, a lanyard with three logos | none | tone; the unit is a filing cabinet that breathes |
| Mon pm | *the empty evidence case* arrives | **INT+Administer** (routine 8) to read the manifest; **WIS+Notice** to see the seal is wrong | a check buys precision, not the clue |
| Tue | witness interview at Kurvi | **CHA+Talk** (difficulty set by the witness's fear); **WIS+Empathy-equivalent = Notice** | consent, and when *not* to push |
| Tue pm | the depot | **DEX+Sneak** or **INT+Program** for the audit trail; either works | two routes, one truth |
| Wed | jurisdiction fight (SuPo vs Europol vs the ministry) | **INT+Administer**, **CHA+Lead** | institutions are the antagonist |
| Wed pm | **downtime**: the flat, the bar, a friend, a bad decision | none; tags only | the character is built out of hours |
| Thu | the ordinary crime underneath | CWN combat possible, always avoidable | lethality; a gunfight is a failure state |
| Fri | the report | the player writes the conclusion; the unit grades it | the institution's version vs the player's |

**The case (PROPOSAL, non-supernatural by construction).** A sealed evidence case with an impossible
tracking identity turns out to have been *re-labelled* by a clerk protecting a relative — a mundane
crime with a real victim, an institutional cover-up, and one detail (an obsolete radio identifier) that
remains unexplained. The player may close it as fraud, as anomaly, or as both. **No metaphysics is
confirmed in Act I.**

### 4.2 Specialist track (PROPOSAL)

The player picks one at creation, which shapes two skills and a handful of scene permissions, never a new
subsystem: **tactical** (SWAT-style entry and scene security), **infosec** (logs, authentication, forensic
accounting), **analyst** (archives, link analysis, source evaluation), **monitored psionic asset** (the
latent PSI is on file; the BCI is both tool and leash). The scenario file lists the same four tracks; the
canonical version belongs with the character-creation pass (D77, §11).

### 4.3 Shift / downtime cycle (PROPOSAL)

A week is five shifts plus two downtime beats. Shifts spend CWN scenes; downtime spends *choices* —
who you see, what you do, what you admit. Downtime is where reputation, relationships and personality
tags come from (§6), which is why it is a mechanic and not a menu: the character is what happens between
cases.

### 4.4 Tabletop equivalents

Everything above runs on paper: the case is a clue list and a manifest, the checks are CWN 2d6, the
combat is CWN's, the tags are lines on the sheet. The console slice already runs one case this way
(`docs/tabletop/PRINTABLE_SHEET_1053.md`, `docs/PORTABLE_CONSOLE_CASE.md`); the Goal tag has its own paper
procedure (`docs/rules/GOAL_TAG_1119.md`).

---

## 5. Memory and revelation plan

**The rule: the past is authored, its meaning is played.** `design/characters/ROOKIE_MEMORIES.md` (#1123)
is the author's page for the actual memories; this section specifies the *structure and delivery*, not
the content.

### 5.1 The three categories (never mixed in play)

| category | example shape | how the game presents it |
| --- | --- | --- |
| **Confirmed biography** | a birth record, a school, a dead parent, a clinic | documents and testimony that corroborate each other; stated plainly when found |
| **Misleading interpretation** | a memory that *looks* like an abduction; a file that *looks* like a cover-up | presented with at least one mundane reading that also fits; never resolved by fiat |
| **The Wanderer revelation** | the Higher Self (Act IV) | only after the ladder; reframes rather than contradicts |

### 5.2 The ladder (PROPOSAL: seven fragments, each with a redundant route)

| # | fragment | delivery | redundancy (missing it cannot hide the revelation) |
| --- | --- | --- | --- |
| F1 | a recurring smell/room in a dream | dream, Act I downtime | an article about the same building |
| F2 | a date that recurs (a licence, a case number, a funeral) | document, Act I | a colleague's offhand remark |
| F3 | a childhood photo with a person nobody remembers | conversation, Act II | a school record with the same gap |
| F4 | a medical file that describes something not human-standard | clinic, Act II | a second clinic's file, or a Bionics test |
| F5 | the protagonist's own Ö-Mappi file, opened early | archive, Act II/III | a leak, or Romppainen's admission |
| F6 | an astral echo of a place the protagonist has never been | astral, Act III | a news photograph of the same street |
| F7 | the Higher Self | astral, Act IV | none needed; this is the reveal |

**Redundancy rule.** Every essential revelation has at least two independent routes, and the game never
gates F7 behind a roll. A player who misses F1–F3 still understands Act IV; they lose *texture*, not
comprehension. This is the GUMSHOE principle already used by the investigation layer
(`src/rules/investigation.py`: core clues are granted, rolls buy cost and precision).

### 5.3 Spoiler boundary

Before Act IV the game may say: *you were not born where they told you*; it may not say *you are a
Wanderer*. Dreams may be intense; they may not be exposition. If a scene would prove the answer, it is
an Act IV scene.

---

## 6. Choice and transformation map

### 6.1 What changes, and how it is recorded

| track | how it changes | mechanism status |
| --- | --- | --- |
| **Goals** | explicit objectives, short/medium/long, retired on completion | **implemented** (`src/rules/goals.py`, #1119) |
| **Reputation** | one integer per faction, −4…+4, created only when earned; absent ≠ zero | **planned** (next tag type; #1119 roadmap) |
| **Personality** | behavioural guidelines, occasionally a named ±1 on a specified CWN action | **planned** (`Pacifist-2` is the canonical first example) |
| **Relationships** | trust, debt, visibility; separate from ideology | **implemented for NPCs** (`mud/nopunk_mud/ideology.py`); player-facing use is **planned** |
| **Professional standing** | rank, access, assignments | CWN XP/advancement + institutional fiction; **no new meter** |
| **Substance use** | fiction first; consequences through CWN Strain/healing where relevant | **planned** (AWN addiction exists as an optional overlay, #928; not wired to this campaign) |
| **Bionics** | hidden biological traits with provenance | **planned** (§8.2) |
| **Polarization (StO/StS)** | sustained patterns of service vs domination | **research only** (Law of One Phase 1, #1124) |

### 6.2 The separation that matters

The issue is explicit, and the design keeps it in the code, not in a paragraph:

> *Ordinary lifestyle choices, minor vice, dependency, politics, sexuality, or imperfect behaviour do not
> automatically determine Polarization.*

Polarization therefore reads **patterns over time** — repeated choices about other people's agency, with
recorded stakes — and not events. Getting drunk, falling in love, being rude to a superior, or having a
bad week cannot move it. Using a person as an instrument, or refusing to when it would have been easier,
can. The implementation proposal (§8.6) is a *ledger of consequential choices*, not a virtue counter.

---

## 7. Act II's moral turning point in detail

**The situation (PROPOSAL).** A ministry is using the "anomalous" classification to disappear people it
finds inconvenient — not aliens, not psychics, just people. The protagonist holds the mechanism and one
witness who can prove it.

**Four defensible approaches.**

| approach | what it protects | what it costs | what it can teach |
| --- | --- | --- | --- |
| **Shelter** the witness, drop the case | one person's safety | the mechanism survives; the protagonist's credibility | service as protection |
| **Weaponise** the witness to break the ministry | the public's right to know | the witness's agency; possibly their life | service as exposure, and its arrogance |
| **Institutionalise** the witness — hand them to the body that can treat them | continuity, "proper channels" | ownership dressed as care | service as domination in a kind voice |
| **Walk away** with the file | the protagonist's own integrity | everyone else | complicity by exit |

**Why this is the Act II hinge.** None of the four is the "lawful" option and none is the "good" option.
The polarity question is not *did you obey* but *did you treat a person as an end*: shelter and weaponise
can both be StO if the witness consents and is protected; institutionalise and walk away can both drift
StS even while looking professional. That is the distinction the issue demands, and it is the one the
rules must not flatten.

**Awakening trigger (PROPOSAL, with alternates).** The first technique fires when the protagonist reaches
for another mind *because the choice has already been made*: to hold a mind that is slipping (Telepathy
Thread), to shield a witness from an interrogation (Metapsionics Dampen), or to follow a trace that is not
physical (Telepathy Empathic Trace). Players who solved the act without violence awaken through the
protective route; players who solved it violently awaken through the same route, later and worse.

---

## 8. Rules by act — what exists, what is planned, what must not be built yet

**CWN is the core and is not modified.** Everything else is additive and introduced when a scene needs it.

| rule module | first needed | source | status on `main` (2026-11-04) |
| --- | --- | --- | --- |
| CWN core: attributes, skills, checks, saves, combat, damage, Strain, cyberware, equipment, advancement | Act I, shift one | CWN SRD (CC0) | **implemented**: `src/rules/cwn_*.py`, coverage in `docs/rules/CWN_COVERAGE_1068.md` |
| Investigation layer (core clues granted, rolls buy precision) | Act I | GUMSHOE-informed mod | **implemented**: `src/rules/investigation.py`, `docs/design/ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md` |
| Goal tag (short/medium/long, CWN XP) | Act I downtime | #1119 | **implemented**: `src/rules/goals.py` |
| BCI + defensive psychotronic implant as cyberware | Act I, issued kit | CWN cyberware + fiction | **fiction only**: CWN cyberware procedures exist; these two items are authored equipment, not new rules (§8.4) |
| SWN psionics: Telepathy (Thread, Command, Deep Scan, Empathic Trace), Metapsionics defence (Dampen, Torch Shield, Sever) | Act II awakening | SWN (procedure implemented, catalogue reference-only) | **implemented as procedure**: `src/rules/swn_psionics.py`, `src/rules/psionics.py`, `data/rules/psionics_techniques.json`; *effects* stay in the book (`docs/design/ISSUE_1043_PSIONICS_FACTIONS.md`) |
| **Astral Projection** | Act III (first), Act IV (full) | **no SWN equivalent in the implemented catalogue** | **missing**: needs an explicit compatible procedure; Phase 1 proposes the shape (`docs/law_of_one/WITHOUT_NUMBER_COMPATIBILITY_PHASE1.md`, "Astral Projection") |
| Bionics mod (AWN-mutation-inspired) | Act II discovery, Act III use | AWN mutations as *inspiration* only; AWN has no verified open licence | **not implemented**: no module, no table transcription. Design constraints in §8.2 |
| Psychotronics as a category | Act II, when the implant matters | CWN cyberware + QIP fiction | **not implemented** beyond cyberware; §8.4 fixes the boundary |
| Polarization / Catalyst / Awareness | Act II first track, Act III procedure | Law of One Phase 1 (#1124) | **research only**: `docs/law_of_one/WITHOUT_NUMBER_COMPATIBILITY_PHASE1.md` |
| Chakra / SMC / Higher Self | Act III–IV | Law of One Phase 1 (narrative proposals) | **research only** |
| SWN space/orbital tools | Act IV, if visited | SWN (procedure now, catalogues as data) | **partial**: `src/rules/swn_starships.py`, `swn_sector.py`, faction engine |

### 8.1 Explicitly not built for this campaign yet

No new dice, no new skill list, no chakra UI, no astral travel engine, no polarity meter in the HUD, no
psychotronic item catalogue, no Bionics mutation table, no second XP economy, no parallel psionic
resource pool. **Each of those is added only when a specific scene in §§3–4 needs it.**

### 8.2 Bionics (planned; design constraints only)

Biological/genetic change, frequently invisible, distinct from cyberware and from PSI:
provenance (biotech procedure, engineered lineage, hybridisation, or latent potential), concealment
(the bearer may not know), and mechanical restraint (a trait, a permission, or an eligibility gate —
never a free SWN technique and never a duplicate Effort pool). AWN mutations are *inspiration*; AWN's
text is not licensed for transcription here (`data/sources/game_system_rights.json`). **Not implemented.**

### 8.3 Astral Projection (planned; the one PSI gap this campaign forces)

The implemented SWN catalogue has Telepathy, Metapsionics, Biopsionics, Telekinesis, Precognition and
Teleportation — no astral procedure. Teleportation is not astral projection. The Phase 1 supplement
already sketches the compatible shape: attunement, body anchor, projected state, reachable region,
return/snap-back/severance, and consequences on the physical layer. Treat that as the design source, and
do not invent a second travel engine for it.

### 8.4 Psychotronics (boundary, not a subsystem)

A psychotronic device **always requires a human conscious operator**; it amplifies or mediates an
existing psychic capacity and calls the existing resolver. It is cyberware when implanted (CWN Strain,
CWN installation, CWN hacking surface) and equipment when external. Non-QIP microwave devices are
external only — never implants, never "psionics" in this setting's terminology. The protagonist's
defensive implant is therefore: a CWN cyberware item, fiction-first, whose effect is a *modifier or
permission defined by the scene's rules*, not a second psionic system.

### 8.5 Awakening without railroading

At least two routes into Act II's awakening, tied to the moral choice rather than to a scripted trigger:
the **protective** route (shield/hold/reach for someone) and the **investigative** route (follow a trace
that is not physical). Both are scenes, not cutscenes; both are gated on the player having made a
consequential choice, not on a die roll.

### 8.6 Polarization as a ledger (proposal)

If and when it is implemented: record **consequential choices with stakes** — who was used, who
consented, who was protected, who paid — and derive the trajectory from *sustained patterns*. Never from
a single act, never from lifestyle, never from a die roll. Keep it out of the character sheet's core
numbers; it is a narrative track with explicit thresholds and warnings, per Phase 1.

---

## 9. Institutions and continuity

| institution | role in the campaign | canon / caution |
| --- | --- | --- |
| **Europol, Helsinki Field Office / Ö-Mappi** | the protagonist's employer; cross-border intelligence and coordination, **not** independent local arrest powers | CANON (#1114, #626). National police execute searches and detentions under their own law — a permanent source of scenes |
| **Finnish police / Suojelupoliisi** | hosts, rivals, sometimes the only adults in the room; Lotta Kallio's home institution | CANON-ish (#626). Jurisdiction friction is the procedural engine, not a villain |
| **Ministry / municipal authorities** | the institution that wants the case closed | PROPOSAL; unnamed on purpose, so it can be specific later |
| **UNSA** | an institution and later collaborator; may become a plot element | CANON: UNSA exists but the federal project failed (`README.md`); **not** the protagonist's employer |
| **The Confederacy** | Act IV counterpart; offers service, revelation and a politics | CANON: `rulebook/16_CONFEDERACY_SOURCE_AND_CONTACT.md`; **not automatically morally correct** |
| **Orion Group** | the exploitative alternative; present from Act II as a corporate/political force | CANON: `rulebook/12_BEINGS.md` §11.4 |
| **Zookeepers** | public benefactors with an unexplained agenda | CANON: `README.md`, `rulebook/10_SINGULARITY_CRISIS.md` |
| **The Greys** | Act IV's ambiguous technology brokers | CANON: `rulebook/12_BEINGS.md` §11.6 |

**Uncertainties to keep uncertain (OPEN).** The degree of Europol's operational independence in Finland;
whether Ö-Mappi is a Europol unit or a SuPo unit seconded to Europol (the repository uses both framings);
what the Quarantine's end actually was; who the Wanderers are working for, if anyone; whether the Higher
Self is an entity, a metaphor, or the protagonist's own future. Do not resolve these in a scenario
without an author ruling.

---

## 10. Endings

Four trajectories, each with a real cost, none of them a moral grade:

1. **Wanderer in the Confederacy (StO)** — the protagonist serves at cosmic scale. Cost: the human
   relationships that cannot follow; the suspicion that service at that altitude is another kind of
   instrumentalisation.
2. **Europol officer, humanity first (StO)** — the protagonist uses everything they learned inside the
   institution that raised them. Cost: the Confederacy may be right about some things they must now
   refuse; the institution remains imperfect.
3. **StS — domination or personal power** — the protagonist exploits both sides. Cost: everyone who
   believed in them. Present this as a **choice with an authored epilogue**, not a punishment.
4. **Reconciliation (attempt)** — human and Confederacy obligations held together for a season. Cost:
   it does not hold forever; the epilogue says what broke and what did not.

**Rules interaction.** If the positive-path mod implements "zero polarization ⇒ NPC handoff", ending 3
must be delivered through that handoff rather than by ignoring it: the player chooses, the epilogue
narrates the character as someone others now watch. This is the honest way to keep the rule and the
player's agency.

**Not a false binary.** Confederacy ≠ StO; Europol ≠ StO; disagreement ≠ StS; imperfection ≠ StS. A
protagonist who leaves Europol can be StO; one who stays can drift StS; the ending text must be able to
say so.

---

## 11. Open questions and author decisions

| # | question | options | blocks | proposed default |
| --- | --- | --- | --- | --- |
| **D76** | Are the draft NPCs (Aino, Mikke, Leena) canon, renamed, or replaced? | adopt as-is / rename / author's own cast | every Act I scene, and the console slice's cast | keep as draft names, marked draft |
| **D77** | Is the specialist track player-chosen or authored? | four tracks / fixed "monitored psionic asset" / no track | character creation, Act I scene permissions | four tracks, PSI on file regardless |
| **D78** | What is Act III? | bridge act / institutional act / personal act / fold into II | the whole late campaign | bridge act as sketched, marked PROPOSAL |
| **D79** | What is the authored hidden past? | Tomi writes it | §5 content, Act IV payoff | **author's** (`design/characters/ROOKIE_MEMORIES.md`) |
| **D80** | How is the StS ending delivered against the zero-polarization handoff? | NPC handoff + epilogue / explicit exception / refuse StS ending | ending 3, Law of One compatibility | handoff + epilogue |
| **D81** | When do orbital/space rules enter? | Act IV only / Act III optional / never | SWN starship integration, art scope | Act IV only |
| **D82** | Where is the comedy line, and how lethal is Act I? | Maniac-absurd + CWN as written / drier tone / starter protection | every scene's voice and the tutorial's difficulty | Maniac-absurd, CWN lethal, fighting designed as a failure state |

All seven are carried on `docs/design/AUTHOR_DECISION_QUEUE.md` (rows D76–D82). Until the author rules, this
document is the proposal, not the ruling.

---

## 12. References and cross-links

**Rules authority**
* `rulebook/WITHOUT_NUMBER_BASELINE.md` — the binding chassis.
* `docs/architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md` — engine-neutral rules, adapters, tabletop parity.
* `docs/rules/CWN_COVERAGE_1068.md` — what is implemented, partial and missing.
* `docs/rules/GOAL_TAG_1119.md` — the first tag, with its paper procedure.
* `docs/design/ISSUE_1043_PSIONICS_FACTIONS.md` — SWN psionics procedure and its licensing boundary.

**Setting and institutions**
* `docs/world/ALTERNATE_HISTORY_1114.md` — the Europol frame and the alternate history.
* `docs/design/ISSUE_626_ROMPPAINEN_EUROPOL_UNIT.md` — the unit, its doctrine and its cast cautions.
* `rulebook/10_SINGULARITY_CRISIS.md` — the NHI Crisis, the Quarantine's end, the three ASI outcomes.
* `rulebook/12_BEINGS.md`, `rulebook/16_CONFEDERACY_SOURCE_AND_CONTACT.md` — beings, Wanderers, the
  Confederacy, Orion.
* `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md`, `rulebook/21_PSI_PARADIGM_SHIFT.md` — the PSI
  revolution and its social consequences.
* `docs/world/NHI_FACTIONS_922.md` — faction landscape.

**Existing playable material**
* `docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md` — the Europol-graduate first day; the Act I seed.
* `data/scenarios/lakkahaltia/*` — the shipped case graph; `docs/PORTABLE_CONSOLE_CASE.md`,
  `docs/tabletop/PRINTABLE_SHEET_1053.md` — its paper and console forms.
* `data/world/helsinki_locations.json`, `helsinki_map.json`, `lexicon.json` — the city.
* `docs/design/GAMEPLAY_LOOP.md` — the shift/downtime loop this outline's Act I assumes.
* `docs/design/ISSUE_724_CRPG_DESIGN_MEMO.md` — the loop-and-tactics memo; not a campaign outline.
* `docs/design/VISION.md` — long-term direction (aspirational, authorizes no mechanics).

**Metaphysics, research-only**
* `docs/law_of_one/WITHOUT_NUMBER_COMPATIBILITY_PHASE1.md` (issue #1124) — polarization, catalyst,
  astral projection, SMC, density: proposed treatments, **not approved rules**.
* `docs/law_of_one/RULES_INVENTORY.md` — the generated Phase 1 inventory.

**Author slots (do not fill these in)**
* `design/characters/ROOKIE_MEMORIES.md` (#1123) — the protagonist's memories.
* `design/characters/HARRI_ROMPPAINEN.md`, `TOMMY_PILGRIM.md` — character documents.
* `docs/design/AUTHOR_DECISION_QUEUE.md` — where D76–D82 go once decided.

---

## 13. Acceptance trace for #1132

| criterion | where it is met |
| --- | --- |
| one draft outline at a clear path, linked from the index | this file; `README.md` link added |
| four acts, Act III marked as proposal | §3, Act III banner |
| Act I grounded, BCI + psychotronic implant, Kurvi housing, Helsinki life, Maniac comedy | §2.1, §3 Act I, §4 |
| fixed past and open future, memory structure | §2, §5 |
| Act II: StO/StS decision, awakening, bounded PSI, missions beyond Helsinki | §3 Act II, §7, §8 |
| ordinary choices do not determine polarization | §6.2, §8.6 |
| Act IV: Higher Self, expanded PSI, science fantasy/orbital, player-determined ending | §3 Act IV, §10 |
| StO ≠ Confederacy, StS ≠ disagreement, zero-polarization interaction | §10 |
| CWN immutable; Bionics AWN-inspired; PSI focus on projection/telepathy/defence; psychotronics as implants | §8 |
| new rules only as scenes demand; documentation only | §8.1 and the whole document |

**What this document is not:** rules, prose, a scenario tree, or a promise that Act III exists. It is the
outline the author can accept, amend or reject — and the map of what the repository already has when
someone starts building it.
