# CWN progression and System Strain implementation (#564)

Godot implementation: `src/godot/cwn_progression.gd`. Tests: `tests/godot/test_cwn_progression.gd`.

This follows the canonical `rulebook/WITHOUT_NUMBER_BASELINE.md`, using CWN for standard operators. It implements fast/slow cumulative XP thresholds, skill upgrade costs and level gates, Focus and Edge award levels, base attack bonus, HP rerolls and guaranteed one-point improvement, System Strain capacity/recovery, and ordinary natural healing. The implementation does not invent custom PSI Effort, hacking, cyberware item catalogs or narrative trauma procedures.

**Strain API contract:** `current` is *temporary accumulated* strain only, and `permanent` is separate installed-cyberware strain. The aggregate may not exceed Constitution. `strain_after_rest` takes the aggregate currently tracked strain (inclusive of permanent) and will not reduce it below permanent. If tracking temporary strain separately, first sum temporary+permanent before calling it. No rounding of fractional permanent strain is performed.

Source references:
- https://cwn.quadrifons.com/rules-of-the-game/character-advancement/
- https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/system-strain/
- https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/natural-healing-first-aid-poisons/

Run: `godot --headless --path . --script tests/godot/test_cwn_progression.gd`

Not yet implemented: complete character generation, Foci/Edges catalogs, full CWN combat and trauma, detailed pharmaceuticals/cyberware activation, first-aid procedures, SWN PSI. Keep original SRD text and commercial assets out of the repo unless allowed by the source license.
