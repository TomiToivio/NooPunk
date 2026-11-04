"""Offline tests for issue #1144 source monitoring."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools/poll_monitoring_sources.py"
spec = importlib.util.spec_from_file_location("poll_monitoring_sources", SCRIPT)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class SourceMonitoringTests(unittest.TestCase):
    def test_registry_and_user_links(self):
        data = json.loads(monitor.REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual([], monitor.validate_registry(data))
        videos = {s.get("platform_ids", {}).get("youtube_video") for s in data["sources"]}
        self.assertTrue({"qUc-uAlJU2k", "skOadFbPEPs", "b8UFh7BQZ2A"} <= videos)
        self.assertTrue(all(not s.get("feed_url") for s in data["sources"] if s["status"] == "unverified"))

    def test_canonical_and_dedup(self):
        a = {"url": "https://example.com/watch?v=1&utm_source=x", "canonical_url": monitor.canonical_url("https://example.com/watch?v=1&utm_source=x")}
        b = {"url": "https://example.com/watch?v=1", "canonical_url": monitor.canonical_url("https://example.com/watch?v=1")}
        self.assertEqual(1, len(monitor.unique_items([a, b])))
        seen = {a["canonical_url"]}
        self.assertEqual([], monitor.unique_items([b], seen))

    def test_rss_missing_metadata_and_provenance(self):
        data = b"<rss><channel><item><title>Case</title><link>https://example.org/case</link></item></channel></rss>"
        items = monitor.parse_feed(data, "ufo-asiaa")
        self.assertIsNone(items[0]["published"])
        self.assertEqual("source_statement", items[0]["evidence_level"])
        self.assertEqual("review_required", items[0]["canon_status"])

    def test_atom(self):
        feed = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Test</title><id>abc</id><updated>2026-11-04</updated><link href="https://example.org/item"/></entry></feed>'
        items = monitor.parse_feed(feed, "sample")
        self.assertEqual("2026-11-04", items[0]["published"])
        self.assertEqual("https://example.org/item", items[0]["canonical_url"])

    def test_deleted_and_broken_feed_handling(self):
        self.assertEqual([], monitor.parse_feed(b"<rss><channel/></rss>", "sample"))
        with self.assertRaises(ValueError):
            monitor.parse_feed(b"<html/>", "sample")
        with self.assertRaises(Exception):
            monitor.parse_feed(b"invalid", "sample")

    def test_duplicate_ids_and_non_https(self):
        bad = {"sources": [
            {"id": "x", "priority": "P0", "status": "active", "canonical_url": "https://a.org"},
            {"id": "x", "priority": "wrong", "status": "active", "canonical_url": "http://b.org"},
        ]}
        self.assertGreaterEqual(len(monitor.validate_registry(bad)), 3)

    def test_dry_run_no_network(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps({"sources": []}), encoding="utf-8")
            self.assertEqual(0, monitor.main(["--registry", str(path), "--dry-run"]))


if __name__ == "__main__":
    unittest.main()
