# NoöPunk Psychotronics: QIP Implants, Neurotechnology and Counterintelligence

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** Issue [#1137](https://github.com/TomiToivio/NooPunk/issues/1137); researched 2026-11-04. Planning only; do not implement, modify the CWN core, or copy a published ruleset. **Evidence labels:** [E] empirical/approved; [X] experimental; [H] contested theory or parapsychology; [F] fictional 2045 premise; [P] draft mechanics. Tomi edits this proposal first, then separately authorizes matching tabletop and Python implementation.

## Preflight: what already exists for this subsystem

- **Author canon — binding:** [`design/BIONICS.md`](../../design/BIONICS.md) — QIP devices require a human
  operator; non-QIP devices cannot be installed as cyberware ("they would fry your meat"); uploading and resleeving
  are the QIP-adjacent experimental technologies.
- **Cyberware base:** `src/rules/cwn_cyberware.py` and `data/rules/cwn_*.json` — the implant economy this must
  extend. CWN is immutable.
- **Cost source:** `src/rules/swn_psionics.py` — a QIP device spends the **operator's** Effort. It never adds a
  second resource, and a device with no operator produces no PSI at all.

## Author's dual definition, preserved
**[F] Quantum Information Panpsychism (QIP) devices** amplify/interact with conscious-agent PSI and **always need a conscious operator**. In 2045 these can be external apparatus or miniature neurocybernetic implants. **Non-QIP psychotronics** refers in-setting to conventional neuroscience, electromagnetic/sensory stimulation, pharmaceuticals, media manipulation, conditioning and psychological operations. These need *not* involve a psychic operator and must **not** acquire the benefits of real PSI by name alone. The author's [BIONICS.md](../../design/BIONICS.md) additionally distinguishes some dangerous large electromagnetic apparatus from implantable safe QIP designs.

## Technology reality check (reviewed 2026-11-04)
| Tier | 2026 status and source | 2045 portrayal and limit |
|---|---|---|
| [E/X] Implanted neural speech interfaces | Wairagkar et al., *Nature* (2025), https://www.nature.com/articles/s41586-025-09127-3 : 256 implanted electrodes enabled near-real-time speech synthesis for one participant with ALS | Common consumer BCIs **[F]** remain extrapolation; implantation/calibration/privacy/security matter |
| [X] fMRI semantic decoding | Tang et al., *Nature Neuroscience* (2023), https://www.nature.com/articles/s41593-023-01304-9 : semantic gist reconstruction after many hours' individual training, requires cooperation; scanner infrastructure | Mind reading helmet as bulky, limited, probabilistic, often comically overpromised; no universal thought extraction |
| [X] Noninvasive brain stimulation | TMS/tES and focused ultrasound have clinically investigated effects; effects depend on technique, location and population. Clinical/regulatory claims require specific device approval, not generalized mind control | Nerve stimulation, attention/feedback, side effects and consent; realistic labs and failed calibrations |
| [E] Psychoactive drugs and psychological influence | Drugs can alter mood/perception; persuasion and information influence exist; **no validated chemical or flashing-light protocol for guaranteed obedience** | Treat MKULTRA-style coercion as abusive clandestine experimentation and plot, not an operational recipe |
| [H/F] QIP-consciousness amplification | Faggin/D'Ariano consciousness interpretation is contested and not a demonstrated PSI engineering discipline; first-party discussion https://www.youtube.com/watch?v=0FUFewGHLLg | Licensed fictional QIP implant that amplifies an operator's latent PSI; **never claim scientifically proven in 2026** |

## Device families: proposal
| Family | Operator | Effect contract | Gameplay interface |
|---|---|---|---|
| Standard Europol BCI | Human operator for ordinary usage; software signal processing | Ordinary communications, ID, hands-free UI, controlled data exchange | Existing CWN cyberware, hacking/communications; not inherently telepathic |
| **Defensive QIP implant** (rookie standard) | **Conscious operator mandatory** | One *specified* bounded defensive PSI technique, not general mindreading | Implant is permission/source; SWN-compatible PSI effect uses **one** cost/activation, plus CWN cyberware constraints |
| External QIP "helmet" | Conscious operator | Larger calibration apparatus, possible limited remote noetic contact under authorized conditions | Equipment/item with duration, setup, traceability, power supply, constraints |
| fMRI/EEG brain decoding lab | Cooperative subject/recording setup, technicians or automation; no psychic required | Decoding constrained learned signals or semantic patterns | Tech/medical access and forensic uncertainty; **not** supernatural Telepathy |
| TMS/tES/ultrasound neurostimulator | No psychic operator required; trained professional and equipment | Bounded neurophysiological effects, possible adverse reactions | Treatment/exposure tags, clinical oversight, ordinary saves when appropriate |
| Memetic/subliminal propaganda platform | Humans/automation, no QIP | Influence and incentives with imperfect, socially mediated outcomes | CWN Talk/Connect/Program, social/reputation tags; not deterministic mind control |
| Historical-style MKULTRA lab | Characters/operators as NPC institutions | Misuse of sensory tech/drugs/psychology, contested files and scandals | Investigation, civil liberties, secrecy, institutional fallout, **no coercive real-world instructions** |

**Aesthetic note [F]:** ridiculous mind-reading helmets, cabling, flickering lights, clinical chaperones, archival tape labels and propaganda presentations; the **technology is functional only to its limited written effect**. A comic device may be powerful inside the story without claiming magical reliability. Consumer BCI is visually seamless while elite labs can still be embarrassingly theatrical.

## Rules proposal [P]
1. **Ownership**: BCI and defensive implant are employer-issued. Track `asset_id,owner,calibration,availability,licence,maintenance,operator`; a housing contract is not an implant stat.
2. **Cyberware baseline:** installation, damage and System Strain governed only by CWN where applicable. No second implant strain pool.
3. **QIP enablement:** implant grants **access to** a pre-authored PSI defence under a named device limit. The *same PSI effect resolver* serves natural awakened PSI later. Once advanced, choose device-assisted or innate version; **not automatic double protection**.
4. **Non-QIP interfaces:** an fMRI scan is a medical/forensic check, not a telepathic ability. Calibration, cooperation, consent and legal warrant matter. Strong claims must have evidence quality tags.
5. **Failure modes:** `Needs Calibration`, `Signal Artifact`, `Operator Fatigue`, `Consent Withdrawn`, `Compromised Firmware`, `Unlicensed Use`, `Psychic Interference` (QIP only). Prefer tags and existing saves/checks to another resource economy.
6. **Legal/ethics:** EU/Europol psychics registration, privacy and Finnish enforcement competence per existing setting. Coercive research raises rights issues and evidence-admissibility questions. A scanner output is not proof of alien identity.
7. **Countermeasures:** ordinary infosec for BCI firmware, mundane shielding/clinical review for neuro devices, PSI-specific defence for a **QIP psychic intrusion** only; do not treat jamming a radio as automatically blocking an astral mind.

### Small tabletop scenario
Europol rookie's issued defensive implant warns of a suspected QIP contact during an interview. The PC decides to activate their **one authorized defence**. Whether the witness is lying still requires normal investigation. A lab later identifies an ordinary BCI artifact from a previous firmware upgrade, raising a false positive and a privacy complaint. The scene can be run with CWN + one defined implant response + `Suspected Intrusion` tag, no mind-reading system.

### Interfaces for eventual code (not implementation)
`PsychotronicDevice{id,category:qip|neural|social,implant:boolean,operator_required,psi_effect_id?,source,licence,owner,calibration,tags}`; commands `is_available`, `enable_psi`, `calibrate`, `log_use`, `remove`. Integrates CWN cyberware/System Strain and single shared PSI effect definition.

### Alternatives and open decisions
- How small and safe are 2045 consumer BCIs versus clinical implants? Author to decide; clinical evidence **does not imply** mobile-phone prevalence in 2026.
- Starting implant: passive warning only, reactive shield, or actively sustained defence? Prefer a *bounded reactive shield* for playable scenarios, but cost/timing undecided.
- May firmware hacking disable the defensive implant? Only if a named scenario and an authorized CWN infosec mechanic justify it; do not make all implanted PSI network-addressable by default.
- Is psychotronic supply a public utility, corporate subscription, or Europol-controlled privilege? *Ubik*-style billing and service industry is a strong narrative hook.
- How to model cyberware System Strain under AWN disaster survival; do not introduce duplicate System Strain.

**Next gate:** Tomi edits. Approved design later updates tabletop rules, Python and tests, not in this draft phase.
