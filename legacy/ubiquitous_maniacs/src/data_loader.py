"""Backward-compatible exports for the social graph data loaders."""

from .social.data_loader import load_people_records, load_relationship_records

__all__ = ["load_people_records", "load_relationship_records"]
