"""Structure guard for the #171–#180 lore-and-light-rules expansion.

Issues #171–#180 added a lot of lore and light-rules content across the rulebook
chapters. That content is mostly prose, which can drift or be silently deleted.
This guard pins the presence of the major additions and, just as importantly,
pins that the *reservations* they were careful not to cross are still in place
(equipment statistics stay undefined; psi powers are capabilities, not stat
blocks; deep hacking stays deferred).

It asserts structure and presence only; it does not constrain wording.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def flat(relative: str) -> str:
    """Whitespace-collapsed, lowercased text, so wrapping cannot hide a term."""
    text = (ROOT / relative).read_text(encoding="utf-8")
    return " ".join(text.split()).lower()


class BestiaryTests(unittest.TestCase):
    """RULEBOOK.md §§44–46."""

    def test_types_of_beings_section_exists(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("## 44. types of beings", text)

    def test_density_is_consciousness_not_species(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("density is a level of consciousness", text)
        # the key investigative principle: appearance cannot decide density
        self.assertIn("appearance alone cannot tell you which", text)

    def test_core_beings_are_catalogued(self) -> None:
        text = flat("RULEBOOK.md")
        for being in ("small greys", "tall greys", "orion hybrids", "men in black",
                      "plasmoids", "cryptoterrestrials", "higher self"):
            with self.subTest(being=being):
                self.assertIn(being, text)

    def test_hybrid_verification_rule(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("voight-kampff", text)
        self.assertIn("you do not shoot because someone seems non-human", text)
        # EMP must stay parked, not restored
        self.assertIn("do not restore", text)


class SingularityCrisisTests(unittest.TestCase):
    def test_section_exists_with_three_survivors(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("## 45. the singularity crisis", text)
        self.assertIn("panopticon", text)
        self.assertIn("the noösphere", text)

    def test_explanation_is_deliberately_open(self) -> None:
        text = flat("RULEBOOK.md")
        for explanation in ("contagion", "human attack", "nhi intervention",
                            "convergent failure", "something stranger"):
            with self.subTest(explanation=explanation):
                self.assertIn(explanation, text)


class ConfederationOrionTests(unittest.TestCase):
    def test_opposing_metaphysics_section(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("## 46. confederation and orion", text)
        self.assertIn("become the source", text)
        self.assertIn("return toward the source", text)

    def test_cyborgist_model(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("ai = human + llm + language + internet", text)
        self.assertIn("institutions become minds", text)


class PsychicChapterTests(unittest.TestCase):
    def test_psi_power_and_psychotronic_lists(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("psi powers", text)
        self.assertIn("psychotronic technologies", text)

    def test_muddy_boundary_principle(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("operational rather than ontological", text)

    def test_sleep_phase_and_disconnected_systems(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("four-way disentanglement", text)
        self.assertIn("assemblage integrity", text)

    def test_seity_is_parked(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("seity", text)
        self.assertIn("do not build mechanics on this yet", text)

    def test_atmanspacher_theory_present(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("atmanspacher", text)
        self.assertIn("structural correlations", text)
        self.assertIn("induced correlations", text)
        # must be framed as one in-world theory, not established fact
        self.assertIn("paradigm among rivals", text)


class PhysicalChapterTests(unittest.TestCase):
    def test_harm_ladder(self) -> None:
        text = flat("rulebook/3_PHYSICAL.md")
        for state in ("scratched", "wounded", "critical", "down"):
            with self.subTest(state=state):
                self.assertIn(state, text)

    def test_equipment_list(self) -> None:
        text = flat("rulebook/3_PHYSICAL.md")
        for category in ("weapons", "armor", "sensors and surveillance", "vehicles"):
            with self.subTest(category=category):
                self.assertIn(category, text)


class CyberneticChapterTests(unittest.TestCase):
    def test_implant_list(self) -> None:
        text = flat("rulebook/5_CYBERNETIC.md")
        for family in ("somatic and prosthetic", "neural and cognitive",
                       "psychotronic", "identity, memory and continuity"):
            with self.subTest(family=family):
                self.assertIn(family, text)

    def test_resleeving_lore_present(self) -> None:
        text = flat("rulebook/5_CYBERNETIC.md")
        self.assertIn("resleeving", text)
        self.assertIn("neo-feudal immortality", text)


class ReservationsPreservedTests(unittest.TestCase):
    """The new content must not have crossed the author-owned reservations."""

    def test_equipment_statistics_still_undefined(self) -> None:
        self.assertIn("equipment statistics remain undefined",
                      flat("rulebook/5_CYBERNETIC.md"))
        self.assertIn("statistics are undefined here by design",
                      flat("rulebook/3_PHYSICAL.md"))

    def test_deep_hacking_still_deferred(self) -> None:
        self.assertIn("deep hacking remains a separate deferred subsystem",
                      flat("rulebook/5_CYBERNETIC.md"))

    def test_psi_powers_are_capabilities_not_stat_blocks(self) -> None:
        self.assertIn("capability", flat("rulebook/6_PSYCHIC.md"))

    def test_agents_md_records_the_scope(self) -> None:
        text = flat("AGENTS.md")
        self.assertIn("issues #171–#180 add", text)

    def test_agents_md_still_reserves_numeric_statistics(self) -> None:
        self.assertIn("equipment statistics", flat("AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
