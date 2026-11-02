# Issue #1044 — WWN High Mage as the NoöPunk hermetic PSI practitioner

P0 of the issue, shipped as a rules module. P1 (WWN/SWN faction comparison) and P2 (the full WWN and
Law of One inventories) are written as documents, not as code — the issue orders them that way.

## Source and licence

All numbers come from the **Worlds Without Number SRD**, which this repository has already verified as
CC0 (`data/sources/game_system_rights.json`), so implementing the tables is permitted. No SRD prose is
copied: the module states the arithmetic and paraphrases each Art in one line. The SRD text was read
from the published SRD (classes, arcane traditions, spells), and every table below is checked against
it in `tests/test_wwn_high_mage.py`.

## What is implemented

`src/rules/wwn_high_mage.py` + `tests/test_wwn_high_mage.py` (27 cases).

| WWN rule | Implementation |
| --- | --- |
| Full High Mage progression | `HIGH_MAGE_TABLE` — max spell level, castings/day, prepared slots, arts per level |
| Partial High Mage progression | `PARTIAL_HIGH_MAGE_TABLE` — its own table, **not** a halved full mage |
| Effort | `effort_max()` = 1 + Magic skill + better of Int/Cha, minimum 1; partial −1, minimum 1 |
| Separate Effort pools | `POOL = "high_mage"`; nothing can spend an SWN psychic's pool (`rules.swn_psionics`) here |
| Arts: commit / reclaim | `commit()`, `release()`, `Duration.DURATION`, `end_turn()`, `rest()` |
| Turn- and day-bound Effort | Turn Effort returns at end of Turn and cannot be reclaimed early; day Effort needs a comfortable rest |
| Arts with a usage cap | `Art.once_per` (`round` / `turn` / `day`) enforced in `commit()` |
| Learning a spell | `learn()` — only spells at or below the level's maximum, once each |
| Preparation | `prepare()` — one hour after a night's rest, never more than the prepared slots |
| Casting economy | `cast()` — prepared only, no armour/shield, no damage in the round, daily limit, same spell reusable |
| Persistence | `snapshot()` / `to_json()` / `.from_json()` with a schema version |

Reskin (the issue's "magick is psionics" premise, applied to naming only):

| WWN term | NoöPunk term | Mechanically |
| --- | --- | --- |
| High Mage | hermetic practitioner / ritual PSI operator | identical |
| spell | ritual working | identical |
| Art | trained noetic reflex | identical |
| Effort | committed attention | identical |
| Magic skill | Magic skill (unchanged) | identical |

The in-world disagreement — factions arguing whether they practise magic or psi — is a fiction layer.
The rules never take a side; `POOL` is the only place the distinction is mechanically visible, and it
exists to keep two resource pools apart, not to rank them.

## Coverage matrix: spells

The SRD's High Magic corpus is **86 spells** (21 level 1, 20 level 2, 18 level 3, 13 level 4,
11 level 5). Status:

| Batch | Status | Note |
| --- | --- | --- |
| Casting/preparation rules that govern all spells | **implemented** | the economy above |
| Spell identity and level | **implemented** | `Spell(identifier, name, level)` |
| Individual spell effects | **not implemented — deliberate** | effects are content data. Writing 86 effect entries as Python would put a rule catalogue in the rule module and duplicate what the table reads at play time. The next increment is a data file plus an effect-resolver interface, one batch per level, with the coverage matrix below kept in sync. |

Until that data file exists, a spell may be *known and prepared* but has no automated effect: the GM
resolves it. That is honest, not silent — the module never pretends an effect exists.

## Coverage matrix: arts

All **15** SRD High Mage Arts are present in `ARTS` with duration, paraphrase and usage cap, and
`test_every_srd_art_is_present_and_typed` fails if one disappears. What is *not* modelled is each
Art's special resolution: Counter Magic's opposed check, Inexorable Effect's forced re-roll and
Swift Casting's action-economy change are recorded as `note` + `once_per` and resolved by the caller.
That boundary is deliberate: those are scene-level resolutions that belong with combat/turn code, and
duplicating them here would create a second action economy.

## Crosswalk with SWN psionics (issue requirement)

| question | answer in this implementation |
| --- | --- |
| shared pool? | **no** — `POOL = "high_mage"`; SWN psychic Effort is `rules.swn_psionics.Psychic`, a different object |
| double power? | no — a CWN character may hold both packages, but no ability reads the other's pool |
| System Strain? | Psychic Conversion Art spends a casting slot to remove System Strain; strain itself is CWN's (`cwn_strain`) |
| armour/BCI interaction | High Magic is blocked by armour and shields, as WWN says; cyberware rules stay CWN's and are untouched |
| occult artifacts | not modelled here; equipment-side concern |

## Not done, and why

- **No CWN change**: no skill, save, hit die or advancement rule is touched. The package is additive.
- **No UI/help command yet.** The slice a player can run today is via the rules API and tests. The
  in-game surface (`practise`, `prepare`, `cast`, `arts`) needs an authored scene to be useful and
  belongs with the #1042 command increment.
- **No spell effect automation** (see matrix).
- **P1 comparison** and **P2 inventories** are separate documents so the code stays reviewable.

## Follow-up issues this implies

1. High Magic spell data file + effect-resolver interface, batched by level, with the matrix updated.
2. In-game command surface for the practitioner package, gated by what the character has learned.
3. WWN/SWN faction comparison (P1) — separate issue; touches `swn_faction_turn` and `wwn_projects`.
4. Law of One concept matrix (P2) — separate issue; lore, not rules.
