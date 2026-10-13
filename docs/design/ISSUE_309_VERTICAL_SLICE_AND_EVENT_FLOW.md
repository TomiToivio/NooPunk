# #309 §8 — the vertical-slice pitch, the cross-scale event flow, and who acts

**Scope:** three of the four §8 artifacts that had no file of their own — item 1 (a one-page pitch of a
single overhead-map turn), item 2 (the cross-scale world-state/event-flow architecture, showing where
consequences travel and where simulation is abstracted) and item 4 (the separation of human-played,
LLM-played and rules-driven roles, with the limits of delegation). Item 3 (engines), item 5 (the S1
release scope), item 6 (distribution) and item 8 (UGC governance) already live in
`ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md` and `ISSUE_309_DISTRIBUTION_AND_UGC_GOVERNANCE.md`; item 7's
attribution half now lives in `docs/ATTRIBUTION_POLICY.md`, and its licence half is row **D10**.

**What this is.** A pitch and an architecture sketch: the shape of one turn, the path a consequence
takes through the layers, and who is allowed to move what.

**What this is not.** Not a mechanic, a rule, a number or a canon ruling. **`RULEBOOK.md` still says NO
RULES APPROVED and the rules gate is row D11**, so the example below is an *illustration of the
interface and the causal shape*, not an approved procedure. Nothing here authorizes implementation, and
the hard caps in `VISION.md` §7b still bound what S1-a may contain.

---

## 1. The pitch: one overhead-map turn

> **One screen, four presses, and a reason.** You are the founder of a small Helsinki nonprofit with a
> filed anomaly report, a leased office and one ally in the ministry. The map is overhead and stays
> overhead. You select your own portrait on it, not a mode: **the leader is an entity on the same board
> as everything else.**

**The turn, as the player experiences it:**

1. **Read the situation.** The map shows Helsinki, a handful of Finnish institutional nodes, and two
   abstract foreign contacts greyed out because the link is currently unreliable. A discourse panel
   carries two live narratives — the ministry's "procedural review" and a rival's "cover-up" framing —
   each with the organizations currently amplifying it. Nothing is a numeric opinion meter; the panel
   says *who is saying what, and through which channel*.
2. **Choose the leader's move.** Her sheet offers the moves her position actually supports: attend the
   ministry review, brief the press, or spend the week on the research. Choosing the ministry review is
   a *delegation as well as an action*: two of the four agents are committed to it, so they cannot do
   anything else this turn.
3. **Resolve.** The resolution is one mechanism reused everywhere — the same resolution the RPG layer
   already uses for a skill check, applied here to an institutional encounter rather than a locked door.
   The roll is seeded and the log records it.
4. **See what changed, and why.** Three panels update together: the ministry node's *relationship* to
   the faction shifts; the "procedural review" narrative gains the ministry as an amplifier while the
   rival framing loses a channel; and one foreign contact becomes reachable again because a courier
   arrived. The turn summary states the causal chain in one sentence — *the review was attended, so the
   ministry's own framing strengthened, so the rival's channel narrowed*.

**What makes this the right slice:** the three pillars fed each other **inside one screen, with no mode
change.** A character decision moved the strategy layer, which moved the discourse layer, which changed
who cooperates — which sets up the next character decision. If any of those three presses is missing,
the loop is broken and the MVP has failed by `VISION.md` §7b's own test.

**What the pitch deliberately does not show:** travel between cities (it costs time and may be unsafe —
`VISION.md`), an LLM doing anything load-bearing, a space layer, or a number the player cannot explain.
The greyed foreign contact is there precisely to make the shrinking-horizon premise visible in the
interface rather than in a lore document.

---

## 2. The cross-scale event flow

Consequences travel along **one path**, and every layer may *abstract* rather than simulate. Reading the
diagram downward is a decision becoming history; reading upward is history becoming a situation.

```
   PERSON ─────────────────────────────────────────────────────────────┐
   leader / agent sheet · relationships · obligations                  │
        │ a choice                                              ▲       │
        ▼                                                       │       │
   RULES ── one resolution mechanism, seeded, logged ──────► OUTCOME   │
        │  (the same one the RPG layer already uses)              │       │
        ▼                                                       │       │
   FACTION ── standing, committed agents, obligations ◄──────────┘       │
        │            (abstracted when the faction is a rival)            │
        ▼                                                               │
   DISCOURSE ── who amplifies which narrative, through which channel    │
        │        (the layer the player *reads* to know why)              │
        ▼                                                               │
   INSTITUTIONS ── government support, legitimacy, conditions           │
        │          (cooperative, revocable — never ownership)            │
        ▼                                                               │
   WORLD ── travel and communications availability, crisis phase ───────┘
            (small readable states, authored events, no transport sim)
```

**Where simulation is abstracted, deliberately:**

| Layer | Simulated | Abstracted |
| --- | --- | --- |
| Person | the player's leader; named recurring NPCs | everyone else exists as a name on a card |
| Faction | standing and commitments | rival factions' internal deliberation |
| Discourse | who amplifies what, and via which channel | audience size; no population model |
| Institutions | the relationship to *this* faction | the rest of the state's machinery |
| World | travel and comms availability per link | geography, logistics, economy |

**The rule the diagram encodes:** a layer may be **coarse**, but it may never be **opaque**. If the
player cannot read why power moved, the abstraction has gone too far — which is §8's own criterion
(*"clarity of power shifts"*, below) restated as an architecture constraint.

**The one upward edge that matters:** the world layer feeds back into the person layer as *availability*
— a stranded agent, an unreachable ally, a courier that arrived. That single edge is what makes the NHI
Crisis a narrative experience rather than a difficulty modifier.

---

## 3. Who acts: human, LLM, and rules

Three kinds of actor share the board. The separation is the §8 item 4 deliverable, and its
load-bearing rule is the second row.

| Actor | May | May not |
| --- | --- | --- |
| **Rules** | resolve a check, move standing, advance the turn, write the log | be bypassed by dialogue or by a model |
| **Human** (player) | choose among the moves their position supports; delegate | exceed committed agents, or act outside the position |
| **LLM** (optional) | *propose*: dialogue, interpretation, a faction's plausible deliberation | mutate authoritative state; be required to play |

**The delegation limit, stated once:** a delegation transfers *who performs* an action, never *whether it
is permitted*. An agent sent to the ministry review spends the turn there; a manager may keep running a
portfolio remotely **while deployed** (that is #323's distinction, not a new one); and no arrangement
creates a free extra mission. Delegation is how one strategic UI covers several scales — never how the
player escapes the action economy.

**LLM parity is parity of *roles*, not of implementation.** A model may inhabit a rival leader, a
bureaucrat or a hostile analyst; it may not be load-bearing. The released game must be fully playable
with models disabled, and every model output is a *proposal* checked against authorized actions and
canonical facts before it can touch state.

---

## 4. What this does not do

- **It approves no rule.** The turn above is an illustration; D11 governs.
- **It adds no canon and no name.** Nothing here is a ruling on #338, #328 or #346's rows.
- **It commits no renderer.** The pitch is renderer-neutral on purpose; row D13 picks one.
- **It does not promise the foreign contacts.** They exist in the pitch to represent a link that may be
  unreliable, not a content commitment.
