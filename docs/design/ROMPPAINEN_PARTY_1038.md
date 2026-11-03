# Inspector Romppainen and the UNSA party (#1038)

**Status:** gameplay and character design for future implementation, not evidence that control/companion mechanics are coded. Companion commands must eventually be tested in the Evennia solo campaign. See [literary direction](LITERARY_CROSS_MEDIA_1037.md).

## Romppainen: authored protagonist, major NPC, occasional companion

Harri S. Romppainen is a senior UNSA inspector and the protagonist of the humorous Etsivä Romppainen prose. His familiar personality is retained, although he is older, wiser and more balanced. **The game's default PC is a newly assigned Europol field agent; the UNSA-rookie framing is historical (#1114).** Do not make Romppainen the permanent player avatar or let his expertise auto-solve cases.

Four coherent, contradictory motivations:

| Facet | Drive | Network | Play/narrative tension |
| --- | --- | --- | --- |
| Revolutionary anarchist | Anti-domination and political idealism | Radicals, European socialists, senior political contacts | Uses credentials and political patronage while distrusting state coercion |
| Academic intellectual | Investigate mind, PSI, AGI/NHI and ontological anomalies | Researchers, universities, noetics | Exclusive access to data keeps him in institutions he opposes |
| Investigator | Defend people against exploitation and colonization | UNSA, Europol, victims and witnesses | Protecting humanity may conflict with institutional emergency powers |
| Hedonistic street cop | Recover from trauma and impossible responsibilities | Pubs, clubs, sex workers, dealers, bohemian circles | Personal vulnerabilities, real reciprocal relationships, unreliable secrecy |

Addictions, including alcohol/substances or compulsive behavior, are **possible authored character arcs**, not a compulsory cluster of diagnoses, a joke about sex workers, or a gameplay reward. Represent consequences and agency.

**Unresolved political premise:** a fictional Finnish socialist EU leader with some inspiration from the public image of Sanna Marin knows Romppainen personally. Political patronage may have helped secure his UNSA/Europol role. This is fictional worldbuilding and must not be mistaken for claims about the real person. A socialist Europe may remain deeply coercive and administratively compromised. The EU/Europol discovery that UNSA member states are rogue, failed or captured is a potential legitimacy-crisis story, not mandatory canon. Romppainen may eventually become an insider dissident, leaker, or independent investigator. Do not prewrite that outcome.

## Playable/controllable party roles

| Role | Availability | Design guardrail |
| --- | --- | --- |
| **Rookie PC** | Always | Blank-slate personality and politics; core investigator |
| **Laura Wendt** | Nearly always | Rookie *UNSA* agent, experienced military/SWAT veteran; capable independent partner |
| **Harri Romppainen** | Special cases | Boss, mentor, exceptional investigator; rare player-controlled party companion |
| **Psionic asset(s)** | Mission-required | The **only** active party specialists with strong PSI; others may have latent/passive sensitivity or psychotronics |
| **Technical asset(s)** | Case-required | Netrunners/hackers, forensics, drones, electronics and related specialists |
| **SWAT asset(s)** | High-threat scenes | Tactical police backup; prefer swift lethal confrontations, not a squad-based war game |

Default: **PC + Laura**, with at most two additional on-scene companions as a provisional cap. Technical specialists and SWAT units can instead assist remotely/off-screen. Party availability should be scenario-gated and not an arbitrary hard lock on investigation progress.

## Strong PSI: scripted versus bounded

- General usable effects can include **limited telepathy** for interviewing and interrogation, bounded mental influence, and **telekinesis** in action scenes. Every effect needs narrative constraints and should respect the existing core/mod distinction.
- **Remote viewing, precognition and astral projection** are authored *scenario events* rather than unconstrained freeform commands; unlimited versions would spoil clues and create unimplementable state.
- The PC, Laura and Romppainen **do not develop strong active psi**. Passive/latent experiences or tools remain viable.
- Psionic specialists are rare and have agency. “Controllable” should mean directing or proposing an action within allowed commands, not overriding their judgment or removing consequences.

## Investigation, combat and player agency

- This is primarily a *police detective story* with investigation, witnesses, social conflict, and occasional dangerous operations.
- Preserve existing CWN combat; do not rewrite it. Stage short, consequential, potentially lethal confrontations, including street fights and sudden gunfights. Treat an entire SWAT team as a support unit/off-screen asset if per-soldier turns would swamp a case.
- Core clues should remain obtainable without possessing every specialist or passing an arbitrary single skill roll. GUMSHOE-style overlays can help, but never silently replace the base system.
- Human, scripted and future LLM-controlled actors should use compatible actions and permissions. NPCs retain relationships, loyalties, objections and narrative limits.
- No mandatory LLM or multiplayer dependency for the initial campaign. Agents and multiplayer remain future layers.

## Proposed implementation milestones (not yet completed)

- [ ] Define party membership, availability and command interfaces in the Evennia architecture.
- [ ] Add deterministic solo tests for PC + Laura; preserve existing quest/save-state compatibility.
- [ ] Add mission-specific recruit/remote-support tests for one technical asset and one PSI asset.
- [ ] Add a scripted Romppainen appearance with controllable companion actions but no automatic solution.
- [ ] Add a short CWN combat encounter with optional SWAT support; exercise refusal and aftermath.
- [ ] Validate strong-vs-passive PSI restrictions and ensure freeform precognition/remote viewing cannot bypass scenarios.
- [ ] Record dialogue/canon review by Tomi before treating proposed personal/political details as final.

Related: #1038, #1037, #950.
