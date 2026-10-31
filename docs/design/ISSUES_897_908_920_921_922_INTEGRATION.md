# NoöPunk cross-issue implementation map

This document coordinates #897 (foundational CWN/UI/art lock), #908 (Godot image library), #920 (UNSA field party), #921 (Crisis history), and #922 (NHI/human factions).

## Precedence and non-negotiables
- CWN is the **permanent core rules baseline**; SWN/WWN may extend it selectively. Narrative and psyche/ideology/faction systems are optional overlays, not alternate resolution engines. Historical documents describing earlier Fate or 1d10 decisions are a record, not an invitation to restore those baselines.
- Default art is **1970s European SF comic illustration**, recognizably mundane Helsinki, with anomalies only at authored moments. See [art lock](../ART_DIRECTION.md), [image pipeline](../ART_DIRECTION_IMAGES.md), [art bible](../art/ART_BIBLE_1974.md).
- Main UI is location-driven investigative narrative, not the legacy tactical top-down map.
- Tony German is the rookie PC; Laura is the usual optional partner; Romppainen is a recurring senior specialist, not a default party slot.

## Existing infrastructure, avoid duplicating
- `FACTIONS.md` contains the author's extensive NHI account; do not overwrite it with a simplified taxonomy.
- `images/manifest.json`, `godot/core/image_library.gd`, `docs/ART_DIRECTION_IMAGES.md` already establish image handling. The approved Romppainen portrait remains **pending binary**, not a loaded resource.
- `docs/CWN_CHASSIS.md`, CWN coverage and Godot implementation notes record historical decisions and partial implementations. Confirm runtime parity before marking the baseline fully implemented.

## Follow-on runtime contracts (not falsely claimed complete)
### Party and authorization (#920)
- Active party count: 1–4 **including Tony**. Default solo or Tony+Laura; temporary Romppainen, hacker or prescripted psionic asset subject to authorization and availability.
- Remote human controller and narrow AI assistant **never** consume party slots; operational decisions require a named human approver, log and authority.
- Record companion state, loyalty/trust, available missions, leave/rejoin reasons and save migrations. Refuse a fifth active member.
- Only designated authorized NPC assets trigger **scripted active PSI**; the PC's implant provides passive protection / limited ESP, not an active power tree.
- Supo/Europol/UNSA jurisdiction is an explicit source of permission checks, contradictory orders and consequences.
- Test 1, 2, 3 and 4 slots; fifth-member rejection; save/load; no approval → no AI actions; nonasset → no active PSI.

### Investigation and faction persistence (#897/#922)
- Persist discovered map nodes, active leads, clue evidence/provenance, interviews, faction reputation, relationship flags, party membership and noetic state.
- Keep NHI allegiance *alleged until established*; do not equate being a biologic, Noetic or Construct with membership in a given bloc.
- Make critical clues obtainable without one mandatory successful roll; standard CWN handles non-core actions and combat.
- [UNSA human faction design](../world/UNSA_HUMAN_PROXY_FACTIONS.md) defines the requested social gameplay layer.

### Crisis history (#921)
- Use [historian's memorandum](../world/NHI_CRISIS_HISTORIAN_MEMORANDUM.md); reconcile relative chronology with the existing canonical timeline before writing dates.
- Preserve separate public facts, contested interpretations and classified unknowns, including the distinction between evident NHI presence and **official contact after Singularity onset**.

### Image pipeline (#908)
- Four types are portraits, social encounters, locations and events. Load only actually committed and manifest-registered assets via `res://images/`.
- Missing portraits use explicit placeholders; do not claim the approved portrait has been imported.
- Test Godot import, aspect ratio and content review when actual art is available.

## Delivery tracking
| Issue | Established now | Still required |
|---|---|---|
| #897 | Baseline decisions and architectural crosswalk | Verified full CWN parity and complete narrative vertical slice |
| #908 | Art direction/pipeline present | Approved binary art, screen validation and import tests |
| #920 | Party and authority contract documented | Godot recruit/save/UI/AI-approval/PSI implementations and tests |
| #921 | Six-phase historian overview and hooks | Reconcile exact canonical timeline and runtime archives |
| #922 | Existing NHI lore and human-proxy investigation design | Typed runtime faction relations, evidence and reputation tests |

Do not close an issue merely because a planning document was added.
