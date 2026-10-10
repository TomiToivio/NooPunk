## 17. Social and ideological mechanics: Affect, Factions, Motivations, Reputation and Contacts

**Status: NOÖPUNK NATIVE, issue #107.**

NoöPunk uses **one Affect graph** for Factions, Motivations, Reputation and Contacts. The detailed specification is [rulebook/4_SOCIAL.md](rulebook/4_SOCIAL.md); the engine-neutral representation is [src/simulation/affect.py](src/simulation/affect.py). The canonical **terminology** for the faction system — Contacts, Motivations, Faction Reputation, US / FRONTIER and the graph layers — is [rulebook/8_FACTIONS.md](rulebook/8_FACTIONS.md).

Every relation has a Target, semantic Affect label, and Affect Score from -10 to +10 (issue #144). Labels such as Knows, Trusts, Supports, Loves, Fears, Distrusts, Hates and Opposes are not collapsed into generic sentiment. Multiple labelled relations toward one target are allowed, all relations are directional, and an absent edge means unknown rather than neutral.

Factions are changing discursive formations represented as US^(positive/constitutive Affects) + FRONTIER^(negative/antagonistic Affects). This adapts Emilia Palonen's Formula of Populism as a general model of political/social identification, not a populism classifier. US and FRONTIER may articulate demands, signifiers, identities, factions, institutions, technologies and individuals.

Character Motivations use the same edge representation. Faction membership supplies starting Affects, not mind control. Multiple factions preserve different labels as ambivalence; matching target+label edges are combined; explicitly personal Motivations can override inherited matching edges while provenance is retained.

Reputation is directional from the evaluating faction/actor toward the character. Contacts are person-to-person social edges, including friends, acquaintances, professional ties and enemies. The default UNSA affiliation is represented through the same system alongside the character's personal faction identity, and the score scale is **−10…+10** ([rulebook/8_FACTIONS.md](rulebook/8_FACTIONS.md)).

At the architecture level, face-to-face, text/chat, voice/video, Mesh and PSI communication are channels over the same social layer. The first playable interaction model is text-forward and hub-based, documented in [docs/design/GAMEPLAY_LOOP.md](docs/design/GAMEPLAY_LOOP.md), with a small Asteroid Belt/station slice as the preferred initial scope.

---

## 18. Gear, augmentation, software, and technology

**Status: LEGACY EP2 DATA, selectively imported.**

EP2 provides useful starting categories for gear, implants, augmentations, weapons, armor, software, mesh tools, and transhuman technology.

Do not blindly import giant catalogs.

For the first playable version:

- import only what the scenario needs;
- preserve provenance;
- prefer structured data;
- test whether each item has a meaningful simulation role;
- reskin/rewrite setting-specific descriptions.

The **global technology baseline is Eclipse Phase-level transhuman technology**. Access, infrastructure, legality, wealth, ideology, and local development may vary sharply between societies and locations, especially because Earth is still intact and planetary institutions remain central.

---

## 19. AI, AGI, infomorphs, and non-human agents

**Status: ADAPTED / INSPIRED / NOÖPUNK NATIVE DIRECTION.**

EP2 provides useful machinery for artificial and digital persons, but NoöPunk has its own AI/AGI/NHI themes.

The rules architecture must not assume that every important agent has a biological body.

NoöPunk also rejects the idea that intelligence can be understood simply by counting compute. **Consciousness and agency are more important than raw compute.**

A useful unit of analysis for contemporary/near-future AI is an assemblage such as:

> **HUMAN + LLM + LANGUAGE + INTERNET**

The LLM is one component in a larger cognitive and social system. Human intention, language, accumulated cultural knowledge, network infrastructure, tools, memory and machine inference jointly produce practical agency.

Likewise, human minds are extended through language, artifacts, institutions, other people and machines. Intelligence is usually collective and distributed. In this limited functional sense, language itself behaves like cognitive infrastructure: linguistic structures can be stored, transmitted and “executed” by human or machine interpreters to produce new cognition and action.

This is compatible with extended-mind approaches and with NoöPunk's broader distinction between **intelligence**, **agency**, and **phenomenal consciousness**.

Concordia should eventually support:

- humans,
- augmented humans,
- cyborgs,
- transhumans,
- digital persons,
- AI/AGI agents,
- other agent types where later world design requires them.

The exact metaphysical or legal status of these categories is world design, not something the rules engine should silently decide.

---

## 20. Important and background NPCs

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Not every NPC needs an LLM.

Use at least two broad levels:

#### Full agents

Important characters may use Concordia + LLM cognition, memory, goals, conversation, and the full relevant character state.

#### Lightweight agents

Background characters may use deterministic logic, state machines, Mesa-style agents, or extremely limited behavior.

Lightweight agents should not become socially omniscient merely because the game can call an LLM.

Promote an NPC to a full agent only when the simulation or story benefits from it.

---

## 21. Social-science simulation layer

**Status: NOÖPUNK NATIVE.**

NoöPunk is an RPG **and** a social simulation.

The simulation should eventually model some combination of:

- organizations,
- factions,
- ideologies,
- discourse,
- social networks,
- institutions,
- resources,
- political economy,
- collective action,
- technological diffusion,
- public opinion,
- hegemonic struggle,
- social change.

These systems are not substitutes for individual RPG mechanics.

Keep explicit boundaries between:

- RPG mechanics,
- agent cognition,
- social simulation,
- world simulation,
- narration.

Let them exchange state through defined interfaces.

---

## 22. Structured actions for Concordia

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Whenever practical, agents should choose from structured legal actions rather than asking an LLM to invent arbitrary mechanical commands.

Example:

```json
{
  "action": "hack",
  "actor": "character-id",
  "target": "system-id",
  "method": "credential_attack"
}
```

The rules engine validates and resolves the action.

The GM/narrator then converts the result into prose.

This separation is important for reproducibility and social-science simulation.

---

## 23. Persistence and reproducibility

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

World state and agent memory must persist.

Simulation tests should be reproducible.

Where randomness is involved:

- allow a seeded RNG;
- record important rolls/results;
- make save/load round trips testable;
- avoid hidden LLM-generated numeric state changes.

The same saved state plus the same deterministic inputs should reproduce the same mechanical results.

---

## 24. Lighter rules escape hatches

**Status: EXPERIMENTAL REFERENCES.**

EP2 is an influence and a legacy prototype source, quarantined from the intended CC release surface (see docs/licenses/ISSUE_200_CC_RELEASE_GATE.md); it is not a chassis.

If a subsystem is too cumbersome for Concordia, compare lighter approaches including:

- Transhumanity's Fate,
- Neon City Overdrive-style EP conversions (proprietary; a comparison only, not a source),
- Powered by the Apocalypse-style EP conversions,
- later native NoöPunk mechanics.

The design lesson may be:

> preserve the useful world-model concept while radically compressing the mechanic.

Do not switch the entire game system casually. Replace subsystems deliberately and record the change here.

---

## 25. Rules adapter contract

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Concordia should communicate with an abstract rules interface rather than hard-coded EP classes.

Conceptually:

```python
class RulesEngine:
    def check(...): ...
    def attack(...): ...
    def defend(...): ...
    def social_check(...): ...
    def hack(...): ...
    def damage(...): ...
```

This allows the implementation to evolve from:

```text
EP2
  ↓
simplified EP2
  ↓
mixed EP2 / NoöPunk
  ↓
native NoöPunk
```

without replacing the simulation architecture.

---

## 26. Rule-change procedure

Every meaningful mechanical change should follow this sequence:

1. **Identify the current rule.**
2. **Mark its provenance:** EP2 baseline, modified EP2, NoöPunk native, experimental, or deferred.
3. **Write the new human-readable rule in RULEBOOK.md.**
4. **Record what it replaces.**
5. **Update structured data/code.** The per-subsystem status record for this step is
   [`data/rules/conversion_matrix.json`](data/rules/conversion_matrix.json), explained
   in [`docs/rules/EP2_CONVERSION_MATRIX.md`](docs/rules/EP2_CONVERSION_MATRIX.md):
   update the row for the subsystem you changed, so the inherited / modified /
   replaced / deferred picture stays readable in one place rather than only in this
   ledger's prose.
6. **Add or update deterministic tests.**
7. **Update Concordia adapters/prompts only after the rule is stable enough to execute.**
8. **Record licensing/provenance if EP-derived material or external data is involved.**

Do not leave important canonical mechanics only in issue comments or commits.

---

## 27. Change ledger

Use this table to track major mechanical mutations.

| Date | Subsystem | From | To | Status / reason |
| --- | --- | --- | --- | --- |
| 2026-10-03 | Overall chassis | Original-from-scratch NoöPunk rules reset | EP2 homebrew foundation with evolutionary replacement | **Current direction.** Issue #60 supersedes the archived reset for active development. |
| 2026-10-03 | Runtime priority | Tabletop-first staged ports | Concordia-first playable RPG/simulation using tabletop-readable rules | **Current direction.** The rulebook remains canonical documentation, while Concordia is the immediate playable target. |
| 2026-10-03 | Setting continuity | Separate NoöPunk world progressively replacing Eclipse Phase | **Alternate Eclipse Phase timeline before the Fall; year 20XX; Earth intact; EP technology baseline** | **Current direction.** Preserve EP concepts by default and document deliberate timeline divergences. |
| 2026-10-03 | Layer ontology | Four layers treated implicitly across §15–§19 | **Explicit four-layer ontology with structural couplings (§36)** | Issue #78. Couplings made explicit because the interfaces are where the gameplay is; no mechanics defined. |
| 2026-10-04 | AGI catastrophe structure | Earlier drafts used named contemporary AI companies for a four-disaster cascade | **Multiple rogue-AGI disasters with fictionalized 20XX actors and no fixed global sequence (#98)** | Issue #98 supersedes the named-company chronology. Detailed named variants are archived; active canon keeps the disasters structural and unordered. |

| 2026-10-04 | Theory sections | Four-layer ontology and bibliography deleted by a stale-branch clobber (`901ba05`) | **Restored as §36 (four NoöPunk systems) and §37 (theoretical sources)** | The clobber removed 703 lines; the glossary kept `## 34.`, so number-keyed guards read the wrong section and the loss was silent. Restored by heading text; §27 number stays with the glossary. |
| 2026-10-04 | Sources list | Two competing sources sections (#99 landed twice as §35 and §38) | **Merged into a single §35; the duplicate §38 removed** | Issue #101. The union of both copies is kept: the fuller fiction and RPG entries from §38, the broader field list and preambles from §35. §35 now declares itself the design-facing map beside the §37 theory bibliography, and §33.2's Wendt citation is re-pointed from the stale §35.5 to §36.5. |
| 2026-10-06 | Default affiliation and Affect-graph prose | In-world `UNHSS` naming and a `-100 to +100` Affect/Contact/Reputation score in `RULEBOOK.md` prose | **`UNSA` everywhere in-world; the Affect graph reads `-10 to +10`** | Issue #149 was rebased to `rulebook/8_FACTIONS.md` alone before merge (`40e10a5`), so the rename and rescale reached the chapter, schema, runtime and data but not the canonical prose — the book contradicted its own §38 and `8_FACTIONS.md`. Residue cleared; the separate Law-of-One **Polarization** axis (§9.3, `-100 ... 0 ... +100`) is a different subsystem and keeps its wider band. |

Add rows whenever a major subsystem is replaced or substantially reskinned.

---

## 28. Immediate rulebook work

As the first playable vertical slice is implemented, expand this file with concise executable descriptions of:

- [ ] exact EP2-derived test procedure used by code;
- [ ] opposed test procedure;
- [ ] pools/resources actually implemented;
- [ ] damage/wound procedure;
- [ ] stress procedure;
- [ ] combat sequence;
- [ ] basic mesh/hacking procedure;
- [ ] social action procedure;
- [ ] embodiment/morph rules used by the prototype;
- [ ] inventory/gear rules;
- [ ] character creation subset;
- [ ] save/load relevant state;
- [ ] structured action vocabulary exposed to agents.

Only document mechanics that we actually intend to use. The purpose is not to rewrite Eclipse Phase.

---

## 29. Definition of a healthy rulebook

This document is healthy when a developer, player, or agent can answer:

- What rules are we currently using?
- Which ones still come from EP2?
- Which have been changed?
- Which are native NoöPunk?
- Which systems are intentionally unfinished?
- What does the deterministic code resolve?
- What is left to Concordia/LLM judgment?
- Where did an imported rule or dataset come from?
- Why did a major mechanic change?

If the answer requires spelunking through old commits, Discord-like issue archaeology, or guessing from Python, update this rulebook.

---

## 30. Governing principle

**Build first. Play it. Simulate it. Observe what Concordia actually needs. Then simplify and mutate the rules.**

NoöPunk should remain playable throughout its transformation.

The destination is **not a separate setting wearing borrowed EP mechanics**.

The destination is a playable **alternate pre-Fall Eclipse Phase timeline** in which NoöPunk's paradigm shifts reshape an intact Earth and wider transhuman civilization. Rules may still mutate through use, but the Eclipse Phase continuity and technology baseline are now intentional parts of the premise.

## 31. Persistent EP2 test-session subset (#60)

**Status: native orchestration around the existing EP2 homebrew test kernel.**

A GM supplies each actor's legal test IDs and trusted skill/aptitude, modifier and
pool choice. The player or agent chooses an offered ID; it cannot supply a roll,
rating or numeric outcome. Python rolls 00–99 and invokes the existing EP2 test
adapter. The pool update, random-generator state and result are committed together
to SQLite before agents observe the result. Rejected actions spend no resources
and create no memory. Saved sessions resume their random sequence, character
sheets, morph labels, remaining pools and ordered shared event log.

This is a test-resolution subset: social and mesh skill checks may use it, but
it does not yet grant access, inflict damage or implement full hacking/combat.
The event log is shared mechanical memory; private cognition and retrieval remain
Concordia integration work. A failed observer delivery may be replayed from the log.
No new setting facts, NPC personalities or mechanical subsystems are defined here.

Implementation: `src/concordia_runtime/ep2_session.py`.


## 32. Embodiment and inventory subset (#60)

**Status: compact EP2-homebrew adapter / native persistence layer.**

The playable prototype now treats identity and embodiment as separate state.

An embodiment record contains only the fields currently needed by code:

- name;
- broad kind such as biological or synthetic;
- durability;
- wound threshold;
- explicit traits.

This is **not** a complete Eclipse Phase morph catalog. It is a minimal executable
representation that can later be replaced by licensed structured EP data or a more
complete NoöPunk embodiment model.

Characters may also carry structured gear. Each gear record has:

- a stable item ID;
- name;
- category;
- quantity;
- tags;
- explicit machine-readable effects.

Gear with identical metadata may stack. Conflicting records may not silently share
an ID. Adding and removing gear is deterministic and quantity-safe.

The persistent session records resleeving/body-platform changes and inventory changes
as mechanical events in the same ordered SQLite event log used for test resolution.
Reloading the session preserves the current embodiment, inventory and history.

An older character sheet's `morph` label can bootstrap a minimal embodiment record so
the prototype remains compatible with the earlier #60 character state.

Implementation:

- `src/eclipse_phase_homebrew/embodiment.py`
- `src/concordia_runtime/ep2_session.py`

Still deferred:

- full EP2 morph statistics and catalogs;
- gear price/economy rules;
- armor and weapon-specific mechanics;
- augmentation installation/removal;
- cortical-stack and resleeving procedure;
- identity continuity rules;
- inventory mass/capacity;
- automatic gear effects on tests.

These should be added only when the playable scenario needs them.


---

