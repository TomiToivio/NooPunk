# NoöPunk Godot: isometric art direction and asset procurement shortlist (2026-10-26)

## Creative direction

**Target:** a predominantly narrative detective RPG with an orthographic/near-isometric 3D camera, chunky low-poly/voxel-inspired models, modest texture resolution, crisp readable silhouettes and restrained lighting. References: Cloudpunk (urban mood), Shadows of Doubt (investigation and interior density), Shadowrun: Dragonfall (tactical encounters), Disco Elysium and Citizen Sleeper (dialogue, choices and consequences). Reference the *principles*, not copyrighted art.

**Setting treatment:** recognisable Nordic hospitals, municipal offices, apartment buildings and wet streets first; subtle uncanny anomalies and modest cybernetic intrusions second. One muted everyday scene should remain legible without neon. The present first-person playable slice is a working baseline, not something to delete.

**Gameplay balance (initial hypothesis):** 60% investigation/dialogue, 25% exploration, 15% tactical encounters; flexible by scenario. Dialogue and evidence checks use the existing WN adapter; do not duplicate mechanics in presentation scripts. Tactical encounters, when built, should be optional where narrative alternatives are credible.

**Camera prototype:** try a Godot Camera3D with orthographic projection, 35–45° downward pitch and approximately 45° horizontal yaw; click-to-move *or* WASD as an accessibility option, smooth wall/roof fade, clearly labeled interactables and dialogue UI independent of scene scale. Compare fixed camera vs rotating camera. This is a proposal; usability must be tested.

## Free / libre candidates

| Asset | URL | Use | License / distribution action |
| --- | --- | --- | --- |
| Quaternius Downtown City MegaKit (free Standard subset) | https://quaternius.com/packs/downtowncitymegakit.html | contemporary street blocks, background buildings | Pack lists CC0; free tier is ~60–70%, Godot engine project in paid Source tier. Record exact downloaded version |
| Quaternius Universal Base Characters | https://quaternius.com/ | NPC proxy meshes and rig pipeline | Older pack pages list CC0; **check exact pack and Quaternius' newer licensing before downloading** |
| Quaternius Universal Animation Library | https://quaternius.com/ | ambulatory NPC animation experiments | Verify exact release and licence; retarget test |
| KayKit Dungeon Pack FREE | https://kaylousberg.itch.io/kaykit-dungeon-pack | modular wall/door/furniture prototype, not final hospital art | Free tier explicitly CC0; glTF supported |
| Kenney asset catalogue | https://kenney.nl/assets | UI, generic props, prototyping geometry | Verify license on the *selected* pack; many are CC0 |
| Poly Haven | https://polyhaven.com/ | HDRI and surface textures | CC0 library; retain provenance |
| ambientCG | https://ambientcg.com/ | asphalt, concrete, laminate and wall textures | Check selected download's CC0 notice |
| OpenGameArt isometric CC0 collection | https://opengameart.org/content/cc0-isometric | concepts and 2D testing | Collection metadata is NOT a substitute for validating each contributor and pack |
| Godot Dialogic 2 | https://github.com/dialogic-godot/dialogic | optional dialogue editor assessment | MIT project; assess compatibility and whether integration helps existing JSON dialogue first |
| Godot Phantom Camera | https://github.com/ramokz/phantom-camera | optional camera transitions | Check current license, Godot compatibility, and whether a lightweight native Camera3D is simpler |

**Free does not imply redistributable.** For example, https://reodesuxz.itch.io/free-pixel-cyberpunk-city-tileset-16x16 allows free commercial use but forbids standalone file redistribution: evaluate only as a local/private example pending explicit repo distribution permission. Do not automatically vendor.

## Paid candidates for later (NOT purchased)

| Priority | Asset | URL | Published tier price observed 2026-10-26 | Strength | Caution |
| --- | --- | --- | --- | --- | --- |
| 1, art-study candidate | monogon Voxel Cyberpunk City | https://maxparata.itch.io/cyberpunkcity-monogon | €12.95 base / €30 source / €49.90 dev | distinctly voxel / isometric streets and buildings | Listing says CC BY-ND 4.0. Derivatives, repacking, public source redistribution and Godot optimization need written clarification before integration |
| 1, art-study candidate | monogon Voxel Cyberpunk Buildings | https://maxparata.itch.io/voxelcyberpunkbuildings | €19.95 starter / €30 source / €49.90 dev | building silhouettes for city-level sets | Verify purchase agreement and exact license; do not commit samples |
| 2 | monogon Voxel Cyberpunk Streets | https://maxparata.itch.io/voxelcyberpunkstreet | €16.95 base / €30 source / €59.95 dev | dense street and road geometry | Check license, performance and compatibility |
| 2 | Synty POLYGON Sci-Fi City | https://syntystore.com/products/polygon-sci-fi-city | $49.99 USD | coherent modular environment, NPCs and vehicles, Godot 4.6.2+ support listed | Commercial licence; do not check purchased source packs into public GitHub |
| 3 | Synty POLYGON City | https://syntystore.com/collections/godot-asset-packs | $19.99 USD listed | more ordinary real-world city assets and props | Confirm exact Godot release and terms prior to purchase |
| 3, alternate 2D | monogon Isometric Cyberpunk City | https://maxparata.itch.io/isocyberpunkcity-monogon | €9.95 | 400+ sprites, rapid 2D mockup | CC BY-ND 4.0 listed; not a direct replacement for 3D 360° camera |
| 3, optional | monogon Voxel Cyberpunk Bundle | https://maxparata.itch.io/cyberpunkcity-monogon | €189.90 advertised bundle | breadth if the style is chosen | Do not buy until licensing and art pipeline are proven |

Prices are snapshots in merchants' listed currencies, not invoices or purchase commitments; taxes/discounts can change.

## Licensing gate

For every downloaded candidate record publisher, source URL, exact variant, download date, file manifest, license text/link, redistributability, modification rights, attribution and export formats. Keep paid files out of public Git and in gitignored local folders where permitted. Do not assume CC BY-ND permits modifying art or distributing modified source assets. Do not redistribute restricted free samples. Never use recognizable Cloudpunk, Shadows of Doubt or other game screenshots as in-game assets.

## Implement next

1. Keep the existing Godot 4.7.2 hospital slice working; baseline headless suites must still pass.
2. Add an **optional** isometric exploration camera/controller, switchable from the existing first-person route, with no duplication of story or game-state code. Preserve FPS as a debug mode.
3. Prototype one hospital reception/consultation room using existing primitives, then a strictly validated CC0 kit. Add roof/wall fade, outline/hit targets, character occlusion, readable journal/dialogue at 1080p and 720p.
4. Write an import test for glTF scale/orientation, collision, materials and atlas handling. Add screenshots and frame-time measurements across camera modes.
5. After proof of style, commission/create distinctive Finnish municipal and psychiatric-hospital assets and restrained uncanny props, rather than turning a pack into the whole identity.
6. Make tactical turn-based combat a later separate test scene using existing WN rules. No combat implementation is necessary to approve the narrative art milestone.

**Decision gate:** compare screenshots, FPS and usability in a low-neon daylight hospital scene, a rainy urban evening and a quiet anomalous scene. If voxel assets cannot support close indoor investigation, use mixed low-poly 3D with voxel-inspired pixelated materials instead.
