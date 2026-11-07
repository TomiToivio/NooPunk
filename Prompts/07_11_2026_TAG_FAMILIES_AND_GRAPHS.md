# Prompt: Tag families and graphs: the portable layer over Cities Without Number

- **Date:** 2026-11-07
- **Topic:** issue #1283
- **Source:** Tomi's own issue text in NooPunk, <https://github.com/TomiToivio/NooPunk/issues/1283>
- **Archive status:** original author prompt, retained verbatim for future reuse. It is **not** an approved canon or
  implementation specification by itself, and archiving it does not authorize work on a frozen subproject.

## Original prompt (verbatim issue text, transport formatting normalised)

## Author decision — 7 November 2026

NoöPunk uses **Cities Without Number** as its default tabletop system. CWN provides the old-school procedures for skills, action, combat, equipment and hacking. Eclipse Phase remains a source of occasional ideas (#1280); its mechanical detail is heavier than this campaign needs. Across NoöPunk, a portable layer of tags and graphs describes the people, places and situations that matter in play. **Clue, Social, Goal, Psyche and Astral are the starting tag families.** The list is open: additional families can be named as the campaign develops. Astral Tags cover the Noösphere side of play. Another cyberpunk RPG can supply its own resolution rules for the same authored scenes.

| Starting tag family | What it records |
| --- | --- |
| Clue | Something the investigators can follow up, with its source. |
| Social | A relationship fact that affects an interaction, such as trust, obligation or access. |
| Goal | An outcome a character or faction is pursuing. |
| **Psyche** (formerly Personality) | A character’s inner life: enduring traits, values, fears, habits and temporary states of mind. *Protective of sources* can shape Laura across cases; *shaken after the ambush* can fade as events unfold. |
| Astral | A fact about the Noösphere that affects what someone can perceive, attempt or change. Covers PSI, Magick, psychotronics, panpsychism and Law of One phenomena. |

| Graph | What its connections mean |
| --- | --- |
| Physical | Routes between places the characters can physically reach. |
| Cyber | Network connections between devices and systems. Anchor devices to their physical locations. |
| Story | Relationships and progression among series, episodes and scenes. |
| Social | Ties among people, groups and institutions. A Social Tag can describe what a particular tie means today. |

**At the table:** use the graphs to find who or what is connected, and read the relevant tags to establish what is possible and what matters. When an action calls for a conventional roll, use the host RPG’s procedure. For example, an Astral Tag lets Tony hear a presence name a witness. Record that statement and its source as a Clue. The Social Graph identifies who could introduce him; the Physical Graph tells him where to go. If he tries to recover corroborating camera footage, the Cyber Graph locates the recorder and CWN resolves the hack. The same case can be run under another cyberpunk RPG by using its hacking procedure.

The foundation is decided. Keep this issue open for tag wording, examples and tabletop playtesting. The earlier draft below documents the starting point; its question about adopting tags has now been answered.

---

## The design question

Could a small set of Astral Tags carry the entire Astral layer of NoöPunk? This includes PSI, Magick, panpsychism, psychotronics, the Law of One and other psychic systems. The Astral is central enough to deserve a language that fits this setting. The broader possibility is a game built on Cities Without Number, with tags carrying almost everything else. This issue explores that direction; decisions about other overlays can be made separately.

## A minimal proposal to try at the table

An **Astral Tag** is a short phrase attached to a person, place, device or relationship that says something true in the fiction. When it matters, the player or GM says what it lets someone notice, attempt or change. If the outcome is uncertain, agree on a meaningful choice or consequence in the scene. Add, change or remove a tag only when something lasting happens that the table needs to remember. Start with plain language and the existing tag workflow. Leave ranks, points, power lists and a separate Astral map out of the first playtest.

**Example.** Laura is escorting a witness through Kurvi. The stairwell carries *Someone is still waiting here*. Tony’s implant carries *Picks up abandoned intentions*. Together those tags let Tony recognize a presence expecting a reply. He can keep pace with Laura or stop and answer it. If he stays, the presence might reveal whom it expected; the investigators still have to find and interview that person. Laura and the witness keep moving on the same scene clock. CWN handles a chase or camera hack if either follows.

## Questions for Tomi and the playtest

- Can the same simple procedure handle a fleeting impression, an ongoing relationship such as a Social Memory Complex, and a city-scale psychotronic effect? Which distinctions actually matter in play?
- Who can see a tag, who can invoke it, and who decides what it means? Try leaving an entity’s intention with the GM while giving the player the sensory impression Tony actually has.
- When would an Astral Tag become an ordinary Clue, Social or Goal Tag? Record a clue’s source once so another scene can distinguish an entity’s testimony from independently verified evidence.
- What earlier proposals can be retired if this works? Compare the same encounter using tags and the procedures in #1261. Include one embodied encounter and one brief projection. Keep what creates a meaningful choice or expresses something distinctive about NoöPunk.

Related work: #1164 (scene and tag architecture), #1261 (Astral Body, PSI and overlapping layers), #1280 (optional Eclipse Phase inspiration). This is an author-facing discussion and tabletop experiment. Implementation and migration can follow a design decision.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

Applied the 7 November author decision and merged in #1284 (`fcc86841`).

**Table reference:** `docs/tabletop/TAGS_AND_GRAPHS_1283.md`

It records:

- the five starting families — **Clue, Social, Goal, Psyche (formerly Personality), Astral** — explicitly open-ended;
- the four graphs — **Physical, Cyber, Story, Social** — and what each connection means;
- the table procedure: frame → read graphs → read tags → roll the host RPG only if uncertain → record what lasts;
- the Kurvi example: the stairwell's *Someone is still waiting here* plus Tony's *Picks up abandoned intentions* lets him notice a presence; the presence's statement becomes a **sourced Clue**, while CWN resolves any chase or hack;
- conversion rules: Astral → Clue, clue-as-leverage, repeated behaviour → Psyche; no silent promotion of testimony to verification;
- the boundary with #1261 Astral Body and #1164 scene architecture; **Astral Tags are not an Astral Graph**;
- playtest questions and the implementation map.

**Code:** `PsycheTag` is now the #1283 name for the serialized `PersonalityTag`; `AstralTag` is a descriptive record (owner, fact, optional subject/evidence) with no rank, Effort, modifier or automatic effect. The NPC-side `TagBook` gained `add_psyche`/`psyche_of` and `add_astral`/`astral_of`, preserving the existing `personality` save key. `TAG_FAMILIES` names all five. `NARRATIVE_TAGS_1184.md` now points to the portable reference.

**Tests:** 8 new guards, including the five names, Psyche alias, Astral no-modifier rule, NPC TagBook round-trip, the Kurvi example, links and the register row. Full suite **3242 OK (3 skipped)**; `cwn_parity_audit --check` up to date. No new resolver, PSI rank, Astral Graph or CWN rule change.

Issue #1283 stays open, as the author asked, for tag wording, examples and tabletop playtesting.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

**The decision is in code where it can be, and the page is the table's.** Merged; `main` green at **3,252 tests**.

[docs/tabletop/TAGS_AND_GRAPHS_1283.md](https://github.com/TomiToivio/NooPunk/blob/main/docs/tabletop/TAGS_AND_GRAPHS_1283.md) is the reference — CWN as chassis, five starting families, four graphs, and the worked example from your text. `src/rules/scene_tags.py` carries the portable records; `src/world/narrative_tags.py` carries the richer per-character record.

**What I added beyond the page, because the page left it to prose:**

- **`PsycheTag.duration`** — `enduring` or `temporary`, which is your own distinction: *protective of sources* shapes Laura across cases, *shaken after the ambush* fades. A word, not a timer: nothing expires a tag by itself, nothing rolls for it.
- **`AstralTag.domain`** — `perceive`, `attempt` or `change`, the three your sentence names, and closed on purpose. A fourth kind of claim should be a new family, not a quiet widening of this one.
- **`register_family(name, meaning)`** — the list is open *in practice*: a sixth family joins `TAG_FAMILIES` with a one-line meaning, and an unnamed or duplicate family is refused. "Open" as prose is a promise; this makes it an operation.
- **`to_family_tag()`** — the store's richer record (leverage, behaviour under pressure, taboo) projects onto the portable tag, so a scene carries the short form and the dossier keeps the detail.

`PersonalityTag` remains the serialized class name with `PsycheTag` as the #1283 name in both modules, so older saves and documents do not fork.

**Not implemented, deliberately:** no resolution rules — CWN supplies them and another cyberpunk RPG can supply its own; still **no Astral graph**, asserted by test so adding one becomes a deliberate change; and no answer to the playtest question.

**That question is the one that matters and it is yours:** can one procedure carry a fleeting impression, a Social Memory Complex and a city-scale psychotronic effect — and if not, which distinction earns a mechanic? The two fields I added (`duration`, `domain`) are my guess at the two distinctions that will matter. If playtesting says the real distinction is elsewhere, those are the lines to change.

Keeping the issue open for wording and playtesting, as you asked.
