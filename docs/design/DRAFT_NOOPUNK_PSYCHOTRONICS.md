# DRAFT — NoöPunk Psychotronics: QIP devices, neurotechnology, and institutional coercion

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED**
>
> Phase A of [#1137](https://github.com/TomiToivio/NooPunk/issues/1137). Proposal only: no Python, no rulebook
> chapter, no equipment entry, no CWN change. The author owns the canon; this file exists to be edited or
> rejected.
>
> Companion drafts: [Psionics](DRAFT_NOOPUNK_PSIONICS.md) · [Bionics](DRAFT_NOOPUNK_BIONICS.md) ·
> [Europol rookie](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md) ·
> [Tags](DRAFT_NOOPUNK_CHARACTER_TAGS.md). Cross-document map: see the issue.

**Evidence key:** **[a]** established clinical technique · **[b]** experimental demonstrator with limits ·
**[c]** contested hypothesis · **[d]** NoöPunk fiction. Everything below is **[d]** unless tagged.

---

## 1. What the author already decided

From [`design/BIONICS.md`](../../design/BIONICS.md) — this is author text, not agent invention:

* Psychotronics **boost the natural latent PSI ability** of human consciousness, which is **why QIP
  psychotronic technology always requires a human operator**.
* They are installed as **cybernetic implants** *or* exist as an **external device requiring an operator**.
* **Some psychotronic devices are not QIP**: they are based on **microwave radiation**, need no operator, and
  **are not real PSI**. Crucially: *"Psychotronics based on microwave radiation or other non-QIP technology
  cannot be installed as cybernetic augmentations: they would fry your meat."*
* QIP is also the basis for **experimental mind uploading and resleeving** — rare, controlled, and not
  Eclipse-Phase-ubiquitous.
* The **Europol rookie's default kit** includes a BCI and a **basic defensive psychotronic implant**.

From [#1137](https://github.com/TomiToivio/NooPunk/issues/1137) §2, the required split:

1. **QIP-based psychotronics [d]** — amplifies or mediates natural PSI; requires a conscious operator.
2. **Non-QIP neurotechnology [b]** — BCI, EEG/fMRI decoding, neurofeedback, stimulation, drugs, priming,
   propaganda. **No operator with PSI needed, and no claim of paranormal effect.**
3. **Institutional coercion / counterintelligence [d, historical]** — MKULTRA-shaped programmes, absurd helmets,
   flashing-light laboratories, media campaigns, interrogation psychology. Modelled as **investigation, ethics,
   consent and exposure**, never as an operating manual.

---

## 2. Existing rules: what psychotronics must attach to

| anchor | exact source | what it already gives us |
|---|---|---|
| **CWN cyberware** | SRD §Cyberware; `src/rules/cwn_cyberware.py` — `surgery_check_modifier`, `installation_cost`, `complication`, `removal_terms`, `resolve_brutal_removal` | installation as a surgical procedure with cost, difficulty, complications and removal terms. **Psychotronic implants are cyberware and pay these costs.** |
| **CWN System Strain** | `src/rules/cwn_strain.py` — `SystemStrain` | the body's tolerance budget. **This is the only implant resource**; psychotronics do not add a second one. |
| **CWN equipment / ownership** | `src/rules/cwn_equipment.py`, `data/rules/cwn_equipment.json`, `cwn_catalogue.json` | cost, encumbrance, legality of possession |
| **CWN Hacking grammar** | `src/rules/cwn_hacking.py` — access pool, security difficulty, alert clock | the **access → permission → contested check → detection** shape a networked device must respect |
| **NoöPunk tags** | `data/rules/noopunk_tags.json` — kinds `attribute/skill/status/other`, fields incl. `duration`, `source`, `stacking` | device conditions are **status tags**, not new statistics |
| **CWN core immutability** | [`CWN_IMMUTABLE_CORE_1068.md`](../rules/CWN_IMMUTABLE_CORE_1068.md) | psychotronics is an **additive mod**; it may never shadow a CWN outcome |

**Gap that this draft has to fill:** CWN has no concept of a *device that changes what a mind can do*. It has
tools that add a bonus and cyberware that costs strain. Psychotronics needs a third thing: **an enabler with a
reliability state**. That is the whole mechanical invention here — one state, not a power list.

---

## 3. What the real world supports, and what it does not

| claim | tier | source (date) | limit that shapes the design |
|---|---|---|---|
| Implanted BCIs restore communication in paralysis | **[a]** | clinical trials: BrainGate/UC Davis speech neuroprosthesis (*NEJM* 2021); Neuralink PRIME (NCT06429735); Synchron COMMAND | requires surgery, a trained decoder, a cooperative user, and months of calibration |
| **Inner speech** can be decoded from motor cortex | **[b]** | Kunz et al., *Cell* 188(17):4658–4673 (Aug 2025) | the same work shows **simple mental strategies prevent decoding** — the wearer can defend private thought |
| Semantic decoding from **fMRI** | **[b]** | Tang et al., *Nat. Neurosci.* 26:858–866 (2023) | subject-specific model, cooperative attention, **gist not verbatim**; scanner-grade hardware |
| Precise **non-invasive deep** neuromodulation | **[b]** | *Nat. Commun.* (Sep 2025) — 256-element 555 kHz array + real-time fMRI | laboratory system, individualised planning, one circuit at a time |
| Neuromodulation changes **valuation**, not commands | **[b]** | *Nat. Commun.* (2025) — nucleus accumbens TUS, d≈0.5–0.7 | a nudge with a measurable effect, not obedience |
| Consumer EEG "mind reading" | **not established [c]** | — | EEG is a noisy scalp average; it supports attention/SSVEP-class interfaces, not thought transcription |
| A helmet that reads minds at range | **fiction [d]** | — | NoöPunk keeps it as **aesthetic and institutional menace**, and the book should say so |

**The engineering rule this produces:** in 2045 a device may be *very good at one narrow thing* (a decoder for
one person's attempted speech; a stimulus aimed at one circuit) and *useless at everything else*. Unrestricted
thought extraction is not a technology that exists in the setting's own physics — the setting's QIP doctrine
explains why (consciousness is not classical computation, so a classical machine cannot host or read it).

---

## 4. The three categories, as three different kinds of object

### 4.1 QIP psychotronics [d] — the enabler

| property | draft |
|---|---|
| **Requires** | a conscious operator with the latent ability, and a device |
| **Form** | cybernetic implant (pays CWN surgery + System Strain) or external device (bulky, obvious, needs a hand) |
| **Effect** | it does not *grant* a power; it **lowers the requirement** for an effect the operator is eligible for, by one step, at a stated cost |
| **State** | `reliability`: calibrated / drifting / failed — a status tag, checked when the fiction makes it interesting |
| **Why it can fail** | the operator's state matters: fear, exhaustion and pain all push it toward "drifting" |
| **Cost** | implant: System Strain at installation, then a **condition tag** per significant use. External: a scene action to set up, and it cannot be used while moving |

**Anti-double-charge (binding for Phase B):** a QIP device spend is **not** a psi spend. If the operator pays a
condition for the effect, the device does not also charge; if the device charges, the operator pays nothing extra.
One effect, one payer — the same rule as the psionics draft.

### 4.2 Non-QIP neurotechnology [b] — the honest machine

| property | draft |
|---|---|
| Requires | an operator trained in its use, but **no PSI** |
| Form | clinical stimulation array, BCI, drug regimen, priming protocol, media campaign |
| What it does | **exactly what the evidence says**: it decodes what a cooperating person attempts to say; it shifts arousal, valuation or attention; it makes a message easier to believe by repeating it |
| What it never does | read an unwilling mind, compel a specific act, or detect a lie reliably |
| Mechanical shape | CWN skill checks with equipment bonuses; **no psi tags at all** |
| Cost | infrastructure, consent, calibration time, and legal exposure — not "charges" |

This category is the one that keeps the setting honest. A hospital's stimulation suite and a police interview
room are **the same technology** with different legal cover, and that is a better horror than a magic helmet.

### 4.3 Institutional coercion [d] — the investigation

MKULTRA-shaped programmes are **backstory and case material**: a leaked procurement file, a ward of patients, a
media campaign that worked. They are modelled as **scenes with evidence, consent problems and consequences**:

* a clue that can only be obtained by reading a programme's files;
* a rights violation that makes the obtained evidence inadmissible, or the case political;
* a victim who is a witness, not a monster;
* an institution that will protect itself.

**No procedure for coercing a person is written here, and none should be.** The game's interest is the exposure.

---

## 5. Draft device catalogue (tags, not stat blocks)

Five device *kinds*, deliberately small. Prices are **omitted on purpose**: CWN prices exist and no invented
number may contradict them ([author approval gate](../../AGENTS.md)).

| device | category | what it enables | state tags | notes |
|---|---|---|---|---|
| **Defensive screen implant** (issued kit) | QIP implant | resists an incoming psychic effect; grants the defence check a second attempt at a cost | `calibrated` → `drifting` after a hard failure | the rookie's default; cannot attack, cannot sense |
| **Field amplifier** (external) | QIP external | lowers the requirement for one already-eligible effect, once per scene | `warm`, `obvious`, `needs-setup` | looks like a 2040s radio direction-finder; cannot be carried discreetly |
| **Clinical decoder suite** | non-QIP | decodes a *cooperating* subject's attempted speech over hours | `calibrated`, `subject-trained` | hospital, not field; a warrant or consent scene |
| **Stimulation array** | non-QIP | shifts arousal/valuation for a scene; a nudge with a stated direction | `charging`, `loud` | needs a room, a technician and a legal basis |
| **"Insight helmet"** | pseudo-QIP, **fraud** | nothing. It is a prop used to frighten detainees | — | the setting's best joke and its worst abuse; **explicitly non-functional** |

The last row is deliberate: a game about institutions needs a fake device, because institutions buy fake devices.

---

## 6. Reliability, calibration, privacy and countermeasures — the four tags

Rather than an energy economy, four words do the work. Each is a **status tag** with a duration and a source.

1. **reliability** — `calibrated / drifting / failed`. Drift is the interesting state: it still works, but the GM
   decides *what* it does. Repair is a scene with a technician.
2. **calibration** — a device tuned to *one* person. Using it on another imposes a penalty stated before the roll,
   or simply does not work. This is the strongest anti-abuse lever in the draft.
3. **privacy** — a device that reads or records creates a **record**. In a police setting a record is evidence,
   and evidence has rules: chain of custody, admissibility, the subject's rights. A psychotronic recording is
   *not* automatically usable in court, and that is a plot engine.
4. **countermeasure** — the target's defence: a Faraday layer, a jammer, a mental discipline, or simply refusing
   to cooperate (the *Cell* 2025 result: private thought is defensible).

**No energy economy.** A charge counter invites resource management as the core loop. These four tags produce
scenes instead.

---

## 7. Two tabletop examples

**Example A — the ward.**
A clinic's decoder suite could confirm what a comatose witness was trying to say. It requires: consent or a
court order, twelve hours, a trained technician, and a subject who is trying. The player who wants the answer
fast must obtain the **authority**, not roll well. Meanwhile the same suite, used without consent, is the
crime the case is about.

**Example B — the drifting implant.**
The rookie's issued implant has been through two fights and is `drifting`. In the stairwell, when the hostile
psychic pushes, the GM asks her to roll — and states the cost first: *"on a failure the screen holds, but it
takes your hearing for the scene."* On an 8, it holds. She cannot hear the partner calling her name, and the
scene's tension becomes a physical fact rather than a number.

---

## 8. Python model / interface proposal (design only — Phase B)

```
src/rules/noopunk_psychotronics.py
    @dataclass Device(kind: str, category: str, reliability: str, calibrated_to: str | None)
    def enable_effect(*, device: Device, operator_eligible: bool, effect: str) -> Outcome
        # returns allowed/refused-with-reason; never rolls
    def device_condition(*, device: Device, hard_failure: bool) -> str
    def privacy_record(*, device: Device, lawful_basis: str | None) -> dict
    def legal_admissibility(*, record: dict, jurisdiction: str) -> bool
```

Constraints:

* **No new resolution.** `enable_effect` answers a permission question; the check itself is CWN's.
* **No second cost.** If the effect costs a condition, the device does not also charge strain, and vice versa —
  a test must assert the single-payer rule both ways.
* `privacy_record` exists so that "we recorded it" is a **data object** the investigation layer can refuse.
  This is the one place where psychotronics may touch investigation — as evidence with provenance, never as a
  clue dispenser.

---

## 9. Interaction and precedence

| with | rule |
|---|---|
| **CWN cyberware** | implants are cyberware: surgery, cost, strain, complications, removal. No exceptions. |
| **Psionics** | a device **enables**, never grants. It may lower a requirement by one step; it may never create a second Telepathy. |
| **Bionics** | a bionic modification is biology and does not need a device; a hybrid's ability is not psychotronic. Different fiction, different failure modes. |
| **Investigation** | a recording is evidence with provenance, admissibility and a chain of custody. Psi still grants no clues. |
| **Tags** | all four device words are status tags. No new stat, no charge track. |
| **Acts** | I: issued defensive implant only. II: external amplifier appears in the conspiracy. III: clinical suites and programmes become case material. IV: QIP's deeper uses (uploading, resleeving) are *mentioned*, not playable. |

---

## 10. Open decisions for Tomi

1. **Is the defensive implant QIP or plain CWN cyberware?** The campaign doc says equipment; if it is QIP it needs
   an operator-sense, which a rookie does not have.
2. **Reliability as a tag or as a real clock?** Tags are cheap and story-first; a clock is more predictable.
3. **Does a psychotronic record ever count as evidence?** If yes, under what authority, and who can suppress it?
4. **How visible is a field amplifier?** "Obvious" is the anti-abuse lever; make it as obvious as you want.
5. **Are non-QIP devices regulated at all**, or is that the point — that the boring technology is unregulated?
6. **The fraud helmet:** keep it as satire, or is it too close to something you would rather not depict?
7. **Uploading/resleeving:** name it in the setting bible only, or allow a late-campaign scene?

---

## 11. Bibliography (checked in this pass)

| source | date | status |
|---|---|---|
| Kunz et al., *Cell* 188(17):4658–4673 — inner speech, and its defensibility | Aug 2025 | open access, confirmed |
| Tang et al., *Nat. Neurosci.* 26:858–866 | 2023 | confirmed; paywalled body |
| *Nat. Commun.* — 256-element TUS, deep circuits | Sep 2025 | abstract confirmed |
| *Nat. Commun.* — TUS of nucleus accumbens, reward sensitivity | 2025 | results confirmed |
| Clinical BCI trials: NCT06429735 (PRIME), Synchron COMMAND | 2024–2026 | registrations confirmed; outcomes not independently verified here |
| CWN cyberware / strain / hacking — `src/rules/cwn_cyberware.py`, `cwn_strain.py`, `cwn_hacking.py` | repo, current `main` | symbols verified by reading the modules |
| MKULTRA historical record | 1950s–1970s, declassified | treated as **history and case material**, not as procedure |
