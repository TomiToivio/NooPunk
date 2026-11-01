"""Guard against accidental claims of complete CWN parity without evidence (#1025)."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

def load():
    spec = importlib.util.spec_from_file_location("cwn_mud_parity_1025", ROOT / "tools/cwn_mud_parity_1025.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_initial_inventory_is_honest_and_stable():
    report = load().build()
    assert report["total_families"] >= 12
    assert report["verified_complete"] == 0
    assert len({row["family"] for row in report["families"]}) == report["total_families"]
    for row in report["families"]:
        assert row["status"] == "unverified"
        assert not row["source_pdf_reviewed"]
        assert not row["in_game_command_verified"]
        assert not row["playtest_verified"]
        for group in ("rules_code_paths", "mud_code_paths", "test_paths", "command_candidates"):
            assert all((ROOT / path).is_file() for path in row[group])

def test_missing_files_do_not_count_as_implemented(tmp_path):
    report = load().build(tmp_path)
    assert all(not row["rules_code_paths"] and not row["mud_code_paths"]
               for row in report["families"])

def test_markdown_never_claims_completion():
    text = load().markdown(load().build())
    assert "not full book parity" in text
    assert "Book verified" in text
    assert "Playable verified" in text
