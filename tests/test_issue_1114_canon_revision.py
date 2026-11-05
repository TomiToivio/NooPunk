"""#1114 revision guards: one playable timeline, and the Mandela Effect kept unresolved.

The revision's whole value is that it **supersedes** a chronology that had already landed. Documents rot in
exactly that direction: somebody adds a scene, a table or a summary, and the superseded account creeps back in
because it is the more exciting one. These tests keep the baseline and the memory apart.

Deliberately not tested: the prose's quality, the exact wording of any paragraph, or whether the Mandela Effect
has a cause. It does not, and a test that demanded one would be the bug.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALT = ROOT / "docs/world/ALTERNATE_HISTORY_1114.md"
PROGRAMMA = ROOT / "docs/world/PROGRAMMA_1114.md"
ANCHORS = ROOT / "docs/world/SOVIET_RESEARCH_ANCHORS_1114.md"
FORTRESS = ROOT / "docs/world/CANON_FORTRESS_EUROPE_1113.md"
POST = ROOT / "docs/world/POST_NHI_WORLD_1005.md"
RULEBOOK_TIMELINE = ROOT / "rulebook/7_TIMELINE.md"
CHRONOLOGY = ROOT / "data/world/chronology_1113.json"

RELATIVE_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def plain(source: str) -> str:
    """Prose with markdown emphasis removed: a bolded word still has to be findable."""
    return re.sub(r"[*`_]+", "", source).replace("\n", " ")


class OnePlayableTimeline(unittest.TestCase):
    def test_the_three_documents_exist(self):
        for path in (ALT, PROGRAMMA, ANCHORS):
            self.assertTrue(path.is_file(), f"missing {path.name}")

    def test_the_baseline_is_stated(self):
        body = text(ALT)
        for claim in ("collapse", "failed state", "intercept", "Finnish–Russian border"):
            self.assertIn(claim, body, f"the baseline does not state {claim!r}")

    def test_the_old_assertion_is_gone(self):
        """The previous revision said the USSR never collapses, in those words. It must not come back."""
        body = text(ALT).lower()
        self.assertNotIn("soviet union never collapses", body)
        self.assertNotIn("no yeltsin succession and no post-soviet russian federation", body)

    def test_the_reform_era_survives_only_as_memory(self):
        body = plain(text(ALT))
        self.assertIn("Mandela", body)
        # wherever the reform-era USSR is described, the document must also say it is not the baseline
        self.assertRegex(body, r"not\s+verified rulers of the playable world")
        self.assertIn("not settled", body)

    def test_the_troika_names_are_preserved_exactly(self):
        body = text(ALT)
        for name in ("Павел Пластик", "Настя Машин", "Игорь Мотор"):
            self.assertIn(name, body, f"{name} was lost in the revision")

    def test_rulebook_timeline_no_longer_asserts_survival(self):
        body = text(RULEBOOK_TIMELINE)
        self.assertNotIn("The Soviet Union survives, reforms", body)
        self.assertIn("collapsed in 1991", body)

    def test_the_fortress_document_names_the_right_actor(self):
        body = text(FORTRESS)
        self.assertNotIn("A restored Soviet Union invades Ukraine", body)
        self.assertIn("Russia invades Ukraine", body)

    def test_the_post_crisis_reference_agrees(self):
        body = text(POST)
        self.assertNotIn("The USSR survives the Cold War, reforms under", body)
        self.assertIn("Mandela", body)


class TheChronologyDataAgrees(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(text(CHRONOLOGY))
        cls.by_id = {e["id"]: e for e in cls.data["events"]}

    def test_russia_is_the_invader(self):
        event = self.by_id.get("russia_ukraine_invasion")
        self.assertIsNotNone(event, "the Russian invasion event is missing")
        self.assertIn("Russia", event["regions"])
        self.assertNotIn("soviet_ukraine_invasion", self.by_id)

    def test_the_interception_is_canon_and_undated(self):
        event = self.by_id.get("eu_russia_war_uap_interception")
        self.assertIsNotNone(event, "the UAP nuclear interception is not in the chronology")
        self.assertEqual(event["status"], "canon")
        self.assertNotRegex(event["when"], r"\b(19|20)\d{2}\b",
                            "the issue explicitly leaves the war's date open")

    def test_the_soviet_restoration_is_a_claim_not_canon(self):
        coup = self.by_id["soviet_coup"]
        self.assertEqual(coup["status"], "in_world_claim",
                         "a Soviet restoration cannot be canon in a timeline where the USSR collapsed")

    def test_no_canon_event_after_1991_has_a_soviet_actor(self):
        """The USSR existed before 1991, so a 1930s event may name it. A 2045 event may not."""
        offenders = []
        for event in self.data["events"]:
            if event["status"] != "canon" or "Soviet Union" not in event.get("regions", []):
                continue
            when = str(event["when"])
            years = [int(y) for y in re.findall(r"\b(19\d{2}|20\d{2})\b", when)]
            years += [int(d) for d in re.findall(r"\b(19\d0)s\b", when)]  # "1930s" is before 1991 too
            if years and min(years) < 1991:
                continue
            offenders.append(event["id"])
        self.assertEqual(offenders, [], f"these canon events still assume a Soviet state: {offenders}")


class TheSecretHistoryKeepsItsProvenance(unittest.TestCase):
    def test_the_five_levels_are_declared(self):
        body = text(PROGRAMMA).upper()
        for level in ("PLAYABLE BASELINE", "ACCEPTED SECRET HISTORY", "CONTESTED TESTIMONY",
                      "MANDELA-EFFECT MATERIAL", "AUTHOR-ONLY UNKNOWN"):
            self.assertIn(level, body, f"the provenance ladder is missing {level}")

    def test_the_programme_is_not_the_russian_government(self):
        body = plain(text(PROGRAMMA)).lower()
        self.assertRegex(body, r"not\s+the government of present-day russia")
        self.assertRegex(body, r"not\s+proof that the ussr survived")

    def test_the_coercion_is_named_and_the_ideal_kept_distinct(self):
        body = plain(text(PROGRAMMA)).lower()
        self.assertIn("hive mind", body)
        self.assertIn("voluntary", body)

    def test_mj12_is_contested_not_established(self):
        body = text(PROGRAMMA)
        section = body.split("## 3. MJ-12")[1].split("## 4.")[0].upper()
        self.assertIn("CONTESTED TESTIMONY", section)

    def test_clue_tiers_and_custody_exist(self):
        body = text(PROGRAMMA).lower()
        for word in ("clue tiers", "chain of custody", "contested", "confidence"):
            self.assertIn(word, body, f"the investigation design is missing {word}")


class TheResearchStaysHonest(unittest.TestCase):
    def test_the_three_labels_are_used(self):
        body = text(ANCHORS)
        for label in ("[HISTORY]", "[CLAIM]", "[GAME CANON]"):
            self.assertIn(label, body, f"the anchors document is missing {label}")

    def test_it_forbids_turning_a_claim_into_proof(self):
        body = plain(text(ANCHORS)).lower()
        self.assertIn("never proof", body)
        self.assertIn("real closed city", body)

    def test_it_cites_the_required_sources(self):
        body = text(ANCHORS)
        for anchor in ("SETKA", "Vasiliev", "ZATO", "Voronezh", "lawofone.info/s/8#6"):
            self.assertIn(anchor, body, f"{anchor} is not in the anchors catalogue")

    def test_the_law_of_one_is_not_a_narrator(self):
        body = plain(text(ANCHORS)).lower()
        self.assertIn("not independently validated", body)


class DocumentsStillLink(unittest.TestCase):
    def test_every_relative_markdown_link_resolves(self):
        broken = []
        for path in (ALT, PROGRAMMA, ANCHORS):
            for match in RELATIVE_LINK.finditer(text(path)):
                target = match.group(1)
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.name} -> {target}")
        self.assertEqual(broken, [], "broken links: " + "; ".join(broken))

    def test_the_three_documents_cross_reference_each_other(self):
        alt = text(ALT)
        self.assertIn("PROGRAMMA_1114.md", alt)
        self.assertIn("SOVIET_RESEARCH_ANCHORS_1114.md", alt)
        self.assertIn("ALTERNATE_HISTORY_1114.md", text(PROGRAMMA))
        self.assertIn("ALTERNATE_HISTORY_1114.md", text(ANCHORS))


if __name__ == "__main__":
    unittest.main()
