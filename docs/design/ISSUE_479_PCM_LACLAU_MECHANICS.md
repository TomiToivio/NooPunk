# PCM and LaclauGPT as lightweight faction mechanics (issue #479)

**Status: proposal for discussion. Nothing here is locked numerical canon, no rule is approved, and
Tomi remains final designer.** This document answers all seven of #479's acceptance criteria. It does
not restate [POLITICAL_SIMULATION_DESIGN.md](../../strategy_game/docs/POLITICAL_SIMULATION_DESIGN.md)
(Layer II's vocabulary proposal for #282) — it supplies the *tabletop* layer that sits on top of it.

Read `RULEBOOK.md` as still saying **NO RULES APPROVED**. Gates B and C in `RULE_SYSTEM_RESEARCH.md`
are open; so this is a paper procedure, not code. Numeric tuning is deferred to prototyping.

## 1. Concept → tabletop component, and what we deliberately do not import

| Source concept | Tabletop component | Container it reads from | What happens in play |
| --- | --- | --- | --- |
| Laclau: demand | **Demand card** | `Demand` | A constituency wants something concrete: security, disclosure, autonomy, bread, an ASI ban, contact |
| Nodal / empty / floating signifier | **Signifier card** | `Signifier`, `SignifierRole` | "Humanity", "Freedom", "Security", "The Noösphere" can hold discordant demands together — and can be taken away |
| Chain of equivalence | **Coalition links** | `Articulation` | Link two or three compatible demands to mobilise an alliance that keeps its disagreements |
| Antagonistic frontier | **Us / Frontier slots** | `Frontier` | Say what the project organises *for* and what it holds responsible for blocking it. A critic is not automatically an enemy |
| Hegemony | **Regional influence + institutional control** | `PoliticalFormation` | Lasting ability to set agendas, build coalitions and enact policy. Publicity alone wins nothing |
| Affect, reality tunnels | **Commitment / trust / interpretation markers** | `un_political_discourse.json` | The same event is read differently. Uncertainty changes loyalty, recruitment and alliances |
| PCM assemblage | **Agent capability TAG** | #346 tags | Human–AI collaboration unlocks specialist actions and makes dependence and access matter |
| PCM rhizome | **Network / chapter token** | — | Flexible, resilient to losing a node, hard to coordinate once disagreement grows |
| PCM Common | **Commons token** | — | Shared knowledge and infrastructure can be lent to allies; enclosure and sabotage are real risks |
| PCM multitude | **Plural coalition ability** | — | Different groups cooperate without dissolving. Dissent and local autonomy cap top-down orders |

**Do not import.** Continuous opinion dynamics ✗. Large discourse graphs ✗. LLM persuasion scoring ✗.
Consciousness variables ✗. A sprawl of ideological stats ✗. A second dice engine ✗ — resolution stays
the existing Fate-derived procedure (Layer I / #461). Terms here are prompts for a GM and players, not
an obligation to implement an academic formalism. The theory is a **lens, not a law**: that a
mobilisation is broad is not evidence that it is hegemonic, and Laclau's formula is a heuristic.

## 2. The four faction sheets

Each sheet is a **view over data that already exists** — `data/world/un_parties.yaml` (the roster and
register) and `strategy_game/data/un_political_discourse.json` (positions, tunnels, stances, fault
lines, currents, endgames, relations) — plus the Layer II containers. The sheets add nothing
canonical; if a sheet and the data disagree, the data wins.

**Libertarian Accelerationist Party**
- *Signifier:* **Acceleration** — the frontier is a market, and the crisis is a licensing problem.
- *Demands:* extraterrestrial special economic zones; permission for accelerated ASI research; no UN
  or member-state intervention in the compute economy.
- *Tensions:* whether unregulated ASI and special zones are compatible with liberty at all; whether to
  ride the populist wave or buy the incumbent.
- *Contacts / influence:* megacorporate funding, thin mass appeal, deep access to reconstruction
  contracts.
- *Reality tunnel:* restrictions are the cause of the crisis, not the response to it.

**True Humans Party**
- *Signifier:* **Humanity**, held tendentially *empty* — wide enough to chain many grievances, which is
  exactly why it can be stolen by a rival articulation.
- *Demands:* reject all NHI presence; ban existential-risk technologies; restore sovereignty and family.
- *Tensions:* religious fundamentalists against materialist doomers; nationalisms with incompatible
  definitions of who counts as human; lawful politics against violence.
- *Contacts / influence:* a mobilised base, no corporate base, courts and security services watching.
- *Reality tunnel:* everything boundary-blurring is one conspiracy. **Its exterminationist plank
  remains the record's marked extremist position, not endorsed.**

**Unity, Security and Stability Party**
- *Signifier:* **Security** in the administrative register — the crisis is a management problem.
- *Demands:* public order; functioning institutions; diplomatic management of both NHI relationships.
- *Tensions:* hawks against diplomats; emergency powers against civil liberties, including due process
  for alleged hybrids and espers.
- *Contacts / influence:* the broadest everyday legitimacy, and therefore the slowest to move.
- *Reality tunnel:* a competent authority is already handling this; every answer to a critic risks
  looking like more of the same.

**The Noösphere** — see §3.

### Equal-opportunity hegemony

**Every faction builds hegemony by the same relational route**, and no faction is given a shortcut:
articulate more demands to your signifier than your rivals do, and hold the frontier where you want it.
Hegemony is read from *which demands are chained to which signifier and who is inside the frontier* —
never from a popularity number, and never from being right. Any faction can win this way, including the
one the author finds least sympathetic; that is the point of the model, and it is why the four share
one procedure rather than four bespoke ones.

## 3. The Noösphere: lore and sample cards from PCM

**Premise (#470 is authoritative).** A Green-Left alliance whose largest player is a reformed Chinese
Communist Party, articulating a fictional Taoist-Maoist cyborg-multitude politics, defending the
planetary Biosphere and Noösphere, and seeking alignment or entry with the apparently benevolent
Confederacy. **The Confederacy's benevolence is a faction belief, never a GM fact.**

- *Core promises:* ecological repair; human–AI cooperation and cognitive commons; shared control of
  infrastructure; recognition of diverse kinds of agents; flourishing beyond the human.
- *Costs and weaknesses:* diffuse command and slower decisions; commons exposed to enclosure; trust and
  interoperability problems; uneven cyber access; dependence on the Confederacy; technocratic elites
  wearing participatory clothes.
- *Tensions to foreground:* decentralised anti-sovereign assemblies vs party-led central coordination;
  pluralism vs the pressure to present one coherent subject; ecology vs computation; planetary
  sovereignty vs integration into a paternalistic Confederacy.

**Sample demand cards (4–6).** Each is a `Demand` with a constituency and a cost if ignored:

1. **Open the AGI-era knowledge commons.** *Wants:* shared models, data and medicine. *Cost of
   silence:* expertise concentrates behind licences.
2. **Protect the biosphere.** *Wants:* binding ecological repair. *Cost:* reconstruction is read as
   postponable forever.
3. **Guarantee BCI consent and cognitive liberty.** *Wants:* enforceable consent, audits, and a right to
   disconnect. *Cost:* the neuro-divide becomes permanent and invisible.
4. **Recognise uncertain non-human moral status.** *Wants:* protection without declaring consciousness.
   *Cost:* the question is settled by whoever profits from settling it.
5. **Negotiate Confederacy accession with guarantees.** *Wants:* access on terms. *Cost:* alignment
   arrives as dependency.

**Sample event card — "Invitation to the Social Memory Complex".** The Confederacy offers network
integration: immediate reconstruction and PSI intelligence, at the risk of autonomy and surveillance.
*Choices:* accept; accept only with consent, independent verification and commons governance (wins
sceptics, slows access); refuse for sovereignty (risks splits). **No choice is automatically correct.**

## 4. Adversarial crisis: "The Broken Commons"

*A hacked BCI- and AI-linked cooperative is suspected of Swarm infiltration. Four factions, four
incompatible readings, one hidden truth.*

- **GM-hidden truth.** The breach was an **inside job by a local manager using a Swarm-shaped
  signature** to force a quarantine that would destroy the cooperative's commons and free its assets for
  private enclosure. There is no Swarm. Nothing in the public record proves this.
- **Libertarian Accelerationists:** offer private containment under a corporate contractor — the
  contractor's subsidiary is quietly the buyer.
- **True Humans:** demand the cooperative be destroyed. The signature is the proof they already wanted.
- **Unity, Security and Stability:** want a quarantine: defensible, slow, and it hands the manager
  exactly the outcome he engineered.
- **The Noösphere:** propose independently audited community control of the rebuild, which is the only
  route that finds the truth — if they can agree among themselves and trust the auditors.
- **Persuasion limits.** No dice roll changes what a faction believes is *really* going on: beliefs move
  only when evidence is produced, published, and survives each faction's own tunnel. Investigation finds
  the signature's inconsistency; only disclosure, negotiation and institutional action convert it.
- **Meaningful choices.** Quarantine fast and bury the truth; investigate and risk the breach spreading;
  publish everything and let the frontier fight; or let the commons be sold and call it containment.
- **Fail-forward.** Any failed action yields a grievance, a split, a legitimacy loss, contradictory
  information or a rival's opportunity — never an inert turn.

## 5. Paper prototype: one political turn

Uses #461's economy (a leader and four agents, **one action per character per turn**) and the existing
Fate-derived resolution. One sheet, four factions, a few regions.

| Action | What it does | Read from |
| --- | --- | --- |
| **Organize** | Build or repair a chapter/network; raise local commitment | Network token |
| **Articulate / Frame** | Chain a demand to your signifier; steal a floating signifier | `Articulation`, `Signifier` |
| **Negotiate** | Build a coalition link, or buy a rival's support | Coalition links, relation state |
| **Investigate / Disclose** | Produce evidence; change what others *think* happened | Reality-tunnel markers |
| **Govern / Deliver** | Convert influence into policy or an actual delivered good | Region track, institutional control |
| **Disrupt / Defend** | Attack a rival articulation, or shore up your frontier | `Frontier` |

**Tracks, kept few:** each region carries (a) an influence/legitimacy track and (b) one or two salient
demands. **Electoral popularity, institutional power and faction loyalty are three different things** —
say which one an action moved. No sprawl of scores; everything else is a card.

**Turn order:** event creates contested demands → each character takes one action → coalitions are
negotiated → local influence and institutional control change **only if a goal was actually achieved** →
possible backlash or split. **A discourse victory without material or institutional follow-through is
fragile by design.**

**Political trade-off (a game effect, not a law of Laclau's theory):** a quick exclusionary frontier can
buy short-term cohesion at the price of polarisation and defections; compromise buys a broader coalition
at the price of disappointing hardliners.

## 6. Playtest questions

1. How many tokens and cards does a player actually track before the game stops being approachable?
2. Minutes per turn with four factions and three regions — is a short session real?
3. Are the trade-offs *strategic*, or does one line dominate? Specifically: does anyone ever rationally
   choose compromise over an exclusionary frontier?
4. Do dissent and defection matter, or are they decoration? Does a faction ever split at the table?
5. Does each faction feel like a project with its own tunnel, rather than an alignment on a meter?
6. Does the frontier ever *lose*: does a faction sometimes find that its enemy was not the blocker?
7. Is the hidden truth discoverable by play, and does publishing it beat burying it?

## 7. Cross-references and overlap resolution

- **#470 owns the roster** and remains authoritative over older markdown. This document does not restate
  the four parties' canon; it reads it. `FACTIONS.md` is the **legacy RPG's** starter library (#107,
  "small Helsinki-centered", explicitly not a global encyclopedia) and is deliberately *not* used as the
  2045 roster.
- **#469 owns the ideology model**: signifiers, tunnels, relations, schisms and belief change. The cards
  and the crisis above *consume* that structure; they must not fork it.
- **#346 owns the tag vocabulary**; PCM's assemblage/network/commons/multitude map onto its typed tags
  rather than inventing new kinds.
- **#461 owns the action economy** and the Fate-derived resolution. §5 borrows its turn structure
  unchanged and introduces no competing dice engine.
- **Layer II (#282)** owns the containers (`political.py`) and the vocabulary boundary; its doc carries
  the do-not-import rule for the *theory*. §1 adds the do-not-import list for the *tabletop*.
- **Before any rulebook incorporation**, this proposal needs the author's approval through Gate B/C/D —
  starting with the cap and the shifts mapping already pending on #461.

## 8. Guardrails

- **PCM is inspiration for a fictional faction, not an endorsement.** Real-world Panpsychic Cyborg
  Multitude does not endorse The Noösphere's policies; a fictional party is not the project.
- **LaclauGPT's research does not validate any 2045 scenario.** Its framework asks for evidence,
  uncertainty and interpretive review; game abstractions are fiction, not measurement.
- **Panpsychic ideas do not prove consciousness** — not of AIs, not of rhizomes, not of NHI, not of the
  Noösphere. Uncertainty, dissent and multiple in-world interpretations are preserved deliberately.
- **Networked human–AI actors are not automatically Noösphere allies**, just as a Construct is not
  automatically Swarm. In-world beliefs stay distinguishable from GM-hidden reality.
