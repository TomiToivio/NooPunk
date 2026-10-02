# The unified tag engine (issue #51 prototype)

> **Status: prototype.** This document and the code it describes are a **prototype
> on the non-canonical `fixture:` route**, not a rulebook. `RULEBOOK.md` §5 is the
> source of truth, and it says the four systems are canonical while the statistics
> inside them are **not yet finalized**. Nothing here should be read as canon.

## The central constraint

> **Attributes are tags too.**

There is no separate attribute subsystem underneath the tag system. An attribute
tag is an ordinary `Tag` with `category="attribute"`; it appears inside the same
stack as skill, gear, cyberware, condition, relationship and ideology tags, and it
resolves through the same engine.

```text
REF +2                 # attribute tag
Pistol +2              # skill tag
Smartlink +1           # cyberware tag
-------------------------------------
stack total = +5  ->  2d6 + 5 vs difficulty
```

That is the issue's worked example, and it is what the prototype produces.

## What is canonical, and what is prototype

| Element | Status | Source |
|---|---|---|
| the four systems: Physical / Social / Psychic / Cybernetic | **canonical** | `RULEBOOK.md` §5 |
| Luhmannian grounding, Cybernetic as NoöPunk's extension | **canonical** | `RULEBOOK.md` §5, `THEORETICAL_SOURCES.md` |
| the systems are analytically distinct but *entangled* | **canonical** | `RULEBOOK.md` §5 |
| 2d6 skill check, `6/8/10/12/14` ladder | **canonical** | `RULEBOOK.md` §4 |
| the prototype attribute vocabulary (FIT, REF, CHA, SOC, INT, WIL, PSY, CYB, NET) | **prototype, non-canonical** | issue #51's own proposal |
| the stack cap, tag ratings, dice mechanic | **prototype, undecided** | issue #51 defers them |
| sample characters | **fixtures** | `fixture:` ids, invented to exercise the engine |

The prototype vocabulary is deliberately **not** written into `data/rules/core.json`.
A test asserts that: putting a prototype attribute list into the shared canon would
turn a proposal into canon (`AGENTS.md` §1/§2).

## The model

`src/tags/model.py`:

- **`System`** — the four canonical systems.
- **`Category`** — attribute, skill, specialization, background, profession, gear,
  cyberware, biomod, psionic, relationship, faction, reputation, ideology, condition,
  injury, environment, advantage. These are *labels for reasoning about applicability*,
  not separate rules subsystems.
- **`Tag`** — one unified structure: `name`, `rating`, `category`, `system`, `scope`,
  `source`, `provenance`. Serialises to and from dicts for saves and agent memory.
- **`SystemPresence`** — whether an entity meaningfully exists in each system.
  **`False` means "does not participate", which is not the same as a low score.**
- **`Entity`** — tags plus presence plus narrative flags. Identical structure for a
  human PC, an NPC and an autonomous agent (issue principle 10).

Narrative flags (beliefs, goals, loyalties, relationships) are stored on the entity
but are **not** dice modifiers. The issue is explicit: "these are not necessarily
added to every dice roll. They are fictional flags for Concordia and the GM system."
A test asserts flags are not reachable as tags.

## The resolver

`src/tags/resolve.py`:

```text
relevant tags -> sum -> 2d6 + sum vs difficulty -> mechanical outcome -> narrative interpretation
```

Relevance, applied in order:

1. **Attribute tags** count when their *system* matches the action's system, and —
   when the caller nominates one — when it is that attribute. RULEBOOK §4 says the
   GM selects the attribute that fits the action, and an action rarely depends on a
   whole system's attributes at once.
2. **Ordinary tags** count when their declared `scope` intersects the action's
   facets. Scope-based relevance is what makes applicability reproducible instead of
   depending on a GM's or an LLM's mood.
3. `(name, category)` duplicates collapse to the strongest.
4. **At most one tag per category contributes**, so synonymous causes do not pay
   twice — the issue's anti-abuse rule. "Pistol +2" and "Handguns +2" cannot both
   stack.
5. The counted tags are capped (`STACK_CAP_DEFAULT = 6`, injectable, **prototype**).

Everything not counted is recorded in `Stack.excluded` with a machine-readable
reason, so a result is auditable rather than merely reported.

The dice and the difficulty ladder come from the shared `rules` layer, so the
prototype cannot fork the resolution engine (`AGENTS.md` §13).

## Absent layers

An action in a system the entity does not participate in is **refused**, not rolled
at a penalty:

```text
fixture:utility-ai  "feel empathy"  ->  UNRESOLVED (unresolved_absent_system)
fixture:noetic      "punch someone" ->  UNRESOLVED (unresolved_absent_system)
fixture:vr-agent    "lift a crate"  ->  UNRESOLVED (unresolved_absent_system)
```

A test asserts this holds even with a perfect roll and the easiest difficulty, because
presence is a precondition rather than a modifier.

## Cross-layer propagation

One event resolved across all four layers, from the same engine and the same entity,
with a distinct stack per layer — issue item 14:

```text
PHYSICAL    FIT -1 = -1                                   total 6   failure
PSYCHIC     WIL +2  Meditative discipline +1 = +3          total 10  success
SOCIAL      CHA +2  Union organizer +2  Corporate etiquette +1 = +5  total 12  success
CYBERNETIC  CYB +0 = +0                                    total 7   failure
```

Different outcomes per layer, one engine, entangled because they share the entity.
That is what "distinct but entangled" means mechanically here.

## What this prototype demonstrated

- An attribute tag and a skill tag are genuinely interchangeable machinery — no
  privileged path exists for attributes, and a test proves that removing them from
  the stack breaks resolution.
- Scope-based relevance plus one-cause-per-category gives reproducible stacking
  without an ontology that has to be finished first.
- Presence-as-a-fact handles the AI/noetic/VR cases the issue asks for, and does it
  without inventing a "Psychic 0" that would misrepresent a non-conscious AI.
- One resolver genuinely covers combat, social, hacking, investigation and psionics;
  no domain needed its own engine.

## What is not done

- **The Concordia Game Master loop** (issue item 7) and the LLM-facing items
  (11–13: GNS balance test, social-first loop, narrative interpretation). These need
  the Concordia GM that `docs/CONCORDIA_ARCHITECTURE.md` still lists as unbuilt.
  Doing them here would mean inventing it.
- **Every decision the issue defers**: the exact dice mechanic, whether negative tags
  subtract or raise difficulty, tag ratings for non-attribute tags, advancement,
  how social tags update dynamically, how absent layers interact with the +3 ceiling,
  serialisation *policy* for simulation state, and the complexity budget. The
  prototype takes these as inputs or reports them unresolved; it does not choose.
- **The comparison against CY_BORG / Neon City Overdrive / Shadowrun / Eclipse Phase**
  (items 8–9). That is a playtest judgement, not something a prototype can assert
  about itself.

## Running the prototype

```bash
python3 -m unittest tests.test_issue51_tag_engine     # 36 tests
```

```python
import sys; sys.path.insert(0, "src")
from tags import resolve_action, sample_entities
from tags.model import System

entity = sample_entities()["fixture:runner"]
result = resolve_action(
    entity, action="shoot", facets=("ranged", "combat"),
    system=System.PHYSICAL, attribute="REF", difficulty=10, dice_total=7,
)
print(result.stack.explanation(), "->", result.check.total, result.success)
```
