# #943: Noösphere and Ontological Apocalypse overlay (CWN-first)

**Status:** proposed modular implementation, awaiting review. **Source books:** Fraser Simons, *The Veil*, second printing (2018), user-supplied PDF; D. Vincent Baker and Meguey Baker, *Apocalypse World*, 2nd edition (2016), user-supplied PDF.

## Source comparison and compatibility

| Book and location | Source-derived concept | NoöPunk original adaptation | Reject |
| --- | --- | --- | --- |
| *The Veil* pp. 7–11 | Constant mixed digital/physical reality, not a separate cyberspace | Noösphere has physical/cybernetic/psychic/social evidence channels in one scene | Separate mandatory cyberspace subsystem |
| *The Veil* pp. 28–46 | Character moves and emotion-based States/spikes | Emotion as nonnumeric player-selected descriptor | Emotion modifiers, spikes and a second attribute economy |
| *The Veil* pp. 268–276 | Beliefs and growth through play | Rookie agent's choices, relationships and beliefs are player-authored | Preset personality, playbook advancement |
| *The Veil* pp. 278–362 | MC principles, motivations, questions, threats and scenario sheets | Grounded fiction-first GM notes, faction responses, threat records | Independent PbtA GM dice |
| *Apocalypse World* pp. 8–11, 148–150 | Psychic maelstrom; opening one's mind to uncanny perception | Open Your Mind as a *procedural prompt*, authorized through existing PSI/CWN mechanics | Free universal psychic access or AW move results |
| *Apocalypse World* pp. 80–94, 106–122 | MC agenda, threats and countdown clocks | Reversible event-driven apocalypse/faction clocks | Automatic apocalyptic railroad |
| *Apocalypse World* pp. 9–11, 136–151 | 2d6 moves with 6-/7–9/10+ results | Narrative consequences after ordinary CWN outcomes | Second dice and partial-success engine |

These are summaries/interpretations, not copied rules text or an assertion that every book passage is openly licensed.

## Existing system inventory and boundary

- `godot/core/`: CWN canonical mechanics; no changes here.
- `godot/narrative/investigation.gd`, `src/rules/investigation.py`: GUMSHOE-inspired clues; core facts cannot be lost by failed dice; do not reimplement.
- `mods/noopunk/gumshoe_investigation.gd`: optional GUMSHOE investigative pools, disputed under D61; no interaction with this module.
- `mods/noopunk/stress.gd` and `mods/noopunk/psyche.gd`: existing psychological exposure/Stress. Do not add another harm track or assume active PSI.
- `godot/narrative/faction_intelligence.gd`: faction assertions, source confidence and reputation; use it instead of duplicating faction tables.
- `godot/narrative/party_roster.gd`: rookie PC plus companions, occasional NPC supervisor Romppainen, existing authorizations.
- `mods/noopunk/noosphere.gd`: optional **new** source-neutral evidence/clock/identity glue. It does not roll, charge resources, change stats, derive truth or resolve actions. The existing Stress and PSI systems remain authoritative.

## Procedures

**N1: Open Your Mind.** Player describes intention, channel and plausible access. Ordinary accessible evidence may be narrated; essential investigative facts remain covered by GUMSHOE. A risky action is *delegated* to standard CWN checks, hacking or approved SWN PSI Effort, never decided by N1. The module refuses psychic contact if active PSI capability was not authorized. A report of contact is not an ontological verdict.

**N2: Triangulate Reality.** Keep observations separate from interpretations and record sources independently. `triangulate` counts distinct evidence *channels*, not genuine independence of devices or witnesses; the GM must still check common-mode contamination. High-stakes consequences require conscious human approval and corroboration under the existing UNSA doctrine.

**N3: Reactive Noösphere.** The GM frames possible institutional, psychic and network responses. Only recorded actor actions or established consequences move a clock. No counterparty overrides a succeeded CWN roll retrospectively.

**Emotions and identity.** Six lower-case *The Veil*-inspired descriptive emotion labels are voluntary and have no ranks, point pools, spikes or dice effect. Player-initiated identity choices are recorded as statements, never assigned by a die or an NPC. Romppainen remains the protagonist's supervisor and occasionally available ally, never the protagonist.

## Threat clocks: independent, event-driven and reversible

Example campaign clocks (definitions to be authored per case, not an imposed timeline):

| Clock | Actor/motivation | Advance trigger | Stall or regression |
| --- | --- | --- | --- |
| NHI disclosure | Public institutions, witnesses and NHI factions; competing claims | Verified leak / open contact / institutional response | Corroborated correction or a negotiated disclosure delay |
| Rogue ASI acceleration | Rogue systems and counterintelligence | Proven containment breach / infrastructure capture | Isolation, power shutdown or successful containment |
| Cyber-psychic convergence | Multiple competing Noösphere actors | Confirmed shared anomaly / new interface deployment | Containment, disconnection or successful countermeasure |
| UNSA authority | UN agencies, member states, rivals | Mandate vote / emergency power expansion | Judicial review / political opposition |

A clock has a 0–6 stage and event history, no autonomous timer. Transitions require a written trigger and can move by one stage per adjudicated event. They describe story consequences and **cannot roll, modify CWN statistics or decree a character belief**. A terminal stage is not automatically the final campaign outcome.

## Generic example: unknown signal

A rookie agent perceives contradictory sensor reports while investigating a mundane communications outage. The protected records search is a standard CWN task. The existence of an essential timestamp discrepancy follows GUMSHOE core-clue procedure. The agent chooses whether to interpret the pattern as cyber interference, a noetic phenomenon, or insufficient evidence. A voluntary attempt to perceive a psychic signal requires the approved PSI capability; no automatic mind-reading. Verified hostile transmission can advance an authored faction clock. The player's emotions and interpretation remain theirs.

## Acceptance / tests

- [x] Inventory prior layers and delimit CWN/GUMSHOE/PSI/Stress ownership
- [x] Compare book concepts with a compatibility table
- [x] Source-neutral Noösphere implementation and generic demonstration
- [x] No second dice engine, psychic capability, mental-health pool or character advancement
- [x] Event-driven reversible clocks, evidence provenance and choice-driven identity
- [ ] Run Godot headless tests (not available in the authoring environment at initial commit)
- [ ] Review scene integration, preserve GUMSHOE core-clue guarantee and verify save migration
- [ ] Confirm publishing license/attribution before distribution

## Rights and reuse

*The Veil* copyright/credits (p. 2 of book) explicitly license **text** under CC BY-SA 3.0 Unported, excluding its separately copyrighted images and graphic elements. It also states certain *Apocalypse World* moves were used with permission; that permission is not automatically transferable. *Apocalypse World* 2e (copyright page, book p. iv) is ©2016 D. Vincent Baker and Meguey Baker; do not infer the whole book is open licensed. This file uses fresh descriptions and original NoöPunk implementation, **no copied text, images, playbooks, or distinctive moves**. Before release, review attribution/ShareAlike obligations and the licensing of all reused material. Keep #897 and #932 separate from this mod.
