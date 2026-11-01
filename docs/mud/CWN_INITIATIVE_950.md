# CWN initiative: NoöPunk MUD parity note (#950)

Source: [CWN SRD: Combat Initiative](https://cwn.quadrifons.com/rules-of-the-game/combat/combat-initiative/) and [Combat Sequence](https://cwn.quadrifons.com/rules-of-the-game/combat/combat-sequence).

The tabletop procedure and the MUD's `nopunk_mud.cwn.initiative` agree:

1. Normally **each side**, rather than each participant, rolls **1d8 + that side's best Dexterity modifier**. NPCs generally add zero.
2. Sides act in descending order. **A PC side wins an equal-score tie**. Members of a side choose their order within that side's turn.
3. **The initiative order is retained between rounds**. Do not roll again after each round.
4. If the GM determines that one or more groups were completely unaware, the non-surprised sides get **one free round** before normal initiative. Vigilant groups cannot be surprised.
5. Optional individual initiative uses the same 1d8 + Dexterity procedure for each character, and PCs win ties.
6. An applicable automatic-initiative power takes precedence; multiple such actors roll normally to determine relative order.

## Engine behavior and limits

`initiative_order` accepts explicit rolls and one entry per side (or combatant for the optional variant). `surprise_round` returns the eligible actors for the free round. Calls are deterministic and validate d8 boundaries, duplicate names, and unknown surprised groups. Exact ties between two PC sides or two NPC sides retain input order; the SRD does not specify a further tie-break. These functions **do not yet drive an Evennia encounter loop**, determine whether surprise actually applies, select a side's best Dexterity, implement morale, or enforce automatic-initiative powers. Those require authoritative character/encounter state and additional tests.

This adds no NoöPunk-specific tabletop rule. It creates a tested Python implementation of the existing CWN procedure, not a new dice mechanic. Do not mark the full combat or encounter coverage row as implemented based on this helper alone.
