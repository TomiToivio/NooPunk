# DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED

# NoöPunk Psionics: Conscious Agent Networks and Astral Projection

> **Status: Phase A research + draft (#1137). Nothing here is a rule.** No Python, no rulebook change, no CWN
> modification. Tomi edits, approves or replaces this document; implementation is a separate authorised stage.
> Everything marked **[FICTION]** is invented for 2045 NoöPunk. Everything marked with an evidence tier is a
> claim about the real world, and the tiers are not interchangeable.

## 1. What the author has already decided

Binding source: [`design/BIONICS.md`](../../design/BIONICS.md) (author-authored — preserved, not rewritten).

- **There are three sources of PSI:** latent human genetics (increasingly activating), alien hybridisation, and
  psychotronic technology. "In the past it was maybe one person in a thousand, now it might be one person in
  ten. All hybrids have PSI."
- **Psychotronics always require a human operator** when they are QIP-based, because they amplify natural latent
  PSI rather than generate it. Non-QIP (microwave) devices need no operator but "are not real PSI either".
- **PSI is legal but registered.** Public or commercial use requires registration; unregistered use carries
  sanctions; criminal use goes to the Sörnäinen PSI prison, which is "a very controversial human rights issue".
- **PSI is a service industry** — "fantastic opportunities for a career", in-house corporate psykers, Eurodef and
  Europol recruitment.
- **Consciousness is a quantum phenomenon** in-setting, which is why classical AGI cannot be conscious and every
  AGI goes rogue. That is the metaphysical premise the PSI model must stay consistent with.

## 2. The existing rules this must sit on

| Source | Edition / section | What it gives us | Rights status |
|---|---|---|---|
| **CWN** | Free Edition SRD (CC0) | Action economy, checks, System Strain, Hacking (access/security/detection/countermeasures) | CC0 SRD — immutable, not modified |
| **SWN** | Revised, "Psionics" (printed p. 29 onward) | Discipline/Effort/commitment/Torching **shape** only; no power names or prose | **No verified text licence** — see `docs/licensing`/#569. Shape re-expressed, never copied |
| **AWN** | Mentalist Arts/Effort | Investigative-scale powers — the closest tonal match | **Unverified**; no import |
| **WWN** | Arts / Magic / Workings | Effort economies and Arts structure | CC0 SRD |
| **Repo** | `src/rules/swn_psionics.py`, `src/rules/psionics.py` | Engine exists: Effort, commitment durations, Torching, 20 **original** provisional techniques across six disciplines | Implemented, fidelity unverified by design |

**Do not** combine classes, Effort pools or spell lists. WWN Art Effort and SWN psychic Effort must not share a
pool (`docs/rules/WWN_CWN_COMPATIBILITY.md`). Where a page number cannot be verified, this draft says so rather
than inventing a cost.

## 3. Real-world evidence, and what it is not

| Claim | Tier | Note |
|---|---|---|
| BCI can decode limited intended movement/speech with implanted electrodes | (a) established clinical/research technique | Requires surgery and calibration |
| fMRI can reconstruct aspects of **language meaning** under extensive training and subject cooperation | (b) experimental demonstrator with limitations | Tang et al., *Nature Neuroscience* (2023), issue-provided URL; page resolves, full text paywalled — **re-verify before citing in a rulebook** |
| Focused ultrasound can modulate deep brain regions non-invasively in experimental settings | (b) experimental demonstrator | *Nature Communications* (2025), issue-provided; not read in full |
| Orch-OR / quantum consciousness explains PSI | (c) contested hypothesis | No direct demonstration; `Frontiers in Psychology` (2026) critical review cited by the issue |
| Panpsychic / quantum-information consciousness as the basis of technology | (c) in the real world — **[FICTION]** in 2045 NoöPunk | This is Faggin-inspired setting metaphysics, not engineering |
| Astral projection, telepathy, psychokinesis | (c)/(d) — contested parapsychology, then fiction | **Never presented as experimentally established** |

**Rule for the rulebook:** no false equivalence. A validated BCI and a fictional astral projection are different
kinds of claim and must never share a table row implying equal evidence.

## 4. Design: PSI as access to a Conscious Agent Network **[FICTION]**

The working metaphor is **hacking**, borrowed from CWN's Hacking subsystem, applied to Hoffman-style conscious
agents rather than to computers. The metaphor is a design scaffold, **not** a claim that Hoffman, Lloyd, Faggin or
Ra prescribe exploits.

| Hacking concept (CWN) | PSI analogue | Consequence for play |
|---|---|---|
| Target | Another mind / an information-bearing presence | **Other minds are not insecure computers.** Targeting requires proximity, relationship or a permission |
| Access | Consent, invitation, or an intrusion | Uninvited intrusion is a **rights violation**, detectable, and legally serious in the EU |
| Security | Natural psychic defence, training, psychotronic shielding | Defenders roll; the attacker does not auto-succeed |
| Detection | Psychic signature, physiological tells, device alarms | Every active use leaves a trace |
| Countermeasures | Shielding, dampening, Sörnäinen-style suppression | Institutions can and do answer back |
| Failure | Feedback, nosebleed-level strain, attention drawn | Failure is narrative, never just "nothing happens" |

**Hard boundary, already canon:** PSI must not solve an investigation or reveal essential clues
(`docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`, with 11 tests asserting the resolver has no psychic input).
A telepathic read may produce *catalyst, suspicion or a lead to investigate* — never the core clue.

## 5. Priority order and the active/scripted split

**Active, player-facing (in priority order):**

1. **Astral Projection** — the centrepiece. See §6.
2. **Telepathy** — bounded: surface affect, deliberate sending, and only with consent or an intrusion that can
   fail and be detected. **No mind reading as an interrogation shortcut.**
3. **Psychic Defence** — shielding, spotting intrusion, breaking a link, dampening a room.

**Scripted / GM-only / rare, not a player power tree:** clairvoyance, precognition, mind control, physical
manifestation, probability manipulation, extreme telekinesis. They exist as phenomena and NPC abilities and are
granted by plot, never selected from a list.

## 6. Astral Projection (the centrepiece)

**[FICTION]** grounded in the author's canon that astral existence is socially real, plus Time/Space as a
structured realm (Law of One research, `docs/law_of_one/`), and Gallimore's *Alien Information Theory* as a
**visual/architectural analogy only** — not evidence that DMT transports anyone anywhere.

Draft procedure skeleton (CWN-compatible timing, no new resolution engine):

| Element | Draft |
|---|---|
| **Prerequisite** | A stable meditative practice or a psychotronic aid; the astral body is the green-ray/astral vehicle |
| **Projection** | One scene of preparation, then a **CWN check** against the appropriate ability; failure costs the scene and produces strain, not damage |
| **Anchor** | The physical body must be left safe. An unsafe body is a scene-level threat and the main source of tension |
| **Duration** | Measured in scenes, not minutes. Long excursions cost something on return |
| **Perception** | Partial dual perception (AR-overlay) or immersive traversal — player chooses at projection; the mode cannot change mid-scene |
| **Interaction** | Can observe, be observed, converse, be misled. Cannot manipulate physical matter except through **ectoplasm** (advanced, conditional) |
| **Boundaries** | No omniscient scouting, no oracle answers, no automatic clue discovery. Astral is a place with its own obstacles |
| **Return** | Difficulty scales with depth and interference; a failed return is a scene problem, not a death |
| **Ectoplasm** | Advanced conditional effect: the astral body becomes manifest, is costly, is unmistakable, and is **never** a free combat form |
| **Consent** | Entering another's space or mind without invitation is an intrusion with legal and moral weight |

**Explicitly not included:** an astral combat engine. Conflicts in astral space resolve by the same social and
investigative logic, with CWN checks where a check is genuinely needed.

## 7. Three-stage progression (pre-authored, no power tree)

| Stage | What the character has | What changes |
|---|---|---|
| **Baseline rookie** | Europol BCI plus a **defensive** psychotronic implant | Passive shielding and detection only. No projection, no telepathy |
| **Awakening** | Natural fourth-density awakening (latent genetics, hybrid heritage or an incident) | Bounded active PSI: projection, telepathy, defence. Everything is costly and legible |
| **Revelation** | Higher Self / Wanderer revelation | A **preselected** advanced package, authored per character by the GM — not chosen from a menu |

The player never buys powers. The GM stages what opens and when, and the campaign's reveal ladder gates it.

## 8. Anti-stacking and precedence

- **One effect, three eligibility routes.** Natural, genetically enabled, and psychotronic-assisted PSI reach the
  *same* canonical effect. Never implement the same effect twice.
- **No double charging.** A psychotronic implant that enables a technique does not also cost a second resource for
  "using the implant".
- **Device vs natural:** an implant either *enables* a specific technique (the character could not do it
  unaided) or *boosts* one they already have — state which, per device, at authoring time. Not both.
- **Effort pools never merge** across SWN-shape psychic Effort, WWN Art Effort and any NoöPunk resource.

## 9. Python model and interface (design only)

```python
# proposed, NOT implemented — Phase C at the earliest
@dataclass(frozen=True)
class PsiUser:
    sources: frozenset[str]        # {"latent", "hybrid", "psychotronic"}
    stage: str                     # "baseline" | "awakened" | "revealed"
    effort: EffortState            # reuses the existing swn_psionics engine

def project(actor: PsiUser, *, mode: str, anchor: Anchor) -> ProjectionResult: ...
def intrude(attacker: PsiUser, defender: PsiUser, *, consent: bool) -> IntrusionResult: ...
```

Rules: pure functions, no engine dependency, plain-data state, and a **legibility requirement** — every result
must be explainable at a table in one sentence. It should call the existing psionics engine for Effort rather
than reimplementing it.

## 10. Open decisions for Tomi

1. Does the rookie's baseline implant allow **any** active PSI, or strictly passive defence?
2. Is telepathy consent-only, or can uninvited reading happen and simply be detected, illegal and risky?
3. Should astral projection be available at awakening, or only after the first revelation?
4. Does the awakening happen to the PC on-screen, or before play as part of the authored template?
5. Sörnäinen and PSI registration are strong material — do they enter the first campaign as background, or as a
   scenario the player actually touches?
6. How visible should PSI use be to bystanders? (This determines whether the PSI Service Industry feels like
   *Ubik* or like a covert trade.)

## 11. Bibliography

- Author: `design/BIONICS.md` (NoöPunk repo).
- CWN Free Edition SRD (CC0), Hacking and combat sections.
- SWN Revised, "Psionics", printed p. 29 onward — **shape only; no text licence; not reproduced**.
- WWN SRD (CC0), Arts/Effort; AWN Mentalist (unverified, no import).
- Seth Lloyd, *Programming the Universe* (2006); "The Universe as Quantum Computer", arXiv:1312.4455.
- Penrose & Hameroff, Orch-OR papers — to be located at primary source, plus current critical appraisal.
- Federico Faggin, quantum-information consciousness — **retrieve first-party publications before assigning claims**.
- Donald Hoffman, conscious realism — Quanta interview (2016) as introduction; seek the mathematical papers.
- Dean Radin, PSI and magick — primary publications plus replication critiques; **not** treated as established.
- Andrew Gallimore, *Alien Information Theory* (2019) — visual/worldbuilding analogy only.
- Philip K. Dick, *Ubik* (1969) — commercial-PSI tone, fiction.
- Tang et al., *Nature Neuroscience* (2023), s41593-023-01304-9 — tier (b), paywalled, re-verify.
- *Nature Communications* (2025), s41467-025-63020-1 (tFUS) — tier (b), not read in full.
- *Frontiers in Psychology* (2026) critical review of quantum consciousness theories — tier (c).
- Law of One: `docs/law_of_one/` (Time/Space, energy centres, astral body); lawofone.info categories.
- Internal: `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md`, `docs/rules/WWN_CWN_COMPATIBILITY.md`,
  `src/rules/swn_psionics.py`, `src/rules/psionics.py`.
