# Theory integration proposal: three paradigm shifts (#321)

**Design research only. No canon or rules approval is implied.** Relevant bibliography: Diana Walsh Pasulka, *American Cosmic: UFOs, Religion, Technology* (Oxford University Press, 2019); *Encounters: Experiences with Nonhuman Intelligences* (St. Martin's Essentials, 2023). The first studies religion, UFO culture and technological knowledge communities; the second investigates encounters and changing interpretive frames. Neither establishes an empirically validated unified AI–NHI–PSI theory. Their usefulness for NoöPunk is a **fictional extrapolation about knowledge, credibility and institutional contestation**. Claims of real NHI and PSI must be framed as disputed. Related inspirations include Jacques Vallée (interpretation and ambiguity), Alexander Wendt (political construction of UFO knowledge) and Philip K. Dick (unstable lived reality); these are distinct approaches, not scientific corroboration.

## Crosswalk (orthogonal axes, not equivalences)

| Lens | Unit of analysis | Playable design implication | Caution |
| --- | --- | --- | --- |
| Luhmann living systems | Biological self-production | Embodied viability and material dependence | Not identical to Physical space |
| Luhmann psychic systems | Consciousness/meaning | Reported experience and personal interpretation | Not equivalent to Astral |
| Luhmann social systems | Recursive communications | Scientific, legal, political, media and economic claims | Not reducible to individual minds or Cyber |
| Luhmann function systems | Differentiated communication codes | Science tests claims; law assesses admissibility; politics makes decisions | Avoid one shared 'truth score' |
| Castells | Network access, programming, switching | Who reaches which publics and institutions | Reach does not imply persuasion |
| Laclau | Demands, signifiers, antagonistic articulations | Competing meanings of 'humanity', 'security', 'NHI' | No universal scalar hegemony |
| NoöPunk Physical | Infrastructure/embodiment domain | Material site and effects | Can contain social and psychic phenomena |
| NoöPunk Astral | Fictional experience/PSI domain | Perception and interpretation | Fictional ontology not a real-world claim |
| NoöPunk Cyber | Network/AI/digital domain | Media circulation and digital actors | Social communication crosses all domains |
| Earlier #78 four-system scheme | Physical/Psychic/Social/Cybernetic adapted design terms | Optional comparison vocabulary | Distinct from Luhmann's three system *types* |

Luhmann's operational closure means biological, conscious and communicative processes do not become identical simply by influencing one another; **structural coupling** permits reciprocal perturbations without a single causal register.

## Directional event/data flow

```text
[Physical incident] ---> [evidence ledger] ----> [scientific claim]
      |                      |                         |
      v                      +----> [legal/security claim]
[Psychic experience] ------> [testimony] ----> [media communication]
                                                    |
                                                    v
[Cyber channels / Castells reach] <---------- [attributed claims]
             |                                      |
             +-----> [audience reception] <----------+
                            |
                            v
              [Laclaudian rival articulations]
                            |
                            v
             [leader missions / faction choice]
                            |
                            v
        [local material/institutional outcomes]
                            |
                  next turn feeds back
```

A material event may *cause* records, but a communicated attribution never retroactively changes the underlying evidence. Communication links may influence access, not determine agreement.

## Minimal common schema proposal

Reuse `strategy_game.core.Event`, `Leader`, `Faction`, `Location`, `NetworkEdge`, `WorldState` and `Provenance`. Propose an optional `Incident` record (`id, location_id, material_observations, provenance`); `Experience` (`observer_id, incident_id, testimony`); `Claim` (`speaker_id, incident_id, frame, evidence_refs, audience_ids`); and `Interpretation` (`faction_id, claim_id, signifier_ids`). Do **not** coerce testimony into an observed fact. Explicitly preserve provenance and uncertainty. These types are **not implemented**.

## Worked turn (branching, author-discussion only)

2027, University and Hospital: a lab reports a puzzling signal. Physical: a sensor log; psychic: a researcher's vivid experience; cyber: an ambiguous model output. The scientist requests independent replication, a minister calls for a security review, a broadcaster frames it as AI, a community group calls for openness, and an accelerationist party calls it a commercialization opportunity. All claims have attributed speakers and distinct evidence status. Through existing communication ties a broadcast reaches more people, without guaranteeing assent.

**Branch A: transparent review.** A council leader asks the university for independent checks, a journalist publishes the methodology, and a local institution gains trust while the origin remains unknown. **Branch B: secrecy.** Another leader obtains a confidentiality order, increasing security access but reducing credibility with opponents; a coalition around the floating signifier 'humanity' forms against the perceived cover-up. The next turn offers different alliances and mission targets. Neither branch proves an alien, an AGI, or a psychic mechanism.

## Two bounded alternatives and approval gates

**Minimal passive interpretation:** keep one attributed narrative per card and player-visible rival claims; use existing party network and legitimacy fields without introducing belief meters. Cheap, explainable, appropriate for first slice.

**Modest stateful extension:** add sparse belief/reception records with provenance, update them on a small set of institution-linked events, and let leader relations affect which claims are heard. Needs author approval of what counts as reception, how contradictory claims persist, and whether confidence can change.

**First MVP:** event cards, local responses, leader identity, visible communication links and conflicting labels. **Defer:** ontology resolution, consciousness simulation, full ABM, complex PSI, mandatory LLMs, and any predictive representation of real-world political behaviour. Keep the existing strategy scaffold and main rulebook untouched until an explicit design gate.
