# Godot asset shortlist — isometric voxel detective RPG

> **Summary view: [`ASSETS.md`](ASSETS.md).** This page stays as the long-form per-pack detail
> (import notes, triangle counts, tier prices) that the summary condenses; where they disagree,
> the licence text on the vendor's own page wins.

Researched 2026-10-26. Scope: the legacy NoöPunk RPG / Godot front end, not the strategy crossover.
This is a sourcing and presentation proposal, not a change to rules or setting canon.
No packs purchased, downloaded, imported, or tested in Godot during this research.

## Recommended direction

Build a small 3D environment viewed through an orthographic/isometric camera, with blocky silhouettes,
restrained textures and readable interaction markers. Use Cloudpunk / Shadows of Doubt as voxel and
urban atmosphere references; Shadowrun: Dragonfall for spatial readability and eventual turn-based
encounters; Disco Elysium / Citizen Sleeper for conversations, portraits, evidence and consequential
choices. These are references, not sources of reusable assets.

Start with the existing hospital case and a small street test scene. Keep recognizable institutional
furniture and architecture prominent; selective cyberpunk props will fit the grounded direction better
than filling every room with neon. A coherent palette and consistent model scale matter more than pack size.

Current repository baseline: docs/godot/README.md describes Godot 4.7.2, the Compatibility renderer,
first-person WASD/mouse controls, primitive geometry, a JSON dialogue runner and one GameState save.
Isometric movement, camera occlusion and asset integration are future work, not existing features.
Do not replace the working case or its rules adapter just to adopt an asset pack.

## Free reusable art — first prototype

Licences below are stated on the linked publisher pages. Before importing, inspect the downloaded
pack's licence and record actual filenames in [ASSET_MANIFEST.md](ASSET_MANIFEST.md).
CC0 art is freely reusable content; it is distinct from an open-source software addon.

| Asset / official source | Price / page licence | Best use | Godot route / limitations | Priority |
| --- | --- | --- | --- | --- |
| [Kenney Furniture Kit](https://kenney.nl/assets/furniture-kit) | Free, CC0; 140 assets | Reception desks, chairs, beds, institutional offices | 3D pack; exact archive formats still to inspect. Convert to GLB if needed. Ordinary furniture is not a complete medical equipment kit. | First |
| [Kenney City Kit (Commercial)](https://kenney.nl/assets/city-kit-commercial) | Free, CC0; 50 assets reported by official search result | Street block and exterior massing | Low-poly 3D, not voxel. Archive formats and interiors not verified. Full-page retrieval was rate-limited; licence/count evidence is the official-page search excerpt. | First exterior |
| [Quaternius Ultimate Animated Character Pack](https://quaternius.com/packs/ultimatedanimatedcharacter.html) | Free, CC0; 52 models | NPC stand-ins and animation experiments | FBX, OBJ, Blend. Use FBX or Blender-to-GLB for animation; OBJ does not carry rigs/animation. Character style needs harmonizing. | First NPCs |
| [Quaternius Cyberpunk Game Kit](https://quaternius.com/packs/cyberpunkgamekit.html) | Free, CC0; 71 models | Selective machinery, modular pieces, cyberpunk accents | glTF, FBX, OBJ, Blend; includes animated content. Action/platformer-oriented content is less useful than ordinary furniture for the hospital. | Second |
| [Kenney UI Pack](https://kenney.nl/assets/ui-pack) | Free, CC0; 430 assets | Buttons, panels, journal/evidence UI prototypes | 2D assets; inspect archive formats and use through Godot Controls/themes. Rework visual styling for a restrained detective interface. | First UI |
| [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds) | Free, CC0; 100 sounds | Journal, terminal and menu feedback | Audio pack; inspect actual encoding on download. This does not supply hospital/urban ambience. | First audio |

**Free starting set:** Furniture Kit + animated characters + UI Pack + Interface Sounds. Add City Kit
for one street, then only the Cyberpunk Game Kit pieces that fit. These are compatible starting
materials, not a pre-matched art direction.

## Free voxel samples — useful to evaluate, not cleared for public inclusion

| Asset | What is actually free | Fit and constraints |
| --- | --- | --- |
| [monogon Voxel Cyberpunk City](https://maxparata.itch.io/cyberpunkcity-monogon) | FreeSample.zip; complete packs are paid | Closest stylistic match. Page lists CC BY-ND 4.0. Use sample to assess scale and import workload; resolve modification/distribution terms before integration. |
| [monogon Voxel City](https://maxparata.itch.io/voxelcity) | Selected-prop sample | Stronger everyday-city complement to neon environments; also lists CC BY-ND 4.0. |
| [monogon Free Voxel Dystopian Characters](https://maxparata.itch.io/voxel-dystopian-characters) | Free/name-your-price character downloads | Page permits commercial/noncommercial projects and supplies VOX, PNG palette, OBJ/MTL, GIF. This research did not establish complete modification/source-redistribution terms. Do not label CC0 or assume animation/rigging from a rotating GIF. |

The paid city pages explicitly display **Creative Commons Attribution–NoDerivatives 4.0** while also
offering editable VOX files and broad game-use language. Treat that as a sourcing ambiguity:
obtain written clarification covering recolouring, mesh edits, optimization and distribution of
adapted assets in a game before choosing them as the production base. Do not assume buying the
Source tier resolves it. Preserve attribution and the supplied licence. No contact has been sent.

## Paid wishlist — purchase later

Prices observed on 2026-10-26, not quotes. Itch pages mix dollar labels in descriptive tables with EUR
download thresholds; EUR amounts below use the download section where available. Recheck currency,
tax, tier contents and licence at purchase. No purchases are authorized or performed by this document.

| Rank / asset | Observed price / tier | What it contributes | Integration and purchase condition |
| --- | --- | --- | --- |
| A — [monogon Voxel Cyberpunk City](https://maxparata.itch.io/cyberpunkcity-monogon) | Base €12.95; Source €30; Dev €49.90 | 39 building modules, 6 complete buildings, 56 props, 17 billboards, 14 road modules, 1 rigged character | Best voxel/cyberpunk fit. Source adds VOX; Dev adds Unity prefabs/optimized geometry, not a verified native Godot project. Base mesh formats still need inspection. Hold pending ND clarification and sample import. |
| A — [monogon Voxel Noir Crime Detective](https://maxparata.itch.io/voxelnoir) | Descriptive table: Base $12.95; Source $30; Dev $39.90; verify checkout currency | 30 buildings, 60 building modules, 1 vehicle, 1 character, 6 props, 3 ground tiles | Particularly relevant detective/urban palette; not a furnished hospital. Source adds VOX; Dev describes Unity package. Same CC BY-ND clarification needed. |
| B — [monogon Voxel City](https://maxparata.itch.io/voxelcity) | Descriptive table: Starter $15.95; Source $30; Dev $49.90; verify checkout currency | 146 items including transit, ambulance, street furniture, vehicles and buildings | Good grounded city complement. Starter explicitly has unoptimized OBJ/textures; Dev adds optimized FBX/atlas and Unity package. Same ND issue; validate triangle counts before selection. |
| B — [Synty POLYGON Sci-Fi City](https://syntystore.com/products/polygon-sci-fi-city) | $49.99 USD listed | 509 unique assets, 20 characters, urban modules, vehicles and props | Publisher lists Godot 4.6.2 project / 4.6.2+ compatibility plus FBX sources. Low-poly alternative, not voxel. Characters have no animations included. Check Compatibility-renderer appearance and the purchased licence; keep paid assets private under repo policy. |

**Buying order:** evaluate free voxel samples first. If the modification terms are clarified, compare
Cyberpunk City and Noir in the same small scene and buy only the better-fitting base pack initially.
If those terms do not meet the project needs, remain with CC0 assets or evaluate Synty's native Godot
pack as an alternative visual direction. Do not buy several inconsistent styles or a large bundle
before the art test. Source tiers only help if editing rights are clear; Unity Dev tiers are not
automatically worth the premium for Godot.

## Open-source Godot tools for narrative gameplay

| Tool | Licence / advertised version | Fit | Recommendation |
| --- | --- | --- | --- |
| [Dialogue Manager](https://github.com/nathanhoad/godot_dialogue_manager) | MIT; current README describes v4 for Godot 4.6+ | Script-like branching conversations, conditions, stateless runtime | First tool to evaluate if the current JSON authoring becomes cumbersome. Keep GameState and rules_adapter authoritative; dialogue requests checks instead of defining mechanics. |
| [Dialogic 2](https://github.com/dialogic-godot/dialogic) | MIT; current README requires Godot 4.5+ | Visual dialogue/timeline authoring, portraits and character management | Alternative when visual authoring/portrait presentation matters more. Review release maturity and save integration. Example fonts have separate notices. |

Do not install both. The current dialogue runner already works; compare one existing conversation,
conditional evidence response and save/resume path before any migration. Retain MIT notices and pin
the chosen addon version. Version-range compatibility is not a tested integration claim.

Turn-based combat templates are not recommended as a rules foundation: NoöPunk already has the
Without Number adapter, and a generic template would introduce another state/rules system.
Use spatial presentation inspiration without importing Shadowrun mechanics or Citizen Sleeper dice rules.

## Next implementation proposal

1. Make a separate isometric art-test scene using the free set: a reception desk, corridor, NPC and
   one street frontage. Reuse existing case interactions and evidence identifiers.
2. Establish orthographic camera framing and comfortable text size. Test wall/roof cutaway or fading,
   click targets and keyboard navigation before building a large map.
3. Normalize metres, floor pivots, palette, roughness and texel/voxel scale. Keep painterly dialogue
   portraits as a later, separately commissioned/original art layer if desired; no portrait pack was
   verified in this search.
4. Preserve the existing renderer initially. Compare lighting, emission and shadows in the actual
   Compatibility build; marketplace screenshots are not performance or appearance guarantees.
5. Check collisions, door clearance, animation scale, material counts and mesh density. Keep low-cost
   collision shapes separate from visual meshes.
6. Only after the visual test, choose a single production style and reconsider the conditional wishlist.
   Tactical encounters remain a later layer behind the existing rules adapter.

For the import pipeline, [Godot's official format documentation](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
recommends glTF 2.0 / GLB, supports FBX through ufbx, and notes OBJ's lack of skeletons, animations and
pivots. Direct Blend import needs Blender installed. VOX is an authoring format here: plan an explicit
mesh export/conversion step rather than treating it as a native Godot scene.

## Provenance and verification

Research uses official creator pages, official addon repositories and Godot documentation linked
in each row. Listings may be cached and prices can change. No download licence files or imported
models have been inspected; all entries are **candidates**, not the shipped manifest.

Before adding files, record creator, URL, downloaded version/date, exact licence text, attribution,
modifications and file paths in ASSET_MANIFEST.md. Preserve public placeholders. Purchased assets
stay outside public Git under the existing manifest policy.

Reviewed project instructions: AGENTS.md (including its current author override), docs/godot/README.md
and docs/godot/ASSET_MANIFEST.md. This documentation-only research adds no rules, runtime dependencies
or prose tests. No game tests were run because executable code is unchanged.

Remaining gaps: verified modular medical equipment, a coherent voxel civilian rig/animation set,
original detective portraits, hospital ambience and Helsinki-specific architecture. The shortlist
does not pretend these are solved by a generic cyberpunk city pack.
