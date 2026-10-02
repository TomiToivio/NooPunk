"""Unified NoöPunk tag engine (issue #51 prototype).

Attributes are tags: there is no separate attribute subsystem beneath the tag
system, which is the issue's central constraint. See :mod:`tags.model` for the
rules about what is canonical and what is a non-canonical prototype.
"""

from .model import (
    CANONICALITY_NOTE,
    HUMAN_ATTRIBUTE_MAX,
    HUMAN_ATTRIBUTE_MIN,
    PROTOTYPE_ATTRIBUTE_SYSTEMS,
    PROTOTYPE_ATTRIBUTES,
    SYSTEMS,
    TAG_RATING_MAX,
    TAG_RATING_MIN,
    Category,
    Entity,
    Source,
    System,
    SystemPresence,
    Tag,
    TagError,
    attribute_tag,
)
from .resolve import (
    STACK_CAP_DEFAULT,
    AppliedTag,
    Outcome,
    Stack,
    StackingError,
    build_stack,
    resolve_action,
    sample_entities,
)

__all__ = [
    "CANONICALITY_NOTE",
    "HUMAN_ATTRIBUTE_MAX",
    "HUMAN_ATTRIBUTE_MIN",
    "PROTOTYPE_ATTRIBUTES",
    "PROTOTYPE_ATTRIBUTE_SYSTEMS",
    "STACK_CAP_DEFAULT",
    "SYSTEMS",
    "TAG_RATING_MAX",
    "TAG_RATING_MIN",
    "AppliedTag",
    "Category",
    "Entity",
    "Outcome",
    "Source",
    "Stack",
    "StackingError",
    "System",
    "SystemPresence",
    "Tag",
    "TagError",
    "attribute_tag",
    "build_stack",
    "resolve_action",
    "sample_entities",
]
