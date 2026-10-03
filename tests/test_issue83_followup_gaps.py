# -*- coding: utf-8 -*-
"""Guard for the #83 lore items that landed after the main §33 integration.

Issue #83 was integrated into ``RULEBOOK.md`` by the author as §33.7–§33.32. A review
against the issue found a few specific items the §33 integration did not yet carry:

* the **Eclipse Phase *Factors* analogue** (an amoeboid / slime-mold-like starfaring
  biological species), which the issue asks NoöPunk to keep alongside the ETI machine
  analogue;
* the **Tabby's Star / KIC 8462852** technosignature specifics (the issue names the star
  and the "slow dipper" candidate class);
* the **"Nazi Zookeepers" in-setting false theory** (the issue is explicit that the
  cosmic order must not endorse twentieth-century racial mythology);
* the **"Stone Age members of the galactic club"** framing.

This guard pins those additions and the anti-invention constraints around them. It is a
structure guard in the style of ``test_issue60_setting_canon.py``: it asserts the lore is
recorded and that no mechanics were smuggled in.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = "RULEBOOK.md"

_YEAR_RE = re.compile(r"\b20[3-9]\d\b")


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


def section(heading: str) -> str:
    """Body of a ``### 33.x`` subsection, or "" when missing."""
    text = read()
    marker = f"### {heading}"
    if marker not in text:
        return ""
    body = text.split(marker, 1)[1]
    nxt = re.search(r"(?m)^### ", body)
    return body[: nxt.start()] if nxt else body


def flat(heading: str) -> str:
    body = re.sub(r"[>*_`]", " ", section(heading))
    return " ".join(body.split()).lower()


class FactorsAndEtiArchetypesTests(unittest.TestCase):
    """#83 asks NoöPunk to keep the Eclipse Phase Factors and ETI analogues."""

    def test_the_new_subsection_exists(self) -> None:
        self.assertIn("### 33.29a", read())

    def test_the_factors_analogue_is_present(self) -> None:
        body = flat("33.29a")
        self.assertIn("factors", body)
        self.assertRegex(body, r"amoeboid|ameboid|slime-mold")
        self.assertIn("starfaring", body)

    def test_the_eti_analogue_is_present_and_does_not_dominate(self) -> None:
        body = flat("33.29a")
        self.assertIn("eti", body)
        self.assertRegex(body, r"does not dominate|does \*\*not\*\* dominate")

    def test_no_galactic_hierarchy_is_imported(self) -> None:
        self.assertIn("without importing its galactic hierarchy", flat("33.29a"))


class TechnosignatureTests(unittest.TestCase):
    """The issue names Tabby's Star / KIC 8462852 and the slow-dipper class."""

    def test_tabbys_star_is_named(self) -> None:
        body = flat("33.23")
        self.assertRegex(body, r"boyajian|tabby's star")
        self.assertIn("kic 8462852", body)

    def test_slow_dippers_and_dyson_signatures(self) -> None:
        body = flat("33.23")
        self.assertIn("slow dipper", body)
        self.assertIn("dyson-swarm", body)

    def test_epistemic_ambiguity_is_kept(self) -> None:
        body = flat("33.23")
        self.assertRegex(body, r"natural explanations|natural causes")
        self.assertIn("subset of the anomalous population eventually proves technological", body)


class NaziZookeepersTests(unittest.TestCase):
    """The issue requires the racial reading to be an in-setting FALSE theory."""

    def test_the_false_theory_is_recorded(self) -> None:
        body = flat("33.11")
        self.assertIn("nazi", body)
        self.assertIn("false theory", body)
        self.assertIn("nordic", body)

    def test_the_cosmos_does_not_endorse_it(self) -> None:
        body = flat("33.11")
        self.assertRegex(
            body,
            r"not\s+\*\*not\*\*\s+the cosmology|is \*\*not\*\* the cosmology|never the truth of the cosmology",
        )


class StoneAgeGalacticClubTests(unittest.TestCase):
    def test_the_stone_age_framing_is_present(self) -> None:
        body = flat("33.22")
        self.assertIn("stone age", body)


class AntiInventionTests(unittest.TestCase):
    def test_the_additions_introduce_no_mechanics(self) -> None:
        text = (flat("33.11") + flat("33.22") + flat("33.23")
                + flat("33.29a")).lower()
        for mechanic in ("2d6", "hit point", "initiative", "skill check", "armour"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, text)

    def test_no_concrete_future_dates_are_assigned(self) -> None:
        text = " ".join(section(h) for h in ("33.11", "33.22", "33.23", "33.29a"))
        offenders = [m.group(0) for m in _YEAR_RE.finditer(text)]
        self.assertEqual(offenders, [], f"the additions assign concrete years: {offenders}")


if __name__ == "__main__":
    unittest.main()
