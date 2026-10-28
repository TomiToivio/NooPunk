# #719: original NoöPunk systems, exploratory candidate designs

Status: **research/design proposals, not approved mechanics**. CWN owns character actions, cyberware, hacking and factions; SWN owns trained psionics and Effort; #704 owns clue discovery; #712 owns attribute/narrative-layer comparisons. The proposals below do not claim the underlying scholarship validates a simulator.

## Gap / analogue matrix

| Gap | Existing closest approach | Useful idea | Main mismatch / legal caveat |
| --- | --- | --- | --- |
| Contested political signifiers, chains of equivalence and hegemony | Reign's organisation actions; Legacy's faction eras; Urban Shadows' debts; Spire's city politics | Relations between demands, public arenas and institutions | Reputation meters alone flatten ideological articulation; read edition-specific licences before reuse |
| Cyber + collective/psychic Noösphere | The Veil, Eclipse Phase, astral/virtual settings | Identity, emotion, embodiment, access and continuity | PbtA emotional stats should not displace CWN; commercial setting lore not reusable |
| Ambiguous manifestation, alternative ontologies | Mage paradigms, Unknown Armies identities, Trail of Cthulhu Stability, Kult, Nobilis | Disputed interpretations, strain and contact | No psychiatric condition implies truth; religious/cosmological fiction is not science |
| 3D→4D / StS vs StO | Mage advancement and relationship/ethics systems | Optional qualitative campaign progression | No moral power ladder or compulsory metaphysical alignment |

**Sources for concepts (research pointers):** LaclauGPT Phase 1 paper `https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md`; CWN SRD `https://cwn.quadrifons.com/`; GUMSHOE SRD `https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/`; Fate SRD `https://fate-srd.com/`. *The Veil*, *Urban Shadows*, *Legacy*, *Reign*, *Spire*, *Mage*, *Unknown Armies*, *Kult*, *Nobilis* and *Invisible Sun* are comparative references, not licensed dependencies. Verify exact rules and rights against primary editions before commercial adaptation.

## Module 1 candidate: discursive struggle

State: `Faction{id,resources,institutions,demands}`, `Demand{id,stakeholders}`, `Articulation{speaker,arena,signifier,linked_demands,frontier,evidence}`, `Arena{reach,gatekeepers}`, `Uptake{arena,faction,demand,observed_support}`, `Institution{rules,capacity}`. A signifier's function (nodal/floating/empty) is **context-dependent interpretation**, not a global enum or keyword frequency. Preserve rival readings and source-level provenance.

One faction action per faction turn, choosing **articulate** (link demands under signifier), **broker** (build a coalition with concessions), **contest** (offer counter-articulation / break link), **organise** (grow a movement or communications access), or **institutionalise** (convert existing coalition plus material support to policy). Resolve uncertainty with current faction resources and CWN faction procedures, not new dice. Cap each action to two named demands and one arena; change at most one bounded influence step in one arena and demand a material tradeoff. Affective commitment and antagonism are narrated and tracked by relationships, not a left/right meter or a fixed populism score. Palonen's Formula is an interpretive lens, **not** a literal numeric equation. A successful speech alone cannot seize an institution: uptake and veto/organisational access matter.

**Three-turn hypothetical:** (1) a hospital union articulates 'safety' as patient dignity plus staff autonomy in a professional arena; an employer coalition mobilises 'safety' as centralised AI monitoring. (2) a civil-rights group backs the union but demands data-access safeguards, imposing a coalition cost; employers contest the union's signifier in mass media. (3) a hospital board with an existing veto adopts only an audit requirement, not the union's maximal platform. Competing readings of 'safety' persist and the actor with louder messaging does not automatically win. Mechanical outcomes in this example are authored, not measured.

## Module 2 candidate: Noösphere interface

State: `Node{id,substrate,access_modes,permissions}`, `Link{channel,latency,trust}`, `Contact{participants,claimed_identity,evidence}`, `Experience{witness,description,provenance}`, optional independent `Insight` and `Stability` tracks (bounded 0–3, *not* clinical diagnoses). Access channels: terminal/BCI, isolated physical ingress, psychotronics, learned SWN PSI with normal skill/Effort. The interface does not grant a psychic technique just by connecting a BCI.

Procedure: declare target and channel → verify reachable access + permissions → if contested, make an existing CWN Program/Talk/Notice/etc. check or SWN technique → log observable evidence and claimed interpretation separately → apply source-appropriate exposure, time, privacy or Effort consequence → permit independent corroboration. One connection, one uncertain action, one consequence at a time. No new general-purpose currency. Recovery of Stability uses established downtime/support; increasing Insight is not guaranteed correct knowledge or reduced wellbeing.

**Hospital example:** Romppainen gets an authorized EEG record, the AI flags an anomalous pattern and a telepath reports a dream-image. Neither identifies a visitor. Unauthorized ward-network intrusion risks an audit alert, while a later independent power log may discriminate technical faults from tampering. A disembodied AI can participate through a permitted network node, not through invented physical stats.

## Module 3 candidate: anomalous contact / consciousness

State: `Encounter{id,observations,source_channels,competing_hypotheses}`, `Witness{id,interpretations}`, `Choice{beneficiaries,consent,externalities}`; optional `Practice{discipline,relationships,milestones}`, optional fictional `DensityNarrative{stage,tradition}`. Use service-to-self and service-to-others as **descriptions of choices within a fictional tradition**, not global binary morality, political alignment, psychiatric status or power multipliers.

Procedure: witness an observation (with a mundane access path), list >=2 interpretations including one non-anomalous explanation, choose whether to attempt contact, use existing CWN/SWN actions and risks, record effects on relationships and material conditions. A 'third-to-fourth density' arc can unlock *narrative responsibilities, changed perspectives and new community commitments* after three separately played milestones (e.g. reciprocity, dissent, reconciliation), never automatic psionic rank, immunity or universal enlightenment. Any player can opt out or use a materialist interpretation. Fiction inspired by Vallée's interdimensional hypothesis or Law of One is never labelled empirical confirmation.

**Contact example:** a mirror reflection addresses a patient. It may be an environmental fault, manipulation, altered perception, or an external visitor. A contact team protects the witness's consent while recording independent traces. A campaign's optional '4D' milestone might change how a collective votes or shares memory; dissenters remain playable, and no faction automatically becomes good or evil.

## Interface contracts and prototype limits

All three modules consume existing CWN actions/checks, CWN faction turns, SWN Effort and the #704 case graph. Never add a second die ladder or spendable Insight points. Attach source, witness, timestamp, medium and uncertainty to claims. Preserve human, AI, cyborg and nonembodied participation via access capabilities rather than invented biological ability scores. Physical, cyber, social and noetic are intersecting channels, not competing ontological verdicts.

**Playtest protocol (not yet executed):** three tables or sessions of four turns each (a competing 'AGI' signifier, hospital BCI/PSI, and ambiguous contact). Log choices, costs, contrary evidence, action count, stalled paths, player hypothesis plurality and whether any one meter predetermines an ending. Failure thresholds: >1 additional mandatory numeric resource per module, an unearned PSI action, a guaranteed paranormal conclusion, or a faction takeover from speech alone. Compare a no-module CWN baseline at the same scenario; measure referee minutes and comprehension.

**Open decisions:** Which faction procedure supplies the one action? Does Insight exist as a number or narrative tag? How should player opt-in to density progression work? Which references are cleared for commercial adaptation? **Next actions:** approve one small paper prototype per module; conduct playtests; separately scope implementation issues after author sign-off. The current issue remains a design project until evidence and rights audit are complete.
