# #950 — the CWN core is already here; the port is gap-closing, not a rewrite

**Status: audit record. No rule changes, no new mechanics.** It corrects a claim two other #950
documents make, because acting on that claim would mean re-implementing twenty working modules.

## 1. The claim that needed checking

Two documents landed on `main` for #950 say, in effect, that the Python CWN core is mostly absent:

* `docs/rules/MUD_CWN_COMPLIANCE.md` (hand-written) marks **skills/backgrounds, initiative/action
  economy/shock, injuries/healing, encumbrance/weapons/armour/gear mods/crafting/wages, cyberware,
  hacking, advancement, vehicles/drones/pharma** as `missing`, with the Python target column empty.
* `docs/rules/CWN_SRD_PAGE_AUDIT_950.md` (generated, 82 pages) counts **68 of 82** pages `missing`,
  and its Python column is empty for armour, weapons, hacking, injuries and most of the rest.

Both are careful documents. Both are measuring the wrong thing for a *migration* issue: they ask
"is this rule implemented in `mud/nopunk_mud/cwn_core.py`?" — a file written this week — rather than
"does a Python module already implement this rule?" The answer to the second question is different.

## 2. What the repository actually contains

`data/mud/cwn_compliance.json` records one row per linked-SRD system and names the module and test
that own it. `tools/cwn_compliance_audit.py --check` resolves every claim against the tree: each
named module must **import**, each named test file must **exist**, and a row may not claim
`implemented` without a **Python** test. Current result:

```
rows: 46
  implemented     30
  partial         7
  godot-only      6
  missing         1
  omitted-by-srd  2
OK: every named module imports and every named test file exists
```

The code that exists, and is exercised:

| Present and tested in `src/rules/` | What the two #950 documents called it |
| --- | --- |
| `cwn_combat.py`, `cwn_combat_actions.py`, `cwn_attack_modifiers.py`, `cwn_trauma.py` | initiative, action economy, shock, maneuvers — "missing" |
| `cwn_major_injury.py`, `cwn_healing.py`, `cwn_injury_procedure.py`, `cwn_strain.py` | injuries, stabilisation, healing, System Strain — "missing" |
| `cwn_encumbrance.py`, `cwn_equipment.py`, `cwn_gear_mods.py` | encumbrance, weapons, armour, gear mods, crafting — "missing" |
| `cwn_hacking.py`, `cwn_program_catalogue.py` | hacking: access, verbs/subjects, programs, demons — "missing" |
| `cwn_advancement.py`, `cwn_backgrounds.py`, `cwn_edges_foci.py`, `cwn_foci.py` | advancement, skills/backgrounds, edges, foci — "missing" |
| `cwn_vehicles.py`, `cwn_drones.py` | vehicles, drones — "missing" |

Twenty modules, twenty-four test files, and the suite that covers them:

```
python3 -m unittest discover -s tests -p "test_cwn_*.py"
Ran 441 tests ... OK
```

## 3. What is genuinely missing — the actual work queue

The same audit, read the other way. These are the only real gaps, in the order the solo campaign
needs them:

| Gap | Size | Note |
| --- | --- | --- |
| focus gear budget | small | character creation cannot be finished without it |
| mission time (scenes, rounds, mission clocks) | small | every MUD scene needs the clock; also quest timing |
| wages and bribes | small | prices before the first shopping scene |
| pharmaceuticals / street drugs | medium | effects + the catalogue Godot already has |
| cyberware mods and systems | medium | catalogue + effect procedures |
| cyberware alienation | medium | a whole subsystem implemented in GDScript, absent in Python |
| chases and pursuit | medium | the round structure is GDScript only |
| demon and watchdog catalogues | small | the opposition model exists; the data does not |
| skillplugs | small | **absent in both games** — the one true zero |

## 4. What this changes, and what it does not

**Changes:** the porting plan. Every "missing" system above becomes "wire the existing module to an
Evennia command and a test that runs headless", which is days of work rather than weeks. The MUD's
`mud/world/cwn.py` in the sibling scaffold already takes this approach for attributes, saves and
checks.

**Does not change:** the CWN lock, the SRD's own omissions (antagonists, optional rules — still not
claimed), the fact that Evennia runtime behaviour is unverified in the scaffold, and the phase-1
priority order. Nor does it license importing Godot code: the Python modules are the target, GDScript
is the reference.

## 5. Reproducing this record

```bash
python3 tools/cwn_compliance_audit.py --check                      # imports + test paths + claims
python3 tools/cwn_compliance_audit.py --markdown > docs/rules/MUD_CWN_COMPLIANCE.md
python3 -m unittest discover -s tests -p "test_cwn_*.py"           # 441 tests
```

`tools/cwn_compliance_audit.py` is a **documentation/data audit**, not a CI gate: it is not wired
into any workflow, and it asserts only relationships (a module imports, a test file exists), never
prose. The generated matrix is the document; the JSON is the source; neither may be edited by hand.
