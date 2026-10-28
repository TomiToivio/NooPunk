"""Terminal scenes are endings, not dead ends (#709).

The investigation model's validate() requires every scene to hold a core clue, because a scene with no
exit is a trap. That rule is right for pass-through scenes and wrong for the last one: a confrontation,
an arrest, the final interview is where the case stops. Before this, an author had to fake a core clue
in the ending just to satisfy the lint, which is how a lint teaches people to lie to it.

Stdlib unittest only — NoöPunk's CI has no pytest.
"""

from __future__ import annotations

import unittest

from src.rules.investigation import Case, Clue, ClueKind, InvestigationError, Scene


def clue(cid: str, sid: str, kind: ClueKind = ClueKind.CORE) -> Clue:
    return Clue(
        id=cid, scene_id=sid, kind=kind, competency="Forensics", fact=f"fact {cid}",
    )


class TestTerminalScenes(unittest.TestCase):
    def test_a_terminal_scene_needs_no_core_clue(self):
        case = Case(
            id="lakkahaltia",
            scenes=(
                Scene(id="intake", title="Intake", clues=(clue("C1", "intake"),)),
                Scene(id="confrontation", title="Confrontation", clues=(), terminal=True),
            ),
        )
        case.validate()

    def test_a_non_terminal_scene_without_a_core_clue_is_still_a_dead_end(self):
        case = Case(
            id="bad",
            scenes=(
                Scene(id="intake", title="Intake", clues=(clue("C1", "intake"),)),
                Scene(id="corridor", title="Corridor", clues=()),
            ),
        )
        with self.assertRaises(InvestigationError) as ctx:
            case.validate()
        self.assertIn("corridor", str(ctx.exception))

    def test_a_terminal_scene_may_still_carry_optional_clues(self):
        case = Case(
            id="ok",
            scenes=(
                Scene(id="intake", title="Intake", clues=(clue("C1", "intake"),)),
                Scene(
                    id="confrontation", title="Confrontation", terminal=True,
                    clues=(clue("O1", "confrontation", ClueKind.OPTIONAL),),
                ),
            ),
        )
        case.validate()

    def test_the_obscure_only_rule_does_not_fire_on_an_empty_terminal_scene(self):
        # all(...) over an empty tuple is True, so the guard had to be scoped to non-empty core sets.
        case = Case(
            id="ok",
            scenes=(Scene(id="end", title="End", clues=(), terminal=True),),
        )
        case.validate()


if __name__ == "__main__":
    unittest.main()
