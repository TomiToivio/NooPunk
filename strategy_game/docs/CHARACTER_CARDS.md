# Character cards

Reusable, data-driven game pieces for the digital tabletop: RPG characters, faction members,
encounters and investigations, and NHI worldbuilding. Cards are readable at a glance and
expandable in detail, and work in a UI or in text-first play.

**This layer is content and schema, not mechanics.** No statistic is derived, no roll is
compared, no effect is applied and no action is resolved. Gates A–D in
`docs/RULE_SYSTEM_RESEARCH.md` remain open, and `AGENTS.md` §4 reserves resolution, thresholds
and cadence to the author. `to_card()` leaves `prerequisites` and `effects` empty on purpose.

Code: `strategy_game/characters.py` · Content: `strategy_game/data/character_cards.json` ·
Tests: `strategy_game/tests/test_character_cards.py`

## The three families

| family | what it is | lifecycle |
| --- | --- | --- |
| `canonical` | A unique, persistent, authored character: faction leader, patron, councillor, rival or contact. Canonical identities carry across campaigns; decisions and consequences change their game *state*, never their identity. | Never instanced. Must cite `sources`. A canonical card is refused as an instantiation template. |
| `archetype` | A reusable, unnamed template: faction organizer, corporate security, netrunner, intelligence officer, researcher, activist, soldier, bureaucrat, journalist, commuter, shopkeeper, civilian witness. | Instanced with a name when it becomes important. The instance records its `template_id` and `GENERATED` provenance. |
| `nhi` | A game-facing exemplar of one of the four setting categories. | Not instanced. Must carry a classification derived from the codex. |

Ordinary civilians are gameplay-significant: a commuter, a shopkeeper or a witness is meaningful
to social and investigation play, not combat filler.

## Shared schema

Every card carries:

- `identifier` — a stable slug, unique in the roster.
- `family` — `canonical` / `archetype` / `nhi`.
- `display_name`, `role`, `summary` — the readable face.
- `faction_ids` — affiliations, validated against the known faction ids when supplied.
- `tags` — typed tags in issue #346's shared vocabulary: `belief`, `competence`, `equipment`,
  `relationship`, `asset`, `goal`. Occupation and social role live in `role`; the tag kinds are
  the ones #346 already declares, so there is no second tag scheme.
- `declared_actions` — optional labels from `investigation`, `influence`, `recruitment`,
  `espionage`, `field_operations`, `cyber`, `psi`, `combat`. Names only: nothing resolves one.
- `statuses`, `state` — declared progression fields (injury, loyalty, allegiance). Carried,
  never computed.
- `relationships` — ties to other cards by id and kind label.
- `visibility` — `public` / `private` / `concealed` (display policy; no rule reads it).
- `claim_status` — how well-established a claim is (below).
- `art_ref` — artwork kept outside the card, so placeholder art exists from day one.
- `provenance` — where the content came from, defaulting to `UNKNOWN` so an unrecorded origin
  stays visible instead of reading as fact.
- `sources`, `gm_notes` — citations for authored content, and an author-facing note.

## NHI classification: keep five things apart

An NHI card carries `category`, `species_ref`, `origin_hypotheses`, `allegiances` and a
certainty, and these are **never** collapsed into one another. A Grey, a mantid or an orb is not
a whole ontological category.

The classification is **derived from `data/codex.json`**, not asserted by a card author:

| card field | codex field |
| --- | --- |
| `category` | `ontology` — `biologic` / `construct` / `noetic` / `plasmoid` |
| `species_ref` | the codex entry `identifier` |
| `contested` | true when `alternative_ontologies` lists another reading |
| `claim_status` | `knowledge_status` |
| `reveal_stage` | `reveal_stage` |
| `origin_hypotheses` | `origin_claims`, quoted |
| `allegiances` | `faction_relationships`, quoted |

`validate(codex=...)` reports any card that contradicts its codex entry, references a species
that does not exist, or lists an unknown faction id. So a card cannot promote a rumour into
canon, settle a contested classification, or invent an origin claim. Classification may be
provisional, contested or redacted — and the exemplars include a contested one on purpose.

## Visibility and spoilers

Four readable states matter: public information, player-known facts, GM-only secrets, and
uncertain claims. Claim statuses are `canon`, `player_known`, `reported_claim`, `rumour`,
`source_mythology` and `gm_truth`. Uncertain claims stay readable *because* the setting is about
living with uncertainty; `gm_truth` is redacted.

- `render_front(card)` prints the compact face and never prints `gm_notes`.
- `render_detail(card, reveal_secrets=False)` withholds a redacted GM note behind
  `[redacted …]` until the caller asks; with `codex=…` it expands the referenced lore.
- Card metadata therefore cannot spoil a reveal by being read.

## Using cards

```python
from strategy_game.characters import load_character_cards, codex_entry_map, render_front, render_detail, to_card

roster = load_character_cards()
codex = codex_entry_map()
roster.validate(codex=codex)                       # () when every card agrees with canon

roster.get("sir_mars_eldrich")                    # the canonical exemplar
roster.filter(family="nhi", category="plasmoid")  # four categories are covered
roster.filter(faction="ulp", tag="competence")

netrunner = roster.instantiate("archetype_netrunner", display_name="Mika's Cousin")
netrunner.state["loyalty"] = "bought"             # declared, not computed

print(render_front(netrunner))
print(render_detail(netrunner, reveal_secrets=True))

card = to_card(netrunner)                         # the shared tabletop primitive
```

## Adding a card

1. Add an entry to `strategy_game/data/character_cards.json` (the loader checks `format` and
   `version`).
2. Give it a stable slug id, a family, and the fields that family requires: `sources` for
   canonical, `tags` for archetypes, a codex-derived classification for NHI.
3. For canon, cite where it comes from — an issue number, a repo document, a codex identifier.
   Canon is never invented in a card.
4. Run the tests:

```bash
python3 -m unittest discover -s strategy_game/tests -t . -q
```

## Deliberately absent

No attribute, skill value, target number, modifier, difficulty, threshold, cost, cadence, win
condition or effect application. `to_card()` produces a `persistent_record` character card with
empty mechanic slots, and the data file is checked for mechanic-looking keys. Turning any of
this into a rule is gated work, and the design record for it lives in
`docs/RULE_SYSTEM_RESEARCH.md`.
