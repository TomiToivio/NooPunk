# #719 — NoöPunk-original systems: hegemony, the Noösphere, and interdimensional consciousness

**Status:** research and design. Not canon, not approved, not implemented. Proposals are marked as
proposals, and each carries the epistemic label the repository already uses: **(A) source claim**,
**(B) NoöPunk reading**, **(C) not supported by the source**.

Scope: only what CWN/SWN do not cover. The investigation layer is #704; the attribute question is #716;
neither is reopened here.

---

## 1. Gap analysis

| problem | covered by CWN/SWN? | closest analogue elsewhere | verdict |
|---|---|---|---|
| tactical combat, gear, hacking, cyberware | **yes** — leave alone | — | do not touch |
| psionics as a trained capability | **yes (SWN)** | — | reuse principles |
| finding clues without stalling | **yes (#704)** | GUMSHOE | done |
| **ideological struggle between factions** | no | faction/company rules in several games model *resources*, not *meaning* | **genuine gap** |
| **Noösphere as both network and psychosphere** | no | cyberpunk decks model a network; horror games model a mind | **genuine gap** |
| **consciousness development / StS–StO** | no | sanity tracks model damage, not development | **genuine gap** |

**(B) The design principle for all three:** they must be *state with consequences*, not lore with dice. If
a subsystem cannot change what a character can do next session, it is a paragraph, not a mechanic.

## 2. Module 1 — Hegemony (LaclauGPT → tabletop)

**(A) Source claim.** Laclau's apparatus — demands, articulation, chains of equivalence and difference,
nodal points, floating and tendentially empty signifiers, antagonistic frontier — is an *analytical*
framework. The LaclauGPT paper proposes a method; it is not a validated simulator. **(C) Not supported:**
any claim that a game mechanic derived from it predicts real political outcomes.

**(B) NoöPunk reading:** hegemony is the process by which one faction's particular demand becomes the
group's universal one. That is a contest over *signifiers*, and it is playable without simulating a
society.

**Mechanic — three tracks per faction, no new dice.**

1. **Articulation** (0–6): how many distinct demands are currently linked to your chain. Linking a new
   demand costs a scene and a concession; each link makes collective action cheaper and your message
   broader.
2. **Legitimacy** (0–3): institutional uptake. Rises through public acts, rulings, media, elections; falls
   when the frontier is exposed as sectional rather than universal.
3. **Frontier** (named, not scored): the antagonistic line "us / them". Declaring one gives +1 to
   mobilise your own chain and −1 to any negotiation with the named other *for as long as it stands*.

**Signifiers.** A nodal point is a *slot*, not a word: whoever controls it decides what the chain means.
A floating signifier can be attached to two chains at once; a tendentially empty one can be filled by
anyone who spends a scene defining it. Resolution is the existing CWN social check; the tracks change what
success *buys*, never whether you succeed.

**Bounded complexity:** three numbers and one sentence per faction, updated once per session.

**Play example — the signifier contest.** Two factions both claim "public safety". Faction A has
Articulation 4 and Legitimacy 2; B has 2 and 3. A spends a scene attaching "the ward closures" to its
chain; B answers by declaring a frontier against "the AI contractors". A's mobilisation gains +1; B's
negotiation with the contractors takes −1. Neither roll decides who is *right* — only who is heard.

## 3. Module 2 — The Noösphere: Teilhard meets Gibson

**(A) Source claim.** Teilhard's noösphere is a speculative cosmology; Gibson's cyberspace is fiction.
**(C) Not supported:** that either describes an existing layer of reality.

**(B) NoöPunk reading:** the Noösphere is one substrate with two *interfaces* — a network you log into and
a psychic field you attune to. The same intrusion can be a hack and a possession depending on which
interface you use, and neither reading is privileged.

**Mechanic — one substrate, two access modes, one cost.**

- **Presence** (0–3): how strongly you are *in* the substrate. Network access raises it by equipment;
  psychic access raises it by training. Both are the same number, which is the point.
- **Two modes:** `Interface` (technical) and `Noöspace` (psychic) are separate skills, but they read the
  same state. A fact learned one way is the same fact.
- **Cost — Trace:** every action in the substrate leaves a trace, whether packet or psychic residue. Trace
  is not damage; it is what other actors can find you by. At Trace 3, something finds *you* first.
- **Ontological bleed:** using the psychic interface on a network artefact (or the reverse) is possible
  and produces a reading that is *true but mistranslated* — a clue that must be checked, never trusted.

**Bounded complexity:** one number (Presence) and one counter (Trace) per character.

**Play example — Romppainen's mixed investigation.** He reads the ward's door controller with `Interface`
(technical) and the patient's account with `Noöspace` (psychic). Both raise Presence; both leave Trace.
The controller log and the account agree on a time — that agreement is the fact; *why* they agree stays a
hypothesis, and the anomaly gate still demands the discriminating test before anyone calls it precognition.

## 4. Module 3 — Interdimensional contact and consciousness development

**(A) Source claim.** Vallée's interdimensional hypothesis and the Law of One's density progression are
fictional/speculative frameworks. **(C) Not supported:** any empirical claim about NHI or consciousness
evolution.

**(B) NoöPunk reading:** contact is *ambiguous by construction*; development is *chosen and costly*, not
granted. Service-to-self and service-to-others are behavioural constraints on what a character can do,
never an alignment label.

**Mechanic — development as a WWN major project, not a level.**

- **Stages** are qualitative: `ordinary` → `attuned` → `coherent`. Each transition is a project requiring
  evidence, a witness and a cost, and each is *reversible only by another project*. No stage is strictly
  better: `attuned` sees more and is more visible; `coherent` resists influence and struggles to change.
- **StS/StO** is a *record of acts*, not a score: three columns of what you did for yourself, for others,
  and at whose expense. A faction may read it; the rules never total it into a morality number.
- **Contact** uses the investigation layer: every contact produces a **fact** and at least two readings,
  and the anomaly gate applies unchanged. A contact never proves an ontology.

**Bounded complexity:** one stage per character, one three-column record per character, no new track.

**Play example — 3D → 4D progression.** A character who has twice acted at cost to themselves to keep a
patient's account intact may attempt the `attuned` project. It needs a witness (another character who can
say what changed), evidence (the case record), and a cost (something given up). Success does not reveal
what the contact was; it changes what the character can *do* — and makes them findable by whatever else is
attuned.

## 5. Cross-system constraints

- **One resolution system.** All three use the CWN 2d6 check; none adds a die, a pool or a second ladder.
- **No new harm economy.** Trace, Presence and development stages are not damage; HP, Strain and
  conditions remain the only harm.
- **The anomaly gate is upstream.** Any psychic or contact material must pass through
  `src/rules/anomaly_gate.py` before it can conclude anything.
- **No free powers.** PSI remains a trained capability with Effort; a stage is not a power list.
- **Licensing:** all three are original text. Nothing here is adapted from a proprietary source. Where a
  concept comes from a book (Laclau, Teilhard, Vallée, Law of One), the *idea* is used and the expression
  is not copied — and the epistemic label stays attached.

## 6. Open decisions (author)

1. Does the hegemony module belong to the tabletop RPG, the strategy game, or both? It fits both, and
   building it twice would be the classic duplicate.
2. Is Presence per-character or per-scene? Per-character is simpler; per-scene models "the network is
   watching" better.
3. Do development stages gate anything mechanical, or are they purely fictional permissions? Gating is
   stronger; permissions are safer.
4. Does StS/StO stay a record forever, or may a faction ever *score* it? Scoring would make it a morality
   stat and lose the ambiguity the setting depends on.

## 7. Playtest protocol (not run)

One session per module, three total. For each: does the module change a decision the players make? Record
the decision, the numbers that moved, and whether anyone could explain the rule back after the scene. A
module that produces narration but no decision is a paragraph — cut it or fold it into fiction.

## 8. Follow-ups

- #712 (layers and attributes), #716 (attribute decision), #704 (investigation) — all separate.
- If the hegemony module is accepted: one implementation issue, tabletop only, no code.
- If the Noösphere module is accepted: reconcile with #119 (Noöspace) before writing any code.
- If development is accepted: reconcile with #191 (Law of One) so the two do not describe the same
  progression twice.
