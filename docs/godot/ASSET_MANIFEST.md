# Asset manifest — Godot slice (#631)

> **Superseded for the shopping decision by [`ASSETS.md`](ASSETS.md)** — that file now carries the
> free and paid packs with verified licences and the machine-readable list in
> `data/assets/manifest.json`. This page is kept because it records the *placeholder* asset
> decision of the first slice (primitives only, nothing third-party committed).

**Nothing third-party is committed in this slice.** Every visible object is a `BoxMesh`, `CapsuleMesh` or
`Label3D` created by `godot/scenes/level_builder.gd`, with flat `StandardMaterial3D` colours. That is a
deliberate choice for the first milestone: a playable case with placeholder art is reviewable, whereas a
licence problem in the repository is not.

## Researched shortlist

See [the 2026-10-26 asset shortlist](ASSET_SHORTLIST_2026-10-26.md) for specific free/CC0 art,
MIT dialogue tools, conditional paid voxel packs, observed prices and an isometric art-test proposal.
These are sourcing candidates only; none has been imported or added to this shipped manifest.

## Intended sources for the next milestone

Listed because the issue names them; **none is used yet**, and each must be checked per pack before use.

| Source | What it is good for here | Licence to verify per pack |
| --- | --- | --- |
| [Kenney](https://kenney.nl/assets) | modular hospital and office kits, props, UI | CC0 for most packs; the asset page states the licence per pack |
| [Quaternius](https://quaternius.com/) | low-poly characters and furniture | CC0 for most packs; check the individual page |
| [Poly Haven](https://polyhaven.com/) | HDRIs, textures, some models | CC0 |
| [Synty](https://syntystore.com/) | commercial low-poly environments | **purchased licence; never commit to this public repository** |

## Checklist before any asset is added

1. **Read the pack's own licence file**, not a marketplace summary. Record: licence name, version,
   redistribution allowed (yes/no), attribution required (yes/no), commercial use, modification.
2. **Record the provenance** in this manifest: pack name, source URL, licence, date downloaded, who
   verified it, and the exact files added.
3. **Purchased assets stay out of this repository.** Synty and similar licences generally forbid
   redistribution; keep them in a local `godot/assets_private/` (git-ignored) and document how a
   developer obtains them.
4. **CC0 attribution is optional but recorded anyway**, so a later relicensing review is a grep, not an
   archaeology project.
5. **Formats:** prefer `.glb` for models and `.png`/`.webp` for textures; keep source `.blend`/`.psd`
   files out unless the licence explicitly covers redistribution of sources.
6. **Import settings are code**, too: commit `.import` files for anything shipped, so the build is
   reproducible.
7. **No assets from a copyrighted game or film**, and no AI-generated models whose training provenance
   is unclear.

## What the current slice contains instead

| Node | Geometry | Where it comes from |
| --- | --- | --- |
| Floors, ceilings, walls | `BoxMesh` with `StandardMaterial3D` | `level_builder.gd::_build_rooms`, `_build_walls` |
| Props (terminal, cabinet, desk) | `BoxMesh` + `BoxShape3D` | `level_builder.gd::_build_props` |
| NPCs (doctor, nurse, patient) | `CapsuleMesh` + `CapsuleShape3D` + `Label3D` name | `level_builder.gd::_build_npcs` |
| HUD | Godot controls built in `hud.gd` | no textures, theme defaults |

Fonts are Godot's built-in default, which ships with the engine and needs no attribution.

## Licence of this repository's own content

Unchanged by this slice: the repository's own code and text remain under the project's existing terms
(see `docs/ATTRIBUTION_POLICY.md` and the repository licence). This manifest grants nothing and changes
nothing; it records what is inside the build.
