# Issue #966: Evennia phase-1 continuation

## Implemented in this increment

- `mud/nopunk_mud/solo_resolver.py` connects the pure `solo_arc` injected callback to `cwn_core.skill_check` using published CWN 2d6 resolution, attribute modifiers, rank and explicit difficulty bands.
- Explicit-dice tests demonstrate success, failure consequences and recovery to an ending without an LLM or Evennia server.
- This is **not** a claim that `solo_arc` is yet mounted as an Evennia command. The separate `solo` command runs `CampaignEngine`, a different self-contained case. Do not conflate the two.

## GUMSHOE licence decision

Two *different* publisher documents exist, rather than contradictory licenses for one PDF:
- **OGL version (selected by #932):** https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf ; 68 pages; first page declares OGL 1.0 and excludes listed game-line trademarks as Product Identity. No permission for logo.
- **CC BY 3.0 version (earlier #704):** the publisher also released separate CC editions; the 303-page v3 file is recorded in `data/sources/game_system_rights.json` for historical #704 material.

**Policy:** new #932-derived content must use the specified OGL edition, with its own license notices / Product Identity exclusions if redistributing SRD Open Game Content. Existing original investigative mechanics need not be recopied. Do not import OGL prose without completing OGL compliance review. Do not relicense the OGL PDF as CC BY, or silently treat CC content as OGL.

## Remains unfinished

- Install and boot the Evennia server, verify its client and persistent restart behavior.
- Wire a character-creation/sheet bridge and the `solo_arc` resolver into a user-facing Evennia scenario if that arc is retained; reconcile duplicated case interfaces.
- Combat, hacking, Helsinki travel data, inventory, economy, companions, campaign and side quests.
- Preserve **UNSA/UNHA** and **Pleyadian/Pleiadian** as unresolved authorial naming decisions; do not silently canonize a choice.
- Art remains human authored per #966.
