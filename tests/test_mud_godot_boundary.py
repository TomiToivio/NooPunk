"""#946: the MUD and the Godot game must not be able to break each other.

The boundary is only real if something checks it. Two engines, one repository, and a shared canon is
exactly the arrangement where a refactor in one silently changes the other.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUD = ROOT / "mud"
GODOT_DIRS = [ROOT / "godot", ROOT / "scenes"]


def _files(root: Path, suffixes: tuple[str, ...]):
    if not root.is_dir():
        return []
    return [p for p in root.rglob("*") if p.is_file() and p.suffix in suffixes]


class MudBoundaryTest(unittest.TestCase):
    def test_the_mud_directory_exists_and_is_documented(self):
        self.assertTrue(MUD.is_dir(), "mud/ must exist once the MUD is a project")
        self.assertTrue((MUD / "README.md").is_file(), "the boundary decision must be written down")

    def test_the_mud_contains_no_godot_artifacts(self):
        """A .gd or .tscn under mud/ means the two runtimes have started to merge."""
        strays = _files(MUD, (".gd", ".tscn", ".godot"))
        self.assertEqual([str(p.relative_to(ROOT)) for p in strays], [])

    def test_the_mud_does_not_reference_godot_resources(self):
        offenders = []
        for path in _files(MUD, (".py", ".md", ".json", ".txt")):
            # A boundary test may name the literal it forbids; only runtime code is scanned.
            if "tests" in path.relative_to(MUD).parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "res://" in text and path.name != "README.md":
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_godot_code_does_not_import_the_mud(self):
        offenders = []
        for directory in GODOT_DIRS:
            for path in _files(directory, (".gd",)):
                text = path.read_text(encoding="utf-8", errors="ignore")
                if "mud." in text or "mud/" in text:
                    offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_agent_guidance_states_the_boundary(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="ignore")
        self.assertIn("mud/", agents, "AGENTS.md must name the MUD boundary")
        self.assertIn("Godot", agents)

    def test_agent_guidance_states_mud_primacy(self):
        """#950: if primacy is not written where agents read, the next agent builds Godot features."""
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="ignore")
        self.assertIn("#950", agents, "AGENTS.md must record the #950 pivot")
        self.assertIn("primary", agents.lower())
        self.assertIn("secondary/legacy", agents.lower())

    def test_the_mud_readme_declares_phase_one_without_llm(self):
        readme = (MUD / "README.md").read_text(encoding="utf-8")
        self.assertIn("#950", readme)
        self.assertIn("no LLM", readme.replace("no** LLM", "no LLM"))


if __name__ == "__main__":
    unittest.main()
