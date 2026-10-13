# NHI Codex: scope record and research status

Status: **scope record for issue [#348](https://github.com/TomiToivio/NooPunk/issues/348).** It defines
no capability, statistic or mechanic for any entity. Per the code-only testing policy (#271) nothing
here is asserted by a test; the executable half is `strategy_game/codex/`, tested by
`strategy_game/tests/test_codex_entities.py` and `test_codex_translation.py`.

## 1. What landed

| Module | Contents |
| --- | --- |
| `codex/entities.py` | `EntityRecord` with the issue's field list, `EntityOntology` (Biologics / Noetics / Plasmoids / Constructs), `EntityForm` (species, polity, organization, avatar, individual, vessel/technology, mythonym), `KnowledgeStatus` (the issue's six registers), `EntityDescriptor` (`RULEBOOK.md` §43.4 extended categories), `ConsciousnessStatus` (the never-derived posture) |
| `codex/codex.py` | `Codex` — lookup by identifier, display name or alias; queries by ontology, form, stage and register; a player-facing projection that withholds GM material |
| `codex/translation.py` | `CommunicationMode`, the `TranslationStage` ladder, `Lexicon`/`Meaning`, `ContactSession`, `machine_candidate`, `signal_variant` |
| `data/codex.json` | 17 entries, all four ontologies represented |

## 2. The three modelling decisions that carry the issue's own constraints

**Ontology is not affiliation.** The issue's central warning is that the four kinds are *not* four
political factions, and that "a Greys' synthetic drone might be a Construct controlled by a
biologic/Noetic operator". So `ontology` (what it is) and `faction_relationships` (who it is bound to)
are independent fields, and nothing derives one from the other. An Orion-aligned Construct is
representable without contradiction.

**A primary category is revisable.** `alternative_ontologies` carries rival hypotheses, and a test
forbids listing the primary among them: the field holds *rival readings*, not a duplicate. `hypotheses`
returns the primary first, then the rivals, so a UI can show "most likely … but also …". The shipped
codex exercises this on the entry the issue itself leaves open — Orbs of Light, whose primary reading
is Plasmoid with Noetic and Construct alternatives.

**GM-only material is withheld by the code, not by a template.** `Codex.player_records()` filters out
GM-only entries and `player_view()` drops every `gm_secrets` value. A test asserts that no GM secret
present in the shipped file survives in `player_payload()`, so the issue's "do not spoil GM-only truths
in player UI" is a property of the code rather than a promise about a renderer.

Two smaller ones: the translation lexicon has **no method returning a single translation** (a test
asserts the absence, because ambiguity *is* the dramatic content), and a value present in a record but
unrecognised **raises** rather than falling back to a default — a typo must not load as a plausible
classification that looks deliberate. That contract caught four of my own data errors while writing
the file.

## 3. What this unit does NOT do

- **No capability, statistic or effect.** `AGENTS.md` §4 reserves "NHI taxonomy or capabilities"; this
  is the record layer a later approved subsystem reads from. The issue's own line applies — gameplay
  consequences such as diplomacy or research unlocks belong to the strategy layer.
- **No conlang and no linguistics engine.** The issue requires neither for the MVP; the translation
  model is a game model of partial understanding, with display-confidence labels rather than
  probabilities.
- **No join to `WorldState`.** Gate D again, as on #347.
- **No species taxonomy beyond the four kinds.** Where the issue says "avoid overdefining mysterious
  entities", the record keeps alternatives and leaves the question open rather than resolving it.

## 4. Research status, per claim

The issue's work items include genuine research tasks. Being explicit about what is and is not
verified, because a recalled claim and a sourced one must not sit unlabelled beside each other:

| Claim in the codex | Status |
| --- | --- |
| The four ontologies, the reveal order (orbs / metallic spheres / Pleiadian delegates first, the flagship later), the candidate pool, the Q'uo composite, Ra's post-biological status, the Merkabah-as-vehicle correction, MIB as Noetic rather than a species, the Pascagoula vegetal/Sirius/fusion attribution being **NoöPunk invention** | **Transcribed from the issue body.** The author's own candidates and corrections; no independent verification claimed. |
| "Confederation" is a historical human exonym rather than the UCCC's official name | **Author ruling, implemented.** The issue locks the bloc names; a test asserts the old label appears only as an exonym. |
| L/L Research source names (Hatonn, Latwii, Laitos, Oxal, Q'uo) and their group-versus-species relationships | **NOT independently verified.** The issue's work item asks to check these against the L/L Research transcripts. The codex records Ra and Q'uo only, at `source_mythology`, with the archive cited as a reference. **The transcript verification is still open.** |
| Pascagoula witness-described morphology | **NOT independently verified.** Recorded as `reported_claim` with the 1973 accounts cited as public ufology archives. |
| The Bennu-inspired avian lineage, the Maldek survivor civilisation, the mycelial and cephalopod candidates | **Author-labelled creative options**, recorded as `rumour`/`source_mythology` and explicitly not history. |

The remaining research work items — the L/L transcript pass, the ufology morphology check, the
mythology spelling and category inventory — are **open**, and they are content work: author-reviewed,
not testable.

## 5. Open questions for the author

1. **The reveal stages are free text.** No stage vocabulary is imposed, because inventing one would be
   inventing a typology. The issue names three waves (initially common / gradually / the flagship
   later); if those are the stages, they should be declared once and the entries re-tagged.
2. **Which `KnowledgeStatus` values the shipped entries should carry.** They are set from the issue's
   own framing — the two blocs as `canon`, the common trio as `player_known`, myth-derived entries as
   `source_mythology`, witness cases as `reported_claim`, MIB as the single `gm_truth`. That reading is
   mine and is a one-line change per entry.
3. **The flagship species.** Three candidates are in the file (avian, mycelial, cephalopod); the issue
   asks to select from research and playtesting, and the selection is not mine.
4. **The lexicon's confidence vocabulary.** Low/medium/high is a display convention I chose, not an
   approved scale.
5. **The translation scene prototype's board consequences.** The issue wants "a single translation
   scene and failed interpretation with explicit alternative meanings, research/skill choices and
   board consequences". The data model supports it; the scene needs the strategy layer's rules
   (Gate C) and the skill-check procedure (Gate A).

## 6. What the second pass added (2026-10-13): descriptors, the consciousness posture, the polity fix

Three gaps the first pass left open are now closed as **structure, validation and code-only tests** — no
mechanic, no statistic, no new canon:

1. **The `RULEBOOK.md` §43.4 extended descriptors** are carried as `EntityDescriptor` /
   `EntityRecord.ontology_descriptors`: Process, Ecology, Assemblage, Collective, Geotic,
   Hybrid/Composite, Anomaly/Unclassified. They are a *second, non-exclusive* axis on top of the primary
   ontology, because §43.4 says "some are better treated as cross-cutting descriptors than as formal
   classes". `Codex.by_descriptor()` queries them.
2. **The consciousness posture** is `ConsciousnessStatus` on the entity record, sharing the vocabulary of
   the already-merged character-card layer (`unknown` / `contested` / `asserted_in_world`), defaulting to
   `unknown` and **never derived** — no method returns a boolean, and an in-world assertion needs a cited
   source (`rulebook/6_PSYCHIC.md` §6.7.3). The plasmoid entries carry `contested`, on their own
   "unresolved" text, so a plasmoid's physical existence stays a different question from its consciousness.
3. **The ontology-on-a-polity inconsistency** is reconciled: `EntityRecord.ontology` may now be **absent**
   for a faction form (`polity`/`organization`), recorded as an explicit `null` with a stated
   `ontology_absent_reason`; a body form may not omit its substrate, and an omission without a reason is
   refused. `uccc` and `orion_sphere` now record the absence (their own `biology_or_substrate` reads
   "not applicable"), so the type/faction collapse §43.4 forbids is gone. `djinn` keeps its single
   dominant substrate as §43.3 permits.

The translation model also gained `LOAD_BEARING_SIGNIFIERS` — the issue's own pragmatics list
("gift", "weapon", "we", "voluntary", "service", "harvest", "ownership", "individual") — as the declared
set `EntityRecord.referent_collisions` names when an entity expresses one non-equivalently (the UCCC
"we", a metallic sphere's "individual"). Misunderstanding is already a *state*, not a failure: the ladder
never moves backwards, so a falsified reading closes a hypothesis while the entity stays open (§16.4).

### PENDING — author rulings this pass did **not** make

- **Whether a §43.4 descriptor becomes a formal `EntityOntology` value.** §43.4 names Process as "the
  strongest candidate for an additional formal class"; the structure makes that decision expressible and
  does not pre-empt it.
- **Whether a phenomenon/manifestation gets its own `EntityForm` value or a typed status field.**
  `EntityForm` is unchanged (no `phenomenon` value was invented); the record now carries a free-text
  `entity_status` so "phenomenon" or "not an entity" can be recorded without a locked taxonomy.
- **Which entries carry which descriptors, and which carry `referent_collisions`.** Three descriptor
  assignments and two referent collisions are populated from the entries' own text; the rest are the
  author's.
- The **flagship species**, the **reveal-stage vocabulary**, the **confidence vocabulary** and the
  **translation scene's board consequences** (Gates A and C) remain open, as in §5 and §4.
