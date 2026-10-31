"""#908: an approved asset means the bytes are there and match their record.

The manifest is only worth having if a wrong entry fails somewhere. These tests build manifests and real
PNG/WebP bytes in a temp tree and assert that the checker refuses each way an image library goes wrong:
an unknown category, a portrait cropped wide, a hash from a re-export, an approval with no file, and —
the rule #908 leads with — science-fiction scenery in a Helsinki scene that nobody asked for.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import image_manifest as im  # noqa: E402


def png_bytes(width: int, height: int) -> bytes:
    """A minimal, valid-enough PNG: signature, IHDR, empty IDAT, IEND. Headers are what the checker reads."""

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00")) + chunk(b"IEND", b""))


class ManifestFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for category in im.CATEGORIES:
            (self.root / "images" / category).mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def manifest(self, *assets: dict, pending: tuple[dict, ...] | dict = ()) -> dict:
        return {
            "schema_version": im.SCHEMA_VERSION,
            "root": im.MANIFEST_ROOT,
            "categories": list(im.CATEGORIES),
            "assets": list(assets),
            "pending": list(pending) if isinstance(pending, tuple) else [pending] if pending else [],
        }

    def write_image(self, category: str, name: str, width: int, height: int) -> dict:
        data = png_bytes(width, height)
        path = self.root / "images" / category / name
        path.write_bytes(data)
        return {
            "id": Path(name).stem,
            "category": category,
            "path": f"{im.MANIFEST_ROOT}{category}/{name}",
            "licence": "original work, CC BY 4.0",
            "provenance": "generated for NoöPunk, 2026-10-31",
            "approved": True,
            "dimensions": {"width": width, "height": height},
            "sha256": hashlib.sha256(data).hexdigest(),
        }


class HeaderTests(unittest.TestCase):
    def test_png_and_webp_sizes_are_read_from_headers(self):
        self.assertEqual(im.image_size(png_bytes(600, 800)), (600, 800))
        vp8x = (b"RIFF" + struct.pack("<I", 0) + b"WEBP" + b"VP8X"
                + struct.pack("<I", 10) + b"\x00\x00\x00\x00"
                + (1920 - 1).to_bytes(3, "little") + (1080 - 1).to_bytes(3, "little"))
        self.assertEqual(im.image_size(vp8x), (1920, 1080))

    def test_junk_is_not_an_image(self):
        self.assertIsNone(im.image_size(b"not an image at all"))


class AcceptanceTests(ManifestFixture):
    def test_a_correct_portrait_passes(self):
        self.assertEqual(im.validate(self.manifest(
            self.write_image("characters/portraits", "harri_romppainen_street.png", 600, 800)),
            self.root), [])

    def test_a_correct_landscape_passes(self):
        self.assertEqual(im.validate(self.manifest(
            self.write_image("locations", "helsinki_kamppi_rain_evening.png", 1920, 1080)),
            self.root), [])

    def test_resolve_returns_the_file_for_an_approved_asset(self):
        manifest = self.manifest(
            self.write_image("characters/portraits", "harri_romppainen_street.png", 600, 800))
        resolved = im.resolve(manifest, "harri_romppainen_street", self.root)
        self.assertIsNotNone(resolved)
        self.assertTrue(resolved.is_file())


class RefusalTests(ManifestFixture):
    def problems(self, *assets: dict, pending: tuple[dict, ...] | dict = ()) -> list[str]:
        return im.validate(self.manifest(*assets, pending=pending), self.root)

    def test_a_portrait_cropped_to_wide_is_refused(self):
        problems = self.problems(
            self.write_image("characters/portraits", "harri_romppainen_street.png", 1920, 1080))
        self.assertTrue(any("allowed composition" in p for p in problems), problems)

    def test_a_hash_from_another_export_is_refused(self):
        asset = self.write_image("locations", "kamppi.png", 1920, 1080)
        asset["sha256"] = "0" * 64
        self.assertTrue(any("sha256 does not match" in p for p in self.problems(asset)))

    def test_declared_dimensions_must_match_the_file(self):
        asset = self.write_image("locations", "kamppi.png", 1920, 1080)
        asset["dimensions"] = {"width": 1280, "height": 720}
        self.assertTrue(any("dimensions say" in p for p in self.problems(asset)))

    def test_approval_without_a_file_is_refused(self):
        orphan = {"id": "ghost", "category": "events", "path": f"{im.MANIFEST_ROOT}events/ghost.png",
                  "licence": "x", "provenance": "y", "approved": True,
                  "dimensions": {"width": 1600, "height": 1200}, "sha256": "0" * 64}
        self.assertTrue(any("has no file" in p for p in self.problems(orphan)))

    def test_an_unknown_category_is_refused(self):
        asset = self.write_image("events", "beat.png", 1600, 1200)
        asset["category"] = "wallpapers"
        self.assertTrue(any("unknown category" in p for p in self.problems(asset)))

    def test_a_path_outside_its_category_is_refused(self):
        asset = self.write_image("events", "beat.png", 1600, 1200)
        asset["path"] = f"{im.MANIFEST_ROOT}locations/beat.png"
        self.assertTrue(any("path must live under" in p for p in self.problems(asset)))

    def test_a_non_snake_case_id_is_refused(self):
        asset = self.write_image("events", "beat.png", 1600, 1200)
        asset["id"] = "Beat-01"
        self.assertTrue(any("snake_case" in p for p in self.problems(asset)))

    def test_a_missing_licence_is_refused(self):
        asset = self.write_image("events", "beat.png", 1600, 1200)
        asset["licence"] = ""
        self.assertTrue(any("licence is required" in p for p in self.problems(asset)))

    def test_unjustified_science_fiction_is_refused(self):
        asset = self.write_image("locations", "helsinki_street.png", 1920, 1080)
        asset["sci_fi_motifs"] = ["hovering_car"]
        self.assertTrue(any("sci_fi_justification" in p for p in self.problems(asset)))

    def test_justified_science_fiction_is_accepted(self):
        asset = self.write_image("locations", "helsinki_street_anomaly.png", 1920, 1080)
        asset["sci_fi_motifs"] = ["hovering_car"]
        asset["sci_fi_justification"] = "the anomaly scene the story asks for"
        self.assertEqual(self.problems(asset), [])

    def test_a_pending_asset_that_already_has_bytes_must_be_promoted(self):
        pending = {"id": "harri_romppainen_street", "category": "characters/portraits",
                   "target_path": f"{im.MANIFEST_ROOT}characters/portraits/harri_romppainen_street.png",
                   "status": "awaiting_binary_upload"}
        (self.root / "images/characters/portraits/harri_romppainen_street.png").write_bytes(
            png_bytes(600, 800))
        self.assertTrue(any("promote it to assets" in p for p in self.problems(pending=pending)))

    def test_unjustified_science_fiction_in_a_pending_brief_is_refused(self):
        pending = {"id": "helsinki_street", "category": "locations",
                   "target_path": f"{im.MANIFEST_ROOT}locations/helsinki_street.png",
                   "status": "awaiting_binary_upload", "sci_fi_motifs": ["hovering_car"]}
        self.assertTrue(any("sci_fi_justification" in p for p in self.problems(pending=pending)))

    def test_pending_assets_are_never_resolved(self):
        pending = {"id": "harri_romppainen_street", "category": "characters/portraits",
                   "target_path": f"{im.MANIFEST_ROOT}characters/portraits/harri_romppainen_street.png",
                   "status": "awaiting_binary_upload"}
        manifest = self.manifest(pending=pending)
        self.assertIsNone(im.resolve(manifest, "harri_romppainen_street", self.root))


class ShippedManifestTests(unittest.TestCase):
    def test_the_repository_manifest_is_valid(self):
        """The real file, not a fixture: whatever is committed must be truthful."""
        if not im.MANIFEST.exists():  # pragma: no cover - only before #909 lands
            self.skipTest("images/manifest.json not present yet")
        manifest = im.load()
        self.assertEqual(im.validate(manifest), [])
        self.assertEqual(json.loads(json.dumps(manifest)), manifest)


if __name__ == "__main__":
    unittest.main()
