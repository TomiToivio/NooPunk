# Godot assets: open-source and commercial (#728)

**Survey only. Nothing purchased, nothing imported.** Licence statements are what each source
says on 2026-10-28 and must be re-read at download time; a store page is not a licence.

## 1. Free / open — verified live

| asset | licence | use in the slice | link status |
|---|---|---|---|
| **Industrial Cyberpunk 3D Tilepack** (slipperhat) | **CC0** — commercial use, no attribution required | modular industrial props; documents a **Godot ORM workflow** | 200 |
| **KayKit / Kay Lousberg packs** | **CC0** | characters and props, low-poly, single atlas | 200 |
| **Kenney asset packs** | **CC0** | UI kits, audio, prototype props — best breadth per hour | 200 |
| **Quaternius** | **CC0** | low-poly buildings, vehicles, nature | 200 |
| **Poly Pizza** | CC0 / CC-BY mix — **check per model** | quick one-off props | 200 |
| **MagicaVoxel** (tool) | free | authoring the voxel look ourselves | 200 |
| **Godot Asset Library** | varies per asset | addons, shaders, camera rigs | 200 |
| **OpenGameArt** | varies (CC0 / CC-BY / CC-BY-SA) | textures, audio, fonts — **check per file** | 200 |
| **Freesound** | varies (CC0 / CC-BY / **BY-NC**) | ambience, foley — **NC files are forbidden** for Vasama | 200 |
| **Google Fonts** | SIL OFL | UI and body text; **verify Finnish diacritics** (ä, ö) before committing | 200 |

**The trap in the free list:** Freesound and OpenGameArt mix CC0 with **CC-BY-NC**. A single NC
sound in a commercial build is a licensing defect. Every downloaded file needs its licence
recorded next to it.

## 2. Commercial — to price later, not now

| vendor | what | typical price | licence model | Godot caveat |
|---|---|---|---|---|
| **Synty POLYGON** | modular cyberpunk/science-fiction kits | $20–$300 per pack; bundles ~$25 on Humble historically | perpetual, royalty-free, **5 seats** | Unity-first pipeline: **animations need rework** in Godot |
| **Sonniss GDC audio bundles** | multi-GB royalty-free SFX/music | free (annual bundle) | royalty-free, per bundle terms | site returns **403** to scripted requests; fetch in a browser |
| **itch.io premium packs** | bespoke cyberpunk kits | $5–$60 | varies — **read each** | quality varies wildly |
| **Fab / Unity Asset Store** | large catalogues | varies | Unity-centric licences | conversion cost often exceeds the price |

**Do not buy yet.** The art direction question — 2D isometric vs voxel vs low-poly 3D — is still
open (#724 §7), and the three have incompatible pipelines. Buying before that decision is how a
project owns a pack it never opens.

## 3. What the slice actually needs, and the cheapest way to get it

| need | cheapest adequate source |
|---|---|
| four hospital rooms | **slipperhat CC0** modular kit + **MagicaVoxel** for bespoke furniture |
| ~30 props | Kenney + Quaternius CC0, recoloured to the palette |
| 6 characters | KayKit CC0 low-poly humans; portraits are 2D art, not models |
| UI (case board, dialogue, network graph) | **Kenney UI pack (CC0)** + custom shader for the neon frame |
| ambience (fluorescent hum, rain, corridor) | Freesound **CC0 only**, licence recorded per file |
| fonts | Google Fonts OFL, Finnish glyphs verified |

**Total cash cost of the slice: €0.** Every element above has a CC0 path. Paid assets become
worth considering only when the art direction is settled and the slice proves the loop.

## 4. Licensing rules the build must respect

1. **A store licence is not a repository licence.** Paid assets never enter the public repo;
   they live outside git behind a manifest — the same rule the Ubiquitous Maniacs corpus follows.
2. **NC is forbidden** in anything that could ship commercially (Vasama). This includes
   Freesound NC files and all Eclipse Phase text (CC BY-NC-SA).
3. **Attribution is collected as files arrive**, not reconstructed later. Every imported asset
   gets an entry in `NOTICE` with source, licence and URL.
4. **CC0 still gets credited** — it is not required, and it is the decent thing, and it protects
   against a later provenance question.

## 5. Recommended order

1. Build the slice with **CC0 only** (proves the loop at zero cost).
2. Settle the art direction with the slice in hand.
3. Only then evaluate Synty or an itch premium kit, against a specific unmet need.
