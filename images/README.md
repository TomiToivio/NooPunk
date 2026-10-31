# NoöPunk Godot image library

This directory is located at Godot's project root (`project.godot`), so runtime references use `res://images/...`.

- `characters/portraits/` — character-sheet poses and portraits
- `social_encounters/` — interactions, dialogue and character moments
- `locations/` — surroundings and interiors
- `events/` — story beats, random events, combat and anomalies

**Read [image art direction](../docs/ART_DIRECTION_IMAGES.md) and [issue #908](https://github.com/TomiToivio/NooPunk/issues/908) before generating/importing art.**

The approved Romppainen street portrait belongs at `characters/portraits/harri_romppainen_helsinki_street.png`. The binary is not included until it is actually transferred and verified. Do not assume a path in the metadata exists before checking it.

## Enforced by tooling

| Rule | Where it is enforced |
| --- | --- |
| every asset is described in `manifest.json` | `tools/check_image_manifest.py`, `tests/test_image_manifest_908.py` |
| ids unique, filenames `lowercase_snake_case` | same |
| a file lives in the directory its category names | same |
| declared dimensions match the actual file | same |
| **sci-fi motifs only on `events`, and only with a justification** | same |
| provenance recorded for anything committed | same |

Screens reference assets **by id** through `godot/ui/image_library.gd`, never by a raw
`res://images/...` path. Layout geometry lives in `godot/ui/image_layout.gd`.

Adding an asset: name it `lowercase_snake_case`, put it in its category directory, add a manifest entry with
real dimensions, run `python3 tools/check_image_manifest.py`, then look at it in Godot at 1280x720 before
declaring it done.
