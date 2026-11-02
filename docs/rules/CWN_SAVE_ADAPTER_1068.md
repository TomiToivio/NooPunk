# #1068: CWN saving-throw interface adapter (partial implementation)

**Status:** narrow code-and-test improvement. **Not** a full CWN source audit.

The existing core procedure in `src/rules/wn_core.py` accepts *attribute modifiers* keyed by STR/DEX/CON/INT/WIS/CHA. A character sheet typically has *scores* (3–18) keyed by full names, abbreviations or lowercase names. Mixing these API contracts was identified in `docs/RULES_PARITY_1053.md`.

`src/rules/cwn_save_adapter.py` converts scores to modifiers through the existing canonical `wn_core.attribute_modifier` function, and delegates the saving-throw target computation to `wn_core.save_target`. It rejects missing required attribute pairs and conflicting aliases; neither rule changes the CWN formula. The new adapter also handles Luck without requiring attribute scores.

**At the table:** For Physical use the better Strength/Constitution modifier; for Evasion the better Dexterity/Intelligence modifier; for Mental the better Wisdom/Charisma modifier; for Luck none. Subtract character level and that modifier from 16 to obtain the target. Roll 1d20 against it, with natural 1 failing and natural 20 succeeding. Reference: [CWN SRD](https://cwn.quadrifons.com/), saving throws; [Free Edition PDF](https://tesera.ru/images/items/2301450/CWN_Free_Version_081123.pdf).

Test: `python -m pytest tests/test_cwn_save_adapter_1068.py -q`.

**Remaining:** migrate and test the existing Evennia/MUD wrapper entry points to delegate to this adapter; re-run `tools/rules_parity_probe.py --check`; verify other source procedures against the PDF and SRD, rule by rule. The canonical CWN formula and parameters were not modified in this change.
