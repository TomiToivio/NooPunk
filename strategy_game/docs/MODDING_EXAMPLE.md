# Data-only tabletop modding example (#347)

The example in [`../data/mods/example_contact.json`](../data/mods/example_contact.json) is **fictional, noncanonical, offline and read-only content**. It shows how a new overseas research contact and a new event card can be added without changing Python domain classes. This is an authoring test, **not** a mod loader wired into the playable campaign.

Run from the repository root:

```sh
python -m unittest strategy_game.tests.test_tabletop_mod_example
```

The `nodes` array uses `BoardNode.from_dict` keys `identifier`, `label`, optional `kind`, `layer` and `tags`. The `cards` array uses `Card.from_dict` with `identifier`, `card_type` (e.g. `event`, `relationship`, `research`), `title`, optional `role` (`persistent_record` or `playable_move`), `text`, `tags`, `visibility`, `prerequisites`, `effects` and `provenance`. Give every node and card a unique, stable identifier. The demonstration uses `noopunk.mod_example.v1` only for its own fixture format, not as an official universal mod manifest.

**No executable rules are encoded:** empty `effects` and `prerequisites` are intentional. A new card does not imply a legal move, automatic contact, an accessible internet route, diplomatic allegiance, a dice check, or a result. Foreign contacts are dormant until narrative decisions activate them. Do not put classified NHI cosmology in player-visible cards. The JSON is loaded with the Python standard library, and the existing `Board` and `Card` serializers validate the records.

For a new mod, copy this fixture under another filename, replace the fictional titles and IDs, and adapt the test's `load_example(path)` to that path. This demonstrates **data extensibility**; it does not yet support installing, discovering, activating or sandboxing third-party mod packages, nor does it integrate mod records into one authoritative saved campaign state. Those remain separate tasks in #347.
