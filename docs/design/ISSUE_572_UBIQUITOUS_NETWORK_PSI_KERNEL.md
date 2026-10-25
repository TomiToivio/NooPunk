# NoöPunk original subsystem kernel: first playable slice (#572 / #564)

**Status:** executable additive prototype, not a silent replacement for the legacy 1d10 or the approved Fate crossover. Runtime: `src/rules/noopunk_extensions.py`; offline tests: `tests/test_noopunk_extensions.py`.

## Ubiquitous hacking: cyberspace is a mesh of everything

Pre-crisis NoöPunk has ubiquitous computing, wearables, surveillance systems, vehicles, buildings, cyberware, agent devices and proxied physical objects. Any connected device may relay information, including through intermediate nodes, rather than requiring a single central Internet. Players discover and exploit *paths* across this mesh. Crisis-era fragmentation changes the links, not the abstract possibility of hacking.

**Procedure (no GM fiat route):** draw named nodes and bidirectional links; remove links broken by isolation or crisis; find an online route using deterministic shortest-path search; classify the intended action as BLOCKED, PERMITTED or CONTESTED. Authorization and actual skill resolution are separate. An air-gapped node can be approached physically. Social ties, psychic contact and institutional relations are not automatically machine links. Any contested intrusion then runs through the *owning RPG layer's existing resolver*: d10 in the legacy tabletop, Fate in the crossover. This prototype does not implement intrusion damage, persistence, or security escalation; those remain subsystem work.

## Learnable natural PSI: SWN-inspired resource economy, NoöPunk ontology

**Every human has the potential to learn PSI** through disciplined practice, regardless of species/subclass/implant or special origin. Five initial competence domains are perception, telepathy, psychokinesis, precognition and noetic defence. Training ranges from 0 (not learned) to 4 (mastered); spending a training advancement increases the skill by one, with exact character XP pricing deferred to the canonical advancement design.

A trained discipline may be attempted using one point of available **Effort**: a one-shot effect spends a point until rest, a maintained effect commits a point until explicitly released. The demonstrator uses capacity 2 at initialization; that number is **prototype calibration**, not a retroactive change to current rulebooks. Training and capacity persist across save/reload. The test never determines success solely from Effort; permission and difficulty still belong to the scene resolver. Natural PSI is not explained by an alien virus. **BCI communication and psychotronic assistance are distinct technological channels** and must not silently confer learned PSI.

The design takes abstract inspiration from the SWN psychic resource approach, but all text and code here is independently authored: no SWN spell text, class features, proprietary tables or setting are imported, consistent with `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`. WWN's CC0 SRD also permits examination of committed resources.

## New systems beyond the four books

- **Crisis pressure:** individual localities have independent *scarcity*, *trust* and *exposure*. Supply shocks raise scarcity; solidarity changes trust; encounters affect exposure. A national or global collapse is not presumed. This is an optional campaign-state tracker, not a second combat system.
- **NHI contact diplomacy:** *reciprocity* (mutual exchange) and *autonomy* (capacity to refuse outside control) are distinct variables. A helpful proposal may still demand unacceptable assimilation. Neither Confederacy nor Orion receives a fixed moral alignment.
- **Future integration seams:** Noösphere single-locus and gateway invariants, AGI containment, BCI permissions, psychotronic devices and faction turn remain separate subsystem contracts, not packed into a universal hacking or PSI skill.

## Tabletop example

Three nodes: investigator's BCI `A`, hospital entrance panel `B`, restricted medical database `C`. Links `A-B` and `B-C`; `C` is protected by the hospital. The path exists but an unauthorized investigator has a contested intrusion, not free access. Remove `B-C` in the network crisis and the remote attempt is blocked without a roll. A person with trained telepathy (1) and 2 Effort commits one to maintain a noetic impression; remaining available Effort becomes 1, and releasing the effect restores the committed point. This mental channel is not a substitute TCP/IP connection.

## Test and acceptance

Run `python -m unittest tests.test_noopunk_extensions -v` (also included in ordinary `tests/` CI discovery). Tests cover connected multihop pathfinding, protection and denial, offline access, stable deterministic route selection, a learnable human PSI discipline, sustained/spent Effort, save/reload, distinct contact dimensions and local crisis pressure. No network, LLM or third-party packages required.

**Not yet complete:** integration into scenario CLI and character schema, approved PSI XP and capacity curves, security escalation, hackable AI agents, cyberware interface resources, system-wide Noösphere transitions and paper character sheet. These require additional small migrations rather than an unaudited rewrite.
