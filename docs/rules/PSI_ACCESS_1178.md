# Psychic and Edge access policy (#1178)

> **Status: implemented policy.** `src/rules/psi_access.py`, tested by
> `tests/test_issue_1178_psi_access.py`. This is an **access layer**, not a rules engine: it contains no
> Effort costs, no technique lists and no discipline ranks.
>
> **Scope:** who may choose what. The published rules still decide what a chosen ability *does*.

The issue's own framing: *"the player character may select only Telepathy and Telekinesis"*. That is a
policy question, and it can be enforced before the printed SWN text is available — which matters,
because the alternative is a character builder that quietly offers Precognition.

---

## 1. The access matrix

| Option | Player character | NPC | Where the mechanics live |
| --- | --- | --- | --- |
| **Telepathy** | **selectable** | yes | SWN discipline; Focus rules when verified |
| **Telekinesis** | **selectable** | yes | SWN discipline; Focus rules when verified |
| Biopsionics, Metapsionics, Precognition, Teleportation | **no** | yes | SWN; NPCs and authored scenes only |
| **Astral Projection** | **scripted** — OOBE, NDE, psychotronic event | yes | authored scene, never a selectable power |
| **Mutant** (AWN Edge) | **no** — NPC-only | yes | AWN Mutant Edge; *Hybrid* is one possible, unprovable origin |
| **Mentalist** (AWN Edge) | **selectable** | yes | AWN Mentalist rules, not reconstructed as SWN techniques |
| **Spellcaster** (CWN Edge) | **selectable** | yes | CWN Edge rules |
| **Summoner** (CWN Edge) | **selectable** | yes | CWN Edge rules |
| Psychotronic implant effects | **granted while used** | yes | equipment rules; a grant is never a selectable option |

**Magick is PSI and PSI is Magick** is a statement about the fiction. The mechanics and resource costs
of spellcasting, summoning and psionics **remain distinct**; knowing Telepathy grants no free casting.

---

## 2. The two loopholes this module closes

**One: Psychic Training Focus as a back door.** A Focus advances a discipline. If it could be pointed at
Biopsionics, the restriction in §1 would be decorative. `validate_selection()` therefore checks
`focus_disciplines` against the same player list. A full Psychic may select both allowed
disciplines; a Partial Psychic (`partial_psychic=True`) must stay within their one chosen
discipline. Neither can use the Focus to open a prohibited discipline.

**Two: a device grant quietly becoming an option.** A psychotronic implant may do something remarkable.
It may not make a prohibited discipline selectable at advancement. `Grant.selectable` is **always
`False`**, and constructing one with `selectable=True` raises.

---

## 3. What is deliberately not implemented

| Item | Why not | What would unblock it |
| --- | --- | --- |
| **Psychic Training Focus levels and Effort increases** | They are printed rules. This repository does not transcribe them from memory (`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`; #1043) | The authorised edition, quoted into the private rules reference; then a parity test |
| **Discipline technique lists and costs** | Same reason | Same |
| **Astral Graph and navigation** | Deferred by #1178 §2 until an authored projection scene needs its own navigable graph | A scripted projection scene that requires it |
| **Mutant mutation tables** | AWN tables are published; inventing probabilities would be worse than leaving them out | The book, plus a specific NPC template to implement |

`PSYCHIC_TRAINING_FOCUS_AVAILABLE = False` exists so that the omission is **visible in code**, not just
in a document. A caller that tries to simulate the Focus can check the flag and say why.

---

## 4. The two drafts this supersedes

The author's decision conflicts with two earlier drafts, which now carry their own notes:

- [`DRAFT_NOOPUNK_PSIONICS.md`](../design/DRAFT_NOOPUNK_PSIONICS.md) — listed Astral Projection, bounded Telepathy and **Psychic Defence** as playable abilities.
- [`DRAFT_EUROPOL_ROOKIE_BUILD_1174.md`](../design/DRAFT_EUROPOL_ROOKIE_BUILD_1174.md) — the awakening ladder granted **psychic defence** at Level 1.

In both cases: **Astral Projection is scripted**, and **Psychic Defence is not a SWN discipline** — as a
player-facing effect it belongs to the psychotronic implant's equipment rules or to a scripted event.

---

## 5. The legal fiction that makes this matter

Author decision, quoted from the issue thread because it is a rule about how Europol behaves and not
merely about powers:

> **Europol has to *prove* a person is a Hybrid before it may use lethal force on them.**

Proposed rulebook wording: *suspicion of hybrid ancestry is grounds for investigation and detention
under applicable law, never for summary force; an unregistered hybrid who has committed no crime is a
regulatory and civil-rights case, not a target.*

This is not a combat permission. It is a **burden of proof**, and it turns every hybrid investigation
into a procedural problem — which is the point.

---

## 6. Cross-references

- [`WORLD_GRAPHS_1178.md`](WORLD_GRAPHS_1178.md) — the four graph families and the corrected node semantics
- [`DRAFT_GRAPH_SCENES_1164.md`](../design/DRAFT_GRAPH_SCENES_1164.md) — scene kinds, including Action
- [`ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md`](../design/ARCHITECTURE_1184_GAMEPLAY_INTERFACES.md) — the interface architecture
- [`DRAFT_ASTRAL_GRAPH_SWN_PSI_1164.md`](../design/DRAFT_ASTRAL_GRAPH_SWN_PSI_1164.md) — historical PSI/astral proposal, superseded on nodes and projection
