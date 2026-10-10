# Issue #200: Creative Commons release gate and migration inventory

**Status: implementation planning, not a final legal clearance or license selection.**
The author wants NoöPunk's published rules and worldbook to be **fully Creative Commons** and to remain usable for both tabletop and computer RPGs. This document records constraints that cannot be silently waived in a later mechanics PR. It is not the final `LICENSE` file.

## Proposed publication approach

- **Preferred option to review:** CC BY-SA 4.0 for NoöPunk-original creative rulebook and worldbook writing. CC BY 4.0 remains an option if downstream permissiveness is more important than ShareAlike. Explicit author approval is required for either selection.
- **Separate software license:** evaluate MIT/Apache-2.0/GPL or another appropriate software license for runtime/code, rather than automatically applying CC to programming source. Source-code artifacts and creative prose need separate provenance records.
- **No borrowed text by default.** Independently write the core Attribute/Skill/dice model, hardware rules, PSI, combat, investigation and cybergraph procedures. Use source mechanics only where permissions clearly cover the specific material. A freely available PDF, hosted SRD or public repository is **not** by itself an open license.
- **Attribution:** acknowledge Fudge, Psi-Punk, Fate, Transhumanity's Fate, Eclipse Phase, Apocalypse World, The Veil, Cities Without Number and Stars Without Number as design inspirations, with named rights holders where confirmed. Acknowledge without implying endorsement.

## Reuse boundary: verify each component before importing

| Reference | Source license / status | Permitted route into commercially reusable CC NoöPunk |
| --- | --- | --- |
| **Fudge 1995 PDF** | Special royalty-free 1995 legal notice; not CC | Design inspiration and independently drafted mechanics; avoid copying protected text/tables |
| **Fudge later SRD** | Designated OGL 1.0a Open Game Content | Inspiration only for CC-only core unless separate CC-compatible permission; OGL is not CC |
| **Psi-Punk** | OGL 1.0a for designated portions; Product Identity excluded | Inspiration only for CC-only core unless separately authorized |
| **Fate Core official SRD** | CC BY 3.0 for licensed text; OGL alternative | Eligible adaptation with exact attribution, change notes and compatible release terms, excluding logos/art not granted |
| **Transhumanity's Fate** | CC BY-NC-SA 3.0 (2016 v1.1) | **No protected expression** in commercially reusable CC core; independent design lessons only |
| **Eclipse Phase 2e** | CC BY-NC-SA 4.0 (attached version) | **No protected expression** in commercially reusable CC core; independent system comparison only |
| **The Veil** | CC BY-SA 3.0 for text in attached edition | A compatible CC BY-SA adaptation route may be possible with attribution and ShareAlike; do not assume CC BY 4.0-only can absorb adaptations |
| **Apocalypse World** | Exact edition and applicable open grant **not verified** | Narrative design inspiration only until proven |
| **Cities Without Number** | Verify exact authorized SRD/public-domain/open-content designation separately from full book | Use only rights-cleared part or independent procedures |
| **Stars Without Number** | Verify exact authorized SRD/public-domain/open-content designation separately from full book | Use only rights-cleared part or independent procedures |

The classification refers to **copyrightable expression and licensed text/art**, not ownership of general concepts such as having attributes, skill checks, graph-based hacking or clocks. A mechanic's mathematical idea and the specific wording, arrangement, charts or fiction expressing it are different questions. When uncertain, draft original wording and commission a release-stage legal review.

## Existing prototype quarantine

The repository already documents an **Eclipse Phase 2E homebrew prototype** at
[`ECLIPSE_PHASE_HOMEBREW.md`](ECLIPSE_PHASE_HOMEBREW.md). That file explicitly says the experimental rules code and adapter may be **CC BY-NC-SA-derived**. It is **not suitable to bundle as if CC BY-SA/CC BY NoöPunk rules**.

Before any public CC release:

1. **Inventory** the EP2-derived paths and their imports, generated fixtures and adapters. Check whether any code, text, data or art is a licensed derivative. Do not assume the entire repository is clean merely because a file has no copyright header.
2. **Isolate and mark** the prototype as noncommercial/research-only pending provenance review; do not delete it unexpectedly while existing tests or agents depend on it.
3. **Reimplement independently** any required shared behavior that would otherwise pull in incompatible licensed expression; retain independent test fixtures and authored explanations of the behavior.
4. **Check distribution boundaries** so publication packaging, rulebook generation, Godot artifacts and Concordia assets do not absorb the NC content.
5. Track each reviewed component's source, version, rights clause, attribution and resolution before marking the main release CC-compatible.

## Mechanics migration contract

- Keep six separate character Attributes: `FIT / REF / INT / SOC / CYB / PSY`.
- Keep the existing Skill names, field specializations and status of trained-only/untrained, subject to textual provenance checks.
- Compare an independently implemented **Fudge/Fate-inspired Attribute + Skill resolution** against the current `STAT + Skill + 1d10` without silently switching numbers/dice in code.
- Fate-inspired aspects, narrative stakes and complications must not obscure deterministic character/equipment maths.
- Hardware `Interface / Network / Compute` are not new character attributes.
- Preserve four-domain interplay (Physical/Social/Cybernetic/Psychic) and embodied/astral/cyber-projected action legality, including the post-Singularity possibility of characters remaining offline.
- A tabletop-authored, unit-testable rules contract is authoritative; Godot and Ollama/Concordia implementations must use identical outcomes.

## Release checklist

- [ ] Select and commit a definitive CC license and document attribution policy.
- [ ] Create a **per-component** rights/provenance ledger; include author, edition, URL, governing clause, reused quantity, source portion and reason the adaptation is permitted.
- [ ] Verify Apocalypse World, Cities Without Number and Stars Without Number licensed *specific SRDs* against publisher-authored documents.
- [ ] Separate or replace all potentially NC-derived EP2 experimental material from the intended CC release distribution.
- [ ] Document whether CC BY-SA contributions may be integrated into the chosen publication model.
- [ ] Publish an independent, playtestable Fudge/Fate-inspired kernel **only after a recorded approval of the numerical migration**.
- [ ] Add checks that flag unreviewed third-party material in packaging and prevent reintroduction of explicitly excluded licenses.
- [ ] Run tabletop and digital parity tests; maintain one-game / one-rules invariants.

Related: issue #200, `AGENTS.md`, `docs/archive/DESIGN_PRINCIPLES.md`, `docs/licenses/ECLIPSE_PHASE_HOMEBREW.md`.
