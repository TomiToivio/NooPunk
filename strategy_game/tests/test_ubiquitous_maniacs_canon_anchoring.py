"""The Ubiquitous Maniacs scenario must not contradict this repository's canon.

The corpus it unifies predates the canon and contradicts it in twelve recorded places
(`archive/ubiquitous-maniacs-2026-10/MIGRATION_MAP.md`, rows C1–C12). Three of those
contradictions are load-bearing for the scenario, and two of them are **name collisions with
different referents** — the migration map names them as the most dangerous rows precisely
because they do not look like conflicts:

* **C5, the institution.** The corpus's setting is *UFAB*, which appears in **none** of this
  repository's canon rulebook files. Canon has the UNSA, the Academy, Eurodef, the Supo and
  Ö-Mappi. The scenario must therefore be anchored to a canon institution, and must not
  present UFAB as one.
* **C3, the name.** The corpus's protagonist is *Emil* Romppainen; canon's is *Dr. Harri S.
  Romppainen* ("Dirty Harry"), a different man. The scenario must use the canon character.
* **C4, the other collision.** The corpus's *Lotta Kallio* is a person; canon's *Kallio* is a
  **district**. The scenario must not use the name for a person.

These are executable contracts over the scenario's own data, not judgements about the prose.
They assert that specific strings are absent and specific ones present, because those
strings are the contradiction. The policy of `AGENTS.md` and issue #271 forbids tests over
lore and canon *in general*; what is pinned here is narrower and mechanical — that this
scenario's cast and setting do not contradict the canon's own cast and setting — which is a
property of executable data.

The check that the corpus's own material is absent is in
`tests/test_third_party_expression_absent.py`, which is about third-party expression rather
than about canon.
"""
from __future__ import annotations

import unittest

from strategy_game.scenarios import ubiquitous_maniacs as scenario


class CanonAnchoringTests(unittest.TestCase):
    """The scenario is anchored to canon and does not reintroduce the corpus's conflicts."""

    def test_the_cast_uses_the_canon_romppainen_not_the_corpus_one(self) -> None:
        """C3: the corpus's *Emil* Romppainen is a different man from canon's Harri Romppainen."""
        names = [character.name for character in scenario.cast().values()]
        self.assertTrue(any("Harri Romppainen" in name for name in names),
                        "the canon Romppainen must be in the cast")
        for name in names:
            self.assertNotIn("Emil", name,
                             "the corpus's *Emil* Romppainen is a different character (C3)")

    def test_the_cast_does_not_use_the_corpus_ingrid_falk(self) -> None:
        """C3/C4: canon has *Laura* Falk; the corpus's *Ingrid* Falk is a different person."""
        names = [character.name for character in scenario.cast().values()]
        for name in names:
            self.assertNotIn("Ingrid", name,
                             "the corpus's Ingrid Falk is a different character from Laura Falk")

    def test_the_cast_does_not_turn_kallio_into_a_person(self) -> None:
        """C4: canon's *Kallio* is a district, not a person."""
        for name in (c.name for c in scenario.cast().values()):
            self.assertNotIn("Kallio", name, "Kallio is a district in canon, not a person (C4)")

    def test_the_scenario_does_not_claim_the_corpus_institution(self) -> None:
        """C5: UFAB appears in no canon rulebook file, so the scenario must not present it as one."""
        prose = " ".join(scene["text"] for scene in scenario.SCENES.values())
        self.assertNotIn("UFAB", prose,
                         "the corpus's UFAB is not a canon institution (C5)")

    def test_the_scenario_is_anchored_to_a_canon_institution(self) -> None:
        """The scenario's frame names the UNSA, which is canon."""
        self.assertIn("UNSA", scenario.FRAME)
        self.assertIn("UNSA", scenario.FACILITY)

    def test_the_scenario_states_no_exact_future_date(self) -> None:
        """C2 and `AGENTS.md` §6: future dates are 20XX unless the author says otherwise."""
        prose = " ".join(scene["text"] for scene in scenario.SCENES.values())
        self.assertNotRegex(prose, r"\b20[0-4][0-9]\b",
                            "the narration must not assign an exact future year")
        self.assertIn("20XX", scenario.FRAME)

    def test_the_scenario_does_not_claim_the_fall_happened(self) -> None:
        """C1: canon is pre-Fall; the corpus is post-Fall. The scenario must not narrate the Fall."""
        prose = " ".join(scene["text"] for scene in scenario.SCENES.values()).lower()
        for phrase in ("after the fall", "post-fall", "the fall happened", "since the fall"):
            self.assertNotIn(phrase, prose, "canon is pre-Fall (C1)")

    def test_the_scenario_says_it_is_not_canon(self) -> None:
        """The module must declare its status, as the Kallio case does."""
        doc = (scenario.__doc__ or "")
        self.assertIn("not canon", doc.lower())


if __name__ == "__main__":
    unittest.main()
