# SWN faction assets — the paper sheet

The faction turn is a strategic game played between sessions: a few dice, one sheet per faction, and a map of
worlds. This page is the pencil-and-paper procedure for the **asset catalogue** — buying, fielding and
fighting with assets — and it matches `data/rules/swn_faction_assets.json` row for row.

Source: *Stars Without Number: Revised Edition — Deluxe Edition*, pp.211–223. The numbers below are the
book's; its ability descriptions are not reproduced, so read the asset's own entry before you use it.

## What a faction tracks

| box | what goes in it |
|---|---|
| FacCreds | the faction's money; assets are bought with it |
| Cunning / Force / Wealth | the three ratings. Every attack adds one of them |
| Hit points | the faction's own pool; destroying a Base of Influence takes them down |
| Assets | one line per asset: name, HP, world, level |
| Homeworld | where assets may be bought without a Base of Influence elsewhere |
| Goal, tag | one goal at a time, usually one tag |

## Buying an asset (one per turn)

1. **Pick the asset** from your category's table at its level or below. Its *Cost* is in FacCreds.
2. **Check the world.** You need a Base of Influence on that world, or it is your homeworld, and the world's
   tech level must be at least the asset's *TL*.
3. **Pay the cost** and write the asset down with its printed HP.
4. **It cannot act yet.** A bought asset can neither attack, defend, nor use its special benefit until the
   beginning of your next turn.

The Base of Influence is the exception: it is bought with the **Expand Influence** action, costs as much as
its own maximum hit points, and does not count against your maximum number of assets.

## Attacking (one action per turn, any number of assets)

1. Choose one of your assets and one known enemy asset **on the same world**. A stealthed asset cannot be
   targeted until it is discovered.
2. You roll **1d10 + your rating named in the attack line** (a military unit adds Force; a cyberninja adds
   Cunning).
3. The defender rolls **1d10 + the rating named after "vs."** on your attack line — that is not always the
   same attribute.
4. **Higher total wins.** On a win, roll the attack line's damage die and deduct it from the defender's HP.
   **On a tie, both succeed:** your damage lands *and* the defender's counterattack lands.
5. If the defender survives and its Counter line has a die, it returns that damage. If the Counter line says
   `None`, a failed attack costs you nothing.
6. An asset attacks **once per turn**. A defender may defend as many times as it is attacked, as long as it
   survives.

## Worked example

UNSA has Cunning 3, Force 2, Wealth 1. A Smugglers asset (4 HP, Cunning 1) attacks a rival's False Front
(2 HP, Cunning 1).

* Smugglers' line is `Cunning vs. Wealth, 1d4 damage`. UNSA rolls 1d10 + 3; the rival rolls 1d10 + its
  Wealth.
* UNSA rolls 8 → 11. The rival rolls 4 + 1 → 5. The attack lands: 1d4 comes up 4, the False Front is
  destroyed.
* False Front's Counter line is `None`, so nothing comes back.

Now the same Smugglers against a Party Machine (10 HP, `Cunning vs. Cunning, 2d6 damage`, counter `1d6`):
both sides add Cunning, so the rating cancels out and the dice decide it — and if it is a tie, the Smugglers
take 1d6 on top of landing their own hit.

## The letters in the Note column

`A`, `S`, `P` are the book's own markers (access, stealth, planetary permission). They are recorded in the
catalogue so you can look up what each asset's entry says; this page does not interpret them, and neither
does the Python code — a marker the rules text explains must not be guessed at by a table.

## What the code does and does not do

`src/rules/swn_faction_assets.py` implements the catalogue, the attack exchange above (dice, ratings, tie
rule, counterattack) and the purchase rules (catalogue cost, one per turn, Base of Influence refused). It
does **not** implement the roughly sixty individual special abilities: each is a rule that changes what an
action is allowed to be, and a generic placeholder would be worse than leaving it to the GM with the book
open.
