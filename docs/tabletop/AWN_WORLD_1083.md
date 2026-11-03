# AWN world records: tabletop procedure (#1083)

This is an **optional NoöPunk overlay**. CWN character checks, healing, combat and saves, SWN faction turns, and the AWN region ledger stay unchanged. This is a format for recording scenario decisions, not a reproduction of AWN tables. AWN licensing remains unverified (see `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`).

## Pencil-and-paper procedure

1. Create a region on the region sheet (`src/rules/awn_region.py`). Write its ID and current date. Do not label the whole world collapsed merely because one region has failed.
2. Place each enclave in **exactly one** region, recording its ID, name, tags, current dominance and cohesion as descriptive text. Do not invent numerical AWN ratings. Enclave decisions happen when narrated events justify them, not on SWN faction turns.
3. Describe sites separately: ID, region, optional enclave, tags, features, occupants, hazards and possible salvage. These are **scenario-authored** facts. A tag does not award equipment, roll a check, or imply an encounter.
4. For a crisis, name a region, a crisis ID and a nonnegative pressure counter. Start at zero unless the author recorded a different opening condition. The counter is NoöPunk **tracking metadata**, not an AWN rules table. A dated event with a clear cause can add or subtract pressure. Mark it resolved only after a narrated stabilizing event. Passing time alone changes nothing.
5. On each scene consequence, write the event ID, ISO date, target, cause and source. A CWN mission contributes *evidence* to the ledger; it does not itself run a faction turn. SWN faction assets link by ID to an enclave, but SWN remains the authority for asset mechanics.
6. When using the Python library, `WorldLedger.to_dict()` is the paper sheet's JSON equivalent, and `from_dict()` loads that state. World records do not silently enter an existing save schema; the host campaign must opt in and persist the ledger separately until a tested migration exists.

## Distinct clocks and authority

| Scale | Authority | Advances only when |
| --- | --- | --- |
| Character action | CWN / shared case session | Player takes a validated action |
| Enclave or crisis | Optional `awn_world.WorldLedger` | Dated, caused world event is recorded |
| Material-collapse region | `awn_region.RegionLedger` | Dated, caused region transition |
| Faction assets and turns | SWN faction engine | Its published faction procedure advances |

**No shared turn loop. No rules in adapters. No automatic apocalypse.**

## Acceptance and remaining work

The present increment includes the cross-scale model, reference validation, event provenance, serialization and unit tests. It **does not** claim AWN's settlement statistics/actions/turns, a full Python Stress tracker, a playable crisis campaign, physical Tarot cards, spell effects, new GUI/LLM engines or authored story material.

The outstanding work is tracked in #1080, #1081, #1083, #1084 and #1085. #1086 decisions D70, D71 and D74 are explicitly reserved for the author. No agent-created episode, personality or side-quest is canonical.

### Manual example (pure NoöPunk tracking, not AWN rule numbers)

- Region: `helsinki`; enclave: `kurvi`; site: `tunnel`; faction asset `relay` belongs to `unsa` at `kurvi`.
- A dated incident causes `blackout` pressure to increase by 2, **because the author records that incident**.
- A later successful CWN mission supplies source evidence; a separate, narrated restoration event reduces the counter by 2 and marks the crisis resolved.
- No time advance, encounter reward or SWN faction action is inferred from the above.


## AWN opt-in eligibility and crossing a border (#1109)

**NoöPunk regional integration rule**, not a published AWN character or combat replacement. On the
GM's regional sheet, tick **AWN active** only if this optional layer is enabled for the campaign.
For each scene, locate its region and read the most recent dated region state. If AWN is off,
ignore the region's AWN-only scarcity and anomaly-response overlays; do not erase existing
regional facts, previous events, Stress or saved world records. Continue ordinary CWN checks,
System Strain, combat and healing as usual. Independent SWN psionics/faction and WWN options
are governed by their own availability and never switched on or off by this AWN checkbox.

If AWN is on, the region sheet supplies the following *NoöPunk activation policy*: a
functioning region with no active anomaly adds nothing; an emergency region adds privation
strain; an After the Fall material state additionally brings travel/supplies and site hazards;
recorded anomaly activity can add anomaly response. These are eligibility names, not new
unpublished dice bonuses or automatically applied injuries. Where a named procedure does not
exist, the GM uses the published CWN check and records the AWN-specific gap.

**Paper example (2045, two locations):** A UNSA team interviews a witness in functioning
Helsinki. Although the witness has suffered a global ontological shock, there is no automatic
regional hunger/privation check. The same team then enters a ruined western-US quarantine
sector with failed supply chains. With AWN checked on, travel/supply and hazard procedures
become eligible there, while their CWN character sheets, psychic skills and saved Stress
meters remain the same. An aid convoy dated the next day restores the sector's supply state
from `after_the_fall` to `emergency`: the GM writes the event, cause and provenance, then
removes the travel/supplies and site-hazard eligibility once no other material axis remains
collapsed. Turning AWN off temporarily would have hidden effects without erasing this recovery.

**Python mirror:** `RegionState.active_overlays(awn_enabled=False)` returns `()`;
`RegionLedger.world_at(date, awn_enabled=False)["overlays"]` returns `{}` while
`to_dict()` remains unchanged. Test: `tests/test_awn_region.py::OptionalAWNActivation1109Tests`.
