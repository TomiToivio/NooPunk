# The faction card layer: the four card types as records (issue #346, criterion 4)

**PROPOSAL. Approves nothing.** `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**, and this
layer implements no rule. Issue #346's acceptance criterion 4 asks to *"Specify the four card types:
character, organization, research and government influence, **with minimal effects and
interactions**"*. Before this layer only the **character** family had a record; organization,
research and government cards had none. This layer supplies the missing records and is honest about
which half of the criterion it can meet.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/faction_cards.json` | the four type specifications, the control vocabulary, the six declared interactions, three generic example cards, the open questions |
| `strategy_game/faction_cards.py` | the record schema, the referential validator, the projection onto the shared `Card` primitive, and the player/GM split |
| `strategy_game/tests/test_faction_cards.py` | executable contracts (issue #271: code only) |
| `strategy_game/characters.py` + `data/character_cards.json` | the **character** card family (issue #356), *consumed* here, never duplicated |

## 1. Which half of criterion 4 this meets, and which half it does not

The criterion has two clauses, and they are different kinds of thing:

- **"Specify the four card types."** This is a schema. It is met: `CARD_TYPE_IDS` declares the four
  types, each has a `CardTypeSpec` naming what it represents, its tag scope, its control vocabulary
  and what it may not carry, and the shipped roster carries an example of each of the three types
  that had no layer before.
- **"…with minimal effects and interactions."** An *effect* is a mechanic. It is **not** met, and it
  must not be met by an agent: `AGENTS.md` §4 reserves resolution, thresholds and effects to the
  author. The issue's own "Illustrative mechanical function" column is therefore carried as
  **declared data with `enforced: false`** — legible to a reviewer, applied by nothing — and what each
  interaction *changes* is a `pending_author_decisions` entry with its reason.

**A container is not a rule.** The declared interaction chain is the container; the effect is the rule,
and the rule is the author's.

## 2. The four types, consumed not restated

| Type | Represents | Tag scope |
| --- | --- | --- |
| `character` | the founder, managers, field agents, patrons and significant NPCs | `character` |
| `organization` | NGOs, corporations, labs, media platforms, security teams, religious bodies, networks | `organization` |
| `research` | insights, discoveries, AGI/PSI/NHI knowledge, theories, breakthroughs, applied technologies | `research` |
| `government` | political influence or control in a city, region/state or other jurisdiction | `government` |

The **character** type is *consumed*: the card record and its schema live in `characters.py` (issue
#356, the `canonical` / `archetype` / `nhi` families). This layer declares the type so the four-type
vocabulary is complete and so a roster can reference a character card by id; it ships **no** character
card of its own, because a second character record would be the parallel system the criterion is not
asking for.

The scope vocabulary is issue #346's own `TAG_SCOPES` (from `faction_creation.py`) and the tag-kind
vocabulary is `characters.TAG_KINDS`; the validator refuses a tag attached at a scope its own
definition does not allow, so `REMOTE_VIEWING_TEAM` (a faction/organization asset) cannot be filed on
a `research` card as if it were a `REMOTE_VIEWER` competence.

## 3. Control is a named position, never ownership by default

The issue is explicit that a corporate patron's organization card *"remains distinguishable from
outright faction ownership"* and that starting government support is *"collaboration, not political
ownership"*. So a card carries a **named control state** — `owned`, `allied`, `infiltrated`,
`patron_controlled`, `cooperating`, `autonomous`, `contested` — transcribed from the issue's own
wording, and **no control state is assumed**: a card with no control state must record the reason it
has none, and a blank-and-silent field is refused by the validator. An empty field with a reason is a
question; an invented value is a rule.

## 4. Effects are declared, never enforced — and never carried

The issue's interaction chain is transcribed into `declared_interactions`, each with `enforced: false`
and a reason:

1. a character can lead a faction-controlled organization;
2. an organization produces research;
3. research improves advocacy or operations;
4. deployed agents use those capabilities to gain government influence;
5. government influence can in turn fund or restrict organizations and research;
6. a patron's organization card remains distinguishable from outright ownership.

A card never carries a resolved effect or a statistic: the record schema **refuses** the keys
(`effects`, `effect`, `prerequisites`, `stat`, `threshold`, `cost`, …) by name, and the projection
onto the shared `Card` primitive leaves `prerequisites` and `effects` empty on purpose — exactly as
`characters.to_card` does. What a declared link *does* is left open.

## 5. The one gap in the shared primitive, recorded not papered over

`strategy_game/tabletop/cards.py` declares members for `character`, `organization` and `research` but
**none** for `government`. Extending that enum would touch the board layer's file, which belongs to a
sibling unit (#347), so the gap is recorded as `UNPROJECTABLE` and a pending decision, and
`to_card()` refuses a government card **by name** rather than guessing a mapping (`CardType.PLACE`
would be a guess). A government card is a full record in this layer regardless; only its projection
onto the primitive is outstanding.

## 6. What the author still has to decide

- **What each declared interaction changes** — the effect, and any magnitude in it (`RULEBOOK.md`:
  no rules approved).
- **Whether the shared `Card` primitive gains a `government` member** (the board layer's call).
- **Whether a fifth card type is ever added** — the issue names four, and a card type is the author's.

Each is a `pending_author_decisions` entry with the reason it is open, and a contract asserts that no
entry is missing its reason.

**Cross-link:** the **strategic-consequence seam** to the RPG layer (#389) is declared next door in
`strategy_game/relationship_seam.py`, and documented in [`COUNCIL_LAYER.md`](COUNCIL_LAYER.md) §7. This
card layer resolves nothing either: it names types, holds records, and refuses the mechanics.
