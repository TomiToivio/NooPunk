# NoöPunk game design memo: systems, selves, and the Noösphere

> **Status:** exploratory design memo for issue #31.  
> **Authority:** this document does **not** finalize rules or override `RULEBOOK.md`, `docs/DESIGN_PRINCIPLES.md`, `docs/RULES_RESET_MEMO.md`, or author-specified decisions.  
> **Purpose:** develop a theoretical and mechanical vocabulary for later tabletop design.

## 1. Design goal

NoöPunk should make two apparently incompatible things true at the same time.

First, it should remain grounded enough that bodies hurt, organizations have procedures, money matters, networks have owners, implants require maintenance, bureaucracies survive revelations, and social position can matter more than personal heroism.

Second, the setting should be able to become completely psychedelic: psi phenomena, altered reality, non-human intelligence, distributed minds, synthetic bodies, social memory complexes, anomalous contact, and ontologies in which ordinary matter is only one interface to something much stranger.

The target is not superhero escalation. It is **asymmetric posthumanism**.

A character may be extraordinary in one domain and painfully ordinary in another. A full-conversion cyborg can still be lonely. A terrifying psychic can still be bad at paperwork. A globally famous politician can still be incapable of repairing a broken terminal. A distributed human-AI assemblage can still lose access to its apartment because the landlord's identity service cannot reconcile its legal personhood.

The game should therefore reward **difference between systems**, not flatten characters into a single power level.

A useful tone test is:

> A character may be a nearly posthuman psychic cyborg plugged into the emerging Noösphere and still have rent problems, a disastrous ex, a municipal access card that stopped working, and an employer demanding a doctor's certificate.

That contrast is not a joke pasted on top of the setting. It is the setting.

## 2. Existing design constraints

This memo must fit the existing NoöPunk design architecture.

The following remain authoritative:

- the three design balances in `docs/DESIGN_PRINCIPLES.md`;
- tabletop first, with Godot and Concordia following later;
- an original NoöPunk rules system developed from first principles;
- the existing six attributes: **FIT, REF, INT, CHA, CYB, PSY**;
- ordinary-human 3d6 attribute generation and the existing modifier scale;
- the legacy provisional 2d6 skill-check engine already specified in `RULEBOOK.md`.

Therefore this memo does **not** replace the six attributes with four new stats.

Instead, it explores a deeper character architecture in which the six attributes may operate **inside or across four systems**:

1. biological / physical;
2. psychic / consciousness;
3. social / communication;
4. cybernetic.

The four systems are best treated, at least initially, as **ontological and mechanical domains**, not as a replacement attribute list.

## 3. Luhmann as design inspiration

Niklas Luhmann is useful here precisely because he resists the intuitive idea that society is simply a collection of human beings.

In a simplified game-design reading:

- living systems reproduce life;
- psychic systems reproduce consciousness;
- social systems reproduce communication.

A person is therefore not a tiny sovereign box containing "body + mind + society." Biological, psychic, and social processes are analytically distinct even though they continually depend on and perturb one another.

This is alien enough to ordinary RPG design to be productive.

Most RPGs quietly assume that the player character is one unified agent. Attributes are properties of that agent. Social interaction is something the agent does. Technology is equipment attached to the agent.

A Luhmann-inspired NoöPunk can instead ask:

> What if a character is a temporary coupling of several operationally distinct systems?

This is especially appropriate for a game about cyborgification, AI, networks, altered consciousness, NHI, and the Noösphere.

### 3.1 The important correction

This memo should not claim that Luhmann described "biological, psychic and social character stats." He did not.

Nor should NoöPunk claim that human experience is actually cleanly separable into four boxes.

The value is in the productive tension:

- **lived experience feels entangled**;
- **systems theory distinguishes operations**.

Mechanically, that gives NoöPunk a way to model characters whose body, consciousness, social existence, and machine integration can change at different speeds and even come apart.

### 3.2 The fourth system: cybernetic

The proposed fourth category, the **cybernetic system**, is a deliberate NoöPunk extension rather than a claim about Luhmann's own taxonomy.

The design question is not merely whether computers are "complex enough." The stronger question is whether contemporary or future digital systems can recursively reproduce the operations that constitute them.

Candidate examples include:

- AI-agent ecologies;
- self-maintaining software infrastructures;
- algorithmic markets;
- autonomous bot networks;
- platform moderation systems;
- distributed machine identities;
- persistent digital persons;
- human-AI assemblages whose decisions and memories recursively produce later decisions and memories.

For NoöPunk, the cybernetic domain becomes interesting when a machine network is no longer merely a tool but starts to behave as an operational environment with its own continuity, memory, boundaries, dependencies, and modes of failure.

The game does not need to settle the philosophical question. It can make the dispute part of the world.

## 4. Four systems as character domains

### 4.1 Biological / physical system

This domain concerns embodiment, metabolism, sensorimotor capability, physical continuity, injury, exhaustion, and the material substrate that currently carries most human activity.

Possible mechanical contents:

- wounds;
- fatigue;
- pain;
- disease;
- reflex load;
- physical augmentation;
- sensory bandwidth;
- replacement organs;
- synthetic bodies;
- bodily dependency on drugs, charging, maintenance, or environmental conditions.

Existing **FIT** and **REF** naturally live heavily in this domain, but the relationship should not be exclusive.

A cybernetic body may use CYB for some operations while still taking biological or physical-system consequences.

### 4.2 Psychic / consciousness system

This domain concerns the moment-to-moment reproduction of subjective experience: perception, attention, memory, self-model, imagination, intention, altered states, anomalous cognition, and continuity of experience.

Possible mechanical contents:

- attention;
- memory integrity;
- identity continuity;
- altered-state susceptibility;
- psi capability;
- ontological shock;
- contact experiences;
- dream / waking permeability;
- dissociation;
- competing self-models;
- anomalous perception.

Existing **PSY** belongs strongly here. **INT** may contribute to some psychic operations but should not be treated as a synonym for consciousness.

A key design distinction is that "powerful psyche" should not automatically mean "mentally healthy," "rational," or "immune to strangeness."

### 4.3 Social / communication system

This is the most important place not to collapse Luhmann into a conventional Charisma stat.

Social systems are not a property stored inside a person. They arise through communication and persist beyond the intentions of any participant.

A character therefore has social capacities, but also **positions inside communication systems**.

Possible mechanical contents:

- reputation;
- recognized role;
- institutional access;
- legal status;
- organizational membership;
- authority;
- public narrative;
- media visibility;
- obligations;
- debts;
- discourse position;
- factional alignment;
- network centrality;
- trust;
- credentials;
- sanctions.

**CHA** can remain an attribute for interpersonal or expressive capability. It should not become a universal measure of social power.

A shy civil servant with CHA -1 may possess immense institutional leverage because they control a key process. A charismatic celebrity with CHA +3 may have no authority inside a particular bureaucracy.

That distinction is deeply NoöPunk.

### 4.4 Cybernetic system

The cybernetic domain concerns persistent machine-mediated continuity: interfaces, software agents, synthetic cognition, network identity, machine embodiment, data, automation, hacking, distributed infrastructure, and human-machine coupling.

Possible mechanical contents:

- interface fluency;
- machine integration;
- AI collaboration;
- network presence;
- synthetic embodiment;
- compute;
- sensor fusion;
- drones;
- digital copies;
- distributed identity;
- autonomous subagents;
- algorithmic reputation;
- machine-readable credentials;
- cybernetic dependencies.

**CYB** belongs strongly here, but should not merely mean "hacking stat."

A corporate executive with embedded decision-support systems, a swarm operator, an uploaded human, a street hacker, and a cyborg athlete may all possess high CYB for very different reasons.

## 5. The six attributes inside the four-system model

A provisional mapping can help think without changing canon.

| Attribute | Strongest affinity | Important secondary roles |
|---|---|---|
| FIT | Biological | Cybernetic embodiment, survival under coupling stress |
| REF | Biological | Cybernetic sensorimotor loops |
| INT | Psychic | Cybernetic analysis, social expertise |
| CHA | Social | Psychic expression, mediated communication |
| CYB | Cybernetic | Biological augmentation, social network presence |
| PSY | Psychic | Social resonance, anomalous / Noöspheric coupling |

This table should **not** become a hard rule yet.

The interesting design space begins when one attribute can be expressed through a different system.

Examples:

- REF through a biological nervous system;
- REF through predictive cyberware;
- CHA through face-to-face performance;
- CHA through a synthetic avatar;
- PSY through solitary anomalous perception;
- PSY coupled into a social memory complex.

This suggests that future actions may be described by three layers:

> **attribute + skill + system context**

The existing 2d6 + skill + attribute check can therefore survive while the fiction gains a richer systems layer.

## 6. Recommended direction: systems as tracks and contexts, not four replacement stats

**Recommendation:** do not add four large numerical attributes on top of the existing six.

That would create redundant bookkeeping and undermine the already specified attribute system.

Instead, explore a hybrid model:

- the six attributes remain the primary personal modifiers;
- skills remain learned capacities;
- the four systems become **domains with state, dependencies, and failure tracks**;
- social and cybernetic domains can extend outside the biological individual;
- powers and disadvantages attach to systems and couplings.

This would let the character sheet answer different questions:

- **Attributes:** what can you personally bring to a check?
- **Skills:** what have you learned?
- **Systems:** what kind of entity/process is currently doing the work, and what can fail?
- **Roles / assets / relationships:** what external structures can act through you or for you?
- **Conditions:** what is currently damaged, overloaded, captured, isolated, or transformed?

## 7. System coupling as the core NoöPunk mechanic

The most promising design concept is **coupling**.

Characters should not simply have four independent health bars. Gameplay becomes interesting when operations cross boundaries.

Examples:

### Biological + cybernetic

- reflex booster;
- neural interface;
- synthetic limb;
- exoskeleton;
- implanted sensor;
- cybernetic immune regulation.

Possible benefit: extraordinary performance.

Possible cost: overload, maintenance, rejection, latency, vendor lock-in, EMP vulnerability, firmware dependency, pain, or legal restrictions.

### Psychic + cybernetic

- BCI-assisted memory;
- AI-supported cognition;
- psi amplified through machine pattern detection;
- machine-mediated altered states;
- consciousness interacting with synthetic agents.

Possible benefit: cognition or psi beyond ordinary limits.

Possible cost: identity drift, false memories, dependency, competing agency, feedback loops, inability to determine which thoughts originated where.

### Psychic + social

- charismatic mass experience;
- cultic or religious contact;
- group psi;
- shared dreams;
- collective panic;
- social memory complexes.

Possible benefit: coordination, shared insight, large-scale anomalous effects.

Possible cost: loss of privacy, crowd capture, ideological possession, identity diffusion.

### Social + cybernetic

- algorithmic reputation;
- platform identity;
- autonomous agents representing a person;
- smart contracts;
- corporate systems;
- automated bureaucracy;
- bot-amplified discourse.

Possible benefit: reach, speed, institutional leverage.

Possible cost: deplatforming, model misclassification, frozen credentials, algorithmic scandal, identity fragmentation.

### Biological + psychic

- meditation;
- drugs;
- sleep deprivation;
- trauma;
- DMT-like contact states;
- sensory deprivation;
- psi under physiological stress.

Possible benefit: altered access to consciousness.

Possible cost: bodily danger, unreliable perception, addiction, exhaustion.

## 8. Coupling should create capability and vulnerability simultaneously

A central rule-design principle should be:

> **Every powerful coupling opens another attack surface.**

Not every advantage must be mathematically balanced. The point is structural vulnerability, not point-buy symmetry.

A cyborg body can exceed ordinary human physical limits, but now depends on power, maintenance, firmware, replacement parts, and infrastructure.

A psychic can perceive things unavailable to others, but may have difficulty separating signal from interpretation.

A public figure can move institutions, but their identity belongs partly to media systems they do not control.

A distributed AI-human assemblage can survive the death of one body, but may face continuity disputes among copies.

This allows anime-level capabilities without turning the game into conventional superhero power scaling.

## 9. Four distinct kinds of damage and failure

A future rules pass should test whether each system needs its own failure vocabulary.

### Biological failure

Examples:

- wounded;
- exhausted;
- poisoned;
- disabled;
- unconscious;
- dead.

### Psychic failure

Examples:

- overloaded;
- dissociated;
- memory-corrupted;
- identity-fractured;
- reality-uncertain;
- contact-saturated.

These must be written carefully. They should not reduce real psychiatric conditions to game-monster aesthetics.

The game can focus instead on fictional cognitive and ontological consequences of anomalous experiences.

### Social failure

Examples:

- disgraced;
- sanctioned;
- fired;
- expelled;
- discredited;
- legally erased;
- credential-revoked;
- isolated from a network;
- captured by an institution or public narrative.

Social "damage" can be devastating without injuring the body.

### Cybernetic failure

Examples:

- disconnected;
- compromised;
- forked;
- corrupted;
- rate-limited;
- deauthenticated;
- model-poisoned;
- compute-starved;
- hijacked;
- vendor-locked;
- desynchronized.

This gives the game multiple meanings of survival.

## 10. What counts as death?

NoöPunk should eventually make death an ontological problem rather than only a hit-point threshold.

Possible states:

- the body dies but a cybernetic copy continues;
- a body survives but the recognized social person is legally dead;
- a fork survives while the original consciousness does not;
- a psychic continuity persists across bodies;
- a social memory complex preserves memories but not individual subjectivity;
- a corporation or AI maintains a person's public communication after their death;
- multiple agents claim to be the same person.

The game should resist answering too quickly which continuation is "really" the same person.

That ambiguity is fertile PKD territory.

## 11. Metaphysics: Law of One structure, NoöPunk skin

The Law of One is useful here not as doctrine, but as a **structural source** for science-fantasy metaphysics.

Especially useful motifs include:

- developmental densities;
- Service-to-Others and Service-to-Self polarization;
- social memory complexes;
- consciousness evolution;
- entities whose apparent physical form is only part of what they are.

NoöPunk should not simply import this cosmology.

Instead, it can translate these motifs through four other lenses.

## 12. Vallée lens: the phenomenon refuses one category

Jacques Vallée's work is useful because it destabilizes a simple "aliens in metal spacecraft" interpretation.

For NoöPunk, NHI phenomena can remain causally real while producing manifestations that are:

- physical;
- psychic;
- symbolic;
- technological;
- folkloric;
- religious;
- social;
- absurd.

The same event might generate radar data, a contact experience, a meme wave, a new religious movement, a classified program, and contradictory eyewitness memories.

The game should preserve this **category instability**.

A good campaign need not reveal that one explanatory model was secretly correct all along.

## 13. Pasulka lens: contact becomes culture and institution

Diana Walsh Pasulka is useful for emphasizing that anomalous experiences do not enter society as raw facts. They are interpreted through:

- religions;
- scientific institutions;
- intelligence agencies;
- media;
- personal mythology;
- technological culture;
- secrecy;
- prestige;
- disbelief.

For a sociological RPG, this is gold.

A "contact event" is not only an encounter scene. It becomes paperwork, doctrine, academic controversy, leaked video, platform moderation, grant funding, cult formation, procurement, counterintelligence, and family conflict.

## 14. Hoffman lens: reality as interface

Donald Hoffman's interface-theory framing provides a useful fictional model: perception need not reveal reality as it fundamentally is.

NoöPunk can use this without asserting it as established science.

In game terms, ordinary perception may be a species-specific interface. Psi, NHI contact, BCI, altered states, or synthetic cognition may expose different interfaces.

The key consequence is not "psychics see the true world."

It is:

> different systems may expose different partial interfaces to whatever reality is.

This keeps epistemic uncertainty alive.

## 15. Gallimore lens: hyperdimensional psychedelic ecology

Andrew Gallimore's speculative work around DMT phenomenology is useful as inspiration for an ecology of apparently autonomous entities, spaces, and information-rich altered states.

NoöPunk can borrow the **design possibility** of stable or repeatable altered-state environments without declaring their metaphysical interpretation.

Questions for play:

- Are these internal cognitive spaces?
- Alternate interfaces?
- Shared virtuality generated by brains?
- Higher-dimensional environments?
- NHI communication channels?
- A Noöspheric layer?
- Something for which all of these labels are wrong?

The setting works best if evidence accumulates faster than certainty.

## 16. Densities as phase transitions, not character levels

If NoöPunk uses anything resembling Law-of-One densities, they should **not** become D&D-style levels.

A better interpretation is a set of ontological phase transitions that can apply to:

- individuals;
- groups;
- species;
- machine networks;
- social memory complexes;
- civilizations.

Crossing such a threshold could change what kinds of coupling are possible rather than simply adding bonuses.

This is a **speculative idea**, not a recommendation for immediate rules.

## 17. Service-to-Others / Service-to-Self as attractors, not alignment boxes

The StO / StS polarity is mechanically interesting but dangerous if reduced to "good / evil alignment."

A NoöPunk version could treat them as **organizational attractors**.

For example:

- systems oriented toward reciprocal coordination, commons, federation, mutual recognition;
- systems oriented toward hierarchy, capture, control, extraction, and asymmetric agency.

Real characters and organizations can contain both tendencies.

This could eventually interact with factions, institutional structure, and Noöspheric phenomena without becoming a morality score.

For now, this should remain **speculative**.

## 18. Social memory complexes and the Noösphere

The Law-of-One concept most naturally compatible with NoöPunk is the **social memory complex**.

A NoöPunk version could emerge from several overlapping mechanisms:

- BCI;
- AI memory mediation;
- shared vector stores;
- collective archives;
- psi;
- distributed cognition;
- institutional memory;
- human-machine communication;
- anomalous synchronization.

The crucial design choice is to avoid treating it as simple telepathy.

A social memory complex should raise social-theory questions:

- Who can write?
- Who can forget?
- Who controls indexing?
- Can memories be minority reports?
- Can the collective misremember?
- What happens to secrets?
- Is refusal possible?
- Who owns a dead member's memories?
- Is there a distinction between communication and consciousness?
- Can a social system remember without any individual remembering?

That last question is especially Luhmannian.

## 19. Power without superheroification

NoöPunk should permit extreme capability while preventing a single "power score" from swallowing the rest of play.

Recommended design principles:

1. **No universal level.** Advancement should be local.
2. **Extreme abilities can be narrow.** A psychic may be spectacular in one class of phenomenon.
3. **Costs are concrete.** Time, infrastructure, maintenance, obligations, exposure, social consequences.
4. **Institutions remain powerful.** Being able to bend a spoon does not grant a passport.
5. **Every system can fail differently.**
6. **Scale is not sovereignty.** A character may affect something huge without controlling the consequences.
7. **Information is not certainty.** Extraordinary perception can generate new ambiguity.
8. **Power can create dependency.** The stronger the coupling, the harder disengagement may become.

## 20. Progression

**Recommendation:** advancement should be system-specific and mostly horizontal / transformational rather than uniformly vertical.

Possible advancement channels:

- biological training or modification;
- new skills;
- cybernetic integration;
- institutional position;
- new relationships;
- reputation;
- psi development;
- access to a collective;
- legal status;
- equipment;
- AI partners;
- altered-state training;
- factional trust;
- knowledge.

A campaign can therefore change a character enormously without producing a level-20 demigod.

A normal journalist who gains access to an NHI contact network may become globally important while remaining physically ordinary.

## 21. Disadvantages should be real parts of the character

NoöPunk's tragicomedy becomes mechanical when disadvantages are not merely flavor.

Candidate forms:

- obligations;
- dependencies;
- maintenance requirements;
- debts;
- legal restrictions;
- incompatible identities;
- family ties;
- institutional duties;
- platform bans;
- unreliable equipment;
- unwanted fame;
- ideological commitments;
- awkward social roles;
- employer control;
- contested personhood;
- time-consuming care work.

The goal is not to punish powerful characters.

The goal is to make every character exist in a world.

## 22. Sociological simulation: characters are positions as well as persons

A character sheet should eventually describe more than the organism.

Candidate categories:

### Person
- attributes;
- skills;
- conditions.

### Relations
- allies;
- dependents;
- rivals;
- family;
- contacts;
- AI partners.

### Organizations
- memberships;
- roles;
- authority;
- duties;
- sanctions.

### Communication position
- reputation;
- audience;
- credentials;
- public narratives;
- discourse communities.

### Infrastructure
- devices;
- network access;
- compute;
- implants;
- platforms;
- transportation;
- housing.

### Noöspheric position
- psi relationships;
- contact history;
- anomalous entanglements;
- collective-memory membership.

This makes "character" partially external.

That is a useful break from heroic-individualist RPG design.

## 23. Institutions should have agency without becoming NPCs

A Luhmannian game should allow systems to generate outcomes nobody intended.

A corporation, ministry, platform, laboratory, church, union, intelligence service, or movement should not need a single mastermind to behave coherently.

Mechanically, organizations could later have:

- routines;
- goals or codes;
- resources;
- communication channels;
- thresholds;
- inertia;
- escalation procedures;
- memory;
- blind spots.

This is an excellent fit for the later Concordia simulation runtime, but tabletop procedures must be designed first.

## 24. A character can win locally and lose systemically

This should be a recurring design pattern.

Examples:

- You persuade the official, but the database rejects the application.
- You expose the scandal, but the media system reframes it.
- You hack the corporation, but its insurers and suppliers automatically isolate you.
- You prove psi works, but scientific institutions fight over replication standards for ten years.
- You make contact with NHI, but nobody agrees whether it was religion, espionage, psychosis, software, or physics.
- You survive the firefight, but your synthetic body warranty is void.

These are not "GM gotchas." They are the world responding through multiple systems.

## 25. Tone: Don't Look Up without turning into parody

The comedy should emerge from **structural mismatch**.

Examples:

- interdimensional disclosure is delayed by procurement rules;
- the first verified telepath is sued for violating data-protection law;
- a Noöspheric collective has a moderation dispute;
- an NHI contact protocol becomes an ISO standard;
- an uploaded person loses a court case because their backup timestamp is wrong;
- a psychic rescue operation is postponed because the team lacks travel authorization;
- the world's most powerful cyborg cannot enter a building because its body is not in the accessibility database.

The world should still take consequences seriously.

People can die. Institutions can oppress. Contact can be terrifying. Cybernetics can exploit. Psi can destabilize.

The absurdity comes from the fact that cosmic transformation does not delete sociology.

## 26. Campaign scale

NoöPunk should support movement among several scales:

- apartment;
- workplace;
- neighborhood;
- city;
- corporation;
- state;
- transnational network;
- Noösphere;
- interdimensional / cosmic environment.

The rules should resist converting larger scale directly into bigger combat numbers.

A cosmic-scale event can create a small, concrete mission.

Example:

> Humanity has convincing evidence of social memory complexes. The player characters are assigned to a Finnish working group that must decide whether shared memories are personal data.

That is a NoöPunk adventure.

## 27. Example characters

These are design probes, not canon NPCs.

### 27.1 The psychic payroll clerk

A municipal payroll specialist with ordinary physical abilities and little combat competence.

Strengths:
- frighteningly accurate anomalous intuition;
- deep institutional knowledge;
- trusted access to municipal systems.

Weaknesses:
- hates confrontation;
- terrified of becoming publicly known;
- psi becomes noisy around large crowds;
- cannot afford to quit the day job.

Design question: can PSY + social position make this person campaign-defining without turning them into a superhero?

### 27.2 The full-conversion union mechanic

Almost entirely synthetic body, extraordinary strength and resilience, expert technical skills.

Strengths:
- extreme physical/cybernetic performance;
- can survive environments lethal to baseline humans;
- strong labor network.

Weaknesses:
- requires specialized maintenance;
- body firmware belongs to a bankrupt manufacturer;
- poor interpersonal tact;
- ongoing legal dispute about whether replacement components count as healthcare or industrial equipment.

Design question: can posthuman embodiment create more social dependency rather than less?

### 27.3 The distributed researcher

A scientist whose working identity is shared among a biological person, local AI models, wearable memory, and a partial cloud fork.

Strengths:
- extraordinary recall and parallel analysis;
- can continue some work while asleep;
- high scientific reputation.

Weaknesses:
- different components remember different conversations;
- authorship disputes;
- cannot always tell which commitments "they" made;
- university HR recognizes only one component.

Design question: when does cybernetic extension become multiple persons?

### 27.4 The contact celebrity

A completely ordinary person who had the best-documented NHI contact event in history.

Strengths:
- enormous media visibility;
- direct access to governments, cults, scientists, and intelligence services;
- may have a genuine anomalous relationship.

Weaknesses:
- no privacy;
- nobody believes the same interpretation of their experience;
- every faction wants to capture their narrative;
- they are not actually good at public speaking.

Design question: can social-system power be huge while personal CHA remains mediocre?

### 27.5 The Noöspheric dropout

Former member of an experimental social memory complex who disconnected.

Strengths:
- retains fragments of collective expertise;
- unusual psychic/social sensitivity;
- understands collective cognition from inside.

Weaknesses:
- memories of events they never personally experienced;
- former collective still speaks about them as if they are a missing organ;
- mundane solo decision-making feels strangely difficult;
- friends cannot tell where "their" opinions begin.

Design question: what does individuation mean after collective memory?

## 28. Candidate tabletop procedure: describe the system first

One low-risk experiment for later playtesting:

Before a consequential check, identify **what system is actually doing the work**.

Examples:

- biological: climbing a wall;
- psychic: resisting an anomalous intrusion;
- social: invoking professional authority;
- cybernetic: coordinating autonomous drones;
- coupled: using BCI to guide a psi search through a network.

Then use the existing attribute + skill engine.

The system label would initially alter only:

- possible consequences;
- available assets;
- relevant conditions;
- what can be damaged or overloaded.

This could make the four-system model mechanically meaningful without rewriting the core dice engine.

**Recommendation:** if prototyped, start here.

## 29. Candidate tabletop procedure: consequence crosses the boundary

A second experiment:

On a failed or costly coupled action, the consequence may land on either participating system.

Example:

A psychic + cybernetic search succeeds, but the player must choose one:

- psychic overload;
- cybernetic trace;
- corrupted memory;
- loss of network access.

This turns coupling into a narrative/gamist decision while remaining simulation-friendly.

**Recommendation:** promising, but should be tested after the basic four-system vocabulary is stable.

## 30. Candidate tabletop procedure: systemic leverage

For explicitly social actions, distinguish:

- personal persuasion;
- role authority;
- institutional procedure;
- network leverage.

This prevents CHA from eating sociology.

A character with weak CHA may still achieve an outcome because the rule, office, union, law, credential, or network is on their side.

A charismatic character may persuade everyone in the room yet lack the structural leverage to make the institution act.

**Recommendation:** strong fit for NoöPunk and worth developing in a dedicated social-system subsystem review.

## 31. What should remain ambiguous

The setting should not rush to canonize answers to:

- whether consciousness is fundamental;
- whether psi is nonlocal, hyperdimensional, informational, spiritual, or something else;
- whether NHI are extraterrestrial, interdimensional, posthuman, symbolic, multiple categories, or none of these;
- whether DMT-like spaces are internal or external;
- whether a copy is the same person;
- whether a social memory complex is conscious;
- whether cybernetic systems are genuinely autopoietic;
- whether the Noösphere is one thing or a label for several coupled phenomena.

The world can establish **effects** without establishing one final ontology.

That ambiguity is a feature.

## 32. Recommendations vs speculative ideas

### Recommendations for later design work

1. Preserve the existing six attributes.
2. Treat biological, psychic, social, and cybernetic as systems/domains rather than four replacement attributes.
3. Make system coupling central.
4. Let powerful couplings create new vulnerabilities.
5. Distinguish social position from personal CHA.
6. Give systems different failure modes.
7. Keep advancement local rather than universal.
8. Keep institutions causally important.
9. Preserve metaphysical ambiguity.
10. Prototype the system label as a consequence/context layer on top of the existing 2d6 + skill + attribute engine.
11. Design tabletop rules before digital implementation.

### Speculative ideas requiring explicit later approval

- density-like phase transitions;
- StO / StS organizational attractors;
- formal social-memory-complex rules;
- separate system damage tracks;
- identity-continuity mechanics;
- copy / fork rules;
- psi-cybernetic feedback mechanics;
- Noöspheric collective-character play;
- organization-level turns;
- explicit autopoiesis mechanics.

None of these are canon merely because they appear in this memo.

## 33. Open design questions

1. Are the four systems visible as explicit sections on the character sheet?
2. Does each need a condition track?
3. Should only coupled actions invoke special coupling rules?
4. Can one system temporarily substitute for another?
5. Can characters intentionally externalize functions, for example memory into cybernetic systems or agency into institutions?
6. How should social-system consequences be bounded so they remain playable?
7. How much asymmetry can the existing attribute/check engine tolerate before probabilities break?
8. Should extreme posthuman capability exceed the ordinary ±3 attribute modifier range, use assets, or use special permissions?
9. How should psi work without becoming a conventional spell list?
10. How should cybernetic embodiment differ mechanically from equipment?
11. Can organizations be partially player-controlled?
12. When does a distributed character become a party?
13. How should the game distinguish memory sharing from consciousness sharing?
14. How should collective identity interact with responsibility and consent?
15. Can a character be biologically dead but still playable?
16. What happens when legal, social, psychic, and cybernetic definitions of the same person disagree?

## 34. Suggested next design tasks

This memo points naturally to several later, separate subsystem discussions.

1. **Character architecture:** decide whether the four systems appear explicitly on the sheet.
2. **Attributes:** map the existing six attributes to system contexts without changing them.
3. **Conditions:** explore system-specific failure states.
4. **Social system:** design roles, institutions, reputation, obligations, and structural leverage.
5. **Cybernetic system:** review against the legacy chassis hacking/cyberware chassis before deciding rules.
6. **Psychic system:** define the boundaries of PSY and psi without creating generic magic.
7. **Coupling:** prototype one minimal tabletop coupling procedure.
8. **Noösphere:** develop social memory complexes and contact metaphysics as worldbook material before hard mechanics.

Each should remain a separate author-driven decision.

## 35. References and inspirations

These are intellectual and tonal references, not claims that their speculative propositions are established facts.

- Luhmann, Niklas. *Social Systems*.
- Luhmann, Niklas. *The Society of Society*.
- Maturana, Humberto R. and Francisco J. Varela. Work on autopoiesis.
- Vallée, Jacques. *Passport to Magonia* and later work on anomalous phenomena.
- Pasulka, D. W. *American Cosmic* and *Encounters*.
- Hoffman, Donald D. *The Case Against Reality* and interface-theory work.
- Gallimore, Andrew R. *Alien Information Theory* and related speculative work on DMT phenomenology.
- The Law of One / Ra Material, used here strictly as a source of fictional metaphysical structures.
- Philip K. Dick, especially works concerned with unstable reality, identity, institutions, memory, and ordinary people caught inside impossible ontologies.
- Stanisław Lem, *Solaris*.
- Arkady and Boris Strugatsky, *Roadside Picnic*.
- *Don't Look Up*, as a tonal reference for institutional and media absurdity surrounding an overwhelming reality shift.

## 36. Closing design thesis

NoöPunk's distinctive character model does not need to answer "what is a person?" with a single rule.

It can make that the game.

A player character begins as a practical unit for play, but the world keeps pulling that unit apart:

- the body can be replaced;
- the psyche can encounter things the body cannot explain;
- society can define the person differently from the person;
- cybernetic systems can remember, act, and speak in the person's name;
- the Noösphere can make private consciousness less private;
- NHI can make every category provisional.

The result should still be playable at the table.

That is the design challenge: **cosmic ontology with mundane consequences, posthuman power with ordinary vulnerability, and sociology that refuses to disappear just because reality became psychedelic.**
