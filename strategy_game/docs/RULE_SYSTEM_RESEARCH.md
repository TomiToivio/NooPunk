# NoöPunk Strategy Game: rule-system research and architecture

**Status: design options only, never canonical rules.** Issue: [#282](https://github.com/TomiToivio/NooPunk/issues/282). Historical frame: roughly 2026–2045, with real data and speculative NoöPunk setting inputs explicitly distinguished.

## Design promise
A distinct faction strategy game with **three complementary player-facing lenses**: a faction leader who experiences stories, a political field whose ideological boundaries are contested, and a manageable set of faction assets/decisions. The world map is a board, not empty 3D terrain. The network overlays politics rather than treating all power as territorial control. Limit maintenance and keep decisions/events salient; avoid Terra Invicta's idle time and CK3's excessive scale.

## Comparative references (inspiration, not copied rules)
| Example | Study | Avoid |
| --- | --- | --- |
| Crusader Kings III | character traits, character-driven political dilemmas, relationships and personal power | dynastic sprawl, medieval mechanics, sprawling map micro |
| Terra Invicta councilors | handful of influential operatives, global institutions, contested access, faction agendas | dozens of repetitive actions, opaque long campaigns, glacial pacing |
| Dune: Adventures in the Imperium houses | house identity, objectives, holdings, political obligations and house-scale narrative stakes | porting licensed rules or presuming a specific dice/economy system |
| Citizen Sleeper | scarce but meaningful narrative choices, consequence-driven text interface | forced borrowing of its dice economy |
| Disco Elysium | ideology, personal contradictions and leader's interiority as narrative | requiring its skill voice or extensive character stats |
| Democracy 4 | policies and public perceptions as interacting systems | treating politically constructed identities as fixed demographic preferences |
| LaclauGPT | evidence-grounded discourse analysis, signifiers, articulations, fronts, uncertainty | mistakenly interpreting a classifier as a validated causal simulator |

Source starting points:
- CK3: https://ck3.paradoxwikis.com/Game_rules
- Terra Invicta: https://wiki.hoodedhorse.com/Terra_Invicta/Councilors
- LaclauGPT primary theory: https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md
- NoöPunk background social simulation issue: https://github.com/TomiToivio/NooPunk/issues/152

Dune rulebooks requested for comparative analysis were not available as readable attachments in this run. Read the actual books before claiming any detailed house-management rule correspondence.

## Layer I: Leader RPG options
Represent the leader with name/identity plus *uninterpreted* author-defined attribute values and personality trait tags. Candidate narrative methods to compare later: Fate aspects, PbtA moves, CK3 event dilemmas, and lightweight skill checks. **No die, DC, modifier, move, trait list, skill or numeric range is selected.** Keep UI textual first, portrait/character card later. Leader experience must matter without a sprawling individual RPG.

## Layer II: Political simulation options
Laclau/Mouffe/Palonen describe articulations of political identities and demands, equivalential chains, antagonistic frontiers, and nodal/floating/empty signifiers. Castells offers network-making, programming/switching and communication power; consider discourse-network analysis as an evidence-to-network bridge. Keep descriptive analytic labels and hypothetical generative mechanisms in different modules. Political hegemony is not automatically a scalar score, and identities must not be frozen as stable political parties or populations. Candidate representations: events, utterances, demands, organizations, communicative ties, inferred formations and confidence/provenance. If using real-world corpora, honor privacy, sampling constraints and provenance. Test plausibility, sensitivity and reproducibility before accepting any simulated dynamics as meaningful.

**Agent approach:** Mesa for aggregate/non-central actors; optional Ollama or Concordia for a handful of faction leaders. LLM output is a proposal, not authority over game state. A validated rule layer must eventually transform proposals into state changes. An entirely non-LLM path is required. Model costs, nondeterminism and prompt injections need controls.

## Layer III: Faction management options
Possible later decisions concern leaders, field offices, institutions, legitimacy, coalitions, media channels, research, operations and logistical assets. Do not select an economy or military system yet. Show physical **location**, social **network position**, and ideological **formation** as distinct dimensions. Assess how to represent transnational networks crossing national borders and how to keep resource locations visibly differentiated from network edges.

## Proposed technical boundaries
- `strategy_game/core.py`: frozen typed data objects only, no simulated causal transitions.
- `strategy_game/ports.py`: explicit independently swappable protocols for the RPG, political simulation and faction operations, plus optional agents.
- `strategy_game/view.py`: pure view-model builder for globe point overlays and graph nodes/edges; UI engine remains undecided.
- `strategy_game/__main__.py`: empty-state JSON console demo to verify standalone installation.
- Save-state JSON schema version and provenance for replayable future research.
- Future optional adapters: NetworkX for multiplex network queries; Mesa for background ABM; Ollama/Concordia for NPC deliberation; desktop UI via a lightweight Python framework or browser served by Python. Do not pick UI engine yet.

## Questions for author review
1. Which actor types deserve full LLM leaders, and which can stay aggregate?
2. How do leader personality tags affect decisions without trapping ideology in fixed labels?
3. What makes a hegemonic shift legible to a player without pretending political change is a measured score?
4. How small can the global board be while retaining cross-border network power?
5. When are political statements analytical observations, fictional events, or generated conjectures?
6. What is the minimum meaningful faction decision loop, and how can dead turns be avoided?
7. How should transitions between three layers preserve transparency and player agency?

## Separate rule-authoring gates
Gate A: author-approved leader RPG rules. Gate B: author-approved political-simulation methodology and simulation assumptions. Gate C: author-approved strategy rules. Gate D: explicit integration contract and prototype playtest. Until all relevant gates, **no gameplay mechanics are implemented**.
