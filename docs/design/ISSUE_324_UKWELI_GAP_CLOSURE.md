# Ukweli local geography and naming — the gaps the acceptance record carried (issue #324 addendum)

**Status: design record. It approves no rule, implements no mechanic and decides no canon question that
belongs to the author.** It lands the *structure* for the geography and naming questions issue #324
raised and left open, and it records each decision as **PENDING with a reason** rather than filling it
in. Documents are reviewed editorially and by playtesting, never by CI
([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Why an addendum and not a closure.** [#324](https://github.com/TomiToivio/NooPunk/issues/324) was
**already closed** by PR [#379](https://github.com/TomiToivio/NooPunk/pull/379), which landed the
generic city-and-environs schema and its validator plus
[`ISSUE_324_ACCEPTANCE.md`](ISSUE_324_ACCEPTANCE.md). That record closed the schema and the seven
deliverables, and it **carried forward four items** as still open: *the state's formal name*, *the third
party's name*, *the restricted island's relationship and legal autonomy*, and — implicitly, in its
island row — *the island count*. This record addresses exactly those four, and nothing else. It does not
re-open #324 or restate its deliverables.

---

## 1. The state's name — closed as a **register mapping**, not as a choice between two names

- **#324** (the issue title and body) says *Republic of Ukweli* throughout.
- **#325** states: *"**Official name: People's Republic of Ukweli.** The name reflects its communist
  independence tradition and the longevity of its governing party, not a present-day one-party
  dictatorship."* It further marks the name **load-bearing** for the setting's own joke: "Not quite
  Cuba, comrade" only works because the formal name misleads.
- **#328/#331/#332** and `GLOBAL_FACTIONS.md` name only **New Ukweli**, without naming the state.

**What is factual.** #325 is the dedicated setting issue and the author's own declaration of the official
name; #324's plainer form is ordinary shorthand written before #325 landed. The two are therefore not
rival official names but a **register** difference, and the register mapping is the closure:

| Register | Form | Where it belongs |
| --- | --- | --- |
| **Official** | **People's Republic of Ukweli** | treaties, the formal self-description, the joke's straight line |
| **Everyday** | **Ukweli**, **New Ukweli** | the map, the city, ordinary conversation |
| **Informal** | *Republic of Ukweli* | #324's own title and body, and older prose |

This is recorded in `strategy_game/data/ukweli_geography.json` → `state_names`, and the scenario data's
`setting` string now reads *People's Republic of Ukweli, Indian Ocean*. **Aligning the data to #325 is
not inventing a name**: it is the author's own statement, and the record cites it.

**PENDING — the residual question.** Whether the **informal short form may persist** in issue titles and
prose is the author's, and it is recorded as `state_names.residual_pending` with a container instead of
an answer. A reader who wants the plainer form to be the *official* one reverses this by changing #325's
sentence; that is one deliberate edit, and this record says so rather than hiding the choice.

## 2. The third party's name — **PENDING**, and deliberately so

| Form | Where |
| --- | --- |
| **LFP — Libertarian Freedom Party of Ukweli** | #325 (setting authority), #326 (leaders) |
| **ULP — Ukweli Libertarian Party** | #327's table, `data/ukweli_local.json`, `data/global_factions.json` |

**What is factual:** the **data id is `ulp`** in both `ukweli_local.json` and the landed Sir Mars
Eldrich card, so a fourth id would fork the data and is not created. **What is the author's:** the
display **label**. Issue #326 — which owns the party's people — deliberately left the label open, and a
landed contract (`tests/test_ukweli_leaders.py::test_naming_conflict_is_surfaced_and_not_resolved`)
asserts that it stays surfaced rather than resolved. **This record therefore does not settle it**, and
that is the correct outcome rather than an omission: settling it here would contradict a just-landed
decision that the question belongs to the author. It is carried with a `todo: requires author
specification` in `party_labels`.

## 3. Eldrich Island and the Freedom Colony — **PENDING**, as three named options

Issue #326 states the relationship is **undefined**, and the canon-reuse inventory records the map
schema as blocked on it ([`ISSUE_324_UKWELI_CANON_REUSE.md`](ISSUE_324_UKWELI_CANON_REUSE.md) §4.3).
What the options cost, transcribed from #326's own analysis:

| Option | What it buys, and what it spends |
| --- | --- |
| **Same place** | one node does the work of two: the island *is* the enclave. Simplest map; the family's private residence and a business enclave become one political object |
| **Adjacent** | one node with two faces: mansion and colony share infrastructure and fate. Cheapest for the node budget, richest for internal conflict |
| **Separate, linked** | two nodes out of 6–8: a *domestic* base (Mars at home) and a *public* one (the enclave) — politically opposite assets, at the cost of a node |

This record declares all three and **asserts none**, with `resolved: false` and an empty `ruling_source`.
The two island nodes on the board are **not** equated with either place, and
`local_geography.problems()` reports any relation that claims to be resolved without a cited ruling.
The restricted island's legal autonomy is carried in the same place.

## 4. The island count — **CLOSED** in the configuration, with the trade-off recorded

**The gap.** #324 asks for *one modern city, multiple islands and 6–8 simple locations*, with one island
in the set marked restricted; and the setting bible
([`../world/PEOPLES_REPUBLIC_OF_UKWELI.md`](../world/PEOPLES_REPUBLIC_OF_UKWELI.md) §8) states as
**CANON**: *"One city plus 3–4 islands represented by 6–8 location nodes, one marked restricted."* The
live configuration carried **two** island nodes (`outer_island`, `airfield_island`) and **no** restricted
node, so the configuration contradicted the canon it was meant to instantiate. An exclusion island is
canon in its own right: #325 designates an entire island a prohibited/protected zone, publicly to
safeguard Ukweli's biodiversity.

**What landed.** The board now carries **three island nodes, one of them restricted**, still inside the
eight-node cap both issues state:

| Node | Role | `island` | `access` |
| --- | --- | --- | --- |
| `outer_island` | villages, tourism, ferry-dependent communities | true | open |
| `airfield_island` | the strategic island: airfield and communications | true | open |
| **`exclusion_island`** | **the biodiversity exclusion zone** | true | **restricted** |

**The trade, stated rather than hidden.** Eight is the cap, and the board was already full, so a third
island could not be added without folding a city role. The **historic quarter is folded into the
waterfront civic node** (`civic`, now *Old Harbor and Civic Centre*), keeping its `heritage` and `trade`
tags. The role chose itself on the least-loss principle: the historic quarter and the civic centre are
two faces of one waterfront, whereas the *coastal hinterland* is a different kind of place — mainland
countryside and the identity party's rural base — and cannot be folded into an urban node. The location
labels are explicitly **proposals**, not recovered canon (`REPUBLIC_OF_UKWELI.md`), so folding one edits
a proposal rather than canon.

**The restricted island carries no route.** No ferry or bridge edge connects it, so no leader reaches it
under the provisional travel rules in `local_slice.py` — which is what a *prohibited zone* means, and it
means the restriction is expressed as structure rather than as a rule about the board.

**PENDING — the author's part.** Recorded in `island_count.pending`: **three island nodes or four**: and
if a fourth is wanted, **which listed city or environs role gives way**. Choosing the count and the trade
is a scenario decision, so it is recorded as an option list, never picked.

## 5. What landed, and where

| Artefact | What it is |
| --- | --- |
| `strategy_game/data/ukweli_geography.json` | the declared geography: the island set, the naming registers, the open relations and the pending decisions |
| `strategy_game/local_geography.py` | the reader and the validator (islands, the single exclusion island, the naming registers, the still-open relations) |
| `strategy_game/tests/test_local_geography.py` | 38 executable contracts over that record |
| `strategy_game/data/ukweli_local.json` | the board: three island nodes, one restricted; the folded civic node; the official name in `setting` |
| `strategy_game/data/city_scenario_schema.json` | the generic location record gains optional `island` (bool) and `access` (`open` / `restricted` / `prohibited`) — a reusable capability for any city, not an Ukweli special case |
| `docs/scenarios/REPUBLIC_OF_UKWELI.md`, `docs/world/PEOPLES_REPUBLIC_OF_UKWELI.md`, `strategy_game/docs/INTERFACE_SPIKE.md`, `strategy_game/docs/CITY_SCENARIO_SCHEMA.md`, `strategy_game/README.md` | the label lists and the schema notes, updated to match the configuration |
| `ISSUE_324_ACCEPTANCE.md` | an addendum pointer, and the island row corrected on landing |

## 6. #324's acceptance bullets, revisited

The merged acceptance record walked all eight bullets; this table records **only what the addendum
changes or leaves open**, so the two do not fork:

| Bullet | Position after this addendum |
| --- | --- |
| One modern city, multiple islands, 6–8 simple locations, no national/global playable map | **Strengthened.** Three island nodes, one restricted, still eight locations and seven routes |
| Existing lore checked for continuity, preserved/revised elements attributed | The state-name registers are now attributed to #325 as the source, and the party-label conflict is attributed to both sides rather than to one |
| Geography, culture and politics remain scenario data, not engine assumptions | **Strengthened.** The island/access markers are schema fields on a location record; no engine code reads them |
| *(carried-forward)* the state's formal name | **Closed as a register mapping**, with the informal-form question PENDING |
| *(carried-forward)* the third party's name | **PENDING**, deliberately, matching #326 |
| *(carried-forward)* the restricted island's relationship and legal autonomy | **PENDING**, carried as three named options |

## 7. What this record deliberately does not do

- It **decides no canon question**: the informal short form, the party label and the island relation all
  stay PENDING, each with a reason and a container.
- It **adds no rule, number, threshold, magnitude or scale**: `numeric_scale_approved` stays false in the
  record, and nothing here is read as a cost, a route, a control or a score.
- It **does not re-open #324** or restate the schema work PR #379 landed; it cites that record and adds
  to it.
- It **touches no file** owned by #325 for society or by #326 for people: the setting bible gains a
  corrected label list, not new lore.
- It carries **no test over prose**: the contracts in `test_local_geography.py` exercise the record and
  its validator, never a document's wording (#271).
