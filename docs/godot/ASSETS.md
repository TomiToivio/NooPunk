# Art and audio assets for the NoöPunk detective RPG (#631)

**Status: research note. No asset is approved, imported or purchased.** Every licence line below was read
off the source's own page or API on **2026-10-26**; where a store blocked automated reading, the row says
so instead of guessing. Re-read every licence at download time — store pages change, and a licence summary
is not a licence.

## The look we are aiming at, and what it implies

| Reference | What it actually is | What we take from it | What it costs to imitate |
| --- | --- | --- | --- |
| **Cloudpunk** | Voxel city at night, rain, neon, flying traffic; camera close to the street | Voxel or chunky low-poly city, wet reflective surfaces, strong fog and bloom, hand-placed neon signage | A voxel city kit or a very disciplined low-poly kit; post-processing does most of the mood |
| **Shadows of Doubt** | Fully voxel, procedurally furnished interiors, 1980s-analogue cyberpunk, first-person detective work | Voxel interiors the player can read at a glance; evidence as physical objects in rooms | Runtime voxel tooling plus a voxel authoring pipeline — the biggest technical commitment of the three |
| **Shadowrun: Dragonfall** | Isometric, turn-based, painted portraits, dense dialogue | Isometric framing, portraits for every speaker, tactical layer later | A 2D/3D isometric kit, portraits, and a combat rule set we have deliberately not built |
| **Disco Elysium** | Painted isometric backgrounds, expressive 2D portraits, dialogue as the whole game | Portraits carry characterisation; the world can be a *diorama* rather than an open city | Portrait art is the expensive part; backgrounds can be 3D rendered flat |
| **Citizen Sleeper** | 2D comic panels, dice as the action economy, very few moving parts | UI as the game surface; a die roll the player watches | UI kit + dice, cheap to make, cheap to localise |

**Conclusion (a recommendation, not a decision):** *voxel 3D seen through an isometric camera*. It is the
only option that satisfies Cloudpunk/Shadows of Doubt **and** keeps the existing Godot 3D slice — a
pixel-art 2D isometric pipeline would discard `src/godot/lakkahaltia_scene.gd` and every 3D node it builds,
and a low-poly non-voxel kit loses the specific Cloudpunk read.

## What the game actually needs

| Need | Why | Volume |
| --- | --- | --- |
| **Isometric / 2.5D modular interior and street kit** | one psychiatric-hospital case first (entrance, corridor, reception, consultation room), one street | small |
| **Voxel or low-poly retro character models** | 4–6 named NPCs plus the player, dialogue-facing | small |
| **UI kit for a dialogue-heavy game** | evidence board, journal, skill-check roll, branching choices — this is where the player spends the time | medium |
| **Ambient audio: hospital, street, rain, fluorescent hum** | tone is grounded-realism-with-uncanny, not action | small |
| **Fonts** | legible at 1080p, Finnish diacritics (ä, ö) — verify before committing to a font | tiny |

The gameplay reference is *Shadowrun: Dragonfall*'s isometric framing and *Disco Elysium* / *Citizen
Sleeper*'s dialogue density. That means **the UI and text system carry the game**, and the 3D kit can stay
deliberately simple.

## Free assets that are actually usable (verified)

### 3D — environments and props

| Pack | Source | Licence (as stated) | Formats | Fits |
| --- | --- | --- | --- | --- |
| **Industrial Cyberpunk 3D Tilepack** | <https://slipperhat.itch.io/industrial-cyberpunk-3d-tilepack> | **CC0**, "free for commercial use, no attribution required" | `.glb` + `.obj`, PBR, explicit Godot ORM workflow | 24 low-poly industrial tiles — the best-documented free cyberpunk kit for Godot. Industrial, not domestic: no hospital furniture |
| **Quaternius — Cyberpunk Game Kit** | <https://quaternius.com/packs/cyberpunkgamekit.html> | **CC0** | `.blend`, FBX, OBJ, glTF | neon street furniture, signs, terminals — closest free match to Cloudpunk's street layer |
| **Quaternius — Cube World Kit** | <https://quaternius.com/packs/cubeworldkit.html> | **CC0** | glTF/FBX/OBJ, cube-based | blocky/voxel-adjacent look without a voxel engine |
| **Quaternius — Downtown City Mega Kit / Buildings** | <https://quaternius.com/> | CC0 (same site-wide statement) | glTF/FBX/OBJ | city blocks, low-rise Helsinki massing |
| **Kenney — Mini Dungeon / Mini Forest / Tiny City**, **Furniture Kit**, **Space Kit**, **City Kit (Commercial / Suburban / Industrial / Roads)** | `https://kenney.nl/assets/<slug>` | **CC0** (each asset page states it) | glTF/OBJ | chunky readable props; hospital interiors, reception, wards, streets |
| **KayKit — Dungeon / Block Bits / Furniture Bits / City Builder Bits** | <https://kaylousberg.itch.io/kaykit-dungeon> · Godot Asset Library 2123 for City Builder Bits | **CC0** ("Creative Commons Zero") | FBX/glTF/OBJ | modular interiors; Block Bits is the voxel-flavoured one; City Builder Bits is a 32+ model street shell with a single gradient atlas |
| **Poly Haven** | <https://polyhaven.com/license> | **CC0 / public domain** | HDRIs, textures, some models | the single biggest mood win: night HDRIs, wet asphalt, frosted glass |
| **ambientCG** | <https://ambientcg.com/license> | **CC0** (site also lists MIT for its browser) | PBR textures | surfaces: lino, concrete, tile, snow |

### 2D and UI

| Pack | Source | Licence | Fits |
| --- | --- | --- | --- |
| **Kenney — UI Pack**, **Input Prompts**, **Crosshair Pack**, **Skyboxes** | `https://kenney.nl/assets/<slug>` | **CC0** | HUD, journal, evidence board, key prompts, night sky |
| **Kenney — RPG Urban Pack**, **Isometric Blocks**, **Isometric Miniature Dungeon** | `https://kenney.nl/assets/<slug>` | **CC0** | 2D isometric placeholders for a tactical layer, icons |
| **Cyberpunk Isometric Pixel Art Pack** | <https://crabcrabcrabs.itch.io/cyberpunk-isometric-city-pack> | "free for personal and commercial projects" — **not stated as CC0** | small isometric building set, 2D; *record the exact wording, ask before shipping* |

### Audio (CC0, verified)

| Pack | Source | Licence | Fits |
| --- | --- | --- | --- |
| **Kenney — RPG Audio**, **Interface Sounds**, **Digital Audio** | `https://kenney.nl/assets/rpg-audio` | **CC0** | UI clicks, doors, footsteps, ward ambience beds |
| OpenGameArt / Freesound | <https://opengameart.org/> · <https://freesound.org/> | **per item**: CC0 or CC-BY; some CC-BY-NC | hospital HVAC hum, fluorescent buzz, rain. Filter by licence, record it per file |

### Fonts

Google Fonts (<https://fonts.google.com/>) — every family on the site is OFL or Apache, but check the
family page. Shortlist that reads "Finnish bureaucracy meets cyberpunk": *Chakra Petch* (technical),
*Rajdhani* (condensed signage), *Space Grotesk* (neutral, modern), *IBM Plex Sans / Mono* (institutional
forms). **Check ä and ö before committing** — a UI font that mangles Finnish is unusable here.

### Godot-native tooling (not art, but it decides what art is cheap)

| Tool | Licence (verified via GitHub API, 2026-10-26) | Why |
| --- | --- | --- |
| **Zylann/godot_voxel** | **MIT**, ~3.9k stars, pushed 2026-10-01 | the realistic route to a Shadows of Doubt interior: runtime voxel meshes in Godot 4 |
| **nathanhoad/godot_dialogue_manager** | **MIT**, ~3.9k stars, pushed 2026-10-25 | dialogue as data; replaces the hand-rolled graph once one JSON file stops being enough |
| **dialogic-godot/dialogic** | **MIT**, ~6.1k stars, pushed 2026-08-30 | visual-novel authoring; weaker on game-state conditions |
| **ramokz/phantom-camera** | **MIT**, ~3.6k stars | Cinemachine-like camera work — exactly what an isometric/diorama camera needs |
| **bitwes/Gut** | licence not reported by the API | in-editor unit testing; optional, the slice already has a headless runner |
| **MagicaVoxel** | free, **not open source** | voxel authoring; exports `.obj`/`.glb` that Godot imports |

`godot_voxel` + MagicaVoxel is the whole Shadows-of-Doubt-shaped pipeline.

## Licence traps — read these before buying or downloading

1. **CC BY-ND forbids the modification a game needs.** `maxparata.itch.io/isometric-cyberpunk-streets` and
   `...-buildings` are **CC BY-ND 4.0** (*NoDerivatives*). They look perfect — 250+ and 130+ voxel-tagged
   sprites, Godot-friendly — but a game recolours, crops and re-poses its art, which ND does not permit.
   Treat them as references only.
2. **A store licence is not a repository licence.** Nothing purchased may be committed to this public
   repository; paid assets live outside git, referenced by the manifest — the same rule the Ubiquitous
   Maniacs corpus follows.
3. **"Free for personal and commercial use" is not a licence name.** If the terms do not say CC0 or an
   equivalent, record the exact wording and ask before shipping.
4. **Attribution is collected as you go**, not reconstructed later — see `docs/sources/GAME_SYSTEM_RIGHTS.md`
   and the release guard.
5. **Godot import reality:** `.glb`/`.gltf` is the safe format. Unity-first packs (Synty) may need material
   and animation rework; read Synty's own compatibility notes before paying.
6. **Do not mix pipelines.** A voxel corridor next to a low-poly ward reads as two different games.

## Paid, worth buying later (prices seen on the store page, EUR, Finland, 2026-10-26)

Synty's terms allow shipping assets inside a game but not redistributing the raw files (perpetual,
non-exclusive, royalty-free, **5 seats**), so **Synty packs can never be committed here**. KayKit and
Quaternius packs are CC0, so buying those is safe to commit.

| # | Pack | Store | Price seen | Commit-safe | What it buys us | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **KayKit Complete** | <https://kaylousberg.itch.io/kaykit-complete> | **€150.00** | **yes (CC0)** | the whole KayKit library incl. character animations | **buy first** |
| 2 | **POLYGON – Sci-Fi City Pack** | Synty | **€57.27** | no | neon city blocks for Cloudpunk-ish exteriors | high |
| 3 | **POLYGON – Sci-Fi Horror** | Synty | **€34.37** *(80 % off, regular €171.82)* | no | hospital corridors, flickering fixtures, "Riget" institutional dread — the closest thing to a hospital pack Synty sells | high, **while on sale** |
| 4 | **POLYGON – City Pack** | Synty | **€22.90** | no | ordinary Helsinki streets, cars, street furniture | medium |
| 5 | **POLYGON – Heist Pack** | Synty | **€34.36** | no | offices, banks, vaults — modern interiors that mix with the hospital | medium |
| 6 | **SIMPLE Office** / **SIMPLE House Interiors** | Synty | **€11.45** each | no | cheap cartoon furniture for greyboxing | low |
| 7 | **POLYGON – Sci-Fi Cyber City** | Synty | **€229.10** | no | the big neon city, if the exterior act becomes real | later |
| 8 | **Sci-Fi Civilians – Sidekick Modular Characters** | Synty | **€229.10** | no | modular people, if 3D characters replace 2D portraits | later |
| 9 | **POLYGON – Nightclubs** | Synty | **€114.55** | no | a bar/club location outside the ward | later |
| 10 | **Synty bundles via Humble Bundle / Fanatical** | various | historically ~€25 for a bundle; not verified today | no | best value if the art direction lands on Synty; bundles mix CC0 and proprietary — check each pack | watch |
| 11 | **SyntyPass** | <https://syntystore.com/> | price on the product page, **not verified** | no | a month of library access instead of buying packs | evaluate at art-pass time |

**Minimum viable art pass:** 1 + 2 + 3 + 4 = **≈ €264** (KayKit Complete, Sci-Fi City, Sci-Fi Horror on
sale, City Pack) — characters, interiors, hospital dread and a street, with the CC0 half committable and
the Synty half kept local.

**Portraits, if we go Disco Elysium-shaped:** no verified pack is recommended. Painted portraits are the
one thing that must be commissioned or made in-house; a stock pack reads as stock. Budget for an artist,
not a store.

## Recommended order (no purchase until step 3 passes)

1. **Free, this milestone.** Import Kenney Furniture Kit + Quaternius Cyberpunk Game Kit +
   slipperhat's Industrial Cyberpunk Tilepack, replace the primitive ward geometry, record every file in
   `data/assets/manifest.json`. Zero cost, all CC0.
2. **Prove the camera and the mood.** Add `phantom-camera`, then tune fog, bloom and wet-floor reflections
   against a Poly Haven night HDRI. The reference look lives here, not in polycount. If it does not read as
   Cloudpunk at this step, no purchase will fix it.
3. **Then buy KayKit Complete (€150, CC0, committable)** and **Sci-Fi Horror while it is 80 % off**, kept in
   a git-ignored `godot/assets_private/` with acquisition notes.
4. **Voxel is a separate decision.** If Shadows of Doubt is the target, prototype `godot_voxel` +
   MagicaVoxel on one corridor **before** buying any non-voxel kit, because the pipelines do not mix.
5. **Portraits last**, commissioned, once the case's cast is fixed.

## Licence checklist for anything that enters the repository

1. Read the pack's own licence file, not a marketplace summary.
2. Record: pack, URL, licence, date verified, verifier, files added.
3. CC0 or a permissive licence that allows redistribution → may be committed. **"Use in a game only" terms
   → never commit**; keep local and document acquisition.
4. Attribution, if required, goes in the credits screen *and* the manifest.
5. Keep `.import` files for anything shipped, so the build reproduces.
6. No assets ripped from a published game, and none whose AI-training provenance is unclear.

The machine-readable version of this list lives in `data/assets/manifest.json`.
