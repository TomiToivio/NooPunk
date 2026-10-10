# NoöPunk rulebook segmentation and editorial ownership

**Status: lossless staging, not a replacement of the canonical `RULEBOOK.md`.**

Issue [#232](https://github.com/TomiToivio/NooPunk/issues/232), parent [#200](https://github.com/TomiToivio/NooPunk/issues/200).

The original rulebook was **320,640 characters** when segmented. Its complete text, including introductions, mechanics, sources, glossary, faction lore, duplicated or historical descriptions and all later appended material, is preserved **in original order** in nine files under this directory. The `manifest.json` records exact start/end offsets; the files can be reassembled from `manifest.json` and compared with the canonical source by hand (the former `test_issue232_lossless_segments.py` was removed under issue #271 as a documentation test). **No sections were removed, rewritten, reconciled, superseded or silently dropped** in this operation. Existing `rulebook/*.md` chapters and the root `RULEBOOK.md` remain as they were.

| Snapshot | Coverage in original rulebook | Proposed eventual book ownership |
| --- | --- | --- |
| [01_PLAYER_CORE.md](01_PLAYER_CORE.md) | Introduction, history, attributes, Skills and original contents | **Basic Rules** / **Lore** split later |
| [02_DOMAIN_QUICKSTART.md](02_DOMAIN_QUICKSTART.md) | Original Physical, Social, Cybernetic and Psychic chapter stubs | **Physical**, **Social**, **Cybernetic**, **Psychic** books |
| [03_CHARACTER_GENERATION.md](03_CHARACTER_GENERATION.md) | Initial lifepath and character generation | **Character Generation** |
| [04_CORE_REFERENCE.md](04_CORE_REFERENCE.md) | Older extended rules architecture through cyber/PSI coverage | **Basic Rules** plus domain books |
| [05_SYSTEMS_AND_ENGINEERING.md](05_SYSTEMS_AND_ENGINEERING.md) | Extended social/gear/AI, simulation and engineering notes | **Social**, **Cybernetic**, **GM Reference** |
| [06_WORLD_CANON.md](06_WORLD_CANON.md) | Extended canonical world history and setting material (§33) | **NoöPunk Lore** |
| [07_GLOSSARY_AND_SOURCES.md](07_GLOSSARY_AND_SOURCES.md) | Glossary, references, source discussion | **Lore**, references and credits |
| [08_WORLD_SYSTEMS_AND_CAMPAIGN.md](08_WORLD_SYSTEMS_AND_CAMPAIGN.md) | Four-system theoretical framework and campaign, faction, UNSA lore | **GM Reference** / **Lore** / domain books |
| [09_LATE_LORE_AND_CATALOGS.md](09_LATE_LORE_AND_CATALOGS.md) | Late lore, NHI, psychotronics, field catalogs and equipment | **Lore**, **Psychic**, **Cybernetic**, **Physical** |

## Target reading structure: seven readable books

This is an **editorial destination**, not a new mechanical design. Prefer a small root `RULEBOOK.md` as an index **only after** migrations preserve old anchors/links and all tests pass.

1. **Basic Rules:** shared Fudge/Fate-inspired Attribute+Skill engine, -3..+3 difficulty scale, action resolution, outcomes, clocks, cross-domain AP.
2. **Character Generation:** lifepath, UNSA academy, stat/skill assignment, specialist fields, faction affiliations, advancement.
3. **Physical Systems:** physical skills, tactical conflict, harm, weapons/armor, first aid, vehicles.
4. **Cybernetic Systems:** implants, Interface/Network/Compute, local AR/WLAN, graph hacking, global networking, immersive VR, AI agents.
5. **Psychic Systems:** psychic traits, ESP/PSI/psychotronics, dreams, projection and Noöspace encounters, altered states.
6. **Social Systems:** relationships, motivations, faction/affect networks, dialogue, investigation, evidence and reputation.
7. **NoöPunk Lore:** chronological 20XX world, Singularity Crisis, NHI/xenopolitics, factions, species/beings, theory, citations, glossary and detailed catalogs.

A separately navigable **GM toolkit** can be a subsection/book later if it becomes sufficiently large; do not duplicate universal roll, AP or skill formulas. Player-facing and GM-facing chapters should reference the same canonical domain rules and source tables. The tabletop rulebook is the source of truth for computer runtime and Concordia/Ollama integrations.

## Agent file ownership and concurrency

| Child issue | Owns editorial section after canonical migration |
| --- | --- |
| [#217](https://github.com/TomiToivio/NooPunk/issues/217), [#225](https://github.com/TomiToivio/NooPunk/issues/225) | Basic Rules core / shared AP |
| [#218](https://github.com/TomiToivio/NooPunk/issues/218) | Character Generation |
| [#219](https://github.com/TomiToivio/NooPunk/issues/219), [#228](https://github.com/TomiToivio/NooPunk/issues/228) | Physical Systems / inventory interfaces |
| [#221](https://github.com/TomiToivio/NooPunk/issues/221), [#222](https://github.com/TomiToivio/NooPunk/issues/222) | Cybernetic Systems |
| [#223](https://github.com/TomiToivio/NooPunk/issues/223), [#224](https://github.com/TomiToivio/NooPunk/issues/224) | Psychic Systems |
| [#220](https://github.com/TomiToivio/NooPunk/issues/220), [#226](https://github.com/TomiToivio/NooPunk/issues/226) | Social Systems / investigations |
| [#227](https://github.com/TomiToivio/NooPunk/issues/227), [#230](https://github.com/TomiToivio/NooPunk/issues/230) | Beings, Lore, GM toolkit |
| [#229](https://github.com/TomiToivio/NooPunk/issues/229) | Narrative rules integrated with Basic and Social |
| [#231](https://github.com/TomiToivio/NooPunk/issues/231) | Copyright notices, provenance, release license |
| [#232](https://github.com/TomiToivio/NooPunk/issues/232) | Migration/integration, navigation, loss checks, runtime parity |

**Until the index cutover, update canonical `RULEBOOK.md` or already existing `rulebook/*.md` following existing author/agent governance, not these generated snapshots.** If someone changes the root file, the reconstruction guard will fail until #232 re-segments the new complete text, proving changes were incorporated. Assign one agent to regenerate snapshots from the new root rather than having everyone edit overlapping duplicates. Do not modify the snapshots independently and then mistake them for the published book.

## Integrity checks and later migration

- [x] Source text segmented into nine contiguous excerpts in original order.
- [x] Every excerpt recorded in `manifest.json` with source offsets.
- [x] No canonical file or existing chapter modified.
- [x] Exact reconstruction guard for full content.
- [ ] Move *approved canonical text* to the seven future book sections, preserve every passage (or explicitly archive obsolete historical notes), citations and existing link targets.
- [ ] Decide cross-book link/anchor compatibility and a link-checker before replacing `RULEBOOK.md` with a navigation index.
- [ ] Re-run all tests and inspect diffs for dropped sections and contradictory rules after each migration.
- [ ] Ratify CC license and verify third-party rights before republishing any copied expression.

This work is intentionally compatible with other agents editing combat, hacking, psi, social systems and lore on separate branches.
