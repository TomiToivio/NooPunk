"""Lossless #232 rulebook segmentation: never drop, edit or reorder canonical text."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/rulebook_segments/manifest.json"


class LosslessRulebookSplit(unittest.TestCase):
    def test_segments_reconstruct_current_canonical_rulebook_exactly(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(m["canonical"], "RULEBOOK.md")
        source = (ROOT / m["canonical"]).read_text(encoding="utf-8")
        assembled = []
        cursor = 0
        for entry in m["segments"]:
            p = ROOT / entry["path"]
            self.assertTrue(p.is_file(), entry["path"])
            chunk = p.read_text(encoding="utf-8")
            self.assertEqual(entry["source_start"], cursor)
            self.assertEqual(entry["source_end"], cursor + len(chunk))
            self.assertEqual(entry["length"], len(chunk))
            assembled.append(chunk)
            cursor += len(chunk)
        self.assertEqual(cursor, len(source))
        self.assertEqual("".join(assembled), source)

    def test_segments_are_unique_and_stay_below_a_reviewable_size(self):
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        paths = [e["path"] for e in m["segments"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertGreaterEqual(len(paths), 7)
        self.assertLessEqual(max(e["length"] for e in m["segments"]), 100000)


if __name__ == "__main__":
    unittest.main()
