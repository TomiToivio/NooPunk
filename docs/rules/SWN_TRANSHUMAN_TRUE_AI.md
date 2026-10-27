# Transhumanity and True AI: NoöPunk gameplay integration

Reference: Kevin Crawford, *Stars Without Number Revised* deluxe (2017), **Transhuman Campaigns**, printed pp. 248–265, and **True Artificial Intelligences**, printed pp. 280–289. These are the source chapters, not text licensed for republication. This document and implementation describe original NoöPunk adaptations and distinguish them from source-specific effects.

## Core design

Transhuman existence is a story about *who* survives, not just what body survives. SWN contrasts soft and hard transhuman possibilities. NoöPunk models both with `DuplicationPolicy`: soft permits at most one active agent per lineage, while hard permits active divergence. These are **scenario policies**, not claims about actual consciousness. Mind, imprint, shell and backup are distinct persistent entities. A backup never automatically merges with a surviving original.

The SWN chapter also discusses economies of abundance, reputation, artificial bodies and revival. NoöPunk should implement resource allocation and reputation as separate social/faction mechanics, not automatically assume universal post-scarcity wealth. Early Helsinki campaigns use expensive experimental shells, medical restrictions and disputed legal continuity, rather than casual ubiquitous immortality.

True AIs are distinct from ordinary automation and programmed agents. SWN's chapter includes autonomous artificial minds, physical embodiments, limiting safeguards and AI identity cores. The NoöPunk implementation tracks an independent core ID, legal personhood, autonomy rating, online/isolation/termination states, host capabilities, operational permissions and auditable brake changes. An isolated AI cannot issue actions even if the host is networked; a non-networked host cannot perform network actions. **Brake logic and its legal oversight rule are NoöPunk rulings**, not a mechanical claim about safety effectiveness in the real world.

## Python APIs

* `src/rules/swn_transhuman.py`: `Shell`, `Imprint`, `Mind`, `ContinuityRegistry`, `DuplicationPolicy`.
* `src/rules/swn_true_ai.py`: `AIHost`, `TrueAI`, `AIState`.
* `tests/test_swn_transhuman_true_ai.py`: continuity, forks, occupation conflict, isolation, host constraints, brake/permission gates and termination.

## Canon connections

* **BCI vs PSI:** A cortical link can transfer digital information but does not grant Telepathy discipline.
* **Resleeving vs duplication:** Moving a living agent to a new shell preserves the same registry ID; instantiating a backup creates a new agent, even if its memories match.
* **Rogue AGI and Blackwall:** Isolation is a controllable game state, not proof that a superintelligent entity is containable.
* **NHI vs AI:** Biological, non-human and artificial agents can have overlapping behaviors; retain provenance as a separate attribute rather than inferring it from appearance.
* **Post-crisis politics:** AI personhood, consent to copying, ownership of backups and access to life-extension technology are campaign conflicts, not decided technical facts.

## Remaining for full SWN conversion

SWN shell catalogues and statistics, body design costs, actual revival limitations, Face economy, societal policies, detailed true-AI PC advancement, cognition actions, AI core physics, Godot adapters and campaign UI remain to be implemented. Any such additions should be independently checked against the source, expressed in original NoöPunk language, and tested. Do not upload the source PDF or its protected explanatory prose.
