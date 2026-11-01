# Agents working in `design/` and from design documents (#989)

**This directory is Tomi's.** Agents do not author, rewrite, translate or "improve" design documents
unless Tomi explicitly asks for that specific edit. The canonical workflow is
[`README.md`](README.md); this file only tells an agent how to work from it, and must not become a
second source of truth.

## The three steps

1. Tomi writes a design document here.
2. Tomi creates an issue from that document.
3. Agents implement the document through that issue.

No design document means no implementation of that content. An issue without a design document does
not authorize agent-invented canon.

## Before writing code

- Read the linked design document **in full** and `design/README.md`.
- State in the PR/issue: the document, the issue, the scope, and what is deliberately out of scope.
- Implement only the described increment. Do not preempt later documents or add unrequested features.
- Where the document is precise, follow it exactly. Where it explicitly allows latitude, use judgment
  inside existing canon. Where it is silent on something consequential, ask Tomi; do not invent canon.

## Document types

| Type | Meaning |
|---|---|
| Day | Calendar/world-time events, independent of player progress. No Day document = no special event that day. |
| Character | NPCs. |
| Mission | Scripted PC/party missions. |
| Interaction | Dialogue and social encounter scripts. |
| Storyline | Progress-gated main story. |
| Missions | Side missions; scripted or repeatable/procedural. |
| Location | Visitable places and nested sublocations (Helsinki → UNSA HQ → Romppainen's office). |
| Rules | CWN-compatible mods, equipment and extra mechanics. |
| Encounters | Random encounters, independent of the main story. |
| Events | Random events, independent of the main story. |

**Day ≠ Storyline.** Day content follows world time; the storyline follows player progress. Authored
missions, repeatable side content and random encounters/events are different categories.

## Boundaries

- **Finnish:** preserve Tomi's Finnish verbatim. Agents author **English only**; never translate,
  correct or imitate. The Finglish mix is intentional. See `docs/FINNISH.md`.
- **Runtime:** implement the Python Evennia MUD in `mud/` unless Tomi says otherwise (#950).
- **Rules:** CWN is the locked core; additions are mods/overlays (#897). Update the tabletop rulebook
  when mechanics change.
- **Canon sync:** implemented scenarios/lore go into the tabletop rules with references and spoiler
  safeguards; do not leak gated reveals.
- **Verification:** test deterministic mechanics, routing, day-vs-storyline triggers and location
  hierarchy; state what was implemented and what remains.

## Manual compliance check

There is no prose test for this workflow (per #271). Reviewers verify: a named design document and
issue, a diff inside that scope, Tomi's Finnish preserved, English-only authorship, tests or an
explicit untested note, and tabletop sync or a stated reason it does not apply.
