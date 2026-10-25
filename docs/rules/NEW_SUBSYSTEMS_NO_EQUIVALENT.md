# Subsystems with no Without Number equivalent — and why they must be authored, not borrowed

**Status: design principle plus inventory. No rule is approved here; this records a design ruling.**

## 1. The ruling

> Where CWN, SWN, AWN or WWN has **no equivalent** for a NoöPunk subsystem, NoöPunk authors its own subsystem.

The rule matters most in the case it is easiest to get wrong. It is not the *obvious* gap that hurts — nobody
is tempted to import "noosphere rules" from a book that has none. What hurts is the **near** equivalent: the
mechanic close enough to look like a fit, borrowed because it saves authoring, which silently redefines a
NoöPunk concept in the terms of the donor game.

Three examples, all real, all rejected below:

| NoöPunk subsystem | the tempting near-equivalent | what borrowing it would actually do |
|---|---|---|
| **BCI cognition** | CWN **System Strain** | Strain is *bodily tolerance of implants*. Borrowing it makes thinking-with-a-machine a question of flesh, and deletes the cognitive cost the setting is about. |
| **Natural PSI** | SWN **psionic disciplines** | Disciplines are a *class* structure with a virus-adjacent history. Borrowing them makes PSI a role and a training tree, not a human capacity that spreads through teaching. |
| **Noösphere** | WWN **magic** | Magic is a spell economy. Borrowing it turns a shared cognitive field into a resource a character spends. |

So the test for every row is not "is there something similar?" but **"does importing it preserve the concept, or
replace it?"** If the latter: author.

## 2. The inventory

| # | Subsystem | Nearest thing in the family | Why it is not equivalent | Owner |
|---|---|---|---|---|
| 1 | **Ubiquitous network** | CWN hacking (host-centric, access as scarcity) | NoöPunk's field is *abundant access, scarce safety*: the difficulty is being noticed, not connecting. `rulebook/22` §22.5 gives the routes; the ambient field is missing. | [`SUBSYSTEM_UBIQUITOUS_NETWORK.md`](SUBSYSTEM_UBIQUITOUS_NETWORK.md) |
| 2 | **PSI as learnable natural capacity** | SWN psionics | SWN makes psi a class-and-discipline structure; canon §6.1 makes it natural and viral-free, and #21 makes training the mechanism. Shape adopted (cost pool, staged learning), ontology refused. | [`SUBSYSTEM_PSI_LEARNABLE.md`](SUBSYSTEM_PSI_LEARNABLE.md) |
| 3 | **Noösphere / cross-domain state** | WWN magic; nothing else | A shared cognitive layer with gateways and realm actions has no analogue in a fantasy spell economy. `src/rules/noospace_projection.py` is explicitly **provisional** and must not be promoted by a conversion. | canon `18_CROSS_DOMAIN_STATE.md` |
| 4 | **NHI contact** | SWN alien/AI material (protected) | Contact is the setting's founding event and its epistemic problem; SWN's material is a different genre's setting and is also licence-blocked. | canon `12_BEINGS.md`, `15_XENOPOLITICS.md` |
| 5 | **Psychotronics and psychosurgery** | none | Technology-mediated PSI and a four-layer surgical construct (Jungian + psychedelic + cybernetic + psychotronic) exist in no WN book. | canon `6_PSYCHIC.md` §6.2, `17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md` |
| 6 | **BCI cognition** | CWN cyberware + System Strain | Strain measures the body's tolerance; BCI measures a cognitive relationship and a communications channel. Substituting one for the other is the error named in §1. | canon `5_CYBERNETIC.md` §6.2.3 |
| 7 | **AGI/ASI law and the three swarms** | none | Panopticon, Noösphere and Thanatos with licence classes and a threshold is a political-legal construct, not a stat block. | canon `22` §22.6–§22.7 |
| 8 | **Discourse / ideological analysis** | none | The Laclau-derived layer (equivalence, antagonistic frontier, nodal points) has no mechanical analogue anywhere in the family and is not a game mechanic in any of the four books. | PCM/LaclauGPT lineage |

## 3. What "authoring a subsystem" obliges

A new subsystem is not a paragraph of flavour. To count as authored here it must supply:

1. **A named procedure** — the steps a table performs, in order.
2. **A stated invariant** — the thing dice may never overrule (e.g. an air gap is never remotely crossable).
3. **Its own vocabulary**, declared, so two subsystems do not silently share a word with different meanings.
4. **A testable contract** — deterministic assertions that hold **before** any number is authored.
5. **An explicit open-numbers list** — what remains an author decision, so a later session cannot mistake a
   placeholder for a ruling.

The two specifications above follow this shape deliberately: three-layer model and staged learning, each with
invariants, vocabulary and a contract, and each ending in a list of numbers it refuses to invent.

## 4. What this does not license

- It does **not** authorize new mechanics in the runtime. Both specifications are design documents; the #566
  ruling explicitly left numeric subsystems `DEFER`.
- It does **not** let an agent author technique lists, cost values, or scene numbers. Those are `AGENTS.md` §1
  territory — canon and numbers belong to the author.
- It does **not** contradict the matrix: where a WN mechanic *does* preserve the concept, the matrix's `MODIFY`
  verdicts stand (Shock, access prerequisites, morale, mission clock, effort-as-shape).

## 5. Ordering of work

1. **Ubiquitous network** — highest value, because it is the subsystem most likely to be replaced by CWN's
   hacking by accident, and its invariants are already testable (`test_cyber_access.py`).
2. **PSI learnable** — second, because layer B's implementation already exists and only the learning stages and
   cost shape are missing.
3. **BCI cognition** — third, and only after the System-Strain substitution in §1 is explicitly refused in the
   matrix (row 11), so the two documents cannot disagree.
4. The remaining rows are canon-owned and need no new subsystem document; they need the conversion to *stop*
   at them.
