# NoöPunk images and Godot art direction

**Authority:** [issue #908](https://github.com/TomiToivio/NooPunk/issues/908) and [foundational issue #897](https://github.com/TomiToivio/NooPunk/issues/897).

## Visual contract

The approved Romppainen Helsinki street illustration is the baseline: **1970s European science-fiction comic art**, crisp expressive ink lines, hand-colored shaded blocks, warm ochre/rust/olive accents, dusty Nordic blue and subdued painterly grain. Mœbius-era bande dessinée is a *reference*, not a request to trace or reproduce specific copyrighted panels.

Helsinki should look **recognizably everyday**. Early locations show ordinary streets, trams, newsstands, institutional offices, modest period furnishings, rainy pavements and believable people. Do **not** add flying saucers, hovering cars, cosmic skylines, neon cyberpunk, elaborate robot parts or sci-fi landmarks unless the user specifically asks or the depicted story event requires them. Technology is optional and understated: analog controls, 1970s imagined future materials, and discreet **standard BCI only** for Romppainen.

## Asset taxonomy

| Category | Repo path / Godot path | Subject | Preferred composition |
| --- | --- | --- | --- |
| Character sheets | `images/characters/portraits/` / `res://images/characters/portraits/` | Character standing or posed, consistent recognizable look | 3:4 or 2:3 portrait |
| Social encounters | `images/social_encounters/` | NPCs in conversations and situations, including rookie welcome | 4:3 or 16:9 |
| Locations | `images/locations/` | Interiors, Helsinki streets, neighborhood and mission views | 16:9 |
| Events | `images/events/` | Clues, action, combat, narrative and anomaly moments | 16:9 or 4:3 |

Keep text out of generated art when possible, and overlay typography / dialogue through Godot. Separate real-photo reference material from publicly committed art.

## Character lock: Inspector Dr. Harri Romppainen

Short, stocky, middle-aged, dark curly seventies haircut and moustache, perceptive **green eyes** visible behind clear metal-framed eyeglasses, eccentric psychologically penetrating smile and poised psychedelic-intellectual energy. Weathered detective coat, patterned collar, seventies radical intellectual sensibility, optional cigarette. *Not* mirrored sunglasses. Use one minimal standard retro BCI when visible. The approved **Helsinki street-corner** illustration (the most recent user-approved image) is the canonical character-sheet pose; preserve recognizable facial proportions and outfit across scenes. An office welcome for the new UNSA rookie belongs in `social_encounters` and should be more everyday than overtly science fictional.

Tommy Pilgrim is a distinct character, not an alternative label or model for Romppainen.

## Naming and imports

- Use lowercase snake_case, unique stable asset ids, PNG or good-quality WebP files, and retain non-destructive original art masters outside the runtime image tree if needed.
- Suggested canonical file: `images/characters/portraits/harri_romppainen_helsinki_street.png`.
- Provide metadata in `images/manifest.json`: id, category, path, description, source/provenance, approval, license, dimensions, and narrative location.
- In Godot 4: `const PORTRAIT = preload("res://images/characters/portraits/harri_romppainen_helsinki_street.png")` after the image binary exists. Set `TextureRect.texture = PORTRAIT`; use `expand_mode = TextureRect.EXPAND_IGNORE_SIZE`, `stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED` or `STRETCH_KEEP_ASPECT_COVERED` as the layout requires. Test crop and safe-area behavior; never cut off eyes or smiles.
- Treat the PNG reference path as **pending** until the file is uploaded, verified and added to the manifest; do not introduce a failing `preload()` prematurely.

## Review checklist

1. Correct visual category and actual story place.
2. Same recurring character face and wardrobe, piercing eyes and signature expression.
3. Normal Helsinki first, extraordinary content only with narrative justification.
4. No generic 1980s cyberpunk/glossy neon.
5. Valid licensing/provenance and actual file in Git.
6. Godot imports and layout verified at different aspect ratios.
