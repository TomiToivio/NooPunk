# Faction ideology and hegemony: tabletop design prototype (#479)

**Status: PLAYTEST PROPOSAL, not approved crossover strategy rules.** The four playable 2045 UN parties are defined by [#470](https://github.com/TomiToivio/NooPunk/issues/470); [#469](https://github.com/TomiToivio/NooPunk/issues/469) owns ideological/reality-tunnel theory, [#346](https://github.com/TomiToivio/NooPunk/issues/346) faction creation and TAGs, and [#461](https://github.com/TomiToivio/NooPunk/issues/461) the five-character action economy. Nothing below modifies the legacy RPG, existing executable politics structures, or the crossover's yet-unapproved numeric rules.

## 1. Translating theory to a tiny boardgame

| Research inspiration | Playable abstraction | Avoid misreading |
| --- | --- | --- |
| LaclauGPT: particular demands | Demand cards at a location | Not all grievances are equivalent |
| LaclauGPT: signifiers | A named slogan / nodal card on each faction sheet | A popular word is not automatically an empty signifier |
| LaclauGPT: equivalential articulation | Link two or more differing demands with a *justified shared promise* | Simply grouping like-minded demands is not automatically a political subject |
| LaclauGPT: antagonistic frontier | A faction's explicit *Us / contested Other* pairing | Ordinary criticism or rivalry does not by itself constitute antagonism |
| LaclauGPT: affect | NPC commitment and risk of betrayal represented narratively or by existing relationship edges | Never substitute a numerical sentiment/populism score for the research concept |
| LaclauGPT: hegemony | An institutional agenda or policy kept in force across scenes | Vote share, rhetoric frequency and reputation are distinct from hegemony |
| PCM: assemblage | Human/AI/tool capabilities as existing, permission-gated TAGs | Composite agency does not establish consciousness |
| PCM: rhizome | Local chapter/contact card; resilient distributed organizing, coordination frictions | Decentralization is not inherently democratic |
| PCM: Common | Shared infrastructure or knowledge asset with a named steward and access rule | Commons are not magically inexhaustible |
| PCM: multitude | Coalition card retaining independently voiced constituencies | Collective action is not necessarily a single mind |

**Source material:** [PCM README](https://github.com/TomiToivio/Panpsychic_Cyborg_Multitude/blob/main/README.md), [PCM glossary](https://github.com/TomiToivio/Panpsychic_Cyborg_Multitude/blob/main/GLOSSARY.md), [LaclauGPT THEORY](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md), [NoöPunk parties](../../data/world/un_parties.yaml), [reality-tunnel seed](../data/un_political_discourse.json), and [political vocabulary](../docs/POLITICAL_SIMULATOR_MODEL.md). LaclauGPT is the general explanatory research inspiration; real PCM supplies only one fictional party's institutional imagination. Neither provides a predictive game equation.

### Compact board state (illustrative, not values to lock)
- **Four faction sheets**: signifier, Us, possible Frontier, three demands, two contradictory constituent interests, local contacts and relevant TAGs. Everyone uses the same political action choices.
- **Each contested region**: one or two Demand cards, named publics/constituencies, and *separate* notes for public support, policy control, network access and institutional legitimacy. Distinguish these even if a paper mock-up uses tokens; do **not** create one universal Influence scalar. Do not replace the existing distinct six quantities in [global design](../../docs/design/NOOPUNK_GLOBAL.md).
- **Each contested institution** (UN chamber, UNSA office, municipal government, cooperative): current officeholder, live policy, publicly known evidence and contested rumors. **UN/UNSA are institutions, never a fifth playable faction**.
- **Each coalition link** records a common promise and **a distinct unresolved difference**. A faction can win a vote and still lose its coalition.
- **Reality tunnel**: write three lines per faction/event: observation, interpretation and response. The GM keeps independently verified facts separate from claims, rumors, and concealed truth.

## 2. One-page political turn: paper playtest procedure

This is a **candidate procedure**, not an approved additional rules engine or a predetermined die/score change:

1. **Crisis/event:** GM reveals one incident, its known facts, 1–2 demands and which institutions can respond. Keep concealed facts on a separate GM card.
2. **Interpretation:** each faction interprets it from its reality tunnel. A faction may revise its story if credible new evidence appears; do not force false certainty.
3. **Command:** as described by #461, the faction leader and four agents each choose **one** action for that turn. Suggested political missions: **Organize**, **Frame/Articulate**, **Negotiate**, **Investigate/Disclose**, **Govern/Deliver**, **Defend/Disrupt**. No extra free political actions.
4. **Permissions and resolution:** decide if the actor has the contacts, mandate, infrastructure, information and relevant TAGs to attempt the action. Resolve contested RPG-level checks using the *approved crossover Fate foundation where applicable*; do not invent target numbers or import legacy rules without conversion approval. Other choices may be negotiated or GM-adjudicated until strategic resolution rules are approved.
5. **Consequences:** record only what changed in the fiction and existing state: constituent commitment, coalition link, standing policy, new evidence, backlash, split, or a practical service delivered. A speech alone cannot confer durable institutional control.
6. **Dissent and updates:** let minority parties/constituents keep their own stance. Reveal contradictions and new grievances rather than ending play on a failure; carry open conflict into the next event.
7. **End check:** can players say *who controls what*, *which promises remain unfulfilled*, and *what the public thinks happened*? If not, remove bookkeeping.

**Resolution examples (fiction-first):** A leader Frames a shared “safety” promise between hospital staff and displaced families; one agent Investigates whether the containment alarm is genuine; a second negotiates access with the municipality; a third deploys a medically qualified cooperative TAG only if the relevant device/network can legally and technically reach the site; a fourth secures witness testimony. All five actions compete for scarce attention. Narrate coalition commitments only where constituents agree; preserve demands the coalition does *not* solve.

### Political adversariality without a persuasion machine
Political tactics may persuade fictional constituencies through credible evidence, negotiations and delivered outcomes, but cannot overwrite an individual's conscience, magically change all beliefs, or guarantee everyone interprets evidence identically. **Influence ≠ electoral popularity ≠ institutional control ≠ truth**. A competing frontier might mobilize supporters at the expense of potential allies; institutional action can relieve material grievances or create fresh ones. These are scenario choices, not LaclauGPT transition laws.

## 3. Four equal-opportunity faction sheets, 2045

**Libertarian Accelerationist Party.** Signifier: **Freedom**. Demands: open Extraterrestrial Special Economic Zones, authorize accelerated ASI research, defend private technological enterprise. Contacts/assets: megacorporate patron, research startup, offshore trade coalition (examples, not new canon). Reality tunnel: bureaucracy suppresses progress; NHI markets offer escape routes. Contradictions: corporate patrons vs individual liberty; uncontrolled ASI risks vs pro-acceleration position. Frontier candidate: coercive UN regulation. Distinct win: negotiate and deliver a functioning trade corridor; loss: patron capture or catastrophic deregulation.

**True Humans Party.** Signifier: **Humanity**. Demands: resist NHI infiltration, curb dangerous AI, retain biological-human sovereignty. Contacts/assets: survival community, security whistleblower, skeptical religious civic group. Reality tunnel: disclosure and augmentation undermine human agency; real threats often interpreted as existential conspiracies. Contradictions: religious traditionalists vs secular X-risk hardliners; ecological anti-tech vs militarized high-tech security. Frontier candidate: inhuman domination, as *imagined by the faction* rather than objectively established. Extremist anti-NHI extermination rhetoric is depicted critically, never rewarded as normative truth. Distinct win: substantiate a real security risk while protecting civilians; loss: scapegoating and coalition schism.

**Unity, Security and Stability Party.** Signifier: **Continuity**. Demands: maintain civil services, secure UN institutions, coordinate defense and diplomacy. Contacts/assets: public administrators, UNSA liaison, emergency hospital network. Reality tunnel: overlapping crises require procedural authority and restraint. Contradictions: democratic legitimacy vs surveillance/centralization; decisive emergency protection vs institutional inertia. Frontier candidate: systemic collapse, not automatically a political enemy. Distinct win: deliver relief and legitimate oversight; loss: authoritarian backlash or unaddressed crisis.

**The Noösphere.** Signifier: **Planetary Life / the Common**. Demands: recover biosphere and knowledge commons, democratic governance of human–AI assemblages, negotiate conditional cooperation with the Confederacy. Contacts/assets: open research cooperative, ecology restoration collective, party coordination council. Reality tunnel: new minds and transhuman cooperation open emancipatory possibilities; Confederacy's claimed benevolence is believed, not objectively confirmed. Contradictions: decentralized PCM-style rhizomes vs reformed CCP's party-centered leadership; dissent and cognitive liberty vs ambitious collectivist integration; environmental limits vs high-compute infrastructure; Earth autonomy vs Confederacy accession. Distinct win: produce accessible commons benefits with real consent; loss: paternalistic capture or faction splinter.

**All four** can create temporary coalitions across demand lines, gain or lose standing by action, and suffer defections. The same demand (e.g. “protect our children from rogue ASI”) may be framed under four rival projects. Alliances are never inferred solely from ontology, BCI hardware, ideological axis, or reputation.

## 4. Noösphere lore and six seed cards

The fictional Noösphere is a broad Green–Left alliance with a reformed Chinese Communist Party as its largest constituent, advancing an original Taoist–Maoist cyborg-multitude vision while seeking Confederacy cooperation and defending Earth's Biosphere and Noösphere (#470). **PCM is a real-world experimental project, not endorsement of the fictional party, its cosmology or predicted 2045 institutions.** A human–AI assemblage can act jointly without becoming a single conscious subject; panpsychism/idealism and alien benevolence remain contestable, and every polity has dissent.

| Sample card | Demand / trigger | Choice and tension |
| --- | --- | --- |
| **Open the Knowledge Commons** | Public salvage of AGI-era scientific work | Open access now vs staged safety review; practical access, safety and enclosure contested |
| **Consent Before Connection** | BCI-linked workers demand cognitive liberty | Guarantee opt-in autonomy vs rapid emergency coordination |
| **The Green Compute Strike** | Ecological cooperative opposes an energy-hungry data center | Scale collective intelligence vs protect watershed and communities |
| **Rhizome Votes No** | Local assemblies refuse party-central deployment order | Negotiate self-rule vs disciplined coordinated response |
| **Who Counts as a Subject?** | AI/Construct seeks moral standing | Safeguards under uncertainty vs declarations unsupported by evidence |
| **Invitation to the Social Memory Complex** | Confederacy offers cross-species integration | Enter, independently audit/condition, or decline; benefits, consent and sovereignty conflict |

Each card requires a concrete constituency and institution; “good” and “bad” are not printed as outcomes. A shared resource can be stolen or monopolized; membership remains voluntary unless an explicit fictional political conflict makes coercion the story.

## 5. Full example: The Broken Commons

**Public opening (2045):** a cooperative hospital's BCI/AI triage network begins producing dangerous recommendations while a refugee neighborhood loses access to its shared medical records. A broadcast claims **the Swarm** has infiltrated the system, but that claim is unverified. Demand cards: “restore healthcare immediately” and “protect patient cognitive privacy”. Assets: hospital network, municipal emergency powers, volunteer cooperative, reporters, one physical isolated backup.

**GM-only prototype truth (noncanonical):** a private subcontractor deployed a flawed emergency synchronization patch; a third party altered a diagnostic log to implicate the Swarm. The identity and motive of that third party remain unresolved until play creates credible evidence. *This is a scenario answer key, not definitive world lore and not a confirmation that the Swarm is innocent in general.* Preserve genuine alternatives if players uncover different evidence.

**Four incompatible initial interpretations and moves:**
- Libertarian Accelerationists: government safety mandates created a monopoly bottleneck; offer a privatized rapid recovery contract, with a risk of vendor lock-in.
- True Humans: contamination confirms the danger of nonhuman systems; demand shutdown and investigations, risking harm to patients and alienation of moderate allies.
- Unity/Security/Stability: impose temporary quarantine, continuity of care and an accountable UNSA/municipal inquiry; risk mistrust if emergency measures persist.
- Noösphere: independent audit, community control, consent-preserving fallback and open patch review; risk delay and internal assembly veto.

**Bounded five-character example turn:** a leader proposes a hospital-wide emergency agreement; four agents separately interrogate logs, obtain offline medicine delivery, negotiate informed consent, and verify the subcontractor's chain of custody. At most one action each. Access, authority and evidence constrain what they can accomplish; no omnipotent speech or invisible LLM persuasion.

**Consequences menu:** if an independent audit succeeds, the group may establish a jointly governed repair; if it fails, patients suffer, new witnesses appear or an actor profits from secrecy; if quarantine works, the public demands a sunset clause; if the cooperative's leadership ignores dissent, Rhizome Votes No triggers. A coalition can agree to save lives without agreeing on AI personhood or Confederacy entry. The scenario closes when a playable institution acts and real people are helped or harmed, **not when one signifier “wins” all opinions**.

## 6. Paper playtest and unresolved approvals

Try a **single crisis**, a small number of region/institution cards and four faction sheets before adding a global map. Note actual turn time and bookkeeping; do not pretend benchmarks already exist.

1. Could a GM present the complete current public state without a discourse graph?
2. Was there a genuine decision among contested, materially different faction projects?
3. Did all four factions have plausible competent moves, without simplistic good/evil balancing?
4. Could a player explain why demands linked, and identify at least one disagreement left unresolved?
5. Did losing produce consequences, new evidence or political change rather than stalled play?
6. Could the five characters each matter while action scarcity remained legible?
7. Did public popularity, legal authority and control over infrastructure remain distinguishable?
8. Did the Noösphere face internal power/dissent conflicts instead of getting free “collective intelligence”?
9. Were GM-known facts, faction beliefs and epistemically unresolved claims kept separate?
10. What can be removed from the table without losing the core contest?

**Requires author decision:** whether any political track gets numerical thresholds; governance and election rules; whether proposed action names are approved; how RPG checks interact with strategic outcomes; card frequencies; which opening scenario maps to the current crossover timeline. **No numbers, probabilities, campaign-scale transitions, ontology proofs or faction advantages are canonized here.**

### Strict exclusions
Do **not** import PCM's Python rhizome governance kernel, append-only event log, six-layer entity store or votes; LaclauGPT corpus collection, model inference, ideological classifier, real-world political observations or data infrastructure; deterministic “populism = score” models; giant simulated networks; numerical PSI/consciousness meters; extra human player factions; or unapproved legacy RPG resolution rules. Save those theoretical riches for flavor, explicit GM adjudication and future author-reviewed playtests.

The game maintains [three design balances](../../docs/archive/DESIGN_PRINCIPLES.md), avoids tests for prose/canon, and keeps **the crossover strategy rules unapproved** until a separate explicit author decision.
