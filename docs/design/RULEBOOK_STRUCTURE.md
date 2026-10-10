# Rulebook structure: how the parts work (for agents)

Written for other agents working on the #200 / #217–#232 subsystem issues. Read this before
editing `RULEBOOK.md` or anything under `rulebook/`.

## The short version

| File | Status |
| --- | --- |
| `RULEBOOK.md` | **Canonical, and the file to edit.** 6108 lines, 64 headings. |
| `rulebook/00_INDEX.md` | Generated navigable index. Links every section to its part. |
| `rulebook/parts/*.md` | Twelve **generated, verbatim segments** of `RULEBOOK.md`. Do not hand-edit. |
| `data/rules/rulebook_split_manifest.json` | Frozen SHA-256 of every section body. The proof nothing was lost. |
| `tools/split_rulebook.py` | Regenerates all of the above. |

**Edit `RULEBOOK.md`, then run `python3 tools/split_rulebook.py --apply` in the same commit.**
If you edit `RULEBOOK.md` and do not regenerate, `tests/test_issue232_rulebook_split.py` fails with
that instruction. If you hand-edit a part, the same guard fails and names the section.

## Why the parts are generated rather than the rulebook being cut up

The obvious move — move each section's body into a part and leave `RULEBOOK.md` as an index — was
tried first and **it failed 309 tests**. The suite reads `RULEBOOK.md`'s *body*, not merely its
headings. Rewriting 309 tests would have been the largest possible risk to the content this work
exists to protect, and "do not lose anything" was the explicit requirement.

So the direction is reversed. `RULEBOOK.md` stays canonical; the parts are a navigable view. The
whole diff to `RULEBOOK.md` is **7 added lines and 0 removed** — the navigation block — which is
checkable with `git diff`.

## The shape guards you must not break

Three tests constrain `RULEBOOK.md`'s structure, and all of them are about cross-references:

1. **`test_issue101_sources_dedup::test_top_level_numbering_is_contiguous`** splits the file on the
   literal marker `# Extended canon and reference material` and requires `## 1.`–`## 9.` before it
   and contiguous `## 1.`–`## N.` after it.
2. **`test_issues171_180_cross_references`** builds the §-reference *universe* from RULEBOOK.md's
   headings plus each self-numbering `rulebook/*.md` chapter. Every `§N` anywhere must resolve
   against that union — so a heading deleted from `RULEBOOK.md` silently orphans references.
3. The same guard requires every self-numbering `rulebook/*.md` to be **linked from
   `RULEBOOK.md`**. That is why the navigation block exists at all: `00_INDEX.md` self-numbers.

`rulebook/parts/` is deliberately one level down, because `rulebook/*.md` is globbed by guard 2 —
putting twelve generated parts in that glob would impose self-numbering and link requirements on
all of them for no benefit.

## The two numbering runs — a real finding, not a bug to fix silently

`RULEBOOK.md` contains **two independent `## N.` runs**:

| Run | Lines | Sections | What it is |
| --- | --- | --- | --- |
| core | 2–650 | `1`–`9` | The current rulebook: Stats, Skills, the four domains, Character Generation. |
| extended canon | 651–6108 | `1`–`54` | A preserved reference ledger, including the 1816-line world-lore section. |

So `RULEBOOK.md §51` unambiguously means the extended-canon harm ladder, and `§5` is *ambiguous*
between core "Physical Systems" and ledger "Primary Eclipse Phase references". The contiguity guard
asserts the two runs separately, so this is **deliberate and guarded** — not drift.

#232's first acceptance criterion asks for "no conflicting rules definitions". Reconciling these
two runs means choosing which is canonical and renumbering one of them, which would break an
unknown number of `§N` cross-references across the repository. **That is an author/design decision,
not an agent's**, so it is reported here and left alone.

## Working on a subsystem issue (#217–#232)

Each subsystem issue maps onto one or two parts:

| Issue | Part(s) |
| --- | --- |
| #217 core resolution | `01_basic_rules`, plus `src/rules/kernel_prototype.py` |
| #218 character creation | `02_character_generation`, `09_characters_and_beings` |
| #219 physical / combat | `03_physical_systems` |
| #220 social | `06_social_systems` |
| #221–#222 cyber, cyberspace | `04_cybernetic_systems` |
| #223–#224 psychic, astral | `05_psychic_systems` |
| #226 UNSA investigations | `10_campaign_unsa_factions` |
| #227 transhuman / NHI / NPCs | `09_characters_and_beings` |
| #228 equipment and economy | `04_cybernetic_systems`, `12_glossary_sources_catalogs` |
| #229 narrative layer | `src/rules/aspects_prototype.py` (see below) |
| #230 OSR / GM toolkit | `10_campaign_unsa_factions`, `11_concordia_and_parity` |
| #231 CC publication | `data/sources/game_system_rights.json` |
| #232 this structure | all of the above |

Existing prototypes you should build on rather than duplicate:

- `src/rules/issue200_resolution_lab.py` (#207) — exact odds on the raw scale.
- `data/rules/fudge_scale_migration.json` (#213) — the **author-directed** 1–10 → −3..+3 mapping.
  Consume it; do not re-declare it.
- `src/rules/kernel_prototype.py` (#209/#215) — candidate combination rules on the ladder.
- `src/rules/aspects_prototype.py` (#233) — aspects, narrative resource, consequences.

## Rules that apply to every change here

- **`AGENTS.md` is the canonical contract** and `docs/archive/DESIGN_PRINCIPLES.md` the design
  invariants. There is no automated build gate on this: documentation tests were removed under #270/#271, and agreement between these documents and the binding invariants
  disagree — including a check that the AGENTS.md `§13.2` pole sentence matches the canonical
  document (see issue #200 and PR #214).
- **New numeric values are DRAFT** until the author calibrates them. Say so in the docstring.
- **Deterministic and auditable**: rolls and state transitions belong in code with tests, never in
  an LLM prompt.
- **No invented lore or rules.** `AGENTS.md` §4 reserves unspecified numbers, factions and
  technologies to the author.
