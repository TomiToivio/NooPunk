# #950: CWN Deluxe reference audit and port roadmap

**Status:** audit *started*, not comprehensive coverage. This document identifies the actual reference sections and the first tested Python slice. The uploaded **Cities Without Number: Deluxe** PDF is a personal reference only; **do not commit the PDF or reproduce its full proprietary rules text**.

## Sources and traceability

CWN Deluxe by Kevin Crawford (2023), book pagination in the PDF's table of contents (PDF page offset +4):
- Character creation pp. 4–26: attributes p.5, skills pp.5–6, backgrounds pp.7–13, contacts p.14, edges p.16, foci p.18, starting gear pp.25–26.
- Rules pp.28–47: time, saving throws p.30, checks p.31, combat pp.32–39, injuries p.40, vehicle combat p.42, chases p.43, growth p.44, crafting p.46.
- Equipment pp.48–89: gear and armor, weapons, pharma, cyberware, decks, drones, vehicles.
- Hacking pp.90–105: cyberspace, actions, programs, security, networks.
- Mission creation pp.132–179; reactions and morale pp.180–195.
- **Deluxe supplemental material pp.222–255**: variant humanity, alienation, cheap cyber, magic/spellcasting, spirits, graced and magical gear. These are *optional*, not all baseline CWN requirements.

Check the linked web SRD separately for coverage: https://cwn.quadrifons.com/ . The **Deluxe book** includes additional material, so classify covered-in-SRD and deluxe-only independently. Avoid assuming coverage from function/file names.

## Migration matrix (initial; evidence-based)

| Source (CWN Deluxe book page) | Existing Godot | Python MUD | Automated evidence | Status |
|---|---|---|---|---|
| Attributes and modifiers (5) | Existing CWN implementations in `godot/core/`; exact parity not yet audited | `systems/cwn.py:attribute_modifier` | `test_cwn_character.py` | Partial |
| Skills, 2d6, untrained (5–6, 31) | Godot CWN implementations; comparison pending | `systems/cwn.py:skill_check`, `CmdCheck` | `test_cwn_character.py` | Partial |
| Saving targets (30) | Audit pending | `systems/cwn.py:save_target` | `test_cwn_character.py` | Partial |
| Character creation, backgrounds, edges, foci (4–26) | Audit pending | Initial seeded attributes only | none | Missing |
| Combat, damage, trauma and recovery (32–43) | Audit pending | No usable combat yet | none | Missing |
| Advancement and crafting (44–47) | Audit pending | Not yet ported | none | Missing |
| Equipment, cyberware, drones, vehicles (48–89) | Audit pending | Not yet ported | none | Missing |
| Hacking (90–105) | Audit pending | Not yet ported | none | Missing |
| Missions, NPC reactions and morale (132–195) | Audit pending | Original deterministic UNSA case prototype | `test_solo_campaign.py` | Partial original campaign; not CWN procedural parity |
| Deluxe optional magic, spirits, variants (222–255) | Audit pending | Not enabled | none | Deferred/optional |

## Priorities

1. Port source-backed CWN character creation and advancement, including edges/foci and starting gear, without copying licensed game text.
2. Implement combat and hacking resolution as pure Python functions with deterministic dice fixtures and Evennia command integration.
3. Expand UNSA playable investigation beyond the initial missing-researcher prologue: quests, dialogue trees, consequences and persistent NPCs.
4. Map all remaining CWN Deluxe source sections individually, explicitly marking optional and omitted features.
5. Every mechanical change must update this table, tests and `rulebook/WITHOUT_NUMBER_BASELINE.md` (or explain why the published tabletop rule is unchanged).

**Rulebook parity:** the tabletop baseline remains published CWN + selected SWN/WWN/AWN, with original NoöPunk modules isolated. `RULEBOOK.md` contains superseded historic text; do not regenerate its derived segments by editing a generated segment directly.
