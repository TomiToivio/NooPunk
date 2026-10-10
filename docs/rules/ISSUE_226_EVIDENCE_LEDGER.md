# #226: UNSA investigation evidence ledger, first playable increment

**Status:** first deterministic, engine-neutral procedure; not a complete police procedural, not legal advice, and not a final die mechanic. This does not change Fudge/Fate core resolution or override UNSA/world canon.

An investigation needs an auditable answer to **who found what, where, and who handled it afterwards**. Every discovered object, interview record, electronic trace or anomalous psychic impression receives a unique evidence ID, a collector, a location and a case/session key. The source type is one of physical, digital, testimony, PSI lead or other.

At the table, write an index card per item. When somebody collects it, transfers it to a specialist, analyzes it, seals it or questions it, append a chronological event rather than editing the earlier record. To hand over custody the recorded current custodian must make the transfer, which names the new custodian. Analyses and sealing also require the current custodian. Questioning can instead record contradictions and challenges. This is a *bookkeeping guard*, not a ruling that off-book actions are physically impossible: such events should be represented as disputed/broken-chain case narrative, with GM adjudication, rather than falsely certified transfers.

**PSI leads are not proof.** A psychometric vision or telepathic impression may point investigators toward a witness or location, but is never automatically transformed into objective forensic evidence. The game should seek independent verification and preserve provenance. The `lead_only()` check allows an LLM GM to gate claims without asserting the psychic impression was proven.

**Computer runtime:** `src/rules/investigation_evidence.py` holds independent code with append-only immutable custody events. `EvidenceLedger.export()` provides a stable JSON-friendly event history for Godot/Concordia/Ollama to inspect. LLMs may suggest questioning or lead text but must not rewrite history or impersonate a custodian. Case clocks, warrants, admissibility and penalties are not invented by this first slice.

**Existing chapter ownership:** #226 owns the substantive investigation procedure; #220 owns social dialogue/contacts; #230 owns scenario generation; #232 owns compiled rulebook navigation. Do not fork core roll/AP rules into these files. The current root `RULEBOOK.md` remains the authority until the segmented cutover is approved.

**Next sections:** explicit jurisdiction and warrant scenarios, contested chain-of-custody/forgery, no single-roll clue locks, false-positive forensic/PSI leads, forensic AI trust boundaries, NHI diplomatic procedure and an introductory UNSA case.

Test: `python -m unittest discover -s tests -p 'test_issue226_evidence_ledger.py'`.
