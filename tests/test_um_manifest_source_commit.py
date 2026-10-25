"""The import commit is a historical fact, not a live reading of the upstream repository.

The bug
-------

`tools/build_ubiquitous_maniacs_manifest.py` wrote `source commit at import` from
`git -C <upstream> rev-parse HEAD` — the upstream checkout's **current** head.

The field means *the commit this corpus was imported from on its import date*. Stamping it from
live state rewrites history: once the upstream repository advanced past the imported commit, every
run rewrote the manifest, and `--check` could never pass again on any machine that had the upstream
clone. The generator reported its own recorded fact as drift, permanently.

That is worse than a stale artefact: a provenance record that silently updates itself proves
nothing about what was actually imported.

Resolution order after the fix: explicit `NOOPUNK_PCM_SOURCE_COMMIT` (a deliberate re-import pin),
then the commit already recorded in `manifest.json`, then upstream `HEAD` for a first build.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = REPO / "tools" / "build_ubiquitous_maniacs_manifest.py"

IMPORTED_COMMIT = "b0b3a47b57da0f9f28e167d634be67e0ae883dab"
UPSTREAM_HEAD = "e1eb752119af8a0f06d3a747b372f53d4bd3f00a"


def load_tool():
    """Import the generator from its file path.

    The module must be registered in ``sys.modules`` *before* execution: it defines
    ``@dataclass`` types, and dataclasses resolves annotations through
    ``sys.modules[cls.__module__]``, which is None for a spec-loaded module that was never
    registered. Without this the import fails with
    ``AttributeError: 'NoneType' object has no attribute '__dict__'``.
    """
    name = "um_manifest_tool"
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


class SourceCommitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

        # an "upstream" checkout whose HEAD is NOT the imported commit
        upstream = self.root / "upstream"
        upstream.mkdir()
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
        subprocess.run(["git", "init", "-q"], cwd=upstream, check=True, env=env)
        (upstream / "f").write_text("x", encoding="utf-8")
        subprocess.run(["git", "add", "f"], cwd=upstream, check=True, env=env)
        subprocess.run(["git", "commit", "-qm", "c"], cwd=upstream, check=True, env=env)
        self.upstream = upstream

        self.manifest = self.root / "manifest.json"
        self.patches = [
            mock.patch.object(self.tool, "SOURCE_ROOT", upstream),
            mock.patch.object(self.tool, "MANIFEST_JSON", self.manifest),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self) -> None:
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def write_manifest(self, commit: str) -> None:
        self.manifest.write_text(
            json.dumps({"source": {"commit": commit}}), encoding="utf-8"
        )

    def test_a_recorded_import_commit_survives_an_advanced_upstream(self) -> None:
        """The whole bug: live HEAD must not overwrite the recorded import commit."""
        self.write_manifest(IMPORTED_COMMIT)
        resolved = self.tool._source_commit()
        self.assertEqual(resolved, IMPORTED_COMMIT)
        head = subprocess.run(
            ["git", "-C", str(self.upstream), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        self.assertNotEqual(resolved, head, "the live head overwrote the recorded commit")

    def test_an_explicit_pin_wins_so_a_reimport_stays_deliberate(self) -> None:
        self.write_manifest(IMPORTED_COMMIT)
        with mock.patch.dict(os.environ, {"NOOPUNK_PCM_SOURCE_COMMIT": UPSTREAM_HEAD}):
            self.assertEqual(self.tool._source_commit(), UPSTREAM_HEAD)

    def test_a_first_build_still_falls_back_to_upstream_head(self) -> None:
        """No recorded commit and no pin: the original behaviour is correct here."""
        head = subprocess.run(
            ["git", "-C", str(self.upstream), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        self.assertEqual(self.tool._source_commit(), head)

    def test_a_malformed_recorded_commit_is_not_treated_as_provenance(self) -> None:
        """A blanked or truncated field must not block a first build."""
        head = subprocess.run(
            ["git", "-C", str(self.upstream), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        for bad in ("", "unavailable", IMPORTED_COMMIT[:12]):
            with self.subTest(bad=bad):
                self.write_manifest(bad)
                self.assertEqual(self.tool._source_commit(), head)


if __name__ == "__main__":
    unittest.main()
