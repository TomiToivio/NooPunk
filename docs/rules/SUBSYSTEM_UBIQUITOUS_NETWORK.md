# The Ubiquitous Network — a NoöPunk subsystem with no Without Number equivalent

**Status: design specification. No number is approved; no runtime path is changed.**
Owner layer: **A** (`STAT + Skill + 1d10 ≥ DV`), per the #566 ruling. Layer B keeps its Fate kernel.

## 1. Why this subsystem exists

CWN/SWN/AWN/WWN all model hacking as **reaching a host**: you have a target machine, you roll, you are in.
That model presupposes a network you *enter* and devices you *select*.

NoöPunk's network is the opposite shape. `rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md` already says networks
have geography again and gives five access classes (§22.5), but it describes **routes to a chosen target**. What
it does not yet give is the layer underneath: the fact that in 2045 **the street itself is a network** — every
camera, door, wearable, vehicle, sensor and lamp is addressable, most of it badly secured, all of it owned by
someone. Hacking is not a visit to a place; it is *being inside a field of addressable things and deciding what
to touch*.

That is the "ubiquitous network", and none of the four Without Number books has it. Their hacking assumes
scarcity of access. NoöPunk's assumes **abundance of access and scarcity of safety** — the difficulty is never
"can I connect", it is "what notices me while I do".

## 2. The three-layer model

The subsystem is one assessment in three parts, resolved **before** any skill roll. This ordering is the whole
design: a check answers *whether you succeed*, and must never answer *whether the thing was reachable*.

| layer | question | source of truth | can a roll change it? |
|---|---|---|---|
| **Geography** | is there a route at all? | `#344` connectivity class × §22.5 access class | **never** |
| **Field** | what is addressable from where I stand, and who else is in it? | the scene's device inventory | no — it is inventory, not luck |
| **Touch** | do I get the thing I wanted, and what does it cost? | the layer A kernel (`STAT + Skill + 1d10 ≥ DV`) | yes |

**The invariant, already enforced in code and restated here:** an air-gapped target has no remote route in any
era, for any skill, and prose cannot grant one. If the scene needs it reached, the scene supplies a body, a
medium, or a machine that went in through the door.

## 3. The field

A scene declares a **field**: the addressable things present, each with an owner and a vigilance.

| field property | what it means | authored by |
|---|---|---|
| **density** | how many addressable objects are present (a stairwell vs a shopping street vs a data centre) | the scene |
| **ownership** | who receives the object's telemetry, and how quickly they read it | the scene |
| **vigilance** | the chance the field *notices* an action rather than the actor succeeding | the scene |
| **envelope** | how far class 2 (nearby wireless / IoT) extends here; walls, shields and distance end it | the scene, per §22.5.1 |

The field is **inventory, not difficulty**. A crowded street is not a harder check; it is a *louder* one. That
distinction is what makes the subsystem feel like NoöPunk rather than a difficulty slider.

## 4. The procedure

1. **Classify the route** from §22.5 (1–5). If the target's connectivity class admits no route to your access
   class, the attempt is **impossible** and the conversation ends there.
2. **Read the field** the scene declared: what is in the envelope, who owns it, how vigilant it is.
3. **Choose a touch**: one object, one intended effect. "I hack the building" is not a touch.
4. **Resolve** with the layer A kernel. The difficulty is about the *object*, never about the network's existence.
5. **Notify**: if the touch is loud relative to the field's vigilance, the owner learns *something* — not
   necessarily what you did. Being noticed is a consequence track, not a failure state.

Step 5 is the part the Without Number books do not have and CWN's "trace" only approximates: **notice is social
and institutional** — a guard, a landlord, a platform, a neighbour — not a numeric alarm clock owned by the GM.

## 5. What this replaces, and what it must not replace

- It **sits on top of** §22.5's five access classes and `#344`'s connectivity tags. It does not rename them and
  does not fork them; the orthogonality table in §22.5.2 remains the authority.
- It **does not** import CWN's hacking procedures, program verbs or Access costs. Those assume host-centric
  access and a matrix-like network, which is the model this subsystem exists to avoid.
- It **does not** create a new skill. `5_CYBERNETIC.md` and #22's skill list govern which skill applies; the
  subsystem decides *whether a skill applies at all*.

## 6. What is deliberately left open

These are author decisions and are **not** filled in here:

- the **numbers** for density, vigilance and notice thresholds (reserved: `AGENTS.md` §4);
- whether notice is a single escalating track or per-owner clocks;
- whether a "quiet" touch exists as a technique or only as a scene fact;
- how Safenet's gateway logging (class 4) differs from a class 2 owner noticing — both are "noticed", but one is
  a record and the other is a person.

## 7. Testable contract (for the implementation issue)

The subsystem is deterministic by construction, which means it can be tested without any author number:

1. a target with connectivity `isolated` returns **impossible** for every access class except 1;
2. an influence edge in a social graph never produces a route;
3. the field's contents are read from scene data, and a scene with an empty envelope yields no class 2 touches;
4. a successful touch with high vigilance produces a notice event, and a lower-vigilance field does not — the
   *ordering* is testable even while the threshold is unauthored.

Items 1–2 are already proved by `strategy_game/tests/test_cyber_access.py`. Items 3–4 would be new tests against
whatever scene structure the implementation chooses.
