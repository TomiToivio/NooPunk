# The EP2 → NoöPunk conversion matrix

> **Canonical data:** [`data/rules/conversion_matrix.json`](../../data/rules/conversion_matrix.json).
> This document explains the matrix; it does not restate every row.
>
> **Status:** work package B of issue #60. **Issue #60 is canon.**
>
> **This document records status. It does not decide canon.**

## 1. What this is for

Issue #60 asks for a matrix converting Eclipse Phase 2E into NoöPunk, and asks the
work to be evolutionary: EP2 is the chassis, subsystems get simplified, reskinned or
replaced **deliberately**, with each change written down rather than vanishing into
code or an issue comment.

At the time of writing, 39 boxes in that issue are unchecked and several agents have
landed real work against them. The problem this file addresses is that **nobody could
see the current state** — which EP2 subsystem is inherited, which is half-ported,
which was deliberately dropped, and which is an author decision not yet taken.

So the matrix answers one question per subsystem:

**what is the status of this EP2 subsystem in NoöPunk right now, and how do we know?**

## 2. How to read a row

Each row in the data file carries:

- **`ep2_reference`** — where the subsystem lives in the EP2 rules (chapter and page
  group, from the online rules' own navigation), and `ep2_covered`, which is `false`
  where EP2 has no equivalent at all (most NoöPunk-native architecture).
- **`rulebook_section`** — the section of `RULEBOOK.md` that governs it.
- **`status`** — one of `RULEBOOK.md` §3's five provenance labels, **verbatim**:
  `EP2 BASELINE` / `MODIFIED EP2` / `NOÖPUNK NATIVE` / `EXPERIMENTAL` / `DEFERRED`.
  A sixth value, `NOT YET MAPPED`, exists for the honest case where the EP2 source has
  not been read and recording a status would be fabrication. **No row currently uses
  it**, because every EP2 reference here was read from the online rules.
- **`implemented`** — a **code** verdict, measured by inspecting `src/`, not a design
  verdict. The two are independent on purpose: psionics is *specified* and
  deliberately **not** implemented; the social-science layer is *specified* as
  NoöPunk-native direction and not implemented either.
- **`conversion_target`** — keep / simplify / reskin / replace / expand / defer.
- **`not_implemented`** — the parts of the EP2 subsystem deliberately left out, so a
  later reader does not mistake a partial port for a complete one.

The distinction that matters most: **`status` is the repo's own label, not this
document's opinion.** Where a section header in `RULEBOOK.md` says `EP2 BASELINE`,
the row says `EP2 BASELINE`, even when the code implements only a fragment of it —
and the fragment size is recorded separately under `not_implemented`.

## 3. The current picture

30 subsystems. 21 implemented. Status distribution:

| status | count |
|---|---|
| `EP2 BASELINE` | 16 |
| `DEFERRED` | 6 |
| `NOÖPUNK NATIVE` | 6 |
| `MODIFIED EP2` | 1 |
| `EXPERIMENTAL` | 1 |

**What is inherited essentially unchanged:** percentile roll-under resolution, the
33/66 superior band, critical doubles with 00/99 absolutes, defaulting, the ±60
modifier cap, the four pools and their five common spend manipulations, opposed
tests, character representation as a sheet, and embodiment and inventory as compact
objects.

**What NoöPunk owns outright:** the NPC tiering (scripted and LLM actors coexisting),
the structured-action seam that keeps the LLM out of the mechanics, persistence and
reproducibility, the rules-adapter contract, and the whole setting.

**What is deliberately deferred:** character creation, reputation networks, psionics,
economy, vehicles, advancement.

**The one row worth reading closely is psionics.** The EP2 source is available (ch14)
and the setting is saturated with psi lore — and both `RULEBOOK.md` §16 and the #74
prototype say it stays **mechanically deferred**, because the project expects to
*replace* that subsystem rather than inherit it. Implementing it now would pre-empt an
author decision. The matrix records that as `DEFERRED`, not as a gap to fill.

## 4. The partial ports, stated plainly

Four inherited subsystems are implemented **only in fragment**, and the matrix says so
rather than letting the label imply completeness:

- **Combat** — one attack resolution exists. EP2 ch12 has thirty sections: melee vs
  ranged, five weapon categories, armor, weapon traits and accessories, special
  attacks, vehicle movement. None of that is ported.
- **Mesh/hacking** — one hack action exists. Mesh topology, authentication and
  encryption, apps and links, mesh inserts, online research: not ported.
- **Embodiment** — a compact object exists. The biomorph/pod/synthmorph/uplift
  catalogues, resleeving, forking and merging, backups: not ported.
- **Harm** — harm state and a wound threshold exist. Damage tracks, healing, repair,
  psychosurgery and disorders: not ported.

This is consistent with `RULEBOOK.md` §8: everything beyond the smallest playable
kernel stays deferred until play demonstrates a need.

## 5. What this matrix does NOT do

**It does not resolve the character-layer question.** Two binding documents currently
disagree:

- `AGENTS.md` §4 says the **four-system unified tag model** (Physical / Social /
  Psychic / Cybernetic, attributes as typed tags) is the canonical character
  direction;
- `AGENTS.md` §13.9 and §15, rewritten by #60/#63, make **EP2 the mechanical chassis**,
  and `RULEBOOK.md` §9 declares character identity `EP2 BASELINE`.

Both were written by the author at different times, and deciding between them changes
how characters are represented. That is an author decision. The matrix records the
disagreement in `unresolved_questions` and leaves it open — a matrix that silently
picked a winner would be the same error as editing the tests until they agreed with
whichever document happened to be read first.

**It does not invent EP2 detail.** Every EP2 reference was read from the online rules
site's own navigation, not recalled. Where a subsystem is not implemented and its
source has not been read, the row says so.

**It does not port anything.** This is a map, not a change to the mechanics. Nothing
in `src/` is modified by it.

## 6. How to keep it honest

The companion guard, `tests/test_issue60_conversion_matrix.py`, enforces the
properties a later session would otherwise drift:

- every `status` is one of §3's five labels, spelled exactly (the repo uses
  `NOÖPUNK`, with the umlaut);
- every `rulebook_section` that is claimed actually exists in `RULEBOOK.md`;
- every row marked `implemented` names at least one file that **exists**, and the
  kernel it names actually resolves a check when called;
- the `unresolved_questions` list cannot be emptied silently — the character-layer
  question is asserted to still be recorded as open;
- the count of subsystems cannot silently fall.

When you change a subsystem's status, change it in **both** the rulebook section
header and this matrix, then follow `RULEBOOK.md` §26's rule-change procedure and add
a row to its change ledger. Two sources of truth is how the drift this document exists
to expose actually happens.
