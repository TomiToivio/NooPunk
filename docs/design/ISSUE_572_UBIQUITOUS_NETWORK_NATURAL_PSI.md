# NoöPunk optional extension profile: omnimesh and natural PSI (#572, #564)

**Status:** executable *opt-in prototype*, not yet the approved canonical tabletop rules or a replacement for Fate/1d10. Implemented in `src/rules/noopunk_extensions.py`; run `python -m unittest tests.test_noopunk_extensions -v`. No internet, LLM, classes or character levels.

## Ubiquitous network, not ubiquitous reach

Hacking takes place on an **omnipresent constellation** of people, devices, robots, implants, local radios, infrastructure, servers, couriers and sometimes psychic or psychotronic channels. Connectivity is modeled as actual typed *edges*, not a single Matrix or an automatic worldwide internet. A path can mix wired, radio, mesh, BCI and physical courier hops. No technical route exists solely because two people or organizations share a social link. Disconnected targets stay disconnected until someone or something creates a real bridge. An air-gapped clinic console might be reached by a drone carrying an interface, but cannot be hacked through a fictional remote socket. The installed `strategy_game/cyber.py` still governs era-specific permissions and containment illegality.

Network action loop: discover node → establish concrete path → establish authorization/intrusion conditions → perform contested test in owning RPG resolver → record evidence, exposure and organizational consequences. A psychic message does **not** silently become an IP connection: an adapter or explicit event must translate it.

## Natural human PSI with SWN-inspired structure

Natural potential is human and **learnable through instruction/practice** rather than limited to a stock Psychic class, alien genetics, a virus or implant. Learn a discipline from untrained to trained rating 0, then up to 4 by explicit training. The provisional original discipline vocabulary is telepathy, perception, precognition, influence, psychokinesis, healing and shielding. Learned competence unlocks attempts, never guarantees success. Techniques and costs are authored for NoöPunk, not copied from a commercial SWN book.

An optional **Effort-like commitment ledger** tracks named sustained effects with capacity, used and available budget. Commitments can be serialized/restored and release after effects end or rest. **Numeric capacity, progression costs, action difficulties, trauma and refresh cadence are provisional** and require independent author review; these are not SWN's formulas. Actual contests use the existing 1d10 tabletop resolver or Fate crossover resolver, never an extra imported die.

Three kinds of apparent telepathy remain distinct: natural PSI, psychotronic instrument and BCI network exchange. Noösphere and cross-realm action require their separate permission/gateway model.

## Additional NoöPunk-native subsystems to implement separately

| Domain | Without Number gap | New explicit contract |
| --- | --- | --- |
| Social/noetic discourse | Institutions, ideology and collective beliefs are not combat HP | Claim → circulation → interpretation → alignment/contestation → institutional response |
| AGI/ASI containment | No native model of rogue model containment in degraded networks | Capability scope, sandbox boundary, physical ingress, escalation and audit trail |
| NHI contact/diplomacy | No generic SRD substitutes for NoöPunk's nonbinary contact factions | Signal/provenance, translation, negotiation, legitimacy and disclosure |
| Cybernetic cognition | Implant tolerance ≠ attention/cognitive bandwidth | Interface connection, consent, competing streams, sustained concentration |
| Biological/psychic/social crossings | No native simultaneous three-system ontology | Single-locus agency, gateway permission, cross-domain effect and witness evidence |
| Crisis communities | AWN assumes survival situations that are not universal before the Fall | Local service failure, supplies, solidarity, recovery and political legitimacy |

All new subsystems must follow permission → declared cost → layer-specific check when contested → observable outcome → save/replay. The list above is a backlog, not a claim of finished engines.

## Copyright boundary

SWN provides a **comparative design pattern** of discipline training and committed mental resources. No SWN power descriptions, class text, setting, tables, or other protected expression is imported. Consult `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`.
