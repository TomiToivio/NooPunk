"""Behavioral tests of the executable discourse reader, not lore/canon text checks."""
import json
import pytest
from strategy_game.un_political_discourse import load_un_political_discourse, interpret_event


def test_reader_exposes_distinct_perspectives():
    view = interpret_event("confederacy_harvest_offer")
    assert len(view["party_readings"]) == len(load_un_political_discourse()["parties"])
    assert len({p["party_id"] for p in view["party_readings"]}) == len(view["party_readings"])
    assert all(p["stance"] for p in view["party_readings"])
    assert view["event"]["status"] == "observed"


def test_unknown_event_is_not_invented():
    with pytest.raises(KeyError):
        interpret_event("invented-event")


def test_loader_allows_future_party_additions(tmp_path):
    payload = load_un_political_discourse()
    newcomer = json.loads(json.dumps(payload["parties"][0]))
    newcomer["id"] = "future_party"
    payload["parties"].append(newcomer)
    path = tmp_path / "extra.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert len(load_un_political_discourse(path)["parties"]) == len(payload["parties"])


def test_loader_rejects_duplicate_ids(tmp_path):
    payload = load_un_political_discourse()
    payload["parties"].append(dict(payload["parties"][0]))
    path = tmp_path / "duplicate.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        load_un_political_discourse(path)
