"""Structure guard for the #191 Confederacy technology and sphere lore.

Issue #191 is a living tracker whose two hard rules are (1) **evidence discipline** — never
let a contested real-world claim be written as established fact or as Ra canon — and (2) the
`AGENTS.md` §4 reservation on numeric statistics and full subsystems. Those rules are easy to
state and easy to lose in a later edit, so this guard pins them structurally.

It asserts *structure and bound*, never wording: the sections may be rewritten freely as long
as they keep their evidence-class markers, their "not Ra" attribution, and their no-statistics
bound.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "rulebook" / "11_ONTOLOGY.md"
EQUIPMENT = ROOT / "rulebook" / "13_EQUIPMENT.md"
RULEBOOK = ROOT / "RULEBOOK.md"


def flat(path: Path) -> str:
    """Collapse wrapping AND strip markdown emphasis, for prose assertions.

    Emphasis markers matter: the section says "Ra **does not** describe Jackson's …", so a
    regex written against the plain words fails on the ``**``. Strip ``*``/``_``/backticks so
    assertions test the prose, not its formatting.
    """
    text = path.read_text(encoding="utf-8")
    text = text.replace("*", "").replace("`", "")
    text = re.sub(r"(?<=\w)_(?=\w)", "", text)
    return re.sub(r"\s+", " ", text)


class SphereEvidenceDisciplineTests(unittest.TestCase):
    """§10.8.1-10.8.2 must keep the POSS-I material labelled as contested."""

    def setUp(self) -> None:
        self.text = flat(ONTOLOGY)

    def test_sphere_sections_exist(self) -> None:
        self.assertRegex(self.text, r"###\s*10\.8\.1")
        self.assertRegex(self.text, r"###\s*10\.8\.2")

    def test_primary_sources_are_cited_by_id(self) -> None:
        for ident in ("2609.09461", "2609.05105"):
            self.assertIn(ident, self.text, f"missing primary-source id {ident}")

    def test_evidence_class_is_stated_not_hidden(self) -> None:
        """The whole point: a contested claim stays labelled contested."""
        self.assertRegex(self.text, r"contested",
                          "the POSS-I material must keep an explicit evidence class")
        self.assertRegex(self.text, r"model-dependent|model dependent",
                          "the modelling result must stay labelled model-dependent")

    def test_the_papers_are_not_overclaimed(self) -> None:
        """Pin the negative claim — no artificial object / craft / sphere / NHI."""
        self.assertRegex(
            self.text,
            r"No artificial object, no craft, no sphere, and no NHI is claimed",
            "the section must keep its explicit non-claim",
        )

    def test_ra_is_recorded_as_silent(self) -> None:
        """Ra must not be recruited to support the Jackson taxonomy or the transients."""
        self.assertRegex(self.text, r"does not describe Jackson'?s sphere",
                          "must keep the 'Ra is silent' note")

    def test_four_layer_taxonomy_is_present(self) -> None:
        for layer in ("Orbital Sentinels", "Atmospheric Wardens",
                      "Local Microcustodians", "Noetic relays"):
            self.assertIn(layer, self.text, f"missing sphere layer {layer}")


class MindBodySpiritMappingTests(unittest.TestCase):
    """§10.6.0 must keep the four-system architecture intact."""

    def test_mapping_section_exists(self) -> None:
        self.assertRegex(flat(ONTOLOGY), r"###\s*10\.6\.0")

    def test_mapping_does_not_delete_the_cybernetic_layer(self) -> None:
        text = flat(ONTOLOGY)
        self.assertRegex(text, r"Cybernetic.{0,80}no Ra counterpart|no Ra counterpart",
                         "the mapping must keep the 'Cybernetic has no Ra counterpart' caution")


class CrystalTransducerBoundTests(unittest.TestCase):
    """§12.4.4 must stay a descriptive list inside the reserved area."""

    def setUp(self) -> None:
        self.text = flat(EQUIPMENT)

    def test_section_exists(self) -> None:
        self.assertRegex(self.text, r"###\s*12\.4\.4")

    def test_operator_constraints_are_cited_from_ra(self) -> None:
        for anchor in ("29.30", "2.3", "57.6", "57.9", "29.31"):
            self.assertIn(anchor, self.text, f"missing Ra operator anchor {anchor}")

    def test_the_three_hard_constraints_survive(self) -> None:
        self.assertRegex(self.text, r"operator-gated", "must keep operator-gating")
        self.assertRegex(self.text, r"subject-scaled", "must keep subject-scaling")
        self.assertRegex(self.text, r"refused", "must keep the refusal constraint")

    def test_the_refusal_rationale_is_stated(self) -> None:
        self.assertRegex(self.text, r"free-will grounds|free will",
                         "the 29.31 refusal must stay explained as a free-will position")

    def test_no_numeric_statistics_creep_in(self) -> None:
        """Reject a stat block: a numeric column that is not a leading key column.

        Mirrors the #187 guard. A legitimate table may still lead with a numeric key, so only
        numeric *non-key* columns (the shape of a stat line) are offenders.
        """
        offenders: list[str] = []
        columns: dict[int, list[str]] = {}
        rows = 0
        header_seen = False

        def flush() -> None:
            nonlocal columns, rows, header_seen
            if rows >= 2:
                for idx, cells in columns.items():
                    if idx == 0:
                        continue
                    if len(cells) >= 2 and all(
                        c and re.fullmatch(r"[-−+]?\d+(?:[.,]\d+)?%?", c) for c in cells
                    ):
                        offenders.append(f"numeric column {idx}: {cells}")
            columns, rows, header_seen = {}, 0, False

        for line in EQUIPMENT.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s.startswith("|"):
                flush()
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) or not c for c in cells):
                continue
            if not header_seen:
                header_seen = True
                continue
            rows += 1
            for idx, cell in enumerate(cells):
                columns.setdefault(idx, []).append(cell)
        flush()
        self.assertEqual(offenders, [],
                         "the equipment chapter must not tabulate statistics:\n  "
                         + "\n  ".join(offenders))


if __name__ == "__main__":
    unittest.main()
