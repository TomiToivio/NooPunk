# Character cards MVP (issue #356)

Cards live in `data/world/character_cards.json` (schema version 1). Three families share a light data contract:

* `canonical`: one stable identity, e.g. Sir Mars Eldrich, never spawned from a template.
* `archetype`: reusable unnamed faction/civilian templates; spawned instances have independent mutable state.
* `nhi`: generic samples from the four **ontologies** (Biologics, Constructs, Noetics, Plasmoids). Ontology, species, origin hypotheses, certainty and faction allegiance are separate fields. All example origins are hypotheses, not authoritative in-world revelations.

Use existing character attributes/TAGs and strategic action names. Stats are illustrative card values, **not new dice formulas**. No tactical view is assumed. The `public` section contains facts players may see. `gm_only` and NHI origin hypotheses are hidden unless `--gm` is explicitly requested. The text front is usable without artwork.

```bash
python scripts/character_cards.py --validate
python scripts/character_cards.py --type nhi
python scripts/character_cards.py --id leader.sir_mars_eldrich
python scripts/character_cards.py --id archetype.security --instantiate guard-001 --name Arja
python -m unittest discover -s tests -p test_character_cards.py
```

Actions are reusable references for faction missions or RPG scenes; instantiation has no automatic dice roll. A newly instantiated security contractor can be assigned to a faction operation by storing its `instance_id` in an encounter/mission state. Do not reveal `--gm` output to players.

This first iteration supplies data, validation, CLI filter/search, safe public/GM text views and template instantiation. A graphical rendering, persisted missions and player-facing UI remain future work.
