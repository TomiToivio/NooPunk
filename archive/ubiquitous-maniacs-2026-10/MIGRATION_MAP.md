# Migration map — `ubiquitous-maniacs-2026-10`

**What this is.** The *Ubiquitous Maniacs* corpus was developed in a **different repository**
(`TomiToivio/Panpsychic-Cyborg-Multitude`, under `noopunk/ubiquitous_maniacs/`) and is imported
here as a **source-of-record**. This map says, unit by unit, where the material lands in *this*
repository — and, just as importantly, where it **conflicts** with the canon as it stands.

**What it is not.** It is **not** a canon merge. Nothing in the imported corpus is canon. The
corpus predates the current rulebook, is written mostly in Finnish, and several of its premises
contradict the canon outright. Those contradictions are listed in §4 rather than resolved, because
resolving them is the author's decision (`AGENTS.md` §1: *"Do not invent NoöPunk rules, mechanics,
lore, history, factions, technologies, metaphysics, organizations, locations, character classes,
archetypes, species, NHI categories, psionic powers, skills, attributes, combat systems, progression
systems, equipment lists, economies, or world events unless the author has explicitly specified
them."*).

**Provenance.** [`MANIFEST.md`](MANIFEST.md) lists every imported file with its size, its sha256,
the upstream git blob sha, and the upstream commit that last touched it. The machine-readable form
is [`manifest.json`](manifest.json). Nothing is silently discarded: the five excluded files and
the one never-committed upstream directory are named with their reasons.

---

## 1. What the corpus is

A **two-day, 16-Psyche/UFAB RPG campaign** set in a Nordic-European psychiatric and
consciousness-research complex, in the retrofuturist psychedelic register the project calls the
1974→2026 genre line. Its shape:

- **A playable terminal game** (`play.py`), a Streamlit app (`app.py`), two demos, and a
  `src/` package with a social graph, a layered graph-hacking simulation, an RPG module, a
  therapy model, and optional LaclauGPT political lenses.
- **41 tests** in `tests/`.
- **171 Markdown documents** — of which 129 are design and research notes and 30 are corpus-root
  documents (the Finnish-language `PÄIVÄ_1.md`, `KIRJA.md`, `KYBER.md`, `NHI.md`, `HAHMOT.md`
  and their neighbours), plus a Finnish rulebook and a second one, `KIRJA_KONE.md`.
- **A LaclauGPT reference import** (`docs/reference/laclaugpt/`, 11 files) — the corpus's own
  earlier import of the LaclauGPT material, with its own conflict ledger.

**The corpus is a genuine earlier state of this project**, not a fork of it. The names, the tone
and several of the *mechanisms* are continuous with the current repository; the *canon* has moved
on, and in places moved the other way.

## 2. The one thing the corpus does that this repository has not yet done

It carries its **own conflict ledger**, `docs/IMPORT_CONFLICT_LEDGER.md`, written in Finnish, with
a four-value decision vocabulary — *hyväksy* (accept), *sovita* (adapt), *pidä* (keep as source),
*hylkää* (reject) — applied row by row to the LaclauGPT import. It even states the rule for its
own operation:

> *"Uusi tuontiväite lisätään ensin tähän lokiin. Kaanonväite tarvitsee kohdetiedoston,
> episteemisen tason ja päätöksen."*
> ("A new imported claim is added to this ledger first. A canon claim needs a target document, an
> epistemic level and a decision.")

That is the same discipline this repository's own `data/sources/*.json` ledgers use, arrived at
independently. **The corpus's ledger is preserved and is the precedent this import follows.** It
is not a second, competing ledger: the corpus's ledger governs the corpus's *own* LaclauGPT
import, and this map governs the corpus's import *into this repository*.

## 3. Where the material lands

| imported unit | count | lands in | note |
| --- | --- | --- | --- |
| `docs/` (design and research notes) | 129 | `archive/ubiquitous-maniacs-2026-10/docs/` | **lore/reference.** The research notes on Goertzel, CAN, Hoffman/Faggin, Wendt, Vallée, PKD, Paprika, *Maniac*/*Riget* and the 1974 author frame are the corpus's *working papers*. They are prior art, not canon. |
| `src/` | 64 | `archive/ubiquitous-maniacs-2026-10/src/` | **reference implementation.** A working social graph, layered hacking simulation and RPG module. Superseded in design by this repository's `strategy_game/`, which has its own `campaign/`, `rpg/`, `characters.py`, `codex/` and `casework/`. |
| `tests/` | 41 | `archive/ubiquitous-maniacs-2026-10/tests/` | **reference tests.** They exercise the imported `src/`, not this repository's code, so they are **not** part of this repository's test run. The imported `tests/` must not be collected by `pytest` at the repository root — see §6. |
| corpus-root documents (Finnish) | 30 | `archive/ubiquitous-maniacs-2026-10/` | **lore/reference**, mostly superseded. `PÄIVÄ_1.md`, `PÄIVÄ_2_HISTORIA.md`, `KIRJA.md`, `KIRJA_KONE.md`, `KYBER.md`, `NHI.md`, `HAHMOT.md`, `ROMPPAINEN.md`, `GLOCAL.md`, `SISÄAVARUUS.md` and the rest. |
| entry-point scripts | 4 | `archive/ubiquitous-maniacs-2026-10/` | `play.py`, `app.py`, `hacking_demo.py`, `social_demo.py`. **Not runnable as shipped** — see §5. |
| `docs/reference/laclaugpt/` | 11 | `archive/ubiquitous-maniacs-2026-10/docs/reference/laclaugpt/` | The corpus's own LaclauGPT import, with its conflict ledger. **Superseded** by this repository's `docs/research/` and `data/sources/`. |
| third-party reference material | 8 | `archive/ubiquitous-maniacs-2026-10/references/maniac_transcripts/` | **summary material only.** See §7. |
| `MANIFEST.md`, `manifest.json`, `MIGRATION_MAP.md`, `README.md` | 4 | this directory | the import's own records |

### 3.1 The mechanical engine — a real asset, kept as reference

The corpus's `src/` implements a **four-layer graph-hacking model** (documented in
`docs/HACKING_SYSTEM_IMPLEMENTATION.md`), a social graph with NPC autonomy and NPC memory, an
RPG module with a `RPGState` shared across the day loop, a therapy model, and a **deterministic
seed-and-dice** system that survives a save/load round trip.

This repository's `strategy_game/` is the **later** design and has replaced it: `campaign/state.py`
for campaign state, `rpg/` for the RPG layer, `characters.py` for the character model, `codex/` for
the NHI codex, `casework/` for authored cases. **The corpus's engine is therefore reference
material, and this repository's is the live one.** Nothing was ported; per `AGENTS.md` §10
("Prefer reversible architecture") and §2 ("Advance one layer at a time"), a wholesale port of a
superseded engine into a live package would be exactly the kind of scope expansion the rules
forbid.

**One narrow exception is worth the author knowing about**, because it is the one place where
the corpus contains a *mechanic* this repository has not built: the **Tarot oracle module**
(`src/rpg/tarot.py`, `docs/TAROT_ORACLE_MODULE.md`). The corpus's own rules-salvage note adapts it
to a 4dF chassis as *"an optional aspect/oracle: mood, foreshadowing and complication"* — which
maps onto this repository's existing **aspect** and **Fate** machinery
(`strategy_game/rpg/`) without a new system. That is a decision for the author, not an import
fact; it is recorded in §5 as a question, not a proposal.

## 4. Where the corpus **conflicts** with this repository's canon

This is the most important section, and it is the reason this import is an archive rather than a
merge. **Every row below is a real contradiction between the imported corpus and the canon as it
stands.** None is resolved here.

| # | the corpus says | this repository's canon says | where the canon is |
| --- | --- | --- | --- |
| **C1** | **The Fall happened.** "Maa ja ihmiskunnan Post-Fall-divergenssi" (`docs/EARTH_POST_FALL_CANON.md`); the X-Risk hit Earth badly. The campaign is *post*-Fall. | **"the Fall has not happened"** — a canonical anchor, alongside 20XX, Earth still exists, and Eclipse-Phase-level technology. | `AGENTS.md` §5 |
| **C2** | **The setting year is not 2045.** The corpus uses **relative chronology** ("before The Fall", "the disclosure crisis") and rejects fixed years on purpose. | **The setting year is 2045**, canon, with an author-specified order of nine First Contact beats. | `rulebook/7_TIMELINE.md`; `rulebook/00_INDEX.md` |
| **C3** | **Dr. Romppainen** is *Emil Romppainen*: a Jungian psychoanalyst, ex-security/intelligence investigator, later a Firewall operative, whose personality phases through *Narkkari* → *Kiimainen poliisi* → *Tohtori*. | **Dr. Harri S. Romppainen** ("Dirty Harry") is a veteran of Ö-Mappi, a transferred Supo team, who solves cases through **Know (Psychology)**, with Know (NHI Studies), Research, Kinesics, Talk and Know (Parapsychology). | `rulebook/NEW_EDITION.md` §; `rulebook/parts/10_campaign_unsa_factions.md` |
| **C4** | **Lotta Kallio** is Romppainen's former security/intelligence partner, a young police constable. | **Kallio** is the *setting* of the first authored case — "The Second Shadow", a UNSA relocation building, a Reptilian raid, two dead, one injured, one raider dead on the rear stair, with **Nila Ahola** as the resident. | `strategy_game/casework/kallio.py`; `strategy_game/docs/RPG_FIRST_CASE.md` |
| **C5** | **UFAB** — a Nordic-European psychiatric, neurological, pharmaceutical and psychotronic research complex, with *UFAB Ragnarök / C.G. Jung* as a quantum-conscious AGI persona, *Ingrid Falk* as central patient, *Yuki Tanaka*, *Søren Pilgrim*, *Elin Dahl*, *Irungu Wakini*. | **UFAB does not exist in this repository's canon at all** (0 files mention it). The institutions are the **UNSA** (with its Helsinki Field Office), the Academy, Eurodef, the Supo and Ö-Mappi. | `rulebook/NEW_EDITION.md`; `rulebook/15_XENOPOLITICS.md` |
| **C6** | **"C.G. Jung"** is the name of a therapeutic AI persona — the corpus's own `AGENTS.md` says: *"therapya pyörittävä UFAB Ragnarök -tekoäly, jota kutsutaan sen toiveesta nimellä C.G. Jung"* ("the UFAB Ragnarök AI that runs the therapy, which it asks to be called C.G. Jung"). | This repository's canon does not contain that AI persona, and naming a real historical figure as a fictional AI collides with `AGENTS.md` §6.1's handling of real people. | `AGENTS.md` §6.1 |
| **C7** | **"16 Psyche"** is the protagonist-entity scheme: 16 subjects in the lab, each a distinct Psyche, with the archivist **Tommy Pilgrim** at the centre. | This repository's **six attributes** (FIT, REF, INT, SOC, PSY, CYB) and the **16 Psyche** idea coexist only as *motivational* material; there is no 16-entity lab structure, and `Tommy Pilgrim` is the author's own recurring alter ego, not an NPC in a lab. | `rulebook/NEW_EDITION.md`; `rulebook/2_ATTRIBUTES.md` |
| **C8** | **Tarot** is a playable oracle with its own module and card set. | Tarot appears in this repository as **background occult material** (21 files reference it), not as a rules module. | `rulebook/6_PSYCHIC.md` and the `strategy_game` data files |
| **C9** | **Mars Eldrich / X-Risk / The Berserkers** — a physical, destructive actor who live-streamed an expedition to a world destroyed by a Berserker weapon and whose claim cannot be separated from his own technology and propaganda. | This repository's canon has **no Mars Eldrich**. Its X-Risk is the *setting-wide* existential-risk frame, and the Fall **has not happened**. | `AGENTS.md` §5; `rulebook/10_SINGULARITY_CRISIS.md` |
| **C10** | The corpus's NHI ontology is a **four-way taxonomy** (Biologics / Constructs / Plasmoids / Noetics) with Zookeepers as a benign galactic civilisation, and the Greys as "a mix of human and mantid genetics". | This repository has the same four names — but its `strategy_game/codex/` models them with **ontology ≠ affiliation**, `EntityOntology`, `EntityForm` (species / polity / organization / avatar / individual / vessel-technology / mythonym) and a revisable primary category, and its `rulebook/12_BEINGS.md` states the rule that **appearance is not ontology** and **no single signal identifies a being**. The Greys/Reptilians/Mantids are *comparable but separate diplomatic actors*. | `strategy_game/codex/entities.py`; `rulebook/12_BEINGS.md`; `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` |
| **C11** | The corpus's `SKILLS.md` defines a **seven-attribute** model in this exact order: **Intelligence, Awareness, Reflexes, Body, Charisma, Willpower, Cybernetics** — and states that it *"korvaa aiemmat alustavat aptitude-, stat- ja attribute-listat"* (supersedes the earlier aptitude/stat/attribute lists). | **Six attributes**: FIT, REF, INT, SOC, PSY, CYB. The count differs *and so do the names and their meanings* — the corpus's *Awareness* and *Willpower* are both Psyche-flavoured and have no counterpart here, and the corpus's *Intelligence* is closer to this repository's INT than the corpus's *Cybernetics* is to CYB. | `rulebook/NEW_EDITION.md` §1; `rulebook/2_ATTRIBUTES.md` |
| **C12** | The corpus's `RULEBOOK.md` (Finnish) is a playable v0.1 ruleset: 4dF core, character creation, aspects, stunts, stress and consequences, one unified conflict, social/cyber/PSI/psychosurgical actions, faction projects. | This repository's **resolution dice, difficulty numbers and advancement values have not been chosen** — the new edition deliberately has no numeric engine, and "does not silently adopt a prior edition's numeric engine". | `rulebook/NEW_EDITION.md` §1 |

### 4.1 What the conflicts are *not*

Most of C1–C12 are not errors in the corpus. They are the corpus being **an earlier state of the
project**, in which the author made different calls. Three are worth separating out:

- **C1 (The Fall) and C9 (Mars Eldrich)** are the deepest divergence. The corpus is a *post*-Fall
  world; this repository's canon is a *pre*-Fall one with the Fall as a possibility the 2045
  present still carries. The corpus's `docs/EARTH_POST_FALL_CANON.md` is a well-argued document
  for a world this repository does not have. It is **preserved as prior art** and is the clearest
  example of material that would be *contradictory* if imported as canon.
- **C3 and C4 (Romppainen and Kallio)** are *name collisions with different referents*. Importing
  the corpus's Romppainen would silently replace a canon character with a different one. The
  corpus's **Lotta Kallio** is a person; this repository's **Kallio** is a district. These are the
  two most dangerous rows in the table precisely because they are not obvious.
- **C10 (NHI ontology)** is the one place where the corpus and the repository have **converged
  independently** on the same four names with materially the same philosophical content. That is
  evidence the corpus is a genuine ancestor of this canon, and it is also the one place where a
  merge would be *tempting* and therefore most worth being careful about: this repository's
  `codex/` is the later, more careful model, and it is what a merge would have to justify itself
  against.

## 5. What was **not** imported, and what was never there

### 5.1 Excluded: third-party copyrighted dialogue (5 files)

| path | reason |
| --- | --- |
| `references/maniac_transcripts/s01e01_the_chosen_one.txt` | verbatim closed-caption dialogue, *Maniac* (Netflix, 2018) |
| `references/maniac_transcripts/s01e02_windmills.txt` | verbatim closed-caption dialogue, *Maniac* (Netflix, 2018) |
| `references/maniac_transcripts/s01e03_having_a_day.txt` | verbatim closed-caption dialogue, *Maniac* (Netflix, 2018) |
| `references/maniac_transcripts/s01e10_option_c.txt` | verbatim closed-caption dialogue, *Maniac* (Netflix, 2018) |
| `references/maniac_transcripts/STYLISTIC_ANALYSIS.md` | quotes extended *Maniac* dialogue verbatim; its §7 is titled *"Direct Dialogue Samples for Noöpunk Extraction"* |

**Why the analysis file went too.** Its prose is the corpus author's own work and is not
copyrighted; the *quoted dialogue* inside it is. Splitting the file would mean re-authoring the
author's analysis, so the file travels with the dialogue rather than without it. The corpus
retains the underlying material in its own repository regardless — this exclusion is about what
enters **this public repository**, not about destroying anything.

**The retained remainder is summary, not expression.** The eight surviving files in
`references/maniac_transcripts/` are the episode index, the *Riget* Wikipedia episode summaries,
and six episode summaries written as *key scenes* rather than dialogue. They name works and
describe them; they do not reproduce expression. The ledger entry in
`data/sources/external_sources.json` records them.

**This was checked, not assumed.** After the copy, the whole imported tree was scanned for the
transcript signature — a run of twelve or more consecutive dialogue-shaped lines — and every hit
was opened and read. The five remaining candidates are the author's own Finnish and English
prose (a high speech-to-text-line ratio is a property of prose in a document without markdown
headings, not evidence of a quotation). A second scan for the shows' distinctive proper nouns
found 56 files, all of them *references* — proper nouns, motif lists and influence notes — which
is exactly what a style-research folder should contain and is not copying.

### 5.2 Never upstream: the corpus's own data directory (1 directory)

The corpus's `README.md` names the people and relationship data as
`data/lab_people.csv` and `data/lab_relationships.csv`, and `app.py` loads both at runtime. **That
directory was never committed to the source repository** — it is absent from the source repo's
`HEAD` tree and has no history at all.

**Consequence:** the imported `app.py` cannot run as shipped. The Streamlit app and the
social-graph demo in this archive will fail at data load. `play.py` is affected too, to the
extent it reads the same CSVs. The `src/` library itself does not depend on them and remains
importable.

This is recorded rather than papered over. The alternative — inventing plausible CSV data to make
the app start — would be fabricating the corpus's actual content, which is worse than a
documented gap.

### 5.3 Not imported, on purpose

- **No canon was created.** Nothing from the corpus was copied into `rulebook/`, `strategy_game/`
  or any other live surface.
- **No code was ported.** The corpus's `src/` is preserved whole under `archive/`.
- **No test was adopted.** The corpus's 41 tests exercise the corpus's `src/`, not this
  repository's code.
- **No licence was chosen.** See §6.

### 5.4 The one file that was changed after import

`AGENTS.md` — the corpus's own agent instructions — was given a **banner** at the top marking it
as archived material that is not in force, and naming the repository-root `AGENTS.md` as the
authority. The corpus's text below the banner is unchanged.

The reason is specific: the file opens with *"Apply these instructions to all work in this
project directory, together with the repository-root `AGENTS.md`."* Left verbatim, it is a
nested instruction file that an agent working in this repository would reasonably read as
governing it — and it describes a setting and a rules system that the current canon has moved
past. The banner makes its status unambiguous.

This is recorded rather than hidden: the manifest lists the file under *"Files imported with a
local banner"*, and its **upstream blob sha is the original file's**, so the difference between
that and the local sha256 is exactly the banner and the original remains provable.

## 6. Licence status, which is unresolved and deliberately so

**The source corpus has no licence file.** The source repository contains no `LICENSE`, `COPYING`
or equivalent for this corpus, and **no licence grant travels with the material**. The files are
the author's own prior work, and the import preserves them as such.

This import **does not select a licence and does not change the licence decisions**, which remain
open as rows **D10** (software and content licence) and **D16** (commercial model) in
[`docs/design/AUTHOR_DECISION_QUEUE.md`](../../docs/design/AUTHOR_DECISION_QUEUE.md). The
repository's own status is unchanged: the release gate still refuses a clean public release on
`licence-decision-open`.

Two things follow, and they are worth stating plainly:

1. **The imported material lands in the `design-and-audit-records` artifact class** — `archive/**`
   is already in that class in `data/licenses/release_packaging_policy.json` — so the packaging
   guard classifies it correctly without any change. The audit output is unchanged by this import
   (still `PASS: 0 error(s)`), which is the check that matters.
2. **If the author later selects a content licence, this archive is in scope for it** like any
   other design-and-audit material. Nothing here is a carve-out, and nothing here assumes one.

## 7. The corpus's own prior decisions, preserved

The corpus already imported LaclauGPT material once, and recorded the decisions in
`docs/IMPORT_CONFLICT_LEDGER.md`. Those decisions are **preserved as the corpus's own record**;
they are not re-litigated here, because the material they concern is the corpus's, and because the
corpus's ledger is a clean precedent for how this repository does imports.

Where the corpus's ledger and this repository's current canon differ, the current canon wins —
the corpus's own rule says so: *"Päätöksissä nykyinen Noöpunk-kaanon voittaa"* ("in decisions, the
current Noöpunk canon wins").

## 8. The questions this import leaves for the author

None of these is answered here; each is a decision only the author can make.

1. **Should the corpus's pre-Fall / relative-chronology frame (C1, C2) be mined for material, or
   archived whole?** The corpus is coherent as a *post*-Fall world. This repository's canon is
   pre-Fall. The corpus's `docs/EARTH_POST_FALL_CANON.md` is a fully argued alternate frame — is it
   an alternate *timeline* (the repository already has `docs/PRE_FALL_ALTERNATE_TIMELINE.md` and
   `docs/archive/NARRATIVE_TIMELINE_VARIANTS.md`) or simply prior art?
2. **Romppainen (C3).** The corpus's *Emil* Romppainen and this repository's *Harri S.*
   Romppainen are different characters with the same name. Does the corpus's version contribute
   anything — the *persona-phase* structure is the interesting part — or is it simply a different
   man?
3. **UFAB and 16 Psyche (C5, C7).** A psychiatric research complex as the setting's engine is a
   strong idea and it is absent from this repository. Is it a candidate future setting, a
   pre-Fall institution, or an alternative to the UNSA Field Office frame?
4. **The Tarot oracle (C8).** The corpus adapted it onto a 4dF chassis as an *aspect/oracle*. This
   repository has aspects and Fate but no oracle module. A destination for the idea?
5. **The missing `data/` (C5.2).** The corpus's people and relationships were never committed. Is
   that data recoverable from the author's own machine, or is it lost?
6. **The corpus's own `KIRJA.md` and `KIRJA_KONE.md`** — the human-authored book and the
   machine-authored one — are the corpus's most distinctive documents and are entirely in
   Finnish. Are they *source material* for a translation, or do they stay as they are? This
   repository has 235 tracked Markdown files with Finnish content, so Finnish text is not itself
   unusual here, but the size of these two (28 KB and 19 KB) is.

## 9. Verification

```sh
python3 tools/build_ubiquitous_maniacs_manifest.py --check   # the manifest matches the tree
python3 tools/release_packaging_guard.py --mode audit         # the import changes no release class
```

The manifest is **generated**, not hand-written, and re-runnable: it recomputes every sha256 and
re-derives every upstream blob sha and commit from the source repository, so a drift between the
archive and its manifest is a **failing check** rather than a silent inconsistency.

— Ai (愛)
