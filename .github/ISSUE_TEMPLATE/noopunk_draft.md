---
name: NoöPunk rules/scenario draft (child of #814)
about: One Tomi-authored draft, implemented in tabletop and Godot
title: "draft: <one section or scenario>"
labels: ""
---

<!-- Child issue of the permanent meta-issue #814. One draft, one section, one PR. -->

## The draft

<!-- Paste Tomi's draft verbatim. Do not summarise it, do not "improve" it in place. -->

## Scope of this child task

- Section covered:
- Explicitly **not** covered:

## Decisions the implementation must honour

<!-- Agents fill this in BEFORE writing code or prose. One line per decision the draft makes. -->

1.

## Ambiguities and the reading taken

<!-- Every place the draft is silent or self-conflicting, with the option each reading implies.
     Behaviour-changing ambiguities wait for Tomi; the rest are recorded with the reading taken. -->

| ambiguity | readings | taken | why |
| --- | --- | --- | --- |

## Deliverables

- [ ] Tabletop: `rulebook/<chapter>` or `scenarios/<id>` updated, with CWN/SWN baseline references
- [ ] Contract: `data/rules/*.json` (+ `src/rules/` layer of record) where numbers are involved
- [ ] Godot: kernel in `godot/core/` and its call sites, in the single canonical tree
- [ ] Tests: Python contract, Godot behaviour, and the shared worked example (tabletop ↔ Godot)
- [ ] Departures from the draft and open questions recorded below

## Departures and open questions for Tomi

<!-- Anything implemented differently from the draft, and anything the draft left undecided. -->

## Links

- Meta-issue: #814
- Protocol: `docs/workflow/NOOPUNK_DRAFT_PROTOCOL.md`
- PR:
