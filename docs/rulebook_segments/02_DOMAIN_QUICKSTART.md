## 5. Physical Systems

### 5.1. Physical traits

Physical traits are persistent physical advantages, disadvantages or unusual bodily characteristics. They describe durable features rather than temporary conditions.

### 5.2. Physical statuses

Physical statuses are temporary physical conditions such as **hungry, tired, wounded** or similar short-term states. A status may alter checks, available actions or recovery while it remains active.

### 5.3. Physical actions

Physical actions include ordinary movement and interaction with the material world: moving between locations, sneaking past a guard, climbing, carrying, pursuing, attacking, restraining, escaping and other actions resolved through the normal STAT + Skill + 1d10 engine when uncertainty matters.

### 5.4. Physical locations

The first Concordia implementation uses a **Citizen Sleeper 2-inspired location structure**.

A character occupies a larger location, such as a city, and within it a current sublocation. In the current sublocation the character may perform available tasks or move to another accessible sublocation.

**Open locations** are persistently available and can be revisited. Initial examples include:

- the player's office in the **Europol / Suojelupoliisi HQ**;
- locations around **Helsinki**;
- the player's **home**.

**Quest locations** are temporary mission spaces unlocked for a specific operation. A team may travel there for investigation, exploration, combat, social interaction, hacking, psionics or mixed objectives.

Quest locations may exist primarily in **Physical space, Cyberspace or Noöspace**, and a single quest may cross all three.

### 5.5. Combat

Combat is a structured form of opposed physical action. Use the core opposed-check architecture for attacks and defences. Existing combat, damage and test-session material is preserved in the extended reference material until the independent NoöPunk combat subsystem is fully consolidated here.

### 5.6. Weapons

Weapons are tools that modify or enable attacks. Weapon categories, damage procedures and detailed equipment statistics remain subject to consolidation from the existing rules ledger rather than being invented by this reordering issue.

### 5.7. Armor

Armor mitigates or changes the consequences of physical attacks. Existing armor and protection material remains valid where it does not conflict with later independent-system decisions.

### 5.8. Wounds

Wounds are consequences of physical harm and may also create temporary Physical statuses. The existing harm/wound rules remain reference canon pending their final independent-system pass.

### 5.9. First Aid

First Aid covers immediate treatment, stabilization and short-term physical recovery. Detailed procedures remain to be consolidated from existing material.

---

## 6. Social Systems

### 6.1. Social Interactions

A **Social Interaction** is a conversation between two or more characters. It may be:

- face-to-face;
- online;
- telepathic.

With human-controlled characters or LLM agents, conversation should remain primarily free-form. Scripted NPCs may expose a more limited interaction space.

A Social Interaction may include social skill checks, use of psionics, cybernetic hacking or other cross-system actions. It can escalate into physical combat, shift into Cyberspace, or continue telepathically through Noöspace.

### 6.2. Social skill checks

When uncertainty matters, social actions use the same core engine as other actions:

```text
Social STAT + relevant Skill + 1d10 vs DV
```

or an opposed roll against another character's appropriate STAT + Skill.

The roll resolves the uncertain mechanical question. It does not replace free-form dialogue or dictate a human player's beliefs.

### 6.3. Trading

Trading covers buying, selling, exchanging, bargaining and other economic interaction. It may use money, contracts, access, favors, reputation, barter or other setting-specific forms of value.

### 6.4. Romance

Romance is a special form of intimate Social Interaction. It is handled through the same general relationship framework as other Contacts, with free-form role-play taking priority over mechanical coercion.

### 6.5. Contacts

**Contacts** are a character's personal social connections.

A Contact has a signed relationship score from **-10 to +10** and may include a specific **Affect**.

- **+10** = Love
- **0** = Neutral / no meaningful Affect
- **-10** = Hate
- if no more specific Affect is needed, positive edges default to **Likes** and negative edges to **Dislikes**

A Contact is a personal relationship, not general standing with a group.

Contacts form a **Social Network Graph**: characters are nodes and relationships are signed, weighted edges with optional Affect labels. This graph can be combined with Motivation, Reputation and Faction graphs for analysis and visualization.

### 6.6. Factions

A Faction is an organized social or ideological formation. NoöPunk models Faction ideology using LaclauGPT's Formula of Populism:

- **US** contains actors, goals, empty signifiers and other objects the Faction identifies with, supports or treats as part of its political/social identity.
- **FRONTIER** contains actors, goals and signifiers the Faction defines itself against, opposes, fears or rejects.

US/FRONTIER is a structured ideological boundary, not a flavor-text alignment field.

### 6.7. Reputation

**Faction Reputation** measures a character's standing with a Faction on the same **-10 to +10** signed scale and may include a specific Affect.

Reputation matters especially when meeting somebody who does not yet know the character personally. An unknown NPC may initially react according to the character's Reputation with the NPC's Faction. Once a personal Contact relationship exists, that relationship can diverge from inherited Faction attitudes.

### 6.8. Motivations

**Motivations** describe what a character desires, supports, seeks, resists or opposes.

They use the same **-10 to +10** signed scale:

- positive values represent desire, attraction, support or commitment;
- negative values represent opposition, aversion or rejection.

Motivations may carry a specific Affect such as **Dreams of**, **Supports**, **Desires**, **Opposed to** or **Hates**.

### 6.9. Encounters

An Encounter begins when the character unexpectedly meets somebody who starts a Social Interaction, or when somebody contacts the character remotely.

Encounters may arrive through physical presence, messaging, calls, telepresence, augmented reality or telepathic/Noetic contact. They can become conversations, negotiations, investigations, hacking situations, psychic confrontations or combat.

---

## 7. Cybernetic Systems

### 7.1. Cybernetic Implants

Cybernetic implants are integrated technologies that modify, augment, monitor or connect the body and mind. Some implants merely provide tools; others create direct Cybernetic capability.

### 7.2. Cyberspace

**Cyberspace** is computational and networked information space. It is distinct from both physical Spacetime and psychic Noöspace, although interfaces can connect all three.

### 7.3. BCI

Brain-computer interfaces connect neural activity directly to software, networks, devices, synthetic environments and other cybernetic systems. BCI is a central bridge between biological characters and the Cybernetic domain.

### 7.4. Hacking

Hacking is adversarial or investigative interaction with computational systems. It uses ordinary checks and opposed checks with appropriate Cybernetic/technical STATs and Skills. Detailed procedures are preserved in the existing mesh/hacking material pending consolidation.

### 7.5. VR/AR

Virtual Reality and Augmented Reality are standard interfaces to digital environments. They may be accessed through conventional devices or direct BCI.

### 7.6. WLAN Devices

Networked wireless devices form the local machine environment around characters and locations. Access, trust, security, ownership and control of these devices can become game-relevant.

### 7.7. Cyberspace Actions

Cyberspace actions include connecting, searching, scanning, authenticating, spoofing, exploiting, defending, monitoring, controlling devices and moving through virtual or networked spaces. Uncertain actions use the standard resolution engine.

### 7.8. Brain Damage

Cybernetic attacks, BCI malfunction, overload, hostile psychotronics or unsafe neural interfaces may cause neurological consequences. Detailed Brain Damage rules remain deferred to the consolidated health/cybernetic design rather than invented here.

---

## 8. Psychic Systems

### 8.1. Psyche

The Psychic system covers **psychology, consciousness and psionics**.

Psychic STATs and Skills govern self-directed awareness, will, intuition, Noetic perception and PSI where appropriate. The exact active STAT list follows the latest canonical Stats section.

**Sleepers** are people who have not undergone meaningful Psychic Awakening. **Psychic Awakening** is the development or activation of direct Noetic sensitivity and capability. Awakening is not synonymous with moral goodness, sanity or social status.

### 8.2. Psychic traits

Psychic traits are persistent personality, consciousness or Noetic characteristics. They are longer-lived than Psychic statuses.

### 8.3. Psychic statuses

Psychic statuses are temporary mental, emotional or Noetic conditions. They may include shock, dissociation, temporary insanity, intrusive contact, psychic overload, dream contamination and other transient conditions.

### 8.4. Psionics

Psionics are natural or technologically augmented interactions mediated through consciousness and Noöspace. Existing canon treats PSI as part of the setting's post-QIP consciousness model rather than as a viral infection.

Detailed powers are consolidated here over time from the existing psionics material.

### 8.5. Noöspace

**Noöspace** is the formal scientific/technical name for the domain commonly called the **Astral Plane**. It is the quantum-informational domain of Conscious Agents and consciousness in NoöPunk's fictional post-QIP ontology.

Spacetime is physical reality. Cyberspace is computational information space. Noöspace is the Noetic domain. The Noösphere is the emerging planetary network of minds, AIs, Noetics, institutions, biospheric cognition, NHI and collective symbols increasingly organizing itself within Noöspace.

Noöspace can be accessed through OOBEs, remote viewing, lucid dreams, meditation, psychedelics, psychotronics, QIP interfaces, ritual and some forms of NHI contact. Detailed topology and ontology are preserved in the extended canon material.

### 8.6. Psychic Attack

Psychic Attack is hostile use of PSI or Noetic interaction against another mind, Conscious Agent or psychically accessible system. Detailed attack procedures remain to be designed using the ordinary NoöPunk opposed-check architecture.

### 8.7. Psychic Defence

Psychic Defence covers resistance, shielding, counter-influence, grounding, trained mental discipline and technological/psychotronic protection against hostile Noetic effects.

### 8.8. Polarization

Polarization models the direction and development of consciousness, influenced in part by Law-of-One service-to-others / service-to-self ideas.

The exact mechanical relationship between **Willpower** and **Empathy** remains a design question. Polarization should describe an evolution of consciousness rather than a simple morality score.

### 8.9. Psychotronic Technologies

Psychotronic technologies connect engineering with PSI and Noetic phenomena. They include:

- cybernetic or neural implants that augment natural psionics;
- sensors, amplifiers, shields and interfaces;
- heavy psychotronic weaponry;
- controlled use of psychedelics and other PSI boosters.

They do not turn PSI into conventional magic-item fantasy; they are technological interfaces to the setting's consciousness model.

### 8.10. Noetic Beings

Noetic Beings are entities encountered primarily or significantly through Noöspace.

The deeper ontology is the **Conscious Agent Network**. Noetic beings may include individual minds, collective formations, archetypal figures, dream entities, DMT entities, NHI minds, interdimensional beings, group minds and other Conscious Agents.

### 8.11. Dreams

Dreams can be ordinary psychological events, but in NoöPunk some dreams are genuinely **precognitive**, telepathic or otherwise PSI-mediated.

Dreams can also function as **OOBEs** or access routes into Noöspace.

### 8.12. Magick

In NoöPunk:

> **Magick is PSI. PSI is Magick.**

Historical occult and spiritual traditions are interpreted as partial cultural maps, techniques and vocabularies for real Noetic phenomena.

Important traditions include **Shamanism** and **Hermeticism**, alongside other regional and historical systems. They may preserve useful techniques without being complete literal cosmologies.

### 8.13. CE-5

CE-5 is treated primarily as a **summoning/contact practice for Noetic beings** rather than a guaranteed spacecraft-calling technique.

Possible outcomes include Noetic entities, anomalous lights/orbs, telepathic contact, plasmoid-like manifestations and, more rarely, unambiguous physical craft.

---

