# LaclauGPT Data Storage — Noöpunk import

Imported from `LaclauGPT-Data-Storage/noöpunk` on 2026-08-05.

These files are reference material, not automatically authoritative Noöpunk canon. They were kept together so useful ideas can be incorporated selectively without overwriting the newer Finnish documents in `noöpunk/` and `noopunk_ubiquitous_maniacs/`.

The integration has been implemented through reviewed Finnish documents under `noopunk_ubiquitous_maniacs/docs/`. See `INTEGRATION_PLAN.md` for the roadmap and `noopunk_ubiquitous_maniacs/docs/IMPORT_CONFLICT_LEDGER.md` for the final accept/adapt/hold/reject decisions.

## Contents

- `CAMPAIGN.md` — 2026–2049 campaign progression and six-act structure.
- `HELSINKI.md` — Europol/NHI Helsinki disappearances campaign.
- `NHI_FACTIONS.md` — NHI and interdimensional faction notes.
- `NHI_SINGULARITY.md` — disclosure crisis, Singularity, and 2049 geopolitics.
- `NOÖPUNK.md` — early high-level setting synthesis and influences.
- `QIP.md` — quantum information panpsychism, consciousness, and psionics.
- `RULES.md` — early English game mechanics and tarot resolution system.
- `TAROT.md` — Noöpunk-themed major arcana concepts.
- `WORLD.md` — early worldbuilding overview; imported source version dated 2026-08-05.

## Recommended reuse

The strongest candidates for selective integration are:

1. `HELSINKI.md` for scenarios and campaign structure.
2. `CAMPAIGN.md` and `NHI_SINGULARITY.md` for timeline material.
3. `NHI_FACTIONS.md` for faction design.
4. `QIP.md` for comparison with the current `GLOCAL.md`, `PSIONICS.md`, and `PHENOMENOLOGY.md` framework.
5. `RULES.md` and `TAROT.md` as optional mechanics, after reconciling them with the current `RULEBOOK.md`.

Do not merge claims or dates into current canon without checking them against the newer documents. In particular, the imported rules and world files differ from the versions already stored under `obsolete/`.

## Implemented integration (selective porting)

The LaclauGPT → Noöpunk integration ports **mechanics and one campaign frame**, not canon. The implemented artifacts live outside this reference directory:

- **Helsinki campaign frame** — `data/rpg/campaigns/helsinki/` (locations, characters, four phase scenarios). Ported from `HELSINKI.md` as a standalone 2026 frame using B's 4dF mechanics; A's CP-RED `STAT+Skill+1d10`/DV stats were **not** ported. Phase 3/4 revelation checks use B's Tarot alternative resolver (`resolver: "tarot"`).
- **NHI factions (contested)** — `data/rpg/factions/nhi_factions.json` carries Watchers and Architects from `NHI_SINGULARITY.md`, each flagged `canon: "contested"`. Per B's `NHI_ONTOLOGY.md` / `MYSTERY_AND_TIMELINE_SUPERPOSITION.md`, NHI nature/history must not collapse into one definitive timeline; these factions are **one in-world interpretation, not authoritative canon**.
- **Tarot resolution, QIP psi-escalation, populism lens** — see `src/rpg/tarot.py`, `src/rpg/psi.py`, `src/political/populism_analysis.py`. A's `RULES.md`/`TAROT.md`/`QIP.md` concepts are ported as 4dF-tiered effects on B's existing resolver, not as A's stat system.

These docs remain human-readable reference only; no runtime code reads this directory.
