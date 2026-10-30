# NoöPunk Step 2: UNSA rookie

Canonical tabletop rules: `noopunk/rulebook/RULEBOOK.md`  
Canonical playable Godot project: `noopunk/game/`

Open `noopunk/game/project.godot` in Godot 4.3+ or run `godot --path noopunk/game` from the repository root. At launch, the character sheet displays a fresh seven-attribute 3d6 roll, with signed modifiers. Choose **Reroll seven attributes** to reroll, then **Continue** to walk with WASD or arrow keys. Press **C** to reopen the sheet; its values persist while navigating the room. No character statistics affect movement yet.

Validation (from repository root):

```sh
godot --headless --path noopunk/game --script res://tests/attributes_smoke.gd
godot --headless --path noopunk/game --script res://tests/smoke.gd
godot --headless --path noopunk/game --quit-after 60
```

Manual smoke: launch, check seven signed values, reroll, continue, walk, press C to inspect retained values, reroll, continue and walk again. Range boundaries 3..18 and conversion tests are in `attributes_smoke.gd`.

This issue #835 implements one synchronized slice under permanent meta-issue #827. Further rules and any dice-based resolution are deliberately undecided. Legacy projects are untouched.
