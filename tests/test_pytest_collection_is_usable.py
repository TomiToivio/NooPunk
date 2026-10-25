"""A guard against the defect that made `pytest` unusable in this repository.

The defect
----------

The two test roots — `tests/` and `strategy_game/tests/` — are **not packages**, so pytest's default
"prepend" import mode imports each test module under its **bare basename**. Two modules named
`test_character_cards.py`, one in each root, therefore collide:

    ERROR tests/test_character_cards.py
    import file mismatch:
    imported module 'test_character_cards' has __file__ = '.../strategy_game/tests/...'
    HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
    !!! Interrupted: 1 error during collection !!!
    2466 tests collected, 1 error

Collection **aborts** on that one error, so a bare `pytest` from the repository root ran **none** of
the 2,466 tests it had already collected. CI was unaffected because it uses `unittest discover -s`,
which takes an explicit start directory — which is exactly why the breakage survived: the two
invocation styles disagreed and only the developer-facing one was broken.

The fix is `addopts = --import-mode=importlib` in `pytest.ini`, which keys modules by their full
path. This test pins both halves of it:

1. `pytest.ini` still carries the import mode (deleting it silently reintroduces the abort);
2. no basename appears in both roots (a new collision would still be *reported* rather than
   quietly tolerated, even though importlib mode now copes with it).

The second assertion is deliberately about hygiene rather than about breakage: with importlib mode
two same-named modules are legal, but they are still a sign that one of them should be renamed, and
a bare-basename invocation from any other runner will hit the original problem again.
"""
from __future__ import annotations

import configparser
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEST_ROOTS = ("tests", "strategy_game/tests")


def _basenames(root: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path in sorted((ROOT / root).glob("test_*.py")):
        found.setdefault(path.name, []).append(f"{root}/{path.name}")
    return found


class PytestCollectionTests(unittest.TestCase):
    def test_pytest_ini_keeps_importlib_mode(self) -> None:
        """Deleting the setting reintroduces the abort, so it is asserted, not assumed."""
        parser = configparser.ConfigParser()
        parser.read(ROOT / "pytest.ini", encoding="utf-8")
        addopts = parser.get("pytest", "addopts", fallback="")
        self.assertIn(
            "--import-mode=importlib",
            addopts,
            "pytest.ini must keep --import-mode=importlib: without it the two test roots are "
            "imported by bare basename and collection aborts on the first duplicate name, "
            "running none of the suite.",
        )

    def test_no_test_module_name_appears_in_both_roots(self) -> None:
        """A duplicate basename is a latent version of the same defect for other runners."""
        seen: dict[str, list[str]] = {}
        for root in TEST_ROOTS:
            for name, paths in _basenames(root).items():
                seen.setdefault(name, []).extend(paths)
        duplicates = {name: paths for name, paths in seen.items() if len(paths) > 1}
        self.assertEqual(
            duplicates,
            {},
            "the same test module name exists in both test roots; rename one so bare-basename "
            f"runners cannot collide: {duplicates}",
        )

    def test_both_test_roots_are_still_where_ci_expects_them(self) -> None:
        """CI runs `unittest discover -s tests` and `-s strategy_game/tests`; both must exist."""
        for root in TEST_ROOTS:
            with self.subTest(root=root):
                self.assertTrue((ROOT / root).is_dir(), f"{root} is missing")
                self.assertTrue(
                    list((ROOT / root).glob("test_*.py")),
                    f"{root} contains no test modules",
                )


if __name__ == "__main__":
    unittest.main()
