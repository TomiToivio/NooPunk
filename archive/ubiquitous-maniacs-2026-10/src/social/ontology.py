from __future__ import annotations


REQUIRED_PERSON_FIELDS = ("id", "name", "role")
REQUIRED_RELATIONSHIP_FIELDS = ("source", "target", "relationship")
ALLOWED_ROLES = {"patient", "staff", "ai"}


def validate_person_record(person: dict[str, object]) -> None:
    missing = [field for field in REQUIRED_PERSON_FIELDS if field not in person or person[field] in ("", None)]
    if missing:
        raise ValueError(f"Henkilötiedosta puuttuu pakollisia kenttiä: {missing}")

    role = str(person["role"])
    if role not in ALLOWED_ROLES:
        raise ValueError(f"Tuntematon henkilön rooli: {role}")


def validate_relationship_record(
    relationship: dict[str, object],
    people_by_id: dict[str, dict[str, object]],
) -> None:
    missing = [
        field
        for field in REQUIRED_RELATIONSHIP_FIELDS
        if field not in relationship or relationship[field] in ("", None)
    ]
    if missing:
        raise ValueError(f"Suhdetiedosta puuttuu pakollisia kenttiä: {missing}")

    source = str(relationship["source"])
    target = str(relationship["target"])
    if source not in people_by_id:
        raise ValueError(f"Tuntematon lähdehenkilö: {source}")
    if target not in people_by_id:
        raise ValueError(f"Tuntematon kohdehenkilö: {target}")
    if source == target:
        raise ValueError("Henkilöllä ei saa olla suhdetta itseensä.")

    try:
        int(relationship["relationship"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Suhteen arvon tulee olla kokonaisluku: {relationship}") from exc
