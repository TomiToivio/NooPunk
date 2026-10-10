# -*- coding: utf-8 -*-
"""Guard for the #197 alignment: marketing positioning, UNSA lore, academy lifepath.

Pins the properties that #197 specifies and that a later edit could silently lose:

1. the **public-facing positioning** exists in `README.md` — genre line, the three
   comparison touchstones, the "pre-Eclipse Phase" *degree-of-transformation* shorthand
   (never a prequel), the not-postapocalypse/no-cosmic-horror tone bound, and the explicit
   no-affiliation disclaimer;
2. the **UNSA name canon** is the one #197 mandates — *United Nations Security
   Administration*, with the former *UN X-Risk Administration* preserved as institutional
   history — and the machine-readable `data/world/organizations.yaml` agrees with the
   rulebook;
3. §38 keeps the **academy/lifepath premise**: pooled member-state secondment, the Academy
   as training/education/research, UNSA as *not* a world government, the shift from
   early two-sided diplomacy to the NHI cold war, and the newly-graduated default team;
4. `rulebook/14_CHARACTER_GENERATION.md` carries the **five-step lifepath**, the
   Geeks/Jocks/Freaks *student slang* (not classes), and the worked graduate backgrounds;
5. the issue's **cross-links** to #144 / #158 / #159 survive.

Asserts structure and presence only, never wording beyond the required invariants.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
RULEBOOK = ROOT / "RULEBOOK.md"
CHARGEN = ROOT / "rulebook" / "14_CHARACTER_GENERATION.md"
ORG = ROOT / "data" / "world" / "organizations.yaml"
FACTIONS = ROOT / "FACTIONS.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flat(text: str) -> str:
    return " ".join(text.split())


class PositioningTests(unittest.TestCase):
    """#197 §1 — genre, tone, audience, pitch and comparative positioning."""

    def setUp(self) -> None:
        self.readme = read(README)
        self.flat_readme = flat(self.readme)

    def test_genre_and_supporting_registers(self) -> None:
        self.assertIn("## Genre and positioning", self.readme)
        for term in ("cyberpunk science fantasy", "investigative adventure",
                     "transhumanism", "NHI crisis", "post-catastrophe reconstruction"):
            self.assertIn(term, self.flat_readme)

    def test_three_comparison_touchstones(self) -> None:
        for term in ("Shadowrun", "Eclipse Phase", "The X-Files"):
            self.assertIn(term, self.flat_readme)

    def test_pre_eclipse_phase_is_degree_not_prequel(self) -> None:
        self.assertIn("pre-Eclipse Phase", self.flat_readme)
        self.assertIn("not a prequel and not shared continuity", self.flat_readme)
        self.assertIn("degree of societal transformation", self.flat_readme)

    def test_tone_avoids_full_postapocalypse_and_cosmic_horror(self) -> None:
        self.assertIn("not a full postapocalypse", self.flat_readme)
        self.assertIn("not Lovecraftian cosmic horror", self.flat_readme)

    def test_no_affiliation_and_positioning_hypothesis(self) -> None:
        self.assertIn("positioning hypothesis", self.flat_readme)
        self.assertIn("claims no affiliation", self.flat_readme)


class UNSANamingTests(unittest.TestCase):
    """#197 §2 — the official expansion, the former name, and the in-universe nicknames."""

    def setUp(self) -> None:
        self.book = read(RULEBOOK)
        self.book_flat = flat(self.book)
        self.org = read(ORG)
        self.factions = read(FACTIONS)

    def test_official_expansion_is_the_administration(self) -> None:
        self.assertIn("United Nations Security Administration (UNSA)", self.book)
        self.assertIn("United Nations Security Administration", self.org)
        self.assertIn("United Nations Security Administration", self.factions)

    def test_the_old_expansion_is_gone(self) -> None:
        for text in (self.book, self.org, self.factions):
            self.assertNotIn("United Nations Security Agency", text)

    def test_former_name_is_preserved_as_history(self) -> None:
        self.assertIn("UN X-Risk Administration", self.book)
        self.assertIn("UN X-Risk Administration", self.org)
        self.assertNotIn("UN X-Risk Agency", self.book)

    def test_nicknames_are_informal_and_flagged_as_such(self) -> None:
        self.assertIn("X-Files", self.book_flat)
        self.assertIn("X-Com", self.book_flat)
        self.assertIn("not official departments", self.book_flat)
        self.assertIn("any connection to the existing entertainment franchises", self.book_flat)

    def test_mj12_stays_rejected(self) -> None:
        self.assertIn("not an acceptable nickname", self.book_flat)

    def test_machine_readable_model_matches_the_rulebook(self) -> None:
        self.assertIn("canonical_name: United Nations Security Administration", self.org)
        self.assertIn("former_names", self.org)
        self.assertIn("not_a_world_government", self.org)
        self.assertIn("UNSA Academy", self.org)


class UNSASettingTests(unittest.TestCase):
    """#197 §2 — origins, Academy, sovereignty bound, cold war, default team."""

    def setUp(self) -> None:
        self.book = read(RULEBOOK)
        self.book_flat = flat(self.book)

    def test_pooled_member_state_secondment_origin(self) -> None:
        self.assertIn("#### Origins: pooled member-state resources", self.book)
        self.assertIn("act of pooling", self.book_flat)
        self.assertIn("secondment", self.book_flat)

    def test_academy_is_training_education_and_research(self) -> None:
        self.assertIn("#### The Academy and the research mandate", self.book)
        self.assertIn("its **own Academy**", self.book)
        self.assertIn("training institution", self.book_flat)
        self.assertIn("continuing-education school", self.book_flat)
        self.assertIn("research centre", self.book_flat)

    def test_unsa_is_not_a_world_government(self) -> None:
        self.assertIn("#### UNSA is not a world government", self.book)
        self.assertIn("UNSA is an agency, not a sovereign", self.book_flat)
        self.assertIn("States retain their sovereignty", self.book_flat)

    def test_diplomacy_subsection_is_the_cold_war_one(self) -> None:
        self.assertIn("#### Diplomacy and the emerging NHI cold war", self.book)
        self.assertIn("diplomatic toward both blocs", self.book_flat)

    def test_orion_is_a_hybrid_cold_proxy_conflict_not_an_invasion(self) -> None:
        self.assertIn("hybrid, cold and proxy conflict", self.book_flat)
        self.assertIn("rather than open invasion", self.book_flat)

    def test_confederacy_is_friendly_but_not_above_criticism(self) -> None:
        self.assertIn("Friendly is not the same as settled", self.book_flat)
        self.assertIn("not above criticism", self.book_flat)

    def test_default_team_is_new_graduates(self) -> None:
        self.assertIn("team of newly graduated UNSA agents on their first", self.book_flat)
        self.assertIn("instructors, commanding officers", self.book_flat)
        self.assertIn("forbids other campaign models", self.book_flat)


class LifepathAndSlangTests(unittest.TestCase):
    """#197 §3 — the five-step lifepath, the student slang, the worked backgrounds."""

    def setUp(self) -> None:
        self.chargen = read(CHARGEN)
        self.chargen_flat = flat(self.chargen)

    def test_five_step_lifepath(self) -> None:
        self.assertIn("## 13.8 The default lifepath in five steps (issue #197)", self.chargen)
        for step in ("Childhood, social origins and formative experience",
                     "The experience that made UNSA recruit them",
                     "UNSA Academy common training",
                     "Specialty",
                     "Graduation, relationships and first assignment"):
            self.assertIn(step, self.chargen_flat)

    def test_academy_training_is_the_equalizer(self) -> None:
        self.assertIn("equalizing step", self.chargen_flat)

    def test_geeks_jocks_freaks_is_slang_not_classes(self) -> None:
        self.assertIn("Geeks, Jocks & Freaks", self.chargen_flat)
        self.assertIn("student slang, not an official or mandatory classification",
                      self.chargen_flat)
        self.assertIn("no mechanical weight", self.chargen_flat)

    def test_slang_carries_the_pathology_caution(self) -> None:
        self.assertIn("inherently pathological", self.chargen_flat)
        self.assertIn("categories overlap", self.chargen_flat.lower())

    def test_worked_graduate_backgrounds(self) -> None:
        self.assertIn("## 13.10 Example new-graduate backgrounds (issue #197)", self.chargen)
        self.assertIn("Four worked examples", self.chargen_flat)

    def test_edges_remain_unsettled(self) -> None:
        self.assertIn("does not settle", self.chargen_flat)
        self.assertIn("separate mechanical", self.chargen_flat)

    def test_limitations_section_still_closes_the_chapter(self) -> None:
        self.assertIn("## 13.11 What this chapter deliberately does NOT define", self.chargen)


class CrossLinkTests(unittest.TestCase):
    """#197 — coordinate with, do not replace, #144 / #158 / #159."""

    def setUp(self) -> None:
        self.chargen = read(CHARGEN)

    def test_cross_links_survive(self) -> None:
        for issue in ("#144", "#158", "#159"):
            self.assertIn(issue, self.chargen)


if __name__ == "__main__":
    unittest.main()
