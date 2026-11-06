import json
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from src.simulation.ai26_experiment import trial
from src.simulation.ai26_input import read_relations


class ContestationTests(unittest.TestCase):
    def test_paired_contacts_and_replay(self):
        args = (12, 30, ["public-control", "private-control"])
        control = trial(9, 0, *args)
        changed = trial(9, 1, *args)
        assert changed == trial(9, 1, *args)
        assert control["incoming_contacts"] == changed["incoming_contacts"]
        memberships = changed["initial_affiliations"].copy()
        for row in changed["snapshots"]:
            for event in (e for e in changed["events"] if e["turn"] == row["turn"]):
                assert event["synthetic"]
                if event["action_type"] == "disaffiliate":
                    assert memberships.pop(event["actor"]) == event["target"]
                elif event["action_type"] == "affiliate":
                    memberships[event["actor"]] = event["target"]
            assert memberships == row["member_of"]
        assert control["snapshots"][-1]["member_of"] == control["initial_affiliations"]
        assert changed["snapshots"][-1]["member_of"] != control["initial_affiliations"]
        assert 0 in trial(4, 0, 10, 1, args[-1])["incoming_contacts"].values()


    def test_reviewed_projection(self):
        try:
            import laclaugpt_data_analysis.canonical
        except ModuleNotFoundError as exc:
            if exc.name != "laclaugpt_data_analysis":
                raise
            self.skipTest("Install the optional upstream Data Analysis package")
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp_path = Path(directory.name)
        stamp = "2026-01-01T00:00:00Z"
        url = "https://example.invalid/synthetic"
        attrs = dict(provenance_id="p", evidence_ids=["e"], review_status="ACCEPTED")
        record = dict(schema_version="1.2.0", source_url=url,
                      review=dict(status="ACCEPTED", reviewer="fixture", reviewed_at=stamp),
                      provenance=[dict(provenance_id="p", method="fixture", created_at=stamp)],
                      evidence=[dict(evidence_id="e", kind="text", source_url=url, quote="AI for all", provenance_id="p")],
                      analysis=dict(signifiers=[dict(object_id=k, kind="signifier", label=k,
                                                     uncertainty="tentative", **attrs) for k in ("AI", "all")],
                                    relations=[dict(relation_id="r", relation_type="articulates",
                                                    source_ref="AI", target_ref="all", **attrs)]))
        path = tmp_path / "example.json"
        path.write_text(json.dumps(record))
        result = read_relations(path)
        assert result["objects"]["AI"]["uncertainty"] == "tentative"
        assert result["evidence"]["e"]["quote"] == "AI for all"
        for field, value in (("review_status", "PROVISIONAL"), ("evidence_ids", ["missing"]),
                             ("target_ref", "unknown"), ("provenance_id", "missing")):
            bad = json.loads(json.dumps(record))
            bad["analysis"]["relations"][0][field] = value
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                read_relations(path)
