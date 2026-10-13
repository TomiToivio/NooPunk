# The MVP local-city slice — the design as it now stands (issue #322)

**Status: design record and map of the landed structure. It implements no rule, approves no mechanic and
resolves no open question.** [`MVP_LOCAL_CITY_M0.md`](../../strategy_game/docs/MVP_LOCAL_CITY_M0.md) is
#322's M0 deliverable and states the minimal schema and the turn loop; this record completes the *design*
half the issue is actually about — **a few four-character factions, a small board, the six quantities
kept distinct, and the global-party link without binding to any roster count** — and walks #322's own
acceptance criteria to say what is met, what is gated and what needs the author.

Mechanics stay gated: `docs/design/VISION.md` §7 puts them at **S0-A, awaiting author approval**, and
[`INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md) says the faction view
may show records but must not *"assign actions, resources or victories"* before rule approval. Documents
are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

---

## 1. Scope: one city, and only one city

**The world is global; the game board is local.** The playable arena is one city and its environs —
districts, an industrial/logistics zone, islands and a short coastal hinterland. National and global
forces enter as institutions, background conditions and **event effects**, never as a playable map.

The city is a **scenario configuration**, not a hard-coded country: the merged generic schema
(`strategy_game/data/city_scenario_schema.json`) is country-agnostic and a test proves it by validating
and building a **synthetic second city** through the same bridge. Ukweli is the *first* configuration,
not a special case.

**Out of scope — permanently, not "later":** tactical combat; individual citizens; parcel-level
geography or street navigation; a detailed economics model; a planetary or global map; world simulation;
full national elections; simulated international politics; and the LaclauGPT research pipeline imported
as a runtime dependency.

## 2. The small board

Eight nodes at most, five at least, per #322's own envelope, and the same envelope the schema caps. The
current configuration is exactly eight, and it is *scenario data*: a second city is a configuration, not
a code change.

| # | Node | Kind |
| --- | --- | --- |
| 1 | Old Harbor | city |
| 2 | Civic and Commercial Centre | city |
| 3 | Mixed Neighborhoods | city |
| 4 | University and Hospital | city |
| 5 | Industrial Logistics Port | city |
| 6 | Outer Island Communities | island |
| 7 | Airfield Island | island |
| 8 | Coastal Hinterland | environs |

Islands link by **simple ferry/bridge/boat adjacencies with no pathfinding and no maritime simulator**; a
*district* may be a mainland neighbourhood or an entire island, and both use the same small location
model (a district may be an island — #324's own words).

**The restricted exclusion island is declared, and it is not a board node.** The setting bible states as
canon *"one city plus 3–4 islands … one marked restricted"*, and the board carries two islands and no
closed one. Placing the island needs a ninth node — which the cap forbids — or the removal of a node
whose set is now pinned by a **merged board projection** as well as by the schema, so **which role gives
way is the author's trade**, recorded rather than taken. The declaration, its access class and the reason
it is off the board live in `strategy_game/data/ukweli_geography.json`, and
[`ISSUE_324_UKWELI_GAP_CLOSURE.md`](ISSUE_324_UKWELI_GAP_CLOSURE.md) §4 walks it.

Node classification is **structure, not a rule**: `island` and `access` are optional schema fields on a
location record (the config marks its two islands and leaves `access` unrecorded because nothing is
closed), read by `strategy_game/local_geography.py`, and no engine code interprets them as a cost, a
route, a control or a score. A board marker that contradicts the declaration is *reported*, and an
unrecorded marker stays **unknown** rather than being read as "not an island".

## 3. Four-character factions

**The shape, which is the issue's requirement.** Every faction — the player's and every NPC faction,
through the **same data model and the same rules** — carries **exactly four leader seats**, one per
portfolio, and **every active move is carried out by a named leader**:

| Portfolio | What its holder serves | Institutional tie the seat needs |
| --- | --- | --- |
| **politics** | seats, office, institutional access | the state apparatus and the governing record |
| **networks** | opinion/support, membership, reach | labour, civic and mass organisations |
| **operations** | membership/resources, resilience | the port, industry and the resource base |
| **research** | access *via* intelligence, articulation | universities and technical intelligence |

Money, volunteers, contacts and equipment are **resources and capacity, never extra action slots**: at
MVP a faction has **at most four leader-led actions per turn**, reduced by injury or unavailability. That
is what keeps all four characters consequential rather than decorative — the scarcity is the argument.

**PENDING — the names, and only the names.** #322 asks for four **named** characters per faction. The
structure is landed; the twelve seats are **declared blanks**, each annotated with the institutional tie
it needs and marked `TODO: requires author specification`
(`strategy_game/data/ukweli_leaders.json`, `strategy_game/docs/LEADER_COUNCIL_SYSTEM.md`). **Inventing
twelve people is exactly what `AGENTS.md` §1 forbids**, so this record does not: it lands the roster shape
and the two people who are already canon (Sir Mars Eldrich as an independent patron who holds **no** seat,
Sir Uranus and Sir Mercury as invocable historical generations). The player's own local leader is the
first of the four seats and is named by the author like the rest.

## 4. The six quantities kept distinct

The issue's acceptance criterion is that **discourse, communication networks and institutions** are
present as small, testable mechanics — and that no single "influence" number stands in for them. The
distinction already exists in code, and this design **consumes it rather than restating it**:

| # | Quantity | What it is | What it is **not** |
| --- | --- | --- | --- |
| 1 | **Opinion / support** | how a constituency currently feels | not membership; not seats; not hegemony |
| 2 | **Organizational membership / resources** | members, volunteers, funds, equipment, capacity | does not buy extra actions — it *amplifies* a leader-led move |
| 3 | **Legislative representation** | seats held in a body | not opinion; not office |
| 4 | **Office and government control** | who holds which executive office | not seats; not access |
| 5 | **Institutional access** | reaching and being heard by a ministry, regulator or broadcaster | not ownership of the system; not seats; not hegemony |
| 6 | **Laclauian discursive hegemony** | which articulation is nodal, where the frontier runs | **not a scalar**; not ownership; not popularity |

`strategy_game/quantities.py` carries the six by name (transcribed from
[`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7, the acceptance criterion of the global record), and
`strategy_game/council.py` makes the consequence explicit: **four leader-led moves against six
non-identical quantities means a faction cannot pursue all of its priorities in a turn**. That scarcity —
not decoration — is what makes four offices an argument rather than a menu.

**Why there is no "increase influence" button.** Each quantity must move for a **visible, different
reason**: organising moves #1/#2, a legislative vote moves #3, a coalition moves #4, a negotiation opens
#5, a framing play moves #6. A single scalar would collapse exactly the distinctions the criterion exists
to preserve, so **no arithmetic over these names exists anywhere in the package** — the guard is real and
tested (`tests/test_political_layer.py::NoQuantifiedPoliticsTests` asserts the political layer declares no
numeric field and no metric-shaped field name).

## 5. The global-party link — without binding to any roster count

This is the part #322 asks for that had no structure: **global shocks, local effects**, with the local
factions linked to the wider global layer and the globe *not* simulated.

**The trap it has to avoid.** Three global rosters are unreconciled — **four / seven / eleven**
([`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §6B.3) — so a design that binds to "a handful of factions"
before that is settled encodes an arbitrary number. This record binds to **none**.

**What landed** (`strategy_game/data/local_global_link.json`, read by `strategy_game/local_global_link.py`):
each local party *tends* toward a named global **current**, with `membership: false`, a named basis, and
the quantities the tendency plausibly touches:

| Local party | Tends toward | Touches | Cannot move |
| --- | --- | --- | --- |
| **cpu** | establishment-pragmatic **Critical** | institutional access, articulation | membership/resources |
| **cpu** | public-interest **Cyborgist** | opinion/support, institutional access | legislative seats |
| **uip** | **Doomer / Human Sovereignty** after disruptive NHI events | opinion/support, articulation | institutional access |
| **ulp** | **Accelerationist** trade and technology | membership/resources, institutional access | opinion/support, legislative seats |

**Three rules the structure enforces, all tested:**

1. **A tendency is not a membership.** Outside networks recruit *individuals* inside mainstream parties,
   civil services and corporations without the party itself becoming them, so a link that asserts
   belonging is reported as a defect.
2. **No count is asserted.** The record declares `roster_count_asserted: false`, carries no roster-shaped
   field on any link, and `problems()` reports a link field that names a roster size. Naming a *current*
   is a name; the roster size stays the author's open question, recorded with its reason.
3. **Local research is adoption.** `shock_intake` records that global developments arrive as **external
   event cards or modifiers**, that local "research" means **acquiring, adapting and deploying** global
   science and technology and contesting its political meaning, and that the local layer **does not
   simulate international politics** — the issue's own out-of-scope line, as a checked field.

`ulp` is used as the **data id** throughout; the party's display label is open and is *not* settled here
(see [`ISSUE_324_UKWELI_GAP_CLOSURE.md`](ISSUE_324_UKWELI_GAP_CLOSURE.md) §2). The four-roster, seven-
roster and eleven-roster readings are all compatible with this layer as written, which is the point.

## 6. The turn loop

From [`MVP_LOCAL_CITY_M0.md`](../../strategy_game/docs/MVP_LOCAL_CITY_M0.md) §4, unchanged: **six steps** —
(1) draw one global-to-local event, (2) show the situation, (3) faction allocation of scarce resources
and ≤4 leader assignments, (4) deterministic resolution (seeded dice or thresholds; **no LLM, no
network**), (5) consequences that **visibly change something** (the loop has no idle turns), (6) a short
consequential report. The action menu is **six verbs sharing one resolution pattern** — *campaign,
organise, negotiate, investigate, communicate, develop* — rather than a bespoke subsystem each.

**Faction change, not classes.** Organizations move along **independent dimensions** (public legitimacy,
openness/discipline, institutional vs extra-institutional tactics, coercion, spiritual authority, illegal
activity), **never** a single `party → extremist → cult → militia → gang` track; in the MVP those
transitions are **tags and events**. Coercion and illegal activity appear as **tags with social
consequences, never as instructions** — the game models political consequences and must not become a
manual for real-world violence, coercion or crime.

## 7. #322's acceptance criteria, walked

| # | Criterion | Position |
| --- | --- | --- |
| 1 | One city and environs only; playable locations from **generic configurable templates** | **met.** Generic schema + validator merged (PR #379); a synthetic second city builds through the same bridge |
| 2 | Each faction has **four active named characters**, incl. the player's leader; NPC factions the same model | **structure met, names PENDING.** Four seats × four portfolios for all three factions, one move each; the twelve seats are declared blanks requiring author specification (#326) |
| 3 | A normal party can change **organizational form and tactics** within one consistent model | **structure met, mechanics gated (M4).** Independent dimensions as tags; the transition *rules* are S0-A |
| 4 | Global events influence the local simulation; local research **imports/adapts** technology; no international politics | **met as structure.** `local_global_link.py` shock intake, `adopt_technology` in the slice, both flags checked; the event *deck* is M3 |
| 5 | Discourse, communication networks and institutions present as **small, testable mechanics** | **partly met, partly gated.** The six quantities and the political vocabulary are landed and tested (`quantities.py`, `council.py`, `politics.py`); the *mechanics* are S0-A |
| 6 | **Deterministic, headless** run without LLMs; a short scenario; an inspectable turn-by-turn history | **met.** `local_slice.py`: same seed ⇒ byte-identical 12-turn transcript, no model, no service, standard library only |
| 7 | MVP fast and eventful; tactical combat, detailed economics, full national elections, individual citizens, planetary simulations and a global map **out of scope** | **met.** Recorded as permanent scope in §1 and in M0; no such system exists or is planned |

## 8. Milestones

| | Milestone | State |
| --- | --- | --- |
| **M0** | design note: schema, turn loop, boundaries | **delivered** (PR #335) |
| **M1** | deterministic vertical slice: city data, 3 × 4 leaders, serialization, resolver, CLI | **substantially delivered** by the labelled *provisional* slice (`local_slice.py`) — unapproved playtest assumptions, not `strategy_game/RULEBOOK.md` |
| **M2** | core politics: issues/signifiers, district support, Castilian ties, institutional legitimacy, 4–6 actions, readable logs | **structure present, mechanics gated** |
| **M3** | global event deck, local research/adoption with costs and risks | **gated** |
| **M4** | organizational evolution via non-exclusive tags and event-driven shifts | **gated** |
| **M5** | playtest: complete ~12-turn scenario, rival AI, end criteria, sample transcript | **gated** |

**The gate is the author's.** `docs/design/VISION.md` §7b defines the MVP and §7 puts mechanics at S0-A.
M2–M5 are not this record's to claim, and `local_slice.py`'s own rule note lists its omissions honestly
(no player event choices, uniform rival AI, no organizational-form transitions, no scenario picker, no
win/loss).

## 9. What this record refuses to invent

- **Twelve named leaders.** The roster shape is landed; the people are the author's (#326).
- **Turn counts, thresholds, dice mechanics, action costs, win/loss conditions.** Every one is a rule the
  author has not given; M0 records the DRAFT positions as DRAFT.
- **Roster counts.** The global 4 / 7 / 11 question is not touched, and the link layer is built so no
  count is needed.
- **Faction numbers for the board.** #322's "3–5 competing factions" is resolved to **three**, matching
  the canonical three-party lineup (#325) and the setting's own *"V1 is three political parties, not
  eleven global playable factions"*; the *four-or-five* alternative stays the author's.
- **A scenario launcher / picker.** The merged acceptance record lists it as a new deliverable rather
  than a missing file, and this record does not pretend otherwise.
- **Any second vocabulary for the political layer.** `politics.py` and `political.py` remain an
  unreconciled fork (VISION §12 Step B); this record adds no third and picks neither.

## 10. What this record deliberately does not do

- It defines **no rule, number, threshold, resolution formula or outcome table**.
- It **changes no legacy RPG file** and does not touch `RULEBOOK.md` in either game.
- It **resolves none of the open questions** it names; each is recorded with a reason and a container.
- It carries **no test over prose**: the contracts it points at exercise modules and data, never a
  document's wording (#271).
