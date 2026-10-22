from pathlib import Path

import pytest

from src.social import ALLOWED_ROLES, load_people_records, load_relationship_records
from src.social.ontology import validate_person_record, validate_relationship_record


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_roles_are_allowed() -> None:
    people = load_people_records(DATA_DIR / "lab_people.csv")
    for person in people:
        validate_person_record(person)
        assert person["role"] in ALLOWED_ROLES


def test_relationship_references_are_valid() -> None:
    people = load_people_records(DATA_DIR / "lab_people.csv")
    relationships = load_relationship_records(DATA_DIR / "lab_relationships.csv")
    people_by_id = {person["id"]: person for person in people}
    for relationship in relationships:
        validate_relationship_record(relationship, people_by_id)


def test_invalid_role_raises_error() -> None:
    with pytest.raises(ValueError):
        validate_person_record({"id": "x", "name": "Virhe", "role": "other"})


def test_self_edge_raises_error() -> None:
    people_by_id = {"a": {"id": "a", "name": "A", "role": "patient"}}
    with pytest.raises(ValueError):
        validate_relationship_record(
            {"source": "a", "target": "a", "relationship": 0},
            people_by_id,
        )
