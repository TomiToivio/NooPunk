# Rules Constitution — module tiers

**Generated** by `python3 tools/rules_constitution_audit.py --markdown` from the
`module_tiers` block of `data/rules/rules_constitution.json`. Do not edit by hand.

**Issue:** https://github.com/TomiToivio/NooPunk/issues/1006 · **Sources and precedence:** `docs/rules/RULES_CONSTITUTION.md`

**Precedence:** `CWN` → `SWN` → `WWN` → `AWN`

**Minimum playable:** `CWN` + `SWN` — which in module terms is `cwn-core` + `swn-companion`. `tests/test_rules_constitution_modules.py` proves it by running the baseline with every
`noopunk-mod` module refused by an import hook.

| Tier | Modules |
| --- | ---: |
| `cwn-core` | 25 |
| `swn-companion` | 9 |
| `optional-source` | 2 |
| `noopunk-mod` | 20 |
| `infrastructure` | 4 |
| `experimental` | 5 |
| `legacy` | 3 |

## What each tier is

* **`cwn-core`** — Cities Without Number, as written. The baseline.
* **`swn-companion`** — Stars Without Number, imported whole-procedure. Psionics is the essential companion.
* **`optional-source`** — WWN / AWN, opt-in, one procedure, named in the module docstring.
* **`noopunk-mod`** — Original NoöPunk overlays: they read core state and add narrative state, never core resolution.
* **`infrastructure`** — Boundary, tag vocabulary and catalogues; not rules.
* **`experimental`** — Prototypes and labs that are NOT canonical and not part of play.
* **`legacy`** — Retired code kept for import compatibility. Never authoritative.

### `cwn-core`

* `src/rules/cwn_advancement.py`
* `src/rules/cwn_attack_modifiers.py`
* `src/rules/cwn_backgrounds.py`
* `src/rules/cwn_character.py`
* `src/rules/cwn_combat.py`
* `src/rules/cwn_combat_actions.py`
* `src/rules/cwn_core.py`
* `src/rules/cwn_drones.py`
* `src/rules/cwn_edges_foci.py`
* `src/rules/cwn_encumbrance.py`
* `src/rules/cwn_equipment.py`
* `src/rules/cwn_foci.py`
* `src/rules/cwn_gear_mods.py`
* `src/rules/cwn_hacking.py`
* `src/rules/cwn_healing.py`
* `src/rules/cwn_initiative.py`
* `src/rules/cwn_injury_procedure.py`
* `src/rules/cwn_major_injury.py`
* `src/rules/cwn_mission_time.py`
* `src/rules/cwn_program_catalogue.py`
* `src/rules/cwn_strain.py`
* `src/rules/cwn_trauma.py`
* `src/rules/cwn_vehicles.py`
* `src/rules/without_number.py`
* `src/rules/wn_core.py`

### `swn-companion`

* `src/rules/psionics.py`
* `src/rules/swn_faction_operations.py`
* `src/rules/swn_faction_turn.py`
* `src/rules/swn_progression.py`
* `src/rules/swn_psionics.py`
* `src/rules/swn_sector.py`
* `src/rules/swn_starships.py`
* `src/rules/swn_transhuman.py`
* `src/rules/swn_true_ai.py`

### `optional-source`

* `src/rules/awn_survival.py`
* `src/rules/wwn_projects.py`

### `noopunk-mod`

* `src/rules/anomaly_gate.py`
* `src/rules/aspects_prototype.py`
* `src/rules/cross_domain_state.py`
* `src/rules/field_agent.py`
* `src/rules/first_case_drill.py`
* `src/rules/investigation.py`
* `src/rules/investigation_evidence.py`
* `src/rules/mental_load.py`
* `src/rules/narrative_layer.py`
* `src/rules/narrative_moves.py`
* `src/rules/natural_psi.py`
* `src/rules/noopunk_crisis_contact.py`
* `src/rules/noopunk_extensions.py`
* `src/rules/noopunk_social_extensions.py`
* `src/rules/noopunk_tags.py`
* `src/rules/noospace_projection.py`
* `src/rules/party.py`
* `src/rules/physical_combat.py`
* `src/rules/social.py`
* `src/rules/ubiquitous_network.py`

### `infrastructure`

* `src/rules/equipment_catalog_index.py`
* `src/rules/mod_boundary.py`
* `src/rules/tag_fixtures.py`
* `src/rules/tags.py`

### `experimental`

* `src/rules/issue200_cross_system_converter.py`
* `src/rules/issue200_resolution_lab.py`
* `src/rules/issue200_scale_migration.py`
* `src/rules/issue217_resolution.py`
* `src/rules/kernel_prototype.py`

### `legacy`

* `src/rules/__init__.py`
* `src/rules/_retired.py`
* `src/rules/core.py`

**Maintenance rule.** A new module under `src/rules/` must be classified here in the
same commit. An unclassified module is a rule nobody has agreed to.

