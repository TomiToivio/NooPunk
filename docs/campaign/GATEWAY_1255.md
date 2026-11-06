# Gateway: induction, the bounded astral mission, and when an Astral Graph is justified (#1255)

> **Status: design draft for author review.** Gateway is a *venue and a procedure*, not a new subsystem.
> No mechanics are added here; every resolution remains a published CWN/SWN check, and the astral layer
> stays behind authored events (see `docs/world/IMMORTALITY_AND_NOETICS_1255.md` §6).
>
> **The one-sentence version:** Gateway is what a police force builds when it decides that talking to the
> dead is evidence work — expensive, supervised, recorded, and admissible only after corroboration.

---

## 1. What Gateway is

A suite, not a machine: an isolation/flotation chamber, neural interfaces, psychotronic transducers, QIP
quantum sensors and compute, monitored physiological support, and an **external mission operator** whose
job is to bring the projector back.

**Four properties that define it:**

| Property | Consequence in play |
| --- | --- |
| **Fixed venue** | A mission happens somewhere with a door, power and a duty log — not wherever the plot needs it |
| **Consented and supervised** | Somebody outside the chamber holds the abort, and their judgement is a character in the scene |
| **Recorded** | Biometrics, operator notes and the projector's own account are three separate records that can disagree |
| **Not a teleport** | The chamber does not move anyone; it *admits* a mind to a representation and returns it |

**What Gateway is not:** a third PC discipline. The selectable disciplines remain **Telepathy and
Telekinesis**; projection is reached through authored events and this facility, never by choosing it.

**Who owns one:** Europol's serious-crime directorate keeps a small number; Sampo runs the research
units; Orion leases "continuity evaluation suites" that are the same hardware with a different consent
form; the Council has inspection rights nobody enjoys exercising.

---

## 2. Procedure (authored scenes, in order)

1. **Briefing** — what question is the mission allowed to answer? A Gateway session without a question
   is a séance, and the setting treats that as misconduct.
2. **Safety checks** — medical, psychotronic, and the operator's go/no-go. This is where a scene can
   legitimately *stop*: no roll to force it through.
3. **Induction** — entered as a scene with its own sensory signature. Failure states are fictional
   (drift, delay, unwanted link), not a new penalty track.
4. **The mission proper** — one small authored space: an exploration, an interview, a clue. Not a
   campaign map.
5. **Extraction of evidence** — what the projector can carry back is *testimony plus at most one
   bounded artefact*, and it is provable only later.
6. **Recovery** — physiological, and socially awkward: the projector is a witness whose account cannot
   be corroborated inside the chamber.
7. **Corroboration** — the real work. A Gateway clue is worth exactly what a physical clue elsewhere
   makes it worth.

**Risks, all fictional and scene-bound:** deception by the contacted entity; memory distortion on
return; an unwanted lingering link; astral predation; loss of bodily awareness; support-system failure
(which is the operator's scene, not the projector's).

---

## 3. When an Astral Graph is justified

The default is **Story scenes plus Astral tags**: a one-room conversation, a vision, a short dream. Most
astral content never needs a graph.

Build a **bounded, mission-specific** network only when the mission genuinely requires navigation:

```text
astral locations = nodes        permitted transitions = edges        agents occupy nodes
```

**Hard constraints, from #1196 and the #1178 graph semantics:**

- **Bounded and mission-specific** — created for one approved mission, not a persistent world map.
- **Entry location and return anchor** are explicit; leaving is a defined move, not an improvisation.
- **Barriers and time behaviour** are authored per mission; unknown links stay hidden until discovered.
- **No free traversal into other graphs.** Links to Physical/Story graphs are **clue and event
  references**, never automatic portals.
- **A node is not an agent.** The #1178 invariant holds here too: an occupant is never a location.
- **Reusable locales only after several approved missions justify them.**

Implementation status: **not built.** `Astral` remains a postponed scene type, and there is no fifth
graph family. Those two facts are pinned by `tests/test_lore_policy_1255.py`, so this page cannot
describe a capability the code does not have without a test failing first. This is the specification
that mission will be built against, nothing more.

---

## 4. The introductory mission — what is specified, what is missing

**Specified here (mechanics and shape only):**

- **Question:** interview a dead scientist about a claim that an astral deceiver may have planted in the
  record. The mission can succeed as procedure and still yield false evidence — that is the point.
- **Space:** three astral locations (approach, the scientist's study, a threshold that should not be
  there), two permitted transitions, one hidden link discoverable by clue.
- **Twist available to the author:** the third location exists because the *operator's* equipment is
  misconfigured, not because the dead built it. A fault is a clue.
- **Physical anchor:** the scientist's sealed office in Helsinki, which the projector can later compare
  against what they were shown.

**Deliberately missing — needs the author:** the nightmare/dream prose, the scientist's name and voice,
the interview dialogue, and the in-world consent forms. An agent will not invent Tomi's characters.

---

## 5. Cross-references

- `docs/world/IMMORTALITY_AND_NOETICS_1255.md` — what the astral layer is, and what it refuses to prove.
- `docs/research/HIA_DOSSIER_1255.md` — the quantum/psychotronic distinction Gateway sits on.
- `docs/tabletop/WORLD_GRAPHS_1178.md` — the paper procedure and the four graph families.
- `docs/rules/SCENE_TYPES_1184.md` — the scene types a Gateway mission is composed of.
- `#1152` (scripted dreams), `#1196` (astral graph deferred), `#1178` (graph semantics), `#1254`.
