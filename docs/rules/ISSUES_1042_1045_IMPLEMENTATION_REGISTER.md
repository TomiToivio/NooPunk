# NoöPunk cross-system implementation register (#1042–#1045)

**Scope:** A staged integration register, not a claim of complete SWN/WWN/AWN rules parity. The Cities Without Number (CWN) mechanics remain authoritative and unchanged. New Evennia-compatible components must be optional, deterministic, persistent, and auditable. The older Godot implementation is not the canonical target.

## #1042: LaclauGPT DA/DNA/SNA, status: foundational code added
- New pure-Python optional `mud/nopunk_mud/discourse_network.py`: versioned snapshot; DA identity, values, demands, signifiers, antagonisms and goals; DNA actor–concept–stance–source–event records; SNA communication and affiliation records; separate explicitly-authorized game trust/access/reputation.
- Positions support `observed`, `fictional` and `gameplay` provenance. Agreement/conflict is calculated from explicit public, certain statements, not from communication or personal trust. An external caller must control visibility and observed knowledge.
- **Still needed**: wire the ledger into actual Evennia persistence and command visibility; deterministic event ingestion from meaningful investigative dialogue; identity reconciliation, player fog-of-war authorization, playable Helsinki case, UI; evidence reconciliation with LaclauGPT research schemas. The ledger is an interface prototype, not a completed campaign.
- **Later**: SWN faction-turn projection, UNSA Country Director (nondeployable), finite field-agent roster, faction-only support personnel, organization-versus-individual ideology, time-series brokerage/switchers. Do not allow dialogue to create free strategic actions.

## #1043: SWN Revised import register
**High priority and still required:** the *full* SWN Revised Psionics chapter and Factions chapter. Existing `tests/test_swn_psionics.py`, `tests/test_swn_faction_operations.py`, `tests/test_swn_space_factions.py`, `tests/test_psionics_catalogue.py` and MUD faction overlays indicate earlier work but **do not independently prove SWN chapter-level parity**. Run and audit those tests and inspect the implementation before calling any component complete.

### Psionics (SWN Revised printed p. 29 onward)
- [ ] Psychic and Partial Psychic compatibility with CWN character creation and advancement.
- [ ] **Biopsionics, Metapsionics, Precognition, Telekinesis, Telepathy, Teleportation:** complete discipline/technique list, training, acquisition, level gates, targeting, range, saves, and environment constraints.
- [ ] Psychic Effort maximum, commitment duration and recovery; System Strain and torching consequences.
- [ ] Persistent psychic state for PCs and NPCs, command discovery, activation and failure handling; no free PSI from BCI/psychotronic tags.
- [ ] Rule-page parity matrix and deterministic tests per technique, edge case, persistence and CWN compatibility.

### Factions (SWN Revised printed p. 211 onward)
- [ ] Force, Cunning, Wealth, FacCreds, XP/goals and all source-defined asset categories, stats and costs.
- [ ] Faction turn, actions, asset movement, attacks, defenses, loss, faction growth, goals and economy with seeded determinism and persistence.
- [ ] UNSA institutional hierarchy, finite deployable CWN agent roster, faction-only blue berets/police/scientists/analysts; mission-support cost validation.
- [ ] Country Director usable **only in faction turns**; never field-deployable.
- [ ] Integrate DA/DNA/SNA through *projection*, not a second replacement faction engine.

Other SWN chapters remain **on-demand/deferred**, including Systems, Equipment/Vehicles, Starships, Sector and Adventure Creation, Xenobestiary, GM Resources, Transhuman Campaigns, Space Magic, True AI, Societies and Mechs.

## #1044: WWN / occult science fantasy
**Current implementation priority: High Mage**, not wholesale WWN migration.
- [ ] Full/Partial High Mage eligibility and progression crosswalk to CWN.
- [ ] Arts, High Mage Effort and commitment/recovery semantics; ritual/preparation, spell slots and levels, saves and interruption.
- [ ] Source-linked coverage table for every High Magic spell, with unit tests and an Evennia character/NPC vertical slice.
- [ ] Maintain separate WWN magic and SWN psionics game resources, while using one in-universe Hermetic/PSI ontology. No double-granted abilities.
- [ ] Compare WWN Factions/Major Projects (including Magic rating, projects and renown) with existing SWN baseline; assess additive-only faction fields rather than replacing SWN.
- [ ] Build WWN section backlog: character options, classes/foci, rules gap audit, magic/arcane traditions, bestiary and anomalous encounters, faction/project options, campaign/adventure generators, magic items and occult apparatus.
- [ ] Law of One **106-session coverage ledger**: source session, concept, reskin vocabulary, fictional interpretation, faction, lore-versus-mechanic, implementation status. This has **not** been performed by this code-only first pass. Apply real-world mythology and ufology, no Tolkien races or copied Otherscape expression.
- Reference: WWN Free (2021) *Magic and Arcane Traditions*, *Factions and Major Projects*, user-provided copy; https://wwn.quadrifons.com/ and https://www.lawofone.info/.

## #1045: AWN localized After the Fall and optional Crisis Campaign
- New `mud/nopunk_mud/crisis_regions.py`: persistent named regions, global disclosure flag independent from local physical collapse, opt-in `functioning / emergency / after_the_fall / contested / recovering` labels, source event ID and reason for transitions, independent severity axes for infrastructure, safety, supplies, governance, communications, anomalies, ontological shock. This is **original NoöPunk state**, not a direct copy of an AWN mechanic.
- Existing `docs/AWN_STRESS_928.md` describes prior AWN Stress, Breakdown and Hardening implementation: reuse and verify against current MUD rather than duplicate.
- **Still needed**: AWN chapter-level parity inventory with confirmed source mechanics, region-to-scene activation, population and logistics simulation, enclave turns, crisis turns, recovery pathways, crisis-site generator, Evennia integration and tests.
- AWN printed section inventory: Character Creation (4–35: backgrounds, edges, mutations, stigmas, foci); Rules (36–69: combat/major injury, healing/disease/radiation, stress/addiction, tracking/travel/hunger/supplies); Equipment (70–103: repair, scrap/build/mods, arms/armor, vehicles, mysterious tech); Enclaves (104–135); Campaigns (136–201: crisis/exploration modes, regions, crises, sites, hazards and adventures); Creatures (202–229); Albuquerque example (230–253, **not imported canon**); Deluxe Supplement (254–293: techno-wizards, Ash Sorcerer, Mentalist, power armor, hubs, mass combat).
- Comparison needed: AWN enclaves are **local survivor communities**, SWN factions are **strategic organizations**, WWN major projects are **project objectives**. Cross-reference rather than merging their clocks and economies.
- Source: Kevin Crawford, *Ashes Without Number Deluxe* (2025), user-supplied PDF, not redistributable.

## Delivery gates
1. Every rules import has a source chapter/page, license review, deterministic acceptance tests, persistence test, and a no-change-CWN regression.
2. Separate **implemented**, **prototype**, **planned**, **blocked**, and **deferred**. Never close #1042 or #1043 on the basis of this register.
3. First vertical slices: a documented ideology-driven Helsinki NPC interaction; one SWN psychic technique and one full faction turn; one WWN High Mage spell and Art; an AWN region transition and mission with aid/scarcity.
4. The full Law of One and complete source-rule catalogs require dedicated source-by-source audits.
