"""Regression guard for issue #107: the unified Affect graph.

Two independent reasons this file never ran in CI, both fixed here:

1. it defined module-level ``test_*`` functions rather than ``TestCase`` classes, so
   ``unittest discover`` matched the filename and collected nothing -- "Ran 0 tests ...
   OK". It also had no ``__main__`` block, so running it directly did nothing.
2. it imported ``pytest`` and used ``pytest.raises``. CI's install step runs
   ``pip install -r requirements.txt``, which contains only the pinned Concordia
   dependency -- pytest is not installed, so the module would have raised ImportError the
   moment discovery tried to import it.

The repository documents the same trap for ``test_world_ideology.py`` in
``.github/workflows/python-scaffold.yml`` and gives that file its own runner step. This
guard instead becomes a ``unittest.TestCase`` so the existing discovery run both imports
and collects it, with no dependency beyond the standard library.

The graph semantics asserted here are unchanged from the original file: validation bounds,
unknown versus explicit-neutral, directionality and multiple labels, inheritance that
preserves ambivalence, personal override, and round-trip serialisation.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulation.affect import (  # noqa: E402
    AffectEdge,
    AffectGraph,
    inherit_faction_affects,
)


def edge(source, target, affect, score, domain):
    return AffectEdge(
        source=source,
        source_type="faction" if domain.startswith("faction_") else "character",
        target=target,
        target_type="concept",
        affect=affect,
        affect_score=score,
        domain=domain,
    )


class AffectGraphTests(unittest.TestCase):
    def test_validation_bounds(self) -> None:
        with self.assertRaises(ValueError):
            edge("a", "b", "Supports", 11, "motivation")
        with self.assertRaises(ValueError):
            edge("a", "b", "Supports", 10, "sentiment")

    def test_unknown_differs_from_explicit_neutral(self) -> None:
        graph = AffectGraph()
        self.assertEqual(graph.between("a", "b"), [])
        self.assertEqual(graph.effective_score("a", "b", "Knows"), 0)
        graph.add(edge("a", "b", "Knows", 0, "contact"))
        self.assertEqual(len(graph.between("a", "b", domain="contact")), 1)

    def test_multiple_labels_and_directionality(self) -> None:
        graph = AffectGraph()
        graph.add(edge("pc", "AGI", "Supports", 3, "motivation"))
        graph.add(edge("pc", "AGI", "Fears", -4, "motivation"))
        graph.add(edge("AGI", "pc", "Distrusts", -2, "reputation"))
        self.assertEqual({x.affect for x in graph.between("pc", "AGI")},
                         {"Supports", "Fears"})
        self.assertEqual([x.affect for x in graph.between("AGI", "pc")], ["Distrusts"])

    def test_inheritance_preserves_ambivalence_and_means_matching_labels(self) -> None:
        inherited = inherit_faction_affects(character_id="pc", faction_edges=[
            edge("a", "AGI", "Supports", 7, "faction_us"),
            edge("b", "AGI", "Supports", 5, "faction_us"),
            edge("b", "AGI", "Fears", -6, "faction_frontier")])
        by = {x.affect: x for x in inherited}
        self.assertEqual(by["Supports"].affect_score, 6)
        self.assertEqual(by["Fears"].affect_score, -6)
        self.assertEqual(by["Supports"].metadata["inherited_from"], ["a", "b"])

    def test_personal_override(self) -> None:
        personal = AffectEdge(source="pc", source_type="character", target="AGI",
                              target_type="concept", affect="Supports", affect_score=8,
                              domain="motivation", metadata={"origin": "personal"})
        inherited = inherit_faction_affects(
            character_id="pc",
            faction_edges=[edge("a", "AGI", "Supports", 7, "faction_us"),
                           edge("b", "AGI", "Fears", -6, "faction_frontier")],
            personal_edges=[personal])
        by = {x.affect: x for x in inherited}
        self.assertEqual(by["Supports"].affect_score, 8)
        self.assertEqual(by["Fears"].affect_score, -6)

    def test_round_trip(self) -> None:
        graph = AffectGraph([edge("pc", "friend", "Trusts", 5, "contact")])
        self.assertEqual(AffectGraph.from_dict(graph.to_dict()).edges, graph.edges)


if __name__ == "__main__":
    unittest.main()
