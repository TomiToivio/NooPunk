# HELSINKI — FACTIONS (template, #1141)

> **STATUS: TEMPLATE / DRAFT OUTLINE. Agent-written scaffolding, not canon.**
> Companion documents: [WORLD](HELSINKI_WORLD.md) · [CITY](HELSINKI_CITY.md) · **FACTIONS** (this file) ·
> [FACES & XENOBESTIARY](HELSINKI_FACES_XENOBESTIARY.md).
>
> **Source:** *Stars Without Number (Revised)*, **Factions** — faction statistics and the faction turn
> from printed **p. 211**; the asset catalogue from printed **pp. 219 (Cunning), 221 (Force),
> 223 (Wealth)**. The repository holds no copy of the book; asset rows quoted below come from
> [`data/rules/swn_faction_assets.json`](../data/rules/swn_faction_assets.json), which records the
> printed page for each row. **Verify the edition you hold before relying on a printed number.**
> Coverage and licensing status: [`docs/rules/SWN_COVERAGE_1105.md`](../docs/rules/SWN_COVERAGE_1105.md).

## Scope: local actors only

This file holds **Helsinki-area actors that affect the Europol rookie campaign**. It is not a galactic
or global faction encyclopedia: the Confederacy, Orion, UNSA and megacorporations appear only as a
**local cell or presence**, and only if play actually needs one. Global factions stay in
[`docs/world/NHI_FACTIONS_922.md`](../docs/world/NHI_FACTIONS_922.md).

**Not every organisation is a mechanical faction.** A union, a police unit or a street gang becomes one
only when it takes faction turns, holds assets and competes for influence. Everything else is an
organisation with a name and a jurisdiction — [CITY](HELSINKI_CITY.md) §3.

**Rules boundary.** SWN Revised is the faction-turn model (**Force**, **Cunning**, **Wealth**,
FacCreds, goals, assets). WWN's faction/major-project tooling and AWN's **Enclaves** are *alternatives
for a different scale*, not extra wallets. CWN core rules are untouched, and CWN is not a faction
system — SWN fills that gap here, explicitly.

## How to use this file

1. Heading, **one labelled example**, `<!-- Tomi writes below -->`.
2. Statuses: **AUTHOR CANON**, **REPOSITORY CANON**, **EXAMPLE ONLY / NOT CANON**, **OPEN**,
   **GM SECRET**.
3. **Never guess a printed statistic.** If a value is not verified against the source you hold, it is
   `TBD`, not a plausible number.
4. Stable IDs: `hel_faction_*`, `hel_asset_*`. Assets are defined **inside** their faction record; do
   not create a second asset catalogue.

---

## 1. The faction record

| field | meaning | source |
| --- | --- | --- |
| `faction_id` | stable key | — |
| `name`, `scope` | who, and where they can act | — |
| `source_system` | `swn_faction` \| `wwn_project` \| `awn_enclave` | see §4 |
| `force`, `cunning`, `wealth` | the three faction statistics | SWN p. 211 |
| `fac_creds` | faction currency | SWN p. 211 |
| `goal` | the current faction goal | SWN p. 211 |
| `tags` | faction tags | SWN p. 211 |
| `base_of_influence` | the asset that anchors the faction | asset catalogue |
| `force_assets`, `cunning_assets`, `wealth_assets` | asset rows with location and HP | pp. 219/221/223 |
| `jurisdiction`, `relations` | local legality and who tolerates whom | this file |
| `campaign_visibility` | Act in which the player can perceive them | campaign outline |
| `player_interactions` | what a Europol officer can do to/with them | — |

```yaml
# EXAMPLE ONLY — NOT CANON
faction_id: hel_faction_001
name: "Helsinki municipal infrastructure unit"
scope: "Greater Helsinki only"
source_system: "swn_faction"
force: "TBD — determine by SWN procedure"
cunning: "TBD — determine by SWN procedure"
wealth: "TBD — determine by SWN procedure"
fac_creds: "TBD"
goal: "Keep city services running through a crisis"
tags: ["public mandate", "budget constrained"]
base_of_influence: "TBD"
force_assets: []
cunning_assets: []
wealth_assets: []
jurisdiction: "Municipal; cannot arrest or search."
relations: ["hel_org_001 (co-dependent)", "hel_corp_001 (contractor)"]
campaign_visibility: "Act I"
player_interactions: ["Request a utility record", "Trade a favour for a shutdown"]
source: "illustrative"
```

<!-- Tomi writes below -->

---

## 2. One sample of every asset category

These are **real catalogue rows** (name, cost, HP, printed page) taken from
[`data/rules/swn_faction_assets.json`](../data/rules/swn_faction_assets.json) — not invented numbers.
They illustrate the format only; the faction above does not own them until you say so.

```yaml
# CATALOGUE EXAMPLES — real rows, illustrative ownership
cunning_assets:
  - source_asset_id: false_front        # "False Front", cost 1, HP 2, p. 219
    location: hel_district_kurvi
force_assets:
  - source_asset_id: hitmen             # "Hitmen", cost 2, HP 1, p. 221
    location: hel_district_kurvi
wealth_assets:
  - source_asset_id: franchise          # "Franchise", cost 2, HP 3, p. 223
    location: hel_district_kurvi
```

<!-- Tomi writes below -->

**Rule:** an asset's special ability is **printed rules text**; the table reads the entry. The Python
side (`src/rules/swn_faction_turn.py`, `swn_faction_assets.py`) implements bookkeeping only, never a
paraphrase of an ability.

---

## 3. One worked faction turn (bookkeeping only)

The engine validates legality — one action per turn, committed assets alive, credits sufficient. **The
dice and the asset tables belong to the table.** This example is executable today:

```python
from rules.swn_faction_turn import Asset, Faction

faction = Faction(identifier="hel_faction_001", credits=4)
faction.add_asset(
    Asset(identifier="hel_asset_false_front", faction="hel_faction_001",
          location="hel_district_kurvi", hp=2, max_hp=2,
          tags=("cunning", "false_front")),
    cost=1,                      # printed cost of "False Front" (p. 219)
)
event = faction.act("expand", asset_ids=("hel_asset_false_front",),
                    target="hel_district_kallio")
faction.next_turn(income=1)      # income is the table's result, not an engine guess
```

```yaml
# EXAMPLE ONLY — the same turn on paper
# 1. Income: table result -> 1 FacCred (record it, do not compute it in the engine)
# 2. Action: expand, using False Front (p. 219) into Kallio
# 3. Resolve the printed roll at the table; apply the printed consequence
# 4. Record the asset's new location and HP; one action spent
```

<!-- Tomi writes below -->

---

## 4. Delegating to WWN or AWN (choose one mode per actor)

| mode | use when | why |
| --- | --- | --- |
| `swn_faction` | the actor competes for influence with assets and goals | SWN's turn is the campaign's strategic clock |
| `wwn_project` | the actor pursues a **single long endeavour** (a bridge, a treaty, a cure) | WWN models projects, not influence warfare |
| `awn_enclave` | the actor is a **settlement** managing survival and growth | AWN models communities, not factions |

**One actor, one mode.** Taking a faction action and an enclave action for the same organisation in the
same turn is double-dipping: choose the frame that describes what it is trying to do, and record the
delegate explicitly. WWN project and AWN enclave tooling live in
[`src/rules/wwn_projects.py`](../src/rules/wwn_projects.py) and
[`src/rules/awn_world.py`](../src/rules/awn_world.py); the enclave/crisis/site ledger is #1089.

---

## 5. Reputation is not a faction statistic

A character's standing with a local actor is a **character tag** — the proposed −4…+4 scale from
[#1137](https://github.com/TomiToivio/NooPunk/issues/1137) — and it belongs on the character sheet, not
in the faction's Force/Cunning/Wealth. Confusing the two produces the classic bug: a player's opinion
score silently becoming an organisation's military strength.

```yaml
# EXAMPLE ONLY — NOT CANON
reputation:
  hel_faction_001: { value: -1, why: "Closed a case that embarrassed the unit", tag: "obstructive" }
```

<!-- Tomi writes below -->

---

## 6. What this file will not do

* No invented asset, cost, HP or ability value — unverified rows are `TBD`.
* No global faction encyclopedia; local presence only.
* No second economy: one faction wallet, one mode per actor.
* No CWN change. Factions act in the strategy layer; the rookie still resolves a search with CWN.

## Unresolved decisions in this document

| # | question | blocks |
| --- | --- | --- |
| F1 | Which local actors are mechanical factions, and which are merely organisations? | the whole file's scope |
| F2 | Are the fictional example ids (`hel_faction_001` etc.) replaced by real cast, or reused? | cross-references from CITY and FACES |
| F3 | Does the campaign want a faction turn at all in Act I, or only from Act II? | pacing; whether SWN is needed early |
| F4 | Which actors are Orion- or Confederacy-adjacent, and do they know it? | Act II antagonists |

*Record answers here, in this file, with a date and the author's name.*
