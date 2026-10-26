# Art and audio assets for the NoöPunk detective RPG (#631)

**Status: research note. No asset is approved, imported or purchased.** Licences below are what each
source states about itself on 2026-10-26; every one must be re-read at download time, because store pages
change and a licence summary is not a licence.

## What the game actually needs

| Need | Why | Volume |
|---|---|---|
| **Isometric / 2.5D modular interior and street kit** | one psychiatric-hospital case first (entrance, corridor, reception, consultation room), one street | small |
| **Voxel or low-poly retro character models** | 4–6 named NPCs plus the player, dialogue-facing | small |
| **UI kit for a dialogue-heavy game** | evidence board, journal, skill-check roll, branching choices — this is where the player spends the time | medium |
| **Ambient audio: hospital, street, rain, fluorescent hum** | tone is grounded-realism-with-uncanny, not action | small |
| **Fonts** | legible at 1080p, Finnish diacritics (ä, ö) — verify before committing to a font | tiny |

The gameplay reference is *Shadowrun: Dragonfall*'s isometric framing and *Disco Elysium* / *Citizen
Sleeper*'s dialogue density. That means **the UI and text system carry the game**, and the 3D kit can stay
deliberately simple.

## Free / open — verified this pass

| Asset | Licence (as stated) | Good for | Caveat |
|---|---|---|---|
| **Industrial Cyberpunk 3D Tilepack** — `slipperhat.itch.io/industrial-cyberpunk-3d-tilepack` | **CC0**, "free for commercial use, no attribution required" | 24 low-poly tiles, **.GLB + .OBJ with PBR**, explicit Godot ORM workflow | industrial, not domestic; no hospital furniture |
| **KayKit City Builder Bits** — Godot Asset Library asset 2123 | **CC0** | 32+ low-poly city models, single gradient atlas, mobile-friendly | stylised, not cyberpunk; good for the street shell |
| **Cyberpunk Isometric Pixel Art Pack** — `crabcrabcrabs.itch.io/cyberpunk-isometric-city-pack` | "free for personal and commercial projects" — **not stated as CC0** | small isometric building set, 2D | licence wording is vaguer than CC0; treat as *verify before shipping* |
| **MagicaVoxel** (tool, not assets) | free | building the Shadows-of-Doubt-style voxel look yourself | you must author the models |

**Avoid as a base:** `maxparata.itch.io/isometric-cyberpunk-streets` and `-buildings` are **CC BY-ND 4.0** —
*NoDerivatives*. They are attractive (250+ and 130+ sprites, voxel-tagged, Godot-friendly), but a game
requires editing, recolouring and re-posing sprites, which ND does not permit. Usable only as untouched
whole-sprite references, which is not how a game kit is used.

## Paid — to consider later, not now

| Asset | Price seen | Licence model | Note |
|---|---|---|---|
| **Synty POLYGON** line (e.g. *Prison Map* $29.99; *Palm City* $299.99) | per pack | One Time Purchase: perpetual, non-exclusive, royalty-free, worldwide, **5 seats** | **Godot caveat:** reviewers report extra work needed to use the animations; Synty's own compatibility notes are the thing to read before buying. Unity-first pipeline. |
| **Synty bundles via Humble Bundle** | historically ~$25 for the whole bundle | same licence | best value if the art direction lands on Synty; watch for expiry |
| **Humble / Fanatical gamedev bundles** | varies | varies per bundle | check each pack's licence individually — bundles mix CC0 and proprietary |

**Do not buy anything yet.** The art direction question — pixel-art isometric (2D) vs voxel (3D) vs
low-poly 3D — is unresolved, and the three have incompatible pipelines. Buying before that decision is
how a project ends up with a paid pack it never uses.

## Licence traps to keep in mind

1. **CC BY-ND forbids the modification a game needs.** Prefer CC0 wherever possible.
2. **A store licence is not a repository licence.** Nothing purchased may be committed to NoöPunk's public
   repository; paid assets live outside git, referenced by a manifest (the same rule the Ubiquitous Maniacs
   corpus follows).
3. **"Free for personal and commercial use" is not a licence name.** If the terms do not name CC0 or an
   equivalent, record the exact wording and ask before shipping.
4. **Attribution obligations must be collected as you go**, not reconstructed later — the repo already has
   `docs/sources/GAME_SYSTEM_RIGHTS.md` and a release guard for this reason.
5. **Godot import reality:** .GLB/.glTF is the safe format; Unity-first packs (Synty) may need material and
   animation rework.

## Recommended first step (no purchase)

Build the vertical slice with **CC0 only**: the slipperhat tilepack for structure, KayKit for the street
shell, and MagicaVoxel for the few props the hospital case needs. That proves the gameplay loop without
committing to an art pipeline. Revisit the paid list only after the slice is playable and the art
direction is chosen.
