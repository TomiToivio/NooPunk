# Issue #228: source-linked light equipment catalog

This first step indexes the **existing authored equipment descriptions** rather than constructing speculative gear statistics. The source of truth remains `rulebook/13_EQUIPMENT.md` and the quick-reference `rulebook/9_FIELD_CATALOGS.md`; the index is derived at read time and is not a competing equipment book.

Run `python -m src.rules.equipment_catalog_index` to print machine-readable JSON, or call `search_catalog("forensic")` to find existing entries with their **original source path, line number and chapter**. The index extracts only recognized, explicitly written Markdown table rows or bold catalog bullets. It intentionally excludes unstructured text and cannot claim that its search results include *all* gear in the narrative.

The record contains item names and existing light descriptions with provenance only, **no damage, price, equipment rating, cyber bonus, manufacturer or economy**. Thus it is suitable for a Concordia/Ollama GM as a constrained retrieval source without silently letting the model invent mechanical values; a later approved equipment schema can add validated optional ratings after #217 core resolution and #219/#221 interfaces are settled.

**Parallel-agent boundaries:** #228 handles equipment inventory and machine-readable provenance, #219 physical damage and combat, #221 cyber hardware properties, #223 psychotronics, #226 evidence procedure, and #232 book assembly. Existing UNSA equipment capabilities remain in `data/rules/unsa_academy.json`. A device can appear in more than one authored source; duplicate citations should remain visible rather than being silently collapsed.

The extractor is independently written project code and reuses only existing NoöPunk repo text. Final publication and code licensing remain gated by #231. No third-party RPG expression is introduced in this change.

Tests: `python -m unittest discover -s tests -p 'test_issue228_equipment_catalog_index.py'`.
