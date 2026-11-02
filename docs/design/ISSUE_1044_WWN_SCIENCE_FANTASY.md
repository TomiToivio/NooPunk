# Science-fantasy canon: WWN, Hermetic PSI, and the Law of One (source: #1044)

<!--
PROVENANCE: transcribed from the author's own issue text, unedited in substance.

STATUS: SOURCE MATERIAL, not an implementation order. Where the source says a rule must come from a book that
is not in this repository, the rule stays unimplemented here rather than guessed. Check the licensed book.
-->

# NoöPunk = Cyberpunk + Science Fantasy / New Weird (WWN integration and Law of One canon)

## Canonical creative direction
NoöPunk combines cyberpunk and fantasy, comparable structurally to *Shadowrun* or *Metro: Otherscape*. **Otherscape is the preferred aesthetic/worldbuilding reference**: adapt living, real-world mythologies, historical occultism, local beliefs and social institutions into a dystopian technological city. **No Tolkienisms**: do not introduce elves, dwarves, orcs, Tolkien-style races, or generic D&D fantasy cosmology. Never simply replace aliens with fantasy races.

NoöPunk's fantasy emerges from **UFO Disclosure and the resulting Ontological Shock / Ontological Apocalypse**. For the social and disclosure framing, investigate **Alexander Wendt**, **Diana Walsh Pasulka**, **Richard Dolan**. In-universe, **Jacques Vallée's and John Keel's interdimensional / ultraterrestrial account is substantially correct**, while the extraterrestrial hypothesis accounts for only part of the phenomenon. NHI includes more than extraterrestrial biological visitors. A cultural label such as *haltija*, *spirit*, *elemental*, *psychic construct*, *nonlocal intelligence* or *higher-density being* may reflect contested interpretations of encounters, not necessarily separate Tolkien-like species.

**The Law of One / Ra Material is the underlying canonical metaphysics of the setting**, heavily reinterpreted in Jacques Vallée-style science fantasy to avoid campy literalism. It should shape the cosmology but not become an infallible public explanation known to UNSA, factions, or player characters. Noösphere/PSI/NHI and local folklore should retain investigative mystery and ambiguity in-world. Avoid unsolicited real-world scientific-validity debates in creative worldbuilding.

## Locked system architecture
- **Cities Without Number (CWN) stays the permanent primary OSR rules engine**; do not change or replace its mechanics. Evennia MUD is the main game.
- **Stars Without Number (SWN)** supplies science-fiction expansions, especially psionics and the baseline faction system.
- **Worlds Without Number (WWN)** supplies fantasy/occult expansions and potentially supplementary faction features; selectively **add WWN rules only as needed**, as discrete opt-in compatible modules.
- AWN stress and other previously approved OSR extensions remain optional overlays.
- Existing GUMSHOE investigation, PbtA/The Veil Noösphere and LaclauGPT ideology mods must coexist without changing CWN core.
- Do not mistake Otherscape's elegant *worldbuilding* for an instruction to replace CWN with its tag resolution system.

## P0: IMPLEMENT WWN HIGH MAGE AS HERMETIC / PSI MAGICK
**This is the immediate implementation task.** Translate the WWN High Mage class/tradition into a clean selectable NoöPunk occult-PSI module in Evennia, using the actual WWN rules (not a bespoke fantasy caster).
- **Core interpretation:** magick and psionics are two traditions/technical vocabularies for PSI; use the Dean Radin-inspired NoöPunk premise **“magick is psionics; psionics is magick.”** This is the setting's model, not a requirement to flatten the distinct SWN and WWN game mechanics.
- Reskin **High Mage** as *Hermetic practitioner / ritual PSI operator*; translate spell nomenclature and narrative effects into consciousness, focused intention, ritual, symbols, altered states, noetic field manipulation, psychotronics, etc. It should be possible for factions/characters to disagree about whether they use “magic” or “psi”.
- Implement **Full/Partial High Mage**, class eligibility/advancement, Magic skill integration/mapping with CWN skills **without changing CWN skills**, spell repertoire, preparation, daily casting limits, spell levels, spell interruption/saves, High Mage Arts, art selection, High Mage Effort and commitment/recovery (day/scene/indefinite) exactly as supported by WWN. Review the *entire* High Mage spell list, implement legal/available spells in batches with a tracked coverage matrix. No silent omissions.
- Crosswalk with **SWN psionics**: identify overlap, coexistence, independent resource pools, compatibility with System Strain, cyberware/BCI and occult artifacts. Avoid granting power twice or collapsing mechanical distinctions by fiat.
- Start with a vertical slice: creation of a CWN-based character with the High Mage extension; choose an art; prepare/cast one accurately implemented WWN High Magic spell; expend/recover Effort; save state/reload via Evennia; use from a normal UNSA scenario. NPC Hermeticists should use the same system.
- Implement unit/integration tests for the High Mage rules, casting economy, saves, state persistence and compatibility with CWN/SWN. Expose help/UI and concise tabletop documentation, including the exact reference and reskin mapping.
- **Licensing:** use the compatible WWN SRD/open content and cite specific rule references; do not copy copyrighted Otherscape text, art or proprietary material into the repo.

## P1: COMPARE WWN AND SWN FACTIONS; ENHANCE, DON'T REPLACE
Review WWN **Factions and Major Projects** against the SWN faction mechanics that are already designated the baseline:
- compare attributes (**WWN Force/Wealth/Cunning, Magic rating**, SWN counterparts), assets, tags, faction turns, actions, goals, resource accounting, asset conflicts and movement;
- evaluate what WWN contributes for a post-disclosure world: **Magic rating/occult capacity**, fantasy-appropriate or psychic asset analogues, faction tags, and **Major Projects / Renown / opposition / difficulty / scope** for large player goals;
- propose a compatibility table: **adopt as additive mod / map existing SWN concept / defer / reject**, with clear reasons and no SWN schema-breaking replacements;
- for UNSA, the Zookeepers/UCCC, Orion sphere, Sirians, Panopticon, Noösphere, and local occult cults, outline how a faction's use/control of PSI alters strategy and political antagonisms;
- align optional mechanics with **LaclauGPT ideology/discourse network** layer and reputations, but defer the full strategy simulation until needed.
**Deliverable:** a written comparison and bounded implementation plan; implement only clearly approved, low-risk enhancements after the comparative review. This is secondary to P0.

## P2: WWN rule implementation backlog (inventory entire free rulebook, then prioritize)
Create a permanent source-linked WWN chapter/feature checklist with status `not assessed / candidate / planned / implemented / deferred / rejected`. Initial inventory (not automatically an implementation mandate):
1. Character Creation: High Mage **P0**; other partial Mage traditions, relevant Foci, progression and compatible skill options (selectively).
2. Magic and Arcane Traditions: spellcasting and spell preparation **P0**; High Mage Arts/Spells **P0**; Elementalist, Necromancer, Healer, Vowed, Thought Noble or other magic/psychic traditions **later / evaluate and reskin**, magic workings/rituals, enchanting, magic items and crafting.
3. Rules of the Game: review saves, combat, System Strain, exploration, hazards, chases and gear only to address missing fantasy/PSI use cases; **CWN takes precedence**.
4. Factions and Major Projects: **P1 comparison**; possibly Magic ratings, tags, occult assets, Renown, project scope/opposition and faction-project interactions.
5. Creatures of a Far Age / monsters: **adapt paranormal/NHI/construct encounters**, folklore and psychotronic anomalies, no fantasy race imports.
6. Setting/worldbuilding: use procedural tools for strange sites, haunted Helsinki, anomalies, occult networks, social conflict and off-world/noetic realms; do **not** import the Latter Earth setting.
7. Campaign / adventure generation: assess reusable investigative locations, cults, factions, mysteries and encounter procedures.
8. Equipment / treasures / magical items: occult implements, talismans, ritual circuits, psychotronics and psi-tech hybrids; only where needed.
9. Other classes, backgrounds, character options: evaluate case-by-case; **no wholesale class migration**, no permanent rules-chassis changes.
Add individual acceptance criteria, dependencies, source pointers and approximate priority per feature.

## P2: FULL LAW OF ONE COVERAGE AND CYBERPUNK RESKIN PROJECT
Study **all 106 Ra sessions** and topical index; build a traceable **concept → NoöPunk interpretation → faction/phenomenon → gameplay mechanic or lore → implementation status → source session** matrix. No assertion that it is finished merely from surveying a synopsis. Plan all concepts (some may stay lore-only rather than forced mechanics):
- One Infinite Creator, unity, free will, Logos / sub-Logos, mind/body/spirit complexes and evolution of consciousness;
- densities, cycles/harvest, reincarnation, higher self, wanderers and social memory complexes;
- service-to-others/service-to-self polarization and contact/ethical dilemmas; avoid mechanical moral essentialism;
- Orion, Confederation, contact, UFOs, interdimensional phenomena, thought forms and disputed NHI encounters;
- energy centers, mind/body/spirit balancing, psychic powers, healing, ritual magic, intention and artifacts;
- archetypical mind, tarot, veiling, time/space versus space/time, planetary change and ontological effects.
Translate terms into accessible, coherent noetic science-fantasy equivalents. Preserve the fiction's real-world folklore and occult history as local manifestations and contested explanatory traditions, rather than turning every spirit into a stereotyped extraterrestrial. Cross-reference NoöPunk's pre-existing factions and Noösphere canon; avoid retconning established lore without explicit review.

## Otherscape design reference (use attached books)
Study the uploaded **Metro: Otherscape Core Book** and **Tokyo: Otherscape Setting Book** *for setting design*, especially the **Self / Mythos / Noise** interplay; mythological Sources; occult artifacts, esoterica and exposure; local supernatural institutions, traditions, power markets, gangs, security forces, corporations and social movements; Tokyo's **Bureau of Onmyō**, **Yōkai Database** and related setting integration.
- Use as comparative inspiration for **Helsinki: NoöPunk**: Finnish and global folklore, theosophy, Hermeticism, folklore-linked NHI, PSI organizations, occult trade, UNSA jurisdictions and human rights, conspiracy and ideological struggle.
- Reuse concepts at a high level; **do not copy Otherscape tags, rules, proprietary text, images or specific characters/settings**. Keep the Moebius/1970s psychedelic retrofuturist aesthetic and science-fantasy tone, not generic 1980s fantasy-cyberpunk visuals.

## Acceptance criteria / deliverables
- [ ] Source-backed WWN inventory with priorities and per-feature migration status.
- [ ] High Mage Hermetic PSI module fully implemented for a documented initial playable slice, with tests and Evennia persistence; comprehensive High Mage spell/arts coverage tracked.
- [ ] CWN unchanged; SWN psionics coexist and resource interactions are documented.
- [ ] WWN/SWN faction comparison written, with explicit additive proposal and defer list.
- [ ] Traceable Law of One session/category coverage matrix and a first reskin glossary; whole-corpus completion tracked honestly.
- [ ] Otherscape-to-NoöPunk worldbuilding principles written, without Tolkienisms.
- [ ] Updated bilingual lore/docs, with agents authoring English; existing Finnish authorial text preserved.
- [ ] Work split into follow-up implementation issues/PRs; CI/tests and documentation updated.

## References
- Uploaded: *Worlds Without Number Free PDF* (Kevin Crawford, 2021), especially **Character Creation, Magic and the Arcane Traditions, Factions and Major Projects**.
- WWN SRD: https://wwn.quadrifons.com/2.0%20The%20Rules%20of%20the%20Game.html
- WWN High Mage: https://wwn.quadrifons.com/1.0%20Character%20Creation/1.5.0%20Class%20List/1.5.10%20The%20High%20Mage.html
- WWN Factions: https://wwn.quadrifons.com/6.0%20Factions/Faction%20Statistics.html
- WWN Major Projects: https://wwn.quadrifons.com/7.0%20Major%20Projects/Major%20Projects%20and%20Existing%20Factions.html
- Uploaded: *Metro: Otherscape Core Book* (2024); *Tokyo: Otherscape Setting Book* (2024). These uploads may not be accessible to automation agents: ask them to use licensed user-supplied copies only where access is provided.
- Law of One whole-session corpus, categories and glossary: https://www.lawofone.info/ (copyright held by L/L Research; link and summarize, do not copy the full text into the repo).
- https://en.wikipedia.org/wiki/Interdimensional_UFO_hypothesis
- https://en.wikipedia.org/wiki/Extraterrestrial_UFO_hypothesis
- Wendt/Pasulka/Dolan; Vallée/Keel; Dean Radin: conceptual inspirations for fiction, not rules replacements.

