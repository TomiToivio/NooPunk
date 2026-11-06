# Astral Body — tabletop procedure (#1261)

> **Revision status.** The progression below describes the earlier runtime. For current technique ranks and plane access, use the [evening design revision](../rules/ASTRAL_SUPERSKILL_1261.md).

> **Status: author-readable procedure for approval.** The structural part is implemented
> (`src/rules/astral_body.py`, 30 tests). The parts that need a ruling are marked **AWAITING APPROVAL**
> and are not implemented, so nothing here can quietly become a house rule.
>
> This is NoöPunk **fictional ontology**, informed by Faggin, Hoffman, the Law of One, Jung and OOBE
> traditions. It is not a claim about established physics.

---

## 1. Three Spaces, one informational reality

| Space | What it is | How it renders |
| --- | --- | --- |
| **Physical Space** | the ordinary embodied interface to constrained three-dimensional experience | particles, matter, objects |
| **Information Space** | multidimensional quantum information and communication among conscious agents | relations, connections, resonance |
| **Consciousness Space** | an agent's subjective interior — qualia and meaning | symbols, memories, archetypes |

These are **descriptive levels, not three travel maps**. A projection is a different *interface to the
same reality*, not a second body in a second universe.

**The limitation that makes it playable:** a human does not perceive Hilbert-space structure faithfully
on projecting. The familiar headset still renders rooms, bodies and voices. Learning to see the
conscious-agent network exchanging information is an **authored development**, never a default control.

## 2. Two modes

**Space/Time (near-physical astral).** Corresponds closely to a physical place but is not identical to
it. Helsinki can appear overlaid with thoughtforms, residues and other projections. The physical
address is an **anchor**, not a guarantee: a locked door is not automatically passable, and what you see
is not reliable enough to be evidence.

**Time/Space (inner Noöspace).** Foregrounds qualia, concept, memory and archetype. Physical
geography is irrelevant: "distance" is resonance or accessibility. Time may feel nonlinear without
becoming mechanical precognition or an editable past.

### The perception contract (enforced in code)

| State | Physical entities | Astral agents | Physical navigation |
| --- | --- | --- | --- |
| Embodied | ordinary senses | no | Physical Graph |
| Projected, Space/Time | **perceptible but fallible** | yes | astral locations with physical anchors |
| Projected, Time/Space | **no direct physical perception** | yes | symbolic links only |
| Returned | ordinary senses | no | Physical Graph |

Two consequences a referee must hold on to:

- *"I saw it in the astral"* is a **lead**, never a proof.
- A remembered or dreamed room in Time/Space is a **representation**. It does not become line of sight.

## 3. Planes and densities are two different axes

| Plane | Density correspondence (NoöPunk-specific) |
| --- | --- |
| Lower Astral | nightmare-like or hellish experiential regions; not every nightmare is a location |
| Physical | densities 1–3 |
| Astral planes | densities 1–4; 4th-density life is more properly anchored here |
| Devachanic | density 5 |
| Etheric | density 6 |
| Buddhic | density 7 |

And separately: **densities 1–5 primarily experience Space/Time; 6–7 primarily Time/Space.**

There is no contradiction in a 4th-density being living on an astral plane while experiencing
Space/Time: *plane* is where it is, *mode* is how it perceives. Both are orthogonal to whether it is
physically resident.

**These mappings are NoöPunk's, not Ra's.** The Ra material describes seven astral and seven devachanic
levels and infinitely many planes (17.36–17.38); it does not establish this table. Treat it as setting
correspondence, not as seven maps, power levels, or permission for a low-density visitor to enter a
higher plane.

## 4. The procedure

1. **Entry is scripted.** Sleep, NDE, psychotronic session, or an authored event. There is no will-power
   projection, no seventh discipline, no travel button.
2. **Note the anchor.** Write down the body's physical location. It does not change while projected.
3. **Set the mode.** Space/Time by default. Time/Space only through an authored transition.
4. **Project.** In Space/Time you move among astral locations anchored to real places. Astral obstacles,
   boundaries and entities can still block you; ordinary material barriers may be passed **when the
   scene permits**.
5. **Interact.** Astral Body to Astral Body uses CWN unarmed combat. Perception stays inside the
   contract above.
6. **Return.** Defined exit, an interrupted projection, or a forced return. The actor is embodied again
   at the same location, once.
7. **Record.** What was seen and what was *inferred* are two different lines on the sheet.

**Disorientation, unreliable memory and partial returns are narration**, not dice, unless a real rules
need appears at the table.

## 5. Combat

**What is implemented.**

- **Targeting eligibility.** You can only strike a target that is *astrally present*. A hidden
  projection cannot be shot by an ordinary person; a visibly manifested apparition is visible but **not
  tangible**, so it cannot be shot either. ESP may reveal a projector; eyes may not.
- **Action rights.** A projected body cannot take an ordinary physical action: no punching doors,
  picking up a gun, or firing one.
- **One actor, one body.** Returning restores the embodied state without creating a duplicate.

**What is AWAITING APPROVAL.**

- **The damage bridge.** Astral damage to the CWN body — shared HP, temporary astral injuries, forced
  return, coma, rescue — is the one place where a wrong guess invents a second health track. The
  function `apply_astral_damage()` exists only to **refuse**, with an explanation, until the adapter is
  approved.
- **The SWN technique whitelist.** Telepathy and Telekinesis may be more effective than a punch, but
  only where the *published* technique permits that target and effect. Each permitted interaction must
  be quoted from SWN Revised and listed; inventing a generic "psychic attack" is exactly what the issue
  forbids.

**Default at the table until then:** resolve the exchange with CWN unarmed combat, record the
consequence in the scene, and let the body at home be the stake. The astral body is in danger; the sheet
does not gain a second meter.

## 6. The Lower Astral and dream construction

A sleeping person may be seen **constructing** a dream: a visible landscape of memories, symbols and
figures being generated around them. A near-physical projector sees the sleeping body; an authored
transition reveals the dream's own symbolic space.

- Distinguish, in GM notes, **the dreamer, the dream avatar, a shared thoughtform and an independent
  visitor** — even when the players cannot.
- The dreamer does **not** automatically perceive the visitor. Entering or altering a dream needs
  authored permission, and never becomes unlimited telepathic intrusion.
- **Not every nightmare is an attack, and not every Lower Astral entity is hostile.**

**Source ambiguity is a rule, not a mood.** Player-facing text never reveals what generated a dream
unless an authored reveal does (see `docs/campaign/DREAMS.md`).

## 7. The dead

In NoöPunk, the dead can continue as conscious agents, usually resting and preparing for reincarnation.
They are **usually in Time/Space**, so an ordinary near-physical OOBE **does not find them**. Contact
requires an authored encounter, a psychotronic route, or a deliberately constructed path into
Time/Space — never a "summon any deceased person" action.

Contact scenes should carry **identity uncertainty, consent, and different kinds of postmortem
existence**. A conversation with a dead parent is a scene about grief and evidence, not a lookup table.

**In-world, this changed law, religion and research.** Institutions exist: admissibility of testimony,
licences, stack ownership, burial law, privacy and rescue services. That ordinariness is the point —
the extraordinary should arrive through paperwork (see *Summerland* as inspiration, not mechanics).

## 8. Three illustrative scenes — **NONCANONICAL**

Each is design illustration until Tomi writes it as campaign prose.

**A. Helsinki bedroom OOBE (Space/Time).** Tony wakes outside himself: the room is right and wrong at
once, a figure stands where no one should be. He can observe or return. The body stays in the bed; the
overlay gives neither perfect reconnaissance nor a hand that can move a curtain.

**B. Dream Helsinki gateway (Time/Space).** From a near-physical street he passes into a symbolic
university corridor whose route follows association, not addresses. He meets an agent and a sign he
recognises. The sign becomes a **question**, not admissible evidence.

**C. Psychotronic laboratory session.** An authorised session with staff monitoring his body. For a
moment the interface changes and he sees relations between conscious agents rather than humanoid
shapes. No high-dimensional renderer is required — the prose does the work.

## 9. What the engine does, and what it refuses

| Implemented | Refuses |
| --- | --- |
| projection state, one actor, fixed body anchor | second character sheet or astral HP track |
| perception filters per mode | physical sight from Time/Space |
| action-rights denial while projected | astral teleportation, resurrection, resleeving |
| targeting eligibility, ESP and manifestation | a generic Astral Combat skill |
| memory/interpretation separation | automatic evidence from astral perception |
| scripted entry, authored mode shift | at-will projection or a new discipline |

## 10. Questions for approval

1. **Damage bridge:** shared CWN HP, a temporary astral condition, or forced return — which one is canon
   when an Astral Body loses a fight?
2. **SWN whitelist:** which published Telepathy and Telekinesis techniques may target an astral body?
3. **Manifestation:** may a projector ever be *heard*, and does that require a separate authored channel
   from being seen?
4. **The dead:** is contact with a deceased relative a once-per-campaign authored scene, or a repeatable
   procedure with a cost?
5. **Ψ / Mannerheim–Yamamoto:** does the resleeving economy belong in this line at all, or only in #1255?

---

# Rank ladder (author update 2026-11-06): Astral Projection as an Astral-domain superskill

> **Supersedes the flat "scripted, not a skill" framing above.** Astral Projection now has **ranks
> 0–4**, and each rank states three things at once: the character's *model of reality*, *what she can
> perceive*, and *what she can actually do*. It stays narrow outside Noöspace — it does very little in a
> Physical or Cyber scene — and it never becomes a CWN or hacking substitute.
>
> **The initial campaign allows 0 or 1.** Ranks 2–4 are implemented as gates and refused at character
> creation until a later campaign earns them (`src/rules/astral_body.py`, 20 tests in
> `tests/test_astral_ranks_1261.py`).

| Rank | Model of reality | Perceives | Can do | Code |
| --- | --- | --- | --- | --- |
| **0 — Disorientation** | Astral is dreamlike; physical laws still assumed; may not tell sleep from waking | Near Astral plus a warped physical overlay | Separate, walk, basic encounter, return. **No flight, no Lower Astral** | `can_fly=False`, planes `{near_astral}` |
| **1 — Lucidity** | Astral geometry is not metric; dreams are built from Quantum Information | The same, plus dreams being constructed | **Flight**, **Lower Astral** and dream-world entry | `can_fly=True`, planes `+lower_astral` |
| **2 — Agent network** | Solid-seeming objects are rendered quantum information exchanged between agents | Agents as information structures | **ROTE** (transmit information) and **learn an Ident**; no jump yet | `can_send_rote`, `can_learn_ident` |
| **3 — Authorized agency** | Appearance is a rendering; information lies beneath | Interface versus information | **Use Ident** (instant arrival at a known agent), permission-gated quantum-information editing | `can_use_ident`, `may_edit` |
| **4 — Cosmological** | Noöspace as an infinite-dimensional Hilbert space; branching, reconverging timelines | Higher planes, dim alternative timelines | **Devachanic / Etheric / Buddhic** access, Akashic research | `planes() == PLANES` |

## Ordering corrections this page now follows

- **Devachanic/Etheric/Buddhic are Level 4**, not Level 2. The old accessibility text is superseded.
- **Entering a dream world is not switching modes.** Level 1 reaches *inner dream worlds*; deliberate
  Space/Time ↔ Time/Space switching is still an authored transition (`shift_mode(authored=True)`).
- **Duration caps are provisional** — 10 / 60 / 600 / 2880 / 10080 minutes (`PROVISIONAL_MINUTES`). They
  are ceilings, not promises: a longer projection does not buy better knowledge.

## Ident, stated narrowly

An **Ident** is a Conscious Agent's persistent noetic address. It is:

- **eternal while the same agent exists** — it survives death, reincarnation, resleeve and upload;
- **not inherited by a copy, fork or simulation** (`Ident.survives("fork") is False`);
- **not a name, a body, a photograph, an address or a consent token** — `learn_ident()` demands one of
  three sources (authored encounter, consensual exchange, recognition technique) and refuses everything
  else;
- **learnable at rank 2, usable only at rank 3**;
- **never a way through a ward** — a blocked arrival says so without naming where the agent is.

Level 3 editing is **permission, not power**: `may_edit(owner=…, editor=…)` allows your own information
or an unclaimed limbo, and refuses another agent's, a protected mind, a physical system or a Cyber node.

## What is still not code

- the **damage bridge** (`ASTRAL_DAMAGE_BRIDGE_APPROVED = False`), the published-technique whitelist, and
  manifestation channels — the three questions in §10 above, unchanged;
- **ranks 2–4 behaviour** beyond their gates: ROTE payloads, quantum-information editing consequences and
  Akashic research are design-only by author instruction;
- the **provisional Effort and action costs** for a jump — settled against the published psionics
  framework before any number is written.

## Cross-references

- [`PSI_ACCESS_1178.md`](../rules/PSI_ACCESS_1178.md) — Astral Projection remains scripted, not a power
- [`PSI_CARRYOVER_1196.md`](../rules/PSI_CARRYOVER_1196.md) — why the Astral graph is still deferred
- [`../campaign/DREAMS.md`](../campaign/DREAMS.md) — dream source ambiguity
- `docs/rules/ASTRAL_PSI_1164.md` — the earlier design record, superseded where it conflicts

## Additional fail-closed action gating (PR #1266)

`src/rules/astral_progression_1261.py` is an additive **scene-action authorization** adapter, not a replacement for `AstralSkill` or `astral_body.py`. Rank 0 permits observation, walking, astral contact and return. Rank 1 additionally permits flight in Space/Time and entry to a Lower Astral dream world **only through an authored gateway**. Inactive projections, invalid rank values and unknown actions fail closed. Rank 2–4 actions are still design-only, regardless of capabilities described in the rank model. This gate alone never overrides consent, physical-targeting rules, mode transitions, SWN Effort or entry eligibility. Voluntary entry, Effort/duration, the damage bridge and the SWN whitelist still await author approval.


## Rank 0–1 action authorization (PR #1266; #1261)

The rank table in `src/rules/astral_progression.py` is authoritative for
superskill progression and optional duration data. The complementary
`src/rules/astral_progression_1261.py` supplies **per-action, fail-closed
rank gates**, not a second progression ladder. Projection state, perception
and targeting remain owned by `src/rules/astral_body.py`.

At rank **0**, while projected, observe, walk, permitted astral contact and
return pass the rank gate. Rank **1** also permits **flight in the near Astral
Space/Time mode**, and Lower Astral entry **only through an authored gateway**.
Neither rank may use ROTE, Ident, information editing or higher-plane travel.
These remain design-only even if a caller supplies rank 2–4. Rank permission
never overrides physical targeting, consent, scene access or SWN Effort.

**Tabletop loop:** establish an authorised projection event and fixed body
anchor; render Space/Time according to rank; offer local observation, contact,
movement or return, plus rank-1 flight and authored dream gateways; apply the
existing Astral Body perception and CWN combat rules; return to the same body.
The passage from a dream landscape to Time/Space still requires an **authored
mode transition**, not just a rank check. Keep astral observations separate
from admissible physical evidence. The rank gate **does not grant entry**
without an appropriate scripted or approved voluntary trigger.

**Unresolved:** native character creation eligibility, voluntary initiation,
Effort and recovery, provisional duration activation, the astral damage bridge,
and the SWN technique whitelist require separate author approval. This change
does not activate any of them. Test coverage for these action gates is in
`tests/test_astral_rank_actions_1261.py`; the original
`tests/test_astral_progression_1261.py` remains on the superskill table.
