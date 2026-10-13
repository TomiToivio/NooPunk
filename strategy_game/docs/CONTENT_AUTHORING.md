# Content authoring — the modding schema (issue #347, item 9)

**What this is.** The authoring contract for data-driven content: what a modder (or an agent) may add
by editing data, which module validates it, and what every addition must not do. It is enforced by
`strategy_game/tests/test_content_authoring.py`, not merely described here.

## The rule

Content is **data**. A new card, node, event seed or deck entry is an edit to a JSON file plus the
validator that already owns that kind — never a new mechanic, never a new rule, never canon. If an
addition would need a number that changes play, it is not content: it is a rule, and rules are the
author's (`strategy_game/RULEBOOK.md` still says NO RULES APPROVED).

## The ten example kinds, and where each lives

`strategy_game/content_schema.py` declares the registry; `kind_examples()` counts what ships.

| Kind | Data file | Records | Validated by |
| --- | --- | --- | --- |
| character | `data/character_cards.json` | `entries` | `characters.load_character_cards()` |
| faction | `data/global_factions.json` | `factions` | — (data only) |
| organization | `data/faction_cards.json` | `cards`, `card_type == "organization"` | `faction_cards.load_faction_cards()` |
| place | `data/ukweli_local.json` | `locations` | `local_slice` |
| research | `data/faction_cards.json` | `cards`, `card_type == "research"` | `faction_cards.load_faction_cards()` |
| event | `data/global_factions.json` | `event_card_seeds` | — (data only; seeds may be bare strings) |
| mission | `data/council.json` | `worked_example.missions` | `council.load_council()` |
| relationship | `data/ukweli_local.json` | `relationships` | — (data only) |
| ideology / signifier | `data/global_factions.json` | `factions[].core_signifiers` | — (data only) |
| tarot (placeholder) | `data/tarot_placeholder.json` | `cards` | `tabletop.tarot.tarot_deck()` |

## Adding a card

1. Copy the shape of an **existing** record of the same kind; do not invent fields.
2. Give it a new `id` (or `identifier` — follow the file's own choice) and a distinguishable name.
3. Keep tags typed: the only tag vocabulary is `faction_creation.json`'s six kinds.
4. Save and validate: `python3 -m unittest strategy_game.tests.test_content_authoring`.

## Adding a node

A place is a record in `ukweli_local.json` (`locations`) or a geography record in
`ukweli_geography.json`; a new **foreign** node is the same shape with a new `id`. The authoring test
performs exactly this addition in a temporary copy and loads it through `local_geography`, so the
claim is proven, not asserted.

## What the test guarantees

- **Every kind has an example.** `missing_kinds()` must be empty — today the counts are character 17,
  faction 7, organization 1, place 8, research 1, event 11, mission 4, relationship 2, signifier 16,
  tarot 3.
- **A new card and a new foreign node load from data alone**, through the modules that own those kinds.
- **Shipped data is not touched by the test**: file digests are compared before and after.
- **The registry holds no mechanic**: it is scanned for mechanic vocabulary, with its own token list
  excluded from the scan.

## What is deliberately absent

No numeric effect, no cost, no threshold and no interaction is defined anywhere in the registry, and
`faction_cards.py` sets `EFFECTS_ENFORCED = False` with `declared_interaction_effects` recorded as a
pending author decision. Content may *declare* relationships between cards; it may not price them.
