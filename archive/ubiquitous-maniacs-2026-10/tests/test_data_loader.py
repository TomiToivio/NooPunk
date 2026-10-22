from pathlib import Path

from src.social import load_people_records, load_relationship_records


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_people_data_loads_six_people() -> None:
    records = load_people_records(DATA_DIR / "lab_people.csv")
    assert len(records) == 6
    assert sum(record["role"] == "patient" for record in records) == 2
    assert sum(record["role"] == "staff" for record in records) == 3
    assert sum(record["role"] == "ai" for record in records) == 1
    jung = next(record for record in records if record["id"] == "ufab_ragnarok")
    assert jung == {"id": "ufab_ragnarok", "name": "UFAB Ragnarök (C.G. Jung)", "role": "ai"}


def test_relationship_data_loads() -> None:
    records = load_relationship_records(DATA_DIR / "lab_relationships.csv")
    assert records
    assert all("source" in record and "target" in record and "relationship" in record for record in records)
