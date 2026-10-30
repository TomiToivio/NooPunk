# SWN Revised → NoöPunk conversion matrix

> **Coverage column partly superseded, 2026-10-30:** "pending" cells below describe the state before
> the 2026-10-26 [Without Number baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md) and before #749's
> Godot slice. The chapter map and the licence boundary stand. Current per-subsystem dispositions:
> [`ISSUE_747_WN_RESKIN_MATRIX.md`](../design/ISSUE_747_WN_RESKIN_MATRIX.md); the Godot engine gaps are
> measured in [`ISSUE_749_MVP_DELIVERY_LEDGER.md`](../godot/ISSUE_749_MVP_DELIVERY_LEDGER.md).

Source: *Stars Without Number Revised* (Kevin Crawford, Sine Nomine, © 2017), user-supplied deluxe PDF, 325 PDF pages. Printed chapter starting pages below follow the book table of contents. This is a design and implementation map **not a reproduction of copyrighted source prose or tables**. Refer to the authorized book for power, item, ship and faction asset catalogues.

**Architecture:** Cities Without Number remains the primary rules chassis for ordinary characters, combat, injury, cyberware and hacking. SWN is supplementary for psionics, space, alien creatures, strategic factions and appropriate science-fiction equipment; WWN is supplementary for interdimensional worlds and AWN for disaster regions. Preserve the grounded Nordic investigative starting scenarios; spacefaring is optional and appears later.

| SWN chapter (printed start) | NoöPunk adaptation | Repository integration | Coverage |
| --- | --- | --- | --- |
| Character Creation (3) | Existing six stats, attributes and skill checks; CWN character core is authoritative | `src/rules/wn_core.py`, `src/rules/cwn_advancement.py` | Shared chassis present; SWN backgrounds and class/foci equivalences not fully mapped |
| Psionics (29) | Natural psychic disciplines with separate BCI and psychotronic sources | `src/rules/swn_psionics.py`, `src/rules/swn_progression.py`, `src/rules/psionics.py` | Effort, basic progression; power catalogue, torching pending |
| Systems (45) | Reuse CWN skill checks, saves, conflict, injuries and System Strain | `src/rules/wn_core.py`, `src/rules/cwn_*.py` | Major shared mechanics present; detailed delta audit pending |
| Equipment and Vehicles (61) | Use present CWN cyberpunk gear, augment with SWN future technology and vehicles | `data/rules/`, `src/rules/equipment_catalog_index.py` | Catalogue delta and vehicle maneuvers pending |
| Starships (93) | Modular hull, drive, cargo, fuel, defenses and combat roles | `src/rules/swn_sector.py` | Added travel budget model; construction and ship combat pending |
| History of Space (121) | Replace SWN's default history with NoöPunk's NHI Crisis, AGI acceleration, UN and interdimensional discoveries | World lore | SWN history intentionally not imported |
| Sector Creation (129) | Region/planet/Noöspace node graph with hazards and scenario tags | `src/rules/swn_sector.py` | Basic route validation present; procedural generation pending |
| Adventure Creation (173) | Investigation case generator with ambiguous anomalous evidence and faction consequences | Existing NoöPunk scenarios | Complete table conversion pending |
| Xenobestiary (193) | NHI, alien ecology, hybrid and anomalous NPC archetypes | Existing world/scenario schemas | Creature statistics and reactions pending |
| Factions (211) | Turn, assets, resources, action commitment; three human blocs + NHI factions | `src/rules/swn_faction_turn.py` | Added one-action scheduler and ownership checks; canonical asset actions/combat pending |
| Game Master Resources (231) | Case prep, events, recurring contacts and active timelines | Scenario tools | Crosswalk pending |
| Transhuman Campaigns (248; deluxe) | Sleeving, identity, augmentation, transhuman social systems | NoöPunk cybernetics/world | Future adaptation |
| Space Magic (266; deluxe) | Interdimensional science fantasy, not evidence of real-world paranormal truth | NoöPunk Noöspace | Future adaptation |
| Heroic Characters (274; deluxe) | Optional cinematic campaign setting; regular campaign remains dangerous | Optional mode | Future adaptation |
| True Artificial Intelligences (280; deluxe) | Rogue AGI, Blackwall, NHI/AI distinctions, restricted UN technology | NoöPunk AGI canon | Future adaptation |
| Societies (290; deluxe) | Societal traits, ideologies and regime dynamics | NoöPunk faction/simulation | Future adaptation |
| Mechs (300; deluxe) | Rare combat walkers and cyberpunk industrial exoskeletons | Vehicle/combat | Future adaptation |

## Rules integration contracts and safeguards

* The new `swn_sector` model deliberately takes scenario-specified travel days, fuel and drive requirements; it does **not** claim to reproduce SWN spike-drive numerical tables.
* The new `swn_faction_turn` model manages ownership, currency, one action per turn and commitments. It does **not** resolve canonical SWN asset combat, movement or buying prices. Records carry `resolved=False` until another system resolves them.
* Do not replace existing CWN combat or healing with incompatible duplicate SWN routines.
* Do not copy the uploaded PDF or any copyrighted prose, creature write-ups, ship lists or tables into this public repository. Implement original descriptions and selectively adapt mechanics.
* Preserve the user's tonal direction: recognizably contemporary Nordic reality with incremental anomalies, not default interstellar space opera.

## Next required implementation slices

1. SWN ship design and ship-to-ship tactical combat with original test fixtures, linked to the CWN action model.
2. SWN faction rating and asset consequences, with deterministic, scenario-driven outcomes and campaign persistence.
3. Sector and adventure generation contracts, alien/NHI archetypes and optional off-world mission examples.
4. Transhumanity, AI, societies and mechs, each as separate optional mechanics packages.
5. SWN psionics individual effects, torching and System Strain, with Godot/Python parity.
6. Integrate adapters in Godot; run full Python/Godot validation before claiming playable completeness.

Tests for this incremental stage: `python -m unittest tests.test_swn_space_factions`.
