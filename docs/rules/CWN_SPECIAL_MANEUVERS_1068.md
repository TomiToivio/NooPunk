# CWN special combat maneuvers: tabletop and Python parity (#1068)

**Canonical source:** [CWN SRD, Special Combat Maneuvers](https://cwn.quadrifons.com/rules-of-the-game/combat/special-combat-maneuvers/).
This is a tabletop-ready paraphrase and code mapping; it adds **no NoöPunk Mod** and changes no CWN core rule.

| Maneuver | Tabletop procedure | Python implementation |
| --- | --- | --- |
| Shove | First hit with a melee attack without damage, then opposed Strength/Exert or Strength/Punch. The attacker must win; choose to push up to 3m or knock prone. | `shove` |
| Grapple | Hit with an unarmed melee attack while both hands are free; deal no immediate attack damage. Win opposed Strength/Punch to grapple. Victim and attacker cannot move or use other than unarmed/body-mounted weapons; victim automatically takes assailant's unarmed hit damage at end of each round. | `start_grapple`, `GrappleState` |
| Escape | Victim spends Main Action; win opposed Strength/Punch against **every** assailant if more than one. | `escape_grapple` |
| Drag / throw | Grappler spends Main Action and wins opposed Strength/Punch; move together up to 3m or throw victim 2m and knock prone. A tie or loss releases the target. | `move_grappled_target` |
| Size | Apply -2 to skill checks against substantially larger humanoids; -4 to barely wrestlable shapes/quadrupeds. | `size_check_modifier` |
| Two weapons | Both relevant weapon skills at rank 1+. Choose one weapon per attack, -1 to hit, +2 hit damage only when target is within both weapons' ranges; not to Shock. | `dual_wield` |
| Ranged execution | Only an entirely unsuspecting target. One uninterrupted minute of preparation, then Dexterity/Shoot vs 6 (within 2m), 8 (normal range) or 10 (long range); successful check ignores AC. | `execution_ranged_difficulty` |
| Melee execution | One uninterrupted minute near unsuspecting target, then an automatic melee hit in reach. | `execution_melee_auto_hit` |
| Execution result | Successful execution hit forces Physical save penalized by attacker's combat skill; failure yields Mortal Wound at 0 HP or unconsciousness for nonlethal weapons. Save success still takes ordinary damage. Every execution hit is a Traumatic Hit. | `execution_hit` |

Use the **existing** CWN melee-attack, opposed skill-roll, Physical save, damage/Trauma, and Main Action resolution functions for the dice and accounting; do **not** duplicate their formulas inside this module. In the pure helper functions, rolled totals and hit/save outcomes are caller-supplied. This keeps the rules usable with pencil and dice and independent of Evennia/CLI/browser.

Evidence: `tests/test_cwn_special_maneuvers_1068.py` covers ties, hand prerequisites, multiple grapplers, large targets, dual wield damage versus Shock, all three execution difficulties and execution consequences. No deluxe-only text is claimed.

Remaining #1068 work: full source-verified audit of other chapters, adapting combat entry points, reconciling the legacy reader rulebook, and CI parity validation across *all* rules.
