"""The mixed-genre example as a running artefact: one sheet, one kernel per run, four environments.

The base system (`src/rules/wn_core.py`) is the **default**; `--system legacy` keeps the transitional
`1d10` layer runnable beside it. Both are asserted, so neither can drift silently.

What is proven here, rather than claimed:

* the demo runs **offline** — an audit hook in the child refuses sockets and resolvers;
* it is **deterministic** — the same seed replays byte for byte, a different seed moves the dice;
* it uses **one kernel per run** — every check line's arithmetic is recomputed exactly;
* it uses **one sheet** — one sheet line, unchanged at the end;
* it covers **four environment types** — cyberpunk, crisis ruins, NHI outpost, noetic realm;
* it respects the **shared action clock** — never more than three AP in an exchange.

Code-only, per `AGENTS.md` and issue #271: the running artefact, not the prose.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mixed_genre_demo.py"

_NETWORK_BLOCKER = '''\
"""Refuse every outbound network call in the mixed-genre demo."""
import sys


def _deny(event, args):
    if event in {
        "socket.connect",
        "socket.getaddrinfo",
        "socket.gethostbyname",
        "urllib.Request",
        "http.client.connect",
    }:
        raise RuntimeError("network access attempted during the #615 demo: " + event)


sys.addaudithook(_deny)
'''

_WN_LINE = re.compile(
    r"check\s+(?P<attr>[A-Z]{3}) (?P<score>\d+)\((?P<mod>[+-]\d+)\) \+ (?P<skill>[A-Za-zö ]+?)"
    r" (?P<level>\d) \+ 2d6\((?P<dice>\d+,\d+)\) = (?P<total>\d+) vs DV (?P<dv>\d+)"
)
_LEGACY_LINE = re.compile(
    r"check\s+(?P<stat>[A-Z]{3}) (?P<stat_val>\d+) \+ (?P<skill>[A-Za-zö ]+?) (?P<skill_val>\d+)"
    r" \+ 1d10\((?P<die>\d+)\) = (?P<total>\d+) vs DV (?P<dv>\d+)"
)
_SCENES = ("SCENE 1", "SCENE 2", "SCENE 3", "SCENE 4")


class MixedGenreExampleTests(unittest.TestCase):
    _blocker: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls._blocker = tempfile.TemporaryDirectory()
        (Path(cls._blocker.name) / "sitecustomize.py").write_text(_NETWORK_BLOCKER, encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._blocker.cleanup()

    def _run(self, seed: int, *extra: str) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join((self._blocker.name, str(ROOT)))
        for key in list(env):
            if key.endswith(("_API_KEY", "_TOKEN", "_SECRET")):
                env.pop(key, None)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--seed", str(seed), *extra],
            cwd=str(ROOT), env=env, text=True, capture_output=True, timeout=120, check=False,
        )

    def test_the_demo_runs_offline_and_exits_cleanly(self) -> None:
        for system in ("wn", "legacy"):
            with self.subTest(system=system):
                done = self._run(615, "--system", system)
                self.assertEqual(done.returncode, 0, done.stderr[-2000:])
                self.assertIn("one grammar", done.stdout)

    def test_the_base_system_is_the_default(self) -> None:
        out = self._run(615).stdout
        self.assertIn("system wn", out)
        self.assertIn("kernel 2d6 + attribute modifier + skill level", out)
        self.assertNotIn("kernel 1d10", out)

    def test_the_same_seed_replays_byte_for_byte(self) -> None:
        for system in ("wn", "legacy"):
            with self.subTest(system=system):
                first = self._run(615, "--system", system)
                second = self._run(615, "--system", system)
                self.assertEqual(first.stdout, second.stdout)
                self.assertNotEqual(first.stdout, self._run(616, "--system", system).stdout,
                                    "the seed must reach the dice")

    def test_all_four_environment_types_appear(self) -> None:
        out = self._run(615).stdout
        for scene in _SCENES:
            self.assertIn(scene, out)
        for module_marker in ("CWN module", "AWN module", "SWN module", "WWN module"):
            self.assertIn(module_marker, out)

    def test_one_sheet_is_printed_and_unchanged_at_the_end(self) -> None:
        out = self._run(615).stdout
        self.assertEqual(out.count("sheet  {"), 1, "exactly one sheet is introduced")
        self.assertIn("sheet  unchanged:", out)

    def test_the_base_system_arithmetic_is_two_d6_plus_modifier_plus_level(self) -> None:
        out = self._run(615).stdout
        matches = list(_WN_LINE.finditer(out))
        self.assertGreaterEqual(len(matches), 3, "the demo must actually resolve checks")
        for match in matches:
            dice = sum(int(d) for d in match["dice"].split(","))
            total = dice + int(match["mod"]) + int(match["level"])
            self.assertEqual(total, int(match["total"]), f"arithmetic broke on: {match.group(0)}")
            self.assertTrue(-2 <= int(match["mod"]) <= 2, match.group(0))
            self.assertTrue(0 <= int(match["level"]) <= 4, match.group(0))

    def test_the_transitional_layer_still_resolves_on_its_own_kernel(self) -> None:
        out = self._run(615, "--system", "legacy").stdout
        matches = list(_LEGACY_LINE.finditer(out))
        self.assertGreaterEqual(len(matches), 3)
        for match in matches:
            total = int(match["stat_val"]) + int(match["skill_val"]) + int(match["die"])
            self.assertEqual(total, int(match["total"]), f"arithmetic broke on: {match.group(0)}")
            self.assertTrue(1 <= int(match["die"]) <= 10)
        self.assertIn("kernel 1d10", out)

    def test_the_action_clock_is_the_shared_three_ap_exchange(self) -> None:
        out = self._run(615).stdout
        self.assertIn("3 AP each", out)
        spends = [int(m) for m in re.findall(r"AP (\d+)\)", out)]
        self.assertTrue(all(spend <= 3 for spend in spends), spends)
        exchanges = re.search(r"(\d+) exchange\(s\)", out)
        if exchanges is None:
            self.fail("the transcript must report its exchange count")
        self.assertGreaterEqual(int(exchanges.group(1)), 1)

    def test_the_reach_gate_is_shown_refusing_a_route(self) -> None:
        """The canon pairing table is visible in the transcript, not merely imported."""
        out = self._run(615).stdout
        self.assertIn("safenet -> safenet-exposed: possible", out)
        self.assertIn("safenet -> private-linked: impossible", out)


if __name__ == "__main__":
    unittest.main()
