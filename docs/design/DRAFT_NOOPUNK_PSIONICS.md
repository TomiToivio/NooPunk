> **Superseded-by [#1178](https://github.com/TomiToivio/NooPunk/issues/1178) on player access.**
> A player character may select only **Telepathy** and **Telekinesis** from the SWN disciplines.
> **Astral Projection is scripted** (OOBE, NDE, psychotronic event), not a playable technique.
> **Psychic Defence is not a SWN discipline**: as a player-facing ability it belongs to the
> psychotronic implant's equipment rules or to a scripted event, not to a discipline tree.
> The rest of this file remains the historical research record for the PSI slice.
> Current policy: [`docs/rules/PSI_ACCESS_1178.md`](../rules/PSI_ACCESS_1178.md).

# NoöPunk Psionics: Conscious-Agent-Network and Astral Rules

> **Partially superseded by [#1178](https://github.com/TomiToivio/NooPunk/issues/1178) (2026-11-05).**
> Player-selectable SWN powers are **Telepathy and Telekinesis only**; Astral Projection is
> **scripted** (sleeping OOBE, NDE, Monroe-style technology), and the Astral Graph is deferred.
> The historical projection loop below is not current player-rule authority.

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** Issue [#1137](https://github.com/TomiToivio/NooPunk/issues/1137); researched 2026-11-04. Planning only; do not implement, modify the CWN core, or copy a published ruleset. **Evidence labels:** [E] empirical/approved; [X] experimental; [H] contested theory or parapsychology; [F] fictional 2045 premise; [P] draft mechanics. Tomi edits this proposal first, then separately authorizes matching tabletop and Python implementation.

## Preflight: what already exists for this subsystem

- **Author canon — binding:** [`design/BIONICS.md`](../../design/BIONICS.md) fixes **three** PSI sources (latent
  human genetics, alien hybridisation, psychotronic technology), states that QIP psychotronics **always require a
  conscious human operator**, that non-QIP (microwave) devices "are not real PSI either", and sets the registration
  law and the Sörnäinen prison. Where this draft and that file could be read differently, that file wins; the
  disagreement is a question for the author, not a rewrite.
- **Engine — extend, do not rebuild:** `src/rules/swn_psionics.py` and `src/rules/psionics.py` already implement
  Effort accounting, commitment durations and Torching, with 20 **original** provisional techniques. A new PSI
  resolver would be a second engine.
- **Hard boundary:** `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md` — PSI must not deliver core clues; 11 tests
  assert the investigation resolver has no psychic input.

## Design decision in one sentence
**[P]** Treat **PSI and magick as one underlying fictional consciousness-mediated phenomenon** with different learned practices, while **CWN handles action resolution**. Start with **three pre-authored playable abilities: Astral Projection, bounded Telepathy, and Psychic Defence**. Never add a second general skill system; everything else is introduced only for a scene that can actually adjudicate it.

## Source and evidence ledger
| Source | What it contributes | What it does NOT establish |
|---|---|---|
| Seth Lloyd, *The Universe as Quantum Computer* (2012/2013) [H in this synthesis] | Quantum-information ontology and computational vocabulary; [P] fictional network topology | Real-world proof of controllable PSI or remotely hackable consciousness |
| Penrose & Hameroff, *Consciousness in the Universe* (2014) [H] | Orch-OR microtubule hypothesis and discrete events | Established neural mechanism for telepathy/astral projection; biological feasibility contested |
| Faggin & D'Ariano, QIP/consciousness interpretation [H] | Conscious quantum entities and irreducible subjective experience, fictional operator gating | Reproducibly demonstrated paranormal engineering |
| Donald Hoffman, conscious-agent formalism [H] | Conscious agent networks; perceptual interface rather than ultimate reality | Demonstration that ordinary cyberspace is literally an astral network |
| Dean Radin, PSI/magick proposals [H] | Ritual, intention and PSI as potentially related in-universe traditions | Mainstream-accepted repeatable proof of magick/telepathy |
| Law of One [F] | Density, veiling, Time/Space, Wanderer, Higher Self, SMC and free will | Scientific data; the source's categories remain distinguishable from proposed rules |
| Andrew Gallimore, *Alien Information Theory* (2019) [F aesthetics/H interpretation] | Hyperdimensional-feeling, DMT-inspired interactive alien architecture | Established externally existing DMT realm |
| Philip K. Dick, *Ubik* [F] | Bureaucratic PSI contractors, everyday consumer psychic countermeasures, absurd corporate fees | Actual commercial PSI industry |

Research references: Lloyd https://arxiv.org/abs/1312.4455 ; Orch-OR https://pubmed.ncbi.nlm.nih.gov/24070914/ ; critical assessment https://pubmed.ncbi.nlm.nih.gov/19792156/ ; Hoffman https://www.quantamagazine.org/the-evolutionary-argument-against-reality-20160421/ ; Faggin interview linked to D'Ariano paper https://www.youtube.com/watch?v=0FUFewGHLLg ; Law of One https://www.lawofone.info/categories.php ; Gallimore (bibliography) https://search.worldcat.org/search?q=Andrew+Gallimore+Alien+Information+Theory . **Check primary Radin studies and independent replication reviews before making empirical claims; here PSI remains [H]/[F].**

## Published RPG comparison and reuse
| Rule family | Reusable procedure | Limitation / adaptation |
|---|---|---|
| **CWN** | Unmodified skills, saves, action timing, hacking, combat and damage | Network hacking is a **metaphor and design template**, not literal reuse of software devices for minds. No ability silently patches CWN hacking. |
| **SWN Revised Psychic** | Telepathy, Metapsionics, Effort and relevant defensive gating | Some techniques too strong for a clue-based campaign; no freely selected broad powers. Source book/source edition must be verified before numbers. |
| **AWN Deluxe Mentalist**, pp.264–269 | Mentalism, lesser/greater Arts, bounded Effort and subtler psychic domains; especially Mindreading, Clairvoyance, Psychokinesis and Body Control | This is an **alternative package**, not a free add-on to SWN Psychic, and some Arts still break investigation if unrestricted. |
| **WWN Magic/Arts/Workings** | Ritual duration, preparation, lasting effects and costs | Magick/PSI ontology may coincide, but no simultaneous separate WWN spellbook + SWN psychic free progression. |

**[P] Best integration:** reuse selected SWN Psychic **effects/contracts** when directly appropriate; use the *scale and scene-safety* of AWN Mentalist as a design benchmark; model specifically needed magick rituals with a single compatible WWN Workings-style procedure. Commit to **one power eligibility + one cost source per activation**. Cross-check `docs/rules/PSI_INVESTIGATION_BOUNDARY_1105.md` before approval: PSI cannot automatically deliver core clues or bypass competence, access and inquiry.

## Three layers of experienced reality
- **Physical:** embodied material events governed by CWN. Ordinary witnesses can see physically embodied fourth-density beings. Astral entities need actual manifestation to act physically.
- **Cyber:** information overlays, BCI data, security and software, governed by CWN hacking. These are *machines*, not souls.
- **Astral / Time-Space:** [F] an additional conscious-agent experiential layer. **AR-overlay mode** perceives astral information while embodied; **VR-like projection mode** enters a disembodied perspective while the body remains anchored. Neither mode is simply software. Distinguish astral realm, body state, density and visibility.

**[P] Hacking vocabulary only:** access = attunement/relationship/consented opening; authentication = focused intention/identity; scan = limited perception; firewall = Psychic Defence, shielding or boundaries; trace = reciprocal awareness; exploit = dangerous violation with strong consequences, **not automatically possible against another will**. No operational instructions for manipulating real people.

## Core play loop: Astral Projection (highest priority)
**[P] Permission and entry.** Requires an authored unlocked Attunement/ability, a declared intention, a prepared or stable physical anchor, an accessible target plane/location and a recognized entry condition. An ordinary third-density dream/NDE may involve involuntary projection **[F]**, but does not confer controlled travel.

1. **Enter:** mark `astral_state=projected`, `body_anchor=<location>`, `realm=<named region>`; commit the designated PSI Effort *or* approved Chakra pool cost, **not both**. Entry follows specified CWN timing after rules approval.
2. **Orient:** choose an authorized path; information available is bounded by the place and guide, not omniscience. A projected agent does **not** automatically view classified files or an inaccessible person's private memory.
3. **Interact:** communicate, investigate, bargain, navigate; CWN checks and saves are used only where appropriate. A narrative tag tracks `Anchor Strained`, `Intrusive Presence`, `Misread Symbol` or `Consent Withdrawn`.
4. **Countermeasures:** Psychic Defence, personal boundaries and hostile astral conditions can resist; a successful intrusion may impose a narrative consequence but not override all NPC autonomy.
5. **Return:** defined exit action/trigger; restore embodied perspective, resolve consequences and release committed resources per the approved cost contract. Provide recovery route if disrupted; no indefinite GM-imposed captivity.
6. **Manifestation:** separate rare advanced permission/ability to produce ectoplasmic or physical interaction. Astral perspective alone cannot attack physical targets or bypass physical locks.

**Visual brief [F/P]:** nested impossible architecture, self-reorganizing glyphs, informational beings, hyper-saturated DMT-like geometry and world semantics conveyed as experiential patterns. Retain a few stable landmarks and interface cues so players can actually navigate. Do not portray real DMT experiences as proof of these realms.

## Other active capabilities (bounded)
| Ability | [P] first power | Defensive limits and story contract |
|---|---|---|
| Telepathy | Consent-based affect/short-message link with named target, within authored conditions | No blanket read-any-mind, secret extraction, effortless detection of lies or guaranteed clue acquisition; resistance and social consequences |
| Psychic Defence | Respond to a specified intrusion/hostile psychic effect; negate or reduce *that* effect | Limits per scene/available resources, no perpetual immunity, avoid stacking baseline implant and innate effect without a defined choice |
| Astral Projection | Narrow named-region projection; advanced breadth after Higher Self | Anchor/realm/return always tracked |
| Magick | Specific authored ritual = PSI through intention, symbols and practice | WWN-style costs/duration when needed; no extra spell system |

**Scripted-only by default:** higher-self revelations, precognition, planetary SMC insights, involuntary dreams/NDEs, reality-bending, mass mind control, broad probability editing, scene-breaking remote viewing. No active omniscient power button.

## Campaign staging and example
| Act | Status |
|---|---|
| I | Defensive **implant-mediated** PSI only; natural powers not unlocked; ordinary dreams scripted |
| II | A pre-authored natural Telepathy/Defence unlock after fourth-density awakening, not a player-selected skill tree |
| III (proposal) | First controlled, **bounded Astral Projection** with a physical anchor; first full astral rules slice |
| IV | Higher Self revelation, Wanderer identity and pre-authored stronger projection/telepathy/defence; exact pre-incarnate service revealed **only in finale** |

**Tabletop example [P]:** in Act III, the rookie enters a supervised projection from a clinic. The assigned astral destination is an echo of a station platform. The player can ask the guide a question, investigate symbolic signage, or return. The scene grants one scheduled memory fragment regardless of skill checks; an optional CWN inquiry determines which context clue is recognized. A hostile entity attempts a contact: use the approved Psychic Defence once, record `Anchor Strained` on a failure, then resolve a safe return. No secret real-world case facts can be taken by arbitrary astral reading.

## Proposed implementation interface (NOT CODE)
`PsiAbility{id,source,unlock_act,prerequisites,activation,resource_owner,cost,duration,targets,restrictions,scripted_only,provenance}`; `AstralState{embodied|overlay|projected|manifesting,anchor,realm,entry,exit,consequences}`; commands `can_activate`, `commit/release`, `enter/return`, `defend`, `emit_scene_event`. All delegate ordinary rolls to CWN; no psychic hook inside the investigation resolver.

## Alternatives and author decision queue
1. Prefer **SWN Psychic with AWN Mentalist design constraints**, or select AWN Mentalist as the entire mutually exclusive player package? Current author requirement names SWN tweak, so default first option.
2. What exact beginning implant defence (trigger, capacity, cost, cooldown) and how does innate defence interact with it?
3. Do voluntary projection events first appear in Act III or only immediately before Act IV? Act III remains a proposal.
4. Is astral travel point-to-point by discovered landmarks, or an abstract scene connection graph? Recommend bounded graph, never unlimited map.
5. Whether to use SWN Effort or the later proposed Law of One Chakra pools for newly authored PSI; never double charge.
6. Which WWN magical Workings fit rare practice without reproducing spells? Any concrete working must be scene-authorized.
7. Which claims in Radin/Faggin/Gallimore are *aesthetic* versus mechanical? Label before author acceptance.

**Next gate:** Tomi edits and approves. Only then implement parallel tabletop + Python and gold-test three scenarios (consensual telepathy, psychic defence, astral entry/return).

---

## Merged review pass — what this section adds

A second draft of this same subsystem was written in parallel on the same day; this file and that one were
reconciled rather than shipped twice. The earlier text above stands as the base. The sections below are the
material it did not contain: quantified procedures, the audit results, and the decisions that need a number
rather than a principle.

### The projection clock, quantified

The six steps above need one track so that "the thread home" is a thing a table can see. Proposal:

| element | draft value | why |
|---|---|---|
| **link boxes** | 3 | fits on a sheet as three tick boxes, and is short enough that a scene can fill two |
| **filled by** | each interference (+1), each scene spent past the first (+1), any ectoplasmic manifestation (+2) | every way of staying longer costs the same currency |
| **return difficulty** | 2 without an anchor, 0 with one, **+ boxes filled** | the anchor is the whole reason to prepare |
| **loss** | three boxes = lost: a *scene* of finding the way back, not a death | the failure is interesting, not terminal |
| **reset** | after a full sleep | no long-term resource to track |

**Distinct from every other track.** It is not System Strain (that is the body), not Effort (that is a trained
mind's reserve), and not hit points. A projected character's *physical* body is still where they left it and can
be found, moved or hurt — that is a scene fact the GM narrates, not a second combat board.

### One effect, three sources, one payer

| route | eligibility | what it may pay | what it may never do |
|---|---|---|---|
| natural awakening | latent trait, wakes in Act II | a condition tag per use | grant a second implementation of Telepathy |
| bionic eligibility | a trait that unlocks the latent capability | the bionic's own cost (supply, detection) | be a power in itself |
| psychotronic device | an issued or external device with a conscious operator | the device's tag state | lower a requirement more than one step |

Precedence, in order: **CWN first**; then one payer per scene (the player names it, and the fiction says why the
others do not stack); then a device may only *enable*, never out-rank a natural ability; then scripted phenomena
are never player actions and never consume anything.

### Evidence that changes the design, not just the bibliography

Kunz et al., *Cell* 188(17):4658–4673 (2025) reports inner-speech decoding **and** that simple mental strategies
robustly prevent it. That is the strongest single support in the whole file for the setting's central claim: **a
mind is not a machine that can be read, it is a person who can decline.** Every psychic procedure here should
leave the target a way to refuse — and refusing should be a real option, not a formality.

### Implementation constraints (Phase B, if approved)

* **No new die.** Every contested check takes a total that the CWN resolver produced; the psi module never rolls.
* **No import in either direction** between the psi module and `src/rules/investigation.py` — the AST guard that
  already protects `swn_psionics` (see `tests/test_1105_psi_investigation_boundary.py`) must cover it too.
* **Serialize.** `Projection` state round-trips to JSON, so a save/replay reproduces the same scene.
* **`may_stack(payers) -> str`** returns the single legal payer, with a reason readable at a table.

### Page anchors used above

SWN Revised Deluxe: Psionics pp. 30–41, Telepathy 40–41, Biopsionics 32–33, Metapsionics 34–35. AWN Deluxe: The
Mentalist p. 264, Mentalist Disciplines p. 266. WWN: Magic p. 62, Magical Workings p. 90, Arts of the Gyre p. 344.
CWN: SRD §Hacking plus `src/rules/cwn_hacking.py`. All anchors come from `data/rules/*_sections.json`, not from
memory.
