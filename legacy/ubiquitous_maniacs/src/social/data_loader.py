from __future__ import annotations

from pathlib import Path

import pandas as pd

from .ontology import REQUIRED_PERSON_FIELDS, REQUIRED_RELATIONSHIP_FIELDS


def _load_csv_records(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(f"Puuttuva datatiedosto: {path}")
    dataframe = pd.read_csv(path)
    dataframe = dataframe.where(pd.notnull(dataframe), None)
    return dataframe.to_dict(orient="records")


def load_people_records(path: Path) -> list[dict[str, object]]:
    records = _load_csv_records(path)
    for record in records:
        missing = [field for field in REQUIRED_PERSON_FIELDS if field not in record]
        if missing:
            raise ValueError(f"Henkilötiedostosta puuttuu pakollisia sarakkeita: {missing}")
    return records


def load_relationship_records(path: Path) -> list[dict[str, object]]:
    records = _load_csv_records(path)
    for record in records:
        missing = [field for field in REQUIRED_RELATIONSHIP_FIELDS if field not in record]
        if missing:
            raise ValueError(f"Suhdetiedostosta puuttuu pakollisia sarakkeita: {missing}")
    return records
