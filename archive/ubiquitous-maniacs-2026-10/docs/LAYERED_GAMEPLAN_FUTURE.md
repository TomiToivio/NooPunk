# Noopunk future plan: layered game structure

## Status

This is a future-facing design note.

It does not authorize implementation yet.

Its purpose is to preserve one concrete long-term direction for combining:

- Citizen Sleeper style narrative RPG;
- graph-based cybernetic / psychotronic / psionic hacking;
- microscale social network simulation;
- Deadeye Deepfake Simulacrum style top-down embodied operations.

The explicit rule is:

> we do not go this far yet.

This note exists so the direction is not forgotten while current work stays focused on smaller slices.

---

## 1. Target combination

The intended long-term combo is:

1. **Narrative / RPG core**
   Citizen Sleeper style scenes, dialogue, checks, therapy, investigation, and relationship drama.
2. **Psyche / CAN hacking**
   A graph-based intrusion layer combining psionics, psychotronic hacking, cybernetic hacking, and psychosurgery.
3. **Social graph simulation**
   A small Castellsian network-society simulator on the scale of roughly 6-16 active nodes per layer.
4. **Physical / top-down immersive shell**
   A 0-budget Cyberpunk 2077 / Deus Ex style layer with retro vector or 8-bit top-down presentation in the spirit of Deadeye Deepfake Simulacrum.

The goal is not four disconnected minigames.

The goal is:

> four interfaces into one underlying world-state.

More precisely:

> the layers should represent different ontologies of the same situation, not different unrelated genres.

Example:

> Ingrid refuses to cooperate with Romppainen.

That one event could appear simultaneously as:

- **Narrative / RPG:** dialogue refusal, relationship choice, internal monologue, social clock pressure;
- **Social graph:** trust edge weakens, alliance structure shifts, broker positions change;
- **Psyche / CAN graph:** defensive attractor strengthens, trauma node activates, attachment path destabilizes;
- **Physical layer:** Ingrid leaves the room, locks a door, takes a device, disappears into a new location.

That is the intended whole-game logic in miniature.

---

## 2. Core principle

Do not merge everything into one giant system too early.

Keep the layers modular and let the player move between them through explicit handoffs.

This fits current Noopunk direction better than trying to build:

- an open-world RPG;
- a full immersive sim;
- a full strategy sim;
- and a full psyche-hacking simulator

all at once.

The likely winning structure is:

- one canonical state;
- multiple gameplay lenses;
- explicit transitions between them.

---

## 3. One canonical state, many interfaces

All four layers should eventually read and write the same underlying state.

That shared state should contain at least:

- actors;
- relationship edges;
- scenes and dialogue flags;
- location and access state;
- devices and implants;
- investigation facts and uncertainties;
- anomaly state;
- layer-coupling information.

Different modes would then expose different parts of the same system:

- RPG reveals lived experience and decisions;
- social simulation reveals network consequences;
- hacking reveals hidden structures and intervention points;
- physical mode reveals spatial risk, embodiment, and material access.

An important long-term rule follows from this:

> every significant character or entity should exist as one object with multiple projections, not as separate disconnected versions per subsystem.

---

## 4. Layer responsibilities

## Narrative / RPG

This remains the emotional center of Noopunk.

It handles:

- dialogue;
- scenes;
- choices;
- therapy sessions;
- relationship turns;
- investigation as lived experience;
- fail-forward narrative checks.

This is where the deepest authored content budget should remain.

The practical reason is simple:

- a graph saying `TRUST = -0.73` is not interesting by itself;
- Ingrid staring at Romppainen and asking, "Did you go into my psyche again?" is gameplay.

The narrative layer is where the player understands what the other abstractions actually mean.

## Social graph simulation

This is the microscale network layer.

It handles:

- trust;
- suspicion;
- attraction;
- authority;
- dependency;
- ideological alignment;
- blackmail leverage;
- shared trauma and resonance.

The point is not mass society simulation.

The point is a small, legible network where each edge matters.

Useful node types could eventually include:

- people;
- AI agents;
- institutions;
- factions;
- occasionally important constructs.

Useful edge types could eventually include:

- trust;
- affection;
- authority;
- information flow;
- dependency;
- ideological alignment;
- fear;
- surveillance;
- hostility.

Different graph projections may also reveal different realities of the same cast:

- professional network;
- emotional network;
- information network;
- institutional command network.

## Psyche / CAN hacking

This is the graph-based intrusion and psychosurgery layer.

It handles:

- cybernetic access;
- implant intrusion;
- memory clusters;
- dissociated personas;
- psychic field drift;
- psychotronic relays;
- noetic edges;
- AI agents;
- symbolic and traumatic knots inside psyche-space.

This is not ordinary cyberpunk netrunning alone.

It is a cross-layer system where cyber, astral, and psychosurgical operations can collapse into one encounter.

The distinctive Noopunk claim is:

> cyberattack, psionics, and psychotherapy can become one abstract mechanic when represented as manipulation of a conscious-agent network.

The target is not always "a computer." It may be:

- an AI;
- a human psyche;
- a BCI;
- a collective unconscious structure;
- a cybernetic system;
- a dream;
- a hallucination;
- a social assemblage.

## Physical / top-down immersive shell

This is the embodied operation layer.

It handles:

- movement;
- line of sight;
- stealth;
- terminals;
- locks and devices;
- drones and robots;
- room layout;
- infiltration and escape;
- physical risk.

This layer should stay small and disciplined.

Its job is not to dominate the whole project.

---

## 5. Handoff model

The layers should eventually communicate through explicit requests and results.

Illustrative examples:

- RPG -> `social_tick_requested`
- RPG -> `physical_scene_requested`
- RPG -> `hacking_encounter_requested`
- Social sim -> `relationship_changed`
- Social sim -> `rumor_created`
- Physical layer -> `access_gained`
- Physical layer -> `alarm_triggered`
- Hacking layer -> `memory_exposed`
- Hacking layer -> `implant_compromised`
- Hacking layer -> `psyche_drift`
- Hacking layer -> `psychosurgery_effect`

The practical principle is:

> one layer should request or perturb another, not absorb its whole logic.

---

## 6. Recommended first integrated slice

Do not start from a sandbox.

Start from one canonical vertical slice with a clear sequence.

Recommended shape:

1. morning social scene in the ward or laboratory;
2. RPG interaction with one or two important NPCs;
3. small physical infiltration or embodied access sequence;
4. access to a terminal, implant, or psychotronic device;
5. one small hacking / psyche encounter;
6. return to dialogue and social consequences.

This proves that the layers can feed one another without requiring a full game in every mode.

---

## 7. Physical layer scope discipline

The biggest risk is overbuilding the physical layer because it is seductive.

To avoid that, the first physical shell should be:

- one floor or one compact zone;
- a few rooms;
- a few doors, terminals, and devices;
- 2-4 active NPCs;
- stealth-lite rather than combat-heavy;
- strong atmosphere, low systemic sprawl.

The target is not full Deus Ex.

The target is:

> a credible embodied shell for the narrative and hacking layers.

The physical layer should mainly produce situations for the other three systems rather than consume the whole game with combat.

Illustrative loop:

- break into a laboratory to reach a server;
- the server gives access to a BCI or psychotronic relay;
- that access opens a psyche graph;
- the psyche intrusion alters a relationship;
- the relationship shift restructures the social graph;
- the new graph state creates retaliation, alliance, or further dialogue.

---

## 8. Hacking design principle

The hacking layer should start graph-first, not minigame-first.

The node ontology can later include:

- implant;
- device;
- credential;
- memory cluster;
- trauma knot;
- dissociated persona;
- trust bridge;
- psychotronic relay;
- noetic gateway;
- AI process;
- symbolic archetype;
- CAN edge.

Possible action verbs could later include:

- probe;
- spoof;
- stabilize;
- sever;
- rewrite;
- resonate;
- mirror;
- anchor.

The point is not to mimic existing netrunner UI conventions too narrowly.

The point is to let cybernetic, psychotronic, psionic, and psychosurgical operations share one graph vocabulary.

Example target shape:

```text
           [Mother]
              |
              v
[Abandonment] -> [Defiance] <- [Romppainen]
       |            |
       v            v
    [Fear]       [Attachment]
```

Possible interaction verbs in such a graph could later include:

- inspect;
- strengthen;
- weaken;
- sever;
- bridge;
- entangle;
- suppress;
- induce superposition;
- collapse state.

The important consequence is ethical and social, not just mechanical:

> you can hack a person, and the person may notice.

---

## 9. Social simulator limits

The social simulator should remain intentionally microscale.

Recommended active range:

- 6-10 core actors in a slice;
- hard cap around 16 active nodes per layer in the near-term design vision.

That makes the system readable enough that:

- every edge can matter;
- every shift can be narratively legible;
- the player can actually reason about the network.

The goal is not huge population simulation.

The goal is dense meaningful relation space.

This is best treated as a microscale Castellsian network society rather than a population sim.

---

## 10. Pacing and genre expansion

The long-term structure should preserve phased expansion rather than reveal every ontology immediately.

Suggested rhythm:

1. shabby cyberpunk noir and paranoia;
2. interpersonal and therapeutic drama;
3. psyche-space and psychsurgery;
4. consciousness hacking and x-risk scale revelation.

This means the game can begin looking almost ordinary in genre terms and only later reveal what kind of world it really is.

That gradual opening is a strength.

One possible full loop looks like this:

```text
Narrative event
    ->
Choose objective
    ->
Social investigation
    ->
Physical operation
    ->
Cyber / psychotronic access
    ->
Conscious Agent Network manipulation
    ->
Social consequences
    ->
New dialogue
    ->
World state changes
```

Or more compactly:

```text
Dialogue
-> betrayal
-> social graph fracture
-> physical confrontation
-> psyche hack
-> trauma revelation
-> new faction
```

---

## 11. Explicit non-goals for now

This note should not be used to justify current implementation of:

- a full open city;
- a combat-heavy immersive sim;
- a giant procedural cast;
- realtime simulation of all layers at once;
- seamless blending of every interface;
- fully generalized psyche-graph infinity from the start.

These are future possibilities, not current milestones.

Also do not begin with:

- giant maps;
- full inventory systems;
- large weapon catalogs;
- fully generalized stats for every subsystem;
- 16 fully autonomous embodied AI actors in one live scene;
- a complete psychosurgery ontology.

---

## 12. Recommended milestone order for the future

When this direction becomes relevant, the safest order is:

1. define the shared state schema;
2. define layer handoff contracts;
3. complete one RPG + social integrated slice;
4. add a minimal physical top-down shell;
5. add a minimal hacking / psyche graph encounter;
6. connect consequences across layers;
7. only then expand content and scope.

The key principle is:

> prove coupling on one slice before scaling any individual subsystem.

An ideal later prototype could be as small as:

- one building;
- four characters;
- one mystery;
- one psyche hack;
- one social conflict;
- one physical infiltration.

For example:

- UFAB laboratory at night;
- Romppainen, Ingrid, Tanaka, and Pilgrim;
- somebody has modified UFAB Ragnarok;
- nobody admits doing it;
- the player interrogates, investigates, infiltrates, hacks, and possibly enters somebody's psyche;
- the result is contradictory memories and a trust decision.

---

## 13. Failure philosophy

Every layer should fail forward.

Examples:

- physical failure -> suspicion, injury, lost access, altered route;
- hacking failure -> drift, false memory, alarm, contamination, partial rewrite;
- social failure -> rumor, distance, manipulation opportunity, faction tension;
- RPG failure -> costly success rather than dead stop.

No layer should produce a flat "nothing happens" result.

---

## 14. Scale limits

To stop this turning into a sprawling pseudo-AAA project too early, keep only three active scales in mind:

## Personal

One person:

- dialogue;
- memory;
- psyche;
- relationships;
- immediate choices.

## Local network

Roughly up to 16 meaningful nodes:

- laboratory;
- criminal cell;
- police unit;
- cult;
- company team;
- therapy cohort.

## Physical scene

One compact playable space:

- lab floor;
- apartment;
- nightclub;
- metro station;
- corporate office;
- warehouse.

Larger politics can exist as background state, but not as a full live simulation target in the near-term vision.

---

## 15. Event system as central nervous system

The layers will eventually need one underlying event logic.

Illustrative events:

```text
PSYCHE_NODE_ACTIVATED
actor: Ingrid
node: abandonment_complex
intensity: 0.82
```

This could later trigger:

- dialogue variation;
- relationship change;
- AI behavior change;
- visual effect;
- quest update;
- altered social edge.

Likewise:

```text
SOCIAL_EDGE_CHANGED
source: Romppainen
target: Ingrid
trust: -0.22
```

This could later perturb:

- available dialogue;
- willingness to cooperate;
- defensive psyche structures;
- physical movement or avoidance behavior.

This event logic should eventually function as the central nervous system of the layered game.

---

## Summary

The likely best long-term formula is:

> Citizen Sleeper style narrative core, Noopunk-specific CAN/psychosurgery hacking, a small high-legibility social graph simulator, and a tightly scoped DDS-style embodied shell.

But not yet.

For now this stays a preserved future direction, not an implementation target.
