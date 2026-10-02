"""Guard: every test module must be runnable on its own.

Why this exists
---------------
`tests/test_issue51_text_game.py` imported `simulation` / `text_game` without putting
`src/` on `sys.path`, while every other test module in this repository did. The
consequence was subtle and CI never saw it:

* under `python -m unittest discover -s tests -p "test_*.py"` it passed, because an
  earlier-collected module had already inserted `src/` on the path;
* run on its own it failed with `ModuleNotFoundError: No module named 'simulation'`,
  and pytest could not even collect it.

So the suite was green only by an accident of collection order. A test file that
cannot be run alone is a defect even when the aggregate run is green: it breaks
bisecting and single-file debugging, and starts failing in the ordinary run the moment
anyone renames a file so it collects first.

What is checked
---------------
For every ``tests/test_*.py`` that imports a ``src/`` package at module scope, the file
must also put ``src/`` on ``sys.path`` before that import, derived from its own
location. Nothing else about the test's content is constrained.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"

#: Top-level packages that live in src/ and that tests import directly.
SRC_PACKAGES = ("simulation", "text_game", "rules", "concordia_runtime")

_IMPORT = re.compile(r"(?m)^\s*(?:from|import)\s+(" + "|".join(SRC_PACKAGES) + r")\b")


def _test_files() -> list[Path]:
    return sorted(TESTS.glob("test_*.py"))


def _imports_src(text: str) -> bool:
    return bool(_IMPORT.search(text))


class TestIsolationGuard(unittest.TestCase):
    def test_there_are_test_files_to_check(self) -> None:
        """A guard over an empty set would pass vacuously."""
        self.assertGreater(len(_test_files()), 10, "expected a populated test suite")

    def test_every_test_file_that_imports_src_sets_sys_path(self) -> None:
        offenders = [
            path.name
            for path in _test_files()
            if _imports_src(path.read_text(encoding="utf-8"))
            and "sys.path" not in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(
            offenders,
            [],
            "these test modules import a src/ package but never put src/ on "
            "sys.path, so they only pass when an earlier-collected module does it "
            f"first: {offenders}",
        )

    def test_the_path_insertion_targets_src_from_the_test_location(self) -> None:
        """`sys.path.insert(0, str(ROOT / "src"))` — not a cwd-relative guess."""
        for path in _test_files():
            text = path.read_text(encoding="utf-8")
            if not _imports_src(text) or "sys.path" not in text:
                continue
            with self.subTest(test=path.name):
                self.assertRegex(
                    text,
                    r'sys\.path\.insert\(\s*0\s*,\s*str\(\s*ROOT\s*/\s*"src"\s*\)',
                    "src/ must be derived from the test file's own location",
                )


class TestKnownOffenderIsFixed(unittest.TestCase):
    def test_the_text_game_test_sets_its_own_path(self) -> None:
        """The specific defect: green under discover, broken on its own."""
        text = (TESTS / "test_issue51_text_game.py").read_text(encoding="utf-8")
        self.assertIn("sys.path.insert", text)
        self.assertIn('"src"', text)


if __name__ == "__main__":
    unittest.main()
