# Godot slice #631 — current status

The playable ward from #633 is the active implementation. See
[run instructions and controls](../GODOT.md). The initial #632 adapter-only gate
is superseded: Godot 4.5.1 was installed and a clean checkout was run headlessly.

A follow-up audit found #633 used the retired d10 adapter despite the current
author override. The active scene now uses the existing Without Number adapter,
standard attributes and 2d6 checks. Character, position and once-per-case check
results persist in version-2 saves; incompatible legacy saves are rejected.

Checked root `AGENTS.md`, current baseline, design principles, #564 timeline,
#615 and #626. No nested instructions apply. No private/external NoöPunk-specific
skill file was available to update. Tests cover executable behavior only.

The concurrent alternative implementation in #636 was closed to preserve one
active Godot game. Legacy runtimes remain intact. No new asset pack was added;
the original primitive-geometry manifest remains applicable.

Headless checks cover game logic, both endings, persistence, ward load and actual
interaction calls. Desktop visual playtest and duration remain outstanding.
Follow-ons: licensed art and pacing, CWN hacking/cybernetics, SWN PSI, tactical
missions, then global strategy. WWN/AWN modules activate when the scenario needs them.
