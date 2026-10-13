"""Executable contract for the standalone strategy scaffold CLI."""
from __future__ import annotations

import contextlib
import importlib
import io
import json
import unittest

from strategy_game.core import WorldState
from strategy_game.view import board_view


class EntrypointTests(unittest.TestCase):
    def test_import_does_not_print(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            module = importlib.import_module("strategy_game.__main__")
            importlib.reload(module)
        self.assertEqual(output.getvalue(), "")

    def test_main_prints_empty_board_json(self) -> None:
        from strategy_game.__main__ import main

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertIsNone(main())
        self.assertEqual(json.loads(output.getvalue()), board_view(WorldState()))


if __name__ == "__main__":
    unittest.main()
