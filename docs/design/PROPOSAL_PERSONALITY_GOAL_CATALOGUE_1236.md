# NoöPunk: Common Personality and Goal Tags

> **Status: proposed author-facing catalogue for #1236 / #1218.** These are selectable *examples*, not approved immutable canon. Use existing `src/world/narrative_tags.py` and `docs/rules/NARRATIVE_TAGS_1184.md`; no new stats or modifiers, no replacement Goal engine. Tags should be instantiated with concrete owners, sources and outcomes.

## Semantics

A Personality Tag describes observable behavioral disposition and has **trait, lever, under_pressure, taboo**. An NPC can be inconsistent, but the inconsistency should be motivated. The PC chooses his reaction; do not forcibly move Tony's character. Goal Tags express **intended outcomes** and use existing `open`, `blocked`, `done`, `abandoned` states; short/medium/long are authoring labels, not a new enum. A political ideology is best represented by an actionable **long-term Goal**, not an ideology attribute. Social Tags describe concrete alliances, antagonisms, obligations or trust between *specific parties*. Clue Tags contain sourced observations and claims, which are not automatically true. Names below are **display vocabulary**, never bonuses to CWN rolls.

## Personality vocabulary

| Trait | Lever: what gets attention | Under pressure | Taboo / personal limit |
|---|---|---|---|
| Curious | Puzzle, anomaly | Investigates despite inconvenience | Accept an explanation without looking |
| Skeptical | Verifiable evidence | Demands corroboration | Declare an accusation proved on rumor |
| Empathetic | Person in distress | Protects the vulnerable | Sacrifice a witness casually |
| Procedural | Clear lawful process | Searches policy for a defensible path | Falsify official records |
| Idealistic | Credible ethical purpose | Challenges authority | Betray openly held principle |
| Pragmatic | Workable compromise | Trades ideals for immediate results | Waste lives on symbolism |
| Loyal | Proven comradeship | Protects colleagues | Abandon a trusted partner |
| Independent | Freedom of action | Defies interference | Surrender judgment uncritically |
| Cautious | Practical risk reduction | Delays action for confirmation | Risk civilians without cause |
| Reckless | Urgency, challenge | Acts before obtaining backup | Admit fear publicly |
| Methodical | Traceable evidence | Checks every step | Ignore a missing detail |
| Improvisational | Unusual opportunity | Finds a workaround | Follow a failed script indefinitely |
| Sociable | New contact | Seeks a network of helpers | Leave a friend isolated |
| Reserved | Privacy, discretion | Withdraws and observes | Reveal a confidence needlessly |
| Cheerful | Chance to help | Keeps morale up with practical encouragement | Humiliate a frightened person |
| Cynical | Exposing hypocrisy | Anticipates institutional failure | Trust public relations alone |
| Ambitious | Promotion, recognition | Competes and takes initiative | Accept permanent obscurity |
| Protective | Safety of companions | Interposes themselves | Abandon somebody in their care |
| Obsessive | Unfinished evidence | Returns repeatedly to the case | Leave a contradiction unresolved |
| Compassionate | Chance for rehabilitation | Seeks nonviolent alternatives | Enjoy another person's suffering |
| Authoritarian | Clear hierarchy/order | Tightens control | Openly challenge trusted authority |
| Anti-authoritarian | Arbitrary power | Resists imposed control | Treat authority as inherently legitimate |
| Secretive | Confidential information | Conceals motive | Disclose guarded personal truth |
| Romantic | Mutual emotional connection | Risks vulnerability | Treat love solely as transaction |
| Suspicious | Hidden motive | Tests others' loyalty | Trust a stranger immediately |
| Scholarly | Interesting theory/archive | Researches instead of acting | Destroy a unique manuscript |

These are **sample dispositions**, not universal moral diagnoses. An NPC's taboo may be broken at a meaningful cost, creating an event and potentially changing the tag. Multiple traits may conflict. Every NPC should begin with **2–4 salient Personality Tags**, each given specific lever, stress response and taboo rather than an entire encyclopedic list.

## Goal vocabulary

| Horizon | Example Goal Tag (player/NPC) | Possible Story / Task connection |
|---|---|---|
| Short | Complete today's Europol briefing and paperwork | Daily and Task Loop |
| Short | Obtain a lawful surveillance authorization | Administer Task; bureaucratic blocker |
| Short | Authenticate the scanner evidence | Forensic Task; Clue Tag |
| Short | Find a witness before shift change | Connect/Talk; Investigation Scene |
| Short | Contact a trusted informant | HUMINT; Social Scene |
| Short | Protect Laura during an operation | Action Scene |
| Short | Secure a private-network terminal | Physical + Cyber Graph |
| Short | Recover a courier's missing storage medium | Investigation/Exploration |
| Short | Get enough food and clean water | AWN supply crisis |
| Short | Attend a dinner date | Appointment / Character Loop |
| Medium | Build a reliable HUMINT network in Kallio | Connect; recurring contacts |
| Medium | Expose a criminal organization financing extremists | Evidence and faction ties |
| Medium | Earn colleagues' professional trust | Social Tag events |
| Medium | Identify the source of a psychotronic attack | PSI + Investigation |
| Medium | Understand an apparent precognitive dream | Dream Arc; uncertainty preserved |
| Medium | Reconcile a contradictory childhood memory | Lifepath memory Arc |
| Medium | Earn authorization for specialist psychotronic work | Institutional Task |
| Medium | Repair a damaged relationship | Character Loop |
| Medium | Recover from addiction and rebuild routines | Existing AWN addiction rules + optional Arc |
| Medium | Stop a hostile faction's infiltration campaign | SWN Faction Loop consequences |
| Long | Defend Helsinki residents and their civil liberties | Institutional / ethical career direction |
| Long | Protect EU society from rogue ASI | European security ideology |
| Long | End psychotronic surveillance without due process | Civil-liberties political goal |
| Long | Preserve strict human control over AI systems | Decelerationist political goal |
| Long | Liberalize AI research and challenge the AGI ban | Accelerationist political goal |
| Long | Establish NHI-human coexistence | Diplomatic or religious-political aim |
| Long | Advance the Zookeeper religion | Faith/political faction objective |
| Long | Expose the true history of the NHI Crisis | Long campaign investigation |
| Long | Build a resilient community outside Helsinki | AWN Enclave actions |
| Long | Restore democratic accountability to Plato | Institutional reform |
| Long | Advance a European social revolution | Ideological faction goal |
| Long | Protect a family or long-term partnership | Personal life Arc |
| Long | Control Helsinki's organized crime | Criminal faction objective |
| Long | Become an expert investigator without compromising ethics | Personal career aspiration |

Faction goals use the **same goal schema** as NPC goals. A faction may want `Maintain the AGI ban` while a character wants `Overturn the AGI ban`; Social Tags connect their antagonism. A Clue Tag may contain a seized manifesto alleging either aim, but is not proof that the faction actually pursues it.

## Suggested defaults and checks

- **Tony:** select 2 starting personality tendencies and 1 revisable long-term Goal in lifepath; short goals arise from daily work. No forced worldview, romance or drug use.
- **Laura:** disciplined/protective/experienced field operator; actual traits authored in the companion NPC dossier.
- **Salla:** cheerful/resourceful/knowledgeable, with other potential traits grounded in events.
- **Romppainen:** intellectually curious, irreverent and professionally skilled, balancing four previously established facets.
- Every goal has **one owner**, a human-readable statement and a reason for activation. A player can reject or revise proposed goals.
- Keep **subjective recollection** and **hidden ground truth** separate. Belief is never inferred automatically from a dream or clue.
- Reuse canonical `PersonalityTag` record fields (`npc`, `trait`, `lever`, `under_pressure`, `taboo`). If player tags need a schema adaptation, propose it separately and test it; do not silently treat the `npc` field as an arbitrary character type.
- No numeric personalities, no personality-to-dice bonuses, no involuntary player coercion.
