"""The MUD / Godot boundary, asserted rather than promised (#946).

The issue's non-negotiable boundary is that the two games share canon and rules data and
share no runtime. That is a claim about imports, so it is a test about imports: the MUD
package may reach into the shared Python kernel and must never reach into Godot.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

MUD = Path(__file__).resolve().parents[1]
REPO = MUD.parent

#: Import roots that would mean the two games had been entangled.
FORBIDDEN = ("godot", "src.godot", "project.godot", "concordia")


def _modules() -> list[Path]:
    return [p for p in MUD.rglob("*.py") if "__pycache__" not in p.parts
            and "server/conf" not in p.as_posix().replace("\\", "/")]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


class BoundaryTests(unittest.TestCase):
    def test_the_mud_never_imports_the_godot_game(self) -> None:
        offenders = {
            str(path.relative_to(REPO)): sorted(
                name for name in _imports(path)
                if any(token in name for token in FORBIDDEN)
            )
            for path in _modules()
        }
        offenders = {path: hits for path, hits in offenders.items() if hits}
        self.assertEqual(offenders, {}, "the MUD reached into the Godot game")

    def test_the_shared_kernel_is_reached_by_pathnot_by_copy(self) -> None:
        adapter = MUD / "world" / "cwn.py"
        text = adapter.read_text(encoding="utf-8")
        self.assertIn("SHARED_RULES", text)
        self.assertIn("from rules.wn_core import", text)
        # The one formula the MUD must not own.
        self.assertNotIn("2d6", text)
        for token in ("randint", "random."):
            self.assertNotIn(token, text, "the MUD rolled its own dice")

    def test_the_game_dir_is_not_the_godot_project(self) -> None:
        self.assertTrue((MUD / "server" / "conf" / "settings.py").exists())
        self.assertFalse((MUD / "project.godot").exists())
        self.assertFalse((MUD / "scenes").exists())


if __name__ == "__main__":
    unittest.main()
