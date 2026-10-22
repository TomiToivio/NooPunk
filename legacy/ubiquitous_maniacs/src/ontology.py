"""Backward-compatible exports for the social graph ontology."""

from .social.ontology import (
    ALLOWED_ROLES,
    REQUIRED_PERSON_FIELDS,
    REQUIRED_RELATIONSHIP_FIELDS,
    validate_person_record,
    validate_relationship_record,
)

__all__ = [
    "ALLOWED_ROLES",
    "REQUIRED_PERSON_FIELDS",
    "REQUIRED_RELATIONSHIP_FIELDS",
    "validate_person_record",
    "validate_relationship_record",
]
