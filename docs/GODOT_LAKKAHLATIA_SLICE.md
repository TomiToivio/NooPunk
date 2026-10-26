# NoöPunk Godot detective vertical slice (#631)

Godot 4 native prototype. Default entrypoint is `res://scenes/main.tscn` and the gameplay script is `src/godot/lakkahaltia_case.gd`.

## Run

Install Godot 4 and open the repository root containing `project.godot`, then **Run Project (F6/F5 depending on editor setup)**. From a terminal:

```sh
godot --path . --editor
godot --path . 
godot --headless --path . --script tests/godot/test_lakkahaltia.gd
```

The game is fully offline, with simple drawn geometry; no external asset packs or licensed proprietary graphics are included. Arrow keys or WASD move; **E** interacts within range; **J** reads case notes; **F5** saves and **F9** loads. Buttons on the right perform journal/save/load actions. Talk to the doctor, nurse and patient; examine the medical record and terminal; gather 3 clues and choose an ambiguous interpretation. Revisit a record after a failed 2d6 check.

## Design/rules status

This is the **first minimal playable room-and-clue slice**, not a full 10–15 minute production scenario. Locations are stylized blockout rectangles and navigation is not yet collision-aware. Dialogue and clue logic are currently embedded in GDScript; extracting validated resources, evidence categories, branching narrative trees, investigation journal UI and a 3D/isometric art pipeline is follow-up work.

The checks shown use the current Without Number **2d6 + ability modifier + skill** baseline, with the illustrative investigator in `rulebook/WITHOUT_NUMBER_BASELINE.md`: WIS 11 / Notice-0 and INT 14 / Program-1, target 8. This is not yet a general canonical character-creation/combat/hacking engine. Legacy `src/godot/core_rules.gd` remains untouched for compatibility; it implements obsolete d10 and **must not be used** for newly designed checks. See #564 and #615 for rules conversion.

For additional environments, use properly licensed Kenney, Quaternius, or Poly Haven assets; keep any commercial asset license manifest, and do not commit redistributable copies of purchased assets without permission. No assets have been downloaded for this slice.

## Next steps

1. Pin tested Godot version and run smoke test in CI.
2. Fix and refine 2D/3D world navigation, collision, UI layout and art.
3. Move NPCs and branching narrative data out of the main script.
4. Finish baseline game state, characters, quests, endings and test coverage; integrate source-licensed CWN/SWN/WWN/AWN procedures without copying proprietary book text.
5. Add credible incident evidence and competing explanations while maintaining grounded Nordics/Hermetic New Weird tone.

Known limitation: the runtime was not executable in the authoring environment; the Godot headless test is provided for validation by CI/local agents. This slice is **not yet verified as runnable** until that test passes.
